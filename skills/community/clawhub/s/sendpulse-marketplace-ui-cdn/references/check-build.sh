#!/bin/sh
# Is this repo wired to the CDN stylesheet correctly? No Node, no browser, no build — just grep
# over the files that carry the contract, so it runs anywhere and in a pre-commit hook.
#
#   ./check-build.sh                 # the current repo
#   ./check-build.sh path/to/integration
#
# It checks the things that fail silently: a self-hosted copy of the bundle, a missing tokens.css
# (the bundle reads 28 custom properties and defines none), a missing bundle-fixes.css, app CSS
# linked before the design system, a var() name no stylesheet defines, both theme builds loaded at
# once. It cannot tell you whether the result looks right in dark — that is verify.mjs.
#
# FAIL = broken or about to break. WARN = worth a look, may be deliberate. Exit 1 on any FAIL.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=${1:-.}
[ -d "$root" ] || { echo "not a directory: $root" >&2; exit 2; }
cd "$root"
fails=0
warns=0

ok()   { printf '  ok    %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1"; fails=$((fails + 1)); }
warn() { printf '  WARN  %s\n' "$1"; warns=$((warns + 1)); }

BUNDLE=sp-marketplace-app-ui.min.css

printf '\n%s\n' "CDN stylesheet wiring — $(pwd)"

# ---------------------------------------------------------------- 1. the stylesheet
printf '\nthe bundle\n'
# Any shell, whatever the backend language: the one thing every candidate has in common is that it
# names the bundle. Templates count — the <link> is often emitted by the server.
shell=$(grep -rls "$BUNDLE" \
          --include='*.html' --include='*.htm' --include='*.php' --include='*.twig' \
          --include='*.jinja' --include='*.j2' --include='*.erb' --include='*.ejs' \
          --include='*.hbs' --include='*.pug' --include='*.tmpl' --include='*.gohtml' \
          --include='*.vm' --include='*.cshtml' \
          . 2>/dev/null | grep -v node_modules | head -1 || true)

if [ -z "$shell" ]; then
  fail "nothing links $BUNDLE — this is the CDN route; a repo with @sendpulse/styles in package.json is the other one"
else
  ok "shell: $shell"
  grep -q "https://cdn\.sendpulse\.com/dist/css/$BUNDLE" "$shell" \
    && ok 'linked from cdn.sendpulse.com' \
    || fail "$shell links $BUNDLE from somewhere other than https://cdn.sendpulse.com/dist/css/ — its url(/img/…) and url(/my.fonts/…) resolve against the stylesheet's origin, so a copy breaks every glyph"
fi
# A vendored copy is the same mistake, whether or not it is the one being linked.
copy=$(find . -name "$BUNDLE" -not -path './node_modules/*' 2>/dev/null | head -1 || true)
[ -z "$copy" ] \
  && ok 'no self-hosted copy of the bundle in the repo' \
  || fail "$copy is a local copy of the bundle — serve it from the CDN instead (non-negotiable #1)"

# ---------------------------------------------------------------- 2. the two required files
printf '\ntokens.css and bundle-fixes.css\n'
for f in tokens.css bundle-fixes.css; do
  found=$(find . -name "$f" -not -path './node_modules/*' 2>/dev/null | head -1 || true)
  if [ -z "$found" ]; then
    case $f in
      tokens.css) fail "no tokens.css in the repo — the bundle reads 28 custom properties and defines none, so panels render transparent and focus rings vanish. Copy references/tokens.css" ;;
      *)          fail "no bundle-fixes.css in the repo — the .nav foundation, the status-dot specificity and the .input-group row stay broken. Copy references/bundle-fixes.css" ;;
    esac
  elif [ -n "$shell" ] && ! grep -q "$f" "$shell"; then
    fail "$found exists but $shell never links it"
  else
    ok "$f present and linked"
  fi
done

# ---------------------------------------------------------------- 3. load order is the contract
printf '\nload order\n'
if [ -n "$shell" ]; then
  # Match on href= rather than the filename alone: every one of these files gets named in prose and
  # in comments too, and a <link> often wraps across lines, so the tag itself is not greppable.
  ln() { grep -nE "href=[^>]*$1" "$shell" | head -1 | cut -d: -f1 || true; }
  b=$(ln "$BUNDLE"); t=$(ln 'tokens\.css'); x=$(ln 'bundle-fixes\.css')
  order_ok=1
  [ -n "$b" ] && [ -n "$t" ] && [ "$t" -lt "$b" ] && { fail "$shell links tokens.css before the bundle — the bundle's own values win"; order_ok=0; }
  [ -n "$t" ] && [ -n "$x" ] && [ "$x" -lt "$t" ] && { fail "$shell links bundle-fixes.css before tokens.css"; order_ok=0; }
  # The app's own stylesheet, whatever it is called, must come last: everything in those two files
  # is single-class specificity on purpose, and app CSS is what overrides them.
  app=$(grep -nE 'href=[^>]*\.css' "$shell" | grep -v "$BUNDLE" | grep -v 'tokens\.css' \
        | grep -v 'bundle-fixes\.css' | grep -v 'fonts\.googleapis' | tail -1 | cut -d: -f1 || true)
  if [ -n "$app" ] && [ -n "$x" ] && [ "$app" -lt "$x" ]; then
    fail "$shell links app CSS before bundle-fixes.css — the fixes cannot win a conflict they are meant to win"
    order_ok=0
  fi
  [ "$order_ok" = 1 ] && ok 'bundle → tokens.css → bundle-fixes.css → app CSS'
