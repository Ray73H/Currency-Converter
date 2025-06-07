import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from google.genai import types
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

tools = [
    {
        "function_declarations": [
            {
                "name": "extract_currency_conversion_info",
                "description": "Extracts structured currency conversion info in ISO 4217 format (e.g. USD, EUR).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_currency": {
                            "type": "string",
                            "description": "Three-letter ISO currency code (e.g. USD, EUR, GBP)"
                        },
                        "output_currency": {
                            "type": "string",
                            "description": "Three-letter ISO currency code (e.g. USD, EUR, GBP)"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount to convert (e.g. 100)"
                        },
                    },
                    "required": ["input_currency", "output_currency", "amount"]
                }
            }
        ]
    }
]

model = genai.GenerativeModel('gemini-2.0-flash', tools=tools)

chat = model.start_chat()

response = chat.send_message(
    "Convert 100 dollars to euros"
)

print(response)