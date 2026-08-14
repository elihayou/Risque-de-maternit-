from pathlib import Path
import re

import joblib
import pandas as pd
import streamlit as st
from PIL import Image


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Risque Maternel IA",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CHEMINS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

MODEL_PATH = BASE_DIR / "random_forest_risque_maternel.pkl"

HOME_IMAGE = ASSETS_DIR / "accueil.png"
HERO_IMAGE = ASSETS_DIR / "hero.png"
LOGOS_IMAGE = ASSETS_DIR / "logos.png"
PDF_PATH = ASSETS_DIR / "document_projet.pdf"


# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "email" not in st.session_state:
    st.session_state.email = ""

if "page" not in st.session_state:
    st.session_state.page = "accueil"

if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "prediction_step" not in st.session_state:
    st.session_state.prediction_step = 0

if "prediction_values" not in st.session_state:
    st.session_state.prediction_values = {}

if "dernier_resultat" not in st.session_state:
    st.session_state.dernier_resultat = None


# =========================================================
# STYLE
# =========================================================

def appliquer_style():

    dark = st.session_state.theme == "dark"

    if dark:
        background = "#0f172a"
        text = "#f8fafc"
        secondary = "#cbd5e1"
        card = "#1e293b"
    else:
        background = "#f5f8fc"
        text = "#0f172a"
        secondary = "#64748b"
        card = "#ffffff"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background};
            color: {text};
        }}

        .main-title {{
            font-size: 42px;
            font-weight: 800;
            color: {text};
        }}

        .subtitle {{
            font-size: 19px;
            color: {secondary};
            line-height: 1.6;
        }}

        .card {{
            background-color: {card};
            padding: 25px;
            border-radius: 18px;
            margin-bottom: 20px;
        }}

        .result {{
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin: 20px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


appliquer_style()


# =========================================================
# MODELE
# =========================================================

@st.cache_resource
def charger_modele():

    if not MODEL_PATH.exists():
        return None, f"Le fichier {MODEL_PATH.name} est introuvable."

    try:
        modele = joblib.load(MODEL_PATH)
        return modele, None

    except Exception as erreur:
        return None, str(erreur)


model, model_error = charger_modele()


# =========================================================
# VARIABLES DU MODELE
# =========================================================

VARIABLES = [
    {
        "nom": "Age",
        "label": "👤 Âge",
        "description": "Âge en années.",
        "min": 1,
        "max": 120,
        "type": "int",
    },
    {
        "nom": "SystolicBP",
        "label": "🩸 Pression artérielle systolique",
        "description": "Valeur de la pression systolique.",
        "min": 1,
        "max": 300,
        "type": "int",
    },
    {
        "nom": "BS",
        "label": "🍬 Glycémie",
        "description": "Valeur de glycémie attendue par le modèle.",
        "min": 0.01,
        "max": 100.0,
        "type": "float",
    },
    {
        "nom": "BodyTemp",
        "label": "🌡️ Température corporelle",
        "description": "Température utilisée par le modèle.",
        "min": 0.01,
        "max": 120.0,
        "type": "float",
    },
    {
        "nom": "HeartRate",
        "label": "❤️ Fréquence cardiaque",
        "description": "Fréquence cardiaque.",
        "min": 1,
        "max": 300,
        "type": "int",
    },
    {
        "nom": "DiastolicBP",
        "label": "🩸 Pression artérielle diastolique",
        "description": "Valeur de la pression diastolique.",
        "min": 1,
        "max": 250,
        "type": "int",
    },
]


# =========================================================
# UTILITAIRES
# =========================================================

def email_valide(email):

    expression = (
        r"^[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    return re.match(expression, email) is not None


def aller(page):

    st.session_state.page = page
    st.rerun()


def recommencer_prediction():

    st.session_state.prediction_step = 0
    st.session_state.prediction_values = {}
    st.session_state.dernier_resultat = None


def nom_resultat(prediction):

    valeur = str(prediction).strip().lower()

    if valeur == "high risk" or "high" in valeur:
        return "Risque maternel élevé", "🔴"

    if valeur == "low risk" or "low" in valeur:
        return "Risque maternel faible", "🟢"

    return str(prediction), "🔵"


# =========================================================
# PAGE DE CONNEXION
# =========================================================

def page_connexion():

    st.title("🩺 Risque Maternel IA")

    st.subheader(
        "Une interface intelligente pour l'aide "
        "à l'évaluation du risque maternel."
    )

    st.divider()

    st.header("🔐 Accéder à la plateforme")

    st.write(
        "Entrez votre adresse e-mail et votre mot de passe "
        "pour accéder à votre espace."
    )

    email = st.text_input(
        "📧 Adresse e-mail",
        placeholder="exemple@domaine.com",
        key="email_connexion",
    )

    password = st.text_input(
        "🔑 Mot de passe",
        type="password",
        placeholder="Votre mot de passe",
        key="mot_de_passe",
    )

    if st.button(
        "🚀 Se connecter",
        type="primary",
        width="stretch",
    ):

        email = email.strip()

        if not email:

            st.warning("Veuillez saisir votre adresse e-mail.")

        elif not email_valide(email):

            st.error("Veuillez saisir une adresse e-mail valide.")

        elif not password:

            st.warning("Veuillez saisir votre mot de passe.")

        elif len(password) < 6:

            st.warning(
                "Le mot de passe doit contenir au moins 6 caractères."
            )

        else:

            st.session_state.logged_in = True
            st.session_state.email = email
            st.session_state.page = "accueil"

            recommencer_prediction()

            st.rerun()

    st.info(
        "🔒 Cette version utilise une authentification "
        "locale de démonstration."
    )


# =========================================================
# SIDEBAR
# =========================================================

def afficher_sidebar():

    with st.sidebar:

        st.title("🩺 Risque Maternel IA")

        st.caption(
            "Intelligence artificielle pour "
            "l'aide à l'évaluation du risque maternel."
        )

        st.divider()

        st.write("👤 **Session active**")
        st.caption(st.session_state.email)

        st.divider()

        st.subheader("🧭 Navigation")

        if st.button(
            "🏠 Accueil",
            width="stretch",
        ):
            aller("accueil")

        if st.button(
            "🔮 Évaluation",
            width="stretch",
        ):
            aller("prediction")

        if st.button(
            "📊 Analyse du modèle",
            width="stretch",
        ):
            aller("analyse")

        if st.button(
            "📖 À propos",
            width="stretch",
        ):
            aller("apropos")

        if st.button(
            "📚 Documentation",
            width="stretch",
        ):
            aller("documentation")

        st.divider()

        st.subheader("🎨 Apparence")

        choix = st.radio(
            "Mode",
            ["☀️ Clair", "🌙 Nuit"],
            index=(
                0
                if st.session_state.theme == "light"
                else 1
            ),
        )

        nouveau_theme = (
            "dark"
            if choix == "🌙 Nuit"
            else "light"
        )

        if nouveau_theme != st.session_state.theme:

            st.session_state.theme = nouveau_theme
            st.rerun()

        st.divider()

        if st.button(
            "🚪 Déconnexion",
            width="stretch",
        ):

            st.session_state.logged_in = False
            st.session_state.email = ""
            recommencer_prediction()

            st.rerun()


# =========================================================
# ACCUEIL
# =========================================================

def page_accueil():

    st.title("🩺 Risque Maternel IA")

    st.subheader(
        "Une nouvelle façon de visualiser "
        "le risque maternel."
    )

    st.write(
        "Risque Maternel IA utilise un modèle "
        "d'apprentissage automatique pour produire "
        "une estimation algorithmique à partir "
        "de plusieurs paramètres."
    )

    if HERO_IMAGE.exists():

        st.image(
            Image.open(HERO_IMAGE),
            width="stretch",
        )

    st.divider()

    st.header("👋 Bienvenue")

    st.write(
        "Choisissez une action pour commencer."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("🔮 Évaluer un risque")

        st.write(
            "Saisissez les paramètres progressivement "
            "et obtenez une estimation."
        )

        if st.button(
            "Commencer une évaluation →",
            width="stretch",
        ):
            aller("prediction")

    with col2:

        st.subheader("📊 Comprendre le modèle")

        st.write(
            "Consultez les informations disponibles "
            "sur le modèle."
        )

        if st.button(
            "Voir l'analyse →",
            width="stretch",
        ):
            aller("analyse")

    with col3:

        st.subheader("📚 Documentation")

        st.write(
            "Découvrez le fonctionnement de "
            "la plateforme."
        )

        if st.button(
            "Lire la documentation →",
            width="stretch",
        ):
            aller("documentation")

    if HOME_IMAGE.exists():

        st.divider()

        st.header("🩺 Notre vision")

        st.image(
            Image.open(HOME_IMAGE),
            width="stretch",
        )

    st.warning(
        "⚠️ Le résultat fourni par cette application "
        "est une estimation algorithmique. "
        "Il ne constitue pas un diagnostic médical "
        "et ne remplace pas l'avis d'un professionnel "
        "de santé."
    )


# =========================================================
# EVALUATION
# =========================================================

def page_prediction():

    st.title("🔮 Évaluation du risque")

    st.write(
        "Saisissez progressivement les paramètres "
        "nécessaires au modèle."
    )

    if model is None:

        st.error(
            f"Impossible de charger le modèle : {model_error}"
        )
        return

    if st.session_state.dernier_resultat is not None:

        afficher_resultat()
        return

    step = st.session_state.prediction_step

    if step >= len(VARIABLES):

        executer_prediction()
        return

    variable = VARIABLES[step]

    st.divider()

    st.subheader(
        f"Étape {step + 1} / {len(VARIABLES)}"
    )

    st.header(variable["label"])

    st.write(variable["description"])

    nom = variable["nom"]

    ancienne_valeur = (
        st.session_state.prediction_values.get(nom)
    )

    if variable["type"] == "int":

        valeur = st.number_input(
            variable["label"],
            min_value=variable["min"],
            max_value=variable["max"],
            value=(
                int(ancienne_valeur)
                if ancienne_valeur is not None
                else int(variable["min"])
            ),
            step=1,
            key=f"input_{nom}",
        )

    else:

        valeur = st.number_input(
            variable["label"],
            min_value=float(variable["min"]),
            max_value=float(variable["max"]),
            value=(
                float(ancienne_valeur)
                if ancienne_valeur is not None
                else float(variable["min"])
            ),
            step=0.01,
            key=f"input_{nom}",
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if step > 0:

            if st.button(
                "← Précédent",
                width="stretch",
            ):

                st.session_state.prediction_values[nom] = valeur
                st.session_state.prediction_step -= 1

                st.rerun()

    with col2:

        if step == len(VARIABLES) - 1:

            texte_bouton = "🔎 Obtenir la prédiction"

        else:

            texte_bouton = "Continuer →"

        if st.button(
            texte_bouton,
            type="primary",
            width="stretch",
        ):

            st.session_state.prediction_values[nom] = valeur
            st.session_state.prediction_step += 1

            st.rerun()

    st.write("")

    if st.button(
        "🔄 Recommencer",
        width="stretch",
    ):

        recommencer_prediction()
        st.rerun()


# =========================================================
# EXECUTION DU MODELE
# =========================================================

def executer_prediction():

    valeurs = st.session_state.prediction_values

    try:

        donnees = {
            variable["nom"]: [valeurs[variable["nom"]]]
            for variable in VARIABLES
        }

        X = pd.DataFrame(donnees)

        prediction = model.predict(X)[0]

        resultat = {
            "prediction": prediction,
            "features": X,
            "classes": [],
            "probs": [],
        }

        if hasattr(model, "predict_proba"):

            resultat["probs"] = model.predict_proba(X)[0]
            resultat["classes"] = list(model.classes_)

        st.session_state.dernier_resultat = resultat

        st.rerun()

    except Exception as erreur:

        st.error(
            "Une erreur est survenue pendant la prédiction."
        )

        st.exception(erreur)


# =========================================================
# RESULTAT
# =========================================================

def afficher_resultat():

    resultat = st.session_state.dernier_resultat

    prediction = resultat["prediction"]

    label, icone = nom_resultat(prediction)

    st.divider()

    if "élevé" in label.lower():

        st.error(
            f"{icone} {label}"
        )

    elif "faible" in label.lower():

        st.success(
            f"{icone} {label}"
        )

    else:

        st.info(
            f"{icone} {label}"
        )

    classes = resultat.get("classes", [])
    probabilites = resultat.get("probs", [])

    if len(classes) > 0:

        st.subheader("📊 Probabilités")

        probabilites_df = pd.DataFrame(
            {
                "Classe": [
                    str(classe)
                    for classe in classes
                ],
                "Probabilité": [
                    round(float(probabilite) * 100, 2)
                    for probabilite in probabilites
                ],
            }
        )

        st.dataframe(
            probabilites_df,
            width="stretch",
            hide_index=True,
        )

    st.subheader("📋 Paramètres utilisés")

    valeurs = st.session_state.prediction_values

    donnees = []

    for variable in VARIABLES:

        donnees.append(
            {
                "Variable": variable["label"],
                "Valeur": valeurs.get(
                    variable["nom"],
                    "—",
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(donnees),
        width="stretch",
        hide_index=True,
    )

    st.warning(
        "⚠️ Cette prédiction est produite par un modèle "
        "informatique. Elle ne constitue pas un diagnostic "
        "médical."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 Nouvelle évaluation",
            type="primary",
            width="stretch",
        ):

            recommencer_prediction()
            st.rerun()

    with col2:

        if st.button(
            "🏠 Retour à l'accueil",
            width="stretch",
        ):

            recommencer_prediction()
            aller("accueil")


# =========================================================
# ANALYSE
# =========================================================

def page_analyse():

    st.title("📊 Analyse du modèle")

    st.write(
        "Informations disponibles sur le modèle "
        "chargé par l'application."
    )

    if model is None:

        st.error(
            f"Modèle indisponible : {model_error}"
        )
        return

    st.info(
        "🤖 Modèle chargé : "
        "random_forest_risque_maternel.pkl"
    )

    if hasattr(model, "feature_importances_"):

        importances = model.feature_importances_

        noms = [
            variable["nom"]
            for variable in VARIABLES
        ]

        if len(importances) == len(noms):

            df = pd.DataFrame(
                {
                    "Variable": noms,
                    "Importance": importances,
                }
            ).sort_values(
                "Importance",
                ascending=False,
            )

            st.subheader(
                "📈 Importance des variables"
            )

            st.bar_chart(
                df.set_index("Variable")
            )

            st.dataframe(
                df,
                width="stretch",
                hide_index=True,
            )

    else:

        st.info(
            "Ce modèle ne fournit pas directement "
            "l'importance des variables."
        )


# =========================================================
# A PROPOS
# =========================================================
def page_apropos():

    st.title("📖 À propos")

    st.subheader(
        "Présentation du projet Risque Maternel IA"
    )

    st.write(
        """
        Risque Maternel IA est une solution numérique
        d'aide à la décision médicale utilisant
        l'intelligence artificielle pour estimer
        le niveau de risque maternel à partir de
        plusieurs paramètres médicaux.
        """
    )

    st.divider()

    st.header("📄 Document du projet")

    if PDF_PATH.exists():

        # =========================
        # AFFICHAGE DU PDF
        # =========================

        st.subheader("👁️ Consulter le document")

        pdf_bytes = PDF_PATH.read_bytes()

        import base64

        pdf_base64 = base64.b64encode(
            pdf_bytes
        ).decode("utf-8")

        pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{pdf_base64}"
            width="100%"
            height="800"
            style="
                border:none;
                border-radius:15px;
            ">
        </iframe>
        """

        st.markdown(
            pdf_display,
            unsafe_allow_html=True
        )

        # =========================
        # TELECHARGEMENT
        # =========================

        st.download_button(
            label="📥 Télécharger le document PDF",
            data=pdf_bytes,
            file_name="document_projet.pdf",
            mime="application/pdf",
            width="stretch",
        )

    else:

        st.error(
            "❌ Le document PDF est introuvable."
        )

        st.info(
            "Vérifie que document_projet.pdf se trouve "
            "dans le dossier assets."
        )
# =========================================================
# DOCUMENTATION
# =========================================================

def page_documentation():

    st.title("📚 Documentation")

    st.write(
        "Guide rapide d'utilisation de "
        "Risque Maternel IA."
    )

    st.subheader("1️⃣ Connexion")

    st.write(
        "Entrez votre adresse e-mail et votre "
        "mot de passe pour accéder à l'application."
    )

    st.subheader("2️⃣ Évaluation")

    st.write(
        "Ouvrez le module Évaluation et saisissez "
        "progressivement les paramètres demandés."
    )

    st.subheader("3️⃣ Résultat")

    st.write(
        "Le modèle produit une classe de risque et, "
        "lorsque cette information est disponible, "
        "les probabilités associées."
    )

    st.subheader("4️⃣ Analyse")

    st.write(
        "La page Analyse permet de consulter les "
        "informations disponibles sur le modèle."
    )

    st.subheader("5️⃣ À propos")

    st.write(
        "La page À propos présente le projet et "
        "permet d'accéder au document PDF."
    )

    st.warning(
        "⚠️ Les résultats produits par l'intelligence "
        "artificielle doivent être interprétés avec "
        "prudence et ne remplacent pas une évaluation "
        "médicale professionnelle."
    )


# =========================================================
# APPLICATION
# =========================================================

if not st.session_state.logged_in:

    page_connexion()

else:

    afficher_sidebar()

    if st.session_state.page == "accueil":

        page_accueil()

    elif st.session_state.page == "prediction":

        page_prediction()

    elif st.session_state.page == "analyse":

        page_analyse()

    elif st.session_state.page == "apropos":

        page_apropos()

    elif st.session_state.page == "documentation":

        page_documentation()

    else:

        st.session_state.page = "accueil"
        st.rerun()


# =========================================================
# PIED DE PAGE
# =========================================================

st.divider()

st.caption(
    "🩺 Risque Maternel IA · "
    "Démonstration académique · 2026"
)
