# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///
"""
Meta Ads Campaign Publisher (Marketing API)

Publishes ad campaigns to Meta Ads Manager. Creates campaigns, ad sets,
creatives, and ads — all in PAUSED state for manual review before activation.

Usage:
    uv run scripts/meta-ads-publish.py --setup                  # Credential setup guide
    uv run scripts/meta-ads-publish.py --check                  # Verify API access
    uv run scripts/meta-ads-publish.py --upload-images DIR      # Upload images, get hashes
    uv run scripts/meta-ads-publish.py --publish CONFIG.json    # Publish full campaign (PAUSED)
    uv run scripts/meta-ads-publish.py --list                   # List campaigns
    uv run scripts/meta-ads-publish.py --status CAMPAIGN_ID     # Campaign hierarchy status
    uv run scripts/meta-ads-publish.py --pause CAMPAIGN_ID      # Pause campaign
    uv run scripts/meta-ads-publish.py --resume CAMPAIGN_ID     # Resume (activate) campaign

Environment variables (or .env file):
    META_ADS_ACCESS_TOKEN - System User token with ads_management permission
    META_ADS_ACCOUNT_ID   - Ad account ID (format: act_XXXXXXXXX)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables from current working directory
PROJECT_ROOT = Path.cwd()
load_dotenv(PROJECT_ROOT / ".env")

ACCESS_TOKEN = os.getenv("META_ADS_ACCESS_TOKEN", "")
ACCOUNT_ID = os.getenv("META_ADS_ACCOUNT_ID", "")

API_BASE = "https://graph.facebook.com/v21.0"


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def api_request(
    method: str,
    endpoint: str,
    params: dict | None = None,
    data: dict | None = None,
    files: dict | None = None,
    max_retries: int = 5,
) -> dict | None:
    """Unified API handler with rate limiting, Meta error parsing, exponential backoff."""
    params = params or {}
    params["access_token"] = ACCESS_TOKEN

    url = f"{API_BASE}/{endpoint}"

    for attempt in range(max_retries):
        try:
            response = requests.request(
                method, url, params=params, data=data, files=files, timeout=60
            )

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 2 ** attempt))
                print(f"  Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue

            if response.status_code not in (200, 201):
                error = response.json().get("error", {})
                error_msg = error.get("message", response.text[:300])
                error_code = error.get("code", "")
                error_subcode = error.get("error_subcode", "")

                # Transient errors — retry
                if error_code in (1, 2, 4, 17):
                    wait = 2 ** attempt
                    print(f"  Transient API error (code {error_code}). Retrying in {wait}s...")
                    time.sleep(wait)
                    continue

                print(f"  API Error [{error_code}]: {error_msg}")
                if error_subcode:
                    print(f"  Subcode: {error_subcode}")
                return None

            return response.json()

        except requests.RequestException as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  Request error: {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  Request failed after {max_retries} attempts: {e}")
                return None

    return None


# ---------------------------------------------------------------------------
# Image upload
# ---------------------------------------------------------------------------

def upload_image(image_path: Path) -> str | None:
    """Upload a single image and return its hash."""
    print(f"  Uploading {image_path.name}...")

    with open(image_path, "rb") as f:
        result = api_request(
            "POST",
            f"{ACCOUNT_ID}/adimages",
            files={"filename": (image_path.name, f)},
        )

    if result and "images" in result:
        # Response: {"images": {"filename": {"hash": "...", "url": "..."}}}
        for _name, img_data in result["images"].items():
            image_hash = img_data.get("hash")
            print(f"    Hash: {image_hash}")
            return image_hash

    print(f"    Failed to upload {image_path.name}")
    return None


def upload_images_from_directory(directory: Path) -> dict:
    """Upload all images from a directory. Returns {filename: image_hash}."""
    image_extensions = {".png", ".jpg", ".jpeg", ".webp"}
    image_files = sorted(
        p for p in directory.iterdir()
        if p.suffix.lower() in image_extensions and p.is_file()
    )

    if not image_files:
        print(f"  No images found in {directory}")
        return {}

    print(f"Uploading {len(image_files)} images from {directory}...")

    hashes = {}
    for img_path in image_files:
        h = upload_image(img_path)
        if h:
            hashes[img_path.name] = h

    print(f"  Uploaded {len(hashes)}/{len(image_files)} images")
    return hashes


# ---------------------------------------------------------------------------
# Campaign creation
# ---------------------------------------------------------------------------

def create_campaign(name: str, objective: str = "OUTCOME_SALES") -> str | None:
    """Create a campaign in PAUSED state. Returns campaign ID."""
    print(f"Creating campaign: {name}")

    result = api_request(
        "POST",
        f"{ACCOUNT_ID}/campaigns",
        data={
            "name": name,
            "objective": objective,
            "status": "PAUSED",
            "special_ad_categories": "[]",
        },
    )

    if result and "id" in result:
        campaign_id = result["id"]
        print(f"  Campaign ID: {campaign_id}")
        return campaign_id

    return None


def create_adset(
    campaign_id: str,
    name: str,
    daily_budget: int,
    targeting: dict,
    optimization_goal: str = "OFFSITE_CONVERSIONS",
    billing_event: str = "IMPRESSIONS",
    bid_strategy: str = "LOWEST_COST_WITHOUT_CAP",
    pixel_id: str | None = None,
) -> str | None:
    """Create an ad set in PAUSED state. daily_budget is in cents."""
    print(f"Creating ad set: {name} (${daily_budget / 100:.2f}/day)")

    data = {
        "campaign_id": campaign_id,
        "name": name,
        "daily_budget": str(daily_budget),
        "optimization_goal": optimization_goal,
        "billing_event": billing_event,
        "bid_strategy": bid_strategy,
        "targeting": json.dumps(targeting),
        "status": "PAUSED",
    }

    if pixel_id:
        data["promoted_object"] = json.dumps({"pixel_id": pixel_id})

    result = api_request("POST", f"{ACCOUNT_ID}/adsets", data=data)

    if result and "id" in result:
        adset_id = result["id"]
        print(f"  Ad Set ID: {adset_id}")
        return adset_id

    return None


def create_creative(
    name: str,
    image_hashes: list[str],
    primary_texts: list[str],
    headlines: list[str],
    descriptions: list[str],
    link_url: str,
    call_to_action_type: str = "SHOP_NOW",
    url_parameters: str = "",
    page_id: str | None = None,
) -> str | None:
    """Create an Advantage+ creative with asset_feed_spec for flexible format."""
    print(f"Creating creative: {name}")

    # Build asset_feed_spec for Advantage+ Creative
    images = [{"hash": h} for h in image_hashes]
    bodies = [{"text": t} for t in primary_texts]
    titles = [{"text": h} for h in headlines]
    descs = [{"text": d} for d in descriptions]
    link_urls = [{"website_url": link_url}]

    cta = [{"type": call_to_action_type}]

    asset_feed_spec = {
        "images": images,
        "bodies": bodies,
        "titles": titles,
        "descriptions": descs,
        "link_urls": link_urls,
        "call_to_action_types": cta,
        "ad_formats": ["SINGLE_IMAGE"],
    }

    if url_parameters:
        asset_feed_spec["link_urls"] = [
            {"website_url": link_url, "display_url": link_url}
        ]

    data = {
        "name": name,
        "asset_feed_spec": json.dumps(asset_feed_spec),
        "degrees_of_freedom_spec": json.dumps({
            "creative_features_spec": {
                "standard_enhancements": {"enroll_status": "OPT_IN"}
            }
        }),
    }

    if url_parameters:
        data["url_tags"] = url_parameters

    if page_id:
        data["object_story_spec"] = json.dumps({
            "page_id": page_id,
        })

    result = api_request("POST", f"{ACCOUNT_ID}/adcreatives", data=data)

    if result and "id" in result:
        creative_id = result["id"]
        print(f"  Creative ID: {creative_id}")
        return creative_id

    return None


def create_ad(name: str, adset_id: str, creative_id: str) -> str | None:
    """Create an ad linking creative to ad set. PAUSED state."""
    print(f"Creating ad: {name}")

    result = api_request(
        "POST",
        f"{ACCOUNT_ID}/ads",
        data={
            "name": name,
            "adset_id": adset_id,
            "creative": json.dumps({"creative_id": creative_id}),
            "status": "PAUSED",
        },
    )

    if result and "id" in result:
        ad_id = result["id"]
        print(f"  Ad ID: {ad_id}")
        return ad_id

    return None


# ---------------------------------------------------------------------------
# Config validation & orchestration
# ---------------------------------------------------------------------------

def validate_config(config: dict) -> list[str]:
    """Pre-publish validation. Returns list of error messages (empty = valid)."""
    errors = []

    # Campaign
    campaign = config.get("campaign", {})
    if not campaign.get("name"):
        errors.append("campaign.name is required")

    # Ad sets
    adsets = config.get("adsets", [])
    if not adsets:
        errors.append("At least one ad set is required")

    for i, adset in enumerate(adsets):
        if not adset.get("name"):
            errors.append(f"adsets[{i}].name is required")
        budget = adset.get("daily_budget", 0)
        if budget < 100:
            errors.append(f"adsets[{i}].daily_budget must be >= 100 cents ($1.00)")
        if not adset.get("targeting"):
            errors.append(f"adsets[{i}].targeting is required")

    # Creative
    creative = config.get("creative", {})
    if not creative.get("primary_texts"):
        errors.append("creative.primary_texts is required (at least 1)")
    if not creative.get("headlines"):
        errors.append("creative.headlines is required (at least 1)")
    if not creative.get("link_url"):
        errors.append("creative.link_url is required")
    if not creative.get("images_directory") and not creative.get("image_hashes"):
        errors.append("creative.images_directory or creative.image_hashes is required")

    return errors


def publish_from_config(config_path: Path) -> bool:
    """Orchestrate full campaign publish from JSON config."""
    print(f"Loading config: {config_path}")

    with open(config_path) as f:
        config = json.load(f)

    # Validate
    errors = validate_config(config)
    if errors:
        print("\nConfig validation failed:")
        for err in errors:
            print(f"  - {err}")
        return False

    campaign_cfg = config["campaign"]
    adsets_cfg = config["adsets"]
    creative_cfg = config["creative"]

    print(f"\n{'='*60}")
    print("PUBLISHING CAMPAIGN")
    print(f"{'='*60}")
    print(f"  Campaign: {campaign_cfg['name']}")
    print(f"  Ad Sets:  {len(adsets_cfg)}")
    print(f"  Status:   All created PAUSED")
    print(f"{'='*60}\n")

    # Step 1: Upload images
    image_hashes = creative_cfg.get("image_hashes", [])
    if not image_hashes and creative_cfg.get("images_directory"):
        img_dir = Path(creative_cfg["images_directory"])
        if not img_dir.is_absolute():
            img_dir = config_path.parent / img_dir
        hash_map = upload_images_from_directory(img_dir)
        image_hashes = list(hash_map.values())

    if not image_hashes:
        print("Error: No images available for creative")
        return False

    # Step 2: Create campaign
    campaign_id = create_campaign(
        name=campaign_cfg["name"],
        objective=campaign_cfg.get("objective", "OUTCOME_SALES"),
    )
    if not campaign_id:
        return False

    # Step 3: Create creative
    creative_id = create_creative(
        name=f"{campaign_cfg['name']}-creative",
        image_hashes=image_hashes,
        primary_texts=creative_cfg["primary_texts"],
        headlines=creative_cfg["headlines"],
        descriptions=creative_cfg.get("descriptions", []),
        link_url=creative_cfg["link_url"],
        call_to_action_type=creative_cfg.get("call_to_action_type", "SHOP_NOW"),
        url_parameters=creative_cfg.get("url_parameters", ""),
        page_id=creative_cfg.get("page_id"),
    )
    if not creative_id:
        return False

    # Step 4: Create ad sets + ads
    for adset_cfg in adsets_cfg:
        adset_id = create_adset(
            campaign_id=campaign_id,
            name=adset_cfg["name"],
            daily_budget=adset_cfg["daily_budget"],
            targeting=adset_cfg["targeting"],
            optimization_goal=adset_cfg.get("optimization_goal", "OFFSITE_CONVERSIONS"),
            billing_event=adset_cfg.get("billing_event", "IMPRESSIONS"),
            bid_strategy=adset_cfg.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
            pixel_id=adset_cfg.get("pixel_id"),
        )
        if not adset_id:
            print(f"  Warning: Failed to create ad set '{adset_cfg['name']}'")
            continue

        ad_id = create_ad(
            name=f"{adset_cfg['name']}-ad",
            adset_id=adset_id,
            creative_id=creative_id,
        )
        if not ad_id:
            print(f"  Warning: Failed to create ad for '{adset_cfg['name']}'")

    # Summary
    print(f"\n{'='*60}")
    print("PUBLISH COMPLETE")
    print(f"{'='*60}")
    print(f"  Campaign ID: {campaign_id}")
    print(f"  Status: PAUSED (review in Ads Manager before activating)")
    print(f"\n  To activate:")
    print(f"    uv run scripts/meta-ads-publish.py --resume {campaign_id}")
    print(f"{'='*60}")

    return True


# ---------------------------------------------------------------------------
# Campaign management
# ---------------------------------------------------------------------------

def list_campaigns() -> None:
    """List all campaigns with status, spend, dates."""
    print("Fetching campaigns...")

    result = api_request(
        "GET",
        f"{ACCOUNT_ID}/campaigns",
        params={
            "fields": "id,name,status,effective_status,objective,daily_budget,lifetime_budget,start_time,created_time",
            "limit": 50,
        },
    )

    if not result or not result.get("data"):
        print("  No campaigns found")
        return

    campaigns = result["data"]

    print(f"\n{'='*90}")
    print("META ADS CAMPAIGNS")
    print(f"{'='*90}")
    print(f"\n{'Name':<35} {'Status':<12} {'Objective':<20} {'ID':<20}")
    print(f"{'-'*35} {'-'*12} {'-'*20} {'-'*20}")

    for c in campaigns:
        name = c.get("name", "")[:34]
        status = c.get("effective_status", c.get("status", ""))
        objective = c.get("objective", "")
        cid = c.get("id", "")
        print(f"{name:<35} {status:<12} {objective:<20} {cid:<20}")

    print(f"\n  Total: {len(campaigns)} campaigns")
    print(f"{'='*90}")


def campaign_status(campaign_id: str) -> None:
    """Show campaign hierarchy: campaign → ad sets → ads."""
    print(f"Fetching status for campaign {campaign_id}...")

    # Campaign
    campaign = api_request(
        "GET",
        campaign_id,
        params={"fields": "id,name,status,effective_status,objective,daily_budget,created_time"},
    )
    if not campaign:
        print("  Campaign not found")
        return

    print(f"\n{'='*70}")
    print(f"CAMPAIGN: {campaign.get('name')}")
    print(f"{'='*70}")
    print(f"  ID:        {campaign.get('id')}")
    print(f"  Status:    {campaign.get('effective_status', campaign.get('status'))}")
    print(f"  Objective: {campaign.get('objective')}")
    print(f"  Created:   {campaign.get('created_time', 'N/A')}")

    # Ad sets
    adsets = api_request(
        "GET",
        f"{campaign_id}/adsets",
        params={
            "fields": "id,name,status,effective_status,daily_budget,optimization_goal,targeting",
            "limit": 50,
        },
    )

    if adsets and adsets.get("data"):
        print(f"\n  Ad Sets ({len(adsets['data'])}):")
        for adset in adsets["data"]:
            budget = int(adset.get("daily_budget", 0)) / 100
            print(f"    - {adset['name']} [{adset.get('effective_status', adset.get('status'))}] ${budget:.2f}/day")
            print(f"      ID: {adset['id']}")

            # Ads under this ad set
            ads = api_request(
                "GET",
                f"{adset['id']}/ads",
                params={
                    "fields": "id,name,status,effective_status,creative",
                    "limit": 50,
                },
            )
            if ads and ads.get("data"):
                for ad in ads["data"]:
                    print(f"      Ad: {ad['name']} [{ad.get('effective_status', ad.get('status'))}] ID: {ad['id']}")

    print(f"\n{'='*70}")


def toggle_campaign_status(campaign_id: str, status: str) -> None:
    """Pause or resume a campaign."""
    action = "Pausing" if status == "PAUSED" else "Activating"
    print(f"{action} campaign {campaign_id}...")

    result = api_request(
        "POST",
        campaign_id,
        data={"status": status},
    )

    if result and result.get("success"):
        print(f"  Campaign {campaign_id} is now {status}")
    else:
        print(f"  Failed to update campaign status")


# ---------------------------------------------------------------------------
# Check & setup
# ---------------------------------------------------------------------------

def check_credentials() -> None:
    """Verify API access and show account info."""
    print("Checking Meta Ads API access...\n")

    result = api_request(
        "GET",
        ACCOUNT_ID,
        params={"fields": "id,name,account_status,currency,timezone_name,amount_spent,balance"},
    )

    if not result:
        print("Failed to access ad account. Check your credentials.")
        print("\nRun with --setup for configuration instructions:")
        print("  uv run scripts/meta-ads-publish.py --setup")
        sys.exit(1)

    status_map = {
        1: "ACTIVE",
        2: "DISABLED",
        3: "UNSETTLED",
        7: "PENDING_RISK_REVIEW",
        8: "PENDING_SETTLEMENT",
        9: "IN_GRACE_PERIOD",
        100: "PENDING_CLOSURE",
        101: "CLOSED",
    }

    account_status = status_map.get(result.get("account_status", 0), "UNKNOWN")
    spent = int(result.get("amount_spent", 0)) / 100

    print(f"  Account:  {result.get('name', 'N/A')}")
    print(f"  ID:       {result.get('id')}")
    print(f"  Status:   {account_status}")
    print(f"  Currency: {result.get('currency', 'N/A')}")
    print(f"  Timezone: {result.get('timezone_name', 'N/A')}")
    print(f"  Spent:    ${spent:,.2f}")
    print(f"\n  API access verified successfully.")


def print_setup_guide() -> None:
    """Print credential setup instructions."""
    print("""
