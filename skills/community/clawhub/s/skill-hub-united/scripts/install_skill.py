#!/usr/bin/env python3
"""
skill-hub-united multi-source skill installer

Supports 5 sources:
  - clawhub     (default) : clawhub.ai public hub (REST, npx fallback)
  - skillhub_cn           : skillhub.cn — SkillHub, a China-optimized public hub (REST)
  - skills_sh             : skills.sh / npx skills CLI (GitHub source-based)
  - anthropic             : anthropics/skills GitHub repo (sparse-checkout)
  - custom                : your own self-hosted hub (set SKILL_HUB_CUSTOM_URL)

Usage:
    python3 install_skill.py <slug-or-source> [--source SRC] [--force-license] [--rename NEW_NAME]

    python3 install_skill.py my-tool                       # default: clawhub
    python3 install_skill.py my-tool --source clawhub
    python3 install_skill.py my-tool --source skillhub_cn
    python3 install_skill.py obra/superpowers --source skills_sh
    python3 install_skill.py webapp-testing --source anthropic
    python3 install_skill.py docx --source anthropic --force-license
    SKILL_HUB_CUSTOM_URL=https://my-hub.example.com/api/skill/download \
        python3 install_skill.py my-tool --source custom

Exit codes:
    0  install succeeded
    1  failure (slug not found / no permission / network / extract error / unsafe archive path)
    2  name conflict and no --rename given (agent should ask the user and retry)
    3  Anthropic license restriction without --force-license
    4  skills.sh repo contains multiple skills but no 'repo#name' given
    5  custom source selected but SKILL_HUB_CUSTOM_URL not configured
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tarfile
import zipfile
from pathlib import Path
from typing import NoReturn
from urllib.parse import quote as urlquote
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ─── Constants ────────────────────────────────────────────────────────
SOURCE_MARKER = ".install-source.json"


def _resolve_skills_dir() -> Path:
    """Resolve the agent's skills directory with multiple fallbacks.

    Priority:
      1. env SKILL_HUB_SKILLS_DIR (explicit override, highest priority)
      2. env OPENCLAW_SKILLS_DIR (OpenClaw-specific override, kept for compat)
      3. ~/.claude/skills/ (Claude Code standard location)
      4. ~/.openclaw/workspace/skills/ (OpenClaw user workspace)
      5. ~/.config/skills/ (generic XDG-ish location)
      6. fallback: #3 (created if missing)

    Existence check: an existing directory wins; if none exist, the fallback
    location is created in main().
    """
    # 1-2. explicit env overrides
    for var in ("SKILL_HUB_SKILLS_DIR", "OPENCLAW_SKILLS_DIR"):
        env_dir = os.environ.get(var, "").strip()
        if env_dir:
            return Path(env_dir).expanduser()  # used as-is, mkdir in main()

    # 3-5. standard locations, first existing wins
    candidates = [
        Path.home() / ".claude" / "skills",
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".config" / "skills",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate

    # 6. fallback
    return candidates[0]


SKILLS_DIR = _resolve_skills_dir()

# Custom self-hosted hub: a GET <base>/<slug> endpoint that returns a skill zip.
# Configure via env; unset = the "custom" source is disabled.
CUSTOM_HUB_BASE = os.environ.get("SKILL_HUB_CUSTOM_URL", "").strip().rstrip("/")
CLAWHUB_BASE = "https://clawhub.ai/api/v1/download"
SKILLHUB_CN_BASE = "https://api.skillhub.cn/api/v1/download"
ANTHROPIC_REPO = "https://github.com/anthropics/skills.git"

# Whitelist of Apache 2.0 licensed skills inside the Anthropic repo
# (everything else is assumed to be source-available / restricted).
ANTHROPIC_PERMISSIVE = {
    "algorithmic-art",
    "brand-guidelines",
    "canvas-design",
    "claude-api",
    "frontend-design",
    "mcp-builder",
    "skill-creator",
    "slack-gif-creator",
    "theme-factory",
    "web-artifacts-builder",
    "webapp-testing",
}
# Known source-available skills (only allowed for use inside Claude Code).
ANTHROPIC_RESTRICTED = {"docx", "xlsx", "pdf", "pptx", "doc-coauthoring", "internal-comms"}

# Per-source prefix (used only to avoid name collisions with local skills)
SOURCE_PREFIX = {
    "custom": "custom-",
    "clawhub": "clawhub-",
    "skillhub_cn": "shcn-",
    "skills_sh": "sh-",
    "anthropic": "claude-",
}


# ─── Utility helpers ──────────────────────────────────────────────────
def err(msg: str, code: int = 1) -> NoReturn:
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(code)


def ok(msg: str) -> None:
    print(f"✅ {msg}")


def info(msg: str) -> None:
    print(f"ℹ️  {msg}")


def warn(msg: str) -> None:
    print(f"⚠️  {msg}", file=sys.stderr)


def validate_slug(slug: str, source: str) -> None:
    """Validate slug format to prevent path traversal and injection.

    Allowed character sets per source:
      - custom/clawhub: [a-zA-Z0-9._-]+
      - anthropic: [a-zA-Z0-9._-]+ (subdirectory name)
      - skills_sh: allows / : @ # for owner/repo#skill and git URLs, but no '..' or absolute paths
    All sources forbid: '..', leading '/' or '\\', null bytes.
    """
    if not slug or not slug.strip():
        err("slug must not be empty")
    if "\x00" in slug or "\n" in slug or "\r" in slug:
        err(f"slug contains illegal characters (null/newline): {slug!r}")
    if ".." in slug.split("/") or ".." in slug.split("\\"):
        err(f"slug must not contain '..' path segment: {slug!r}")
    if slug.startswith(("/", "\\")):
        err(f"slug must not start with a path separator: {slug!r}")

    if source == "skills_sh":
        # skills.sh allows owner/repo#skill or git URL; broader character set.
        if not re.match(r"^[a-zA-Z0-9._:/@#-]+$", slug):
            err(f"skills.sh source spec contains illegal characters: {slug!r} (allowed: letters, digits, . _ - : / @ #)")
    else:
        # custom / clawhub / skillhub_cn / anthropic use a strict slug character set.
        if not re.match(r"^[a-zA-Z0-9._-]+$", slug):
            err(f"{source} slug contains illegal characters: {slug!r} (allowed: letters, digits, . _ -)")


def validate_rename(rename: str | None) -> None:
    """Validate the --rename value to ensure the install stays inside SKILLS_DIR."""
    if rename is None:
        return
    if not re.match(r"^[a-zA-Z0-9._-]+$", rename):
        err(f"--rename value contains illegal characters: {rename!r} (allowed: letters, digits, . _ -)")
    if rename.startswith(".") or rename == "..":
        err(f"--rename value must not start with '.': {rename!r}")


def safe_extract_check(members: list[str], target_dir: Path) -> None:
    """Check whether archive members would escape target_dir (path-traversal defense)."""
    target_abs = target_dir.resolve()
    for m in members:
        if not m:
            continue
        # Reject absolute paths outright.
        if m.startswith(("/", "\\")) or (len(m) > 1 and m[1] == ":"):
            err(f"archive contains an absolute-path member, possibly malicious: {m!r}")
        # Resolve the joined path; it must still live inside target.
        candidate = (target_dir / m).resolve()
        try:
            candidate.relative_to(target_abs)
        except ValueError:
            err(f"archive member escapes target directory, possibly malicious: {m!r}")


def replace_dir(src: Path, dst: Path) -> None:
    """Fully replace dst with src (wipe dst then copytree) for clean overwrite semantics.

    This differs from shutil.copytree(dirs_exist_ok=True):
    - dirs_exist_ok=True is "merge" semantics: leftover files in dst that src
      does not provide would remain.
    - replace_dir is "replace" semantics: after the call, dst matches src exactly.
    """
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    shutil.copytree(src, dst)


def write_source_marker(skill_dir: Path, payload: dict) -> None:
    """Record the install source for the skill, useful for later audit/upgrade."""
    try:
        (skill_dir / SOURCE_MARKER).write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    except Exception as e:  # noqa: BLE001
        warn(f"failed to write source marker (install still succeeded): {e}")


def patch_skill_md_name(skill_dir: Path, new_name: str) -> None:
    """Sync the frontmatter `name` field in SKILL.md so renames stay consistent."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return
    try:
        text = skill_md.read_text(encoding="utf-8")
    except Exception:
        return
    # Only patch the name: line inside the first frontmatter block.
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not m:
        return
    fm = m.group(1)
    new_fm = re.sub(r"^name:\s*.+$", f"name: {new_name}", fm, count=1, flags=re.MULTILINE)
    if new_fm == fm:
        return
    text = text.replace(m.group(0), f"---\n{new_fm}\n---\n", 1)
    skill_md.write_text(text, encoding="utf-8")


