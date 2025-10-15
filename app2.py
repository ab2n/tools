import json
import openai  # pip install openai

# --- CONFIG ---
openai.api_key = "TON_API_KEY"  # Remplace par ta clé

# Fichier JSON exporté de Streamlit
input_file = "notes_streamlit.json"
output_file = "notes_retraite.json"

# Prompt générique pour OD v2/v3
def build_prompt(segment_text):
    return f"""
Tu es l'Opérateur de Décision Ultime.

Voici un segment de notes brutes :
\"\"\"{segment_text}\"\"\"

Rends uniquement la sortie structurée JSON avec les champs suivants :
- version_pre_machee: {{"objectif": "...", "ressources": "...", "blocages": "...", "parties_prenantes": "..."}}
- role_reel: "..."
- checklist_a_trous: [...]
- plan_action: {{"decision_recommandee": "...", "confiance": "...", "checklist_etapes": [...], "alternatives": [...]} }
- meta: "..."

Aucune explication, retourne uniquement un objet JSON.
"""

# --- LECTURE JSON INITIAL ---
with open(input_file, "r", encoding="utf-8") as f:
    segments = json.load(f)

retraite_segments = []

# --- TRAITEMENT SEGMENT PAR SEGMENT ---
for seg in segments:
    texte = seg.get("texte", "")
    
    prompt = build_prompt(texte)
    
    # Appel API OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    # Le modèle renvoie un JSON dans le texte
    try:
        json_retraite = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print(f"Erreur JSON pour segment {seg['id']}")
        json_retraite = {}

    retraite_segments.append({
        "id": seg["id"],
        "texte_original": texte,
        "texte_retraite": json_retraite
    })

# --- ÉCRITURE DU JSON RETRAITÉ ---
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(retraite_segments, f, ensure_ascii=False, indent=2)

print(f"JSON retraité généré : {output_file}")
