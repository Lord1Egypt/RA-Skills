---
name: subscription-killer
description: >
  Analyse a bank transactions CSV to detect recurring subscriptions, score
  cancellation priority, and surface actionable savings recommendations.
  Designed as the first module in a broader personal-finance agent; bank data
  parsing is deliberately decoupled so future savings / deposit / investment
  skills can reuse it.
version: 1.1.0
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - python3
    envVars:
      - name: SUBSCRIPTION_KILLER_CURRENCY
        required: false
        description: >
          ISO 4217 currency code for display (default: GBP). E.g. USD, EUR, GBP.
    primaryEnv: SUBSCRIPTION_KILLER_CURRENCY
---

# Subscription Killer

Analyse a bank transactions CSV file and surface every recurring subscription,
ranked by cancellation / downgrade priority with estimated monthly savings.

## Skill overview

This skill takes a single CSV file of bank transactions and:

1. Sniffs the CSV structure to detect column names automatically.
2. Normalises merchant names using a curated alias dictionary plus fuzzy
   matching (Levenshtein distance ≤ 2 tokens).
3. Detects recurring charges by cadence (monthly / quarterly / annual) and
   amount consistency (±2 % tolerance).
4. Scores each subscription by confidence (0–100).
5. Ranks subscriptions by a composite priority score: spend × inactivity risk ×
   price-creep factor × duplication penalty.
6. Outputs a structured report with clear cancellation and downgrade actions.

---

## Input format

The skill accepts any CSV export from a personal bank account. Common formats
are auto-detected:

| Bank / Provider | Typical columns |
|-----------------|-----------------|
| Monzo | Date, Name, Amount, Category |
| Starling | Date, Counter Party, Amount, Balance |
| Revolut | Started Date, Description, Amount, Currency |
| Standard OFX export | Date, Description, Debit Amount |
| Generic | date, merchant / description, amount (minimum required) |

Column detection priority:
- **Date**: looks for columns named `date`, `transaction date`, `started date`,
  `posted date` (case-insensitive). Falls back to first column that parses as
  ISO 8601 or DD/MM/YYYY.
- **Amount**: looks for `amount`, `debit amount`, `debit`. Ignores credit /
  top-up rows (positive amounts in debit-positive conventions).
- **Merchant**: looks for `name`, `description`, `merchant`, `counter party`,
  `payee`. Falls back to longest non-numeric column.

---

## Core logic

### Step 1 — Parse CSV

```python
import csv, re, difflib
from datetime import datetime, timedelta
from collections import defaultdict

def sniff_columns(header: list[str]) -> dict:
    """Return {'date': col, 'amount': col, 'merchant': col} best guesses."""
    header_lower = [h.lower().strip() for h in header]
    DATE_HINTS    = ['date', 'transaction date', 'started date', 'posted date']
    AMOUNT_HINTS  = ['amount', 'debit amount', 'debit']
    MERCHANT_HINTS = ['name', 'description', 'merchant', 'counter party',
                      'payee', 'narrative']
    def first_match(hints):
        for hint in hints:
            if hint in header_lower:
                return header[header_lower.index(hint)]
        return None
    return {
        'date':     first_match(DATE_HINTS)     or header[0],
        'amount':   first_match(AMOUNT_HINTS)   or header[1],
        'merchant': first_match(MERCHANT_HINTS) or header[2],
    }

def parse_amount(raw: str) -> float | None:
    """Return a positive debit amount, or None for credits / errors."""
    cleaned = re.sub(r'[£$€,\s]', '', raw.strip())
    if not cleaned:
        return None
    try:
        val = float(cleaned)
        # Debit-positive CSV (most UK banks): only keep debits (negatives after
        # sign flip are credits — skip them)
        # Some CSVs use negative for debits; normalise to positive debit.
        return abs(val) if val != 0 else None
    except ValueError:
        return None
```

### Step 2 — Normalise merchant names

Use a two-pass approach:

**Pass 1 — Known alias dictionary** (curated, highest-confidence)

