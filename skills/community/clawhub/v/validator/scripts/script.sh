#!/usr/bin/env bash
# validator — Input validator
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail
VERSION="3.0.1"

BOLD='\033[1m'; GREEN='\033[0;32m'; RED='\033[0;31m'; RESET='\033[0m'
pass() { echo -e "  ${GREEN}✓ VALID${RESET} $1"; }
fail() { echo -e "  ${RED}✗ INVALID${RESET} $1"; }

cmd_email() {
    local addr="${1:?Usage: validator email <address>}"
    if echo "$addr" | grep -qE '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'; then
        pass "$addr"
    else
        fail "$addr — must be user@domain.tld"
        return 1
    fi
}

cmd_url() {
    local url="${1:?Usage: validator url <url>}"
    if echo "$url" | grep -qE '^https?://[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})(:[0-9]+)?(/.*)?$'; then
        pass "$url"
        if command -v curl >/dev/null 2>&1; then
            local code
            code=$(curl -sL -o /dev/null -w '%{http_code}' --max-time 5 "$url" 2>/dev/null || echo "000")
            echo "  HTTP status: $code"
        fi
    else
        fail "$url — must start with http:// or https://"
        return 1
    fi
}

cmd_ip() {
    local addr="${1:?Usage: validator ip <address>}"
    # IPv4
    if echo "$addr" | grep -qE '^([0-9]{1,3}\.){3}[0-9]{1,3}$'; then
        local valid=true
        IFS='.' read -ra octets <<< "$addr"
        for o in "${octets[@]}"; do
            if [ "$o" -gt 255 ] 2>/dev/null; then valid=false; fi
        done
        if $valid; then
            pass "$addr (IPv4)"
            # Check type
            case "$addr" in
                10.*|172.1[6-9].*|172.2[0-9].*|172.3[0-1].*|192.168.*) echo "  Type: Private" ;;
                127.*) echo "  Type: Loopback" ;;
                0.*) echo "  Type: Reserved" ;;
                *) echo "  Type: Public" ;;
            esac
        else
            fail "$addr — octets must be 0-255"
            return 1
        fi
    # IPv6
    elif echo "$addr" | grep -qE '^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$'; then
        pass "$addr (IPv6)"
    else
        fail "$addr — not a valid IPv4 or IPv6 address"
        return 1
    fi
}

cmd_phone() {
    local num="${1:?Usage: validator phone <number>}"
    local clean
    clean=$(echo "$num" | tr -d ' ()-.')
    if echo "$clean" | grep -qE '^\+?[0-9]{7,15}$'; then
        pass "$num (digits: ${#clean})"
    else
        fail "$num — 7-15 digits expected"
        return 1
    fi
}

cmd_date() {
    local str="${1:?Usage: validator date <date-string>}"
    if date -d "$str" >/dev/null 2>&1; then
        local parsed
        parsed=$(date -d "$str" '+%Y-%m-%d %H:%M:%S')
        pass "$str → $parsed"
    else
        fail "$str — cannot parse as date"
        return 1
    fi
}

cmd_json() {
    local file="${1:?Usage: validator json <file>}"
    [ ! -f "$file" ] && { fail "File not found: $file"; return 1; }
    if python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
        local size
        size=$(wc -c < "$file")
        pass "$file (${size} bytes, valid JSON)"
    else
        fail "$file"
        python3 -c "
import json
try:
    json.load(open('$file'))
except json.JSONDecodeError as e:
    print('  Error: line {}, col {}: {}'.format(e.lineno, e.colno, e.msg))
" 2>/dev/null
        return 1
    fi
}

cmd_yaml() {
    local file="${1:?Usage: validator yaml <file>}"
    [ ! -f "$file" ] && { fail "File not found: $file"; return 1; }
    if python3 -c "
import sys
try:
    import yaml
    yaml.safe_load(open('$file'))
    sys.exit(0)
except ImportError:
    # Fallback: basic syntax check
    with open('$file') as f:
        for i, line in enumerate(f, 1):
            if '\t' in line:
                print('  Warning: tab character on line {}'.format(i))
    sys.exit(0)
except yaml.YAMLError as e:
    print('  Error: {}'.format(e))
    sys.exit(1)
" 2>/dev/null; then
        pass "$file (valid YAML)"
    else
        fail "$file"
        return 1
    fi
}

