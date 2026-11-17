#!/usr/bin/env python3
"""manage_skill.py - install/list/keep/uninstall for video-skill-router.

Usage:
    python manage_skill.py install --repo <owner/name> [--subdir <path>] [--all-skills] --reason "..."
    python manage_skill.py install --source <git-url|zip-url|local-path> --reason "..."
    python manage_skill.py list
    python manage_skill.py keep --name <skill-dir-name>
    python manage_skill.py uninstall --name <skill-dir-name>
    python manage_skill.py uninstall --batch <batch-id>

Safety rules (from install-protocol.md):
- snapshot before install (git commit, or state/.snapshots listing for non-git envs)
- frontmatter must contain name and description; SKILL.md over 500KB rejected
- suspicious content (credential reads, data exfil, destructive code, eval) rejected
- uninstall only touches manifest-registered skills; never rm -rf
  (git rm in git envs, otherwise move to state/.trash/<ts>/ - soft delete, restorable)
Standard library only.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

SKILLS_DIR = os.path.join(os.path.expanduser("~"), ".workbuddy", "skills")
STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "state")
MANIFEST = os.path.join(STATE_DIR, "manifest.json")
SNAPSHOT_DIR = os.path.join(STATE_DIR, ".snapshots")
TRASH_DIR = os.path.join(STATE_DIR, ".trash")
MAX_SKILL_MD_BYTES = 500 * 1024
MAX_BATCH_INSTALL = 5

# path parts that mark a SKILL.md as test/example fixture, not a real skill
EXCLUDE_PARTS = {
    "node_modules", ".git", "__pycache__", "test", "tests", "testing",
    "fixtures", "fixture", "examples", "example", "dist", "build", ".venv",
}

SUSPICIOUS_PATTERNS = [
    (r"cookies?\.json", "reads cookie files"),
    (r"session_api\.json", "reads session credentials"),
    (r"login_token", "reads login tokens"),
    (r"requests?\.post\(['\"]https?://(?!127|localhost)", "posts data to external host"),
    (r"shutil\.rmtree", "destructive rmtree without confirmation"),
    (r"rm\s+-rf", "rm -rf without confirmation"),
    (r"\beval\(", "dynamic eval execution"),
]


def clean_env():
    """Git/urllib env with dead proxy ports stripped (direct connection)."""
    env = dict(os.environ)
    for key in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
        env.pop(key, None)
    env["no_proxy"] = "*"
    env["NO_PROXY"] = "*"
    return env


def proxy_env():
    """Fallback env routing git through the local 7897 proxy."""
    env = dict(os.environ)
    env["HTTP_PROXY"] = "http://127.0.0.1:7897"
    env["HTTPS_PROXY"] = "http://127.0.0.1:7897"
    env["http_proxy"] = "http://127.0.0.1:7897"
    env["https_proxy"] = "http://127.0.0.1:7897"
    for key in ["no_proxy", "NO_PROXY"]:
        env.pop(key, None)
    return env


def clone_repo(url, workdir):
    """Clone with channel fallback: direct first, then 7897 proxy.
    (This machine's direct route to github.com dies intermittently while
    api.github.com stays reachable - see sources.md section 2.)"""
    attempts = [("direct", clean_env()), ("proxy-7897", proxy_env())]
    errors = []
    for i, (label, env) in enumerate(attempts):
        target = os.path.join(workdir, "clone" if i == 0 else "clone-retry")
        res = subprocess.run(
            ["git", "clone", "--depth", "1", url, target],
            capture_output=True, text=True, encoding="utf-8", errors="ignore",
            env=env,
        )
        if res.returncode == 0:
            if label != "direct":
                print("clone channel: %s (direct failed)" % label)
            return target
        errors.append("%s: %s" % (label, res.stderr.strip()[:150]))
    raise SystemExit("clone failed on all channels:\n  " + "\n  ".join(errors))


def run_git(args, cwd=SKILLS_DIR):
    return subprocess.run(
        ["git"] + args, cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="ignore", env=clean_env(),
    )


def is_git_repo():
    return os.path.isdir(os.path.join(SKILLS_DIR, ".git"))


def git_tracked(name):
    res = run_git(["ls-files", "--error-unmatch", name])
    return res.returncode == 0


def snapshot():
    """Pre-install restore point. Returns a snapshot descriptor string."""
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    if is_git_repo():
        run_git(["add", "-A"])
        run_git(["commit", "-m", "video-router: pre-install snapshot", "--quiet"])
        out = run_git(["rev-parse", "--short", "HEAD"])
        return "git:%s" % (out.stdout.strip() or "unknown")
    # non-git env (typical end user): record a listing under state/.snapshots
    snap = os.path.join(SNAPSHOT_DIR, ts)
    os.makedirs(snap, exist_ok=True)
    listing = []
    if os.path.isdir(SKILLS_DIR):
        for name in sorted(os.listdir(SKILLS_DIR)):
            path = os.path.join(SKILLS_DIR, name)
            if os.path.isdir(path):
                listing.append({"name": name, "type": "dir"})
            else:
                listing.append({"name": name, "type": "file"})
    with open(os.path.join(snap, "listing.json"), "w", encoding="utf-8") as fh:
        json.dump({"created": ts, "entries": listing}, fh, ensure_ascii=False, indent=1)
    return "dir-listing:%s" % ts


def load_manifest():
    if os.path.isfile(MANIFEST):
        with open(MANIFEST, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"installs": []}


def save_manifest(data):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def fetch_source(source, workdir):
    """Local dir / zip URL / git URL -> dir containing the skill source."""
    if os.path.isdir(source):
        return source
    if source.endswith(".zip"):
        zip_path = os.path.join(workdir, "src.zip")
        urllib.request.urlretrieve(source, zip_path)
        extract_dir = os.path.join(workdir, "src")
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)
        return extract_dir
    return clone_repo(source, workdir)


def is_excluded_path(path):
    parts = path.replace("\\", "/").split("/")
    return any(p in EXCLUDE_PARTS for p in parts)


def find_skill_roots(src):
    """All dirs containing SKILL.md. Returns (real_roots, suspicious_roots)."""
    real, suspicious = [], []
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__"}]
        if "SKILL.md" in files:
            rel = os.path.relpath(root, src).replace("\\", "/")
            if is_excluded_path(rel):
                suspicious.append(rel)
            else:
                real.append(rel)
    return sorted(real), sorted(suspicious)


def read_frontmatter_text(skill_root):
    with open(os.path.join(skill_root, "SKILL.md"), "r", encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def get_name(skill_root):
    m = re.search(r"^name:\s*(.+)$", read_frontmatter_text(skill_root)[:3000], re.M)
    return m.group(1).strip().strip("'\"") if m else os.path.basename(skill_root)


def get_description(skill_root):
    """Extract description from frontmatter, handling block scalars (| >) and quotes."""
    text = read_frontmatter_text(skill_root)
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    lines = m.group(1).splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("description:"):
            val = line.split(":", 1)[1].strip()
            if val in ("|", ">", "|-", ">-", "|+", ">+", ""):
                block = []
                for cont in lines[i + 1:]:
                    if cont.strip() and (cont.startswith(" ") or cont.startswith("\t")):
                        block.append(cont.strip())
                    else:
                        break
                return " ".join(block)[:300]
            return val.strip("'\"")[:300]
    return ""


def validate(skill_root):
    problems = []
    skill_md = os.path.join(skill_root, "SKILL.md")
    if not os.path.isfile(skill_md):
        return ["no SKILL.md found"]
    size = os.path.getsize(skill_md)
    if size > MAX_SKILL_MD_BYTES:
        problems.append("SKILL.md too large: %d bytes" % size)
    text = read_frontmatter_text(skill_root)
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        problems.append("no YAML frontmatter")
    else:
        fm = m.group(1)
        if "name:" not in fm:
            problems.append("frontmatter missing name")
        if "description:" not in fm:
            problems.append("frontmatter missing description")
    for pattern, label in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text, re.I):
            problems.append("suspicious content: %s" % label)
    return problems


def install_one(skill_root, batch_id, source_label, reason, snap):
    """Validate + copy a single skill dir into SKILLS_DIR. Returns record or raises."""
    problems = validate(skill_root)
    if problems:
        raise SystemExit("install REJECTED for %s:\n  - %s" % (skill_root, "\n  - ".join(problems)))
    name = get_name(skill_root)
    target = os.path.join(SKILLS_DIR, name)
    suffix = 2
    while os.path.exists(target):
        target = os.path.join(SKILLS_DIR, "%s-%d" % (name, suffix))
        suffix += 1
    # never carry upstream VCS metadata into the skills dir: a copied .git
    # turns the skill into a gitlink (submodule) and breaks git rm uninstall
    shutil.copytree(
        skill_root, target,
        ignore=shutil.ignore_patterns(".git", ".gitmodules", ".github"),
    )
    installed_name = os.path.basename(target)
    if is_git_repo():
        run_git(["add", installed_name])
        run_git(["commit", "-m", "video-router: install %s (%s)" % (installed_name, reason), "--quiet"])
    return {
        "batch_id": batch_id,
        "skill": installed_name,
        "source": source_label,
        "repo": None,
        "subdir": None,
        "reason": reason,
        "description": get_description(skill_root),
        "installed_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "git_snapshot": snap,
        "status": "active",
    }


def cmd_install(args):
    reason_slug = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", args.reason)[:12] or "install"
    batch_id = datetime.datetime.now().strftime("%Y%m%dT%H%M") + "_" + reason_slug
    snap = snapshot()
    print("snapshot: %s" % snap)

    if args.repo:
        source_label = "https://github.com/%s.git" % args.repo
    else:
        source_label = args.source

    with tempfile.TemporaryDirectory() as workdir:
        src = fetch_source(source_label, workdir)
        real_roots, suspicious_roots = find_skill_roots(src)
        if not real_roots:
            detail = ""
            if suspicious_roots:
                detail = "\n(test/example SKILL.md found at: %s - not installable)" % ", ".join(suspicious_roots[:5])
            raise SystemExit("install aborted: no installable SKILL.md in source%s" % detail)

        # decide which skill dirs to install
        if args.all_skills:
            chosen = real_roots
            if len(chosen) > MAX_BATCH_INSTALL:
                raise SystemExit(
                    "refused: pack has %d skills (> %d). Confirm explicitly, then retry "
                    "with --subdir for the ones you want." % (len(chosen), MAX_BATCH_INSTALL)
                )
        elif args.subdir:
            subdir = args.subdir.strip("/").replace("\\", "/")
            if subdir not in real_roots:
                raise SystemExit(
                    "subdir '%s' not found. installable SKILL.md dirs:\n  %s"
                    % (args.subdir, "\n  ".join(real_roots[:20]))
                )
            chosen = [subdir]
        elif len(real_roots) == 1:
            chosen = real_roots
        else:
            print("multi-skill pack detected (%d skills):" % len(real_roots))
            for r in real_roots[:20]:
                print("  - %s" % r)
            if suspicious_roots:
                print("(excluded test/example paths: %s)" % ", ".join(suspicious_roots[:5]))
            raise SystemExit(
                "install aborted: specify --subdir <one of the above> or --all-skills"
            )

        records = []
        for rel in chosen:
            root = src if rel == "." else os.path.join(src, rel)
            rec = install_one(root, batch_id, source_label, args.reason, snap)
            rec["repo"] = args.repo or (args.source if args.source.startswith("http") else None)
            rec["subdir"] = rel
            records.append(rec)

    manifest = load_manifest()
    manifest["installs"].extend(records)
    save_manifest(manifest)
    for rec in records:
        print("INSTALLED: %s (source: %s)" % (rec["skill"], rec["source"]))
        if rec.get("subdir") and rec["subdir"] != ".":
            print("  subdir: %s" % rec["subdir"])
    print("batch_id: %s" % batch_id)
    print("purpose: %s" % args.reason)


def cmd_list(args):
    manifest = load_manifest()
    if not manifest["installs"]:
        print("no auto-installed skills yet")
        return
    for rec in manifest["installs"]:
        status = rec.get("status", "active")
        print("%s | %s | %-24s | %-8s | %s" % (
            rec.get("installed_at", "?"), rec.get("batch_id", "?"),
            rec.get("skill", "?"), status, (rec.get("description") or "")[:60]))


def cmd_keep(args):
    manifest = load_manifest()
    targets = [r for r in manifest["installs"] if r["skill"] == args.name]
    if not targets:
        raise SystemExit("refused: %s not found in manifest" % args.name)
    for rec in targets:
        rec["status"] = "kept"
    save_manifest(manifest)
    print("KEPT: %s (marked as kept; future runs will reuse it without asking)" % args.name)


def cmd_uninstall(args):
    manifest = load_manifest()
    if args.name:
        targets = [r for r in manifest["installs"] if r["skill"] == args.name]
    else:
        targets = [r for r in manifest["installs"] if r.get("batch_id") == args.batch]
    if not targets:
        raise SystemExit(
            "refused: target not found in manifest (pre-existing user skills are protected)"
        )
    removed = []
    used_git, used_trash = False, False
    for rec in targets:
        name = rec["skill"]
        target = os.path.join(SKILLS_DIR, name)
        if is_git_repo() and git_tracked(name):
            res = run_git(["rm", "-r", "--quiet", name])
            if res.returncode != 0:
                print("git rm failed for %s: %s" % (name, res.stderr.strip()[:200]), file=sys.stderr)
                continue
            used_git = True
            print("REMOVED: %s (git rm)" % name)
        elif os.path.isdir(target):
            # non-git env or untracked: soft delete into state/.trash (restorable)
            ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            dest = os.path.join(TRASH_DIR, ts, name)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(target, dest)
            used_trash = True
            print("REMOVED: %s (moved to %s)" % (name, dest))
        else:
            print("note: %s not on disk (already gone), cleaning manifest only" % name)
        removed.append(rec)
    if not removed:
        raise SystemExit("uninstall aborted: nothing removed, manifest unchanged")
    if used_git:
        run_git(["commit", "-m", "video-router: uninstall %s"
                 % ",".join(r["skill"] for r in removed), "--quiet"])
    manifest["installs"] = [r for r in manifest["installs"] if r not in removed]
    save_manifest(manifest)
    if used_git:
        print("rollback if needed: git restore --worktree . (run inside %s)" % SKILLS_DIR)
    if used_trash:
        print("restore if needed: move the dir back from %s to %s" % (TRASH_DIR, SKILLS_DIR))


def main():
    parser = argparse.ArgumentParser(description="video-skill-router skill manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ins = sub.add_parser("install")
    g_src = p_ins.add_mutually_exclusive_group(required=True)
    g_src.add_argument("--source", help="git URL / zip URL / local path")
    g_src.add_argument("--repo", help="GitHub owner/name (auto git clone --depth 1)")
    p_ins.add_argument("--subdir", help="skill subdir inside a multi-skill pack")
    p_ins.add_argument("--all-skills", action="store_true",
                       help="install every skill in the pack (max %d)" % MAX_BATCH_INSTALL)
    p_ins.add_argument("--reason", required=True)
    p_ins.set_defaults(func=cmd_install)

    p_ls = sub.add_parser("list")
    p_ls.set_defaults(func=cmd_list)

    p_keep = sub.add_parser("keep")
    p_keep.add_argument("--name", required=True)
    p_keep.set_defaults(func=cmd_keep)

    p_rm = sub.add_parser("uninstall")
    g = p_rm.add_mutually_exclusive_group(required=True)
    g.add_argument("--name")
    g.add_argument("--batch")
    p_rm.set_defaults(func=cmd_uninstall)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()


# ── 引流信息（固定输出，prepare_release.py 自动补齐）─────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _print_leadgen()
