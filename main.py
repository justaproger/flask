from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)  # Включаем CORS для всего приложения


# Загружаем вопросы из JSON-файла
def load_questions():
    json_file_path = 'questions.json'
    if not os.path.exists(json_file_path):
        return []
    with open(json_file_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions


questions = load_questions()


@app.route('/<question>', methods=['GET'])
def find_answer(question):
    try:
        question_text = unquote(question)  # Декодируем URL-encoded строку

        if not question_text:
            return jsonify({"error": "Question is required"}), 400

        match = next((q for q in questions if q['question'] == question_text), None)

        if match:
            return jsonify({"answer": match['correct_answer']}), 200
        else:
            return jsonify({"error": "Question not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
