#!/usr/bin/env bash
# Natural-language expense logger.
# Takes the user's literal message as a single argument and parses it.
# Usage: log.sh "i bought a pencil for 10 euro under business category"
# Optional: --date YYYY-MM-DD --account <account> --category <category> --preview
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: log.sh \"<user message>\" [--date YYYY-MM-DD] [--account <account>] [--category <category>] [--preview]" >&2
  exit 1
fi

DATE_OVERRIDE=""
ACCOUNT_OVERRIDE=""
CATEGORY_OVERRIDE=""
PREVIEW_ONLY="0"
SKIP_DUP_CHECK="0"
MESSAGE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --preview) PREVIEW_ONLY="1"; shift ;;
    --skip-duplicate-check) SKIP_DUP_CHECK="1"; shift ;;
    --date) DATE_OVERRIDE="$2"; shift 2 ;;
    --account) ACCOUNT_OVERRIDE="$2"; shift 2 ;;
    --category) CATEGORY_OVERRIDE="$2"; shift 2 ;;
    --)
      shift
      if [[ $# -gt 0 ]]; then
        MESSAGE="$1"
        shift
      fi
      ;;
    *)
      if [[ -z "$MESSAGE" ]]; then
        MESSAGE="$1"
        shift
      else
        echo "Unknown argument: $1" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$MESSAGE" ]]; then
  echo "Error: missing expense message" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LEARNED_ALIAS_FILE="${SCRIPT_DIR}/../data/learned_category_aliases.json"

PARSED="$(
python3 - "$MESSAGE" "$CATEGORY_OVERRIDE" "$LEARNED_ALIAS_FILE" <<'PY'
import json
import os
import re
import sys

msg = sys.argv[1]
category_override = sys.argv[2].strip()
learned_alias_file = sys.argv[3]
lower = msg.lower()

CURRENCY_WORDS = [
    "rm",
    "euros", "euro", "eur",
    "dollars", "dollar", "usd",
    "pounds", "pound", "gbp", "sterling",
    "ringgit", "myr",
    "yen", "jpy",
    "rupees", "rupee", "inr",
    "baht", "thb",
    "rupiah", "idr",
    "francs", "franc", "chf",
    "yuan", "rmb", "cny",
    "lira", "try",
    "sgd", "aud", "cad", "nzd", "hkd",
]

amount_str = None
amount_match_span = None

m = re.search(r'([€£¥$])\s*(\d+(?:[.,]\d+)?)', msg)
if m:
    amount_str = f"{m.group(1)}{m.group(2)}"
    amount_match_span = m.span()

if not amount_str:
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*([€£¥$])', msg)
    if m:
        amount_str = f"{m.group(1)}{m.group(2)}"
        amount_match_span = m.span()

if not amount_str:
    m = re.search(r'\b(rm|myr|usd|eur|gbp|sgd|aud|cad|jpy|cny|thb|idr|inr|chf|hkd|nzd|try)\s*(\d+(?:[.,]\d+)?)\b', lower)
    if m:
        amount_str = msg[m.start():m.end()].strip()
        amount_match_span = m.span()

if not amount_str:
    word_alt = "|".join(CURRENCY_WORDS)
    m = re.search(rf'(\d+(?:[.,]\d+)?)\s*({word_alt})\b', lower)
    if m:
        amount_str = f"{m.group(1)} {m.group(2)}"
        amount_match_span = m.span()

if not amount_str:
    word_alt = "|".join(CURRENCY_WORDS)
    m = re.search(rf'\b({word_alt})\s*(\d+(?:[.,]\d+)?)', lower)
    if m:
        amount_str = f"{m.group(2)} {m.group(1)}"
        amount_match_span = m.span()

if not amount_str:
    m = re.search(r'(\d+(?:[.,]\d+)?)', msg)
    if m:
        amount_str = m.group(1)
        amount_match_span = m.span()

if not amount_str:
    print(json.dumps({"error": "could not find an amount in the message"}))
    raise SystemExit(0)

CATEGORY_ALIASES = {
    "Housing": ["housing", "rent", "mortgage", "apartment", "flat", "condo", "landlord", "lease", "property tax", "hoa", "accommodation"],
    "Transport": ["transport", "transportation", "uber", "taxi", "bus", "metro", "subway", "tram", "train", "petrol", "fuel", "gas station", "parking", "toll", "car wash", "grab", "lyft", "commute", "ride"],
    "Groceries": ["grocery", "groceries", "supermarket", "market", "tesco", "lidl", "aldi", "carrefour", "hypermarket", "minimarket", "produce", "butcher", "vegetable", "vegetables", "fruit", "fruits"],
    "Dining Out": ["dining out", "dining", "restaurant", "cafe", "café", "coffee", "pizza", "mcdonald", "mcdonalds", "kfc", "starbucks", "wolt", "glovo", "deliveroo", "takeaway", "takeout", "lunch", "dinner", "breakfast", "brunch", "fast food", "burger", "sushi", "noodles"],
    "Personal Care": ["personal care", "haircut", "salon", "barber", "spa", "skincare", "cosmetics", "beauty", "nails", "waxing", "massage"],
    "Shopping": ["shopping", "electronics", "amazon", "ikea", "furniture", "appliance", "gadget", "retail", "mall"],
    "Utilities": ["utilities", "utility", "electricity", "water bill", "internet", "broadband", "phone bill", "mobile plan", "gas bill", "netflix", "spotify", "disney", "streaming", "subscription"],
    "Fun": ["fun", "movie", "cinema", "concert", "bowling", "bar", "pub", "club", "night out", "show", "karaoke", "amusement", "entertainment"],
    "Business": ["business", "work expense", "office supply", "office", "software tool", "domain", "hosting", "cloud service", "aws", "coworking", "freelance", "client meeting", "business travel"],
    "Other": ["other", "misc", "miscellaneous"],
    "Donation": ["donation", "charity", "sadaqah", "mosque", "food bank"],
    "Childcare": ["childcare", "daycare", "nursery", "school fees", "tuition", "kindergarten", "preschool", "nanny", "babysitter"],
    "Travel": ["travel", "flight", "hotel", "airbnb", "vacation", "holiday", "trip", "visa fee"],
    "Zakat": ["zakat"],
    "Debt Payment": ["debt payment", "debt", "loan", "installment", "credit card payment", "emi"],
    "Fitness": ["fitness", "gym", "yoga", "pilates", "crossfit", "personal trainer", "workout"],
    "Family Support": ["family support", "remittance"],
    "Taxes": ["taxes", "tax", "vat", "council tax"],
    "Maintenance": ["maintenance", "repair", "plumber", "electrician", "handyman", "appliance repair", "car repair"],
    "Painting": ["painting", "paint", "wall paint", "decorating"],
    "TestGround": ["testground", "test entry", "dummy entry"],
    "Learning": ["learning", "ebook", "book", "course", "udemy", "coursera", "class", "training", "tutorial"],
    "Sports": ["sports", "football", "basketball", "tennis", "swimming", "cycling"],
    "Pet": ["pet", "vet", "veterinary"],
    "Gifts": ["gifts", "gift", "present"],
    "Special Occasions": ["special occasions", "special occasion", "birthday party", "wedding", "anniversary event", "graduation"],
    "Dress": ["dress", "clothes", "clothing", "shirt", "shoes", "bag", "handbag", "jacket", "outfit", "fashion", "zara", "uniqlo"],
    "Hobby": ["hobby", "craft", "photography gear", "gaming", "musical instrument", "art supply"],
    "Insurance": ["insurance"],
    "Medical": ["medical", "doctor", "hospital", "clinic", "pharmacy", "medicine", "prescription", "dental", "dentist", "health checkup"],
}

if os.path.exists(learned_alias_file):
    try:
        with open(learned_alias_file, "r", encoding="utf-8") as f:
            learned = json.load(f)
        if isinstance(learned, dict):
            for cat_name, aliases in learned.items():
                if cat_name in CATEGORY_ALIASES and isinstance(aliases, list):
                    for alias in aliases:
                        if isinstance(alias, str) and alias.strip():
                            CATEGORY_ALIASES[cat_name].append(alias.strip().lower())
    except Exception:
        pass

flat_aliases = []
BUILTIN_ALIAS_SET = set()
if os.path.exists(learned_alias_file):
    try:
        with open(learned_alias_file, "r", encoding="utf-8") as f:
            learned = json.load(f)
    except Exception:
        learned = {}
else:
    learned = {}

LEARNED_ALIAS_SET = set()
if isinstance(learned, dict):
    for aliases in learned.values():
        if isinstance(aliases, list):
            for alias in aliases:
                if isinstance(alias, str) and alias.strip():
                    LEARNED_ALIAS_SET.add(alias.strip().lower())

for cat_name, aliases in CATEGORY_ALIASES.items():
    for alias in aliases:
        flat_aliases.append((alias, cat_name))
        if alias not in LEARNED_ALIAS_SET:
            BUILTIN_ALIAS_SET.add(alias)
flat_aliases.sort(key=lambda item: -len(item[0]))

category = None
category_alias_hit = None
explicit_category = False
category_source = "none"
EXPLICIT_CATEGORY_ALIASES = {
    "Housing": ["housing"],
    "Transport": ["transport"],
    "Groceries": ["groceries", "grocery"],
    "Dining Out": ["dining out", "dining"],
    "Personal Care": ["personal care"],
    "Shopping": ["shopping"],
    "Utilities": ["utilities", "utility"],
    "Fun": ["fun"],
    "Business": ["business"],
    "Other": ["other"],
    "Donation": ["donation", "charity"],
    "Childcare": ["childcare"],
    "Travel": ["travel"],
    "Zakat": ["zakat"],
    "Debt Payment": ["debt payment", "debt"],
    "Fitness": ["fitness"],
    "Family Support": ["family support"],
    "Taxes": ["taxes", "tax"],
    "Maintenance": ["maintenance"],
    "Painting": ["painting"],
    "TestGround": ["testground"],
    "Learning": ["learning"],
    "Sports": ["sports"],
    "Pet": ["pet"],
    "Gifts": ["gifts", "gift"],
    "Special Occasions": ["special occasions", "special occasion"],
    "Dress": ["dress", "clothes", "clothing"],
    "Hobby": ["hobby"],
    "Insurance": ["insurance"],
    "Medical": ["medical"],
}

def normalize_override(raw):
    text = raw.strip().lower()
    text = re.sub(r'=zategory\d+\s*', '', text)
    text = re.sub(r'[\W_]+', ' ', text, flags=re.UNICODE)
    return " ".join(text.split())

if category_override:
    override = normalize_override(category_override)
    for cat_name, aliases in EXPLICIT_CATEGORY_ALIASES.items():
        normalized_aliases = [normalize_override(alias) for alias in aliases]
        if override == normalize_override(cat_name) or override in normalized_aliases:
            category = cat_name
            category_alias_hit = override
            explicit_category = True
            category_source = "explicit"
            break
    if not category:
        print(json.dumps({"error": f"unknown category override: {category_override}"}))
        raise SystemExit(0)

explicit_prep_patterns = [
    r'\bunder\s+([a-z][a-z\s]*?)(?:\s+category)?\b',
    r'\bto\s+([a-z][a-z\s]*?)\s+category\b',
    r'\binto\s+([a-z][a-z\s]*?)\s+category\b',
    r'\bin\s+([a-z][a-z\s]*?)\s+category\b',
    r'\bas\s+([a-z][a-z\s]*?)(?:\s+category)?\b',
    r'\bcategory\s*[:\-]?\s*([a-z][a-z\s]+?)\b',
]

if not category:
    for pat in explicit_prep_patterns:
        for match in re.finditer(pat, lower):
            candidate = match.group(1).strip()
            if not candidate:
                continue
            words = candidate.split()
            for i in range(len(words), 0, -1):
                probe = " ".join(words[:i])
                for cat_name, aliases in EXPLICIT_CATEGORY_ALIASES.items():
                    if probe == cat_name.lower() or probe in aliases:
                        category = cat_name
                        category_alias_hit = probe
                        explicit_category = True
                        category_source = "explicit"
                        break
                if category:
                    break
            if category:
                break
        if category:
            break

if not category:
    for cat_name, aliases in EXPLICIT_CATEGORY_ALIASES.items():
        for alias in aliases:
            if re.search(rf'\b{re.escape(alias)}\b', lower):
                category = cat_name
                category_alias_hit = alias
                explicit_category = True
                category_source = "explicit"
                break
        if category:
            break

if not category:
    for alias, cat_name in flat_aliases:
        if re.search(rf'\b{re.escape(alias)}\b', lower):
            category = cat_name
            category_alias_hit = alias
            category_source = "learned" if alias in LEARNED_ALIAS_SET else "builtin"
            break

if not category:
    category = "Other"

desc = msg
if amount_match_span:
    desc = desc[:amount_match_span[0]] + " " + desc[amount_match_span[1]:]

desc = re.sub(r'\d+(?:[.,]\d+)?', ' ', desc)
for word in CURRENCY_WORDS:
    desc = re.sub(rf'\b{re.escape(word)}\b', ' ', desc, flags=re.IGNORECASE)
for symbol in ["€", "£", "¥", "$"]:
    desc = desc.replace(symbol, " ")

if category_alias_hit:
    for prep in ["under", "to", "into", "in", "as", "for"]:
        desc = re.sub(rf'\b{prep}\s+{re.escape(category_alias_hit)}\s*category\b', ' ', desc, flags=re.IGNORECASE)
        desc = re.sub(rf'\b{prep}\s+{re.escape(category_alias_hit)}\b', ' ', desc, flags=re.IGNORECASE)
    desc = re.sub(rf'\b{re.escape(category_alias_hit)}\s*category\b', ' ', desc, flags=re.IGNORECASE)
    desc = re.sub(rf'\b(?:under|to|into|in|as|for)\s+{re.escape(category_alias_hit)}\b', ' ', desc, flags=re.IGNORECASE)

desc = re.sub(r'\bcategory\b', ' ', desc, flags=re.IGNORECASE)
desc = re.sub(r'\bfo\b', ' ', desc, flags=re.IGNORECASE)

fillers = {
    "i", "we", "you", "he", "she", "they",
    "bought", "buy", "buying", "paid", "pay", "paying", "spent", "spend", "spending",
    "log", "logged", "logging", "record", "track",
    "please", "pls", "the", "a", "an", "some", "to", "for", "of", "on", "at", "in", "with", "from",
    "and", "also", "just", "want", "wants", "wanted", "need", "needs", "needed",
    "can", "could", "would", "should", "will", "gonna",
    "it", "this", "that", "these", "those", "my", "our", "your", "me", "us", "them",
    "expense", "expenses", "purchase", "purchased", "order", "ordered",
    "is", "was", "were", "be", "been", "being",
    "got", "get",
    "today", "yesterday", "tomorrow", "now",
}

tokens = re.split(r'\s+', desc.strip())
tokens = [t for t in tokens if t and t.lower().strip(".,!?") not in fillers and t.strip(".,!?")]
desc = " ".join(tokens).strip(" .,!?-")
if not desc:
    desc = "expense"

CATEGORY_EMOJIS = {
    "Housing": "🏡", "Transport": "🚙", "Groceries": "🍎", "Dining Out": "🍕",
    "Personal Care": "❤️", "Shopping": "🛍️", "Utilities": "💡", "Fun": "🎬",
    "Business": "💻️", "Other": "❓", "Donation": "🕌", "Childcare": "🐣",
    "Travel": "✈️", "Zakat": "🌟", "Debt Payment": "💸", "Fitness": "💪",
    "Family Support": "🏘️", "Taxes": "💵", "Maintenance": "🧰", "Painting": "🎨",
    "TestGround": "🤖", "Learning": "📚", "Sports": "🏀", "Pet": "🐶",
    "Gifts": "🎁", "Special Occasions": "🥰", "Dress": "👚", "Hobby": "🪂",
    "Insurance": "🛡️", "Medical": "🩺",
}
emoji = CATEGORY_EMOJIS.get(category, "")
cat_display = f"{category} {emoji}".strip()

if category_source in ("builtin", "learned", "explicit"):
    question = f"Log *{desc}* under {cat_display}?"
else:
    question = f"Log *{desc}* under {cat_display}? (best guess — reply yes or give me the right category)"

print(json.dumps({
    "amount": amount_str,
    "description": desc,
    "category": category,
    "explicitCategory": explicit_category,
    "categorySource": category_source,
    "question": question,
}))
PY
)"

