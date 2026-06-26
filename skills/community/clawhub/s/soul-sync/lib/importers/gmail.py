#!/usr/bin/env python3
"""
Gmail Importer v2 — Analyzes recent emails to extract personality insights.

Classifies emails into categories (personal, work, transactional, marketing/newsletters)
and extracts different signals from each:
- Personal: communication style, tone, key relationships
- Work: industry, role signals, work patterns
- Newsletters/Marketing: actual interests (what they subscribe to)
- Transactional: spending patterns, services used (light signals)
- Spam/Noise: ignored entirely

Processes locally. Raw email content is never stored — only synthesized insights.
"""
import os
import sys
import json
import re
import base64
from datetime import datetime, timezone
from email.utils import parseaddr
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
MAX_EMAILS = 300  # Analyze last N emails (mix of sent + inbox)
MAX_SENT = 150
MAX_INBOX = 150


# === Email Classification ===

# Domains/patterns that indicate transactional/automated emails
TRANSACTIONAL_SENDERS = {
    "noreply", "no-reply", "donotreply", "do-not-reply", "mailer-daemon",
    "notifications", "notification", "alert", "alerts", "billing",
    "receipt", "receipts", "orders", "shipping", "tracking",
    "verify", "verification", "confirm", "confirmation", "security",
    "support", "help", "info", "admin", "system", "automated",
    "postmaster", "bounce",
}

TRANSACTIONAL_DOMAINS = {
    "amazonses.com", "sendgrid.net", "mailchimp.com", "constantcontact.com",
    "mailgun.org", "sparkpostmail.com", "mandrillapp.com",
}

SPAM_SUBJECT_PATTERNS = [
    r"(?i)unsubscribe", r"(?i)verify your", r"(?i)confirm your",
    r"(?i)reset your password", r"(?i)security alert",
    r"(?i)your order", r"(?i)order confirmation", r"(?i)shipping confirmation",
    r"(?i)delivery notification", r"(?i)tracking number",
    r"(?i)your receipt", r"(?i)payment received", r"(?i)invoice",
    r"(?i)your statement", r"(?i)account update",
    r"(?i)act now", r"(?i)limited time", r"(?i)exclusive offer",
    r"(?i)you've been selected", r"(?i)congratulations",
    r"(?i)click here", r"(?i)sign up",
]

# Subject patterns that indicate newsletters/marketing (but contain interest signals)
NEWSLETTER_PATTERNS = [
    r"(?i)weekly digest", r"(?i)daily digest", r"(?i)newsletter",
    r"(?i)this week in", r"(?i)top stories", r"(?i)what's new",
    r"(?i)roundup", r"(?i)\bnews\b", r"(?i)update from",
    r"(?i)new episode", r"(?i)new post", r"(?i)just published",
]

# Known newsletter/content sender patterns → interest categories
INTEREST_SENDER_MAP = {
    # Bitcoin / Crypto
    "bitcoin": "Bitcoin & Cryptocurrency",
    "crypto": "Cryptocurrency",
    "lightning": "Lightning Network",
    "coindesk": "Cryptocurrency News",
    "coinbase": "Cryptocurrency",
    "blockfi": "Crypto Finance",
    "swan": "Bitcoin",
    "river": "Bitcoin",
    "strike": "Bitcoin/Lightning",
    "fold": "Bitcoin Rewards",
    # Tech
    "github": "Software Development",
    "gitlab": "Software Development",
    "hackernews": "Tech News",
    "ycombinator": "Tech / Startups",
    "techcrunch": "Tech News",
    "theverge": "Tech News",
    "wired": "Technology",
    "arstechnica": "Technology",
    "substack": "Independent Writing",
    # AI
    "openai": "Artificial Intelligence",
    "anthropic": "AI Research",
    "huggingface": "Machine Learning",
    # Home / Energy
    "solar": "Solar Energy",
    "tesla": "Electric Vehicles / Tesla",
    "homeassistant": "Home Automation",
    # Finance
    "robinhood": "Stock Trading",
    "schwab": "Investing",
    "fidelity": "Investing",
    "baird": "Financial Advisory",
    "vanguard": "Investing",
    # Shopping / Services (light signals)
    "amazon": "Online Shopping",
    "ebay": "Online Shopping",
}


