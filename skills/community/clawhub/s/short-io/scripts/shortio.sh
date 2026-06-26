#!/usr/bin/env bash
# shortio.sh — Short.io link management helper
# Usage: shortio.sh <command> [options]

set -euo pipefail

# Secrets file: override with SHORTIO_SECRETS_FILE env var, or defaults to ~/.secrets/shortio.env
SECRETS_FILE="${SHORTIO_SECRETS_FILE:-${HOME}/.secrets/shortio.env}"
API_BASE="https://api.short.io"
STATS_BASE="https://statistics.short.io"

# ── Colour output ──────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[short.io]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }
die()   { err "$*"; exit 1; }

# ── Load API key ───────────────────────────────────────────────────
load_key() {
  if [[ -f "$SECRETS_FILE" ]]; then
    # shellcheck source=/dev/null
    source "$SECRETS_FILE"
  fi
  if [[ -z "${SHORT_IO_API_KEY:-}" ]]; then
    die "SHORT_IO_API_KEY not set. Add it to $SECRETS_FILE:\n  SHORT_IO_API_KEY=your_key_here"
  fi
}

# ── Shared curl wrapper ────────────────────────────────────────────
api_get() {
  local url="$1"
  curl -sf "$url" \
    -H "authorization: ${SHORT_IO_API_KEY}" \
    -H "accept: application/json"
}

api_post() {
  local url="$1"
  local body="$2"
  curl -sf -X POST "$url" \
    -H "authorization: ${SHORT_IO_API_KEY}" \
    -H "content-type: application/json" \
    -H "accept: application/json" \
    -d "$body"
}

api_delete() {
  local url="$1"
  curl -sf -X DELETE "$url" \
    -H "authorization: ${SHORT_IO_API_KEY}" \
    -H "accept: application/json"
}

# ── Commands ───────────────────────────────────────────────────────

cmd_domains() {
  # List all domains
  info "Fetching domains..."
  api_get "${API_BASE}/api/domains" | jq -r '
    .[] | "\(.id)\t\(.hostname)"
  ' | column -t -s $'\t' -N "DOMAIN_ID,HOSTNAME"
}

cmd_list() {
  # List links for a domain
  # Usage: list --domain-id <id> [--limit <n>]
  local domain_id="" limit=50

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --domain-id) domain_id="$2"; shift 2 ;;
      --limit)     limit="$2";     shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done

  [[ -z "$domain_id" ]] && die "Required: --domain-id <id>\n  Tip: run 'domains' command to find your domain ID"

  info "Listing links for domain ${domain_id} (limit: ${limit})..."
  api_get "${API_BASE}/api/links?domain_id=${domain_id}&limit=${limit}" | jq -r '
    .links[] | "\(.id)\t\(.shortURL)\t\(.originalURL | .[0:60])\t\(.clicks // 0) clicks"
  ' | column -t -s $'\t' -N "LINK_ID,SHORT_URL,ORIGINAL_URL,CLICKS"
}

cmd_get() {
  # Get link details by ID
  # Usage: get --link-id <id>
  local link_id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --link-id) link_id="$2"; shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done

  [[ -z "$link_id" ]] && die "Required: --link-id <id>"

  info "Fetching link ${link_id}..."
  api_get "${API_BASE}/links/${link_id}" | jq '{
    id,
    shortURL,
    path,
    domain,
    originalURL,
    title,
    clicks,
    createdAt,
    tags
  }'
}

cmd_create() {
  # Create a short link
  # Usage: create --domain <hostname> --url <originalURL> [--path <slug>] [--title <title>] [--tags <tag1,tag2>]
  local domain="" url="" path="" title="" tags_raw=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --domain) domain="$2"; shift 2 ;;
      --url)    url="$2";    shift 2 ;;
      --path)   path="$2";   shift 2 ;;
      --title)  title="$2";  shift 2 ;;
      --tags)   tags_raw="$2"; shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done

  [[ -z "$domain" ]] && die "Required: --domain <hostname>"
  [[ -z "$url" ]]    && die "Required: --url <originalURL>"

  # Build JSON body using jq for safe escaping
  local body
  body=$(jq -n \
    --arg domain "$domain" \
    --arg url "$url" \
    --arg path "$path" \
    --arg title "$title" \
    '{
      domain: $domain,
      originalURL: $url,
      path: (if $path != "" then $path else null end),
      title: (if $title != "" then $title else null end)
    } | del(.[] | nulls)')

  # Append tags array if provided
  if [[ -n "$tags_raw" ]]; then
    local tags_json
    tags_json=$(echo "$tags_raw" | tr ',' '\n' | jq -R . | jq -s .)
    body=$(echo "$body" | jq --argjson tags "$tags_json" '. + {tags: $tags}')
  fi

  info "Creating short link..."
  local result
  result=$(api_post "${API_BASE}/links" "$body")

  local short_url
  short_url=$(echo "$result" | jq -r '.shortURL')
  ok "Short link created: ${short_url}"

  echo "$result" | jq '{id, shortURL, path, domain, originalURL, title, clicks, createdAt}'
}

