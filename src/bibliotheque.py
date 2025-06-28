from exceptions import (
    LivreIndisponibleError,
    QuotaEmpruntDepasseError,
    MembreInexistantError,
    LivreInexistantError
)
#_______________________________________________________Class Livre__________________________________________________________________________________
class Livre:
    def __init__(self,ISBN,titre,auteur,annee,genre,statut):
        self.ISBN=ISBN
        self.titre=titre
        self.auteur=auteur
        self.annee=annee
        self.genre=genre
        self.statut=statut
    def __str__(self):
         return f"{self.titre} par {self.auteur} ({self.annee}) - {self.statut}"
    def __repr__(self):
         return f"Livre('{self.ISBN}', '{self.titre}', '{self.auteur}', {self.annee}, '{self.genre}', '{self.statut}')"
    def to_dict(self):
        return {
            "ISBN": self.ISBN,
            "titre": self.titre,
            "auteur": self.auteur,
            "annee": self.annee,
            "genre": self.genre,
            "statut": self.statut
        }
    @classmethod
    def from_dict(cls, data: dict):
    
         return cls(
            ISBN=data['ISBN'],
            titre=data['titre'],
            auteur=data['auteur'],
            annee=data['annee'],
            genre=data['genre'],
            statut=data.get('statut', 'disponible')
        )
#_______________________________________________________classe Membre_____________________________________________________________________________
class Membre:
    def __init__(self,id_membre,nom):
        self.id_membre = id_membre
        self.nom = nom
        self.livres_empruntes = []

    def emprunter_livre(self, ISBN: str):
        """Ajoute un livre à la liste des emprunts"""
        self.livres_empruntes.append(ISBN)
    def retourner_livre(self, ISBN: str):
        """Retire un livre de la liste des emprunts"""
        self.livres_empruntes.remove(ISBN)
    
    def __str__(self):
        return f"Membre {self.nom} (ID: {self.id_membre}) - Livres empruntés: {self.livres_empruntes}"
    
    def to_dict(self):
        return {
            "id_membre": self.id_membre,
            "nom": self.nom,
            "livres_empruntes": self.livres_empruntes
        }
    
    @classmethod
    def from_dict(cls, data: dict):
    
        membre = cls(
            id_membre=data['id_membre'],
            nom=data['nom']
        )
        membre.livres_empruntes = data.get('livres_empruntes', [])
        return membre
#________________________________________________________classe Bibliotheque______________________________________________________________________
import json
import csv
from datetime import datetime
from typing import List, Dict
from visualisations import Visualisation

