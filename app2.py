import json
import openai  # pip install openai

# --- CONFIG ---
openai.api_key = "TON_API_KEY"  # Remplace par ta clé

input_file = "notes_streamlit.json"  # JSON export Streamlit
output_file = "notes_retraite.json"  # JSON retraité généré

# --- Fonction pour construire le prompt OD v3 ---
def build_prompt(segment_text):
    prompt = (
        "Tu es l'Opérateur de Décision Ultime.\n\n"
        "Voici un segment de notes brutes :\n"
        f"\"\"\"{segment_text}\"\"\"\n\n"
        "Rends uniquement la sortie structurée JSON avec les champs suivants :\n"
        "- version_pre_machee: {\"objectif\": \"...\", \"ressources\": \"...\", \"blocages\": \"...\", \"parties_prenantes\": \"...\"}\n"
        "- role_reel: \"...\"\n"
        "- checklist_a_trous: [...]\n"
        "- plan_action: {\"decision_recommandee\": \"...\", \"confiance\": \"...\", \"checklist_etapes\": [...], \"alternatives\": [...]}\n"
        "- meta: \"...\"\n\n"
        "Aucune explication, retourne uniquement un objet JSON."
    )
    return prompt

# --- Lecture du JSON initial ---
with open(input_file, "r", encoding="utf-8") as f:
    segments = json.load(f)

retraite_segments = []

# --- Traitement segment par segment ---
for seg in segments:
    texte = seg.get("texte", "")
    
    prompt = build_prompt(texte)
    
    # Appel API OpenAI GPT-5-mini
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    # Récupération du JSON généré par GPT
    try:
        json_retraite = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print(f"Erreur JSON pour segment {seg['id']}, segment laissé vide")
        json_retraite = {}

    retraite_segments.append({
        "id": seg["id"],
        "texte_original": texte,
        "texte_retraite": json_retraite
    })

# --- Écriture du JSON retraité ---
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(retraite_segments, f, ensure_ascii=False, indent=2)

print(f"JSON retraité généré : {output_file}")