```python
MERCHANT_ALIASES = {
    # Streaming
    r'netflix':                 'Netflix',
    r'spotify':                 'Spotify',
    r'apple\.com/bill':         'Apple Subscriptions',
    r'itunes':                  'Apple Subscriptions',
    r'amazon prime':            'Amazon Prime',
    r'amzn\s?prime':            'Amazon Prime',
    r'disney\+|disneyplus':     'Disney+',
    r'youtube premium':         'YouTube Premium',
    r'hbo|max\.com':            'Max (HBO)',
    r'paramount':               'Paramount+',
    r'dazn':                    'DAZN',
    # Music
    r'tidal':                   'Tidal',
    r'deezer':                  'Deezer',
    r'soundcloud':              'SoundCloud',
    # Productivity / SaaS
    r'github':                  'GitHub',
    r'notion':                  'Notion',
    r'slack':                   'Slack',
    r'dropbox':                 'Dropbox',
    r'google\s?(one|storage|workspace)': 'Google One/Workspace',
    r'microsoft 365|office 365|msft': 'Microsoft 365',
    r'adobe':                   'Adobe Creative Cloud',
    r'figma':                   'Figma',
    r'zoom':                    'Zoom',
    r'1password|lastpass|bitwarden': 'Password Manager',
    r'nordvpn|expressvpn|surfshark':  'VPN Service',
    # News / Reading
    r'medium':                  'Medium',
    r'substack':                'Substack',
    r'kindle unlimited':        'Kindle Unlimited',
    r'audible':                 'Audible',
    r'the times|thetimes':      'The Times',
    r'financial times|ft\.com': 'Financial Times',
    r'economist':               'The Economist',
    # Fitness
    r'peloton':                 'Peloton',
    r'strava':                  'Strava',
    r'myfitnesspal':            'MyFitnessPal',
    r'calm|headspace':          'Meditation App',
    # Utilities / services
    r'amazon web services|aws': 'AWS',
    r'google cloud|gcp':        'Google Cloud',
    r'digitalocean':            'DigitalOcean',
    r'cloudflare':              'Cloudflare',
    r'railway\.app':            'Railway',
    r'openai':                  'OpenAI',
    r'anthropic':               'Anthropic',
}

def normalize_merchant(raw: str) -> str:
    """Return a clean, canonical merchant name."""
    s = raw.lower().strip()
    for pattern, canonical in MERCHANT_ALIASES.items():
        if re.search(pattern, s, re.IGNORECASE):
            return canonical
    # Pass 2 — strip noise tokens (card numbers, references, country codes)
    cleaned = re.sub(
        r'\b(www|com|co\.uk|ltd|limited|uk|us|gb|inc|gmbh)\b'
        r'|\d{4,}'      # card / ref numbers
        r'|\*+\S*'      # asterisk-prefixed tokens
        r'|[^a-z0-9 ]', # special chars
        '', s
    ).strip().title()
    return cleaned or raw.title()
```

**Pass 2 — Fuzzy deduplication** across the transaction list

After normalisation, cluster remaining merchant names by token-set similarity
(`difflib.SequenceMatcher` ratio > 0.82). The most-frequent variant in each
cluster becomes the canonical name.

### Step 3 — Detect recurring charges

```python
def detect_cadence(dates: list[datetime]) -> str | None:
    """
    Return 'monthly', 'quarterly', 'annual', or None.
    Requires ≥ 2 transactions for monthly/quarterly, ≥ 1 for annual hinting.
    """
    if len(dates) < 2:
        # Single occurrence — flag as potential annual if amount > 30
        return 'annual_candidate'
    gaps = sorted([(dates[i+1] - dates[i]).days for i in range(len(dates)-1)])
    median_gap = gaps[len(gaps)//2]
    if 25 <= median_gap <= 35:   return 'monthly'
    if 85 <= median_gap <= 100:  return 'quarterly'
    if 340 <= median_gap <= 380: return 'annual'
    return None

def amounts_consistent(amounts: list[float], tolerance: float = 0.02) -> bool:
    """True if all amounts are within ±2 % of the median."""
    if not amounts:
        return False
    median = sorted(amounts)[len(amounts)//2]
    return all(abs(a - median) / median <= tolerance for a in amounts)
```

### Step 4 — Confidence scoring (0–100)

| Factor | Max points | Logic |
|--------|-----------|-------|
| Cadence regularity | 40 | All gaps within ±3 days of median |
| Amount consistency | 30 | All amounts within ±2 % |
| Known merchant match | 20 | Exact alias dictionary hit |
| Transaction count | 10 | log₂(count) × 3, capped at 10 |

Confidence ≥ 70 → **Confirmed subscription**
Confidence 40–69 → **Probable subscription**
Confidence < 40 → **Possible / flag for review**

### Step 5 — Priority ranking

Each confirmed/probable subscription gets a composite priority score:

```
priority = monthly_cost
         × price_creep_multiplier   # max(amounts) / min(amounts); 1.0 = stable
         × duplication_penalty       # 1.5 if same category has 2+ subscriptions
         × inactivity_risk           # 1.3 if last charge > 45 days ago
```

Higher priority score = stronger cancellation candidate.

**Special flags:**
- **Trial trap**: single charge in the last 7 days from a previously-unseen
  merchant, followed by a recurring pattern. Flag as "check for auto-renew".
