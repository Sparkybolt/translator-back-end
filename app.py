from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import tempfile

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text", "")
    target = data.get("target", "en")

    try:
        translator = GoogleTranslator(source="auto", target=target)
        translated = translator.translate(text)

        return jsonify({
            "success": True,
            "translated": translated
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")

    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_data = fp.read()

        encoded = base64.b64encode(audio_data).decode("utf-8")

        return jsonify({
            "success": True,
            "audio": encoded
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/")
def home():
    return "Translator API is running."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
