import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from chatbot.api import (
    get_joke,
    get_quote,
    get_advice,
    get_cat_fact,
    get_weather,
    get_news,
)

# ------------------ NLTK Setup ------------------
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
lemmatizer = WordNetLemmatizer()

# ------------------ Load Model & Data ------------------
model = load_model("chatbot/chatbot_model.h5")
intents = json.loads(open("D:\Chatbot_using_python\chatbot\Intent.json", encoding="utf-8").read())
words = pickle.load(open("chatbot/words.pkl", "rb"))
classes = pickle.load(open("chatbot/classes.pkl", "rb"))


# ------------------ Preprocessing ------------------
def clean_up_sentence(sentence):
    """Tokenize and lemmatize the input sentence"""
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=False):
    """Convert sentence into bag-of-words vector"""
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)


# ------------------ Prediction Logic ------------------
def predict_class(sentence):
    """Predict intent based on model output"""
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def get_response(ints, intents_json):
    """Get chatbot response from predicted intent"""
    
    # Check if a prediction was made (i.e., 'ints' is not empty)
    if not ints:
        return "I'm not sure I understand that 🤔"
    
    # Extract the predicted intent name (which is stored under the key "intent")
    # This is the tag you want to find in your JSON.
    tag = ints[0]["intent"]
    
    # Loop through all intents in the JSON file
    matching_intent = next(
        (it for it in intents_json["intents"] if it.get("intent") == tag), None
    )
    if matching_intent:
        # Return a randomly selected response from the matching intent
        return random.choice(matching_intent.get("responses", []))

    # Fallback response if the predicted tag is not found in the JSON file
    return "I'm not sure how to respond to that."

# ------------------ City Name Extraction ------------------
def extract_city(text):

    words = nltk.word_tokenize(text)
    city = None
    for i, w in enumerate(words):
        if w.lower() == "in" and i + 1 < len(words):
            city = words[i + 1]
            break
    return city


# ------------------ Chatbot Response Logic ------------------
def chatbot_response(msg):
    """Main chatbot logic — combines AI model + APIs"""
    text = msg.lower()

    # Handle API-based responses first
    if "joke" in text:
        return get_joke()

    elif "quote" in text:
        return get_quote()

    elif "advice" in text:
        return get_advice()

    elif "cat" in text or "cats" in text:
        return get_cat_fact()

    elif "weather" in text:
        city = extract_city(text)
        return get_weather(city) if city else get_weather("dhaka")

    elif "news" in text or "headline" in text:
        return get_news()

    # Otherwise use model-based intent prediction
    ints = predict_class(msg)
    return get_response(ints, intents)
