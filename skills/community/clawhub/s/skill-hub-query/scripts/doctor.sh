#!/usr/bin/env bash
# skill-hub-query: doctor (one-shot self-check of token / connectivity / cache)
#
# Design: doctor is a diagnostic; one failing check must NOT stop subsequent
# checks. Each step is wrapped with if/||true to ensure all 5 phases run.
set -euo pipefail
SELF_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# shellcheck source=./_lib.sh
source "${SELF_DIR}/_lib.sh"

setup_legacy_notice

# Track diagnostic temp files for clean removal on any exit path.
_DOCTOR_TMP_FILES=()
_doctor_cleanup() {
  local f
  for f in "${_DOCTOR_TMP_FILES[@]:-}"; do
    [[ -n "$f" ]] && rm -f "$f" 2>/dev/null
  done
  rm -f "${_LEGACY_NOTICE_MARKER:-}" 2>/dev/null
}
trap _doctor_cleanup EXIT

echo "=== skill-hub-query self-check ==="
echo ""

# ---------- skillhub.cn provider branch ----------
# When SKILL_HUB_PROVIDER=skillhub_cn, run a tailored diagnostic that reflects
# what's actually supported (install/detail/versions only). Generic-contract
# behavior is unaffected when the env var is unset.
if is_skillhub_cn; then
  echo "[provider] SKILL_HUB_PROVIDER = skillhub_cn"
  echo "[provider] base URL          = ${SKILLHUB_CN_BASE}"
  echo ""

  echo "[1/3] checking dependencies..."
  _SHCN_MISSING=0
  for cmd in jq curl file unzip; do
    if command -v "$cmd" >/dev/null 2>&1; then
      echo "  ok   $cmd"
    else
      echo "  miss $cmd (install via your package manager, e.g. apt install -y $cmd)"
      _SHCN_MISSING=1
    fi
  done
  echo ""

  echo "[2/3] connectivity probe (GET ${SKILLHUB_CN_BASE}/api/v1/skills/skill-creator)"
  _shcn_body="$(mktemp)"; _DOCTOR_TMP_FILES+=("$_shcn_body")
  _shcn_http="$(curl -sSL --max-time 10 -o "$_shcn_body" -w "%{http_code}" \
    "${SKILLHUB_CN_BASE}/api/v1/skills/skill-creator" 2>/dev/null || echo "000")"
  case "$_shcn_http" in
    200)
      _shcn_slug="$(jq -r '.skill.slug // "?"' "$_shcn_body" 2>/dev/null || echo "?")"
      _shcn_ver="$(jq -r '.latestVersion.version // "?"' "$_shcn_body" 2>/dev/null || echo "?")"
      echo "  ok   reachable (probe slug=$_shcn_slug latestVersion=$_shcn_ver)"
      ;;
    000)
      echo "  err  network unreachable; check connectivity / proxy / DNS"
      ;;
    *)
      echo "  warn HTTP $_shcn_http (the probe slug may simply be missing; provider URL still reachable)"
      ;;
  esac
  rm -f "$_shcn_body"
  echo ""

  echo "[3/3] operation matrix"
  echo "  available (skillhub.cn public API):"
  echo "    - install <slug>          bash $SELF_DIR/install.sh <slug>"
  echo "    - query slug <slug>       bash $SELF_DIR/query.sh slug <slug>"
  echo "    - query versions <slug>   bash $SELF_DIR/query.sh versions <slug>"
  echo "    - query keyword <kw>      bash $SELF_DIR/query.sh keyword <kw>   (live, no cache)"
  echo "    - query today             bash $SELF_DIR/query.sh today          (live, no cache)"
  echo "    - query combo --keyword=  bash $SELF_DIR/query.sh combo --keyword=xx [--category=xx] [--source=xx]"
  echo "  unavailable (no public API):"
  echo "    - sync (live mode; no local cache needed -- sync.sh is a no-op here)"
  echo "    - query author / time modes (no equivalent filter on skillhub.cn)"
  echo "    - edit (card metadata is a one-way mirror from upstream)"
  echo ""
  echo "=== summary ==="
  if [[ "$_SHCN_MISSING" == "1" ]]; then
    echo "[blocking] missing dependency above; install the listed tool(s) first."
    exit 1
  fi
  echo "[ok] skillhub.cn provider is configured and reachable."
  exit 0
fi

ISSUES=()
TIPS=()
add_issue() { ISSUES+=("$1"); }
add_tip()   { TIPS+=("$1"); }
OPENAPI_OK=0
LEGACY_OK=0

# 1) Dependencies
echo "[1/5] checking dependencies..."
for cmd in jq curl file unzip; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "  ok   $cmd"
  else
    echo "  miss $cmd"
    add_issue "missing dependency '$cmd'; install with your package manager (e.g. apt install -y $cmd)"
  fi
done
echo ""

