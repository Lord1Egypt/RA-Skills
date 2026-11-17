#!/usr/bin/env python3
"""UDI Validator — parse and validate medical device UDI strings (GS1 / HIBCC / ICCBBA).

Usage:
    python udi_validate.py "<udi string 1>" "<udi string 2>" ...
    python udi_validate.py --file barcode_dump.txt          # raw barcode output, one string per line (GS1-29 separators allowed)
    python udi_validate.py --checkdigit 0694758932004       # compute GTIN-14 check digit

Exit codes: 0 = all valid, 1 = at least one invalid, 2 = usage error.

License: MIT
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta

GROUP_SEP = "\x1d"  # GS1 FNC1 / group separator (ASCII 29)

# AI -> (fixed_length or None for variable, max_len, name)
AI_TABLE = {
    "00": (18, 18, "SSCC"),
    "01": (14, 14, "GTIN (UDI-DI)"),
    "02": (14, 14, "GTIN of contained trade items"),
    "10": (None, 20, "Batch / lot number"),
    "11": (6, 6, "Production date (YYMMDD)"),
    "12": (6, 6, "Due date (YYMMDD)"),
    "13": (6, 6, "Packaging date (YYMMDD)"),
    "15": (6, 6, "Best before date (YYMMDD)"),
    "16": (6, 6, "Sell by date (YYMMDD)"),
    "17": (6, 6, "Expiration date (YYMMDD)"),
    "20": (2, 2, "Internal product variant"),
    "21": (None, 20, "Serial number"),
    "22": (None, 29, "Consumer product variant"),
    "240": (None, 30, "Additional product identification"),
    "241": (None, 30, "Customer part number"),
    "250": (None, 30, "Secondary serial number"),
    "251": (None, 30, "Reference to source entity"),
    "30": (None, 8, "Count of trade items"),
    "37": (None, 8, "Count of trade items contained"),
    "710": (None, 20, "NHRN — Germany"),
    "711": (None, 20, "NHRN — France"),
    "712": (None, 20, "NHRN — Spain"),
    "713": (None, 20, "NHRN — Brasil"),
}

VARIABLE_AIS_TRIED = ["10", "21", "22", "240", "241", "250", "251", "30", "37", "710", "711", "712", "713"]


def gtin_check_digit(partial: str) -> str | None:
    """Compute GS1 mod-10 check digit for a 13-digit (or any) GTIN prefix."""
    digits = partial.strip()
    if not digits.isdigit() or len(digits) < 2:
        return None
    total = 0
    for i, ch in enumerate(reversed(digits)):
        weight = 3 if i % 2 == 0 else 1
        total += int(ch) * weight
    return str((10 - total % 10) % 10)


def gtin_valid(gtin: str) -> bool:
    if len(gtin) not in (8, 12, 13, 14) or not gtin.isdigit():
        return False
    body, cd = gtin[:-1], gtin[-1]
    return gtin_check_digit(body) == cd


def parse_gs1_date(v: str, label: str) -> tuple[str, str]:
    """Return (verdict, human_date). GS1 date = YYMMDD; DD '00' = day unknown."""
    yy, mm, dd = int(v[:2]), int(v[2:4]), int(v[4:6])
    year = 2000 + yy
    if not 1 <= mm <= 12:
        return ("INVALID: month %02d out of range" % mm, "")
    if dd == 0:
        return ("OK (day unknown '00')", f"{year}-{mm:02d} (day unknown)")
    try:
        d = date(year, mm, dd)
    except ValueError:
        return ("INVALID: day %02d not in month" % dd, "")
    note = ""
    if "expir" in label.lower() and d < date.today():
        note = " — WARNING: already expired"
    return ("OK" + note, d.isoformat())


def detect_agency(raw: str) -> str:
    s = raw.strip()
    if s.startswith("="):
        return "ICCBBA (ISBT 128)"
    if s.startswith("+"):
        return "HIBCC"
    return "GS1"


def parse_gs1(s: str) -> tuple[list[tuple[str, str, str, str]], list[str]]:
    """Parse a GS1 element string -> (rows of (ai, value, name, verdict), problems)."""
    s = s.replace(" ", "").replace(GROUP_SEP, "\x1d").strip()
    if s.startswith("]C1") or s.startswith("]d2") or s.startswith("]e0"):
        s = s[3:]  # symbology identifier
    rows: list[tuple[str, str, str, str]] = []
    problems: list[str] = []
    i = 0
    while i < len(s):
        if s[i] == "\x1d":  # stray group separator before next AI — skip
            i += 1
            continue
        ai = None
        for cand in (s[i:i + 4], s[i:i + 3], s[i:i + 2]):
            if cand in AI_TABLE:
                ai = cand
                break
        if ai is None:
            problems.append(f"position {i}: unknown AI starting at '{s[i:i+4]}' (first 4 chars shown)")
            break
        fixed, maxlen, name = AI_TABLE[ai]
        i += len(ai)
        if fixed is not None:
            value = s[i:i + fixed]
            if len(value) < fixed:
                problems.append(f"AI ({ai}) {name}: needs {fixed} chars, only {len(value)} left")
                break
            i += fixed
            term = None
        else:
            value = ""
            term = None
            for j in range(i, min(i + maxlen, len(s))):
                if s[j] == "\x1d":
                    term = "GS"
                    break
                value += s[j]
            i += len(value) + (1 if term else 0)
        verdict = ""
        if ai in ("01", "02"):
            verdict = "OK (check digit valid)" if gtin_valid(value) else \
                "INVALID: GTIN check digit wrong (expected '%s' at last position)" % (gtin_check_digit(value[:-1]) or "?")
            if not value.isdigit():
                verdict = "INVALID: GTIN must be digits"
        elif ai in ("11", "12", "13", "15", "16", "17"):
            verdict, human = parse_gs1_date(value, name)
            rows.append((ai, value, f"{name} -> {human}", verdict))
            continue
        rows.append((ai, value, name, verdict))
    return rows, problems


def hibcc_rough(s: str) -> list[str]:
    """Very rough HIBCC segmentation for triage only (no check-char arithmetic)."""
    notes = ["HIBCC detected: full check-character validation requires official HIBCC tools."]
    body = s[1:]
    if len(body) < 6:
        notes.append("too short: labeler code (3-5) + product number minimum expected")
    else:
        notes.append(f"labeler code candidate: '{body[:4]}…' (first chars), remaining = product/serial fields")
    return notes


def report_one(raw: str) -> bool:
    agency = detect_agency(raw)
    print(f"\n=== input: {raw!r}")
    print(f"issuing agency: {agency}")
    ok = True
    if agency.startswith("GS1"):
        rows, problems = parse_gs1(raw)
        for ai, value, name, verdict in rows:
            line = f"  ({ai}) {name:<42} = {value}"
            if verdict:
                line += f"   [{verdict}]"
            print(line)
            if "INVALID" in verdict or "WARNING" in verdict:
                ok = False
        for p in problems:
            print(f"  PROBLEM: {p}")
            ok = False
        if not rows and not problems:
            print("  PROBLEM: nothing parsed")
            ok = False
    elif agency.startswith("HIBCC"):
        for n in hibcc_rough(raw):
            print("  " + n)
    else:
        print("  ICCBBA (ISBT 128) detected: use ICCBBA official database for validation.")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="Medical device UDI validator (GS1 / HIBCC / ICCBBA triage)")
    ap.add_argument("strings", nargs="*", help="UDI strings to validate")
    ap.add_argument("--file", help="file with one UDI per line (raw barcode output ok)")
    ap.add_argument("--checkdigit", help="compute GS1 GTIN check digit for a digit prefix")
    args = ap.parse_args()

    if args.checkdigit:
        cd = gtin_check_digit(args.checkdigit)
        print(f"GTIN prefix {args.checkdigit} -> check digit {cd} -> full: {args.checkdigit}{cd}")
        return 0 if cd else 2

    inputs = list(args.strings)
    if args.file:
        with open(args.file, encoding="utf-8", errors="replace") as f:
            inputs += [ln.strip() for ln in f if ln.strip()]
    if not inputs:
        ap.print_help()
        return 2

    all_ok = True
    for raw in inputs:
        if not report_one(raw):
            all_ok = False
    print("\nVERDICT:", "ALL VALID" if all_ok else "PROBLEMS FOUND (see above)")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
