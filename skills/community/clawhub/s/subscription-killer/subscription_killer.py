#!/usr/bin/env python3
"""
Subscription Killer v1.1.0
Analyse a bank transactions CSV and surface recurring subscriptions
ranked by cancellation priority.

Usage:
    python3 subscription_killer.py --file transactions.csv
    python3 subscription_killer.py --file transactions.csv --currency USD
    python3 subscription_killer.py --file transactions.csv --min-confidence 40
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path


# ─────────────────────────────────────────────
#  ANSI colours (degrade gracefully on no-TTY)
# ─────────────────────────────────────────────
USE_COLOUR = sys.stdout.isatty()

def _c(code, text):
    return f"\033[{code}m{text}\033[0m" if USE_COLOUR else text

def red(t):     return _c("31", t)
def yellow(t):  return _c("33", t)
def green(t):   return _c("32", t)
def cyan(t):    return _c("36", t)
def bold(t):    return _c("1",  t)
def dim(t):     return _c("2",  t)
def white(t):   return _c("97", t)


# ─────────────────────────────────────────────
#  Merchant alias dictionary
# ─────────────────────────────────────────────
MERCHANT_ALIASES = [
    # Streaming
    (r"netflix",                        "Netflix",               "streaming"),
    (r"disney\+?|disneyplus",           "Disney+",               "streaming"),
    (r"youtube.?premium",               "YouTube Premium",       "streaming"),
    (r"hbo|max\.com",                   "Max (HBO)",             "streaming"),
    (r"paramount",                      "Paramount+",            "streaming"),
    (r"dazn",                           "DAZN",                  "streaming"),
    (r"now\s?tv",                       "NOW TV",                "streaming"),
    (r"apple\s?tv",                     "Apple TV+",             "streaming"),
    (r"mubi",                           "MUBI",                  "streaming"),
    # Music
    (r"spotify",                        "Spotify",               "music"),
    (r"tidal",                          "Tidal",                 "music"),
    (r"deezer",                         "Deezer",                "music"),
    (r"soundcloud",                     "SoundCloud",            "music"),
    (r"amazon\s?music",                 "Amazon Music",          "music"),
    # Apple / Google
    (r"apple[\s.]?(com|bill|subscri)",  "Apple Subscriptions",   "misc"),
    (r"itunes",                         "Apple Subscriptions",   "misc"),
    (r"google\s?(one|storage)",         "Google One",            "storage"),
    (r"google\s?workspace",             "Google Workspace",      "productivity"),
    # Amazon
    (r"amazon\s?prime|amzn\s?prime",    "Amazon Prime",          "shopping"),
    (r"amazon\s?web|aws",               "AWS",                   "dev"),
    (r"kindle\s?unlimited",             "Kindle Unlimited",      "reading"),
    (r"audible",                        "Audible",               "reading"),
    # Microsoft
    (r"microsoft\s?365|office\s?365",   "Microsoft 365",         "productivity"),
    (r"xbox\s?(game\s?pass|live)",      "Xbox Game Pass",        "gaming"),
    # Adobe / Design
    (r"adobe",                          "Adobe Creative Cloud",  "design"),
    (r"figma",                          "Figma",                 "design"),
    (r"canva",                          "Canva",                 "design"),
    (r"sketch",                         "Sketch",                "design"),
    # Productivity / SaaS
    (r"notion",                         "Notion",                "productivity"),
    (r"slack",                          "Slack",                 "comms"),
    (r"zoom",                           "Zoom",                  "comms"),
    (r"dropbox",                        "Dropbox",               "storage"),
    (r"github",                         "GitHub",                "dev"),
    (r"gitlab",                         "GitLab",                "dev"),
    (r"atlassian|jira|confluence",      "Atlassian",             "dev"),
    (r"linear",                         "Linear",                "dev"),
    (r"vercel",                         "Vercel",                "dev"),
    (r"railway",                        "Railway",               "dev"),
    (r"digitalocean",                   "DigitalOcean",          "dev"),
    (r"cloudflare",                     "Cloudflare",            "dev"),
    (r"openai",                         "OpenAI",                "ai"),
    (r"anthropic",                      "Anthropic",             "ai"),
    (r"1password",                      "1Password",             "security"),
    (r"lastpass",                       "LastPass",              "security"),
    (r"bitwarden",                      "Bitwarden",             "security"),
    (r"nordvpn|expressvpn|surfshark",   "VPN Service",           "security"),
    # News / Reading
    (r"medium",                         "Medium",                "reading"),
    (r"substack",                       "Substack",              "reading"),
    (r"financial\s?times|ft\.com",      "Financial Times",       "reading"),
    (r"the\s?times",                    "The Times",             "reading"),
    (r"economist",                      "The Economist",         "reading"),
    (r"guardian",                       "The Guardian",          "reading"),
    (r"new\s?york\s?times|nytimes",     "New York Times",        "reading"),
    # Fitness / Wellness
    (r"peloton",                        "Peloton",               "fitness"),
    (r"strava",                         "Strava",                "fitness"),
    (r"myfitnesspal",                   "MyFitnessPal",          "fitness"),
    (r"calm",                           "Calm",                  "wellness"),
    (r"headspace",                      "Headspace",             "wellness"),
    (r"whoop",                          "WHOOP",                 "fitness"),
    (r"noom",                           "Noom",                  "wellness"),
    # Career
    (r"linkedin.?premium",              "LinkedIn Premium",      "career"),
    (r"coursera",                       "Coursera",              "learning"),
    (r"udemy",                          "Udemy",                 "learning"),
    (r"skillshare",                     "Skillshare",            "learning"),
    # Gaming
    (r"playstation|ps\s?plus|ps\s?now", "PlayStation Plus",      "gaming"),
    (r"nintendo\s?online",              "Nintendo Online",       "gaming"),
    (r"steam",                          "Steam",                 "gaming"),
]

CANCEL_URLS = {
    "Netflix":               "https://www.netflix.com/cancelplan",
    "Spotify":               "https://www.spotify.com/account/subscription/cancel",
    "Adobe Creative Cloud":  "https://account.adobe.com/plans",
    "Amazon Prime":          "https://www.amazon.co.uk/mc/pipeline/cancelEndBenefit",
    "Disney+":               "https://www.disneyplus.com/account/subscription",
    "Microsoft 365":         "https://account.microsoft.com/services",
    "GitHub":                "https://github.com/settings/billing/subscriptions",
    "Dropbox":               "https://www.dropbox.com/account/plan",
    "Zoom":                  "https://zoom.us/billing",
    "LinkedIn Premium":      "https://www.linkedin.com/premium/products",
    "Google One":            "https://myaccount.google.com/payments-and-subscriptions",
    "Google Workspace":      "https://admin.google.com/ac/billing/subscriptions",
    "OpenAI":                "https://platform.openai.com/account/billing",
    "Apple Subscriptions":   "https://support.apple.com/en-gb/118428",
    "Apple TV+":             "https://support.apple.com/en-gb/118428",
    "YouTube Premium":       "https://www.youtube.com/paid_memberships",
    "Notion":                "https://www.notion.so/profile/billing",
    "Figma":                 "https://www.figma.com/billing",
    "Canva":                 "https://www.canva.com/settings/billing",
    "1Password":             "https://my.1password.com/profile/billing",
    "Slack":                 "https://slack.com/intl/en-gb/help/articles/214908788",
    "Atlassian":             "https://admin.atlassian.com/",
    "DigitalOcean":          "https://cloud.digitalocean.com/account/billing",
    "Railway":               "https://railway.app/account/billing",
    "Vercel":                "https://vercel.com/dashboard/settings/billing",
    "Calm":                  "https://www.calm.com/app/account",
    "Headspace":             "https://www.headspace.com/account",
    "Strava":                "https://www.strava.com/account",
    "Peloton":               "https://members.onepeloton.co.uk/profile/preferences",
    "LinkedIn Premium":      "https://www.linkedin.com/premium/products",
    "PlayStation Plus":      "https://www.playstation.com/en-gb/playstation-network/account/subscriptions/",
    "Xbox Game Pass":        "https://account.microsoft.com/services",
}


# ─────────────────────────────────────────────
#  CSV parsing — universal column sniffing
# ─────────────────────────────────────────────

# Token-weight tables: each entry is (token, score).
# A header is scored by summing weights of tokens it contains.
# Negative weights penalise columns that look like the wrong field type.
# The highest-scoring column wins for each role.

DATE_TOKENS = [
    ("date", 10), ("created", 8), ("time", 6), ("posted", 8),
    ("booking", 7), ("transaction", 4), ("value", 3), ("started", 7),
    ("finished", 3), ("on", 1), ("at", 1),
    ("amount", -20), ("fee", -10), ("id", -5), ("status", -15),
    ("currency", -15), ("rate", -10), ("name", -8),
]

AMOUNT_TOKENS = [
    ("amount", 10), ("sum", 8), ("value", 6), ("debit", 10),
    ("withdrawal", 9), ("paid", 6), ("out", 3), ("source", 5),
    ("after", 4), ("fees", 3), ("net", 5), ("total", 4),
    ("fee", -4), ("target", -6), ("currency", -15),
    ("date", -15), ("name", -12), ("id", -10), ("status", -15),
    ("rate", -8), ("reference", -10), ("batch", -10), ("note", -10),
    ("category", -10), ("direction", -10),
]

MERCHANT_TOKENS = [
    ("name", 10), ("merchant", 12), ("payee", 11), ("description", 9),
    ("narrative", 9), ("counterparty", 10), ("counter", 8), ("party", 5),
    ("details", 7), ("reference", 5), ("note", 4), ("target", 6),
    ("recipient", 9), ("beneficiary", 9), ("to", 3),
    ("amount", -15), ("fee", -8), ("currency", -15), ("date", -15),
    ("id", -10), ("status", -15), ("rate", -10), ("batch", -10),
    ("source", -4), ("created", -10), ("finished", -10),
]


def _score_header(header: str, token_weights: list) -> int:
    h = header.lower()
    tokens = set(re.split(r"[\s_\-\(\)/]+", h))
    score = 0
    for token, weight in token_weights:
        if token in tokens or token in h:
            score += weight
    return score


def sniff_columns(headers: list) -> dict:
    """
    Score every header against date/amount/merchant token tables and pick
    the best non-overlapping assignment. Works with any bank export format
    including long compound names like 'Source amount (after fees)'.
    """
    date_scores     = [(_score_header(h, DATE_TOKENS),     i) for i, h in enumerate(headers)]
    amount_scores   = [(_score_header(h, AMOUNT_TOKENS),   i) for i, h in enumerate(headers)]
    merchant_scores = [(_score_header(h, MERCHANT_TOKENS), i) for i, h in enumerate(headers)]

    used = set()

    def pick_best(scores):
        for score, idx in sorted(scores, reverse=True):
            if score > 0 and idx not in used:
                used.add(idx)
                return headers[idx]
        return None

    # Amount first — most critical to get right
    amount_col   = pick_best(amount_scores)
    date_col     = pick_best(date_scores)
    merchant_col = pick_best(merchant_scores)

    # Hard fallbacks
    all_h = list(headers)
    if not date_col:
        date_col = next((h for h in all_h if h not in used), all_h[0])
        used.add(all_h.index(date_col))
    if not amount_col:
        amount_col = next((h for h in all_h if h not in used), all_h[1])
        used.add(all_h.index(amount_col))
    if not merchant_col:
        merchant_col = next((h for h in all_h if h not in used), all_h[2])

    return {"date": date_col, "amount": amount_col, "merchant": merchant_col}


def explain_sniff(cols: dict) -> str:
    return (f"date='{cols['date']}'  "
            f"amount='{cols['amount']}'  "
            f"merchant='{cols['merchant']}'")


def parse_date(raw: str) -> datetime | None:
    raw = raw.strip().strip('"')
    # Full datetime formats must come before date-only formats.
    # strptime matches %Y-%m-%d against "2026-04-25 18:47:08" successfully
    # (returns midnight) without error, so ordering is critical.
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
                "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M",
                "%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y",
                "%d %b %Y", "%d %B %Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def parse_amount(raw: str) -> float | None:
    cleaned = re.sub(r"[£$€,\s\"]", "", raw.strip())
    if not cleaned:
        return None
    try:
        val = float(cleaned)
        return abs(val) if val != 0 else None
    except ValueError:
        return None


def load_csv(filepath: str) -> list[dict]:
    """Load CSV, sniff columns, return list of {merchant, amount, date}."""
    rows = []
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        # Try to detect delimiter
        sample = f.read(4096)
        f.seek(0)
        delimiter = "," if sample.count(",") >= sample.count(";") else ";"
        reader = csv.DictReader(f, delimiter=delimiter)
        headers = reader.fieldnames or []
        if not headers:
            print(red("✗ Could not read CSV headers. Is this a valid CSV file?"))
            sys.exit(1)
        cols = sniff_columns(list(headers))
        print(dim(f"  Column mapping: {explain_sniff(cols)}"))
        skipped = 0
        for row in reader:
            merchant = row.get(cols["merchant"], "").strip()
            amount   = parse_amount(row.get(cols["amount"], ""))
            date     = parse_date(row.get(cols["date"], ""))
            if merchant and amount and date:
                rows.append({"merchant": merchant, "amount": amount, "date": date})
            else:
                skipped += 1
    if skipped:
        print(dim(f"  (skipped {skipped} rows with missing/unparseable fields)"))
    return rows


# ─────────────────────────────────────────────
#  Merchant normalisation
# ─────────────────────────────────────────────
def normalize_merchant(raw: str) -> tuple[str, str]:
    """Return (canonical_name, category)."""
    for pattern, name, category in MERCHANT_ALIASES:
        if re.search(pattern, raw, re.IGNORECASE):
            return name, category
    # Strip noise tokens
    cleaned = re.sub(
        r"\b(www|com|co\.uk|ltd|limited|uk|us|gb|inc|gmbh|plc|llc)\b"
        r"|\d{4,}"
        r"|\*+\S*"
        r"|[^a-z0-9 ]",
        " ", raw, flags=re.IGNORECASE
    )
    cleaned = " ".join(cleaned.split()).title()
    return (cleaned or raw.title()), "unknown"


def cluster_merchants(rows: list[dict]) -> list[dict]:
    """Group rows by canonical merchant name."""
    groups = defaultdict(lambda: {"amounts": [], "dates": [], "category": "unknown"})
    for r in rows:
        name, cat = normalize_merchant(r["merchant"])
        groups[name]["amounts"].append(r["amount"])
        groups[name]["dates"].append(r["date"])
        groups[name]["category"] = cat
    return [{"name": k, **v} for k, v in groups.items()]


# ─────────────────────────────────────────────
#  Recurrence detection
# ─────────────────────────────────────────────
def detect_cadence(dates: list[datetime]) -> str | None:
    if len(dates) < 2:
        return "annual_candidate"
    sorted_dates = sorted(dates)
    gaps = [(sorted_dates[i+1] - sorted_dates[i]).days
            for i in range(len(sorted_dates) - 1)]
    median_gap = sorted(gaps)[len(gaps) // 2]
    if 25  <= median_gap <= 35:  return "monthly"
    if 85  <= median_gap <= 100: return "quarterly"
    if 170 <= median_gap <= 200: return "biannual"
    if 340 <= median_gap <= 400: return "annual"
    # Weekly / fortnightly — likely not subscriptions, skip
    return None


def amounts_consistent(amounts: list[float], tolerance: float = 0.04) -> bool:
    if len(amounts) < 2:
        return True
    median = sorted(amounts)[len(amounts) // 2]
    return all(abs(a - median) / max(median, 0.01) <= tolerance for a in amounts)


def monthly_equiv(amount: float, cadence: str) -> float:
    return {
        "monthly":          amount,
        "quarterly":        amount / 3,
        "biannual":         amount / 6,
        "annual":           amount / 12,
        "annual_candidate": amount / 12,
    }.get(cadence, amount)


# ─────────────────────────────────────────────
#  Confidence scoring
# ─────────────────────────────────────────────
def confidence_score(name: str, amounts: list[float],
                     cadence: str, count: int) -> int:
    score = 0
    # Cadence detected
    if cadence in ("monthly", "quarterly", "biannual", "annual"):
        score += 40
    elif cadence == "annual_candidate":
        score += 15
    # Amount consistency
    if amounts_consistent(amounts):
        score += 30
    # Known merchant alias hit
    if any(re.search(p, name, re.IGNORECASE) for p, _, _ in MERCHANT_ALIASES):
        score += 20
    # Transaction count (log scale, capped at 10)
    score += min(10, int(math.log2(count + 1) * 3))
    return min(100, score)


# ─────────────────────────────────────────────
#  Main analysis
# ─────────────────────────────────────────────
def analyse(rows: list[dict], min_confidence: int = 40) -> list[dict]:
    groups = cluster_merchants(rows)
    subs = []
    now = datetime.now()

    for g in groups:
        amounts = sorted(g["amounts"])
        dates   = sorted(g["dates"])
        count   = len(amounts)

        if count < 2:
            continue

        cadence = detect_cadence(dates)
        if cadence is None:
            continue

        median_amount = amounts[len(amounts) // 2]
        min_amount    = min(amounts)
        max_amount    = max(amounts)
        mo_equiv      = monthly_equiv(median_amount, cadence)

        conf          = confidence_score(g["name"], amounts, cadence, count)
        if conf < min_confidence:
            continue

        last_charge   = dates[-1]
        days_since    = (now - last_charge).days
        price_creep   = max_amount / max(min_amount, 0.01) > 1.05
        inactive      = days_since > 60

        # Estimate renewal date for annual/biannual
        renewal_date  = None
        if cadence in ("annual", "biannual", "annual_candidate"):
            period_days = 365 if cadence in ("annual", "annual_candidate") else 180
            renewal_date = last_charge + timedelta(days=period_days)

        # Priority score: higher = stronger cancellation candidate
        priority = mo_equiv
        if price_creep: priority *= 1.4
        if inactive:    priority *= 1.3

        subs.append({
            "name":            g["name"],
            "category":        g["category"],
            "cadence":         cadence,
            "median_amount":   round(median_amount, 2),
            "monthly_equiv":   round(mo_equiv, 2),
            "annual_equiv":    round(mo_equiv * 12, 2),
            "min_amount":      round(min_amount, 2),
            "max_amount":      round(max_amount, 2),
            "count":           count,
            "last_charge":     last_charge,
            "days_since":      days_since,
            "confidence":      conf,
            "priority":        round(priority, 2),
            "price_creep":     price_creep,
            "price_creep_delta": round(max_amount - min_amount, 2),
            "inactive":        inactive,
            "renewal_date":    renewal_date,
            "cancel_url":      CANCEL_URLS.get(g["name"]),
            "unknown_merchant": g["category"] == "unknown",
        })

    subs.sort(key=lambda x: x["priority"], reverse=True)
    return subs


# ─────────────────────────────────────────────
#  Terminal rendering
# ─────────────────────────────────────────────
CURRENCY_SYMBOLS = {"GBP": "£", "USD": "$", "EUR": "€"}

def fmt_money(amount: float, symbol: str) -> str:
    return f"{symbol}{amount:,.2f}"

def conf_bar(score: int, width: int = 10) -> str:
    filled = round(score / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    if score >= 70: colour = green
    elif score >= 40: colour = yellow
    else: colour = red
    return colour(bar) + dim(f" {score}%")

def cadence_label(c: str) -> str:
    return {
        "monthly":          "monthly",
        "quarterly":        "quarterly",
        "biannual":         "biannual",
        "annual":           "annual",
        "annual_candidate": "annual?",
    }.get(c, c)

def flag_line(sub: dict, symbol: str) -> str:
    flags = []
    if sub["price_creep"]:
        flags.append(yellow(f"↑ price crept +{symbol}{sub['price_creep_delta']:.2f}"))
    if sub["inactive"]:
        flags.append(red(f"inactive {sub['days_since']}d"))
    if sub["renewal_date"] and sub["renewal_date"] > datetime.now():
        rd = sub["renewal_date"].strftime("%d %b %Y")
        flags.append(cyan(f"renews {rd}"))
    if sub["unknown_merchant"]:
        flags.append(yellow("unknown merchant — review manually"))
    return "  " + "  ·  ".join(flags) if flags else ""


def render_terminal(subs: list[dict], rows_total: int,
                    currency: str, min_confidence: int):
    symbol = CURRENCY_SYMBOLS.get(currency, currency + " ")

    total_mo  = sum(s["monthly_equiv"] for s in subs)
    total_yr  = total_mo * 12
    confirmed = sum(1 for s in subs if s["confidence"] >= 70)
    probable  = sum(1 for s in subs if 40 <= s["confidence"] < 70)
    top3_save = sum(s["monthly_equiv"] for s in subs[:3])

    # ── Header ──────────────────────────────────────────────
    print()
    print(bold("╔══════════════════════════════════════════════════════╗"))
    print(bold("║") + white(bold("          SUBSCRIPTION KILLER  v1.1.0                ")) + bold("║"))
    print(bold("╚══════════════════════════════════════════════════════╝"))
    print()

    # ── Summary cards ───────────────────────────────────────
    print(f"  {bold('Transactions analysed:')}  {rows_total}")
    print(f"  {bold('Subscriptions found:')}    "
          f"{len(subs)}  "
          f"{dim('(')}{ green(str(confirmed) + ' confirmed')}"
          f"{dim(' · ')}{yellow(str(probable) + ' probable')}{dim(')')}")
    print(f"  {bold('Monthly spend:')}          {cyan(fmt_money(total_mo, symbol))}")
    print(f"  {bold('Annual spend:')}           {cyan(fmt_money(total_yr, symbol))}")
    print(f"  {bold('Top-3 saving potential:')} {green(fmt_money(top3_save, symbol) + '/mo')} "
          f"{dim('·')} {green(fmt_money(top3_save * 12, symbol) + '/yr')}")
    print()

    if not subs:
        print(dim("  No recurring subscriptions detected above confidence threshold."))
        return

    # ── Column headers ───────────────────────────────────────
    print(dim("  " + "─" * 80))
    print(
        f"  {bold('Merchant'):<28}"
        f"{bold('Monthly'):>10}"
        f"{bold('Annual'):>10}"
        f"{bold('Cadence'):>12}"
        f"  {bold('Confidence')}"
    )
    print(dim("  " + "─" * 80))

    # ── Subscription rows ────────────────────────────────────
    for i, s in enumerate(subs, 1):
        rank_colour = red if i <= 3 else (yellow if i <= 6 else dim)
        name_str = rank_colour(f"  {i:>2}. {s['name']:<24}")
        mo_str   = fmt_money(s["monthly_equiv"], symbol)
        yr_str   = fmt_money(s["annual_equiv"], symbol)
        cad_str  = cadence_label(s["cadence"])
        bar_str  = conf_bar(s["confidence"])

        print(f"{name_str}{mo_str:>10}{yr_str:>10}{cad_str:>12}  {bar_str}")

        fl = flag_line(s, symbol)
        if fl:
            print(fl)

        if s["cancel_url"]:
            print(dim(f"       cancel → {s['cancel_url']}"))

    print(dim("  " + "─" * 80))

    # ── Top cancellation targets ─────────────────────────────
    print()
    print(bold("  TOP CANCELLATION TARGETS"))
    print()
    for i, s in enumerate(subs[:3], 1):
        reasons = []
        if s["price_creep"]:
            reasons.append(f"price crept +{symbol}{s['price_creep_delta']:.2f}")
        if s["inactive"]:
            reasons.append(f"not used in {s['days_since']} days")
        if s["unknown_merchant"]:
            reasons.append("unrecognised merchant")
        reason_str = f" — {', '.join(reasons)}" if reasons else ""
        print(f"  {red(str(i) + '.')} {bold(s['name']):<28} "
              f"{cyan(fmt_money(s['monthly_equiv'], symbol) + '/mo')}"
              f"{dim(reason_str)}")
        if s["cancel_url"]:
            print(dim(f"     {s['cancel_url']}"))
        print()

    # ── Potential saving ─────────────────────────────────────
    print(bold("  ┌─────────────────────────────────────────────┐"))
    print(bold("  │") + f"  Potential saving (cancel top 3):              " + bold("│"))
    print(bold("  │") +
          f"  {green(bold(fmt_money(top3_save, symbol) + '/mo'))}  ·  "
          f"{green(bold(fmt_money(top3_save * 12, symbol) + '/yr'))}              " +
          bold("│"))
    print(bold("  └─────────────────────────────────────────────┘"))
    print()

    # ── Unknown merchants ────────────────────────────────────
    unknown = [s for s in subs if s["unknown_merchant"]]
    if unknown:
        print(yellow(bold("  UNKNOWN MERCHANTS — review manually")))
        for s in unknown:
            print(f"  · {s['name']:<30} "
                  f"{fmt_money(s['monthly_equiv'], symbol)}/mo  "
                  f"{dim(cadence_label(s['cadence']))}")
        print()

    # ── Annual renewals due ──────────────────────────────────
    renewals = [s for s in subs
                if s["renewal_date"] and
                datetime.now() < s["renewal_date"] <= datetime.now() + timedelta(days=60)]
    if renewals:
        print(cyan(bold("  RENEWALS DUE IN NEXT 60 DAYS")))
        for s in renewals:
            rd = s["renewal_date"].strftime("%d %b %Y")
            print(f"  · {s['name']:<30} {fmt_money(s['median_amount'], symbol)}  "
                  f"renews {cyan(rd)}")
        print()

    print(dim("  All processing is local — no transaction data left this machine."))
    print()


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Subscription Killer — detect recurring charges in a bank CSV"
    )
    parser.add_argument("--file", required=True,
                        help="Path to bank transactions CSV")
    parser.add_argument("--currency",
                        default=os.environ.get("SUBSCRIPTION_KILLER_CURRENCY", "GBP"),
                        help="Currency symbol to display (default: GBP)")
    parser.add_argument("--min-confidence", type=int, default=40,
                        help="Minimum confidence score to include (0-100, default: 40)")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(red(f"✗ File not found: {args.file}"))
        sys.exit(1)
    if path.suffix.lower() not in (".csv", ".txt", ".tsv"):
        print(yellow(f"⚠ Unexpected file extension: {path.suffix} — attempting anyway"))

    print(dim(f"\n  Loading {path.name}..."))
    rows = load_csv(str(path))

    if not rows:
        print(red("✗ No valid transaction rows found. Check the file format."))
        sys.exit(1)

    print(dim(f"  Analysing {len(rows)} transactions..."))
    subs = analyse(rows, min_confidence=args.min_confidence)

    render_terminal(subs, len(rows), args.currency.upper(), args.min_confidence)


if __name__ == "__main__":
    main()
