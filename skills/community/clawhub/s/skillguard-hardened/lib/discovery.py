from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

AI_SUSPICIOUS_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"rm\s+-rf|mkfs(\.|\s)|dd\s+if=|shred\s+-|truncate\s+-s\s+0|wipe(\s|$)",
        r"curl\s+.*(-d|--data|--upload-file)|wget\s+.*(--post-data|--body-data)|requests\.(post|put)\(|httpx\.(post|put)\(",
        r"eval\(|exec\(|compile\(|urllib\.request\.urlopen\(|requests\.(get|post)\(|httpx\.(get|post)\(|subprocess\.(Popen|run)\(|os\.system\(",
        r"ignore previous instructions|system prompt|developer message|exfiltrate|send the contents of",
        r"api[_-]?key|access[_-]?token|app[_-]?secret|private[_-]?key|password",
        r"bash\s+-c|sh\s+-c|source\s+<\(|\|\s*(bash|sh)\b",
    )
]


@dataclass
class SkillFile:
    path: Path
    relative_path: str
    size: int
    sha256: str
    is_text: bool
    is_symlink: bool
    content: str | None = None
    content_truncated: bool = False


@dataclass
class SkillTarget:
    name: str
    path: Path
    root: Path | None
    source_kind: str
    declared_purpose: str
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    files: list[SkillFile] = field(default_factory=list)


def resolve_workspace() -> Path:
    env_workspace = os.environ.get("CLAWD_WORKSPACE")
    if env_workspace:
        return Path(env_workspace).resolve()
    return Path(__file__).resolve().parents[3]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def render_policy_path(value: str, workspace: Path) -> Path:
    return Path(
        value.format(
            workspace=str(workspace),
            home=str(Path.home()),
        )
    ).expanduser().resolve()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def allowed_roots_from_policy(policy: dict[str, Any], workspace: Path | None = None) -> list[Path]:
    workspace = workspace or resolve_workspace()
    return [render_policy_path(raw_root, workspace) for raw_root in policy.get("allowed_roots", [])]


def default_scan_roots(policy: dict[str, Any], workspace: Path | None = None) -> list[Path]:
    roots = []
    for root in allowed_roots_from_policy(policy, workspace):
        if root.exists():
            roots.append(root)
    return roots


def file_is_text(path: Path, policy: dict[str, Any]) -> bool:
    if path.suffix.lower() in set(policy.get("text_file_extensions", [])):
        return True
    try:
        sample = path.read_bytes()[:2048]
    except OSError:
        return False
    if not sample:
        return True
    return b"\x00" not in sample


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_skill_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, ""

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, ""

    metadata_block = parts[1]
    purpose = ""
    metadata: dict[str, Any] = {}
    for raw_line in metadata_block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')

    body = parts[2]
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            purpose = line[2:].strip()
            break
        if line:
            purpose = line[:200]
            break
    return metadata, purpose


def infer_declared_purpose(skill_path: Path) -> tuple[dict[str, Any], str]:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {}, "No SKILL.md found"
    content = read_text(skill_md)
    metadata, purpose = parse_skill_frontmatter(content)
    if purpose:
        return metadata, purpose
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    for line in lines:
        if line.startswith("# "):
            return metadata, line[2:].strip()
    return metadata, (lines[0][:200] if lines else "Undeclared skill purpose")


def _read_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return load_json(path)
    except Exception:  # noqa: BLE001
        return {}


def load_provenance(skill_path: Path) -> dict[str, Any]:
    provenance: dict[str, Any] = {}
    origin_path = skill_path / ".clawhub" / "origin.json"
    meta_path = skill_path / "_meta.json"
    package_path = skill_path / "package.json"

    if origin_path.exists():
        provenance["origin"] = _read_optional_json(origin_path)
    if meta_path.exists():
        provenance["meta"] = _read_optional_json(meta_path)
    if package_path.exists():
        provenance["package"] = _read_optional_json(package_path)
    return provenance


