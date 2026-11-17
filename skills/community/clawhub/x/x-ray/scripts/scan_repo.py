from pathlib import Path
from collections import Counter
import json
import sys

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "venv",
}

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".vue": "Vue",
    ".svelte": "Svelte",
}


def should_ignore(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)

def scan_repository(root: Path):
    files = []
    directories = set()
    languages = Counter()

    for path in root.rglob("*"):
        if should_ignore(path.relative_to(root)):
            continue

        if path.is_dir():
            directories.add(str(path.relative_to(root)))
            continue

        files.append(str(path.relative_to(root)))

        language = LANGUAGE_MAP.get(path.suffix.lower())
        if language:
            languages[language] += 1

    return {
        "project_name": root.name,
        "total_files": len(files),
        "total_directories": len(directories),
        "languages": dict(languages.most_common()),
        "files": files,
    }


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    result = scan_repository(target)

    print(json.dumps(
        result,
        ensure_ascii=False,
        indent=2
    ))


if __name__ == "__main__":
    main()