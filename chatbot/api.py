import requests
import random

# ============================================================
# ✅ 1. Joke API (free, no key needed)
# ============================================================
def get_joke():
    try:
        url = "https://v2.jokeapi.dev/joke/Any"
        res = requests.get(url).json()
        if res.get("type") == "single":
            return f"😂 {res['joke']}"
        else:
            return f"🤣 {res['setup']} ... {res['delivery']}"
    except Exception:
        return "Sorry, I couldn't fetch a joke right now."


# ============================================================
# ✅ 2. Quote API (free, no key needed)
# ============================================================
def get_quote():
    try:
        url = "https://api.quotable.io/random"
        res = requests.get(url).json()
        return f"💭 {res['content']} — {res['author']}"
    except Exception:
        return "Sorry, I couldn't get a quote right now."


# ============================================================
# ✅ 3. Advice API (free, no key needed)
# ============================================================
def get_advice():
    try:
        url = "https://api.adviceslip.com/advice"
        res = requests.get(url).json()
        return f"💡 {res['slip']['advice']}"
    except Exception:
        return "Sorry, I couldn't fetch any advice."


# ============================================================
# ✅ 4. Cat Facts API (free, no key needed)
# ============================================================
def get_cat_fact():
    try:
        url = "https://catfact.ninja/fact"
        res = requests.get(url).json()
        return f"🐱 {res['fact']}"
    except Exception:
        return "Couldn't get a cat fact now 😿"


# ============================================================
# ✅ 5. Weather API (Open-Meteo, no key needed)
# ============================================================
def get_weather(city):
    try:
        # Get city coordinates using Open-Meteo Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_res = requests.get(geo_url).json()
        if "results" not in geo_res:
            return f"Couldn't find weather info for {city} 😕"

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        weather_res = requests.get(weather_url).json()
        data = weather_res.get("current_weather", {})

        temp = data.get("temperature")
        wind = data.get("windspeed")
        return f"🌤 Weather in {city.title()}: {temp}°C, Windspeed {wind} km/h."
    except Exception:
        return f"Sorry, I couldn't get weather for {city}."


# ============================================================
# ✅ 6. News API (GNews, Free Key)
# ============================================================
# Free API key from: https://gnews.io (create free account)
# Replace below demo key with your own if expired
GNEWS_API_KEY = "demo"  # <-- Replace with your free API key from gnews.io

def get_news():
    try:
        url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=us&max=5&apikey={GNEWS_API_KEY}"
        res = requests.get(url).json()
        articles = res.get("articles", [])
        if not articles:
            return "No news found right now 📰"
        news_sample = random.choice(articles)
        return f"🗞 {news_sample['title']} — {news_sample['source']['name']}"
    except Exception:
        return "Sorry, couldn't fetch the news right now."
