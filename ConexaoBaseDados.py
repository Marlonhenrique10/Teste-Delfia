import pyodbc
from datetime import datetime

def Conexao():

    try:
        conexao_string = 'DRIVER={ODBC Driver 17 for SQL Server};'\
                         'SERVER=DESKTOP-PIM0RRT\SQLSERVER;'\
                         'DATABASE=Delfia;'\
                         'Trusted_Connection=yes;'
        
        # Conexão com o banco de dados
        conn = pyodbc.connect(conexao_string)

        print('Deu certo a conexão')
        return conn
    except Exception as erro:
        print(f'Deu erro a conexão: {erro}')
    finally:
        print('Terminou')

def criar_tabela():
    try:
        conex = Conexao()
        cursor = conex.cursor()

        cursor.execute('''
                CREATE TABLE info_voo (
                    Empresa VARCHAR(10),
                    Companhia_de_voo VARCHAR(255),
                    Preco_total VARCHAR(10),
                    Taxa_de_embarque VARCHAR(10),
                    Taxa_de_servico VARCHAR(10),
                    Tempo_de_voo_minutos INT,
                    Data_hora_ida DATETIME,
                    Data_hora_volta DATETIME
                )
        ''')

        conex.commit()
        conex.close()
    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        print('Terminou')

def inserir_dados_voo(dados):

    try:
        conn = Conexao()
        cursor = conn.cursor()

        for dado in dados:

            data_hora_ida_format = dado['Data_hora_ida'].strftime('%d/%m/%Y %H:%M')
            data_hora_volta_format = dado['Data_hora_volta'].strftime('%d/%m/%Y %H:%M')

            cursor.execute('''INSERT INTO info_voo (Empresa, Companhia_de_voo, Preco_total, Taxa_de_embarque,'''\
                           '''Taxa_de_servico, Tempo_de_voo_minutos, Data_hora_ida, Data_hora_volta)'''\
                           '''VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', dado['Empresa'], dado['Companhia_de_voo'], dado['Preco_total'], dado['Taxa_de_embarque'],\
                            dado['Taxa_de_servico'], dado['Tempo_de_voo_minutos'], data_hora_ida_format, data_hora_volta_format)
        conn.commit()
        conn.close()
    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        print('Terminou o insert')

if __name__ == '__main__':
    Conexao()