import requests
import json  # Import JSON library

URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def emotion_detector(text_to_analyze):
    payload = {"raw_document": {"text": text_to_analyze}}
    
    try:
        response = requests.post(URL, json=payload, headers=HEADERS)
        if response.status_code != 200:
            return {"error": f"API Error {response.status_code}: {response.text}"}

        # Convert response text to a dictionary
        response_data = json.loads(response.text)

        # Extract the first emotion prediction
        predictions = response_data.get("emotionPredictions", [])
        if not predictions:
            return {"error": "No emotion predictions found"}

        emotions = predictions[0].get("emotion", {})

        # Extract required emotions
        required_emotions = {key: emotions.get(key, 0) for key in ['anger', 'disgust', 'fear', 'joy', 'sadness']}

        # Determine dominant emotion
        dominant_emotion = max(required_emotions, key=required_emotions.get, default="unknown")
        required_emotions['dominant_emotion'] = dominant_emotion

        return required_emotions

    except Exception as e:
        return {"error": str(e)}
