# main.py
from bibliotheque import Bibliotheque, Livre, Membre
from exceptions import *
from datetime import datetime
import json, csv
import os

def afficher_menu():
    print("\n====== MENU BIBLIOTHÈQUE ======")
    print("1. Ajouter un livre")
    print("2. Supprimer un livre")
    print("3. Enregistrer un membre")
    print("4. Supprimer un membre")
    print("5. Emprunter un livre")
    print("6. Retourner un livre")
    print("7. Rechercher un livre")
    print("8. Générer les statistiques visuelles")
    print("9. Sauvegarder les données")
    print("10. Charger les données")
    print("0. Quitter")

def main():
    biblio = Bibliotheque()
    
    # Chargement automatique au démarrage
    if os.path.exists("data"):
        try:
            biblio.charger_donnees()
            print("Données chargées avec succès")
        except Exception as e:
            print(f"Erreur au chargement : {e}")

    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        try:
            if choix == "1":
                print("\n--- Ajout d'un livre ---")
                isbn = input("ISBN : ")
                titre = input("Titre : ")
                auteur = input("Auteur : ")
                annee = int(input("Année : "))
                genre = input("Genre : ")
                statut = input("Statut (disponible/emprunté) : ").lower()
                livre = Livre(isbn, titre, auteur, annee, genre, statut)
                biblio.ajouter_livre(livre)

            elif choix == "2":
                print("\n--- Suppression d'un livre ---")
                isbn = input("ISBN du livre à supprimer : ")
                biblio.supprimer_livre(isbn)

            elif choix == "3":
                print("\n--- Enregistrement d'un membre ---")
                id_membre = input("ID membre : ")
                nom = input("Nom complet : ")
                membre = Membre(id_membre, nom)
                biblio.enregistrer_membre(membre)

            elif choix == "4":
                print("\n--- Suppression d'un membre ---")
                id_membre = input("ID membre à supprimer : ")
                biblio.supprimer_membre(id_membre)

            elif choix == "5":
                print("\n--- Emprunt d'un livre ---")
                id_membre = input("Votre ID membre : ")
                isbn = input("ISBN du livre à emprunter : ")
                biblio.emprunter_livre(isbn, id_membre)

            elif choix == "6":
                print("\n--- Retour d'un livre ---")
                id_membre = input("Votre ID membre : ")
                isbn = input("ISBN du livre à retourner : ")
                biblio.retourner_livre(isbn, id_membre)

            elif choix == "7":
                print("\n--- Recherche de livres ---")
                crit = input("Critère (titre/auteur/genre/statut) [laisser vide pour tous] : ")
                if crit:
                    val = input(f"Valeur pour {crit} : ")
                    resultats = biblio.rechercher_livres(crit, val)
                else:
                    resultats = biblio.rechercher_livres()
                
                if not resultats:
                    print("Aucun résultat trouvé")
                else:
                    print(f"\n{len(resultats)} résultat(s) :")
                    for i, livre in enumerate(resultats, 1):
                        print(f"{i}. {livre.titre} | {livre.auteur} | {livre.annee} | {livre.genre} | {livre.statut}")

            elif choix == "8":
                print("\n--- Génération des statistiques ---")
                try:
                    # Génère les graphiques dans le dossier stats/
                    biblio.generer_statistiques("assets")
                    
                    # Affiche aussi les stats textuelles
                    stats = biblio.obtenir_statistiques()
                    print("\nStatistiques textuelles :")
                    print(f"- Livres totaux : {stats['total_livres']}")
                    print(f"- Livres disponibles : {stats['livres_disponibles']}")
                    print(f"- Livres empruntés : {stats['livres_empruntes']}")
                    print(f"- Membres inscrits : {stats['total_membres']}")
                    
                    print("\nGraphiques générés dans le dossier 'stats/'")
                except Exception as e:
                    print(f"Erreur lors de la génération : {e}")

            elif choix == "9":
                print("\n--- Sauvegarde des données ---")
                biblio.sauvegarder_donnees()
                print("Données sauvegardées dans data/")

            elif choix == "10":
                print("\n--- Chargement des données ---")
                biblio.charger_donnees()
                print("Données chargées depuis data/")

            elif choix == "0":
                print("\nSauvegarde automatique avant fermeture...")
                biblio.sauvegarder_donnees()
                print("Au revoir !")
                break

            else:
                print("Choix invalide. Veuillez réessayer.")
        
        except ValueError as e:
            print(f"Erreur de valeur : {e}")
        except (LivreInexistantError, MembreInexistantError) as e:
            print(f"Erreur : {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    # Création du dossier stats s'il n'existe pas
    if not os.path.exists("assets"):
        os.makedirs("assets")
    main()