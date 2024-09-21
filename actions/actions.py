# actions.py

import re
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import math
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from . import Ter_Data
from . import Ter_Fonc
from datetime import datetime
import pytz

class ActionProvideTrainSchedule(Action):

    def name(self) -> Text:
        return "action_provide_train_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        def trouver_lieu_proche(lieu_utilisateur, liste_lieux):
            lieu_proche, score = process.extractOne(lieu_utilisateur, liste_lieux)
            return lieu_proche if score >= 60 else ""
        departure_station = tracker.get_slot("departure_station")
        arrival_station = tracker.get_slot("arrival_station")
        
        heure=  tracker.get_slot("heure")
        heure = re.search(r'\d+', heure).group()
        if departure_station and arrival_station:
            departure_station= trouver_lieu_proche(departure_station, Ter_Data.lieu)
            arrival_station= trouver_lieu_proche(arrival_station, Ter_Data.lieu)
            if departure_station in Ter_Data.lieu and arrival_station in Ter_Data.lieu:

                index_horaires = [index for index, heures in enumerate(Ter_Data.horaires_trains[departure_station]) if heures.startswith(f"{heure}:")]
                horaires = ""
                if index_horaires != []:
                    for i in index_horaires:
                        horaires += f"{Ter_Data.horaires_trains[departure_station][i]} --> {Ter_Data.horaires_trains[arrival_station][i]}\n"

                    dispatcher.utter_message(f"Les horaires de {departure_station} à {arrival_station} pour {heure}h sont: \n{horaires}")
                else:
                    dispatcher.utter_message(f"Aucun train disponible à {heure}h pour ce trajet.")
            else:
                dispatcher.utter_message("Désolé, je n'ai pas trouvé d'horaires pour ce trajet.")
        else:
            dispatcher.utter_message("Je n'ai pas toutes les informations nécessaires pour vous fournir les horaires.")

        return []



class ActionProvideNearestStation(Action):

    def name(self) -> Text:
        return "action_provide_nearest_station"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        location = tracker.get_slot('location')
        if location != None :
            latitude_str, longitude_str = location.split(',')

            latitude = float(latitude_str.strip())
            longitude = float(longitude_str.strip())


            lieu_proche, distance_min = Ter_Fonc.trouver_lieu_proche(latitude, longitude, Ter_Data.gare)


            dispatcher.utter_message(text=f"D'aprés votre position la gare la plus proche de vous est {lieu_proche}, à une distance de {distance_min:.2f} km.")
            return []
        else:
            dispatcher.utter_message(text="Veuillez me partager votre position actuelle.")
            return []

class ActionProvideNearestStationByLieu(Action):

    def name(self) -> Text:
        return "action_provide_nearest_station_by_lieu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


       
        lieu = tracker.get_slot('lieu')
        # Appel de la fonction pour trouver le lieu correspondant
        lieuTrouver, coordonnees = Ter_Fonc.trouver_lieu_Similaire(lieu, Ter_Data.lieux_dakar)

        lieu_proche, distance_min = Ter_Fonc.trouver_lieu_proche(coordonnees[0], coordonnees[1], Ter_Data.gare)


        dispatcher.utter_message(text=f"la gare la plus proche de {lieuTrouver} est la {lieu_proche} à une distance de {distance_min:.2f} km.")
        return []
class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # add different functionalities like google search, wiki search, etc to provide more answer
        latest_message = tracker.latest_message.get("text")
        dispatcher.utter_message(text="Désolé, je n'ai pas compris. Pouvez-vous reformuler votre question ?")
        return []