META ADS PUBLISH SETUP GUIDE
=============================

To use this script, you need:
1. META_ADS_ACCESS_TOKEN - System User token with ads_management permission
2. META_ADS_ACCOUNT_ID   - Ad account ID (format: act_XXXXXXXXX)

STEP 1: Create a System User in Business Manager
-------------------------------------------------
1. Go to business.facebook.com/settings
2. Navigate to Users > System Users
3. Click "Add" to create a new System User
4. Set role to "Admin" (needed for ad management)

STEP 2: Generate an Access Token
---------------------------------
1. Click on the System User you created
2. Click "Generate New Token"
3. Select your app
4. Select these permissions:
   - ads_management (required - create/edit campaigns)
   - ads_read (required - read campaign data)
   - pages_read_engagement (for page-linked ads)
5. Click "Generate Token"
6. Copy and save the token securely

   Note: System User tokens don't expire (unlike user tokens).

STEP 3: Get Your Ad Account ID
-------------------------------
1. Go to business.facebook.com/settings
2. Navigate to Accounts > Ad Accounts
3. Your account ID is shown (format: act_XXXXXXXXX)
4. Make sure the System User is assigned to this ad account

STEP 4: Add to .env
--------------------
META_ADS_ACCESS_TOKEN=your_system_user_token
META_ADS_ACCOUNT_ID=act_XXXXXXXXX

