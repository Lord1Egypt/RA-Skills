#!/usr/bin/env python3
"""
Contacts Importer — Analyzes contact data to build a relationship map.
Supports Google Contacts (People API) and vCard (.vcf) files.

Extracts: key people, relationship categories, communication frequency.
"""
import os
import sys
import json
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))

def get_google_contacts():
    """Fetch contacts via Google People API."""
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        return None, "Google API dependencies not installed."
    
    SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]
    
    token_paths = [
        os.path.join(WORKSPACE, "mission-control", "data", "gmail_token.json"),
        os.path.join(WORKSPACE, "email-agent", "token.json"),
    ]
    
    token_path = next((p for p in token_paths if os.path.exists(p)), None)
    if not token_path:
        return None, "No Google OAuth token found."
    
    try:
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        service = build("people", "v1", credentials=creds)
        results = service.people().connections().list(
            resourceName="people/me",
            pageSize=500,
            personFields="names,emailAddresses,phoneNumbers,organizations,relations,birthdays,memberships"
        ).execute()
        
        return results.get("connections", []), None
    except Exception as e:
        return None, str(e)

def parse_vcf_file(filepath):
    """Parse a vCard (.vcf) file into contact entries."""
    contacts = []
    current = {}
    
    try:
        with open(filepath, "r", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line == "BEGIN:VCARD":
                    current = {}
                elif line == "END:VCARD":
                    if current:
                        contacts.append(current)
                    current = {}
                elif ":" in line:
                    key, _, value = line.partition(":")
                    key = key.split(";")[0].upper()
                    if key == "FN":
                        current["name"] = value
                    elif key == "EMAIL":
                        current.setdefault("emails", []).append(value)
                    elif key == "TEL":
                        current.setdefault("phones", []).append(value)
                    elif key == "ORG":
                        current["organization"] = value
                    elif key == "TITLE":
                        current["title"] = value
    except FileNotFoundError:
        pass
    
    return contacts

def analyze_contacts(contacts, source="google"):
    """Extract relationship insights from contacts."""
    total = len(contacts)
    
    organizations = Counter()
    has_email = 0
    has_phone = 0
    has_org = 0
    categories = {"work": 0, "personal": 0, "unknown": 0}
    names = []
    
    for contact in contacts:
        if source == "google":
            name_data = contact.get("names", [{}])[0]
            name = name_data.get("displayName", "")
            emails = [e.get("value", "") for e in contact.get("emailAddresses", [])]
            phones = [p.get("value", "") for p in contact.get("phoneNumbers", [])]
            orgs = contact.get("organizations", [])
        else:  # vcf
            name = contact.get("name", "")
            emails = contact.get("emails", [])
            phones = contact.get("phones", [])
            orgs = [{"name": contact.get("organization", "")}] if contact.get("organization") else []
        
        if name:
            names.append(name)
        if emails:
            has_email += 1
        if phones:
            has_phone += 1
        if orgs:
            has_org += 1
            for org in orgs:
                org_name = org.get("name", "") if isinstance(org, dict) else str(org)
                if org_name:
                    organizations[org_name] += 1
        
        # Categorize (heuristic)
        email_str = " ".join(emails).lower()
        if any(domain in email_str for domain in [".edu", ".gov", ".org"]) or orgs:
            categories["work"] += 1
        elif phones and not emails:
            categories["personal"] += 1
        else:
            categories["unknown"] += 1
    
    # Determine social style
    if total > 500:
        social_style = "Large network — highly connected"
    elif total > 200:
        social_style = "Solid network — well-connected"
    elif total > 50:
        social_style = "Moderate network — selective connections"
    else:
        social_style = "Small, tight network — values close relationships"
    
    top_orgs = [org for org, _ in organizations.most_common(5)]
    
    return {
        "source": "contacts",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "key_contacts": names[:20],
            "network_size": total,
            "social_style": social_style,
            "top_organizations": top_orgs,
            "contact_breakdown": {
                "with_email": has_email,
                "with_phone": has_phone,
                "with_organization": has_org,
            },
            "categories": categories,
            "interests": [],
            "communication_style": f"{'Email-centric' if has_email > has_phone else 'Phone-centric'} communicator based on contact data",
        },
        "confidence": min(total / 100, 1.0),
        "items_processed": total,
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    source = "google"
    contacts = None
    error = None
    
    # Check for VCF file argument
    if len(sys.argv) > 1 and sys.argv[1].endswith(".vcf"):
        contacts = parse_vcf_file(sys.argv[1])
        source = "vcf"
        if not contacts:
            error = f"No contacts found in {sys.argv[1]}"
    else:
        # Try Google Contacts
        contacts, error = get_google_contacts()
    
    if error or contacts is None:
        # Fallback: check for exported VCF in common locations
        vcf_paths = [
            os.path.expanduser("~/Downloads/contacts.vcf"),
            os.path.expanduser("~/contacts.vcf"),
            os.path.join(WORKSPACE, "contacts.vcf"),
        ]
        for path in vcf_paths:
            if os.path.exists(path):
                contacts = parse_vcf_file(path)
                source = "vcf"
                error = None
                break
    
    if error or not contacts:
        result = {
            "source": "contacts",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "error": error or "No contacts found. Export a .vcf file or set up Google Contacts OAuth.",
        }
    else:
        result = analyze_contacts(contacts, source)
    
    output_path = os.path.join(IMPORT_DIR, "contacts.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
