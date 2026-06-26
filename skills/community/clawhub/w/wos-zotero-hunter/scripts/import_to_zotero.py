#!/usr/bin/env python3
"""
WoS Literature Hunter - Zotero Import Script

Imports academic papers into Zotero with full metadata.
Handles collection creation, DOI-based metadata resolution via Crossref API,
and structured paper import.

Usage:
    echo '[{"title": "...", "doi": "10.xxx", ...}]' | python3 import_to_zotero.py \\
        --zotero-key YOUR_KEY --zotero-id YOUR_ID --collection "my-collection"

    # Or with papers from stdin (JSON list)
    python3 import_to_zotero.py \\
        --zotero-key YOUR_KEY --zotero-id YOUR_ID \\
        --collection "perovskite-stability" \\
        --papers papers.json

The script can also resolve DOIs from titles via Crossref when DOIs are missing.
"""

import json
import sys
import subprocess
import argparse
import time
import urllib.parse
from typing import Optional


def lookup_doi_via_crossref(title: str) -> Optional[str]:
    """Look up a paper's DOI via Crossref API by title."""
    query = urllib.parse.quote(title[:200])
    url = f"https://api.crossref.org/works?query.title={query}&rows=1"
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "10", url],
            capture_output=True, text=True, timeout=12,
        )
        data = json.loads(result.stdout)
        items = data.get("message", {}).get("items", [])
        if items:
            return items[0].get("DOI")
    except Exception:
        pass
    return None


def enrich_metadata_via_crossref(paper: dict) -> dict:
    """Enrich paper metadata using Crossref API by DOI or title."""
    doi = paper.get("doi", "")

    # If no DOI, try title lookup
    if not doi and paper.get("title"):
        doi = lookup_doi_via_crossref(paper["title"])
        if doi:
            paper["doi"] = doi

    if not doi:
        return paper  # Can't enrich without DOI

    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "10", url],
            capture_output=True, text=True, timeout=12,
        )
        data = json.loads(result.stdout)
        msg = data.get("message", {})
        if not msg:
            return paper

        # Title
        if msg.get("title"):
            paper["title"] = msg["title"][0]

        # Journal
        if msg.get("container-title"):
            paper["journal"] = msg["container-title"][0]

        # Authors
        authors = msg.get("author", [])
        if authors:
            paper["creators"] = [
                {
                    "creatorType": "author",
                    "firstName": a.get("given", ""),
                    "lastName": a.get("family", ""),
                }
                for a in authors
            ]

        # Date
        pub = (
            msg.get("published-print")
            or msg.get("issued")
            or msg.get("created")
            or {}
        )
        dp = pub.get("date-parts", [[None]])[0]
        if dp and dp[0]:
            paper["year"] = str(dp[0])

        # Other fields
        for src_key, dst_key in [
            ("volume", "volume"),
            ("issue", "issue"),
            ("page", "pages"),
        ]:
            if msg.get(src_key):
                paper[dst_key] = msg[src_key]

        # Abstract
        if msg.get("abstract"):
            paper["abstract"] = msg["abstract"][:1000]

        # ISSN
        issn_list = msg.get("ISSN", [])
        if issn_list:
            paper["issn"] = issn_list[0]

        # URL
        paper["url"] = f"https://doi.org/{doi}"

    except Exception:
        pass

    return paper