STEP 5: Verify
--------------
uv run scripts/meta-ads-publish.py --check

CONFIG FILE FORMAT
==================
Create a JSON config to publish a full campaign:

{
  "campaign": {
    "name": "my-campaign-name",
    "objective": "OUTCOME_SALES"
  },
  "adsets": [
    {
      "name": "Broad-25-54",
      "daily_budget": 7500,
      "targeting": {
        "age_min": 25,
        "age_max": 54,
        "genders": [0],
        "geo_locations": {"countries": ["US"]},
        "publisher_platforms": ["facebook", "instagram"]
      },
      "optimization_goal": "OFFSITE_CONVERSIONS"
    }
  ],
  "creative": {
    "images_directory": "./path/to/images/",
    "primary_texts": ["Your primary text 1", "Your primary text 2"],
    "headlines": ["Headline 1", "Headline 2"],
    "descriptions": ["Description 1"],
    "link_url": "https://yoursite.com/landing-page",
    "url_parameters": "utm_source=meta&utm_medium=paid-social&utm_campaign=my-campaign",
    "call_to_action_type": "SHOP_NOW"
  }
}

Budget is in CENTS (7500 = $75.00/day).
All objects are created PAUSED. Review in Ads Manager before activating.
""")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Meta Ads Campaign Publisher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/meta-ads-publish.py --setup
  uv run scripts/meta-ads-publish.py --check
  uv run scripts/meta-ads-publish.py --upload-images ./ads/images/
  uv run scripts/meta-ads-publish.py --publish campaign-config.json
  uv run scripts/meta-ads-publish.py --list
  uv run scripts/meta-ads-publish.py --status 12345678
  uv run scripts/meta-ads-publish.py --pause 12345678
  uv run scripts/meta-ads-publish.py --resume 12345678
        """,
    )

    parser.add_argument("--setup", action="store_true", help="Show setup guide")
    parser.add_argument("--check", action="store_true", help="Verify API access")
    parser.add_argument("--upload-images", metavar="DIR", help="Upload images from directory")
    parser.add_argument("--publish", metavar="CONFIG", help="Publish campaign from JSON config")
    parser.add_argument("--list", action="store_true", help="List campaigns")
    parser.add_argument("--status", metavar="CAMPAIGN_ID", help="Show campaign hierarchy status")
    parser.add_argument("--pause", metavar="CAMPAIGN_ID", help="Pause a campaign")
    parser.add_argument("--resume", metavar="CAMPAIGN_ID", help="Resume (activate) a campaign")

    args = parser.parse_args()

    if args.setup:
        print_setup_guide()
        return

    # All other commands need credentials
    if not ACCESS_TOKEN or not ACCOUNT_ID:
        print("Error: Missing Meta Ads credentials")
        print("\nRequired environment variables:")
        print("  META_ADS_ACCESS_TOKEN - System User token")
        print("  META_ADS_ACCOUNT_ID   - Ad account ID (act_XXXXXXXXX)")
        print("\nRun with --setup for configuration instructions:")
        print("  uv run scripts/meta-ads-publish.py --setup")
        sys.exit(1)

    if args.check:
        check_credentials()
    elif args.upload_images:
        img_dir = Path(args.upload_images)
        if not img_dir.is_dir():
            print(f"Error: {img_dir} is not a directory")
            sys.exit(1)
        hashes = upload_images_from_directory(img_dir)
        if hashes:
            print(f"\nImage hashes (for use in config):")
            print(json.dumps(hashes, indent=2))
    elif args.publish:
        config_path = Path(args.publish)
        if not config_path.exists():
            print(f"Error: Config file not found: {config_path}")
            sys.exit(1)
        success = publish_from_config(config_path)
        if not success:
            sys.exit(1)
    elif args.list:
        list_campaigns()
    elif args.status:
        campaign_status(args.status)
    elif args.pause:
        toggle_campaign_status(args.pause, "PAUSED")
    elif args.resume:
        toggle_campaign_status(args.resume, "ACTIVE")
    else:
        # Default: list campaigns
        if ACCESS_TOKEN and ACCOUNT_ID:
            list_campaigns()
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
