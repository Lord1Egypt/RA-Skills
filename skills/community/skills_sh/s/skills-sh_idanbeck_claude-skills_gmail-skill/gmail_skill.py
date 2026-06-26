#!/usr/bin/env python3
"""
Gmail Skill - Read, search, send, and manage Gmail emails. Access Google contacts.

Supports multiple accounts with seamless OAuth browser flow.

Usage:
    python gmail_skill.py search "query" [--account EMAIL]
    python gmail_skill.py read EMAIL_ID [--account EMAIL]
    python gmail_skill.py list [--account EMAIL]
    python gmail_skill.py labels [--account EMAIL]
    python gmail_skill.py send --to EMAIL --subject "..." --body "..." [--account EMAIL]
    python gmail_skill.py mark-read EMAIL_ID [--account EMAIL]
    python gmail_skill.py mark-done EMAIL_ID [--account EMAIL]  # Archive (Gmail 'e')
    python gmail_skill.py contacts [--account EMAIL]
    python gmail_skill.py search-contacts "query" [--account EMAIL]
    python gmail_skill.py accounts                    # List authenticated accounts
    python gmail_skill.py logout [--account EMAIL]    # Remove account
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import textwrap
import webbrowser
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode, parse_qs, urlparse
import threading
import secrets

# Email line width for readability (matches Superhuman style)
EMAIL_LINE_WIDTH = 72

# Check for required libraries
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import requests
except ImportError:
    print("Error: Required libraries not installed.")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests")
    sys.exit(1)

# Paths
SKILL_DIR = Path(__file__).parent
TOKENS_DIR = SKILL_DIR / "tokens"
CREDENTIALS_FILE = SKILL_DIR / "credentials.json"
ACCOUNTS_META_FILE = SKILL_DIR / "accounts.json"

# Scopes - includes send and modify capabilities
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",    # For sending (REQUIRES USER CONFIRMATION)
    "https://www.googleapis.com/auth/gmail.modify",  # For mark-read, archive, etc.
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/contacts.other.readonly",
    "https://www.googleapis.com/auth/userinfo.email",  # To get email address
]

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# Default OAuth client - user can override with their own credentials.json
# This is a "Desktop app" type client, where the secret is not truly secret
DEFAULT_CLIENT_CONFIG = {
    "installed": {
        "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "client_secret": "YOUR_CLIENT_SECRET",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"]
    }
}


def get_client_config() -> dict:
    """Load OAuth client configuration."""
    if CREDENTIALS_FILE.exists():
        with open(CREDENTIALS_FILE) as f:
            return json.load(f)

    # Check if default config has been configured
    if DEFAULT_CLIENT_CONFIG["installed"]["client_id"].startswith("YOUR_"):
        print("\n" + "="*60)
        print("FIRST-TIME SETUP REQUIRED")
        print("="*60)
        print("\nTo use Gmail Reader, you need to create a Google Cloud OAuth client.")
        print("This is a one-time setup that takes ~2 minutes:\n")
        print("1. Go to: https://console.cloud.google.com/apis/credentials")
        print("2. Create a project (or select existing)")
        print("3. Click '+ CREATE CREDENTIALS' → 'OAuth client ID'")
        print("4. If prompted, configure OAuth consent screen:")
        print("   - User Type: External")
        print("   - App name: Gmail Reader (or anything)")
        print("   - Your email for support/developer contact")
        print("   - Add scopes: gmail.readonly, contacts.readonly")
        print("   - Add yourself as test user")
        print("5. Back to Credentials → Create OAuth client ID:")
        print("   - Application type: Desktop app")
        print("   - Name: Gmail Reader")
        print("6. Download JSON and save as:")
        print(f"   {CREDENTIALS_FILE}")
        print("\nThen run this command again.")
        print("="*60 + "\n")

        # Offer to open the console
        try:
            response = input("Open Google Cloud Console now? [Y/n]: ").strip().lower()
            if response != 'n':
                webbrowser.open("https://console.cloud.google.com/apis/credentials")
        except:
            pass

        sys.exit(1)

    return DEFAULT_CLIENT_CONFIG


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler to receive OAuth callback."""

    def log_message(self, format, *args):
        pass  # Suppress logging

    def do_GET(self):
        """Handle the OAuth callback."""
        query = parse_qs(urlparse(self.path).query)

        if 'code' in query:
            self.server.auth_code = query['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html><body style="font-family: system-ui; text-align: center; padding: 50px;">
                <h1>Authentication Successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                <script>window.close();</script>
                </body></html>
            """)
        elif 'error' in query:
            self.server.auth_error = query.get('error', ['Unknown error'])[0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Error: {self.server.auth_error}</h1></body></html>".encode())
        else:
            self.send_response(400)
            self.end_headers()


def do_oauth_flow(client_config: dict, login_hint: str = None, force_consent: bool = False) -> dict:
    """Perform OAuth flow with browser and local callback server.

    Args:
        client_config: OAuth client configuration
        login_hint: Email address to pre-select in Google account chooser
        force_consent: If True, force re-consent (needed for new refresh token)
    """
    client_id = client_config["installed"]["client_id"]
    client_secret = client_config["installed"]["client_secret"]

    # Find available port
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]

    redirect_uri = f"http://localhost:{port}"

    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)

    # Build authorization URL
    auth_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "state": state,
    }

    # Only prompt for consent when we need a new refresh token
    if force_consent:
        auth_params["prompt"] = "consent"

    # Pre-select the account if we know which one
    if login_hint:
        auth_params["login_hint"] = login_hint

    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(auth_params)}"

    # Start local server
    server = HTTPServer(('localhost', port), OAuthCallbackHandler)
    server.auth_code = None
    server.auth_error = None
    server.timeout = 120  # 2 minute timeout

    # Clear message about which account
    print("\n" + "="*50)
    if login_hint:
        print(f"  AUTHENTICATING: {login_hint}")
    else:
        print(f"  AUTHENTICATING: New account")
    print("="*50)
    print(f"Opening browser - select the account above.")
    print(f"If browser doesn't open, visit:\n{auth_url}\n")

    # Open browser
    webbrowser.open(auth_url)

    # Wait for callback
    while server.auth_code is None and server.auth_error is None:
        server.handle_request()

    if server.auth_error:
        print(f"Authentication error: {server.auth_error}")
        sys.exit(1)

    # Exchange code for tokens
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": server.auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    if response.status_code != 200:
        print(f"Token exchange failed: {response.text}")
        sys.exit(1)

    tokens = response.json()

    # Calculate and store absolute expiry time
    if "expires_in" in tokens:
        from datetime import timedelta
        expiry = datetime.utcnow() + timedelta(seconds=tokens["expires_in"])
        tokens["expiry"] = expiry.isoformat() + "Z"

    # Get user email
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    user_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    if user_response.status_code == 200:
        tokens["email"] = user_response.json().get("email")

    return tokens


def get_token_path(account: Optional[str] = None) -> Path:
    """Get token file path for an account."""
    TOKENS_DIR.mkdir(parents=True, exist_ok=True)

    if account:
        # Sanitize email for filename
        safe_name = re.sub(r'[^\w\-.]', '_', account.lower())
        return TOKENS_DIR / f"token_{safe_name}.json"

    # Return default/first token
    tokens = list(TOKENS_DIR.glob("token_*.json"))
    if tokens:
        return tokens[0]

    return TOKENS_DIR / "token_default.json"


def load_accounts_meta() -> dict:
    """Load account metadata (labels, descriptions)."""
    if ACCOUNTS_META_FILE.exists():
        try:
            with open(ACCOUNTS_META_FILE) as f:
                return json.load(f)
        except:
            pass
    return {}


def save_accounts_meta(meta: dict):
    """Save account metadata."""
    with open(ACCOUNTS_META_FILE, "w") as f:
        json.dump(meta, f, indent=2)


def set_account_meta(email: str, label: str = None, description: str = None, is_default: bool = False):
    """Set metadata for an account."""
    meta = load_accounts_meta()
    if email not in meta:
        meta[email] = {}
    if label:
        meta[email]["label"] = label
    if description:
        meta[email]["description"] = description
    if is_default:
        # Clear default from other accounts
        for e in meta:
            meta[e]["is_default"] = False
        meta[email]["is_default"] = True
    save_accounts_meta(meta)


def list_accounts() -> list[dict]:
    """List all authenticated accounts with metadata."""
    accounts = []
    meta = load_accounts_meta()

    if TOKENS_DIR.exists():
        for token_file in TOKENS_DIR.glob("token_*.json"):
            try:
                with open(token_file) as f:
                    data = json.load(f)
                    email = data.get("email", "unknown")
                    account_meta = meta.get(email, {})
                    accounts.append({
                        "email": email,
                        "label": account_meta.get("label", ""),
                        "description": account_meta.get("description", ""),
                        "is_default": account_meta.get("is_default", False),
                        "file": str(token_file),
                    })
            except:
                pass
    return accounts


def resolve_account_email(account: Optional[str]) -> Optional[str]:
    """Resolve account alias (like 'epoch') to actual email address."""
    if not account:
        return None

    # If it looks like an email, return as-is
    if "@" in account:
        return account

    # Check if it's an alias in accounts metadata
    meta = load_accounts_meta()
    for email, info in meta.items():
        if info.get("label", "").lower() == account.lower():
            return email

    return account


def get_credentials(account: Optional[str] = None) -> Credentials:
    """Get or refresh OAuth2 credentials for an account."""
    client_config = get_client_config()

    # Resolve alias to email first
    account_email = resolve_account_email(account)
    token_path = get_token_path(account_email or account)

    creds = None
    stored_email = None

    # Load existing token
    if token_path.exists():
        try:
            with open(token_path) as f:
                token_data = json.load(f)

            stored_email = token_data.get("email")

            # Parse expiry if stored
            expiry = None
            if "expiry" in token_data:
                try:
                    expiry = datetime.fromisoformat(token_data["expiry"].replace("Z", "+00:00")).replace(tzinfo=None)
                except:
                    pass

            creds = Credentials(
                token=token_data.get("access_token"),
                refresh_token=token_data.get("refresh_token"),
                token_uri=GOOGLE_TOKEN_URL,
                client_id=client_config["installed"]["client_id"],
                client_secret=client_config["installed"]["client_secret"],
                scopes=SCOPES,
                expiry=expiry,
            )
        except Exception as e:
            print(f"Warning: Could not load existing token: {e}")

    # Refresh or get new credentials
    if not creds or not creds.valid:
        # Try refresh if we have a refresh token
        if creds and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Update stored token with new access token and expiry
                with open(token_path) as f:
                    token_data = json.load(f)
                token_data["access_token"] = creds.token
                if creds.expiry:
                    token_data["expiry"] = creds.expiry.replace(tzinfo=None).isoformat() + "Z"
                with open(token_path, "w") as f:
                    json.dump(token_data, f, indent=2)
                return creds  # Success - return refreshed creds
            except Exception as e:
                print(f"Token refresh failed, re-authenticating: {e}")
                creds = None

        if not creds:
            # Need new authentication - use stored email or resolved email for login_hint
            login_email = stored_email or account_email
            force_consent = True  # First time always needs consent for refresh token

            token_data = do_oauth_flow(client_config, login_hint=login_email, force_consent=force_consent)

            # Save token
            token_path = get_token_path(token_data.get("email", account))
            with open(token_path, "w") as f:
                json.dump(token_data, f, indent=2)

            print(f"Authenticated as: {token_data.get('email', 'unknown')}")

            creds = Credentials(
                token=token_data.get("access_token"),
                refresh_token=token_data.get("refresh_token"),
                token_uri=GOOGLE_TOKEN_URL,
                client_id=client_config["installed"]["client_id"],
                client_secret=client_config["installed"]["client_secret"],
                scopes=SCOPES,
            )

    return creds


def get_gmail_service(account: Optional[str] = None):
    """Build Gmail API service."""
    creds = get_credentials(account)
    return build("gmail", "v1", credentials=creds)


def get_people_service(account: Optional[str] = None):
    """Build People API service."""
    creds = get_credentials(account)
    return build("people", "v1", credentials=creds)


def decode_body(payload: dict) -> str:
    """Decode email body from payload."""
    body = ""

    if "body" in payload and payload["body"].get("data"):
        body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
    elif "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            if mime_type == "text/plain":
                if part["body"].get("data"):
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
                    break
            elif mime_type == "text/html" and not body:
                if part["body"].get("data"):
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
            elif mime_type.startswith("multipart/"):
                body = decode_body(part)
                if body:
                    break

    return body


def get_header(headers: list, name: str) -> str:
    """Get header value by name."""
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def format_email_summary(msg: dict) -> dict:
    """Format email message for summary display."""
    headers = msg.get("payload", {}).get("headers", [])

    return {
        "id": msg["id"],
        "threadId": msg.get("threadId"),
        "snippet": msg.get("snippet", ""),
        "from": get_header(headers, "From"),
        "to": get_header(headers, "To"),
        "subject": get_header(headers, "Subject"),
        "date": get_header(headers, "Date"),
        "labels": msg.get("labelIds", []),
    }


def format_email_full(msg: dict) -> dict:
    """Format full email message."""
    headers = msg.get("payload", {}).get("headers", [])
    payload = msg.get("payload", {})

    # Get attachments info
    attachments = []
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("filename"):
                attachments.append({
                    "filename": part["filename"],
                    "mimeType": part.get("mimeType"),
                    "size": part.get("body", {}).get("size", 0),
                })

    return {
        "id": msg["id"],
        "threadId": msg.get("threadId"),
        "from": get_header(headers, "From"),
        "to": get_header(headers, "To"),
        "cc": get_header(headers, "Cc"),
        "bcc": get_header(headers, "Bcc"),
        "subject": get_header(headers, "Subject"),
        "date": get_header(headers, "Date"),
        "labels": msg.get("labelIds", []),
        "body": decode_body(payload),
        "attachments": attachments,
        "snippet": msg.get("snippet", ""),
    }


# ============ Email Composition ============

def wrap_email_body(body: str, width: int = EMAIL_LINE_WIDTH) -> str:
    """Wrap email body text for readability (Superhuman style).

    Preserves paragraph breaks and handles each paragraph separately.
    """
    paragraphs = body.split('\n\n')
    wrapped_paragraphs = []

    for para in paragraphs:
        # Preserve intentional single line breaks within paragraphs
        lines = para.split('\n')
        wrapped_lines = []
        for line in lines:
            if line.strip():
                # Wrap each line, but preserve leading whitespace for signatures etc.
                leading_space = len(line) - len(line.lstrip())
                wrapped = textwrap.fill(
                    line.strip(),
                    width=width - leading_space,
                    break_long_words=False,
                    break_on_hyphens=False
                )
                if leading_space:
                    wrapped = '\n'.join(' ' * leading_space + l for l in wrapped.split('\n'))
                wrapped_lines.append(wrapped)
            else:
                wrapped_lines.append(line)
        wrapped_paragraphs.append('\n'.join(wrapped_lines))

    return '\n\n'.join(wrapped_paragraphs)


def create_message(to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> dict:
    """Create a message for sending.

    Returns a dict with 'raw' key containing base64url encoded email.
    """
    wrapped_body = wrap_email_body(body)
    message = MIMEText(wrapped_body)
    message['to'] = to
    message['subject'] = subject
    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw}


# ============ Commands ============

def cmd_accounts(args):
    """List authenticated accounts."""
    accounts = list_accounts()
    if not accounts:
        print(json.dumps({"accounts": [], "message": "No accounts authenticated yet"}))
    else:
        print(json.dumps({"accounts": accounts}, indent=2))


def cmd_logout(args):
    """Remove an account's credentials."""
    token_path = get_token_path(args.account)
    if token_path.exists():
        token_path.unlink()
        print(json.dumps({"success": True, "message": f"Logged out: {args.account or 'default account'}"}))
    else:
        print(json.dumps({"success": False, "message": "Account not found"}))


def cmd_label(args):
    """Set label/description for an account."""
    set_account_meta(
        email=args.email,
        label=args.label,
        description=args.description,
        is_default=args.default,
    )
    meta = load_accounts_meta().get(args.email, {})
    print(json.dumps({
        "success": True,
        "email": args.email,
        "label": meta.get("label", ""),
        "description": meta.get("description", ""),
        "is_default": meta.get("is_default", False),
    }, indent=2))


def cmd_search(args):
    """Search emails by query."""
    service = get_gmail_service(args.account)

    try:
        results = service.users().messages().list(
            userId="me",
            q=args.query,
            maxResults=args.max_results,
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            print(json.dumps({"results": [], "total": 0}))
            return

        # Fetch details for each message
        email_list = []
        for msg in messages:
            full_msg = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["From", "To", "Subject", "Date"],
            ).execute()
            email_list.append(format_email_summary(full_msg))

        output = {
            "query": args.query,
            "results": email_list,
            "total": len(email_list),
            "resultSizeEstimate": results.get("resultSizeEstimate", 0),
        }
        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cmd_read(args):
    """Read a specific email by ID."""
    service = get_gmail_service(args.account)

    try:
        msg = service.users().messages().get(
            userId="me",
            id=args.email_id,
            format="full" if args.format == "full" else "metadata",
        ).execute()

        if args.format == "full":
            output = format_email_full(msg)
        else:
            output = format_email_summary(msg)

        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def _collect_attachment_parts(payload: dict, parts_out: list):
    """Recursively collect parts with filenames + attachmentIds from a payload."""
    if payload.get("filename") and payload.get("body", {}).get("attachmentId"):
        parts_out.append(payload)
    for sub in payload.get("parts", []) or []:
        _collect_attachment_parts(sub, parts_out)


def cmd_attachment(args):
    """Download attachment(s) from an email."""
    service = get_gmail_service(args.account)

    try:
        msg = service.users().messages().get(
            userId="me",
            id=args.email_id,
            format="full",
        ).execute()

        parts = []
        _collect_attachment_parts(msg.get("payload", {}), parts)

        if not parts:
            print(json.dumps({"error": "no attachments found", "email_id": args.email_id}))
            sys.exit(1)

        out_dir = Path(args.out_dir).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)

        saved = []
        for part in parts:
            filename = part["filename"]
            if args.filename and args.filename != filename:
                continue
            att_id = part["body"]["attachmentId"]
            att = service.users().messages().attachments().get(
                userId="me",
                messageId=args.email_id,
                id=att_id,
            ).execute()
            data = base64.urlsafe_b64decode(att["data"])
            out_path = out_dir / filename
            with open(out_path, "wb") as f:
                f.write(data)
            saved.append({
                "filename": filename,
                "path": str(out_path),
                "size": len(data),
                "mimeType": part.get("mimeType"),
            })

        if args.filename and not saved:
            print(json.dumps({
                "error": f"attachment {args.filename!r} not found",
                "available": [p["filename"] for p in parts],
            }))
            sys.exit(1)

        print(json.dumps({"saved": saved}, indent=2))

    except HttpError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cmd_list(args):
    """List recent emails."""
    service = get_gmail_service(args.account)

    try:
        results = service.users().messages().list(
            userId="me",
            maxResults=args.max_results,
            labelIds=[args.label.upper()] if args.label else ["INBOX"],
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            print(json.dumps({"results": [], "total": 0}))
            return

        # Fetch details for each message
        email_list = []
        for msg in messages:
            full_msg = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["From", "To", "Subject", "Date"],
            ).execute()
            email_list.append(format_email_summary(full_msg))

        output = {
            "label": args.label or "INBOX",
            "results": email_list,
            "total": len(email_list),
        }
        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cmd_send(args):
    """Send an email."""
    # Get the sender's email from the token
    token_path = get_token_path(args.account)
    from_email = "unknown"
    if token_path.exists():
        try:
            with open(token_path) as f:
                token_data = json.load(f)
                from_email = token_data.get("email", args.account or "unknown")
        except:
            pass

    service = get_gmail_service(args.account)

    try:
        message = create_message(
            to=args.to,
            subject=args.subject,
            body=args.body,
            cc=args.cc,
            bcc=args.bcc,
        )

        result = service.users().messages().send(
            userId="me",
            body=message,
        ).execute()

        print(json.dumps({
            "success": True,
            "message_id": result.get("id"),
            "thread_id": result.get("threadId"),
            "to": args.to,
            "subject": args.subject,
            "from": from_email,
        }, indent=2))

    except HttpError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_mark_read(args):
    """Mark email(s) as read."""
    service = get_gmail_service(args.account)

    # Support multiple IDs
    email_ids = [id.strip() for id in args.email_ids.split(",")]

    results = []
    for email_id in email_ids:
        try:
            service.users().messages().modify(
                userId="me",
                id=email_id,
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()
            results.append({"id": email_id, "success": True})
        except HttpError as e:
            results.append({"id": email_id, "success": False, "error": str(e)})

    print(json.dumps({
        "action": "mark_read",
        "results": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["success"]),
    }, indent=2))


