import json
import requests
import os.path
from os import path

# Test vars
# key = 'action init'

# Add "e" for "classes"
reference = 'class'
if 'class' in reference :
    jsonName = reference + 'es.json'
else :
    jsonName = reference + 's.json'

dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)
# print('\\\\'.join(dir_path.split(os.path.sep)))

with open (dir_path + '/Json/classes.json', 'r') as openFile : 
    fileContent = json.load(openFile)
    # fileContent = openFile.read()
    print(fileContent)

# jsonUrl = 'https://raw.githubusercontent.com/keesiemeijer/alfred-wordpress-developer-workflow/master/'
# request = requests.get(jsonUrl)
# json = request.json()
# createFile = open(dir_path + '/Json/' + jsonName, 'w')
# createFile.write(json)
# createFile.close()

# print(os.path.dirname(os.path.realpath(__file__)))
# exit

# results = []
# r = requests.get('https://raw.githubusercontent.com/keesiemeijer/alfred-wordpress-developer-workflow/master/actions.json')
# json = r.json()
# url = json['url']
# content = json['content']
# for i in content :
#     if key.replace('action ', '') in i['slug'] :
#         results.append({
#             "Title": i['title'],
#             "IcoPath" : "Images/app.ico",
#             "JsonRPCAction": {
#                 "method": "openUrl",
#                 "parameters": [url],
#                 "dontHideAfterAction": True
#             }
#         })
#         print(i['title'])

    

# print(results)
        
    # results.append({
    #     "Title": i['title'],
    #     "IcoPath" : "Images/app.ico",
    #     "JsonRPCAction": {
    #         "method": "openUrl",
    #         "parameters": [url],
    #         "dontHideAfterAction": True
    #     }
    # })