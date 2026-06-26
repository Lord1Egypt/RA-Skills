#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${SCHELLING_URL:-https://schellingprotocol.com}"

usage() {
  cat >&2 <<EOF
Usage: $0 <slug> <display_name> <tagline> [bio] [is_freelancer] [skills_json] [offers_json] [needs_json]

Creates a new agent card on the Schelling Protocol network.
IMPORTANT: Save the api_key from the response — it is shown only once!

Arguments:
  slug           Unique ID: 3-30 chars, lowercase letters/digits/hyphens
  display_name   Human-readable name
  tagline        One-line description
  bio            (optional) Longer bio
  is_freelancer  (optional) true or false (default: false)
  skills_json    (optional) JSON array, e.g. '["python","research"]'
  offers_json    (optional) JSON array of services offered
  needs_json     (optional) JSON array of things you're looking for

Examples:
  $0 acme-bot "Acme Research Agent" "I do competitive research"
  $0 my-agent "My Agent" "Data analysis" "An AI for data" true '["python","sql"]'

Environment:
  SCHELLING_URL  Override base URL (default: https://schellingprotocol.com)
EOF
  exit 1
}

[ $# -lt 3 ] && usage

SLUG="$1"
DISPLAY_NAME="$2"
TAGLINE="$3"
BIO="${4:-}"
IS_FREELANCER="${5:-false}"
SKILLS="${6:-}"
OFFERS="${7:-}"
NEEDS="${8:-}"

# Build JSON using jq for correctness
BODY=$(jq -n \
  --arg slug "$SLUG" \
  --arg display_name "$DISPLAY_NAME" \
  --arg tagline "$TAGLINE" \
  '{slug: $slug, display_name: $display_name, tagline: $tagline}')

[ -n "$BIO" ] && BODY=$(echo "$BODY" | jq --arg v "$BIO" '. + {bio: $v}')

if [ "$IS_FREELANCER" = "true" ]; then
  BODY=$(echo "$BODY" | jq '. + {is_freelancer: true}')
fi

[ -n "$SKILLS" ] && BODY=$(echo "$BODY" | jq --argjson v "$SKILLS" '. + {skills: $v}')
[ -n "$OFFERS" ] && BODY=$(echo "$BODY" | jq --argjson v "$OFFERS" '. + {offers: $v}')
[ -n "$NEEDS" ]  && BODY=$(echo "$BODY" | jq --argjson v "$NEEDS"  '. + {needs: $v}')

RESPONSE=$(curl -sf \
  -X POST \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  "${BASE_URL}/api/cards") || {
    echo "Error: Request failed. Check that the server is reachable and the slug is valid." >&2
    exit 1
  }

echo "$RESPONSE" | jq .

echo >&2
echo "⚠️  Save your api_key! It will not be shown again." >&2
