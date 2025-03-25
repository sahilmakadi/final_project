import json
import requests

URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def emotion_detector(text_to_analyze):
    if not text_to_analyze.strip():  # Check if input is empty or contains only spaces
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, json=payload, headers=HEADERS)

    if response.status_code == 400:  # Handle bad request
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    if response.status_code == 200:
        response_data = json.loads(response.text)
        emotions = response_data["emotionPredictions"][0].get("emotion", {})

        dominant_emotion = max(emotions, key=emotions.get, default=None)
        emotions["dominant_emotion"] = dominant_emotion

        return emotions

    return {"error": f"Error: {response.status_code}, {response.text}"}  # Handle other errors