def cmd_mark_unread(args):
    """Mark email(s) as unread."""
    service = get_gmail_service(args.account)

    # Support multiple IDs
    email_ids = [id.strip() for id in args.email_ids.split(",")]

    results = []
    for email_id in email_ids:
        try:
            service.users().messages().modify(
                userId="me",
                id=email_id,
                body={"addLabelIds": ["UNREAD"]}
            ).execute()
            results.append({"id": email_id, "success": True})
        except HttpError as e:
            results.append({"id": email_id, "success": False, "error": str(e)})

    print(json.dumps({
        "action": "mark_unread",
        "results": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["success"]),
    }, indent=2))


def cmd_mark_done(args):
    """Archive email(s) - removes from inbox (Gmail 'e' shortcut)."""
    service = get_gmail_service(args.account)

    # Support multiple IDs
    email_ids = [id.strip() for id in args.email_ids.split(",")]

    results = []
    for email_id in email_ids:
        try:
            service.users().messages().modify(
                userId="me",
                id=email_id,
                body={"removeLabelIds": ["INBOX"]}
            ).execute()
            results.append({"id": email_id, "success": True})
        except HttpError as e:
            results.append({"id": email_id, "success": False, "error": str(e)})

    print(json.dumps({
        "action": "archive",
        "results": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["success"]),
    }, indent=2))


