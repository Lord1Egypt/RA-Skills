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
import subprocess
import sys
import time
import zipfile
from datetime import datetime

from sber_api import API, SberAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def request_statement_print(account: str, date_str: str, api: SberAPI | None = None) -> str:
    """Запрашивает формирование печатной формы выписки за дату (YYYY-MM-DD). Возвращает taskId."""
    if api is None:
        api = SberAPI()
    api.refresh()

    url = f"{API}/v1/statement/print?accountNumber={account}&statementDate={date_str}&format=PDF"

    def _run(cert: str, key: str, cacert: str):
        cmd = [
            "curl", "-sS", "--max-time", "30",
            "--cert", cert, "--key", key, "--cacert", cacert,
            url,
            "Authorization: Bearer " + api.access_token,
        ]
        return subprocess.run(cmd, capture_output=True, text=True)

    res = api._execute_with_tls(_run)
    if res.returncode != 0:
        raise RuntimeError(f"curl failed: {res.stderr}")

    out = res.stdout.strip().strip('"')
    if not out.isdigit():
        raise RuntimeError(f"Unexpected response from Sber print request: {res.stdout}")
    return out


def poll_download_task(task_id: str, timeout_sec: int = 60, api: SberAPI | None = None) -> dict:
    """Опрашивает статус задачи формирования файлов."""
    if api is None:
        api = SberAPI()
    api.refresh()

    url = f"{API}/v1/statement/tasks-for-download/{task_id}"

    start = time.time()
    while time.time() - start < timeout_sec:
        def _run(cert: str, key: str, cacert: str):
            cmd = [
                "curl", "-sS", "--max-time", "15",
                "--cert", cert, "--key", key, "--cacert", cacert,
                url,
                "Authorization: Bearer " + api.access_token,
            ]
            return subprocess.run(cmd, capture_output=True, text=True)

        res = api._execute_with_tls(_run)
        if res.returncode == 0:
            try:
                data = json.loads(res.stdout)
                state = data.get("state")
                if state == "EXECUTED":
                    return data
                elif state in ("FAILED", "ERROR"):
                    raise RuntimeError(f"Task failed: {res.stdout}")
            except json.JSONDecodeError:
                pass
        time.sleep(2)

    raise TimeoutError(f"Task {task_id} timed out after {timeout_sec}s")


def download_zip(download_url: str, api: SberAPI | None = None) -> bytes:
    """Скачивает zip-архив с apifiles.sberbank.ru."""
    if api is None:
        api = SberAPI()
    api.refresh()

    def _run(cert: str, key: str, cacert: str):
        cmd = [
            "curl", "-sS", "--max-time", "60",
            "--cert", cert, "--key", key, "--cacert", cacert,
            download_url,
            "Authorization: Bearer " + api.access_token,
        ]
        return subprocess.run(cmd, capture_output=True)

    res = api._execute_with_tls(_run)
    if res.returncode != 0 or not res.stdout.startswith(b"PK\x03\x04"):
        raise RuntimeError(f"Failed to download zip from {download_url}: {res.stderr[:200]}")
    return res.stdout


def fetch_executed_orders(
    date_str: str,
    account: str,
    out_dir: str = "/home/synthet1x/.openclaw/workspace/media/out",
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
    parser.add_argument("--out-dir", default="/home/synthet1x/.openclaw/workspace/media/out", help="Папка сохранения")

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
