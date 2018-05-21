# -*- coding: utf-8 -*-
"""
Created on Thu May  3 15:45:14 2018

beginning of fun lol api coding

@author: Spencer
"""

#import necessary libraries
import json
import urllib

#initializations
apikey='RGAPI-9a6a7643-8ef8-4795-98bf-e648cc8ebb26'
champId={}
champIdInv={}
champAlph=()

"""
example call
print(json.loads(urllib.request.urlopen(
'https://na1.api.riotgames.com/lol/static-data/v3/champions?api_key=RGAPI-830909d0-99e2-4394-afdf-3c074eee9ae7').read()))
"""

class lolapi:
    
    def __init__(self, api_key, region='na1'):
        self.api_key = api_key
        self.region = region
        self.cache = {}
        
    def apiCall(self, category, function):
                return json.loads(urllib.request.urlopen('https://' + self.region + '.api.riotgames.com/lol/' + category + '/v3/' +
                                                         function + '?api_key=' + self.api_key).read())

    def getId(self, summonerName):
        #returns ID of given name for use in lookup by ID
        if summonerName not in self.cache:
            id = self.apiCall('summoner', 'summoners/by-name/'+summonerName)['id']
            self.cache[summonerName] = id
        return self.cache[summonerName]
    
    def summonerStats(self, summonerName):
        id = self.getId(summonerName)
        return self.apiCall('summoner', 'summoners/'+str(id))
    
    def allMasteries(self, summonerName):
        id = self.getId(summonerName)
        return self.apiCall('champion-mastery','champion-masteries/by-summoner/'+str(id))
    
    def championMastery(self, summonerName, champion):
        if champion in champId:
            id = self.getId(summonerName)
            thisId = champId[champion]
            return self.apiCall('champion-mastery','champion-masteries/by-summoner/'+str(id)+'/by-champion/'+str(thisId))
        else:
            print('Not a valid champion.')
            return
    
    
    
#initialize object and useful lists
b=lolapi(apikey)
championsFull = b.apiCall('static-data','champions')['data']
for champ in championsFull:
    champId[champ] = championsFull[champ]['id']
    champIdInv[championsFull[champ]['id']]=champ
champAlf = sorted(championsFull)
    


def listNeededTokens(summonerName,api=b):
    m5 = {}
    m6 = {}
    for champ in api.allMasteries(summonerName):
        if champ['championLevel'] == 5 and champ['tokensEarned'] != 2:
            m5[champIdInv[champ['championId']]] = 2-champ['tokensEarned']
        elif champ['championLevel'] == 6 and champ['tokensEarned'] != 3:
            m6[champIdInv[champ['championId']]] = 3-champ['tokensEarned']
    print('Mastery 6:\n')
    for champ in sorted(m6):
        print(champ + ' - ' + str(m6[champ]))
    print('\n\nMastery 5:\n')
    for champ in sorted(m5):
        print(champ + ' - ' + str(m5[champ]))
    return




