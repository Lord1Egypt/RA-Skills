#!/usr/bin/env python3
"""Stage 2: scan the cloned repo for structure, manifests, entry points."""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

LANG_EXT = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go",
    ".java": "Java", ".kt": "Kotlin", ".rs": "Rust",
    ".rb": "Ruby", ".php": "PHP", ".cs": "C#",
    ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++",
    ".swift": "Swift", ".m": "Objective-C", ".scala": "Scala",
    ".sh": "Shell", ".vue": "Vue", ".svelte": "Svelte",
}

MANIFEST_FILES = {
    "package.json", "pyproject.toml", "requirements.txt", "setup.py",
    "go.mod", "pom.xml", "build.gradle", "Cargo.toml", "Gemfile",
    "composer.json", "Dockerfile", "docker-compose.yml",
    "docker-compose.yaml", ".github/workflows", "Makefile",
}

ENTRY_PATTERNS = [
    r"^main\.(py|go|rs|js|ts)$",
    r"^index\.(js|ts|jsx|tsx)$",
    r"^app\.(py|js|ts)$",
    r"^cli\.(py|js|ts)$",
    r"^server\.(py|js|ts|go)$",
    r"^manage\.py$",
]

IGNORE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    "dist", "build", "target", ".next", ".nuxt", "coverage",
    ".pytest_cache", ".mypy_cache", "vendor",
}


def walk_tree(root: Path, max_depth: int = 4):
    tree = {}
    file_counts = Counter()
    lang_loc = Counter()
    manifests = []
    entry_candidates = []
    all_files = []

    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        depth = len(rel.parts)
        # prune
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        if depth > max_depth:
            dirnames[:] = []
            continue

        file_counts[str(rel) or "."] = len(filenames)
        for fn in filenames:
            fp = Path(dirpath) / fn
            relfp = fp.relative_to(root)
            all_files.append(str(relfp))
            ext = fp.suffix.lower()
            if ext in LANG_EXT:
                try:
                    with open(fp, "rb") as f:
                        loc = sum(1 for _ in f)
                    lang_loc[LANG_EXT[ext]] += loc
                except Exception:
                    pass
            if fn in MANIFEST_FILES or fn.startswith("Dockerfile"):
                manifests.append(str(relfp))
            for pat in ENTRY_PATTERNS:
                if re.match(pat, fn):
                    entry_candidates.append(str(relfp))
                    break

    # build a compact tree (top 2 levels only for display)
    compact = defaultdict(list)
    for f in all_files:
        parts = f.split("/")
        if len(parts) == 1:
            compact["."].append(parts[0])
        else:
            compact[parts[0]].append("/".join(parts[1:]))

    return {
        "total_files": len(all_files),
        "language_loc": dict(lang_loc.most_common()),
        "manifests": manifests,
        "entry_candidates": entry_candidates,
        "top_level": sorted(compact.keys()),
        "file_count_per_dir": dict(file_counts.most_common(20)),
    }


def read_readme(root: Path) -> str:
    for name in ("README.md", "README.rst", "README.txt", "readme.md", "README"):
        p = root / name
        if p.exists():
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
                lines = txt.splitlines()[:300]
                return "\n".join(lines)
            except Exception:
                pass
    return ""


def parse_manifests(root: Path, manifests: list[str]) -> dict:
    deps = {}
    for m in manifests:
        p = root / m
        if not p.is_file():
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if m.endswith("package.json"):
            try:
                obj = json.loads(content)
                deps[m] = {
                    "dependencies": list((obj.get("dependencies") or {}).keys()),
                    "devDependencies": list((obj.get("devDependencies") or {}).keys()),
                    "scripts": list((obj.get("scripts") or {}).keys()),
                }
            except Exception:
                pass
        elif m.endswith("requirements.txt"):
            deps[m] = [
                line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                for line in content.splitlines()
                if line.strip() and not line.startswith("#")
            ]
        elif m.endswith("pyproject.toml"):
            # naive grep
            deps[m] = re.findall(r'"([a-zA-Z0-9_\-]+)"', content)[:50]
        elif m.endswith("go.mod"):
            deps[m] = re.findall(r"^\s*([a-zA-Z0-9._/\-]+)\s+v[\d.]+", content, re.M)
        elif m.endswith("Cargo.toml"):
            deps[m] = re.findall(r"^([a-zA-Z0-9_\-]+)\s*=", content, re.M)
    return deps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo_path")
    args = ap.parse_args()

    root = Path(args.repo_path)
    if not root.is_dir():
        sys.exit(f"ERROR: not a directory: {root}")

    tree = walk_tree(root)
    readme = read_readme(root)
    deps = parse_manifests(root, tree["manifests"])

    out = {
        "repo_path": str(root),
        "structure": tree,
        "readme_excerpt": readme,
        "parsed_manifests": deps,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