def import_papers(
    zotero_key: str,
    zotero_user_id: str,
    collection_name: str,
    papers: list[dict],
    dry_run: bool = False,
) -> dict:
    """Import papers into Zotero collection. Returns summary dict."""
    try:
        from pyzotero import zotero as pz
    except ImportError:
        print("ERROR: pyzotero not installed. Run: pip install pyzotero")
        sys.exit(1)

    if dry_run:
        print(f"[DRY RUN] Would import {len(papers)} papers to '{collection_name}'")
        for i, p in enumerate(papers):
            print(f"  {i+1}. [{p.get('year','?')}] {p.get('title','N/A')[:80]}")
        return {"status": "dry_run", "collection": collection_name, "succeeded": 0, "failed": 0, "total": len(papers)}

    zot = pz.Zotero(int(zotero_user_id), "user", zotero_key)

    # Create or find collection
    coll_key = None
    existing = zot.collections()
    for c in existing:
        if c["data"]["name"] == collection_name:
            coll_key = c["data"]["key"]
            print(f"Using existing collection: {collection_name} ({coll_key})")
            break

    if not coll_key:
        resp = zot.create_collections([{"name": collection_name}])
        if resp.get("successful"):
            coll_key = list(resp["successful"].values())[0]["key"]
            print(f"Created collection: {collection_name} ({coll_key})")
        else:
            print(f"ERROR: Failed to create collection: {resp}")
            return {"status": "error", "message": "Collection creation failed"}

    # Import papers
    succeeded = 0
    failed = 0
    imported_keys = []

    for paper in papers:
        title = paper.get("title", "Untitled")
        doi = paper.get("doi", "")
        print(f"Importing: {title[:70]}...")

        # Enrich metadata via Crossref if DOI available
        if doi and not paper.get("journal"):
            paper = enrich_metadata_via_crossref(paper)

        # Build item template
        t = zot.item_template("journalArticle")
        t["title"] = paper.get("title", title)
        t["DOI"] = doi
        t["url"] = paper.get("url", f"https://doi.org/{doi}" if doi else "")
        t["date"] = str(paper.get("year", ""))
        t["publicationTitle"] = paper.get("journal", "")
        t["volume"] = str(paper.get("volume", ""))
        t["issue"] = str(paper.get("issue", ""))
        t["pages"] = str(paper.get("pages", ""))
        t["abstractNote"] = paper.get("abstract", "")
        t["ISSN"] = paper.get("issn", "")
        t["libraryCatalog"] = paper.get("source", "Web of Science")
        t["extra"] = paper.get("extra", "")
        t["collections"] = [coll_key]

        # Authors
        creators = paper.get("creators", [])
        if not creators and paper.get("authors"):
            # Parse plain-text authors "LastName, FirstName; ..."
            auth_str = paper["authors"]
            for name in auth_str.split(";"):
                name = name.strip()
                if "," in name:
                    last, first = name.split(",", 1)
                    creators.append(
                        {
                            "creatorType": "author",
                            "firstName": first.strip(),
                            "lastName": last.strip(),
                        }
                    )
                elif name:
                    creators.append(
                        {"creatorType": "author", "firstName": "", "lastName": name}
                    )
        t["creators"] = creators

        try:
            resp = zot.create_items([t])
            if resp.get("successful"):
                key = list(resp["successful"].values())[0]["key"]
                imported_keys.append(key)
                succeeded += 1
                print(f"  ✓ {key}")
            else:
                failed += 1
                print(f"  ✗ Failed: {resp.get('failed', resp)}")
        except Exception as e:
            failed += 1
            print(f"  ✗ Error: {e}")

        time.sleep(0.15)  # Rate limit

    return {
        "status": "ok",
        "collection": collection_name,
        "collection_key": coll_key,
        "succeeded": succeeded,
        "failed": failed,
        "total": len(papers),
        "keys": imported_keys,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Import academic papers into Zotero collection"
    )
    parser.add_argument(
        "--zotero-key",
        required=True,
        help="Zotero API key (from https://www.zotero.org/settings/keys)",
    )
    parser.add_argument(
        "--zotero-id",
        required=True,
        help="Zotero user/library ID (numeric)",
    )
    parser.add_argument(
        "--collection",
        required=True,
        help="Zotero collection name (created if it doesn't exist)",
    )
    parser.add_argument(
        "--papers",
        help="Path to JSON file containing papers list",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate papers without importing",
    )
    args = parser.parse_args()

    # Read papers
    if args.papers:
        with open(args.papers) as f:
            papers = json.load(f)
    else:
        papers = json.load(sys.stdin)

    if not isinstance(papers, list):
        print("ERROR: Input must be a JSON list of paper objects")
        sys.exit(1)

    # Enrich missing metadata
    print(f"Processing {len(papers)} papers...")
    for i, paper in enumerate(papers):
        if not paper.get("journal") and paper.get("doi"):
            print(f"  Enriching: {paper.get('title', 'N/A')[:60]}...")
            papers[i] = enrich_metadata_via_crossref(paper)
            time.sleep(0.2)

    # Import
    result = import_papers(
        args.zotero_key,
        args.zotero_id,
        args.collection,
        papers,
        args.dry_run,
    )

    # Summary
    print()
    print("=" * 50)
    print(f"Collection: {result.get('collection')}")
    print(f"Imported: {result.get('succeeded', 0)}/{result.get('total', 0)}")
    if result.get("failed"):
        print(f"Failed: {result['failed']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
