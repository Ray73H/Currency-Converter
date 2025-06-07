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
                            "description": "Three-letter ISO currency code (e.g. USD, EUR, GBP)",
                        },
                        "output_currency": {
                            "type": "string",
                            "description": "Three-letter ISO currency code (e.g. USD, EUR, GBP)",
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount to convert (e.g. 100)",
                        },
                    },
                    "required": ["input_currency", "output_currency", "amount"],
                },
            }
        ]
    }
]

model = genai.GenerativeModel("gemini-2.0-flash", tools=tools)
chat = model.start_chat()
model2 = genai.GenerativeModel("gemini-2.0-flash")
chat2 = model2.start_chat()

app = FastAPI()


def fetch_exchange(from_currency: str, to_currency: str, amount: float) -> float:
    response = requests.get(
        f"https://api.frankfurter.dev/v1/latest?base={from_currency}&symbols={to_currency}"
    )

    if response.ok:
        data = response.json()
        rate = data["rates"][to_currency]
        converted = round(amount * rate, 2)
        return converted
    else:
        print(f"Error: {response.status_code} - {response.text}")


class QueryRequest(BaseModel):
    user_query: str


class QueryResponse(BaseModel):
    response: str


@app.post("/ask", response_model=QueryResponse)
async def ask_llm(request: QueryRequest):
    user_message = request.user_query

    try:
        response = chat.send_message(user_message)

        function_call = (
            response.candidates[0].content.parts[0].function_call
            if response.candidates
            and response.candidates[0].content
            and response.candidates[0].content.parts
            else None
        )

        if function_call is None or not hasattr(function_call, "args"):
            raise ValueError("Gemini response does not include a valid function call.")

        args = dict(function_call.args)
        input_curr = args.get("input_currency")
        output_curr = args.get("output_currency")
        amount = args.get("amount")
        if not input_curr or not output_curr or not amount:
            raise ValueError("No arguments returned by Gemini function call.")

        rate = fetch_exchange(input_curr, output_curr, amount)
        print(rate)

        prompt = (
            f"Given this currency conversion:\n"
            f"{amount} {input_curr} = {rate} {output_curr}\n"
            f"Write a natural language sentence summarizing this."
        )
        llm_final_response = chat2.send_message(prompt)
        return QueryResponse(
            response=llm_final_response.candidates[0].content.parts[0].text
        )
    except (IndexError, AttributeError, ValueError) as e:
        raise RuntimeError(f"Failed to extract function call arguments: {e}")
    except Exception as e:
        return QueryResponse(
            response=f"Sorry, something went wrong processing your request: {e}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
