import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID")

@app.route('/', methods=['GET'])
def verify_webhook():
    verify_token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if verify_token == "VOXVIBE_SECRET_TOKEN":
        return challenge
    return "Invalid Token", 403

@app.route('/', methods=['POST'])
def handle_instagram_comment():
    data = request.json
    try:
        comment_info = data['entry']['changes']['value']
        comment_text = comment_info['text'].upper()
        user_id = comment_info['from']['id']
        username = comment_info['from']['username']
        
        if "LINK" in comment_text:
            audio_url = generate_ai_voice(username)
            if audio_url:
                send_instagram_dm(user_id, audio_url)
                
    except Exception as e:
        print("Error processing comment:", str(e))
        
    return jsonify({"status": "success"}), 200

def generate_ai_voice(username):
    url = f"https://elevenlabs.io{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": f"Hey {username}! Aapne jo link maanga tha, wo ye raha. Niche click kijiye.",
        "model_id": "eleven_monolingual_v1"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return "https://yourfreehosting.com" 
    return None

def send_instagram_dm(user_id, audio_url):
    url = f"https://facebook.com{META_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "attachment": {
                "type": "audio", 
                "payload": {"url": audio_url}
            }
        }
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(port=5000)
