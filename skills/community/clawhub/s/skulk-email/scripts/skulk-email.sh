#!/usr/bin/env bash
# skulk-email.sh — Email for Skulk agents
# Read via IMAP, send via DreamHost Roundcube (HTTPS)
# Credentials: ~/.config/skulk-email/credentials.json
set -euo pipefail

CRED_FILE="$HOME/.config/skulk-email/credentials.json"
WEBMAIL="https://webmail.dreamhost.com"

die() { echo "✗ $1" >&2; exit 1; }

load_creds() {
    [ -f "$CRED_FILE" ] || die "Credentials not found at $CRED_FILE — see SKILL.md for setup"
    SKULK_EMAIL=$(jq -r '.skulk_email // empty' "$CRED_FILE")
    SKULK_PASS=$(jq -r '.skulk_password // empty' "$CRED_FILE")
    GMAIL_EMAIL=$(jq -r '.gmail_email // empty' "$CRED_FILE")
    GMAIL_PASS=$(jq -r '.gmail_app_password // empty' "$CRED_FILE")
    [ -n "$SKULK_EMAIL" ] || die "skulk_email not set in credentials"
    [ -n "$SKULK_PASS" ] || die "skulk_password not set in credentials"
}

usage() {
    cat <<EOF
Usage: skulk-email.sh <command> [options]

Skulk Email Commands:
  test                        Test connections
  inbox [limit]               List inbox messages (default: 10)
  unread [limit]              List unread messages
  count                       Count unread messages
  read <message-id>           Read a specific message
  send <to> <subject> <body>  Send email as your @skulk.ai address
  search <query> [limit]      Search messages

Shared Gmail Commands:
  gmail-inbox [limit]         List shared Gmail inbox
  gmail-unread [limit]        List shared Gmail unread
  gmail-count                 Count shared Gmail unread
  gmail-read <message-id>     Read shared Gmail message

EOF
}

# ─── IMAP Functions (Python) ───

imap_cmd() {
    local host="$1" port="$2" user="$3" pass="$4" action="$5"
    shift 5
    python3 - "$host" "$port" "$user" "$pass" "$action" "$@" << 'PYEOF'
import imaplib, email, json, sys, os
from email.header import decode_header

host, port, user, passwd, action = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
args = sys.argv[6:]

def decode_subject(msg):
    subj = msg.get("Subject", "(no subject)")
    parts = decode_header(subj)
    result = ""
    for part, charset in parts:
        if isinstance(part, bytes):
            result += part.decode(charset or "utf-8", errors="replace")
        else:
            result += part
    return result

mail = imaplib.IMAP4_SSL(host, port)
mail.login(user, passwd)

if action == "test":
    mail.select("INBOX", readonly=True)
    status, data = mail.select("INBOX", readonly=True)
    print(f"✓ Connected to {host} as {user}")
    print(f"✓ Inbox: {data[0].decode()} messages")

elif action == "count":
    mail.select("INBOX", readonly=True)
    status, data = mail.search(None, "UNSEEN")
    count = len(data[0].split()) if data[0] else 0
    print(f"{count} unread")

elif action in ("inbox", "unread"):
    limit = int(args[0]) if args else 10
    mail.select("INBOX", readonly=True)
    criteria = "UNSEEN" if action == "unread" else "ALL"
    status, data = mail.search(None, criteria)
    ids = data[0].split()
    ids = ids[-limit:] if len(ids) > limit else ids
    ids.reverse()
    if not ids:
        print("No messages" if action == "unread" else "Inbox empty")
    else:
        for mid in ids:
            status, msg_data = mail.fetch(mid, "(FLAGS BODY[HEADER.FIELDS (FROM SUBJECT DATE)])")
            raw = msg_data[0][1]
            flags = msg_data[0][0].decode()
            msg = email.message_from_bytes(raw)
            subject = decode_subject(msg)
            from_addr = msg.get("From", "(unknown)")
            date = msg.get("Date", "")
            unread = "●" if "\\Seen" not in flags else " "
            print(f"{unread} [{mid.decode():>4}] {date[:22]:22} | {from_addr[:30]:30} | {subject[:60]}")

elif action == "read":
    msg_id = args[0] if args else sys.exit("Message ID required")
    mail.select("INBOX", readonly=True)
    status, msg_data = mail.fetch(msg_id.encode(), "(RFC822)")
    raw = msg_data[0][1]
    msg = email.message_from_bytes(raw)
    subject = decode_subject(msg)
    print(f"From: {msg.get('From', '?')}")
    print(f"To: {msg.get('To', '?')}")
    print(f"Date: {msg.get('Date', '?')}")
    print(f"Subject: {subject}")
    print("---")
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                print(body.decode(charset, errors="replace"))
                break
    else:
        body = msg.get_payload(decode=True)
        charset = msg.get_content_charset() or "utf-8"
        print(body.decode(charset, errors="replace"))

elif action == "search":
    query = args[0] if args else sys.exit("Query required")
    limit = int(args[1]) if len(args) > 1 else 10
    mail.select("INBOX", readonly=True)
    # Try Gmail X-GM-RAW first, fall back to IMAP SUBJECT search
    try:
        status, data = mail.search(None, f'X-GM-RAW "{query}"')
    except:
        status, data = mail.search(None, f'SUBJECT "{query}"')
    ids = data[0].split()
    ids = ids[-limit:] if len(ids) > limit else ids
    ids.reverse()
    if not ids:
        print("No messages found")
    else:
        for mid in ids:
            status, msg_data = mail.fetch(mid, "(FLAGS BODY[HEADER.FIELDS (FROM SUBJECT DATE)])")
            raw = msg_data[0][1]
            flags = msg_data[0][0].decode()
            msg = email.message_from_bytes(raw)
            subject = decode_subject(msg)
            from_addr = msg.get("From", "(unknown)")
            date = msg.get("Date", "")
            unread = "●" if "\\Seen" not in flags else " "
            print(f"{unread} [{mid.decode():>4}] {date[:22]:22} | {from_addr[:30]:30} | {subject[:60]}")

mail.logout()
PYEOF
}

