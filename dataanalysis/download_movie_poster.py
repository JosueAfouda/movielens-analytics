import pandas as pd
import requests
from pathlib import Path
from tqdm import tqdm

# === Configuration des chemins ===
BASE_DIR = Path(__file__).resolve().parent
output_dir = BASE_DIR / "output"
enriched_path = output_dir / "links_enriched.parquet"
poster_dir = output_dir / "posters"
poster_dir.mkdir(parents=True, exist_ok=True)

# === Charger les métadonnées enrichies ===
df = pd.read_parquet(enriched_path)

# === Fonction pour télécharger une image si elle n'existe pas déjà ===
def download_image(movie_id, url):
    try:
        filepath = poster_dir / f"{movie_id}.jpg"
        if filepath.exists():
            return str(filepath)

        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            return str(filepath)
        else:
            return None
    except Exception as e:
        print(f"Erreur pour movieId {movie_id} : {e}")
        return None

# === Télécharger les posters ===
local_paths = []
print("Téléchargement des affiches...")
for _, row in tqdm(df.iterrows(), total=len(df)):
    movie_id = row["movieId"]
    current_path = poster_dir / f"{movie_id}.jpg"

    if current_path.exists():
        local_paths.append(str(current_path))
    else:
        url = row["poster_url"]
        local_path = download_image(movie_id, url)
        local_paths.append(local_path)

df["local_poster_path"] = local_paths

# === Sauvegarde du fichier enrichi ===
df.to_parquet(enriched_path, index=False)
print("Téléchargement terminé. Fichier mis à jour :", enriched_path)

print("Affiches téléchargées et chemins locaux ajoutés au fichier enrichi.")
print(df.head())

# Pour chatgpt après 14:42
# Mais le problème est que moi j'ai arrêté le script. 
# Je ne suis pas sûr que la colonne "local_poster_path" a été créé puis sauvegarder dans links_enriched.parquet