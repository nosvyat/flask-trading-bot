from flask import Flask, request, jsonify
import logging
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 🔧 Настройки Telegram
TELEGRAM_TOKEN = '8177702369:AAHml_aWJyJkpQieXvoDbmgtx5voXYHfZeg'
TELEGRAM_CHAT_ID = '-4903125944'  # ← Замени на свой chat_id, если нужно

# 🚀 Функция отправки сообщения в Telegram
def send_to_telegram(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        app.logger.error(f'Ошибка при отправке в Telegram: {e}')

# 📩 Приём webhook-сигналов от TradingView
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    app.logger.info(f'Получен сигнал: {data}')

    # 🧠 Формируем сообщение
    message = f"""{'⬆️LONG⬆️' if data.get('side') == 'LONG' else '⬇️SHORT⬇️'}
Цена входа: {data.get('pair')} {data.get('entry')}
Сумма сделки: {data.get('amount')}
Плечо: {data.get('leverage')}

После входа пришлите скрин сделки.
Тейк и Стоплосс пришлю позже.
"""
    # 🔁 Отправляем в Telegram
    send_to_telegram(message)

    return jsonify({'status': 'ok'})

# 📍 Запуск локально (если нужно)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