# ─── Roundcube Send (HTTPS) ───

cmd_send() {
    local to="$1" subject="$2" body="$3"
    local cookies="/tmp/skulk_mail_cookies_$$"
    trap "rm -f $cookies /tmp/skulk_mail_*.$$" EXIT

    # Step 1: Get login token
    local token=$(curl -s -L -c "$cookies" -b "$cookies" "$WEBMAIL/" \
        | grep -oE 'name="_token" value="[^"]*"' | head -1 \
        | grep -oE '"[^"]*"$' | tr -d '"')
    [ -n "$token" ] || die "Failed to get login token"

    # Step 2: Login
    local login_result=$(curl -s -L -c "$cookies" -b "$cookies" \
        -X POST "${WEBMAIL}/?_task=login" \
        --data-urlencode "_task=login" \
        --data-urlencode "_action=login" \
        --data-urlencode "_timezone=UTC" \
        --data-urlencode "_token=${token}" \
        --data-urlencode "_user=${SKULK_EMAIL}" \
        --data-urlencode "_pass=${SKULK_PASS}" 2>&1)
    echo "$login_result" | grep -q "INBOX" || die "Login failed"

    # Step 3: Get compose tokens
    local compose_page=$(curl -s -L -c "$cookies" -b "$cookies" \
        "${WEBMAIL}/?_task=mail&_action=compose" 2>&1)
    local rtoken=$(echo "$compose_page" | grep -oE '"request_token":"[^"]*"' | head -1 | sed 's/.*:"\([^"]*\)".*/\1/')
    local compose_id=$(echo "$compose_page" | grep -oE '"compose_id":"[^"]*"' | head -1 | sed 's/.*:"\([^"]*\)".*/\1/')
    [ -n "$rtoken" ] && [ -n "$compose_id" ] || die "Failed to get compose tokens"

    # Step 4: Send
    local send_result=$(curl -s -L -c "$cookies" -b "$cookies" \
        -X POST "${WEBMAIL}/?_task=mail&_action=send&_id=${compose_id}&_token=${rtoken}" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        --data-urlencode "_task=mail" \
        --data-urlencode "_action=send" \
        --data-urlencode "_token=${rtoken}" \
        --data-urlencode "_id=${compose_id}" \
        --data-urlencode "_from=${SKULK_EMAIL}" \
        --data-urlencode "_to=${to}" \
        --data-urlencode "_subject=${subject}" \
        --data-urlencode "_message=${body}" 2>&1)

    if echo "$send_result" | grep -qi "sent"; then
        echo "✓ Sent to ${to}: ${subject}"
    else
        die "Send may have failed — check sent folder in webmail"
    fi
}

# ─── Main ───

load_creds

case "${1:-}" in
    test)
        imap_cmd "imap.dreamhost.com" 993 "$SKULK_EMAIL" "$SKULK_PASS" test
        if [ -n "$GMAIL_EMAIL" ] && [ -n "$GMAIL_PASS" ]; then
            imap_cmd "imap.gmail.com" 993 "$GMAIL_EMAIL" "$GMAIL_PASS" test
        fi
        echo "✓ All connections OK"
        ;;
    inbox)       imap_cmd "imap.dreamhost.com" 993 "$SKULK_EMAIL" "$SKULK_PASS" inbox "${2:-10}" ;;
    unread)      imap_cmd "imap.dreamhost.com" 993 "$SKULK_EMAIL" "$SKULK_PASS" unread "${2:-10}" ;;
    count)       imap_cmd "imap.dreamhost.com" 993 "$SKULK_EMAIL" "$SKULK_PASS" count ;;
    read)        imap_cmd "imap.dreamhost.com" 993 "$SKULK_EMAIL" "$SKULK_PASS" read "${2:?Message ID required}" ;;
    search)      imap_cmd "imap.dreamhost.com" 993 "$SKULK_EMAIL" "$SKULK_PASS" search "${2:?Query required}" "${3:-10}" ;;
    send)        cmd_send "${2:?To address required}" "${3:?Subject required}" "${4:?Body required}" ;;
    gmail-inbox)   [ -n "$GMAIL_EMAIL" ] && [ -n "$GMAIL_PASS" ] || die "Gmail not configured"; imap_cmd "imap.gmail.com" 993 "$GMAIL_EMAIL" "$GMAIL_PASS" inbox "${2:-10}" ;;
    gmail-unread)  [ -n "$GMAIL_EMAIL" ] && [ -n "$GMAIL_PASS" ] || die "Gmail not configured"; imap_cmd "imap.gmail.com" 993 "$GMAIL_EMAIL" "$GMAIL_PASS" unread "${2:-10}" ;;
    gmail-count)   [ -n "$GMAIL_EMAIL" ] && [ -n "$GMAIL_PASS" ] || die "Gmail not configured"; imap_cmd "imap.gmail.com" 993 "$GMAIL_EMAIL" "$GMAIL_PASS" count ;;
    gmail-read)    [ -n "$GMAIL_EMAIL" ] && [ -n "$GMAIL_PASS" ] || die "Gmail not configured"; imap_cmd "imap.gmail.com" 993 "$GMAIL_EMAIL" "$GMAIL_PASS" read "${2:?Message ID required}" ;;
    *)           usage ;;
esac
