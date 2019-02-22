import socket
import os
import threading

def file_send(file_name,sockobj):

    #Listando arquivos disponíveis para download
    result = []
    for _, _, arq in os.walk('/home/andre/Área de Trabalho/Server'):
        result.append(arq)
        list_file = result[0]
        
    for i in range(len(list_file)):
        file_name = str(list_file[i])
        sockobj.send(file_name.encode())
        for j in range(100000):
            a = "+Time"
    sockobj.send("0".encode())
        
    file_name = sockobj.recv(1024)

    if(os.path.isfile(file_name)):
        #Caso o arquivo exista, envio uma resposta de OK (1) e o tamanho do arquivo para o cliente
        result = "1" + str(os.path.getsize(file_name))
        sockobj.send(result.encode())

        #Recebo uma resposta do cliente se deseja baixar o arquivo, onde "1" indica que sim
        answer_client = sockobj.recv(1024).decode()

        if(int(answer_client[0])):
            #Abro o arquivo para leitura e envio os dados via socket
            with open(file_name,'rb') as file_send:
                send_data = file_send.read(1024)
                sockobj.send(send_data)

                while(send_data!=None):
                    send_data = file_send.read(1024)
                    sockobj.send(send_data)
    else:
        #Caso o arquivo não exista, envio uma resposta de erro (0)
        sockobj.send("0".encode())

    #Fecha conexão
    sockobj.close()

def init_server():
    host = ''
    port = 5000

    #Inicia servidor
    sockobj = socket.socket()
    sockobj.bind((host,port))
    sockobj.listen(10)

    print("Servidor iniciado e pronto para uso!")
    while(True):
        client,address = sockobj.accept()
        print("Cliente "+address[0]+" conectado com sucesso!")

        #Inicia thread para estabelecer comunicação com o cliente
        thread = threading.Thread(target=file_send, args=("file_send", client))
        thread.start()
    
    #Encerra servidor
    sockobj.close()

init_server()
