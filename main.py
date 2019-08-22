#encoding=utf8

import json
import os.path
from os import path
import requests
from bs4 import BeautifulSoup
import webbrowser
from wox import Wox, WoxAPI

class WordPressCodex(Wox) :

    def query(self, query) :

        results = []
        references = [
            'action',
            'class',
            'filter',
            'function',
            'hook',
        ]

        dir_path = os.path.dirname(os.path.realpath(__file__))

        for reference in references :
            if reference in query : # "action "...

                # Add "e" for "classes"
                if 'class' in reference :
                    jsonName = reference + 'es.json'
                else :
                    jsonName = reference + 's.json'

                # If no json files found, try to fetch it and make json files
                if not (path.exists(dir_path + '/Json/' + jsonName)) :
                    jsonUrl = 'https://raw.githubusercontent.com/keesiemeijer/alfred-wordpress-developer-workflow/master/' + jsonName
                    request = requests.get(jsonUrl)
                    fileContent = request.json()

                    # Create file and add the json content
                    with open(dir_path + '/Json/' + jsonName, 'w') as createFile :
                        createFile.write(fileContent)

                # Open json file content
                with open(dir_path + '/Json/' + jsonName, 'r') as openFile : 
                    fileContent = json.load(openFile)

                url = fileContent['url']
                content = fileContent['content']
                secondSearch = query.replace(reference + ' ', '').replace(' ', '_')

                # Add reference items
                for item in content :
                    if not secondSearch or secondSearch == ' ' or len(secondSearch) <= 2  :
                        results.append({
                            'Title': item['title'],
                            'SubTitle': item['slug'].replace('_', ' ').capitalize(),
                            'IcoPath' : 'Images/app.ico',
                            'JsonRPCAction': {
                                'method': 'openUrl',
                                'parameters': [url + '/' + item['slug']],
                                'dontHideAfterAction': True
                            }
                        })

                    else :
                        if secondSearch in item['slug'] :
                            results.append({
                                'Title': item['title'],
                                'SubTitle': item['slug'].replace('_', ' ').capitalize(),
                                'IcoPath' : 'Images/app.ico',
                                'JsonRPCAction': {
                                    'method': 'openUrl',
                                    'parameters': [url + '/' + item['slug']],
                                    'dontHideAfterAction': True
                                }
                            })

            # Add references as result if search is empty or nearly empty
            elif not query or query == ' ' or len(query) <= 3 :
                if 'class' in reference :
                    resultTitle = reference.capitalize() + 'es'
                else :
                    resultTitle = reference.capitalize() + 's'

                results.append({
                    'Title': resultTitle,
                    'SubTitle': 'Search ' + resultTitle,
                    'IcoPath' : 'Images/app.ico',
                    'JsonRPCAction': {
                        'method': 'Wox.ChangeQueryText',
                        'parameters': ['wp ' + reference + ' ', True],
                        'dontHideAfterAction': True
                    }
                })

        return results

    def openUrl(self, url) :
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__" :
    WordPressCodex()
