import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "not_set")

if GROQ_API_KEY == "not_set":
    print("Fehler: GROQ_API_KEY ist nicht gesetzt. Bitte setze den API-Schlüssel in der .env Datei.")
    exit(1)

def triage_email(text):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "Du analysierst Kundenanfragen. Antworte ausschließlich als JSON, kein Text davor oder danach."
                },
                {
                    "role": "user",
                    "content": f"""Analysiere diese Anfrage und gib JSON zurück mit:
- kategorie: Support / Sales / Spam / Dringend
- prioritaet: Hoch / Mittel / Niedrig
- zusammenfassung: 1 Satz
- vorgeschlagene_antwort: 2-3 Sätze

Anfrage: {text}"""
                }
            ],
            "temperature": 0.3
        }
    )
    
    raw = response.json()
    content = raw["choices"][0]["message"]["content"]
    clean = content.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


print("=" * 60)
print("  KI Email Triage – powered by Groq LLaMA 3.3")
print("=" * 60)
print("Tippe eine Kundenanfrage ein (oder 'exit' zum Beenden)\n")

while True:
    anfrage = input("📧 Anfrage: ").strip()
    
    if anfrage.lower() == "exit":
        print("Beendet.")
        break
        
    if not anfrage:
        continue
    
    print("⏳ Analysiere...\n")
    result = triage_email(anfrage)
    
    print(f"📂 Kategorie:   {result['kategorie']}")
    print(f"⚡ Priorität:   {result['prioritaet']}")
    print(f"📝 Zusammenfassung: {result['zusammenfassung']}")
    print(f"✉️  Antwort:    {result['vorgeschlagene_antwort']}")
    print("-" * 60 + "\n")