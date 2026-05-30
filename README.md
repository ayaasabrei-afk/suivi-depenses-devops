#  Application de Suivi de Dépenses Personnelles (Module DevOps)

[![Flask App CI Pipeline](https://github.com/ayaasabrei-afk/suivi-depenses-devops/actions/workflows/ci.yml/badge.svg)](https://github.com/ayaasabrei-afk/suivi-depenses-devops/actions)

Ce projet consiste en une application web de gestion et de suivi de dépenses personnelles, développée avec le framework **Flask** et une persistance des données sous **SQLite**. Ce mini-projet met en œuvre une chaîne DevOps complète intégrant l'Intégration Continue (CI) et la conteneurisation.

---

##  Fonctionnalités Applicatives
* 🛒 **Gestion CRUD :** Saisie, consultation et suppression des dépenses et revenus par catégorie (alimentation, transport, loisirs, etc.).
*  **Visualisation :** Graphiques mensuels (camemberts et histogrammes) pour analyser le budget.
*  **Exportation :** Extraction instantanée des données au format CSV.

---

## 🛠️ Architecture et Technologies DevOps

### 1. Gestion de Versions (Git)
* Respect d'un workflow professionnel avec une branche de développement (`develop`) et une branche de production stable (`main`).
* Messages de commit normalisés suivant la convention *Conventional Commits*.

### 2. Intégration Continue (CI) - GitHub Actions
Le pipeline d'intégration continue est décrit dans `.github/workflows/ci.yml`. Il se déclenche automatiquement à chaque `push` et `pull_request`. Il assure :
* L'isolation de l'environnement virtuel (Python 3.10).
* L'installation rigoureuse des dépendances listées dans `requirements.txt`.
* L'exécution automatisée des tests unitaires via `pytest`.

### 3. Conteneurisation - Docker & Docker Compose
* **Dockerfile :** Optimisé via un *Multi-stage build* (étape `builder` pour la compilation des dépendances et étape `runner` ultra-légère pour l'exécution).
* **Docker Compose :** Permet d'isoler l'application et de garantir sa portabilité complète sur n'importe quel environnement Linux, Windows ou macOS.

---

##  Lancement et Déploiement Local

L'application a été entièrement conteneurisée pour être reproductible. Vous pouvez la cloner et la lancer en local à l'aide d'une commande unique.

### Prérequis
* Docker installé sur votre machine.
* Docker Compose activé.

### Instructions de démarrage
1. Clonez le dépôt et placez-vous à la racine du projet.
2. Exécutez la commande suivante dans votre terminal :
```bash
docker-compose up --build