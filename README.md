# Chatbot TER IA

## Description du projet

TER IA est un assistant virtuel sophistiqué conçu pour faciliter l'accès aux informations relatives au TER Sénégal. Ce chatbot intelligent, développé avec le framework Rasa, offre une interface conversationnelle intuitive pour aider les utilisateurs à obtenir des renseignements sur les horaires, les gares, les tarifs et d'autres aspects du service ferroviaire.

## Fonctionnalités principales

1. **Consultation des horaires** : Obtenez les horaires des trains entre deux gares spécifiques.
2. **Informations tarifaires** : Renseignez-vous sur les tarifs des billets entre différentes gares.
3. **Localisation des gares** : Trouvez la gare la plus proche de votre emplacement actuel.
4. **Prochains départs** : Consultez les horaires des prochains trains à partir d'une gare donnée.
5. **Assistance générale** : Répondez aux questions fréquentes sur le service TER.

## Architecture du projet

Le projet TER IA est structuré selon l'architecture Rasa, qui comprend plusieurs composants clés :

### 1. Compréhension du langage naturel (NLU)

Le module NLU est responsable de l'interprétation des messages des utilisateurs. Il utilise des techniques d'apprentissage automatique pour classifier les intentions et extraire les entités pertinentes.

Fichier principal : `nlu.yml`

### 2. Gestion du dialogue

Ce composant gère le flux de la conversation en utilisant des "stories" prédéfinies et un modèle de dialogue entraîné.

Fichier principal : `stories.yml`

### 3. Actions personnalisées

Les actions définissent le comportement spécifique du chatbot en réponse aux intentions de l'utilisateur.

Fichier principal : `actions.py`

### 4. Configuration du domaine

Le domaine définit l'univers dans lequel le chatbot opère, incluant les intentions, entités, slots, actions et réponses.

Fichier principal : `domain.yml`

## Concepts clés de Rasa

### Intents (Intentions)

Les intentions représentent le but ou l'objectif de l'utilisateur dans un message. Par exemple :

- `greet` : L'utilisateur salue le chatbot
- `ask_train_schedule` : L'utilisateur demande les horaires de train
- `ask_ticket_price` : L'utilisateur s'enquiert du prix d'un billet

### Entities (Entités)

Les entités sont des informations spécifiques extraites du message de l'utilisateur. Par exemple :

- `departure_station` : La gare de départ
- `arrival_station` : La gare d'arrivée
- `time` : L'heure souhaitée pour le voyage

### Slots

Les slots sont des variables qui stockent des informations tout au long de la conversation. Ils permettent au chatbot de se souvenir des détails importants. Par exemple :

- `location` : La position actuelle de l'utilisateur
- `departure_station` : La gare de départ choisie
- `arrival_station` : La gare d'arrivée sélectionnée

### Actions

Les actions sont les opérations que le chatbot peut effectuer en réponse aux intentions de l'utilisateur. Elles peuvent être simples (comme envoyer un message) ou complexes (comme interroger une base de données). Exemples :

- `action_provide_train_schedule` : Fournit les horaires de train
- `action_calculate_ticket_price` : Calcule le prix d'un billet

### Forms

Les forms sont des structures qui permettent de collecter systématiquement des informations auprès de l'utilisateur. Par exemple :

- `horaire_lieu_form` : Collecte les informations de départ et d'arrivée pour une recherche d'horaires
- `horaire_heure_form` : Demande l'heure souhaitée pour un trajet

## Configuration et installation

1. **Prérequis** :

   - Python 3.7 ou supérieur
   - pip (gestionnaire de paquets Python)

2. **Installation de Rasa** :

   ```
   pip install rasa
   ```

3. **Clonage du repository** :

   ```
   git clone https://github.com/votre-username/ter-ia-chatbot.git
   cd ter-ia-chatbot
   ```
  

4. **Entraînement du modèle** :
   ```
   rasa train
   ```

## Utilisation

1. **Lancement du serveur d'actions** :
   Dans un terminal, exécutez :

   ```
   rasa run actions
   ```

2. **Démarrage du chatbot** :
   Dans un autre terminal, lancez :

   ```
   rasa shell
   ```

3. Vous pouvez maintenant interagir avec le chatbot en tapant vos messages dans le terminal.

## Personnalisation et extension

Pour adapter le chatbot à vos besoins spécifiques :

1. **Ajout de nouvelles intentions** : Modifiez `nlu.yml` pour inclure de nouveaux exemples d'entraînement.
2. **Création de nouvelles stories** : Ajoutez des scénarios de conversation dans `stories.yml`.
3. **Implémentation d'actions personnalisées** : Développez de nouvelles actions dans `actions.py`.
4. **Mise à jour du domaine** : Reflétez vos changements dans `domain.yml`.

Après chaque modification, n'oubliez pas de réentraîner le modèle avec `rasa train`.

## Contributing

Les contributions sont les bienvenues ! Si vous trouvez des problèmes ou avez des suggestions d'amélioration, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Author
- Développé par : Mouhamed Diouf
- GitHub: [@MdCode002](https://github.com/MdCode002)
- Email: dioufmouhamed002@gmail.com

## License

Ce projet est sous licence [MIT License](LICENSE).
