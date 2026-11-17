#!/usr/bin/env python3
"""Read-only preflight checks for a ClawHub release directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile
from typing import Any, Iterable
import zipfile


MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 50 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 10_000
IGNORED_DIRS = {".git", ".clawhub", ".clawdhub", "node_modules", "__pycache__", ".pytest_cache"}
LIFECYCLE_SCRIPTS = {"preinstall", "install", "postinstall", "prepare", "prepublish", "prepublishOnly"}
SECRET_PATTERNS = (
    ("private-key", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("github-token", re.compile(rb"\bgh[opusr]_[A-Za-z0-9_]{20,}\b")),
    ("gitlab-token", re.compile(rb"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("npm-token", re.compile(rb"\bnpm_[A-Za-z0-9]{20,}\b")),
    ("aws-access-key", re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("slack-token", re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("bearer-token", re.compile(rb"(?i)\bauthorization\s*:\s*bearer\s+[A-Za-z0-9._~+/=-]{16,}")),
    ("jwt", re.compile(rb"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")),
    ("generic-secret-assignment", re.compile(
        rb"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|session[_-]?cookie)"
        rb"\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-=]{16,}"
    )),
)
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PERSONAL_PATH_PATTERN = re.compile(
    rb"(?:"
    + re.escape(b"/" + b"Users/") + rb"[^/\s]+/|"
    + re.escape(b"/" + b"home/") + rb"[^/\s]+/|"
    + rb"[A-Za-z]" + re.escape(b":\\" + b"Users\\") + rb"[^\\\s]+" + re.escape(b"\\")
    + rb")"
)
INTERNAL_HOST_PATTERN = re.compile(
    rb"(?i)\b(?:" + b"local" + b"host" + rb"|[A-Za-z0-9.-]+\.(?:internal|local))\b"
)
FRONTMATTER_FIELD = re.compile(r"^([A-Za-z0-9_-]+):(?:[ \t]*(.*))?$")


def add(findings: list[dict[str, str]], severity: str, code: str, message: str) -> None:
    findings.append({"severity": severity, "code": code, "message": message})


def classify(root: Path, findings: list[dict[str, str]]) -> str:
    has_skill = (root / "SKILL.md").is_file()
    has_plugin = (root / "openclaw.plugin.json").is_file()
    package = root / "package.json"
    package_signals = False
    if package.is_file():
        try:
            data = json.loads(package.read_text(encoding="utf-8"))
            package_signals = any(key in data for key in ("openclaw", "clawhub")) or "openclaw" in json.dumps(data).lower()
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            add(findings, "error", "invalid-package-json", f"package.json is not valid JSON: {exc}")
    if has_skill and (has_plugin or package_signals):
        return "ambiguous"
    if has_skill:
        return "skill"
    if has_plugin or package_signals:
        return "plugin-package"
    return "unknown"


def walk_entries(root: Path) -> Iterable[Path]:
    """Yield every non-root entry without following directory symlinks."""
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = sorted(os.scandir(current), key=lambda entry: entry.name)
        except OSError:
            continue
        for entry in entries:
            path = Path(entry.path)
            yield path
            if entry.is_dir(follow_symlinks=False) and entry.name not in IGNORED_DIRS:
                stack.append(path)


def load_ignore_patterns(root: Path) -> list[tuple[bool, str, str]]:
    patterns: list[tuple[bool, str, str]] = []
    for filename in (".gitignore", ".clawhubignore", ".clawdhubignore"):
        path = root / filename
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            negated = line.startswith("!")
            if negated:
                line = line[1:].strip()
            if line:
                patterns.append((negated, line.replace("\\", "/"), filename))
    return patterns


def pattern_matches(rel: str, pattern: str, is_dir: bool = False) -> bool:
    anchored = pattern.startswith("/")
    pattern = pattern.lstrip("/")
    directory_pattern = pattern.endswith("/")
    pattern = pattern.rstrip("/")
    if not pattern:
        return False
    rel_path = PurePosixPath(rel)
    if "/" not in pattern and not anchored:
        matched = any(PurePosixPath(part).match(pattern) for part in rel_path.parts)
    else:
        matched = rel_path.match(pattern)
    if directory_pattern:
        matched = matched or rel == pattern or rel.startswith(pattern + "/")
        if is_dir and rel_path.match(pattern):
            matched = True
    return matched


def publish_exclusion(rel: str, is_dir: bool, patterns: list[tuple[bool, str, str]], package_type: str) -> str | None:
    parts = PurePosixPath(rel).parts
    if any(part in {".git", ".clawhub", ".clawdhub", "node_modules"} for part in parts):
        return "built-in directory exclusion"
    if any(part.startswith(".") for part in parts):
        return "hidden path excluded by ClawHub skill publishing"
    excluded_by: str | None = None
    for negated, pattern, source in patterns:
        if pattern_matches(rel, pattern, is_dir=is_dir):
            excluded_by = None if negated else f"matched {source}: {pattern}"
    if package_type == "skill" and rel.lower() == "skill-card.md":
        return "generated skill-card.md is stripped by ClawHub CLI"
    return excluded_by


def check_links(path: Path, root: Path, findings: list[dict[str, str]]) -> None:
    if path.suffix.lower() not in {".md", ".markdown"}:
        return
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().strip("<>").split(maxsplit=1)[0].split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#", "data:")):
            continue
        candidate = (path.parent / target).resolve(strict=False)
        try:
            candidate.relative_to(root)
        except ValueError:
            add(findings, "error", "link-outside-root", f"{path.relative_to(root)} links outside the package: {target}")
            continue
        if not candidate.exists():
            add(findings, "error", "missing-reference", f"{path.relative_to(root)} references missing path: {target}")


def check_json(path: Path, root: Path, findings: list[dict[str, str]]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        add(findings, "error", "invalid-json", f"{path.relative_to(root)} is not valid JSON: {exc}")
        return None
    if not isinstance(data, dict):
        add(findings, "error", "invalid-json-root", f"{path.relative_to(root)} must contain a JSON object")
        return None
    return data


def scan_content(content: bytes, label: str, findings: list[dict[str, str]]) -> None:
    for secret_label, pattern in SECRET_PATTERNS:
        if pattern.search(content):
            add(findings, "error", "possible-secret", f"Possible {secret_label} in {label}; value intentionally omitted")
    if PERSONAL_PATH_PATTERN.search(content):
        add(findings, "warning", "personal-path", f"Machine-specific personal path found in {label}")
    if INTERNAL_HOST_PATTERN.search(content):
        add(findings, "warning", "internal-host", f"Local or internal hostname found in {label}")


def safe_archive_name(name: str) -> bool:
    normalized = name.replace("\\", "/")
    parts = PurePosixPath(normalized).parts
    return bool(normalized) and not normalized.startswith("/") and ".." not in parts


def scan_archive(path: Path, root: Path, findings: list[dict[str, str]]) -> None:
    rel = path.relative_to(root).as_posix()
    try:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as archive:
                members = archive.infolist()
                if len(members) > MAX_ARCHIVE_MEMBERS:
                    add(findings, "error", "archive-member-limit", f"Archive has too many members: {rel}")
                    return
                total = 0
                for member in members:
                    if not safe_archive_name(member.filename):
                        add(findings, "error", "unsafe-archive-path", f"Unsafe archive member path in {rel}: {member.filename}")
                        continue
                    mode = member.external_attr >> 16
                    if stat.S_ISLNK(mode):
                        add(findings, "error", "archive-symlink", f"Archive contains symlink: {rel}!{member.filename}")
                        continue
                    if member.is_dir():
                        continue
                    total += member.file_size
                    if member.file_size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                        add(findings, "error", "archive-size-limit", f"Archive expands beyond review limits: {rel}")
                        return
                    scan_content(archive.read(member), f"{rel}!{member.filename}", findings)
            return
        if tarfile.is_tarfile(path):
            with tarfile.open(path, "r:*") as archive:
                members = archive.getmembers()
                if len(members) > MAX_ARCHIVE_MEMBERS:
                    add(findings, "error", "archive-member-limit", f"Archive has too many members: {rel}")
                    return
                total = 0
                for member in members:
                    if not safe_archive_name(member.name):
                        add(findings, "error", "unsafe-archive-path", f"Unsafe archive member path in {rel}: {member.name}")
                        continue
                    if member.issym() or member.islnk():
                        add(findings, "error", "archive-symlink", f"Archive contains link: {rel}!{member.name}")
                        continue
                    if not member.isfile():
                        continue
                    total += member.size
                    if member.size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                        add(findings, "error", "archive-size-limit", f"Archive expands beyond review limits: {rel}")
                        return
                    extracted = archive.extractfile(member)
                    if extracted is not None:
                        scan_content(extracted.read(), f"{rel}!{member.name}", findings)
    except (OSError, zipfile.BadZipFile, tarfile.TarError) as exc:
        add(findings, "warning", "archive-unreadable", f"Could not inspect archive {rel}: {exc}")


def validate_skill_frontmatter(root: Path, findings: list[dict[str, str]]) -> None:
    path = root / "SKILL.md"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        add(findings, "error", "unreadable-skill", f"Cannot read SKILL.md: {exc}")
        return
    if not text.startswith("---\n"):
        add(findings, "error", "missing-frontmatter", "SKILL.md must begin with closed YAML frontmatter")
        return
    end = text.find("\n---", 4)
    if end < 0:
        add(findings, "error", "missing-frontmatter", "SKILL.md must begin with closed YAML frontmatter")
        return
    frontmatter_lines = text[4:end].splitlines()
    fields: dict[str, str] = {}
    block_fields: set[str] = set()
    current_block: str | None = None
    for line in frontmatter_lines:
        if current_block and line[:1].isspace() and line.strip():
            block_fields.add(current_block)
            continue
        current_block = None
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = FRONTMATTER_FIELD.match(line)
        if match:
            key = match.group(1)
            value = (match.group(2) or "").strip().strip("'\"")
            fields[key] = value
            if value in {"|", ">", "|-", ">-", "|+", ">+"}:
                current_block = key
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name:
        add(findings, "error", "missing-frontmatter-field", "SKILL.md frontmatter needs name")
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        add(findings, "error", "invalid-skill-name", "SKILL.md name must be lowercase kebab-case and at most 64 characters")
    if not description or (description.startswith(("|", ">")) and "description" not in block_fields):
        add(findings, "error", "missing-frontmatter-field", "SKILL.md frontmatter needs a non-empty scalar description")


def iter_local_paths(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        if value and not value.startswith(("http://", "https://", "node:", "#")):
            yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from iter_local_paths(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_local_paths(nested)


def validate_plugin(root: Path, findings: list[dict[str, str]]) -> None:
    plugin = check_json(root / "openclaw.plugin.json", root, findings) if (root / "openclaw.plugin.json").exists() else None
    package = check_json(root / "package.json", root, findings) if (root / "package.json").exists() else None
    if package is not None:
        for field in ("name", "version"):
            if not isinstance(package.get(field), str) or not package[field].strip():
                add(findings, "error", "missing-package-field", f"package.json needs a non-empty {field}")
        scripts = package.get("scripts")
        if isinstance(scripts, dict):
            for script_name in sorted(LIFECYCLE_SCRIPTS.intersection(scripts)):
                add(findings, "warning", "lifecycle-script", f"Review package.json lifecycle script before release: {script_name}")
        for section in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
            deps = package.get(section)
            if isinstance(deps, dict):
                for dep, spec in deps.items():
                    if isinstance(spec, str) and (spec.startswith(("git+", "http://", "https://", "file:")) or "github:" in spec):
                        add(findings, "warning", "non-registry-dependency", f"Review {section} source for {dep}")
        for value in (package.get("main"), package.get("module"), package.get("bin"), package.get("exports")):
            for candidate in iter_local_paths(value):
                normalized = candidate.split("?", 1)[0].lstrip("./")
                if normalized and not any(ch in normalized for ch in "*{}") and not (root / normalized).exists():
                    add(findings, "error", "missing-entrypoint", f"package.json references missing entrypoint: {candidate}")
        files = package.get("files")
        if isinstance(files, list):
            for item in files:
                if isinstance(item, str) and not list(root.glob(item)):
                    add(findings, "warning", "unmatched-package-file", f"package.json files entry matches nothing: {item}")
    if plugin is not None and package is not None:
        for field in ("name", "version"):
            if isinstance(plugin.get(field), str) and isinstance(package.get(field), str) and plugin[field] != package[field]:
                add(findings, "error", "manifest-mismatch", f"{field} differs between openclaw.plugin.json and package.json")
    if plugin is not None:
        for key in ("entry", "entrypoint", "main", "skills"):
            if key in plugin:
                for candidate in iter_local_paths(plugin[key]):
                    normalized = candidate.lstrip("./")
                    if normalized and not any(ch in normalized for ch in "*{}") and not (root / normalized).exists():
                        add(findings, "error", "missing-plugin-path", f"openclaw.plugin.json references missing path: {candidate}")


def build_fingerprint(files: list[dict[str, Any]]) -> str:
    # Node's localeCompare sorts case-insensitively for these portable paths.
    payload = "\n".join(
        f"{item['path']}:{item['sha256']}" for item in sorted(files, key=lambda item: item["path"].casefold())
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate(raw_path: str, expected_fingerprint: str | None = None) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    supplied = Path(raw_path).expanduser()
    if not supplied.exists() or not supplied.is_dir():
        return {"path": str(supplied), "type": "unknown", "status": "fail", "files_checked": 0,
                "findings": [{"severity": "error", "code": "not-directory", "message": "Path is not an existing directory"}]}
    if supplied.is_symlink():
        return {"path": str(supplied), "type": "unknown", "status": "fail", "files_checked": 0,
                "findings": [{"severity": "error", "code": "symlink-root", "message": "Package root must not be a symlink"}]}
    root = supplied.resolve()
    package_type = classify(root, findings)
    if package_type == "ambiguous":
        add(findings, "error", "ambiguous-type", "Both Skill and plugin-package markers are present")
    elif package_type == "unknown":
        add(findings, "error", "unknown-type", "No authoritative Skill or plugin-package marker was found")

    ignore_patterns = load_ignore_patterns(root)
    files_checked = 0
    bytes_scanned = 0
    publish_files: list[dict[str, Any]] = []
    excluded_files: list[dict[str, str]] = []
    executable_files: list[str] = []

    for path in walk_entries(root):
        rel = path.relative_to(root).as_posix()
        try:
            mode = path.lstat().st_mode
        except OSError as exc:
            add(findings, "error", "unreadable-entry", f"Cannot stat {rel}: {exc}")
            continue
        if stat.S_ISLNK(mode):
            try:
                target = path.resolve(strict=True)
                target.relative_to(root)
            except (OSError, ValueError):
                add(findings, "error", "unsafe-symlink", f"Symlink is broken or resolves outside the package: {rel}")
            else:
                add(findings, "warning", "symlink", f"Review symlink before release: {rel}")
            continue
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            add(findings, "error", "special-file", f"Non-regular file found: {rel}")
            continue

        files_checked += 1
        size = path.stat().st_size
        if mode & 0o111:
            executable_files.append(rel)
            try:
                with path.open("rb") as handle:
                    header = handle.read(2)
            except OSError:
                header = b""
            if header != b"#!":
                add(findings, "warning", "unexpected-executable", f"Executable file has no script shebang: {rel}")
        if size > MAX_FILE_BYTES:
            add(findings, "error", "large-file", f"File exceeds the 10 MiB skill publish limit: {rel}")
            content = b""
        else:
            try:
                content = path.read_bytes()
            except OSError as exc:
                add(findings, "error", "unreadable-file", f"Cannot read {rel}: {exc}")
                content = b""
            else:
                bytes_scanned += len(content)
                scan_content(content, rel, findings)
                if b"TODO" in content and rel in {"SKILL.md", "openclaw.plugin.json", "package.json"}:
                    add(findings, "warning", "scaffold-marker", f"Release metadata still contains TODO: {rel}")
                check_links(path, root, findings)
                if path.suffix.lower() in {".zip", ".tar", ".tgz", ".gz", ".bz2", ".xz"}:
                    scan_archive(path, root, findings)

        reason = publish_exclusion(rel, False, ignore_patterns, package_type)
        if reason:
            excluded_files.append({"path": rel, "reason": reason})
        elif package_type == "skill" and content:
            publish_files.append({"path": rel, "size": size, "sha256": hashlib.sha256(content).hexdigest()})

    if package_type == "skill":
        validate_skill_frontmatter(root, findings)
        if not any(item["path"].lower() in {"skill.md", "skills.md"} for item in publish_files):
            add(findings, "error", "manifest-excluded", "The publish candidate does not include SKILL.md")
        publish_total = sum(item["size"] for item in publish_files)
        if publish_total > MAX_TOTAL_BYTES:
            add(findings, "error", "total-size-limit", "Skill publish candidate exceeds the 50 MiB total limit")
        fingerprint = build_fingerprint(publish_files)
    else:
        publish_total = None
        fingerprint = None
    if package_type == "plugin-package":
        validate_plugin(root, findings)

    if expected_fingerprint is not None:
        if fingerprint is None:
            add(findings, "error", "fingerprint-unavailable", "Cannot enforce a skill fingerprint for this package type")
        elif fingerprint != expected_fingerprint:
            add(findings, "error", "fingerprint-mismatch", "Publish fingerprint differs from the confirmed release plan")

    severities = {item["severity"] for item in findings}
    status = "fail" if "error" in severities else "warn" if "warning" in severities else "pass"
    return {
        "path": str(root),
        "type": package_type,
        "status": status,
        "files_checked": files_checked,
        "bytes_scanned": bytes_scanned,
        "publish_files": publish_files if package_type == "skill" else None,
        "excluded_files": excluded_files,
        "publish_total_bytes": publish_total,
        "fingerprint": fingerprint,
        "executable_files": executable_files,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Package directory to inspect")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--expect-fingerprint", help="Fail unless the skill publish fingerprint matches this value")
    args = parser.parse_args()
    result = validate(args.path, expected_fingerprint=args.expect_fingerprint)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['status'].upper()}: {result['type']} at {result['path']} ({result['files_checked']} files checked)")
        if result.get("fingerprint"):
            print(f"Publish fingerprint: {result['fingerprint']}")
        for item in result["findings"]:
            print(f"[{item['severity'].upper()}] {item['code']}: {item['message']}")
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
