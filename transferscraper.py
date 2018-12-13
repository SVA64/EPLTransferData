#https://www.transfermarkt.co.uk/transfers/transferrekorde/statistik?saison_id=2016&land_id=0&ausrichtung=&spielerposition_id=&altersklasse=&leihe=&w_s=w&plus=1
#https://www.transfermarkt.co.uk/transfers/transferrekorde/statistik?ajax=yw2&altersklasse=&ausrichtung=&land_id=0&leihe=&page=2&plus=1&saison_id=2016&sort=nummer&spielerposition_id=&w_s=w

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

SeasonsList = []
PlayersList = []
AgesList = []
SellingteamsList = []
BuyingteamsList = []
MarketvaluesList = []
FeesList = []

totaldata = pd.DataFrame({"Season":SeasonsList, "Players":PlayersList, "Ages":AgesList, "Selling Team":SellingteamsList, "Buying Team":BuyingteamsList, "Marketvalues":MarketvaluesList, "Fees":FeesList})
for s in range(5):
    for p in range(10):
        page = "https://www.transfermarkt.co.uk/transfers/transferrekorde/statistik?ajax=yw2&altersklasse=&ausrichtung=&land_id=0&leihe=&page=" + str(p+1) + "&plus=1&saison_id=201" + str(s+3) + "&sort=nummer&spielerposition_id=&w_s=w"
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        Seasons = pageSoup.find_all("td", {"class": "zentriert"})
        Players = pageSoup.find_all("a", {"class": "spielprofil_tooltip"})
        Ages = pageSoup.find_all("td", {"class": "zentriert"})
        Sellingteams = pageSoup.find_all("a", {"class": "vereinprofil_tooltip"})
        Buyingteams = pageSoup.find_all("a", {"class": "vereinprofil_tooltip"})
        Marketvalues = pageSoup.find_all("td", {"class": "rechts"})
        Fees = pageSoup.find_all("td", {"class": "rechts"})
        special = ["á","ó", "î", "ô", "û", "í", "é","â", "ê", "É", "ð","ć","ø","ú","ï","ö","ü","ğ","ë","ß","ř","ë","ä","š","Č","Ö","ç","ñ","ã","Ø"]
        latin = ["a", "o", "i", "o", "u", "i", "e", "a", "e", "E", "d","c","o","u","i","o","u","g","e","ss","r","e","a","s","C","O","c","n","a","o"]


 #      poop = ["poop", "bob", "moon"]
 #      original = ["p", "o"]
 #      news = ["d", "x"]
 #      for c in range(len(poop)):
 #          for i in range(len(poop[c])):
 #              for j in range(len(original)):
 #                  if poop[c][i] == original[j]:
 #                      poop[c]=poop[c].replace(poop[c][i],news[j])
 #       print(poop)


        Marketvalues2 = []
        Fees2 = []

        for i in range(len(Marketvalues)):
            if (i) % 2 == 0:
                Marketvalues2.append(Marketvalues[i])
            elif (i+1) % 2 == 0:
                Fees2.append(Marketvalues[i])

        Buyingteams2 = []
        Sellingteams2 = []
        for i in range(len(Sellingteams)):
            if (i+3) % 4 == 0:
                Sellingteams2.append(Sellingteams[i])
            elif (i+1) % 4 == 0:
                Buyingteams2.append(Sellingteams[i])

        id = []
        Ages2=[]
        Seasons2=[]
        for j in range(len(Ages)):
            if j % 4 == 0:
                id.append(Ages[j])
            elif (j+2) % 4 == 0:
                Seasons2.append(Ages[j])
            elif (j+3) % 4 == 0:
                Ages2.append(Ages[j])

        for k in range(len(Players)):
            SeasonsList.append(Seasons2[k].text)
            PlayersList.append(Players[k].text)
            AgesList.append(Ages2[k].text)
            SellingteamsList.append(Sellingteams2[k].text)
            BuyingteamsList.append(Buyingteams2[k].text)
            MarketvaluesList.append(Marketvalues2[k].text)
            FeesList.append(Fees2[k].text)

        for q in range(len(PlayersList)):
            for i in range(len(PlayersList[q])):
                for j in range(len(special)):
                    if PlayersList[q][i] == special[j]:
                        PlayersList[q]=PlayersList[q].replace(PlayersList[q][i],latin[j])

        for q in range(len(SellingteamsList)):
            for i in range(len(SellingteamsList[q])):
                for j in range(len(special)):
                    if SellingteamsList[q][i] == special[j]:
                        SellingteamsList[q]=SellingteamsList[q].replace(SellingteamsList[q][i],latin[j])

        for q in range(len(BuyingteamsList)):
            for i in range(len(BuyingteamsList[q])):
                for j in range(len(special)):
                    if BuyingteamsList[q][i] == special[j]:
                        BuyingteamsList[q]=BuyingteamsList[q].replace(BuyingteamsList[q][i],latin[j])

        df = pd.DataFrame({"Season":SeasonsList, "Players":PlayersList, "Ages":AgesList, "Selling Team":SellingteamsList, "Buying Team":BuyingteamsList, "Marketvalues":MarketvaluesList, "Fees":FeesList})
        totaldata.append(df)
        print(p)
        print("done")
    print(s+3)
    print("season done")

df.to_csv("2013-2017transferdatafinal.csv", encoding='utf-8')
