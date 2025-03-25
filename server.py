from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def detect_emotion():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Check if 'text' key is in request
        if "text" not in data:
            return jsonify({"error": "Missing 'text' parameter"}), 400

        text = data["text"]
        
        # Call the emotion detection function
        emotion_result = emotion_detector(text)

        if emotion_result["dominant_emotion"] is None:
            return jsonify({"error": "Invalid text! Please try again!"}), 400
        # Format the response as required
        formatted_response = (
            f"For the given statement, the system response is 'anger': {emotion_result['anger']}, "
            f"'disgust': {emotion_result['disgust']}, 'fear': {emotion_result['fear']}, "
            f"'joy': {emotion_result['joy']} and 'sadness': {emotion_result['sadness']}. "
            f"The dominant emotion is {emotion_result['dominant_emotion']}."
        )

        return jsonify({"response": formatted_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