cmd_csv() {
    local file="${1:?Usage: validator csv <file>}"
    [ ! -f "$file" ] && { fail "File not found: $file"; return 1; }
    FILE="$file" python3 << 'PYEOF'
import csv, os, sys
f = os.environ["FILE"]
errors = []
cols = None
with open(f) as fh:
    reader = csv.reader(fh)
    for i, row in enumerate(reader, 1):
        if cols is None:
            cols = len(row)
        elif len(row) != cols:
            errors.append("Line {}: {} columns (expected {})".format(i, len(row), cols))
        if i > 10000:
            break

if errors:
    print("  \033[0;31m\u2717 INVALID\033[0m {} ({} errors)".format(f, len(errors)))
    for e in errors[:5]:
        print("  " + e)
    sys.exit(1)
else:
    print("  \033[0;32m\u2713 VALID\033[0m {} ({} rows, {} columns)".format(f, i, cols or 0))
PYEOF
}

cmd_domain() {
    local name="${1:?Usage: validator domain <domain>}"
    if echo "$name" | grep -qE '^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'; then
        pass "$name (format OK)"
        if command -v dig >/dev/null 2>&1; then
            local ip
            ip=$(dig +short "$name" A 2>/dev/null | head -1)
            if [ -n "$ip" ]; then
                echo "  DNS: $ip"
            else
                echo "  DNS: No A record found"
            fi
        fi
    else
        fail "$name — invalid domain format"
        return 1
    fi
}

cmd_credit_card() {
    local num="${1:?Usage: validator credit-card <number>}"
    local clean
    clean=$(echo "$num" | tr -d ' -')
    NUM="$clean" python3 << 'PYEOF'
import os, sys
num = os.environ["NUM"]
if not num.isdigit() or len(num) < 13 or len(num) > 19:
    print("  \033[0;31m\u2717 INVALID\033[0m — must be 13-19 digits")
    sys.exit(1)

# Luhn algorithm
digits = [int(d) for d in num]
digits.reverse()
total = 0
for i, d in enumerate(digits):
    if i % 2 == 1:
        d *= 2
        if d > 9:
            d -= 9
    total += d

if total % 10 == 0:
    # Detect card type
    card_type = "Unknown"
    if num[0] == '4':
        card_type = "Visa"
    elif num[:2] in ('51','52','53','54','55'):
        card_type = "MasterCard"
    elif num[:2] in ('34','37'):
        card_type = "Amex"
    elif num[:4] == '6011' or num[:2] == '65':
        card_type = "Discover"
    elif num[:2] == '35':
        card_type = "JCB"
    print("  \033[0;32m\u2713 VALID\033[0m Luhn check passed ({})".format(card_type))
else:
    print("  \033[0;31m\u2717 INVALID\033[0m Luhn check failed")
    sys.exit(1)
PYEOF
}

show_help() {
    cat << EOF
validator v$VERSION — Input validator

Usage: validator <command> <input>

Formats:
  email <address>         Validate email format
  url <url>               Validate URL (+ HTTP check if curl available)
  ip <address>            Validate IPv4/IPv6 address
  phone <number>          Validate phone number (7-15 digits)
  date <string>           Validate and parse date string
  domain <name>           Validate domain (+ DNS lookup if dig available)
  credit-card <number>    Luhn algorithm check + card type detection

Files:
  json <file>             Validate JSON syntax
  yaml <file>             Validate YAML syntax
  csv <file>              Validate CSV structure (column consistency)

  help                    Show this help
  version                 Show version

Requires: python3 (for json/csv/credit-card). Optional: curl, dig
EOF
}

[ $# -eq 0 ] && { show_help; exit 0; }
case "$1" in
    email)       shift; cmd_email "$@" ;;
    url)         shift; cmd_url "$@" ;;
    ip)          shift; cmd_ip "$@" ;;
    phone)       shift; cmd_phone "$@" ;;
    date)        shift; cmd_date "$@" ;;
    json)        shift; cmd_json "$@" ;;
    yaml)        shift; cmd_yaml "$@" ;;
    csv)         shift; cmd_csv "$@" ;;
    domain)      shift; cmd_domain "$@" ;;
    credit-card) shift; cmd_credit_card "$@" ;;
    help|-h)     show_help ;;
    version|-v)  echo "validator v$VERSION"; echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com" ;;
    *)           echo "Unknown: $1"; show_help; exit 1 ;;
esac
