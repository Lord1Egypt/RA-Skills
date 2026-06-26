#!/usr/bin/env zsh
# setup.sh — one-time setup for wine-archive
set -euo pipefail

SCRIPT_DIR="${0:A:h}"
cd "$SCRIPT_DIR"

echo "wine-archive setup"
echo "=================="

# 1. Check Node version
NODE_VERSION=$(node -e 'process.stdout.write(process.version)' 2>/dev/null || echo "")
if [[ -z "$NODE_VERSION" ]]; then
  echo "Error: Node.js not found. Install Node.js >= 22 and try again."
  exit 1
fi

NODE_MAJOR=$(echo "$NODE_VERSION" | sed 's/v\([0-9]*\).*/\1/')
if [[ "$NODE_MAJOR" -lt 22 ]]; then
  echo "Warning: Node.js $NODE_VERSION detected. Node >= 22 is recommended (needed for node:sqlite in shared/)."
fi

echo "Node: $NODE_VERSION"

# 2. Install npm dependencies
echo ""
echo "Installing dependencies..."
npm install

# 3. Create data directories
echo ""
echo "Creating data directories..."
mkdir -p data/wine/labels

# 4. Initialize the SQLite database
echo ""
echo "Initializing wine database..."
node scripts/wine-service.js init

# 5. Copy .env.example → .env if not already present
if [[ ! -f ".env" ]]; then
  cp .env.example .env
  echo ""
  echo "Created .env from .env.example — add your ANTHROPIC_API_KEY if you want LLM features."
else
  echo ""
  echo ".env already exists — skipping."
fi

echo ""
echo "Setup complete."
echo ""
echo "Quick start:"
echo "  npm run wine:add -- --text \"Had a Broadbent Vinho Verde 2024 from Minho. Bought at Nugget for \$14. Rated 4/5.\""
echo "  npm run wine:list"
echo "  npm run wine:recall -- --text \"show me what I had last week\""
echo ""
echo "To export your archive:"
echo "  npm run wine:export -- --out my-wines.json --include-images"
echo ""
echo "To import an archive:"
echo "  npm run wine:import -- --in my-wines.json"
