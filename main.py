"""Модули для реализации сервера restapi c помощью Flask и документирования"""
import os
from flask import jsonify, request, abort
import requests
import connexion
import uvicorn

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")

API_KEY = os.environ['API_KEY']

@app.route('/api/rates')
def get_rate():
    """Функция конвертирует передаваемое значение по текущему курсу валюты"""
    try:
        rate_from = request.args.get('rateFrom')
        rate_to = request.args.get('rateTo')
        value = request.args.get('value', 0)
        url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{rate_from}/{rate_to}/{value}'
        res = requests.get(url).json()
        result = {'result': res['conversion_result']}
        return jsonify(result)
    except requests.exceptions.JSONDecodeError:
        abort(500)

if __name__ == '__main__':
    uvicorn.run("main:app", port=3000, log_level="debug")
