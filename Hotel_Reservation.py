import streamlit as st
import pandas as pd
import datetime
import openpyxl
from PIL import Image


st.set_page_config(
    page_title="INES Hotel",
    page_icon=":hotel:",
    layout="wide"
)

# Define the CSS animation code for the title
title_animation = '''
<style>
.title {
  animation-name: title-animation,text-color-animation;
  
  animation-duration: 2s;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
  text-align: center;
  font-size: 80px;
}

@keyframes title-animation {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
  @keyframes text-color-animation {
  0% {
    color: #393646;
  }
  50% {
    color: #4F4557;
  }
  100% {
    color: #6D5D6E;
  }
}
  
}
</style>
'''

# Inject the CSS code into the streamlit app
st.markdown(title_animation, unsafe_allow_html=True)

# Add an animated title to the streamlit app
st.markdown('<h1 class="title">INES Hotel</h1>', unsafe_allow_html=True)









# Load your images
image1 = Image.open("city-sleeper-twin-room.jpg")
image2 = Image.open("SB-Architects_Conrad-Playa-Mita_Terrace.jpg")
image3 = Image.open("Absmall02resize.1506079172.3059.jpg")

# Use the columns function to put the images side by side
col1, col2,col3 = st.columns(3)
with col1:
    st.image(image1)
with col2:
    st.image(image2)
with col3:
    st.image(image3)    

# image = Image.open("C:/Users/moham/OneDrive/Bureau/Hotel_Reservation/40b3566310d686be665d9775f59ca9cd.jpg")
# st.image(image, use_column_width=True)
# image = Image.open("C:/Users/moham/OneDrive/Bureau/Hotel_Reservation/184305239.jpg")
# st.image(image, use_column_width=True)


# Add a stylesheet for your Streamlit app
def add_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Call the add_css function with the name of your CSS file
add_css("style.css")

# Chargement des données
chambres = pd.read_excel("chambres.xlsx")
reservations = pd.read_excel("reservations.xlsx")
avis = pd.read_excel("avis.xlsx")

# Fonction pour vérifier la disponibilité d'une chambre
def verifier_disponibilite(date_arrivee, date_depart, chambre):
    reservations_chambre = reservations[reservations["chambre"] == chambre]
    reservations_chambre["date_arrivee"] = pd.to_datetime(reservations_chambre["date_arrivee"])
    reservations_chambre["date_depart"] = pd.to_datetime(reservations_chambre["date_depart"])
    disponibilite = True
    for index, row in reservations_chambre.iterrows():
        if date_arrivee < row["date_depart"] and date_depart > row["date_arrivee"]:
            disponibilite = False
            break
    return disponibilite

# Fonction pour calculer le prix total d'une réservation
def calculer_prix_total(date_arrivee, date_depart, chambre):
    duree = (datetime.datetime.strptime(date_depart, "%Y-%m-%d") - datetime.datetime.strptime(date_arrivee, "%Y-%m-%d")).days
    prix_nuit = chambres[chambres["chambre"] == chambre]["prix_nuit"].iloc[0]
    prix_total = duree * prix_nuit
    return prix_total

# Page d'accueil
st.title("Réservation d'hôtel en ligne")

# Affichage des chambres disponibles
st.header("Chambres disponibles")
disponibles = chambres["chambre"].tolist()
chambre_selectionnee = st.selectbox("Sélectionnez une chambre :", disponibles)
date_arrivee = st.date_input("Date d'arrivée :")
date_depart = st.date_input("Date de départ :")
if date_arrivee >= date_depart:
    st.error("La date de départ doit être supérieure à la date d'arrivée.")
else:
    if verifier_disponibilite(date_arrivee, date_depart, chambre_selectionnee):
        prix_total = calculer_prix_total(str(date_arrivee), str(date_depart), chambre_selectionnee)
        st.success(f"La chambre {chambre_selectionnee} est disponible du {date_arrivee} au {date_depart}. Le prix total de la réservation est de {prix_total} €.")
        if st.button("Réserver"):
            reservations = reservations.append({"chambre": chambre_selectionnee, "date_arrivee": str(date_arrivee), "date_depart": str(date_depart)}, ignore_index=True)
            reservations.to_excel("reservations.xlsx", index=False)
            st.success("La réservation a été effectuée avec succès !")
    else:
        st.warning(f"La chambre {chambre_selectionnee} n'est pas disponible du {date_arrivee} au {date_depart}.")


st.header("Ajouter un avis")
avis_texte = st.text_input("Entrez votre avis :")
if st.button("Envoyer l'avis"):
    avis = avis.append({"chambre": chambre_selectionnee, "date": datetime.datetime.now(), "avis": avis_texte}, ignore_index=True)
    avis.to_excel("avis.xlsx", index=False)
    st.success("Votre avis a été ajouté avec succès !")
    avis_chambre = avis[avis["chambre"] == chambre_selectionnee]
    
st.header("Avis des clients")
avis_chambre = avis[avis["chambre"] == chambre_selectionnee]
avis_chambre = avis_chambre.dropna()
if not avis_chambre.empty:
    st.table(avis_chambre[["date", "avis"]])
    
else:
    st.warning("Aucun avis pour cette chambre.")


