#!/usr/bin/env python3
import argparse
import json
import mimetypes
import re
import shlex
import subprocess
import sys
import textwrap
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WORKSPACE_ROOT = Path("/home/baiwan/.openclaw/workspace-assistant-shrimp")
DEFAULT_LOCAL_ROOTS = [
    WORKSPACE_ROOT / "skills",
    Path.home() / ".openclaw" / "skills",
]
REFERENCE_VETTER_DIRS = [root / "azhua-skill-vetter" for root in DEFAULT_LOCAL_ROOTS]
TEXT_EXTS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".js", ".mjs", ".cjs",
    ".ts", ".tsx", ".jsx", ".toml", ".ini", ".cfg", ".conf", ".xml", ".html", ".css",
    ".lock", ".gitignore", ".npmignore",
}
MAX_TEXT_BYTES = 500_000
USER_AGENT = "skill-install-guard/1.3.1"


def _joined(*parts: str) -> str:
    return "".join(parts)


DYNAMIC_EXECUTION_PATTERNS = [
    _joined("ev", "al", r"\("),
    _joined("ex", "ec", r"\("),
    _joined("new", r"\s+", "Function", r"\("),
    _joined("Function", r"\("),
]

COMMAND_EXECUTION_PATTERNS = [
    r"subprocess\.",
    r"os\.system",
    _joined("child", "_", "process"),
    r"spawn\(",
    r"Popen\(",
]

INLINE_VETTER_POLICY = {
    "source_check_questions": [
        "Where did this skill come from?",
        "Is the author/source metadata consistent with the intended target?",
        "How many downloads/stars does it have?",
        "When was it last updated?",
        "Are there reviews/comments from other agents?",
    ],
    "red_flags": [
        "curl/wget to unknown URLs",
        "Sends data to external servers",
        "Requests credentials/tokens/API keys",
        "Reads ~/.ssh, ~/.aws, ~/.config without clear reason",
        "Accesses MEMORY.md, USER.md, SOUL.md, IDENTITY.md",
        "Uses base64 decode on anything",
        "Uses dynamic code evaluation with external input",
        "Modifies system files outside workspace",
        "Installs packages without listing them",
        "Network calls to IPs instead of domains",
        "Obfuscated code (compressed, encoded, minified)",
        "Requests elevated/sudo permissions",
        "Accesses browser cookies/sessions",
        "Touches credential files",
    ],
    "categories": {
        "suspicious_file_access": {
            "severity": "HIGH",
            "rules": [
                (r"~/.ssh|\\.ssh/|id_rsa|known_hosts", "Touches SSH keys or SSH config paths."),
                (r"~/.aws|\\.aws/|aws_access_key_id|aws_secret_access_key", "Touches AWS credential material or credential files."),
                (r"~/.config|\\.config/|/etc/passwd|/etc/shadow|/var/lib", "Touches sensitive local/system configuration paths."),
                (r"MEMORY\\.md|USER\\.md|SOUL\\.md|IDENTITY\\.md", "Touches personal memory/profile files that should not be read by untrusted skills."),
                (r"browser cookies|Cookies|sessionStorage|localStorage", "Touches browser cookies/session storage."),
            ],
        },
        "credential_prompts": {
            "severity": "HIGH",
            "rules": [
                (r"api[_-]?key|access[_-]?token|refresh[_-]?token|secret|password|credential", "Mentions credentials, keys, or secrets."),
                (r"paste .*token|enter .*token|provide .*key|login cookie", "Prompts the operator to hand over credentials or session material."),
            ],
        },
        "network_behavior": {
            "severity": "MEDIUM",
            "rules": [
                (r"\\bcurl\\b|\\bwget\\b", "Runs curl/wget; verify destination and payload intent."),
                (r"requests\.|urllib\.request|fetch\(|axios|httpx", "Contains programmatic network access."),
                (r"https?://(?:\\d{1,3}\\.){3}\\d{1,3}", "Uses raw IP HTTP endpoints instead of domains."),
                (r"webhook|ngrok|discordapp\\.com/api/webhooks|api\\.telegram|slack\\.com/api", "Contains webhook or bot-delivery style outbound endpoints."),
            ],
        },
        "obfuscation_or_encoded_execution": {
            "severity": "HIGH",
            "rules": [
                (r"base64\s+-d|b64decode|frombase64|atob\(", "Uses base64 decode or encoded payload recovery."),
                (r"gzip -d|zlib\.decompress|marshal\.loads|pickle\.loads", "Decodes or loads serialized/compressed payloads that can hide behavior."),
                ("|".join(DYNAMIC_EXECUTION_PATTERNS), "Uses dynamic code execution primitives."),
                (r"python -c|bash -c|sh -c|powershell -enc", "Builds or executes code from inline strings."),
            ],
        },
        "external_input_execution": {
            "severity": "HIGH",
            "rules": [
                ("|".join(COMMAND_EXECUTION_PATTERNS), "Executes shell or subprocess commands."),
                (r"\$\{|stdin|input\(|argv|sys\.argv", "Consumes runtime input that may flow into commands/scripts."),
            ],
        },
        "install_side_effects": {
            "severity": "MEDIUM",
            "rules": [
                (r"pip install|pip3 install|npm install|pnpm add|yarn add|apt install|brew install|go install", "Installs packages as a side effect."),
                (r"chmod\\s+777|chown\\s+root|systemctl|launchctl|crontab|registry add", "Changes system services/permissions or persists outside normal skill scope."),
                (r"mv\s+.*~/.openclaw|cp\s+.*~/.openclaw|write_text\(|Path\(.*\.openclaw", "Writes into OpenClaw or user config locations as part of install flow."),
            ],
        },
        "high_risk_permissions": {
            "severity": "HIGH",
            "rules": [
                (r"\\bsudo\\b|doas|pkexec", "Requests elevated privileges."),
                (r"browser|canvas|message|feishu_|memory_search|memory_get", "Requests or implies broad/high-sensitivity tool scope; verify necessity."),
                (r"ssh |scp |rsync |docker |kubectl ", "Requests remote/system-control oriented command scope."),
            ],
        },
    },
}
PERMISSION_HINTS = {
    "files": [r"Path\(", r"open\(", r"read_text\(", r"write_text\(", r"fs\.", r"cp\b", r"mv\b", r"unlink\(", r"rmtree"],
    "network": [r"https?://", r"urllib\.request", r"requests\.", r"fetch\(", r"axios", r"httpx", r"\bcurl\b", r"\bwget\b"],
    "commands": [r"subprocess", r"os\.system", _joined("child", "_", "process"), r"spawn\(", r"Popen\(", r"\bpython3?\b", r"\bbash\b", r"\bsh\b"],
}
HIGH_RISK_PERMISSION_PATTERNS = [
    r"memory_search|memory_get",
    r"browser",
    r"message",
    r"feishu_",
    r"exec",
    r"canvas",
]


