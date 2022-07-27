"""
Project: UPBGEMultiplayerOnlineV7
Version: 7.0
Author: Henrique Rodrigues Pereira ( https://github.com/RIick013 / https://www.youtube.com/c/RIick013 )
"""

import bge, configparser
o, scene = bge.logic.getCurrentController().owner, bge.logic.getCurrentScene()

config = configparser.ConfigParser(delimiters=("="))
config.read(bge.logic.expandPath("//")+"config.ini")

scene.objects["nickname"]["Text"] = config["player"]["nickname"]

def main():
    if len(o["Text"]) == 16: o["Text"] = o["Text"][:-1]
    
def save():
    config.set("player", "nickname", str(scene.objects["nickname"]["Text"]))
    with open(bge.logic.expandPath("//")+"config.ini", "w") as file:
        config.write(file)
