#!/usr/bin/env python3
"""
RA-Skills bulk content downloader v2.0

Fetches actual SKILL.md content for all 90k+ community skills.
Replaces stub metadata files with real skill content.

Usage:
  python3 tools/bulk_download.py
  python3 tools/bulk_download.py --source clawhub --threads 8
  python3 tools/bulk_download.py --source skills_sh --limit 100 --dry-run
  python3 tools/bulk_download.py --source lobehub,browse_sh,gstack

Set GITHUB_TOKEN env var for higher GitHub API rate limits (5000/hr vs 60/hr).

Sources: clawhub (69842), skills_sh (19938), lobehub (505), browse_sh (389), gstack (52)
"""

import os, json, sys, re, time, io, zipfile, base64, argparse, threading
import urllib.request, urllib.parse, urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).parent.parent
REGISTRY = ROOT / "registry.json"
COMMUNITY = ROOT / "skills" / "community"
ERRORS_LOG = ROOT / "tools" / "download_errors.log"

CLAWHUB_API = "https://clawhub.ai/api/v1"
LOBEHUB_RAW = "https://raw.githubusercontent.com/lobehub/lobe-chat-agents/main/src"
GITHUB_API = "https://api.github.com"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
_print_lock = threading.Lock()
_stats = {"done": 0, "skip": 0, "err": 0}
_stats_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg):
    with _print_lock:
        print(msg, flush=True)

def sanitize(name, maxlen=80):
    s = re.sub(r"[^\w\-]", "_", name).lower()
    return (s or "unknown")[:maxlen]

def partition_char(name):
    clean = re.sub(r"[^a-zA-Z0-9]", "", name)
    return clean[0].lower() if clean else "_"

def source_slug(source):
    return re.sub(r"[^\w]", "_", source).lower()

def skill_out_dir(src, identifier):
    slug = source_slug(src)
    san = sanitize(identifier)
    first = partition_char(san)
    return COMMUNITY / slug / first / san

def is_stub(path):
    """True if SKILL.md has no real content — just our generated metadata stub."""
    if not path.exists():
        return True
    content = path.read_text(encoding="utf-8", errors="ignore")
    if "- **Category:**" in content and "- **Source:**" in content:
        return True
    body = re.sub(r"^---.*?---", "", content, flags=re.DOTALL).strip()
    return len(body) < 100

