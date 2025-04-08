import streamlit as st
import pandas as pd
from pathlib import Path
import re

# === Configuration et chargement des fichiers ===
output_dir = Path(__file__).resolve().parents[1] / "output"
movie_stats = pd.read_parquet(output_dir / "top_movies_by_ratings.parquet")
genre_df = pd.read_parquet(output_dir / "genre_df.parquet")
tags_df = pd.read_parquet(output_dir / "user_tag_stats.parquet")
ratings_df = pd.read_parquet(output_dir / "ratings.parquet")

# Pour les métadonnées supplémentaires (ex: lien vers IMDb)
links_path = output_dir / "meta.json"
if links_path.exists():
    import json
    with open(links_path) as f:
        meta_links = json.load(f)
else:
    meta_links = {}

# === Filtres de recherche ===
st.title("🔎 Explorateur de films")

with st.expander("🎯 Filtres avancés", expanded=True):
    col1, col2, col3 = st.columns([1, 1, 2])

    all_genres = sorted(set(genre_df['genre']))
    selected_genres = col1.multiselect("Genres", all_genres, default=all_genres[:3])

    movie_stats["year"] = movie_stats["title"].apply(
        lambda x: int(re.search(r"\((\d{4})\)", x).group(1)) if re.search(r"\((\d{4})\)", x) else None
    )
    years = movie_stats['year'].dropna().astype(int)
    selected_years = col2.slider("Année de sortie", min_value=int(years.min()), max_value=int(years.max()), value=(1990, 2010))

    selected_rating = col1.slider("Note moyenne min.", 0.0, 5.0, 3.5, 0.1)
    selected_votes = col2.slider("Nombre de votes min.", 0, int(movie_stats['rating_count'].max()), 50, 10)

    tag_options = sorted(tags_df['tag'].unique())
    selected_tags = col3.multiselect("Tags à inclure", tag_options)

    keyword = col3.text_input("Mot-clé dans le titre")

# === Filtrage des films ===
filtered_movies = movie_stats.copy()

############################################################

# Initialisation du client
from moviesdk import MovieClient, MovieConfig
config = MovieConfig(movie_base_url="https://movielens-api-rmr7.onrender.com")
client = MovieClient(config=config)

# Vérification que l'API est opérationnelle
client.health_check()

# Mise en cache locale des genres
genre_cache = {}

def get_genres_with_cache(movie_id: int):
    if movie_id in genre_cache:
        return genre_cache[movie_id]
    try:
        movie = client.get_movie(movie_id)
        genres = movie.genres  # Ex: "Comedy|Drama"
        genre_cache[movie_id] = genres
        return genres
    except Exception:
        return None

# Application sur la DataFrame
filtered_movies['genre'] = filtered_movies['movieId'].apply(get_genres_with_cache)


#################################################################


if selected_genres:
    filtered_movies = filtered_movies[filtered_movies['genre'].apply(lambda g: any(genre in g for genre in selected_genres))]

filtered_movies = filtered_movies[
    (filtered_movies['avg_rating'] >= selected_rating) &
    (filtered_movies['rating_count'] >= selected_votes) &
    (filtered_movies['year'].between(*selected_years))
]

if keyword:
    filtered_movies = filtered_movies[filtered_movies['title'].str.contains(keyword, case=False)]

if selected_tags:
    def has_tags(row):
        return all(tag in row.get('tags', '') for tag in selected_tags)
    if 'tags' in filtered_movies.columns:
        filtered_movies = filtered_movies[filtered_movies.apply(has_tags, axis=1)]

# === Résumé en haut ===
st.markdown("## 🔎 Résultats de la recherche")
k1, k2, k3 = st.columns(3)
k1.metric("🎞️ Nombre de films", len(filtered_movies))
k2.metric("⭐ Note moyenne", f"{filtered_movies['avg_rating'].mean():.2f}" if not filtered_movies.empty else "N/A")
k3.metric("👥 Votes moyens", f"{filtered_movies['rating_count'].mean():.0f}" if not filtered_movies.empty else "N/A")

# === Affichage des films sous forme de cartes ===
def generate_card(movie):
    imdb_url = meta_links.get(str(movie['movieId']), {}).get('imdb', "#")
    poster_url = meta_links.get(str(movie['movieId']), {}).get('poster', "https://via.placeholder.com/120x180?text=No+Image")

    with st.container():
        cols = st.columns([1, 4])
        with cols[0]:
            st.image(poster_url, width=120)
        with cols[1]:
            st.markdown(f"### [{movie['title']}]({imdb_url})")
            st.markdown(f"**Genres :** {movie['genre']}")
            st.markdown(f"**Note moyenne :** ⭐ {movie['avg_rating']:.2f}")
            st.markdown(f"**Nombre d'évaluations :** {movie['rating_count']}")
            if 'tags' in movie:
                st.markdown(f"**Tags :** *{movie['tags']}*")
        st.divider()

# Afficher les cartes pour les 20 premiers films
if filtered_movies.empty:
    st.warning("Aucun film ne correspond à vos critères.")
else:
    for _, movie in filtered_movies.sort_values("avg_rating", ascending=False).head(20).iterrows():
        generate_card(movie)
