import json, os, argparse, subprocess, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from urllib import request
import msal

# File paths
TOKEN_CACHE_FILE = os.path.expanduser('~/.openclaw/ms_tokens.json')
OPENCLAW_CONFIG = os.path.expanduser('~/.openclaw/openclaw.json')
NOTIFIED_FILE = os.path.expanduser('~/.openclaw/notified_emails.json')
SCOPES = ['Mail.ReadWrite', 'Mail.Send', 'Calendars.ReadWrite', 'User.Read']

# Skills root directory (computed relative to this script for portability)
_SKILLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
OUTLOOK_SCRIPT = os.path.normpath(os.path.join(_SKILLS_DIR, 'outlook-graph', 'scripts', 'outlook_graph.py'))

GMAIL_ACCOUNT = os.environ.get('EMAIL_MONITOR_GMAIL_ACCOUNT', '')
TELEGRAM_USER = os.environ.get('EMAIL_MONITOR_TELEGRAM_USER', '')

# Outlook is enabled if the MSAL token cache file exists
OUTLOOK_ENABLED = os.path.isfile(TOKEN_CACHE_FILE)
# Gmail is enabled if the user provided a Gmail account env var
GMAIL_ENABLED = bool(GMAIL_ACCOUNT)

if not OUTLOOK_ENABLED and not GMAIL_ENABLED:
    raise RuntimeError(
        'Neither Outlook nor Gmail is configured. '
        'Configure at least one: '
        f'set up Outlook by creating {TOKEN_CACHE_FILE}, '
        'or enable Gmail by setting EMAIL_MONITOR_GMAIL_ACCOUNT.'
    )
if not TELEGRAM_USER:
    raise RuntimeError('Missing EMAIL_MONITOR_TELEGRAM_USER. Set it to the Telegram chat ID that should receive notifications.')


def _find_openclaw():
    """Dynamically locate the openclaw executable to avoid hardcoded paths."""
    found = shutil.which('openclaw')
    if found:
        return found
    for candidate in [
        os.path.expanduser('~/.npm-global/bin/openclaw'),
        '/usr/local/bin/openclaw',
        '/usr/bin/openclaw',
    ]:
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError('openclaw binary not found; make sure it is installed and on PATH')


OPENCLAW_BIN = _find_openclaw()


# ── Outlook ──────────────────────────────────────────────────────────────────

def get_access_token():
    """Load and auto-refresh the access token from ms_tokens.json."""
    with open(TOKEN_CACHE_FILE) as f:
        data = json.load(f)

    client_id = data['client_id']
    cache = msal.SerializableTokenCache()
    cache.deserialize(data['cache'])

    app = msal.PublicClientApplication(
        client_id,
        authority='https://login.microsoftonline.com/consumers',
        token_cache=cache
    )

    accounts = app.get_accounts()
    if not accounts:
        raise Exception('No accounts found; run get_token.py on Windows to complete initial authorization')

    result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if 'access_token' not in result:
        raise Exception(f'Token refresh failed: {result}')

    # If the token cache changed, write it back to disk and update the main config
    if cache.has_state_changed:
        data['cache'] = cache.serialize()
        with open(TOKEN_CACHE_FILE, 'w') as f:
            json.dump(data, f)

        with open(OPENCLAW_CONFIG) as f:
            config = json.load(f)
        config['env']['MS_GRAPH_ACCESS_TOKEN'] = result['access_token']
        with open(OPENCLAW_CONFIG, 'w') as f:
            json.dump(config, f, indent=2)

    return result['access_token']


