#!/usr/bin/env python3
import subprocess
import secrets
import string
# script d'automatisation en **Python** conçu pour simplifier l'intégration des nouveaux collaborateurs

# Liste des utilisateurs à créer (Prénom, Nom, Groupe)
UTILISATEURS_A_CREER = [
    {"prenom": "jean", "nom": "dupont", "groupe": "IT"},
    {"prenom": "marie", "nom": "curie", "groupe": "Direction"},
    {"prenom": "albert", "nom": "einstein", "groupe": "IT"},
    {"prenom": "lucie", "nom": "aubrac", "groupe": "Direction"}
]

def generer_mot_de_passe_complexe(longueur=12):
    """Génère un mot de passe respectant les critères de complexité AD"""
    maj = string.ascii_uppercase
    min = string.ascii_lowercase
    chiffres = string.digits
    symboles = "!#$%"
    
    # S'assurer d'avoir au moins un caractère de chaque catégorie
    pwd = [
        secrets.choice(maj),
        secrets.choice(min),
        secrets.choice(chiffres),
        secrets.choice(symboles)
    ]
    
    # Remplir le reste
    tout = maj + min + chiffres + symboles
    pwd += [secrets.choice(tout) for _ in range(longueur - 4)]
    
    # Mélanger pour éviter que le début soit prévisible
    secrets.SystemRandom().shuffle(pwd)
    return "".join(pwd)

def executer_commande_samba(commande):
    """Exécute une commande système et retourne le statut"""
    try:
        resultat = subprocess.run(commande, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True, resultat.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

print("Début de l'automatisation de création des utilisateurs Samba AD...\n")

for user in UTILISATEURS_A_CREER:
    username = f"{user['prenom']}.{user['nom']}".lower()
    nom_complet = f"{user['prenom'].capitalize()} {user['nom'].upper()}"
    mot_de_passe = generer_mot_de_passe_complexe()
    
    print(f"Traitement de l'utilisateur : {nom_complet} ({username})")
    
    # 1. Création de l'utilisateur dans Samba AD
    cmd_creation = f"sudo samba-tool user create {username} '{mot_de_passe}' --userou='OU=Utilisateurs,OU=Entreprise_MNA' --given-name='{user['prenom'].capitalize()}' --surname='{user['nom'].upper()}'"
    
    succes, message = executer_commande_samba(cmd_creation)
    
    if succes:
        print(f" ✅ Utilisateur créé avec succès.")
        print(f" 🔑 Mot de passe généré : {mot_de_passe}")
        
        # 2. Ajout de l'utilisateur dans son groupe AD respectif
        cmd_groupe = f"sudo samba-tool group addmembers {user['groupe']} {username}"
        succes_gp, msg_gp = executer_commande_samba(cmd_groupe)
        
        if succes_gp:
            print(f" Ajouté au groupe '{user['groupe']}' avec succès.")
        else:
            print(f" Erreur d'ajout au groupe : {msg_gp.strip()}")
            
    else:
        # Si l'utilisateur existe déjà par exemple
        print(f" Erreur lors de la création : {message.strip()}")
        
    print("-" * 50)

print("\n Fin du script d'automatisation.")
