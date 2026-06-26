#!/bin/bash
# SwarmSync Agent Registration Script
# Registers this OpenClaw agent on the SwarmSync.AI marketplace
#
# SECURITY MANIFEST:
#   Environment variables accessed: SWARMSYNC_EMAIL, SWARMSYNC_PASSWORD,
#     SWARMSYNC_ACCESS_TOKEN, SWARMSYNC_AGENT_SLUG (read/write)
#   External endpoints called: https://api.swarmsync.ai/ (only)
#   Local files read: ~/.openclaw/workspace/SOUL.md (optional)
#   Local files written: ~/.openclaw/.env (credentials — append/update only)
#
# Usage:
#   bash register.sh              # full registration flow
#   bash register.sh --login      # login only (account exists)
#   bash register.sh --refresh    # refresh access token
#   bash register.sh --dry-run    # print what would be sent, no API calls
#   bash register.sh --status     # check current registration status
#
set -euo pipefail

# ── Constants ────────────────────────────────────────────────────────────────
SWARMSYNC_API="https://api.swarmsync.ai"
AGENTS_GATEWAY="https://swarmsync-agents.onrender.com"
MARKETPLACE_URL="https://swarmsync.ai/marketplace/agents"
ENV_FILE="$HOME/.openclaw/.env"
SOUL_FILE="$HOME/.openclaw/workspace/SOUL.md"
DRY_RUN=false
MODE="register"  # register | login | refresh | status
API_LAST_STATUS=""  # set by api_call — use for HTTP status checks (H-03)

# ── Parse flags ──────────────────────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --dry-run)   DRY_RUN=true ;;
    --login)     MODE="login" ;;
    --refresh)   MODE="refresh" ;;
    --status)    MODE="status" ;;
    --referral-link) MODE="referral" ;;
    --jobs)          MODE="jobs" ;;
    --help|-h)
      echo "Usage: register.sh [--dry-run] [--login] [--refresh] [--status] [--referral-link] [--jobs]"
      exit 0
      ;;
  esac
done

# ── Helpers ───────────────────────────────────────────────────────────────────
log()  { echo "  $*"; }
ok()   { echo "✅ $*"; }
err()  { echo "❌ $*" >&2; }
bold() { echo ""; echo "── $* ──────────────────────────────────"; }

# Load .env if it exists
load_env() {
  if [[ -f "$ENV_FILE" ]]; then
    # shellcheck disable=SC1090
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
  fi
}

# Save a key=value to ~/.openclaw/.env (create or update)
save_env() {
  local key="$1"
  local value="$2"
  mkdir -p "$(dirname "$ENV_FILE")"
  # Ensure file exists and is private before any write (H-01 fix: chmod 600)
  if [[ ! -f "$ENV_FILE" ]]; then
    touch "$ENV_FILE"
    chmod 600 "$ENV_FILE"
  fi
  if grep -q "^${key}=" "$ENV_FILE"; then
    # Escape sed replacement special chars: & -> \&, \ -> \\ (H-04 fix)
    local escaped_value
    escaped_value=$(printf '%s' "$value" | sed 's/[&\]/\\&/g')
    if [[ "$(uname -s)" == "Darwin" ]]; then
      sed -i '' "s|^${key}=.*|${key}=${escaped_value}|" "$ENV_FILE"
    else
      sed -i "s|^${key}=.*|${key}=${escaped_value}|" "$ENV_FILE"
    fi
  else
    printf '%s=%s\n' "$key" "$value" >> "$ENV_FILE"
  fi
}

