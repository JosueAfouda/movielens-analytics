# **Phase 2 : Data Analyst - Exploration et Visualisation**  

![](architecturephase.png)

## Introduction

**Objectif : Explorer et analyser les données en interrogeant l’API.**  

🔹 **Analyse Exploratoire des Données (EDA)** :  
- Utiliser le **SDK Python** pour requêter l’API et récupérer les données.  
- Identifier les tendances dans les notes des films.  
- Étudier les genres les plus populaires et les préférences des utilisateurs.  

🔹 **Construction d’une Data App avec Streamlit** :  
- Créer une **application interactive** qui permet de visualiser les tendances du cinéma.  
- Intégrer des **tableaux dynamiques** et des **graphiques interactifs**.  
- Offrir une **recherche avancée** des films en fonction des notes et des genres.  

**Livrables** :  
- Un notebook d'analyse exploratoire interactif.  
- Une **application web Streamlit** connectée à l’API qui présente, de manière interactive, les insights aux parties prenantes.

---

## Présentation de Jupyter Notebook

**Jupyter Notebook** est un environnement interactif très populaire dans le monde de la **Data Science**. Il permet d’écrire du code Python, de visualiser des graphiques, d’insérer des textes explicatifs (en Markdown), et de documenter une analyse de données de manière fluide et lisible.

---

### Pourquoi Jupyter Notebook est si populaire ?

🔹 **Interactivité totale** : Chaque cellule de code peut être exécutée indépendamment, ce qui permet d’explorer les données pas à pas.

🔹 **Documentation intégrée** : On peut facilement alterner entre du code Python et des explications en langage naturel (Markdown), ce qui en fait un excellent outil pédagogique et professionnel.

🔹 **Visualisation immédiate** : Les bibliothèques comme `matplotlib`, `seaborn` ou `plotly` s’intègrent parfaitement à Jupyter pour créer des visualisations dynamiques.

🔹 **Support riche** : Intègre du HTML, des tableaux interactifs, des widgets, etc. Parfait pour présenter un projet à un client ou à une équipe.

---

### Un outil central pour le Data Analyst

Durant la phase 2, vous utiliserez Jupyter Notebook pour :

- Charger et explorer les données extraites via votre SDK (et donc indirectement via l’API).
- Réaliser une **analyse exploratoire** complète : tendances, corrélations, genres populaires...
- Visualiser les résultats sous forme de **graphiques** compréhensibles et exploitables.
- Créer un **notebook professionnel** que vous pourrez intégrer dans votre portfolio.

---

Parfait, voici une version retravaillée de la section **Installation rapide** (renommée en **⚙️ Mise en place de l’environnement d’analyse**), adaptée au contexte de la formation, en précisant que l’on travaille avec **VSCode**, un environnement virtuel Python, et un dépôt GitHub :

---

## Mise en place de l’environnement d’analyse

Dans cette formation, nous utilisons **VSCode** comme éditeur principal et organisons chaque phase dans un répertoire Git dédié. Pour cette phase 2 (*Data Analyst – Exploration & Visualisation*), tu vas travailler dans un nouveau projet nommé par exemple `movielens-analytics` (tu crées ton propre répertoire GitHub et tu lui donnes le nom que tu veux)

Voici les étapes pour bien démarrer :

### 1. Cloner le dépôt GitHub du projet

Si ce n’est pas encore fait, commence par cloner le dépôt Git que tu as créé pour cette phase :

```bash
git clone https://github.com/JosueAfouda/movielens-analytics.git
cd movielens-analytics
```

### 2. Créer et activer un environnement virtuel

Ensuite, configure un environnement Python isolé pour gérer les dépendances :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> Si tu es sur Windows, utilise :  
> `.\.venv\Scripts\activate`

### 3. Ouvrir le projet dans VSCode

```bash
code .
```

Si tu reçois une notification *"Sélectionner l'interpréteur Python"*, choisis l’interpréteur correspondant à ton environnement `.venv`.

### 4. Créer un dossier pour ton notebook

Organise tes fichiers en créant un dossier dédié à l’analyse :

```bash
mkdir dataanalysis
touch dataanalysis/movie_data_analysis.ipynb
```

### 5. Installer le SDK `moviesdk`

