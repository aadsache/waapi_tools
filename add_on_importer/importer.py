import os
import tkinter as tk
from tkinter import filedialog
from waapi import WaapiClient, CannotConnectToWaapiException


window = tk.Tk()
window.withdraw()

folderpath = filedialog.askdirectory()

def get_file_imports(folderpath ):

    file_paths=[]
    if(folderpath):
        files = os.listdir(folderpath)
        for i in files:
            if (not os.path.isdir(i))and(i.endswith('wav')):
                file_path=folderpath+'/'+i
                file_paths.append({"audioFile": file_path, "objectPath": "\\Actor-Mixer Hierarchy\\Default Work Unit\\<Sound>{}".format(i)})#里面写Sound或者Sound SFX竟然是一样的
        
    else:
        print("no folder selected")
        os.system('pause')
    
    return file_paths

def importer(import_paths):
    try:
        
        with WaapiClient() as client:#"ws://127.0.0.1:8080/waapi"
    
            args={

            "importOperation": "useExisting", 

            "default": {"importLanguage": "SFX"}, 

            "imports": import_paths
            }
            
            client.call("ak.wwise.core.audio.import", args)

    except CannotConnectToWaapiException:
        print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

importer(get_file_imports(folderpath))

os.system('pause')
    



