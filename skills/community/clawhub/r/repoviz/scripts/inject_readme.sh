#!/usr/bin/env sh
# repoviz inject_readme.sh -- insert/update generated diagram Markdown in a README
# between <!-- repoviz:start --> and <!-- repoviz:end --> markers. On first use the
# marked section is appended to the end of the file; later runs replace it in place
# (idempotent -- safe to re-run after regenerating diagrams).
# Usage: sh scripts/inject_readme.sh "<README.md>" '<json array of {title,url,note}>'
# Value restrictions: no double quotes, no "}", no tabs/newlines inside values.
set -u

PROG=${0##*/}

die() { printf '%s: %s\n' "$PROG" "$*" >&2; exit 1; }

[ $# -eq 2 ] || die "usage: sh $PROG \"<README.md>\" '<json array of {title,url,note}>'"

readme=$1
json=$2

[ -f "$readme" ] || die "no such file: $readme"
case $readme in
  *.md|*.markdown) ;;
  *) die "target should be a Markdown file: $readme" ;;
esac

# Parse the JSON array into TSV rows: title \t url \t note (same grammar as build_html.sh).
items=$(printf '%s' "$json" | awk '
  BEGIN { RS = "}" }
  function field(rec, key,   re, s) {
    re = "\"" key "\"[ \\t]*:[ \\t]*\"[^\"]*\""
    if (match(rec, re)) {
      s = substr(rec, RSTART, RLENGTH)
      sub("^\".*\"[ \\t]*:[ \\t]*\"", "", s)
      sub("\"$", "", s)
      return s
    }
    return ""
  }
  {
    t = field($0, "title"); u = field($0, "url"); n = field($0, "note")
    if (u ~ /^https:\/\/(www\.)?x-cmd\.com\/draw([\/?]|$)/) printf "%s\t%s\t%s\n", t, u, n
  }
')

[ -n "$items" ] || die "no usable {\"title\",\"url\"} entries -- url must be an x-cmd.com draw render URL (https://x-cmd.com/draw...); example: [{\"title\":\"Architecture\",\"url\":\"https://x-cmd.com/draw/archmap?n=a;fe;A&n=b;be;B&e=a;b\",\"note\":\"2 tiers\"}]"

block="${TMPDIR:-/tmp}/$PROG.$$.md"
trap 'rm -f "$block" "$readme.repoviz-new"' 0 HUP INT TERM

# Build the marked block: marker, one Markdown section per diagram, marker.
{
  printf '%s\n' '<!-- repoviz:start -->'
  printf '%s\n' "$items" | awk -F '\t' '{
    printf "### %s\n\n![%s](%s)\n\n", $1, $1, $2
    if ($3 != "") printf "*%s*\n\n", $3
  }'
  printf '%s\n' '<!-- repoviz:end -->'
} > "$block" || die "cannot build block"

if grep -q '<!-- repoviz:start -->' "$readme" && grep -q '<!-- repoviz:end -->' "$readme"; then
  # Replace the marked region in place.
  awk -v blkfile="$block" '
    BEGIN { while ((getline line < blkfile) > 0) blk = blk line "\n" }
    /<!-- repoviz:start -->/ { printf "%s", blk; skip = 1; next }
    /<!-- repoviz:end -->/   { if (skip) { skip = 0; next } }
    !skip { print }
  ' "$readme" > "$readme.repoviz-new" || die "failed to rewrite $readme"
  mv "$readme.repoviz-new" "$readme"
  printf 'updated: %s (repoviz block replaced)\n' "$readme"
else
  # First use -- append the marked section.
  {
    printf '\n## Diagrams\n\n'
    cat "$block"
  } >> "$readme" || die "failed to append to $readme"
  printf 'updated: %s (repoviz block appended)\n' "$readme"
fi
