"""
rebrand — Generic rebrand pipeline.

Transforms an internal source directory into a public destination directory
suitable for publication (marketplace, open-source, multi-tenant).

Operations (in order):
  1. Copy .py, .md, LICENSE, *.json, *.yaml from source → destination
  2. Strip jargon (configurable patterns)
  3. Fix hardcoded sys.path inserts in test files
  4. Regenerate MANIFEST.txt with SHA-256 hashes
  5. Validate via custom validator (if provided)
  6. Return byte-to-byte audit report

Idempotent: running twice produces identical output (modulo timestamps).
Pure Python stdlib, zero dependencies.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

__version__ = "0.1.5"

# Default jargon patterns to strip — GENERIC ONLY (safe for any project).
# Cluster/org/codename patterns are NOT in defaults.
# Load them via --config examples/cluster-jargon.yaml if you need them.
DEFAULT_JARGON_PATTERNS = [
    # Generic author/creator/team mentions (line-start + inline)
    (re.compile(r'^#?\s*Auteur[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'\*?\*?Author[:\s][^\n]*', re.MULTILINE), ""),
    (re.compile(r'\*?\*?Auteur[:\s][^\n]*', re.MULTILINE), ""),
    (re.compile(r'^#?\s*Created by:[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'\*?\*?Created by[:\s][^\n]*', re.MULTILINE), ""),
    (re.compile(r'^#?\s*Lead:[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'^#?\s*To validate:[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'^#?\s*Validated by:[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'^#?\s*Status:[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'^#?\s*Date:[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'^#?\s*License:[^\n]*\n', re.MULTILINE), ""),
    # Internal codename/version markers (generic)
    (re.compile(r'\(premier jet\)'), ""),
    (re.compile(r'\(PREMIER JET\)'), ""),
    (re.compile(r'\bfirst draft\b'), "first version"),
    (re.compile(r'\bpremier jet\b'), "first version"),
    # Path: hardcoded internal paths (auto-detect)
    (re.compile(r'^Path:\s+/[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'^\*\*Path:\*\*\s+`/[^\n]*\n', re.MULTILINE), ""),
    # Latin club mottos (and similar flair) — generic catch-all
    (re.compile(r'^[#]?\s*_In Altum[^\n]*\n', re.MULTILINE), ""),
    (re.compile(r'\bIn\s+Altum\b', re.IGNORECASE), ""),  # mid-line + line-start
]

# SENSITIVE patterns (cluster/org/codename) — NOT in defaults.
# Load via --config examples/cluster-jargon.yaml ONLY if you know what you're doing.
# These can destroy innocent code (e.g. a user with a file named merlin.py).
SENSITIVE_PATTERN_NAMES = {
    "cluster_codename",  # matches "cluster X Stellaris/Hub/Group/Team"
    "l9_hub",            # matches "L9 Hub" (could be legitimate product name)
    "agent_emoji",       # matches 🐺/🌬️ (could appear in test data)
    "axioma_stellaris",  # matches "Axioma Stellaris" (any casing)
}

# Default file exclude patterns
DEFAULT_EXCLUDE_PATTERNS = [
    re.compile(r'\.auto\.md$'),       # editor backup files
    re.compile(r'\.pyc$'),            # Python bytecode
    re.compile(r'__pycache__'),       # Python cache dirs
    re.compile(r'\.swp$'),            # Vim swap files
    re.compile(r'\.bak$'),            # Generic backups
    re.compile(r'\.orig$'),           # Git merge backups
    re.compile(r'^\.DS_Store$'),      # macOS metadata
    re.compile(r'^ORCHESTRATION\.md$'),  # internal task tracker
    re.compile(r'^INTERNAL[_-].*'),   # internal-* files
    re.compile(r'^MANIFEST\.txt$'),   # regenerated from scratch
]


def sha256_file(path: Path) -> str:
    """Compute SHA-256 of a file (byte-to-byte)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jargon_from_config(config_path: Path) -> List[Tuple[re.Pattern, str]]:
    """Load jargon patterns from a config file.

    Supports 3 formats, auto-detected by extension then content:
    - `.yaml` / `.yml` → YAML structured (requires PyYAML)
    - `.json` → JSON structured
    - other / no extension → line-based (`pattern:replacement` per line)
    """
    with open(config_path) as f:
        content = f.read()
    
    suffix = config_path.suffix.lower()
    
    # Extension-based detection (Souleymane's BUG #1 fix)
    if suffix in (".yaml", ".yml"):
        try:
            import yaml
            data = yaml.safe_load(content)
        except ImportError:
            raise RuntimeError(
                "PyYAML is required for YAML config. "
                "Install with: pip install PyYAML"
            )
    elif suffix == ".json" or content.strip().startswith("{"):
        # Try YAML first (superset of JSON), fall back to json
        try:
            import yaml
            data = yaml.safe_load(content)
        except ImportError:
            data = json.loads(content)
    else:
        # Line-based fallback
        patterns = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                pat, _, rep = line.partition(":")
                patterns.append((re.compile(pat), rep))
        return patterns
    
    # Structured format (YAML or JSON)
    if not isinstance(data, dict):
        return []
    
    patterns = []
    for entry in data.get("jargon", []):
        if isinstance(entry, dict):
            patterns.append((re.compile(entry["pattern"]), entry.get("replacement", "")))
        elif isinstance(entry, str):
            patterns.append((re.compile(entry), ""))
    return patterns


