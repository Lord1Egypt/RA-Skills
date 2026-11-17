# Сервер Flask: форма с SmartCaptcha + проверка токена через /validate. Подробности: ../../docs/server-validation.md
import json
import os
import sys

import requests
from flask import Flask, render_template, request

SMARTCAPTCHA_SERVER_KEY = os.environ.get("SMARTCAPTCHA_SERVER_KEY")
SMARTCAPTCHA_CLIENT_KEY = os.environ.get("SMARTCAPTCHA_CLIENT_KEY")

if not SMARTCAPTCHA_SERVER_KEY or not SMARTCAPTCHA_CLIENT_KEY:
    sys.exit("Задайте переменные окружения SMARTCAPTCHA_SERVER_KEY и SMARTCAPTCHA_CLIENT_KEY.")

app = Flask(__name__)


def check_captcha(token: str, ip: str) -> bool:
    """Проверяет токен: POST https://smartcaptcha.yandexcloud.net/validate,
    параметры secret, token, ip в формате x-www-form-urlencoded.

    Семантика из документации:
    - HTTP-код != 200, таймаут или сетевая ошибка -> fail-open (пропускаем пользователя),
      чтобы сбой сервиса капчи не блокировал ваших пользователей и не задерживал ответ;
    - иначе пользователь прошел проверку, только если поле status == "ok".
      Поле message — только для диагностики, не сравнивайте его в коде.
    """
    try:
        resp = requests.post(
            "https://smartcaptcha.yandexcloud.net/validate",
            data={
                "secret": SMARTCAPTCHA_SERVER_KEY,
                "token": token,
                # Параметр необязателен, но передавайте его:
                # это улучшает качество работы SmartCaptcha.
                "ip": ip,
            },
            # Таймаут, чтобы при недоступности сервиса
            # не задерживать обработку запроса пользователя.
            timeout=1,
        )
    except requests.RequestException as err:
        print(f"Allow access due to an error: {err}", file=sys.stderr)
        return True  # fail-open: таймаут или сетевая ошибка

    server_output = resp.content.decode()
    if resp.status_code != 200:
        print(
            f"Allow access due to an error: code={resp.status_code}; message={server_output}",
            file=sys.stderr,
        )
        return True  # fail-open
    return json.loads(server_output)["status"] == "ok"


@app.get("/")
def index():
    # Ключ клиента (sitekey) подставляется в шаблон страницы.
    return render_template("index.html", sitekey=SMARTCAPTCHA_CLIENT_KEY)


@app.post("/submit")
def submit():
    # Виджет добавляет токен в форму как скрытое поле <input name="smart-token">.
    token = request.form.get("smart-token")

    # Токена нет — пользователь не прошел капчу. В /validate не ходим: без токена ответ будет
    # "status": "failed" с сообщением "Invalid or expired Token".
    if not token:
        return "Отклонено: пройдите проверку капчи.", 400

    # request.remote_addr: если приложение стоит за обратным прокси, восстановите реальный
    # IP пользователя (например, через werkzeug ProxyFix), иначе сюда попадет IP прокси.
    if check_captcha(token, request.remote_addr):
        message = request.form.get("message", "") or "(пусто)"
        return f"Принято: проверка пройдена. Сообщение: {message}"
    return "Отклонено: проверка капчи не пройдена.", 403


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
