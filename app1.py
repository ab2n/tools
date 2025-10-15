import streamlit as st
import pandas as pd
import requests
import io
import zipfile
import time

st.set_page_config(page_title="Téléchargeur d'images", page_icon="📦")

st.title("📦 Téléchargeur d'images depuis un fichier Excel ou CSV")

uploaded_file = st.file_uploader("📤 Upload ton fichier Excel ou CSV", type=["xlsx", "csv"])

if uploaded_file:
    # Lecture du fichier
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"Fichier chargé avec succès ({len(df)} lignes)")
    st.write("Aperçu des données :")
    st.dataframe(df.head())

    # Choisir la colonne contenant les URLs
    colonne_url = st.selectbox("🧭 Choisis la colonne contenant les URLs :", df.columns)

    if st.button("📥 Télécharger les images et créer un .zip"):
        urls = df[colonne_url].dropna().unique()
        total = len(urls)

        if total == 0:
            st.warning("Aucune URL trouvée dans cette colonne.")
        else:
            st.info(f"{total} images à télécharger...")

            progress_bar = st.progress(0)
            status_text = st.empty()

            # Créer un zip en mémoire
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i, url in enumerate(urls, start=1):
                    try:
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()
                        filename = f"image_{i:04d}.png"
                        zip_file.writestr(filename, response.content)
                    except Exception as e:
                        st.warning(f"❌ Impossible de télécharger {url} ({e})")

                    # Mise à jour de la progression
                    progress = int(i / total * 100)
                    progress_bar.progress(progress)
                    status_text.text(f"Téléchargement {i}/{total} ({progress}%)")
                    time.sleep(0.05)  # Petite pause pour fluidifier la progression

            st.success("✅ Téléchargement terminé !")

            # Préparer le bouton de téléchargement
            zip_buffer.seek(0)
            st.download_button(
                label="📦 Télécharger le fichier ZIP",
                data=zip_buffer,
                file_name="images.zip",
                mime="application/zip"
            )

st.markdown("---")
st.caption("🧰 Fait avec Streamlit – par ChatGPT")
