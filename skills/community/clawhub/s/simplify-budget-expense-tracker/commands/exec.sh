#!/usr/bin/env bash
set -euo pipefail

COMMAND_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_SKILL_DIR="$(cd "${COMMAND_DIR}/.." && pwd)"
DEFAULT_OPENCLAW_HOME="$(cd "${DEFAULT_SKILL_DIR}/../.." && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-${CODEX_HOME:-${DEFAULT_OPENCLAW_HOME}}}"
SKILL_DIR="${SIMPLIFY_BUDGET_SKILL_DIR:-${DEFAULT_SKILL_DIR}}"
SCRIPT_DIR="${SKILL_DIR}/scripts"

if [[ ! -d "$SCRIPT_DIR" ]]; then
  echo "Error: Simplify Budget scripts directory not found at ${SCRIPT_DIR}" >&2
  exit 1
fi

export GOOGLE_SA_FILE="${GOOGLE_SA_FILE:-${OPENCLAW_HOME}/sa.json}"
export SPREADSHEET_ID="${SPREADSHEET_ID:-12zEXdPR9CO7tuFIRqkIM3cQJHvtKo0Q6mXitxiW2WQg}"
export TRACKER_CURRENCY="${TRACKER_CURRENCY:-EUR}"
export TRACKER_CURRENCY_SYMBOL="${TRACKER_CURRENCY_SYMBOL:-€}"
CATEGORY_CACHE_DIR="${OPENCLAW_HOME}/cache/simplify-budget"
CATEGORY_CACHE_FILE="${CATEGORY_CACHE_DIR}/categories.tsv"

fetch_categories_cached() {
  local ttl="${SIMPLIFY_BUDGET_CATEGORY_CACHE_TTL_SECONDS:-21600}"
  mkdir -p "$CATEGORY_CACHE_DIR"

  if [[ -s "$CATEGORY_CACHE_FILE" ]]; then
    if python3 - "$CATEGORY_CACHE_FILE" "$ttl" <<'PY'
import os
import sys
import time

path = sys.argv[1]
ttl = int(sys.argv[2])
raise SystemExit(0 if time.time() - os.path.getmtime(path) < ttl else 1)
PY
    then
      cat "$CATEGORY_CACHE_FILE"
      return 0
    fi
  fi

  local tmp_cache
  tmp_cache="$(mktemp)"
  bash "${SCRIPT_DIR}/get_categories.sh" > "$tmp_cache"
  mv "$tmp_cache" "$CATEGORY_CACHE_FILE"
  cat "$CATEGORY_CACHE_FILE"
}

normalize_date_arg() {
  local value="${1:-}"
  local lowered
  lowered="$(printf '%s' "$value" | tr '[:upper:]' '[:lower:]')"
  case "$lowered" in
    "" | today )
      date +%F
      ;;
    yesterday )
      python3 -c "from datetime import date, timedelta; print((date.today() - timedelta(days=1)).isoformat())"
      ;;
    * )
      # Try to resolve any natural-language or relative date via Python
      python3 - "$value" <<'PY'
import sys
import re
from datetime import date, timedelta

raw = sys.argv[1].strip().lower()

# Already YYYY-MM-DD
if re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
    print(raw)
    raise SystemExit(0)

# N days ago
m = re.match(r"^(\d+)\s+days?\s+ago$", raw)
if m:
    print((date.today() - timedelta(days=int(m.group(1)))).isoformat())
    raise SystemExit(0)

# N weeks ago
m = re.match(r"^(\d+)\s+weeks?\s+ago$", raw)
if m:
    print((date.today() - timedelta(weeks=int(m.group(1)))).isoformat())
    raise SystemExit(0)

# last week
if raw == "last week":
    print((date.today() - timedelta(weeks=1)).isoformat())
    raise SystemExit(0)

# Month name + day, e.g. "march 31" or "31 march"
months = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
          "july":7,"august":8,"september":9,"october":10,"november":11,"december":12,
          "jan":1,"feb":2,"mar":3,"apr":4,"jun":6,"jul":7,"aug":8,
          "sep":9,"oct":10,"nov":11,"dec":12}
m = re.match(r"^([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?$", raw)
if not m:
    m = re.match(r"^(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]+)$", raw)
    if m:
        m = type("m", (), {"group": lambda self, i: [None, m.group(2), m.group(1)][i]})()
if m and m.group(1) in months:
    month_num = months[m.group(1)]
    day_num = int(m.group(2))
    year = date.today().year
    try:
        candidate = date(year, month_num, day_num)
        if candidate > date.today():
            candidate = date(year - 1, month_num, day_num)
        print(candidate.isoformat())
        raise SystemExit(0)
    except ValueError:
        pass

# Fall back: pass through as-is and let write_expense.sh validate
print(sys.argv[1].strip())
PY
      ;;
  esac
}

