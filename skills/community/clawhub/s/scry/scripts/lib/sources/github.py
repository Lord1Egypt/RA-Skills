"""GitHub source for SCRY skill.

Multi-strategy search:
1. Established repos — top stars, recently updated
2. Trending repos — recently created with stars
3. REST API fallback (no gh CLI needed)

Filters out low-quality results (0 stars, student projects).
"""

import json
import subprocess
import shutil
from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus


# Minimum stars to include (filters noise)
MIN_STARS_ESTABLISHED = 5
MIN_STARS_TRENDING = 1


def _log(msg: str):
    import sys
    sys.stderr.write(f"[GitHub] {msg}\n")
    sys.stderr.flush()


class GitHubSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="github",
            display_name="GitHub",
            tier=1,
            emoji="\U0001f419",
            id_prefix="GH",
            has_engagement=True,
            requires_keys=[],
            requires_bins=["gh"],
            domains=["tech", "dev"],
        )

    def is_available(self, config):
        if shutil.which("gh"):
            return True
        return True  # REST API fallback

    def _gh_search(self, search_query, sort, limit, timeout, extra_flags=None):
        """Run gh search repos with given query and sort."""
        cmd = [
            "gh", "search", "repos", search_query,
            f"--sort={sort}",
            f"--limit={limit}",
            "--json", "name,fullName,description,url,stargazersCount,forksCount,createdAt,updatedAt,language",
        ]
        if extra_flags:
            cmd.extend(extra_flags)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError, OSError):
            pass
        return []

    def _rest_search(self, query_str, sort, from_date, limit, timeout):
        """Fallback search using GitHub REST API."""
        url = (
            f"https://api.github.com/search/repositories"
            f"?q={quote_plus(query_str)}"
            f"&sort={sort}"
            f"&per_page={limit}"
        )
        headers = {"Accept": "application/vnd.github.v3+json"}
        try:
            data = http.get(url, headers=headers, timeout=timeout)
            return data.get("items", [])
        except Exception:
            return []

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)
        half = max(dc["max_results"] // 2, 5)
        timeout = max(dc["timeout"], 20)

        all_items = []
        seen_urls = set()

        if shutil.which("gh"):
            # Strategy 1: Established repos — most stars, recently updated
            established = self._gh_search(
                core, sort="stars", limit=half, timeout=timeout,
                extra_flags=[f"--updated=>{from_date}"],
            )
            for repo in self._parse_gh_cli(established, topic):
                if repo["url"] not in seen_urls and repo["engagement"].get("stars", 0) >= MIN_STARS_ESTABLISHED:
                    seen_urls.add(repo["url"])
                    all_items.append(repo)

            # Strategy 2: Trending repos — recently created, gaining stars
            trending = self._gh_search(
                f"{core} stars:>={MIN_STARS_TRENDING}", sort="stars", limit=half, timeout=timeout,
                extra_flags=[f"--created=>{from_date}"],
            )
            for repo in self._parse_gh_cli(trending, topic):
                if repo["url"] not in seen_urls and repo["engagement"].get("stars", 0) >= MIN_STARS_TRENDING:
                    seen_urls.add(repo["url"])
                    repo["_trending"] = True
                    all_items.append(repo)

        else:
            # REST API fallback — single query, established repos
            rest_query = f"{core} pushed:>{from_date} stars:>={MIN_STARS_ESTABLISHED}"
            repos = self._rest_search(rest_query, "stars", from_date, dc["max_results"], timeout)
            for repo in self._parse_rest_api(repos, topic):
                if repo["url"] not in seen_urls:
                    seen_urls.add(repo["url"])
                    all_items.append(repo)

        # Sort by stars descending
        all_items.sort(key=lambda x: x.get("engagement", {}).get("stars", 0), reverse=True)
        return all_items[:dc["max_results"]]

    def _parse_gh_cli(self, repos, topic):
        """Parse results from gh CLI."""
        items = []
        for repo in repos:
            full_name = repo.get("fullName", "") or repo.get("name", "")
            name = repo.get("name", "")
            description = repo.get("description", "") or ""
            url = repo.get("url", "")

            if not name or not url:
                continue

            # Use updatedAt for "last active" date
            item_date = None
            updated = repo.get("updatedAt", "") or repo.get("createdAt", "")
            if updated:
                dt = dates.parse_date(updated)
                if dt:
                    item_date = dt.date().isoformat()

            language = repo.get("language", "") or ""

            stars = repo.get("stargazersCount", 0) or 0
            forks = repo.get("forksCount", 0) or 0

            # Build display title: owner/repo
            display = full_name if "/" in full_name else name

            items.append({
                "title": display,
                "url": url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, f"{name} {description}"),
                "engagement": {
                    "stars": stars,
                    "forks": forks,
                },
                "author": full_name.split("/")[0] if "/" in full_name else "",
                "snippet": description[:300],
                "language": language,
            })
        return items

    def _parse_rest_api(self, repos, topic):
        """Parse results from GitHub REST API."""
        items = []
        for repo in repos:
            full_name = repo.get("full_name", "") or repo.get("name", "")
            description = repo.get("description", "") or ""
            url = repo.get("html_url", "")

            if not full_name or not url:
                continue

            item_date = None
            updated = repo.get("pushed_at", "") or repo.get("updated_at", "")
            if updated:
                dt = dates.parse_date(updated)
                if dt:
                    item_date = dt.date().isoformat()

            items.append({
                "title": full_name,
                "url": url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, f"{full_name} {description}"),
                "engagement": {
                    "stars": repo.get("stargazers_count", 0) or 0,
                    "forks": repo.get("forks_count", 0) or 0,
                },
                "author": repo.get("owner", {}).get("login", "") if isinstance(repo.get("owner"), dict) else "",
                "snippet": description[:300],
                "language": repo.get("language", "") or "",
            })
        return items

    def enrich(self, items, depth, config):
        """Add README snippets for top repos if gh CLI available."""
        if depth == "quick" or not shutil.which("gh"):
            return items

        # Fetch README for top 3 repos by stars
        top = sorted(items, key=lambda x: x.get("engagement", {}).get("stars", 0), reverse=True)[:3]
        for item in top:
            url = item.get("url", "")
            # Extract owner/repo from URL
            parts = url.rstrip("/").split("/")
            if len(parts) >= 2:
                owner_repo = f"{parts[-2]}/{parts[-1]}"
                try:
                    result = subprocess.run(
                        ["gh", "api", f"repos/{owner_repo}/readme", "--jq", ".content"],
                        capture_output=True, text=True, timeout=10,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        import base64
                        try:
                            readme = base64.b64decode(result.stdout.strip()).decode("utf-8", errors="ignore")
                            # Extract first meaningful paragraph
                            lines = [l.strip() for l in readme.split("\n") if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("!") and not l.strip().startswith("[") and len(l.strip()) > 20]
                            if lines:
                                item["snippet"] = lines[0][:300]
                        except Exception:
                            pass
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                    pass

        return items


def get_source():
    return GitHubSource()