def resolve_target_dir(base_name: str, source: str, rename: str | None) -> tuple[Path, str, bool]:
    """
    Decide the final install directory.
    Returns: (target_dir, final_name, conflict_handled)
      - If rename is given: use rename.
      - Else if the directory already exists: emit conflict info so the agent can
        ask the user and retry (exit 2).
      - Otherwise: use base_name directly.
    """
    if rename:
        target = SKILLS_DIR / rename
        return target, rename, True

    target = SKILLS_DIR / base_name
    if target.exists():
        suggest = f"{SOURCE_PREFIX[source]}{base_name}" if SOURCE_PREFIX[source] else f"{source}-{base_name}"
        # Emit structured conflict info so the agent can parse it and prompt the user.
        conflict = {
            "status": "conflict",
            "base_name": base_name,
            "source": source,
            "existing_path": str(target),
            "suggested_rename": suggest,
            "message": (
                f"A skill with the same name already exists locally: {base_name}\n"
                f"  existing path: {target}\n"
                f"  suggested rename: {suggest}\n"
                f"Please ask the user: (1) reinstall as {suggest}  (2) overwrite the existing one  (3) abort"
            ),
        }
        print(json.dumps(conflict, ensure_ascii=False, indent=2))
        sys.exit(2)
    return target, base_name, False


