#!/usr/bin/env bash
# add-brand.sh
# ============
# Interactively scaffold a new brand DESIGN.md in assets/design-md/<slug>/.
#
# Why this exists:
# - XDesign ships 58 brands as DESIGN.md. Adding a 59th is repetitive work.
# - Without a template, the agent improvises a structure and over time
#   the catalog drifts (some brands have 5 fields, some have 30).
# - This script enforces a stable schema and writes a well-formed file.
#
# Usage:
#   ./scripts/add-brand.sh <slug> <display-name> [primary-color-hex]
#
# Example:
#   ./scripts/add-brand.sh shopify Shopify #95BF47

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <slug> <display-name> [primary-color-hex]" >&2
  exit 1
fi

SLUG="$1"
NAME="$2"
COLOR="${3:-#000000}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="$SKILL_ROOT/assets/design-md/$SLUG"

if [[ -d "$OUT_DIR" ]]; then
  echo "[ERR] $OUT_DIR already exists. Refusing to overwrite." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

cat > "$OUT_DIR/DESIGN.md" <<EOF
# $NAME — Design System

> Slug: \`$SLUG\`
> Primary color: \`$COLOR\`
> Last updated: $(date -u +"%Y-%m-%d")

## Identity
- **Display name:** $NAME
- **Slug:** $SLUG
- **Industry:** TODO
- **Brand voice:** TODO (3-5 adjectives, e.g. "playful, technical, trustworthy")

## Color tokens

| Token | Hex | Usage |
|---|---|---|
| \`--color-primary\`   | $COLOR | CTAs, links, brand moments |
| \`--color-bg\`        | #ffffff | Page background |
| \`--color-surface\`   | TODO   | Cards, elevated surfaces |
| \`--color-text-1\`    | TODO   | Primary text |
| \`--color-text-2\`    | TODO   | Secondary text |
| \`--color-border\`    | TODO   | Dividers, hairlines |
| \`--color-success\`   | TODO   | Positive states |
| \`--color-warning\`   | TODO   | Caution states |
| \`--color-danger\`    | TODO   | Destructive states |

## Typography
- **Display font:** TODO
- **Body font:** TODO
- **Mono font:** TODO
- **Type scale:** TODO (1.125 / 1.2 / 1.25 modular ratio)

## Geometry
- **Corner radius (default):** TODO
- **Spacing scale:** TODO (4 / 8 / 12 / 16 / 24 / 32 / 48)
- **Shadow elevation:** TODO

## Iconography
- **Style:** TODO (line / filled / duotone)
- **Stroke width:** TODO
- **Library:** TODO (Lucide / Tabler / Phosphor / custom)

## Component signatures
- **Buttons:** TODO (shape, hierarchy, primary/secondary/destructive variants)
- **Inputs:** TODO (border style, focus ring, error state)
- **Cards:** TODO (radius, shadow, padding)

## Anti-patterns
- ❌ Don't use colors outside the token palette without explicit override
- ❌ Don't mix this brand's font with another brand's in the same canvas
- ❌ Don't drop the corner radius below the brand minimum (it kills consistency)

## Source references
- TODO (website URL, brand guidelines, screenshot)

## Notes for downstream agents
- When asked to design "in the style of $NAME", pull tokens from this file first.
- Don't add fields that aren't filled in — they confuse the next consumer.
EOF

# Append to the catalog index so the new brand shows up
CATALOG="$SKILL_ROOT/references/design-system-catalog.md"
if [[ -f "$CATALOG" ]]; then
  # Insert a bullet under the "## Brands" heading (idempotent: skip if already present)
  if ! grep -q "\`$SLUG\`" "$CATALOG"; then
    # Use awk to inject the new entry
    awk -v slug="$SLUG" -v name="$NAME" '
      /^## Brands/ { print; in_brands=1; next }
      in_brands && /^## / { print "- `" slug "` — " name; in_brands=0 }
      { print }
      END { if (in_brands) print "- `" slug "` — " name }
    ' "$CATALOG" > "$CATALOG.tmp" && mv "$CATALOG.tmp" "$CATALOG"
  fi
fi

echo "[OK] Scaffolded brand: $OUT_DIR/DESIGN.md"
echo "     Next: fill in the TODO fields, then commit."