def strip_jargon(text: str, patterns: Optional[List] = None) -> Tuple[str, int]:
    """Remove jargon from a string. Returns (cleaned, n_stripped)."""
    patterns = patterns or DEFAULT_JARGON_PATTERNS
    n = 0
    for pattern, replacement in patterns:
        new_text, count = pattern.subn(replacement, text)
        if count > 0:
            text = new_text
            n += count
    return text, n


def fix_sys_path(text: str) -> Tuple[str, int]:
    """Replace hardcoded sys.path.insert with Path(__file__).parent.
    Returns (fixed, n_fixed)."""
    pattern = re.compile(
        r'sys\.path\.insert\(\s*0\s*,\s*[\"\'][^\"\']*[\"\']\s*\)'
    )
    new_text, count = pattern.subn(
        'sys.path.insert(0, str(Path(__file__).parent))',
        text
    )
    if count > 0 and "from pathlib import Path" not in new_text:
        lines = new_text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                lines.insert(i, "from pathlib import Path")
                new_text = "\n".join(lines)
                break
    return new_text, count


def remove_blank_lines_excess(text: str) -> str:
    """Remove runs of 3+ blank lines down to 2 (clean docstring format)."""
    return re.sub(r'\n{4,}', '\n\n\n', text)


def rebrand_file(src: Path, dst: Path, patterns: Optional[List] = None, *, dry_run: bool = False) -> Dict:
    """Copy a file from src to dst, stripping jargon and fixing paths.
    Returns audit info."""
    content = src.read_text(encoding="utf-8", errors="replace")
    original_size = len(content.encode("utf-8"))
    
    cleaned, n_jargon = strip_jargon(content, patterns)
    cleaned, n_path = fix_sys_path(cleaned)
    cleaned = remove_blank_lines_excess(cleaned)
    
    new_size = len(cleaned.encode("utf-8"))
    
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        # Force write: even if content is identical, ensure file exists
        dst.write_text(cleaned, encoding="utf-8")
    
    return {
        "file": src.name,
        "src_size": original_size,
        "dst_size": new_size,
        "jargon_lines_stripped": n_jargon,
        "sys_path_fixed": n_path,
        "modified": cleaned != content,
    }


def regenerate_manifest(dst_dir: Path, project_name: str) -> Path:
    """Regenerate MANIFEST.txt with SHA-256 of all files in dst_dir.

    Akasha-style: NO timestamp, NO random, NO env-dependent content.
    Same input → same output, byte-to-byte, forever.
    """
    manifest = dst_dir / "MANIFEST.txt"
    lines = [
        f"# Manifest — {project_name} (public)",
        f"# Generated by axiom-rebrand v{__version__}",
        "",
    ]
    for f in sorted(dst_dir.iterdir()):
        if f.is_file() and f.name != "MANIFEST.txt":
            h = sha256_file(f)
            size = f.stat().st_size
            lines.append(f"{h}  {f.name}  ({size} bytes)")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def validate(dst_dir: Path, validator: Path) -> bool:
    """Run a custom validator on dst_dir. Returns True if it passes."""
    try:
        result = subprocess.run(
            [sys.executable, str(validator), str(dst_dir)],
            capture_output=True, text=True, timeout=30
        )
        # Generic: any "OK" or "100" or "PASS" in output
        output = (result.stdout + result.stderr).upper()
        return any(marker in output for marker in ["100/100", "OK", "PASS", "ALL GREEN"])
    except Exception:
        return False


