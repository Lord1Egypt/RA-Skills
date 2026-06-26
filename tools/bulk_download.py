#!/usr/bin/env python3
"""
RA-Skills bulk content downloader v3.0 — FULL FOLDERS

Fetches the complete skill folder (SKILL.md + scripts, references, assets,
README, _meta.json, etc.) for every community skill and lays it down on disk so
the whole registry works fully offline.

Usage:
  python3 tools/bulk_download.py
  python3 tools/bulk_download.py --source clawhub --threads 16
  python3 tools/bulk_download.py --source skills_sh --limit 100 --dry-run
  python3 tools/bulk_download.py --source lobehub,browse_sh,gstack

Tokens (env vars):
  CLAWHUB_TOKEN  — ClawHub API auth (required for reliable ClawHub access).
  GITHUB_TOKEN   — GitHub API (5,000 req/hr vs 60). Needed for skills_sh/gstack.

A `.ra_complete` sentinel is written into each finished folder so re-runs resume
instead of re-downloading. It is git-ignored. Use --force to re-fetch anyway.

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
CLAWHUB_TOKEN = os.environ.get("CLAWHUB_TOKEN", "")
MARKER = ".ra_complete"

_print_lock = threading.Lock()
_stats = {"done": 0, "skip": 0, "err": 0, "files": 0}
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

def safe_relpath(relpath):
    """Sanitize an archive/repo-relative path: block traversal, cap each
    component at 80 chars (per project path-length rule), keep dots/dashes."""
    parts = []
    for p in str(relpath).replace("\\", "/").split("/"):
        p = p.strip()
        if p in ("", "."):
            continue
        if p == "..":
            return None
        p = re.sub(r"[^\w.\-]", "_", p)[:80]
        if p:
            parts.append(p)
    return "/".join(parts) if parts else None

def write_skill_files(out_dir, files):
    """Write {relpath: bytes|str} into out_dir and drop the completion marker."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    for rel, data in files.items():
        sr = safe_relpath(rel)
        if not sr:
            continue
        dest = out_dir / sr
        dest.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        dest.write_bytes(data)
        written += 1
    (out_dir / MARKER).write_text("ok", encoding="utf-8")
    return written

def has_skill_md(files):
    return any(k.lower().split("/")[-1] == "skill.md" for k in files)

