from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
import csv
import io

app = Flask(__name__)
DB_FILE = 'database.db'

# Fonction pour initialiser la base de données au démarrage
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                montant REAL NOT NULL,
                type TEXT NOT NULL,
                categorie TEXT NOT NULL
            )
        ''')
    conn.close()

# Route principale : Affiche le tableau de bord
@app.route('/')
def index():
    init_db()  # S'assure que la table existe
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()
        
        # Calculs automatiques des totaux pour l'affichage
        total_revenus = sum(t['montant'] for t in transactions if t['type'] == 'Revenu')
        total_depenses = sum(t['montant'] for t in transactions if t['type'] == 'Depense')
        solde = total_revenus - total_depenses
        
        # Préparation des données pour le graphique camembert (Dépenses uniquement)
        categories_dict = {}
        for t in transactions:
            if t['type'] == 'Depense':
                categories_dict[t['categorie']] = categories_dict.get(t['categorie'], 0) + t['montant']
    
    return render_template('index.html', transactions=transactions, 
                           total_revenus=total_revenus, total_depenses=total_depenses, solde=solde,
                           labels=list(categories_dict.keys()), values=list(categories_dict.values()))

# Route pour AJOUTER un mouvement (Revenu ou Dépense)
@app.route('/add', methods=['POST'])
def add_transaction():
    titre = request.form.get('titre')
    montant = float(request.form.get('montant'))
    t_type = request.form.get('type')
    categorie = request.form.get('categorie')
    
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('INSERT INTO transactions (titre, montant, type, categorie) VALUES (?, ?, ?, ?)',
                     (titre, montant, t_type, categorie))
    return redirect(url_for('index'))

# Route pour SUPPRIMER un mouvement
@app.route('/delete/<int:id>')
def delete_transaction(id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('DELETE FROM transactions WHERE id = ?', (id,))
    return redirect(url_for('index'))

# Route pour EXPORTER les données en format CSV
@app.route('/export-csv')
def export_csv():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT titre, montant, type, categorie FROM transactions')
        rows = cursor.fetchall()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Titre', 'Montant', 'Type', 'Categorie']) # En-tête du fichier
    writer.writerows(rows)
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=rapport_depenses.csv"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)