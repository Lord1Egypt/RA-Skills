#!/usr/bin/env python3
"""
QQ Mail Manager - IMAP/SMTP client for QQ邮箱

Usage:
    python3 qqmail.py inbox [--limit N] [--folder FOLDER]
    python3 qqmail.py read --index N [--folder FOLDER]
    python3 qqmail.py send --to ADDR --subject SUBJ --body BODY [--attachment PATH] [--dry-run]
    python3 qqmail.py reply --index N --body BODY [--folder FOLDER] [--dry-run]
    python3 qqmail.py search [--subject KW] [--from ADDR] [--since DATE] [--limit N]
    python3 qqmail.py folders

Environment:
    QQMAIL_USER       QQ email address (e.g. 123456789@qq.com)
    QQMAIL_AUTH_CODE   Authorization code (授权码, NOT QQ password)
"""

import argparse
import email
import email.encoders
import email.header
import email.utils
import imaplib
import io
import json
import os
import smtplib
import ssl
import sys
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Fix Windows console encoding for Chinese characters
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# QQ Mail server config
IMAP_SERVER = "imap.qq.com"
IMAP_PORT = 993
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465

# Max chars for email preview in inbox listing
PREVIEW_MAX_CHARS = 200
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RULES_FILE = os.path.join(BASE_DIR, "rules.agent.json")
RULES_SCHEMA_FILE = os.path.join(BASE_DIR, "rules.schema.json")
VALID_RULE_ACTIONS = {"archive", "mark-read", "mark-unread", "review"}


def contains_non_ascii(value):
    """Return True when the string contains non-ASCII characters."""
    return any(ord(ch) > 127 for ch in value or "")


def normalize_charset(charset):
    """Normalize non-standard or unknown email charset labels."""
    if not charset:
        return "utf-8"
    value = str(charset).strip().strip('"').lower()
    if value in {"unknown-8bit", "x-unknown", "unknown", "8bit", "binary"}:
        return "utf-8"
    return value


def safe_decode_bytes(data, charset=None):
    """Decode bytes from email headers/bodies with pragmatic fallbacks."""
    if not isinstance(data, bytes):
        return str(data)

    candidates = [
        normalize_charset(charset),
        "utf-8",
        "gb18030",
        "gbk",
        "big5",
        "latin-1",
    ]
    tried = set()
    for candidate in candidates:
        if not candidate or candidate in tried:
            continue
        tried.add(candidate)
        try:
            return data.decode(candidate, errors="replace")
        except LookupError:
            continue
    return data.decode("utf-8", errors="replace")


def get_credentials():
    """Read credentials from environment variables."""
    user = os.environ.get("QQMAIL_USER", "").strip()
    auth_code = os.environ.get("QQMAIL_AUTH_CODE", "").strip()
    if not user:
        print("ERROR: QQMAIL_USER environment variable not set.")
        print("Set it to your QQ email address, e.g.: export QQMAIL_USER=123456789@qq.com")
        sys.exit(1)
    if not auth_code:
        print("ERROR: QQMAIL_AUTH_CODE environment variable not set.")
        print("Get an authorization code (授权码) from QQ Mail settings:")
        print("  mail.qq.com → 设置 → 账户 → IMAP/SMTP服务 → 生成授权码")
        sys.exit(1)
    return user, auth_code


def get_mail_user(required=True):
    """Read the mailbox user without requiring an SMTP/IMAP auth code."""
    user = os.environ.get("QQMAIL_USER", "").strip()
    if not user and required:
        print("ERROR: QQMAIL_USER environment variable not set.")
        print("Set it to your QQ email address, e.g.: export QQMAIL_USER=123456789@qq.com")
        sys.exit(1)
    return user or "(QQMAIL_USER not set)"


def decode_header_value(raw):
    """Decode an email header value (handles encoded words like =?UTF-8?B?...?=)."""
    if raw is None:
        return ""
    parts = email.header.decode_header(raw)
    decoded = []
    for data, charset in parts:
        if isinstance(data, bytes):
            decoded.append(safe_decode_bytes(data, charset))
        else:
            decoded.append(data)
    return " ".join("".join(decoded).split())


def parse_message_date(msg):
    """Parse an email Date header into a datetime, or return None."""
    date_str = msg.get("Date", "")
    if not date_str:
        return None
    try:
        return email.utils.parsedate_to_datetime(date_str)
    except Exception:
        return None


