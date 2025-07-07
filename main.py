import os
import time
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from models import IncidentReport
from pydantic import ValidationError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

# 1. Ladda upp träningsfilen
file = client.files.create(file=open("övning5/incidentdata.jsonl", "rb"), purpose="fine-tune")
print(f"Uploaded file ID: {file.id}")

# 2. Skapa fine-tuning-jobb
fine_tune_job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-3.5-turbo"
)

print(f"Created fine-tuning job with id {fine_tune_job.id}.")

# 3. Vänta tills jobbet är klart
status = fine_tune_job.status
while status not in ["succeeded", "failed"]:
    print(f"Job status: {status}. Väntar 30 sekunder...")
    time.sleep(30)
    fine_tune_job = client.fine_tuning.jobs.retrieve(fine_tune_job.id)
    status = fine_tune_job.status

if status == "succeeded":
    fine_tuned_model = fine_tune_job.fine_tuned_model
    print(f"Fine-tuned model ready: {fine_tuned_model}")

    # 4. Testa modellen med några exempel-loggar
    test_logs = [
        "Logg: 'Får bluescreen varje gång datorn startar om.'\nIncidentrapport:",
        "Logg: 'Outlook kraschar när jag försöker skicka mail.'\nIncidentrapport:",
        "Logg: 'VPN tappar uppkoppling efter 30 sekunder.'\nIncidentrapport:"
    ]

    def generate_incident(log_prompt, model_primary, model_fallback="gpt-4o"):
        for model in [model_primary, model_fallback]:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": log_prompt}]
                )
                content = response.choices[0].message.content.strip()

                # Försök att parsa JSON
                parsed_json = json.loads(content)

                # Validera med Pydantic
                incident = IncidentReport(**parsed_json)
                print(f"✅ Lyckad parsning med modell {model}.")
                return incident.model_dump()  # Returnera som dict för DataFrame

            except (json.JSONDecodeError, ValidationError) as e:
                print(f"⚠️  Felaktigt svar från modell {model}:\n{content}\nFel: {e}")
                continue  # Prova nästa modell

        print("❌ Inget giltigt svar erhölls ens med fallback.")
        return None

    results = []

    # Använd funktionen här:
    for log in test_logs:
        incident_dict = generate_incident(log, fine_tuned_model)
        if incident_dict:
            results.append(incident_dict)

    # 5. Skapa DataFrame om vi har resultat
    if results:
        df = pd.DataFrame(results)
        print("\n✅ Incidentrapporter:")
        print(df)
    else:
        print("❌ Inga giltiga incidentrapporter genererades.")

else:
    print("❌ Fine-tuning job failed.")