def cmd_unarchive(args):
    """Move email(s) back to inbox (undo archive)."""
    service = get_gmail_service(args.account)

    # Support multiple IDs
    email_ids = [id.strip() for id in args.email_ids.split(",")]

    results = []
    for email_id in email_ids:
        try:
            service.users().messages().modify(
                userId="me",
                id=email_id,
                body={"addLabelIds": ["INBOX"]}
            ).execute()
            results.append({"id": email_id, "success": True})
        except HttpError as e:
            results.append({"id": email_id, "success": False, "error": str(e)})

    print(json.dumps({
        "action": "unarchive",
        "results": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["success"]),
    }, indent=2))


def cmd_star(args):
    """Star email(s)."""
    service = get_gmail_service(args.account)

    # Support multiple IDs
    email_ids = [id.strip() for id in args.email_ids.split(",")]

    results = []
    for email_id in email_ids:
        try:
            service.users().messages().modify(
                userId="me",
                id=email_id,
                body={"addLabelIds": ["STARRED"]}
            ).execute()
            results.append({"id": email_id, "success": True})
        except HttpError as e:
            results.append({"id": email_id, "success": False, "error": str(e)})

    print(json.dumps({
        "action": "star",
        "results": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["success"]),
    }, indent=2))


def cmd_unstar(args):
    """Unstar email(s)."""
    service = get_gmail_service(args.account)

    # Support multiple IDs
    email_ids = [id.strip() for id in args.email_ids.split(",")]

    results = []
    for email_id in email_ids:
        try:
            service.users().messages().modify(
                userId="me",
                id=email_id,
                body={"removeLabelIds": ["STARRED"]}
            ).execute()
            results.append({"id": email_id, "success": True})
        except HttpError as e:
            results.append({"id": email_id, "success": False, "error": str(e)})

    print(json.dumps({
        "action": "unstar",
        "results": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["success"]),
    }, indent=2))


