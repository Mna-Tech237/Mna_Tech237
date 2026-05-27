# Lab d'Architecture SecOps : Contrôleur de Domaine Samba AD & SIEM Wazuh

Ce projet présente la mise en place complète d'une infrastructure d'entreprise sécurisée et supervisée, déployée dans un environnement de test (Lab) sous **Debian**. L'objectif est de simuler un réseau d'entreprise hybride où les clients distants accèdent aux ressources internes de manière sécurisée tout en étant audités en temps réel.

---

## Architecture du Réseau

L'architecture repose sur l'interconnexion de plusieurs composants clés à travers un réseau local et un tunnel VPN maillé :

* **Contrôleur de Domaine (DC) :** Debian Server configuré avec Samba AD DC (`192.168.100.5`).
  
* **Serveur DNS :** BIND9 intégré à Samba (via le module DLZ) pour la résolution interne et la gestion des enregistrements SRV Active Directory.
 
* **Supervision SIEM :** Serveur **Wazuh** (Indexer, Manager et Dashboard) installé sur le même hôte pour la détection d'intrusions et l'analyse de logs.
  
* **Réseau privé virtuel :** **Tailscale** utilisé pour permettre la jonction sécurisée et la gestion de clients Windows géographiquement distants.

---

## Technologies & Services Utilisés

* **OS :** Debian (Serveur), Windows 10/11 Pro (Client distant)
  
* **Annuaire & Fichiers :** Samba4 (Active Directory), protocoles SMB/CIFS, ACLs POSIX
  
* **Réseau :** BIND9, Tailscale (VPN), UFW (Pare-feu)
  
* **Sécurité / Supervision :** Wazuh (HIDS/SIEM), Protocoles TLS/HTTPS (Apache2 avec redirection automatique)

---

## Fonctionnalités Implémentées

### 1. Gestion des Identités & Droits (Active Directory)
* Provisionnement du domaine `mnalab.com`.
  
* Création d'Unités d'Organisation (OU), de groupes (`IT`, `Direction`) et d'utilisateurs via `samba-tool`.
  
* Administration graphique à distance depuis le client Windows via les outils **RSAT** (`dsa.msc`, `gpmc.msc`).

### 2. Partage de Fichiers Sécurisé (Serveur NAS/Samba)
* Mise en place de partages réseau avec restriction stricte par groupe AD via la configuration du fichier `smb.conf`.
  
* Application de permissions Linux de type `770` pour garantir le cloisonnement des données (Ex: accès refusé au groupe `IT` sur le dossier `Direction`).

### 3. Réseau Distant & Résolution de Noms (Split DNS)
* Configuration de Tailscale pour encapsuler le trafic Active Directory sensible (Kerberos, LDAP, RPC).
  
* Mise en place d'un système **Split DNS** sur la console Tailscale redirigeant uniquement les requêtes de la zone `mnalab.com` vers le serveur BIND9 de la Debian.
  
* Sécurisation du pare-feu **UFW** en restreignant l'accès aux ports d'authentification AD uniquement pour l'interface `tailscale0`.

### 4. Serveur Web & Durcissement (Hardening HTTPS)
* Déploiement d'un serveur web Apache2 pour l'intranet.
  
* Activation des modules SSL/Rewrite et configuration d'un hôte virtuel pour **forcer la redirection automatique du HTTP vers le HTTPS** afin de chiffrer tous les flux.

### 5. Surveillance Centralisée (SIEM Wazuh)
* Installation de la pile Wazuh pour collecter, analyser et corréler les événements de sécurité de l'infrastructure.
* Surveillance des tentatives de connexion sur l'annuaire, des modifications de fichiers et détection des comportements suspects.

---
