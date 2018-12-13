import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import textwrap

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

PlayersList = []
RatingsList = []
SeasonsList= []

globaldata = pd.DataFrame({"Players":PlayersList, "Ratings":PlayersList})
special = ["á","ó", "î", "ô", "û", "í", "é","â", "ê", "É", "ð","ć","ø","ú","ï","ö","ü","ğ","ë","ß","ř","ë","ä","š","Č","Ö","ç","ñ","ã","Ø", "ž", "Š", "ý", "à", "è", "ì", "ò", "ù", "Ã", "Á", "Ó", "Í", "Ú", "ę"]
latin = ["a", "o", "i", "o", "u", "i", "e", "a", "e", "E", "d","c","o","u","i","o","u","g","e","ss","r","e","a","s","C","O","c","n","a","o", "z", "S", "y", "a", "e", "i", "o", "u", "A", "A", "O", "I", "U", "e"]


#"https://www.fifaindex.com/players/fifa1" +str(s+4) +"_1" +str(s+3)+"/"+ str(p+1)+ "/?league=13&order=desc"
for s in range(5):
    for p in range(22):
        urls = ["https://www.fifaindex.com/players/fifa14_13/" +str(p+1)+"/?league=13&order=desc",
                "https://www.fifaindex.com/players/fifa15_14/"+str(p+1)+"/?league=13&order=desc",
                "https://www.fifaindex.com/players/fifa16_73/"+str(p+1)+"/?league=13&order=desc",
                "https://www.fifaindex.com/players/fifa17_173/"+str(p+1)+"/?league=13&order=desc",
                "https://www.fifaindex.com/players/fifa18_278/"+str(p+1)+"/?league=13&order=desc"]
        page = urls[s]
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        Players = pageSoup.find_all("td", {"data-title": "Name"})
        Ratings = pageSoup.find_all("td", {"data-title": "OVR / POT"})
        RatingsList2 = []
        RatingsList3 = []
        for k in range(len(Players)):
            PlayersList.append(Players[k].text)
            RatingsList.append(Ratings[k].text)
            SeasonsList.append("201"+str(s+3))


        for z in range(len(RatingsList)):
            for w in range(0,len(RatingsList[z]),2):
                RatingsList2.append(RatingsList[z][w:w+2])
#print([word[i:i+3] for i in range(0, len(word), 3)])

        for y in range(len(RatingsList2)):
            if (y) % 2 == 0:
                RatingsList3.append(RatingsList2[y])

        # print(RatingsList)
        # print(RatingsList2)
        # print(RatingsList3)
        # print(len(RatingsList))
        # print(len(RatingsList2))
        # print(len(RatingsList3))
        for q in range(len(PlayersList)):
            for i in range(len(PlayersList[q])):
                for j in range(len(special)):
                    if PlayersList[q][i] == special[j]:
                        PlayersList[q]=PlayersList[q].replace(PlayersList[q][i],latin[j])

        df = pd.DataFrame({"Players":PlayersList, "Ratings":RatingsList3, "Season":SeasonsList})
        print(p+1)
        print("done")
    globaldata.append(df)
    print(s+4)
    print("season done")

df.to_csv("ratingdatafinal.csv", encoding='utf-8')