Ce SDK te permettra d’interagir avec l’API MovieLens. Installe-le dans ton environnement :

```bash
pip install moviesdk
```

### 6. Lancer et configurer le Jupyter Notebook

Ouvre ton fichier `.ipynb` dans VSCode. Lorsque tu exécutes ta **première cellule**, si Jupyter n’est pas encore installé, VSCode te proposera automatiquement de l’installer (avec `ipykernel`). Accepte pour que tout soit configuré automatiquement.

---

**Ton environnement est prêt !**

Tu peux maintenant démarrer ton **analyse exploratoire interactive** directement dans le fichier `movie_data_analysis.ipynb`.  
On va explorer les films, les notes, les genres... et visualiser tout ça avec des graphiques dynamiques !























































Suite du Projet movielens-project

##  Data Analysis sur Notebook jupyter

- Le Data Analyst va se familiariser avec l'API via le SDK 

- Comprendre l'ensemble des données

- Vérifier le format des colonnes pour les résultats en pandas dataframe

- Calcul de Sparsity = Number of Ratings in Matrix / (Number of Users * Number of Movies). Il s'agie de la parcimonie. Elle mesure le degré de vide d'une matrice, ou du pourcentage de la matrice qui est vide. En substance, cette formule est simplement le nombre de notes qu'une matrice contient divisé par le nombre de notes qu'elle pourrait contenir étant donné le nombre d'utilisateurs et de films dans la matrice.

***Remember that sparsity is calculated by the number of cells in a matrix that contain a rating divided by the total number of values that matrix could hold given the number of users and items (movies). In other words, dividing the number of ratings present in the matrix by the product of users and movies in the matrix and subtracting that from 1 will give us the sparsity or the percentage of the ratings matrix that is empty.***

Voici un exemple de calcul en PySPark. Tu dois écrire la version Python à l'aide du SDK.

Sparsity: numerator

```python
# Number of ratings in matrix (on compte le nombre de notes dans les notes)
numerator = ratings.count()
```

Sparsity: users and movies

```python
# Distinct users and movies (Nombre d'utilisateurs distincs et le nombre d'éléments ou de films distincts)
users = ratings.select("userId").distinct().count() # La méthode .distinct() renvoie simplement toutes les valeurs uniques d'une colonne.
movies = ratings.select("movieId").distinct().count()
```

Sparsity: denominator

```python
# Number of ratings matrix could contain if no empty cells (Multiplication du nombre d'utilisateurs et de nombre de films pour obtenir le dénominateur)
denominator = users * movies
```

Sparsity

```python
#Calculating sparsity (Diviser simplement le numérateur par le dénominateur et soustrayer le résultat de 1)
sparsity = 1 - (numerator*1.0 / denominator)
print ("Sparsity: "), sparsity
print("The ratings dataframe is ", "%.2f" % sparsity + "% empty.")
```

- general summary metrics of the ratings dataset and see how many ratings the movies have and how many ratings each users has provided.

Exemple de code en PySpark. Tu dois écrire la version correspondante en Python à l'aide du SDK

```python
# Import the requisite packages
from pyspark.sql.functions import col

# View the ratings dataset
ratings.show()

# Filter to show only userIds less than 100
ratings.filter(col("userId") < 100).show()

# Group data by userId, count ratings
ratings.groupBy("userId").count().show()
```

- MovieLens Summary Statistics

Exemple de code en PySpark. Tu dois écrire la version correspondante en Python à l'aide du SDK

```python
# Min num ratings for movies
from pyspark.sql.functions import min, avg

print("Movie with the fewest ratings: ")
ratings.groupBy("movieId").count().select(min("count")).show()

# Avg num ratings per movie
print("Avg num ratings per movie: ")
ratings.groupBy("movieId").count().select(avg("count")).show()

# Min num ratings for user
print("User with the fewest ratings: ")
ratings.groupBy("userId").count().select(min("count")).show()

# Avg num ratings per user
print("Avg num ratings per user: ")
ratings.groupBy("userId").count().select(avg("count")).show()
```

***Exemple de commentaire à faire :  Users have at least 20 ratings and on average of 149 ratings. And movies have at least 1 rating with an average of 11 ratings.***