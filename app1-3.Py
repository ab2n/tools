import streamlit as st
import json
import os

st.title("Recherche fichiers BU Projet")

# Charger le JSON
with open("arborescence.json", "r", encoding="utf-8") as f:
    files_data = json.load(f)

query = st.text_input("Que cherchez-vous ?")

if query:
    results = [f for f in files_data if query.lower() in f.get("title","").lower()]
    st.write(f"{len(results)} résultats trouvés :")
    
    for r in results:
        st.write(f"**{r['title']}** - {r['path']}")
        if st.button(f"Ouvrir {r['title']}", key=r['path']):
            os.startfile(r['path'])
