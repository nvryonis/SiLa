from gettext import translation
from flask import Flask, render_template, request, jsonify
from google.cloud import translate_v2 as translate

app = Flask(__name__)



@app.route('/')
def index():
    translations = translation.query.all()
    return render_template('index.html', translations=translations)

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text')
    target_language = 'el'  # 希腊语的 ISO 639-1 代码

    # 使用 Google Translate API 进行翻译
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    translated_text = result['input']

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
