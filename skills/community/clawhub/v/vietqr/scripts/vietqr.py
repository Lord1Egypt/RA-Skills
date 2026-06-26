#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import unicodedata
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode, quote

BASE_URL = "https://img.vietqr.io/image"
BANK_ALIASES = {
    "mbbank": "MBBank",
    "mb": "MBBank",
    "vietcombank": "Vietcombank",
    "vcb": "Vietcombank",
    "techcombank": "Techcombank",
    "tcb": "Techcombank",
    "acb": "ACB",
    "tpbank": "TPBank",
    "tpb": "TPBank",
    "bidv": "BIDV",
    "vietinbank": "VietinBank",
    "ctg": "VietinBank",
    "agribank": "Agribank",
    "vbard": "Agribank",
    "sacombank": "Sacombank",
    "stb": "Sacombank",
    "vpbank": "VPBank",
    "vpb": "VPBank",
    "hdbank": "HDBank",
    "hdb": "HDBank",
    "vib": "VIB",
    "shb": "SHB",
    "seabank": "SeABank",
    "ocb": "OCB",
    "msb": "MSB",
    "lpbank": "LPBank",
    "lienvietpostbank": "LPBank",
    "pvcombank": "PVcomBank",
    "pvb": "PVcomBank",
    "eximbank": "Eximbank",
    "eib": "Eximbank",
}
_BANK_RE = re.compile(r"^[A-Za-z0-9]{2,32}$")
_ACCOUNT_RE = re.compile(r"^[0-9]{6,19}$")
_TEMPLATE_RE = re.compile(r"^[A-Za-z0-9_-]{2,32}$")
_AMOUNT_WITH_UNIT_RE = re.compile(r"^([0-9]+(?:[.,][0-9]+)?)\s*([a-zA-Z\u00C0-\u1EF9\u0111\u0110]+)$")
_WHOLE_NUMBER_SEPARATORS_RE = re.compile(r"^[0-9][0-9.,_\s]*$")
_THOUSANDS_GROUP_RE = re.compile(r"^[0-9]{1,3}(?:[.,_\s][0-9]{3})+$")
_UNIT_MULTIPLIERS = {
    "k": 1_000,
    "nghin": 1_000,
    "ngan": 1_000,
    "m": 1_000_000,
    "tr": 1_000_000,
    "trieu": 1_000_000,
    "cu": 1_000_000,
}


def build_vietqr_url(
    bank: str,
    account: str,
    amount: int | None = None,
    note: str | None = None,
    account_name: str | None = None,
    template: str = "compact2",
) -> str:
    bank = normalize_bank(bank)
    account = validate_account(account)
    template = validate_template(template)
    path = f"{BASE_URL}/{quote(bank)}-{quote(account)}-{quote(template)}.png"

    params: dict[str, str] = {}
    if amount is not None:
        params["amount"] = str(validate_amount(amount))
    if note:
        params["addInfo"] = note.strip()
    if account_name:
        params["accountName"] = account_name.strip()

    if not params:
        return path
    return f"{path}?{urlencode(params)}"


def normalize_bank(bank: str) -> str:
    raw = bank.strip()
    if not raw:
        raise ValueError("Bank is required")

    alias_key = _normalize_alias_key(raw)
    if alias_key in BANK_ALIASES:
        return BANK_ALIASES[alias_key]

    if not _BANK_RE.fullmatch(raw):
        raise ValueError("Bank must be 2-32 letters/digits, or a supported alias")
    return raw


def validate_account(account: str) -> str:
    value = account.strip()
    if not _ACCOUNT_RE.fullmatch(value):
        raise ValueError("Account must be numeric and 6-19 digits long")
    return value


def validate_template(template: str) -> str:
    value = template.strip()
    if not _TEMPLATE_RE.fullmatch(value):
        raise ValueError("Template must be 2-32 chars: letters, numbers, '_' or '-'")
    return value


def validate_amount(amount: int) -> int:
    if amount <= 0:
        raise ValueError("Amount must be a positive integer")
    return amount


def parse_amount(value: str) -> int:
    raw = value.strip()
    if not raw:
        raise ValueError("Amount is required")

    cleaned = _strip_vnd_suffix(raw)
    if not cleaned:
        raise ValueError("Amount is required")

    if cleaned.isdigit():
        return validate_amount(int(cleaned))

    if _WHOLE_NUMBER_SEPARATORS_RE.fullmatch(cleaned) and _THOUSANDS_GROUP_RE.fullmatch(cleaned):
        whole = re.sub(r"[.,_\s]", "", cleaned)
        return validate_amount(int(whole))

    match = _AMOUNT_WITH_UNIT_RE.fullmatch(cleaned)
    if not match:
        raise ValueError(
            "Amount must be a positive integer, or use Vietnamese shorthand like 10k, 1.5tr, 1,5tr"
        )

    amount_part = match.group(1).replace(",", ".")
    unit_key = _normalize_alias_key(match.group(2))
    multiplier = _UNIT_MULTIPLIERS.get(unit_key)
    if multiplier is None:
        raise ValueError("Amount unit is not supported. Use k, nghin, ngan, tr, trieu, or cu")

    try:
        scaled = Decimal(amount_part) * Decimal(multiplier)
    except InvalidOperation as err:
        raise ValueError("Amount format is invalid") from err

    if scaled != scaled.to_integral_value():
        raise ValueError("Amount shorthand must resolve to a whole number")

    return validate_amount(int(scaled))


def _normalize_alias_key(text: str) -> str:
    lowered = text.strip().lower()
    ascii_text = unicodedata.normalize("NFD", lowered)
    ascii_text = "".join(ch for ch in ascii_text if unicodedata.category(ch) != "Mn")
    ascii_text = ascii_text.replace("đ", "d")
    return re.sub(r"[^a-z0-9]+", "", ascii_text)


def _strip_vnd_suffix(amount_text: str) -> str:
    lowered = amount_text.strip().lower()
    lowered = re.sub(r"\s+", " ", lowered)
    lowered = re.sub(r"(?:\s)?(?:vnd|vnđ|đ)$", "", lowered).strip()
    return lowered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate VietQR image URLs.")
    parser.add_argument("--bank", help="Bank code or bank name alias, e.g. MBBank")
    parser.add_argument("--account", help="Bank account number")
    parser.add_argument(
        "--amount",
        type=parse_amount,
        default=None,
        help="Transfer amount (positive integer or k/K shorthand, e.g. 10k, 2.5K)",
    )
    parser.add_argument("--note", default=None, help="Transfer note / addInfo")
    parser.add_argument("--account-name", default=None, help="Account holder name")
    parser.add_argument("--template", default="compact2", help="QR template, e.g. compact2")
    parser.add_argument("--markdown", action="store_true", help="Print markdown image preview")
    parser.add_argument("--list-banks", action="store_true", help="List built-in bank aliases and exit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.list_banks:
        print("Supported aliases:")
        for alias, bank in sorted(BANK_ALIASES.items()):
            print(f"- {alias} -> {bank}")
        return

    if not args.bank:
        raise SystemExit("Invalid input: --bank is required")
    if not args.account:
        raise SystemExit("Invalid input: --account is required")

    try:
        url = build_vietqr_url(
            bank=args.bank,
            account=args.account,
            amount=args.amount,
            note=args.note,
            account_name=args.account_name,
            template=args.template,
        )
    except ValueError as err:
        raise SystemExit(f"Invalid input: {err}") from err

    if args.markdown:
        print(f"![VietQR]({url})")
    else:
        print(url)


if __name__ == "__main__":
    main()