def classify_email(from_addr, from_name, subject, labels):
    """Classify an email into a category.
    
    Returns: 'personal', 'work', 'newsletter', 'transactional', or 'spam'
    """
    from_lower = from_addr.lower()
    from_name_lower = (from_name or "").lower()
    subject_lower = (subject or "").lower()
    label_set = set(labels or [])

    # Gmail's own spam/trash
    if "SPAM" in label_set or "TRASH" in label_set:
        return "spam"

    # Check sender for transactional patterns
    local_part = from_lower.split("@")[0] if "@" in from_lower else ""
    domain = from_lower.split("@")[1] if "@" in from_lower else ""

    if local_part in TRANSACTIONAL_SENDERS:
        # But check if it's a newsletter first
        for pattern in NEWSLETTER_PATTERNS:
            if re.search(pattern, subject or ""):
                return "newsletter"
        return "transactional"

    if any(d in domain for d in TRANSACTIONAL_DOMAINS):
        return "transactional"

    # Check subject for spam patterns
    spam_score = sum(1 for p in SPAM_SUBJECT_PATTERNS if re.search(p, subject or ""))
    if spam_score >= 2:
        return "transactional"

    # Check for newsletter patterns
    for pattern in NEWSLETTER_PATTERNS:
        if re.search(pattern, subject or ""):
            return "newsletter"

    # Promotions label = marketing/newsletter
    if "CATEGORY_PROMOTIONS" in label_set:
        return "newsletter"

    # Social label
    if "CATEGORY_SOCIAL" in label_set:
        return "newsletter"

    # Forums label
    if "CATEGORY_FORUMS" in label_set:
        return "newsletter"

    # Updates label — likely transactional
    if "CATEGORY_UPDATES" in label_set:
        return "transactional"

    # If it's in SENT, it's personal or work
    if "SENT" in label_set:
        return "personal"

    # Default: if it's in primary inbox, it's personal
    if "CATEGORY_PERSONAL" in label_set or "INBOX" in label_set:
        return "personal"

    return "personal"


def extract_interest_from_sender(from_addr, from_name):
    """Try to derive an interest category from the sender."""
    combined = f"{from_addr} {from_name or ''}".lower()
    for keyword, interest in INTEREST_SENDER_MAP.items():
        if keyword in combined:
            return interest
    return None


def extract_interest_from_subject(subject):
    """Try to derive interest topics from newsletter/marketing subjects."""
    if not subject:
        return []
    
    interests = []
    lower = subject.lower()
    
    # Topic keyword detection
    topic_keywords = {
        "bitcoin": "Bitcoin",
        "btc": "Bitcoin",
        "lightning network": "Lightning Network",
        "crypto": "Cryptocurrency",
        "ethereum": "Ethereum",
        "ai ": "Artificial Intelligence",
        "artificial intelligence": "Artificial Intelligence",
        "machine learning": "Machine Learning",
        "llm": "Large Language Models",
        "open source": "Open Source",
        "solar": "Solar Energy",
        "home automation": "Home Automation",
        "smart home": "Smart Home",
        "3d print": "3D Printing",
        "raspberry pi": "Raspberry Pi / SBC",
        "self-host": "Self-Hosting",
        "privacy": "Digital Privacy",
        "security": "Cybersecurity",
        "linux": "Linux",
        "docker": "Containers / Docker",
        "kubernetes": "Kubernetes",
        "python": "Python",
        "node.js": "Node.js",
        "javascript": "JavaScript",
        "rust": "Rust",
        "nostr": "Nostr / Decentralized Social",
        "decentraliz": "Decentralization",
        "sovereign": "Digital Sovereignty",
        "self-improv": "Self Improvement",
        "productiv": "Productivity",
        "startup": "Startups",
        "entrepren": "Entrepreneurship",
        "real estate": "Real Estate",
        "invest": "Investing",
        "trading": "Trading",
        "options": "Options Trading",
        "photo booth": "Photo Booth / Events",
        "event": "Events Industry",
    }
    
    for keyword, topic in topic_keywords.items():
        if keyword in lower:
            interests.append(topic)
    
    return interests


