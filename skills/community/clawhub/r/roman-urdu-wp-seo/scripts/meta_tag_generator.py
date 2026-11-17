#!/usr/bin/env python3
"""Draft blended English + Roman Urdu metadata for WordPress content.

The output is a draft for editorial review. It does not call an API, inspect a
website, or publish metadata to WordPress.
"""

from __future__ import annotations

import argparse
import json
import re


def clean(value: str) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def title_case_keyword(keyword: str) -> str:
    """Use readable title casing while preserving common product names."""
    protected = {
        "wordpress": "WordPress",
        "python": "Python",
        "seo": "SEO",
        "google": "Google",
    }
    words = []
    for word in clean(keyword).split():
        cased = word if word.isupper() else word.capitalize()
        words.append(protected.get(word.casefold(), cased))
    return " ".join(words)


def length_status(value: str, minimum: int, maximum: int) -> str:
    size = len(value)
    if size < minimum:
        return f"short ({size}; target {minimum}-{maximum})"
    if size > maximum:
        return f"long ({size}; target {minimum}-{maximum})"
    return f"within target ({size}; target {minimum}-{maximum})"


def generate(
    keyword: str,
    topic: str,
    audience: str | None = None,
    benefit: str | None = None,
    brand: str | None = None,
) -> dict[str, object]:
    keyword = clean(keyword)
    topic = clean(topic)
    audience = clean(audience) if audience else "Pakistan ke readers"
    benefit = clean(benefit) if benefit else "ka practical guide"
    brand_suffix = f" | {clean(brand)}" if brand else ""

    title = f"{title_case_keyword(keyword)}: {benefit}{brand_suffix}"
    description = (
        f"{topic} ke liye {audience} ka practical guide. "
        f"Features aur {benefit.lower()} ko asan andaaz mein samjhein."
    )
    slug = re.sub(r"[^a-z0-9]+", "-", keyword.casefold()).strip("-")

    return {
        "seo_title": title,
        "meta_description": description,
        "slug": slug,
        "character_counts": {
            "seo_title": len(title),
            "meta_description": len(description),
        },
        "length_status": {
            "seo_title": length_status(title, 50, 60),
            "meta_description": length_status(description, 140, 160),
        },
        "review_notes": [
            "Confirm the Roman Urdu phrase sounds natural.",
            "Verify every claim against the article before publishing.",
            "Character targets are heuristics, not display guarantees.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Draft English + Roman Urdu/Hinglish WordPress metadata."
    )
    parser.add_argument("--keyword", required=True, help="Primary keyword")
    parser.add_argument("--topic", required=True, help="Article topic")
    parser.add_argument(
        "--audience",
        help="Optional audience phrase, such as 'Pakistan ke buyers'",
    )
    parser.add_argument(
        "--benefit",
        help="Optional Roman Urdu/Hinglish benefit phrase",
    )
    parser.add_argument("--brand", help="Optional brand suffix")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of a text report",
    )
    args = parser.parse_args()

    result = generate(
        args.keyword, args.topic, args.audience, args.benefit, args.brand
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"SEO title: {result['seo_title']}")
    print(f"Title status: {result['length_status']['seo_title']}")
    print(f"Meta description: {result['meta_description']}")
    print(f"Description status: {result['length_status']['meta_description']}")
    print(f"Suggested slug: {result['slug']}")
    print("Review before publishing: confirm phrasing and accuracy.")


if __name__ == "__main__":
    main()