ERROR="$(echo "$PARSED" | jq -r '.error // empty')"
if [ -n "$ERROR" ]; then
  echo "Error: $ERROR" >&2
  exit 1
fi

AMOUNT="$(echo "$PARSED" | jq -r '.amount')"
DESCRIPTION="$(echo "$PARSED" | jq -r '.description')"
CATEGORY="$(echo "$PARSED" | jq -r '.category // empty')"
EXPLICIT_CATEGORY="$(echo "$PARSED" | jq -r '.explicitCategory')"

if [[ "$PREVIEW_ONLY" == "1" ]]; then
  echo "$PARSED"
  exit 0
fi

if [[ "$EXPLICIT_CATEGORY" != "true" ]]; then
  echo "Error: category not explicitly confirmed; run with --preview first or pass --category" >&2
  exit 1
fi

DATE_ARG="${DATE_OVERRIDE:-$(date +%Y-%m-%d)}"
ACCOUNT_ARG="${ACCOUNT_OVERRIDE:-Revolut}"

if [[ "$SKIP_DUP_CHECK" != "1" ]]; then
  DUP_JSON="$(bash "$SCRIPT_DIR/find_expenses.sh" --date "$DATE_ARG" --description "$DESCRIPTION" --limit 5 2>/dev/null || echo '[]')"
  DUP_COUNT="$(printf '%s' "$DUP_JSON" | python3 -c 'import json,sys; print(len(json.loads(sys.stdin.read())))')"
  if [[ "$DUP_COUNT" -gt 0 ]]; then
    echo "DUPLICATE_FOUND: \"${DESCRIPTION}\" may already be logged for ${DATE_ARG}. Run with --skip-duplicate-check to log anyway."
    exit 0
  fi
fi

bash "$SCRIPT_DIR/write_expense.sh" \
  --amount "$AMOUNT" \
  --description "$DESCRIPTION" \
  --category "$CATEGORY" \
  --date "$DATE_ARG" \
  --account "$ACCOUNT_ARG"