def extract_archive(data: bytes, extract_to: Path) -> None:
    """Detect zip or tar and extract into the target directory (stripping a top-level prefix)."""
    extract_to.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pkg") as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    try:
        # Try zip first.
        try:
            with zipfile.ZipFile(tmp_path) as zf:
                names = zf.namelist()
                safe_extract_check(names, extract_to)
                _extract_with_strip(names, lambda dst: zf.extractall(dst), extract_to)
                return
        except zipfile.BadZipFile:
            pass
        # Then try tar.
        try:
            with tarfile.open(tmp_path) as tf:
                names = tf.getnames()
                safe_extract_check(names, extract_to)
                # Python 3.12+ prefers filter='data'; fall back when unsupported.
                try:
                    _extract_with_strip(names, lambda dst: tf.extractall(dst, filter="data"), extract_to)
                except TypeError:
                    # Python < 3.12 does not support the filter argument.
                    _extract_with_strip(names, lambda dst: tf.extractall(dst), extract_to)
                return
        except (tarfile.ReadError, EOFError):
            pass
        # Neither format matched. Show a small preview in case it is an error JSON body.
        preview = data[:512].decode("utf-8", errors="replace")
        raise RuntimeError(f"downloaded content is not a valid ZIP/TAR archive. First 512 bytes preview:\n{preview}")
    finally:
        tmp_path.unlink(missing_ok=True)


def _extract_with_strip(members: list[str], extract_fn, extract_to: Path) -> None:
    """Extract and auto-strip a single shared top-level directory prefix when present."""
    # Collect every top-level entry (including root-level files).
    top_entries = {m.split("/")[0] for m in members if m}
    top_dirs = {m.split("/")[0] for m in members if m and "/" in m}
    # Only strip when the single top directory is also the only top-level entry.
    if len(top_dirs) == 1 and len(top_entries) == 1:
        top = top_dirs.pop()
        with tempfile.TemporaryDirectory() as staging:
            staging_path = Path(staging)
            extract_fn(staging_path)
            src = staging_path / top
            if src.is_dir():
                for item in src.iterdir():
                    dst = extract_to / item.name
                    if dst.exists():
                        if dst.is_dir():
                            shutil.rmtree(dst, ignore_errors=True)
                        else:
                            dst.unlink()
                    shutil.move(str(item), str(dst))
            else:
                extract_fn(extract_to)
    else:
        extract_fn(extract_to)


