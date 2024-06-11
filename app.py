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

landscape_dico = {
    'Afghanistan': 'Asie',
    'Albanie': 'Europe',
    'Algérie': 'Afrique',
    'Argentine': 'Amérique du Sud',
    'Australie': 'Océanie',
    'Autriche': 'Europe',
    'Bangladesh': 'Asie',
    'Belgique': 'Europe',
    'Brésil': 'Amérique du Sud',
    'Canada': 'Amérique du Nord',
    'Chine': 'Asie',
    'Colombie': 'Amérique du Sud',
    'République tchèque': 'Europe',
    'Danemark': 'Europe',
    'Égypte': 'Afrique',
    'Éthiopie': 'Afrique',
    'Finlande': 'Europe',
    'France': 'Europe',
    'Allemagne': 'Europe',
    'Grèce': 'Europe',
    'Hongrie': 'Europe',
    'Inde': 'Asie',
    'Indonésie': 'Asie',
    'Iran': 'Asie',
    'Irak': 'Asie',
    'Irlande': 'Europe',
    'Israël': 'Asie',
    'Italie': 'Europe',
    'Japon': 'Asie',
    'Jordanie': 'Asie',
    'Kenya': 'Afrique',
    'Liban': 'Asie',
    'Libye': 'Afrique',
    'Malaisie': 'Asie',
    'Mexique': 'Amérique du Nord',
    'Maroc': 'Afrique',
    'Népal': 'Asie',
    'Pays-Bas': 'Europe',
    'Nouvelle-Zélande': 'Océanie',
    'Nigéria': 'Afrique',
    'Norvège': 'Europe',
    'Pakistan': 'Asie',
    'Pérou': 'Amérique du Sud',
    'Philippines': 'Asie',
    'Pologne': 'Europe',
    'Portugal': 'Europe',
    'Roumanie': 'Europe',
    'Russie': 'Europe',
    'Arabie saoudite': 'Asie',
    'Singapour': 'Asie',
    'Afrique du Sud': 'Afrique',
    'Corée du Sud': 'Asie',
    'Espagne': 'Europe',
    'Sri Lanka': 'Asie',
    'Soudan': 'Afrique',
    'Suède': 'Europe',
    'Suisse': 'Europe',
    'Syrie': 'Asie',
    'Thaïlande': 'Asie',
    'Tunisie': 'Afrique',
    'Turquie': 'Europe',
    'Ouganda': 'Afrique',
    'Ukraine': 'Europe',
    'Émirats arabes unis': 'Asie',
    'Royaume-Uni': 'Europe',
    'États-Unis': 'Amérique du Nord',
    'Venezuela': 'Amérique du Sud',
    'Viêt Nam': 'Asie',
    'Yémen': 'Asie',
    'Zimbabwe': 'Afrique',
    'Islande': 'Europe',
    'Luxembourg': 'Europe',
    'Monaco': 'Europe',
    'Saint-Marin': 'Europe',
    'Liechtenstein': 'Europe',
    'Malte': 'Europe',
    'Andorre': 'Europe',
    'Lettonie': 'Europe',
    'Estonie': 'Europe',
    'Lituanie': 'Europe',
    'Slovaquie': 'Europe',
    'Slovénie': 'Europe',
    'Croatie': 'Europe',
    'Bosnie-Herzégovine': 'Europe',
    'Serbie': 'Europe',
    'Monténégro': 'Europe',
    'Macédoine du Nord': 'Europe',
    'Kosovo': 'Europe',
    'Arménie': 'Asie',
    'Azerbaïdjan': 'Asie',
    'Géorgie': 'Europe',
    'Kazakhstan': 'Asie',
    'Koweït': 'Asie',
    'Oman': 'Asie',
    'Qatar': 'Asie',
    'Bahreïn': 'Asie',
    'Chypre': 'Europe',
    'Bhoutan': 'Asie',
    'Maldives': 'Asie',
    'Bolivie': 'Amérique du Sud',
    'Paraguay': 'Amérique du Sud',
    'Uruguay': 'Amérique du Sud',
    'Guyana': 'Amérique du Sud',
    'Suriname': 'Amérique du Sud',
    'Equateur': 'Amérique du Sud',
    'Chili': 'Amérique du Sud',
    'Honduras': 'Amérique centrale',
    'Guatemala': 'Amérique centrale',
    'Salvador': 'Amérique centrale',
    'Nicaragua': 'Amérique centrale',
    'Costa Rica': 'Amérique centrale',
    'Panama': 'Amérique centrale',
    'Jamaïque': 'Caraïbes',
    'Bahamas': 'Caraïbes',
    'Barbade': 'Caraïbes',
    'Cuba': 'Caraïbes',
    'Haïti': 'Caraïbes',
    'Madagascar': 'Afrique',
    'Turkménistan': 'Asie',
    'Ouzbékistan': 'Asie',
    'Kirghizistan': 'Asie',
}


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

def chooseNewCountry():
    Limgs = []
    session["country"], session["continent"] = random.choice(list(landscape_dico.items()))
    url = "https://www.bing.com/images/search?q="+session["country"]+"+city&form=HDRSC4&first=1"
    html_data = requests.get(url).text
    soup = BeautifulSoup(html_data, "html.parser")
    divTag = soup.find_all("div",id="b_content")
    soup2 = BeautifulSoup(str(divTag), "html.parser")
    imgTags = soup2.find_all("a")
    pattern = r'murl":"(.*?)",'
    for i in imgTags:
        match = re.search(pattern, str(i))
        if match:
            extracted_text = match.group(1)
            Limgs.append(extracted_text)

    session["img"] = random.choice(Limgs)


@app.route('/landscape',methods=['GET','POST'])
def landscape():
    if request.method == 'GET':
        session["continentFoud"] = 0
        session["country"]= ""
        session["continent"] = ""
        session["img"] = ""
        textVar = "D'où vient ce paysage ??"
        session["textContinent"] = "?"
        chooseNewCountry()
    elif request.method == 'POST':
        if session["continentFoud"] == 0:
            name = request.form["name"]
            if name in landscape_dico :
                if landscape_dico[name] == session["continent"]:
                    session["continentFound"] = 1
                    session["textContinent"] = session["continent"]
                if name == session["country"]:
                    textVar = "Bravo c'était bien "+name
                else :
                    textVar = "Non essaye encore..." 
            else :
                textVar = "Pays Inconnu" 
    return render_template("landscape.html",continent=session["textContinent"],img = session["img"],textVar = textVar,data = landscape_dico)

@app.route('/showansw', methods=['GET', 'POST'])
def answr():
    textVar = "C'était "+session["country"]
    return render_template("landscape.html",continent=session["continent"],img = session["img"],textVar = textVar,data = landscape_dico)


@app.route('/',methods=['GET','POST'])
def mainMenu():
    return render_template('index.html')

@app.route('/index2',methods=['GET','POST'])
def index2():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)),debug=True)