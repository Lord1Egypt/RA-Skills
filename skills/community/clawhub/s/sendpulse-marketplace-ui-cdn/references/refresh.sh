#!/bin/sh
# ---------------------------------------------------------------------------------------------
# Re-derive this folder's generated lists from the live CDN and report what drifted.
#
#   references/refresh.sh            # check only — prints a diff, changes nothing
#   references/refresh.sh --write    # also rewrite classes.txt and icons.txt in place
#
# Exit 0 = the shipped lists still match the bundle. Exit 1 = something drifted (read the diff).
# Run it before trusting the skill after a gap, and any time a class you expect is missing.
#
# A drift line naming a class that DISAPPEARED is the one to act on: grep SKILL.md, components.md,
# gaps.md, tokens.md, kitchen-sink.html and examples/ for it, because something in the skill still
# recommends it. A newly APPEARED class needs nothing — --write picks it up.
#
# What it does NOT rewrite: tokens.css. It tells you which custom-property *names* appeared or
# vanished, but the light and dark *values* come from a different stylesheet and picking them is a
# judgement call — the command is in tokens.css's own header.
# -------------------------------------------------------------------------------------------
set -eu

BUNDLE_URL="https://cdn.sendpulse.com/dist/css/sp-marketplace-app-ui.min.css"
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
write=0
[ "${1:-}" = "--write" ] && write=1

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
drift=0

printf 'fetching %s\n' "$BUNDLE_URL"
curl -fsS -o "$tmp/bundle.css" "$BUNDLE_URL" || {
  echo "could not fetch the bundle — check the URL and your network" >&2; exit 2; }
printf '  %s bytes\n\n' "$(wc -c < "$tmp/bundle.css" | tr -d ' ')"

# --- classes ---------------------------------------------------------------------------------
# icon-*/glyphicon-* excluded on purpose: the first is icons.txt, the second is the inherited
# Bootstrap 3 icon font, left out so it cannot be picked by accident (SKILL.md non-negotiable #6).
grep -oE '\.[a-zA-Z_][a-zA-Z0-9_-]*' "$tmp/bundle.css" | sed 's/^\.//' | sort -u \
  | grep -Ev '^(icon|glyphicon)-' > "$tmp/classes.txt"

# --- icons -----------------------------------------------------------------------------------
grep -oE '\.icon-[a-zA-Z0-9_-]+' "$tmp/bundle.css" | sed 's/^\.icon-//' | sort -u > "$tmp/icons.txt"

# --- custom properties the bundle reads ------------------------------------------------------
# The bundle defines none of its own, so every var() it reads is one tokens.css has to supply.
grep -oE 'var\(--[A-Za-z0-9_-]+' "$tmp/bundle.css" | sed 's/var(--//' | sort -u > "$tmp/vars.txt"
grep -oE '^[[:space:]]*--[A-Za-z0-9_-]+' "$here/tokens.css" \
  | sed 's/^[[:space:]]*--//' | sort -u > "$tmp/tokens.txt"

report() {  # name  fresh  shipped
  if diff -q "$2" "$3" >/dev/null 2>&1; then
    printf '%-18s unchanged — %s\n' "$1" "$(wc -l < "$2" | tr -d ' ')"
  else
    drift=1
    printf '%-18s DRIFTED (shipped %s, live %s)\n' \
      "$1" "$(wc -l < "$3" | tr -d ' ')" "$(wc -l < "$2" | tr -d ' ')"
    comm -13 "$3" "$2" | sed 's/^/    + /'
    comm -23 "$3" "$2" | sed 's/^/    - /'
  fi
}

report classes.txt "$tmp/classes.txt" "$here/classes.txt"
report icons.txt   "$tmp/icons.txt"   "$here/icons.txt"
report tokens.css  "$tmp/vars.txt"    "$tmp/tokens.txt"

glyph=$(grep -oE '\.glyphicon-[a-zA-Z0-9_-]+' "$tmp/bundle.css" | sort -u | wc -l | tr -d ' ')
printf '%-18s %s inherited Bootstrap icons, excluded from classes.txt\n' 'glyphicon-*' "$glyph"

echo
if [ "$drift" -eq 0 ]; then
  echo 'everything matches the live bundle.'
  exit 0
fi

if [ "$write" -eq 1 ]; then
  cp "$tmp/classes.txt" "$here/classes.txt"
  cp "$tmp/icons.txt"   "$here/icons.txt"
  echo 'classes.txt and icons.txt rewritten.'
  echo 'Now re-read the drift above: a dropped class may be named in SKILL.md or kitchen-sink.html'
  echo '(grep for it), and any token change needs its values from tokens.css'"'"'s header command.'
else
  echo 'nothing written. Re-run with --write to update classes.txt and icons.txt,'
  echo 'then check whether SKILL.md or kitchen-sink.html names anything that disappeared.'
fi
exit 1