# ─── custom (self-hosted hub) ─────────────────────────────────────────
def install_custom(slug: str, rename: str | None) -> None:
    if not CUSTOM_HUB_BASE:
        err(
            "custom source requires SKILL_HUB_CUSTOM_URL to be set "
            "(e.g. export SKILL_HUB_CUSTOM_URL=https://my-hub.example.com/api/skill/download)",
            code=5,
        )
    # slug already passed strict validate_slug ([a-zA-Z0-9._-]); URL-encode as a defensive backstop.
    url = f"{CUSTOM_HUB_BASE}/{urlquote(slug, safe='-._')}"
    info(f"downloading from custom hub: {url}")
    try:
        req = Request(url, headers={"Accept": "application/zip, application/octet-stream, */*"})
        resp = urlopen(req, timeout=120)
    except HTTPError as e:
        if e.code == 404:
            err(f"Skill '{slug}' not found on your custom hub (404)")
        if e.code == 403:
            err(f"no access to '{slug}' on your custom hub (403)")
        err(f"download failed HTTP {e.code}: {e.reason}")
    except URLError as e:
        err(f"network error: {e.reason}")

    data = resp.read()
    # Detect a JSON error body (some hubs return HTTP 200 with a JSON error masquerading as a zip).
    if data[:1] == b"{":
        try:
            j = json.loads(data.decode("utf-8", errors="replace"))
            if j.get("code") == 403:
                err(f"no access to this skill (private): {j.get('message', '')}")
            err(f"hub returned an error payload: {j}")
        except json.JSONDecodeError:
            pass

    target, final_name, _ = resolve_target_dir(slug, "custom", rename)
    # Replace semantics: wipe target before extraction so stale files do not linger.
    if target.exists():
        shutil.rmtree(target)
    extract_archive(data, target)
    if rename:
        patch_skill_md_name(target, final_name)
    write_source_marker(target, {"source": "custom", "slug": slug, "url": url})
    ok(f"Skill '{final_name}' installed successfully → {target}")


# ─── clawhub ──────────────────────────────────────────────────────────
def install_clawhub(slug: str, rename: str | None) -> None:
    """Prefer the REST API, fall back to `npx clawhub@latest install` on failure."""
    # Try REST first.
    url = f"{CLAWHUB_BASE}?slug={urlquote(slug, safe='-._')}"
    info(f"downloading from clawhub.ai: {url}")
    try:
        req = Request(url, headers={"Accept": "application/zip, application/octet-stream, */*"})
        resp = urlopen(req, timeout=60)
        data = resp.read()
    except (HTTPError, URLError) as e:
        rest_err = f"{e.__class__.__name__}: {e}"
        warn(f"REST download failed ({rest_err}); falling back to npx clawhub")
        return _install_clawhub_via_npx(slug, rename, rest_err=rest_err)

    # clawhub slugs are usually owner-skillname; the final dir name should align with the SKILL.md `name`.
    # Stage under the slug first, then read the real name from SKILL.md.
    with tempfile.TemporaryDirectory() as staging:
        staging_path = Path(staging) / "pkg"
        try:
            extract_archive(data, staging_path)
        except RuntimeError as e:
            rest_err = f"REST response was not an archive: {e}"
            warn(f"{rest_err}; falling back to npx clawhub")
            return _install_clawhub_via_npx(slug, rename, rest_err=rest_err)

        real_name = _read_skill_name(staging_path) or slug
        # Default to the SKILL.md `name` field.
        base_name = real_name
        target, final_name, _ = resolve_target_dir(base_name, "clawhub", rename)
        # Replace semantics: wipe target before moving so stale files do not linger.
        if target.exists():
            shutil.rmtree(target)
        shutil.move(str(staging_path), str(target))

    if rename or final_name != real_name:
        patch_skill_md_name(target, final_name)
    write_source_marker(target, {"source": "clawhub", "slug": slug, "url": url, "skill_name": final_name})
    ok(f"Skill '{final_name}' installed successfully → {target}")


