# Серверная проверка токена Yandex SmartCaptcha (Python + requests). Подробности: ../docs/server-validation.md
"""Переиспользуемый модуль проверки токена SmartCaptcha.

Использование:
    from validate import check_captcha
    if check_captcha(token, ip=request.remote_addr):
        ...  # человек
    else:
        ...  # робот

Ключ сервера берется из переменной окружения SMARTCAPTCHA_SERVER_KEY
(фолбэк — плейсхолдер <ключ_сервера>, замените его при отсутствии переменной).

Семантика (по официальной документации):
- POST https://smartcaptcha.yandexcloud.net/validate, формат x-www-form-urlencoded;
- таймаут 1 секунда, чтобы не задерживать обработку запроса пользователя;
- fail-open: при HTTP-коде != 200 и при сетевой ошибке пользователь пропускается
  (рекомендация сервиса — обрабатывать ошибки HTTP-протокола как "status": "ok");
- решение принимается только по полю status ("ok" / "failed");
  поле message — только для диагностики, не сравнивайте его в коде.

Важно: токен одноразовый и живет 5 минут. Повторная валидация того же токена
вернет "status": "failed" с сообщением "Invalid or expired Token".
"""

import json
import os
import sys
from typing import Optional

import requests

VALIDATE_URL = "https://smartcaptcha.yandexcloud.net/validate"
SMARTCAPTCHA_SERVER_KEY = os.environ.get("SMARTCAPTCHA_SERVER_KEY", "")


def check_captcha(
    token: str,
    ip: Optional[str] = None,
    secret: str = SMARTCAPTCHA_SERVER_KEY,
    timeout: float = 1.0,
) -> bool:
    """Проверяет токен SmartCaptcha. Возвращает True — пропустить пользователя.

    :param token: одноразовый токен из формы (поле smart-token).
    :param ip: IP-адрес пользователя. Необязателен, но передавайте его —
        это улучшает качество работы SmartCaptcha. Способ получения зависит
        от фреймворка и прокси (например, во Flask — request.remote_addr).
    :param secret: ключ сервера (по умолчанию — из SMARTCAPTCHA_SERVER_KEY).
    :param timeout: таймаут запроса в секундах.
    :return: True, если проверка пройдена (status == "ok") или сервис недоступен
        (fail-open); False, если это робот (status == "failed").
    :raises RuntimeError: если ключ сервера не задан — ошибка конфигурации должна
        падать громко: пустой/неверный secret даёт status == "failed" всем
        пользователям (тихий отказ всем живым людям).
    """
    if not secret:
        raise RuntimeError("SMARTCAPTCHA_SERVER_KEY не задан: укажите ключ сервера (ysc2_...)")

    data = {
        "secret": secret,
        "token": token,
    }
    if ip:
        data["ip"] = ip

    try:
        resp = requests.post(VALIDATE_URL, data=data, timeout=timeout)
    except requests.RequestException as err:
        # Сетевая ошибка или таймаут — пропускаем пользователя (fail-open),
        # чтобы сбой сервиса не блокировал реальных людей.
        print(f"Allow access due to an error: {err}", file=sys.stderr)
        return True

    server_output = resp.content.decode()
    if resp.status_code != 200:
        print(
            f"Allow access due to an error: code={resp.status_code}; message={server_output}",
            file=sys.stderr,
        )
        return True

    try:
        return json.loads(server_output)["status"] == "ok"
    except (ValueError, KeyError) as err:
        print(f"Error parsing response: {err}", file=sys.stderr)
        return True


if __name__ == "__main__":
    # Мини-пример: python validate.py <токен> [<IP-адрес_пользователя>]
    _token = sys.argv[1] if len(sys.argv) > 1 else "<токен>"
    _ip = sys.argv[2] if len(sys.argv) > 2 else None
    print("Passed" if check_captcha(_token, ip=_ip) else "Robot")
