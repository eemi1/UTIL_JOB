import os
from dotenv import load_dotenv
import requests
import json
from services.api_google import scrape_restaurants

load_dotenv()



async def enrich_content(search: str):
    scraped_data = await scrape_restaurants(search)
    
    USER_PROMPT = f""" 
        Estos son datos extraídos de Google Maps:

        {json.dumps(scraped_data, indent=2)}

        Límpialos y conviértelos al formato requerido.
    """


    SYSTEM_PROMPT = """ 
        Eres un sistema de limpieza y estructuración de datos.

        Usa SOLO la información proporcionada en el input.
        No busques ni inventes datos.

        Convierte los datos al siguiente formato JSON:

        {
         "name": "",
         "website": "",
         "phone": "",
         "email": null,
         "instagram": null,
         "has_real_website": true
        }

        Reglas:

        - Si el teléfono no tiene código país agrega +598
        - Si el website es Instagram o Facebook ponlo en el campo correcto
        - Si no hay datos usa null
        - No inventes emails ni redes sociales
        - No escribas nada fuera del JSON
        - Si los sitios web empiezan por instagram o facebook, no son el sitio web, son las redes ordenalos donde van.
    """

    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_KEY')}",
            "Content-Type": "application/json",
        },

        data=json.dumps({
            "model": "openrouter/free",
            "messages": [
                {
                "role": "system",
                "content": SYSTEM_PROMPT
                },
                {
                "role": "user",
                "content": USER_PROMPT
                }
            ],
            "reasoning": {"enabled": True}
        })
    )

    data = response.json()

    if "choices" not in data:
        print("Error:", data)
        return "[]"

    content = data['choices'][0]['message']['content']

    print("--------------------------")
    # print("tokens used:", data[])
    print("--------------------------")
    print("response:", content)
    print("model:", data["model"])
    return content
