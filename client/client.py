"""
Project: UPBGEMultiplayerOnlineV7
Version: 7.0
Author: Henrique Rodrigues Pereira ( https://github.com/RIick013 / https://www.youtube.com/c/RIick013 )
"""

import bge, configparser, json, socket, threading, traceback
from collections import OrderedDict

info, players_dict = "", {}
class client(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("connection", bool()), 
        ("connection address", str()),
        ("buffer", int()), ("buffer adjustment", bool()),
        ("minion", str()), 
    ])
    
    def start(self, args):
        self.scene = bge.logic.getCurrentScene()
        
        # - args
        self.__enabled = args["connection"]
        self.__IP, self.__PORT = str("".join(args["connection address"].split(":")[-2])), int("".join(args["connection address"].split(":")[-1]))
        self.__buffer, self.__buffer_adjustment = args["buffer"], args["buffer adjustment"]    
        self.__minion = self.scene.objectsInactive[args["minion"]]
        
        # - client
        self.socket, self.connected = socket.socket(socket.AF_INET, socket.SOCK_STREAM), False
        
        # - complements
        self.config = configparser.ConfigParser()
        self.config.read(bge.logic.expandPath("//")+"config.ini")
        
        self.object["nickname"] = self.config["player"]["nickname"]
        
        self.object.worldPosition = self.scene.objects["spawner"].worldPosition.copy()
    
    def connect(self):
        try:
            # - connect
            print("-client: connecting in ({}:{})".format(self.__IP, self.__PORT))
            self.socket.connect((self.__IP, self.__PORT))            
            
            self.T_connection = threading.Thread(target=self.connection, args=(), daemon=True).start()
            self.connected = True
            
            self.object["status"] = "connecting..." # - status
        
        except:
            print("-client: connection lost!")
            self.connected = True
            
            self.object["status"] = "connection lost" # - status
    
    def insert_player(self, players):
        global players_dict
        for player in players:
            if not player in players_dict.keys():
                print("-session: player {} connected!".format(player))
                # ...
                OBJ = self.scene.addObject(self.__minion, self.object, 0)
                OBJ["nickname"] = str(player)
                players_dict[OBJ["nickname"]] = OBJ 
                
        
    def remove_player(self, players):
        global players_dict
        for player in list(players_dict.keys()):
            if player not in players:
                print("-session: player {} disconnected!".format(player))
                # ...
                players_dict[player].endObject()
                del players_dict[player]
                 
    def connection(self):
        print("-client: connection sucessful!")
        
        self.object["status"] = "connected" # - status
        try:
            if "player-nickname" in self.scene.objects: self.scene.objects["player-nickname"]["Text"] = self.object["nickname"]
            self.socket.send(str(json.dumps({"nickname":self.object["nickname"]})).encode())
    
            while True:
                data = self.socket.recv(self.__buffer).decode()
                if self.__buffer_adjustment: self.__buffer = max(self.__buffer, len(data))
                
                if not data: break
                
                position, position = [], []
                position.append({"posX":self.object.worldPosition[0]})
                position.append({"posY":self.object.worldPosition[1]})
                position.append({"posZ":self.object.worldPosition[2]})
                
                rotation.append({"rotX":self.object.localOrientation.to_euler()[0]})
                rotation.append({"rotY":self.object.localOrientation.to_euler()[1]})
                rotation.append({"rotZ":self.object.localOrientation.to_euler()[2]})
                
                self.socket.send(str(json.dumps({"position":position, "rotation":rotation})).encode())
    
                if "INFO" in data:
                    global info
                    info = dict(eval(str("".join(data.split("$")[-1]))))        
                    if self.object["nickname"] in info: del info[self.object["nickname"]]

                    players = list(info.keys())
                    
                    self.insert_player(players)
                    self.remove_player(players)
                         
        except:
            print("-client: ERROR ({})".format(traceback.format_exc()))
            print("-client: disconnected!")
            self.socket.close()
            
            self.object["status"] = "disconnected" # - status
    
    def update(self):
        if self.__enabled == True:
            if self.object.worldPosition[2] < -10: self.object.worldPosition = self.scene.objects["spawner"].worldPosition.copy() #! - fix fall from the world
            
            if self.connected == False: self.connect()
      
