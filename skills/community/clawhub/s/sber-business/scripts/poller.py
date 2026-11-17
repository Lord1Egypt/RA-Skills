#!/usr/bin/env python3
"""
Поллер операций по счёту через Sber API → мгновенный пуш в Telegram / MAX / Discord / Slack / Webhook.

Ловит и поступления (CREDIT), и списания (DEBIT).
При каждой операции запрашивает актуальный остаток по счёту (closingBalanceRub)
и выводит его в уведомлении быстрее платных банковских СМС.

Запуск: python3 poller.py [--config config.json]
"""

from __future__ import annotations

import argparse
import html
import json
import os
import ssl
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

from sber_api import SberAPI, direction, fmt_amount

BASE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE, "state.json")
LOG_FILE = os.path.join(BASE, "poller.log")
DEFAULT_CONFIG = os.path.join(BASE, "config.json")

MSK = timezone(timedelta(hours=3))
POLL_SECONDS_DEFAULT = 60
OVERLAP_MINUTES = 3
SEEN_KEEP = 800

DEFAULTS = {
    "channel": "telegram",  # telegram | max | discord | slack | webhook
    "pollSeconds": POLL_SECONDS_DEFAULT,
    "minAmount": 0,
    "onlyCredit": False,
    "accounts": [],
    "orgName": "",
    "profile": "default",
    "timezoneOffsetHours": 3,
    "telegram": {
        "enabled": False,
        "token": "",
        "chatId": "",
    },
    "max": {
        "enabled": False,
        "token": "",
        "chatId": "",
    },
    "discord": {
        "enabled": False,
        "webhookUrl": "",
    },
    "slack": {
        "enabled": False,
        "webhookUrl": "",
    },
    "webhook": {
        "enabled": False,
        "url": "",
        "secretHeader": "X-Auth-Token",
        "secretValue": "",
    }
}


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"{ts} {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def load_config(path: str) -> dict:
    cfg = json.loads(json.dumps(DEFAULTS))
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            user = json.load(fh)
        for k, v in user.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k].update(v)
            else:
                cfg[k] = v
    return cfg


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            pass
    return {"last_modify": None, "seen": []}


def save_state(state: dict) -> None:
    state["seen"] = state["seen"][-SEEN_KEEP:]
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False)
    os.replace(tmp, STATE_FILE)


def send_telegram(token: str, chat_id: str, text: str) -> bool:
    import urllib.parse
    import urllib.request
    if not token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return 200 <= resp.status < 300
    except Exception as exc:
        log(f"Telegram send FAIL: {exc}")
        return False