def parse_since_date(value):
    """Parse YYYY-MM-DD into a naive datetime for local comparisons."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: Invalid date format '{value}'. Use YYYY-MM-DD.")
        sys.exit(1)


def message_datetime_for_compare(msg):
    msg_dt = parse_message_date(msg)
    if msg_dt is not None and msg_dt.tzinfo is not None:
        msg_dt = msg_dt.replace(tzinfo=None)
    return msg_dt


def mailbox_quote(name):
    """Quote a mailbox name for IMAP commands."""
    return '"' + name.replace("\\", "\\\\").replace('"', '\\"') + '"'


def fetch_header(conn, msg_id):
    status, data = conn.fetch(msg_id, "(RFC822.HEADER)")
    if status != "OK" or not data or not data[0]:
        return None
    return email.message_from_bytes(data[0][1])


def summarize_header(msg, display_index=None):
    from_addr = decode_header_value(msg.get("From", ""))
    subject = decode_header_value(msg.get("Subject", "(no subject)"))
    date_str = msg.get("Date", "")
    date_parsed = parse_message_date(msg)
    date_display = date_parsed.strftime("%Y-%m-%d %H:%M") if date_parsed else date_str
    return {
        "index": display_index,
        "from": from_addr,
        "subject": subject,
        "date": date_display,
    }


def print_summary(summary, prefix=None):
    label = prefix if prefix is not None else f"[{summary['index']}]"
    print(f"\n{label} {summary['subject']}")
    print(f"    From: {summary['from']}")
    print(f"    Date: {summary['date']}")


def list_message_ids(conn, folder, *, readonly=True, unread=False, since=None):
    status, _ = conn.select(folder, readonly=readonly)
    if status != "OK":
        print(f'ERROR: Cannot open folder "{folder}".')
        return []

    criteria = []
    if unread:
        criteria.append("UNSEEN")
    if since:
        since_dt = parse_since_date(since)
        criteria.append(f"SINCE {since_dt.strftime('%d-%b-%Y')}")
    search_str = " ".join(criteria) if criteria else "ALL"
    status, messages = conn.search(None, search_str)
    if status != "OK":
        print("ERROR: Search failed.")
        return []
    return messages[0].split()


def matches_header_filters(msg, *, from_filter=None, subject_filter=None, since_dt=None):
    """Apply search filters locally against decoded headers."""
    if from_filter:
        from_addr = decode_header_value(msg.get("From", "")).lower()
        if from_filter.lower() not in from_addr:
            return False

    if subject_filter:
        subject = decode_header_value(msg.get("Subject", "")).lower()
        if subject_filter.lower() not in subject:
            return False

    if since_dt:
        msg_dt = message_datetime_for_compare(msg)
        if msg_dt is None:
            return False
        if msg_dt < since_dt:
            return False

    return True


def default_category_for(summary):
    sender = summary["from"].lower()
    subject = summary["subject"].lower()
    text = f"{sender} {subject}"

    if "notifications@github.com" in sender or "github.com" in sender:
        return "github"
    if any(word in text for word in ["job", "engineer", "recruit", "hiring", "career", "职位", "招聘"]):
        return "recruiting"
    if any(word in text for word in ["security", "disabled", "risk", "alert", "风控", "禁用", "异地登录", "安全"]):
        return "security"
    if any(word in text for word in ["invoice", "receipt", "billing", "payment", "paypal", "发票", "账单", "付款", "充值"]):
        return "finance"
    if any(word in text for word in ["newsletter", "substack", "weekly", "digest", "edition", "newsletter", "周刊"]):
        return "newsletter"
    if any(word in text for word in ["noreply", "marketing", "promo", "offer", "discount", "<ad>", "推广", "优惠", "促销"]):
        return "marketing"
    return "review"


def load_rules(path=None):
    path = path or DEFAULT_RULES_FILE
    if not os.path.exists(path):
        print(f"ERROR: Rules file not found: {path}")
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to read rules file {path}: {e}")
        sys.exit(1)
    if isinstance(data, list):
        validate_rules(data, path)
        return {"rules": data}
    if not isinstance(data, dict):
        print(f"ERROR: Rules file must contain a JSON object or list: {path}")
        sys.exit(1)
    data.setdefault("rules", [])
    validate_rules(data["rules"], path)
    return data


def validate_rules(rules, path):
    if not isinstance(rules, list):
        print(f"ERROR: rules must be a list in {path}")
        sys.exit(1)
    for i, rule in enumerate(rules, 1):
        if not isinstance(rule, dict):
            print(f"ERROR: rule #{i} must be an object in {path}")
            sys.exit(1)
        action = rule.get("action", "review")
        if action not in VALID_RULE_ACTIONS:
            print(f"ERROR: rule #{i} has unsupported action {action!r}. Use one of {sorted(VALID_RULE_ACTIONS)}.")
            sys.exit(1)
        if action == "archive" and not rule.get("target"):
            print(f"ERROR: archive rule #{i} must define target.")
            sys.exit(1)
        has_matcher = any(
            key in rule
            for key in (
                "from",
                "from_contains",
                "any_from_contains",
                "subject",
                "subject_contains",
                "any_subject_contains",
                "match_category",
            )
        )
        if not has_matcher:
            print(f"ERROR: rule #{i} has no matcher.")
            sys.exit(1)


def summarize_rules(rules):
    actions = {}
    categories = {}
    targets = {}
    for rule in rules:
        action = rule.get("action", "review")
        category = rule.get("category") or "(none)"
        target = rule.get("target") or "(none)"
        actions[action] = actions.get(action, 0) + 1
        categories[category] = categories.get(category, 0) + 1
        if action == "archive":
            targets[target] = targets.get(target, 0) + 1
    return {
        "count": len(rules),
        "actions": actions,
        "categories": categories,
        "archive_targets": targets,
    }


def json_safe_item(item):
    return {
        key: value
        for key, value in item.items()
        if key != "msg_id"
    }


def emit_json(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def text_preview(value, limit=160):
    value = " ".join((value or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 3] + "..."


def grouped_for_json(grouped, *, preview_limit):
    groups = []
    for (action, target), items in sorted(grouped.items(), key=lambda kv: (kv[0][0] or "", kv[0][1] or "")):
        groups.append({
            "action": action,
            "target": target,
            "count": len(items),
            "items": [json_safe_item(item) for item in items[:preview_limit]],
            "truncated": max(0, len(items) - preview_limit),
        })
    return groups


def rule_matches(rule, summary):
    sender = summary["from"].lower()
    subject = summary["subject"].lower()

    from_contains = rule.get("from_contains") or rule.get("from")
    if from_contains and str(from_contains).lower() not in sender:
        return False

    subject_contains = rule.get("subject_contains") or rule.get("subject")
    if subject_contains and str(subject_contains).lower() not in subject:
        return False

    any_subject_contains = rule.get("any_subject_contains") or []
    if any_subject_contains and not any(str(value).lower() in subject for value in any_subject_contains):
        return False

    any_from_contains = rule.get("any_from_contains") or []
    if any_from_contains and not any(str(value).lower() in sender for value in any_from_contains):
        return False

    match_category = rule.get("match_category")
    if match_category and match_category != summary.get("category"):
        return False

    return True


def classify_summary(summary, rules):
    enriched = dict(summary)
    enriched["category"] = default_category_for(summary)
    for rule in rules:
        if rule_matches(rule, enriched):
            enriched["rule"] = rule.get("name", "(unnamed rule)")
            enriched["category"] = rule.get("category", enriched["category"])
            enriched["action"] = rule.get("action", "review")
            enriched["target"] = rule.get("target")
            return enriched
    enriched["rule"] = None
    enriched["action"] = "review"
    enriched["target"] = None
    return enriched


def mailbox_exists(conn, name):
    status, folders = conn.list()
    if status != "OK":
        return False
    needle = f'"{name}"'
    for folder_raw in folders:
        folder_str = safe_decode_bytes(folder_raw, "utf-8") if isinstance(folder_raw, bytes) else str(folder_raw)
        if folder_str.endswith(needle) or folder_str.rsplit('"', 2)[-2:-1] == [name]:
            return True
    return False


def ensure_mailbox(conn, name, *, quiet=False):
    if mailbox_exists(conn, name):
        return True
    status, data = conn.create(mailbox_quote(name))
    if status == "OK":
        if not quiet:
            print(f"Created folder: {name}")
        return True
    if not quiet:
        print(f'ERROR: Target folder "{name}" does not exist and could not be created: {data}')
    return False


def fetch_matching_ids_locally(conn, folder, *, from_filter=None, subject_filter=None, since_dt=None):
    """Fallback search by scanning message headers locally.

    This avoids IMAP SEARCH charset issues for non-ASCII keywords.
    """
    status, _ = conn.select(folder, readonly=True)
    if status != "OK":
        print(f'ERROR: Cannot open folder "{folder}".')
        return []

    status, messages = conn.search(None, "ALL")
    if status != "OK":
        print("ERROR: Search failed.")
        return []

    msg_ids = messages[0].split()
    if not msg_ids:
        return []

    matches = []
    for msg_id in msg_ids:
        status, data = conn.fetch(msg_id, "(RFC822.HEADER)")
        if status != "OK" or not data or not data[0]:
            continue
        msg = email.message_from_bytes(data[0][1])
        if matches_header_filters(
            msg,
            from_filter=from_filter,
            subject_filter=subject_filter,
            since_dt=since_dt,
        ):
            matches.append(msg_id)
    return matches


def get_email_body(msg):
    """Extract plain text body from an email message."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/plain" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return safe_decode_bytes(payload, charset)
        # Fallback: try text/html if no plain text
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/html" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return f"[HTML content]\n{safe_decode_bytes(payload, charset)}"
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            return safe_decode_bytes(payload, charset)
    return "[No text content]"