class Bibliotheque:
    def __init__(self):
        self.livres: Dict[str, Livre] = {}  
        self.membres: Dict[str, Membre] = {}  
        self.historique: List[Dict] = []  
    
    def ajouter_livre(self, livre: Livre):
        if livre.ISBN in self.livres:
            print(f"Livre avec ISBN {livre.ISBN} déjà existant")
        else:
            self.livres[livre.ISBN] = livre
            print(f"Livre '{livre.titre}' ajouté avec succès")
    
    def supprimer_livre(self, ISBN):
        
        if ISBN not in self.livres:
            raise LivreInexistantError(ISBN)
        
        livre = self.livres[ISBN]
        if livre.statut == "emprunté":
            raise LivreIndisponibleError(ISBN)
        
        del self.livres[ISBN]
        print(f"Livre '{livre.titre}' supprimé avec succès")
    
    def enregistrer_membre(self, membre: Membre):
        
        if membre.id_membre in self.membres:
            print(f"Membre avec ID {membre.id_membre} déjà existant")
        else:
            self.membres[membre.id_membre] = membre
            print(f"Membre '{membre.nom}' enregistré avec succès")
    
    def supprimer_membre(self, id_membre):
        """Supprime un membre de la bibliothèque"""
        if id_membre not in self.membres:
            raise MembreInexistantError(id_membre)
        
        membre = self.membres[id_membre]
        if membre.livres_empruntes:
            raise QuotaEmpruntDepasseError(f"Impossible de supprimer le membre '{membre.nom}' car il a des livres empruntés")
        
        del self.membres[id_membre]
        print(f"Membre '{membre.nom}' supprimé avec succès")
    
    def emprunter_livre(self, ISBN, id_membre):
        """Gère l'emprunt d'un livre"""
        # Vérifications
        if ISBN not in self.livres:
            raise LivreInexistantError(ISBN)
        
        if id_membre not in self.membres:
            raise MembreInexistantError(id_membre)
        
        livre = self.livres[ISBN]
        membre = self.membres[id_membre]
        
        if livre.statut != "disponible":
            raise LivreIndisponibleError(ISBN)
        
        if len(self.membres[id_membre].livres_empruntes) >= 5:  # Quota de 5 livres
            raise QuotaEmpruntDepasseError(id_membre)
        # Effectuer l'emprunt
        membre.emprunter_livre(ISBN)
        livre.statut = "emprunté"
        
        # Ajouter à l'historique
        self.historique.append({
            'date': datetime.now().isoformat(),
            'ISBN': ISBN,
            'id_membre': id_membre,
            'action': 'emprunt'
        })
        
        print(f"Livre '{livre.titre}' emprunté par {membre.nom}")
    
    def retourner_livre(self, ISBN, id_membre):
        
        # Vérifications
        if ISBN not in self.livres:
            raise LivreInexistantError(ISBN)
        
        if id_membre not in self.membres:
            raise MembreInexistantError(id_membre)
        
        livre = self.livres[ISBN]
        membre = self.membres[id_membre]
        
        # Effectuer le retour
        membre.retourner_livre(ISBN)
        livre.statut = "disponible"
        
        # Ajouter à l'historique
        self.historique.append({
            'date': datetime.now().isoformat(),
            'ISBN': ISBN,
            'id_membre': id_membre,
            'action': 'retour'
        })
        
        print(f"Livre '{livre.titre}' retourné par {membre.nom}")
    
    def rechercher_livres(self, critere = "", valeur= ""):
        
        if not critere:
            return list(self.livres.values())
        
        resultats = []
        for livre in self.livres.values():
            if critere.lower() == "titre" and valeur.lower() in livre.titre.lower():
                resultats.append(livre)
            elif critere.lower() == "auteur" and valeur.lower() in livre.auteur.lower():
                resultats.append(livre)
            elif critere.lower() == "genre" and valeur.lower() in livre.genre.lower():
                resultats.append(livre)
            elif critere.lower() == "statut" and valeur.lower() == livre.statut.lower():
                resultats.append(livre)
        
        return resultats
    
    def obtenir_statistiques(self) :
        """Génère des statistiques sur la bibliothèque"""
        stats = {
            'total_livres': len(self.livres),
            'livres_disponibles': len([l for l in self.livres.values() if l.statut == "disponible"]),
            'livres_empruntes': len([l for l in self.livres.values() if l.statut == "emprunté"]),
            'total_membres': len(self.membres),
            'genres': {},
            'auteurs': {},
            'total_emprunts': len([h for h in self.historique if h['action'] == 'emprunt'])
        }
        
        # Statistiques par genre
        for livre in self.livres.values():
            stats['genres'][livre.genre] = stats['genres'].get(livre.genre, 0) + 1
        
        # Statistiques par auteur
        for livre in self.livres.values():
            stats['auteurs'][livre.auteur] = stats['auteurs'].get(livre.auteur, 0) + 1
        
        return stats
    
    def sauvegarder_donnees(self, dossier = "data"):
        """Sauvegarde les données dans des fichiers"""
        import os
        
        # Créer le dossier s'il n'existe pas
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        
        # Sauvegarder les livres (JSON)
        with open(f"{dossier}/livres.json", 'w', encoding='utf-8') as f:
            livres_data = {ISBN: livre.to_dict() for ISBN, livre in self.livres.items()}
            json.dump(livres_data, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder les membres (JSON)
        with open(f"{dossier}/membres.json", 'w', encoding='utf-8') as f:
            membres_data = {id_m: membre.to_dict() for id_m, membre in self.membres.items()}
            json.dump(membres_data, f, ensure_ascii=False, indent=2)
        
        # Sauvegarder l'historique (CSV)
        with open(f"{dossier}/historique.csv", 'w', newline='', encoding='utf-8') as f:
            if self.historique:
                writer = csv.DictWriter(f, fieldnames=['date', 'ISBN', 'id_membre', 'action'])
                writer.writeheader()
                writer.writerows(self.historique)
        
        print(f"Données sauvegardées dans le dossier '{dossier}'")
    
    def charger_donnees(self, dossier= "data"):
        """Charge les données depuis des fichiers"""
        import os
        
        try:
            # Charger les livres
            if os.path.exists(f"{dossier}/livres.json"):
                with open(f"{dossier}/livres.json", 'r', encoding='utf-8') as f:
                    livres_data = json.load(f)
                    self.livres = {ISBN: Livre.from_dict(data) for ISBN, data in livres_data.items()}
            
            # Charger les membres
            if os.path.exists(f"{dossier}/membres.json"):
                with open(f"{dossier}/membres.json", 'r', encoding='utf-8') as f:
                    membres_data = json.load(f)
                    self.membres = {id_m: Membre.from_dict(data) for id_m, data in membres_data.items()}
            
            # Charger l'historique
            if os.path.exists(f"{dossier}/historique.csv"):
                with open(f"{dossier}/historique.csv", 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.historique = list(reader)
            
            print(f"Données chargées depuis le dossier '{dossier}'")
        
       
        except Exception as e:
            print(f"Erreur lors du chargeenmt des données : {e}")
    def generer_statistiques(self, dossier = "assets"):
        import os
        from pathlib import Path
    
        try:
        # Créer le dossier s'il n'existe pas
            Path(dossier).mkdir(parents=True, exist_ok=True)
        
        # Générer les graphiques avec gestion des erreurs individuelles
            try:
                Visualisation.pie_chart_genres(self.livres, dossier)
            except Exception as e:
                print(f"Erreur lors de la génération du diagramme des genres : {str(e)}")
        
            try:
                Visualisation.top_auteurs(self.livres, dossier)
            except Exception as e:
                print(f"Erreur lors de la génération du top auteurs : {str(e)}")
        
            try:
                Visualisation.activite_emprunts(self.historique, dossier)
            except Exception as e:
                print(f"Erreur lors de la génération de la courbe d'activité : {str(e)}")
            
            print(f"Statistiques générées avec succès dans : {os.path.abspath(dossier)}")
        
        except Exception as e:
            print(f"Erreur critique lors de la génération des statistiques : {str(e)}")
            raise