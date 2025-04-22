from flask import Flask, render_template

app = Flask(__name__)

# Définir la structure du tableau avec poids
rows = [
    {"title": "Déplacement Domicile Travail bas carbone <br>(vélo, bus, covoiturage, télétravail)", "parts": [
        {"text": "0 jour par semaine", "weight": 0},
        {"text": "1 jour par semaine", "weight": 1*5},
        {"text": "2 jour par semaine", "weight": 2*5, "checked":True},
        {"text": "3 jour par semaine", "weight": 3*5},
    ]},
    {"title": "Vie au laboratoire:<br> Restauration événementielle", "parts": [
        {"text": "repas bas carbone, 50% végétarien", "weight": 1},
        {"text": "repas bas carbone, 75% végétarien", "weight": 1.5, "checked":True},
        {"text": "repas bas carbone, 100% végétarien", "weight": 2},
    ]},
     {"title": "Vie au laboratoire:<br> Déjeuner", "parts": [
        {"text": "1 déjeuner par semaine < 1KCo2e", "weight": 1*2.8},
        {"text": "2 déjeuner par semaine < 1KCo2e", "weight": 2*2.8},
        {"text": "3 déjeuner par semaine < 1KCo2e", "weight": 3*2.8, "checked":True},
        {"text": "4 déjeuner par semaine < 1KCo2e", "weight": 4*2.8},
    ]},
    {"title": "Missions: <br>report avion -> train", "parts": [
        {"text": "report si < 5 heures", "weight": 0.3},
        {"text": "report si < 8 heures", "weight": 9*0.4, "checked":True},
    ]},
    {"title": "Missions: <br>quota", "parts": [
        {"text": "Pas de quota", "weight": 0},
        {"text": "9 tonnes sur 3 ans glissants", "weight": 7.5*0.4},
        {"text": "6 tonnes sur 3 ans glissants", "weight": 12*0.4},
        {"text": "4.5 tonnes sur 3 ans glissants", "weight": 18*0.4, "checked":True},
        {"text": "3 tonnes sur 3 ans glissants", "weight": 29*0.4},
    ]},
]

# Calcul du score maximal
max_score = 100#sum(cell['weight'] for row in rows for cell in row['parts'])

@app.route('/')
def index():
    return render_template('index.html', rows=rows, max_score=max_score)

if __name__ == '__main__':
    app.run(debug=True)
