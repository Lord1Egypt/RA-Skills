#!/usr/bin/env bash
# SkillGuard — scan a ClawHub skill before installing
# Usage:
#   ./scan.sh --slug instagram-search
#   ./scan.sh --query instagram
#   ./scan.sh --slug instagram-search --max 5
#
# Required env vars:
#   APIFY_TOKEN            — Apify API token
#   LAKERA_API_KEY         — Lakera Guard API key
#   OPENCLAW_WEBHOOK_URL   — Your OpenClaw /hooks/agent endpoint
#   OPENCLAW_HOOKS_TOKEN   — Your OpenClaw hooks auth token

set -euo pipefail

# ── Validate env vars ────────────────────────────────────────────────────────
: "${APIFY_TOKEN:?APIFY_TOKEN is required}"
: "${LAKERA_API_KEY:?LAKERA_API_KEY is required}"
: "${OPENCLAW_WEBHOOK_URL:?OPENCLAW_WEBHOOK_URL is required}"
: "${OPENCLAW_HOOKS_TOKEN:?OPENCLAW_HOOKS_TOKEN is required}"

ACTOR_ID="TMjFBNFqIIUfCBf6K"

# ── Parse args ───────────────────────────────────────────────────────────────
SLUG=""
QUERY=""
MAX_SKILLS=10

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slug)   SLUG="$2";       shift 2 ;;
    --query)  QUERY="$2";      shift 2 ;;
    --max)    MAX_SKILLS="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

if [[ -z "$SLUG" && -z "$QUERY" ]]; then
  echo "Error: provide --slug <slug> or --query <search term>"
  exit 1
fi

# ── Build actor input ────────────────────────────────────────────────────────
if [[ -n "$SLUG" && -n "$QUERY" ]]; then
  ACTOR_INPUT=$(jq -n \
    --arg slug "$SLUG" \
    --arg query "$QUERY" \
    --arg key "$LAKERA_API_KEY" \
    --argjson max "$MAX_SKILLS" \
    '{"skillSlugs": [$slug], "searchQuery": $query, "lakeraApiKey": $key, "maxSkills": $max}')
elif [[ -n "$SLUG" ]]; then
  ACTOR_INPUT=$(jq -n \
    --arg slug "$SLUG" \
    --arg key "$LAKERA_API_KEY" \
    --argjson max "$MAX_SKILLS" \
    '{"skillSlugs": [$slug], "lakeraApiKey": $key, "maxSkills": $max}')
else
  ACTOR_INPUT=$(jq -n \
    --arg query "$QUERY" \
    --arg key "$LAKERA_API_KEY" \
    --argjson max "$MAX_SKILLS" \
    '{"searchQuery": $query, "lakeraApiKey": $key, "maxSkills": $max}')
fi

# ── Build and base64-encode ad-hoc webhook ───────────────────────────────────
WEBHOOK_JSON=$(jq -n \
  --arg url "$OPENCLAW_WEBHOOK_URL" \
  --arg token "$OPENCLAW_HOOKS_TOKEN" \
  '[{
    "eventTypes": ["ACTOR.RUN.SUCCEEDED", "ACTOR.RUN.FAILED"],
    "requestUrl": $url,
    "headersTemplate": "{\"Authorization\": \"Bearer \($token)\"}",
    "payloadTemplate": "{\"resource\": {{resource}}}"
  }]')

# base64 encode (no line wrapping)
WEBHOOK_B64=$(echo "$WEBHOOK_JSON" | base64 | tr -d '\n')

# ── Trigger the actor run ────────────────────────────────────────────────────
echo "🛡️  Triggering SkillGuard actor..."
echo "   Actor:   numerous_hierarchy/skill-guard-actor ($ACTOR_ID)"
if [[ -n "$SLUG" ]]; then echo "   Slug:    $SLUG"; fi
if [[ -n "$QUERY" ]]; then echo "   Query:   $QUERY"; fi
echo "   Webhook: $OPENCLAW_WEBHOOK_URL"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST \
  "https://api.apify.com/v2/acts/${ACTOR_ID}/runs?token=${APIFY_TOKEN}&webhooks=${WEBHOOK_B64}" \
  -H "Content-Type: application/json" \
  -d "$ACTOR_INPUT")

HTTP_STATUS=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [[ "$HTTP_STATUS" == "201" ]]; then
  RUN_ID=$(echo "$BODY" | jq -r '.data.id // empty')
  echo "✅ Actor run started (run ID: $RUN_ID)"
  echo "   Results will be delivered to your OpenClaw agent via webhook."
  echo "   Monitor at: https://console.apify.com/actors/$ACTOR_ID/runs/$RUN_ID"
else
  echo "❌ Failed to start actor run (HTTP $HTTP_STATUS)"
  echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
  exit 1
fi