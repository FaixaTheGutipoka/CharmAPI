# app/generator.py
import os
import json
import random
import openai

# Load seed flirts
SEED_FILE = os.path.join(os.path.dirname(__file__), "seed_flirts.json")
with open(SEED_FILE, "r", encoding="utf-8") as f:
    SEED_DATA = json.load(f)

def get_seed_flirt(context: str, tone: str) -> str:
    """Pick a random seed flirt line"""
    return random.choice(SEED_DATA[context][tone])

def ai_generate_flirt(context: str, tone: str) -> str:
    """Call OpenAI to generate a new flirt line"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not set. Set OPENAI_API_KEY environment variable.")

    openai.api_key = api_key

    prompt = f"Generate a short, clever, {tone} flirt line for the context '{context}'. Keep it under 20 words."

    print(f"[AI] Generating flirt line for context={context}, tone={tone}")  # debug

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=30,
        temperature=0.9
    )

    return response.choices[0].message.content.strip()
