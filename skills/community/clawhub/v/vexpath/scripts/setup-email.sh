#!/usr/bin/env bash
# setup-email.sh — Auto-configure himalaya for Gmail, Outlook, or Hostinger
# Usage: ./setup-email.sh <email> "<Display Name>" "<app-password>"
# Example: ./setup-email.sh you@gmail.com "Jane Smith" "abcd efgh ijkl mnop"

set -euo pipefail

# ── Args ──────────────────────────────────────────────────────────────────────
if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <email> \"<Display Name>\" \"<app-password>\""
  exit 1
fi

EMAIL="$1"
DISPLAY_NAME="$2"
APP_PASSWORD="$(echo "$3" | tr -d ' ')"
DOMAIN="${EMAIL##*@}"

# ── Provider Detection ────────────────────────────────────────────────────────
case "$DOMAIN" in
  gmail.com | googlemail.com)
    PROVIDER="Gmail"
    IMAP_HOST="imap.gmail.com"
    IMAP_PORT=993
    SMTP_HOST="smtp.gmail.com"
    SMTP_PORT=465
    ;;
  outlook.com | hotmail.com | live.com | msn.com)
    PROVIDER="Outlook"
    IMAP_HOST="outlook.office365.com"
    IMAP_PORT=993
    SMTP_HOST="smtp.office365.com"
    SMTP_PORT=587
    ;;
  *)
    PROVIDER="Hostinger"
    IMAP_HOST="imap.hostinger.com"
    IMAP_PORT=993
    SMTP_HOST="smtp.hostinger.com"
    SMTP_PORT=465
    ;;
esac

echo "Detected provider: $PROVIDER"
echo "Email: $EMAIL"
echo "IMAP: $IMAP_HOST:$IMAP_PORT"
echo "SMTP: $SMTP_HOST:$SMTP_PORT"

# ── Config Directory ──────────────────────────────────────────────────────────
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/himalaya"
CONFIG_FILE="$CONFIG_DIR/config.toml"
mkdir -p "$CONFIG_DIR"

# Derive account name from domain
ACCOUNT_NAME=$(echo "$DOMAIN" | sed 's/\..*//' | tr '[:upper:]' '[:lower:]')

# ── Backup Existing Config ────────────────────────────────────────────────────
if [[ -f "$CONFIG_FILE" ]]; then
  cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%s)"
  echo "Existing config backed up"
fi

# ── Write Config ──────────────────────────────────────────────────────────────
cat > "$CONFIG_FILE" << TOML
[accounts.${ACCOUNT_NAME}]
default = true
email = "${EMAIL}"
display-name = "${DISPLAY_NAME}"
downloads-dir = "~/Downloads"

backend.type = "imap"
backend.host = "${IMAP_HOST}"
backend.port = ${IMAP_PORT}
backend.login = "${EMAIL}"
backend.encryption.type = "tls"
backend.auth.type = "password"
backend.auth.raw = "${APP_PASSWORD}"

message.send.backend.type = "smtp"
message.send.backend.host = "${SMTP_HOST}"
message.send.backend.port = ${SMTP_PORT}
message.send.backend.login = "${EMAIL}"
message.send.backend.encryption.type = "tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.raw = "${APP_PASSWORD}"
TOML

chmod 600 "$CONFIG_FILE"
echo ""
echo "Config written to: $CONFIG_FILE (permissions: 600)"
echo "Account name: $ACCOUNT_NAME"

# ── Test Connection ───────────────────────────────────────────────────────────
echo ""
echo "Testing connection..."

if command -v himalaya &>/dev/null; then
  if himalaya folder list 2>&1 | head -5; then
    echo ""
    echo "✓ Connection successful. Email configured for $EMAIL"
  else
    echo ""
    echo "✗ Connection failed."
    echo ""
    echo "Troubleshooting:"
    echo "  - Gmail: Ensure IMAP is enabled and you used an app password"
    echo "  - Outlook: Verify IMAP is enabled in account settings"
    echo "  - Hostinger: Check your email password and account exists"
    echo "  - Try removing spaces from app password"
    echo "  - See references/gmail-setup.md for detailed help"
    exit 1
  fi
else
  echo ""
  echo "himalaya not found. Config written — install himalaya to test."
  echo "  brew install himalaya  OR  cargo install himalaya"
fi
