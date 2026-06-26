#!/usr/bin/env python3
"""
Create the opinionated Website Manager CMS in Notion.

Requires:
- NOTION_ACCESS_TOKEN or NOTION_TOKEN
- NOTION_PARENT_PAGE_ID

Example:
  NOTION_ACCESS_TOKEN=... NOTION_PARENT_PAGE_ID=... \
  python3 scripts/create_notion_cms.py \
    --site-name "Acme Advisory" \
    --site-type generic \
    --domain acmeadvisory.com \
    --city Toronto

By default the script also writes the resulting non-secret Notion IDs to
`.website-manager/notion.json`.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
import urllib.error
import urllib.request


NOTION_VERSION = "2026-03-11"
API_ROOT = "https://api.notion.com/v1"
DEFAULT_SAVE_JSON = ".website-manager/notion.json"


SITE_TYPE_DEFAULTS = {
    "generic": {
        "collection_label": "Content",
        "primary_color": "#1f4b99",
        "accent_color": "#e0892b",
    },
    "professional-services": {
        "collection_label": "Services",
        "primary_color": "#1b3a5c",
        "accent_color": "#d4a853",
    },
    "saas": {
        "collection_label": "Features",
        "primary_color": "#2251ff",
        "accent_color": "#16c47f",
    },
    "pharmacy": {
        "collection_label": "Services",
        "primary_color": "#4a7a5a",
        "accent_color": "#c4603a",
    },
}


def rich_text(content: str) -> dict:
    return {
        "type": "text",
        "text": {"content": content},
    }


def title_prop(content: str) -> dict:
    return {"title": [rich_text(content)]}


def rt_prop(content: str) -> dict:
    return {"rich_text": [rich_text(content)]} if content else {"rich_text": []}


def select_prop(name: str | None) -> dict:
    return {"select": {"name": name}} if name else {"select": None}


def url_prop(value: str | None) -> dict:
    return {"url": value}


def date_prop(value: str | None) -> dict:
    return {"date": {"start": value} if value else None}


def notion_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API_ROOT}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def create_page_parent(page_id: str) -> dict:
    return {"type": "page_id", "page_id": page_id}


def create_data_source_parent(data_source_id: str) -> dict:
    return {"type": "data_source_id", "data_source_id": data_source_id}


def create_child_page(token: str, parent_page_id: str, title: str) -> dict:
    return notion_request(
        "POST",
        "/pages",
        token,
        {
            "parent": create_page_parent(parent_page_id),
            "properties": {"title": title_prop(title)},
        },
    )


def create_database(
    token: str,
    parent_page_id: str,
    title: str,
    description: str,
    properties: dict,
) -> dict:
    return notion_request(
        "POST",
        "/databases",
        token,
        {
            "parent": create_page_parent(parent_page_id),
            "title": [rich_text(title)],
            "description": [rich_text(description)],
            "is_inline": False,
            "initial_data_source": {
                "title": [rich_text(title)],
                "properties": properties,
            },
        },
    )


def get_first_data_source_id(token: str, database_id: str) -> str:
    payload = notion_request("GET", f"/databases/{database_id}", token)
    data_sources = payload.get("data_sources") or []
    if not data_sources:
        raise RuntimeError(f"No data source returned for database {database_id}")
    return data_sources[0]["id"]


def create_row(token: str, data_source_id: str, properties: dict) -> dict:
    return notion_request(
        "POST",
        "/pages",
        token,
        {
            "parent": create_data_source_parent(data_source_id),
            "properties": properties,
        },
    )


def pages_schema() -> dict:
    return {
        "Page Name": {"title": {}},
        "Slug": {"rich_text": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Draft", "color": "gray"},
                    {"name": "Ready", "color": "blue"},
                    {"name": "Published", "color": "green"},
                    {"name": "Needs Update", "color": "orange"},
                ]
            }
        },
        "SEO Title": {"rich_text": {}},
        "SEO Description": {"rich_text": {}},
        "Hero Headline": {"rich_text": {}},
        "Hero Subtext": {"rich_text": {}},
        "Primary CTA Label": {"rich_text": {}},
        "Primary CTA URL": {"url": {}},
        "Secondary CTA Label": {"rich_text": {}},
        "Secondary CTA URL": {"url": {}},
        "Last Published": {"date": {}},
    }


def collections_schema() -> dict:
    return {
        "Name": {"title": {}},
        "Slug": {"rich_text": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Draft", "color": "gray"},
                    {"name": "Ready", "color": "blue"},
                    {"name": "Published", "color": "green"},
                    {"name": "Needs Update", "color": "orange"},
                ]
            }
        },
        "Category": {
            "select": {
                "options": [
                    {"name": "Primary", "color": "blue"},
                    {"name": "Secondary", "color": "purple"},
                    {"name": "Campaign", "color": "orange"},
                ]
            }
        },
        "Summary": {"rich_text": {}},
        "Headline": {"rich_text": {}},
        "SEO Title": {"rich_text": {}},
        "SEO Description": {"rich_text": {}},
        "Featured": {"checkbox": {}},
        "Sort Order": {"number": {"format": "number"}},
        "Primary CTA URL": {"url": {}},
        "Tags": {
            "multi_select": {
                "options": [
                    {"name": "Featured", "color": "yellow"},
                    {"name": "Popular", "color": "green"},
                    {"name": "Evergreen", "color": "blue"},
                ]
            }
        },
    }


def blog_schema() -> dict:
    return {
        "Post Title": {"title": {}},
        "Slug": {"rich_text": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Draft", "color": "gray"},
                    {"name": "Ready", "color": "blue"},
                    {"name": "Published", "color": "green"},
                    {"name": "Needs Update", "color": "orange"},
                ]
            }
        },
        "Category": {
            "select": {
                "options": [
                    {"name": "News", "color": "blue"},
                    {"name": "Guides", "color": "green"},
                    {"name": "Insights", "color": "purple"},
                ]
            }
        },
        "Tags": {
            "multi_select": {
                "options": [
                    {"name": "Featured", "color": "yellow"},
                    {"name": "SEO", "color": "orange"},
                    {"name": "Evergreen", "color": "green"},
                ]
            }
        },
        "SEO Title": {"rich_text": {}},
        "SEO Description": {"rich_text": {}},
        "Hero Image URL": {"url": {}},
        "Author": {"rich_text": {}},
        "Published Date": {"date": {}},
        "Featured": {"checkbox": {}},
    }


def settings_schema() -> dict:
    return {
        "Setting": {"title": {}},
        "Value": {"rich_text": {}},
        "Group": {
            "select": {
                "options": [
                    {"name": "Brand", "color": "blue"},
                    {"name": "Contact", "color": "green"},
                    {"name": "Deployment", "color": "orange"},
                    {"name": "Content", "color": "purple"},
                ]
            }
        },
        "Notes": {"rich_text": {}},
    }


def seed_pages(token: str, data_source_id: str, site_name: str, city: str) -> list[dict]:
    seeds = [
        {
            "Page Name": title_prop("Home"),
            "Slug": rt_prop("home"),
            "Status": select_prop("Draft"),
            "SEO Title": rt_prop(f"{site_name} | {city}"),
            "SEO Description": rt_prop(f"Homepage for {site_name}."),
            "Hero Headline": rt_prop(site_name),
            "Hero Subtext": rt_prop("Replace with your primary offer and proof."),
            "Primary CTA Label": rt_prop("Get Started"),
            "Primary CTA URL": url_prop(None),
            "Secondary CTA Label": rt_prop("Learn More"),
            "Secondary CTA URL": url_prop(None),
            "Last Published": date_prop(None),
        },
        {
            "Page Name": title_prop("About"),
            "Slug": rt_prop("about"),
            "Status": select_prop("Draft"),
            "SEO Title": rt_prop(f"About {site_name}"),
            "SEO Description": rt_prop(f"About {site_name} in {city}."),
            "Hero Headline": rt_prop(f"About {site_name}"),
            "Hero Subtext": rt_prop("Replace with your story, positioning, and trust signals."),
            "Primary CTA Label": rt_prop("Contact Us"),
            "Primary CTA URL": url_prop(None),
            "Secondary CTA Label": rt_prop(""),
            "Secondary CTA URL": url_prop(None),
            "Last Published": date_prop(None),
        },
        {
            "Page Name": title_prop("Contact"),
            "Slug": rt_prop("contact"),
            "Status": select_prop("Draft"),
            "SEO Title": rt_prop(f"Contact {site_name}"),
            "SEO Description": rt_prop(f"Contact {site_name} in {city}."),
            "Hero Headline": rt_prop("Get in Touch"),
            "Hero Subtext": rt_prop("Replace with contact instructions and response expectations."),
            "Primary CTA Label": rt_prop("Call Now"),
            "Primary CTA URL": url_prop(None),
            "Secondary CTA Label": rt_prop(""),
            "Secondary CTA URL": url_prop(None),
            "Last Published": date_prop(None),
        },
        {
            "Page Name": title_prop("Blog"),
            "Slug": rt_prop("blog"),
            "Status": select_prop("Draft"),
            "SEO Title": rt_prop(f"{site_name} Blog"),
            "SEO Description": rt_prop(f"Articles and updates from {site_name}."),
            "Hero Headline": rt_prop("Insights and Updates"),
            "Hero Subtext": rt_prop("Replace with your blog intro and editorial promise."),
            "Primary CTA Label": rt_prop("Subscribe"),
            "Primary CTA URL": url_prop(None),
            "Secondary CTA Label": rt_prop(""),
            "Secondary CTA URL": url_prop(None),
            "Last Published": date_prop(None),
        },
    ]
    return [create_row(token, data_source_id, props) for props in seeds]


def seed_settings(
    token: str,
    data_source_id: str,
    site_name: str,
    domain: str,
    city: str,
    site_type: str,
) -> list[dict]:
    defaults = SITE_TYPE_DEFAULTS[site_type]
    seeds = [
        ("Business Name", site_name, "Brand", "Primary business or brand name."),
        ("Primary Domain", domain, "Brand", "Canonical website domain."),
        ("Primary City", city, "Brand", "Main city used for SEO and contact data."),
        ("Site Type", site_type, "Brand", "Template family used by the website-manager skill."),
        ("Collection Label", defaults["collection_label"], "Content", "Default label for the main structured collection."),
        ("Primary Color", defaults["primary_color"], "Brand", "Primary design token."),
        ("Accent Color", defaults["accent_color"], "Brand", "Accent design token."),
        ("Contact Email", "", "Contact", "Primary public contact email."),
        ("Phone", "", "Contact", "Primary public phone number."),
        ("Street Address", "", "Contact", "Primary mailing or storefront address."),
        ("Hours", "", "Contact", "Canonical opening hours summary."),
        ("Announce Bar Text", "", "Content", "Optional announcement bar copy."),
        ("Netlify Site ID", "", "Deployment", "Required only for automated Netlify deploys."),
        ("Netlify Site URL", "", "Deployment", "Primary deployed Netlify URL."),
    ]
    payloads = []
    for setting, value, group, notes in seeds:
        payloads.append(
            {
                "Setting": title_prop(setting),
                "Value": rt_prop(value),
                "Group": select_prop(group),
                "Notes": rt_prop(notes),
            }
        )
    return [create_row(token, data_source_id, props) for props in payloads]


def build_cms(args: argparse.Namespace, token: str) -> dict:
    hub_title = f"{args.site_name} Website CMS"
    hub_page = create_child_page(token, args.parent_page_id, hub_title)
    hub_page_id = hub_page["id"]

    databases = {}

    page_db = create_database(
        token,
        hub_page_id,
        "Pages",
        "Core static pages and page-level SEO/content fields.",
        pages_schema(),
    )
    page_ds = get_first_data_source_id(token, page_db["id"])
    seed_pages(token, page_ds, args.site_name, args.city)
    databases["pages"] = {"database_id": page_db["id"], "data_source_id": page_ds}

    collections_db = create_database(
        token,
        hub_page_id,
        "Collections",
        "Services, resources, directories, or other structured website sections.",
        collections_schema(),
    )
    collections_ds = get_first_data_source_id(token, collections_db["id"])
    databases["collections"] = {
        "database_id": collections_db["id"],
        "data_source_id": collections_ds,
    }

    blog_db = create_database(
        token,
        hub_page_id,
        "Blog Posts",
        "Editorial posts and article metadata.",
        blog_schema(),
    )
    blog_ds = get_first_data_source_id(token, blog_db["id"])
    databases["blog_posts"] = {"database_id": blog_db["id"], "data_source_id": blog_ds}

    settings_db = create_database(
        token,
        hub_page_id,
        "Site Settings",
        "Global settings and deployment metadata for the site.",
        settings_schema(),
    )
    settings_ds = get_first_data_source_id(token, settings_db["id"])
    seed_settings(token, settings_ds, args.site_name, args.domain, args.city, args.site_type)
    databases["site_settings"] = {
        "database_id": settings_db["id"],
        "data_source_id": settings_ds,
    }

    return {
        "hub_page_id": hub_page_id,
        "hub_page_url": hub_page.get("url"),
        "site_name": args.site_name,
        "site_type": args.site_type,
        "domain": args.domain,
        "city": args.city,
        "databases": databases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the default Website Manager CMS in Notion.")
    parser.add_argument("--site-name", required=True)
    parser.add_argument(
        "--site-type",
        required=True,
        choices=sorted(SITE_TYPE_DEFAULTS.keys()),
    )
    parser.add_argument("--domain", required=True)
    parser.add_argument("--city", required=True)
    parser.add_argument(
        "--parent-page-id",
        default=os.environ.get("NOTION_PARENT_PAGE_ID"),
        help="Shared Notion parent page ID. Defaults to NOTION_PARENT_PAGE_ID.",
    )
    parser.add_argument(
        "--save-json",
        default=DEFAULT_SAVE_JSON,
        help="Where to save the resulting non-secret Notion IDs. Use '-' to disable.",
    )
    args = parser.parse_args()

    token = os.environ.get("NOTION_ACCESS_TOKEN") or os.environ.get("NOTION_TOKEN")
    if not token:
        print("ERROR: NOTION_ACCESS_TOKEN or NOTION_TOKEN must be set.", file=sys.stderr)
        return 2
    if not args.parent_page_id:
        print("ERROR: --parent-page-id or NOTION_PARENT_PAGE_ID is required.", file=sys.stderr)
        return 2

    try:
        result = build_cms(args, token)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP ERROR {exc.code}: {detail}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.save_json != "-":
        save_path = Path(args.save_json)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
