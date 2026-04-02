import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Diagnostic Réglementaire GE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS personnalisé
# =========================
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #0f2747;
}
.result-box {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    border-left: 6px solid #163d73;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
.info-box {
    background-color: #eef4fb;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #d2e0f0;
    margin-bottom: 20px;
}
.small-title {
    font-size: 18px;
    font-weight: 700;
    color: #163d73;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Diagnostic Réglementaire du Groupe Électrogène")

st.markdown("""
<div class="info-box">
<div class="small-title">Contexte réglementaire</div>

Un <b>ERP (Établissement Recevant du Public)</b> est un bâtiment dans lequel des personnes extérieures sont admises, gratuitement ou non.
Le <b>type ERP</b> dépend de l’activité exercée, tandis que la <b>catégorie</b> dépend de l’effectif accueilli.

Cette application permet de :
<ul>
<li>déterminer la catégorie ERP,</li>
<li>identifier le groupe électrogène à prévoir,</li>
<li>afficher les équipements concernés,</li>
<li>justifier le choix selon le niveau d’exigence : <b>Secours</b>, <b>Sécurité</b> ou <b>Temps Zéro</b>.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =========================================================
# Base diagnostic GE
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
}

def expliquer_groupe(type_groupe):
    if "Temps Zéro" in type_groupe:
        return """
**Temps Zéro** : aucune coupure n’est admissible.  
Ce niveau est retenu lorsque les charges alimentées doivent rester disponibles instantanément, sans interruption de service.
"""
    elif "Sécurité" in type_groupe:
        return """
**Groupe de Sécurité** : il est destiné à alimenter les installations participant directement à la protection des personnes.
Ce choix est justifié lorsque l’établissement comporte des fonctions telles que l’éclairage de sécurité, le SSI, le désenfumage ou les équipements de survie.
"""
    elif "Secours" in type_groupe:
        return """
**Groupe de Secours** : il permet d’assurer la continuité d’exploitation pour les usages importants, sans exigence de maintien instantané.
Il est adapté aux charges techniques ou fonctionnelles dont une brève coupure reste admissible.
"""
    else:
        return "Pas d’exigence particulière selon la réglementation ERP pour ce cas."

def categorie_generale(effectif_total: int, seuil_5: int) -> int:
    if effectif_total > 1500:
        return 1
    elif 701 <= effectif_total <= 1500:
        return 2
    elif 301 <= effectif_total <= 700:
        return 3
    elif seuil_5 <= effectif_total <= 300:
        return 4
    else:
        return 5

def seuil_declenchement_standard(code, effectif_total, effectif_sous_sol, effectif_etage):
    regle = SEUILS_STANDARD.get(code)
    if not regle:
        return None
    seuil_base = min(v for v in regle.values() if v is not None)
    return seuil_base

def determiner_categorie_erp(code, effectif_total, effectif_sous_sol=0, effectif_etage=0):
    if effectif_total > 1500:
        return 1, "Effectif total > 1500."
    if 701 <= effectif_total <= 1500:
        return 2, "Effectif total entre 701 et 1500."
    if 301 <= effectif_total <= 700:
        return 3, "Effectif total entre 301 et 700."

    if code in SEUILS_STANDARD:
        seuil5 = seuil_declenchement_standard(code, effectif_total, effectif_sous_sol, effectif_etage)
        return categorie_generale(effectif_total, seuil5), f"Seuil réglementaire retenu = {seuil5}."

    if code in SEUILS_PERSONNALISES:
        seuil5 = SEUILS_PERSONNALISES[code]["total"]
        return categorie_generale(effectif_total, seuil5), f"Seuil personnalisé retenu = {seuil5}."

    if code == "U":
        seuil5 = 100
        return categorie_generale(effectif_total, seuil5), f"Type U : seuil retenu = {seuil5}."

    if code == "J":
        seuil5 = 100
        return categorie_generale(effectif_total, seuil5), f"Type J : seuil retenu = {seuil5}."

    if code == "L":
        seuil5 = 50
        return categorie_generale(effectif_total, seuil5), f"Type L : seuil retenu = {seuil5}."

    return categorie_generale(effectif_total, 100), "Seuil par défaut = 100."

def chercher_diagnostic_ge(code: str, categorie: int):
    resultat = df[
        (df["Code_type"].astype(str).str.strip().str.upper() == code.strip().upper()) &
        (df["Cat_Min"] <= categorie) &
        (df["Cat_Max"] >= categorie)
    ]
    return resultat.iloc[0] if not resultat.empty else None

# =========================
# Sidebar
# =========================
st.sidebar.header("⚙️ Paramètres du diagnostic")

erp_choice = st.sidebar.selectbox("Type d'établissement", list(erp_types.keys()))
effectif_total = st.sidebar.number_input("Effectif total admissible", min_value=0, step=1, value=0)
effectif_etage = st.sidebar.number_input("Effectif en étage", min_value=0, step=1, value=0)
effectif_sous_sol = st.sidebar.number_input("Effectif en sous-sol", min_value=0, step=1, value=0)

code = erp_types[erp_choice]

if effectif_etage + effectif_sous_sol > effectif_total:
    st.warning("La somme effectif étage + sous-sol dépasse l’effectif total.")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
    <div class="result-box">
        <h3>🔎 Données d’entrée</h3>
        <p><b>Type ERP sélectionné :</b> {erp_choice}</p>
        <p><b>Effectif total :</b> {effectif_total}</p>
        <p><b>Effectif en étage :</b> {effectif_etage}</p>
        <p><b>Effectif en sous-sol :</b> {effectif_sous_sol}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="result-box">
        <h3>📌 Lancement</h3>
    </div>
    """, unsafe_allow_html=True)
    lancer = st.button("Lancer le diagnostic réglementaire")

if lancer:
    categorie, justification = determiner_categorie_erp(
        code=code,
        effectif_total=effectif_total,
        effectif_sous_sol=effectif_sous_sol,
        effectif_etage=effectif_etage,
    )

    row = chercher_diagnostic_ge(code, categorie)

    c1, c2, c3 = st.columns(3)
    c1.metric("Catégorie ERP", categorie)
    c2.metric("Code ERP", code)
    c3.metric("Effectif total", effectif_total)

    st.markdown(f"""
    <div class="result-box">
        <h3>📖 Justification réglementaire</h3>
        <p>{justification}</p>
    </div>
    """, unsafe_allow_html=True)

    if row is not None:
        type_grp = row["Type_Groupe"]
        explication = expliquer_groupe(type_grp).replace("\n", "<br>")

        st.markdown(f"""
        <div class="result-box">
            <h3>⚡ Résultat du diagnostic</h3>
            <p><b>Désignation :</b> {row['Designation']}</p>
            <p><b>Type de groupe recommandé :</b> {type_grp}</p>
            <p><b>Équipements concernés :</b> {row['Equipements']}</p>
            <h4>Pourquoi ce groupe ?</h4>
            <p>{explication}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Pas d’exigence particulière selon la réglementation ERP pour ce cas.")

with st.expander("📂 Voir la base de diagnostic utilisée"):
    st.dataframe(df, use_container_width=True)
