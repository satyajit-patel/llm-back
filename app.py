# set up
# > mkdir myproject
# > cd myproject

# // once
# > python -3 -m venv .venv

# > .venv\Scripts\activate
# // run
# flask --app index run
# deactivate // come out from .venv

# // dependencies
# pip install Flask
# pip install python-dotenv
# https://ai.google.dev/api?lang=python
# pip install -q -U google-generativeai
# pip install gunicorn
# pip freeze > requirements.txt


import os
from flask import Flask, request, jsonify
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)

# Initialize CORS
CORS(app)

def scrape_web_content(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract headings and paragraphs
    content = ''
    for heading in soup.find_all(['h1', 'h2', 'h3', 'p']):
        content += heading.get_text() + '\n'
    return content

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    query = data.get('query')
    
    # Step 1: Scrape web content based on user query
    content = scrape_web_content(query)
    
    try:
        # Step 2: Generate a response using LLM
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Generate a detailed response based on the following content: {content}")
        # Send the generated response back
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

