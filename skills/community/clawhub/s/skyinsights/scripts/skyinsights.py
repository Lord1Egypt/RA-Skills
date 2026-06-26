#!/usr/bin/env python3
"""
SkyInsights CLI - CertiK blockchain risk intelligence API wrapper.
Usage:
  python skyinsights.py kya    <address> [chain]
  python skyinsights.py labels <address> [chain]
  python skyinsights.py screen <address> [chain] [rule_set]
  python skyinsights.py kyt    <txn_hash> <chain>
  python skyinsights.py help
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlencode

# screening_v2 submission uses api2; all other endpoints (including /result) use api
BASE_URL = "https://api.skyinsights.certik.com/v4"
SCREEN_SUBMIT_URL = "https://api2.skyinsights.certik.com/v4"

RISK_EMOJI = {
    "None": "✅",
    "Low": "🟡",
    "Medium": "🟠",
    "High": "🔴",
    "Unknown": "⚪",
}

CHAINS_KYA = {
    "btc", "bch", "ltc", "sol", "eth", "polygon", "op", "arb", "avax",
    "bsc", "ftm", "tron", "base", "blast", "scroll", "linea", "sonic",
    "kaia", "world_chain", "unichain", "polygon_zkevm", "multi-chain",
}
CHAINS_LABELS_KYT = CHAINS_KYA - {"multi-chain"}
CHAINS_SCREEN = {
    "btc", "ltc", "sol", "eth", "polygon", "op", "arb", "avax", "bsc", "ftm", "tron"
}

SEP = "━" * 44


def load_credentials():
    key = os.environ.get("SKYINSIGHTS_API_KEY", "")
    secret = os.environ.get("SKYINSIGHTS_API_SECRET", "")
    if key and secret:
        return key, secret

    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, _, value = line.partition("=")
                name = name.strip()
                value = value.strip().strip('"').strip("'")
                if name == "SKYINSIGHTS_API_KEY":
                    key = value
                elif name == "SKYINSIGHTS_API_SECRET":
                    secret = value

    return key, secret


def api_get(path, params, api_key, api_secret, base=None):
    url = f"{base or BASE_URL}{path}?{urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={
            "X-API-KEY": api_key,
            "X-API-SECRET": api_secret,
        },
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        try:
            message = json.loads(body).get("message") or body
        except Exception:
            message = body
        hints = {
            400: "Bad request - check address format or chain name.",
            401: "Unauthorized - verify SKYINSIGHTS_API_KEY and SKYINSIGHTS_API_SECRET.",
            429: "Rate limited - slow down requests.",
            500: "Server error - retry or contact CertiK support.",
        }
        print(f"HTTP {exc.code}: {message}")
        hint = hints.get(exc.code)
        if hint:
            print(f"Hint: {hint}")
        sys.exit(1)


def risk_header(level, title):
    emoji = RISK_EMOJI.get(level, "⚪")
    return f"{emoji} {level.upper()} RISK — {title}"


def fmt_usd(value):
    if value is None:
        return "N/A"
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return str(value)


def print_factors(factors):
    if not factors:
        print("  (none)")
        return
    for category, factor_list in factors.items():
        print(f"  - {category}")
        for factor in factor_list:
            origin = factor.get("origin", "")
            sub_origin = factor.get("sub_origin", "")
            origin_str = f"{origin} ({sub_origin})" if sub_origin else origin
            print(f"    Origin : {origin_str}")
            print(f"    Level  : {factor.get('level', 'Unknown')}")


def print_labels(labels):
    if not labels:
        print("  (none)")
        return
    for label in labels:
        category = label.get("category", "")
        sub_category = label.get("sub_category", "")
        name = label.get("label", "")
        parts = [part for part in (category, sub_category, name) if part]
        print(f"  - {' > '.join(parts)}")


def validate_chain(chain, supported, subcmd):
    if chain not in supported:
        print(f"ERROR: Chain '{chain}' is not supported for '{subcmd}'.")
        print(f"Supported: {' '.join(sorted(supported))}")
        sys.exit(1)


def cmd_kya(address, chain, api_key, api_secret):
    data = api_get("/kya/risk", {"address": address, "chain": chain}, api_key, api_secret)
    result = data.get("data") or data

    level = result.get("risk_level") or "Unknown"
    score = result.get("risk_score", "?")
    entity = result.get("entity") or {}
    labels = result.get("labels") or []
    factors = result.get("risk_factors") or {}

    print(SEP)
    print(risk_header(level, "Address Risk Assessment"))
    print(SEP)
    print(f"Address : {address}")
    print(f"Chain   : {chain}")
    print(f"Score   : {score}/5  |  Level: {level}")

    if entity:
        print()
        print("Entity:")
        if entity.get("name"):
            print(f"  Name    : {entity['name']}")
        if entity.get("country"):
            print(f"  Country : {entity['country']}")
        if entity.get("website"):
            print(f"  Website : {entity['website']}")

    print()
    print("Risk Factors:")
    print_factors(factors)

    print()
    print("Labels:")
    print_labels(labels)
    print(SEP)


def cmd_labels(address, chain, api_key, api_secret):
    data = api_get("/kya/labels", {"address": address, "chain": chain}, api_key, api_secret)
    result = data.get("data") or data

    entity = result.get("entity") or {}
    labels = result.get("labels") or []

    print(SEP)
    print(f"Labels - {address}")
    print(SEP)
    print(f"Address : {address}")
    print(f"Chain   : {chain}")

    if entity:
        print()
        print("Entity:")
        for field in ("name", "country", "website", "type"):
            value = entity.get(field)
            if value:
                print(f"  {field.capitalize():<8}: {value}")

    print()
    print("Labels:")
    print_labels(labels)
    print(SEP)


def derive_risk_level(risk_results):
    order = {"High": 3, "Medium": 2, "Low": 1, "None": 0}
    best = "None"
    for factor_list in risk_results.values():
        for factor in factor_list:
            level = factor.get("level", "None")
            if order.get(level, 0) > order.get(best, 0):
                best = level
    return best if risk_results else "Unknown"


def print_screen_result(result, address, chain, rule_set):
    factors = result.get("risk_results") or {}
    counterparties = result.get("counterparties") or {}
    level = derive_risk_level(factors)

    print(SEP)
    print(risk_header(level, "Screening Result"))
    print(SEP)
    print(f"Address  : {address}")
    print(f"Chain    : {chain}")
    print(f"Rule Set : {rule_set}")
    print(f"Level    : {level}")

    print()
    print("Risk Factors:")
    if not factors:
        print("  No risk factors found")
    else:
        for category, factor_list in factors.items():
            print(f"  - {category}")
            for index, factor in enumerate(factor_list):
                if index > 0:
                    print()
                origin = factor.get("origin", "")
                sub_origin = factor.get("sub_origin", "")
                origin_str = f"{origin} ({sub_origin})" if sub_origin else origin
                print(f"    Origin      : {origin_str}")
                print(f"    Level       : {factor.get('level', 'Unknown')}")
                exposure = factor.get("exposure") or {}
                if exposure:
                    direction = exposure.get("direction", "")
                    usd_amount = fmt_usd(exposure.get("amount_usd"))
                    hop_count = exposure.get("hop_count", "?")
                    counterparty = exposure.get("counterparty_address", "")
                    if direction:
                        print(f"    Direction   : {direction}")
                    if usd_amount != "N/A":
                        print(f"    Amount      : {usd_amount}")
                    if counterparty:
                        print(f"    Counterparty: {counterparty} (hop: {hop_count})")

    if counterparties:
        print()
        items = list(counterparties.items())
        print(f"Counterparties ({len(items)} total, showing up to 10):")
        for address_text, counterparty in items[:10]:
            counterparty_factors = counterparty.get("risk_factors") or {}
            counterparty_level = derive_risk_level(counterparty_factors)
            print(f"  - {address_text} [{counterparty_level}]")
            for category in list(counterparty_factors.keys())[:2]:
                print(f"    -> {category}")

    print(SEP)


def cmd_screen(address, chain, rule_set, api_key, api_secret):
    print(f"Submitting screening for {address} on {chain}...", flush=True)
    submit = api_get(
        "/kya/screening_v2",
        {"address": address, "chain": chain, "rule_set_id": rule_set},
        api_key,
        api_secret,
        base=SCREEN_SUBMIT_URL,
    )
    task_id = (submit.get("data") or {}).get("task_id")
    if not task_id:
        print(f"ERROR: No task_id in response: {submit}")
        sys.exit(1)
    print(f"Task submitted (ID: {task_id}). Waiting for result...", flush=True)

    for attempt in range(30):
        time.sleep(2)
        response = api_get(
            "/kya/screening_v2/result",
            {"task_id": task_id},
            api_key,
            api_secret,
        )
        outer = response.get("data") or response
        status = outer.get("status")
        if status == "SUCCESS":
            result = outer.get("result") or outer
            print_screen_result(result, address, chain, rule_set)
            return
        if status == "FAILED":
            print("ERROR: Screening task failed.")
            sys.exit(1)
        print(f"  [{attempt * 2 + 2}s] Status: {status}...", flush=True)

    print("ERROR: Timed out waiting for screening result (60s).")
    sys.exit(1)


def format_address(address_obj):
    if isinstance(address_obj, dict):
        address = address_obj.get("address", "")
        level = address_obj.get("level") or ""
    else:
        address = str(address_obj)
        level = ""
    emoji = RISK_EMOJI.get(level, "") if level and level != "None" else ""
    return f"{emoji} {address}".strip() if emoji else address


def cmd_kyt(txn_hash, chain, api_key, api_secret):
    data = api_get("/kyt/risk", {"txn_hash": txn_hash, "chain": chain}, api_key, api_secret)
    result = data.get("data") or data

    level = result.get("risk_level") or "Unknown"
    score = result.get("risk_score", "?")
    factors = result.get("risk_factors") or {}
    tokens = result.get("tokens") or []
    total_usdt = result.get("total_usdt")

    transfer = (result.get("transfer") or {}).get("tx_list") or {}
    all_txs = (transfer.get("tx") or []) + (transfer.get("internalTx") or []) + (transfer.get("tokenTx") or [])

    print(SEP)
    print(risk_header(level, "Transaction Risk Assessment"))
    print(SEP)
    print(f"Tx Hash : {txn_hash}")
    print(f"Chain   : {chain}")
    print(f"Score   : {score}/5  |  Level: {level}")
    if tokens:
        print(f"Tokens  : {', '.join(tokens)}")
    if total_usdt is not None:
        print(f"Total   : {fmt_usd(total_usdt)}")

    print()
    print("Risk Factors:")
    print_factors(factors)

    if all_txs:
        print()
        print("Transfers:")
        for transfer_item in all_txs:
            src_obj = transfer_item.get("from", {})
            dst_obj = transfer_item.get("to", {})
            amount = transfer_item.get("amount", "")
            usd_value = fmt_usd(transfer_item.get("usdt_amount") or transfer_item.get("usd_value"))
            token_symbol = transfer_item.get("token_symbol") or transfer_item.get("token", "")
            print(f"  {format_address(src_obj)} -> {format_address(dst_obj)}")
            label = f" {token_symbol}" if token_symbol else ""
            print(f"    Amount: {amount}{label}  ({usd_value})")

    print(SEP)


def cmd_help():
    print(
        """SkyInsights - CertiK Blockchain Risk Intelligence

