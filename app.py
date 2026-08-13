import streamlit as st
import pandas as pd
import joblib
import base64
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Risque Maternel IA", page_icon="🩺", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
MODEL_PATH = BASE_DIR / "random_forest_risque_maternel.pkl"
LOGIN_IMAGE = ASSETS_DIR / "login.png"
HOME_IMAGE = ASSETS_DIR / "accueil.png"

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
header {visibility:hidden;}
footer {visibility:hidden;}
.block-container {padding-top:1.5rem; max-width:1450px;}
.title {font-size:42px;font-weight:800;line-height:1.2;}
.subtitle {font-size:19px;opacity:.72;line-height:1.6;margin-bottom:25px;}
.card {padding:28px;border-radius:20px;border:1px solid rgba(100,120,150,.18);box-shadow:0 8px 30px rgba(0,30,80,.07);margin-bottom:20px;}
.login-title {font-size:38px;font-weight:800;text-align:center;margin-top:35px;}
.login-subtitle {text-align:center;opacity:.7;line-height:1.6;margin-bottom:25px;}
.result-high {padding:25px;border-radius:18px;text-align:center;background:rgba(220,40,40,.08);border:1px solid rgba(220,40,40,.25);}
.result-low {padding:25px;border-radius:18px;text-align:center;background:rgba(20,160,90,.08);border:1px solid rgba(20,160,90,.25);}
.result-title {font-size:30px;font-weight:800;}
.confidence {font-size:21px;font-weight:700;margin-top:8px;}
.disclaimer {padding:18px;border-radius:15px;background:rgba(30,90,200,.07);border:1px solid rgba(30,90,200,.15);line-height:1.6;margin-top:25px;}
.stButton > button {min-height:45px;border-radius:11px;font-weight:700;}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "accueil"
if "email" not in st.session_state:
    st.session_state.email = ""

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None, f"Modèle introuvable : {MODEL_PATH}"
    try:
        return joblib.load(MODEL_PATH), None
    except Exception as error:
        return None, str(error)

modele, model_error = load_model()

# =========================================================
# CONNEXION — SANS PHOTO
# =========================================================