def get_gmail_service():
    """Initialize Gmail API service."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        print(json.dumps({"error": "Gmail dependencies not installed. Run: pip install google-auth-oauthlib google-api-python-client"}))
        sys.exit(1)

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None

    token_paths = [
        os.path.join(WORKSPACE, "mission-control", "data", "gmail_token.json"),
        os.path.join(WORKSPACE, "email-agent", "token.json"),
        os.path.join(WORKSPACE, "token.json"),
    ]
    creds_paths = [
        os.path.join(WORKSPACE, "mission-control", "credentials.json"),
        os.path.join(WORKSPACE, "email-agent", "credentials.json"),
        os.path.join(WORKSPACE, "credentials.json"),
    ]

    token_path = next((p for p in token_paths if os.path.exists(p)), None)
    creds_path = next((p for p in creds_paths if os.path.exists(p)), None)

    if token_path:
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif creds_path:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            print(json.dumps({"error": "No Gmail credentials found. Need credentials.json for OAuth."}))
            sys.exit(1)

    return build("gmail", "v1", credentials=creds)


def analyze_emails(service):
    """Fetch and analyze emails across multiple categories for personality insights."""
    
    # === Fetch sent emails (communication style) ===
    sent_results = service.users().messages().list(
        userId="me", maxResults=MAX_SENT, labelIds=["SENT"]
    ).execute()
    sent_messages = sent_results.get("messages", [])

    # === Fetch inbox emails (interests, subscriptions, relationships) ===
    inbox_results = service.users().messages().list(
        userId="me", maxResults=MAX_INBOX, labelIds=["INBOX"]
    ).execute()
    inbox_messages = inbox_results.get("messages", [])

    # === Process all messages ===
    categories = {"personal": [], "work": [], "newsletter": [], "transactional": [], "spam": []}
    recipients = Counter()
    senders = Counter()
    send_hours = [0] * 24
    send_days = [0] * 7
    total_sent_length = 0
    sent_count = 0
    interest_signals = Counter()  # topic → count (more mentions = stronger signal)
    services_used = set()
    newsletter_senders = Counter()

    all_messages = [(m, "SENT") for m in sent_messages] + [(m, "INBOX") for m in inbox_messages]

    for msg_meta, source_label in all_messages:
        try:
            msg = service.users().messages().get(
                userId="me", id=msg_meta["id"], format="metadata",
                metadataHeaders=["To", "From", "Subject", "Date", "List-Unsubscribe"]
            ).execute()

            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            labels = msg.get("labelIds", [])
            
            # Parse sender
            from_raw = headers.get("From", "")
            from_name, from_addr = parseaddr(from_raw)
            
            # Parse subject
            subject = headers.get("Subject", "")
            
            # Has unsubscribe header? Strong newsletter signal
            has_unsub = "List-Unsubscribe" in headers

            # Classify
            category = classify_email(from_addr, from_name, subject, labels)
            
            # Override: if it has List-Unsubscribe, it's a newsletter/marketing
            if has_unsub and category == "personal":
                category = "newsletter"

            categories[category].append({
                "from": from_addr,
                "from_name": from_name,
                "subject": subject,
                "labels": labels,
            })

            # === Extract signals based on category ===

            if source_label == "SENT":
                # Track recipients
                to = headers.get("To", "")
                _, to_email = parseaddr(to)
                if to_email:
                    recipients[to_email] += 1

                # Track timing
                date_str = headers.get("Date", "")
                if date_str:
                    try:
                        from email.utils import parsedate_to_datetime
                        dt = parsedate_to_datetime(date_str)
                        send_hours[dt.hour] += 1
                        send_days[dt.weekday()] += 1
                    except Exception:
                        pass

                # Track message size (for communication style)
                total_sent_length += msg.get("sizeEstimate", 0)
                sent_count += 1

            if category == "newsletter":
                # Extract interest from sender
                interest = extract_interest_from_sender(from_addr, from_name)
                if interest:
                    interest_signals[interest] += 1
                
                # Extract interest from subject
                subject_interests = extract_interest_from_subject(subject)
                for si in subject_interests:
                    interest_signals[si] += 1
                
                newsletter_senders[from_addr] += 1

            elif category == "transactional":
                # Light signal: what services do they use?
                domain = from_addr.split("@")[1] if "@" in from_addr else ""
                base_domain = ".".join(domain.split(".")[-2:]) if domain else ""
                if base_domain and base_domain not in {"gmail.com", "yahoo.com", "outlook.com"}:
                    services_used.add(base_domain)

            elif category == "personal" and source_label == "INBOX":
                # Track who sends them personal email
                if from_addr:
                    senders[from_addr] += 1

        except Exception:
            continue

    # === Synthesize Insights ===

    # Communication style (from sent emails)
    avg_length = total_sent_length // max(sent_count, 1)
    if avg_length < 500:
        comm_style = "concise and to-the-point"
    elif avg_length < 2000:
        comm_style = "balanced — detailed when needed, brief when not"
    elif avg_length < 5000:
        comm_style = "thorough and detailed"
    else:
        comm_style = "very detailed writer"

    # Work patterns
    peak_hours = sorted(range(24), key=lambda h: send_hours[h], reverse=True)[:3]
    peak_days = sorted(range(7), key=lambda d: send_days[d], reverse=True)[:3]
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    weekend_total = send_days[5] + send_days[6]
    total_sends = sum(send_days) or 1
    weekend_pct = weekend_total / total_sends * 100
    
    night_total = sum(send_hours[22:]) + sum(send_hours[:6])
    total_hourly = sum(send_hours) or 1
    night_pct = night_total / total_hourly * 100

    patterns = f"Most active: {', '.join(f'{h}:00' for h in peak_hours)}"
    patterns += f"; Busiest days: {', '.join(day_names[d] for d in peak_days)}"
    if weekend_pct < 10:
        patterns += "; Rarely emails on weekends"
    elif weekend_pct > 30:
        patterns += "; Frequently active on weekends"
    if night_pct > 20:
        patterns += "; Night owl"

    # Tone estimation
    if avg_length < 800:
        tone = "concise communicator — gets to the point"
    elif avg_length < 3000:
        tone = "balanced communicator — adapts length to context"
    else:
        tone = "detailed communicator — provides thorough context"

    # Top interests (sorted by signal strength)
    top_interests = [topic for topic, count in interest_signals.most_common(15) if count >= 1]

    # Key contacts (from sent — who they write to most)
    top_recipients = [email for email, _ in recipients.most_common(10)]
    
    # People who write to them most (from inbox personal)
    top_senders = [email for email, _ in senders.most_common(10)]
    
    # Merge contacts: sent recipients are stronger signal
    all_contacts = []
    seen = set()
    for c in top_recipients + top_senders:
        if c not in seen:
            seen.add(c)
            all_contacts.append(c)
    all_contacts = all_contacts[:10]

    # Category breakdown (useful for understanding email habits)
    category_counts = {k: len(v) for k, v in categories.items()}

    return {
        "source": "gmail",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "communication_style": comm_style,
            "key_contacts": all_contacts,
            "interests": top_interests,
            "work_patterns": patterns,
            "tone": tone,
            "services_used": sorted(services_used)[:15],
            "top_newsletter_senders": [s for s, _ in newsletter_senders.most_common(10)],
        },
        "email_breakdown": category_counts,
        "confidence": min(sent_count / MAX_SENT, 1.0),
        "items_processed": len(all_messages),
        "details": {
            "sent_analyzed": sent_count,
            "inbox_analyzed": len(inbox_messages),
            "avg_sent_size_bytes": avg_length,
            "interests_signal_strength": dict(interest_signals.most_common(20)),
        }
    }


if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)

    if "--check" in sys.argv:
        try:
            service = get_gmail_service()
            print(json.dumps({"available": True}))
        except Exception as e:
            print(json.dumps({"available": False, "error": str(e)}))
        sys.exit(0)

    try:
        service = get_gmail_service()
        result = analyze_emails(service)

        output_path = os.path.join(IMPORT_DIR, "gmail.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