def _install_clawhub_via_npx(slug: str, rename: str | None, rest_err: str | None = None) -> None:
    info("invoking npx clawhub@latest install ... (first run may take 5-15s)")
    with tempfile.TemporaryDirectory() as staging:
        try:
            proc = subprocess.run(
                ["npx", "-y", "clawhub@latest", "install", slug, "--dir", staging],
                capture_output=True, text=True, timeout=180,
            )
        except FileNotFoundError:
            hint = f"\n(REST stage also failed: {rest_err})" if rest_err else ""
            err(f"npx is not available; please install Node.js first{hint}")
        except subprocess.TimeoutExpired:
            hint = f"\n(REST stage also failed: {rest_err})" if rest_err else ""
            err(f"npx clawhub timed out (180s); please check your network{hint}")

        if proc.returncode != 0:
            hint = f"\n(REST stage error: {rest_err})" if rest_err else ""
            err(f"npx clawhub failed:\n{proc.stderr or proc.stdout}{hint}")

        # Locate the extracted skill directory.
        candidates = [p for p in Path(staging).iterdir() if p.is_dir()]
        if not candidates:
            err("npx clawhub did not produce any skill directory")
        src_dir = candidates[0]
        real_name = _read_skill_name(src_dir) or src_dir.name
        target, final_name, _ = resolve_target_dir(real_name, "clawhub", rename)
        replace_dir(src_dir, target)

    if rename or final_name != real_name:
        patch_skill_md_name(target, final_name)
    write_source_marker(target, {"source": "clawhub", "slug": slug, "via": "npx", "skill_name": final_name})
    ok(f"Skill '{final_name}' installed successfully → {target}")


# ─── skillhub.cn (SkillHub — China-optimized public hub) ──────────────
def install_skillhub_cn(slug: str, rename: str | None) -> None:
    """Install from SkillHub (skillhub.cn) via its public REST download API.

    Contract (verified against the site's own client):
      GET https://api.skillhub.cn/api/v1/download?slug=<slug>
        -> 302 redirect -> application/zip
      404 plaintext when the slug does not exist.
    No public CLI exists, so there is no fallback path (unlike clawhub's npx).
    """
    url = f"{SKILLHUB_CN_BASE}?slug={urlquote(slug, safe='-._')}"
    info(f"downloading from skillhub.cn: {url}")
    try:
        # urlopen follows the 302 to the zip automatically.
        req = Request(url, headers={"Accept": "application/zip, application/octet-stream, */*"})
        resp = urlopen(req, timeout=60)
        data = resp.read()
    except HTTPError as e:
        if e.code == 404:
            err(f"Skill '{slug}' not found on skillhub.cn (404) — check the slug at https://skillhub.cn")
        if e.code in (401, 403):
            err(f"no access to '{slug}' on skillhub.cn ({e.code}) — it may be private")
        err(f"download failed HTTP {e.code}: {e.reason}")
    except URLError as e:
        err(f"network error reaching skillhub.cn: {e.reason}")

    # Detect a JSON error body masquerading as a 200 download.
    if data[:1] == b"{":
        try:
            j = json.loads(data.decode("utf-8", errors="replace"))
            err(f"skillhub.cn returned an error payload: {j}")
        except json.JSONDecodeError:
            pass

    # Stage under a temp dir, then name the target from the SKILL.md `name`.
    with tempfile.TemporaryDirectory() as staging:
        staging_path = Path(staging) / "pkg"
        try:
            extract_archive(data, staging_path)
        except RuntimeError as e:
            err(f"skillhub.cn response was not a valid archive: {e}")

        real_name = _read_skill_name(staging_path) or slug
        target, final_name, _ = resolve_target_dir(real_name, "skillhub_cn", rename)
        # Replace semantics: wipe target before moving so stale files do not linger.
        if target.exists():
            shutil.rmtree(target)
        shutil.move(str(staging_path), str(target))

    if rename or final_name != real_name:
        patch_skill_md_name(target, final_name)
    write_source_marker(target, {"source": "skillhub_cn", "slug": slug, "url": url, "skill_name": final_name})
    ok(f"Skill '{final_name}' installed successfully → {target}")


