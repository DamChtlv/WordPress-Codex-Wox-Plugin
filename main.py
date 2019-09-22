# -*- coding: utf-8 -*-

# Imports
import json
import os

# Wox fix - missing "requests" module
try:
    import requests
except ImportError:
    from pip._internal import main as pip
    pip(['install', '--user', 'requests'])
    import requests

# Wox fix - missing "bs4" module
try:
    from bs4 import BeautifulSoup
except ImportError:
    from pip._internal import main as pip
    pip(['install', '--user', 'bs4'])
    from bs4 import BeautifulSoup

import webbrowser
from wox import Wox, WoxAPI

# Variables
CURRENT_DIR = os.getcwd()
JSON_DIR_NAME = 'Json'
JSON_DIR = os.path.join(CURRENT_DIR, JSON_DIR_NAME) + os.sep
REFERENCES = [
    'action',
    'class',
    'filter',
    'function',
    'hook',
]
STR_REFERENCES = ' '.join(REFERENCES)

class WordPressCodex(Wox):
    wp_ref_version = '5.2.2'

    def __init__(self):
        super().__init__()
        self.load_json()

    def query(self, query):
        results = []

        search = query.replace(' ', '_')
        firstSearch = query.split(' ')[0].replace(' ', '_')
        
        # Prefix query : "wp act..."
        if firstSearch in STR_REFERENCES:
            for reference in REFERENCES:
                if reference in query: 

                    prefixSearch = query.replace(reference + ' ', '')

                    # Download latest version of json file if we don't have it yet
                    json_file = self.get_json_file_path(reference)
                    if not os.path.isfile(json_file):
                        self.get_json_file(reference)

                    # Open json file content
                    with open(json_file, 'r') as openFile:
                        fileContent = json.load(openFile)

                    url = fileContent['url']
                    content = fileContent['content']
                    wp_ref_version = fileContent['version']

                    self.wp_ref_version = wp_ref_version

                    if not prefixSearch :
                        resultTitle = self.get_ref_plural_name(reference).capitalize()
                        results.append({
                            'Title': resultTitle,
                            'SubTitle': 'Search ' + resultTitle,
                            'IcoPath': 'Images/app.ico',
                            'JsonRPCAction': {
                                'method': 'Wox.ChangeQueryText',
                                'parameters': ['wp ' + reference + ' ', True],
                                'dontHideAfterAction': True
                            }
                        })

                    else:

                        firstLevelMatchs = []
                        secondLevelMatchs = []
                        thirdLevelMatchs = []

                        # Split the query by words for the search words scoring system
                        splitWords = prefixSearch.split(' ')
                        for item in content:

                            wordsScore = 0
                            for splitWord in splitWords:
                                if splitWord in item['slug']:
                                    wordsScore += 1

                            resultObject = {
                                'Title': item['title'],
                                'SubTitle': item['slug'].replace('_', ' ').capitalize(),
                                'IcoPath': 'Images/app.ico',
                                'JsonRPCAction': {
                                    'method': 'openUrl',
                                    'parameters': [url + '/' + item['slug']],
                                    'dontHideAfterAction': True
                                }
                            }

                            # If we found the perfect match, prepend it first in the results.
                            if len(splitWords) == wordsScore and prefixSearch.replace(' ', '_') == item['slug']:
                                firstLevelMatchs.append(resultObject)

                            # If we found a match that have all words in it, prepend it in the results after first.
                            elif len(splitWords) == wordsScore and item['slug'].split('_')[0] == prefixSearch.split(' ')[0]:
                                secondLevelMatchs.append(resultObject)

                            # If we found a match that have all words in it, prepend it in the results after second.
                            elif len(splitWords) == wordsScore and prefixSearch.replace(' ', '_') in item['slug']:
                                thirdLevelMatchs.append(resultObject)

                            # Else fallback and append something that match a little
                            elif prefixSearch.replace(' ', '_') in item['slug']:
                                results.append(resultObject)

                        results = firstLevelMatchs + secondLevelMatchs + thirdLevelMatchs + results
                        
                # Add references as result if search is empty or nearly empty
                elif not query or query == ' ' or len(query) <= 2 or query in reference:

                    resultTitle = self.get_ref_plural_name(reference).capitalize()
                    results.append({
                        'Title': resultTitle,
                        'SubTitle': 'Search ' + resultTitle,
                        'IcoPath': 'Images/app.ico',
                        'JsonRPCAction': {
                            'method': 'Wox.ChangeQueryText',
                            'parameters': ['wp ' + reference + ' ', True],
                            'dontHideAfterAction': True
                        }
                    })

        # Wildcard query (no prefix) : "wp get permalink"
        else:

            # Array to store all items found in all json files
            contentItems = []

            for reference in REFERENCES:

                # Download latest version of json file if we don't have it yet
                json_file = self.get_json_file_path(reference)
                if not os.path.isfile(json_file):
                    self.get_json_file(reference)

                # Open json file content
                with open(json_file, 'r') as openFile:
                    fileContent = json.load(openFile)

                url = fileContent['url']
                content = fileContent['content']
                wp_ref_version = fileContent['version']

                self.wp_ref_version = wp_ref_version

                for item in content:
                    item['reference'] = reference.capitalize()
                    item['url'] = url
                    contentItems.append(item)

            firstLevelMatchs = []
            secondLevelMatchs = []
            thirdLevelMatchs = []

            # Split the query by words for the search words scoring system
            splitWords = query.split(' ')
            for item in contentItems:
                
                wordsScore = 0
                for splitWord in splitWords:
                    if splitWord in item['slug']:
                        wordsScore += 1

                resultObject = {
                    'Title': item['title'],
                    'SubTitle': item['reference'] + ' - ' + item['slug'].replace('_', ' ').capitalize(),
                    'IcoPath': 'Images/app.ico',
                    'JsonRPCAction': {
                        'method': 'openUrl',
                        'parameters': [item['url'] + '/' + item['slug']],
                        'dontHideAfterAction': True
                    }
                }

                # If we found the perfect match, prepend it first in the results.
                if len(splitWords) == wordsScore and search == item['slug']:
                    firstLevelMatchs.insert(0, resultObject)

                # If we found a match that have all words in it, prepend it in the results after first.
                elif len(splitWords) == wordsScore and item['slug'].split('_')[0] == search.split('_')[0]:
                    secondLevelMatchs.append(resultObject)

                # If we found a match that have all words in it, prepend it in the results after first.
                elif len(splitWords) == wordsScore:
                    thirdLevelMatchs.insert(1, resultObject)

                # Else fallback and append something that match a little
                elif search in item['slug']:
                    results.append(resultObject)

            results = firstLevelMatchs + secondLevelMatchs + thirdLevelMatchs + results

        # Update "update" result title
        if not os.path.isdir(JSON_DIR):
            title = 'Download JSON files'
        elif not self.wp_ref_version or self.wp_ref_version == '':
            title = 'Update JSON files'
        else:
            title = 'Update JSON files (Current WP version: ' + \
                self.wp_ref_version + ')'

        # Add "update" as result
        if not query or query == ' ' or len(query) <= 2 or query in 'update':
            results.append({
                'Title': title,
                'SubTitle': 'Update WordPress reference json files to latest version',
                'IcoPath': 'Images/app.ico',
                'JsonRPCAction': {
                    'method': 'Wox.ChangeQuery',
                    'parameters': ['wp update', True],
                    'dontHideAfterAction': True
                }
            })

        # Update action
        if query == 'update':
            try:
                self.get_json_files()

                results = []
                results.append({
                    'Title': 'Update done! WP v' + self.wp_ref_version,
                    'SubTitle': 'WordPress references are up-to-date.',
                    'IcoPath': 'Images/app.ico',
                    'JsonRPCAction': {
                        'method': 'Wox.ChangeQuery',
                        'parameters': ['wp ', True],
                        'dontHideAfterAction': True
                    }
                })
                return results

            except:
                self.debug('JSON files update failed...')

        return results


    # Make plural names
    def get_ref_plural_name(self, reference):
        if 'class' in reference:
            ref_plural = reference + 'es'
        else:
            ref_plural = reference + 's'
        return ref_plural

    def get_json_file_name(self, reference):
        json_name = self.get_ref_plural_name(reference) + '.json'
        return json_name

    def get_json_file_path(self, reference):
        json_name = self.get_json_file_name(reference)
        return os.path.join(JSON_DIR, json_name)

    def get_json_file(self, reference):
        json_name = self.get_json_file_name(reference)
        json_file = self.get_json_file_path(reference)
        json_url = 'https://raw.githubusercontent.com/keesiemeijer/alfred-wordpress-developer-workflow/master/' + json_name

        try:
            request = requests.get(json_url)
            distantFileContent = request.json()
            distantFileVersion = distantFileContent['version']

            if not self.wp_ref_version or self.wp_ref_version == '':
                self.wp_ref_version = distantFileVersion

            # If no json file found, try to fetch it and make local json file
            if not os.path.isfile(json_file):
                with open(json_file, 'w') as createFile:
                    json.dump(distantFileContent, createFile)

            # We have json, check version and fetch new one if outdated
            else:
                with open(json_file, 'r') as openFile:

                    localFileContent = json.load(openFile)
                    localJsonVersion = localFileContent['version']
                    if (localJsonVersion != distantFileVersion):
                        with open(json_file, 'w') as createFile:
                            json.dump(distantFileContent, createFile)

        except:
            self.debug('Error while trying to download "' + json_name + '", please try again :)')

    def get_json_files(self):
        for reference in REFERENCES:
            self.get_json_file(reference)

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

    # Create "Json" dir if it doesn't exist and grab json files
    def load_json(self):
        if not os.path.isdir(JSON_DIR):
            try:
                os.mkdir(JSON_DIR)
            except:
                self.debug('Error while making "Json" folder in the plugin directory')

if __name__ == "__main__":
    WordPressCodex()
