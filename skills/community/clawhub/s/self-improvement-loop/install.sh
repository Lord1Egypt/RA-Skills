#!/bin/bash
# install.sh — self-improvement-loop v4.6.13 installer
# v4.6.12: A/B/C/D reference injection into per-agent workspace AGENTS.md + memory.md
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${HOME}/.openclaw/workspace"
CANONICAL_DIR="$WORKSPACE/skills/self-improvement-loop/scripts"
CANONICAL_HOOKS="${HOME}/.openclaw/hooks/self-improvement"
SKILL_HOOKS="$SCRIPT_DIR/hooks"
SKILL_SCRIPTS="$SCRIPT_DIR/scripts"
LEARNINGS_DIR="$WORKSPACE/.learnings"
SKILL_CREATOR_SLUG="yixinli867/skill-creator-2"
SKILL_IMPROVEMENT_SLUG="acautomata/skill-improvement"
OPENCLAW_JSON="${HOME}/.openclaw/openclaw.json"

# ─────────────────────────────────────────────────────────────
# Helper: load per-agent workspaces from openclaw.json
# Returns: agent_id:workspace pairs, one per line
# ─────────────────────────────────────────────────────────────
load_agent_workspaces() {
    python3 -c "
import json, os
path = os.path.expanduser('$OPENCLAW_JSON')
if not os.path.exists(path):
    print(''); exit()
with open(path) as f:
    d = json.load(f)
agents = d.get('agents', {}).get('list', [])
for agent in agents:
    aid = agent.get('id', 'main')
    ws = agent.get('workspace', os.path.expanduser('~/.openclaw/workspace'))
    print(f'{aid}:{ws}')
" 2>/dev/null
}

# ─────────────────────────────────────────────────────────────
# Helper: detect available channels from openclaw.json
# Returns: channel name (e.g. "telegram") or empty
# Sets global CHANNEL and CHANNEL_ACCOUNT
# ─────────────────────────────────────────────────────────────
detect_channel() {
    python3 -c "
import json, os, sys

path = os.path.expanduser('$OPENCLAW_JSON')
if not os.path.exists(path):
    print(''); sys.exit(0)

with open(path) as f:
    d = json.load(f)

channels = d.get('channels', {})
available = []
for name, cfg in channels.items():
    accounts = cfg.get('accounts', {}) if isinstance(cfg, dict) else {}
    if accounts:
        # Pick first available account
        first_account = list(accounts.keys())[0]
        print(f'{name}:{first_account}')
        available.append(name)

if not available:
    print('')
" 2>/dev/null
}

# ─────────────────────────────────────────────────────────────
# Helper: detect user ID from first available channel
# ─────────────────────────────────────────────────────────────
detect_user_id() {
    python3 -c "
import json, os
path = os.path.expanduser('$OPENCLAW_JSON')
if not os.path.exists(path):
    print(''); exit()
with open(path) as f:
    d = json.load(f)
channels = d.get('channels', {})
# Use first available channel
for name, cfg in channels.items():
    if isinstance(cfg, dict):
        accounts = cfg.get('accounts', {})
        for acc_name, acc_cfg in accounts.items():
            ids = acc_cfg.get('allowFrom', [])
            if ids:
                print(ids[0]); exit()
        ids = cfg.get('allowFrom', [])
        if ids:
            print(ids[0]); exit()
print('')
" 2>/dev/null
}

# ─────────────────────────────────────────────────────────────
# Helper: check if skill-creator is installed
# ─────────────────────────────────────────────────────────────
is_skill_creator_installed() {
    [ -d "$WORKSPACE/skills/skill-creator" ]
}

# ─────────────────────────────────────────────────────────────
# Helper: run skill-creator install (non-interactive)
# ─────────────────────────────────────────────────────────────
install_skill_creator() {
    echo "  Installing skill-creator..."
    local output
    output=$(openclaw skill install "https://clawhub.ai/$SKILL_CREATOR_SLUG" 2>&1) && return 0
    echo "  ⚠ skill-creator install output: $output"
    return 1
}

# ─────────────────────────────────────────────────────────────
# Helper: check if skill-improvement is installed
# ─────────────────────────────────────────────────────────────
is_skill_improvement_installed() {
    [ -d "$WORKSPACE/skills/skill-improvement" ]
}

