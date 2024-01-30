import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import re
from ConexaoBaseDados import salvar_produtos

def main():

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.headless = False

    # Abrirá o Chrome maximizado
    chromeOptions.add_argument('--start-maximized')

    # Inicia o Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)

    # Navegar até o site
    driver.get("https://store.vivo.com.br/")

    # Realizar a pesquisa
    botao_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/custom-storefront/header/cx-page-layout[1]/cx-page-slot[6]/custom-searchbox/div/button'))).click()

    # Aguardar a caixa de busca ficar visível
    search_box = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inputSearch"]')))

    # Utilizando pyautogui para enviar o texto diretamente
    search_box.click()
    pg.typewrite("Apple")
    pg.press("enter")

    botao_pop_up = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="consent"]/span'))).click()

    botao_ordernar = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sortingSelect-button"]'))).click()

    preco_maior_primeiro = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sortingSelect"]/ul/li[5]'))).click()

    time.sleep(5)

    container_produtos = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[2]'))).text

    padrao = re.compile(r'(Últimas Peças)?\n(?!.*Poxa, esse produto acabou)(.*?)Por\s*(R\$\s*[\d.,]+)\s*Frete Grátis', re.DOTALL)

    # Procura pelo padrão no texto
    correspondencia = padrao.search(container_produtos)

    if correspondencia:
        ultimas_pecas = correspondencia.group(1) if correspondencia.group(1) else ""
        dados_produto = correspondencia.group(2).strip()
        preco_produto = correspondencia.group(3).strip()

    elemento_produto = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[2]'))
    )

    elemento_produto.click()

    time.sleep(5)
    # Aguardar a caixa de busca ficar visível
    search_box = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="postalCode"]')))

    time.sleep(3)
    # Utilizando pyautogui para enviar o texto diretamente
    search_box.click()
    pg.typewrite("87430000")

    time.sleep(2)
    botao_confirmar_cep = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="applyPostalCode"]'
    ))).click()

    time.sleep(5)
    prazo_entrega = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
        By.XPATH, '/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[1]/product-delivery-time/div/div/div/div/span[1]'
    ))).text

    prazo_entrega = prazo_entrega[:16]

    criar_pdf(ultimas_pecas, dados_produto, preco_produto, prazo_entrega)

    url_pagina_inicial = 'https://store.vivo.com.br/apple/busca?sortCode=pricePriority-desc'

    pegar_50_primeiros_itens(url_pagina_inicial, driver)

    input('Pressione a tecla enter para fechar o chrome')

def criar_pdf(ultimas_pecas, dados_produto, preco_produto, prazo_entrega):

    # Criação do arquivo PDF
    pdf = canvas.Canvas('informacoes_produtos.pdf', pagesize=letter)

    # Adiciona informações ao PDF
    pdf.drawString(15, 750, "Informações do Produto:")
    pdf.drawString(15, 730, f"Últimas Peças: {ultimas_pecas}")
    pdf.drawString(15, 710, f"Descrição do Produto: {dados_produto}")
    pdf.drawString(15, 690, f"Preço do Produto: {preco_produto}")
    pdf.drawString(15, 670, "Informações de Entrega:")
    pdf.drawString(15, 650, f"Prazo de Entrega para CEP 87430-000: {prazo_entrega}")

    # Salva o arquivo PDF
    pdf.save()

def pegar_50_primeiros_itens(url_pagina_inicial, driver):

    driver.get(url_pagina_inicial)

    todos_produtos = []

    contagem_itens = 0

    max_itens = 50

    # Loop para iterar sobre as páginas
    for pagina in range(1, 10):

        time.sleep(5)

        container_produtos = driver.find_element(By.XPATH, '/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[2]/div').text
        padrao = re.compile(r'(Últimas Peças)?\n(?!.*Poxa, esse produto acabou)(.*?)Por\s*(R\$\s*[\d.,]+)\s*Frete Grátis', re.DOTALL)
        correspondencias = padrao.findall(container_produtos)

        # Verifica se ultrapassou o número máximo da quantidade de itens desejados
        itens_restantes = max_itens - contagem_itens
        if itens_restantes <= 0:
            break

        # Limita a quantidade de itens add
        correspondencias = correspondencias[:itens_restantes]

        todos_produtos.extend(correspondencias)

        contagem_itens += len(correspondencias)

        try:
            next_page_button = driver.find_element(By.XPATH, '/html/body/app-root/custom-storefront/main/cx-page-layout/cx-page-slot[2]/cx-product-list/div/section/div/div/div/div[3]/div/div/div/cx-pagination/a[5]')
            next_page_button.click()
        except Exception as e:
            print(f"Erro ao clicar no botão da próxima página: {e}")
            break

    # Fecha o WebDriver
    driver.quit()

    itens_produtos = []

    for produto in todos_produtos:
        ultimas_pecas = 1 if "Últimas Peças" in produto[1] else 0

        matches_parcela = re.search(r"(\d+)x de R\$\s*([\d.,]+)", produto[1])
        parcelas = int(matches_parcela.group(1)) if matches_parcela else 0
        valor_parcela = matches_parcela.group(2) if matches_parcela else ""

        modelo_match = re.search(r"Apple iPhone \d+ [\w\s]+", produto[1])
        modelo = modelo_match.group() if modelo_match else ""
        modelo = modelo[:20]

        capacidade_match = re.search(r"(\d+[GT]B\b)", produto[1])
        capacidade = capacidade_match.group(1) if capacidade_match else ""

        cor_match = re.search(r"B\s*([A-Z][a-z]+)\s*5G", produto[1])
        cor = cor_match.group(1) if cor_match else ""

        tamanho_tela_match = re.search(r"Tela (\d+,\d+\")", produto[1])
        tamanho_tela = tamanho_tela_match.group(1) if tamanho_tela_match else ""

        preco_produto = produto[2].replace("R$", '').strip()

        itens_produtos.append({
            'modelo': modelo,
            'capacidade': capacidade,
            'tamanho_da_tela': tamanho_tela,
            'preco_total': preco_produto,
            'valor_parcela': valor_parcela,
            'quantidade_parcela': parcelas,
            'cor': cor,
            'ultimas_pecas': ultimas_pecas
        })
    
    salvar_produtos(itens_produtos)

if __name__ == '__main__':
    main()