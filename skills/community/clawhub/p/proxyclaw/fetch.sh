#!/usr/bin/env bash
set -euo pipefail

# ProxyClaw fetch — route requests through IPLoop residential proxies
# Usage: ./fetch.sh <URL> [--country CC] [--city CITY] [--session ID] [--asn ASN] [--format raw|markdown] [--timeout N]

URL=""
COUNTRY=""
CITY=""
SESSION_ID=""
ASN=""
FORMAT="raw"
TIMEOUT=30

# ── Input parsing ──
while [[ $# -gt 0 ]]; do
  case "$1" in
    --country)  COUNTRY="$2";    shift 2 ;;
    --city)     CITY="$2";       shift 2 ;;
    --session)  SESSION_ID="$2"; shift 2 ;;
    --asn)      ASN="$2";        shift 2 ;;
    --format)   FORMAT="$2";     shift 2 ;;
    --timeout)  TIMEOUT="$2";    shift 2 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) URL="$1"; shift ;;
  esac
done

if [ -z "$URL" ]; then
  echo "Usage: ./fetch.sh <URL> [--country CC] [--city CITY] [--session ID] [--asn ASN] [--format raw|markdown] [--timeout N]" >&2
  echo "" >&2
  echo "Examples:" >&2
  echo "  ./fetch.sh https://example.com" >&2
  echo "  ./fetch.sh https://example.com --country US --format markdown" >&2
  echo "  ./fetch.sh https://httpbin.org/ip --country DE" >&2
  echo "  ./fetch.sh https://example.com --country US --city newyork" >&2
  echo "  ./fetch.sh https://example.com --session mysession" >&2
  echo "  ./fetch.sh https://example.com --asn 12345" >&2
  exit 1
fi

# ── Input validation ──
if [[ ! "$URL" =~ ^https?:// ]]; then
  echo "Error: URL must start with http:// or https://" >&2
  exit 1
fi

if [ -n "$COUNTRY" ]; then
  COUNTRY="${COUNTRY^^}"
  if [[ ! "$COUNTRY" =~ ^[A-Z]{2}$ ]]; then
    echo "Error: Country must be exactly 2 uppercase letters (e.g., US, DE, GB)" >&2
    exit 1
  fi
fi

if [[ ! "$TIMEOUT" =~ ^[0-9]+$ ]] || [ "$TIMEOUT" -lt 1 ] || [ "$TIMEOUT" -gt 120 ]; then
  echo "Error: Timeout must be 1-120 seconds" >&2
  exit 1
fi

if [[ "$FORMAT" != "raw" && "$FORMAT" != "markdown" ]]; then
  echo "Error: Format must be 'raw' or 'markdown'" >&2
  exit 1
fi

# ── API key check ──
if [ -z "${IPLOOP_API_KEY:-}" ]; then
  echo "Error: IPLOOP_API_KEY not set." >&2
  echo "Get your free key at https://iploop.io/signup.html" >&2
  echo "Then: export IPLOOP_API_KEY=\"your_key\"" >&2
  exit 1
fi

# ── Build proxy auth ──
AUTH="iploop:${IPLOOP_API_KEY}"
[ -n "$COUNTRY" ]    && AUTH="${AUTH}-country-${COUNTRY}"
[ -n "$CITY" ]       && AUTH="${AUTH}-city-${CITY}"
[ -n "$SESSION_ID" ] && AUTH="${AUTH}-session-${SESSION_ID}"
[ -n "$ASN" ]        && AUTH="${AUTH}-asn-${ASN}"

# ── Temp file with guaranteed cleanup ──
TMPFILE=$(mktemp)
trap 'rm -f "$TMPFILE"' EXIT

# ── Fetch ──
CURL_OUT=$(curl -s -o "$TMPFILE" -w "%{http_code} %{content_type}" \
  --max-time "$TIMEOUT" \
  --proxy "http://proxy.iploop.io:8880" \
  --proxy-user "$AUTH" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: en-US,en;q=0.9" \
  "$URL" 2>/dev/null) || {
  echo "Error: Request failed (timeout or connection error)" >&2
  exit 1
}

HTTP_CODE=$(echo "$CURL_OUT" | awk '{print $1}')
CONTENT_TYPE=$(echo "$CURL_OUT" | awk '{print $2}')

if [ "$HTTP_CODE" -ge 400 ]; then
  echo "Error: HTTP $HTTP_CODE from $URL" >&2
  cat "$TMPFILE" >&2
  exit 1
fi

CONTENT=$(cat "$TMPFILE")

# ── Output ──
if [ "$FORMAT" = "markdown" ]; then
  IS_HTML=false
  [[ "$CONTENT_TYPE" == *"text/html"* ]] && IS_HTML=true
  if [ "$IS_HTML" = false ] && echo "$CONTENT" | grep -qi '<html'; then
    IS_HTML=true
  fi

  if [ "$IS_HTML" = true ]; then
    # Convert HTML to markdown using node if available, otherwise basic strip
    if command -v node &>/dev/null; then
      echo "$CONTENT" | node -e "
        const c=[];
        process.stdin.on('data',d=>c.push(d));
        process.stdin.on('end',()=>{
          let h=Buffer.concat(c).toString();
          h=h.replace(/<script[\s\S]*?<\/script>/gi,'');
          h=h.replace(/<style[\s\S]*?<\/style>/gi,'');
          h=h.replace(/<br\s*\/?>/gi,'\n');
          h=h.replace(/<\/p>/gi,'\n\n');
          h=h.replace(/<\/h[1-6]>/gi,'\n\n');
          h=h.replace(/<\/li>/gi,'\n');
          h=h.replace(/<li[^>]*>/gi,'- ');
          h=h.replace(/<h([1-6])[^>]*>/gi,(m,n)=>'#'.repeat(+n)+' ');
          h=h.replace(/<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>([^<]*)<\/a>/gi,'[\$2](\$1)');
          h=h.replace(/<[^>]+>/g,'');
          h=h.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'\"').replace(/&#39;/g,\"'\").replace(/&nbsp;/g,' ');
          h=h.replace(/\n{3,}/g,'\n\n').trim();
          console.log(h);
        });"
    else
      # Fallback: basic HTML tag stripper
      echo "$CONTENT" \
        | sed -e '/<script/,/<\/script>/d' \
              -e '/<style/,/<\/style>/d' \
              -e 's/<[^>]*>//g' \
              -e '/^[[:space:]]*$/d' || true
    fi
  else
    echo "$CONTENT"
  fi
else
  echo "$CONTENT"
fi