def connect_imap():
    """Connect and authenticate to QQ Mail IMAP server."""
    user, auth_code = get_credentials()
    try:
        context = ssl.create_default_context()
        conn = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context)
        conn.login(user, auth_code)
        return conn
    except imaplib.IMAP4.error as e:
        print(f"ERROR: IMAP login failed: {e}")
        print("Check your QQMAIL_USER and QQMAIL_AUTH_CODE.")
        print("Make sure IMAP is enabled in QQ Mail settings.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Cannot connect to {IMAP_SERVER}:{IMAP_PORT}: {e}")
        sys.exit(1)


def cmd_folders(_args):
    """List all mail folders."""
    conn = connect_imap()
    try:
        status, folders = conn.list()
        if status != "OK":
            print("ERROR: Failed to list folders.")
            return
        print("Mail Folders:")
        print("-" * 40)
        for folder_raw in folders:
            if isinstance(folder_raw, bytes):
                folder_str = folder_raw.decode("utf-8", errors="replace")
            else:
                folder_str = str(folder_raw)
            # Parse folder name from IMAP response like: (\\Noselect \\HasChildren) "/" "INBOX"
            parts = folder_str.rsplit('"', 2)
            if len(parts) >= 2:
                folder_name = parts[-2]
            else:
                folder_name = folder_str
            print(f"  {folder_name}")
    finally:
        conn.logout()


def cmd_inbox(args):
    """Read recent emails from inbox (or specified folder)."""
    limit = args.limit or 10
    folder = args.folder or "INBOX"

    conn = connect_imap()
    try:
        msg_ids = list_message_ids(conn, folder, readonly=True, unread=args.unread, since=args.since)
        if not msg_ids:
            print(f"No emails in {folder}.")
            return

        # Get the most recent N emails
        recent_ids = msg_ids[-limit:]
        recent_ids.reverse()  # newest first

        print(f"Recent emails in {folder} (showing {len(recent_ids)} of {len(msg_ids)}):")
        print("=" * 70)

        for i, msg_id in enumerate(recent_ids, 1):
            msg = fetch_header(conn, msg_id)
            if msg is None:
                continue
            print_summary(summarize_header(msg, i))
    finally:
        conn.logout()


