import streamlit as st
import pandas as pd
import json
from openai import OpenAI
from models import IncidentReport
from pydantic import ValidationError
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Incidentrapport AI", layout="wide")
st.title("🚨 AI-baserad Incidentrapport & Dashboard")

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
fine_tuned_model = os.getenv("FINE_TUNED_MODEL")

# Sektion 1: Skapa rapport
st.header("📝 Skapa Incidentrapport")

log_input = st.text_area("Ange supportlogg här:")

if st.button("Generera rapport") and log_input:
    prompt = f"Logg: '{log_input}'\nIncidentrapport:"

    response = client.chat.completions.create(
        model=fine_tuned_model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
        incident = IncidentReport(**parsed)
        st.success("✅ Incidentrapport skapad och validerad!")

        # Visa som tabell
        df = pd.DataFrame([incident.model_dump()])
        st.table(df)

        # Nedladdningsknapp
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Ladda ner som CSV", csv, file_name="incidentrapport.csv", mime="text/csv")

    except (json.JSONDecodeError, ValidationError) as e:
        st.error(f"❌ Kunde inte tolka eller validera:\n\n{content}\n\nFel: {e}")

# Sektion 2: Dashboard
st.header("📊 Ladda upp och analysera rapporter")

uploaded_file = st.file_uploader("Ladda upp CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(df["Kategori"].value_counts())

    with col2:
        st.bar_chart(df["Prioritet"].value_counts())
