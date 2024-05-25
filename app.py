import json
from bs4 import BeautifulSoup
import requests
import re
from requests import post,get
from flask import Flask, render_template, request, session
from urllib.parse import quote
from flask_session import Session
import random
import os
import base64
import yaml

# Todo 
# 1. faire les requetes qui changent avec fichier de config 
# 2. CSS bigo


dinolist = open('dinolist.json', encoding='utf-8')
dataDino = json.load(dinolist) 

hunterlist = open('hunter.json', encoding='utf-8')
dataHunter = json.load(hunterlist) 

animauxlist = open('animaux.json', encoding='utf-8')
dataAnimaux = json.load(animauxlist) 


app = Flask(__name__)
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)

ListDinoOfDay = []
ListhunterOfDay = []
ListAnimalOfDay = []

@app.route('/routeToReset',methods=['GET','POST'])
def NewAll():
    #ajoute tous les randoms ici et je fais des listes comme pour for key,value
    dinoOfDay = randomDino()
    animalOfDay = randomAnimal()
    hunterOfDay = randomHunter()
    print(hunterOfDay,dinoOfDay)
    encoded_values = {}
    for key, value in dinoOfDay.items():

        encoded_values[key+"Dino"] = base64.b64encode(str(value).encode()).decode()

    for key, value in hunterOfDay.items():

        encoded_values[key] = base64.b64encode(str(value).encode()).decode()

    for key, value in animalOfDay.items():

        encoded_values[key] = base64.b64encode(str(value).encode()).decode()

    with open('config.yaml', 'w') as file:
        yaml.dump(encoded_values, file)


    return render_template("index.html")


def randomDino():
    dinochosen = random.choice(list(dataDino.keys()))
    dinoOfDay = dataDino[dinochosen]
    return dinoOfDay

def randomHunter():
    hunterchosen = random.choice(list(dataHunter.keys()))
    hunterOfDay = dataHunter[hunterchosen]
    return hunterOfDay

def randomAnimal():
    animalChosen = random.choice(list(dataAnimaux.keys()))
    animalOfDay = dataAnimaux[animalChosen]
    return animalOfDay

@app.route('/dinodle',methods=['GET','POST'])
def dinodle():
    textDisp = "Trouve Le bon dino !! "
    if request.method == "POST":
        dinoName = request.form.get('dino_name')
        if dinoName in dataDino:
            session["ListTry"].append(dataDino[dinoName])
        else :
            textDisp = "Nom de Dino pas valide !!"
    else : 
        session["ListTry"] = []
        with open('config.yaml', 'r') as dataDayDinoFile:
            dataDayDino = yaml.safe_load(dataDayDinoFile)
            ListDinoOfDay.clear()
            ListDinoOfDay.append(dataDayDino["nameDino"])
            ListDinoOfDay.append(dataDayDino["dietDino"])
            ListDinoOfDay.append(dataDayDino["epochDino"])
            ListDinoOfDay.append(dataDayDino["locomotionDino"])
            ListDinoOfDay.append(dataDayDino["locationDino"])
            ListDinoOfDay.append(dataDayDino["weightDino"])
            ListDinoOfDay.append(dataDayDino["heightDino"])

    return render_template('dinodle.html',ListTry=reversed(session["ListTry"]),ListOfDay=ListDinoOfDay,data=dataDino,textDisp=textDisp)


@app.route('/hunterdle',methods=['GET','POST'])
def hunterdle():
    textDisp = "Trouve le bon Personnage !! "
    if request.method == "POST":
        hunterName = request.form.get('hunter_name')
        if hunterName in dataHunter:
            session["ListTry"].append(dataHunter[hunterName])
        else :
            textDisp = "Nom de Personnage pas valide !!"
    else : 
        session["ListTry"] = []
        with open('config.yaml', 'r') as dataDayHunterFile:
            dataDayhunter = yaml.safe_load(dataDayHunterFile)
            ListhunterOfDay.clear()
            ListhunterOfDay.append(dataDayhunter["nameHunter"])
            ListhunterOfDay.append(dataDayhunter["nenType"])
            ListhunterOfDay.append(dataDayhunter["genreHunter"])
            ListhunterOfDay.append(dataDayhunter["occupationHunter"])
            ListhunterOfDay.append(dataDayhunter["affiliationHunter"])
            ListhunterOfDay.append(dataDayhunter["arcHunter"])
            ListhunterOfDay.append(dataDayhunter["couleurCheuveuxHunter"])

    return render_template('hunter.html',ListTry=reversed(session["ListTry"]),ListOfDay=ListhunterOfDay,data=dataHunter,textDisp=textDisp)


@app.route('/animaldle',methods=['GET','POST'])
def animaldle():
    textDisp = "Trouve le bon Animal !! "
    if request.method == "POST":
        animalName = request.form.get('animal_name')
        if animalName in dataAnimaux:
            session["ListTry"].append(dataAnimaux[animalName])
        else :
            textDisp = "Nom d'animal pas valide !!"
    else : 
        session["ListTry"] = []
        with open('config.yaml', 'r') as dataDayAnimalFile:
            dataDayAnimal = yaml.safe_load(dataDayAnimalFile)
            ListAnimalOfDay.clear()
            ListAnimalOfDay.append(dataDayAnimal["nameAnimal"])
            ListAnimalOfDay.append(dataDayAnimal["classeAnimal"])
            ListAnimalOfDay.append(dataDayAnimal["familleAnimal"])
            ListAnimalOfDay.append(dataDayAnimal["habitatAnimal"])
            ListAnimalOfDay.append(dataDayAnimal["regimeAnimal"])
            ListAnimalOfDay.append(dataDayAnimal["poidsAnimal"])
            ListAnimalOfDay.append(dataDayAnimal["tailleAnimal"])

    return render_template('animal.html',ListTry=reversed(session["ListTry"]),ListOfDay=ListAnimalOfDay,data=dataAnimaux,textDisp=textDisp)

@app.route('/',methods=['GET','POST'])
def mainMenu():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)),debug=False)