import pickle
import socket 

x = '-'*30

# objeto socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# nome da máquina
host = socket.gethostname()

# número da porta
port = 9999

# conexão com o servidor 
client_socket.connect((host, port))

# parte lógica do script
 
usuario = str(input('Digite seu nome de usuário... '))
client_socket.send(f"{usuario}".encode('utf-8'))
print(f'\n           {x} Bem-vindo(a) a sua agenda, {usuario.capitalize()} {x} \n')


while True:

    def tabela_acoes():
        x = '-'*30
        print(f'{x} OPERAÇÕES DO SISTEMA - AGENDA {x}')
        print('-'*91)
        print('  1 - Retornar todos os cadastros\n')
        print('  2 - Criar cadastro\n')
        print('  3 - Alterar cadastro. Para alterar consulte o index do cadastro em 1 - Retornar todos os Cadastros\n')
        print('  4 - Deletar cadastro\n')
        print('  5 - Buscar por nome\n')
        print('  6 - Buscar por letra\n')
        print('  7 - Sair do programa')
        print('-'*91)


    def acoes():
        acao = str(input('Digite o número correspondente a ação desejada... '))
        client_socket.send(f"{acao}".encode())

        if acao == '1': 

            server_response_1 = client_socket.recv(10000)
            dados = pickle.loads(server_response_1)
            
            if len(dados) == 0:
                print(f'\n{usuario.capitalize()}, você ainda não registrou seus contatos...\n')
                print('-'*80)

            else:
                print(f'\n {x} CONTATOS AGENDADOS {x} \n')
                for index, item in enumerate(dados, start=0):
                    print(f'\n Código: {index} | Nome: {item[0]} | Telefone: {item[1]} | E-mail: {item[2]} | Cadastrado por: {item[3]}\n')
                    print('-'*80)
                
        
        elif acao == '2':
            nome = str(input('Digite o nome a ser cadastrado... ')).lower()
            telefone = str(input('Digite o telefone a ser cadastrado... '))
            email = str(input('Digite o e-mail a ser cadastrado... ')).lower()
            client_socket.send(f"{nome},{telefone},{email}".encode('utf-8'))

        
        elif acao == '3':
        
            index_cadastro = int(input('Digite o número do cadastro a ser alterado... '))
            index_index = int(input('Digite 0 para nome, 1 para telefone ou 2 para email... '))
            alteracao = str(input('Digite a alteração... '))

            client_socket.send(f"{index_cadastro},{index_index},{alteracao}".encode('utf-8'))

            
        elif acao == '4':
            e_mail = str(input('Digite o email do cadastro a ser deletado... '))
            client_socket.send(f"{e_mail}".encode('utf-8'))
            server_response_4 = client_socket.recv(1024).decode('utf-8')
            print(server_response_4)
            

        elif acao == '5':

            nome_procurado = str(input('Digite o nome que deseja procurar... ')).lower()
            client_socket.send(f"{nome_procurado}".encode('utf-8'))
        
            server_response_5 = client_socket.recv(10000)
            nome = pickle.loads(server_response_5)

            if len(nome) == 0:
                print(f'\nVocê não possui contatos com o nome {nome_procurado}...\n')
            else:
                print(f'\n{x} CONTATOS COM O NOME "{nome_procurado.upper()}" {x}')
                for n in nome:
                    print(f'\nNome: {n[0]} | Telefone: {n[1]} | E-mail: {n[2]}\n')
                    print('-'*80)


        elif acao == '6':

            letra_procurada = str(input('Digite a letra procurada... ')).lower()
            client_socket.send(f"{letra_procurada}".encode('utf-8'))
            server_response_6 = client_socket.recv(10000)
            letra = pickle.loads(server_response_6)

            if len(letra) == 0:
                print(f'\nA letra {letra_procurada} não corresponde aos contatos cadastrados...\n')

            else:
                print(f'{x} CONTATOS COM A LETRA "{letra_procurada.upper()}" {x}')
                for l in letra:
                    print(f'\nNome: {l[0]} | Telefone: {l[1]} | E-mail: {l[2]}\n')
                    print('-'*80)


        elif acao == '7':
            print('\n', x, 'PROGRAMA ENCERRADO', x, '\n')
            exit()

        
        else:
            print('\n', x, 'COMANDO INVALIDO - PROGRAMA ENCERRADO', x, '\n')
            exit()


    tabela_acoes()
    acoes()

# fechar a conexão do cliente
client_socket.close()