# ─────────────────────────────────────────────────────────────
# Helper: install skill-improvement (non-interactive)
# ─────────────────────────────────────────────────────────────
install_skill_improvement() {
    echo "  Installing skill-improvement..."
    local output
    output=$(openclaw skill install "https://clawhub.ai/$SKILL_IMPROVEMENT_SLUG" 2>&1) && return 0
    echo "  ⚠ skill-improvement install output: $output"
    return 1
}

# ─────────────────────────────────────────────────────────────
# 0. Pre-flight: python3 + skill-creator + skill-improvement + channel detection
# ─────────────────────────────────────────────────────────────
echo "=== self-improvement-loop v4.6.13 installer ==="
echo ""

if ! command -v python3 &>/dev/null; then
    echo "[✗] python3 not found. This skill requires Python 3."
    echo "    Install python3 and retry."
    exit 1
fi
echo "[✓] python3: found"

if is_skill_creator_installed; then
    echo "[✓] skill-creator: found, skipping"
else
    echo "[✓] skill-creator: not found, installing..."
    if install_skill_creator; then
        echo "  ✓ skill-creator installed"
    else
        echo "  ⚠ skill-creator install failed. Run manually after install:"
        echo "    openclaw skill install https://clawhub.ai/$SKILL_CREATOR_SLUG"
    fi
fi

if is_skill_improvement_installed; then
    echo "[✓] skill-improvement: found, skipping"
else
    echo "[✓] skill-improvement: not found, installing..."
    if install_skill_improvement; then
        echo "  ✓ skill-improvement installed"
    else
        echo "  ⚠ skill-improvement install failed. Run manually after install:"
        echo "    openclaw skill install https://clawhub.ai/$SKILL_IMPROVEMENT_SLUG"
        echo "  Note: skill-improvement is required for B path (optimize existing skill)"
    fi
fi

# Detect available channels
echo ""
echo "[0/9] Detecting notification channels..."
CHANNEL_LIST=$(detect_channel)
CHANNEL_COUNT=$(echo "$CHANNEL_LIST" | grep -c ":" || echo 0)

if [ "$CHANNEL_COUNT" -eq 0 ]; then
    echo "  ⚠ No channels detected in openclaw.json."
    echo "    Configure at least one channel (e.g. Telegram, Slack, Discord) before installing."
    echo "    Installation aborted."
    exit 1
elif [ "$CHANNEL_COUNT" -eq 1 ]; then
    CHANNEL_INFO=$(echo "$CHANNEL_LIST" | grep ":")
    export CHANNEL=$(echo "$CHANNEL_INFO" | cut -d: -f1)
    export CHANNEL_ACCOUNT=$(echo "$CHANNEL_INFO" | cut -d: -f2)
    echo "  ✓ Detected channel: $CHANNEL (account: $CHANNEL_ACCOUNT)"
else
    echo "  ⚠ Multiple channels detected:"
    echo "$CHANNEL_LIST" | while IFS=: read -r ch acc; do
        echo "    - $ch (account: $acc)"
    done
    echo "  Please specify which channel to use by setting CHANNEL env var:"
    echo "    CHANNEL=telegram CHANNEL_ACCOUNT=default bash install.sh"
    echo "  Installation aborted."
    exit 1
fi

# ── 1. Create directories ───────────────────────────────
echo ""
echo "[1/9] Creating directories..."
mkdir -p "$CANONICAL_HOOKS"

# Create per-agent .learnings directories
AGENTS_INFO=$(load_agent_workspaces)
if [ -n "$AGENTS_INFO" ]; then
    echo "  Per-agent workspaces:"
    echo "$AGENTS_INFO" | while IFS=: read -r agent_id workspace; do
        agent_learnings="${workspace}/.learnings"
        mkdir -p "$agent_learnings"
        mkdir -p "$agent_learnings/.pending_notifications"
        echo "    ✓ $agent_id: $agent_learnings"
    done
else
    # Fallback: main workspace only
    mkdir -p "$LEARNINGS_DIR"
    mkdir -p "$LEARNINGS_DIR/.pending_notifications"
    echo "  ✓ $LEARNINGS_DIR"
fi

# ── 2. Install Hook ────────────────────────────────────
echo ""
echo "[2/9] Installing Hook..."
cp "$SKILL_HOOKS/handler.js" "$CANONICAL_HOOKS/handler.js"
cp "$SKILL_HOOKS/HOOK.md" "$CANONICAL_HOOKS/HOOK.md"
echo "  ✓ handler.js + HOOK.md → $CANONICAL_HOOKS/"

