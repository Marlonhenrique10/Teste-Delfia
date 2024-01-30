import pyodbc

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

def tabela_existe(conexao, nome_tabela):
    try:
        cursor = conexao.cursor()

        # Verifica se a tabela existe no banco de dados
        cursor.execute(f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{nome_tabela}'")
        resultado = cursor.fetchone()

        return resultado is not None

    except Exception as erro:
        print(f'Erro ao verificar a existência da tabela: {erro}')
        return False

def criar_tabela():
    try:
        conex = Conexao()
        cursor = conex.cursor()

        cursor.execute('''
                CREATE TABLE tabela_produtos (
                    modelo VARCHAR(50),
                    capacidade_GB VARCHAR(10),
                    tamanho_da_tela VARCHAR(10),
                    preco_total VARCHAR(10),
                    valor_parcela VARCHAR(10),
                    quantidade_parcela VARCHAR(10),
                    cor VARCHAR(10),
                    ultimas_pecas BIT
                )
        ''')

        conex.commit()
        conex.close()
    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        print('Terminou')

def salvar_produtos(dados):

    try:
        conn = Conexao()

        if not tabela_existe(conn, 'tabela_produtos'):
            criar_tabela()

        cursor = conn.cursor()

        for dado in dados:

            cursor.execute('''INSERT INTO tabela_produtos (modelo, capacidade_GB, tamanho_da_tela, preco_total,'''\
                           '''valor_parcela, quantidade_parcela, cor, ultimas_pecas)'''\
                           '''VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', dado['modelo'], dado['capacidade'], dado['tamanho_da_tela'], dado['preco_total'],\
                            dado['valor_parcela'], dado['quantidade_parcela'], dado['cor'], dado['ultimas_pecas'])
        conn.commit()
        conn.close()
    except Exception as erro:
        print(f'Erro: {erro}')
    finally:
        print('Terminou o insert')

if __name__ == '__main__':
    Conexao()