def page_connexion():

    st.markdown("""
    <div class="app-header">
        <div class="logo">🩺</div>
        <div class="app-title">RISQUE MATERNEL IA</div>
        <div class="app-subtitle">
            Intelligence artificielle pour l'aide à l'évaluation
            du risque maternel
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.markdown(
        '<div class="login-icon">🔐</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">Bienvenue</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-text">'
        'Connectez-vous pour accéder à votre espace.'
        '</div>',
        unsafe_allow_html=True
    )

    email = st.text_input(
        "📧 Adresse e-mail",
        placeholder="exemple@gmail.com"
    )

    password = st.text_input(
        "🔑 Mot de passe",
        type="password",
        placeholder="Votre mot de passe"
    )

    if st.button(
        "🚀 SE CONNECTER",
        width="stretch",
        type="primary"
    ):

        if not email.strip():

            st.warning(
                "Veuillez saisir votre adresse e-mail."
            )

        elif "@" not in email or "." not in email.split("@")[-1]:

            st.error(
                "Veuillez saisir une adresse e-mail valide."
            )

        elif not password:

            st.warning(
                "Veuillez saisir votre mot de passe."
            )

        elif len(password) < 6:

            st.warning(
                "Le mot de passe doit contenir au moins 6 caractères."
            )

        else:

            st.session_state.logged_in = True
            st.session_state.email = email.strip()
            st.session_state.page = "accueil"

            st.rerun()

    st.caption(
        "Interface de démonstration. "
        "Cette connexion n'est pas un système "
        "d'authentification sécurisé de production."
    )

    st.markdown('</div>', unsafe_allow_html=True)

def menu():
    st.markdown('<div style="text-align:center;font-weight:800;font-size:18px;margin-bottom:12px;">🩺 RISQUE MATERNEL IA</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        if st.button("🏠 Accueil", width="stretch"):
            st.session_state.page = "accueil"
            st.rerun()
    with c2:
        if st.button("📖 À propos", width="stretch"):
            st.session_state.page = "apropos"
            st.rerun()
    with c3:
        if st.button("📚 Documentation", width="stretch"):
            st.session_state.page = "documentation"
            st.rerun()
    with c4:
        if st.button("🔮 Prédiction", width="stretch"):
            st.session_state.page = "prediction"
            st.rerun()
    with c5:
        if st.button("🚪 Déconnexion", width="stretch"):
            st.session_state.logged_in = False
            st.session_state.email = ""
            st.session_state.page = "accueil"
            st.rerun()

    st.caption(f"Connecté : {st.session_state.email}")

def page_accueil():
    st.markdown('<div class="title">Bienvenue sur Risque Maternel IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Une plateforme d’aide à l’évaluation du risque maternel basée sur l’intelligence artificielle.</div>', unsafe_allow_html=True)
    if HOME_IMAGE.exists():
        st.image(Image.open(HOME_IMAGE), width="stretch")
    else:
        st.warning("Image introuvable : assets/accueil.png")
    st.markdown('<div class="disclaimer">🩺 <strong>Important :</strong> le résultat fourni par le modèle est une estimation algorithmique. Il ne remplace pas l’évaluation d’un professionnel de santé.</div>', unsafe_allow_html=True)

def page_apropos():
    st.markdown('<div class="title">📖 À propos du projet</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Présentation du projet.</div>', unsafe_allow_html=True)

    pdf_files = list(BASE_DIR.glob("*.pdf")) + list(ASSETS_DIR.glob("*.pdf"))
    if pdf_files:
        pdf_path = pdf_files[0]
        st.success(f"Document chargé : {pdf_path.name}")
        with open(pdf_path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode("utf-8")
        st.markdown(f'<iframe src="data:application/pdf;base64,{encoded}" width="100%" height="900" style="border:none;border-radius:15px;"></iframe>', unsafe_allow_html=True)
    else:
        st.info("Aucun PDF trouvé. Place ton document PDF dans le dossier du projet ou dans assets.")

def page_documentation():
    st.markdown('<div class="title">📚 Documentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Fonctionnement de la plateforme.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><h3>🤖 Intelligence artificielle</h3>Le système utilise un modèle de classification Random Forest pour produire une estimation du niveau de risque.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3>📊 Variables utilisées</h3>• Age<br>• SystolicBP<br>• BS<br>• BodyTemp<br>• HeartRate<br>• DiastolicBP</div>', unsafe_allow_html=True)

    st.markdown('<div class="disclaimer">⚠️ La prédiction est une estimation issue d’un modèle d’apprentissage automatique et ne constitue pas un diagnostic médical.</div>', unsafe_allow_html=True)

def page_prediction():
    st.markdown('<div class="title">🔮 Prédiction du risque maternel</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Saisissez les six paramètres demandés puis lancez la prédiction.</div>', unsafe_allow_html=True)

    if modele is None:
        st.error("Le modèle n’a pas pu être chargé.")
        st.code(model_error or "Erreur inconnue.")
        return

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Âge (Age)", min_value=0.0, max_value=120.0, value=25.0, step=1.0)
        systolic = st.number_input("Pression systolique (SystolicBP)", min_value=0.0, max_value=300.0, value=120.0, step=1.0)
        bs = st.number_input("Glycémie (BS)", min_value=0.0, max_value=100.0, value=6.0, step=0.1)
    with col2:
        body_temp = st.number_input("Température corporelle (BodyTemp)", min_value=0.0, max_value=120.0, value=98.6, step=0.1)
        heart_rate = st.number_input("Fréquence cardiaque (HeartRate)", min_value=0.0, max_value=300.0, value=75.0, step=1.0)
        diastolic = st.number_input("Pression diastolique (DiastolicBP)", min_value=0.0, max_value=250.0, value=80.0, step=1.0)

    if not st.button("🔮 LANCER LA PRÉDICTION", width="stretch", type="primary"):
        return

    donnees = pd.DataFrame(
        [[age, systolic, bs, body_temp, heart_rate, diastolic]],
        columns=["Age", "SystolicBP", "BS", "BodyTemp", "HeartRate", "DiastolicBP"],
    )

    try:
        prediction = modele.predict(donnees)[0]
        probabilites = modele.predict_proba(donnees)[0]
    except Exception as error:
        st.error("Erreur lors de la prédiction.")
        st.code(str(error))
        return

    classes = list(modele.classes_)
    prediction_index = classes.index(prediction)
    confiance = float(probabilites[prediction_index] * 100)

    st.divider()
    st.subheader("📊 Résultat")

    if prediction == "high risk":
        st.markdown(f'<div class="result-high"><div class="result-title">🔴 Risque maternel élevé</div><div class="confidence">Confiance du modèle : {confiance:.2f} %</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="result-low"><div class="result-title">🟢 Risque maternel faible</div><div class="confidence">Confiance du modèle : {confiance:.2f} %</div></div>', unsafe_allow_html=True)

    prob_high = 0.0
    prob_low = 0.0
    for classe, proba in zip(modele.classes_, probabilites):
        if classe == "high risk":
            prob_high = float(proba * 100)
        elif classe == "low risk":
            prob_low = float(proba * 100)

    st.subheader("📈 Probabilités")
    p1, p2 = st.columns(2)
    with p1:
        st.metric("🔴 High risk", f"{prob_high:.2f} %")
    with p2:
        st.metric("🟢 Low risk", f"{prob_low:.2f} %")

    tableau = pd.DataFrame({
        "Classe": modele.classes_,
        "Probabilité (%)": [round(float(x) * 100, 2) for x in probabilites],
    })
    st.dataframe(tableau, width="stretch", hide_index=True)

    with st.expander("🔎 Voir les données envoyées au modèle"):
        st.dataframe(donnees, width="stretch", hide_index=True)

    with st.expander("⚙️ Informations techniques"):
        st.write("Classes du modèle :", list(modele.classes_))
        if hasattr(modele, "feature_names_in_"):
            st.write("Variables attendues :", list(modele.feature_names_in_))

    st.markdown('<div class="disclaimer">🩺 <strong>Important :</strong> cette prédiction est une estimation produite par un modèle d’intelligence artificielle. Elle ne constitue pas un diagnostic médical et ne remplace pas l’avis d’un professionnel de santé.</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    page_connexion()
    st.stop()

menu()

if st.session_state.page == "accueil":
    page_accueil()
elif st.session_state.page == "apropos":
    page_apropos()
elif st.session_state.page == "documentation":
    page_documentation()
elif st.session_state.page == "prediction":
    page_prediction()
else:
    st.session_state.page = "accueil"
    st.rerun()