def gh_headers():
    h = {"User-Agent": "RA-Skills/2.0", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h

def http_get(url, headers=None, timeout=25, as_json=False, as_bytes=False):
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
    except urllib.error.HTTPError as e:
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# ClawHub
# ---------------------------------------------------------------------------

def clawhub_get_version(slug):
    data = http_get(f"{CLAWHUB_API}/skills/{slug}",
                    headers={"User-Agent": "Mozilla/5.0 (compatible)"}, as_json=True)
    if not isinstance(data, dict):
        return None
    skill = data.get("skill", data)
    lv = data.get("latestVersion") or skill.get("latestVersion")
    if isinstance(lv, dict):
        v = lv.get("version")
        if v:
            return str(v)
    tags = skill.get("tags", {})
    if isinstance(tags, dict):
        latest = tags.get("latest")
        if latest:
            return str(latest)
    return None

def clawhub_fetch(slug):
    version = clawhub_get_version(slug)
    if not version:
        return None
    data = http_get(
        f"{CLAWHUB_API}/download?slug={slug}&version={urllib.parse.quote(version)}",
        headers={"User-Agent": "Mozilla/5.0 (compatible)"},
        timeout=40,
        as_bytes=True,
    )
    if not data:
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            names = zf.namelist()
            for candidate in ("SKILL.md", "skill.md"):
                if candidate in names:
                    return zf.read(candidate).decode("utf-8", errors="replace")
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# LobeHub (uses GitHub raw JSON files)
# ---------------------------------------------------------------------------

def lobehub_fetch(identifier):
    agent_id = identifier.split("/")[-1]
    # Remove locale suffix for zh-CN etc. (prefer the base file)
    for fname in (f"{agent_id}.json", f"{agent_id}.zh-CN.json"):
        data = http_get(f"{LOBEHUB_RAW}/{fname}", as_json=True)
        if not isinstance(data, dict):
            continue
        cfg = data.get("config", {})
        meta = data.get("meta", {})
        system_role = cfg.get("systemRole", "").strip()
        if not system_role:
            continue
        title = meta.get("title", agent_id)
        desc = meta.get("description", "")
        tags = meta.get("tags", [])
        tags_str = ", ".join(tags) if tags else ""
        return (
            f"---\n"
            f"name: {agent_id}\n"
            f'description: "{desc}"\n'
            f"source: LobeHub\n"
            f"tags: [{tags_str}]\n"
            f"compatible: [claude-code, openai-agents, hermes-agent, any-llm]\n"
            f"---\n\n"
            f"# {title}\n\n"
            f"{system_role}\n"
        )
    return None


# ---------------------------------------------------------------------------
# GitHub helpers (gstack, browse.sh, skills.sh)
# ---------------------------------------------------------------------------

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
        return http_get(dl_url, headers=gh_headers(), timeout=timeout)
    return None

def github_list_dir(repo, path, timeout=15):
    url = f"{GITHUB_API}/repos/{repo}/contents/{urllib.parse.quote(path.rstrip('/'))}"
    data = http_get(url, headers=gh_headers(), timeout=timeout, as_json=True)
    return data if isinstance(data, list) else []

def gstack_fetch(source_url):
    # https://github.com/garrytan/gstack/tree/main/autoplan
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/tree/[^/]+/(.+)", source_url)
    if not m:
        return None
    repo, path = m.group(1), m.group(2).rstrip("/")
    return github_get_file(repo, f"{path}/SKILL.md")

def browse_sh_fetch(source_url):
    # https://github.com/browserbase/browse.sh/blob/main/skills/.../SKILL.md
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/blob/[^/]+/(.+)", source_url)
    if not m:
        return None
    repo, path = m.group(1), m.group(2)
    return github_get_file(repo, path)

def skills_sh_fetch(identifier):
    # identifier: skills-sh/<owner>/<repo>/<skill>
    # Strip leading prefix variants
    ident = re.sub(r"^skills[-_]sh/", "", identifier)
    parts = ident.split("/")
    if len(parts) < 3:
        return None
    owner = parts[0]
    repo_name = parts[1]
    skill = "/".join(parts[2:])
    repo = f"{owner}/{repo_name}"

    # Try candidate paths in priority order
    candidates = [
        f"skills/{skill}/SKILL.md",
        f".agents/skills/{skill}/SKILL.md",
        f"{skill}/SKILL.md",
        f"plugins/{repo_name}-claude/skills/{skill}/SKILL.md",
        f"src/{skill}/SKILL.md",
        f"agents/{skill}/SKILL.md",
    ]
    for path in candidates:
        content = github_get_file(repo, path)
        if content and len(content) > 80 and ("---" in content or "#" in content):
            return content
    return None


# ---------------------------------------------------------------------------
# Process a single skill
# ---------------------------------------------------------------------------

def process_skill(skill, dry_run, delay, force):
    source = skill.get("source", "")
    identifier = skill.get("identifier", "")
    source_url = skill.get("sourceUrl", "")

    out_dir = skill_out_dir(source, identifier)
    out_file = out_dir / "SKILL.md"

    if not force and not is_stub(out_file):
        with _stats_lock:
            _stats["skip"] += 1
        return "skip"

    content = None
    try:
        if source == "ClawHub":
            slug = identifier.split("/")[-1]
            content = clawhub_fetch(slug)
            time.sleep(delay)
        elif source == "LobeHub":
            content = lobehub_fetch(identifier)
            time.sleep(delay * 0.3)
        elif source == "gstack":
            content = gstack_fetch(source_url)
            time.sleep(delay * 0.2)
        elif source == "browse.sh":
            content = browse_sh_fetch(source_url)
            time.sleep(delay * 0.2)
        elif source == "skills.sh":
            content = skills_sh_fetch(identifier)
            time.sleep(delay * 0.5)
    except Exception as e:
        with _stats_lock:
            _stats["err"] += 1
        return f"error: {e}"

    if not content or len(content.strip()) < 50:
        with _stats_lock:
            _stats["err"] += 1
        return "no_content"

    if dry_run:
        with _stats_lock:
            _stats["done"] += 1
        return f"dry: {len(content)}b"

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")
        with _stats_lock:
            _stats["done"] += 1
        return "ok"
    except Exception as e:
        with _stats_lock:
            _stats["err"] += 1
        return f"write_error: {e}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SOURCE_MAP = {
    "clawhub":   "ClawHub",
    "skills_sh": "skills.sh",
    "lobehub":   "LobeHub",
    "browse_sh": "browse.sh",
    "gstack":    "gstack",
}

