#!/usr/bin/env bash
#
# install-thetix-skill.sh
#
# Installs the thetix skill into OpenClaw by symlinking into
# ~/.openclaw/skills/thetix and configuring credentials in
# ~/.openclaw/openclaw.json.
#
# Safe to re-run (idempotent) — updates symlink and config on each run.
#
# Usage:
#   bash scripts/install-thetix-skill.sh          # from repo root
#   bash /path/to/install-thetix-skill.sh         # from anywhere

set -euo pipefail

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

info()  { printf '\n\033[1;34m==>\033[0m \033[1m%s\033[0m\n' "$*"; }
warn()  { printf '\033[1;33mWARN:\033[0m %s\n' "$*"; }
error() { printf '\033[1;31mERROR:\033[0m %s\n' "$*" >&2; exit 1; }

# --------------------------------------------------------------------------
# Step 1: Detect skill source directory
# --------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SOURCE="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ ! -f "$SKILL_SOURCE/SKILL.md" ]; then
    error "SKILL.md not found in $SKILL_SOURCE. Run this script from the thetaedge-skill repo."
fi

info "Skill source: $SKILL_SOURCE"

# --------------------------------------------------------------------------
# Step 2: Symlink into ~/.openclaw/skills/thetix
# --------------------------------------------------------------------------

OPENCLAW_SKILLS_DIR="$HOME/.openclaw/skills"

info "Installing thetix skill into $OPENCLAW_SKILLS_DIR/thetix..."

mkdir -p "$OPENCLAW_SKILLS_DIR"
ln -sfn "$SKILL_SOURCE" "$OPENCLAW_SKILLS_DIR/thetix"

info "Symlink created."

# --------------------------------------------------------------------------
# Step 3: Prompt for credentials and write openclaw.json
# --------------------------------------------------------------------------

OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

info "Configuring ThetaEdge credentials..."

# Prompt for API base URL
read -rp "ThetaEdge API base URL [http://localhost:3200]: " api_base
api_base="${api_base:-http://localhost:3200}"

# Prompt for API key (hidden input)
echo "Enter your ThetaEdge API key (input is hidden):"
read -rs api_key
echo ""

if [ -z "$api_key" ]; then
    warn "No API key entered. You can set it later in $OPENCLAW_CONFIG"
    api_key=""
fi

# Build or merge openclaw.json
if [ -f "$OPENCLAW_CONFIG" ]; then
    info "Merging thetix config into existing $OPENCLAW_CONFIG..."

    # Use a temp file for safe in-place update
    tmp_config="$(mktemp)"

    # If python3 is available, use it for proper JSON merge
    if command -v python3 &>/dev/null; then
        python3 -c "
import json, sys

with open('$OPENCLAW_CONFIG') as f:
    config = json.load(f)

config.setdefault('skills', {}).setdefault('entries', {})
config['skills']['entries']['thetix'] = {
    'enabled': True,
    'env': {
        'THETAEDGE_API_KEY': '''$api_key''',
        'THETAEDGE_API_BASE': '''$api_base'''
    }
}

with open('$tmp_config', 'w') as f:
    json.dump(config, f, indent=2)
    f.write('\n')
"
        mv "$tmp_config" "$OPENCLAW_CONFIG"
    else
        # Fallback: overwrite with just our config (no merge without python3)
        warn "python3 not found — overwriting openclaw.json (no merge)."
        rm -f "$tmp_config"
        cat > "$OPENCLAW_CONFIG" <<JSONEOF
{
  "skills": {
    "entries": {
      "thetix": {
        "enabled": true,
        "env": {
          "THETAEDGE_API_KEY": "$api_key",
          "THETAEDGE_API_BASE": "$api_base"
        }
      }
    }
  }
}
JSONEOF
    fi
else
    info "Creating $OPENCLAW_CONFIG..."
    cat > "$OPENCLAW_CONFIG" <<JSONEOF
{
  "skills": {
    "entries": {
      "thetix": {
        "enabled": true,
        "env": {
          "THETAEDGE_API_KEY": "$api_key",
          "THETAEDGE_API_BASE": "$api_base"
        }
      }
    }
  }
}
JSONEOF
fi

chmod 600 "$OPENCLAW_CONFIG"

# Clear sensitive variable
unset api_key

# --------------------------------------------------------------------------
# Step 4: Verify
# --------------------------------------------------------------------------

info "Verifying installation..."

if [ -L "$OPENCLAW_SKILLS_DIR/thetix" ] && [ -f "$OPENCLAW_SKILLS_DIR/thetix/SKILL.md" ]; then
    info "Symlink OK — $OPENCLAW_SKILLS_DIR/thetix -> $(readlink "$OPENCLAW_SKILLS_DIR/thetix")"
else
    error "Symlink verification failed. $OPENCLAW_SKILLS_DIR/thetix/SKILL.md not found."
fi

if [ -f "$OPENCLAW_CONFIG" ]; then
    info "Config OK — $OPENCLAW_CONFIG exists (permissions: $(stat -c '%a' "$OPENCLAW_CONFIG" 2>/dev/null || stat -f '%Lp' "$OPENCLAW_CONFIG" 2>/dev/null))"
else
    error "Config verification failed. $OPENCLAW_CONFIG not found."
fi

# --------------------------------------------------------------------------
# Step 5: Summary
# --------------------------------------------------------------------------

echo ""
echo "============================================"
echo "  thetix skill installed successfully"
echo "============================================"
echo ""
echo "  Skill symlink: ~/.openclaw/skills/thetix -> $SKILL_SOURCE"
echo "  Config file:   ~/.openclaw/openclaw.json"
echo "  API base:      $api_base"
echo ""
echo "Next steps:"
echo "  1. Start Claude Code:  claude"
echo "  2. Test the skill:     /thetix"
echo ""
echo "To update credentials later, re-run this script or edit:"
echo "  ~/.openclaw/openclaw.json"
echo ""
echo "============================================"
