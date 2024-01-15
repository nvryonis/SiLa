from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text', '')
    target_language = data.get('target', 'en')

    try:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
