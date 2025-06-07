import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
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

app = FastAPI()

def fetch_exchange(from_currency: str, to_currency: str) -> float:
    pass

class QueryRequest(BaseModel):
    user_query: str

class QueryResponse(BaseModel):
    response: str
    
@app.post("/ask", response_model=QueryResponse)
async def ask_llm(request: QueryRequest):
    user_message = request.user_query
    print(user_message);
    
    # try:
    #     response = chat.send_message("Convert 100 dollars to euros")
    #     pass
    # except Exception as e:
    #     pass
    # pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)