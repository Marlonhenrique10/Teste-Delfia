from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from datetime import datetime
from ConexaoBaseDados import inserir_dados_voo

def main():

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.headless = False

    # Abrirá o Chrome maximizado
    chromeOptions.add_argument('--start-maximized')

    # Inicia o Chrome
    iniciarChrome = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)

    try:

        funcao_cvc(iniciarChrome)
        # funcao_decolar(iniciarChrome)

    finally:
        print('terminou...')
        ...
        # Fechar o Chrome
        iniciarChrome.quit()

def funcao_cvc(iniciarChrome):

    try:

        dados_voo = []

        camp_ida = "São Paulo"

        camp_destino = "Rio de Janeiro"

        empresa = "cvc"

        # Abrira o site da cvc
        iniciarChrome.get('https://www.cvc.com.br/')

        # Campo de imbarq de ida
        WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div[1]')))\
            .click()
        
        # Campo para digitar a cidade que vai embarcar
        WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div[2]/div[1]/div/input')))\
            .send_keys(camp_ida)
        
        # Campo de onde vai sair (São Paulo, São Paulo)
        WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]/div/div[2]/div[2]/nav/div[1]/div[2]/span[1]')))\
            .click()
        
        # Campo para digitar o destino
        WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[2]/div/div[2]/div[1]/div/input')))\
            .send_keys(camp_destino)
        
        # Campo do destino (Rio de Janeiro, Rio de Janeiro)
        WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[2]/div/div[2]/div[2]/nav/div[1]/div[1]/span[1]')))\
            .click()

        iframe = iniciarChrome.find_element(By.XPATH, '/html/body/iframe[2]')

        # Mudar o foco do WebDriverWait para o iframe
        iniciarChrome.switch_to.frame(iframe)

        # Fechar anuncio
        WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div[1]/div/div/button'))).click()

        # Voltar ao contexto padrão
        iniciarChrome.switch_to.default_content()

        # Campo do mês e ano (ex: Janeiro 2024)
        camp_mes = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div')))\
            .text

        # Loop até achar o mês de novembro na tela da data
        while camp_mes != 'Novembro 2024':

            # Estou pegando o valor do mês para saber em qual mês está
            camp_mes = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div')))\
                .text

            # Campo para selecionar a data
            WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/div/div[2]/div[1]/div[2]')))\
                .click()

            # Quando o mês for novembro, ele add a data da ida e da volta e encerra o código
            if camp_mes == 'Novembro 2024':

                # Campo para add a data início
                WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[1]/td[6]')))\
                    .click()
                
                # Campo para add a data final
                WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[2]/td[2]')))\
                    .click()

                # Botão de selecionar e confirmar a data
                WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/div/div[3]/div[2]/button')))\
                    .click()

                break

            time.sleep(1)

        # Botão para selecionar a quantidade de adulto (Estou marcando 1)
        WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[3]/div[2]/div/div/ul/li[2]/ul/li[1]/div/button[1]')))\
            .click()
        
        # Botão para selecionar e confirmar a quantidade de pessoa para a passagem
        WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[3]/div[2]/div/div/div/button[2]')))\
            .click()
        
        botao_buscar_pacotes = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[4]/button')))\
            .click()
        
        botao_modal_ida = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/span[1]')))\
            .click()

        companhia_voo = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div > div > div.cvc-core-1364 > div.cvc-core-1365 > div.cvc-core-1366 > span')))\
            .text

        tempo_voo = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div > div > div.cvc-core-1364 > div.cvc-core-1368 > div > div.cvc-core-1372 > div.cvc-core-1374 > div.cvc-core-1376 > div.cvc-core-1378')))\
            .text
        
        horas, minutos = tempo_voo.split('h ')
        minutos = minutos.replace('min', '')

        # Converter horas e minutos para int e soma
        total_minutos_voo = int(horas) * 60 + int(minutos)

        botao_fecha_modal_ida = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div > div > div.cvc-core-1351 > div.cvc-core-1352 > button')))\
            .click()

        data_ida = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/span')))\
            .text
        
        hora_ida = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/span')))\
            .text

        data_hora_str = f"{data_ida} {hora_ida}"

        data_hora_formatada_ida = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")

        data_volta = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/div[2]/span')))\
            .text

        hora_volta = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/div[1]/span')))\
            .text
        
        data_hora_str_volta = f"{data_volta} {hora_volta}"

        data_hora_formatada_volta = datetime.strptime(data_hora_str_volta, "%d/%m/%Y %H:%M")

        valor_total = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div[1]/div[2]/div[2]/div/span[2]')))\
            .text
        
        valor_total_sem_espaco = valor_total.strip()

        taxa_servico = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div[1]/div[1]/div[2]/span[2]')))\
            .text
        
        taxa_servico_sem_espaco = taxa_servico.replace("R$", '').strip()

        taxa_embarque = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div[1]/div[1]/div[2]/span[2]')))\
            .text
        
        taxa_embarque_sem_espaco = taxa_embarque.replace("R$", '').strip()

        dados_voo.append({
            'Empresa': empresa,
            'Companhia_de_voo': companhia_voo,
            'Preco_total': valor_total_sem_espaco,
            'Taxa_de_embarque': taxa_embarque_sem_espaco,
            'Taxa_de_servico': taxa_servico_sem_espaco,
            'Tempo_de_voo_minutos': total_minutos_voo,
            'Data_hora_ida': data_hora_formatada_ida,
            'Data_hora_volta': data_hora_formatada_volta
        })

        inserir_dados_voo(dados_voo)

    finally:
        ...

# Essa é a função da decolar, como o site não aceita robô, ele quebra, então não consegui terminar, 
# mas irei deixar aqui sem ser chamada para quem olhar o código, poder ver esse método
def funcao_decolar(iniciarChrome):

    try:
        empresa = "decolar"

        camp_ida = "São Paulo"

        camp_destino = "Rio de Janeiro"

        iniciarChrome.get('https://www.decolar.com/')

        botao_fechar_pop_up = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/nav/div[5]/div[2]/div[4]'))).click()

        campo_remove_pop_up = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div'))).click()

        # for letra in camp_ida:
        #     campo_ida = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/input')))\
        #         .send_keys(letra)
        #     time.sleep(3)
        
        campo_escolher_data = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div')))\
            .click()
        
        campo_data = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div[1]/div[2]/div/div[2]/div[1]/div[1]'))).text

        while campo_data != "Novembro":

            campo_data = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div[1]/div[2]/div/div[2]/div[1]/div[1]'))).text

            campo_mudar_mes = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div[1]/div[2]/div/a[2]'))).click()
            
            if campo_data == "Novembro":

                campo_data_ida = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div[1]/div[2]/div/div[1]/div[3]/div[1]/div')))\
                    .click()
                
                campo_data_volta = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div[1]/div[2]/div/div[1]/div[3]/div[4]/div')))\
                    .click()

                break

            time.sleep(2)

        campo_qtd_pessoa = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[3]/div/div/div/div/input')))\
                    .click()
                
        botao_aplicar_qtd_pessoa = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div[3]/div/div/div[3]/a')))\
            .click()

        for letra in camp_destino:
    
            campo_destino = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div/input')))\
                .send_keys(letra)
            time.sleep(3)

        # botao_buscar = WebDriverWait(iniciarChrome, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div/div/div/div/div/div/div[3]/div[3]/button')))\
        #     .click()

        input("Pressione Enter para encerrar o navegador")
    finally:
        ...

if __name__ == '__main__':
    main()