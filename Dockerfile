# Étape 1 : Construction et isolation des dépendances (Builder)
FROM python:3.10-slim AS builder

WORKDIR /app

# Installation de gcc nécessaire pour compiler certaines extensions Python
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Installation des dépendances dans le dossier local de l'utilisateur root
RUN pip install --no-cache-dir --user -r requirements.txt


# Étape 2 : Image finale d'exécution (Runner) - Ultra légère
FROM python:3.10-slim AS runner

WORKDIR /app

# On copie uniquement les dépendances installées à l'étape 1 sans s'encombrer de gcc
COPY --from=builder /root/.local /root/.local
COPY . .

# Mise à jour du PATH pour que Python trouve les bibliothèques installées
ENV PATH=/root/.local/bin:$PATH

# Le conteneur écoutera sur le port 5000
EXPOSE 5000

# Commande de démarrage du serveur Flask
CMD ["python", "app.py"]