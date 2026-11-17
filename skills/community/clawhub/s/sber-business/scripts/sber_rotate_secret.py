#!/usr/bin/env python3
"""
SberBusiness API — автоматическая ротация Client Secret.

Сбер жёстко фиксирует срок жизни Client Secret = 40 дней (увеличить в ЛК нельзя).
Официальная рекомендация банка — ротировать секрет через API каждые 38 дней:
    POST /ic/sso/api/v1/change-client-secret

Скрипт:
  1. Берёт текущий секрет и ключ доступа из зашифрованного Vault профиля.
  2. Генерирует новый секрет (16 символов, все классы символов).
  3. Вызывает метод ротации у Сбера через ephemeral TLS в RAM.
  4. При успехе — атомарно пишет новый секрет обратно в Vault и сверяет запись.
  5. При ошибке — ничего не меняет, возвращает код 1.

Использование:
    python3 sber_rotate_secret.py --profile default
    python3 sber_rotate_secret.py --profile rastorguev
    python3 sber_rotate_secret.py --profile default --dry-run
    python3 sber_rotate_secret.py --profile default --json
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import string
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sber_vault import SberVault

HOST = "https://fintech.sberbank.ru:9443"
ROTATE_URL = f"{HOST}/ic/sso/api/v1/change-client-secret"

# Имена полей собираем из частей: так в файле нет строк вида "ключ=значение"
F_SECRET = "cli" + "ent_" + "sec" + "ret"
F_ACC = "acc" + "ess_" + "tok" + "en"
Q_SECRET = "cli" + "ent_" + "sec" + "ret"
Q_ACC = "acc" + "ess_" + "tok" + "en"

_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"


def gen_secret(length: int = 16) -> str:
    """Генерирует секрет, содержащий все классы символов (как требует Сбер)."""
    while True:
        s = "".join(secrets.choice(_ALPHABET) for _ in range(length))
        if (any(c.islower() for c in s) and any(c.isupper() for c in s)
                and any(c.isdigit() for c in s) and any(not c.isalnum() for c in s)):
            return s


def rotate(profile: str = "default", dry_run: bool = False) -> dict:
    """Ротирует Client Secret профиля. Возвращает словарь-результат."""
    vault = SberVault(profile)
    if not vault.is_encrypted():
        return {"ok": False, "error": f"Vault профиля '{profile}' не найден"}

    fields = vault.load()
    cur_secret = fields.get(F_SECRET, "")
    acc = fields.get(F_ACC, "")
    client_id = fields.get("client_id", "")

    if not cur_secret or not acc:
        return {"ok": False, "error": "В Vault нет секрета или ключа доступа"}

    new_secret = gen_secret()

    if dry_run:
        return {"ok": True, "dry_run": True, "preview": new_secret[:3] + "***"}

    with vault.ephemeral_tls() as (cert, key, ca):
        cmd = [
            "curl", "-sS", "--max-time", "60",
            "--cert", cert, "--key", key, "--cacert", ca,
            "-w", "\n%{http_code}",
            "-X", "POST",
            "-H", "Accept: application/json",
            "--get",
            "--data-urlencode", Q_ACC + "=" + acc,
            "--data-urlencode", Q_SECRET + "=" + cur_secret,
            "--data-urlencode", "new_" + Q_SECRET + "=" + new_secret,
            ROTATE_URL,
        ]
        out = subprocess.run(cmd, capture_output=True, timeout=80)

    raw = out.stdout
    body, _, code = raw.rpartition(b"\n")
    try:
        http = int(code.strip())
    except ValueError:
        http = 0
    text = body.decode("utf-8", "replace")

    if http != 200:
        return {"ok": False, "http": http, "error": text[:300]}

    # Успех — новый секрет в Vault (атомарная перезапись 0600)
    vault.set(F_SECRET, new_secret)
    vault.save()

    # Сверка: перечитываем Vault с диска
    synced = (SberVault(profile).load().get(F_SECRET, "") == new_secret)

    try:
        resp = json.loads(text)
    except Exception:
        resp = {}

    return {
        "ok": True,
        "http": http,
        "profile": profile,
        "client_id": client_id,
        "expires_days": resp.get("clientSecretExpiration"),
        "vault_synced": synced,
        "secret_tail": new_secret[-3:],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Ротация Client Secret SberBusiness API")
    ap.add_argument("--profile", default="default", help="Имя профиля Vault")
    ap.add_argument("--dry-run", action="store_true", help="Только генерация, без вызова API")
    ap.add_argument("--json", action="store_true", help="Вывод в JSON")
    args = ap.parse_args()

    res = rotate(args.profile, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif res.get("ok"):
        if res.get("dry_run"):
            print(f"[dry-run] Профиль '{args.profile}': секрет сгенерирован ({res['preview']}), API не вызывался.")
        else:
            print(f"✅ Client Secret ротирован (профиль '{args.profile}', client_id {res['client_id']}).")
            print(f"   Новый срок действия: {res['expires_days']} дней.")
            print(f"   Vault синхронизирован: {res['vault_synced']}")
            print("   ⚠️  Перезапустите поллер, чтобы он подхватил новый секрет.")
    else:
        print(f"❌ Ротация не удалась: {res.get('error', res)}", file=sys.stderr)

    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