def cmd_read(args):
    """Read a specific email by index (1-based, from newest)."""
    index = args.index
    folder = args.folder or "INBOX"

    conn = connect_imap()
    try:
        status, _ = conn.select(folder, readonly=True)
        if status != "OK":
            print(f'ERROR: Cannot open folder "{folder}".')
            return

        status, messages = conn.search(None, "ALL")
        if status != "OK":
            print("ERROR: Search failed.")
            return

        msg_ids = messages[0].split()
        if not msg_ids:
            print(f"No emails in {folder}.")
            return

        # Index 1 = newest
        if index < 1 or index > len(msg_ids):
            print(f"ERROR: Index {index} out of range (1-{len(msg_ids)}).")
            return

        target_id = msg_ids[-index]
        status, data = conn.fetch(target_id, "(RFC822)")
        if status != "OK":
            print("ERROR: Failed to fetch email.")
            return

        msg = email.message_from_bytes(data[0][1])

        from_addr = decode_header_value(msg.get("From", ""))
        to_addr = decode_header_value(msg.get("To", ""))
        subject = decode_header_value(msg.get("Subject", "(no subject)"))
        date_str = msg.get("Date", "")
        date_parsed = email.utils.parsedate_to_datetime(date_str) if date_str else None
        date_display = date_parsed.strftime("%Y-%m-%d %H:%M:%S") if date_parsed else date_str

        body = get_email_body(msg)

        # List attachments
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                disposition = str(part.get("Content-Disposition", ""))
                if "attachment" in disposition:
                    filename = decode_header_value(part.get_filename() or "unnamed")
                    attachments.append(filename)

        print("=" * 70)
        print(f"Subject: {subject}")
        print(f"From:    {from_addr}")
        print(f"To:      {to_addr}")
        print(f"Date:    {date_display}")
        if attachments:
            print(f"Attachments: {', '.join(attachments)}")
        print("-" * 70)
        print(body)
        print("=" * 70)
    finally:
        conn.logout()


