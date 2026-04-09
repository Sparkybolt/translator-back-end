from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import tempfile
import os

app = Flask(__name__)


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(force=True)
    text = data.get("text", "")
    target = data.get("target", "en")

    if not text.strip():
        return jsonify({"success": False, "error": "No text provided."})

    try:
        translator = GoogleTranslator(source="auto", target=target)
        translated = translator.translate(text)
        return jsonify({"success": True, "translated": translated})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json(force=True)
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text.strip():
        return jsonify({"success": False, "error": "No text provided."})

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang=lang)
            tts.save(fp.name)
            temp_path = fp.name

        with open(temp_path, "rb") as f:
            audio_data = f.read()

        os.remove(temp_path)

        encoded = base64.b64encode(audio_data).decode("utf-8")
        return jsonify({"success": True, "audio": encoded})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/")
def home():
    return "Translator API is running."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
