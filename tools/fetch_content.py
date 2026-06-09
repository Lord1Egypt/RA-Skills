#!/usr/bin/env python3
import os
import json
import sys
import re
import urllib.request
import urllib.parse

HEADERS = {
    "User-Agent": "RA-Skills-Downloader/1.0",
    "Accept": "text/plain, application/json, */*",
}

def sanitize_name(name):
    sanitized = re.sub(r'[^\w\-]', '_', name).lower()
    return sanitized if sanitized else "unknown"

def get_partition_char(name):
    clean = re.sub(r'[^a-zA-Z0-9]', '', name)
    if clean:
        return clean[0].lower()
    return "_"

def fetch_url(url, as_json=False):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        content = r.read().decode("utf-8")
    if as_json:
        return json.loads(content)
    return content

def fetch_github_skill(url):
    # e.g., https://github.com/owner/repo/tree/main/path/to/skill
    # Convert to API request to see contents
    m = re.match(r'https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)', url)
    if not m:
        # Fallback: check if it is a simple repo
        m_simple = re.match(r'https://github\.com/([^/]+)/([^/]+)', url)
        if m_simple:
            owner, repo = m_simple.groups()
            url = f"https://api.github.com/repos/{owner}/{repo}/readme"
            try:
                readme_info = fetch_url(url, as_json=True)
                if readme_info.get("download_url"):
                    return fetch_url(readme_info["download_url"])
            except Exception:
                pass
        return None
        
    owner, repo, branch, path = m.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    try:
        files = fetch_url(api_url, as_json=True)
    except Exception as e:
        return f"Error fetching GitHub contents: {e}"
        
    if isinstance(files, list):
        for fname in ("SKILL.md", "skill.md", "README.md"):
            for f in files:
                if f.get("name") == fname and f.get("download_url"):
                    return fetch_url(f["download_url"])
        for f in files:
            if f.get("name", "").endswith(".md") and f.get("download_url"):
                return fetch_url(f["download_url"])
    elif isinstance(files, dict) and files.get("download_url"):
        return fetch_url(files["download_url"])
    return None

def fetch_skillssh_skill(url):
    raw_url = url.rstrip("/") + "/raw"
    try:
        return fetch_url(raw_url)
    except Exception:
        # Try raw.githubusercontent logic if they link a github repo in a way
        pass
    try:
        return fetch_url(url)
    except Exception as e:
        return f"Error fetching from skills.sh: {e}"

def fetch_lobehub_skill(identifier):
    # e.g., lobehub/agent-name
    parts = identifier.split("/")
    agent_id = parts[-1] if parts else identifier
    api_url = f"https://chat-agents.lobehub.com/agent/{agent_id}"
    try:
        data = fetch_url(api_url, as_json=True)
        system_role = data.get("config", {}).get("systemRole", "")
        name = data.get("meta", {}).get("title", agent_id)
        desc = data.get("meta", {}).get("description", "")
        return f"# {name}\n\n{desc}\n\n## System Role\n```\n{system_role}\n```"
    except Exception as e:
        return f"Error fetching from LobeHub API: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_content.py <skill-name-or-identifier>")
        sys.exit(1)
        
    query = sys.argv[1]
    
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(tools_dir)
    registry_path = os.path.join(root_dir, "registry.json")
    
    with open(registry_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    skills = data.get("skills", [])
    
    target = None
    for s in skills:
        if s.get("name", "").lower() == query.lower() or s.get("identifier", "").lower() == query.lower():
            target = s
            break
            
    if not target:
        print(f"Skill '{query}' not found in registry.")
        sys.exit(1)
        
    source = target.get("source", "")
    source_url = target.get("sourceUrl", "")
    identifier = target.get("identifier", "")
    name = target.get("name", "")
    
    print(f"Found skill: {name} ({source})")
    if source in ("built-in", "optional"):
        print("This skill is already fully available in the local repository.")
        sys.exit(0)
        
    if not source_url and source != "LobeHub":
        print("Error: No sourceUrl specified for this skill.")
        sys.exit(1)
        
    print(f"Fetching from {source_url or 'LobeHub API'}...")
    content = None
    try:
        if source == "skills.sh":
            content = fetch_skillssh_skill(source_url)
        elif source == "LobeHub":
            content = fetch_lobehub_skill(identifier)
        elif source == "gstack" or "github.com" in source_url:
            content = fetch_github_skill(source_url)
        elif source == "ClawHub":
            print(f"Notice: ClawHub skills usually require browser access. URL: {source_url}")
            print("Attempting static fetch...")
            try:
                content = fetch_url(source_url)
            except Exception as e:
                print(f"Static fetch failed: {e}. Please open in a browser: {source_url}")
                sys.exit(1)
        else:
            # General fallback
            if "github.com" in source_url:
                content = fetch_github_skill(source_url)
            else:
                content = fetch_url(source_url)
    except Exception as e:
        print(f"Failed to fetch content: {e}")
        sys.exit(1)
        
    if not content:
        print("No content could be retrieved.")
        sys.exit(1)
        
    # Save content to the skill folder (using the matching max 80 char length limit)
    clean_source = sanitize_name(source)[:50]
    first_char = get_partition_char(identifier)
    clean_id = sanitize_name(identifier)[:80]
    
    skill_dir = os.path.join(root_dir, "skills", "community", clean_source, first_char, clean_id)
    os.makedirs(skill_dir, exist_ok=True)
    
    content_file = os.path.join(skill_dir, "CONTENT.md")
    with open(content_file, "w", encoding="utf-8") as cf:
        cf.write(content)
        
    print(f"Successfully downloaded and saved content to:")
    print(f"  {content_file}")

if __name__ == "__main__":
    main()
