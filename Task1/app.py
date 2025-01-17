from flask import Flask, request, jsonify, render_template
import re
import requests
from datetime import datetime

app = Flask(__name__)

# Weather API configuration
API_KEY = "5348f7382c9e4213aad180635251701"
BASE_URL = "http://api.weatherapi.com/v1/current.json?key={API key}&q={city name}"

def get_weather(city):
    # Ensure the city name is properly formatted (capitalization, trimming extra spaces)
    city = city.strip().title()
    
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check if city is valid
        if "error" in data:
            return f"Sorry, I couldn't fetch weather information for {city}. Please check the city name and try again."
        
        location = data["location"]["name"]
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        
        return f"The weather in {location} is {condition} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't fetch the weather details. Please try again."


def chatbot_response(user_input):
    # Weather
    if re.search(r"weather in (\w+)", user_input, re.IGNORECASE):
        city = re.search(r"weather in (\w+)", user_input, re.IGNORECASE).group(1)
        return get_weather(city)
    # Greeting
    elif re.search(r"\bhello\b|\bhi\b", user_input, re.IGNORECASE):
        return "Hi there! What can I help you with?"
    # How are you
    elif re.search(r"how are you", user_input, re.IGNORECASE):
        return "I'm just a bot, but I'm here to help!"
    # Weather (mock response)
    elif re.search(r"\bweather\b", user_input, re.IGNORECASE):
        return "I can't fetch the weather now, but you can check a weather app or website!"
    # Current time
    elif re.search(r"\btime\b", user_input, re.IGNORECASE):
        now = datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."
    # Current date
    elif re.search(r"\bdate\b", user_input, re.IGNORECASE):
        today = datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {today}."
    # Simple math calculations
    elif re.search(r"calculate\b|\bwhat is\b", user_input, re.IGNORECASE):
        try:
            # Extract the math expression from the user input
            expression = re.search(r"calculate (.+)|what is (.+)", user_input, re.IGNORECASE)
            if expression:
                math_expression = expression.group(1) or expression.group(2)
                result = eval(math_expression)  # Evaluate the expression
                return f"The result is {result}."
        except:
            return "I couldn't calculate that. Please provide a valid math expression!"
    # Gratitude
    elif re.search(r"\bthank you\b|\bthanks\b", user_input, re.IGNORECASE):
        return "You're welcome! Feel free to ask me anything else."
    # Goodbye
    elif re.search(r"\bbye\b|\bexit\b", user_input, re.IGNORECASE):
        return "Take care! Goodbye!"
    # Default response
    else:
        return "Hmm, I didn't get that. Could you clarify?"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
