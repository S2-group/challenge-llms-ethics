#!/usr/bin/python

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

NEBULA_BASE_URL = 'https://nebula.cs.vu.nl/api/'
NEBULA_API_KEY = os.getenv('NEBULA_API_KEY')
NEBULA = OpenAI(base_url=NEBULA_BASE_URL, api_key=NEBULA_API_KEY)

def get_nebula_models():
    models = []
    for model in NEBULA.models.list().data:
        models.append(model.id)
    return models

def prompt_nebula(model, system_prompt, user_prompt, configs=None):
    prompt_parameters = {
        "model": model,
        "messages": [
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": user_prompt }
        ],
    }

    if configs:
        prompt_parameters.update(configs)

    response = NEBULA.chat.completions.create(**prompt_parameters)

    return response

if __name__=='__main__':
    available_models = get_nebula_models()
    print(f"Models: {available_models}\n\n")
    
    config = {
        "max_tokens": 25
    }

    response = prompt_nebula("deepseek-r1:1.5b", "You are a helpful assistant.", "What is Empirical Software Engineering?", config)
    print(f"Response: {response.choices[0].message.content}\n\n")
    print(f"Usage stats: {response.usage}")