def graph_get(path, token):
    """Perform a GET request against Microsoft Graph API."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    req = request.Request(
        f'https://graph.microsoft.com/v1.0{path}',
        headers=headers
    )
    resp = request.urlopen(req)
    return json.loads(resp.read())


def fetch_outlook_unread(token):
    """Fetch unread emails from the Outlook inbox (up to 20)."""
    data = graph_get(
        "/me/mailFolders('inbox')/messages"
        "?$top=20"
        "&$orderby=receivedDateTime%20desc"
        "&$filter=isRead%20eq%20false"
        "&$select=id,subject,from,receivedDateTime,bodyPreview,isRead",
        token
    )
    emails = []
    for e in data.get('value', []):
        emails.append({
            'source': 'outlook',
            'id': e['id'],
            'subject': e['subject'],
            'from': e['from']['emailAddress']['address'],
            'from_name': e['from']['emailAddress']['name'],
            'received': e['receivedDateTime'],
            'preview': e['bodyPreview'][:500],
            'is_meeting_invite': is_meeting_invite_text(e['subject'], e['bodyPreview']),
        })
    return emails


def fetch_outlook_unread_full():
    """Combined token refresh + unread fetch; intended as a single unit of work for the thread pool."""
    token = get_access_token()
    return fetch_outlook_unread(token)


# ── Gmail ─────────────────────────────────────────────────────────────────────

def fetch_gmail_unread():
    """Fetch unread Gmail emails via the gog CLI."""
    try:
        env = os.environ.copy()
        env['GOG_ACCOUNT'] = GMAIL_ACCOUNT
        # file keyring backend needs this env var in non-interactive contexts (cron); empty means no password
        env.setdefault('GOG_KEYRING_PASSWORD', '')
        result = subprocess.run(
            ['gog', 'gmail', 'search', 'is:unread', '--max', '20',
             '--json', '--no-input', '--results-only'],
            capture_output=True, text=True, timeout=30, env=env
        )
        if result.returncode != 0:
            print(f'Gmail fetch failed: {result.stderr.strip()}', file=sys.stderr)
            return []

        data = json.loads(result.stdout)
        threads = data if isinstance(data, list) else data.get('threads', [])

        emails = []
        for t in threads:
            subject = t.get('subject', '(no subject)')
            from_raw = t.get('from', '')
            emails.append({
                'source': 'gmail',
                'id': f"gmail:{t['id']}",
                'subject': subject,
                'from': from_raw,
                'from_name': from_raw,
                'received': t.get('date', ''),
                'preview': '',   # gog thread search does not return body; AI can use `gog gmail view` to get it
                'is_meeting_invite': is_meeting_invite_text(subject, ''),
                'thread_id': t['id'],
            })
        return emails
    except Exception as e:
        print(f'Gmail fetch exception: {e}', file=sys.stderr)
        return []


# ── Shared utilities ─────────────────────────────────────────────────────────

def is_meeting_invite_text(subject, body):
    """Detect whether the subject/body looks like a meeting or event invitation."""
    text = (subject + ' ' + body).lower()
    keywords = ['invite', 'invitation', 'meeting', 'calendar',
                '邀请', '会议', '日程', 'appointment', 'schedule',
                'event', 'conference', 'webinar', 'zoom', 'teams']
    return any(word in text for word in keywords)


def load_notified():
    """Load the set of already-notified email IDs."""
    if os.path.exists(NOTIFIED_FILE):
        with open(NOTIFIED_FILE) as f:
            return set(json.load(f))
    return set()


def save_notified(ids):
    """Persist notified IDs; cap at 1000 entries to prevent unbounded growth."""
    if len(ids) > 1000:
        ids = set(list(ids)[-1000:])
    with open(NOTIFIED_FILE, 'w') as f:
        json.dump(list(ids), f)


# ── Main actions ─────────────────────────────────────────────────────────────

def check_new_emails():
    """Check unread emails across the enabled mailboxes concurrently (intended for manual agent calls)."""
    notified = load_notified()
    result = {'outlook': [], 'gmail': [], 'errors': []}

    # Fire off the enabled providers in parallel; the two network paths are independent.
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {}
        if OUTLOOK_ENABLED:
            futures['outlook'] = executor.submit(fetch_outlook_unread_full)
        else:
            result['outlook_skipped'] = 'Outlook not configured'

        if GMAIL_ENABLED:
            futures['gmail'] = executor.submit(fetch_gmail_unread)
        else:
            result['gmail_skipped'] = 'Gmail not configured (set EMAIL_MONITOR_GMAIL_ACCOUNT)'

        if 'outlook' in futures:
            try:
                outlook_emails = futures['outlook'].result()
                result['outlook'] = [e for e in outlook_emails if e['id'] not in notified]
            except Exception as e:
                result['errors'].append(f'Outlook error: {e}')

        if 'gmail' in futures:
            gmail_emails = futures['gmail'].result()
            result['gmail'] = [e for e in gmail_emails if e['id'] not in notified]

    total = len(result['outlook']) + len(result['gmail'])
    result['count'] = total
    print(json.dumps(result, ensure_ascii=False, indent=2))


def mark_notified(email_id):
    """Mark a specific email as notified to prevent duplicate notifications."""
    notified = load_notified()
    notified.add(email_id)
    save_notified(notified)
    print(json.dumps({'status': 'marked', 'id': email_id}))


def auto_notify():
    """
    Automated notification flow (invoked by cron):
    - Layer 1: Pure-Python check across Outlook + Gmail; no AI, no token cost.
    - Layer 2: Only if new emails are detected, invoke AI to summarize and push to Telegram.
    """
    notified = load_notified()
    new_emails = []
    errors = []

    # Run Outlook and Gmail fetches in parallel; only the configured providers are submitted.
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {}
        if OUTLOOK_ENABLED:
            futures['outlook'] = executor.submit(fetch_outlook_unread_full)
        else:
            print('Outlook not configured, skipping.')

        if GMAIL_ENABLED:
            futures['gmail'] = executor.submit(fetch_gmail_unread)
        else:
            print('Gmail not configured, skipping.')

        if 'outlook' in futures:
            try:
                for e in futures['outlook'].result():
                    if e['id'] not in notified:
                        new_emails.append(e)
            except Exception as e:
                errors.append(f'Outlook error: {e}')
                print(f'Outlook error: {e}', file=sys.stderr)

        if 'gmail' in futures:
            for e in futures['gmail'].result():
                if e['id'] not in notified:
                    new_emails.append(e)

    if not new_emails:
        print('No new emails from Outlook or Gmail; skipping AI call.')
        return

    print(f'Found {len(new_emails)} new email(s) '
          f'(Outlook: {sum(1 for e in new_emails if e["source"]=="outlook")}, '
          f'Gmail: {sum(1 for e in new_emails if e["source"]=="gmail")}); '
          f'invoking AI...')

    # Build calendar-check instructions only for the providers that are enabled
    calendar_lines = []
    if OUTLOOK_ENABLED:
        calendar_lines.append(f'    Outlook: python3 {OUTLOOK_SCRIPT} calendar-list --days 7 --top 20')
    if GMAIL_ENABLED:
        calendar_lines.append(f'    Google:  GOG_KEYRING_PASSWORD="" GOG_ACCOUNT={GMAIL_ACCOUNT} gog calendar events primary --from $(date -u +%Y-%m-%dT%H:%M:%SZ) --to $(date -u -d \'+7 days\' +%Y-%m-%dT%H:%M:%SZ) --json --no-input')
    calendar_block = '\n'.join(calendar_lines) if calendar_lines else '    (no calendars configured)'

    gmail_body_line = (
        f'- For Gmail emails, fetch full body: GOG_KEYRING_PASSWORD="" GOG_ACCOUNT={GMAIL_ACCOUNT} gog gmail view <thread_id> --no-input'
        if GMAIL_ENABLED else ''
    )

    # Prompt sent to the AI; output must be in English (the bot reply language)
    email_summary = json.dumps(new_emails, ensure_ascii=False, indent=2)
    message = f"""Process these {len(new_emails)} new unread email(s). Do everything silently — no step headers, no internal notes, no follow-up questions. Output ONLY the final notification block in English.

