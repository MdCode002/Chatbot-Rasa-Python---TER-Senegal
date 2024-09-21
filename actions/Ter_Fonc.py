
import math
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
    # Fonction pour calculer la distance de Haversine entre deux points géographiques
def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Rayon de la Terre en kilomètres
            phi1 = math.radians(lat1)
            phi2 = math.radians(lat2)
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)

            a = math.sin(delta_phi / 2) ** 2 + \
                math.cos(phi1) * math.cos(phi2) * \
                math.sin(delta_lambda / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            distance = R * c
            return distance

 # Fonction pour trouver le lieu le plus proche
def trouver_lieu_proche(lat, lon, lieux):
    lieu_proche = None
    distance_min = float('inf')

    for lieu, coord in lieux.items():
        dist = haversine(lat, lon, coord[0][0], coord[0][1])
        if dist < distance_min:
            distance_min = dist
            lieu_proche = lieu

    return lieu_proche, distance_min

 # Fonction pour trouver le lieu le plus similaire au input du user 
def trouver_lieu_Similaire(lieu_utilisateur, lieux_dict, seuil=60):
    lieux = list(lieux_dict.keys())
    # Utilisation de process.extractOne pour obtenir le meilleur match avec un score de similarité
    meilleur_match, score = process.extractOne(lieu_utilisateur, lieux, scorer=fuzz.token_sort_ratio)
    
    # Vérifier si le score est supérieur au seuil de similarité défini
    if score >= seuil:
        return meilleur_match, lieux_dict[meilleur_match]
    else:
        return None, None