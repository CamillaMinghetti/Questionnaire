import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Legge le credenziali dalle secrets di Streamlit
credentials_dict = st.secrets["google_sheets"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, 
    ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])

# Autenticazione con Google Sheets
client = gspread.authorize(creds)

# Apri il tuo Google Sheet usando l'ID fornito
spreadsheet = client.open_by_key("1keTMaYMtN0D-YIClxJFxYAKOMeb1ddKPIHH6Q92LxYw")
worksheet = spreadsheet.sheet1  # Se vuoi un altro foglio, usa spreadsheet.worksheet("NomeFoglio")

# Funzione per salvare i dati su Google Sheets
def save_to_google_sheets(name, clinician, experience_level, procedures_performed, responses):
    new_data = [
        name,
        clinician,
        experience_level,
        procedures_performed,
    ]
    new_data.extend(responses)  # Aggiunge tutte le risposte al questionario

    worksheet.append_row(new_data)  # Scrive una nuova riga su Google Sheets
    st.success("Risposte salvate su Google Sheets!")

# Nome dell'utente
name = st.text_input("Inserisci il tuo nome")

# Prima domanda
clinician = st.radio("Sei un medico?", ["Sì", "No"])
experience_level = None
procedures_performed = None

if clinician == "Sì":
    experience_level = st.radio("Qual è il tuo livello di esperienza?", ["Specializzando", "Resident", "Esperto"])
    procedures_performed = st.radio("Quante endoscopie hai eseguito?", ["<50", "50-100", ">100"])

# Simulazione delle risposte al questionario
responses = []
for i in range(5):  # Simuliamo 5 domande
    response = st.radio(f"Domanda {i+1}: Quale video è più accurato?", ["Sinistra", "Destra"])
    responses.append(response)

# Quando si preme il pulsante "Invia risposte"
if st.button("Invia risposte"):
    save_to_google_sheets(name, clinician, experience_level, procedures_performed, responses)
