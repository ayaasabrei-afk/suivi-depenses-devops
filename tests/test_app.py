import pytest
from app import app, init_db
import os

@pytest.fixture
def client():
    """Configure l'application en mode Test et crée un client virtuel"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        init_db()  # Initialise une base de données propre pour le test
        yield client
    # Nettoyage après le test : on supprime la base de test
    if os.path.exists('database.db'):
        os.remove('database.db')

def test_index_page(client):
    """Vérifie que la page d'accueil s'affiche et répond correctement"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Mon Suivi de D\xc3\xa9penses" in response.data

def test_add_transaction(client):
    """Vérifie qu'un utilisateur peut ajouter un mouvement avec succès"""
    response = client.post('/add', data={
        'titre': 'Mon Salaire de Test',
        'montant': '5000',
        'type': 'Revenu',
        'categorie': 'Salaire'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"5000.0 DH" in response.data