Commands:
  kya    <address> [chain]                   Address risk assessment
  labels <address> [chain]                   Address labels and entity info
  screen <address> [chain] [rule_set]        Full compliance screening
  kyt    <txn_hash> <chain>                  Transaction risk assessment
  help                                       Show this message

Default chain: eth
Default rule_set: standard-mode-rule-set

Supported chains:
  kya    : btc bch ltc sol eth polygon op arb avax bsc ftm tron
           base blast scroll linea sonic kaia world_chain unichain polygon_zkevm
           multi-chain (cross-chain query)
  labels : same as kya (excluding multi-chain)
  screen : btc ltc sol eth polygon op arb avax bsc ftm tron
  kyt    : same as labels

Credentials (env vars or .env file):
  SKYINSIGHTS_API_KEY
  SKYINSIGHTS_API_SECRET
"""
    )


def main():
    args = sys.argv[1:]
    if not args or args[0] == "help":
        cmd_help()
        return

    subcmd = args[0].lower()
    if subcmd not in ("kya", "labels", "screen", "kyt"):
        print(f"Unknown subcommand: {subcmd!r}")
        print("Run 'python skyinsights.py help' for usage.")
        sys.exit(1)

    api_key, api_secret = load_credentials()
    if not api_key or not api_secret:
        print("ERROR: Set SKYINSIGHTS_API_KEY and SKYINSIGHTS_API_SECRET (env or .env file).")
        sys.exit(1)

    if subcmd == "kya":
        if len(args) < 2:
            print("Usage: skyinsights.py kya <address> [chain]")
            sys.exit(1)
        address = args[1]
        chain = args[2] if len(args) > 2 else "eth"
        validate_chain(chain, CHAINS_KYA, "kya")
        cmd_kya(address, chain, api_key, api_secret)
        return

    if subcmd == "labels":
        if len(args) < 2:
            print("Usage: skyinsights.py labels <address> [chain]")
            sys.exit(1)
        address = args[1]
        chain = args[2] if len(args) > 2 else "eth"
        validate_chain(chain, CHAINS_LABELS_KYT, "labels")
        cmd_labels(address, chain, api_key, api_secret)
        return

    if subcmd == "screen":
        if len(args) < 2:
            print("Usage: skyinsights.py screen <address> [chain] [rule_set]")
            sys.exit(1)
        address = args[1]
        chain = args[2] if len(args) > 2 else "eth"
        rule_set = args[3] if len(args) > 3 else "standard-mode-rule-set"
        validate_chain(chain, CHAINS_SCREEN, "screen")
        cmd_screen(address, chain, rule_set, api_key, api_secret)
        return

    if len(args) < 3:
        print("Usage: skyinsights.py kyt <txn_hash> <chain>")
        sys.exit(1)
    txn_hash = args[1]
    chain = args[2]
    validate_chain(chain, CHAINS_LABELS_KYT, "kyt")
    cmd_kyt(txn_hash, chain, api_key, api_secret)


if __name__ == "__main__":
    main()
