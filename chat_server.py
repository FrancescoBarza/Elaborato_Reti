#!/usr/bin/env python3
"""Sistema di Chat Client-Server"""

"""SERVER"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

"""Funzione per accettare le connessioni dei client in entrata."""
def accetta_connessioni_in_entrata():
    while True:
        try:
            client, client_address = SERVER.accept()  # Accetta la connessione del client
            print("%s:%s si è collegato." % client_address)
            # Invia un messaggio di benvenuto al client
            client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
            # Registra il client nel dizionario degli indirizzi
            indirizzi[client] = client_address
            # Avvia un thread per gestire il client
            Thread(target=gestice_client, args=(client,)).start()
        except OSError as e:
            print("Errore durante l'accettazione della connessione:", e)
            break
        except Exception as e:
            print("Errore generico durante l'accettazione della connessione:", e)
            break
        
"""Funzione per gestire la connessione di un singolo client."""
def gestice_client(client): # Prende il socket del client come argomento della funzione.
    try:
        # Riceve il nome del client
        nome = client.recv(BUFSIZ).decode("utf8")
        # Invia un messaggio di benvenuto personalizzato
        benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % nome
        client.send(bytes(benvenuto, "utf8"))
        # Comunica a tutti i client che un nuovo utente si è unito alla chat
        msg = "%s si è unito alla chat!" % nome
        broadcast(bytes(msg, "utf8"))
        # Registra il client nel dizionario dei client
        clients[client] = nome

        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                # Invia il messaggio a tutti i client tranne a se stesso
                broadcast(msg, nome+": ")
            else:
                # Se il client ha inviato "{quit}", chiude la connessione
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]  # Rimuove il client dal dizionario
                # Comunica a tutti i client che l'utente ha lasciato la chat
                broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
                break
    except OSError as e:
        print("Errore durante la gestione del client:", e)
        # Chiude la connessione
        client.close()
        del clients[client]
    except Exception as e:
        print("Errore generico durante la gestione del client:", e)
        # Chiude la connessione
        client.close()
        del clients[client]
        
"""Funzione per inviare un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefisso=""):
    for utente in clients:
        try:
            utente.send(bytes(prefisso, "utf8")+msg)
        except OSError as e:
            print("Errore durante l'invio del messaggio a", clients[utente], ":", e)
            utente.close()
            del clients[utente]
        except Exception as e:
            print("Errore generico durante l'invio del messaggio a", clients[utente], ":", e)
            utente.close()
            del clients[utente]
            
# Dizionario per memorizzare i client e i loro indirizzi
clients = {}
indirizzi = {}

# Configurazione del server
HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

# Creazione del socket del server
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    # Avvia il server per accettare connessioni
    SERVER.listen(5)
    print("In attesa di connessioni...")
    # Avvia un thread per accettare connessioni in entrata
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()  # Aspetta che il thread di accettazione termini
    SERVER.close()  # Chiude il socket del server
