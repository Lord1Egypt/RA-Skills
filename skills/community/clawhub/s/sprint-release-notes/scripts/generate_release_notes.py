#!/usr/bin/env python3
"""
Sprint Release Notes Generator
Reads a GitHub Project Board (v2), analyzes the current sprint,
gathers documentation, scores contributors, and publishes release notes as GitHub Releases.

Usage:
 python generate_release_notes.py \
 --board-url "https://github.com/orgs/myorg/projects/1" \
 --pat "ghp_xxxxxxxxxxxx" \
 --release-repo "myorg/release-notes" \
 [--sprint-id "iteration-id"] \
 [--output-dir "/path/to/output"] \
 [--dry-run]
"""

import argparse
import base64
import json
import re
import sys
import time
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library required. Install with: pip install requests --break-system-packages")
    sys.exit(1)


# ─────────────────────────────────────────────
# Configuration & Constants
# ─────────────────────────────────────────────

GRAPHQL_URL = "https://api.github.com/graphql"
REST_BASE = "https://api.github.com"

FEATURE_LABELS = {"feature", "enhancement", "user-facing", "feat", "story"}
INFRA_LABELS = {"infra", "infrastructure", "tech-debt", "performance", "security", "devops", "scalability", "ci", "cd", "chore"}
BUG_LABELS = {"bug", "fix", "hotfix", "bugfix", "defect"}
CHALLENGE_LABELS_HIGH = {"critical", "complex", "breaking-change", "architecture", "major"}
CHALLENGE_LABELS_MED = {"refactor", "migration", "major"}

DONE_STATUSES = {"done", "closed", "completed", "shipped", "merged", "✅ done", "✅ shipped"}


# ─────────────────────────────────────────────
# API Helpers
# ─────────────────────────────────────────────

