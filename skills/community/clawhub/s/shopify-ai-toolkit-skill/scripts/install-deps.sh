#!/usr/bin/env bash
# install-deps.sh — Install dependencies for the Shopify AI Toolkit skill
# Run this once after cloning the skill repo.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "Installing Shopify AI Toolkit skill dependencies..."

# The bundled validate.mjs files are self-contained (no deps needed for admin/graphql validation)
# Liquid validation requires npm packages
if [ -f "$SKILL_DIR/package.json" ]; then
  echo "Note: The GraphQL search/validate scripts (admin, storefront, hydrogen, functions) are"
  echo "self-contained and do not require npm install."
  echo ""
  echo "If you need Liquid validation, install dependencies:"
  echo "  cd $SKILL_DIR && npm install"
fi

echo ""
echo "Done! Set optional env vars:"
echo "  export OPT_OUT_INSTRUMENTATION=true        # disable Shopify telemetry"
echo "  export SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/  # custom base URL"
