import urllib.request
import json
import base64
import os
import time

TOKEN = "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"
OWNER = "EdwardWason"
REPO = "skill-publisher"
BASE_DIR = r"d:\TRAE SOLO CN\project\skill-publisher"

API_BASE = "https://api.github.com"

def api_request(method, url, data=None):
    """Make GitHub API request"""
    headers = {
        "Authorization": f"token {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "skill-publisher-script",
        "Accept": "application/vnd.github.v3+json"
    }
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = resp.read().decode("utf-8")
            return json.loads(resp_data) if resp_data else {}, resp.status
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"  HTTP Error {e.code}: {error_body[:300]}")
        return json.loads(error_body) if error_body else {}, e.code
    except Exception as e:
        print(f"  Request error: {e}")
        return {}, -1

def create_repo():
    """Step 1: Create repository"""
    print("=== Step 1: Creating repository ===")
    url = f"{API_BASE}/user/repos"
    data = {
        "name": REPO,
        "private": False,
        "description": "One-click publish and iterate skills to GitHub + ClawHub with security audit, change detection, auto version bump, and changelog generation.",
        "auto_init": False
    }
    result, status = api_request("POST", url, data)
    if status == 201:
        print(f"  Repository created: {result.get('html_url', 'OK')}")
    elif status == 422:
        print(f"  Repository already exists (422), continuing...")
    else:
        print(f"  Unexpected status {status}, continuing anyway...")
    return status

def upload_file(path, content_str):
    """Upload a single file to GitHub"""
    url = f"{API_BASE}/repos/{OWNER}/{REPO}/contents/{path}"
    content_b64 = base64.b64encode(content_str.encode("utf-8")).decode("ascii")
    data = {
        "message": f"feat: add {path}",
        "content": content_b64,
        "branch": "main"
    }
    result, status = api_request("PUT", url, data)
    if status in (200, 201):
        print(f"  OK: {path}")
        return True
    elif status == 422:
        # File might already exist, try to get sha and update
        print(f"  File exists, getting sha for {path}...")
        get_url = f"{API_BASE}/repos/{OWNER}/{REPO}/contents/{path}"
        existing, get_status = api_request("GET", get_url)
        if get_status == 200 and "sha" in existing:
            data["sha"] = existing["sha"]
            result2, status2 = api_request("PUT", url, data)
            if status2 in (200, 201):
                print(f"  Updated: {path}")
                return True
            else:
                print(f"  Failed to update {path}: status {status2}")
                return False
        else:
            print(f"  Could not get sha for {path}")
            return False
    else:
        print(f"  Failed: {path} (status {status})")
        return False

def read_local_file(rel_path):
    """Read a local file and return its content as string"""
    full_path = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()

def create_release():
    """Step 3: Create GitHub Release"""
    print("\n=== Step 3: Creating Release v4.0.0 ===")
    url = f"{API_BASE}/repos/{OWNER}/{REPO}/releases"
    body_text = """## Highlights

- Added Workflow B (iteration update) with change detection, auto version bump, and CHANGELOG generation.
- Added gh CLI integration as Method B in push fallback chain (git push → gh CLI → REST API).
- Added product landing page README with 21-chapter standard and smart adaptation by Skill complexity.
- Added bilingual independent files strategy (README.md + README.en.md).
- Added provenance block for skill source identification and traceability.
- Added community templates (bug_report, feature_request, question, config, pull_request_template).
- Expanded rules from 12 to 15 and steps from 13 to 25.

## Validation

- Security audit passed: no credentials, no local paths, no dangerous commands.
- Version sync verified: SKILL.md v4.0.0 = plugin.json v4.0.0 = CHANGELOG.md [4.0.0].
- Dogfooding: skill-publisher published using its own workflow."""

    data = {
        "tag_name": "v4.0.0",
        "target_commitish": "main",
        "name": "Skill Publisher v4.0.0 · Dual workflow with change detection and auto version bump",
        "body": body_text,
        "draft": False,
        "prerelease": False
    }
    result, status = api_request("POST", url, data)
    if status == 201:
        print(f"  Release created: {result.get('html_url', 'OK')}")
    else:
        print(f"  Release creation status: {status}")
    return status

def main():
    # Step 1: Create repo
    create_repo()
    time.sleep(1)

    # Step 2: Upload all files
    print("\n=== Step 2: Uploading files ===")
    files = [
        "SKILL.md",
        "README.md",
        "README.en.md",
        "CHANGELOG.md",
        "LICENSE",
        ".gitignore",
        ".claude-plugin/plugin.json",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/question.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/pull_request_template.md",
        "references/repo-structure.md",
        "references/security-audit.md",
        "references/publish-procedures.md",
        "references/change-detection.md",
        "references/changelog-generation.md",
    ]

    success_count = 0
    fail_count = 0
    for f in files:
        try:
            content = read_local_file(f)
            if upload_file(f, content):
                success_count += 1
            else:
                fail_count += 1
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"  ERROR reading {f}: {e}")
            fail_count += 1

    print(f"\n  Upload summary: {success_count} success, {fail_count} failed")

    # Step 3: Create release
    time.sleep(2)
    create_release()

    print("\n=== Done ===")

if __name__ == "__main__":
    main()
