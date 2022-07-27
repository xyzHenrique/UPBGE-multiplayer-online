"""
Project: UPBGEMultiplayerOnlineV7
Version: 7.0 (
Author: Henrique Rodrigues Pereira ( https://github.com/RIick013 / https://www.youtube.com/c/RIick013 )
"""

import json, random, threading, time, select, socket

__IP = "127.0.0.1"
__PORT = 8080
BUFFER = 8192
TIMEOUT = 0.1
PREFIX = "$"

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((__IP, __PORT))
socket.listen(0)
print("listening on: {}:{}\n".format(__IP, __PORT))

players = {}

### Handle with players who want to join the server
def login(client, nickname):
    print("player: {} logged!!".format(nickname))
    print()
        
    client.send(str("WELCOME{}{}".format(PREFIX, "Welcome player: {}".format(nickname))).encode())
    players[nickname] = {}

### Handle with disconnected players
def on_disconnected(client, address, nickname):
    print("player: {} {} disconnected!".format(nickname, address))
    print()

    del players[nickname]
    client.close()

### Handle with connected players
def on_connected(client, address):
    print("client {} connected!".format(address))
    
    nickname = None
    try:
        inputs, outputs = [client], []
        while inputs:
            r, w, e = select.select(inputs, outputs, inputs, TIMEOUT)
            for connection in r:
                if connection is client:
                    data = json.loads(connection.recv(BUFFER))

                    if "nickname" in data:
                        nickname = str(data["nickname"])
                        if nickname in list(players.keys()):
                            print("client: {} - nickname ({}) in use!".format(address, nickname))
                            print()
        
                            client.send(str("ERROR{}{}".format(PREFIX, "nickname: ({}) in use!".format(nickname))).encode())
                            break
                        else:
                            login(client, nickname)
                    
                    if data:
                        position, rotation = None, None
                
                        if "position" in data: position = data["position"]
                        if "rotation" in data: rotation = data["rotation"]
                        players.update({nickname:{"position":position, "rotation":rotation}})

                        if position == None:
                            time.sleep(0.01)
                        else:
                            client.sendall(str("INFO{}{}".format(PREFIX, players)).encode())
                            ### print("player: {} - position ({}) | rotation ({})".format(nickname, position, rotation))
                        
                else: raise
                             
    except: on_disconnected(client, address, nickname)

while True:
    client, address = socket.accept()
    threading.Thread(target=on_connected, args=(client, address)).start()

