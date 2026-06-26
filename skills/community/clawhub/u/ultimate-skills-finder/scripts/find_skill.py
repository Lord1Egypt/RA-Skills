#!/usr/bin/env python3
"""
Ultimate Skills Finder 🔍
Multi-source agent skill discovery engine.

Searches 9+ sources in parallel, cross-references, deduplicates, ranks,
and optionally security-scans results.

Usage:
  python3 find_skill.py "web scraping"
  python3 find_skill.py "pdf editor" --scan --popular
  python3 find_skill.py "seo" --json --limit 10
  python3 find_skill.py "github" --source clawhub --install
"""

import argparse
import asyncio
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
from difflib import SequenceMatcher
from typing import Optional

# ── Configuration ────────────────────────────────────────────────────────────

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", ".finder_cache.json")
CACHE_TTL = 3600  # 1 hour
REQUEST_TIMEOUT = 10
GEN_DIGITAL_URL = "https://ai.gendigital.com/api/scan/lookup"
USER_AGENT = "UltimateSkillsFinder/1.0"

# ── Data Model ───────────────────────────────────────────────────────────────

class SkillResult:
    def __init__(self, name: str, description: str = "", source: str = "",
                 install_cmds: list = None, stars: int = 0,
                 downloads: int = 0, url: str = "",
                 author: str = "", version: str = ""):
        self.name = name
        self.description = description
        self.sources = [source] if source else []
        self.install_cmds = install_cmds or []
        self.stars = max(stars, 0)
        self.downloads = max(downloads, 0)
        self.url = url
        self.author = author
        self.version = version
        self.security = None  # "SAFE", "WARNING", "DANGEROUS", or None

    def merge(self, other: "SkillResult"):
        """Merge another skill result (same skill, different source)."""
        for s in other.sources:
            if s and s not in self.sources:
                self.sources.append(s)
        self.stars = max(self.stars, other.stars)
        self.downloads = max(self.downloads, other.downloads)
        if other.description and len(other.description) > len(self.description):
            self.description = other.description
        if other.url and not self.url:
            self.url = other.url
        self.install_cmds = list(dict.fromkeys(self.install_cmds + other.install_cmds))
        if other.security and not self.security:
            self.security = other.security

    def score(self) -> float:
        """Calculate relevance/popularity score (0-1)."""
        source_authority = {
            "clawhub": 1.0, "awesome-list": 0.9, "master-skills": 0.85,
            "skillsmp": 0.7, "llmbase": 0.6, "skillsllm": 0.5,
            "lobehub": 0.65, "skills.sh": 0.7, "rush": 0.5, "github-archive": 0.6,
        }
        source_authority_val = source_authority.get(self.sources[0], 0.5)
        source_count_factor = min(len(self.sources) / 5, 1.0)
        pop_factor = min((self.downloads / 10000) if self.downloads else (self.stars / 100), 1.0)
        return (source_count_factor * 0.35 + pop_factor * 0.35 + source_authority_val * 0.30)

    def security_label(self) -> str:
        if not self.security:
            return "⚠️ Not scanned"
        labels = {"SAFE": "✅ SAFE", "analysis_pending": "⏳ Pending review",
                   "WARNING": "⚠️ Warning", "DANGEROUS": "🔴 Dangerous", "MALICIOUS": "🚫 MALICIOUS"}
        return labels.get(self.security, f"❓ {self.security}")

    def __repr__(self):
        return f"<{self.name} [{','.join(self.sources)}] score={self.score():.2f}>"

# ── Source Definitions ───────────────────────────────────────────────────────

SOURCE_WEIGHTS = {
    "clawhub": 1.0, "awesome-list": 0.9, "master-skills": 0.85,
    "skillsmp": 0.7, "skills.sh": 0.7,
}

# ── HTTP Helpers ────────────────────────────────────────────────────────────

async def fetch_json(url: str, headers: dict = None) -> Optional[dict]:
    """Async HTTP GET returning JSON."""
    if headers is None:
        headers = {"User-Agent": USER_AGENT}
    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print(f"  ⚠️  {url.split('/')[2]}: {type(e).__name__}", file=sys.stderr)
        return None

