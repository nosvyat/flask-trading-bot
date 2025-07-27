from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    app.logger.info(f"Получен сигнал: {data}")
    return jsonify({'status': 'ok'})
