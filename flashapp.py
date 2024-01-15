from flask import Flask, render_template, request, jsonify
from google.cloud import translate_v2 as translate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
db = SQLAlchemy(app)

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(255), nullable=False)
    translated_text = db.Column(db.String(255), nullable=False)
    target_language = db.Column(db.String(10), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    translations = Translation.query.all()
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

    # 保存翻译结果到数据库
    translation = Translation(original_text=text, translated_text=translated_text, target_language=target_language)
    db.session.add(translation)
    db.session.commit()

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)