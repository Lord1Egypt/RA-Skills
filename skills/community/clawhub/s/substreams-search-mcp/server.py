#!/usr/bin/env python3
"""MCP server that searches the substreams.dev package registry."""

import json
from typing import Optional

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("substreams-search")

REGISTRY_URL = "https://substreams.dev/packages"


PAGE_SIZE = 24
MAX_PAGES = 50


def _fetch_packages(query: str, sort: str = "most_downloaded", network: str | None = None) -> list[dict]:
    """Fetch and parse packages from substreams.dev, paginating through all results.

    The registry only supports single-word search. For multi-word queries,
    we search for the first word and filter results client-side.
    """
    words = query.strip().split()
    search_term = words[0] if words else query
    extra_words = [w.lower() for w in words[1:]]

    params: dict[str, str] = {"search": search_term, "sort": sort}
    if network:
        params["network"] = network

    all_packages: list[dict] = []
    seen_urls: set[str] = set()

    for page in range(1, MAX_PAGES + 1):
        params["page"] = str(page)
        resp = requests.get(REGISTRY_URL, params=params, timeout=15)
        resp.raise_for_status()

        page_packages = _parse_cards(resp.text)
        if not page_packages:
            break

        for pkg in page_packages:
            if pkg["url"] not in seen_urls:
                seen_urls.add(pkg["url"])
                all_packages.append(pkg)

        if len(page_packages) < PAGE_SIZE:
            break

    if extra_words:
        all_packages = [
            p for p in all_packages
            if all(w in p["name"].lower() or w in p["creator"].lower() or w in p["network"].lower() for w in extra_words)
        ]

    return all_packages


def _parse_cards(html: str) -> list[dict]:
    """Parse package cards from the substreams.dev HTML response."""
    soup = BeautifulSoup(html, "html.parser")
    grid = soup.find(id="packages-grid")
    if not grid:
        return []

    packages = []
    for link in grid.find_all("a", class_="block", href=True):
        href = link["href"]

        # Package name
        name_el = link.find("p", class_="font-semibold")
        name = name_el.get_text(strip=True) if name_el else href.split("/")[2] if len(href.split("/")) > 2 else ""

        # Creator
        creator_btn = link.find("button", class_="user-filter-link")
        creator = creator_btn.get("data-user", creator_btn.get_text(strip=True)) if creator_btn else ""

        # Network
        network_btn = link.find("button", class_="network-filter-link")
        network = network_btn.get("data-network", "") if network_btn else ""

        # Stats from the bottom section
        bottom = link.find("div", class_="absolute")
        version = ""
        published = ""
        downloads = ""
        if bottom:
            rows = bottom.find_all("div", class_="flex-row")
            for row in rows:
                label_el = row.find("p", class_="uppercase")
                value_el = row.find_all("p")
                if not label_el or len(value_el) < 2:
                    continue
                label = label_el.get_text(strip=True).lower()
                value = value_el[-1].get_text(strip=True)
                if "version" in label:
                    version = value
                elif "publish" in label:
                    published = value
                elif "download" in label:
                    downloads = value

        packages.append({
            "name": name,
            "url": f"https://substreams.dev{href}",
            "creator": creator,
            "network": network,
            "version": version,
            "published": published,
            "downloads": downloads,
        })

    return packages


@mcp.tool()
def search_substreams(
    query: str,
    sort: Optional[str] = "most_downloaded",
    network: Optional[str] = None,
) -> str:
    """Search the substreams.dev package registry for blockchain data stream packages.

    Args:
        query: Search term, e.g. 'solana dex' or 'uniswap'. Multi-word queries filter results to match all words.
        sort: Sort order - one of: most_downloaded, alphabetical, most_used, last_uploaded
        network: Filter by blockchain network, e.g. 'ethereum', 'solana', 'arbitrum-one'
    """
    packages = _fetch_packages(query, sort=sort or "most_downloaded", network=network)

    if not packages:
        return json.dumps({"results": [], "message": f"No packages found for '{query}'"})

    return json.dumps({"results": packages, "count": len(packages)}, indent=2)


if __name__ == "__main__":
    mcp.run()