# ── 3. Install scripts ─────────────────────────────────
echo ""
echo "[3/9] Scripts location..."
echo "  ✓ scripts stay in skill: $CANONICAL_DIR/"

# ── 4. Initialize learnings files ──────────────────────
echo ""
echo "[4/9] Initializing learnings files..."
init_learnings_for_workspace() {
    local learnings_dir=$1
    local agent_name=$2

    for f in LEARNINGS.md ERRORS.md FEATURE_REQUESTS.md; do
        target="$learnings_dir/$f"
        if [ ! -f "$target" ]; then
            # Tier 1: file missing → copy template
            cp "$SCRIPT_DIR/learnings/$f" "$target"
            echo "    ✓ $f"
        elif [ ! -s "$target" ]; then
            # Tier 2: file exists but empty → append template
            cat "$SCRIPT_DIR/learnings/$f" >> "$target"
            echo "    ✓ $f (appended to empty)"
        else
            # Tier 3: file has content → check format
            # v4.6.13: replace if format is outdated (no Pattern-Key field)
            if grep -q "<source>" "$target" 2>/dev/null; then
                echo "    - $f (exists, format OK)"
            else
                cp "$SCRIPT_DIR/learnings/$f" "$target"
                echo "    ✓ $f (format outdated, replaced)"
            fi
        fi
    done
}

# Initialize per-agent workspaces
AGENTS_INFO=$(load_agent_workspaces)
if [ -n "$AGENTS_INFO" ]; then
    echo "$AGENTS_INFO" | while IFS=: read -r agent_id workspace; do
        agent_learnings="${workspace}/.learnings"
        if [ "$agent_id" = "main" ] && [ "$workspace" = "$WORKSPACE" ]; then
            # Main agent with default workspace
            echo "  main:"
            init_learnings_for_workspace "$agent_learnings" "main"
        else
            echo "  $agent_id:"
            init_learnings_for_workspace "$agent_learnings" "$agent_id"
        fi
    done
else
    # Fallback: main workspace only
    echo "  main:"
    init_learnings_for_workspace "$LEARNINGS_DIR" "main"
fi

# ── 5. Register Hook ───────────────────────────────────
echo ""
echo "[5/9] Registering Hook..."
# Skip openclaw hooks list (hangs in some environments) — verify from config instead
if grep -q '"self-improvement"' "$OPENCLAW_JSON" 2>/dev/null; then
    echo "  ✓ Hook already registered in config, skipped"
else
    openclaw hooks install self-improvement "$CANONICAL_HOOKS/handler.js" 2>/dev/null \
        && echo "  ✓ Hook registered" \
        || echo "  ⚠ Hook registration failed. Run manually:"
    echo "    openclaw hooks set self-improvement $CANONICAL_HOOKS/handler.js"
fi

# ── 6. Setup Cron jobs ─────────────────────────────────
echo ""
echo "[6/9] Writing bindings BEFORE cron setup (required for correct per-agent accountId)..."
OPENCLAW_JSON_PATH="${HOME}/.openclaw/openclaw.json"
python3 << PYEOF
import json, os

path = os.path.expanduser('$OPENCLAW_JSON_PATH')
if not os.path.exists(path):
    print('  ⚠ openclaw.json not found, skipping bindings')
