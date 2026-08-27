import csv
import os

ARQUIVO_CSV = "livros.csv"

CAMPOS = ["titulo", "autor", "ano", "isbn", "status"]

def carregar_livros():

    lista_livros = []

    if not os.path.exists(ARQUIVO_CSV):
        return lista_livros

    with open(ARQUIVO_CSV, mode="r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            lista_livros.append(linha)

    return lista_livros


livros = carregar_livros()

def cadastrar_livro(lista_livros, titulo, autor, ano, isbn):

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "isbn": isbn,
        "status": "disponivel"
    }

    lista_livros.append(novo_livro)

    return lista_livros

def listar_livros(lista_livros):

    if not lista_livros:
        print("Nenhum livro cadastrado.\n")
        return

    for livro in lista_livros:
        print(f"Título: {livro['titulo']}")
        print(f"Autor : {livro['autor']}")
        print(f"Ano   : {livro['ano']}")
        print(f"ISBN  : {livro['isbn']}")
        print(f"Status: {livro['status']}\n")

    print(f"Total de livros: {len(lista_livros)}\n")

def buscar_livros(lista_livros, termo, campo):
    
    if campo not in ("titulo", "autor"):
        return []
    termo = termo.lower()
    resultado = []

    for livro in lista_livros:
        if termo in livro[campo].lower():
            resultado.append(livro)
    return resultado

def emprestar_livro(lista_livros, isbn):

    for livro in lista_livros:
        if livro["isbn"] == isbn:

            if livro["status"] == "emprestado":
                return "Este livro já está emprestado."

            livro["status"] = "emprestado"
            return "Empréstimo registrado com sucesso."

    return "Livro não encontrado."


def devolver_livro(lista_livros, isbn):

    for livro in lista_livros:
        if livro["isbn"] == isbn:

            if livro["status"] == "disponivel":
                return "Este livro já está disponível."

            livro["status"] = "disponivel"
            return "Devolução registrada com sucesso."

    return "Livro não encontrado."

def ordenar_livros(lista_livros, campo):
    if campo not in ("titulo", "autor", "ano"):
        return lista_livros

    if campo == "ano":
        return sorted(lista_livros, key=lambda livro: int(livro[campo]))

    return sorted(lista_livros, key=lambda livro: livro[campo].lower())

def salvar_livros(lista_livros):
    with open(ARQUIVO_CSV, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)

        escritor.writeheader()

        for livro in lista_livros:
            escritor.writerow(livro)

def exibir_menu():
    print("1. Cadastrar livro")
    print("2. Listar todos os livros")
    print("3. Buscar algum livro")
    print("4. Ordenar alguns livros")
    print("5. Emprestar algum livro")
    print("6. Devolver algum livro")
    print("7. Status")
    print("0. Sair")

def main():
    print("\nBem-vindo ao Sistema de Gerenciamento de Biblioteca!")

    while True:
        exibir_menu()

        opcao = input("\nEscolha uma opção: ").strip()
        if opcao == "1":

            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            ano = input("Ano: ").strip()
            isbn = input("ISBN: ").strip()

            if not titulo or not autor:
                print("Título e autor não podem ficar em branco!")
                print("Por favor, tente novamente.")
                continue

            if not ano.isdigit():
                print("Ano precisa ser um número!")
                print("Por favor, tente novamente.")
                continue

            if len(ano) != 4:
                print("Ano deve ter 4 dígitos!")
                print("Por favor, tente novamente.")
                continue

            if not isbn:
                print("ISBN não pode ficar em branco!")
                print("Por favor, tente novamente.")
                continue

            print(f"\nConfirme os dados: "
                f"Título: {titulo}\n"
                f"Autor: {autor}\n"
                f"Ano: {ano}\n"
                f"ISBN: {isbn}")

            confirmacao = input("Cadastrar esse livro?: ").strip().lower()

            if confirmacao == "s":
                cadastrar_livro(livros, titulo, autor, ano, isbn)
                salvar_livros(livros)
                print("Parabéns! Livro cadastrado com sucesso!")

            else:
                print("Cadastro cancelado.")
                
        elif opcao == "2":
            listar_livros(livros)

        elif opcao == "3":

            campo = input("Buscar por (titulo/autor): ").strip().lower()

            termo = input("Digite o termo de busca: ").strip()

            encontrados = buscar_livros(livros, termo, campo)

            if not encontrados:
                print("\nNenhum livro encontrado com esse termo!")

            else:
                print(f"\nLivros encontrados ({len(encontrados)}):")

                listar_livros(encontrados)
        elif opcao == "4":

            campo = input("Ordenar por (titulo/autor/ano): ").strip().lower()

            if campo not in ("titulo", "autor", "ano"):
                print("Campo inválido!")
                print("Escolha entre titulo, autor ou ano.")
                continue

            ordenados = ordenar_livros(livros, campo)
            listar_livros(ordenados)
        elif opcao == "5":

            isbn = input("ISBN do livro a emprestar: ").strip()

            if not isbn:
                print("ISBN não pode ficar em branco!")
                print("Por favor, tente novamente.")
                continue

            if not isbn.isdigit():
                print("ISBN precisa ser um número!")
                print("Por favor, tente novamente.")
                continue

            mensagem = emprestar_livro(livros, isbn)
            salvar_livros(livros)
            print(mensagem)

        elif opcao == "6":

            isbn = input("ISBN do livro a devolver: ").strip()

            if not isbn:
                print("ISBN não pode ficar em branco!")
                print("Por favor, tente novamente.")
                continue

            if not isbn.isdigit():
                print("ISBN precisa ser um número!")
                print("Por favor, tente novamente.")
                continue

            mensagem = devolver_livro(livros,isbn)
            salvar_livros(livros)
            print(mensagem)

        elif opcao == "7":
            print(f"\nTotal de livros: {len(livros)}")
            disponiveis = 0
            emprestados = 0
            for livro in livros:
                if livro["status"] == "disponivel":
                    disponiveis += 1

        elif livro["status"] == "emprestado":
            emprestados += 1
            print(f"Livros disponíveis: {disponiveis}")
            print(f"Livros emprestados: {emprestados}\n")
        elif opcao == "0":

            confirmacao = input("Tem certeza que deseja sair?: ").strip().lower()

            if confirmacao != "s":
                print("Retornando ao menu principal.")
                continue

            print("Encerrando o sistema.""Obrigado por utilizar! Até logo!")

            break
        else:
            print("Opção inválida. Tente novamente!")
main()
