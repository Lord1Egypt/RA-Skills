#!/usr/bin/env python3
# CLI-утилита ручной проверки токена Yandex SmartCaptcha через /validate. Подробности: ../docs/server-validation.md
"""Смоук-тест серверной проверки токена SmartCaptcha. Только stdlib (argparse + urllib).

Использование:
    python check_token.py --secret <ключ_сервера> --token <токен> [--ip <ip>]

Если --secret не указан, ключ берется из переменной окружения SMARTCAPTCHA_SERVER_KEY.

Печатает HTTP-код и JSON ответа сервиса. Коды завершения:
    0 — status == "ok"  (проверка пройдена);
    1 — status == "failed"  (робот или ошибка в запросе — смотрите поле message);
    2 — сетевая ошибка или неразборчивый ответ; при HTTP-коде != 200
        ответ все равно разбирается по полю status.

Помните: токен одноразовый и живет 5 минут. После успешной проверки повторный
запуск с тем же токеном вернет "status": "failed" с "Invalid or expired Token" —
это нормальное поведение, а не ошибка интеграции.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

VALIDATE_URL = "https://smartcaptcha.yandexcloud.net/validate"

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_ERROR = 2


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ручная проверка токена SmartCaptcha через POST /validate."
    )
    parser.add_argument(
        "--secret",
        default=os.environ.get("SMARTCAPTCHA_SERVER_KEY"),
        help="Ключ сервера (по умолчанию — из переменной окружения SMARTCAPTCHA_SERVER_KEY).",
    )
    parser.add_argument("--token", required=True, help="Одноразовый токен из формы (поле smart-token).")
    parser.add_argument("--ip", help="IP-адрес пользователя (необязателен, но рекомендуется).")
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Таймаут запроса в секундах (по умолчанию 5; в боевом коде используйте 1).",
    )
    args = parser.parse_args()

    if not args.secret:
        print(
            "Ошибка: укажите --secret или переменную окружения SMARTCAPTCHA_SERVER_KEY.",
            file=sys.stderr,
        )
        return EXIT_ERROR

    params = {"secret": args.secret, "token": args.token}
    if args.ip:
        params["ip"] = args.ip

    request = urllib.request.Request(
        VALIDATE_URL,
        data=urllib.parse.urlencode(params).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            http_code = response.status
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        # Сервис ответил, но код не 2xx. Пробуем разобрать тело ниже —
        # вдруг это JSON со status.
        # В боевом коде такие ошибки рекомендуется обрабатывать как fail-open.
        http_code = err.code
        body = err.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, OSError) as err:
        print(f"Сетевая ошибка: {err}", file=sys.stderr)
        return EXIT_ERROR

    print(f"HTTP {http_code}")
    try:
        parsed = json.loads(body)
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    except ValueError:
        print(body)
        print("Ошибка: ответ сервиса не является корректным JSON.", file=sys.stderr)
        return EXIT_ERROR

    status = parsed.get("status") if isinstance(parsed, dict) else None
    if status == "ok":
        return EXIT_OK
    if status == "failed":
        # Пустое message — это робот; непустое (например, "Invalid or expired Token.")
        # — ошибка в запросе, исправляйте ее на этапе разработки.
        return EXIT_FAILED

    print(f"Ошибка: неожиданное значение поля status: {status!r}.", file=sys.stderr)
    return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
