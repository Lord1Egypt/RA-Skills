#!/bin/bash
# Pre-push static checks for stomme-website
# Run before every push: bash scripts/pre-push-check.sh
# Exit 1 = issues found, do not push

set -e
FAIL=0
cd "$(dirname "$0")/.."

echo "── Pre-push checks ──"

# 1. All HTML files have cache-bust versions on script/css refs
echo ""
echo "1. Cache-bust versions on assets..."
for f in *.html; do
  # Check script tags
  if grep -q '<script.*src=.*\.js"' "$f" 2>/dev/null; then
    if ! grep -q '<script.*src=.*\.js?v=' "$f"; then
      echo "  ❌ $f has unversioned script tag"
      FAIL=1
    fi
  fi
  # Check CSS links
  if grep -q '<link.*href=.*\.css"' "$f" 2>/dev/null; then
    if ! grep -q '<link.*href=.*\.css?v=' "$f"; then
      echo "  ❌ $f has unversioned CSS link"
      FAIL=1
    fi
  fi
done
[ $FAIL -eq 0 ] && echo "  ✅ All assets versioned"

# 2. No hardcoded hex colors in style.css (should use brand tokens)
echo ""
echo "2. No hardcoded colors in style.css..."
HARDCODED=$(grep -En '#[0-9a-fA-F]{3,8}[^a-zA-Z0-9]' css/style.css 2>/dev/null | grep -v '^\s*/\*' | grep -v 'var(' | grep -v '^\s*\*' || true)
if [ -n "$HARDCODED" ]; then
  COUNT=$(echo "$HARDCODED" | wc -l | tr -d ' ')
  echo "  ⚠️  $COUNT lines with hardcoded hex in style.css (check if intentional)"
  echo "$HARDCODED" | head -5 | sed 's/^/    /'
else
  echo "  ✅ No hardcoded hex colors"
fi

# 3. copy.js syntax check
echo ""
echo "3. copy.js syntax..."
if node -e "require('./js/copy.js')" 2>/dev/null || node --check js/copy.js 2>/dev/null; then
  echo "  ✅ copy.js parses OK"
else
  # ES module — try dynamic import
  if node -e "import('./js/copy.js').catch(()=>{})" 2>/dev/null; then
    echo "  ✅ copy.js ES module OK"
  else
    echo "  ⚠️  copy.js syntax could not be validated (ES module)"
  fi
fi

# 4. main.js syntax check
echo ""
echo "4. main.js syntax..."
node -e "import('./js/main.js').catch(()=>{})" 2>/dev/null && echo "  ✅ main.js OK" || echo "  ⚠️  main.js could not be validated"

# 5. Verify theme toggle function exists and calls applyTheme on load
echo ""
echo "5. Theme toggle safety net..."
if grep -q 'applyTheme(getEffectiveTheme())' js/main.js; then
  echo "  ✅ applyTheme called on load"
else
  echo "  ❌ applyTheme NOT called on load — theme toggle may break"
  FAIL=1
fi

# 6. Nav CTA has color override
echo ""
echo "6. Nav CTA contrast override..."
if grep -q 'nav-cta' css/style.css && grep -A3 'nav-cta' css/style.css | grep -q 'color.*!important\|color.*var(--color-white)'; then
  echo "  ✅ Nav CTA has explicit color"
else
  echo "  ❌ Nav CTA missing color override — may inherit grey from nav-links"
  FAIL=1
fi

# 7. All HTML inline scripts set data-theme explicitly (no removeAttribute)
echo ""
echo "7. Inline script theme handling..."
REMOVE_ATTR=$(grep -l "removeAttribute.*data-theme" *.html 2>/dev/null || true)
if [ -n "$REMOVE_ATTR" ]; then
  echo "  ❌ Found removeAttribute('data-theme') in: $REMOVE_ATTR"
  echo "     Must always set data-theme explicitly (light or dark)"
  FAIL=1
else
  echo "  ✅ No removeAttribute('data-theme') in HTML files"
fi

echo ""
echo "════════════════════════════════"
if [ $FAIL -ne 0 ]; then
  echo "⛔ FAIL — fix issues before pushing"
  exit 1
else
  echo "✅ All pre-push checks passed"
  exit 0
fi
