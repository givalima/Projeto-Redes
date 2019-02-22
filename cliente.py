import socket

def download():
    #host = '192.168.13.7' #outro pc como servidor
    host = '' #mesmo pc como servidor
    port = 5000

    print("---------------------------------------------------------------------")
    print("        Bem vindo! Baixe quantos arquivos desejar do servidor        ")
    print("---------------------------------------------------------------------")

    while(True):
        #Inicia conexão
        sockobj = socket.socket()
        sockobj.connect((host, port))

        print("Arquivos disponíveis para download:")
        files_server = sockobj.recv(1024).decode()
        
        while(files_server!='0'):
            print(files_server)
            files_server = sockobj.recv(1024).decode()

        file_name = input("\nDigite o nome do arquivo para download ou 0 para sair: ")

        if(file_name!='0'):
            #Envio
            sockobj.send(file_name.encode())
    
            #Resposta
            receive = sockobj.recv(1024).decode()
            # 1 (True) indica que o arquivo é válido
            if(int(receive[0])):
                file_size = int(receive[1:])
                print("[SUCCESS] Arquivo encontrado!\n\nNome do arquivo: "+str(file_name)+"\nTamanho do arquivo: "+str(file_size)+" bytes")
                query = input("Deseja baixar? (S/N)?: ")
                
                if(query=='S'):
                    sockobj.send(b"1")

                    #Cria novo arquivo para armazenar os dados enviados do servidor
                    file_received = open(file_name+"[download]",'wb')
                    received_total = 0
                    loading = "Baixando."
                    print(loading)
                    cut= 10

                    #Até todos os dados do arquivo do servidor estarem armazenados no arquivo recebido no cliente
                    while(True):
                        if(received_total>=file_size):
                            break
                        #Dados do arquivo recebidos do servidor
                        data_received = sockobj.recv(1024)
                        received_total += len(data_received)

                        #Escreve no arquivo os dados recebidos
                        file_received.write(data_received)

                        #Status do download
                        if(int(received_total/float(file_size)*100)>cut):   
                            loading += "."
                            print(loading)
                            cut +=10
                    print("[SUCCESS] Download concluído com sucesso!\n")
                    file_received.close()

            else: #Caso o arquivo seja inválido
                print("[ERROR] Este arquivo não foi encontrado no servidor.\n")
            
            #Fecha conexão
            sockobj.close()
        else:
            print("Bye.")
            break
download()