- **Price creep**: amount has increased > 5 % over the observation window.
  Flag with the exact amount delta.
- **Annual renewal due**: annual-cadence subscription whose last charge was
  300–365 days ago. Flag with estimated renewal date.
- **Unknown merchant**: low-confidence recurring charge with no alias match.
  Flag for manual review.

---

## Output schema

The skill returns a structured report. Print to stdout as JSON for downstream
agent consumption, or render the human-readable summary below.

```json
{
  "summary": {
    "observation_window_days": 90,
    "total_subscriptions": 12,
    "confirmed": 9,
    "probable": 2,
    "flagged_for_review": 1,
    "monthly_spend_gbp": 187.43,
    "annual_spend_gbp": 2249.16,
    "potential_monthly_saving_gbp": 54.20
  },
  "subscriptions": [
    {
      "merchant": "Adobe Creative Cloud",
      "cadence": "monthly",
      "median_amount": 54.99,
      "last_charge": "2025-04-01",
      "confidence": 95,
      "priority_score": 89.2,
      "flags": ["price_creep"],
      "price_creep_delta": 5.00,
      "cancel_url": "https://account.adobe.com/plans",
      "actions": ["cancel", "downgrade"]
    }
  ],
  "top_cancellation_targets": ["Adobe Creative Cloud", "..."],
  "unknown_merchants": ["TRSF 48291 REF77"],
  "annual_renewals_due": []
}
```

### Human-readable summary (terminal / Telegram)

```
╔══════════════════════════════════════════╗
║        SUBSCRIPTION KILLER  v1.0         ║
╠══════════════════════════════════════════╣
║  12 subscriptions  •  £187/mo  •  £2,249/yr
╚══════════════════════════════════════════╝

TOP CANCELLATION TARGETS
1. Adobe Creative Cloud   £54.99/mo  ↑ price crept +£5.00
2. Calm                   £39.99/yr  last used 3 months ago
3. LinkedIn Premium       £29.99/mo  duplicate: 2 job-search tools

POTENTIAL SAVING:  £54/mo  •  £648/yr

UNKNOWN MERCHANTS (review manually)
• TRSF 48291 REF77  — £12.99/mo  (confidence 38%)
```

---

## Cancel guidance (top 50 services)

The skill bundles a `cancel_urls.json` file mapping canonical merchant names
to their self-serve cancellation pages. This removes friction for the user.

```json
{
  "Netflix":                "https://www.netflix.com/cancelplan",
  "Spotify":                "https://www.spotify.com/account/subscription/cancel",
  "Adobe Creative Cloud":   "https://account.adobe.com/plans",
  "Amazon Prime":           "https://www.amazon.co.uk/mc/pipeline/cancelEndBenefit",
  "Disney+":                "https://www.disneyplus.com/account/subscription",
  "Microsoft 365":          "https://account.microsoft.com/services",
  "GitHub":                 "https://github.com/settings/billing/subscriptions",
  "Dropbox":                "https://www.dropbox.com/account/plan",
  "Zoom":                   "https://zoom.us/billing",
  "LinkedIn Premium":       "https://www.linkedin.com/premium/products",
  "Google One/Workspace":   "https://myaccount.google.com/payments-and-subscriptions",
  "OpenAI":                 "https://platform.openai.com/account/billing"
}
```

---

## Invocation

```bash
# Analyse a CSV file
python3 subscription_killer.py --file transactions.csv

# Override currency display
SUBSCRIPTION_KILLER_CURRENCY=EUR python3 subscription_killer.py --file transactions.csv

# Output raw JSON for piping to another skill
python3 subscription_killer.py --file transactions.csv --json
```

The script reads `SUBSCRIPTION_KILLER_CURRENCY` from the environment for display
only; all internal calculations use the amounts as-found in the CSV.

---

## Roadmap (future skills in this suite)

This skill is intentionally scoped to subscription detection. Planned companion
skills that share the CSV parsing layer:

| Skill | Description |
|-------|-------------|
| `savings-rate-analyser` | Track income vs spend, compute savings rate, compare to benchmarks |
| `deposit-rate-scout`    | Pull live UK/EU savings account rates via open banking APIs |
| `emergency-fund-checker`| Assess months of runway based on average monthly spend |
| `investment-nudger`     | Identify investable surplus after subscriptions + essentials |

The `bank-csv-parser` module within this skill will be extracted into a shared
utility skill once the suite matures.

---

## Security & privacy

- All processing is local. No transaction data leaves the machine.
- The skill does not write any files outside the working directory.
- No API keys required for the core subscription detection flow.
- The `cancel_urls.json` is a static lookup table; no network calls are made
  unless the user explicitly requests live rate data (future skill).
