#!/usr/bin/env python3
"""
Sber Business Payments — поиск контрагентов, создание черновиков платёжек и проверка статуса.
Использует официальный промышленный MCP-сервер Sber API:
https://fintech.sberbank.ru:9443/fintech/api/business-payments/mcp

Авторизация: Zero-Knowledge Vault (mTLS + Bearer токен).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import uuid
from typing import Any

from sber_api import API, SberAPI

MCP_URL = f"{API}/business-payments/mcp"
SBI_PORTAL = "https://sbi.sberbank.ru:9443"


def mcp_call(method: str, params: dict | None = None, api: SberAPI | None = None) -> dict:
    """Вызов MCP JSON-RPC через curl с безопасным ephemeral mTLS из Vault и Bearer."""
    if api is None:
        api = SberAPI()
    api.refresh()

    req_id = str(uuid.uuid4())
    payload = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method,
        "params": params or {},
    }
    payload_bytes = json.dumps(payload, ensure_ascii=False)

    def _run(cert: str, key: str, cacert: str):
        cmd = [
            "curl", "-sS", "--max-time", "30",
            "--cert", cert, "--key", key, "--cacert", cacert,
            "-X", "POST", MCP_URL,
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json, text/event-stream",
            "-H", f"Authorization: Bearer {api.access_token}",
            "-d", payload_bytes,
        ]
        return subprocess.run(cmd, capture_output=True, text=True)

    res = api._execute_with_tls(_run)
    if res.returncode != 0:
        raise RuntimeError(f"curl failed: {res.stderr}")

    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from Sber MCP: {res.stdout[:300]}") from exc

    if "error" in data:
        err = data["error"]
        raise RuntimeError(f"Sber MCP Error [{err.get('code')}]: {err.get('message')} {err.get('data')}")

    return data.get("result") or {}


def search_counterparty(query: str, api: SberAPI | None = None) -> dict | None:
    """Поиск контрагента в справочнике СберБизнес (ИНН, наименование или ФИО)."""
    res = mcp_call("tools/call", {
        "name": "correspondent_rur.get",
        "arguments": {"searchCriteria": query}
    }, api=api)

    content = res.get("content", [])
    if not content:
        return None
    raw_text = content[0].get("text", "")
    try:
        parsed = json.loads(raw_text)
    except Exception:
        return {"raw": raw_text}

    if parsed.get("cause") == "NOT_FOUND":
        return None
    return parsed


def create_payment_draft(
    payee_name: str,
    payee_inn: str,
    payee_account: str,
    payee_bank_bic: str,
    payee_bank_corr: str,
    amount: float,
    purpose: str,
    payee_kpp: str | None = None,
    external_id: str | None = None,
    api: SberAPI | None = None,
) -> dict:
    """Создаёт черновик рублёвого платёжного поручения в СберБизнес.

    Возвращает dict с externalId, статусом и ссылкой на подписание.
    """
    ext_id = external_id or str(uuid.uuid4())
    args: dict[str, Any] = {
        "externalId": ext_id,
        "amount": round(float(amount), 2),
        "purpose": purpose.strip(),
        "payeeName": payee_name.strip(),
        "payeeInn": payee_inn.strip(),
        "payeeAccount": payee_account.strip(),
        "payeeBankBic": payee_bank_bic.strip(),
        "payeeBankCorrAccount": payee_bank_corr.strip(),
    }
    if payee_kpp:
        args["payeeKpp"] = payee_kpp.strip()

    res = mcp_call("tools/call", {
        "name": "rur_payment.create_invoice",
        "arguments": args
    }, api=api)

    content = res.get("content", [])
    raw_text = content[0].get("text", "") if content else ""
    try:
        parsed = json.loads(raw_text)
    except Exception:
        parsed = {"raw": raw_text}

    link = f"{SBI_PORTAL}/ic/ufs/rpp-light/index.html#/payment-creator/{ext_id}"
    parsed["externalId"] = ext_id
    parsed["signUrl"] = link
    return parsed


def get_payment_state(external_id: str, api: SberAPI | None = None) -> dict:
    """Получает текущий статус платёжного поручения по externalId."""
    res = mcp_call("tools/call", {
        "name": "rur_payment.get_state",
        "arguments": {"externalId": external_id.strip()}
    }, api=api)

    content = res.get("content", [])
    raw_text = content[0].get("text", "") if content else ""
    try:
        return json.loads(raw_text)
    except Exception:
        return {"raw": raw_text}


def main() -> int:
    parser = argparse.ArgumentParser(description="Управление платёжками СберБизнес (MCP + Banking Vault)")
    parser.add_argument("--profile", default="default", help="Имя профиля")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # Search
    p_search = subparsers.add_parser("search", help="Поиск контрагента в справочнике банка")
    p_search.add_argument("query", help="ИНН, наименование или ФИО")

    # Create
    p_create = subparsers.add_parser("create", help="Создать черновик платёжного поручения")
    p_create.add_argument("--payee", required=True, help="Наименование получателя")
    p_create.add_argument("--inn", required=True, help="ИНН получателя")
    p_create.add_argument("--kpp", default=None, help="КПП получателя (для юрлиц)")
    p_create.add_argument("--account", required=True, help="Расчётный счёт получателя (20 цифр)")
    p_create.add_argument("--bic", required=True, help="БИК банка получателя (9 цифр)")
    p_create.add_argument("--corr", required=True, help="Корр. счёт банка получателя (20 цифр)")
    p_create.add_argument("--amount", type=float, required=True, help="Сумма платежа в рублях")
    p_create.add_argument("--purpose", required=True, help="Назначение платежа (с информацией об НДС)")
    p_create.add_argument("--external-id", default=None, help="Опциональный внешний UUID")

    # Status
    p_status = subparsers.add_parser("status", help="Проверить статус платежа")
    p_status.add_argument("external_id", help="UUID платежа (externalId)")

    args = parser.parse_args()
    api = SberAPI(profile=args.profile)

    if args.action == "search":
        res = search_counterparty(args.query, api=api)
        if not res:
            print(f"Контрагент по запросу '{args.query}' не найден в справочнике банка ({api.profile}).")
            return 1
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    if args.action == "create":
        res = create_payment_draft(
            payee_name=args.payee,
            payee_inn=args.inn,
            payee_account=args.account,
            payee_bank_bic=args.bic,
            payee_bank_corr=args.corr,
            amount=args.amount,
            purpose=args.purpose,
            payee_kpp=args.kpp,
            external_id=args.external_id,
            api=api,
        )
        print("Результат создания черновика:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
        print(f"\nСсылка для подписания в СберБизнес:\n{res.get('signUrl')}")
        return 0

    if args.action == "status":
        res = get_payment_state(args.external_id, api=api)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