# 2) Paths
echo "[2/5] path configuration..."
echo "  SKILL_DIR             = $SKILL_DIR"
_url_display="$(load_endpoint)"
echo "  Hub URL               = ${_url_display:-(not configured)}"
echo "  API prefix            = $HUB_API_PREFIX"
echo "  Legacy API prefix     = $HUB_LEGACY_API_PREFIX"
echo "  Auth header           = $(load_auth_header)"
echo "  Cache dir             = $CACHE_DIR"
echo "  Credentials file      = $CREDS_FILE"
echo ""
if [[ -z "$_url_display" ]]; then
  add_issue "No Skill Hub URL configured. Set SKILL_HUB_URL or .endpoint in credentials.json (see SKILL.md)."
fi

# 3) Token
echo "[3/5] checking token configuration..."
TOKEN_SOURCE=""
if [[ -n "${SKILL_HUB_TOKEN:-}" ]]; then
  echo "  ok   environment SKILL_HUB_TOKEN is set ($(mask_token "$SKILL_HUB_TOKEN"))"
  TOKEN_SOURCE="env"
elif [[ -f "$CREDS_FILE" ]]; then
  t="$(jq -r '.token // empty' "$CREDS_FILE" 2>/dev/null || echo "")"
  if [[ -n "$t" && "$t" != "null" && "$t" != "<put-your-token-here>" ]]; then
    echo "  ok   credentials file present ($(mask_token "$t"))"
    TOKEN_SOURCE="file"
    check_creds_perms
  else
    echo "  warn credentials file exists but token field is empty or placeholder"
    echo "       edit $CREDS_FILE to set a real token (optional; legacy fallback works without)"
    add_tip "(optional) edit $CREDS_FILE to put a real token there for nicer auth"
  fi
else
  echo "  skip no token configured; the skill will use the legacy fallback channel"
  echo "       (if your Hub requires auth, ask its maintainer for a token)"
  add_tip "(optional, long-term) request a Hub token for full OpenAPI access and private skills"
fi
echo ""

# 4) Connectivity (test both channels; at least one OK = good)
echo "[4/5] connectivity tests..."
ENDPOINT="$(load_endpoint)"
if [[ -z "$ENDPOINT" ]]; then
  echo "  skip connectivity tests: no Hub URL configured"
else

# 4a) OpenAPI (requires token)
if [[ -n "$TOKEN_SOURCE" ]]; then
  echo "  probe OpenAPI: GET ${HUB_API_PREFIX}/search?size=1 (with token)"
  search_body="$(mktemp)"; _DOCTOR_TMP_FILES+=("$search_body")
  auth_hdr="$(load_auth_header)"
  auth_scheme="$(load_auth_scheme)"
  search_http="$(curl -sSL --max-time 10 -o "$search_body" -w "%{http_code}" \
    -H "${auth_hdr}: ${auth_scheme}$(load_token)" \
    "${ENDPOINT}${HUB_API_PREFIX}/search?size=1" 2>/dev/null || echo "000")"
  case "$search_http" in
    200)
      total="$(jq -r '.data.total // "?"' "$search_body" 2>/dev/null || echo "?")"
      first_slug="$(jq -r '.data.records[0].slug // "?"' "$search_body" 2>/dev/null || echo "?")"
      code="$(jq -r '.code // "?"' "$search_body" 2>/dev/null || echo "?")"
      if [[ "$code" == "200" ]]; then
        echo "  ok   OpenAPI authenticated (Hub total=$total, sample slug=$first_slug)"
        OPENAPI_OK=1
      else
        msg="$(jq -r '.message // ""' "$search_body" 2>/dev/null || echo "")"
        echo "  warn HTTP 200 but business code=$code message=$msg"
        add_issue "OpenAPI business error code=$code message=$msg; verify Hub URL and token scope"
      fi
      ;;
    401|403)
      echo "  err  HTTP $search_http -- token invalid or expired"
      add_issue "token invalid (HTTP $search_http); refresh or re-fetch from your Hub maintainer"
      ;;
    000)
      echo "  err  network unreachable"
      add_issue "network unreachable; check connectivity / proxy / DNS"
      ;;
    *)
      echo "  warn HTTP $search_http"
      ;;
  esac
  rm -f "$search_body"
else
  echo "  skip OpenAPI: no token configured"
fi

# 4b) Legacy fallback
echo "  probe Legacy: GET ${HUB_LEGACY_API_PREFIX}/search?size=1 (no auth)"
legacy_body="$(mktemp)"; _DOCTOR_TMP_FILES+=("$legacy_body")
legacy_http="$(curl -sSL --max-time 10 -o "$legacy_body" -w "%{http_code}" \
  "${ENDPOINT}${HUB_LEGACY_API_PREFIX}/search?size=1" 2>/dev/null || echo "000")"