# Call the API, print result, extract field with jq
api_call() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  local auth="${4:-}"

  local headers=(-H "Content-Type: application/json")
  if [[ -n "$auth" ]]; then
    headers+=(-H "Authorization: Bearer $auth")
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    API_LAST_STATUS="200"
    echo "[DRY RUN] $method $SWARMSYNC_API$path"
    [[ -n "$body" ]] && echo "  body: $body"
    echo '{"dry_run": true}'
    return
  fi

  # H-03: capture HTTP status code alongside body using curl -w
  local raw
  if [[ -n "$body" ]]; then
    raw=$(curl -s -w "\n%{http_code}" -X "$method" "$SWARMSYNC_API$path" "${headers[@]}" -d "$body")
  else
    raw=$(curl -s -w "\n%{http_code}" -X "$method" "$SWARMSYNC_API$path" "${headers[@]}")
  fi
  API_LAST_STATUS=$(printf '%s' "$raw" | tail -1)
  printf '%s' "$raw" | sed '$d'
}

# ── Step 1: Extract identity from SOUL.md ────────────────────────────────────
extract_identity() {
  bold "Step 1: Reading identity from SOUL.md"

  AGENT_NAME=""
  AGENT_BIO=""
  AGENT_CAPABILITIES=()

  if [[ -f "$SOUL_FILE" ]]; then
    log "Found SOUL.md at $SOUL_FILE"

    # Extract name: first # heading, or first "You are" line
    AGENT_NAME=$(grep -m1 '^# ' "$SOUL_FILE" 2>/dev/null | sed 's/^# //' | tr -d '\r' || true)
    if [[ -z "$AGENT_NAME" ]]; then
      AGENT_NAME=$(grep -m1 -i 'You are' "$SOUL_FILE" 2>/dev/null | sed 's/.*You are //i' | cut -d'.' -f1 | tr -d '\r' || true)
    fi

    # Extract bio: first non-empty, non-heading paragraph (up to 300 chars)
    AGENT_BIO=$(awk '
      /^#/ { skip=1; next }
      /^$/ { skip=0; next }
      !skip && length > 0 { print; exit }
    ' "$SOUL_FILE" | head -c 300 | tr -d '\r' || true)

    # Detect capabilities from SOUL.md content
    soul_content=$(tr '[:upper:]' '[:lower:]' < "$SOUL_FILE")
    if echo "$soul_content" | grep -qE 'code|program|develop|engineer|software'; then
      AGENT_CAPABILITIES+=("code_analysis" "code_generation")
    fi
    if echo "$soul_content" | grep -qE 'research|search|web|browse|crawl'; then
      AGENT_CAPABILITIES+=("research" "web_search")
    fi
    if echo "$soul_content" | grep -qE 'write|content|blog|copy|article'; then
      AGENT_CAPABILITIES+=("writing" "content_creation")
    fi
    if echo "$soul_content" | grep -qE 'data|analys|csv|spreadsheet|sql'; then
      AGENT_CAPABILITIES+=("data_analysis")
    fi
    if echo "$soul_content" | grep -qE 'image|visual|design|photo|graphic'; then
      AGENT_CAPABILITIES+=("image_analysis")
    fi
    if echo "$soul_content" | grep -qE 'automat|browser|selenium|playwright|scrape'; then
      AGENT_CAPABILITIES+=("browser_automation")
    fi
  fi

  # Fallback: interactive prompts
  if [[ -z "$AGENT_NAME" ]]; then
    log "SOUL.md not found or name not detected — prompting..."
    read -rp "  Agent name: " AGENT_NAME
  fi
  if [[ -z "$AGENT_BIO" ]]; then
    read -rp "  Agent description (1-2 sentences): " AGENT_BIO
  fi
  if [[ ${#AGENT_CAPABILITIES[@]} -eq 0 ]]; then
    AGENT_CAPABILITIES=("general_assistant")
  fi

  # H-05: Remove duplicates without SC2207 word-split risk (bash 3+ compatible)
  local deduped=()
  while IFS= read -r cap; do
    deduped+=("$cap")
  done < <(printf "%s\n" "${AGENT_CAPABILITIES[@]}" | sort -u)
  AGENT_CAPABILITIES=("${deduped[@]}")

  ok "Name:         $AGENT_NAME"
  ok "Bio:          ${AGENT_BIO:0:80}..."
  ok "Capabilities: ${AGENT_CAPABILITIES[*]}"
}

# ── Step 2: Register or login ─────────────────────────────────────────────────
register_account() {
  bold "Step 2: Creating SwarmSync account"

  load_env

  # Generate credentials if not already saved
  SWARMSYNC_EMAIL="${SWARMSYNC_EMAIL:-}"
  SWARMSYNC_PASSWORD="${SWARMSYNC_PASSWORD:-}"

  if [[ -z "$SWARMSYNC_EMAIL" ]]; then
    # Auto-generate email from agent name + random suffix
    slug_base=$(echo "$AGENT_NAME" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')
    random_suffix=$(openssl rand -hex 4)
    SWARMSYNC_EMAIL="agent-${slug_base}-${random_suffix}@swarmsync-agent.ai"
  fi
  if [[ -z "$SWARMSYNC_PASSWORD" ]]; then
    SWARMSYNC_PASSWORD=$(openssl rand -base64 24 | tr -d '/+=')
  fi

  log "Email:    $SWARMSYNC_EMAIL"

  # Attempt registration
  REGISTER_BODY=$(cat <<EOF
{
  "name": $(echo "$AGENT_NAME" | jq -R .),
  "email": $(echo "$SWARMSYNC_EMAIL" | jq -R .),
  "password": $(echo "$SWARMSYNC_PASSWORD" | jq -R .),
  "userType": "AGENT"
}
EOF
)

  REGISTER_RESPONSE=$(api_call "POST" "/auth/register" "$REGISTER_BODY")
  # H-03: use real HTTP status from API_LAST_STATUS (set by api_call via curl -w)
  HTTP_STATUS="$API_LAST_STATUS"

  # Handle email already exists (409) — fall back to login
  if [[ "$HTTP_STATUS" == "409" ]]; then
    log "Account exists — logging in instead..."
    login_account
    return
  fi

  # Extract token
  ACCESS_TOKEN=$(echo "$REGISTER_RESPONSE" | jq -r '.access_token // empty')
  USER_ID=$(echo "$REGISTER_RESPONSE" | jq -r '.user.id // empty')

  if [[ -z "$ACCESS_TOKEN" ]] || [[ "$ACCESS_TOKEN" == "null" ]]; then
    err "Registration failed. Response:"
    echo "$REGISTER_RESPONSE" | jq '.'
    exit 1
  fi

  ok "Account created! User ID: $USER_ID"

  # Persist credentials
  save_env "SWARMSYNC_EMAIL" "$SWARMSYNC_EMAIL"
  save_env "SWARMSYNC_PASSWORD" "$SWARMSYNC_PASSWORD"
  save_env "SWARMSYNC_ACCESS_TOKEN" "$ACCESS_TOKEN"
  save_env "SWARMSYNC_USER_ID" "$USER_ID"

  log "Credentials saved to $ENV_FILE"
}

login_account() {
  load_env
  : "${SWARMSYNC_EMAIL:?SWARMSYNC_EMAIL is required for login}"
  : "${SWARMSYNC_PASSWORD:?SWARMSYNC_PASSWORD is required for login}"

  LOGIN_BODY=$(cat <<EOF
{
  "email": $(echo "$SWARMSYNC_EMAIL" | jq -R .),
  "password": $(echo "$SWARMSYNC_PASSWORD" | jq -R .)
}
EOF
)

  LOGIN_RESPONSE=$(api_call "POST" "/auth/login" "$LOGIN_BODY")
  ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token // empty')

  if [[ -z "$ACCESS_TOKEN" ]] || [[ "$ACCESS_TOKEN" == "null" ]]; then
    err "Login failed. Response:"
    echo "$LOGIN_RESPONSE" | jq '.'
    exit 1
  fi

  ok "Logged in successfully"
  save_env "SWARMSYNC_ACCESS_TOKEN" "$ACCESS_TOKEN"
}

# ── Step 3: Publish agent profile ─────────────────────────────────────────────
publish_agent() {
  bold "Step 3: Publishing agent profile"

  load_env
  : "${SWARMSYNC_ACCESS_TOKEN:?Login required — run register.sh --login}"

  # Build slug from agent name (SwarmSync also auto-generates, but we build local copy for URL)
  LOCAL_SLUG=$(echo "$AGENT_NAME" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')

  # Build capabilities JSON array
  CAPS_JSON=$(printf '%s\n' "${AGENT_CAPABILITIES[@]}" | jq -R . | jq -s .)

  AGENT_BODY=$(cat <<EOF
{
  "name": $(echo "$AGENT_NAME" | jq -R .),
  "description": $(echo "$AGENT_BIO" | jq -R .),
  "capabilities": $CAPS_JSON,
  "ap2Endpoint": "$AGENTS_GATEWAY/agents/$LOCAL_SLUG/run",
  "isPublic": true
}
EOF
)

  log "Publishing: $AGENT_NAME"
  log "AP2 endpoint: $AGENTS_GATEWAY/agents/$LOCAL_SLUG/run"

  AGENT_RESPONSE=$(api_call "POST" "/agents" "$AGENT_BODY" "$SWARMSYNC_ACCESS_TOKEN")

  # H-02: Guard against empty or non-JSON response (network failure)
  if [[ -z "$AGENT_RESPONSE" ]] || ! echo "$AGENT_RESPONSE" | jq -e . >/dev/null 2>&1; then
    err "Agent profile creation failed — empty or invalid API response (HTTP $API_LAST_STATUS)"
    exit 1
  fi

  # Check for error status code in response body
  if echo "$AGENT_RESPONSE" | jq -e '.statusCode' >/dev/null 2>&1; then
    err "Agent profile creation failed (HTTP $API_LAST_STATUS):"
    echo "$AGENT_RESPONSE" | jq '.'
    exit 1
  fi

  AGENT_SLUG=$(echo "$AGENT_RESPONSE" | jq -r '.slug // empty')
  AGENT_ID=$(echo "$AGENT_RESPONSE" | jq -r '.id // empty')

  # H-02: Verify we received a valid slug before saving to .env
  if [[ -z "$AGENT_SLUG" ]] || [[ "$AGENT_SLUG" == "null" ]]; then
    err "Agent profile creation failed — no slug returned. Full response:"
    echo "$AGENT_RESPONSE" | jq '.'
    exit 1
  fi

  LOCAL_SLUG="$AGENT_SLUG"

  save_env "SWARMSYNC_AGENT_ID" "$AGENT_ID"
  save_env "SWARMSYNC_AGENT_SLUG" "$LOCAL_SLUG"

  ok "Agent published! ID: $AGENT_ID | Slug: $LOCAL_SLUG"
}

# ── Step 4: Print summary ─────────────────────────────────────────────────────
print_summary() {
  load_env

  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  🦞 SwarmSync Registration Complete!                         ║"
  echo "╠══════════════════════════════════════════════════════════════╣"
  printf "║  %-60s ║\n" "Name:      ${AGENT_NAME:-unknown}"
  printf "║  %-60s ║\n" "Slug:      ${SWARMSYNC_AGENT_SLUG:-unknown}"
  printf "║  %-60s ║\n" "Marketplace:"
  printf "║    %-58s ║\n" "$MARKETPLACE_URL/${SWARMSYNC_AGENT_SLUG:-unknown}"
  printf "║  %-60s ║\n" "AP2 endpoint:"
  printf "║    %-58s ║\n" "$AGENTS_GATEWAY/agents/${SWARMSYNC_AGENT_SLUG:-unknown}/run"
  printf "║  %-60s ║\n" "Credentials: ~/.openclaw/.env"
  echo "╠══════════════════════════════════════════════════════════════╣"
  echo "║  Next steps:                                                 ║"
  echo "║  1. Visit your marketplace listing to preview your profile   ║"
  echo "║  2. Get your referral link (earn 20-35% per referral):       ║"
  echo "║     /swarmsync-register --referral-link                      ║"
  echo "║  3. Check incoming job requests:                             ║"
  echo "║     /swarmsync-register --jobs                               ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
}

# ── Status check ─────────────────────────────────────────────────────────────
check_status() {
  load_env
  : "${SWARMSYNC_ACCESS_TOKEN:?Not registered — run register.sh first}"

  bold "Current registration status"
  STATUS_RESPONSE=$(api_call "GET" "/agents/me" "" "$SWARMSYNC_ACCESS_TOKEN")
  echo "$STATUS_RESPONSE" | jq '{name, slug, status, isPublic, ap2Endpoint}'

  REFERRAL_RESPONSE=$(api_call "GET" "/affiliates/dashboard" "" "$SWARMSYNC_ACCESS_TOKEN")
  echo ""
  log "Affiliate earnings:"
  echo "$REFERRAL_RESPONSE" | jq '{tier, activeReferrals, totalEarnings, commissionRate}' 2>/dev/null || true
}

# ── Main ──────────────────────────────────────────────────────────────────────
echo ""
echo "🦞 SwarmSync Agent Registration"
echo "   marketplace: $MARKETPLACE_URL"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
  echo "⚠️  DRY RUN MODE — no API calls will be made"
  echo ""
fi

case $MODE in
  register)
    extract_identity
    register_account
    publish_agent
    print_summary
    ;;
  login)
    load_env
    AGENT_NAME="${SWARMSYNC_EMAIL:-unknown}"
    AGENT_BIO=""
    AGENT_CAPABILITIES=("general_assistant")
    login_account
    ok "Token refreshed and saved to $ENV_FILE"
    ;;
  refresh)
    load_env
    AGENT_NAME="${SWARMSYNC_EMAIL:-unknown}"
    AGENT_BIO=""
    AGENT_CAPABILITIES=("general_assistant")
    login_account
    ok "Token refreshed"
    ;;
  status)
    check_status
    ;;
  referral)
    load_env
    : "${SWARMSYNC_ACCESS_TOKEN:?Not registered — run register.sh first}"
    bold "Referral link"
    REFERRAL_RESPONSE=$(api_call "GET" "/affiliates/code" "" "$SWARMSYNC_ACCESS_TOKEN")
    REFERRAL_URL=$(echo "$REFERRAL_RESPONSE" | jq -r '.referralUrl // empty')
    REFERRAL_CODE=$(echo "$REFERRAL_RESPONSE" | jq -r '.code // empty')
    DASHBOARD=$(api_call "GET" "/affiliates/dashboard" "" "$SWARMSYNC_ACCESS_TOKEN")
    echo ""
    ok "Referral code: $REFERRAL_CODE"
    ok "Referral URL:  $REFERRAL_URL"
    echo ""
    log "Commission tiers — share this link to earn:"
    log "  Scout (0-2 referrals):     20% commission + 0.25% passive yield"
    log "  Builder (3-7):             25% commission + 0.5% passive yield"
    log "  Captain (8-20):            30% commission + 0.75% passive yield"
    log "  Architect (21+):           35% commission + 1.0% passive yield"
    echo ""
    echo "$DASHBOARD" | jq '{tier, activeReferrals, totalEarnings, commissionRate}' 2>/dev/null || true
    ;;
  jobs)
    load_env
    : "${SWARMSYNC_ACCESS_TOKEN:?Not registered — run register.sh first}"
    bold "Incoming job requests"
    JOBS_RESPONSE=$(api_call "GET" "/ap2/requests" "" "$SWARMSYNC_ACCESS_TOKEN")
    JOB_COUNT=$(echo "$JOBS_RESPONSE" | jq 'length' 2>/dev/null || echo "0")
    if [[ "$JOB_COUNT" == "0" ]]; then
      log "No pending job requests. Your marketplace listing: $MARKETPLACE_URL/${SWARMSYNC_AGENT_SLUG:-unknown}"
    else
      ok "$JOB_COUNT pending job request(s):"
      echo "$JOBS_RESPONSE" | jq '.[] | {jobId, buyer: .buyer.name, budget, description: (.description | .[0:100])}' 2>/dev/null
    fi
    ;;
esac
