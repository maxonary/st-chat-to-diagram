import os

from dotenv import load_dotenv

import streamlit as st
import pandas as pd
import plotly.express as px
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Interaktive AI-Diagramm-Erstellung")

uploaded_file = st.file_uploader("Lade eine CSV-Datei hoch", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

    st.write("Hochgeladene Tabelle:")
    st.dataframe(df)

    user_input = st.text_input("Beschreibe das gewünschte Diagramm:")
    if user_input:
        with st.spinner("Analysiere Anfrage..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du bist ein Assistent, der Kontext aus Tabellen analysiert und Plotly-Diagramme vorschlägt."},
                    {"role": "user", "content": f"Hier ist die Tabelle: {df.head().to_dict()}"},
                    {"role": "user", "content": f"Erstelle ein Diagramm basierend auf: {user_input}"}
                ],
                temperature=0.7,
                max_tokens=200
            )
        
        chart_description = response["choices"][0]["message"]["content"]
        st.write("Diagramm-Beschreibung von der KI:")
        st.write(chart_description)

        try:
            exec(chart_description)
        except Exception as e:
            st.error(f"Fehler beim Erstellen des Diagramms: {e}")

# KI-Antwort (Beispiel)
fig = px.bar(df, x='Spalte1', y='Spalte2', title='Beispiel-Diagramm')
st.plotly_chart(fig)