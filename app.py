import streamlit as st
import pandas as pd

# =========================================================
# CONFIG PAGE
# =========================================================
st.set_page_config(
    page_title="Diagnostic Réglementaire GE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS PERSONNALISÉ
# =========================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f4f7fb 0%, #eaf1fb 100%);
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #0f2747;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 16px;
        color: #4b6280;
        margin-bottom: 1.5rem;
    }

    .info-box {
        background: linear-gradient(135deg, #eef4fb 0%, #f8fbff 100%);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #d4e1f2;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e4ebf5;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        margin-bottom: 18px;
    }

    .card h3 {
        color: #163d73;
        margin-bottom: 10px;
    }

    .small-title {
        font-size: 17px;
        font-weight: 700;
        color: #163d73;
        margin-bottom: 10px;
    }

    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        border: 1px solid #e4ebf5;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    }

    .metric-label {
        font-size: 13px;
        color: #6b7b93;
        font-weight: 600;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #0f2747;
    }

    .metric-sub {
        font-size: 13px;
        color: #70839c;
        margin-top: 4px;
    }

    .badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
        margin-top: 6px;
        margin-bottom: 10px;
    }

    .badge-securite {
        background-color: #fff4db;
        color: #b26a00;
        border: 1px solid #f2cf75;
    }

    .badge-secours {
        background-color: #eaf4ff;
        color: #0d63b8;
        border: 1px solid #8ec2f5;
    }

    .badge-tempszero {
        background-color: #ffe9e9;
        color: #c62828;
        border: 1px solid #f2a4a4;
    }

    .badge-neutre {
        background-color: #f2f4f7;
        color: #667085;
        border: 1px solid #d0d5dd;
    }

    .result-box-securite {
        background: linear-gradient(135deg, #fffaf0 0%, #fff4db 100%);
        border: 1px solid #f2cf75;
        border-left: 8px solid #e0a100;
        padding: 22px;
        border-radius: 18px;
        margin-top: 10px;
        box-shadow: 0 6px 18px rgba(224,161,0,0.10);
    }

    .result-box-secours {
        background: linear-gradient(135deg, #f4f9ff 0%, #eaf4ff 100%);
        border: 1px solid #8ec2f5;
        border-left: 8px solid #0d63b8;
        padding: 22px;
        border-radius: 18px;
        margin-top: 10px;
        box-shadow: 0 6px 18px rgba(13,99,184,0.10);
    }

    .result-box-tempszero {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe9e9 100%);
        border: 1px solid #f2a4a4;
        border-left: 8px solid #d32f2f;
        padding: 22px;
        border-radius: 18px;
        margin-top: 10px;
        box-shadow: 0 6px 18px rgba(211,47,47,0.10);
    }

    .result-box-neutre {
        background: linear-gradient(135deg, #fafafa 0%, #f2f4f7 100%);
        border: 1px solid #d0d5dd;
        border-left: 8px solid #98a2b3;
        padding: 22px;
        border-radius: 18px;
        margin-top: 10px;
        box-shadow: 0 6px 18px rgba(152,162,179,0.10);
    }

    .note-box {
        background-color: #fff8e6;
        border: 1px solid #f2d27a;
        color: #7a5a00;
        padding: 14px 16px;
        border-radius: 12px;
        margin-top: 14px;
    }

    .footer-note {
        font-size: 13px;
        color: #667085;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# TITRE
# =========================================================
st.markdown('<div class="main-title">⚡ Diagnostic Réglementaire du Groupe Électrogène</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Détermination de la catégorie ERP et du niveau de groupe électrogène recommandé : Aucun, Secours, Sécurité ou Temps Zéro.</div>',
    unsafe_allow_html=True
)

# =========================================================
# CONTEXTE
# =========================================================
st.markdown("""
<div class="info-box">
    <div class="small-title">Contexte réglementaire</div>
    Un <b>ERP (Établissement Recevant du Public)</b> est classé selon :
    <ul>
        <li><b>son type</b> : activité exercée (hôpital, hôtel, restaurant, bureau, etc.) ;</li>
        <li><b>sa catégorie</b> : effectif du public et du personnel admis.</li>
    </ul>
    Cette application permet de :
    <ul>
        <li>déterminer la <b>catégorie ERP</b>,</li>
        <li>tenir compte de l’<b>effectif total</b>, de l’<b>effectif en étage</b> et de l’<b>effectif en sous-sol</b>,</li>
        <li>identifier le <b>niveau de groupe électrogène</b> à prévoir,</li>
        <li>afficher les <b>équipements concernés</b>,</li>
        <li>justifier le choix selon le niveau d’exigence : <b>Secours</b>, <b>Sécurité</b> ou <b>Temps Zéro</b>.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# =========================================================
# BASE DIAGNOSTIC
# =========================================================
data = [
    ["U", "Santé (Hôpitaux)", 1, 4, "Sécurité", "Vital pour blocs opératoires, réanimation, monitoring, SSI, respirateurs, éclairage de sécurité."],
    ["J", "Âgées / Handicapés", 1, 4, "Sécurité", "SSI, SMSI, DAS (portes/clapets), lits médicalisés, désenfumage, sonorisation d'évacuation."],
    ["O", "Hôtels / Pensions", 1, 4, "Sécurité", "Alarme incendie nocturne, balisage des circulations, désenfumage des escaliers."],
    ["Rh", "Internats", 1, 4, "Sécurité", "Protection du public endormi, alerte incendie, SSI, balisage de secours."],
    ["OA", "Hôtels d'altitude", 1, 5, "Sécurité", "Survie en cas d'isolement (chauffage, éclairage), détection incendie."],
    ["L", "Salles spectacles", 1, 2, "Sécurité", "Éclairage anti-panique, sonorisation évacuation, DAS, désenfumage mécanique."],
    ["P", "Salles de danse", 1, 3, "Sécurité", "Éclairage haute puissance pour évacuation rapide, SSI, SMSI."],
    ["Y", "Musées", 1, 3, "Secours", "Conservation hygrométrique, anti-intrusion, caméras, détection incendie."],
    ["X", "Établissements sportifs", 1, 3, "Secours", "Maintien filtration et chauffage des bassins, éclairage des terrains."],
    ["V", "Lieux de culte", 1, 5, "Aucun", "Risque de panique jugé faible par la réglementation."],
    ["M", "Centres Com.", 1, 2, "Secours", "Centrale froid (stocks), encaissement, désenfumage, détection intrusion."],
    ["N", "Restaurants / Cafés", 1, 3, "Secours", "Optionnel (chaîne du froid, éclairage d'ambiance)."],
    ["W", "Banques / Bureaux", 1, 2, "Temps Zéro", "Données essentielles, serveurs, Poste Central de Sécurité (PCS), onduleurs."],
    ["S", "Bibliothèques", 1, 5, "Aucun/Secours", "GE si conservation climatique des archives rares ou systèmes anti-vol."],
    ["T", "Salles d'exposition", 1, 2, "Sécurité", "Éclairage des stands, SSI, protection contre le vol."],
    ["GA", "Gares", 1, 3, "Sécurité", "Désenfumage massif, escaliers mécaniques, signalétique, PCS."],
    ["PS", "Parkings couverts", 1, 5, "Sécurité", "Extraction fumées toxiques, détection CO/NOx, insufflation."],
    ["EF", "Établissements flottants", 1, 5, "Sécurité", "Pompes de cale (épuisement anti-naufrage), alarme, éclairage."],
    ["SG", "Structures gonflables", 1, 5, "Sécurité", "Ventilateurs de maintien de pression (stabilité)."],
    ["BM", "Bains maures", 1, 4, "Secours", "Extraction vapeur, éclairage de sécurité en milieu humide."],
    ["IGH", "Immeubles Grde Ht.", 1, 5, "Sécurité (Redondé)", "Ascenseurs pompiers, surpresseurs incendie, SMSI."],
    ["MIL", "Défense / Radars", 1, 5, "Temps Zéro + Tactique", "Surveillance radar, transmissions, filtration NBC."],
    ["AER", "Aéroports", 1, 5, "Temps Zéro", "Balisage pistes (décollage/atterrissage), tour de contrôle."]
]

df = pd.DataFrame(
    data,
    columns=["Code_type", "Designation", "Cat_Min", "Cat_Max", "Type_Groupe", "Equipements"]
)

erp_types = {
    "U - Santé (Hôpitaux)": "U",
    "J - Âgées / Handicapés": "J",
    "O - Hôtels / Pensions": "O",
    "Rh - Internats": "Rh",
    "OA - Hôtels d'altitude": "OA",
    "L - Salles spectacles": "L",
    "P - Salles de danse": "P",
    "Y - Musées": "Y",
    "X - Établissements sportifs": "X",
    "V - Lieux de culte": "V",
    "M - Centres Com.": "M",
    "N - Restaurants / Cafés": "N",
    "W - Banques / Bureaux": "W",
    "S - Bibliothèques": "S",
    "T - Salles d'exposition": "T",
    "GA - Gares": "GA",
    "PS - Parkings couverts": "PS",
    "EF - Établissements flottants": "EF",
    "SG - Structures gonflables": "SG",
    "BM - Bains maures": "BM",
    "IGH - Immeubles Grde Ht.": "IGH",
    "MIL - Défense / Radars": "MIL",
    "AER - Aéroports": "AER",
}

# =========================================================
# SEUILS 5ÈME CATÉGORIE
# =========================================================
SEUILS_STANDARD = {
    "M": {"sous_sol": 100, "etage": 100, "total": 200},
    "N": {"sous_sol": 100, "etage": 200, "total": 200},
    "O": {"sous_sol": None, "etage": None, "total": 100},
    "P": {"sous_sol": 20, "etage": 100, "total": 120},
    "S": {"sous_sol": 100, "etage": 100, "total": 200},
    "T": {"sous_sol": 100, "etage": 100, "total": 200},
    "V": {"sous_sol": 100, "etage": 200, "total": 300},
    "W": {"sous_sol": 100, "etage": 100, "total": 200},
    "X": {"sous_sol": 100, "etage": 100, "total": 200},
    "Y": {"sous_sol": 100, "etage": 100, "total": 200},
    "OA": {"sous_sol": None, "etage": None, "total": 20},
    "GA": {"sous_sol": None, "etage": None, "total": 200},
}

SEUILS_PERSONNALISES = {
    "Rh": {"total": 100},
    "PS": {"total": 300},
    "EF": {"total": 100},
    "SG": {"total": 50},
    "BM": {"total": 100},
    "IGH": {"total": 1},
    "MIL": {"total": 1},
    "AER": {"total": 1},
    "U": {"total": 100},
    "J": {"total": 100},
    "L": {"total": 50},
}

# =========================================================
# FONCTIONS
# =========================================================
def get_badge_html(type_groupe):
    tg = type_groupe.lower()
    if "temps zéro" in tg:
        return f'<span class="badge badge-tempszero">⚡ {type_groupe}</span>'
    elif "sécurité" in tg:
        return f'<span class="badge badge-securite">🛡️ {type_groupe}</span>'
    elif "secours" in tg:
        return f'<span class="badge badge-secours">🔋 {type_groupe}</span>'
    else:
        return f'<span class="badge badge-neutre">ℹ️ {type_groupe}</span>'

def get_result_box_class(type_groupe):
    tg = type_groupe.lower()
    if "temps zéro" in tg:
        return "result-box-tempszero"
    elif "sécurité" in tg:
        return "result-box-securite"
    elif "secours" in tg:
        return "result-box-secours"
    else:
        return "result-box-neutre"

def expliquer_groupe(type_groupe):
    if "Temps Zéro" in type_groupe:
        return """
<b>Temps Zéro</b> : aucune coupure n’est admissible.<br>
Ce niveau est retenu lorsque les charges alimentées doivent rester disponibles instantanément, sans interruption de service.
"""
    elif "Sécurité" in type_groupe:
        return """
<b>Groupe de Sécurité</b> : il est destiné à alimenter les installations participant directement à la protection des personnes.<br>
Ce choix est justifié lorsque l’établissement comporte des fonctions telles que l’éclairage de sécurité, le SSI, le désenfumage ou les équipements de survie.
"""
    elif "Secours" in type_groupe:
        return """
<b>Groupe de Secours</b> : il permet d’assurer la continuité d’exploitation pour les usages importants, sans exigence de maintien instantané.<br>
Il est adapté aux charges techniques ou fonctionnelles dont une brève coupure reste admissible.
"""
    else:
        return "Pas d’exigence particulière selon la réglementation ERP pour ce cas."

def chercher_diagnostic_ge(code: str, categorie: int):
    resultat = df[
        (df["Code_type"].astype(str).str.strip().str.upper() == code.strip().upper()) &
        (df["Cat_Min"] <= categorie) &
        (df["Cat_Max"] >= categorie)
    ]
    return resultat.iloc[0] if not resultat.empty else None

def get_seuil_info(code):
    if code in SEUILS_STANDARD:
        return SEUILS_STANDARD[code]
    if code in SEUILS_PERSONNALISES:
        return SEUILS_PERSONNALISES[code]
    return {"total": 100}

def determiner_categorie_erp(code, effectif_total, effectif_sous_sol=0, effectif_etage=0):
    # Catégories 1, 2, 3
    if effectif_total > 1500:
        return 1, "Effectif total > 1500."
    if 701 <= effectif_total <= 1500:
        return 2, "Effectif total entre 701 et 1500."
    if 301 <= effectif_total <= 700:
        return 3, "Effectif total entre 301 et 700."

    regle = get_seuil_info(code)
    seuil_total = regle.get("total", 100)
    seuil_sous_sol = regle.get("sous_sol", None)
    seuil_etage = regle.get("etage", None)

    motifs_depassement = []

    if seuil_sous_sol is not None and effectif_sous_sol >= seuil_sous_sol:
        motifs_depassement.append(f"effectif sous-sol ({effectif_sous_sol}) ≥ seuil sous-sol ({seuil_sous_sol})")

    if seuil_etage is not None and effectif_etage >= seuil_etage:
        motifs_depassement.append(f"effectif étage ({effectif_etage}) ≥ seuil étage ({seuil_etage})")

    if effectif_total >= seuil_total:
        motifs_depassement.append(f"effectif total ({effectif_total}) ≥ seuil total ({seuil_total})")

    if motifs_depassement:
        justification = "Classement en 4ᵉ catégorie car " + " ; ".join(motifs_depassement) + "."
        return 4, justification
    else:
        justification = f"Classement en 5ᵉ catégorie car les effectifs restent inférieurs aux seuils applicables (total = {seuil_total}"
        if seuil_etage is not None:
            justification += f", étage = {seuil_etage}"
        if seuil_sous_sol is not None:
            justification += f", sous-sol = {seuil_sous_sol}"
        justification += ")."
        return 5, justification

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("⚙️ Paramètres du diagnostic")

erp_choice = st.sidebar.selectbox("Type d'établissement", list(erp_types.keys()))
effectif_total = st.sidebar.number_input("Effectif total admissible", min_value=0, step=1, value=0)
effectif_etage = st.sidebar.number_input("Effectif en étage", min_value=0, step=1, value=0)
effectif_sous_sol = st.sidebar.number_input("Effectif en sous-sol", min_value=0, step=1, value=0)

code = erp_types[erp_choice]

if effectif_etage + effectif_sous_sol > effectif_total:
    st.sidebar.warning("La somme étage + sous-sol dépasse l’effectif total.")

lancer = st.sidebar.button("🚀 Lancer le diagnostic", use_container_width=True)

# =========================================================
# AFFICHAGE ENTRÉES
# =========================================================
col1, col2 = st.columns([1.1, 1])

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>🔎 Données d’entrée</h3>
        <p><b>Type ERP sélectionné :</b> {erp_choice}</p>
        <p><b>Code :</b> {code}</p>
        <p><b>Effectif total :</b> {effectif_total}</p>
        <p><b>Effectif en étage :</b> {effectif_etage}</p>
        <p><b>Effectif en sous-sol :</b> {effectif_sous_sol}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    seuil_info = get_seuil_info(code)
    seuil_total = seuil_info.get("total", "—")
    seuil_etage = seuil_info.get("etage", "—")
    seuil_sous_sol = seuil_info.get("sous_sol", "—")

    st.markdown(f"""
    <div class="card">
        <h3>📌 Seuils de référence (5ᵉ catégorie)</h3>
        <p><b>Seuil total :</b> {seuil_total}</p>
        <p><b>Seuil étage :</b> {seuil_etage}</p>
        <p><b>Seuil sous-sol :</b> {seuil_sous_sol}</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# DIAGNOSTIC
# =========================================================
if lancer:
    if effectif_etage + effectif_sous_sol > effectif_total:
        st.error("La somme de l’effectif en étage et en sous-sol ne doit pas dépasser l’effectif total.")
    else:
        categorie, justification = determiner_categorie_erp(
            code=code,
            effectif_total=effectif_total,
            effectif_sous_sol=effectif_sous_sol,
            effectif_etage=effectif_etage
        )

        row = chercher_diagnostic_ge(code, categorie)

        st.markdown("## Résultat du diagnostic")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Catégorie ERP</div>
                <div class="metric-value">{categorie}</div>
                <div class="metric-sub">Catégorie déterminée</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Code ERP</div>
                <div class="metric-value">{code}</div>
                <div class="metric-sub">{erp_choice}</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Effectif total</div>
                <div class="metric-value">{effectif_total}</div>
                <div class="metric-sub">Public + personnel</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>📖 Justification réglementaire</h3>
            <p>{justification}</p>
        </div>
        """, unsafe_allow_html=True)

        if row is not None:
            type_grp = row["Type_Groupe"]
            explication = expliquer_groupe(type_grp)
            badge_html = get_badge_html(type_grp)
            result_class = get_result_box_class(type_grp)

            st.markdown(f"""
            <div class="{result_class}">
                <h3>⚡ Résultat du diagnostic</h3>
                {badge_html}
                <p><b>Désignation :</b> {row['Designation']}</p>
                <p><b>Type de groupe recommandé :</b> {type_grp}</p>
                <p><b>Équipements concernés :</b> {row['Equipements']}</p>
                <h4>Pourquoi ce groupe ?</h4>
                <p>{explication}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="note-box">
                <b>Remarque :</b> ce résultat constitue un pré-diagnostic réglementaire. 
                Il doit être complété par une étude détaillée du projet, des normes applicables et des charges réellement secourues.
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("Pas d’exigence particulière selon la réglementation ERP pour ce cas.")

# =========================================================
# BASE DE DONNÉES
# =========================================================
with st.expander("📂 Voir la base de diagnostic utilisée"):
    st.dataframe(df, use_container_width=True)

st.markdown('<div class="footer-note">Application de pré-diagnostic ERP / Groupe électrogène.</div>', unsafe_allow_html=True)
