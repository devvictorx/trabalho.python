import re
import requests
from bs4 import BeautifulSoup

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2

def validar_email(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.fullmatch(padrao, email))

def validar_telefone(telefone):
    padrao = r"^\(\d{2}\)\s?\d{4,5}-\d{4}$"
    return bool(re.fullmatch(padrao, telefone))

def coletar_dados():
    dados = {}
    while True:
        nome = input("Nome: ").strip()
        if nome.replace(" ", "").isalpha() and len(nome) > 1:
            dados["nome"] = nome
            break
        else:
            print("Nome inválido. Por favor, insira um nome válido.")
    while True:
        cpf = input("CPF (somente números ou com pontos e traços): ")
        if validar_cpf(cpf):
            dados["cpf"] = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            break
        else:
            print("CPF inválido. Por favor, tente novamente.")
    while True:
        email = input("Email: ").strip()
        if validar_email(email):
            dados["email"] = email
            break
        else:
            print("Email inválido. Por favor, tente novamente.")
    while True:
        telefone = input("Telefone (formato (XX) XXXX-XXXX ou (XX) XXXXX-XXXX): ").strip()
        if validar_telefone(telefone):
            dados["telefone"] = telefone
            break
        else:
            print("Telefone inválido. Por favor, tente novamente.")
    return dados

def consultar_preco_teclado():
    url = 'https://www.magazineluiza.com.br/busca/teclado-yamaha-psr-e473/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro ao acessar o site. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    produto = soup.find('h1', class_='product-title')
    preco_elementos = soup.find_all('span', class_='price')
    
    if produto and preco_elementos:
        nome_produto = produto.text.strip()
        precos = [float(preco.text.strip().replace('R$', '').replace('.', '').replace(',', '.')) for preco in preco_elementos]
        menor_preco = min(precos) if precos else None
        link_oferta = soup.find('a', class_='product-link')['href'] if soup.find('a', class_='product-link') else ''
        return nome_produto, menor_preco, link_oferta
    else:
        print("Produto ou preço não encontrado na página.")
        return None

def exibir_resultados(dados_produto):
    if dados_produto:
        nome_produto, menor_preco, link_oferta = dados_produto
        print(f"Produto: {nome_produto}")
        print(f"Menor preço: R${menor_preco:.2f}")
        print(f"Link da oferta: {link_oferta}")
    else:
        print("Não foi possível obter as informações do produto.")

def main():
    dados_usuario = coletar_dados()
    print("\nDados coletados:")
    for chave, valor in dados_usuario.items():
        print(f"{chave.capitalize()}: {valor}")
    dados_produto = consultar_preco_teclado()
    exibir_resultados(dados_produto)

if __name__ == "__main__":
    main()
