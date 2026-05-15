import sqlite3
def lolinit(): 
    connexion = sqlite3.connect("todo.db")
    curseur = connexion.cursor()

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT,
            mot_de_passe TEXT
        );
    """)

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tache TEXT,
            important INTEGER,
            statut INTEGER,
            user_id INTEGER
        );
    """)
    connexion.commit() 
    connexion.close()

lolinit()