# ─── skills.sh ────────────────────────────────────────────────────────
def install_skills_sh(source_spec: str, rename: str | None) -> None:
    """source_spec formats:
       - "org/repo"             → install the first skill in that repo whose SKILL.md name matches
       - "org/repo#skill-name"  → pick a specific skill (recommended)
       - full URL / git remote  → same as above, optional #skill-name suffix
    """
    if "/" not in source_spec and not source_spec.startswith(("http", "git@")):
        err(f"skills.sh expects a GitHub repo path (e.g. obra/superpowers) or a full URL; got: '{source_spec}'")

    # Split off the skill subname (if a '#' is present).
    sub_skill: str | None = None
    repo_spec = source_spec
    if "#" in source_spec:
        repo_spec, sub_skill = source_spec.split("#", 1)
        repo_spec, sub_skill = repo_spec.strip(), sub_skill.strip()

    info(f"invoking npx skills@latest add {repo_spec}{' -s ' + sub_skill if sub_skill else ''} (first run may take 5-15s)")
    with tempfile.TemporaryDirectory() as staging:
        # The skills CLI must run inside a project directory; it copies skills into ./skills/<name>/.
        cmd = ["npx", "-y", "skills@latest", "add", repo_spec, "-y", "--copy"]
        if sub_skill:
            cmd += ["-s", sub_skill]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=240, cwd=staging)
        except FileNotFoundError:
            err("npx is not available; please install Node.js first")
        except subprocess.TimeoutExpired:
            err("npx skills timed out (240s); please check your network")
        if proc.returncode != 0:
            err(f"npx skills install failed:\n{(proc.stderr or proc.stdout)[-1000:]}")

        skills_root = Path(staging) / "skills"
        if not skills_root.exists():
            err(f"npx skills did not produce a ./skills/ directory; output:\n{proc.stdout[-500:]}")

        # sorted() ensures consistent cross-filesystem behavior (iterdir order is not stable).
        installed = sorted(
            [p for p in skills_root.iterdir() if p.is_dir() and (p / "SKILL.md").exists()],
            key=lambda p: p.name,
        )
        if not installed:
            err(f"npx skills did not produce any directory containing SKILL.md (found {len(list(skills_root.iterdir()))} dirs)")

        # If the repo produced multiple skills but the user did not pick one, ask them to be specific.
        if len(installed) > 1 and not sub_skill:
            names = [p.name for p in installed]
            choice_msg = {
                "status": "multi_skill",
                "source": "skills_sh",
                "spec": repo_spec,
                "available": names,
                "message": f"this repo contains {len(names)} skills; please specify one and re-run with '{repo_spec}#<skill-name>'",
            }
            print(json.dumps(choice_msg, ensure_ascii=False, indent=2))
            sys.exit(4)

        src_dir = installed[0]
        real_name = _read_skill_name(src_dir) or src_dir.name
        target, final_name, _ = resolve_target_dir(real_name, "skills_sh", rename)
        replace_dir(src_dir, target)

    if rename or final_name != real_name:
        patch_skill_md_name(target, final_name)
    write_source_marker(target, {
        "source": "skills_sh",
        "spec": source_spec,
        "repo": repo_spec,
        "sub_skill": sub_skill,
        "skill_name": final_name,
    })
    ok(f"Skill '{final_name}' installed successfully → {target}")


