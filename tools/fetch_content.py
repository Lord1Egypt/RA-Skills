#!/usr/bin/env python3
"""
On-demand skill content fetcher for RA-Skills.

Usage:
  python3 tools/fetch_content.py <skill-name-or-identifier>
  python3 tools/fetch_content.py aso-playbook
  python3 tools/fetch_content.py "skills-sh/sickn33/antigravity-awesome-skills/00-andruia-consultant"
  python3 tools/fetch_content.py "lobehub/9-somboon"

Set GITHUB_TOKEN env var for higher GitHub API rate limits.
"""
import os, json, sys, re, io, zipfile, base64, urllib.request, urllib.parse, urllib.error

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
CLAWHUB_API = "https://clawhub.ai/api/v1"
LOBEHUB_RAW = "https://raw.githubusercontent.com/lobehub/lobe-chat-agents/main/src"
GITHUB_API = "https://api.github.com"

def gh_headers():
    h = {"User-Agent": "RA-Skills/2.0", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h

def sanitize(name, maxlen=80):
    s = re.sub(r"[^\w\-]", "_", name).lower()
    return (s or "unknown")[:maxlen]

def partition_char(name):
    clean = re.sub(r"[^a-zA-Z0-9]", "", name)
    return clean[0].lower() if clean else "_"

def source_slug(source):
    return re.sub(r"[^\w]", "_", source).lower()

def http_get(url, headers=None, timeout=20, as_json=False, as_bytes=False):
    if headers is None:
        headers = {"User-Agent": "RA-Skills/2.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            if as_bytes:
                return data
            if as_json:
                return json.loads(data)
            return data.decode("utf-8", errors="replace")
    except Exception:
        return None

def github_get_file(repo, path, timeout=20):
    url = f"{GITHUB_API}/repos/{repo}/contents/{urllib.parse.quote(path)}"
    data = http_get(url, headers=gh_headers(), timeout=timeout, as_json=True)
    if not isinstance(data, dict):
        return None
    if data.get("encoding") == "base64" and data.get("content"):
        try:
            return base64.b64decode(data["content"].replace("\n", "")).decode("utf-8", errors="replace")
        except Exception:
            return None
    dl_url = data.get("download_url")
    if dl_url:
        return http_get(dl_url, headers=gh_headers())
    return None

def fetch_clawhub(slug):
    print(f"Fetching ClawHub metadata for '{slug}'...")
    meta = http_get(f"{CLAWHUB_API}/skills/{slug}",
                    headers={"User-Agent": "Mozilla/5.0"}, as_json=True)
    if not isinstance(meta, dict):
        print("Error: Could not reach ClawHub API.")
        return None
    skill = meta.get("skill", meta)
    lv = meta.get("latestVersion") or skill.get("latestVersion")
    version = None
    if isinstance(lv, dict):
        version = lv.get("version")
    if not version:
        tags = skill.get("tags", {})
        version = tags.get("latest") if isinstance(tags, dict) else None
    if not version:
        print("Error: Could not determine version.")
        return None
    print(f"Downloading ZIP (slug={slug}, version={version})...")
    data = http_get(
        f"{CLAWHUB_API}/download?slug={slug}&version={urllib.parse.quote(str(version))}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=40,
        as_bytes=True,
    )
    if not data:
        print("Error: Download failed.")
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            print(f"ZIP contains: {zf.namelist()}")
            for candidate in ("SKILL.md", "skill.md"):
                if candidate in zf.namelist():
                    return zf.read(candidate).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error extracting ZIP: {e}")
    return None

def fetch_lobehub(identifier):
    agent_id = identifier.split("/")[-1]
    print(f"Fetching LobeHub agent '{agent_id}' from GitHub...")
    for fname in (f"{agent_id}.json",):
        data = http_get(f"{LOBEHUB_RAW}/{fname}", as_json=True)
        if not isinstance(data, dict):
            continue
        cfg = data.get("config", {})
        meta_l = data.get("meta", {})
        system_role = cfg.get("systemRole", "").strip()
        if not system_role:
            continue
        title = meta_l.get("title", agent_id)
        desc = meta_l.get("description", "")
        tags = meta_l.get("tags", [])
        return (
            f"---\nname: {agent_id}\ndescription: \"{desc}\"\n"
            f"source: LobeHub\ntags: [{', '.join(tags)}]\n"
            f"compatible: [claude-code, openai-agents, hermes-agent, any-llm]\n---\n\n"
            f"# {title}\n\n{system_role}\n"
        )
    print("Error: Could not fetch from LobeHub GitHub.")
    return None

def fetch_github_tree(source_url):
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/tree/[^/]+/(.+)", source_url)
    if not m:
        return None
    repo, path = m.group(1), m.group(2).rstrip("/")
    print(f"Fetching GitHub tree: {repo}/{path}...")
    return github_get_file(repo, f"{path}/SKILL.md")

def fetch_github_blob(source_url):
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/blob/[^/]+/(.+)", source_url)
    if not m:
        return None
    repo, path = m.group(1), m.group(2)
    print(f"Fetching GitHub blob: {repo}/{path}...")
    return github_get_file(repo, path)

def fetch_skills_sh(identifier):
    ident = re.sub(r"^skills[-_]sh/", "", identifier)
    parts = ident.split("/")
    if len(parts) < 3:
        return None
    repo = f"{parts[0]}/{parts[1]}"
    skill = "/".join(parts[2:])
    print(f"Fetching skills.sh skill '{skill}' from GitHub repo '{repo}'...")
    candidates = [
        f"skills/{skill}/SKILL.md",
        f".agents/skills/{skill}/SKILL.md",
        f"{skill}/SKILL.md",
        f"plugins/{parts[1]}-claude/skills/{skill}/SKILL.md",
        f"src/{skill}/SKILL.md",
    ]
    for path in candidates:
        print(f"  Trying: {path}")
        content = github_get_file(repo, path)
        if content and len(content) > 80:
            print(f"  Found at: {path}")
            return content
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_content.py <skill-name-or-identifier>")
        sys.exit(1)

    query = sys.argv[1]
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(tools_dir)
    registry_path = os.path.join(root_dir, "registry.json")

    with open(registry_path, encoding="utf-8") as f:
        data = json.load(f)
    skills = data.get("skills", data) if isinstance(data, dict) else data

    target = None
    for s in skills:
        if s.get("name", "").lower() == query.lower() or s.get("identifier", "").lower() == query.lower():
            target = s
            break
    if not target:
        # Partial match fallback
        for s in skills:
            if query.lower() in s.get("name", "").lower() or query.lower() in s.get("identifier", "").lower():
                target = s
                break
    if not target:
        print(f"Skill '{query}' not found in registry.")
        sys.exit(1)

    source = target.get("source", "")
    identifier = target.get("identifier", "")
    source_url = target.get("sourceUrl", "")
    name = target.get("name", "")

    print(f"\nSkill: {name}")
    print(f"Source: {source}")
    print(f"Identifier: {identifier}")
    print(f"URL: {source_url}\n")

    if source in ("built-in", "optional"):
        print("This skill already has full local content (built-in/optional).")
        sys.exit(0)

    content = None
    if source == "ClawHub":
        slug = identifier.split("/")[-1]
        content = fetch_clawhub(slug)
    elif source == "LobeHub":
        content = fetch_lobehub(identifier)
    elif source == "gstack" or ("github.com" in source_url and "/tree/" in source_url):
        content = fetch_github_tree(source_url)
    elif source == "browse.sh" or ("github.com" in source_url and "/blob/" in source_url):
        content = fetch_github_blob(source_url)
    elif source == "skills.sh":
        content = fetch_skills_sh(identifier)
    else:
        print(f"Unknown source: {source}")
        sys.exit(1)

    if not content:
        print("\nError: Could not retrieve content.")
        sys.exit(1)

    # Determine output path (matches bulk_download.py structure)
    slug_src = source_slug(source)
    san = sanitize(identifier)
    first = partition_char(san)
    out_dir = os.path.join(root_dir, "skills", "community", slug_src, first, san)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "SKILL.md")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nSaved {len(content):,} bytes to:")
    print(f"  {out_file}")

if __name__ == "__main__":
    main()