def run_tests(dst_dir: Path) -> bool:
    """Run all test_*.py in dst_dir. Returns True if all OK."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(dst_dir), "-p", "test_*.py"],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout.strip().endswith("OK")
    except Exception:
        return False


def rebrand_project(
    src_root: Path,
    dst_root: Path,
    project_name: Optional[str] = None,
    *,
    validator: Optional[Path] = None,
    patterns: Optional[List] = None,
    exclude: Optional[List] = None,
    dry_run: bool = False,
    skip_validate: bool = False,
) -> Dict:
    """
    Rebrand an entire project directory.
    
    Returns an audit report with byte-to-byte info.
    """
    src_root = Path(src_root)
    dst_root = Path(dst_root)
    project_name = project_name or src_root.name
    
    if not src_root.exists():
        return {"error": f"Source not found: {src_root}"}
    
    exclude_patterns = exclude or DEFAULT_EXCLUDE_PATTERNS
    
    file_audits = []
    skills_processed = 0
    
    for src_path in sorted(src_root.rglob("*")):
        if not src_path.is_file():
            continue
        # Skip excluded files
        if any(p.search(src_path.name) for p in exclude_patterns):
            continue
        # Compute relative path
        rel = src_path.relative_to(src_root)
        dst_path = dst_root / rel
        audit = rebrand_file(src_path, dst_path, patterns=patterns, dry_run=dry_run)
        file_audits.append(audit)
    
    # Generate manifest in dst_root (top-level)
    if not dry_run:
        manifest = regenerate_manifest(dst_root, project_name)
        manifest_hash = sha256_file(manifest)
    else:
        manifest_hash = None
    
    # Validate
    if not dry_run and not skip_validate and validator:
        tests_ok = run_tests(dst_root)
        valid_ok = validate(dst_root, validator)
    else:
        tests_ok = None
        valid_ok = None
    
    return {
        "project": project_name,
        "project_name": project_name,  # duplicate for --name CLI compat
        "src": str(src_root),
        "dst": str(dst_root),
        "files": file_audits,
        "files_count": len(file_audits),
        "manifest_hash": manifest_hash,
        "tests_ok": tests_ok,
        "valid_ok": valid_ok,
        "dry_run": dry_run,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="axiom-rebrand: Generic rebrand pipeline (Akasha-style)"
    )
    parser.add_argument("--src", type=Path, required=True,
                        help="Source directory to rebrand from")
    parser.add_argument("--dst", type=Path, required=True,
                        help="Destination directory to write rebranded output")
    parser.add_argument("--name", type=str, default=None,
                        help="Project name (defaults to src basename)")
    parser.add_argument("--config", type=Path, default=None,
                        help="Optional YAML/JSON config with custom jargon patterns")
    parser.add_argument("--validator", type=Path, default=None,
                        help="Optional validator script (e.g. axiom_check.py)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Don't write, just report what would change")
    parser.add_argument("--skip-validate", action="store_true",
                        help="Skip tests + validator (faster)")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON report")
    parser.add_argument("--include-sensitive", action="store_true",
                        help="Include cluster/org/codename patterns (risky, use only if you know what you're doing)")
    parser.add_argument("--version", action="version", version=f"axiom-rebrand v{__version__}")
    args = parser.parse_args(argv)

    # Load patterns from config if provided
    # IMPORTANT: We MERGE with defaults, not replace them.
    # (Defaults are safe for any project; config/sensitive add cluster-specific ones.)
    extra_patterns = None
    if args.config:
        extra_patterns = load_jargon_from_config(args.config)
    elif args.include_sensitive:
        # Load sensitive patterns from bundled examples
        sensitive_config = Path(__file__).parent.parent / "examples" / "cluster-jargon.yaml"
        if sensitive_config.exists():
            extra_patterns = load_jargon_from_config(sensitive_config)
        else:
            print(f"  ⚠️  Sensitive config not found: {sensitive_config}")

    # Merge: defaults + extra (extras are APPENDED)
    if extra_patterns:
        patterns = list(DEFAULT_JARGON_PATTERNS) + list(extra_patterns)
    else:
        patterns = list(DEFAULT_JARGON_PATTERNS)

    # Dry-run warning if sensitive patterns loaded
    if extra_patterns and not args.dry_run and not args.json:
        sensitive_count = sum(1 for p, _ in extra_patterns if any(
            s in (p.pattern if hasattr(p, 'pattern') else str(p))
            for s in ["Axioma", "L9", "Stellaris", "\U0001f43a", "\U0001f32c"]
        ))
        if sensitive_count > 0:
            print(f"  ⚠️  Loaded {sensitive_count} sensitive pattern(s) (cluster/org/codename).")
            print(f"  ⚠️  These can destroy innocent code. Use --dry-run first to preview.")

    report = rebrand_project(
        args.src, args.dst, project_name=args.name,
        validator=args.validator, patterns=patterns,
        dry_run=args.dry_run, skip_validate=args.skip_validate,
    )

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("═" * 55)
        print(f"  🔄 axiom-rebrand v{__version__}")
        print("═" * 55)
        print(f"  Source:      {args.src}")
        print(f"  Destination: {args.dst}")
        print(f"  Dry run:     {args.dry_run}")
        print()
        
        if "error" in report:
            print(f"  ❌ {report['error']}")
            return 1
        
        files = report["files"]
        modified = sum(1 for f in files if f["modified"])
        jargon = sum(f["jargon_lines_stripped"] for f in files)
        paths = sum(f["sys_path_fixed"] for f in files)
        
        print(f"  Files processed: {len(files)}")
        print(f"  Files modified:  {modified}")
        print(f"  Jargon lines stripped: {jargon}")
        print(f"  sys.path fixed:  {paths}")
        
        if report.get("valid_ok") is not None:
            if report["valid_ok"] and report.get("tests_ok"):
                print(f"  ✅ Validation + tests OK")
            else:
                print(f"  ⚠️  Validation/tests failed (valid={report.get('valid_ok')}, tests={report.get('tests_ok')})")
        
        if not args.dry_run and report.get("manifest_hash"):
            print(f"  📦 MANIFEST SHA-256: {report['manifest_hash'][:16]}...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
