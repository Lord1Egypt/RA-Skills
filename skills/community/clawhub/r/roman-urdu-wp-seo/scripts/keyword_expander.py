#!/usr/bin/env python3
"""Generate deterministic Roman Urdu/Hinglish keyword suggestions.

This is an offline editorial helper. It does not estimate search volume, scrape
search engines, call APIs, or publish anything to WordPress.
"""

from __future__ import annotations

import argparse
import json
import re
from typing import Iterable


KNOWN_VARIANTS = {
    "best mobile under 30000": [
        "30 hazar ke andar best mobile",
        "best phone under 30000 Pakistan",
        "30k mein konsa mobile best hai",
    ],
    "online earning ideas": [
        "online earning ke ideas",
        "ghar baithe online paisa kamane ke tareeqe",
        "Pakistan mein online earning",
    ],
    "how to make money online": [
        "online paisa kaise kamayein",
        "internet se paisa kamane ka tareeqa",
        "ghar baithe earning kaise karein",
    ],
    "best laptops for students": [
        "students ke liye best laptop",
        "parhai ke liye acha laptop",
        "student budget mein laptop",
    ],
    "wordpress seo guide": [
        "WordPress SEO kaise karein",
        "WordPress website ko Google par rank kaise karayein",
        "WordPress SEO guide Urdu",
    ],
    "how to start a blog": [
        "blog kaise shuru karein",
        "apna blog banane ka tareeqa",
        "blogging start karne ka method",
    ],
    "best hosting in pakistan": [
        "Pakistan mein best hosting",
        "website ke liye fast hosting",
        "Pakistan hosting kaun si achi hai",
    ],
    "mobile price in pakistan": [
        "Pakistan mein mobile ki price",
        "latest mobile price Pakistan",
        "phone kitne ka hai",
    ],
    "home remedies for cough": [
        "khansi ka gharelu ilaj",
        "khansi ke liye home remedy",
        "khansi ka desi totka",
    ],
    "chicken biryani recipe": [
        "chicken biryani banane ka tareeqa",
        "ghar wali chicken biryani recipe",
        "biryani kaise pakayein",
    ],
    "digital marketing course": [
        "digital marketing ka course",
        "online digital marketing seekhein",
        "Pakistan mein marketing course",
    ],
    "freelancing websites": [
        "freelancing ke liye websites",
        "online freelance kaam kahan milega",
        "Pakistan freelancers ke platforms",
    ],
    "solar panel price": [
        "solar panel ki price Pakistan",
        "ghar ke liye solar system kitne ka hai",
        "solar lagwane ka kharcha",
    ],
    "car maintenance tips": [
        "gari ki maintenance tips",
        "car service kab karwani chahiye",
        "gari ko theek kaise rakhein",
    ],
    "learn python for beginners": [
        "beginners ke liye Python",
        "Python programming kaise seekhein",
        "Python seekhne ka easy tareeqa",
    ],
}

WORD_TRANSLATIONS = {
    "best": "best",
    "how": "kaise",
    "to": "",
    "make": "banayein",
    "money": "paisa",
    "online": "online",
    "ideas": "ideas",
    "guide": "guide",
    "price": "price",
    "prices": "prices",
    "course": "course",
    "recipe": "recipe",
    "tips": "tips",
    "for": "ke liye",
    "students": "students",
    "beginners": "beginners",
    "in": "mein",
    "pakistan": "Pakistan",
}


def clean_phrase(value: str) -> str:
    """Collapse whitespace while preserving the user's keyword casing."""
    if not value:
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def add_location(variant: str, location: str | None) -> str:
    if not location or not location.strip():
        return variant
    if location.casefold() in variant.casefold():
        return variant
    return f"{variant} {location.strip()}".strip()


def generic_variants(keyword: str) -> list[str]:
    """Create fallbacks when the exact phrase is not in the map."""
    words = keyword.split()
    translated = [WORD_TRANSLATIONS.get(w.casefold(), w) for w in words]
    translated = [word for word in translated if word]
    roman_phrase = " ".join(translated)
    variants = [
        f"{roman_phrase or keyword} kaise karein",
        f"{keyword} ke liye asan tareeqa",
        f"{keyword} ka guide Urdu mein",
    ]
    return variants


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = re.sub(r"\s+", " ", item.strip()).casefold()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(item.strip())
    return result


def expand(keyword: str, location: str | None = None, count: int = 3) -> list:
    primary = clean_phrase(keyword)
    known = primary.casefold() in KNOWN_VARIANTS
    candidates = KNOWN_VARIANTS.get(
        primary.casefold(), generic_variants(primary)
    )
    if not known and location:
        candidates = [
            add_location(clean_phrase(c), location) for c in candidates
        ]
    return dedupe(candidates)[: max(1, min(count, 3))]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate offline Roman Urdu/Hinglish keyword variants."
    )
    parser.add_argument("keyword", help="English primary keyword")
    parser.add_argument(
        "--location",
        help="Optional location modifier, such as 'Pakistan' or 'Lahore'",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        choices=(1, 2, 3),
        help="Number of variants to return (default: 3)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of a text report",
    )
    args = parser.parse_args()

    keyword = clean_phrase(args.keyword)
    variants = expand(keyword, args.location, args.count)
    payload = {
        "primary_keyword": keyword,
        "location": args.location,
        "variants": variants,
        "note": "Editorial suggestions only; no volume data fetched.",
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"Primary keyword: {keyword}")
    if args.location:
        print(f"Location: {args.location}")
    print("Suggested Roman Urdu/Hinglish variants:")
    for index, variant in enumerate(variants, start=1):
        print(f"{index}. {variant}")
    print("Note: These are offline editorial suggestions, not volume data.")


if __name__ == "__main__":
    main()
