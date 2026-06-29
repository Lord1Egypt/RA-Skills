#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# init-dashboard.sh — scaffold a Slidev project pre-wired with DataV (datav-vue3)
# for building 大屏 dashboards.
#
#   bash init-dashboard.sh [target-dir]      # default: ./datav-dashboard
#
# It copies this skill's assets/ + example deck into the right Slidev folders and
# runs `npm install`. Idempotent: re-running refreshes the wiring files.
# Requires: node + npm (no pnpm/git needed).
# ---------------------------------------------------------------------------
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-datav-dashboard}"

echo "▸ DataV × Slidev dashboard scaffold"
echo "  skill:  $SKILL_DIR"
echo "  target: $TARGET"

command -v node >/dev/null 2>&1 || { echo "✗ node not found — install Node.js first."; exit 1; }
command -v npm  >/dev/null 2>&1 || { echo "✗ npm not found — install npm first."; exit 1; }

mkdir -p "$TARGET"/{setup,layouts,styles,components}

cp "$SKILL_DIR/assets/setup/main.ts"          "$TARGET/setup/main.ts"
cp "$SKILL_DIR/assets/vite.config.ts"         "$TARGET/vite.config.ts"
cp "$SKILL_DIR/assets/layouts/dashboard.vue"  "$TARGET/layouts/dashboard.vue"
cp "$SKILL_DIR/assets/styles/dashboard.css"   "$TARGET/styles/dashboard.css"
cp "$SKILL_DIR"/assets/components/*.vue        "$TARGET/components/"
cp "$SKILL_DIR/templates/package.json"        "$TARGET/package.json"

# Don't clobber an existing edited deck; write the example as slides.md only if absent.
if [ -f "$TARGET/slides.md" ]; then
  cp "$SKILL_DIR/templates/slides.example.md" "$TARGET/slides.example.md"
  echo "  • slides.md exists — wrote slides.example.md instead (didn't overwrite your deck)"
else
  cp "$SKILL_DIR/templates/slides.example.md" "$TARGET/slides.md"
fi

echo "▸ Installing dependencies (npm install) …"
( cd "$TARGET" && npm install )

cat <<EOF

✓ Done. Next:

    cd $TARGET
    npm run dev        # → http://localhost:3030  (live big-screen preview)

  Other commands:
    npm run build      # static SPA in dist/  (host on any static server / video wall)
    npm run export     # PDF  (add: -- --format png  for images, -- --scale 2 for crisp output)

  Files to edit:
    slides.md              your deck (headmatter already set to 1920×1080)
    styles/dashboard.css   palette tokens (--dv-*) ; add 'theme-purple'/'theme-green' to <html> to switch
    components/            DashPanel (titled border box) + DashGrid (1920×1080 grid)

  Reference docs live in this skill:
    references/components.md         all 39 DataV components + props/examples
    references/design-rules.md       大屏 design spec
    references/slidev-integration.md wiring & scaling
    references/troubleshooting.md    fixes
EOF
