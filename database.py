import psycopg2
import os

def lolinit():
    connexion = psycopg2.connect(os.environ.get("DATABASE_URL"))
    curseur = connexion.cursor()
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            prenom TEXT,
            mot_de_passe TEXT
        )
    """)
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            tache TEXT,
            important INTEGER,
            statut INTEGER,
            user_id INTEGER
        )
    """)
    connexion.commit()
    connexion.close()

lolinit()