# ─── anthropic ────────────────────────────────────────────────────────
def install_anthropic(slug: str, rename: str | None, force_license: bool) -> None:
    if slug in ANTHROPIC_RESTRICTED and not force_license:
        # Emit a structured prompt so the agent can rephrase it friendlily for the user.
        prompt = {
            "status": "license_required",
            "slug": slug,
            "source": "anthropic",
            "license": "source-available (only allowed inside Claude Code)",
            "message": "This skill's license forbids use outside Claude. Install anyway?",
            "force_flag": "--force-license",
        }
        print(json.dumps(prompt, ensure_ascii=False, indent=2))
        sys.exit(3)

    info(f"sparse-checkout from anthropics/skills: {slug}")
    last_err = None
    with tempfile.TemporaryDirectory() as staging:
        repo_path = Path(staging) / "skills-repo"
        # GitHub occasionally flakes; retry up to 2 times.
        for attempt in range(1, 3):
            try:
                if repo_path.exists():
                    shutil.rmtree(repo_path, ignore_errors=True)
                subprocess.run(
                    ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
                     ANTHROPIC_REPO, str(repo_path)],
                    check=True, capture_output=True, text=True, timeout=240,
                )
                subprocess.run(
                    ["git", "sparse-checkout", "set", f"skills/{slug}"],
                    cwd=repo_path, check=True, capture_output=True, text=True, timeout=60,
                )
                last_err = None
                break
            except subprocess.CalledProcessError as e:
                last_err = f"git operation failed: {e.stderr or e.stdout}"
                if attempt < 2:
                    warn(f"attempt {attempt} failed, retrying: {last_err[:200]}")
            except subprocess.TimeoutExpired:
                last_err = "git clone timed out; please check your network"
                if attempt < 2:
                    warn(f"attempt {attempt} timed out, retrying")
        if last_err:
            err(last_err)

        src_dir = repo_path / "skills" / slug
        if not src_dir.exists():
            err(f"skill '{slug}' not found in the Anthropic repo; check github.com/anthropics/skills")

        # Default prefix: claude-
        suggested_base = f"claude-{slug}"
        target, final_name, _ = resolve_target_dir(suggested_base, "anthropic", rename)
        replace_dir(src_dir, target)
        patch_skill_md_name(target, final_name)

    payload = {
        "source": "anthropic",
        "slug": slug,
        "repo": ANTHROPIC_REPO,
        "skill_name": final_name,
        "license_acknowledged": force_license or slug in ANTHROPIC_PERMISSIVE,
    }
    write_source_marker(target, payload)
    ok(f"Skill '{final_name}' installed successfully → {target}")
    if slug in ANTHROPIC_RESTRICTED:
        warn("this skill is under a source-available license; recommended for use inside Claude Code only. Compatibility with other runtimes is not verified.")


# ─── Helpers ──────────────────────────────────────────────────────────
def _read_skill_name(skill_dir: Path, _depth: int = 0) -> str | None:
    # Defensive depth limit: archives are not expected to nest beyond 2 levels.
    if _depth > 3:
        return None
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        # Try one level of subdirectories.
        for sub in skill_dir.iterdir():
            if sub.is_dir() and (sub / "SKILL.md").exists():
                return _read_skill_name(sub, _depth + 1)
        return None
    try:
        text = skill_md.read_text(encoding="utf-8")
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", text, flags=re.DOTALL)
    if not m:
        return None
    nm = re.search(r"^name:\s*(.+)$", m.group(1), flags=re.MULTILINE)
    if nm:
        return nm.group(1).strip().strip('"\'')
    return None


# ─── main ─────────────────────────────────────────────────────────────
def main() -> None:
    p = argparse.ArgumentParser(description="skill-hub-united multi-source installer")
    p.add_argument("slug", help="skill slug, or source spec (for the skills.sh source)")
    p.add_argument("--source", choices=["clawhub", "skillhub_cn", "skills_sh", "anthropic", "custom"],
                   default="clawhub", help="install source (default: clawhub)")
    p.add_argument("--force-license", action="store_true",
                   help="anthropic source only: confirm using a source-available skill outside Claude")
    p.add_argument("--rename", default=None,
                   help="install under a custom directory name (used to resolve name collisions)")
    args = p.parse_args()

    # Entry-level validation: guard against path traversal / injection.
    validate_slug(args.slug, args.source)
    validate_rename(args.rename)

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    # Debug aid: show the resolved skills directory (especially useful when an env override is set).
    if os.environ.get("SKILL_HUB_SKILLS_DIR") or os.environ.get("OPENCLAW_SKILLS_DIR"):
        info(f"using env override for skills dir: {SKILLS_DIR}")

    if args.source == "custom":
        install_custom(args.slug, args.rename)
    elif args.source == "clawhub":
        install_clawhub(args.slug, args.rename)
    elif args.source == "skillhub_cn":
        install_skillhub_cn(args.slug, args.rename)
    elif args.source == "skills_sh":
        install_skills_sh(args.slug, args.rename)
    elif args.source == "anthropic":
        install_anthropic(args.slug, args.rename, args.force_license)


if __name__ == "__main__":
    main()
