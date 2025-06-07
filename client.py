import requests
import json

FASTAPI_URL = "http://127.0.0.1:8000/ask"

def main():
    print("Welcome to the LLM Currency Converter!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        try:
            response = requests.post(FASTAPI_URL, json={"user_query": user_input})
            response.raise_for_status()
            
            data = response.json()
            print(f"LLM: {data['response']}")
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the FastAPI backend. Is it running?")
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with backend: {e}")
        except json.JSONDecodeError:
            print("Error: Could not decode JSON response from backend.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()