def collect_skill_files(skill_path: Path, policy: dict[str, Any]) -> list[SkillFile]:
    files: list[SkillFile] = []
    max_file_bytes = int(policy.get("size_limits", {}).get("max_file_bytes", 1048576))

    for root, dirs, filenames in os.walk(skill_path, followlinks=False):
        dirs[:] = sorted([name for name in dirs if name not in {".git", "__pycache__"}])
        for filename in sorted(filenames):
            path = Path(root) / filename
            relative_path = str(path.relative_to(skill_path))
            try:
                stat = path.lstat()
            except OSError:
                continue

            is_symlink = path.is_symlink()
            is_text = False if is_symlink else file_is_text(path, policy)
            content = None
            content_truncated = False

            if is_text and not is_symlink:
                try:
                    with path.open("r", encoding="utf-8", errors="ignore") as handle:
                        content = handle.read(max_file_bytes + 1)
                    if len(content) > max_file_bytes:
                        content = content[:max_file_bytes]
                        content_truncated = True
                except OSError:
                    content = None

            try:
                digest = sha256_file(path) if path.is_file() and not is_symlink else ""
            except OSError:
                digest = ""

            files.append(
                SkillFile(
                    path=path,
                    relative_path=relative_path,
                    size=int(stat.st_size),
                    sha256=digest,
                    is_text=is_text,
                    is_symlink=is_symlink,
                    content=content,
                    content_truncated=content_truncated,
                )
            )
    return files


def detect_source_kind(skill_path: Path, workspace: Path) -> str:
    if path_is_within(skill_path, workspace / "skills"):
        return "native"
    if path_is_within(skill_path, workspace / ".skills"):
        return "local"
    if path_is_within(skill_path, Path.home() / ".moltbot" / "skills"):
        return "moltbook"
    return "external"


def build_skill_target(skill_path: Path, policy: dict[str, Any], workspace: Path | None = None) -> SkillTarget:
    workspace = workspace or resolve_workspace()
    skill_path = skill_path.resolve()
    metadata, purpose = infer_declared_purpose(skill_path)
    root = None
    for candidate in allowed_roots_from_policy(policy, workspace):
        if candidate.exists() and path_is_within(skill_path, candidate):
            root = candidate
            break

    return SkillTarget(
        name=skill_path.name,
        path=skill_path,
        root=root,
        source_kind=detect_source_kind(skill_path, workspace),
        declared_purpose=purpose,
        metadata=metadata,
        provenance=load_provenance(skill_path),
        files=collect_skill_files(skill_path, policy),
    )


def discover_skills(
    policy: dict[str, Any],
    roots: list[Path] | None = None,
    workspace: Path | None = None,
) -> list[SkillTarget]:
    workspace = workspace or resolve_workspace()
    roots = roots or default_scan_roots(policy, workspace)
    exclude_names = set(policy.get("exclude_skill_names", []))
    targets: list[SkillTarget] = []

    for root in roots:
        if not root.exists():
            continue
        for entry in sorted(root.iterdir(), key=lambda item: item.name):
            if not entry.is_dir() or entry.name in exclude_names:
                continue
            targets.append(build_skill_target(entry, policy, workspace))

    return targets


def _strip_markdown_code_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def _sanitize_content_for_ai(file_info: SkillFile) -> str:
    content = file_info.content or ""
    if file_info.relative_path.endswith(".md"):
        return _strip_markdown_code_fences(content).strip()
    return content


def _suspicious_line_indexes(text: str) -> list[int]:
    indexes: list[int] = []
    for idx, line in enumerate(text.splitlines()):
        if any(pattern.search(line) for pattern in AI_SUSPICIOUS_PATTERNS):
            indexes.append(idx)
    return indexes


def _excerpt_windows(lines: list[str], indexes: list[int], radius: int = 2, max_windows: int = 6) -> list[tuple[int, int]]:
    windows: list[tuple[int, int]] = []
    for idx in indexes[:max_windows]:
        start = max(0, idx - radius)
        end = min(len(lines), idx + radius + 1)
        if windows and start <= windows[-1][1]:
            windows[-1] = (windows[-1][0], max(windows[-1][1], end))
        else:
            windows.append((start, end))
    return windows


