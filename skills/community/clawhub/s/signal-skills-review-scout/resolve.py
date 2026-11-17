#!/usr/bin/env python3
"""First-mile resolver for the review-scout skill: detect what kind of
product this repo is, and pull reviews from whichever surface actually has
a compliant, free (or officially-authenticated) way to read them.

Deliberately does NOT scrape review sites that disallow it in their ToS
(Google Play web pages, Chrome Web Store, G2, Capterra). Where no
compliant path exists, this prints an explicit "no fetch, here's the
manual path" message instead of silently doing nothing or quietly
scraping anyway.

Subcommands:
  detect                                  -> guess product type from cwd
  fetch-ios --app-id ID [--country us] [--pages 5] --download DIR
  fetch-android --package NAME --credentials PATH --download DIR
  guidance <chrome-extension|web-saas|desktop>
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

# ------------------------------------------------------------- detection

def detect(root: Path):
    signals = []
    is_mobile = False
    if (root / "pubspec.yaml").exists():
        signals.append("pubspec.yaml (Flutter)")
        is_mobile = True
    if (root / "android").is_dir():
        signals.append("android/ (native or Flutter Android target)")
        is_mobile = True
    if (root / "ios").is_dir() or list(root.glob("*.xcodeproj")) or list(root.glob("ios/*.xcworkspace")):
        signals.append("ios/ or .xcodeproj (native or Flutter iOS target)")
        is_mobile = True
    if (root / "package.json").exists():
        try:
            pkg = json.loads((root / "package.json").read_text())
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "react-native" in deps or "expo" in deps:
                signals.append("package.json (React Native/Expo)")
                is_mobile = True
        except (json.JSONDecodeError, OSError):
            pass
    manifest = root / "manifest.json"
    is_extension = False
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text())
            if "manifest_version" in data:
                signals.append("manifest.json (browser extension)")
                is_extension = True
        except (json.JSONDecodeError, OSError):
            pass
    is_web = (root / "package.json").exists() and not is_mobile and not is_extension

    if is_mobile:
        kind = "mobile-app"
    elif is_extension:
        kind = "browser-extension"
    elif is_web:
        kind = "web-saas"
    else:
        kind = "unknown"

    return {"kind": kind, "signals": signals}


def cmd_detect(args):
    result = detect(Path(args.path).resolve())
    print(json.dumps(result, indent=2))


# -------------------------------------------------------- iOS App Store
# Public, free, no auth: the customer-reviews RSS/JSON feed. Works for ANY
# app (yours or a competitor's) since Apple publishes it openly. Distinct
# from App Store Connect (which needs developer credentials and only
# covers your own app) — this skill only needs the read path, so the RSS
# feed is sufficient and requires nothing to set up.

def fetch_ios(app_id, country, pages, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    all_entries = []
    for page in range(1, pages + 1):
        url = (
            f"https://itunes.apple.com/{country}/rss/customerreviews/"
            f"page={page}/id={app_id}/sortby=mostrecent/json"
        )
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"page {page}: fetch failed ({e}), stopping", file=sys.stderr)
            break
        entries = data.get("feed", {}).get("entry", [])
        if not entries:
            break
        # entry[0] on page 1 is often the app metadata, not a review, when
        # there are few reviews — skip anything missing a rating.
        entries = [e for e in entries if "im:rating" in e]
        if not entries:
            break
        all_entries.extend(entries)
        print(f"page {page}: {len(entries)} reviews", file=sys.stderr)

    reviews = []
    for e in all_entries:
        reviews.append({
            "id": e.get("id", {}).get("label", ""),
            "rating": int(e.get("im:rating", {}).get("label", 0)),
            "title": e.get("title", {}).get("label", ""),
            "text": e.get("content", {}).get("label", ""),
            "author": e.get("author", {}).get("name", {}).get("label", ""),
            "updated": e.get("updated", {}).get("label", ""),
            "version": e.get("im:version", {}).get("label", ""),
        })

    txt_path = out_dir / f"ios-{app_id}.txt"
    with open(txt_path, "w") as f:
        for r in reviews:
            f.write(f"[{r['updated']}] v{r['version']} {r['rating']}/5 - {r['title']}\n")
            f.write(f"{r['text']}\n\n")

    manifest = {
        "source": "ios-app-store",
        "app_id": app_id,
        "country": country,
        "count": len(reviews),
        "path": str(txt_path),
        "date_range": [reviews[-1]["updated"], reviews[0]["updated"]] if reviews else [None, None],
    }
    manifest_path = out_dir / f"ios-{app_id}-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


def cmd_fetch_ios(args):
    fetch_ios(args.app_id, args.country, args.pages, Path(args.download))


# --------------------------------------------------- Android (Play Store)
# No public feed exists for Play reviews the way Apple's RSS works,
# and scraping the Play Store web page is against Google's ToS. The only
# compliant path is Google's official Android Publisher API
# (reviews.list), which requires: (a) you own the app / are on its Play
# Console with the right permission, (b) a service-account key with the
# Android Publisher API enabled. This is real friction relative to iOS —
# say so rather than pretending it's equally free. It also only ever
# covers YOUR OWN app, never a competitor's — there's no compliant way to
# read a competitor's Play reviews at all.

def cmd_fetch_android(args):
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print(
            "Missing dependencies. This is the one part of review-scout "
            "that needs real setup (official API, not a free public feed):\n"
            "  pip install google-api-python-client google-auth\n"
            "Then: enable the Android Publisher API in the Google Cloud "
            "project linked to your Play Console, create a service account, "
            "grant it 'View app information (read-only)' in Play Console > "
            "Users and permissions, download its JSON key, and pass that "
            "path as --credentials.\n"
            "This only ever works for an app you own — there is no "
            "compliant way to read a competitor's Play Store reviews.",
            file=sys.stderr,
        )
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_file(
        args.credentials,
        scopes=["https://www.googleapis.com/auth/androidpublisher"],
    )
    service = build("androidpublisher", "v3", credentials=creds)

    out_dir = Path(args.download)
    out_dir.mkdir(parents=True, exist_ok=True)
    reviews = []
    token = None
    while True:
        req = service.reviews().list(packageName=args.package, token=token, maxResults=100)
        resp = req.execute()
        reviews.extend(resp.get("reviews", []))
        token = resp.get("tokenPagination", {}).get("nextPageToken")
        if not token:
            break

    txt_path = out_dir / f"android-{args.package}.txt"
    with open(txt_path, "w") as f:
        for r in reviews:
            comment = r.get("comments", [{}])[0].get("userComment", {})
            f.write(
                f"[{comment.get('lastModified', {}).get('seconds', '')}] "
                f"v{comment.get('appVersionName', '')} "
                f"{comment.get('starRating', '')}/5\n"
            )
            f.write(f"{comment.get('text', '')}\n\n")

    manifest = {
        "source": "android-play-store",
        "package": args.package,
        "count": len(reviews),
        "path": str(txt_path),
    }
    (out_dir / f"android-{args.package}-manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


# ------------------------------------------------------ everything else

GUIDANCE = {
    "chrome-extension": (
        "Chrome Web Store has no public reviews API and scraping the store "
        "page violates Google's ToS. Compliant path: the Chrome Web Store "
        "Developer Dashboard lets you export your own extension's reviews "
        "manually (Dashboard > your item > Reviews). Export to CSV/JSON, "
        "drop it in a `tx/` dir, and feed it to Step 3 the same way a "
        "fetched batch would be."
    ),
    "web-saas": (
        "G2, Capterra, and TrustRadius don't offer a free compliant public "
        "reviews API; scraping their pages violates ToS. Compliant paths: "
        "G2's paid Data API (if you're a G2 customer), or a manual export "
        "of your own product's reviews from each platform's vendor "
        "dashboard. If you run in-app feedback/NPS, that's usually the "
        "richer and fully-compliant source anyway — mine that instead via "
        "whatever analytics/support platform you already have connected."
    ),
    "desktop": (
        "Mac App Store reviews are covered by the same public RSS feed as "
        "iOS (`fetch-ios`, same app-id mechanism). Microsoft Store and "
        "direct-download desktop apps have no equivalent free feed; use "
        "in-app feedback or your support inbox instead."
    ),
}


def cmd_guidance(args):
    print(GUIDANCE.get(args.kind, "No guidance for this product type."))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("detect")
    s.add_argument("--path", default=".")
    s.set_defaults(func=cmd_detect)

    s = sub.add_parser("fetch-ios")
    s.add_argument("--app-id", required=True)
    s.add_argument("--country", default="us")
    s.add_argument("--pages", type=int, default=5)
    s.add_argument("--download", required=True)
    s.set_defaults(func=cmd_fetch_ios)

    s = sub.add_parser("fetch-android")
    s.add_argument("--package", required=True)
    s.add_argument("--credentials", required=True)
    s.add_argument("--download", required=True)
    s.set_defaults(func=cmd_fetch_android)

    s = sub.add_parser("guidance")
    s.add_argument("kind", choices=list(GUIDANCE.keys()))
    s.set_defaults(func=cmd_guidance)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
