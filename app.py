from flask import Flask , render_template, request
from flask import redirect

import sqlite3

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')


#confiuration de la base de donnees SQLITE
db_name = 'emargement.db'


#page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

conn = sqlite3.connect(db_name)
c = conn.cursor()

# Création de la table emargement
c.execute("CREATE TABLE IF NOT EXISTS emargement (nom TEXT, prenom TEXT, numero TEXT, email TEXT)")

conn.commit()
conn.close()

#page de soumission du formulaire
@app.route('/submit', methods=['POST'])
def submit():
    nom = request.form['nom']
    prenom = request.form['prenom']
    numero = request.form['numero']
    email = request.form['email']
    
    #connexion a la base de donnees
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    #Insertion des donnees dans la base de donnees
    c.execute("INSERT INTO emargement (nom, prenom, numero, email) VALUES (?, ?, ?, ?)", (nom, prenom, numero, email))


    conn.commit()
    
    #Fermeture de la connexion a la base de donnees
    conn.close()
    
    return redirect('/success')
#Page de succes apres soumission du formulaire
@app.route('/success')
def success():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # Récupération des données d'emargement depuis la base de données
    c.execute("SELECT nom, prenom, numero, email FROM emargement")
    emargement_data = c.fetchall()
    
    # Fermeture de la connexion à la base de données
    conn.close()

    # Retourner le template 'success.html' avec les données récupérées
    return render_template('success.html', emargement_data=emargement_data)



if __name__ == '__main__':
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS emargement (nom TEXT, prenom TEXT, numero TEXT, email TEXT)")



    conn.close()
    
    app.run(debug=True)
    
    