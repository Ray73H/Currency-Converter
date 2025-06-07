# Currency-Converter

## Steps to run

Start virtual environment and install dependencies

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Add these to .env file

    GEMINI_API_KEY=<Key>

Open a terminal and run to start fastAPI backend

    uvicorn main:app --reload

Open a new terminal and run

    python client.py