def main():
    parser = argparse.ArgumentParser(
        description="Bulk download SKILL.md content for all community skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--source", default="all",
        help="Sources to process: all, or comma-separated from: clawhub,skills_sh,lobehub,browse_sh,gstack",
    )
    parser.add_argument("--limit", type=int, default=0, help="Max skills per source (0=all)")
    parser.add_argument("--threads", type=int, default=4, help="Concurrent workers (default 4)")
    parser.add_argument("--delay", type=float, default=0.3, help="Base request delay in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")
    parser.add_argument("--force", action="store_true", help="Re-download even if content exists")
    args = parser.parse_args()

    print(f"=== RA-Skills Bulk Downloader v2.0 ===\n")
    if GITHUB_TOKEN:
        print(f"GitHub token: SET  (5,000 req/hr)")
    else:
        print(f"GitHub token: NOT SET  (60 req/hr — set GITHUB_TOKEN for much faster processing)")

    # Load registry
    print(f"Loading registry from {REGISTRY}...")
    with open(REGISTRY, encoding="utf-8") as f:
        data = json.load(f)
    skills_all = data.get("skills", data) if isinstance(data, dict) else data
    print(f"Total skills: {len(skills_all):,}\n")

    # Determine which sources to process
    if args.source == "all":
        target_sources = set(SOURCE_MAP.values())
    else:
        target_sources = set()
        for key in args.source.split(","):
            key = key.strip()
            if key in SOURCE_MAP:
                target_sources.add(SOURCE_MAP[key])
            else:
                print(f"Unknown source: {key}. Valid: {', '.join(SOURCE_MAP)}")
                sys.exit(1)

    skills = [s for s in skills_all if s.get("source") in target_sources]

    # Group by source for ordered processing
    groups = {}
    for s in skills:
        src = s.get("source", "")
        groups.setdefault(src, []).append(s)

    # Print plan
    print("Processing plan:")
    for src_key, src_name in SOURCE_MAP.items():
        if src_name in groups:
            cnt = min(args.limit, len(groups[src_name])) if args.limit else len(groups[src_name])
            print(f"  {src_name:12s}: {cnt:6,} skills")
    print()

    if args.dry_run:
        print("DRY RUN — no files will be written\n")

    all_errors = []

    # Process each source group
    for src_name, src_skills in groups.items():
        if src_name not in target_sources:
            continue
        batch = src_skills[:args.limit] if args.limit else src_skills
        total_src = len(batch)
        print(f"--- {src_name} ({total_src:,} skills, {args.threads} workers) ---")

        start = time.time()
        errors_src = []

        if args.threads <= 1 or src_name in ("skills.sh",) and not GITHUB_TOKEN:
            # Single-threaded for GitHub-heavy sources without token
            for i, skill in enumerate(batch):
                result = process_skill(skill, args.dry_run, args.delay, args.force)
                if i % 200 == 0:
                    elapsed = time.time() - start
                    rate = (i + 1) / max(elapsed, 1)
                    eta = (total_src - i) / rate / 60 if rate > 0 else 0
                    s = _stats
                    log(f"  [{i:6,}/{total_src:,}] done={s['done']:,} skip={s['skip']:,} err={s['err']:,} | {rate:.1f}/s eta={eta:.0f}m")
                if result.startswith("error") or result == "no_content":
                    errors_src.append(f"{skill.get('identifier','?')}: {result}")
        else:
            with ThreadPoolExecutor(max_workers=args.threads) as ex:
                futures = {ex.submit(process_skill, skill, args.dry_run, args.delay, args.force): skill
                           for skill in batch}
                completed = 0
                for future in as_completed(futures):
                    completed += 1
                    skill = futures[future]
                    result = future.result()
                    if result.startswith("error") or result == "no_content":
                        errors_src.append(f"{skill.get('identifier','?')}: {result}")
                    if completed % 200 == 0:
                        elapsed = time.time() - start
                        rate = completed / max(elapsed, 1)
                        eta = (total_src - completed) / rate / 60 if rate > 0 else 0
                        s = _stats
                        log(f"  [{completed:6,}/{total_src:,}] done={s['done']:,} skip={s['skip']:,} err={s['err']:,} | {rate:.1f}/s eta={eta:.0f}m")

        elapsed = time.time() - start
        print(f"  Finished {src_name} in {elapsed/60:.1f}m")
        all_errors.extend(errors_src)

    # Final summary
    print(f"\n{'='*50}")
    print(f"DONE: {_stats['done']:,}  SKIPPED: {_stats['skip']:,}  ERRORS: {_stats['err']:,}")
    if all_errors:
        ERRORS_LOG.write_text("\n".join(all_errors) + "\n", encoding="utf-8")
        print(f"Error details → {ERRORS_LOG}")
    else:
        print("No errors!")


if __name__ == "__main__":
    main()
