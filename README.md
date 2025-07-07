# 🚀 Automatisk Konvertering av Supportloggar till Incidentrapporter med AI

## 📝 Beskrivning

Detta projekt syftar till att automatiskt konvertera ostrukturerade supportloggar till **incidentrapporter** med:

✅ **Sammanfattning av problemet**  
✅ **Kategorisering:** `nätverk`, `programvara`, `hårdvara`  
✅ **Prioritering:** `Låg`, `Medel`, `Hög`, `Kritisk`  

Allt sker med hjälp av en AI-modell som du först tränar i Python och sedan visualiserar i en interaktiv **Streamlit-dashboard**.

---

## 🗂️ Projektstruktur

| Fil/Folder          | Beskrivning                                                  |
|---------------------|--------------------------------------------------------------|
| `.gitignore`        | Filer och mappar som ignoreras av Git                        |
| `.env`              | Miljövariabler, t.ex. fine-tuned modellnyckel som sparas här |
| `main.py`           | Tränar modellen och returnerar fine-tuned modellnyckel      |
| `models.py`         | Modellhantering och prediktionslogik                          |
| `incidentdata.jsonl`| Datafil med genererade incidentrapporter i JSON Lines-format |
| `dashboard.py`      | Streamlit-dashboard för visualisering och interaktion         |
| `README.md`         | Projektbeskrivning och instruktioner                          |


---

## ⚙️ Steg 1 – Träna modellen och få fine-tuned modellnyckel (`main.py`)

- Kör `main.py` för att:
  - Träna/finjustera GPT-modellen på dina supportloggar.
  - Generera en *fine-tuned modellnyckel*.
  - Spara nyckeln i .env filen tillsammans med din API-KEY.

> **Viktigt:** Denna nyckel behöver du manuellt eller med script klistra in i `.env`-filen under variabeln `FINE_TUNED_MODEL_KEY` så här:


## 📊 Steg 2: Starta Dashboard och visualisera (dashboard.py)

Med API-nyckeln på plats i .env kan du starta dashboarden:
```bash
streamlit run dashboard.py
```
---

## 🎨 Exempel på output från dashboarden (`dashboard.py`)

När du startar dashboarden får du en användarvänlig och interaktiv webbapp med två huvudsektioner:

### 1. 📝 Skapa Incidentrapport
- En stor textyta där du kan klistra in eller skriva en supportlogg.
- En knapp för att generera en AI-baserad incidentrapport baserat på den inskrivna texten.
- När rapporten genererats visas den i en tabell med fälten:
  - **Sammanfattning**
  - **Kategori**
  - **Prioritet**
- En knapp för att ladda ner den skapade rapporten som CSV-fil för enkel hantering och arkivering.
- Om AI-svaret inte kan tolkas eller valideras visas ett tydligt felmeddelande.

### 2. 📊 Ladda upp och analysera rapporter
- En filuppladdare där du kan ladda upp en CSV-fil med tidigare genererade incidentrapporter.
- Den uppladdade datan visas i en interaktiv tabell som anpassar sig efter skärmstorleken.
- Under tabellen finns två stapeldiagram som visualiserar:
  - Fördelning av incidenter per **Kategori** (t.ex. nätverk, programvara, hårdvara).
  - Fördelning av incidenter per **Prioritet** (Låg, Medel, Hög, Kritisk).
- Diagrammen ger snabb visuell överblick över var problemområden och kritikalitet finns.

---

### Layoutöversikt:

| Sektion                      | Funktion / Visning                                      |
|-----------------------------|--------------------------------------------------------|
| **Titel**                   | 🚨 AI-baserad Incidentrapport & Dashboard              |
| **Skapa rapport**           | Textarea för logg, knapp för generering, tabell och nedladdning |
| **Ladda upp och analysera** | Filuppladdare, visning av tabell, stapeldiagram för Kategori och Prioritet |

Den här designen gör det enkelt både att skapa nya rapporter och att analysera stora mängder supportloggar visuellt i en smidig webbaserad app.

---