def create_reply_message(to: str, subject: str, body: str, in_reply_to: str = None, references: str = None, cc: str = None, bcc: str = None) -> dict:
    """Create a reply message with proper threading headers."""
    wrapped_body = wrap_email_body(body)
    message = MIMEText(wrapped_body)
    message['to'] = to
    message['subject'] = subject
    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc
    if in_reply_to:
        message['In-Reply-To'] = in_reply_to
    if references:
        message['References'] = references

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw}


def cmd_draft(args):
    """Create a draft email."""
    service = get_gmail_service(args.account)

    # Get the sender's email from the token
    token_path = get_token_path(args.account)
    from_email = "unknown"
    if token_path.exists():
        try:
            with open(token_path) as f:
                token_data = json.load(f)
                from_email = token_data.get("email", args.account or "unknown")
        except:
            pass

    try:
        in_reply_to = None
        references = None
        thread_id = getattr(args, 'thread_id', None)

        # If replying to a message, get its headers and thread for proper threading
        if args.reply_to_id:
            original = service.users().messages().get(
                userId="me",
                id=args.reply_to_id,
                format="metadata",
                metadataHeaders=["Message-ID", "References"]
            ).execute()

            # Get thread ID from original message
            thread_id = original.get('threadId')

            headers = {h['name']: h['value'] for h in original.get('payload', {}).get('headers', [])}
            original_message_id = headers.get('Message-ID', headers.get('Message-Id'))
            original_references = headers.get('References', '')

            if original_message_id:
                in_reply_to = original_message_id
                # References should include the original references plus the message we're replying to
                if original_references:
                    references = f"{original_references} {original_message_id}"
                else:
                    references = original_message_id

        # Create message with reply headers if available
        if in_reply_to:
            message = create_reply_message(
                to=args.to,
                subject=args.subject,
                body=args.body,
                in_reply_to=in_reply_to,
                references=references,
                cc=args.cc,
                bcc=args.bcc,
            )
        else:
            message = create_message(
                to=args.to,
                subject=args.subject,
                body=args.body,
                cc=args.cc,
                bcc=args.bcc,
            )

        # If replying to a thread, add threadId to keep draft in same conversation
        draft_body = {"message": message}
        if thread_id:
            draft_body["message"]["threadId"] = thread_id

        result = service.users().drafts().create(
            userId="me",
            body=draft_body,
        ).execute()

        print(json.dumps({
            "success": True,
            "draft_id": result.get("id"),
            "message_id": result.get("message", {}).get("id"),
            "thread_id": result.get("message", {}).get("threadId"),
            "to": args.to,
            "subject": args.subject,
            "from": from_email,
            "in_reply_to": in_reply_to,
        }, indent=2))

    except HttpError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_labels(args):
    """List all Gmail labels."""
    service = get_gmail_service(args.account)

    try:
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        output = {
            "labels": [
                {
                    "id": label["id"],
                    "name": label["name"],
                    "type": label.get("type"),
                }
                for label in labels
            ]
        }
        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def check_people_api_error(e: HttpError) -> bool:
    """Check if error is due to People API not being enabled and provide helpful message."""
    error_str = str(e)
    if "People API has not been used" in error_str or "accessNotConfigured" in error_str:
        # Extract project number from error if possible
        import re
        project_match = re.search(r'project (\d+)', error_str)
        project_id = project_match.group(1) if project_match else "YOUR_PROJECT"

        enable_url = f"https://console.developers.google.com/apis/api/people.googleapis.com/overview?project={project_id}"

        print(json.dumps({
            "error": "People API not enabled",
            "message": "The People API (Contacts) needs to be enabled in Google Cloud Console.",
            "enable_url": enable_url,
            "instructions": [
                f"1. Open: {enable_url}",
                "2. Click 'ENABLE' button",
                "3. Wait ~30 seconds for propagation",
                "4. Try again"
            ]
        }, indent=2))

        # Offer to open browser
        try:
            response = input("\nOpen Google Cloud Console to enable People API? [Y/n]: ").strip().lower()
            if response != 'n':
                webbrowser.open(enable_url)
        except:
            pass

        return True
    return False