def gh_headers():
    h = {"User-Agent": "RA-Skills/3.0", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h

def http_get(url, headers=None, timeout=25, as_json=False, as_bytes=False):
    if headers is None:
        headers = {"User-Agent": "RA-Skills/3.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            if as_bytes:
                return data
            if as_json:
                return json.loads(data)
            return data.decode("utf-8", errors="replace")
    except urllib.error.HTTPError:
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# ClawHub — full folder via ZIP, meta description as SKILL.md fallback
# ---------------------------------------------------------------------------

def clawhub_headers():
    h = {"User-Agent": "Mozilla/5.0 (compatible; RA-Skills/3.0)"}
    if CLAWHUB_TOKEN:
        h["Authorization"] = f"Bearer {CLAWHUB_TOKEN}"
    return h

def clawhub_build_skill_md(meta):
    skill = meta.get("skill", meta)
    desc = (skill.get("description") or "").strip()
    if not desc:
        return None
    if desc.lstrip().startswith("---"):
        return desc + "\n"
    slug = skill.get("slug", "")
    name = skill.get("displayName") or slug
    summary = (skill.get("summary") or "").replace('"', "'").strip()
    tags = skill.get("tags") or []
    if isinstance(tags, dict):
        tags = [k for k in tags.keys() if k != "latest"]
    tags_str = ", ".join(str(t) for t in tags) if tags else ""
    lv = meta.get("latestVersion")
    version = lv.get("version") if isinstance(lv, dict) else ""
    return (
        f"---\nname: {slug}\ndescription: \"{summary}\"\n"
        f"source: ClawHub\nversion: {version}\ntags: [{tags_str}]\n"
        f"compatible: [claude-code, openai-agents, hermes-agent, any-llm]\n---\n\n"
        f"# {name}\n\n{desc}\n"
    )

def clawhub_fetch_files(slug):
    meta = http_get(f"{CLAWHUB_API}/skills/{urllib.parse.quote(slug)}",
                    headers=clawhub_headers(), as_json=True)
    files = {}
    version = None
    if isinstance(meta, dict):
        skill = meta.get("skill", meta)
        lv = meta.get("latestVersion") or skill.get("latestVersion")
        if isinstance(lv, dict):
            version = lv.get("version")
    if version:
        data = http_get(
            f"{CLAWHUB_API}/download?slug={urllib.parse.quote(slug)}"
            f"&version={urllib.parse.quote(str(version))}",
            headers=clawhub_headers(), timeout=60, as_bytes=True)
        if data:
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as zf:
                    for info in zf.infolist():
                        if info.is_dir():
                            continue
                        files[info.filename] = zf.read(info)
            except Exception:
                pass
    # Fallback / guarantee a SKILL.md from the meta description.
    if not has_skill_md(files) and isinstance(meta, dict):
        content = clawhub_build_skill_md(meta)
        if content:
            files["SKILL.md"] = content
    return files


# ---------------------------------------------------------------------------
# GitHub folder collection (skills_sh, gstack, browse_sh)
# ---------------------------------------------------------------------------

def github_list_dir(repo, path, timeout=20):
    url = f"{GITHUB_API}/repos/{repo}/contents/{urllib.parse.quote(path.rstrip('/'))}"
    data = http_get(url, headers=gh_headers(), timeout=timeout, as_json=True)
    return data if isinstance(data, list) else []

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
    dl = data.get("download_url")
    return http_get(dl, headers=gh_headers(), timeout=timeout) if dl else None

def collect_github_folder(repo, folder, root_base=None, items=None, depth=0):
    """Recursively download every file under `folder` (raw download_urls do not
    count against the API rate limit). Returns {relpath_under_root_base: bytes}."""
    if root_base is None:
        root_base = folder.rstrip("/")
    if depth > 8:
        return {}
    if items is None:
        items = github_list_dir(repo, folder)
    files = {}
    for it in items:
        t = it.get("type")
        full = it.get("path", "")
        rel = full[len(root_base):].lstrip("/")
        if t == "file":
            url = it.get("download_url")
            if not url:
                continue
            data = http_get(url, headers=gh_headers(), timeout=30, as_bytes=True)
            if data is not None:
                files[rel] = data
        elif t == "dir":
            files.update(collect_github_folder(repo, full, root_base, depth=depth + 1))
    return files

# Per-repo tree cache: skills.sh has ~20k skills across only ~2.5k repos, so we
# fetch each repo's full git tree ONCE (1 API call, recursive) and reuse it for
# every skill in that repo. Raw blob downloads don't count against the API
# limit, so this keeps us comfortably under 5,000 req/hr.
_repo_cache = {}
_repo_cache_lock = threading.Lock()

def get_repo_tree(repo):
    """Return (branch, blob_paths) for a repo, cached. blob_paths is None when
    the tree is truncated (too large) — caller should fall back to listing."""
    with _repo_cache_lock:
        if repo in _repo_cache:
            return _repo_cache[repo]
    result = None
    info = http_get(f"{GITHUB_API}/repos/{repo}", headers=gh_headers(), as_json=True)
    branch = info.get("default_branch") if isinstance(info, dict) else None
    if branch:
        tree = http_get(f"{GITHUB_API}/repos/{repo}/git/trees/{urllib.parse.quote(branch)}?recursive=1",
                        headers=gh_headers(), as_json=True, timeout=45)
        if isinstance(tree, dict) and isinstance(tree.get("tree"), list):
            if tree.get("truncated"):
                result = (branch, None)
            else:
                blobs = [t["path"] for t in tree["tree"] if t.get("type") == "blob"]
                result = (branch, blobs)
    with _repo_cache_lock:
        _repo_cache[repo] = result
    return result

def skills_sh_fetch_files(identifier):
    ident = re.sub(r"^skills[-_]sh/", "", identifier)
    parts = ident.split("/")
    if len(parts) < 3:
        return {}
    owner, repo_name = parts[0], parts[1]
    skill = "/".join(parts[2:]).strip("/")
    repo = f"{owner}/{repo_name}"

    info = get_repo_tree(repo)
    if info is None:
        return {}
    branch, blobs = info
    if blobs is None:
        return skills_sh_fetch_files_listing(repo, repo_name, skill)

    # Find the skill folder: prefer known layouts, then any */<skill-basename>/SKILL.md
    candidates = [
        f"skills/{skill}", f".agents/skills/{skill}", skill,
        f"plugins/{repo_name}-claude/skills/{skill}", f"src/{skill}", f"agents/{skill}",
    ]
    blobset = set(blobs)
    target = None
    for c in candidates:
        if f"{c}/SKILL.md" in blobset or f"{c}/skill.md" in blobset:
            target = c
            break
    if target is None:
        base = skill.split("/")[-1].lower()
        for b in blobs:
            low = b.lower()
            if low.endswith("/skill.md") and low.rsplit("/", 2)[-2] == base:
                target = b.rsplit("/", 1)[0]
                break
    if target is None:
        return {}

    files = {}
    prefix = target + "/"
    for b in blobs:
        if b.startswith(prefix):
            rel = b[len(prefix):]
            raw = f"https://raw.githubusercontent.com/{repo}/{urllib.parse.quote(branch)}/{urllib.parse.quote(b)}"
            data = http_get(raw, headers=gh_headers(), as_bytes=True, timeout=30)
            if data is not None:
                files[rel] = data
    return files

def skills_sh_fetch_files_listing(repo, repo_name, skill):
    """Fallback for truncated trees: list candidate folders directly."""
    candidates = [
        f"skills/{skill}", f".agents/skills/{skill}", skill,
        f"plugins/{repo_name}-claude/skills/{skill}", f"src/{skill}", f"agents/{skill}",
    ]
    for base in candidates:
        items = github_list_dir(repo, base)
        if items and any(it.get("name", "").lower() == "skill.md" for it in items):
            files = collect_github_folder(repo, base, root_base=base, items=items)
            if has_skill_md(files):
                return files
    return {}

def gstack_fetch_files(source_url):
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/tree/[^/]+/(.+)", source_url)
    if not m:
        return {}
    repo, path = m.group(1), m.group(2).rstrip("/")
    return collect_github_folder(repo, path, root_base=path)

def browse_sh_fetch_files(source_url):
    # Upstream repo browserbase/browse.sh was removed; try blob fetch anyway.
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/blob/[^/]+/(.+)", source_url)
    if not m:
        return {}
    repo, path = m.group(1), m.group(2)
    folder = path.rsplit("/", 1)[0]
    files = collect_github_folder(repo, folder, root_base=folder)
    if has_skill_md(files):
        return files
    content = github_get_file(repo, path)
    return {"SKILL.md": content} if content else {}


# ---------------------------------------------------------------------------
# LobeHub — single generated SKILL.md (no upstream folder)
# ---------------------------------------------------------------------------

def lobehub_fetch_files(identifier):
    agent_id = identifier.split("/")[-1]
    for fname in (f"{agent_id}.json", f"{agent_id}.zh-CN.json"):
        data = http_get(f"{LOBEHUB_RAW}/{fname}", as_json=True)
        if not isinstance(data, dict):
            continue
        cfg = data.get("config", {})
        meta = data.get("meta", {})
        system_role = (cfg.get("systemRole") or "").strip()
        if not system_role:
            continue
        title = meta.get("title", agent_id)
        desc = meta.get("description", "")
        tags = meta.get("tags", [])
        tags_str = ", ".join(tags) if tags else ""
        skill_md = (
            f"---\nname: {agent_id}\ndescription: \"{desc}\"\nsource: LobeHub\n"
            f"tags: [{tags_str}]\n"
            f"compatible: [claude-code, openai-agents, hermes-agent, any-llm]\n---\n\n"
            f"# {title}\n\n{system_role}\n"
        )
        return {"SKILL.md": skill_md, "_meta.json": json.dumps(data, ensure_ascii=False, indent=2)}
    return {}


# ---------------------------------------------------------------------------
# Process a single skill
# ---------------------------------------------------------------------------

FETCHERS = {
    "ClawHub":   lambda s: clawhub_fetch_files(s["identifier"].split("/")[-1]),
    "LobeHub":   lambda s: lobehub_fetch_files(s.get("identifier", "")),
    "gstack":    lambda s: gstack_fetch_files(s.get("sourceUrl", "")),
    "browse.sh": lambda s: browse_sh_fetch_files(s.get("sourceUrl", "")),
    "skills.sh": lambda s: skills_sh_fetch_files(s.get("identifier", "")),
}

# Per-source post-fetch delay multiplier (GitHub sources are gentler).
DELAY_MULT = {"ClawHub": 1.0, "LobeHub": 0.3, "gstack": 0.2, "browse.sh": 0.2, "skills.sh": 0.5}

def process_skill(skill, dry_run, delay, force):
    source = skill.get("source", "")
    identifier = skill.get("identifier", "")
    out_dir = skill_out_dir(source, identifier)
    marker = out_dir / MARKER

    if not force and marker.exists():
        with _stats_lock:
            _stats["skip"] += 1
        return "skip"

    fetcher = FETCHERS.get(source)
    if not fetcher:
        with _stats_lock:
            _stats["err"] += 1
        return "unknown_source"

    try:
        files = fetcher(skill)
        time.sleep(delay * DELAY_MULT.get(source, 1.0))
    except Exception as e:
        with _stats_lock:
            _stats["err"] += 1
        return f"error: {e}"

    if not files or not has_skill_md(files):
        with _stats_lock:
            _stats["err"] += 1
        return "no_content"

    if dry_run:
        with _stats_lock:
            _stats["done"] += 1
            _stats["files"] += len(files)
        return f"dry: {len(files)} files"

    try:
        n = write_skill_files(out_dir, files)
        with _stats_lock:
            _stats["done"] += 1
            _stats["files"] += n
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
        description="Bulk download FULL skill folders for all community skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--source", default="all",
                        help="all, or comma-separated: clawhub,skills_sh,lobehub,browse_sh,gstack")
    parser.add_argument("--limit", type=int, default=0, help="Max skills per source (0=all)")
    parser.add_argument("--threads", type=int, default=8, help="Concurrent workers (default 8)")
    parser.add_argument("--delay", type=float, default=0.1, help="Base per-skill delay in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")
    parser.add_argument("--force", action="store_true", help="Re-fetch even if marker exists")
    args = parser.parse_args()

    print("=== RA-Skills Bulk Downloader v3.0 (FULL FOLDERS) ===\n")
    print(f"GitHub token:  {'SET (5,000 req/hr)' if GITHUB_TOKEN else 'NOT SET (60 req/hr)'}")
    print(f"ClawHub token: {'SET' if CLAWHUB_TOKEN else 'NOT SET'}")

    print(f"Loading registry from {REGISTRY}...")
    with open(REGISTRY, encoding="utf-8") as f:
        data = json.load(f)
    skills_all = data.get("skills", data) if isinstance(data, dict) else data
    print(f"Total skills: {len(skills_all):,}\n")

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
    groups = {}
    for s in skills:
        groups.setdefault(s.get("source", ""), []).append(s)

    print("Processing plan:")
    for src_key, src_name in SOURCE_MAP.items():
        if src_name in groups:
            cnt = min(args.limit, len(groups[src_name])) if args.limit else len(groups[src_name])
            print(f"  {src_name:12s}: {cnt:6,} skills")
    print()
    if args.dry_run:
        print("DRY RUN — no files will be written\n")

    all_errors = []
    for src_name, src_skills in groups.items():
        if src_name not in target_sources:
            continue
        batch = src_skills[:args.limit] if args.limit else src_skills
        total_src = len(batch)
        print(f"--- {src_name} ({total_src:,} skills, {args.threads} workers) ---")
        start = time.time()
        errors_src = []

        with ThreadPoolExecutor(max_workers=args.threads) as ex:
            futures = {ex.submit(process_skill, sk, args.dry_run, args.delay, args.force): sk
                       for sk in batch}
            completed = 0
            for future in as_completed(futures):
                completed += 1
                sk = futures[future]
                result = future.result()
                if result.startswith("error") or result in ("no_content", "unknown_source") or result.startswith("write_error"):
                    errors_src.append(f"{sk.get('identifier','?')}: {result}")
                if completed % 200 == 0:
                    elapsed = time.time() - start
                    rate = completed / max(elapsed, 1)
                    eta = (total_src - completed) / rate / 60 if rate > 0 else 0
                    s = _stats
                    log(f"  [{completed:6,}/{total_src:,}] done={s['done']:,} skip={s['skip']:,} "
                        f"err={s['err']:,} files={s['files']:,} | {rate:.1f}/s eta={eta:.0f}m")

        print(f"  Finished {src_name} in {(time.time()-start)/60:.1f}m")
        all_errors.extend(errors_src)

    print(f"\n{'='*50}")
    print(f"DONE: {_stats['done']:,}  SKIPPED: {_stats['skip']:,}  "
          f"ERRORS: {_stats['err']:,}  FILES WRITTEN: {_stats['files']:,}")
    if all_errors:
        ERRORS_LOG.write_text("\n".join(all_errors) + "\n", encoding="utf-8")
        print(f"Error details → {ERRORS_LOG} ({len(all_errors):,} entries)")
    else:
        print("No errors!")


if __name__ == "__main__":
    main()
