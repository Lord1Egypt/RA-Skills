#!/usr/bin/env bash
# unified-mailbox-ai installer
# Installs the skill into ~/.openclaw/workspace/skills/ and helps configure env vars + cron.

set -e

SKILL_NAME="unified-mailbox-ai"
SKILL_DIR="$HOME/.openclaw/workspace/skills/$SKILL_NAME"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
SCRIPT_PATH="$SKILL_DIR/scripts/unified_mailbox_ai.py"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Colors ──────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()    { echo -e "${BLUE}[i]${NC} $*"; }
success() { echo -e "${GREEN}[✓]${NC} $*"; }
warn()    { echo -e "${YELLOW}[!]${NC} $*"; }
error()   { echo -e "${RED}[✗]${NC} $*" >&2; }
ask()     { read -r -p "$(echo -e "${YELLOW}[?]${NC} $1 ")" "$2"; }

echo "============================================"
echo "  unified-mailbox-ai skill installer"
echo "============================================"
echo

# ── Step 1: Preflight ────────────────────────────────────────────────────
info "Checking prerequisites..."

if ! command -v python3 >/dev/null 2>&1; then
    error "python3 not found. Please install Python 3.8 or newer."
    exit 1
fi
success "python3 found: $(python3 --version)"

if ! command -v openclaw >/dev/null 2>&1; then
    warn "openclaw command not found in PATH."
    warn "The skill itself will install, but you need OpenClaw to actually use it."
    warn "Install from https://openclaw.ai if you haven't already."
fi

if [ ! -d "$HOME/.openclaw" ]; then
    error "~/.openclaw does not exist. Run 'openclaw configure' first to set up OpenClaw."
    exit 1
fi
success "OpenClaw directory found"

# Check msal
if ! python3 -c "import msal" 2>/dev/null; then
    warn "Python package 'msal' is not installed (required for Outlook support)."
    ask "Install it now with pip? [y/N]" install_msal
    if [[ "$install_msal" =~ ^[Yy]$ ]]; then
        pip install --user msal || pip3 install --user msal
        success "msal installed"
    else
        warn "Skipping. You'll need to install msal manually if you use Outlook."
    fi
else
    success "Python package 'msal' is installed"
fi

# Check gog
HAS_GOG=0
if command -v gog >/dev/null 2>&1; then
    success "gog CLI found: $(gog --version 2>&1 | head -1 || echo unknown)"
    HAS_GOG=1
else
    warn "gog CLI not found (required for Gmail support)."
    warn "Install from https://gogcli.sh if you want Gmail monitoring."
fi
echo

# ── Step 2: Copy files ──────────────────────────────────────────────────
info "Installing skill files to $SKILL_DIR..."
mkdir -p "$SKILL_DIR/scripts"
cp "$SOURCE_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$SOURCE_DIR/scripts/unified_mailbox_ai.py" "$SKILL_DIR/scripts/unified_mailbox_ai.py"
chmod +x "$SKILL_DIR/scripts/unified_mailbox_ai.py"
success "Skill files installed"
echo

# ── Step 3: Configure mailboxes ─────────────────────────────────────────
info "Mailbox configuration"
echo

ENABLE_OUTLOOK=0
ENABLE_GMAIL=0

if [ -f "$HOME/.openclaw/ms_tokens.json" ]; then
    success "Outlook MSAL token cache found at ~/.openclaw/ms_tokens.json"
    ENABLE_OUTLOOK=1
else
    warn "Outlook MSAL token cache (~/.openclaw/ms_tokens.json) not found."
    warn "If you want Outlook support, install the outlook-graph skill first and complete its OAuth flow."
fi

GMAIL_ACCOUNT=""
if [ "$HAS_GOG" = "1" ]; then
    ask "Enable Gmail monitoring? [y/N]" enable_gmail_input
    if [[ "$enable_gmail_input" =~ ^[Yy]$ ]]; then
        ask "Enter your Gmail address:" GMAIL_ACCOUNT
        if [ -n "$GMAIL_ACCOUNT" ]; then
            ENABLE_GMAIL=1
            success "Will enable Gmail for $GMAIL_ACCOUNT"
        fi
    fi
fi

if [ "$ENABLE_OUTLOOK" = "0" ] && [ "$ENABLE_GMAIL" = "0" ]; then
    error "Neither Outlook nor Gmail will be enabled. Aborting."
    error "Configure at least one mailbox and re-run this installer."
    exit 1
fi
echo

# ── Step 4: Telegram chat ID ────────────────────────────────────────────
info "Telegram configuration"
echo "Your Telegram chat ID is needed so the bot knows where to push notifications."
echo "Tip: message @userinfobot on Telegram to find yours."
ask "Enter your Telegram chat ID:" TELEGRAM_USER

