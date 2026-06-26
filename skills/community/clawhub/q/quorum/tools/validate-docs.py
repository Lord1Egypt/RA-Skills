#!/usr/bin/env python3
"""
validate-docs.py — Detect stale documentation against critic-status.yaml.

Reads the manifest, counts shipped critics, and scans all public .md files for:
  1. Hardcoded critic counts that don't match shipped count
  2. Status markers (🔜, "Planned", "coming") for critics that are actually shipped
  3. "What's coming" / roadmap references to shipped features

Exit codes:
  0 = clean (no findings)
  1 = findings detected
  2 = error (missing manifest, bad YAML, etc.)

Companion rubric:
  This script handles deterministic mechanical checks (counts, versions, status markers).
  For semantic and narrative evaluation (claim accuracy, navigation coherence, onboarding
  progression, boundary discipline), use the Documentation Quality Rubric:
    rubrics/builtin/documentation.json
  Run this script FIRST — its output serves as evidence for DOC-002, DOC-003, and DOC-005.
"""

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

# Maximum file size to process (1 MB) — guards against oversized files in regex operations
MAX_FILE_SIZE_BYTES = 1_048_576

# Maximum characters displayed per line in finding messages
MAX_LINE_DISPLAY_CHARS = 120


def load_manifest(repo_root: Path) -> dict[str, Any]:
    """Load and parse critic-status.yaml with structural validation."""
    manifest_path = repo_root / "critic-status.yaml"
    if not manifest_path.exists():
        print(f"ERROR: {manifest_path} not found", file=sys.stderr)
        sys.exit(2)

    try:
        with open(manifest_path, encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"ERROR: Failed to parse {manifest_path}: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(manifest, dict):
        print(f"ERROR: {manifest_path} must be a YAML mapping, got {type(manifest).__name__}", file=sys.stderr)
        sys.exit(2)

    if "critics" not in manifest or not isinstance(manifest["critics"], dict):
        print(f"ERROR: {manifest_path} must contain a 'critics' mapping", file=sys.stderr)
        sys.exit(2)

    # Validate each critic entry has at least a 'status' field
    for name, info in manifest["critics"].items():
        if not isinstance(info, dict) or "status" not in info:
            print(
                f"ERROR: Critic '{name}' in {manifest_path} must be a mapping with a 'status' field",
                file=sys.stderr,
            )
            sys.exit(2)

    return manifest


def get_critics_by_status(manifest: dict[str, Any], status: str) -> dict[str, dict[str, Any]]:
    """Return dict of critic_name -> info for all critics matching the given status."""
    return {
        name: info
        for name, info in manifest.get("critics", {}).items()
        if info.get("status") == status
    }


def find_md_files(repo_root: Path) -> list[Path]:
    """Find all .md files in the repo, excluding dirs that shouldn't be validated."""
    exclude_dirs = {
        "venv", "node_modules", ".git", "quorum-runs", "__pycache__", "dist",
        ".hypothesis", "external-reviews", "reviews",  # external reviews are point-in-time snapshots
    }
    exclude_files = {
        "SHIPPING.md",      # contains historical context about the problem
        "CHANGELOG.md",     # historical entries reflect state at time of release
    }
    results = []
    for p in repo_root.rglob("*.md"):
        parts = set(p.relative_to(repo_root).parts)
        if not parts & exclude_dirs and p.name not in exclude_files:
            results.append(p)
    return sorted(results)


def read_file_lines(file_path: Path) -> list[str] | None:
    """Read a markdown file and return its lines, or None on failure.

    Skips files exceeding MAX_FILE_SIZE_BYTES to guard against oversized inputs.
    """
    try:
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE_BYTES:
            print(
                f"WARNING: Skipping {file_path} ({file_size} bytes exceeds "
                f"{MAX_FILE_SIZE_BYTES} byte limit)",
                file=sys.stderr,
            )
            return None
        return file_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as e:
        print(f"WARNING: Could not decode {file_path} as UTF-8: {e}", file=sys.stderr)
        return None
    except OSError as e:
        print(f"WARNING: Could not read {file_path}: {e}", file=sys.stderr)
        return None


def check_hardcoded_counts(
    lines: list[str], shipped_count: int, total_count: int, file_path: Path,
) -> list[str]:
    """Flag lines with hardcoded critic counts that don't match shipped count."""
    findings: list[str] = []
    # Match patterns like "4 critics", "ships with 4", "currently 5 critics"
    count_pattern = re.compile(r'\b(\d+)\s+critics?\b', re.IGNORECASE)
    # Also match "ships with N", "ships N critics"
    ships_pattern = re.compile(r'ship[s]?\s+(?:with\s+)?(\d+)', re.IGNORECASE)
    # Also match "N/9 critics" or "N of 9 critics"
    fraction_pattern = re.compile(r'\b(\d+)\s*[/]\s*9\s+critics?\b', re.IGNORECASE)
    # Also match "N/9" in context of shipped/implemented
    fraction_shipped_pattern = re.compile(r'\b(\d+)\s*[/]\s*9\s+(?:critics?\s+)?(?:shipped|implemented|live|built)', re.IGNORECASE)

    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        # Skip lines that are clearly talking about the target architecture (e.g., "9 critics total")
        # But don't skip lines with fraction patterns like "4/9 critics shipped"
        if re.search(r'\b9\s+critics?\b', line, re.IGNORECASE) and \
           ("target" in line_lower or "full" in line_lower) and \
           not re.search(r'\d+\s*/\s*9', line):
            continue
        # Skip lines about thread pool / parallel limits (e.g., "max 4 critics in parallel")
        # But don't skip lines with fraction patterns like "4/9 critics"
        if ("parallel" in line_lower or "threadpool" in line_lower or "max" in line_lower) \
           and not re.search(r'\d+\s*/\s*9', line):
            continue

        # Flag ANY "N/9 critics" or "N of 9" fraction — policy: never expose total target count
        fraction_found = False
        for frac_pat in [fraction_pattern, fraction_shipped_pattern]:
            for match in frac_pat.finditer(line):
                if not fraction_found:
                    findings.append(
                        f"  {file_path}:{i}: Remove target denominator "
                        f"(policy: don't expose total planned count): "
                        f"{line.strip()[:MAX_LINE_DISPLAY_CHARS]}"
                    )
                    fraction_found = True

        for pattern in [count_pattern, ships_pattern]:
            for match in pattern.finditer(line):
                n = int(match.group(1))
                # Only flag if it looks like a shipped count that's wrong
                # Skip 9 (total architecture), 3 (planned), and the correct count
                if n != shipped_count and n != total_count and 2 <= n <= total_count:
                    # Skip lines about specific depth profiles with intentionally fewer critics
                    # (e.g., "quick" depth legitimately runs 2 critics)
                    if "quick" in line_lower and n == 2:
                        continue
                    if any(kw in line_lower for kw in [
                        "ship", "current", "today", "implement", "available",
                        "standard", "have", "run"
                    ]):
                        findings.append(
                            f"  {file_path}:{i}: Hardcoded count '{match.group(0)}' "
                            f"(shipped={shipped_count}): {line.strip()[:MAX_LINE_DISPLAY_CHARS]}"
                        )
    return findings


def check_stale_status_markers(
    lines: list[str], shipped_critics: dict[str, dict[str, Any]], file_path: Path
) -> list[str]:
    """Flag status markers (🔜, Planned, coming) for critics that are actually shipped."""
    findings: list[str] = []
    # Also add display names
    display_map = {
        "cross.consistency": "cross_consistency",
        "cross.artifact": "cross_consistency",
        "code.hygiene": "code_hygiene",
    }

    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        # Check if line has a stale marker
        has_stale_marker = any(marker in line for marker in ["🔜", "Planned", "planned", "coming"])
        if not has_stale_marker:
            continue
        # Skip lines that also say "shipped" or "implemented" (describing current state)
        if any(kw in line_lower for kw in ["shipped", "implemented", "✅"]):
            continue

        # Check if line references a shipped critic by distinctive name
        # Skip generic words like "security", "correctness" that appear in other contexts
        distinctive_shipped = {
            name: info for name, info in shipped_critics.items()
            if name not in ("security", "correctness", "completeness")
        }
        distinctive_names = {
            name.replace("_", "[ _-]?"): name
            for name in distinctive_shipped
        }
        # Filter display_map to only include aliases for actually-shipped critics
        shipped_display_entries = [
            (k, v) for k, v in display_map.items()
            if v in shipped_critics
        ]
        for pattern_name, canonical_name in list(distinctive_names.items()) + shipped_display_entries:
            if re.search(pattern_name, line_lower) or canonical_name.replace("_", " ") in line_lower:
                findings.append(
                    f"  {file_path}:{i}: Stale marker for shipped critic "
                    f"'{canonical_name}': {line.strip()[:MAX_LINE_DISPLAY_CHARS]}"
                )
                break

    return findings


def check_roadmap_shipped(
    lines: list[str], shipped_critics: dict[str, dict[str, Any]], file_path: Path
) -> list[str]:
    """Flag 'roadmap' or 'what's coming' sections that list shipped critics."""
    findings: list[str] = []
    in_roadmap = False
    # Only check for critic names that are distinctive enough to not be common words.
    # "security" and "correctness" are too generic — they appear in rubric domain
    # descriptions, improvement roadmaps, etc. without referring to the critic.
    shipped_lower = {"tester", "cross-consistency", "cross consistency", "cross artifact", "code hygiene"}

    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        # Detect roadmap/coming sections
        if any(kw in line_lower for kw in ["what's coming", "roadmap", "what is coming", "planned"]):
            if line.startswith("#") or line.startswith("**"):
                in_roadmap = True
                continue
        # Exit roadmap section on next heading
        if in_roadmap and line.startswith("#") and "coming" not in line_lower and "roadmap" not in line_lower:
            in_roadmap = False

        if in_roadmap:
            for critic_name in shipped_lower:
                if critic_name in line_lower:
                    findings.append(
                        f"  {file_path}:{i}: Shipped critic '{critic_name}' listed in "
                        f"roadmap/coming section: {line.strip()[:MAX_LINE_DISPLAY_CHARS]}"
                    )
                    break

    return findings


def _extract_pyproject_version(content: str) -> str | None:
    """Extract the version string from pyproject.toml content (pure)."""
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    return match.group(1) if match else None


def _extract_badge_versions(content: str) -> list[str]:
    """Extract version strings from badge markup in README content (pure)."""
    badge_pattern = re.compile(r'badge[/](?:version-)?v?(\d+\.\d+\.\d+)')
    return [m.group(1) for m in badge_pattern.finditer(content)]


def check_version_consistency(repo_root: Path, manifest_version: str) -> list[str]:
    """Check that version strings across the repo match the manifest version."""
    findings: list[str] = []

    pyproject = repo_root / "reference-implementation" / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text(encoding="utf-8")
            pyproject_ver = _extract_pyproject_version(content)
            if pyproject_ver and pyproject_ver != manifest_version:
                findings.append(
                    f"  pyproject.toml: version=\"{pyproject_ver}\" "
                    f"(manifest={manifest_version})"
                )
        except OSError:
            pass

    readme = repo_root / "README.md"
    if readme.exists():
        try:
            content = readme.read_text(encoding="utf-8")
            for badge_ver in _extract_badge_versions(content):
                if badge_ver != manifest_version:
                    findings.append(
                        f"  README.md: badge version \"{badge_ver}\" "
                        f"(manifest={manifest_version})"
                    )
        except OSError:
            pass

    return findings


def check_depth_config_claims(
    lines: list[str], manifest: dict[str, Any], file_path: Path
) -> list[str]:
    """Flag claims about depth configs that don't match the manifest."""
    findings: list[str] = []
    depth_configs = manifest.get("depth_configs", {})
    if not depth_configs:
        return findings

    callable_critics = {
        name for name, info in manifest.get("critics", {}).items()
        if info.get("callable", False)
    }
    callable_count = len(callable_critics)

    for i, line in enumerate(lines, 1):
        line_lower = line.lower()

        # Check for "standard: N critics" or "standard depth runs N"
        for depth_name, critic_list in depth_configs.items():
            depth_pattern = re.compile(
                rf'{depth_name}\s*[:=|—–-]\s*(\d+)\s+critics?',
                re.IGNORECASE
            )
            for match in depth_pattern.finditer(line):
                claimed = int(match.group(1))
                actual = len(critic_list)
                if claimed != actual:
                    findings.append(
                        f"  {file_path}:{i}: {depth_name} depth claims "
                        f"{claimed} critics (actual={actual}): "
                        f"{line.strip()[:MAX_LINE_DISPLAY_CHARS]}"
                    )

    return findings


# ── Framework version header staleness ────────────────────────────────────────

# File basenames where version headers are expected and should be current
_FRAMEWORK_DOC_SUFFIXES = ("_FRAMEWORK.md", "IMPLEMENTATION.md", "TESTER_CRITIC_BRIEF.md")

_RE_VERSION_HEADER = re.compile(
    r"""
    (?:
        \*{2}v(\d+\.\d+\.\d+)\s+(?:State|Status)          # **v0.5.1 State
      | \#{1,4}\s+v(\d+\.\d+\.\d+)\s+(?:State|Status)     # ## v0.5.1 Status
      | Status\s*\(v(\d+\.\d+\.\d+)\)                       # Status (v0.5.1)
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)


def check_framework_version_strings(
    lines: list[str], manifest_version: str, file_path: Path
) -> list[str]:
    """Flag version strings in framework docs that don't match the manifest.

    Only applies to files whose name ends with a known framework suffix.
    Skips version strings inside fenced code blocks.
    """
    name = str(file_path)
    if not any(name.endswith(s) for s in _FRAMEWORK_DOC_SUFFIXES):
        return []

    findings: list[str] = []
    in_code_block = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        m = _RE_VERSION_HEADER.search(line)
        if m:
            found_version = next(g for g in m.groups() if g is not None)
            if found_version != manifest_version:
                findings.append(
                    f"  {file_path}:{i}: Stale version header "
                    f"'v{found_version}' (manifest={manifest_version}): "
                    f"{line.strip()[:MAX_LINE_DISPLAY_CHARS]}"
                )

    return findings


def validate_docs(repo_root: Path) -> list[str]:
    """Run all validation checks and return list of findings."""
    manifest = load_manifest(repo_root)
    shipped = get_critics_by_status(manifest, "shipped")
    shipped_count = len(shipped)
    total_count = len(manifest.get("critics", {}))
    manifest_version = manifest.get("version", "unknown")

    md_files = find_md_files(repo_root)

    all_findings: list[str] = []

    # Version consistency check
    version_findings = check_version_consistency(repo_root, manifest_version)
    if version_findings:
        all_findings.append("VERSION MISMATCH:")
        all_findings.extend(version_findings)

    for md_file in md_files:
        lines = read_file_lines(md_file)
        if lines is None:
            continue

        rel_path = md_file.relative_to(repo_root)
        all_findings.extend(check_hardcoded_counts(lines, shipped_count, total_count, rel_path))
        all_findings.extend(check_stale_status_markers(lines, shipped, rel_path))
        all_findings.extend(check_roadmap_shipped(lines, shipped, rel_path))
        all_findings.extend(check_depth_config_claims(lines, manifest, rel_path))
        all_findings.extend(check_framework_version_strings(lines, manifest_version, rel_path))

    return all_findings


def main() -> int:
    """Entry point. Returns exit code: 0=clean, 1=findings, 2=error."""
    # Find repo root (script is in tools/)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    # Print manifest summary for human readers
    manifest = load_manifest(repo_root)
    shipped = get_critics_by_status(manifest, "shipped")
    planned = get_critics_by_status(manifest, "planned")
    manifest_version = manifest.get("version", "unknown")

    callable_critics = {
        name for name, info in manifest.get("critics", {}).items()
        if info.get("callable", False)
    }
    depth_configs = manifest.get("depth_configs", {})

    print(f"Manifest version: {manifest_version}")
    print(f"Shipped critics ({len(shipped)}): {', '.join(shipped.keys())}")
    print(f"Callable critics ({len(callable_critics)}): {', '.join(sorted(callable_critics))}")
    print(f"Planned critics ({len(planned)}): {', '.join(planned.keys())}")
    if depth_configs:
        for depth_name, critic_list in depth_configs.items():
            print(f"  {depth_name}: {len(critic_list)} critics ({', '.join(critic_list)})")
    print()

    md_files = find_md_files(repo_root)
    print(f"Scanning {len(md_files)} markdown files...\n")

    # Delegate validation logic (no duplication with validate_docs())
    all_findings = validate_docs(repo_root)

    if all_findings:
        print(f"FINDINGS ({len(all_findings)}):\n")
        for finding in all_findings:
            print(finding)
        print(f"\n❌ {len(all_findings)} documentation discrepancies found.")
        print("Update the listed files to match critic-status.yaml, then re-run.")
        return 1

    print("✅ All documentation matches critic-status.yaml. No stale references found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
