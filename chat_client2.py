#!/usr/bin/env python3
"""CLIENT"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

"""Funzione per gestire la ricezione dei messaggi dal server."""
def receive():
    while True:
        try:
            # Quando viene chiamata la funzione receive, si mette in ascolto dei messaggi che
            # Arrivano sul socket
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            # Visualizziamo l'elenco dei messaggi sullo schermo
            # E facciamo in modo che il cursore sia visibile al termine degli stessi
            msg_list.insert(tkt.END, msg)
            # Nel caso di errore e' probabile che il client abbia abbandonato la chat.
        except OSError:
            break
        
"""Funzione per inviare i messaggi al server."""
def send(event=None):
    # Ottiene il messaggio dall'Entry Field
    msg = my_msg.get()  
    # Pulisce l'Entry Field
    my_msg.set("")   
    # Invia il messaggio al server
    client_socket.send(bytes(msg, "utf8")) 
    if msg == "{quit}":
        client_socket.close()  # Chiude il socket del client
        finestra.quit()  # Chiude la finestra della chat
        finestra.destroy()

"""Funzione chiamata quando la finestra della chat viene chiusa."""
def on_closing(event=None):
    my_msg.set("{quit}")  # Imposta "{quit}" come messaggio di chiusura
    send()  # Chiude correttamente la connessione con il server

# Configurazione della GUI Tkinter
finestra = tkt.Tk()
finestra.title("Chat_Elaborato")

# Crea il Frame per contenere i messaggi
messages_frame = tkt.Frame(finestra)
# Crea una variabile di tipo stringa per i messaggi da inviare.
my_msg = tkt.StringVar()
# Indichiamo all'utente dove deve scrivere i suoi messaggi
my_msg.set("Scrivi qui i tuoi messaggi.")
#Crea una scrollbar per navigare tra i messaggi precedenti.
scrollbar = tkt.Scrollbar(messages_frame)

# La parte seguente contiene i messaggi.
msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

#Crea il campo di input e lo associamo alla variabile stringa
entry_field = tkt.Entry(finestra, textvariable=my_msg)
# Leghiamo la funzione send al tasto Return
entry_field.bind("<Return>", send)

entry_field.pack()
# Crea il tasto invio e lo associamo alla funzione send
send_button = tkt.Button(finestra, text="Invio", command=send)
# Integriamo il tasto nel pacchetto
send_button.pack()

finestra.protocol("WM_DELETE_WINDOW", on_closing)

# Connessione al Server
HOST = input('Inserire il Server host: ')
PORT = input('Inserire la porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
# Avvia l'esecuzione della Finestra Chat.
tkt.mainloop()