resolve_category() {
  local value="${1:-}"
  local fallback="${2:-}"
  if [[ -z "$value" ]]; then
    value="$fallback"
  fi

  if [[ -z "$value" ]]; then
    printf '=zategory4\n'
    return 0
  fi

  if [[ "$value" =~ ^=zategory[0-9]+$ ]]; then
    printf '%s\n' "$value"
    return 0
  fi

  if [[ "$value" =~ ^[0-9]+$ ]]; then
    printf '=zategory%s\n' "$value"
    return 0
  fi

  local categories
  categories="$(fetch_categories_cached)"
  local match
  match="$(CATEGORIES="$categories" python3 - "$value" <<'PY'
import os
import sys
import re

needle = sys.argv[1].strip().lower()
lines = [line.rstrip("\n") for line in os.environ.get("CATEGORIES", "").splitlines() if line.strip()]

def norm(s):
    return "".join(ch.lower() for ch in s if ch.isalnum() or ch.isspace()).strip()

def contains_phrase(text, phrase):
    return phrase in text

def classify_category(name_norm):
    checks = [
        ("childcare", ["child", "children", "baby", "kid", "kids", "toddler", "childcare"]),
        ("shopping", ["shopping", "shop", "clothing", "clothes"]),
        ("dining", ["dining", "restaurant", "eat", "food", "takeaway"]),
        ("groceries", ["grocer", "supermarket", "market"]),
        ("transport", ["transport", "car", "fuel", "petrol", "taxi"]),
        ("personal", ["personal care", "skincare", "beauty", "hygiene"]),
        ("utilities", ["utilities", "utility", "internet", "electric", "water", "phone"]),
        ("business", ["business", "work", "office", "client"]),
        ("fun", ["fun", "entertainment", "movie", "game", "hobby"]),
    ]
    for label, markers in checks:
        if any(marker in name_norm for marker in markers):
            return label
    return ""

GROUP_ALIASES = {
    "childcare": [
        "baby", "baby shop", "daughter", "son", "kid", "kids", "child", "children",
        "toddler", "newborn", "diaper", "diapers", "milk powder", "formula",
        "stroller", "pram", "school uniform", "t-shirt for my daughter", "tshirt for my daughter",
    ],
    "shopping": [
        "shirt", "t-shirt", "tshirt", "clothes", "clothing", "dress", "shoes", "bag",
        "iphone", "cable", "charger", "adapter", "usb", "accessory", "gift", "baju",
    ],
    "dining": [
        "coffee", "restaurant", "pizza", "lunch", "dinner", "breakfast", "burger",
        "mcd", "mcdonald", "dominos", "johnny", "donut", "snack", "takeaway",
    ],
    "groceries": [
        "grocery", "groceries", "supermarket", "market", "aeon", "lotus", "tesco",
        "jaya grocer", "big", "mart", "household groceries",
    ],
    "transport": [
        "grab", "uber", "taxi", "bus", "train", "metro", "fuel", "petrol", "shell",
        "petronas", "parking", "toll", "roadtax",
    ],
    "personal": [
        "haircut", "skincare", "shampoo", "soap", "lotion", "makeup", "toiletries",
    ],
    "utilities": [
        "wifi", "internet", "electricity", "water bill", "phone bill", "mobile bill",
        "utility", "utilities",
    ],
    "business": [
        "client", "invoice", "saas", "domain", "hosting", "office", "work expense",
        "software", "subscription for work",
    ],
    "fun": [
        "movie", "cinema", "game", "netflix", "spotify", "concert", "fun",
    ],
}

needle_norm = norm(needle)
needle_tokens = [tok for tok in needle_norm.split() if tok]
categories = []

for line in lines:
    stable_id, full_name = line.split("\t", 1)
    full_norm = norm(full_name)
    categories.append({
        "stable_id": stable_id,
        "full_name": full_name,
        "full_norm": full_norm,
        "group": classify_category(full_norm),
    })

for cat in categories:
    if needle_norm and needle_norm == cat["full_norm"]:
        print(cat["stable_id"])
        raise SystemExit(0)

for cat in categories:
    if needle_norm and needle_norm in cat["full_norm"]:
        print(cat["stable_id"])
        raise SystemExit(0)

scored = []
for cat in categories:
    score = 0
    full_norm = cat["full_norm"]

    token_hits = sum(1 for tok in needle_tokens if len(tok) > 2 and tok in full_norm)
    score += token_hits * 3

    group = cat["group"]
    if group:
        aliases = GROUP_ALIASES.get(group, [])
        alias_hits = sum(1 for alias in aliases if contains_phrase(needle_norm, alias))
        if alias_hits:
            score += alias_hits * 9
            if group == "childcare":
                score += 4

    if group == "shopping" and any(tok in needle_norm for tok in ["shirt", "t-shirt", "tshirt", "clothes", "clothing"]):
        score += 5

    if group == "childcare" and any(tok in needle_norm for tok in ["baby", "daughter", "son", "kid", "child", "children", "toddler"]):
        score += 8

    scored.append((score, cat["stable_id"]))

scored.sort(key=lambda item: item[0], reverse=True)
if scored and scored[0][0] > 0:
    print(scored[0][1])
    raise SystemExit(0)

preferred_groups = ["shopping", "groceries", "transport", "personal", "utilities", "business", "fun", "dining"]
for group in preferred_groups:
    for cat in categories:
        if cat["group"] == group:
            print(cat["stable_id"])
            raise SystemExit(0)

print(categories[0]["stable_id"] if categories else "4")
PY
)"
  printf '=zategory%s\n' "$match"
}

