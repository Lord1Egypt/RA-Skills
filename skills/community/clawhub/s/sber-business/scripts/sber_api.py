#!/usr/bin/env python3
"""
Sber API client — Мультипрофильный банковский клиент с поддержкой Zero-Knowledge Vault.

Безопасность (Banking Vault):
- Ключи, токены и сертификаты хранятся в зашифрованных AES-256-GCM файлах (.vault).
- Ключ шифрования привязан к machine-id хоста и мастер-ключу.
- Сертификаты mTLS создаются только во временной памяти RAM (/dev/shm) на время запроса
  и затираются нулями сразу после выполнения.
- При обновлении токена новая пара мгновенно шифруется обратно в .vault.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from sber_vault import SberVault
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from sber_vault import SberVault

HOST = "https://fintech.sberbank.ru:9443"
TOKEN_URL = f"{HOST}/ic/sso/api/v2/oauth/token"
API = f"{HOST}/fintech/api"
TIMEOUT = 40
SECRETS_DIR = Path(os.path.expanduser("~/.openclaw/secrets"))


class SberAPI:
    def __init__(self, profile: str = "default") -> None:
        self.profile = profile
        self.vault: SberVault | None = None
        self.client_id = ""
        self.client_secret = ""
        self.access_token = ""
        self.refresh_token = ""
        self.account_number = ""
        self.expires_at: datetime | None = None

        # 1. Сначала пробуем безопасное банковское хранилище (Vault)
        try:
            v = SberVault(profile)
            if v.is_encrypted():
                self.vault = v
                self.client_id = v.get("client_id", "")
                self.client_secret = v.get("client_secret", "")
                self.access_token = v.get("access_token", "")
                self.refresh_token = v.get("refresh_token", "")
                self.account_number = v.get("account_number", "")
                exp_ts = v.get("expires_at_ts")
                self.expires_at = datetime.fromtimestamp(exp_ts, tz=timezone.utc) if exp_ts else None
        except Exception as exc:
            print(f"[WARN] Ошибка загрузки Vault для профиля '{profile}': {exc}", file=sys.stderr)

        if not self.vault or not self.client_id:
            raise RuntimeError(
                f"Банковское хранилище Vault для профиля '{profile}' не найдено или не содержит Client ID. "
                f"Пожалуйста, выполните безопасную настройку: python3 scripts/sber_vault.py setup"
            )

    # --- token lifecycle
    def _need_refresh(self) -> bool:
        if not self.access_token:
            return True
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) >= self.expires_at - timedelta(minutes=5)

    def refresh(self, force: bool = False) -> None:
        if not force and not self._need_refresh():
            return

        code, body = self._post_form(TOKEN_URL, {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        })
        if code != 200:
            raise RuntimeError(f"token refresh failed ({self.profile}): {code} {body[:300]!r}")

        d = json.loads(body)
        self.access_token = d["access_token"]
        new_refresh = d.get("refresh_token") or self.refresh_token
        self.refresh_token = new_refresh
        ttl = int(d.get("expires_in") or 3600)
        self.expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)

        if self.vault:
            self.vault.update_tokens(self.access_token, new_refresh, ttl)

    # --- http (curl с ephemeral RAM TLS)
    def _execute_with_tls(self, fn):
        """Выполняет функцию с временными TLS-сертификатами из RAM-диска."""
        if not self.vault:
            raise RuntimeError("Zero-Knowledge Vault не инициализирован. Запустите: python3 scripts/sber_vault.py setup")
        with self.vault.ephemeral_tls() as (cert, key, cacert):
            return fn(cert, key, cacert)

    def _curl(self, url: str, *, headers=None, timeout=TIMEOUT) -> tuple[int, bytes]:
        def _run(cert, key, cacert):
            cmd = [
                "curl", "-sS", "--max-time", str(timeout),
                "--cert", cert, "--key", key, "--cacert", cacert,
                "-w", "\n%{http_code}",
            ]
            for k, v in (headers or {}).items():
                cmd += ["-H", f"{k}: {v}"]
            cmd.append(url)

            out = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
            raw = out.stdout
            body, _, code = raw.rpartition(b"\n")
            try:
                return int(code.strip()), body
            except ValueError:
                return 0, raw

        return self._execute_with_tls(_run)

    def _post_form(self, url: str, fields: dict, timeout=TIMEOUT) -> tuple[int, bytes]:
        def _run(cert, key, cacert):
            cmd = [
                "curl", "-sS", "--max-time", str(timeout),
                "--cert", cert, "--key", key, "--cacert", cacert,
                "-w", "\n%{http_code}",
                "-X", "POST", url,
                "-H", "Content-Type: application/x-www-form-urlencoded",
                "-H", "Accept: application/json",
            ]
            for k, v in fields.items():
                cmd += ["--data-urlencode", f"{k}={v}"]
            out = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
            raw = out.stdout
            body, _, code = raw.rpartition(b"\n")
            try:
                return int(code.strip()), body
            except ValueError:
                return 0, raw

        return self._execute_with_tls(_run)

    def _get(self, path: str, params: dict | None = None) -> tuple[int, dict | None, str]:
        if not params:
            url = API + path
        else:
            qs = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{API}{path}?{qs}"
        code, body = self._curl(url, headers={"Authorization": f"Bearer {self.access_token}"})
        if code == 401:
            self.refresh(force=True)
            code, body = self._curl(url, headers={"Authorization": f"Bearer {self.access_token}"})
        try:
            return code, json.loads(body), ""
        except Exception:
            return code, None, body.decode("utf-8", "replace")[:300]

    # --- data
    def client_info(self) -> dict:
        self.refresh()
        code, data, err = self._get("/v1/client-info")
        if code != 200:
            raise RuntimeError(f"client-info {code}: {err}")
        return data  # noqa

    def accounts(self) -> list[dict]:
        return self.client_info().get("accounts") or []

    def summary(self, account: str | None = None, date: str | None = None) -> dict:
        self.refresh()
        acc = account or self.account_number
        if not acc:
            accs = self.accounts()
            if accs:
                acc = accs[0]["number"]
            else:
                raise ValueError("Не указан номер счёта и в профиле нет открытых счетов")
        d = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        code, data, err = self._get("/v2/statement/summary",
                                    {"accountNumber": acc, "statementDate": d})
        if code != 200:
            raise RuntimeError(f"summary {code}: {err}")
        return data

    def transactions(self, account: str | None = None, date: str | None = None) -> list[dict]:
        self.refresh()
        acc = account or self.account_number
        if not acc:
            accs = self.accounts()
            if accs:
                acc = accs[0]["number"]
            else:
                raise ValueError("Не указан номер счёта")
        d = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        code, data, err = self._get("/v2/statement/transactions",
                                    {"accountNumber": acc, "statementDate": d})
        if code != 200:
            raise RuntimeError(f"transactions {code}: {err}")
        return data.get("transactions") or []

    def increment(self, last_modify: str, account: str | None = None) -> list[dict]:
        """Только новые/изменённые операции с момента last_modify (yyyy-MM-ddTHH:mm:ss)."""
        self.refresh()
        acc = account or self.account_number
        if not acc:
            accs = self.accounts()
            if accs:
                acc = accs[0]["number"]
            else:
                raise ValueError("Не указан номер счёта")
        code, data, err = self._get("/v2/statement/increment",
                                    {"accountNumber": acc, "lastModifyDate": last_modify})
        if code != 200:
            raise RuntimeError(f"increment {code}: {err}")
        return data.get("transactions") or []


def fmt_amount(tx: dict) -> str:
    amt = (tx.get("amountRub") or tx.get("amount") or {}).get("amount", "0")
    try:
        return f"{float(amt):,.2f}".replace(",", " ").replace(".", ",")
    except ValueError:
        return str(amt)


def direction(tx: dict) -> str:
    return (tx.get("direction") or "").upper()


def payer(tx: dict) -> dict:
    rt = tx.get("rurTransfer") or {}
    return {
        "name": rt.get("payerName") or tx.get("payerName") or "",
        "inn": rt.get("payerInn") or "",
        "account": rt.get("payerAccount") or "",
        "bic": rt.get("payerBankBic") or "",
    }


if __name__ == "__main__":
    prof = "default"
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-") and sys.argv[1] not in ("summary", "client-info"):
        prof = sys.argv.pop(1)

    api = SberAPI(profile=prof)
    api.refresh()
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        d = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        for a in api.accounts():
            num = a["number"]
            s = api.summary(account=num, date=d)
            bal = (s.get("closingBalanceRub") or {}).get("amount", 0)
            print(f"[{api.profile}] Счёт {num} ({a.get('name', 'Расчётный')}) — остаток {bal} RUB (на {d})")
    else:
        ci = api.client_info()
        print(f"[{api.profile}] {ci.get('shortName', 'Организация')}  ИНН {ci.get('inn', '')}  ОГРН {ci.get('ogrn', '')}")
        for a in ci.get("accounts", []):
            print(f"  {a['number']}  {a.get('name', '')}  {a.get('state', '')}  открыт {a.get('openDate', '')}")
