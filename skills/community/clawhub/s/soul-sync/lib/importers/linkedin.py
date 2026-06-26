#!/usr/bin/env python3
"""
LinkedIn Importer — Analyzes LinkedIn data export for professional identity.
LinkedIn requires a data export (Settings → Data Privacy → Get a copy of your data).

Extracts: career trajectory, skills, education, professional network, endorsements.
"""
import os
import sys
import json
import csv
import glob
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"

def find_linkedin_export():
    """Find LinkedIn data export directory."""
    search_paths = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
    ]
    
    for base in search_paths:
        if not os.path.isdir(base):
            continue
        for d in os.listdir(base):
            full = os.path.join(base, d)
            if os.path.isdir(full) and "linkedin" in d.lower():
                return full
            # LinkedIn exports have a specific CSV structure
            if os.path.isdir(full) and os.path.exists(os.path.join(full, "Profile.csv")):
                return full
            if os.path.isdir(full) and os.path.exists(os.path.join(full, "Positions.csv")):
                return full
    
    return None

def read_csv(filepath):
    """Read a LinkedIn export CSV file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception:
        return []

def analyze_export(export_dir):
    """Analyze LinkedIn data export."""
    insights = {
        "interests": [],
        "personality_traits": [],
        "communication_style": "",
        "tone": "",
        "key_contacts": [],
    }
    items_processed = 0
    
    # Profile
    profile_rows = read_csv(os.path.join(export_dir, "Profile.csv"))
    profile = {}
    if profile_rows:
        p = profile_rows[0]
        profile = {
            "name": f"{p.get('First Name', '')} {p.get('Last Name', '')}".strip(),
            "headline": p.get("Headline", ""),
            "summary": p.get("Summary", ""),
            "location": p.get("Geo Location", "") or p.get("Location", ""),
            "industry": p.get("Industry", ""),
        }
        insights["profile"] = profile
        if profile["industry"]:
            insights["interests"].append(profile["industry"])
    
    # Positions (career trajectory)
    positions = read_csv(os.path.join(export_dir, "Positions.csv"))
    career = []
    companies = []
    for pos in positions:
        title = pos.get("Title", "")
        company = pos.get("Company Name", "")
        if title or company:
            career.append(f"{title} at {company}".strip(" at"))
            if company:
                companies.append(company)
            items_processed += 1
    
    insights["career"] = career[:10]
    insights["companies"] = companies[:10]
    
    # Determine career level
    titles_lower = " ".join(t.lower() for t in career)
    if any(t in titles_lower for t in ["ceo", "founder", "president", "owner", "partner"]):
        insights["personality_traits"].append("founder/executive — entrepreneurial")
    elif any(t in titles_lower for t in ["director", "vp", "head of", "chief"]):
        insights["personality_traits"].append("senior leadership")
    elif any(t in titles_lower for t in ["senior", "lead", "principal", "staff"]):
        insights["personality_traits"].append("senior individual contributor")
    elif any(t in titles_lower for t in ["manager"]):
        insights["personality_traits"].append("people manager")
    
    if len(positions) > 5:
        insights["personality_traits"].append("experienced professional — multiple roles")
    if len(set(companies)) > 3:
        insights["personality_traits"].append("diverse experience across companies")
    
    # Skills
    skills = read_csv(os.path.join(export_dir, "Skills.csv"))
    skill_names = [s.get("Name", "") for s in skills if s.get("Name")]
    insights["skills"] = skill_names[:20]
    insights["interests"].extend(skill_names[:10])
    items_processed += len(skills)
    
    # Education
    education = read_csv(os.path.join(export_dir, "Education.csv"))
    edu_list = []
    for edu in education:
        school = edu.get("School Name", "")
        degree = edu.get("Degree Name", "")
        field = edu.get("Notes", "") or edu.get("Field of Study", "")
        if school:
            edu_list.append(f"{degree} from {school}".strip(" from") + (f" ({field})" if field else ""))
            if field:
                insights["interests"].append(field)
        items_processed += 1
    insights["education"] = edu_list
    
    # Connections count
    connections = read_csv(os.path.join(export_dir, "Connections.csv"))
    if connections:
        insights["network_size"] = len(connections)
        # Top connection companies
        conn_companies = Counter()
        for conn in connections:
            company = conn.get("Company", "")
            if company:
                conn_companies[company] += 1
        insights["network_companies"] = [c for c, _ in conn_companies.most_common(10)]
        
        # Key contacts (recent connections)
        insights["key_contacts"] = [
            f"{c.get('First Name', '')} {c.get('Last Name', '')}".strip()
            for c in connections[:10]
            if c.get("First Name")
        ]
        items_processed += len(connections)
    
    # Endorsements
    endorsements = read_csv(os.path.join(export_dir, "Endorsement_Received_Info.csv"))
    if not endorsements:
        endorsements = read_csv(os.path.join(export_dir, "Endorsements_Received.csv"))
    if endorsements:
        endorsed_skills = Counter()
        for e in endorsements:
            skill = e.get("Skill Name", "") or e.get("Skill", "")
            if skill:
                endorsed_skills[skill] += 1
        insights["top_endorsed_skills"] = [s for s, _ in endorsed_skills.most_common(10)]
    
    # Communication style from summary/headline
    if profile.get("summary"):
        summary = profile["summary"]
        if len(summary) > 500:
            insights["communication_style"] = "detailed professional communicator — writes thorough summaries"
        elif len(summary) > 100:
            insights["communication_style"] = "balanced professional voice"
        else:
            insights["communication_style"] = "concise — lets credentials speak"
    
    return {
        "source": "linkedin",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": insights,
        "confidence": min(items_processed / 50, 1.0),
        "items_processed": items_processed,
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    export_dir = None
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        export_dir = sys.argv[1]
    else:
        export_dir = find_linkedin_export()
    
    if not export_dir:
        result = {
            "source": "linkedin",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "error": "No LinkedIn data export found.",
            "setup_help": (
                "To use this importer:\n"
                "1. Go to LinkedIn → Settings → Data Privacy → Get a copy of your data\n"
                "2. Select all data categories\n"
                "3. Request archive, wait for email (can take 24h)\n"
                "4. Download and extract to ~/Downloads/\n"
                "5. Run this importer again"
            ),
        }
    else:
        result = analyze_export(export_dir)
    
    output_path = os.path.join(IMPORT_DIR, "linkedin.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
