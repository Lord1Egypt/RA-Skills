#!/usr/bin/env python3
"""
Wikipedia MCP Server
Provides: search, article summary, random article, did_you_know
Uses Wikipedia REST API — free, no API key required.
"""

import sys
import json
import requests

BASE_URL = "https://en.wikipedia.org/api/rest_v1"
HEADERS = {"User-Agent": "wikipedia-mcp/1.0 (https://github.com/openclaw/skills; contact@openclaw.ai)"}


def _get(url: str, params=None) -> requests.Response:
    return requests.get(url, params=params, headers=HEADERS, timeout=10)


def search_wikipedia(query: str, limit: int = 5) -> str:
    """Search Wikipedia for articles matching a query."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": min(limit, 20),
        "format": "json",
        "origin": "*"
    }
    resp = _get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("query", {}).get("search", [])
    if not results:
        return f"No results found for '{query}'."

    output = f"**Search results for '{query}':**\n\n"
    for i, page in enumerate(results, 1):
        title = page.get("title", "Unknown")
        snippet = page.get("snippet", "")
        # Strip HTML tags from snippet
        import re
        snippet = re.sub(r'<[^>]+>', '', snippet)
        output += f"{i}. **{title}**\n"
        if snippet:
            output += f"   {snippet[:200]}...\n"
        output += f"   https://en.wikipedia.org/wiki/{title.replace(' ', '_')}\n\n"
    return output


def get_summary(title: str) -> str:
    """Get a Wikipedia article summary by title."""
    title_slug = title.replace(" ", "_")
    url = f"{BASE_URL}/page/summary/{title_slug}"
    resp = _get(url)
    if resp.status_code == 404:
        return f"Article '{title}' not found on Wikipedia."
    resp.raise_for_status()
    data = resp.json()

    output = f"## {data.get('title', title)}\n\n"
    output += f"{data.get('extract', 'No summary available.')}\n\n"
    if data.get('description'):
        output += f"*({data.get('description')})*\n\n"
    desktop_url = data.get('content_urls', {}).get('desktop', {}).get('page', '#')
    output += f"[Read more →]({desktop_url})"
    if data.get('thumbnail'):
        output += f"\n\n![{data.get('title')}]({data.get('thumbnail', {}).get('source', '')})"
    return output


def get_random() -> str:
    """Get a random Wikipedia article summary."""
    url = f"{BASE_URL}/page/random/summary"
    resp = _get(url)
    resp.raise_for_status()
    data = resp.json()

    output = f"## {data.get('title', 'Random Article')}\n\n"
    output += f"{data.get('extract', 'No summary available.')}\n\n"
    if data.get('description'):
        output += f"*({data.get('description')})*\n\n"
    desktop_url = data.get('content_urls', {}).get('desktop', {}).get('page', '#')
    output += f"[Read more →]({desktop_url})"
    return output


import random


DINO_HOOK_TEMPLATES = [
    "The largest {species} ever found weighed {weight} — equivalent to {comparison}.",
    "For {species}, researchers discovered {discovery} — and it changed everything we thought we knew.",
    "{species} lived in {location} and could {ability}.",
    "Scientists found a {species} {discovery} — making it one of {rarity}.",
    "The {species} wasn't what scientists expected: {twist}.",
]


def dino_fact(species: str = "") -> str:
    """
    Get a compelling 'Did You Know' style fact specifically about dinosaurs or prehistoric life.
    If species is provided, returns a fact about that specific dinosaur.
    Otherwise picks a random dinosaur and returns a fact about it.
    """
    import random

    if species:
        # Get summary for specific species
        title_slug = species.replace(" ", "_")
        url = f"{BASE_URL}/page/summary/{title_slug}"
        resp = _get(url)
        if resp.status_code == 404:
            # Fall back to search
            search_result = search_wikipedia(f"{species} dinosaur", limit=3)
            return f"Couldn't find '{species}' directly on Wikipedia. Try searching:\n\n{search_result}"
        resp.raise_for_status()
        data = resp.json()
        fact = data.get('extract', '')
        title = data.get('title', species)
        if not fact:
            return f"Not enough data on {title} yet. Try a different species!"
        desktop_url = data.get('content_urls', {}).get('desktop', {}).get('page', '#')
        return f"**Did you know about {title}?**\n\n{fact}\n\n*Source: [Wikipedia — {title}]({desktop_url})*"

    # Pick a random dinosaur from a curated list
    dinos = [
        "Tyrannosaurus", "Triceratops", "Velociraptor", "Spinosaurus",
        "Stegosaurus", "Ankylosaurus", "Brachiosaurus", "Parasaurolophus",
        "Pteranodon", "Mosasaurus", "Allosaurus", "Diplodocus",
        "Carnotaurus", "Giganotosaurus", "Carcharodontosaurus",
        "Acrocanthosaurus", "Argentinosaurus", "Therizinosaurus",
        "Utahraptor", "Oviraptor", "Troodon", "Deinonychus",
        "Dimorphodon", "Quetzalcoatlus", "Plateosaurus", "Coelophysis",
        "Mamenchisaurus", "Styracosaurus", "Protoceratops", "Pentaceratops",
    ]
    species = random.choice(dinos)
    return dino_fact(species)


def did_you_know() -> str:
    """Get a random 'Did You Know' style fact from Wikipedia."""
    url = f"{BASE_URL}/page/random/summary"
    resp = _get(url)
    resp.raise_for_status()
    data = resp.json()

    fact = data.get('extract', '')
    title = data.get('title', '')

    if not fact:
        return f"Did you know? {title} is a fascinating topic on Wikipedia!"

    desktop_url = data.get('content_urls', {}).get('desktop', {}).get('page', '#')
    return f"**Did you know?**\n\n{fact}\n\n*Source: [Wikipedia — {title}]({desktop_url})*"


if __name__ == "__main__":
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())
            method = request.get("method", "")
            msg_id = request.get("id")

            if method == "initialize":
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "wikipedia-mcp",
                            "version": "1.0.1"
                        }
                    }
                }))
                sys.stdout.flush()

            elif method == "tools/list":
                tools = [
                    {
                        "name": "search",
                        "description": "Search Wikipedia for articles matching a query",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"},
                                "limit": {"type": "integer", "description": "Max results (default 5, max 20)", "default": 5}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "summary",
                        "description": "Get a Wikipedia article summary by title",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string", "description": "Article title (e.g. 'Tyrannosaurus' or 'Albert_Einstein')"}
                            },
                            "required": ["title"]
                        }
                    },
                    {
                        "name": "random",
                        "description": "Get a random Wikipedia article summary",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "did_you_know",
                        "description": "Get a random 'Did You Know' style fact from Wikipedia — great for hooks, hooks for dino docs!",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "dino_fact",
                        "description": "Get a compelling 'Did You Know' style fact specifically about dinosaurs or prehistoric life. If species is provided, returns a fact about that specific dinosaur. Otherwise picks a random dinosaur.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "species": {"type": "string", "description": "Specific dinosaur name (e.g. 'Tyrannosaurus', 'Spinosaurus'). Leave empty for a random dinosaur."}
                            }
                        }
                    }
                ]
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools}}))
                sys.stdout.flush()

            elif method == "tools/call":
                name = request["params"]["name"]
                args = request["params"].get("arguments", {})

                try:
                    if name == "search":
                        result = search_wikipedia(**args)
                    elif name == "summary":
                        result = get_summary(**args)
                    elif name == "random":
                        result = get_random()
                    elif name == "did_you_know":
                        result = did_you_know()
                    elif name == "dino_fact":
                        result = dino_fact(**args)
                    else:
                        result = f"Unknown tool: {name}"

                    print(json.dumps({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": str(result)}]
                        }
                    }))
                except Exception as e:
                    print(json.dumps({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32603, "message": str(e)}
                    }))
                sys.stdout.flush()

        except Exception as e:
            print(f"# Error: {e}", file=sys.stderr)
            sys.stderr.flush()
