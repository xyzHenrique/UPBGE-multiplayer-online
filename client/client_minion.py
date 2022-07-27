"""
Project: UPBGEMultiplayerOnlineV7
Require: client.py
Version: 7.0
Author: Henrique Rodrigues Pereira ( https://github.com/RIick013 / https://www.youtube.com/c/RIick013 )
"""

import bge
from mathutils import Vector

o, scene = bge.logic.getCurrentController().owner, bge.logic.getCurrentScene()

def main():   
    from client import info, players_dict
    
    # - position/rotation
    info_position, info_rotation = info.get(o["nickname"])["position"], info.get(o["nickname"])["rotation"]

    posX, posY, posZ = dict(info_position[0]), dict(info_position[1]), dict(info_position[2])
    rotX, rotY, rotZ = dict(info_rotation[0]), dict(info_rotation[1]), dict(info_rotation[2])
    print("player: {} ({}) | ({}) | ({}) - ({}) | ({}) | ({})".format(o["nickname"], posX, posY, posZ, rotX, rotY, rotZ))

    # - update position/rotation
    o.worldPosition = Vector((posX.get("posX"),posY.get("posY"),posZ.get("posZ"))) 
    o.localOrientation = Vector((rotX.get("rotX"),rotY.get("rotY"),rotZ.get("rotZ")))

    if o.worldPosition[2] < -10: o.worldPosition = scene.objects["spawner"].worldPosition.copy() #! - fix fall from the world