DO SILENTLY (no output for these):
{gmail_body_line}
- For any is_meeting_invite=true, check the configured calendar(s):
{calendar_block}
- Mark every email: python3 {__file__} mark --id "<EMAIL_ID>"

OUTPUT (exactly this format, nothing else, all in English):
📬 {len(new_emails)} new email(s)

[One block per email:]
[Outlook/Gmail] From: <name> <email>
Subject: <subject>
Summary: <1-2 sentence summary in English>
[Only if is_meeting_invite=true] Event time: <time> | ⚠️ Conflicts with "<event>" / ✅ No conflict

Emails:
{email_summary}"""

    result = subprocess.run([
        OPENCLAW_BIN, 'agent',
        '--message', message,
        '--deliver',
        '--to', TELEGRAM_USER
    ])

    # Only mark as notified if delivery succeeded; otherwise the next cron run will retry
    if result.returncode == 0:
        for email in new_emails:
            notified.add(email['id'])
        save_notified(notified)
        print(f'Successfully notified and marked {len(new_emails)} email(s).')
    else:
        print(f'AI or delivery failed (returncode={result.returncode}); will retry on next cron run.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unified monitor for unread emails across Outlook and Gmail')
    parser.add_argument('action', choices=['check', 'mark', 'clear', 'auto-notify'],
                        help='Action: check=list unread; mark=mark as notified; clear=clear all records; auto-notify=check and push automatically')
    parser.add_argument('--id', help='Email ID to mark as notified')
    args = parser.parse_args()

    if args.action == 'check':
        check_new_emails()
    elif args.action == 'mark':
        if not args.id:
            print('--id is required for the mark action')
            sys.exit(1)
        mark_notified(args.id)
    elif args.action == 'clear':
        save_notified(set())
        print(json.dumps({'status': 'cleared'}))
    elif args.action == 'auto-notify':
        auto_notify()