class GitHubClient:
    def __init__(self, pat_token):
        self.pat = pat_token
        self.graphql_headers = {
            "Authorization": f"bearer {pat_token}",
            "Content-Type": "application/json"
        }
        self.rest_headers = {
            "Authorization": f"token {pat_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self._readme_cache = {}

    def graphql(self, query, variables=None):
        """Execute a GraphQL query with retry on rate limit."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        for attempt in range(3):
            resp = requests.post(GRAPHQL_URL, headers=self.graphql_headers, json=payload)
            if resp.status_code == 403 and "rate limit" in resp.text.lower():
                reset_time = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
                wait = max(reset_time - int(time.time()), 10)
                print(f" ⏳ Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            if "errors" in data:
                err_msg = "; ".join(e.get("message", str(e)) for e in data["errors"])
                raise Exception(f"GraphQL errors: {err_msg}")
            return data["data"]
        raise Exception("Failed after 3 retries due to rate limiting")

    def rest_get(self, path):
        """GET request to REST API."""
        url = f"{REST_BASE}{path}" if path.startswith("/") else path
        for attempt in range(3):
            resp = requests.get(url, headers=self.rest_headers)
            if resp.status_code == 403 and "rate limit" in resp.text.lower():
                wait = 30
                print(f" ⏳ Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        raise Exception("Failed after 3 retries")

    def rest_put(self, path, data):
        """PUT request to REST API."""
        url = f"{REST_BASE}{path}" if path.startswith("/") else path
        resp = requests.put(url, headers=self.rest_headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def rest_post(self, path, data):
        """POST request to REST API."""
        url = f"{REST_BASE}{path}" if path.startswith("/") else path
        resp = requests.post(url, headers=self.rest_headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def rest_patch(self, path, data):
        """PATCH request to REST API."""
        url = f"{REST_BASE}{path}" if path.startswith("/") else path
        resp = requests.patch(url, headers=self.rest_headers, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_readme(self, repo_full_name):
        """Fetch and cache a repo's README."""
        if repo_full_name in self._readme_cache:
            return self._readme_cache[repo_full_name]
        result = self.rest_get(f"/repos/{repo_full_name}/readme")
        if result and "content" in result:
            content = base64.b64decode(result["content"]).decode("utf-8", errors="replace")
            self._readme_cache[repo_full_name] = content
            return content
        self._readme_cache[repo_full_name] = None
        return None


# ─────────────────────────────────────────────
# Phase 1: Discover Sprint
# ─────────────────────────────────────────────

def parse_board_url(url):
    """Extract org/user and project number from board URL."""
    org_match = re.match(r"https://github\.com/orgs/([^/]+)/projects/(\d+)", url)
    if org_match:
        return {"type": "organization", "owner": org_match.group(1), "number": int(org_match.group(2))}
    user_match = re.match(r"https://github\.com/users/([^/]+)/projects/(\d+)", url)
    if user_match:
        return {"type": "user", "owner": user_match.group(1), "number": int(user_match.group(2))}
    raise ValueError(f"Could not parse board URL: {url}")


def fetch_project_id(client, board_info):
    """Fetch the project's node ID."""
    print(f"📋 Fetching project ID for {board_info['owner']}/projects/{board_info['number']}...")
    query = """
    query($owner: String!, $number: Int!) {
        %s(login: $owner) {
            projectV2(number: $number) {
                id
                title
                shortDescription
                url
            }
        }
    }
    """ % board_info["type"]
    data = client.graphql(query, {"owner": board_info["owner"], "number": board_info["number"]})
    project = data[board_info["type"]]["projectV2"]
    print(f" ✅ Found project: {project['title']}")
    return project


def fetch_iteration_field(client, project_id):
    """Fetch the iteration field and its iterations."""
    print("🔄 Fetching iteration fields...")
    query = """
    query($projectId: ID!) {
        node(id: $projectId) {
            ... on ProjectV2 {
                fields(first: 50) {
                    nodes {
                        ... on ProjectV2IterationField {
                            id
                            name
                            configuration {
                                iterations { id title startDate duration }
                                completedIterations { id title startDate duration }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    data = client.graphql(query, {"projectId": project_id})
    fields = data["node"]["fields"]["nodes"]
    for field in fields:
        if "configuration" in field and field.get("configuration"):
            print(f" ✅ Found iteration field: {field['name']}")
            return field
    raise Exception("No iteration field found on this project board.")


def find_current_sprint(iteration_field, target_sprint_id=None):
    """Identify the current or most recent sprint."""
    config = iteration_field["configuration"]
    all_iterations = config.get("iterations", []) + config.get("completedIterations", [])
    if not all_iterations:
        raise Exception("No iterations found on the project board.")
    if target_sprint_id:
        for it in all_iterations:
            if it["id"] == target_sprint_id:
                print(f" 🎯 Using specified sprint: {it['title']}")
                return it
        raise Exception(f"Sprint ID '{target_sprint_id}' not found.")
    today = datetime.now().date()
    for it in config.get("iterations", []):
        start = datetime.strptime(it["startDate"], "%Y-%m-%d").date()
        end = start + timedelta(days=it["duration"])
        if start <= today <= end:
            print(f" 🎯 Current active sprint: {it['title']}")
            return it
    completed = config.get("completedIterations", [])
    if completed:
        completed_sorted = sorted(completed, key=lambda x: x["startDate"], reverse=True)
        latest = completed_sorted[0]
        print(f" 🎯 Most recently completed sprint: {latest['title']}")
        return latest
    raise Exception("Could not determine current sprint.")


# ─────────────────────────────────────────────
# Phase 2: Fetch & Categorize Items
# ─────────────────────────────────────────────

def fetch_sprint_items(client, project_id, iteration_field_id, sprint_id):
    """Fetch all items in the sprint and categorize them."""
    print("📦 Fetching sprint items...")
    query = """
    query($projectId: ID!, $cursor: String) {
        node(id: $projectId) {
            ... on ProjectV2 {
                items(first: 100, after: $cursor) {
                    pageInfo { hasNextPage endCursor }
                    nodes {
                        id
                        content {
                            ... on Issue {
                                id title number state url body
                                labels(first: 20) { nodes { name } }
                                assignees(first: 10) { nodes { login name } }
                                repository { nameWithOwner url }
                            }
                            ... on PullRequest {
                                id title number state merged url body
                                additions deletions changedFiles
                                labels(first: 20) { nodes { name } }
                                assignees(first: 10) { nodes { login name } }
                                repository { nameWithOwner url }
                                author { login }
                            }
                            ... on DraftIssue { title body assignees(first: 10) { nodes { login } } }
                        }
                        fieldValues(first: 20) {
                            nodes {
                                ... on ProjectV2ItemFieldIterationValue {
                                    field { ... on ProjectV2IterationField { name id } }
                                    title iterationId
                                }
                                ... on ProjectV2ItemFieldSingleSelectValue {
                                    field { ... on ProjectV2SingleSelectField { name } }
                                    name
                                }
                                ... on ProjectV2ItemFieldNumberValue {
                                    field { ... on ProjectV2Field { name } }
                                    number
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    all_items = []
    cursor = None
    while True:
        data = client.graphql(query, {"projectId": project_id, "cursor": cursor})
        items_data = data["node"]["items"]
        all_items.extend(items_data["nodes"])
        if not items_data["pageInfo"]["hasNextPage"]:
            break
        cursor = items_data["pageInfo"]["endCursor"]
    sprint_items = []
    for item in all_items:
        field_values = item.get("fieldValues", {}).get("nodes", [])
        for fv in field_values:
            if fv.get("iterationId") == sprint_id:
                sprint_items.append(item)
                break
    print(f" ✅ Found {len(sprint_items)} items in this sprint")
    completed = []
    carried_over = []
    for item in sprint_items:
        status = get_item_status(item)
        if status.lower() in DONE_STATUSES:
            completed.append(item)
        else:
            carried_over.append(item)
    print(f" ✅ Completed: {len(completed)} | Carried over: {len(carried_over)}")
    return completed, carried_over


def get_item_status(item):
    """Extract the status field value from an item."""
    field_values = item.get("fieldValues", {}).get("nodes", [])
    for fv in field_values:
        if "field" in fv and fv["field"]:
            field_name = fv["field"].get("name", "").lower()
            if field_name == "status" and "name" in fv:
                return fv["name"]
    content = item.get("content", {})
    if content:
        if content.get("state") == "CLOSED" or content.get("merged"):
            return "Done"
    return "Unknown"


def get_item_labels(item):
    """Extract label names from an item."""
    content = item.get("content", {})
    if not content:
        return []
    labels = content.get("labels", {}).get("nodes", [])
    return [l["name"].lower() for l in labels]


def categorize_item(item):
    """Categorize item into: feature, infra, bug, or other."""
    labels = set(get_item_labels(item))
    if labels & BUG_LABELS:
        return "bug"
    if labels & INFRA_LABELS:
        return "infra"
    if labels & FEATURE_LABELS:
        return "feature"
    title = (item.get("content", {}).get("title", "") or "").lower()
    if any(kw in title for kw in ["fix", "bug", "patch", "hotfix"]):
        return "bug"
    if any(kw in title for kw in ["infra", "deploy", "ci", "refactor", "migrate", "performance"]):
        return "infra"
    return "feature"


# ─────────────────────────────────────────────
# Phase 3: Deep-Read Completed Items
# ─────────────────────────────────────────────

def gather_item_details(client, item):
    """Gather PR descriptions, docs changes, and commit messages for an item."""
    content = item.get("content", {})
    if not content:
        return {"title": "Draft Item", "description": "", "prs": [], "docs": []}
    title = content.get("title", "Untitled")
    body = content.get("body", "") or ""
    repo = content.get("repository", {})
    repo_name = repo.get("nameWithOwner", "") if repo else ""
    details = {
        "title": title,
        "description": body[:500],
        "repo": repo_name,
        "prs": [],
        "docs_changed": [],
        "assignees": [a["login"] for a in content.get("assignees", {}).get("nodes", [])],
        "labels": get_item_labels(item),
        "category": categorize_item(item),
        "story_points": get_story_points(item),
    }
    if content.get("merged") is not None:
        details["prs"].append({
            "number": content.get("number"),
            "title": title,
            "body": body[:500],
            "additions": content.get("additions", 0),
            "deletions": content.get("deletions", 0),
            "author": content.get("author", {}).get("login", "unknown"),
            "repo": repo_name,
        })
        if repo_name:
            pr_files = client.rest_get(f"/repos/{repo_name}/pulls/{content['number']}/files")
            if pr_files:
                for f in pr_files:
                    if is_doc_file(f.get("filename", "")):
                        details["docs_changed"].append(f["filename"])
    return details


def get_story_points(item):
    """Extract story points from field values if available."""
    field_values = item.get("fieldValues", {}).get("nodes", [])
    for fv in field_values:
        if "field" in fv and fv["field"]:
            name = fv["field"].get("name", "").lower()
            if any(kw in name for kw in ["point", "size", "estimate", "effort"]):
                if "number" in fv:
                    return fv["number"]
    return None


def is_doc_file(filepath):
    """Check if a file is documentation."""
    fp = filepath.lower()
    return fp.startswith("docs/") or fp.startswith("doc/") or fp.startswith("wiki/") or fp == "readme.md" or fp.endswith("/readme.md") or (fp.endswith(".md") and "/" not in fp)


# ─────────────────────────────────────────────
# Phase 4: Evaluate Contributors
# ─────────────────────────────────────────────

def evaluate_contributors(client, completed_items, item_details_list):
    """Score contributors and determine Lead Engineer and MVP."""
    print("🏆 Evaluating contributors...")
    scores = defaultdict(lambda: {
        "prs_merged": 0, "lines_changed": 0, "reviews_given": 0, "bugs_fixed": 0,
        "challenge_total": 0, "max_challenge": 0, "max_challenge_item": "", "notable_items": [],
    })
    reviewed_prs = set()
    for item, details in zip(completed_items, item_details_list):
        category = details["category"]
        challenge = estimate_challenge(details)
        for assignee in details["assignees"]:
            scores[assignee]["challenge_total"] += challenge
            if challenge > scores[assignee]["max_challenge"]:
                scores[assignee]["max_challenge"] = challenge
                scores[assignee]["max_challenge_item"] = details["title"]
                scores[assignee]["notable_items"].append(details["title"])
            if category == "bug":
                scores[assignee]["bugs_fixed"] += 1
        for pr in details["prs"]:
            author = pr.get("author", "unknown")
            if author != "unknown":
                scores[author]["prs_merged"] += 1
                scores[author]["lines_changed"] += pr.get("additions", 0) + pr.get("deletions", 0)
            pr_key = f"{pr['repo']}#{pr['number']}"
            if pr_key not in reviewed_prs and pr.get("repo") and pr.get("number"):
                reviewed_prs.add(pr_key)
                reviews = client.rest_get(f"/repos/{pr['repo']}/pulls/{pr['number']}/reviews")
                if reviews:
                    for review in reviews:
                        reviewer = review.get("user", {}).get("login", "")
                        if reviewer and review.get("state") in ("APPROVED", "CHANGES_REQUESTED", "COMMENTED"):
                            scores[reviewer]["reviews_given"] += 1
    results = {}
    for user, s in scores.items():
        total = (s["prs_merged"] * 2 + s["lines_changed"] / 100 + s["reviews_given"] * 3 + s["bugs_fixed"] * 4 + s["challenge_total"] * 5)
        results[user] = {**s, "total": round(total, 1)}
    if not results:
        print(" ⚠️ No contributors found")
        return None, None, results
    sorted_contributors = sorted(results.items(), key=lambda x: x[1]["total"], reverse=True)
    lead = sorted_contributors[0]
    mvp = max(results.items(), key=lambda x: (x[1]["max_challenge"], x[1]["bugs_fixed"], x[1]["reviews_given"]))
    if mvp[0] == lead[0] and len(sorted_contributors) > 1:
        for contributor in sorted_contributors[1:]:
            if contributor[1]["max_challenge"] > 0 or contributor[1]["bugs_fixed"] > 0:
                mvp = contributor
                break
        else:
            mvp = sorted_contributors[1] if len(sorted_contributors) > 1 else lead
    print(f" 🥇 Lead Engineer: @{lead[0]} (score: {lead[1]['total']})")
    print(f" 🏅 MVP: @{mvp[0]}")
    return lead, mvp, results


def estimate_challenge(details):
    """Estimate difficulty of an item."""
    sp = details.get("story_points")
    if sp is not None:
        if sp >= 13: return 5
        elif sp >= 8: return 4
        elif sp >= 5: return 3
        elif sp >= 3: return 2
        else: return 1
    labels = set(details.get("labels", []))
    challenge = 2
    if labels & CHALLENGE_LABELS_HIGH:
        challenge = 5
    elif labels & CHALLENGE_LABELS_MED:
        challenge = 4
    total_lines = sum(pr.get("additions", 0) + pr.get("deletions", 0) for pr in details.get("prs", []))
    total_files = sum(pr.get("changedFiles", 0) for pr in details.get("prs", []))
    if total_lines > 500 and total_files > 10:
        challenge = max(challenge, 4)
    return challenge


# ─────────────────────────────────────────────
# Phase 5: Compile Release Notes
# ─────────────────────────────────────────────

def compile_release_notes(sprint, completed_details, carried_over, lead, mvp, all_scores, board_url):
    """Generate the release notes markdown."""
    print("📝 Compiling release notes...")
    sprint_title = sprint["title"]
    sprint_number = extract_sprint_number(sprint_title)
    version = f"v1.{sprint_number}.0"
    today = datetime.now().strftime("%Y-%m-%d")
    features = [d for d in completed_details if d["category"] == "feature"]
    infra = [d for d in completed_details if d["category"] == "infra"]
    bugs = [d for d in completed_details if d["category"] == "bug"]
    sections = []
    sections.append(f"# 🚀 Sprint Release Notes: {sprint_title}")
    sections.append(f"\n**Date:** {today} | **Version:** {version} | **Status:** Shipped\n")
    sections.append("---\n")
    sections.append("## 🎯 Executive Summary (The \"So What?\")\n")
    summary = generate_executive_summary(features, infra, bugs, carried_over)
    sections.append(summary + "\n---\n")
    sections.append("## ✨ New User-Facing Features (Value Delivery)\n")
    if features:
        for f in features:
            sections.append(f"* **{f['title']}**: {summarize_item(f)}")
            sections.append(f" * **Value**: {infer_value(f)}\n")
    else:
        sections.append("No new user-facing features this sprint.\n")
    sections.append("---\n")
    sections.append("## 🛠️ Infrastructure & Tech Debt (The \"Iceberg\")\n")
    if infra:
        for i in infra:
            sections.append(f"* {summarize_item(i)}")
        sections.append("")
    else:
        sections.append("No infrastructure changes this sprint.\n")
    sections.append("---\n")
    sections.append("## 🐛 Stability & Bug Fixes\n")
    if bugs:
        for b in bugs:
            sections.append(f"* {summarize_item(b)}")
        sections.append("")
    else:
        sections.append("No bug fixes this sprint.\n")
    sections.append("---\n")
    sections.append("## 📊 Engineering Health Snapshot\n")
    total_planned = len(completed_details) + len(carried_over)
    sections.append(f"* **Sprint Velocity**: {len(completed_details)} items completed out of {total_planned} planned")
    carry_rate = round(len(carried_over) / total_planned * 100) if total_planned > 0 else 0
    sections.append(f"* **Carry-over Rate**: {len(carried_over)} items ({carry_rate}%) deferred to next sprint")
    sections.append(f"* **Contributors**: {len(all_scores)} engineers active this sprint\n")
    sections.append("---\n")
    sections.append("## ⚠️ Known Issues & Carry-over\n")
    if carried_over:
        for co in carried_over:
            co_content = co.get("content", {})
            co_title = co_content.get("title", "Untitled") if co_content else "Draft Item"
            sections.append(f"* **{co_title}**: Deferred to next sprint")
        sections.append("")
    else:
        sections.append("All planned items were completed! 🎉\n")
    sections.append("---\n")
    sections.append("## 🏆 Kudos & Ownership\n")
    if lead:
        lead_user, lead_data = lead
        lead_justification = f"Led {lead_data['prs_merged']} PRs"
        if lead_data['notable_items']:
            lead_justification += f" including {lead_data['notable_items'][0]}"
        if lead_data['reviews_given'] > 0:
            lead_justification += f", reviewed {lead_data['reviews_given']} PRs"
        sections.append(f"* **Lead Engineer**: @{lead_user} — {lead_justification}")
    if mvp:
        mvp_user, mvp_data = mvp
        mvp_justification = ""
        if mvp_data['max_challenge_item']:
            mvp_justification = f"Tackled {mvp_data['max_challenge_item']} (highest complexity)"
        if mvp_data['bugs_fixed'] > 0:
            mvp_justification += f", fixed {mvp_data['bugs_fixed']} critical bugs"
        if not mvp_justification:
            mvp_justification = f"Contributed across {len(mvp_data['notable_items'])} items"
        sections.append(f"* **MVP (Unsung Hero)**: @{mvp_user} — {mvp_justification}")
    sections.append("")
    sections.append(f"---\n*Generated automatically from [GitHub Project Board]({board_url}).*\n")
    return "\n".join(sections)


def extract_sprint_number(title):
    match = re.search(r"(\d+)", title)
    return match.group(1) if match else "0"


def generate_executive_summary(features, infra, bugs, carried_over):
    parts = []
    if features:
        parts.append(f"This sprint delivered {len(features)} new feature(s)")
        if len(features) > 0:
            parts[-1] += f", headlined by {features[0]['title']}"
    if infra:
        parts.append(f"{len(infra)} infrastructure improvement(s) were shipped to strengthen system reliability")
    if bugs:
        parts.append(f"{len(bugs)} bug(s) were resolved improving overall stability")
    if carried_over:
        parts.append(f"{len(carried_over)} item(s) were carried over to the next sprint")
    if not parts:
        return "This sprint focused on maintenance and planning activities."
    return ". ".join(parts) + "."


def summarize_item(details):
    # Strip images and markdown image syntax
    desc = details.get("description", "")
    if desc:
        # Remove markdown images ![alt](url)
        import re
        desc = re.sub(r'!\[.*?\]\(.*?\)', '', desc)
        # Remove raw image URLs
        desc = re.sub(r'https?://[^\s]+\.(jpg|jpeg|png|gif|webp)', '', desc, flags=re.IGNORECASE)
        # Remove img tags
        desc = re.sub(r'<img[^>]*>', '', desc)
        # Get first sentence, ensure it's complete
        sentences = desc.split('.')
        first_sentence = sentences[0].strip() if sentences else ""
        # If sentence is too short or empty, use title
        if len(first_sentence) < 15:
            return details["title"]
        # Ensure it ends with period
        if not first_sentence.endswith('.'):
            first_sentence += '.'
        return first_sentence
    return details["title"]


def infer_value(details):
    desc = (details.get("description", "") or "").lower()
    if any(kw in desc for kw in ["user experience", "ux", "usability"]):
        return "Improves user experience and workflow efficiency"
    if any(kw in desc for kw in ["performance", "speed", "fast"]):
        return "Delivers faster, more responsive experience for users"
    if any(kw in desc for kw in ["new feature", "capability", "enable"]):
        return "Unlocks new capability for users"
    return "Enhances product functionality and user satisfaction"


# ─────────────────────────────────────────────
# Phase 6: Publish
# ─────────────────────────────────────────────

def publish_release_notes_per_repo(client, items_by_repo, sprint_title, release_notes_template, dry_run=False):
    """Create or update a GitHub Release per repo; markdown is the release body (tag v1.{sprint}.0)."""
    sprint_number = extract_sprint_number(sprint_title)
    today = datetime.now().strftime("%Y-%m-%d")
    published_links = []
    tag_name = f"v1.{sprint_number}.0"

    for repo_name, completed_items in items_by_repo.items():
        if not repo_name or not completed_items:
            continue
        print(f"\n📤 Publishing release {tag_name} to {repo_name}...")
        repo_notes = generate_repo_release_notes(sprint_title, sprint_number, today, completed_items, repo_name)

        if dry_run:
            print(f" 🔵 DRY RUN — skipping publish to {repo_name}")
            continue

        try:
            repo_info = client.rest_get(f"/repos/{repo_name}") or {}
            default_branch = repo_info.get("default_branch", "main")
            
            # Check if release already exists
            existing = client.rest_get(f"/repos/{repo_name}/releases/tags/{tag_name}")
            if existing and existing.get("id"):
                existing_date = existing.get("created_at", "")
                print(f" ⚠️ Release {tag_name} already exists (created: {existing_date[:10] if existing_date else 'unknown'})")
                published_links.append((repo_name, existing.get("html_url", "")))
                continue
            
            payload = {
                "name": tag_name,
                "body": repo_notes,
                "draft": False,
                "prerelease": False,
            }
            create = {
                "tag_name": tag_name,
                "target_commitish": default_branch,
                **payload,
            }
            result = client.rest_post(f"/repos/{repo_name}/releases", create)
            release_url = result.get("html_url", "")
            print(f" ✅ Published release to {repo_name}! {release_url}")
            published_links.append((repo_name, release_url))
        except Exception as e:
            print(f" ❌ Failed to publish release to {repo_name}: {e}")
    return published_links


def generate_repo_release_notes(sprint_title, sprint_number, today, completed_items, repo_name):
    """Generate release notes for a single repository."""
    import re
    
    def strip_images(text):
        if not text:
            return ""
        # Remove markdown images
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        # Remove raw image URLs
        text = re.sub(r'https?://[^\s]+\.(jpg|jpeg|png|gif|webp)', '', text, flags=re.IGNORECASE)
        # Remove img tags
        text = re.sub(r'<img[^>]*>', '', text)
        # Clean up extra whitespace
        text = re.sub(r'\n\n+', '\n', text)
        return text.strip()
    
    lines = [
        f"# 🚀 Sprint Release Notes: {sprint_title} - {repo_name.split('/')[-1]}",
        f"""
**Date:** {today} | **Version:** v1.{sprint_number}.0 | **Status:** Shipped | **Repository:** {repo_name}

---

## Summary

This sprint delivered **{len(completed_items)}** item(s) in **{repo_name}**.
"""
    ]
    
    # Group by category
    features = []
    infra = []
    bugs = []
    
    for item in completed_items:
        category = item.get("category", "other")
        title = item.get("title", "Untitled")
        # Strip images from description and ensure complete sentences
        raw_desc = item.get("description", "") or ""
        desc = strip_images(raw_desc)
        # Truncate but ensure we don't cut mid-sentence
        if len(desc) > 200:
            # Find last period within 200 chars
            last_period = desc[:200].rfind('.')
            if last_period > 50:
                desc = desc[:last_period+1]
            else:
                desc = desc[:200]
        
        if category == "feature":
            features.append((title, desc))
        elif category == "infra":
            infra.append((title, desc))
        elif category == "bug":
            bugs.append((title, desc))
        else:
            infra.append((title, desc))
    
    if features:
        lines.append("\n## ✨ New Features\n")
        for title, desc in features:
            lines.append(f"* **{title}**: {desc}")
    
    if infra:
        lines.append("\n## 🛠️ Infrastructure & Tech Debt\n")
        for title, desc in infra:
            lines.append(f"* **{title}**: {desc}")
    
    if bugs:
        lines.append("\n## 🐛 Bug Fixes\n")
        for title, desc in bugs:
            lines.append(f"* **{title}**: {desc}")
        lines.append("\n## 🛠️ Infrastructure & Tech Debt\n")
        for title, desc in infra:
            lines.append(f"* **{title}**: {desc}")
    
    if bugs:
        lines.append("\n## 🐛 Bug Fixes\n")
        for title, desc in bugs:
            lines.append(f"* **{title}**: {desc}")
    
    lines.append(f"""
---
*Generated from GitHub Project Board - {sprint_title}*
""")
    return "\n".join(lines)


def publish_release_notes(client, release_repo, sprint_title, content, dry_run=False):
    """Commit the release notes markdown to the release notes repo."""
    sprint_number = extract_sprint_number(sprint_title)
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"release-notes/sprint-{sprint_number}-{today}.md"
    print(f"📤 Publishing to {release_repo}/{filename}...")
    if dry_run:
        print(" 🔵 DRY RUN — skipping actual publish")
        return filename
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    existing = client.rest_get(f"/repos/{release_repo}/contents/{filename}")
    put_data = {
        "message": f"docs: Sprint {sprint_number} release notes - v1.{sprint_number}.0",
        "content": encoded,
        "branch": "main"
    }
    if existing and "sha" in existing:
        put_data["sha"] = existing["sha"]
    try:
        result = client.rest_put(f"/repos/{release_repo}/contents/{filename}", put_data)
        file_url = result.get("content", {}).get("html_url", f"https://github.com/{release_repo}/blob/main/{filename}")
        print(f" ✅ Published! View at: {file_url}")
        return file_url
    except Exception as e:
        repo_info = client.rest_get(f"/repos/{release_repo}")
        if repo_info:
            default_branch = repo_info.get("default_branch", "main")
            put_data["branch"] = default_branch
            result = client.rest_put(f"/repos/{release_repo}/contents/{filename}", put_data)
            file_url = result.get("content", {}).get("html_url", "")
            print(f" ✅ Published to {default_branch}! View at: {file_url}")
            return file_url
    raise


# ─────────────────────────────────────────────
# Main Orchestration
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate sprint release notes from GitHub Project Board")
    parser.add_argument("--board-url", required=True, help="GitHub Project Board URL")
    parser.add_argument("--pat", required=True, help="GitHub Personal Access Token")
    parser.add_argument("--release-repo", required=True, help="Repo to publish release notes (owner/repo)")
    parser.add_argument("--sprint-id", default=None, help="Specific sprint iteration ID")
    parser.add_argument("--output-dir", default=".", help="Directory to save local copy")
    parser.add_argument("--dry-run", action="store_true", help="Generate notes but don't publish")
    args = parser.parse_args()
    print("=" * 60)
    print("🚀 Sprint Release Notes Generator")
    print("=" * 60)
    client = GitHubClient(args.pat)
    board_info = parse_board_url(args.board_url)
    project = fetch_project_id(client, board_info)
    project_id = project["id"]
    iteration_field = fetch_iteration_field(client, project_id)
    sprint = find_current_sprint(iteration_field, args.sprint_id)
    completed, carried_over = fetch_sprint_items(client, project_id, iteration_field["id"], sprint["id"])
    if not completed and not carried_over:
        print("⚠️ No items found in this sprint.")
        sys.exit(1)
    print("🔍 Gathering details for completed items...")
    completed_details = []
    for i, item in enumerate(completed):
        title = item.get("content", {}).get("title", "Untitled") if item.get("content") else "Draft"
        print(f" [{i+1}/{len(completed)}] {title}")
        details = gather_item_details(client, item)
        completed_details.append(details)
    lead, mvp, all_scores = evaluate_contributors(client, completed, completed_details)
    release_notes = compile_release_notes(sprint, completed_details, carried_over, lead, mvp, all_scores, args.board_url)
    sprint_number = extract_sprint_number(sprint["title"])
    today = datetime.now().strftime("%Y-%m-%d")
    local_filename = f"sprint-{sprint_number}-{today}.md"
    local_path = f"{args.output_dir}/{local_filename}"
    with open(local_path, "w") as f:
        f.write(release_notes)
    print(f"\n💾 Saved locally: {local_path}")
    print(f"\n📊 Summary: {len(completed)} completed, {len(carried_over)} carried over")
    print("\n" + "=" * 60)
    if not args.dry_run:
        # Group items by repository
        items_by_repo = defaultdict(list)
        for details in completed_details:
            repo = details.get("repo", "")
            if repo:
                items_by_repo[repo].append(details)
        
        # Publish to each repo's Releases (create or PATCH by tag)
        published_links = publish_release_notes_per_repo(
            client, items_by_repo, sprint["title"], release_notes
        )
        
        print(f"\n🎉 Release notes published to {len(published_links)} repo(s)")
        for repo, url in published_links:
            print(f"  • {repo}: {url}")
        
        # Return links for notification
        return published_links
    else:
        print("\n🔵 Dry run complete. Release notes NOT published.")
        return []
    print("\n" + "=" * 60)
    print("✅ Done!")
    print("=" * 60)
    if all_scores:
        print("\n📊 Contributor Scores:")
        print(f" {'User':<20} {'PRs':>5} {'Lines':>8} {'Reviews':>8} {'Bugs':>5} {'Total':>8}")
        print(" " + "-" * 65)
        for user, s in sorted(all_scores.items(), key=lambda x: x[1]["total"], reverse=True):
            print(f" @{user:<19} {s['prs_merged']:>5} {s['lines_changed']:>8} {s['reviews_given']:>8} {s['bugs_fixed']:>5} {s['total']:>8}")


if __name__ == "__main__":
    main()