cmd_delete() {
  # Delete a link by ID
  # Usage: delete --link-id <id>
  local link_id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --link-id) link_id="$2"; shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done

  [[ -z "$link_id" ]] && die "Required: --link-id <id>"

  info "Deleting link ${link_id}..."
  api_delete "${API_BASE}/links/${link_id}"
  ok "Link ${link_id} deleted."
}

cmd_stats() {
  # Get stats for a link or domain
  # Usage: stats --link-id <id>
  #        stats --domain-id <id>
  local link_id="" domain_id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --link-id)   link_id="$2";   shift 2 ;;
      --domain-id) domain_id="$2"; shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done

  if [[ -n "$link_id" ]]; then
    info "Fetching stats for link ${link_id}..."
    api_get "${STATS_BASE}/link/${link_id}" | jq .
  elif [[ -n "$domain_id" ]]; then
    info "Fetching stats for domain ${domain_id}..."
    api_get "${STATS_BASE}/domain/${domain_id}" | jq .
  else
    die "Required: --link-id <id> or --domain-id <id>"
  fi
}

cmd_find() {
  # Find a link by original URL
  # Usage: find --domain <hostname> --url <originalURL>
  local domain="" url=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --domain) domain="$2"; shift 2 ;;
      --url)    url="$2";    shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done

  [[ -z "$domain" ]] && die "Required: --domain <hostname>"
  [[ -z "$url" ]]    && die "Required: --url <originalURL>"

  local encoded_url
  encoded_url=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$url', safe=''))" 2>/dev/null \
    || echo "$url" | sed 's|:|%3A|g; s|/|%2F|g')

  info "Searching for link to: ${url}"
  api_get "${API_BASE}/links/by-original-url?domain=${domain}&originalURL=${encoded_url}" | jq '{id, shortURL, path, originalURL, clicks}'
}

cmd_archive() {
  # Archive a link
  # Usage: archive --link-id <id>
  local link_id=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --link-id) link_id="$2"; shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done
  [[ -z "$link_id" ]] && die "Required: --link-id <id>"
  api_post "${API_BASE}/links/archive" "{\"linkId\": \"${link_id}\"}" | jq .
  ok "Link ${link_id} archived."
}

cmd_qr() {
  # Generate QR code for a link
  # Usage: qr --link-id <id> [--output <file.png>] [--size <pixels>]
  local link_id="" output="qr-code.png" size=300

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --link-id) link_id="$2"; shift 2 ;;
      --output)  output="$2";  shift 2 ;;
      --size)    size="$2";    shift 2 ;;
      *) die "Unknown option: $1" ;;
    esac
  done

  [[ -z "$link_id" ]] && die "Required: --link-id <id>"

  info "Generating QR code (${size}px) → ${output}"
  curl -sf -X POST "${API_BASE}/links/qr/${link_id}" \
    -H "authorization: ${SHORT_IO_API_KEY}" \
    -H "content-type: application/json" \
    -d "{\"size\": ${size}}" \
    -o "$output"
  ok "QR code saved to: ${output}"
}

# ── Help ───────────────────────────────────────────────────────────

usage() {
  cat <<EOF
Short.io Link Manager

USAGE:
  shortio.sh <command> [options]

COMMANDS:
  domains                          List all domains (shows domain IDs)
  list    --domain-id <id>         List links for a domain
          [--limit <n>]            Max results (default: 50)
  get     --link-id <id>           Get link details
  create  --domain <host>          Create a short link
          --url <originalURL>
          [--path <slug>]          Custom slug (auto-generated if omitted)
          [--title <title>]
          [--tags <t1,t2>]
  delete  --link-id <id>           Delete a link
  stats   --link-id <id>           Get link click stats
          --domain-id <id>         Get domain stats
  find    --domain <host>          Find link by original URL
          --url <originalURL>
  archive --link-id <id>           Archive a link
  qr      --link-id <id>           Generate QR code PNG
          [--output <file.png>]    Output file (default: qr-code.png)
          [--size <pixels>]        QR size in pixels (default: 300)

SETUP:
  Add your API key to $SECRETS_FILE:
    SHORT_IO_API_KEY=your_secret_key_here

EXAMPLES:
  shortio.sh domains
  shortio.sh list --domain-id 123456
  shortio.sh create --domain d4j.link --url https://example.com/long --path promo
  shortio.sh get --link-id abc123
  shortio.sh stats --link-id abc123
  shortio.sh delete --link-id abc123
  shortio.sh qr --link-id abc123 --output my-qr.png
EOF
}

# ── Main dispatcher ────────────────────────────────────────────────

main() {
  local cmd="${1:-help}"
  shift || true

  case "$cmd" in
    help|-h|--help) usage; exit 0 ;;
  esac

  load_key

  case "$cmd" in
    domains) cmd_domains "$@" ;;
    list)    cmd_list    "$@" ;;
    get)     cmd_get     "$@" ;;
    create)  cmd_create  "$@" ;;
    delete)  cmd_delete  "$@" ;;
    stats)   cmd_stats   "$@" ;;
    find)    cmd_find    "$@" ;;
    archive) cmd_archive "$@" ;;
    qr)      cmd_qr      "$@" ;;
    *) err "Unknown command: ${cmd}"; echo; usage; exit 1 ;;
  esac
}

main "$@"
