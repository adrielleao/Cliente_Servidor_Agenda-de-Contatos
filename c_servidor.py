import socket
import threading
import pickle 
  
agenda = []
with open('dados.pickle', 'rb') as a:
        agenda_pickle = pickle.load(a)
        print(agenda_pickle)

agenda = agenda_pickle

def handle_client(client_socket, client_address):
    print(f"Conexão estabelecida com {client_address}")

    client_message_usuario = client_socket.recv(1024).decode()
    usuario = client_message_usuario

    while True:
        

        client_message_acao = client_socket.recv(1024).decode()
        acao = client_message_acao

        try:
            

            if acao == '1':
                '''
                A ação 1, printa todos os contatos da agenda do usuário especificado
                '''
                with open('dados.pickle', 'rb') as a:   # Operação de leitura em binário
                    agenda = pickle.load(a)             # 

                agenda_usuario = list(filter((lambda x: x[-1] == usuario), agenda)) #Função Lambda
                
                x = pickle.dumps(agenda_usuario)    # O arquivo pickle, conserva a estrutura de dados - Lista 
                client_socket.send(x)               # O arquivo referenciado é enviado ao cliente

            
            elif acao == '2':
                '''
                A ação 2, é responsável pelo decodificação de dados
                enviados pelos usuários e cadastro dos contatos na agenda 
                '''
                with open('dados.pickle', 'rb') as a:
                    agenda = pickle.load(a)

                client_message_2 = client_socket.recv(10000).decode('utf-8')
                nome, telefone, email = client_message_2.split(',')    
                agenda.append([nome, telefone, email, usuario])

                with open('dados.pickle', 'wb') as f:
                    pickle.dump(agenda, f, -1)

            
            elif acao == '3':
                '''
                A ação 3, é reponsável por decodificar os dados enviados pelo usuário e
                alterar nome, telefone ou email do contato selecionado por index
                '''
                with open('dados.pickle', 'rb') as a:
                    agenda = pickle.load(a)

                agenda_usuario = list(filter(lambda x: x[-1] == usuario, agenda))

                client_message_3 = client_socket.recv(10000).decode('utf-8')
                index_cadastro, index_index, alteracao = client_message_3.split(',')

                agenda_usuario[int(index_cadastro)][int(index_index)] = alteracao 

                with open('dados.pickle', 'wb') as f:
                    pickle.dump(agenda, f, -1)

            
            elif acao == '4':
                '''
                A ação 4, recebe o dados e_mail, decodifica-o e exclui o contato
                da agenda usuário e geral, porém não permite a exclusão de dados registrados
                por outros usuários.

                Ex: Ana e Jonas possuem Karla em suas agendas, Ana exclui Karla, porém o cadastro
                de Karla ainda está ativo para o usuário Jonas...
                '''
                with open('dados.pickle', 'rb') as a:
                    agenda = pickle.load(a)

                client_message_4 = client_socket.recv(10000).decode('utf-8')
                e_mail = client_message_4
                  
                agenda_usuario = list(filter(lambda x: x[-1] == usuario, agenda))

                for item in agenda_usuario[:]:
                    if e_mail in item:
                        agenda_usuario.remove(item)
                        acao4 = f'\n---- O contato de {item[0]} foi deletado ----\n'

                for item in agenda[:]:
                    if e_mail in item and item[3] == usuario:
                        agenda.remove(item)
                        print(acao4)

                with open('dados.pickle', 'wb') as f:
                    pickle.dump(agenda, f, -1)

                client_socket.send(acao4.encode('utf-8'))


            elif acao == '5':
                '''
                A ação 5, decodifica o dado nome_procurado e retorna o registro do 
                contato, apenas se houver o nome na agenda
                '''
                with open('dados.pickle', 'rb') as a:
                    agenda = pickle.load(a)

                agenda_usuario = list(filter(lambda x: x[-1] == usuario, agenda))

                client_message_5 = client_socket.recv(10000).decode('utf-8')
                nome_procurado = client_message_5
                
                nome = []
                for n in agenda_usuario:
                    if n[0] == nome_procurado:
                        nome.append(n)

                acao5 = pickle.dumps(nome)
                client_socket.send(acao5)

                with open('dados.pickle', 'wb') as f:
                    pickle.dump(agenda, f, -1)

            
            elif acao == '6':
                '''
                A ação 6, decodifica a variável letra_procurada e retorna o registro do 
                contato, apenas se houver nomes iniciados com a letra
                '''
                with open('dados.pickle', 'rb') as a:
                    agenda = pickle.load(a)

                agenda_usuario = list(filter(lambda x: x[-1] == usuario, agenda))

                client_message_6 = client_socket.recv(10000).decode('utf-8')
                letra_procurada = client_message_6

                letra = []
                for l in agenda_usuario:
                    if l[0][0] == letra_procurada:
                        letra.append(l)

                acao6 = pickle.dumps(letra)
                client_socket.send(acao6)

                with open('dados.pickle', 'wb') as f:
                    pickle.dump(agenda, f, -1)
                

        except ConnectionResetError:
            print(f"Conexão encerrada por: {client_address}")
            break

    client_socket.close()

# objeto socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# nome da máquina
host = socket.gethostname()

# número da máquina
port = 9999

# vinculação do socket a um host e porta
server_socket.bind((host, port))

# estado de "escuta" para futuras conexões
server_socket.listen(5)

print(f"O servidor está 'escutando' {host}:{port}")

# aceita novas conexões de clientes e dá uma nova thread para cada conexão
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()