else:
    with open(path) as f:
        config = json.load(f)

    channels_cfg = config.get('channels', {})
    first_channel = None
    first_channel_account = None
    first_accounts_cfg = {}
    for channel_name, cfg in channels_cfg.items():
        if isinstance(cfg, dict):
            accounts = cfg.get('accounts', {})
            if accounts:
                first_channel = channel_name
                first_channel_account = list(accounts.keys())[0]
                first_accounts_cfg = accounts
                break

    if not first_channel:
        print('  ⚠ No channels found')
    else:
        default_account = channels_cfg.get(first_channel, {}).get('defaultAccount', first_channel_account)
        agents_list = config.get('agents', {}).get('list', [])
        if not agents_list:
            print('  ⚠ No agents found')
        else:
            def map_agent_to_account(agent_id, accounts_cfg, default_account):
                if agent_id in accounts_cfg:
                    return agent_id
                if agent_id == 'main' and 'default' in accounts_cfg:
                    return 'default'
                for acc in accounts_cfg:
                    if agent_id.startswith(acc) or acc.startswith(agent_id):
                        return acc
                if '-' in agent_id:
                    prefix = agent_id.split('-')[0]
                    for acc in accounts_cfg:
                        if acc.startswith(prefix):
                            return acc
                return default_account

            bindings = []
            for agent in agents_list:
                agent_id = agent.get('id', 'main')
                if agent_id == 'claude':
                    continue
                account = map_agent_to_account(agent_id, first_accounts_cfg, default_account)
                if account not in first_accounts_cfg:
                    continue
                bindings.append({
                    'agentId': agent_id,
                    'match': {
                        'channel': first_channel,
                        'accountId': account
                    }
                })

            if bindings:
                config['bindings'] = bindings
                with open(path, 'w') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                print(f'  ✓ Bindings written (channel: {first_channel})')
                for b in bindings:
                    print(f"    - {b['agentId']} → {first_channel}/{b['match']['accountId']}")
            else:
                print('  ⚠ No bindings to add')
PYEOF

echo ""
echo "[7/9] Setting up per-agent Cron jobs..."
TELEGRAM_ID=$(detect_user_id)
if [ -z "$TELEGRAM_ID" ]; then
    echo "  ⚠ Could not auto-detect Telegram user ID."
    echo "    Set TELEGRAM_ID env var or check openclaw.json allowFrom."
else
    echo "  ✓ Detected Telegram ID: $TELEGRAM_ID"
fi

# Show which agents will get crons
AGENTS_INFO=$(load_agent_workspaces)
if [ -n "$AGENTS_INFO" ]; then
    echo "  Will create crons for:"
    echo "$AGENTS_INFO" | while IFS=: read -r agent_id workspace; do
        echo "    - self-improvement-$agent_id → $workspace/.learnings"
    done
fi
echo ""

CHANNEL="$CHANNEL" \
CHANNEL_ACCOUNT="$CHANNEL_ACCOUNT" \
TELEGRAM_ID="$TELEGRAM_ID" \
    python3 "$SKILL_SCRIPTS/setup_crons.py" --force

# ── 7.5. Inject A/B/C/D reference into AGENTS.md and memory.md ──
echo ""
echo "[8/9] Injecting self-improvement reference into per-agent AGENTS.md and memory.md..."

SELF_IMPROVEMENT_REF="## 自我改进（A/B/C/D）

处理 A/B/C/D 之前必须查阅：
skills/self-improvement-loop/scripts/agents-append.md

"

inject_ref() {
    local target_file=$1
    local description=$2

    if [ ! -f "$target_file" ]; then
        echo "  ⚠ $description not found, skipping"
        return
    fi

    # Use python to detect multi-line injection (grep can't match across lines)
    if python3 -c "
import sys
content = open('$target_file').read()
ok = 'A/B/C/D' in content and '必须查阅' in content and 'agents-append' in content
sys.exit(0 if ok else 1)
" 2>/dev/null; then
        echo "  ✓ $description already has reference"
    else
        echo "" >> "$target_file"
        echo "$SELF_IMPROVEMENT_REF" >> "$target_file"
        echo "  ✓ $description: reference injected"
    fi
}

# Inject into each agent's workspace
AGENTS_INFO=$(load_agent_workspaces)
if [ -n "$AGENTS_INFO" ]; then
    echo "$AGENTS_INFO" | while IFS=: read -r agent_id workspace; do
        echo "  $agent_id:"
        inject_ref "$workspace/AGENTS.md" "  AGENTS.md"
        inject_ref "$workspace/memory.md" "  memory.md"
    done
else
    echo "  main:"
    inject_ref "$WORKSPACE/AGENTS.md" "  AGENTS.md"
    inject_ref "$WORKSPACE/memory.md" "  memory.md"
fi

# ── 8. Gateway restart reminder ─────────────────────────
echo ""
echo "[9/9] Gateway restart reminder..."
echo ""
echo "=== Installation complete ==="
echo ""
echo "⚠ Restart gateway to activate Hook:"
echo "   openclaw gateway restart"
echo ""
echo "Verify distill:"
echo "   bash $CANONICAL_DIR/distill.sh --check-only"
echo ""
echo "Check Cron status:"
echo "   openclaw cron list | grep self-improvement"