def cmd_send(args):
    """Send an email via SMTP."""
    user = get_mail_user(required=not args.dry_run)
    to_addr = args.to
    subject = args.subject
    body = args.body
    attachment_path = args.attachment

    if attachment_path and not os.path.isfile(attachment_path):
        print(f"ERROR: Attachment file not found: {attachment_path}")
        sys.exit(1)

    if args.dry_run:
        attachment = os.path.basename(attachment_path) if attachment_path else None
        print("[DRY RUN] Would send email")
        print(f"  From: {user}")
        print(f"  To: {to_addr}")
        print(f"  Subject: {subject}")
        print(f"  Body preview: {text_preview(body)}")
        if attachment:
            print(f"  Attachment: {attachment}")
        print("No message was sent.")
        return

    _, auth_code = get_credentials()

    # Build message
    if attachment_path:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "plain", "utf-8"))

        filename = os.path.basename(attachment_path)
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        email.encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)
    else:
        msg = MIMEText(body, "plain", "utf-8")

    msg["From"] = user
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = email.utils.formatdate(localtime=True)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(user, auth_code)
            server.sendmail(user, [to_addr], msg.as_string())
        print(f"OK: Email sent to {to_addr}")
        print(f"  Subject: {subject}")
        if attachment_path:
            print(f"  Attachment: {os.path.basename(attachment_path)}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"ERROR: SMTP authentication failed: {e}")
        print("Check your QQMAIL_USER and QQMAIL_AUTH_CODE.")
        print("Make sure SMTP is enabled in QQ Mail settings.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to send email: {e}")
        sys.exit(1)


def cmd_reply(args):
    """Reply to a specific email by index (1-based, newest-first)."""
    user = get_mail_user(required=True)
    folder = args.folder or "INBOX"
    index = args.index

    conn = connect_imap()
    try:
        status, _ = conn.select(folder, readonly=True)
        if status != "OK":
            print(f'ERROR: Cannot open folder "{folder}".')
            return

        status, messages = conn.search(None, "ALL")
        if status != "OK":
            print("ERROR: Search failed.")
            return

        msg_ids = messages[0].split()
        if not msg_ids:
            print(f"No emails in {folder}.")
            return

        if index < 1 or index > len(msg_ids):
            print(f"ERROR: Index {index} out of range (1-{len(msg_ids)}).")
            return

        target_id = msg_ids[-index]
        status, data = conn.fetch(target_id, "(RFC822)")
        if status != "OK":
            print("ERROR: Failed to fetch email.")
            return

        original = email.message_from_bytes(data[0][1])
    finally:
        conn.logout()

    reply_to_header = original.get("Reply-To") or original.get("From", "")
    reply_to = email.utils.parseaddr(decode_header_value(reply_to_header))[1]
    if not reply_to:
        print("ERROR: Could not determine reply recipient.")
        sys.exit(1)

    original_subject = decode_header_value(original.get("Subject", "(no subject)"))
    subject = original_subject if original_subject.lower().startswith("re:") else f"Re: {original_subject}"

    msg = MIMEText(args.body, "plain", "utf-8")
    msg["From"] = user
    msg["To"] = reply_to
    msg["Subject"] = subject
    msg["Date"] = email.utils.formatdate(localtime=True)

    message_id = original.get("Message-ID")
    references = original.get("References")
    if message_id:
        msg["In-Reply-To"] = message_id
        msg["References"] = f"{references} {message_id}".strip() if references else message_id

    if args.dry_run:
        print("[DRY RUN] Would send reply")
        print(f"  From: {user}")
        print(f"  To: {reply_to}")
        print(f"  Subject: {subject}")
        print(f"  Body preview: {text_preview(args.body)}")
        print(f"  In-Reply-To: {'yes' if message_id else 'no'}")
        print(f"  References: {'yes' if references or message_id else 'no'}")
        print("No reply was sent.")
        return

    _, auth_code = get_credentials()
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(user, auth_code)
            server.sendmail(user, [reply_to], msg.as_string())
        print(f"OK: Reply sent to {reply_to}")
        print(f"  Subject: {subject}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"ERROR: SMTP authentication failed: {e}")
        print("Check your QQMAIL_USER and QQMAIL_AUTH_CODE.")
        print("Make sure SMTP is enabled in QQ Mail settings.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to send reply: {e}")
        sys.exit(1)


def _resolve_msg_ids(conn, folder, indices=None, from_filter=None, subject_filter=None, since=None, unread=False):
    """Resolve email indices (1-based newest-first) or search filters to IMAP msg ids."""
    since_dt = parse_since_date(since)

    all_ids = list_message_ids(conn, folder, readonly=False, unread=unread, since=since)
    total = len(all_ids)
    if indices:
        result = []
        for idx in indices:
            if 1 <= idx <= total:
                result.append(all_ids[-idx])
        return result

    result = []
    for msg_id in all_ids:
        msg = fetch_header(conn, msg_id)
        if msg is None:
            continue
        if matches_header_filters(
            msg,
            from_filter=from_filter,
            subject_filter=subject_filter,
            since_dt=since_dt,
        ):
            result.append(msg_id)
    return result


def preview_msg_ids(conn, msg_ids, *, max_items=20):
    for i, mid in enumerate(msg_ids[:max_items], 1):
        msg = fetch_header(conn, mid)
        if msg is None:
            continue
        print_summary(summarize_header(msg), prefix=f"[{i}]")
    if len(msg_ids) > max_items:
        print(f"\n... and {len(msg_ids) - max_items} more")


def cmd_archive(args):
    """Move emails to a target folder (archive)."""
    folder = args.folder or "INBOX"
    target = args.target or "Deleted Messages"
    indices = args.index or []
    from_filter = getattr(args, "from", None)
    subject_filter = args.subject
    since = args.since
    unread = args.unread
    if not (indices or from_filter or subject_filter or since or unread):
        print("ERROR: Refusing to archive without a selector. Use --index, --from, --subject, --since, or --unread.")
        return

    conn = connect_imap()
    try:
        msg_ids = _resolve_msg_ids(conn, folder, indices, from_filter, subject_filter, since=since, unread=unread)
        if not msg_ids:
            print("No matching emails found.")
            return

        if args.dry_run:
            print(f"[DRY RUN] Would move {len(msg_ids)} email(s) from {folder} → {target}")
            preview_msg_ids(conn, msg_ids)
            return

        if not ensure_mailbox(conn, target):
            return

        conn.select(folder)
        moved = 0
        # Quote the target folder name for IMAP
        quoted_target = mailbox_quote(target)
        for mid in msg_ids:
            # Copy to target, then flag as deleted in source
            status, _ = conn.copy(mid, quoted_target)
            if status == "OK":
                conn.store(mid, "+FLAGS", "\\Deleted")
                moved += 1
            else:
                # Fetch subject for error reporting
                _, data = conn.fetch(mid, "(RFC822.HEADER)")
                msg = email.message_from_bytes(data[0][1])
                subj = decode_header_value(msg.get("Subject", "?"))
                print(f"  FAILED to move: {subj}")

        conn.expunge()
        print(f"OK: Moved {moved} email(s) from {folder} → {target}")
    finally:
        conn.logout()


def cmd_delete(args):
    """Permanently delete emails (flag as \\Deleted + expunge)."""
    folder = args.folder or "INBOX"
    indices = args.index or []
    from_filter = getattr(args, "from", None)
    subject_filter = args.subject
    since = args.since
    unread = args.unread
    if not (indices or from_filter or subject_filter or since or unread):
        print("ERROR: Refusing to delete without a selector. Use --index, --from, --subject, --since, or --unread.")
        return

    conn = connect_imap()
    try:
        msg_ids = _resolve_msg_ids(conn, folder, indices, from_filter, subject_filter, since=since, unread=unread)
        if not msg_ids:
            print("No matching emails found.")
            return

        if args.dry_run:
            print(f"[DRY RUN] Would permanently delete {len(msg_ids)} email(s) from {folder}")
            preview_msg_ids(conn, msg_ids)
            return

        if args.confirm_delete != "DELETE":
            print('ERROR: Refusing permanent delete without --confirm-delete DELETE.')
            print("Run with --dry-run first, then repeat with --confirm-delete DELETE only after explicit approval.")
            return

        conn.select(folder)
        for mid in msg_ids:
            conn.store(mid, "+FLAGS", "\\Deleted")
        conn.expunge()
        print(f"OK: Deleted {len(msg_ids)} email(s) from {folder}")
    finally:
        conn.logout()


def cmd_mkdir(args):
    """Create a mail folder if it does not already exist."""
    conn = connect_imap()
    try:
        if mailbox_exists(conn, args.name):
            print(f"OK: Folder already exists: {args.name}")
            return
        if ensure_mailbox(conn, args.name):
            print(f"OK: Folder ready: {args.name}")
    finally:
        conn.logout()


def cmd_mark(args, seen):
    """Mark matching emails as read or unread."""
    folder = args.folder or "INBOX"
    indices = args.index or []
    from_filter = getattr(args, "from", None)
    subject_filter = args.subject
    since = args.since
    unread = args.unread
    if not (indices or from_filter or subject_filter or since or unread):
        print("ERROR: Refusing to mark without a selector. Use --index, --from, --subject, --since, or --unread.")
        return

    conn = connect_imap()
    try:
        msg_ids = _resolve_msg_ids(conn, folder, indices, from_filter, subject_filter, since=since, unread=unread)
        if not msg_ids:
            print("No matching emails found.")
            return

        if args.dry_run:
            action = "read" if seen else "unread"
            print(f"[DRY RUN] Would mark {len(msg_ids)} email(s) as {action} in {folder}")
            preview_msg_ids(conn, msg_ids)
            return

        conn.select(folder)
        flag_op = "+FLAGS" if seen else "-FLAGS"
        for mid in msg_ids:
            conn.store(mid, flag_op, "\\Seen")
        action = "read" if seen else "unread"
        print(f"OK: Marked {len(msg_ids)} email(s) as {action} in {folder}")
    finally:
        conn.logout()


def cmd_mark_read(args):
    cmd_mark(args, True)


def cmd_mark_unread(args):
    cmd_mark(args, False)


def cmd_validate_rules(args):
    """Validate an organization rules file without connecting to QQ Mail."""
    rules_path = args.rules or DEFAULT_RULES_FILE
    data = load_rules(rules_path)
    summary = summarize_rules(data.get("rules", []))
    if args.json:
        emit_json({
            "valid": True,
            "rules_file": rules_path,
            "schema_file": RULES_SCHEMA_FILE,
            **summary,
        })
        return

    print(f"OK: Rules file is valid: {rules_path}")
    print(f"Rules: {summary['count']}")
    if summary["actions"]:
        print("Actions:")
        for action, count in sorted(summary["actions"].items()):
            print(f"  {action}: {count}")
    if summary["archive_targets"]:
        print("Archive targets:")
        for target, count in sorted(summary["archive_targets"].items()):
            print(f"  {target}: {count}")


def collect_classified_messages(conn, *, folder, limit, unread=False, since=None, rules_file=None):
    rules = load_rules(rules_file).get("rules", [])
    msg_ids = list_message_ids(conn, folder, readonly=True, unread=unread, since=since)
    recent_ids = msg_ids[-limit:] if limit else msg_ids
    recent_ids.reverse()
    classified = []
    for display_index, msg_id in enumerate(recent_ids, 1):
        msg = fetch_header(conn, msg_id)
        if msg is None:
            continue
        summary = summarize_header(msg, display_index)
        summary["msg_id"] = msg_id
        classified.append(classify_summary(summary, rules))
    return classified


def cmd_plan_organize(args):
    """Classify recent emails and print a non-mutating organization plan."""
    folder = args.folder or "INBOX"
    conn = connect_imap()
    try:
        classified = collect_classified_messages(
            conn,
            folder=folder,
            limit=args.limit,
            unread=args.unread,
            since=args.since,
            rules_file=args.rules,
        )
    finally:
        conn.logout()

    if not classified:
        if args.json:
            emit_json({
                "mode": "plan",
                "mutated": False,
                "folder": folder,
                "count": 0,
                "categories": {},
            })
            return
        print("No emails found for organization planning.")
        return

    buckets = {}
    for item in classified:
        buckets.setdefault(item["category"], []).append(item)

    if args.json:
        emit_json({
            "mode": "plan",
            "mutated": False,
            "folder": folder,
            "count": len(classified),
            "categories": {
                category: {
                    "count": len(items),
                    "items": [json_safe_item(item) for item in items[: args.per_category]],
                    "truncated": max(0, len(items) - args.per_category),
                }
                for category, items in sorted(buckets.items(), key=lambda kv: (-len(kv[1]), kv[0]))
            },
        })
        return

    print(f"Organization plan for {folder}: {len(classified)} email(s)")
    print("=" * 70)
    for category, items in sorted(buckets.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f"\n## {category} ({len(items)})")
        for item in items[: args.per_category]:
            action = item.get("action", "review")
            target = item.get("target")
            rule = item.get("rule")
            suffix = f" -> {action}"
            if target:
                suffix += f":{target}"
            if rule:
                suffix += f" [{rule}]"
            print(f"- [{item['index']}] {item['subject']} | {item['from']}{suffix}")
        if len(items) > args.per_category:
            print(f"- ... {len(items) - args.per_category} more")

    print("\nNo changes were made.")


def cmd_auto_organize(args):
    """Apply archive/mark rules from rules.json. Defaults to dry-run."""
    folder = args.folder or "INBOX"
    apply_changes = args.apply
    conn = connect_imap()
    moved = 0
    marked = 0
    try:
        classified = collect_classified_messages(
            conn,
            folder=folder,
            limit=args.limit,
            unread=args.unread,
            since=args.since,
            rules_file=args.rules,
        )
        actionable = [
            item for item in classified
            if item.get("rule") and item.get("action") in {"archive", "mark-read", "mark-unread"}
        ]
        if not actionable:
            if args.json:
                emit_json({
                    "mode": "apply" if apply_changes else "dry-run",
                    "mutated": False,
                    "folder": folder,
                    "evaluated_count": len(classified),
                    "actionable_count": 0,
                    "groups": [],
                })
                return
            print("No rule-matched emails to organize.")
            return

        grouped = {}
        for item in actionable:
            key = (item.get("action"), item.get("target"))
            grouped.setdefault(key, []).append(item)

        if not apply_changes:
            if args.json:
                emit_json({
                    "mode": "dry-run",
                    "mutated": False,
                    "folder": folder,
                    "evaluated_count": len(classified),
                    "actionable_count": len(actionable),
                    "groups": grouped_for_json(grouped, preview_limit=args.preview_limit),
                    "apply_hint": "Re-run the same command with --apply after explicit user approval.",
                })
                return

            print(f"[DRY RUN] {len(actionable)} rule-matched email(s)")
            for (action, target), items in grouped.items():
                label = f"{action}:{target}" if target else action
                print(f"\n## {label} ({len(items)})")
                for item in items[: args.preview_limit]:
                    print(f"- [{item['index']}] {item['subject']} | {item['from']} [{item['rule']}]")
                if len(items) > args.preview_limit:
                    print(f"- ... {len(items) - args.preview_limit} more")
            print("\nNo changes were made. Re-run with --apply to execute.")
            return

        conn.select(folder)
        should_expunge = False
        skipped = []
        for (action, target), items in grouped.items():
            if action == "archive":
                if not target:
                    skipped.append({"action": action, "reason": "archive rule missing target", "count": len(items)})
                    if not args.json:
                        print("SKIP: archive rule missing target")
                    continue
                if not ensure_mailbox(conn, target, quiet=args.json):
                    skipped.append({"action": action, "target": target, "reason": "target folder unavailable", "count": len(items)})
                    continue
                conn.select(folder)
                for item in items:
                    status, _ = conn.copy(item["msg_id"], mailbox_quote(target))
                    if status == "OK":
                        conn.store(item["msg_id"], "+FLAGS", "\\Deleted")
                        moved += 1
                        should_expunge = True
            elif action in {"mark-read", "mark-unread"}:
                flag_op = "+FLAGS" if action == "mark-read" else "-FLAGS"
                for item in items:
                    conn.store(item["msg_id"], flag_op, "\\Seen")
                    marked += 1

        if should_expunge:
            conn.expunge()
        if args.json:
            emit_json({
                "mode": "apply",
                "mutated": moved > 0 or marked > 0,
                "folder": folder,
                "evaluated_count": len(classified),
                "actionable_count": len(actionable),
                "moved": moved,
                "marked": marked,
                "skipped": skipped,
            })
            return
        print(f"OK: moved {moved} email(s), marked {marked} email(s)")
    finally:
        conn.logout()


def cmd_search(args):
    """Search emails by subject, sender, or date."""
    limit = args.limit or 20
    folder = args.folder or "INBOX"
    since_dt = None

    # Build IMAP search criteria
    criteria = []
    if args.subject:
        criteria.append(f'SUBJECT "{args.subject}"')
    if getattr(args, "from", None):
        criteria.append(f'FROM "{getattr(args, "from")}"')
    if args.since:
        try:
            date_obj = datetime.strptime(args.since, "%Y-%m-%d")
            since_dt = date_obj
            date_imap = date_obj.strftime("%d-%b-%Y")
            criteria.append(f"SINCE {date_imap}")
        except ValueError:
            print(f"ERROR: Invalid date format '{args.since}'. Use YYYY-MM-DD.")
            sys.exit(1)

    if not criteria:
        print("ERROR: Specify at least one search criterion: --subject, --from, or --since")
        sys.exit(1)

    search_str = " ".join(criteria)

    conn = connect_imap()
    try:
        status, _ = conn.select(folder, readonly=True)
        if status != "OK":
            print(f'ERROR: Cannot open folder "{folder}".')
            return

        if contains_non_ascii(args.subject) or contains_non_ascii(getattr(args, "from", None)):
            msg_ids = fetch_matching_ids_locally(
                conn,
                folder,
                from_filter=getattr(args, "from", None),
                subject_filter=args.subject,
                since_dt=since_dt,
            )
        else:
            status, messages = conn.search(None, search_str)
            if status != "OK":
                print("ERROR: Search failed.")
                return
            msg_ids = messages[0].split()

        if not msg_ids:
            print(f"No emails matching: {search_str}")
            return

        # Show most recent matches
        recent_ids = msg_ids[-limit:]
        recent_ids.reverse()

        print(f"Search results ({len(recent_ids)} of {len(msg_ids)} matches):")
        print(f"Criteria: {search_str}")
        print("=" * 70)

        for i, msg_id in enumerate(recent_ids, 1):
            status, data = conn.fetch(msg_id, "(RFC822.HEADER)")
            if status != "OK":
                continue
            msg = email.message_from_bytes(data[0][1])

            from_addr = decode_header_value(msg.get("From", ""))
            subject = decode_header_value(msg.get("Subject", "(no subject)"))
            date_str = msg.get("Date", "")
            date_parsed = parse_message_date(msg)
            date_display = date_parsed.strftime("%Y-%m-%d %H:%M") if date_parsed else date_str

            print(f"\n[{i}] {subject}")
            print(f"    From: {from_addr}")
            print(f"    Date: {date_display}")
    finally:
        conn.logout()


def main():
    parser = argparse.ArgumentParser(
        description="QQ Mail Manager - read, send, search emails via IMAP/SMTP"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # inbox
    p_inbox = subparsers.add_parser("inbox", help="Read recent emails")
    p_inbox.add_argument("--limit", type=int, default=10, help="Number of emails to show (default: 10)")
    p_inbox.add_argument("--folder", type=str, default="INBOX", help="Mail folder (default: INBOX)")
    p_inbox.add_argument("--unread", action="store_true", help="Only show unread emails")
    p_inbox.add_argument("--since", help="Only show emails since date (YYYY-MM-DD)")

    # read
    p_read = subparsers.add_parser("read", help="Read a specific email")
    p_read.add_argument("--index", type=int, required=True, help="Email index (1=newest)")
    p_read.add_argument("--folder", type=str, default="INBOX", help="Mail folder (default: INBOX)")

    # send
    p_send = subparsers.add_parser("send", help="Send an email")
    p_send.add_argument("--to", required=True, help="Recipient email address")
    p_send.add_argument("--subject", required=True, help="Email subject")
    p_send.add_argument("--body", required=True, help="Email body text")
    p_send.add_argument("--attachment", help="Path to attachment file")
    p_send.add_argument("--dry-run", action="store_true", help="Preview without sending")

    # reply
    p_reply = subparsers.add_parser("reply", help="Reply to a specific email")
    p_reply.add_argument("--index", type=int, required=True, help="Email index (1=newest)")
    p_reply.add_argument("--folder", type=str, default="INBOX", help="Mail folder (default: INBOX)")
    p_reply.add_argument("--body", required=True, help="Reply body text")
    p_reply.add_argument("--dry-run", action="store_true", help="Preview without sending")

    # search
    p_search = subparsers.add_parser("search", help="Search emails")
    p_search.add_argument("--subject", help="Search by subject keyword")
    p_search.add_argument("--from", dest="from", help="Search by sender address")
    p_search.add_argument("--since", help="Search since date (YYYY-MM-DD)")
    p_search.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    p_search.add_argument("--folder", type=str, default="INBOX", help="Mail folder (default: INBOX)")

    # folders
    subparsers.add_parser("folders", help="List mail folders")

    # mkdir
    p_mkdir = subparsers.add_parser("mkdir", help="Create a mail folder")
    p_mkdir.add_argument("name", help="Folder name to create")

    # archive
    p_archive = subparsers.add_parser("archive", help="Move emails to another folder")
    p_archive.add_argument("--index", type=int, nargs="+", help="Email indices (1=newest, space-separated)")
    p_archive.add_argument("--from", dest="from", help="Archive all from this sender")
    p_archive.add_argument("--subject", help="Archive all matching this subject")
    p_archive.add_argument("--since", help="Archive emails since date (YYYY-MM-DD)")
    p_archive.add_argument("--unread", action="store_true", help="Only archive unread emails")
    p_archive.add_argument("--dry-run", action="store_true", help="Preview without moving emails")
    p_archive.add_argument("--folder", type=str, default="INBOX", help="Source folder (default: INBOX)")
    p_archive.add_argument("--target", type=str, default="Deleted Messages", help="Target folder (default: Deleted Messages)")

    # delete
    p_delete = subparsers.add_parser("delete", help="Permanently delete emails")
    p_delete.add_argument("--index", type=int, nargs="+", help="Email indices (1=newest, space-separated)")
    p_delete.add_argument("--from", dest="from", help="Delete all from this sender")
    p_delete.add_argument("--subject", help="Delete all matching this subject")
    p_delete.add_argument("--since", help="Delete emails since date (YYYY-MM-DD)")
    p_delete.add_argument("--unread", action="store_true", help="Only delete unread emails")
    p_delete.add_argument("--dry-run", action="store_true", help="Preview without deleting emails")
    p_delete.add_argument("--confirm-delete", help='Required phrase for permanent deletion: DELETE')
    p_delete.add_argument("--folder", type=str, default="INBOX", help="Source folder (default: INBOX)")

    # mark-read / mark-unread
    for name, help_text in [
        ("mark-read", "Mark matching emails as read"),
        ("mark-unread", "Mark matching emails as unread"),
    ]:
        p_mark = subparsers.add_parser(name, help=help_text)
        p_mark.add_argument("--index", type=int, nargs="+", help="Email indices (1=newest, space-separated)")
        p_mark.add_argument("--from", dest="from", help="Match sender")
        p_mark.add_argument("--subject", help="Match subject keyword")
        p_mark.add_argument("--since", help="Match emails since date (YYYY-MM-DD)")
        p_mark.add_argument("--unread", action="store_true", help="Only match unread emails")
        p_mark.add_argument("--dry-run", action="store_true", help="Preview without changing flags")
        p_mark.add_argument("--folder", type=str, default="INBOX", help="Source folder (default: INBOX)")

    # validate-rules
    p_validate_rules = subparsers.add_parser("validate-rules", help="Validate organization rules without connecting to QQ Mail")
    p_validate_rules.add_argument("--rules", default=DEFAULT_RULES_FILE, help=f"Rules JSON path (default: {DEFAULT_RULES_FILE})")
    p_validate_rules.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    # plan-organize
    p_plan = subparsers.add_parser("plan-organize", help="Classify emails and print an organization plan without changes")
    p_plan.add_argument("--limit", type=int, default=50, help="Number of recent emails to classify (default: 50)")
    p_plan.add_argument("--folder", type=str, default="INBOX", help="Source folder (default: INBOX)")
    p_plan.add_argument("--unread", action="store_true", help="Only classify unread emails")
    p_plan.add_argument("--since", help="Only classify emails since date (YYYY-MM-DD)")
    p_plan.add_argument("--rules", default=DEFAULT_RULES_FILE, help=f"Rules JSON path (default: {DEFAULT_RULES_FILE})")
    p_plan.add_argument("--per-category", type=int, default=8, help="Max emails shown per category (default: 8)")
    p_plan.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    # auto-organize
    p_auto = subparsers.add_parser("auto-organize", help="Apply organization rules; dry-run by default")
    p_auto.add_argument("--limit", type=int, default=100, help="Number of recent emails to evaluate (default: 100)")
    p_auto.add_argument("--folder", type=str, default="INBOX", help="Source folder (default: INBOX)")
    p_auto.add_argument("--unread", action="store_true", help="Only evaluate unread emails")
    p_auto.add_argument("--since", help="Only evaluate emails since date (YYYY-MM-DD)")
    p_auto.add_argument("--rules", default=DEFAULT_RULES_FILE, help=f"Rules JSON path (default: {DEFAULT_RULES_FILE})")
    p_auto.add_argument("--preview-limit", type=int, default=20, help="Max preview rows per action (default: 20)")
    p_auto.add_argument("--apply", action="store_true", help="Actually apply archive/mark rules")
    p_auto.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "inbox": cmd_inbox,
        "read": cmd_read,
        "send": cmd_send,
        "reply": cmd_reply,
        "search": cmd_search,
        "folders": cmd_folders,
        "mkdir": cmd_mkdir,
        "archive": cmd_archive,
        "delete": cmd_delete,
        "mark-read": cmd_mark_read,
        "mark-unread": cmd_mark_unread,
        "validate-rules": cmd_validate_rules,
        "plan-organize": cmd_plan_organize,
        "auto-organize": cmd_auto_organize,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