run_write() {
  local amount="" category="" description="" date="" account="Cash" notes=""

  while (($#)); do
    case "$1" in
      --amount) amount="${2:-}"; shift 2 ;;
      --category) category="${2:-}"; shift 2 ;;
      --description|--name) description="${2:-}"; shift 2 ;;
      --date) date="${2:-}"; shift 2 ;;
      --account) account="${2:-}"; shift 2 ;;
      --notes|--note) notes="${2:-}"; shift 2 ;;
      *)
        break
        ;;
    esac
  done

  if [[ -z "$amount" && $# -ge 1 ]]; then amount="$1"; shift; fi
  if [[ -z "$category" && $# -ge 1 ]]; then category="$1"; shift; fi
  if [[ -z "$description" && $# -ge 1 ]]; then description="$1"; shift; fi
  if [[ -z "$date" && $# -ge 1 ]]; then date="$1"; shift; fi
  if [[ "$account" == "Cash" && $# -ge 1 ]]; then account="$1"; shift; fi
  if [[ -z "$notes" && $# -ge 1 ]]; then notes="$1"; shift; fi

  # If no date was explicitly passed, scan description+notes for date hints.
  # This catches cases where the model fails to pass --date but the user's intent
  # is captured in the description (e.g. "ice cream yesterday").
  if [[ -z "$date" ]]; then
    inferred_date="$(python3 - "$description" "$notes" <<'PY'
import sys, re
from datetime import date, timedelta

text = (sys.argv[1] + " " + sys.argv[2]).lower()

MONTHS = {
    "january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
    "july":7,"august":8,"september":9,"october":10,"november":11,"december":12,
    "jan":1,"feb":2,"mar":3,"apr":4,"jun":6,"jul":7,"aug":8,
    "sep":9,"oct":10,"nov":11,"dec":12
}

def resolve(hint):
    h = hint.strip().lower()
    if h == "yesterday":
        return (date.today() - timedelta(days=1)).isoformat()
    m = re.match(r"^(\d+)\s+days?\s+ago$", h)
    if m:
        return (date.today() - timedelta(days=int(m.group(1)))).isoformat()
    m = re.match(r"^(\d+)\s+weeks?\s+ago$", h)
    if m:
        return (date.today() - timedelta(weeks=int(m.group(1)))).isoformat()
    if h == "last week":
        return (date.today() - timedelta(weeks=1)).isoformat()
    for pat in [r"([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?", r"(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]+)"]:
        m = re.search(pat, h)
        if m:
            a, b = m.group(1), m.group(2)
            if a.isdigit():
                a, b = b, a
            if a in MONTHS:
                y = date.today().year
                try:
                    c = date(y, MONTHS[a], int(b))
                    if c > date.today():
                        c = date(y - 1, MONTHS[a], int(b))
                    return c.isoformat()
                except ValueError:
                    pass
    return ""

patterns = [
    r"\byesterday\b",
    r"\b\d+\s+days?\s+ago\b",
    r"\b\d+\s+weeks?\s+ago\b",
    r"\blast\s+week\b",
    r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?\b",
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b",
]
for pat in patterns:
    m = re.search(pat, text)
    if m:
        result = resolve(m.group(0))
        if result:
            print(result)
            raise SystemExit(0)
PY
)"
    if [[ -n "$inferred_date" ]]; then
      date="$inferred_date"
    fi
  fi

  date="$(normalize_date_arg "${date:-today}")"
  category="$(resolve_category "$category" "$description")"

  local args=(
    --amount "$amount"
    --category "$category"
    --description "$description"
    --date "$date"
    --account "$account"
  )
  if [[ -n "$notes" ]]; then
    args+=(--notes "$notes")
  fi

  bash "${SCRIPT_DIR}/write_expense.sh" "${args[@]}"
}

run_find() {
  local query="" limit="10" date_filter="" amount_filter="" description_filter="" notes_filter="" account_filter="" transaction_filter=""
  while (($#)); do
    case "$1" in
      --query) query="${2:-}"; shift 2 ;;
      --limit) limit="${2:-}"; shift 2 ;;
      --date) date_filter="${2:-}"; shift 2 ;;
      --amount) amount_filter="${2:-}"; shift 2 ;;
      --description|--name|--description_text) description_filter="${2:-}"; shift 2 ;;
      --notes|--note|--note_text) notes_filter="${2:-}"; shift 2 ;;
      --account) account_filter="${2:-}"; shift 2 ;;
      --transaction-id|--transaction_id|--id) transaction_filter="${2:-}"; shift 2 ;;
      *)
        if [[ -z "$query" ]]; then
          query="$1"
        elif [[ "$limit" == "10" ]]; then
          limit="$1"
        fi
        shift
      ;;
    esac
  done

  if [[ -n "$date_filter" ]]; then
    date_filter="$(normalize_date_arg "$date_filter")"
  fi

  local args=(
    --query "$query"
    --limit "$limit"
  )
  if [[ -n "$date_filter" ]]; then
    args+=(--date "$date_filter")
  fi
  if [[ -n "$amount_filter" ]]; then
    args+=(--amount "$amount_filter")
  fi
  if [[ -n "$description_filter" ]]; then
    args+=(--description "$description_filter")
  fi
  if [[ -n "$notes_filter" ]]; then
    args+=(--notes "$notes_filter")
  fi
  if [[ -n "$account_filter" ]]; then
    args+=(--account "$account_filter")
  fi
  if [[ -n "$transaction_filter" ]]; then
    args+=(--transaction-id "$transaction_filter")
  fi

  bash "${SCRIPT_DIR}/find_expenses.sh" "${args[@]}"
}

run_update() {
  local transaction_id="" amount="__KEEP__" category="__KEEP__" description="__KEEP__" date="__KEEP__" account="__KEEP__" notes="__KEEP__"
  local parsed_flag_args=0

  if (($#)) && [[ "$1" != --* ]]; then
    transaction_id="$1"
    shift
  fi

  while (($#)); do
    case "$1" in
      --transaction-id|--transaction_id|--transactionId|--id) transaction_id="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --amount) amount="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --category) category="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --description|--name|--description_text) description="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --date) date="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --account) account="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --notes|--note|--note_text) notes="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --clear-notes|--clear_notes) notes="__CLEAR__"; parsed_flag_args=1; shift ;;
      *)
        break
        ;;
    esac
  done

  if [[ -z "$transaction_id" && $# -ge 1 ]]; then transaction_id="$1"; shift; fi

  while (($#)); do
    case "$1" in
      amount=*)
        amount="${1#amount=}"
        parsed_flag_args=1
        shift
        ;;
      category=*)
        category="${1#category=}"
        parsed_flag_args=1
        shift
        ;;
      description=*|name=*)
        description="${1#*=}"
        parsed_flag_args=1
        shift
        ;;
      date=*)
        date="${1#date=}"
        parsed_flag_args=1
        shift
        ;;
      account=*|payment=*|payment_method=*|payment-method=*)
        account="${1#*=}"
        parsed_flag_args=1
        shift
        ;;
      notes=*|note=*)
        notes="${1#*=}"
        parsed_flag_args=1
        shift
        ;;
      clear_notes=*|clear-notes=*)
        if [[ "${1#*=}" =~ ^(1|true|yes)$ ]]; then
          notes="__CLEAR__"
          parsed_flag_args=1
        fi
        shift
        ;;
      *)
        break
        ;;
    esac
  done

  if [[ "$parsed_flag_args" -eq 0 ]]; then
    if [[ $# -eq 1 ]]; then
      category="$1"
      shift
    elif [[ $# -eq 2 ]]; then
      if [[ "$1" =~ ^-?[0-9]+([.][0-9]+)?$ ]]; then
        amount="$1"
        category="$2"
      else
        category="$1 $2"
      fi
      shift $#
    elif [[ $# -eq 3 ]]; then
      if [[ "$1" =~ ^-?[0-9]+([.][0-9]+)?$ ]]; then
        category="$2 $3"
      else
        amount="$1"
        category="$2"
        description="$3"
      fi
      shift $#
    fi
  fi

  if [[ "$amount" == "__KEEP__" && $# -ge 1 ]]; then amount="$1"; shift; fi
  if [[ "$category" == "__KEEP__" && $# -ge 1 ]]; then category="$1"; shift; fi
  if [[ "$description" == "__KEEP__" && $# -ge 1 ]]; then description="$1"; shift; fi
  if [[ "$date" == "__KEEP__" && $# -ge 1 ]]; then date="$1"; shift; fi
  if [[ "$account" == "__KEEP__" && $# -ge 1 ]]; then account="$1"; shift; fi
  if [[ "$notes" == "__KEEP__" && $# -ge 1 ]]; then notes="$1"; shift; fi

  if [[ "$category" != "__KEEP__" ]]; then
    category="$(resolve_category "$category" "$description")"
  fi

  local args=(--id "$transaction_id")
  if [[ "$amount" != "__KEEP__" ]]; then
    args+=(--amount "$amount")
  fi
  if [[ "$category" != "__KEEP__" ]]; then
    args+=(--category "$category")
  fi
  if [[ "$description" != "__KEEP__" ]]; then
    args+=(--description "$description")
  fi
  if [[ "$date" != "__KEEP__" ]]; then
    args+=(--date "$date")
  fi
  if [[ "$account" != "__KEEP__" ]]; then
    args+=(--account "$account")
  fi
  if [[ "$notes" == "__CLEAR__" ]]; then
    args+=(--notes "__CLEAR__")
  elif [[ "$notes" != "__KEEP__" ]]; then
    args+=(--notes "$notes")
  fi

  bash "${SCRIPT_DIR}/update_expense.sh" "${args[@]}"
}

run_delete() {
  local transaction_id=""
  while (($#)); do
    case "$1" in
      --transaction-id|--transaction_id|--transactionId|--id) transaction_id="${2:-}"; shift 2 ;;
      *)
        if [[ -z "$transaction_id" ]]; then
          transaction_id="$1"
        fi
        shift
        ;;
    esac
  done

  bash "${SCRIPT_DIR}/delete_expense.sh" "$transaction_id"
}

run_write_income() {
  local amount="" name="" date="" account="Other" source="Other" notes=""

  while (($#)); do
    case "$1" in
      --amount) amount="${2:-}"; shift 2 ;;
      --name|--description) name="${2:-}"; shift 2 ;;
      --date) date="${2:-}"; shift 2 ;;
      --account|--payment|--payment-method|--payment_method) account="${2:-}"; shift 2 ;;
      --source|--category) source="${2:-}"; shift 2 ;;
      --notes|--note) notes="${2:-}"; shift 2 ;;
      *)
        break
        ;;
    esac
  done

  if [[ -z "$amount" && $# -ge 1 ]]; then amount="$1"; shift; fi
  if [[ -z "$name" && $# -ge 1 ]]; then name="$1"; shift; fi
  if [[ -z "$date" && $# -ge 1 ]]; then date="$1"; shift; fi
  if [[ "$account" == "Other" && $# -ge 1 ]]; then account="$1"; shift; fi
  if [[ "$source" == "Other" && $# -ge 1 ]]; then source="$1"; shift; fi
  if [[ -z "$notes" && $# -ge 1 ]]; then notes="$1"; shift; fi

  date="$(normalize_date_arg "${date:-today}")"

  bash "${SCRIPT_DIR}/write_income.sh" "$amount" "$name" "$date" "$account" "$source" "$notes"
}

run_find_income() {
  local query="" limit="10" date_filter="" amount_filter="" name_filter="" notes_filter="" account_filter="" source_filter="" transaction_filter=""
  while (($#)); do
    case "$1" in
      --query) query="${2:-}"; shift 2 ;;
      --limit) limit="${2:-10}"; shift 2 ;;
      --date) date_filter="${2:-}"; shift 2 ;;
      --amount) amount_filter="${2:-}"; shift 2 ;;
      --name|--description|--description_text) name_filter="${2:-}"; shift 2 ;;
      --notes|--note|--note_text) notes_filter="${2:-}"; shift 2 ;;
      --account|--payment|--payment-method|--payment_method) account_filter="${2:-}"; shift 2 ;;
      --source|--category) source_filter="${2:-}"; shift 2 ;;
      --transaction-id|--transaction_id|--transactionId|--id) transaction_filter="${2:-}"; shift 2 ;;
      *)
        if [[ -z "$query" ]]; then
          query="$1"
        elif [[ "$limit" == "10" ]]; then
          limit="$1"
        fi
        shift
        ;;
    esac
  done

  if [[ -n "$date_filter" ]]; then
    date_filter="$(normalize_date_arg "$date_filter")"
  fi

  local args=(--query "$query" --limit "$limit")
  if [[ -n "$date_filter" ]]; then args+=(--date "$date_filter"); fi
  if [[ -n "$amount_filter" ]]; then args+=(--amount "$amount_filter"); fi
  if [[ -n "$name_filter" ]]; then args+=(--name "$name_filter"); fi
  if [[ -n "$notes_filter" ]]; then args+=(--notes "$notes_filter"); fi
  if [[ -n "$account_filter" ]]; then args+=(--account "$account_filter"); fi
  if [[ -n "$source_filter" ]]; then args+=(--source "$source_filter"); fi
  if [[ -n "$transaction_filter" ]]; then args+=(--transaction-id "$transaction_filter"); fi

  bash "${SCRIPT_DIR}/find_income.sh" "${args[@]}"
}

run_update_income() {
  local transaction_id="" amount="__KEEP__" name="__KEEP__" date="__KEEP__" account="__KEEP__" source="__KEEP__" notes="__KEEP__"
  local parsed_flag_args=0

  if (($#)) && [[ "$1" != --* ]]; then
    transaction_id="$1"
    shift
  fi

  while (($#)); do
    case "$1" in
      --transaction-id|--transaction_id|--transactionId|--id) transaction_id="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --amount) amount="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --name|--description|--description_text) name="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --date) date="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --account|--payment|--payment-method|--payment_method) account="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --source|--category) source="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --notes|--note|--note_text) notes="${2:-}"; parsed_flag_args=1; shift 2 ;;
      --clear-notes|--clear_notes) notes="__CLEAR__"; parsed_flag_args=1; shift ;;
      *)
        break
        ;;
    esac
  done

  if [[ -z "$transaction_id" && $# -ge 1 ]]; then transaction_id="$1"; shift; fi

  while (($#)); do
    case "$1" in
      amount=*)
        amount="${1#amount=}"
        parsed_flag_args=1
        shift
        ;;
      name=*|description=*)
        name="${1#*=}"
        parsed_flag_args=1
        shift
        ;;
      date=*)
        date="${1#date=}"
        parsed_flag_args=1
        shift
        ;;
      account=*|payment=*|payment_method=*|payment-method=*)
        account="${1#*=}"
        parsed_flag_args=1
        shift
        ;;
      source=*|category=*)
        source="${1#*=}"
        parsed_flag_args=1
        shift
        ;;
      notes=*|note=*)
        notes="${1#*=}"
        parsed_flag_args=1
        shift
        ;;
      clear_notes=*|clear-notes=*)
        if [[ "${1#*=}" =~ ^(1|true|yes)$ ]]; then
          notes="__CLEAR__"
          parsed_flag_args=1
        fi
        shift
        ;;
      *)
        break
        ;;
    esac
  done

  if [[ "$parsed_flag_args" -eq 0 ]]; then
    if [[ $# -ge 1 ]]; then amount="$1"; shift; fi
    if [[ $# -ge 1 ]]; then name="$1"; shift; fi
    if [[ $# -ge 1 ]]; then date="$1"; shift; fi
    if [[ $# -ge 1 ]]; then account="$1"; shift; fi
    if [[ $# -ge 1 ]]; then source="$1"; shift; fi
    if [[ $# -ge 1 ]]; then notes="$1"; shift; fi
  fi

  if [[ "$amount" == "__KEEP__" && $# -ge 1 ]]; then amount="$1"; shift; fi
  if [[ "$name" == "__KEEP__" && $# -ge 1 ]]; then name="$1"; shift; fi
  if [[ "$date" == "__KEEP__" && $# -ge 1 ]]; then date="$1"; shift; fi
  if [[ "$account" == "__KEEP__" && $# -ge 1 ]]; then account="$1"; shift; fi
  if [[ "$source" == "__KEEP__" && $# -ge 1 ]]; then source="$1"; shift; fi
  if [[ "$notes" == "__KEEP__" && $# -ge 1 ]]; then notes="$1"; shift; fi

  bash "${SCRIPT_DIR}/update_income.sh" "$transaction_id" "$amount" "$name" "$date" "$account" "$source" "$notes"
}

run_delete_income() {
  local transaction_id=""
  while (($#)); do
    case "$1" in
      --transaction-id|--transaction_id|--transactionId|--id) transaction_id="${2:-}"; shift 2 ;;
      *)
        if [[ -z "$transaction_id" ]]; then
          transaction_id="$1"
        fi
        shift
        ;;
    esac
  done

  bash "${SCRIPT_DIR}/delete_income.sh" "$transaction_id"
}

run_find_recurring() {
  local query="" target_date="" target_month="" mode="month" limit="20"
  while (($#)); do
    case "$1" in
      --query) query="${2:-}"; shift 2 ;;
      --date) target_date="${2:-}"; shift 2 ;;
      --month) target_month="${2:-}"; shift 2 ;;
      --mode) mode="${2:-month}"; shift 2 ;;
      --limit) limit="${2:-20}"; shift 2 ;;
      *)
        if [[ -z "$query" ]]; then
          query="$1"
        fi
        shift
        ;;
    esac
  done

  target_date="$(normalize_date_arg "${target_date:-today}")"
  bash "${SCRIPT_DIR}/find_recurring.sh" --query "$query" --date "$target_date" --month "$target_month" --mode "$mode" --limit "$limit"
}

run_write_recurring() {
  local start_date="" name="" category="" type_value="" frequency="" amount="" account="Other" end_date="" notes="" source=""

  while (($#)); do
    case "$1" in
      --start-date|--start_date|--date) start_date="${2:-}"; shift 2 ;;
      --name|--description) name="${2:-}"; shift 2 ;;
      --category) category="${2:-}"; shift 2 ;;
      --type) type_value="${2:-}"; shift 2 ;;
      --frequency) frequency="${2:-}"; shift 2 ;;
      --amount) amount="${2:-}"; shift 2 ;;
      --account|--payment|--payment-method|--payment_method) account="${2:-}"; shift 2 ;;
      --end-date|--end_date) end_date="${2:-}"; shift 2 ;;
      --notes|--note) notes="${2:-}"; shift 2 ;;
      --source) source="${2:-}"; shift 2 ;;
      *)
        break
        ;;
    esac
  done

  if [[ -z "$start_date" && $# -ge 1 ]]; then start_date="$1"; shift; fi
  if [[ -z "$name" && $# -ge 1 ]]; then name="$1"; shift; fi
  if [[ -z "$category" && $# -ge 1 ]]; then category="$1"; shift; fi
  if [[ -z "$type_value" && $# -ge 1 ]]; then type_value="$1"; shift; fi
  if [[ -z "$frequency" && $# -ge 1 ]]; then frequency="$1"; shift; fi
  if [[ -z "$amount" && $# -ge 1 ]]; then amount="$1"; shift; fi
  if [[ "$account" == "Other" && $# -ge 1 ]]; then account="$1"; shift; fi
  if [[ -z "$end_date" && $# -ge 1 ]]; then end_date="$1"; shift; fi
  if [[ -z "$notes" && $# -ge 1 ]]; then notes="$1"; shift; fi
  if [[ -z "$source" && $# -ge 1 ]]; then source="$1"; shift; fi

  start_date="$(normalize_date_arg "${start_date:-today}")"
  if [[ -n "$end_date" ]]; then
    end_date="$(normalize_date_arg "$end_date")"
  fi

  bash "${SCRIPT_DIR}/write_recurring.sh" "$start_date" "$name" "$category" "$type_value" "$frequency" "$amount" "$account" "$end_date" "$notes" "$source"
}

run_update_recurring() {
  local recurring_id="" start_date="__KEEP__" name="__KEEP__" category="__KEEP__" type_value="__KEEP__" frequency="__KEEP__" amount="__KEEP__" account="__KEEP__" end_date="__KEEP__" notes="__KEEP__" source="__KEEP__"

  if (($#)) && [[ "$1" != --* ]]; then
    recurring_id="$1"
    shift
  fi

  while (($#)); do
    case "$1" in
      --recurring-id|--recurring_id|--recurringId|--id) recurring_id="${2:-}"; shift 2 ;;
      --start-date|--start_date|--date) start_date="${2:-}"; shift 2 ;;
      --name|--description) name="${2:-}"; shift 2 ;;
      --category) category="${2:-}"; shift 2 ;;
      --type) type_value="${2:-}"; shift 2 ;;
      --frequency) frequency="${2:-}"; shift 2 ;;
      --amount) amount="${2:-}"; shift 2 ;;
      --account|--payment|--payment-method|--payment_method) account="${2:-}"; shift 2 ;;
      --end-date|--end_date) end_date="${2:-}"; shift 2 ;;
      --clear-end-date|--clear_end_date) end_date="__CLEAR__"; shift ;;
      --notes|--note) notes="${2:-}"; shift 2 ;;
      --clear-notes|--clear_notes) notes="__CLEAR__"; shift ;;
      --source) source="${2:-}"; shift 2 ;;
      --clear-source|--clear_source) source="__CLEAR__"; shift ;;
      *)
        break
        ;;
    esac
  done

  while (($#)); do
    case "$1" in
      start_date=*|date=*) start_date="${1#*=}"; shift ;;
      name=*|description=*) name="${1#*=}"; shift ;;
      category=*) category="${1#*=}"; shift ;;
      type=*) type_value="${1#*=}"; shift ;;
      frequency=*) frequency="${1#*=}"; shift ;;
      amount=*) amount="${1#*=}"; shift ;;
      account=*|payment=*|payment_method=*|payment-method=*) account="${1#*=}"; shift ;;
      end_date=*|end-date=*) end_date="${1#*=}"; shift ;;
      notes=*|note=*) notes="${1#*=}"; shift ;;
      source=*) source="${1#*=}"; shift ;;
      *)
        shift
        ;;
    esac
  done

  if [[ "$start_date" != "__KEEP__" && "$start_date" != "__CLEAR__" ]]; then
    start_date="$(normalize_date_arg "$start_date")"
  fi
  if [[ "$end_date" != "__KEEP__" && "$end_date" != "__CLEAR__" ]]; then
    end_date="$(normalize_date_arg "$end_date")"
  fi

  bash "${SCRIPT_DIR}/update_recurring.sh" "$recurring_id" "$start_date" "$name" "$category" "$type_value" "$frequency" "$amount" "$account" "$end_date" "$notes" "$source"
}

run_delete_recurring() {
  local recurring_id=""
  while (($#)); do
    case "$1" in
      --recurring-id|--recurring_id|--recurringId|--id) recurring_id="${2:-}"; shift 2 ;;
      *)
        if [[ -z "$recurring_id" ]]; then
          recurring_id="$1"
        fi
        shift
        ;;
    esac
  done

  bash "${SCRIPT_DIR}/delete_recurring.sh" "$recurring_id"
}

run_log() {
  # Usage:
  #   run_log "<raw_text>" [account] [date_hint]
  #   run_log --preview "<raw_text>" [--account <account>] [--date <date_hint>] [--category <category>]
  local raw_text=""
  local account="Cash"
  local date_hint=""
  local preview_only=0
  local category_override=""
  local positional=()

  while (($#)); do
    case "$1" in
      --preview) preview_only=1; shift ;;
      --account) account="${2:-}"; shift 2 ;;
      --date) date_hint="${2:-}"; shift 2 ;;
      --category) category_override="${2:-}"; shift 2 ;;
      --) shift; while (($#)); do positional+=("$1"); shift; done ;;
      --*) echo "Unknown argument: $1" >&2; exit 1 ;;
      *) positional+=("$1"); shift ;;
    esac
  done

  if [[ ${#positional[@]} -ge 1 ]]; then
    raw_text="${positional[0]}"
  fi
  if [[ ${#positional[@]} -ge 2 && "$account" == "Cash" ]]; then
    account="${positional[1]}"
  fi
  if [[ ${#positional[@]} -ge 3 && -z "$date_hint" ]]; then
    date_hint="${positional[2]}"
  fi

  if [[ -z "$raw_text" ]]; then
    echo "Usage: ./log.sh [--preview] \"<raw expense message>\" [account] [date_hint]" >&2
    exit 1
  fi

  local args=("$raw_text")
  if [[ "$preview_only" == "1" ]]; then
    args=(--preview "$raw_text")
  fi
  if [[ -n "$date_hint" ]]; then
    args+=(--date "$(normalize_date_arg "$date_hint")")
  fi
  if [[ -n "$account" ]]; then
    args+=(--account "$account")
  fi
  if [[ -n "$category_override" ]]; then
    args+=(--category "$category_override")
  fi

  bash "${SCRIPT_DIR}/log.sh" "${args[@]}"
}

run_learn_category_alias() {
  local raw_text="${1:-}"
  local category="${2:-}"
  if [[ -z "$raw_text" || -z "$category" ]]; then
    echo "Usage: ./learn_category_alias.sh \"<raw expense message>\" \"<category>\"" >&2
    exit 1
  fi
  bash "${SCRIPT_DIR}/learn_category_alias.sh" "$raw_text" "$category"
}

run_conversation_bridge() {
  bash "${SCRIPT_DIR}/conversation_bridge.sh" "$@"
}

run_find_summary() {
  local target_month=""
  local summary_type=""
  while (($#)); do
    case "$1" in
      --month)
        target_month="${2:-}"
        shift 2
        ;;
      --date)
        target_month="${2:-}"
        shift 2
        ;;
      --type|--metric)
        summary_type="${2:-}"
        shift 2
        ;;
      --period)
        case "${2:-}" in
          this-month|this_month|current-month|current_month|month)
            target_month="$(date +%Y-%m)"
            ;;
          *)
            target_month="${2:-}"
            ;;
        esac
        shift 2
        ;;
      *)
        if [[ -z "$target_month" ]]; then
          case "$1" in
            income|spending|expenses|expense|savings|saving|totals|summary)
              summary_type="$1"
              ;;
            this-month|this_month|current-month|current_month|month|today)
              target_month="$(date +%Y-%m)"
              ;;
            *)
              target_month="$1"
              ;;
          esac
        fi
        shift
        ;;
    esac
  done

  if [[ -z "$target_month" ]]; then
    target_month="$(date +%Y-%m)"
  fi

  local summary_json
  summary_json="$(bash "${SCRIPT_DIR}/find_summary.sh" --month "$target_month")"

  if [[ "$summary_type" =~ ^(income)$ ]]; then
    jq -c '{monthKey, monthLabel, income}' <<<"$summary_json"
  elif [[ "$summary_type" =~ ^(spending|expenses|expense)$ ]]; then
    jq -c '{monthKey, monthLabel, spending}' <<<"$summary_json"
  elif [[ "$summary_type" =~ ^(savings|saving)$ ]]; then
    jq -c '{monthKey, monthLabel, savings}' <<<"$summary_json"
  else
    printf '%s\n' "$summary_json"
  fi
}

run_find_transactions() {
  local query="" limit="20" date_filter="" month_filter="" type_filter=""
  while (($#)); do
    case "$1" in
      --query) query="${2:-}"; shift 2 ;;
      --limit) limit="${2:-20}"; shift 2 ;;
      --date) date_filter="${2:-}"; shift 2 ;;
      --month) month_filter="${2:-}"; shift 2 ;;
      --type) type_filter="${2:-}"; shift 2 ;;
      *)
        if [[ -z "$query" ]]; then
          query="$1"
        elif [[ "$limit" == "20" ]]; then
          limit="$1"
        fi
        shift
        ;;
    esac
  done

  if [[ -n "$date_filter" ]]; then
    date_filter="$(normalize_date_arg "$date_filter")"
  fi

  local args=(--query "$query" --limit "$limit")
  if [[ -n "$date_filter" ]]; then args+=(--date "$date_filter"); fi
  if [[ -n "$month_filter" ]]; then args+=(--month "$month_filter"); fi
  if [[ -n "$type_filter" ]]; then args+=(--type "$type_filter"); fi

  bash "${SCRIPT_DIR}/find_transactions.sh" "${args[@]}"
}


subcommand="${1:-}"
if [[ -z "$subcommand" ]]; then
  echo "Usage: ./exec <script-name> [args...]"
  exit 1
fi
shift || true

case "$subcommand" in
  get_categories.sh)
    bash "${SCRIPT_DIR}/get_categories.sh" "$@"
    ;;
  log.sh|log_natural.sh|preview_expense.sh)
    run_log "$@"
    ;;
  learn_category_alias.sh)
    run_learn_category_alias "$@"
    ;;
  conversation_bridge.sh|budget_conversation.sh)
    run_conversation_bridge "$@"
    ;;
  write_expense.sh|log_expense.sh)
    run_write "$@"
    ;;
  find_expenses.sh|search_expenses.sh|query_expenses.sh)
    run_find "$@"
    ;;
  update_expense.sh|edit_expense.sh)
    run_update "$@"
    ;;
  delete_expense.sh)
    run_delete "$@"
    ;;
  write_income.sh|log_income.sh)
    run_write_income "$@"
    ;;
  find_income.sh|search_income.sh|query_income.sh)
    run_find_income "$@"
    ;;
  update_income.sh|edit_income.sh)
    run_update_income "$@"
    ;;
  delete_income.sh)
    run_delete_income "$@"
    ;;
  find_recurring.sh|search_recurring.sh|query_recurring.sh|list_recurring.sh|list_subscriptions.sh|check_recurring.sh|check_subscriptions.sh)
    run_find_recurring "$@"
    ;;
  write_recurring.sh|add_recurring.sh|log_recurring.sh|add_subscription.sh|create_subscription.sh|log_subscription.sh)
    run_write_recurring "$@"
    ;;
  update_recurring.sh|edit_recurring.sh|update_subscription.sh|edit_subscription.sh)
    run_update_recurring "$@"
    ;;
  delete_recurring.sh|remove_recurring.sh|delete_subscription.sh|remove_subscription.sh)
    run_delete_recurring "$@"
    ;;
  find_summary.sh|monthly_totals.sh|summary.sh|income_summary.sh|expense_summary.sh|month_summary.sh|income_this_month.sh|spending_this_month.sh|savings_this_month.sh)
    run_find_summary "$@"
    ;;
  find_transactions.sh|query_transactions.sh|check_transactions.sh|list_transactions.sh)
    run_find_transactions "$@"
    ;;
  *)
    echo "Unsupported simplify-budget wrapper command: ${subcommand}"
    exit 1
    ;;
esac