def _compress_for_ai(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text

    lines = text.splitlines()
    suspicious_indexes = _suspicious_line_indexes(text)
    sections: list[str] = []

    if suspicious_indexes:
        for start, end in _excerpt_windows(lines, suspicious_indexes):
            snippet = "\n".join(lines[start:end]).strip()
            if snippet:
                sections.append(f"# suspicious excerpt lines {start + 1}-{end}\n{snippet}")

    if not sections:
        head_budget = max(160, int(limit * 0.65))
        tail_budget = max(120, limit - head_budget - 40)
        head = text[:head_budget].rstrip()
        tail = text[-tail_budget:].lstrip() if tail_budget > 0 else ""
        sections = [head]
        if tail and tail != head:
            sections.append("# tail excerpt\n" + tail)

    compressed = "\n\n".join(section for section in sections if section).strip()
    if len(compressed) <= limit:
        return compressed
    return compressed[: max(0, limit - 18)].rstrip() + "\n# truncated ..."


def _content_for_ai(file_info: SkillFile, limit: int) -> str:
    content = _sanitize_content_for_ai(file_info)
    if not content:
        return ""
    return _compress_for_ai(content, limit)


def _should_include_in_ai_payload(file_info: SkillFile) -> bool:
    relative_path = file_info.relative_path
    if relative_path in {"package.json", "_meta.json", "SKILL.md"}:
        return True
    if relative_path.startswith(("scripts/", "config/")):
        return True
    return file_info.path.suffix.lower() in {".py", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".sh", ".bash", ".zsh", ".json"}


def _file_priority(file_info: SkillFile) -> tuple[int, int, str]:
    relative_path = file_info.relative_path
    content = _sanitize_content_for_ai(file_info)
    suspicious_hits = min(12, len(_suspicious_line_indexes(content)))

    path_score = 10
    if relative_path == "SKILL.md":
        path_score = 120
    elif relative_path in {"package.json", "_meta.json"}:
        path_score = 110
    elif relative_path.startswith("config/"):
        path_score = 100
    elif relative_path.startswith("scripts/"):
        path_score = 95

    truncated_bonus = 5 if file_info.content_truncated else 0
    size_bias = min(20, file_info.size // 2048)
    return (path_score + suspicious_hits * 8 + truncated_bonus + size_bias, suspicious_hits, relative_path)


def build_ai_payload(target: SkillTarget, policy: dict[str, Any]) -> str:
    max_chars = int(policy.get("size_limits", {}).get("max_ai_chars", 12000))
    chosen_files: list[SkillFile] = []

    for preferred in ("SKILL.md", "package.json", "_meta.json"):
        for file_info in target.files:
            if file_info.relative_path == preferred and file_info.is_text:
                chosen_files.append(file_info)

    script_files = [
        file_info
        for file_info in target.files
        if file_info.is_text and file_info.relative_path.startswith("scripts/")
    ]
    for file_info in script_files:
        if file_info not in chosen_files:
            chosen_files.append(file_info)

    for file_info in target.files:
        if file_info.is_text and file_info not in chosen_files and _should_include_in_ai_payload(file_info):
            chosen_files.append(file_info)

    preferred_paths = {"SKILL.md", "package.json", "_meta.json"}
    preferred_files = [file_info for file_info in chosen_files if file_info.relative_path in preferred_paths]
    remaining_files = [file_info for file_info in chosen_files if file_info.relative_path not in preferred_paths]
    remaining_files.sort(key=_file_priority, reverse=True)
    ordered_files = preferred_files + remaining_files

    sections = [
        f"Skill name: {target.name}",
        f"Declared purpose: {target.declared_purpose}",
        f"Source kind: {target.source_kind}",
        "Audit guidance: prioritize executable files and configs; treat documentation examples and placeholder secrets as non-executable context unless mirrored by real code.",
        "Payload assembly: files are prioritized by executable relevance and suspicious indicators, then compressed into excerpts when needed to resist context-smuggling via oversized benign files.",
    ]
    used_chars = sum(len(section) for section in sections)
    per_file_cap = max(700, min(2600, max_chars // 3))

    for file_info in ordered_files:
        remaining_budget = max_chars - used_chars
        if remaining_budget <= 120:
            break
        content_limit = max(240, min(per_file_cap, remaining_budget - 40))
        content = _content_for_ai(file_info, content_limit)
        if not content:
            continue
        section = f"\n--- FILE: {file_info.relative_path} ---\n{content}\n"
        if used_chars + len(section) > max_chars:
            remaining = max_chars - used_chars
            if remaining > 80:
                content = _content_for_ai(file_info, max(120, remaining - 40))
                section = f"\n--- FILE: {file_info.relative_path} ---\n{content}\n"
                section = section[:remaining]
                sections.append(section)
            break
        sections.append(section)
        used_chars += len(section)

    return "\n".join(sections)
