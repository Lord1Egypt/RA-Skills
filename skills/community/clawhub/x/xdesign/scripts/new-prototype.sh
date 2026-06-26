#!/usr/bin/env bash
# new-prototype.sh
# =================
# Scaffold a new Mode 2 (Visual Design / Prototype) project.
#
# Why this exists:
# - Mode 2 projects need a specific starter HTML with React+Babel via CDN,
#   design-token CSS variables, and a clean file structure.
# - Inlining the boilerplate every time produces inconsistent output.
# - This script gives the agent (or the user) a one-shot starter.
#
# Usage:
#   ./scripts/new-prototype.sh <project-name> [brand-slug]
#
# Example:
#   ./scripts/new-prototype.sh my-saas-dashboard linear
#   ./scripts/new-prototype.sh my-coffee-site stripe
#
# If brand-slug matches a DESIGN.md in assets/design-md/, the script
# pre-fills the design tokens from that file. Otherwise it leaves
# placeholder tokens for the user to fill in.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-name> [brand-slug]" >&2
  exit 1
fi

PROJECT_NAME="$1"
BRAND_SLUG="${2:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="$SKILL_ROOT/prototypes/$PROJECT_NAME"

if [[ -d "$OUT_DIR" ]]; then
  echo "[ERR] $OUT_DIR already exists. Pick a different project-name." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# Pre-fill tokens if the brand exists
TOKENS_CSS=":root {
  --color-bg:      #ffffff;
  --color-surface: #f7f7f8;
  --color-text:    #0a0a0a;
  --color-text-2:  #6b6b6b;
  --color-accent:  #3b5bff;
  --color-border:  #e5e5e5;
  --radius:        12px;
  --shadow:        0 1px 3px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06);
  --font-sans:     'Inter', system-ui, -apple-system, sans-serif;
}"
if [[ -n "$BRAND_SLUG" ]]; then
  DESIGN_MD="$SKILL_ROOT/assets/design-md/$BRAND_SLUG/DESIGN.md"
  if [[ -f "$DESIGN_MD" ]]; then
    echo "[INFO] Pre-filling tokens from $DESIGN_MD"
    # Crude extraction: pull "Color" lines from the first table.
    # Real agents will refine at runtime.
    TOKENS_CSS="$TOKENS_CSS
/* Tokens auto-extracted from $BRAND_SLUG/DESIGN.md */
$(grep -E '^\|' "$DESIGN_MD" | head -20 || true)"
  else
    echo "[WARN] No DESIGN.md for brand '$BRAND_SLUG' at $DESIGN_MD"
    echo "       Skipping pre-fill. User/agent will need to set tokens."
  fi
fi

cat > "$OUT_DIR/tokens.css" <<EOF
$TOKENS_CSS
EOF

cat > "$OUT_DIR/index.html" <<'HTMLEOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>__PROJECT_NAME__</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="tokens.css">
  <style>
    body { margin: 0; font-family: var(--font-sans); background: var(--color-bg); color: var(--color-text); }
    .app { display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }
    .nav { background: var(--color-surface); border-right: 1px solid var(--color-border); padding: 24px; }
    .nav h1 { font-size: 18px; margin: 0 0 24px; }
    .nav a { display: block; padding: 10px 12px; border-radius: var(--radius); color: var(--color-text-2); text-decoration: none; }
    .nav a:hover { background: var(--color-bg); color: var(--color-text); }
    .main { padding: 48px; }
    .card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); }
  </style>
</head>
<body>
  <div class="app">
    <aside class="nav">
      <h1>__PROJECT_NAME__</h1>
      <a href="#">Overview</a>
      <a href="#">Detail</a>
      <a href="#">Settings</a>
    </aside>
    <main class="main">
      <div class="card">Hello, __PROJECT_NAME__.</div>
    </main>
  </div>
</body>
</html>
HTMLEOF

# Substitute project name (sed is fine here; we control the source)
sed -i '' "s/__PROJECT_NAME__/$PROJECT_NAME/g" "$OUT_DIR/index.html" 2>/dev/null \
  || sed -i "s/__PROJECT_NAME__/$PROJECT_NAME/g" "$OUT_DIR/index.html"

cat > "$OUT_DIR/README.md" <<EOF
# $PROJECT_NAME

Mode 2 (Visual Design) prototype scaffolded by \`scripts/new-prototype.sh\`.

## Run
Open \`index.html\` in a browser. No build step.

## Customize
- Edit \`tokens.css\` to override design tokens.
- Replace the body of \`index.html\` with your screens.
- For multi-page apps, duplicate \`index.html\` and adjust the nav links.

## Source
EOF
if [[ -n "$BRAND_SLUG" ]]; then
  echo "- Design tokens: \`assets/design-md/$BRAND_SLUG/DESIGN.md\`" >> "$OUT_DIR/README.md"
fi

echo "[OK] Scaffolded: $OUT_DIR"
echo "     Open: $OUT_DIR/index.html"
