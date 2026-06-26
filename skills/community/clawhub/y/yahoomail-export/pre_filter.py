#!/usr/bin/env python3
"""
Pre-filter: Rule-based email triage. No LLM needed.
Reads emails.jsonl, applies rules, outputs filtered results.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

# EDIT THIS: Set your base directory for the email purge project
BASE_DIR = Path("~/email-purge").expanduser()
META_FILE = BASE_DIR / "metadata" / "emails.jsonl"
FILTERED_FILE = BASE_DIR / "filtered" / "pre_filter_results.jsonl"
KEEP_FILE = BASE_DIR / "filtered" / "keep.jsonl"
DROP_FILE = BASE_DIR / "filtered" / "drop.jsonl"
REVIEW_FILE = BASE_DIR / "filtered" / "needs_review.jsonl"
STATS_FILE = BASE_DIR / "filtered" / "stats.json"

# --- VIP / Important Senders ---
# EDIT THIS: Add email addresses or domains that should always be kept
# Examples: employers, courts, important clients
VIP_SENDERS = {
    # "your-employer.com",
    # "important-client.com",
}
VIP_DOMAINS = {
    # "courts.gov",
    # "your-employer.com",
}
VIP_PATTERNS = []  # Regex patterns for VIP senders

# --- Search Terms (case-insensitive) ---
# EDIT THIS: Add keywords specific to your needs
# Examples: names, companies, locations, interests
SEARCH_TERMS = [
    # Universities/Schools
    # "university name", "college name",
    # People (family, colleagues, etc.)
    # "firstname", "lastname",
    # Companies/Orgs
    # "company-name",
    # Locations
    # "country-name", "city-name",
    # Personal interests
    # "hobby-name",
]

# --- Deadline/Urgency Keywords ---
DEADLINE_WORDS = [
    "deadline", "due date", "expires", "expiring", "urgent", "asap",
    "time-sensitive", "respond by", "reply by", "submission", "filing",
    "statute of limitations", "sol", "deposition", "hearing date",
    "court date", "trial date", "motion due", "brief due",
]

# --- Junk Indicators ---
JUNK_SENDERS = [
    "noreply@", "no-reply@", "donotreply@", "do-not-reply@",
    "mailer-daemon@",
]
JUNK_DOMAINS = [
    "mailchimp.com", "sendgrid.net", "mandrillapp.com",
    "constantcontact.com", "campaign-archive.com",
    "linkedin.com", "facebook.com", "twitter.com",
    "instagram.com", "pinterest.com",
]
JUNK_PATTERNS = [
    r"unsubscribe", r"opt.out", r"view.in.browser",
    r"weekly digest", r"monthly newsletter", r"daily deal",
]

def is_vip(meta):
    """Check if sender is a VIP."""
    from_addr = meta.get("from", "").lower()
    for pattern in VIP_PATTERNS:
        if re.search(pattern, from_addr):
            return True
    for domain in VIP_DOMAINS:
        if domain in from_addr:
            return True
    for vip in VIP_SENDERS:
        if vip.lower() in from_addr:
            return True
    return False

def contains_search_terms(meta):
    """Check if email matches any search terms."""
    searchable = " ".join([
        meta.get("subject", ""),
        meta.get("from", ""),
        meta.get("body_preview", ""),
        meta.get("to", ""),
        meta.get("cc", ""),
        " ".join(meta.get("attachments", [])),
    ]).lower()
    
    matched = []
    for term in SEARCH_TERMS:
        if term.lower() in searchable:
            matched.append(term)
    return matched

def contains_deadline_words(meta):
    """Check for deadline/urgency keywords."""
    text = (meta.get("subject", "") + " " + meta.get("body_preview", "")).lower()
    matched = []
    for word in DEADLINE_WORDS:
        if word in text:
            matched.append(word)
    return matched

def is_junk(meta):
    """Score how likely this is junk (0-100)."""
    score = 0
    from_addr = meta.get("from", "").lower()
    subject = meta.get("subject", "").lower()
    body = meta.get("body_preview", "").lower()
    
    # Junk sender patterns
    for pattern in JUNK_SENDERS:
        if pattern in from_addr:
            score += 40
            break
    
    for domain in JUNK_DOMAINS:
        if domain in from_addr:
            score += 30
            break
    
    # Junk content patterns
    junk_text = subject + " " + body
    for pattern in JUNK_PATTERNS:
        if re.search(pattern, junk_text, re.IGNORECASE):
            score += 15
    
    # Newsletter indicators
    if any(w in subject for w in ["newsletter", "digest", "weekly update", "monthly", "top 10"]):
        score += 20
    
    # Marketing language
    if any(w in body for w in ["special offer", "limited time", "act now", "click here", "shop now"]):
        score += 15
    
    # No-reply sender + short body = likely automated
    if ("noreply" in from_addr or "no-reply" in from_addr) and len(body) < 500:
        score += 20
    
    return min(score, 100)

def classify_email(meta):
    """Classify an email into keep/drop/review with reasons."""
    reasons = []
    score = 0
    
    # --- Check keep conditions ---
    
    # VIP sender
    if is_vip(meta):
        score += 50
        reasons.append("vip_sender")
    
    # Search term matches
    search_matches = contains_search_terms(meta)
    if search_matches:
        score += 40
        reasons.append(f"search_match:{','.join(search_matches[:3])}")
    
    # Deadline keywords
    deadline_matches = contains_deadline_words(meta)
    if deadline_matches:
        score += 30
        reasons.append(f"deadline:{','.join(deadline_matches[:3])}")
    
    # Has attachments
    if meta.get("has_attachments"):
        score += 15
        reasons.append("has_attachments")
    
    # Unread/starred (check folder/labels)
    labels = [l.lower() for l in meta.get("labels", [])]
    if any(l in labels for l in ["unread", "starred", "flagged", "important"]):
        score += 25
        reasons.append("unread_or_starred")
    
    # --- Check drop conditions ---
    
    junk_score = is_junk(meta)
    if junk_score >= 40:
        score -= 30
        reasons.append(f"junk_score:{junk_score}")
    
    # Very old + no search match + no VIP = lower priority
    try:
        date = datetime.fromisoformat(meta.get("date", ""))
        age_days = (datetime.now() - date.replace(tzinfo=None)).days
        if age_days > 3650 and not search_matches and not is_vip(meta):  # 10+ years
            score -= 10
            reasons.append("very_old")
    except Exception:
        pass
    
    # --- Final classification ---
    if score >= 30:
        classification = "keep"
    elif score <= -10:
        classification = "drop"
    elif junk_score >= 60:
        classification = "drop"
    else:
        classification = "review"
    
    return {
        "classification": classification,
        "score": score,
        "junk_score": junk_score,
        "reasons": reasons,
    }

def main():
    if not META_FILE.exists():
        print(f"No metadata file found at {META_FILE}")
        print("Run download_emails.py first.")
        sys.exit(1)
    
    print("=== Pre-Filter ===")
    
    keep_count = 0
    drop_count = 0
    review_count = 0
    total = 0
    
    with open(META_FILE) as inf, \
         open(KEEP_FILE, "w") as keep_f, \
         open(DROP_FILE, "w") as drop_f, \
         open(REVIEW_FILE, "w") as review_f, \
         open(FILTERED_FILE, "w") as all_f:
        
        for line in inf:
            line = line.strip()
            if not line:
                continue
            
            meta = json.loads(line)
            result = classify_email(meta)
            
            entry = {**meta, **result}
            all_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
            if result["classification"] == "keep":
                keep_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                keep_count += 1
            elif result["classification"] == "drop":
                drop_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                drop_count += 1
            else:
                review_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                review_count += 1
            
            total += 1
            if total % 10000 == 0:
                print(f"  Processed {total}...")
    
    stats = {
        "total": total,
        "keep": keep_count,
        "drop": drop_count,
        "review": review_count,
        "keep_pct": round(keep_count / total * 100, 1) if total else 0,
        "drop_pct": round(drop_count / total * 100, 1) if total else 0,
        "review_pct": round(review_count / total * 100, 1) if total else 0,
    }
    
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n=== Results ===")
    print(f"Total:    {total}")
    print(f"Keep:     {keep_count} ({stats['keep_pct']}%)")
    print(f"Drop:     {drop_count} ({stats['drop_pct']}%)")
    print(f"Review:   {review_count} ({stats['review_pct']}%)")
    print(f"\nStats: {STATS_FILE}")
    print(f"Keep:  {KEEP_FILE}")
    print(f"Drop:  {DROP_FILE}")
    print(f"Review:{REVIEW_FILE}")

if __name__ == "__main__":
    main()