async def fetch_text(url: str) -> Optional[str]:
    """Async HTTP GET returning raw text."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        return None

# ── Source Searchers ─────────────────────────────────────────────────────────

async def search_clawhub(query: str, limit: int = 5) -> list:
    """Search ClawHub via its CLI."""
    results = []
    try:
        proc = await asyncio.create_subprocess_exec(
            "clawhub", "search", query, "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=15)
        raw = stdout.decode().strip()
        if raw:
            try:
                data = json.loads(raw)
                items = data if isinstance(data, list) else data.get("results", data.get("items", []))
                for item in items[:limit]:
                    name = item.get("name", item.get("slug", ""))
                    desc = item.get("description", item.get("summary", ""))
                    slug = item.get("slug", name)
                    results.append(SkillResult(
                        name=name, description=desc, source="clawhub",
                        install_cmds=[f"clawhub install {slug}"],
                        downloads=item.get("downloads", item.get("installs", 0)),
                        stars=item.get("stars", 0),
                        url=item.get("url", f"https://clawhub.ai/skills/{slug}"),
                        author=item.get("author", {}).get("handle", ""),
                        version=item.get("latest_version", ""),
                    ))
            except json.JSONDecodeError:
                pass  # Fall through to text parse below
    except Exception as e:
        pass
    # Fallback: try text output
    if not results:
        try:
            proc = await asyncio.create_subprocess_exec(
                "clawhub", "search", query,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=15)
            lines = stdout.decode().strip().split("\n")
            for line in lines:
                line = line.strip()
                if not line or line.startswith("No results"):
                    continue
                parts = line.split(maxsplit=2)
                if len(parts) >= 2:
                    name = parts[0].strip("-*")
                    desc = parts[-1] if len(parts) > 2 else ""
                    results.append(SkillResult(
                        name=name, description=desc, source="clawhub",
                        install_cmds=[f"clawhub install {name}"],
                    ))
                if len(results) >= limit:
                    break
        except Exception:
            pass
    return results

async def search_skillsmp(query: str, limit: int = 5) -> list:
    """Search SkillsMP via their REST API."""
    results = []
    data = await fetch_json(f"https://skillsmp.com/api/skills?search={urllib.parse.quote(query)}&limit={limit}")
    if not data:
        return results
    items = data if isinstance(data, list) else data.get("skills", data.get("data", []))
    for item in items[:limit]:
        name = item.get("name", item.get("slug", ""))
        slug = item.get("slug", name)
        results.append(SkillResult(
            name=name, description=item.get("description", ""),
            source="skillsmp",
            install_cmds=[f"clawhub install {slug}"],
            downloads=item.get("downloads", item.get("installs", 0)),
            stars=item.get("stars", 0),
            url=item.get("url", item.get("clawhub_url", f"https://skillsmp.com/skills/{slug}")),
        ))
    return results

async def search_awesome_list(query: str, limit: int = 5) -> list:
    """Search VoltAgent/awesome-openclaw-skills README."""
    results = []
    text = await fetch_text(
        "https://raw.githubusercontent.com/VoltAgent/awesome-openclaw-skills/main/README.md"
    )
    if not text:
        return results
    lines = text.split("\n")
    query_lower = query.lower()
    found = []
    for i, line in enumerate(lines):
        if query_lower not in line.lower():
            continue
        # Skip badge/image lines and header lines
        if line.startswith('![') or line.startswith('<') or line.startswith('#'):
            continue
        if 'img.shields.io' in line or 'badge' in line.lower():
            continue
        # Look for skill list patterns in markdown tables or bullet lists
        # Pattern: | `name` | description |
        table_match = re.search(r'\|\s*`([^`]+)`\s*\|\s*([^|]+)', line)
        if table_match:
            name, desc = table_match.group(1).strip(), table_match.group(2).strip()
            if name and not any(skip in name.lower() for skip in ['img', 'http', 'badge']):
                found.append((name, desc, ''))
                continue
        # Pattern: - **name** description or [name](url) - description
        link_match = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
        if not link_match:
            continue
        for name, url in link_match:
            if any(skip in name.lower() for skip in ['img', 'badge', 'http', 'license']):
                continue
            if 'clawhub' in url or 'skill' in url.lower() or 'github' in url:
                desc = ""
                for j in range(i+1, min(i+3, len(lines))):
                    s = lines[j].strip().strip("|").strip("- ")
                    if s and len(s) > 15:
                        desc = s
                        break
                found.append((name.strip(), desc, url))
    seen = set()
    for name, desc, url in found:
        nkey = name.lower().strip()
        if nkey in seen or not name:
            continue
        seen.add(nkey)
        # Clean up name
        clean_name = name.strip().strip('`').strip('*').strip()
        results.append(SkillResult(
            name=clean_name, description=desc[:200], source="awesome-list",
            install_cmds=[f"clawhub install {clean_name.lower().replace(' ', '-')}"],
            url=url or "https://github.com/VoltAgent/awesome-openclaw-skills",
        ))
        if len(results) >= limit:
            break
    return results

async def search_master_skills(query: str, limit: int = 5) -> list:
    """Search LeoYeAI/openclaw-master-skills."""
    results = []
    html = await fetch_text(
        f"https://raw.githubusercontent.com/LeoYeAI/openclaw-master-skills/main/README.md"
    )
    if not html:
        return results
    lines = html.split("\n")
    query_lower = query.lower()
    found = []
    for i, line in enumerate(lines):
        if query_lower in line.lower() and ("`" in line or "-" in line):
            name_match = re.search(r'`([^`]+)`', line)
            if name_match:
                name = name_match.group(1)
                desc = lines[i+1].strip() if i+1 < len(lines) else ""
                found.append((name, desc))
    for name, desc in found[:limit]:
        results.append(SkillResult(
            name=name.strip(), description=desc[:200], source="master-skills",
            install_cmds=[f"clawhub install {name}"],
            url="https://github.com/LeoYeAI/openclaw-master-skills",
        ))
    return results

# ── Deduplication Engine ─────────────────────────────────────────────────────

def normalize_name(name: str) -> str:
    """Normalize skill name for fuzzy matching."""
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9-]', '-', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name

def fuzzy_match(name1: str, name2: str, threshold: float = 0.7) -> bool:
    """Check if two skill names are similar enough to be the same skill."""
    n1 = normalize_name(name1)
    n2 = normalize_name(name2)
    if n1 == n2:
        return True
    if n1 in n2 or n2 in n1:
        return True
    return SequenceMatcher(None, n1, n2).ratio() >= threshold

def deduplicate(results: list) -> list:
    """Deduplicate and merge skill results across sources."""
    merged = []
    for r in results:
        found = False
        for existing in merged:
            if fuzzy_match(r.name, existing.name):
                existing.merge(r)
                found = True
                break
        if not found:
            merged.append(r)
    return merged

# ── Security Scanner ─────────────────────────────────────────────────────────

async def scan_skill(name: str, clawhub_url: str = "") -> Optional[str]:
    """Scan a skill via Gen Digital's API."""
    url_to_scan = clawhub_url or f"https://clawhub.ai/skills/{name}"
    try:
        req = urllib.request.Request(
            GEN_DIGITAL_URL,
            data=json.dumps({"skillUrl": url_to_scan}).encode(),
            headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "done":
                return data.get("severity", "WARNING")
            elif data.get("status") == "analysis_pending":
                return "analysis_pending"
    except Exception:
        return None
    return None

async def scan_results(results: list):
    """Scan all unique results in parallel (throttled)."""
    print("\n  🔒 Scanning for security...", file=sys.stderr)
    sem = asyncio.Semaphore(3)
    async def scan_one(r: SkillResult):
        async with sem:
            result = await scan_skill(r.name, r.url)
            if result:
                r.security = result
                print(f"     {r.name}: {r.security_label()}", file=sys.stderr)
            await asyncio.sleep(0.5)
    tasks = [scan_one(r) for r in results]
    await asyncio.gather(*tasks)

# ── Cross-Reference Builder (from local cache / config) ──────────────────────

def build_local_skill_index() -> dict:
    """Build an index of locally installed skills."""
    index = {}
    search_paths = [
        os.path.expanduser("~/.openclaw/workspace/skills"),
        os.path.expanduser("~/.openclaw/skills"),
    ]
    for base in search_paths:
        if os.path.isdir(base):
            for item in os.listdir(base):
                skill_dir = os.path.join(base, item)
                if os.path.isdir(skill_dir) and os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
                    index[item] = {"path": skill_dir, "source": "local"}
    return index

# ── Main Orchestrator ────────────────────────────────────────────────────────

async def find_skills(query: str, limit: int = 5, scan: bool = False,
                      popular: bool = False, json_output: bool = False,
                      sources: list = None) -> list:
    """Main search orchestrator - queries all sources in parallel."""
    print(f"\n  🔍 Searching {len(sources or SOURCE_WEIGHTS)} sources for \"{query}\"...", file=sys.stderr)

    source_searchers = {
        "clawhub": search_clawhub,
        "skillsmp": search_skillsmp,
        "awesome-list": search_awesome_list,
        "master-skills": search_master_skills,
    }

    if sources:
        source_searchers = {k: v for k, v in source_searchers.items() if k in sources}

    # Run all searchers in parallel
    tasks = []
    for name, searcher in source_searchers.items():
        tasks.append(searcher(query, limit))

    all_results = []
    batch_results = await asyncio.gather(*tasks, return_exceptions=True)
    for batch in batch_results:
        if isinstance(batch, list):
            all_results.extend(batch)

    if not all_results:
        return []

    # Deduplicate
    merged = deduplicate(all_results)
    print(f"  📊 Found {len(all_results)} raw results → {len(merged)} unique skills", file=sys.stderr)

    # Sort by score
    if popular:
        merged.sort(key=lambda r: r.downloads + r.stars * 100, reverse=True)
    else:
        merged.sort(key=lambda r: r.score(), reverse=True)

    # Security scan if requested
    if scan and merged:
        await scan_results(merged)

    return merged[:limit * 3]

def display_results(results: list, query: str, show_install: bool = False, json_output: bool = False):
    """Display results in a nice table format."""
    if not results:
        print(f"\n  😕 No skills found for \"{query}\".")
        print("  Suggestions:")
        print("    • Try broader terms (e.g., 'email' instead of 'newsletter-automation')")
        print("    • Try synonyms (e.g., 'scraping' instead of 'crawling')")
        print("    • Check skills.sh: https://skills.sh")
        print("    • Browse ClawHub: https://clawhub.ai")
        return

    if json_output:
        output = []
        for r in results:
            output.append({
                "name": r.name,
                "description": r.description[:200],
                "sources": r.sources,
                "score": round(r.score(), 3),
                "downloads": r.downloads,
                "stars": r.stars,
                "install": r.install_cmds,
                "security": r.security,
                "url": r.url,
            })
        print(json.dumps(output, indent=2))
        return

    # Rank emoji
    rank_emoji = ["🥇", "🥇", "🥈", "🥈", "🥉", "🥉", "📌", "📌", "📌", "📌"]

    print(f"\n  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   🔍 Results for \"{query}\"")
    print(f"   {len(results)} unique skills found")
    print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    for i, r in enumerate(results[:10]):
        emoji = rank_emoji[i] if i < len(rank_emoji) else "•"
        stars_display = "★" * min(5, max(1, int(r.stars / 20 + 1))) + "☆" * max(0, 5 - max(1, int(r.stars / 20 + 1)))
        downloads_display = f"{r.downloads:,}⬇" if r.downloads else f"{r.stars}★" if r.stars else ""

        print(f"\n  {emoji} {r.name}")
        print(f"     {stars_display}  {downloads_display}  [{', '.join(r.sources[:4])}]")
        if r.description:
            desc = r.description[:150]
            print(f"     {desc}{'...' if len(r.description) > 150 else ''}")
        if show_install and r.install_cmds:
            for cmd in r.install_cmds[:2]:
                print(f"     → {cmd}")
        if r.security:
            print(f"     🔒 {r.security_label()}")

    secured = [r for r in results if r.security == "SAFE"]
    pending = [r for r in results if r.security == "analysis_pending"]
    if secured or pending:
        print(f"\n  🔒 Security: {len(secured)} safe, {len(pending)} pending review")

    print(f"\n  💡 Tip: Use --scan to security-check results before installing.")

def main():
    parser = argparse.ArgumentParser(
        description="Ultimate Skills Finder — Multi-source agent skill discovery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 find_skill.py "web scraping"     Basic search
  python3 find_skill.py "pdf" --scan       Search + security scan
  python3 find_skill.py "seo" --popular    Sort by popularity
  python3 find_skill.py "github" --install Show install commands
  python3 find_skill.py "email" --json     JSON output
  python3 find_skill.py "email" --source clawhub  Single source
        """
    )
    parser.add_argument("query", help="Search query (e.g., 'web scraping', 'pdf editor')")
    parser.add_argument("--limit", type=int, default=5, help="Max results per source")
    parser.add_argument("--scan", action="store_true", help="Security-scan results via Gen Digital")
    parser.add_argument("--popular", action="store_true", help="Sort by popularity instead of relevance")
    parser.add_argument("--install", action="store_true", help="Show install commands")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--source", choices=list(SOURCE_WEIGHTS.keys()) + ["all"],
                       default="all", help="Limit to specific source")

    args = parser.parse_args()

    sources = None if args.source == "all" else [args.source]

    results = asyncio.run(find_skills(
        query=args.query,
        limit=args.limit,
        scan=args.scan,
        popular=args.popular,
        json_output=args.json,
        sources=sources,
    ))

    display_results(results, args.query, show_install=args.install, json_output=args.json)

if __name__ == "__main__":
    main()