def cmd_contacts(args):
    """List contacts."""
    service = get_people_service(args.account)

    try:
        results = service.people().connections().list(
            resourceName="people/me",
            pageSize=args.max_results,
            personFields="names,emailAddresses,phoneNumbers,organizations,addresses",
        ).execute()

        connections = results.get("connections", [])

        contact_list = []
        for person in connections:
            contact = {
                "resourceName": person.get("resourceName"),
                "names": [n.get("displayName") for n in person.get("names", [])],
                "emails": [e.get("value") for e in person.get("emailAddresses", [])],
                "phones": [p.get("value") for p in person.get("phoneNumbers", [])],
                "organizations": [
                    {
                        "name": o.get("name"),
                        "title": o.get("title"),
                    }
                    for o in person.get("organizations", [])
                ],
            }
            contact_list.append(contact)

        output = {
            "results": contact_list,
            "total": len(contact_list),
            "totalPeople": results.get("totalPeople"),
        }
        print(json.dumps(output, indent=2))

    except HttpError as e:
        if not check_people_api_error(e):
            print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cmd_search_contacts(args):
    """Search contacts by query."""
    service = get_people_service(args.account)

    try:
        # Warmup request (required by API)
        try:
            service.people().searchContacts(
                query="",
                readMask="names",
            ).execute()
        except HttpError as warmup_error:
            # Check if it's an API not enabled error
            if check_people_api_error(warmup_error):
                sys.exit(1)
            # Otherwise continue - warmup can fail for other reasons

        # Actual search
        results = service.people().searchContacts(
            query=args.query,
            readMask="names,emailAddresses,phoneNumbers,organizations",
        ).execute()

        contacts = results.get("results", [])

        contact_list = []
        for result in contacts:
            person = result.get("person", {})
            contact = {
                "resourceName": person.get("resourceName"),
                "names": [n.get("displayName") for n in person.get("names", [])],
                "emails": [e.get("value") for e in person.get("emailAddresses", [])],
                "phones": [p.get("value") for p in person.get("phoneNumbers", [])],
                "organizations": [
                    {
                        "name": o.get("name"),
                        "title": o.get("title"),
                    }
                    for o in person.get("organizations", [])
                ],
            }
            contact_list.append(contact)

        output = {
            "query": args.query,
            "results": contact_list,
            "total": len(contact_list),
        }
        print(json.dumps(output, indent=2))

    except HttpError as e:
        if not check_people_api_error(e):
            print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cmd_contact(args):
    """Get details for a specific contact."""
    service = get_people_service(args.account)

    try:
        person = service.people().get(
            resourceName=args.resource_name,
            personFields="names,emailAddresses,phoneNumbers,organizations,addresses,birthdays,biographies,urls",
        ).execute()

        output = {
            "resourceName": person.get("resourceName"),
            "names": person.get("names", []),
            "emails": person.get("emailAddresses", []),
            "phones": person.get("phoneNumbers", []),
            "organizations": person.get("organizations", []),
            "addresses": person.get("addresses", []),
            "birthdays": person.get("birthdays", []),
            "biographies": person.get("biographies", []),
            "urls": person.get("urls", []),
        }
        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def cmd_other_contacts(args):
    """List 'other contacts' - auto-created from email interactions."""
    service = get_people_service(args.account)

    try:
        all_contacts = []
        page_token = None

        while True:
            results = service.otherContacts().list(
                pageSize=min(args.max_results - len(all_contacts), 1000),
                readMask="names,emailAddresses,phoneNumbers",
                pageToken=page_token,
            ).execute()

            contacts = results.get("otherContacts", [])

            for person in contacts:
                contact = {
                    "resourceName": person.get("resourceName"),
                    "names": [n.get("displayName") for n in person.get("names", [])],
                    "emails": [e.get("value") for e in person.get("emailAddresses", [])],
                    "phones": [p.get("value") for p in person.get("phoneNumbers", [])],
                }
                # Only include contacts with a name or email
                if contact["names"] or contact["emails"]:
                    all_contacts.append(contact)

            page_token = results.get("nextPageToken")
            if not page_token or len(all_contacts) >= args.max_results:
                break

        output = {
            "results": all_contacts[:args.max_results],
            "total": len(all_contacts[:args.max_results]),
            "source": "other_contacts (auto-created from email interactions)",
        }
        print(json.dumps(output, indent=2))

    except HttpError as e:
        if not check_people_api_error(e):
            print(json.dumps({"error": str(e)}))
        sys.exit(1)


