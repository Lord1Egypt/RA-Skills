#!/bin/sh
# Does every class in these templates exist in the bundle? No Node, no browser, no framework —
# just grep, so it runs in any repo and in a pre-commit hook.
#
#   ./check-classes.sh $(find src -name '*.html')
#   ./check-classes.sh --app-prefix app- src/app/*.component.html
#   ./check-classes.sh --app-prefix rz- --app-prefix settings- $(find resources -name '*.html')
#   ./check-classes.sh --app-prefix 'wsr__,actions-,address-' resources/**/*.html
#
# --app-prefix may be repeated, or given a comma-separated list. A new app should need one prefix;
# an existing one usually has many, and listing them is how you get from "166 findings" to the few
# that are actually wrong.
#
# Use `find` rather than src/**/*.html: that glob only recurses in zsh.
#
# It reads class="…" / className="…" / className={`…`} attributes, so it covers plain HTML,
# Angular and Vue templates and JSX alike. Class names your code composes at runtime
# ("badge-status-" + status) are invisible to it — that is what verify.mjs catches in the DOM.
# This is the cheap check; verify.mjs is the thorough one.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

# --app-prefix, repeatable and/or comma-separated. Collected into one alternation so an existing
# repo with a dozen prefixes is one flag list rather than a reason not to run the check.
prefixes=""
while [ $# -gt 0 ]; do
  case $1 in
    --app-prefix)
      [ $# -ge 2 ] || { echo "--app-prefix needs a value" >&2; exit 2; }
      prefixes="$prefixes,$2"; shift 2 ;;
    --app-prefix=*) prefixes="$prefixes,${1#--app-prefix=}"; shift ;;
    --) shift; break ;;
    *) break ;;
  esac
done
[ $# -gt 0 ] || { echo "usage: $0 [--app-prefix PREFIX]... FILE..." >&2; exit 2; }

pat=""
if [ -n "$prefixes" ]; then
  oldIFS=$IFS; IFS=,
  for p in $prefixes; do
    [ -n "$p" ] || continue
    esc=$(printf '%s' "$p" | sed 's/[].[^$*\\/]/\\&/g')
    pat="$pat|^$esc"
  done
  IFS=$oldIFS
  pat=${pat#|}
fi

known=$(mktemp); used=$(mktemp)

# Everything the bundle styles, plus what bundle-fixes.css adds, plus the light theme hook the
# bundle has no rule for.
{
  cat "$here/classes.txt"
  sed 's/^/icon-/' "$here/icons.txt"
  grep -oE '\.[a-zA-Z][a-zA-Z0-9_-]*' "$here/bundle-fixes.css" | sed 's/^\.//'
  echo ma-light
} | sort -u > "$known"

# Two passes: quoted attributes (either quote style), then backtick templates, which may contain
# quotes inside their ${…} interpolations and so need their own delimiter. Newlines are flattened
# first so an attribute wrapped across lines is still one match. Interpolations — `${…}` in JSX and
# `{{…}}` in Angular/Vue templates — are dropped: a name assembled at runtime cannot be checked
# from source, and leaving them in reports the expression as an invented class.
flat=$(mktemp); trap 'rm -f "$known" "$used" "$flat"' EXIT
cat "$@" | tr '\n' ' ' > "$flat"
{
  grep -oE '(class|className)="[^"]*"' "$flat" | sed 's/^[^"]*"//; s/"$//'
  grep -oE "(class|className)='[^']*'" "$flat" | sed "s/^[^']*'//; s/'$//"
  grep -oE '(class|className)=\{`[^`]*`' "$flat" | sed 's/^[^`]*`//'
} | sed 's/\${[^}]*}/ /g; s/{{[^}]*}}/ /g' \
  | tr -s ' \t`{}' '\n' \
  | grep -E '^[A-Za-z_][A-Za-z0-9_-]*$' | sort -u > "$used"

# Nothing extracted means the check covered nothing — almost always a glob that matched no
# template, or markup this script cannot read. Saying "clean" there would be a false green.
[ -s "$used" ] || { echo "no class attributes found in $# file(s) — check the glob" >&2; exit 2; }

missing=$(comm -23 "$used" "$known")
glyph=$(printf '%s\n' "$missing" | grep '^glyphicon-' || true)
if [ -n "$pat" ]; then
  missing=$(printf '%s\n' "$missing" | grep -vE "$pat" || true)
fi
missing=$(printf '%s\n' "$missing" | grep -vE '^$' || true)

if [ -z "$missing" ]; then
  echo "clean — $(wc -l < "$used" | tr -d ' ') classes, all defined by the bundle"
  exit 0
fi

echo "Not styled by the bundle:"
printf '%s\n' "$missing" | sed 's/^/  • /'
[ -z "$glyph" ] || echo "(glyphicon-* is Bootstrap's icon font, not the design system — use sp-icon icon-*)"
echo
echo "Either the class is invented — find the real one in classes.txt — or it is your own,"
echo "in which case declare it: --app-prefix <prefix> (repeatable, or comma-separated)."
echo
echo "classes.txt is the CDN marketplace bundle. An app that receives the design system through"
echo "its own build has a larger vocabulary, so a name missing here may still be styled there —"
echo "on that route treat this as a list to review, not a list of bugs."
exit 1
