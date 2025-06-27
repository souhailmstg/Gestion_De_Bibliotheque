import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, List
from bibliotheque import Livre

class Visualisation:
    @staticmethod
    def pie_chart_genres(livres: Dict[str, 'Livre'], save_path: str = None):
        
        genres = {}
        for livre in livres.values():
            genres[livre.genre] = genres.get(livre.genre, 0) + 1

        plt.figure(figsize=(10, 7))
        plt.pie(genres.values(), 
                labels=genres.keys(), 
                autopct='%1.1f%%',
                startangle=90,
                shadow=True)
        plt.title("Répartition des livres par genre")
        
        if save_path:
            plt.savefig(f"{save_path}/stats_genres.png")
        plt.show()

    @staticmethod
    def top_auteurs(livres: Dict[str, 'Livre'], save_path = None):
        
        auteurs = {}
        for livre in livres.values():
            auteurs[livre.auteur] = auteurs.get(livre.auteur, 0) + 1

        top_10 = sorted(auteurs.items(), key=lambda x: x[1], reverse=True)[:10]
        
        plt.figure(figsize=(12, 6))
        plt.bar([a[0] for a in top_10], [a[1] for a in top_10], color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.title("Top 10 des auteurs les plus populaires")
        plt.xlabel("Auteurs")
        plt.ylabel("Nombre de livres")
        plt.tight_layout()
        
        if save_path:
            plt.savefig(f"{save_path}/stats_auteurs.png")
        plt.show()

    @staticmethod
    def activite_emprunts(historique: List[Dict], save_path: str = None):
        
        dates = []
        for entry in historique:
            if entry['action'] == 'emprunt':
                dates.append(datetime.fromisoformat(entry['date']).date())

        # Filtrer les 30 derniers jours
        date_end = datetime.now().date()
        date_start = date_end - timedelta(days=30)
        dates = [d for d in dates if date_start <= d <= date_end]

        # Compter les emprunts par jour
        jours = {}
        for d in dates:
            jours[d] = jours.get(d, 0) + 1

        # Remplir les jours manquants
        for i in range((date_end - date_start).days + 1):
            day = date_start + timedelta(days=i)
            if day not in jours:
                jours[day] = 0

        # Trier par date
        jours_tries = sorted(jours.items())
        
        plt.figure(figsize=(12, 6))
        plt.plot([d[0] for d in jours_tries], [d[1] for d in jours_tries], 
                marker='o', linestyle='-', color='green')
        plt.title("Activité des emprunts (30 derniers jours)")
        plt.xlabel("Date")
        plt.ylabel("Nombre d'emprunts")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(f"{save_path}/stats_emprunts.png")
        plt.show()