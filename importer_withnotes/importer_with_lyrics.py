import os,xlrd,xlwt
from xlutils.copy import copy
from waapi import WaapiClient, CannotConnectToWaapiException


voice_par=[]
notes_par=[]
voice_path=os.path.abspath(os.path.dirname(__file__))
workbook = xlrd.open_workbook(voice_path+'/'+'实验表格.xlsx')
sheets = workbook.sheet_names()
worksheet = workbook.sheet_by_name(sheets[0])

for i in range(1, worksheet.nrows):
    notes_par.append({"object": "\\Actor-Mixer Hierarchy\\Default Work Unit\\Voices\\实验\\{}".format(worksheet.cell_value(i, 1)),
    "value": worksheet.cell_value(i, 3)
    } )
    voice_par.append(
        {"audioFile":worksheet.cell_value(i, 2),
        "objectPath": "\\Actor-Mixer Hierarchy\\Default Work Unit\\Voices\\<ActorMixer>实验\\<Sound>{}".format(worksheet.cell_value(i, 1))})

#import audio
try:
    with WaapiClient("ws://127.0.0.1:8080/waapi") as client:
            
        args={
                "importOperation": "useExisting", 
                "default": {"importLanguage": "SFX"},
                "imports": voice_par
            }
        result=client.call("ak.wwise.core.audio.import", args) 
            
                
except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

#set object notes
try:
    with WaapiClient("ws://127.0.0.1:8080/waapi") as client:
            
        for i in notes_par:
            client.call("ak.wwise.core.object.setNotes", i) 
                           
except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")




print("finished")     