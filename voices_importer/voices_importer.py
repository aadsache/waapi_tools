import os
from waapi import WaapiClient, CannotConnectToWaapiException

def foler_content(folderpath):
    file_dic={}# {name,path}
    if(folderpath):
        files = os.listdir(folderpath)
        for i in files:
            if (not os.path.isdir(folderpath+'/'+i))and(i.endswith('wav')):
                file_dic[i]=folderpath+"/"+i
    
    return file_dic
    
def voices_importer(file_dic,language="EN"):#lanaguage="EN" or "CN"
    def get_voices_imports(file_dic,language):# file_dic--{name，path}
        file_paths=[]
        for key,value in file_dic.items():
            if key.startswith(language):
                file_paths.append({"audioFile": value, "objectPath": "\\Actor-Mixer Hierarchy\\Default Work Unit\\Voices\\<ActorMixer>{}\\<Sound>{}".format(os.path.split(os.path.dirname(value))[-1],key[3:-4])})   
        
        return file_paths
        
    def ww_audio_import(import_paths,language):
        try:
        
            with WaapiClient() as client:
    
                args={

                "importOperation": "useExisting", 

                "default": {"importLanguage": {'EN':'English(US)','CN':'Chinese',}.get(language)}, 

                "imports": import_paths
                }
                
                client.call("ak.wwise.core.audio.import", args)
    
        except CannotConnectToWaapiException:
            print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
        
    
    ww_audio_import(get_voices_imports(file_dic,language),language)

def foler_creater(file_dic):

    characters=[]    
    for value in file_dic.values():
        if not os.path.split(os.path.dirname(value))[-1] in characters:
            characters.append(os.path.split(os.path.dirname(value))[-1])
    
    try:
            
        with WaapiClient() as client:#"ws://127.0.0.1:8080/waapi"
            
            args={
                    "parent": "\\Events\\Default Work Unit", 
                    "type": "Folder", 
                    "name": "Voices", 
                    "onNameConflict": "merge"
                    }
                    
            client.call('ak.wwise.core.object.create',args)#creat root Voices folder
                
    
            for i in characters:
            
                    args={
                        "parent": "\\Events\\Default Work Unit\\Voices", 
                        "type": "Folder", 
                        "name": i, 
                        "onNameConflict": "merge"
                        }
                    client.call('ak.wwise.core.object.create',args)#creat characters folders
                
    except CannotConnectToWaapiException:
        print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

def events_importer(file_dic):
   
    def get_event_argments(file_dic):
        
        argments=[]
        for key,value in file_dic.items():
            
            argments.append({"parent": "\\Events\\Default Work Unit\\Voices\\{}".format(os.path.split(os.path.dirname(value))[-1]), 
                "type": "Event", 
                "name": "{}".format(key[3:-4]), 
                "onNameConflict": "merge",
                "children": [
            {
                
                "name": "", 
                "type": "Action", 
                "@ActionType": 1, 
                "@Target": "\\Actor-Mixer Hierarchy\\Default Work Unit\\Voices\\{}\\{}".format(os.path.split(os.path.dirname(value))[-1],key[3:-4])
            }
            ]
                })
        
        return argments

    

    def ww_event_creat(args):
        try:
            
            with WaapiClient() as client:#"ws://127.0.0.1:8080/waapi"
                
                for i in args:        
                    client.call("ak.wwise.core.object.create", i)

        except CannotConnectToWaapiException:
            print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
    
    foler_creater(file_dic)
    ww_event_creat(get_event_argments(file_dic))
       

def main():
    
    voice_path=os.path.abspath(os.path.dirname(__file__))

    for i in os.listdir(voice_path):
        if  (os.path.isdir(voice_path+'/'+i)):
            name_dic=foler_content(voice_path+'/'+i)
            voices_importer(name_dic,'EN')
            voices_importer(name_dic,'CN')
            events_importer(name_dic)
   
            

if __name__ == '__main__':

    main()
    print("finished") 