case "$legacy_http" in
  200)
    legacy_code="$(jq -r '.code // empty' "$legacy_body" 2>/dev/null || echo "")"
    legacy_success="$(jq -r '.success // empty' "$legacy_body" 2>/dev/null || echo "")"
    if [[ ( -n "$legacy_code" && "$legacy_code" != "200" ) || "$legacy_success" == "false" ]]; then
      legacy_msg="$(jq -r '.message // .errorMsg // ""' "$legacy_body" 2>/dev/null || echo "")"
      echo "  warn legacy HTTP 200 but business failed (code=$legacy_code success=$legacy_success message=$legacy_msg)"
      echo "       legacy may now require auth; consider configuring a token"
      add_tip "legacy channel returned business error (code=$legacy_code); recommend configuring a token"
    else
      legacy_total="$(jq -r '.data.total // "?"' "$legacy_body" 2>/dev/null || echo "?")"
      echo "  ok   legacy reachable (Hub total=$legacy_total, works without token)"
      LEGACY_OK=1
    fi
    ;;
  000)
    echo "  err  legacy unreachable (network)"
    add_issue "both channels unreachable; check network/proxy/DNS"
    ;;
  *)
    echo "  warn legacy HTTP $legacy_http"
    ;;
esac
rm -f "$legacy_body"

# 4c) Optional /edit endpoint probe (for edit.sh)
if [[ "${SKILL_HUB_DISABLE_EDIT:-0}" == "1" ]]; then
  echo "  skip /edit endpoint probe (SKILL_HUB_DISABLE_EDIT=1)"
else
  edit_prefix="${SKILL_HUB_EDIT_PREFIX:-${HUB_LEGACY_API_PREFIX}}"
  echo "  probe /edit endpoint: PUT ${edit_prefix}/edit/__probe__ (empty body, expect 404)"
  edit_body="$(mktemp)"; _DOCTOR_TMP_FILES+=("$edit_body")
  edit_http="$(curl -sSL --max-time 10 -o "$edit_body" -w "%{http_code}" \
    -X PUT \
    -H "Content-Type: application/json" \
    -d '{}' \
    "${ENDPOINT}${edit_prefix}/edit/__probe__" 2>/dev/null || echo "000")"
  case "$edit_http" in
    200|400|403|404|405)
      # Any structured HTTP response means the endpoint route is mounted
      echo "  ok   /edit endpoint mounted (HTTP $edit_http -- expected for empty/nonexistent slug)"
      ;;
    000)
      echo "  warn /edit endpoint unreachable (edit.sh will fail; other features unaffected)"
      add_tip "/edit endpoint unreachable; if you don't need edit.sh, run: export SKILL_HUB_DISABLE_EDIT=1"
      ;;
    *)
      echo "  warn /edit endpoint HTTP $edit_http"
      add_tip "/edit endpoint returned HTTP $edit_http; edit.sh may not work on this Hub"
      ;;
  esac
  rm -f "$edit_body"
fi

if [[ "${OPENAPI_OK:-0}" == "1" || "${LEGACY_OK:-0}" == "1" ]]; then
  echo "  ok   at least one channel works -- skill is usable"
else
  echo "  err  both channels are down -- skill cannot work"
  add_issue "both channels are down; troubleshoot network / token / Hub URL"
fi
fi  # close: if [[ -z "$ENDPOINT" ]]; then ... else ...
echo ""

# 5) Local cache
echo "[5/5] checking local cache..."
if [[ -f "$CACHE_FILE" ]]; then
  cnt="$(jq 'length' "$CACHE_FILE" 2>/dev/null || echo "?")"
  echo "  ok   skill-cache.json present, $cnt skill(s) cached"
else
  echo "  skip skill-cache.json not present (will be created on first use)"
fi
if [[ -f "$CACHE_META" ]]; then
  last_sync="$(jq -r '.lastIncrementalSync // 0' "$CACHE_META" 2>/dev/null || echo "0")"
  if [[ "$last_sync" != "0" ]]; then
    last_dt="$(date -d "@$((last_sync/1000))" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "$last_sync")"
    echo "  info last sync: $last_dt"
  fi
fi
if [[ -f "$VERSIONS_FILE" ]]; then
  vcnt="$(jq 'length' "$VERSIONS_FILE" 2>/dev/null || echo "?")"
  echo "  ok   skill-versions.json present, $vcnt skill(s) tracked locally"
fi
echo ""

echo "=== summary ==="
if [[ "${#ISSUES[@]}" == "0" && "${#TIPS[@]}" == "0" ]]; then
  echo "[ok] all checks passed -- ready to use: bash $SELF_DIR/sync.sh"
else
  if [[ "${#ISSUES[@]}" != "0" ]]; then
    echo "[blocking issues]"
    i=1
    for issue in "${ISSUES[@]}"; do
      echo "  $i. $issue"
      i=$((i+1))
    done
    echo ""
  fi
  if [[ "${#TIPS[@]}" != "0" ]]; then
    if [[ "${#ISSUES[@]}" == "0" ]]; then
      echo "[ok] skill is functional."
    fi
    echo "[optional improvements]"
    i=1
    for tip in "${TIPS[@]}"; do
      echo "  $i. $tip"
      i=$((i+1))
    done
  fi
fi
