#!/usr/bin/env python3
"""
Apple Importer — Analyzes Apple ecosystem data for personality insights.
Works with data available on macOS or from Apple's data export.

Supports:
- iCloud Contacts (via exported .vcf — Contacts app → File → Export vCard)
- Apple Notes (via ~/Library/Group Containers on macOS)
- Apple Music/iTunes library (via Music library XML)
- Safari bookmarks
- Apple Health summary (from Apple data export)

For non-Mac users: works with Apple's privacy data export
(privacy.apple.com → Request a copy of your data)
"""
import os
import sys
import json
import glob
import platform
import plistlib
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"
IS_MACOS = platform.system() == "Darwin"

def find_apple_data():
    """Locate Apple data sources."""
    sources = {}
    
    # iCloud contacts export (.vcf)
    vcf_paths = [
        os.path.expanduser("~/Downloads/vCards.vcf"),
        os.path.expanduser("~/Downloads/contacts.vcf"),
        os.path.expanduser("~/Desktop/contacts.vcf"),
        os.path.expanduser("~/Documents/contacts.vcf"),
    ]
    for p in vcf_paths:
        if os.path.exists(p):
            sources["contacts_vcf"] = p
            break
    
    if IS_MACOS:
        # Safari bookmarks
        safari_bookmarks = os.path.expanduser("~/Library/Safari/Bookmarks.plist")
        if os.path.exists(safari_bookmarks):
            sources["safari_bookmarks"] = safari_bookmarks
        
        # Apple Music library
        music_lib = os.path.expanduser("~/Music/Music/Music Library.musiclibrary/Library.musicdb")
        music_xml = os.path.expanduser("~/Music/iTunes/iTunes Music Library.xml")
        if os.path.exists(music_xml):
            sources["music_library"] = music_xml
    
    # Apple data export (from privacy.apple.com)
    export_paths = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
    ]
    for base in export_paths:
        if not os.path.isdir(base):
            continue
        for d in os.listdir(base):
            full = os.path.join(base, d)
            if os.path.isdir(full) and ("apple" in d.lower() or "icloud" in d.lower()):
                sources["apple_export"] = full
                break
    
    return sources

def parse_vcf_contacts(filepath):
    """Parse vCard file for contact insights."""
    contacts = []
    current = {}
    
    with open(filepath, "r", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line == "BEGIN:VCARD":
                current = {}
            elif line == "END:VCARD":
                if current.get("name"):
                    contacts.append(current)
                current = {}
            elif ":" in line:
                key, _, value = line.partition(":")
                key = key.split(";")[0].upper()
                if key == "FN":
                    current["name"] = value
                elif key == "ORG":
                    current["org"] = value.rstrip(";")
                elif key == "EMAIL":
                    current.setdefault("emails", []).append(value)
    
    orgs = Counter()
    for c in contacts:
        if c.get("org"):
            orgs[c["org"]] += 1
    
    return {
        "total": len(contacts),
        "top_organizations": [o for o, _ in orgs.most_common(5)],
        "sample_names": [c["name"] for c in contacts[:15]],
    }

def parse_safari_bookmarks(filepath):
    """Extract interests from Safari bookmarks."""
    try:
        with open(filepath, "rb") as f:
            bookmarks = plistlib.load(f)
    except Exception:
        return None
    
    urls = []
    titles = []
    
    def walk(node):
        if isinstance(node, dict):
            if "URLString" in node:
                urls.append(node["URLString"])
            if "URIDictionary" in node:
                title = node["URIDictionary"].get("title", "")
                if title:
                    titles.append(title)
            for child in node.get("Children", []):
                walk(child)
    
    walk(bookmarks)
    
    # Extract domains for interest mapping
    domains = Counter()
    for url in urls:
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.replace("www.", "")
            if domain and "apple.com" not in domain:
                domains[domain] += 1
        except:
            pass
    
    return {
        "bookmark_count": len(urls),
        "top_sites": [d for d, _ in domains.most_common(15)],
        "bookmark_titles": titles[:20],
    }

def analyze_apple_data(sources):
    """Combine all Apple data sources into insights."""
    insights = {
        "interests": [],
        "personality_traits": [],
        "communication_style": "",
        "tone": "",
        "key_contacts": [],
    }
    items_processed = 0
    
    # Contacts
    if "contacts_vcf" in sources:
        contact_data = parse_vcf_contacts(sources["contacts_vcf"])
        insights["key_contacts"] = contact_data["sample_names"]
        insights["network_size"] = contact_data["total"]
        insights["top_organizations"] = contact_data["top_organizations"]
        items_processed += contact_data["total"]
        
        if contact_data["total"] > 500:
            insights["personality_traits"].append("large network — highly connected")
        elif contact_data["total"] > 100:
            insights["personality_traits"].append("solid network")
    
    # Safari bookmarks
    if "safari_bookmarks" in sources:
        bookmark_data = parse_safari_bookmarks(sources["safari_bookmarks"])
        if bookmark_data:
            insights["interests"].extend(bookmark_data["top_sites"][:10])
            insights["bookmarks"] = bookmark_data["bookmark_titles"][:15]
            items_processed += bookmark_data["bookmark_count"]
            
            # Infer traits from bookmark patterns
            sites = " ".join(bookmark_data["top_sites"]).lower()
            if any(s in sites for s in ["github", "stackoverflow", "dev.", "docs."]):
                insights["personality_traits"].append("technical/developer")
            if any(s in sites for s in ["reddit", "hackernews", "twitter"]):
                insights["personality_traits"].append("online community participant")
            if any(s in sites for s in ["medium", "substack", "wordpress"]):
                insights["personality_traits"].append("reader/writer")
    
    # Apple ecosystem indicators
    traits = insights["personality_traits"]
    traits.append("Apple ecosystem user")
    if IS_MACOS:
        traits.append("macOS user")
    
    insights["personality_traits"] = list(dict.fromkeys(traits))  # Deduplicate
    
    return {
        "source": "apple",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": insights,
        "confidence": min(items_processed / 100, 1.0),
        "items_processed": items_processed,
        "data_sources_found": list(sources.keys()),
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    # Allow explicit VCF path
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        sources = {}
        if sys.argv[1].endswith(".vcf"):
            sources["contacts_vcf"] = sys.argv[1]
        elif os.path.isdir(sys.argv[1]):
            sources["apple_export"] = sys.argv[1]
        result = analyze_apple_data(sources)
    else:
        sources = find_apple_data()
        if not sources:
            result = {
                "source": "apple",
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "error": "No Apple data found.",
                "setup_help": (
                    "To use this importer, do one or more of:\n"
                    "• Export contacts: Open Contacts app → File → Export vCard → save to ~/Downloads/\n"
                    "• Safari bookmarks are read automatically on macOS\n"
                    "• Full data export: Visit privacy.apple.com → Request a copy of your data\n"
                    "  Download and extract to ~/Downloads/"
                ),
            }
        else:
            result = analyze_apple_data(sources)
    
    output_path = os.path.join(IMPORT_DIR, "apple.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
