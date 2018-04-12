import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import re

# Fonction listant les colonnes dont le titre contient des chaines de caractères
def col_rech_titre(df, fin = True, suffix =""):
    """Affiche le nom des colonnes d'un dataframe contenant une chaîne de caractères.

    - Args:
        df(pandas.dataframe): dataframe
        fin(boolean): flag pour indiquer un préfixe ou un suffixe
        suffix(str): chaîne de caractères recherchée
        
    - Returns:
        Liste contenant les colonnes contenant la chaîne de caractères.
    """
    liste_col = []
    if suffix !="":
        if fin == True:
            for col in df.columns:
                if col.endswith(suffix) == True:
                    liste_col.append(col)
        else:
            for col in df.columns:
                if col.startswith(suffix) == True:
                    liste_col.append(col)                  
    return liste_col 

def recommendation(id_title, index = False):
    """Recommendation de films via kNN.
    - Args:
            id_title(string): movie title ou movie id
            index(boolean): flag pour définir si recherche par id (index) du film
    - Returns:
            query_movie (string): nom + id du film saisi 
            l_recommend (liste): liste des films recommandés
    """
    l_recommend = []
    d_recommend = {}
    d_query = {}
    d_result = {}
    query_movie = ""
    query_index = -1
    # importation des données
    movies = pd.read_csv('movie_metadata_cleaned_digital.csv', sep=";", encoding='utf_8', low_memory=False)
    if index == True :
        # Recherche par l'id (index) du film
        if id_title != "":
            lower_movie_id = str(id_title).lower()
            match = re.search("\D", lower_movie_id)
            if not match:
                #query_index = int(lower_movie_title)        
                # id (imdb) du film 
                if len(movies[movies['imdb_id'] == int(lower_movie_id)].index) > 0:
                    # On choisit le premier film trouvé
                    query_index = movies[movies['imdb_id'] == int(lower_movie_id)].index[0]
    else:
        if id_title != "":
            # titre du film en minuscule
            lower_movie_title = str(id_title).lower()
            movies['low_movie_title'] = movies['movie_title'].str.lower()
            #if len(movies[movies['low_movie_title'].str.contains(lower_movie_title)].index) > 0:
            #    # On choisit le premier film trouvé
            #    query_index = movies[movies['low_movie_title'].str.contains(lower_movie_title)].index[0]
            if len(movies[movies['low_movie_title'].str.strip() == lower_movie_title].index) > 0:
                # On choisit le premier film trouvé
                query_index = movies[movies['low_movie_title'].str.strip() == lower_movie_title].index[0]            

    if query_index > -1:
        l_neighbors = []
        # Recherche de toutes les colonnes "booléennes" du dataframe
        bool_movies = movies[col_rech_titre(movies, False, "bool_")]
        # algo k-NN
        model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'auto')
        model_knn.fit(bool_movies)
        # Recommandation sur les 18 plus proches
        distances, indices = model_knn.kneighbors(bool_movies.loc[query_index, :].reshape(1, -1), n_neighbors = 18)
        for i in range(0, len(distances.flatten())):
            if i == 0:
                #print(movies[movies.index == query_index]['movie_title'].str.strip().values[0] + " (" + str(query_index) + ")")
                query_movie = movies[movies.index == query_index]['movie_title'].str.strip().values[0] + " (id=" + str(query_index) + ")"
                #d_query = {"Recommendations for" : {'name' :  movies[movies.index == query_index]['movie_title'].str.strip().values[0], 'id' : str(query_index)}}
                d_query = {"Recommendations for" : {'name' :  movies[movies.index == query_index]['movie_title'].str.strip().values[0], 'id' : str(movies[movies.index == query_index]['imdb_id'].values[0])}}
            else:
                if query_index != indices.flatten()[i]:
                    l_neighbors.append(indices.flatten()[i])
        # On trie les 5 meilleurs des 18 plus proches en fonction de leur popularité
        if len(l_neighbors) > 0:
            recommend_movies = movies[movies.index.isin(l_neighbors)]
            top_movies = recommend_movies[['movie_title', 'popularity', 'imdb_id']].sort_values('popularity', ascending=False).head(5)
            for i in list(top_movies.index):
                #d_recommend = {'name' : top_movies[top_movies.index == i]['movie_title'].str.strip().values[0], 'id' : str(i)}
                d_recommend = {'name' : top_movies[top_movies.index == i]['movie_title'].str.strip().values[0], 'id' : str(top_movies[top_movies.index == i]['imdb_id'].values[0])}
                l_recommend.append(d_recommend)
            d_result = {"Results" : l_recommend}
        
    return query_movie, d_query, d_result