class ActionNextTrain(Action):
    def name(self) -> Text:
        return "action_next_train"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        def trouver_lieu_proche(lieu_utilisateur, liste_lieux):
            lieu_proche, score = process.extractOne(lieu_utilisateur, liste_lieux)
            return lieu_proche if score >= 60 else ""
        
        next_train_gare = tracker.get_slot("next_train_gare")
        
        if next_train_gare:
            timezone = pytz.timezone('Africa/Dakar')
            heure_actuelle = datetime.now(timezone).strftime("%H:%M")
            next_train_gare = trouver_lieu_proche(next_train_gare, Ter_Data.lieu)
            
            if next_train_gare:
                heure_actuelle_dt = datetime.strptime(heure_actuelle, "%H:%M")
                for temps_str in Ter_Data.horaires_trains[next_train_gare]:
                    temps = datetime.strptime(temps_str, "%H:%M")
                    if temps > heure_actuelle_dt:
                        time = temps.strftime("%H:%M")
                        dispatcher.utter_message(text=f"Le prochain train de {next_train_gare}  passe à {time}")
                        return []
                
            dispatcher.utter_message(text="Désolé, je n'ai pas trouvé de train à partir de maintenant pour {next_train_gare}.")
        
        else:
            dispatcher.utter_message(text="Désolé, je n'ai pas réussi à trouver ce lieu.")
        
        return []
    
class ActionTarifEntreGare(Action):
    def name(self) -> Text:
        # Nom de l'action, utilisé pour l'identifier dans les fichiers de domaine
        return "action_tarif_entre_gare"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Récupérer les valeurs des slots "Ticket_depart" et "Ticket_arrive"
        Ticket_depart = tracker.get_slot("Ticket_depart")
        Ticket_arrive = tracker.get_slot("Ticket_arrive")
        
        # Vérifier si les deux tickets sont fournis
        if Ticket_depart and Ticket_arrive:
            # Trouver les lieux similaires pour les tickets de départ et d'arrivée
            lieuTrouver_depart, coordonnees_depart = Ter_Fonc.trouver_lieu_Similaire(Ticket_depart, Ter_Data.lieux_dakar)
            lieuTicket_arrive, coordonnees_arrive = Ter_Fonc.trouver_lieu_Similaire(Ticket_arrive, Ter_Data.lieux_dakar)
            
            # Vérifier si les coordonnées pour les deux lieux sont trouvées
            if coordonnees_depart and coordonnees_arrive:
                # Trouver les gares les plus proches pour les deux lieux
                lieu_proche_depart, distance_min_depart = Ter_Fonc.trouver_lieu_proche(coordonnees_depart[0], coordonnees_depart[1], Ter_Data.gare)
                lieu_proche_arrive, distance_min_arrive = Ter_Fonc.trouver_lieu_proche(coordonnees_arrive[0], coordonnees_arrive[1], Ter_Data.gare)
                
                # Fonction pour obtenir les forfaits en fonction du nombre de zones traversées
                def Get_Ticket_For_nbzone(nb):
                    forfaits = [forfait for forfait in Ter_Data.forfaits if forfait["zone"] == nb]
                    text = f"Vous devez aller à la gare {lieu_proche_depart} et descendre à la gare {lieu_proche_arrive}. Voici les tickets ou abonnements disponibles :\n"
                    for forfait in forfaits:
                        text += f"- {forfait['type']} : {forfait['prix']} FCFA,\n"
                    return text
                
                # Vérifier si les deux lieux ne sont pas les mêmes
                if lieu_proche_depart != lieu_proche_arrive:
                    # Cas où les deux lieux sont dans la même zone
                    if Ter_Data.gare[lieu_proche_depart][1] == Ter_Data.gare[lieu_proche_arrive][1]:
                        text = Get_Ticket_For_nbzone(1)
                        dispatcher.utter_message(text=text)
                    elif  Ter_Data.gare[lieu_proche_depart][1] + Ter_Data.gare[lieu_proche_arrive][1] == 3 or Ter_Data.gare[lieu_proche_depart][1] + Ter_Data.gare[lieu_proche_arrive][1] == 5:
                        text = Get_Ticket_For_nbzone(2)
                        dispatcher.utter_message(text=text)
                    # Cas où les deux lieux sont dans des zones non adjacentes
                    else:
                        text = Get_Ticket_For_nbzone(3)
                        dispatcher.utter_message(text=text)
                else:
                    dispatcher.utter_message(text="Désolé, mais les deux lieux sont trop proches. Le TER n'est peut-être pas la meilleure solution pour vous déplacer.")
            else:
                dispatcher.utter_message(text="Désolé, je n'ai pas réussi à trouver une correspondance pour les lieux que vous avez fournis.")
        else:
            dispatcher.utter_message(text="Désolé, mais vous devez fournir deux tickets valides.")
        
        return []