def send_max(token: str, chat_id: str, text: str) -> bool:
    import urllib.parse
    import urllib.request
    if not token or not chat_id:
        return False
    url = f"https://platform-api2.max.ru/messages?chat_id={urllib.parse.quote(str(chat_id))}"
    payload = json.dumps({"text": text, "format": "markdown"}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST", headers={
        "Authorization": token,
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return 200 <= resp.status < 300
    except Exception as exc:
        log(f"MAX send FAIL: {exc}")
        return False


def send_webhook(url: str, data: dict, secret_header: str = "", secret_value: str = "") -> bool:
    import urllib.request
    if not url:
        return False
    if not url.lower().startswith("https://"):
        log(f"SECURITY REJECT: Webhook URL {url} is not HTTPS. Banking transaction data requires TLS.")
        return False
    payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if secret_header and secret_value:
        headers[secret_header] = secret_value
    req = urllib.request.Request(url, data=payload, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return 200 <= resp.status < 300
    except Exception as exc:
        log(f"Webhook send FAIL: {exc}")
        return False


def notify(text: str, tx_data: dict, cfg: dict) -> bool:
    channel = (cfg.get("channel") or "").lower()
    ok = True

    if channel == "telegram" or cfg.get("telegram", {}).get("enabled"):
        t = cfg.get("telegram", {})
        ok = send_telegram(t.get("token"), t.get("chatId"), text) and ok

    if channel == "max" or cfg.get("max", {}).get("enabled"):
        m = cfg.get("max", {})
        ok = send_max(m.get("token"), m.get("chatId"), text) and ok

    if channel in ("discord", "slack") or cfg.get("discord", {}).get("enabled") or cfg.get("slack", {}).get("enabled"):
        hook_url = cfg.get("discord", {}).get("webhookUrl") or cfg.get("slack", {}).get("webhookUrl")
        ok = send_webhook(hook_url, {"content": text, "text": text}) and ok

    if channel == "webhook" or cfg.get("webhook", {}).get("enabled"):
        w = cfg.get("webhook", {})
        ok = send_webhook(w.get("url"), tx_data, w.get("secretHeader"), w.get("secretValue")) and ok

    return ok


def human_dt(iso: str, tz_offset: int = 3) -> str:
    if not iso:
        return ""
    raw = iso.strip().replace("Z", "")
    target_tz = timezone(timedelta(hours=tz_offset))
    for fmt, cut in (("%Y-%m-%dT%H:%M:%S", 19), ("%Y-%m-%dT%H:%M", 16)):
        try:
            dt_msk = datetime.strptime(raw[:cut], fmt).replace(tzinfo=MSK)
            return dt_msk.astimezone(target_tz).strftime("%d.%m.%Y %H:%M")
        except ValueError:
            continue
    return iso


def counterparty(tx: dict, is_credit: bool) -> dict:
    rt = tx.get("rurTransfer") or {}
    k = "payer" if is_credit else "payee"
    return {
        "name": rt.get(f"{k}Name") or tx.get(f"{k}Name") or "",
        "inn": rt.get(f"{k}Inn") or "",
        "account": rt.get(f"{k}Account") or "",
        "bic": rt.get(f"{k}BankBic") or "",
    }


def format_notification(tx: dict, account: str, is_credit: bool, balance: str | None = None,
                        org_name: str = "", tz_offset: int = 3, mask_privacy: bool = False) -> str:
    cp = counterparty(tx, is_credit)
    raw_amt = fmt_amount(tx)
    sign = "+" if is_credit else "-"
    amt = f"{sign}{raw_amt}"
    purpose = " ".join((tx.get("paymentPurpose") or "").split())
    date = tx.get("operationDate") or ""
    who = f" {html.escape(org_name.strip())}" if org_name else ""
    head = f"💰 <b>Поступление на расчётный счёт{who}</b>" if is_credit else f"💸 <b>Списание с расчётного счёта{who}</b>"
    role_label = "Плательщик" if is_credit else "Получатель"

    display_acc = account
    display_inn = cp.get("inn") or ""
    if mask_privacy:
        if len(display_acc) > 8:
            display_acc = display_acc[:5] + "..." + display_acc[-4:]
        if len(display_inn) >= 10:
            display_inn = display_inn[:4] + "****" + display_inn[-2:]

    lines = [
        head,
        f"💵 <b>{amt} ₽</b>",
        "",
        f"Счёт: <code>{html.escape(display_acc)}</code>",
    ]
    if cp["name"]:
        lines.append(f"{role_label}: {html.escape(cp['name'])}")
    if display_inn:
        lines.append(f"ИНН: <code>{html.escape(display_inn)}</code>")
    if date:
        lines.append(f"Время: {human_dt(date, tz_offset)}")
    if purpose:
        lines += ["", f"Назначение: {html.escape(purpose)}"]
    if balance:
        lines += ["", f"📊 <b>Остаток на счёте{who}: {html.escape(balance)}</b>"]
    return "\n".join(lines)


def fetch_balance(api: SberAPI, account: str) -> str | None:
    try:
        today_iso = datetime.now(MSK).strftime("%Y-%m-%d")
        summary_data = api.summary(account, today_iso)
        bal_obj = summary_data.get("closingBalanceRub") or summary_data.get("closingBalance") or {}
        val = bal_obj.get("amount")
        if val is not None:
            return f"{float(val):,.2f}".replace(",", " ").replace(".", ",") + " ₽"
    except Exception as exc:
        log(f"balance fetch error: {exc}")
    return None


def poll_once(api: SberAPI, cfg: dict, state: dict, dry: bool, bootstrap: bool) -> int:
    now_msk = datetime.now(MSK)
    if bootstrap or not state.get("last_modify"):
        since = now_msk
        log("bootstrap: фиксируем точку отсчёта, история не пушится")
    else:
        since = datetime.fromisoformat(state["last_modify"])

    floor = since.replace(hour=0, minute=0, second=0, microsecond=0)
    query_from = max(since - timedelta(minutes=OVERLAP_MINUTES), floor).strftime("%Y-%m-%dT%H:%M:%S")

    accounts = cfg.get("accounts") or [a["number"] for a in api.accounts() if a.get("state") == "OPEN"]
    seen = set(state.get("seen") or [])
    sent = 0

    for acc in accounts:
        txs = []
        try:
            txs = api.increment(query_from, account=acc)
        except Exception as exc:
            log(f"increment error acc={acc}: {exc}")

        txs.sort(key=lambda t: t.get("operationDate") or "")

        for tx in txs:
            uid = tx.get("uuid") or f"{tx.get('operationDate')}|{tx.get('amount')}"
            if uid in seen:
                continue
            seen.add(uid)
            if bootstrap:
                continue

            is_credit = direction(tx) == "CREDIT"
            if cfg.get("onlyCredit") and not is_credit:
                continue

            bal_str = fetch_balance(api, acc)
            tz_off = int(cfg.get("timezoneOffsetHours", 3))
            mask = bool(cfg.get("maskPrivacy", False))
            text = format_notification(tx, acc, is_credit, balance=bal_str, org_name=cfg.get("orgName", ""), tz_offset=tz_off, mask_privacy=mask)

            if not dry:
                notify(text, tx, cfg)
            sent += 1
            log(f"NOTIFY acc={acc} amount={fmt_amount(tx)} dir={direction(tx)}")

    state["seen"] = list(seen)
    state["last_modify"] = now_msk.strftime("%Y-%m-%dT%H:%M:%S")
    save_state(state)
    return sent


def main() -> int:
    ap = argparse.ArgumentParser(description="Поллер операций Sber API")
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="Путь к файлу конфигурации config.json")
    ap.add_argument("--profile", default=None, help="Имя профиля в Vault")
    ap.add_argument("--once", action="store_true", help="Один цикл и выход")
    ap.add_argument("--dry", action="store_true", help="Не отправлять, только логировать")
    ap.add_argument("--bootstrap", action="store_true", help="Зафиксировать точку отсчёта без пушей")
    args = ap.parse_args()

    cfg = load_config(args.config)
    prof = args.profile or cfg.get("profile", "default")
    api = SberAPI(profile=prof)

    state = load_state()
    bootstrap = args.bootstrap or not state.get("last_modify")

    api.refresh()
    log(f"Start Sber poller profile={prof} interval={cfg['pollSeconds']}s")

    if args.once:
        poll_once(api, cfg, state, args.dry, bootstrap)
        return 0

    while True:
        try:
            poll_once(api, cfg, state, args.dry, bootstrap)
            bootstrap = False
        except Exception as exc:
            log(f"Cycle error: {exc}")
        time.sleep(int(cfg["pollSeconds"]))


if __name__ == "__main__":
    sys.exit(main())
