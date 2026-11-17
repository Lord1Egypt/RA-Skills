#!/usr/bin/env sh
# repoviz shorten.sh -- create a permanent short link for a ?type= chart definition.
# Usage:
#   sh scripts/shorten.sh <type> '<d-schema json>' [title]
#   echo '<json>' | sh scripts/shorten.sh <type> - [title]
# Example:
#   sh scripts/shorten.sh sankey '{"labels":["A","B"],"links":[{"from":"A","to":"B","value":5}]}' "My flow"
#   -> https://www.x-cmd.com/draw/c/<hash>   (permanent; GET renders the SVG)
# The <json> body is the same schema the render endpoint accepts via ?d= --
# see references/sankey.md ({"labels","links"}) and references/general-charts.md
# ({"data":[{"label","value"},...]} for pie/bar/hbar/line/...).
# Limits: POST is accepted only on the /draw?type= family -- node/edge diagrams
# (/draw/archmap, /draw/arch2, /draw/seq, /draw/uc, ...) return 405 and have no
# short-link form; keep their full URLs. POST must target www.x-cmd.com directly
# (the bare domain 301-redirects and drops the body). Rate limit ~30/min/IP.
set -u

PROG=${0##*/}
UA="repoviz/1.0 (+https://x-cmd.com/draw)"

die() { printf '%s: %s\n' "$PROG" "$*" >&2; exit 2; }

[ $# -ge 2 ] && [ $# -le 3 ] || die "usage: sh $PROG <type> '<d-schema json>' [title]"
command -v curl >/dev/null 2>&1 || die "curl is required"

type=$1
body=$2
[ "$body" = "-" ] && body=$(cat)
title=${3:-}

case $body in
  \{*\}) ;;
  *) die "body must be a JSON object, e.g. {\"labels\":[\"A\",\"B\"],\"links\":[{\"from\":\"A\",\"to\":\"B\",\"value\":5}]}" ;;
esac

query="type=$type"
if [ -n "$title" ]; then
  # percent-encode the title (space %20; keep it minimal and safe)
  enc=$(printf '%s' "$title" | sed 's/%/%25/g; s/ /%20/g; s/&/%26/g; s/#/%23/g')
  query="$query&title=$enc"
fi

printf '%s: notice: uploading chart definition to x-cmd.com; the result is a PERMANENT PUBLIC link\n' "$PROG" >&2
resp=$(curl -sS --max-time 30 -X POST "https://www.x-cmd.com/draw?$query" \
  -H 'content-type: application/json' \
  -A "$UA" \
  --data "$body" 2>&1) || die "POST failed (network) -- note: endpoint is https://www.x-cmd.com/draw"

url=$(printf '%s' "$resp" | grep -oE 'https://[a-z0-9.-]*/draw/c/[a-f0-9]+' | head -1)
if [ -n "$url" ]; then
  printf '%s\n' "$url"
  exit 0
fi

# 4xx bodies carry a plain-text correction example -- surface its first line.
printf '%s: %s\n' "$PROG" "$(printf '%s' "$resp" | head -n 1 | cut -c1-200)" >&2
exit 1