fi

# ---------------------------------------------------------------- 4. the theme
printf '\ntheme\n'
if [ -n "$shell" ]; then
  n=$(grep -c "$BUNDLE" "$shell" || true)
  if [ "$n" -ge 2 ]; then
    grep -q 'force=light' "$shell" && grep -q 'force=dark' "$shell" \
      && ok 'both builds linked as ?force=light and ?force=dark' \
      || fail "$shell links the bundle twice without the ?force=light / ?force=dark pair — two identical builds"
    grep -q 'media' "$shell" \
      && ok 'one build disabled by media — only one is ever active' \
      || fail "$shell links both builds with no media switch — never load both at once"
    grep -q 'theme' "$shell" \
      && ok 'the shell reads ?theme' \
      || fail "$shell links a dark build but never reads ?theme — it can only ever show one"
  else
    ok 'one build linked (single-theme app)'
  fi
  # ma-dark has to sit on <html>: the bundle's own .ma-dark rules and your var() CSS both key off it.
  if grep -q 'documentElement' "$shell" || awk '/<html/,/>/' "$shell" | grep -q 'ma-dark\|ma-light'; then
    ok 'the theme class goes on <html>'
  elif grep -q 'ma-dark' "$shell"; then
    fail "ma-dark is applied somewhere other than <html> in $shell — put it on the root element"
  elif [ "$n" -ge 2 ]; then
    fail "$shell never applies ma-dark — the dark build alone leaves var()-based app CSS light"
  fi
fi

# ---------------------------------------------------------------- 5. app CSS hygiene
printf '\napp CSS\n'
appcss=$(find . \( -name '*.css' -o -name '*.less' -o -name '*.scss' \) \
         -not -path './node_modules/*' -not -name 'tokens.css' -not -name 'bundle-fixes.css' \
         -not -name "$BUNDLE" 2>/dev/null || true)
if [ -z "$appcss" ]; then
  warn 'no app stylesheets found'
else
  # Comments quote the design system's own hexes all the time; only live declarations count.
  hex=$(sed 's|//.*$||' $appcss 2>/dev/null | grep -oE '#[0-9a-fA-F]{3,8}\b' | wc -l | tr -d ' ')
  [ "$hex" = 0 ] \
    && ok 'no hex colours in app CSS' \
    || warn "$hex hex colour(s) in app CSS — use a semantic class, or a value from references/tokens.md"
  # The route-specific trap: only the 28 properties tokens.css defines exist. A var() name lifted
  # from an integration that gets the design system through its own build resolves to nothing here.
  if [ -f "$here/tokens.css" ]; then
    # A declaration is a name followed by a colon, wherever it sits on the line; a use is inside
    # var(…). Matching on line starts only would miss `:root { --x: red }` written on one line.
    decls() { grep -ohE '\-\-[A-Za-z0-9_-]+[[:space:]]*:' "$@" 2>/dev/null | sed 's/[[:space:]]*:$//' | sort -u; }
    known=$(decls "$here/tokens.css")
    used=$(grep -ohE 'var\((--[A-Za-z0-9_-]+)' $appcss 2>/dev/null | sed 's/^var(//' | sort -u || true)
    # Properties the app declares itself are its own business.
    own=$(decls $appcss || true)
    tk=$(mktemp); tu=$(mktemp)
    printf '%s\n%s\n' "$known" "$own" | sed '/^$/d' | sort -u > "$tk"
    printf '%s\n'      "$used"          | sed '/^$/d' | sort -u > "$tu"
    unknown=$(comm -23 "$tu" "$tk")
    rm -f "$tk" "$tu"
    if [ -z "$unknown" ]; then
      ok 'every var() name is defined by tokens.css or by the app itself'
    else
      fail "var() names no stylesheet defines: $(printf '%s' "$unknown" | tr '\n' ' ') — they resolve to nothing (references/tokens.css is the whole list)"
    fi
  fi
  grep -hqs 'prefers-color-scheme' $appcss \
    && fail 'app CSS uses prefers-color-scheme — the theme comes from ?theme=dark, not from the OS' \
    || ok 'no prefers-color-scheme in app CSS'
fi

printf '\n%s\n' "$fails FAIL, $warns WARN"
[ "$fails" = 0 ] || exit 1
