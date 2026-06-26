#!/usr/bin/env python3
"""
Generate an opinionated Website Manager blueprint.

Example:
  python3 scripts/generate_blueprint.py \
    --site-name "Acme Advisory" \
    --site-type generic \
    --domain acmeadvisory.com \
    --city Toronto \
    --collection-name services
"""

from __future__ import annotations

import argparse
import json


SITE_TYPE_DEFAULTS = {
    "generic": {
        "collections_label": "Content",
        "homepage_sections": [
            "Hero",
            "Intro or positioning",
            "Primary offerings or content grid",
            "Proof or trust section",
            "Featured content or updates",
            "Primary CTA",
        ],
    },
    "professional-services": {
        "collections_label": "Services",
        "homepage_sections": [
            "Hero",
            "Credibility strip",
            "Services overview",
            "Case studies or proof",
            "Team preview",
            "Insights preview",
            "Contact CTA",
        ],
    },
    "saas": {
        "collections_label": "Features",
        "homepage_sections": [
            "Hero",
            "Social proof",
            "Feature grid",
            "Pricing teaser",
            "Integrations",
            "Testimonials",
            "Final CTA",
        ],
    },
    "pharmacy": {
        "collections_label": "Services",
        "homepage_sections": [
            "Announcement bar",
            "Hero",
            "Trust strip",
            "Services grid",
            "Why choose us",
            "Team preview",
            "Blog preview",
            "Contact and hours",
        ],
    },
}


def build_blueprint(args: argparse.Namespace) -> dict:
    defaults = SITE_TYPE_DEFAULTS[args.site_type]
    collection_slug = args.collection_slug or args.collection_name.lower().replace(" ", "-")
    return {
        "site_name": args.site_name,
        "site_type": args.site_type,
        "domain": args.domain,
        "city": args.city,
        "default_stack": {
            "implementation": "plain-html-css-js",
            "cms": "notion",
            "hosting": "netlify",
            "git": "optional",
            "automation": "openclaw-cron-when-available",
        },
        "notion_databases": ["Pages", "Collections", "Blog Posts", "Site Settings"],
        "routes": [
            "/",
            "/about",
            "/contact",
            "/blog",
            "/blog/{slug}",
            f"/{collection_slug}",
            f"/{collection_slug}/{{slug}}",
        ],
        "homepage_sections": defaults["homepage_sections"],
        "default_listing": {
            "collection_name": args.collection_name,
            "collection_slug": collection_slug,
            "items_per_page": 9,
            "filters": ["category"],
            "search_fields": ["title", "summary", "category", "tags"],
            "url_params": ["category", "q", "page"],
            "states": ["loading", "empty", "no-results", "invalid-page"],
        },
        "publish_workflow": [
            "Update content in Notion",
            "Rebuild static surfaces that changed",
            "Run validate_links.py",
            "Zip deploy to Netlify",
            "Add GitHub later only if collaboration requires it",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a default Website Manager blueprint.")
    parser.add_argument("--site-name", required=True)
    parser.add_argument(
        "--site-type",
        required=True,
        choices=sorted(SITE_TYPE_DEFAULTS.keys()),
    )
    parser.add_argument("--domain", required=True)
    parser.add_argument("--city", required=True)
    parser.add_argument("--collection-name", default="Services")
    parser.add_argument("--collection-slug")
    args = parser.parse_args()

    print(json.dumps(build_blueprint(args), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
