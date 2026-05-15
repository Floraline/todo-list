from flask import Flask, render_template, request, redirect, session 
from database import lolinit
import sqlite3

app = Flask(__name__)
app.secret_key = "lol971!"

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        prenom = request.form["prenom"]
        mot_de_passe = request.form["mot_de_passe"]
        connexion = sqlite3.connect("todo.db")
        curseur = connexion.cursor()
        curseur.execute("INSERT INTO users (prenom, mot_de_passe) VALUES (?, ?)", (prenom, mot_de_passe))
        connexion.commit()
        connexion.close()
        return redirect("/connexion")
    return render_template("inscription.html")


@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        prenom = request.form["prenom"]
        mot_de_passe = request.form["mot_de_passe"]
        connexion = sqlite3.connect("todo.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM users WHERE prenom = ? AND mot_de_passe = ?", (prenom, mot_de_passe))
        utilisateur = curseur.fetchone()

        if utilisateur:
            session["user_id"] = utilisateur[0]
            connexion.close()
            return redirect("/")
        else:
            connexion.close()
            return render_template("connexion.html", erreur="Prénom ou mot de passe incorrect")
    return render_template("connexion.html")



@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect("/connexion")
    
    if request.method == "POST":
        # ajouter une tâche
        tache = request.form["tache"]
        important = request.form["important"]
        connexion = sqlite3.connect("todo.db")
        curseur = connexion.cursor()
        curseur.execute("INSERT INTO tasks (tache, important, statut, user_id) VALUES (?, ?, 0, ?)", (tache, important, session["user_id"]))
        connexion.commit()
        connexion.close()
        return redirect("/")
    
    # GET → récupérer les infos dans les tables
    connexion = sqlite3.connect("todo.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM tasks WHERE user_id = ?", (session["user_id"],))
    taches = curseur.fetchall()
    curseur.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
    utilisateur = curseur.fetchone()
    connexion.close()
    return render_template("index.html", taches=taches,utilisateur=utilisateur)

@app.route("/supprimer", methods=["POST"])
def supprimer():
    if request.method == "POST":
        id = request.form["id"]
        connexion = sqlite3.connect("todo.db")
        curseur = connexion.cursor()
        curseur.execute("DELETE FROM tasks WHERE id = ?", (id,))
        connexion.commit()
        connexion.close()
        return redirect("/")

@app.route("/terminer", methods=["POST"])
def terminer():
    if request.method == "POST":
        id = request.form["id"]
        connexion = sqlite3.connect("todo.db")
        curseur = connexion.cursor()
        curseur.execute("UPDATE tasks SET statut = 1 WHERE id = ?", (id,))
        connexion.commit()
        connexion.close()
        return redirect("/")

@app.route("/deco", methods=["GET"])
def deco():
    session. clear()
    return redirect("/connexion")



    
    
    
lolinit()
app.run(host='0.0.0.0', port=10000)