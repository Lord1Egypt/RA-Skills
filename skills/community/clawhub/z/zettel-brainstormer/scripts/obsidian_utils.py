import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set


def extract_wikilinks(content: str) -> List[str]:
    """Extract raw wikilink targets from markdown content."""
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def normalize_wikilink_target(link_name: str) -> str:
    """Normalize a wikilink target by removing alias and heading suffix."""
    base = link_name.split("|", 1)[0]
    base = base.split("#", 1)[0]
    return base.strip()


def find_note_path(link_name: str, zettel_dir: Path) -> Optional[Path]:
    """Resolve a wikilink target to a markdown file path."""
    target = normalize_wikilink_target(link_name)
    if not target:
        return None

    exact = zettel_dir / f"{target}.md"
    if exact.exists():
        return exact

    for note in zettel_dir.rglob("*.md"):
        if note.stem.lower() == target.lower():
            return note

    return None


def extract_tags(content: str) -> Set[str]:
    """Extract inline and frontmatter tags from markdown text."""
    tags: Set[str] = set()

    tags.update(re.findall(r"#([\w\-]+)", content))

    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if frontmatter_match:
        fm = frontmatter_match.group(1)
        tags_match = re.search(r"tags:\s*\[([^\]]+)\]", fm)
        if tags_match:
            yaml_tags = [token.strip().strip('"\'') for token in tags_match.group(1).split(",")]
            tags.update(token for token in yaml_tags if token)
        else:
            tags_match = re.search(r"tags:\s*(.+)", fm)
            if tags_match:
                yaml_tags = [token.strip().strip('"\'') for token in tags_match.group(1).split(",")]
                tags.update(token for token in yaml_tags if token)

    return tags


def extract_links_recursive(
    seed_path: Path,
    zettel_dir: Path,
    max_depth: int,
    max_links: int,
) -> Dict[Path, dict]:
    """Traverse linked notes and return note metadata keyed by path."""
    visited: Dict[Path, dict] = {}
    queue = [(seed_path, 0)]

    while queue and len(visited) < max_links:
        current_path, depth = queue.pop(0)
        if current_path in visited or depth > max_depth:
            continue

        try:
            content = current_path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"Warning: could not read {current_path}: {exc}", file=sys.stderr)
            continue

        links = extract_wikilinks(content)
        visited[current_path] = {"level": depth, "links": links, "content": content}

        if depth < max_depth and len(visited) < max_links:
            for link in links:
                linked_path = find_note_path(link, zettel_dir)
                if linked_path and linked_path not in visited:
                    queue.append((linked_path, depth + 1))

    return visited
