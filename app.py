from flask import Flask, render_template,url_for

app = Flask(__name__)


# Calcul du score maximal
max_score:float = 100.0#sum(cell['weight'] for row in rows for cell in row['parts'])

def addImageHtmlCode(imgFileName:str) -> str:
    if (imgFileName!=None):
        return f"<img src=\"{url_for('static', filename=f'images/{imgFileName}')}\" width=\"100%\">"
    return ""

def createTooltipContent(text:str, imgFileName:str=None) -> str:
    return f"<div class=\"tooltip-container\">    <span class=\"info-icon\">&nbsp;&nbsp;🛈</span>    <div class=\"tooltip-content\">      {addImageHtmlCode(imgFileName)}       <p>{text}</p>    </div>  </div>"

def createLinkedTooltipContent(text:str, imgFileName:str=None) -> str:
    return f"<div class=\"tooltip-container\">    <span class=\"info-icon\">&nbsp;&nbsp;🛈</span>    <div class=\"tooltip-content\">      <a href=\"{url_for('static', filename=f'images/{imgFileName}')}\" target=_blank>{addImageHtmlCode(imgFileName)}</a>       <p>{text}</p>    </div>  </div>"

@app.route('/')
def index():
    # Définir la structure du tableau avec poids
    rows = [
    {"title": "Déplacement domicile travail bas carbone"+createTooltipContent("vélo, marche, transport en commun, co-voiturage, télétravail"), "parts": [
        {"text": "0 jour par semaine", "weight": 0},
        {"text": "1 jour par semaine", "weight": 1*4.3},
        {"text": "2 jour par semaine", "weight": 2*4.3, "checked":True},
        {"text": "3 jour par semaine", "weight": 3*4.3},
    ]},
    {"title": "Vie au laboratoire:<br> Restauration événementielle", "parts": [
        {"text": "repas bas carbone, 50% végétarien", "weight": 1},
        {"text": "repas bas carbone, 75% végétarien", "weight": 1.5, "checked":True},
        {"text": "repas bas carbone, 100% végétarien", "weight": 2},
    ]},
     {"title": "Vie au laboratoire:<br> Déjeuner"+createLinkedTooltipContent("Impact moyen de différents types de repas (source ademe)" ,"impact_co2_dejeuner.png"), "parts": [
        {"text": "1 déjeuner par semaine < 1KCo2e", "weight": 1*1.76},
        {"text": "2 déjeuner par semaine < 1KCo2e", "weight": 2*1.76},
        {"text": "3 déjeuner par semaine < 1KCo2e", "weight": 3*1.76, "checked":True},
        {"text": "4 déjeuner par semaine < 1KCo2e", "weight": 4*1.76},
    ]},
    {"title": "Missions: <br>report avion -> train", "parts": [
        {"text": "report si < 5 heures", "weight": 0.3},
        {"text": "report si < 8 heures", "weight": 9*0.323, "checked":True},
    ]},
    {"title": "Missions: <br>quota", "parts": [
        {"text": "Pas de quota", "weight": 0},
        {"text": "9 tonnes sur 3 ans glissants", "weight": 7.5*0.323},
        {"text": "6 tonnes sur 3 ans glissants", "weight": 12*0.323, "checked":True},
        {"text": "4.5 tonnes sur 3 ans glissants", "weight": 18*0.323},
        {"text": "3 tonnes sur 3 ans glissants", "weight": 29*0.323},
    ]},
]



    return render_template('index.html', rows=rows, max_score=max_score)

if __name__ == '__main__':
    app.run(debug=True)