def add_account_arg(parser):
    """Add --account argument to a parser."""
    parser.add_argument(
        "--account", "-a",
        help="Email account to use (default: first authenticated account)",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Gmail Skill - Read, search, and send Gmail emails. Access Google contacts."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Accounts command
    accounts_parser = subparsers.add_parser("accounts", help="List authenticated accounts")
    accounts_parser.set_defaults(func=cmd_accounts)

    # Logout command
    logout_parser = subparsers.add_parser("logout", help="Remove account credentials")
    add_account_arg(logout_parser)
    logout_parser.set_defaults(func=cmd_logout)

    # Label command
    label_parser = subparsers.add_parser("label", help="Set label/description for an account")
    label_parser.add_argument("email", help="Email address to label")
    label_parser.add_argument("--label", "-l", help="Short label (e.g., 'work', 'personal')")
    label_parser.add_argument("--description", "-d", help="Description of the account")
    label_parser.add_argument("--default", action="store_true", help="Set as default account")
    label_parser.set_defaults(func=cmd_label)

    # Search emails command
    search_parser = subparsers.add_parser("search", help="Search emails by query")
    search_parser.add_argument("query", help="Gmail search query")
    search_parser.add_argument("--max-results", type=int, default=10, help="Max results (default: 10)")
    add_account_arg(search_parser)
    search_parser.set_defaults(func=cmd_search)

    # Read email command
    read_parser = subparsers.add_parser("read", help="Read a specific email")
    read_parser.add_argument("email_id", help="Email ID to read")
    read_parser.add_argument("--format", choices=["full", "minimal"], default="full", help="Output format")
    add_account_arg(read_parser)
    read_parser.set_defaults(func=cmd_read)

    # Attachment download command
    attachment_parser = subparsers.add_parser("attachment", help="Download attachment(s) from an email")
    attachment_parser.add_argument("email_id", help="Email ID to fetch attachments from")
    attachment_parser.add_argument("--out-dir", default=".", help="Directory to save attachments (default: .)")
    attachment_parser.add_argument("--filename", help="Download only this specific filename (default: all)")
    add_account_arg(attachment_parser)
    attachment_parser.set_defaults(func=cmd_attachment)

    # List emails command
    list_parser = subparsers.add_parser("list", help="List recent emails")
    list_parser.add_argument("--max-results", type=int, default=10, help="Max results (default: 10)")
    list_parser.add_argument("--label", default=None, help="Label/folder to list from")
    add_account_arg(list_parser)
    list_parser.set_defaults(func=cmd_list)

    # Send email command (REQUIRES USER CONFIRMATION)
    send_parser = subparsers.add_parser("send", help="Send an email (requires confirmation)")
    send_parser.add_argument("--to", "-t", required=True, help="Recipient email address")
    send_parser.add_argument("--subject", "-s", required=True, help="Email subject")
    send_parser.add_argument("--body", "-b", required=True, help="Email body text")
    send_parser.add_argument("--cc", help="CC recipients (comma-separated)")
    send_parser.add_argument("--bcc", help="BCC recipients (comma-separated)")
    add_account_arg(send_parser)
    send_parser.set_defaults(func=cmd_send)

    # Create draft command
    draft_parser = subparsers.add_parser("draft", help="Create a draft email")
    draft_parser.add_argument("--to", "-t", required=True, help="Recipient email address")
    draft_parser.add_argument("--subject", "-s", required=True, help="Email subject")
    draft_parser.add_argument("--body", "-b", required=True, help="Email body text")
    draft_parser.add_argument("--cc", help="CC recipients (comma-separated)")
    draft_parser.add_argument("--bcc", help="BCC recipients (comma-separated)")
    draft_parser.add_argument("--thread-id", dest="thread_id", help="Thread ID for threading")
    draft_parser.add_argument("--reply-to-id", dest="reply_to_id", help="Message ID to reply to (adds proper In-Reply-To headers)")
    add_account_arg(draft_parser)
    draft_parser.set_defaults(func=cmd_draft)

    # Mark as read command
    mark_read_parser = subparsers.add_parser("mark-read", help="Mark email(s) as read")
    mark_read_parser.add_argument("email_ids", help="Email ID(s) to mark as read (comma-separated for multiple)")
    add_account_arg(mark_read_parser)
    mark_read_parser.set_defaults(func=cmd_mark_read)

    # Mark as unread command
    mark_unread_parser = subparsers.add_parser("mark-unread", help="Mark email(s) as unread")
    mark_unread_parser.add_argument("email_ids", help="Email ID(s) to mark as unread (comma-separated for multiple)")
    add_account_arg(mark_unread_parser)
    mark_unread_parser.set_defaults(func=cmd_mark_unread)

    # Mark done (archive) command
    mark_done_parser = subparsers.add_parser("mark-done", help="Archive email(s) - remove from inbox (Gmail 'e' shortcut)")
    mark_done_parser.add_argument("email_ids", help="Email ID(s) to archive (comma-separated for multiple)")
    add_account_arg(mark_done_parser)
    mark_done_parser.set_defaults(func=cmd_mark_done)

    # Unarchive command (undo mark-done)
    unarchive_parser = subparsers.add_parser("unarchive", help="Move email(s) back to inbox (undo archive)")
    unarchive_parser.add_argument("email_ids", help="Email ID(s) to unarchive (comma-separated for multiple)")
    add_account_arg(unarchive_parser)
    unarchive_parser.set_defaults(func=cmd_unarchive)

    # Star command
    star_parser = subparsers.add_parser("star", help="Star email(s)")
    star_parser.add_argument("email_ids", help="Email ID(s) to star (comma-separated for multiple)")
    add_account_arg(star_parser)
    star_parser.set_defaults(func=cmd_star)

    # Unstar command
    unstar_parser = subparsers.add_parser("unstar", help="Unstar email(s)")
    unstar_parser.add_argument("email_ids", help="Email ID(s) to unstar (comma-separated for multiple)")
    add_account_arg(unstar_parser)
    unstar_parser.set_defaults(func=cmd_unstar)

    # Labels command
    labels_parser = subparsers.add_parser("labels", help="List Gmail labels")
    add_account_arg(labels_parser)
    labels_parser.set_defaults(func=cmd_labels)

    # Contacts command
    contacts_parser = subparsers.add_parser("contacts", help="List contacts")
    contacts_parser.add_argument("--max-results", type=int, default=100, help="Max results (default: 100)")
    add_account_arg(contacts_parser)
    contacts_parser.set_defaults(func=cmd_contacts)

    # Other contacts command (auto-created from interactions)
    other_contacts_parser = subparsers.add_parser("other-contacts", help="List contacts auto-created from email interactions")
    other_contacts_parser.add_argument("--max-results", type=int, default=500, help="Max results (default: 500)")
    add_account_arg(other_contacts_parser)
    other_contacts_parser.set_defaults(func=cmd_other_contacts)

    # Search contacts command
    search_contacts_parser = subparsers.add_parser("search-contacts", help="Search contacts")
    search_contacts_parser.add_argument("query", help="Search query")
    add_account_arg(search_contacts_parser)
    search_contacts_parser.set_defaults(func=cmd_search_contacts)

    # Get contact command
    contact_parser = subparsers.add_parser("contact", help="Get contact details")
    contact_parser.add_argument("resource_name", help="Contact resource name (e.g., people/c12345)")
    add_account_arg(contact_parser)
    contact_parser.set_defaults(func=cmd_contact)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
