#!/usr/bin/env python3
"""
Sber Business API — скачивание печатных форм выписок и исполненных платёжных поручений (PDF со штампом банка).
Использует Zero-Knowledge Banking Vault (mTLS в RAM-диске).

Методы:
1. Запрос генерации: GET /v1/statement/print?accountNumber=...&statementDate=...&format=PDF
2. Опрос готовности: GET /v1/statement/tasks-for-download/{taskId}
3. Скачивание zip с apifiles.sberbank.ru:9443
4. Извлечение PDF платёжек со штампом банка "ИСПОЛНЕНО"
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
import urllib.parse
import zipfile
from datetime import datetime

from sber_api import API, SberAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT_DIR = os.path.join(os.getcwd(), "sber_downloads")

# The download URL arrives from the bank's task response. Pin scheme/host/port
# so a tampered response cannot redirect the mTLS client certificate or the
# Bearer token to an arbitrary destination (or inject curl options).
ALLOWED_DOWNLOAD_HOSTS = {"apifiles.sberbank.ru", "fintech.sberbank.ru"}


def validate_download_url(url: str) -> str:
    """Reject any download URL outside the pinned Sber file hosts (HTTPS only)."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https":
        raise ValueError(f"Download URL must use https: {url!r}")
    if parts.hostname not in ALLOWED_DOWNLOAD_HOSTS:
        raise ValueError(f"Download host not allowed: {parts.hostname!r}")
    if parts.port not in (None, 443, 9443):
        raise ValueError(f"Download port not allowed: {parts.port!r}")
    if parts.username or parts.password:
        raise ValueError("Download URL must not embed credentials")
    return url


def request_statement_print(account: str, date_str: str, api: SberAPI | None = None) -> str:
    """Запрашивает формирование печатной формы выписки за дату (YYYY-MM-DD). Возвращает taskId."""
    if not account.isdigit():
        raise ValueError("account must be a numeric account number")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("date_str must be YYYY-MM-DD") from None
    if api is None:
        api = SberAPI()
    api.refresh()

    url = f"{API}/v1/statement/print?accountNumber={account}&statementDate={date_str}&format=PDF"
    # SECURITY: the Bearer token travels via the stdin curl config (see
    # SberAPI._curl), never in argv; the header flag bug (token treated as a
    # second URL) is fixed by using the shared client.
    code, body = api._curl(url, headers={"Authorization": f"Bearer {api.access_token}"}, timeout=30)
    if code != 200:
        raise RuntimeError(f"Sber print request failed: HTTP {code}: {body[:200]!r}")

    out = body.decode("utf-8", "replace").strip().strip('"')
    if not out.isdigit():
        raise RuntimeError(f"Unexpected response from Sber print request: {out[:200]}")
    return out


def poll_download_task(task_id: str, timeout_sec: int = 60, api: SberAPI | None = None) -> dict:
    """Опрашивает статус задачи формирования файлов."""
    if api is None:
        api = SberAPI()
    api.refresh()

    url = f"{API}/v1/statement/tasks-for-download/{task_id}"

    start = time.time()
    while time.time() - start < timeout_sec:
        code, body = api._curl(url, headers={"Authorization": f"Bearer {api.access_token}"}, timeout=15)
        if code == 200:
            try:
                data = json.loads(body)
                state = data.get("state")
                if state == "EXECUTED":
                    return data
                elif state in ("FAILED", "ERROR"):
                    raise RuntimeError(f"Task failed: {body[:300]!r}")
            except json.JSONDecodeError:
                pass
        time.sleep(2)

    raise TimeoutError(f"Task {task_id} timed out after {timeout_sec}s")


def download_zip(download_url: str, api: SberAPI | None = None) -> bytes:
    """Скачивает zip-архив с apifiles.sberbank.ru (строго pinned HTTPS-хост)."""
    validate_download_url(download_url)
    if api is None:
        api = SberAPI()
    api.refresh()

    code, body = api._curl(download_url,
                           headers={"Authorization": f"Bearer {api.access_token}"},
                           timeout=60)
    if code != 200 or not body.startswith(b"PK\x03\x04"):
        raise RuntimeError(f"Failed to download zip from {download_url}: HTTP {code}")
    return body


def fetch_executed_orders(
    date_str: str,
    account: str,
    out_dir: str = DEFAULT_OUT_DIR,
    number: str | None = None,
    profile: str = "default",
) -> list[str]:
    """Скачивает платёжные поручения с отметкой банка за дату.
    
    Если указан number — возвращает только платёжку с этим номером.
    """
    api = SberAPI(profile=profile)
    task_id = request_statement_print(account, date_str, api=api)
    task_info = poll_download_task(task_id, api=api)
    url = task_info.get("url")
    if not url:
        raise RuntimeError(f"No download URL in task info: {task_info}")

    zip_bytes = download_zip(url, api=api)
    z = zipfile.ZipFile(io.BytesIO(zip_bytes))
    
    os.makedirs(out_dir, exist_ok=True)
    saved_files = []

    for item in z.infolist():
        base_name = os.path.basename(item.filename)
        if not base_name.endswith(".pdf"):
            continue

        if number:
            if f"пп {number} " not in base_name and f"пп № {number} " not in base_name and f"пп №{number} " not in base_name:
                continue

        dest_path = os.path.join(out_dir, base_name)
        with open(dest_path, "wb") as f:
            f.write(z.read(item.filename))
        saved_files.append(dest_path)

    return saved_files


def main():
    parser = argparse.ArgumentParser(description="Выгрузка исполненных платёжек из СберБизнес (Banking Vault)")
    parser.add_argument("--profile", default="default", help="Имя профиля")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Дата выписки (YYYY-MM-DD), по умолчанию сегодня")
    parser.add_argument("--account", default=None, help="Расчётный счёт (если не указан, берется из профиля)")
    parser.add_argument("--number", default=None, help="Номер конкретного платёжного поручения (например, 61)")
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR, help="Папка сохранения (по умолчанию ./sber_downloads)")

    args = parser.parse_args()
    api = SberAPI(profile=args.profile)
    acc = args.account or api.account_number
    if not acc:
        accs = api.accounts()
        if accs:
            acc = accs[0]["number"]
        else:
            print("❌ Ошибка: не указан номер счёта (--account) и в банке не найдено открытых счетов", file=sys.stderr)
            sys.exit(1)

    try:
        files = fetch_executed_orders(date_str=args.date, account=acc, out_dir=args.out_dir, number=args.number, profile=args.profile)
        print(f"[{args.profile}] Успешно выгружено файлов: {len(files)}")
        for f in files:
            print(f" - {f}")
    except Exception as exc:
        print(f"[{args.profile}] Ошибка выгрузки: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