if [ -z "$TELEGRAM_USER" ]; then
    error "Telegram chat ID is required. Aborting."
    exit 1
fi
echo

# ── Step 5: Write env vars to openclaw.json ─────────────────────────────
info "Writing environment variables to $OPENCLAW_CONFIG..."

python3 - "$OPENCLAW_CONFIG" "$TELEGRAM_USER" "$GMAIL_ACCOUNT" <<'PYEOF'
import json, sys
config_path, telegram_user, gmail_account = sys.argv[1:]
with open(config_path) as f:
    config = json.load(f)
config.setdefault('env', {})
config['env']['EMAIL_MONITOR_TELEGRAM_USER'] = telegram_user
if gmail_account:
    config['env']['EMAIL_MONITOR_GMAIL_ACCOUNT'] = gmail_account
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
PYEOF
success "Environment variables written to openclaw.json"

# ── Step 6: Append to ~/.bashrc for terminal use ─────────────────────────
ask "Also export these env vars in ~/.bashrc for terminal use? [Y/n]" add_bashrc
if [[ ! "$add_bashrc" =~ ^[Nn]$ ]]; then
    {
        echo ""
        echo "# unified-mailbox-ai skill (added by installer)"
        echo "export EMAIL_MONITOR_TELEGRAM_USER=\"$TELEGRAM_USER\""
        if [ -n "$GMAIL_ACCOUNT" ]; then
            echo "export EMAIL_MONITOR_GMAIL_ACCOUNT=\"$GMAIL_ACCOUNT\""
            echo "export GOG_KEYRING_PASSWORD=\"\""
        fi
    } >> "$HOME/.bashrc"
    success "Added to ~/.bashrc (run 'source ~/.bashrc' to reload)"
fi
echo

# ── Step 7: Register skill in agent's skills list ───────────────────────
ask "Register unified-mailbox-ai in your main agent's skills list? [Y/n]" register
if [[ ! "$register" =~ ^[Nn]$ ]]; then
    python3 - "$OPENCLAW_CONFIG" <<'PYEOF'
import json, sys
config_path = sys.argv[1]
with open(config_path) as f:
    config = json.load(f)
agents = config.get('agents', {}).get('list', [])
for agent in agents:
    skills = agent.setdefault('skills', [])
    if 'unified-mailbox-ai' not in skills:
        skills.append('unified-mailbox-ai')
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print('Registered unified-mailbox-ai with all agents')
PYEOF
    success "Skill registered"
fi
echo

# ── Step 8: Set up cron ─────────────────────────────────────────────────
ask "Set up a cron job to auto-check every 5 minutes? [Y/n]" setup_cron
if [[ ! "$setup_cron" =~ ^[Nn]$ ]]; then
    GMAIL_ENV=""
    KEYRING_ENV=""
    if [ -n "$GMAIL_ACCOUNT" ]; then
        GMAIL_ENV="EMAIL_MONITOR_GMAIL_ACCOUNT=\"$GMAIL_ACCOUNT\""
        KEYRING_ENV="GOG_KEYRING_PASSWORD=\"\""
    fi
    CRON_LINE="*/5 * * * * PATH=\$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin $KEYRING_ENV $GMAIL_ENV EMAIL_MONITOR_TELEGRAM_USER=\"$TELEGRAM_USER\" /usr/bin/python3 \$HOME/.openclaw/workspace/skills/unified-mailbox-ai/scripts/unified_mailbox_ai.py auto-notify"

    # Remove any prior unified_mailbox_ai cron entries, then append the new one
    (crontab -l 2>/dev/null | grep -v 'unified_mailbox_ai\|email_monitor'; echo "$CRON_LINE") | crontab -
    success "Cron job installed:"
    echo "    $CRON_LINE"
fi
echo

# ── Step 9: Test run ─────────────────────────────────────────────────────
ask "Run a test 'check' now to verify everything works? [Y/n]" do_test
if [[ ! "$do_test" =~ ^[Nn]$ ]]; then
    info "Running: python3 $SCRIPT_PATH check"
    GOG_KEYRING_PASSWORD="" \
    EMAIL_MONITOR_TELEGRAM_USER="$TELEGRAM_USER" \
    EMAIL_MONITOR_GMAIL_ACCOUNT="$GMAIL_ACCOUNT" \
    python3 "$SCRIPT_PATH" check || warn "Test run reported errors. Check the output above."
fi

echo
echo "============================================"
success "Installation complete!"
echo "============================================"
echo
echo "Next steps:"
echo "  - Run 'source ~/.bashrc' to load the new env vars in your current shell"
echo "  - Send /new in your Telegram bot, then ask 'check my email' to test interactively"
if [[ ! "$setup_cron" =~ ^[Nn]$ ]]; then
    echo "  - The cron job will run every 5 minutes; check 'crontab -l' to confirm"
fi
echo
