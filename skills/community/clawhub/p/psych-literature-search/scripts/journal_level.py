#!/usr/bin/env python3
"""
Journal Impact Factor & Classification Reference Tool
Provides JIF quartile / level lookup from a curated reference list.
Usage:
  python journal_level.py --journal "Journal of Abnormal Psychology"
  python journal_level.py --list        (print all known journals)
"""

import argparse
import json
import difflib

# Curated journal reference for major psychology journals.
# Format: name -> {if_approx, quartile, category, ssci}
# Data based on 2022-2023 JCR / AJG / ABS reference values.
JOURNAL_DB = {
    # Q1 Top-tier Journals
    "psychological bulletin": {
        "if": 23.0, "quartile": "Q1", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Top (AJG 4* equivalent)", "ssci": True
    },
    "annual review of psychology": {
        "if": 23.6, "quartile": "Q1", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Top (AJG 4* equivalent)", "ssci": True
    },
    "psychological review": {
        "if": 9.8, "quartile": "Q1", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Top (AJG 4 equivalent)", "ssci": True
    },
    "journal of personality and social psychology": {
        "if": 8.5, "quartile": "Q1", "jcr_category": "Psychology, Social",
        "level": "Top (AJG 4 equivalent)", "ssci": True
    },
    "clinical psychology review": {
        "if": 12.8, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "Top (AJG 4 equivalent)", "ssci": True
    },
    "behaviour research and therapy": {
        "if": 5.4, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of abnormal psychology": {
        "if": 5.4, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of consulting and clinical psychology": {
        "if": 5.9, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "developmental psychology": {
        "if": 4.5, "quartile": "Q1", "jcr_category": "Psychology, Developmental",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "child development": {
        "if": 4.3, "quartile": "Q1", "jcr_category": "Psychology, Developmental",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of experimental psychology: general": {
        "if": 6.0, "quartile": "Q1", "jcr_category": "Psychology, Experimental",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "psychological science": {
        "if": 6.4, "quartile": "Q1", "jcr_category": "Psychology, Multidisciplinary",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "personality and individual differences": {
        "if": 3.9, "quartile": "Q2", "jcr_category": "Psychology, Social",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "journal of anxiety disorders": {
        "if": 5.9, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "depression and anxiety": {
        "if": 7.1, "quartile": "Q1", "jcr_category": "Psychiatry",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "cognition": {
        "if": 3.9, "quartile": "Q1", "jcr_category": "Psychology, Experimental",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "memory": {
        "if": 2.8, "quartile": "Q2", "jcr_category": "Psychology, Experimental",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "emotion": {
        "if": 3.5, "quartile": "Q1", "jcr_category": "Psychology, Multidisciplinary",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "social cognitive and affective neuroscience": {
        "if": 4.0, "quartile": "Q1", "jcr_category": "Neurosciences",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of health psychology": {
        "if": 3.5, "quartile": "Q2", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "health psychology": {
        "if": 4.4, "quartile": "Q1", "jcr_category": "Psychology, Multidisciplinary",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "nature human behaviour": {
        "if": 29.9, "quartile": "Q1", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Top (Nature family)", "ssci": True
    },
    "psychological medicine": {
        "if": 7.4, "quartile": "Q1", "jcr_category": "Psychiatry",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of clinical psychology": {
        "if": 3.1, "quartile": "Q2", "jcr_category": "Psychology, Clinical",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "acta psychologica": {
        "if": 2.9, "quartile": "Q2", "jcr_category": "Psychology, Experimental",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "frontiers in psychology": {
        "if": 2.6, "quartile": "Q2", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Medium (Open Access)", "ssci": True
    },
    "plos one": {
        "if": 3.7, "quartile": "Q2", "jcr_category": "Multidisciplinary Sciences",
        "level": "Medium (Open Access, interdisciplinary)", "ssci": False
    },
    "behavior therapy": {
        "if": 4.5, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "cognitive therapy and research": {
        "if": 3.3, "quartile": "Q2", "jcr_category": "Psychology, Clinical",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "journal of applied psychology": {
        "if": 9.4, "quartile": "Q1", "jcr_category": "Psychology, Applied",
        "level": "Top (AJG 4 equivalent)", "ssci": True
    },
    "organizational behavior and human decision processes": {
        "if": 4.6, "quartile": "Q1", "jcr_category": "Psychology, Applied",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of occupational health psychology": {
        "if": 5.4, "quartile": "Q1", "jcr_category": "Psychology, Applied",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "european journal of personality": {
        "if": 4.8, "quartile": "Q1", "jcr_category": "Psychology, Social",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "british journal of psychology": {
        "if": 3.6, "quartile": "Q2", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "european journal of psychology": {
        "if": 2.1, "quartile": "Q3", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Low (AJG 1 equivalent)", "ssci": True
    },
    "international journal of psychology": {
        "if": 3.0, "quartile": "Q2", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "mindfulness": {
        "if": 4.1, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of positive psychology": {
        "if": 4.0, "quartile": "Q2", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "current psychology": {
        "if": 2.7, "quartile": "Q3", "jcr_category": "Psychology, Multidisciplinary",
        "level": "Low-Medium", "ssci": True
    },
    "journal of research in personality": {
        "if": 3.5, "quartile": "Q2", "jcr_category": "Psychology, Social",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "social psychology": {
        "if": 2.3, "quartile": "Q3", "jcr_category": "Psychology, Social",
        "level": "Low-Medium", "ssci": True
    },
    "clinical psychological science": {
        "if": 6.2, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of affective disorders": {
        "if": 6.5, "quartile": "Q1", "jcr_category": "Psychiatry",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "psychotherapy": {
        "if": 4.0, "quartile": "Q1", "jcr_category": "Psychology, Clinical",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of traumatic stress": {
        "if": 3.8, "quartile": "Q2", "jcr_category": "Psychology, Clinical",
        "level": "Medium (AJG 2 equivalent)", "ssci": True
    },
    "psychosomatic medicine": {
        "if": 4.3, "quartile": "Q1", "jcr_category": "Psychiatry",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
    "journal of neuroscience": {
        "if": 5.3, "quartile": "Q1", "jcr_category": "Neurosciences",
        "level": "Top Neuroscience", "ssci": True
    },
    "neuroimage": {
        "if": 5.7, "quartile": "Q1", "jcr_category": "Neuroimaging",
        "level": "Top Neuroimaging", "ssci": True
    },
    "neuroscience and biobehavioral reviews": {
        "if": 9.0, "quartile": "Q1", "jcr_category": "Behavioral Sciences",
        "level": "Top (AJG 4 equivalent)", "ssci": True
    },
    "applied psychology": {
        "if": 5.3, "quartile": "Q1", "jcr_category": "Psychology, Applied",
        "level": "High (AJG 3 equivalent)", "ssci": True
    },
}


def lookup_journal(name: str) -> dict:
    """Fuzzy-match a journal name against the database and return level info."""
    key = name.lower().strip()
    # Exact match
    if key in JOURNAL_DB:
        result = dict(JOURNAL_DB[key])
        result["name"] = name
        result["match_type"] = "exact"
        return result
    # Fuzzy match
    matches = difflib.get_close_matches(key, JOURNAL_DB.keys(), n=3, cutoff=0.55)
    if matches:
        best = matches[0]
        result = dict(JOURNAL_DB[best])
        result["name"] = name
        result["matched_to"] = best
        result["match_type"] = "fuzzy"
        return result
    # Not found
    return {
        "name": name,
        "match_type": "not_found",
        "if": "Unknown",
        "quartile": "Unknown",
        "level": "Unknown (not in reference database)",
        "note": "Check JCR/SJR manually at https://jcr.clarivate.com or https://www.scimagojr.com/"
    }


def main():
    parser = argparse.ArgumentParser(description="Look up psychology journal level/impact factor")
    parser.add_argument("--journal", help="Journal name to look up")
    parser.add_argument("--list", action="store_true", help="Print all known journals")
    args = parser.parse_args()

    if args.list:
        for name, info in sorted(JOURNAL_DB.items()):
            print(f"{name:60s} | Q{info.get('quartile','?')} | IF~{info.get('if','?'):5} | {info.get('level','?')}")
        return

    if args.journal:
        result = lookup_journal(args.journal)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