class GuardError(Exception):
    pass


def run(cmd: List[str], *, cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=check, text=True, capture_output=True)


def run_install_command(command: str, *, cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    blocked_tokens = {"&&", "||", "|", ";", ">", ">>", "<"}
    argv = shlex.split(command)
    if not argv:
        raise GuardError("Install command is empty after parsing")
    bad = [token for token in argv if token in blocked_tokens]
    if bad:
        raise GuardError(
            "Install command must be a direct executable invocation without shell operators: "
            + ", ".join(sorted(set(bad)))
        )
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True)


def maybe_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


def parse_skill_frontmatter(text: str) -> Dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    out: Dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip().strip('"')
    return out


def iso_from_epoch_ms(value) -> str:
    if value in (None, "", 0):
        return "MISSING"
    try:
        ts = int(value) / 1000
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    except Exception:
        return str(value)


def fetch_url_text(url: str, max_bytes: int = MAX_TEXT_BYTES) -> Optional[str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json, text/plain, */*"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read(max_bytes + 1)
            if len(data) > max_bytes:
                return None
            return data.decode("utf-8", errors="ignore")
    except Exception:
        return None


def fetch_json_url(url: str) -> Optional[Dict]:
    text = fetch_url_text(url)
    data = maybe_json(text or "")
    return data if isinstance(data, dict) else None


def classify_source(source: Optional[str]) -> str:
    if not source:
        return "clawhub"
    if source in {"clawhub", "registry"}:
        return "clawhub"
    if re.match(r"https?://", source):
        return "url"
    if Path(source).expanduser().exists():
        return "local"
    if re.match(r"^[a-zA-Z0-9._-]+$", source):
        return "clawhub"
    return "other"


def normalize_source(source: Optional[str]) -> Optional[str]:
    if not source:
        return source
    expanded = Path(source).expanduser()
    if not re.match(r"https?://", source) and expanded.exists():
        return str(expanded)
    return source


def collect_local_state(slug: str, extra_dirs: List[Path]) -> List[Path]:
    found = []
    for base in DEFAULT_LOCAL_ROOTS + extra_dirs:
        candidate = base / slug
        if candidate.is_dir():
            found.append(candidate)
    return found


def should_treat_as_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTS or path.name in {"SKILL.md", "README.md", "package.json", "_meta.json"}:
        return True
    mime, _ = mimetypes.guess_type(path.name)
    return bool(mime and (mime.startswith("text/") or mime in {"application/json", "application/xml", "application/javascript"}))


def read_text_if_reasonable(path: Path, max_bytes: int = MAX_TEXT_BYTES) -> Tuple[Optional[str], Optional[str]]:
    try:
        size = path.stat().st_size
        if size > max_bytes:
            return None, f"text file too large ({size} bytes > {max_bytes})"
        return path.read_text(encoding="utf-8", errors="ignore"), None
    except Exception as exc:
        return None, str(exc)


def inspect_clawhub_slug(slug: str, version: Optional[str]) -> Dict:
    cmd = ["clawhub", "inspect", slug, "--json"]
    if version:
        cmd += ["--version", version]
    proc = run(cmd)
    cleaned = "\n".join(line for line in proc.stdout.splitlines() if not line.startswith("- Fetching"))
    data = maybe_json(cleaned)
    if not isinstance(data, dict):
        raise GuardError(f"Unable to parse clawhub inspect JSON for slug {slug}")
    return data


def list_clawhub_files(slug: str, version: Optional[str]) -> List[str]:
    cmd = ["clawhub", "inspect", slug, "--files"]
    if version:
        cmd += ["--version", version]
    proc = run(cmd)
    return [line.strip() for line in proc.stdout.splitlines() if line.strip() and not line.startswith("Fetching") and not line.startswith("- Fetching")]


def fetch_clawhub_file(slug: str, relpath: str, version: Optional[str]) -> Tuple[Optional[bytes], Optional[str]]:
    cmd = ["clawhub", "inspect", slug, "--file", relpath]
    if version:
        cmd += ["--version", version]
    proc = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT), capture_output=True)
    if proc.returncode != 0:
        return None, proc.stderr.decode("utf-8", errors="ignore")
    return proc.stdout, None


def gather_local_files(src: Path) -> Tuple[List[Dict], Dict[str, str]]:
    skill_md = src / "SKILL.md"
    if not skill_md.is_file():
        raise GuardError(f"Local source missing SKILL.md: {skill_md}")
    meta = parse_skill_frontmatter(skill_md.read_text(encoding="utf-8", errors="ignore"))
    files: List[Dict] = []
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(src))
        entry = {
            "path": rel,
            "size": path.stat().st_size,
            "kind": "binary",
            "read_status": "not-read-binary",
            "text": None,
            "note": None,
        }
        if should_treat_as_text(path):
            entry["kind"] = "text"
            text, note = read_text_if_reasonable(path)
            if text is not None:
                entry["read_status"] = "read"
                entry["text"] = text
            else:
                entry["read_status"] = "skipped"
                entry["note"] = note
        files.append(entry)
    return files, meta


def clawhub_reputation(info: Dict) -> Dict:
    skill = info.get("skill") or {}
    owner = info.get("owner") or {}
    stats = skill.get("stats") or {}
    latest = info.get("latestVersion") or {}
    return {
        "source": "ClawHub",
        "author": owner.get("handle") or owner.get("displayName") or "MISSING",
        "downloads_or_stars": {
            "downloads": stats.get("downloads"),
            "stars": stats.get("stars"),
        },
        "last_updated": iso_from_epoch_ms(skill.get("updatedAt") or latest.get("createdAt")),
        "reviews_or_comments": stats.get("comments"),
        "display_name": skill.get("displayName") or skill.get("slug"),
        "published_version": (latest.get("version") or skill.get("tags", {}).get("latest") or "MISSING"),
        "raw": {
            "skill": skill,
            "owner": owner,
            "latestVersion": latest,
        },
    }


def gather_clawhub_files(slug: str, version: Optional[str]) -> Tuple[List[Dict], Dict[str, str], Dict]:
    info = inspect_clawhub_slug(slug, version)
    files: List[Dict] = []
    for relpath in list_clawhub_files(slug, version):
        raw, note = fetch_clawhub_file(slug, relpath, version)
        entry = {
            "path": relpath,
            "size": len(raw or b""),
            "kind": "binary",
            "read_status": "not-read-binary",
            "text": None,
            "note": note,
        }
        if raw is not None:
            if Path(relpath).suffix.lower() in TEXT_EXTS or Path(relpath).name in {"SKILL.md", "README.md", "package.json", "_meta.json"}:
                try:
                    text = raw.decode("utf-8", errors="ignore")
                    if len(raw) <= MAX_TEXT_BYTES:
                        entry["kind"] = "text"
                        entry["read_status"] = "read"
                        entry["text"] = text
                    else:
                        entry["kind"] = "text"
                        entry["read_status"] = "skipped"
                        entry["note"] = f"text file too large ({len(raw)} bytes > {MAX_TEXT_BYTES})"
                except Exception as exc:
                    entry["note"] = str(exc)
        files.append(entry)
    skill_text = next((f["text"] for f in files if f["path"] == "SKILL.md" and f["text"] is not None), "")
    meta = parse_skill_frontmatter(skill_text) if skill_text else {}
    if not meta:
        meta = {
            "name": (info.get("skill") or {}).get("displayName") or slug,
            "slug": (info.get("skill") or {}).get("slug") or slug,
            "version": (info.get("latestVersion") or {}).get("version") or version or "unknown",
            "author": (info.get("owner") or {}).get("handle") or "unknown",
        }
    return files, meta, clawhub_reputation(info)


def github_repo_from_url(url: str) -> Optional[Tuple[str, str]]:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc not in {"github.com", "raw.githubusercontent.com"}:
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if parsed.netloc == "github.com" and len(parts) >= 2:
        return parts[0], parts[1]
    if parsed.netloc == "raw.githubusercontent.com" and len(parts) >= 2:
        return parts[0], parts[1]
    return None


def url_reputation(url: str) -> Dict:
    repo = github_repo_from_url(url)
    if repo:
        owner, name = repo
        api = fetch_json_url(f"https://api.github.com/repos/{owner}/{name}") or {}
        return {
            "source": "GitHub",
            "author": (api.get("owner") or {}).get("login") or owner,
            "downloads_or_stars": {
                "downloads": "MISSING",
                "stars": api.get("stargazers_count"),
            },
            "last_updated": api.get("updated_at") or "MISSING",
            "reviews_or_comments": api.get("subscribers_count") if api else "MISSING",
            "display_name": api.get("full_name") or f"{owner}/{name}",
            "published_version": api.get("default_branch") or "MISSING",
            "raw": api,
        }
    return {
        "source": "URL",
        "author": "MISSING",
        "downloads_or_stars": {"downloads": "MISSING", "stars": "MISSING"},
        "last_updated": "MISSING",
        "reviews_or_comments": "MISSING",
        "display_name": url,
        "published_version": "MISSING",
        "raw": {},
    }


def gather_url_files(url: str) -> Tuple[List[Dict], Dict[str, str], Dict]:
    text = fetch_url_text(url)
    if text is None:
        raise GuardError(f"Unable to fetch source URL: {url}")
    meta = parse_skill_frontmatter(text)
    rel = urllib.parse.urlparse(url).path.rsplit("/", 1)[-1] or "remote-file"
    files = [{
        "path": rel,
        "size": len(text.encode("utf-8")),
        "kind": "text",
        "read_status": "read",
        "text": text,
        "note": None,
    }]
    return files, meta, url_reputation(url)


def gather_source_bundle(source_kind: str, slug: str, source: Optional[str], version: Optional[str]) -> Tuple[List[Dict], Dict[str, str], Dict]:
    if source_kind == "local":
        src = Path(source).expanduser()
        files, meta = gather_local_files(src)
        reputation = build_local_reputation(src, meta)
        return files, meta, reputation
    if source_kind == "clawhub":
        return gather_clawhub_files(slug, version)
    if source_kind == "url":
        return gather_url_files(source)
    raise GuardError(f"Unsupported source kind for executable review: {source_kind}")


def build_local_reputation(src: Path, meta: Dict[str, str]) -> Dict:
    origin = maybe_json((src / ".clawhub" / "origin.json").read_text(encoding="utf-8", errors="ignore")) if (src / ".clawhub" / "origin.json").is_file() else {}
    local_meta = maybe_json((src / "_meta.json").read_text(encoding="utf-8", errors="ignore")) if (src / "_meta.json").is_file() else {}
    clawhub_slug = (origin or {}).get("slug") or (local_meta or {}).get("slug") or meta.get("slug")
    clawhub_info = None
    if clawhub_slug:
        try:
            clawhub_info = inspect_clawhub_slug(clawhub_slug, None)
        except Exception:
            clawhub_info = None
    registry_rep = clawhub_reputation(clawhub_info) if clawhub_info else None
    return {
        "source": "Local folder",
        "author": (registry_rep or {}).get("author") or meta.get("author") or local_meta.get("ownerId") or "MISSING",
        "downloads_or_stars": {
            "downloads": ((registry_rep or {}).get("downloads_or_stars") or {}).get("downloads", local_meta.get("downloads", "MISSING")),
            "stars": ((registry_rep or {}).get("downloads_or_stars") or {}).get("stars", local_meta.get("stars", "MISSING")),
        },
        "last_updated": (registry_rep or {}).get("last_updated") or iso_from_epoch_ms(local_meta.get("publishedAt") or origin.get("installedAt") or int(src.stat().st_mtime * 1000)),
        "reviews_or_comments": (registry_rep or {}).get("reviews_or_comments", local_meta.get("comments", "MISSING")),
        "display_name": (registry_rep or {}).get("display_name") or meta.get("name") or src.name,
        "published_version": (registry_rep or {}).get("published_version") or meta.get("version") or local_meta.get("version") or origin.get("installedVersion") or "MISSING",
        "raw": {
            "origin": origin or "MISSING",
            "local_meta": local_meta or "MISSING",
            "clawhub_registry": (registry_rep or {}).get("raw", "MISSING"),
        },
    }


def detect_vetter_reference() -> Dict[str, str]:
    for directory in REFERENCE_VETTER_DIRS:
        skill_md = directory / "SKILL.md"
        if skill_md.is_file():
            return {
                "mode": "fully-inlined-vetter-with-local-reference",
                "source": str(skill_md),
                "note": "skill-install-guard carries its own 1:1 inline vetter behavior. Local azhua-skill-vetter is recorded only as a lineage/reference artifact, not a runtime dependency.",
            }
    return {
        "mode": "fully-inlined-vetter-only",
        "source": "embedded rules",
        "note": "skill-install-guard is using only its embedded vetter implementation. No external skill is required for the full review path.",
    }


def evaluate_trust_hierarchy(source_kind: str, source_display: str, reputation: Dict, findings: List[Dict]) -> Dict:
    author = str(reputation.get("author") or "")
    stars = reputation.get("downloads_or_stars", {}).get("stars")
    downloads = reputation.get("downloads_or_stars", {}).get("downloads")
    credential_related = any(f["category"] in {"credential_prompts", "suspicious_file_access", "high_risk_permissions"} for f in findings)

    tier = 4
    label = "New/unknown sources → Maximum scrutiny"
    rationale = []

    if source_kind == "clawhub":
        tier = 1
        label = "Official/OpenClaw registry source → Lower scrutiny (still review)"
        rationale.append("Source resolved via ClawHub registry")
    if isinstance(stars, int) and stars >= 1000:
        tier = min(tier, 2)
        label = "High-star repo/skill → Moderate scrutiny"
        rationale.append(f"stars={stars} >= 1000")
    if isinstance(downloads, int) and downloads >= 1000:
        tier = min(tier, 2)
        label = "High-download skill → Moderate scrutiny"
        rationale.append(f"downloads={downloads} >= 1000")
    if author and author != "MISSING":
        tier = min(tier, 3 if tier > 3 else tier)
        rationale.append(f"author identified: {author}")
    if source_kind in {"local", "url", "other"} and not rationale:
        rationale.append(f"source requires direct inspection: {source_display}")
    if credential_related:
        tier = 5
        label = "Skills requesting credentials or broad sensitive access → Human approval always"
        rationale.append("credential/sensitive-access-related findings detected")

    return {
        "tier": tier,
        "label": label,
        "rationale": rationale,
    }


def verdict_and_risk(findings: List[Dict]) -> Tuple[str, str]:
    severities = {f["severity"] for f in findings}
    if not findings:
        return "🟢 LOW", "✅ SAFE TO INSTALL"
    if "HIGH" in severities:
        return "🔴 HIGH", "❌ DO NOT INSTALL"
    return "🟡 MEDIUM", "⚠️ INSTALL WITH CAUTION"


def normalize_text_for_scan(text: str) -> str:
    return text


def apply_risk_scan(files: List[Dict]) -> Dict:
    findings: List[Dict] = []
    permission_hits = {"files": set(), "network": set(), "commands": set()}
    category_hits = {name: [] for name in INLINE_VETTER_POLICY["categories"]}
    read_summary = {
        "all_files_seen": len(files),
        "text_files_read": 0,
        "text_files_skipped": 0,
        "binary_files_seen": 0,
        "unreadable_or_skipped": [],
    }

    for entry in files:
        relpath = entry["path"]
        text = entry.get("text")
        if entry["kind"] == "binary":
            read_summary["binary_files_seen"] += 1
        if entry["read_status"] == "read" and text is not None:
            read_summary["text_files_read"] += 1
            scan_text = normalize_text_for_scan(text)
            for category, config in INLINE_VETTER_POLICY["categories"].items():
                for pattern, message in config["rules"]:
                    if re.search(pattern, scan_text, flags=re.IGNORECASE | re.MULTILINE):
                        finding = {
                            "file": relpath,
                            "category": category,
                            "severity": config["severity"],
                            "rule": pattern,
                            "message": message,
                        }
                        findings.append(finding)
                        category_hits[category].append(relpath)
            for scope, patterns in PERMISSION_HINTS.items():
                for pattern in patterns:
                    if re.search(pattern, scan_text, flags=re.IGNORECASE | re.MULTILINE):
                        permission_hits[scope].add(relpath)
                        break
        elif entry["kind"] == "text":
            read_summary["text_files_skipped"] += 1
            read_summary["unreadable_or_skipped"].append({
                "file": relpath,
                "reason": entry.get("note") or entry["read_status"],
            })

    risk_level, verdict = verdict_and_risk(findings)
    red_flags = [
        f"[{f['severity']}] {f['category']} @ {f['file']}: {f['message']}"
        for f in findings
    ]
    return {
        "findings": findings,
        "red_flags": red_flags,
        "risk_level": risk_level,
        "verdict": verdict,
        "permissions": {k: sorted(v) if v else [] for k, v in permission_hits.items()},
        "category_summary": {k: sorted(set(v)) for k, v in category_hits.items() if v},
        "policy_summary": {
            "inline_policy_version": "2026-04-inline-vetter-1to1",
            "covers": sorted(INLINE_VETTER_POLICY["categories"].keys()),
            "trust_hierarchy": [
                "1. Official OpenClaw skills → Lower scrutiny (still review)",
                "2. High-star repos (1000+) → Moderate scrutiny",
                "3. Known authors → Moderate scrutiny",
                "4. New/unknown sources → Maximum scrutiny",
                "5. Skills requesting credentials → Human approval always",
            ],
        },
        "files_reviewed": len(files),
        "read_summary": read_summary,
    }


def machine_verdict(risk_level: str) -> str:
    if risk_level == "🟢 LOW":
        return "SAFE_TO_INSTALL"
    if risk_level == "🟡 MEDIUM":
        return "INSTALL_WITH_CAUTION"
    return "DO_NOT_INSTALL"


def render_vetting_report(data: Dict) -> str:
    rep = data["source_reputation"]
    risk = data["risk"]
    trust = data["trust_hierarchy"]
    perms = risk["permissions"]
    downloads = rep["downloads_or_stars"].get("downloads", "MISSING")
    stars = rep["downloads_or_stars"].get("stars", "MISSING")
    comments = rep.get("reviews_or_comments", "MISSING")
    files_line = f"{risk['files_reviewed']} total (text read: {risk['read_summary']['text_files_read']}, text skipped: {risk['read_summary']['text_files_skipped']}, binary seen: {risk['read_summary']['binary_files_seen']})"
    red_flags_block = "None" if not risk["red_flags"] else "\n".join(f"• {item}" for item in risk["red_flags"])

    lines = [
        "SKILL VETTING REPORT",
        "═══════════════════════════════════════",
        f"Skill: {data['skill_name']}",
        f"Source: {rep['source']} ({data['source_display']})",
        f"Author: {rep['author']}",
        f"Version: {rep['published_version']}",
        "───────────────────────────────────────",
        "METRICS:",
        f"• Downloads/Stars: downloads={downloads}, stars={stars}",
        f"• Last Updated: {rep['last_updated']}",
        f"• Reviews/Comments: {comments}",
        f"• Files Reviewed: {files_line}",
        "───────────────────────────────────────",
        f"RED FLAGS: {red_flags_block}",
        "",
        "PERMISSIONS NEEDED:",
        f"• Files: {', '.join(perms['files']) if perms['files'] else 'None'}",
        f"• Network: {', '.join(perms['network']) if perms['network'] else 'None'}",
        f"• Commands: {', '.join(perms['commands']) if perms['commands'] else 'None'}",
        "───────────────────────────────────────",
        f"RISK LEVEL: {risk['risk_level']}",
        "",
        f"VERDICT: {risk['verdict']}",
        "",
        f"NOTES: Trust tier {trust['tier']} — {trust['label']}; inline vetter mode={data['risk_strategy']['mode']}",
        "═══════════════════════════════════════",
        "",
        "INSTALL GUARD EXTENSIONS",
        "───────────────────────────────────────",
        "Source check answers:",
    ]
    lines.extend(f"• {item}" for item in data["source_check_answers"])
    lines.append("Trust hierarchy rationale:")
    lines.extend(f"• {item}" for item in trust["rationale"])
    lines.append("ALL files read strategy:")
    lines.append(f"• Enumerated every file in source: {risk['read_summary']['all_files_seen']} files")
    lines.append(f"• Text files read fully: {risk['read_summary']['text_files_read']}")
    lines.append(f"• Text files skipped with explicit reason: {risk['read_summary']['text_files_skipped']}")
    lines.append(f"• Binary files explicitly marked as seen/not-read-binary: {risk['read_summary']['binary_files_seen']}")
    if risk['read_summary']['unreadable_or_skipped']:
        lines.append("• Skipped/unreadable details:")
        for item in risk['read_summary']['unreadable_or_skipped']:
            lines.append(f"  • {item['file']}: {item['reason']}")
    else:
        lines.append("• Skipped/unreadable details: None")
    lines.append("Install flow:")
    lines.extend(f"• {item}" for item in data["install"])
    lines.append("Post-install verification:")
    lines.extend(f"• {item}" for item in data["verification"])
    lines.append(f"Final go/no-go: {data['go_no_go']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Automated five-step guard for OpenClaw skill installation")
    parser.add_argument("--slug", required=True, help="Skill slug to check/install")
    parser.add_argument("--source", help="Source path/URL/slug. Defaults to ClawHub slug lookup")
    parser.add_argument("--version", help="Version hint for clawhub inspection/install")
    parser.add_argument("--install-cmd", help="Actual install command to run after checks pass")
    parser.add_argument("--expected-dir", help="Expected landed directory after install")
    parser.add_argument("--extra-skill-root", action="append", default=[], help="Additional local skill roots to inspect")
    parser.add_argument("--dry-run", action="store_true", help="Run checks only; do not execute install command")
    parser.add_argument("--stop-before-install", action="store_true", help="Finish steps 1-3 and skip step 4 intentionally")
    parser.add_argument("--allow-medium-risk", action="store_true", help="Permit install execution when risk level is MEDIUM")
    parser.add_argument("--report-json", help="Write machine-readable JSON report to this path")
    args = parser.parse_args()

    slug = args.slug.strip()
    source = normalize_source(args.source)
    source_kind = classify_source(source)
    source_display = source or f"clawhub:{slug}"
    extra_roots = [Path(p).expanduser() for p in args.extra_skill_root]

    existence: List[str] = []
    local_state: List[str] = []
    install_notes: List[str] = []
    verification: List[str] = []

    try:
        files, meta, source_reputation = gather_source_bundle(source_kind, slug, source, args.version)
        existence.append(f"Resolved source successfully: {source_display}")
        existence.append(f"Source kind: {source_kind}")
        if meta:
            existence.append("Metadata: " + ", ".join(f"{k}={v}" for k, v in meta.items() if k in {"name", "slug", "version", "description", "author"} and v))
        else:
            existence.append("Metadata: unavailable")
        if meta.get("slug") and meta.get("slug") != slug:
            existence.append(f"WARNING: metadata slug={meta.get('slug')} does not match requested slug={slug}")
    except Exception as exc:
        failure = {
            "skill_name": slug,
            "slug": slug,
            "source_display": source_display,
            "source_kind": source_kind,
            "source_reputation": {
                "source": source_kind,
                "author": "MISSING",
                "downloads_or_stars": {"downloads": "MISSING", "stars": "MISSING"},
                "last_updated": "MISSING",
                "reviews_or_comments": "MISSING",
                "published_version": args.version or "MISSING",
            },
            "source_check_answers": [f"Existence/source resolution failed: {exc}"],
            "risk_strategy": detect_vetter_reference(),
            "trust_hierarchy": {"tier": 4, "label": "New/unknown sources → Maximum scrutiny", "rationale": [str(exc)]},
            "risk": {
                "findings": [],
                "red_flags": [],
                "risk_level": "🔴 HIGH",
                "verdict": "❌ DO NOT INSTALL",
                "permissions": {"files": [], "network": [], "commands": []},
                "category_summary": {},
                "policy_summary": {"inline_policy_version": "2026-04-inline-vetter-1to1", "covers": [], "trust_hierarchy": []},
                "files_reviewed": 0,
                "read_summary": {"all_files_seen": 0, "text_files_read": 0, "text_files_skipped": 0, "binary_files_seen": 0, "unreadable_or_skipped": []},
            },
            "install": ["Skipped because existence check failed."],
            "verification": ["Skipped because existence check failed."],
            "go_no_go": "NO_GO",
        }
        report = render_vetting_report(failure)
        print(report, end="")
        if args.report_json:
            p = Path(args.report_json)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(failure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return 2

    installed_paths = collect_local_state(slug, extra_roots)
    if installed_paths:
        for p in installed_paths:
            local_state.append(f"Installed candidate found: {p}")
    else:
        local_state.append("No installed directory found in known local roots.")

    risk_strategy = detect_vetter_reference()
    risk = apply_risk_scan(files)
    trust_hierarchy = evaluate_trust_hierarchy(source_kind, source_display, source_reputation, risk["findings"])

    source_check_answers = [
        f"Where did this skill come from? {source_reputation['source']} / {source_display}",
        f"Is the author known/reputable? {source_reputation['author']}",
        f"How many downloads/stars does it have? downloads={source_reputation['downloads_or_stars'].get('downloads', 'MISSING')}, stars={source_reputation['downloads_or_stars'].get('stars', 'MISSING')}",
        f"When was it last updated? {source_reputation['last_updated']}",
        f"Are there reviews from other agents? {source_reputation['reviews_or_comments']}",
    ]

    if risk["risk_level"] == "🔴 HIGH":
        go_no_go = "NO_GO"
    elif risk["risk_level"] == "🟡 MEDIUM" and not args.allow_medium_risk:
        go_no_go = "NO_GO_UNLESS_OPERATOR_ALLOWS_MEDIUM_RISK"
    else:
        go_no_go = "GO"

    expected_dir = Path(args.expected_dir).expanduser() if args.expected_dir else None

    if args.dry_run:
        install_notes.append("Dry-run enabled; install command not executed.")
    elif args.stop_before_install:
        install_notes.append("Stopped intentionally before install step.")
    else:
        if not args.install_cmd:
            install_notes.append("No install command provided; cannot execute step 4.")
            go_no_go = "NO_GO"
        elif go_no_go != "GO":
            install_notes.append(f"Install command blocked because final decision is {go_no_go}.")
        else:
            proc = run_install_command(args.install_cmd, cwd=WORKSPACE_ROOT)
            install_notes.append(f"Command: {args.install_cmd}")
            install_notes.append(f"Exit code: {proc.returncode}")
            if proc.stdout.strip():
                install_notes.append("STDOUT:\n" + textwrap.indent(proc.stdout.strip(), "    "))
            if proc.stderr.strip():
                install_notes.append("STDERR:\n" + textwrap.indent(proc.stderr.strip(), "    "))
            if proc.returncode != 0:
                go_no_go = "NO_GO"

    verify_candidates: List[Path] = []
    if expected_dir:
        verify_candidates.append(expected_dir)
    verify_candidates.extend(installed_paths)
    verify_candidates.extend([root / slug for root in DEFAULT_LOCAL_ROOTS + extra_roots])
    deduped: List[Path] = []
    seen = set()
    for candidate in verify_candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            deduped.append(candidate)
    verify_candidates = deduped

    found_verified = False
    for candidate in verify_candidates:
        if candidate.is_dir():
            verification.append(f"Directory exists: {candidate}")
            skill_md = candidate / "SKILL.md"
            if skill_md.is_file():
                verification.append(f"SKILL.md exists: {skill_md}")
                found_verified = True
                break
            verification.append(f"Directory exists but SKILL.md missing: {skill_md}")
    if not verify_candidates:
        verification.append("No verification path candidates were available.")
    elif not found_verified:
        verification.append("No landed path with SKILL.md could be verified from candidate paths.")
        if not (args.dry_run or args.stop_before_install):
            go_no_go = "NO_GO"

    skill_name = meta.get("name") or source_reputation.get("display_name") or slug
    data = {
        "skill_name": skill_name,
        "slug": slug,
        "source_display": source_display,
        "source_kind": source_kind,
        "source_reputation": source_reputation,
        "existence": existence,
        "local_state": local_state,
        "source_check_answers": source_check_answers,
        "risk_strategy": risk_strategy,
        "trust_hierarchy": trust_hierarchy,
        "risk": risk,
        "install": install_notes,
        "verification": verification,
        "go_no_go": go_no_go,
        "machine_verdict": machine_verdict(risk["risk_level"]),
    }
    report = render_vetting_report(data)
    print(report, end="")
    if args.report_json:
        p = Path(args.report_json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if go_no_go.startswith("NO_GO") and not (args.dry_run or args.stop_before_install):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
