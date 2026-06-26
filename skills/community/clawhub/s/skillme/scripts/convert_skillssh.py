#!/usr/bin/env python3
"""
convert_skillssh.py — Convert a skills.sh skill into OpenClaw SKILL.md format.

Usage:
  python3 convert_skillssh.py <input> [--output <path>]

Input formats:
  owner/repo@skill-name                   e.g. vercel-labs/agent-skills@react-best-practices
  https://skills.sh/owner/repo/skill      skills.sh URL
  https://raw.githubusercontent.com/...  Direct raw GitHub URL

Examples:
  python3 convert_skillssh.py vercel-labs/agent-skills@react-best-practices
  python3 convert_skillssh.py https://skills.sh/vercel-labs/agent-skills/react-best-practices \\
      --output /root/.openclaw/workspace/skills/react-best-practices/SKILL.md
"""

import argparse
import re
import sys
import os
import urllib.request
import urllib.error


def parse_input(raw: str) -> tuple[str, str]:
    """
    Parse any input format into (raw_github_url, skill_name).
    Returns (url, skill_name).
    """
    raw = raw.strip()

    # Already a raw GitHub URL
    if raw.startswith("https://raw.githubusercontent.com/"):
        # Extract skill name from path
        parts = raw.rstrip("/").split("/")
        # Remove SKILL.md if present
        if parts[-1].upper() == "SKILL.MD":
            skill_name = parts[-2]
        else:
            skill_name = parts[-1]
        return raw, skill_name

    # skills.sh URL: https://skills.sh/owner/repo/skill
    if raw.startswith("https://skills.sh/"):
        path = raw[len("https://skills.sh/"):]
        parts = path.strip("/").split("/")
        if len(parts) < 3:
            raise ValueError(f"Cannot parse skills.sh URL: {raw}. Expected format: https://skills.sh/owner/repo/skill")
        owner, repo, *rest = parts
        skill_name = rest[-1] if rest else repo
        # Try the standard path structure
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/skills/{skill_name}/SKILL.md"
        return raw_url, skill_name

    # GitHub URL (non-raw): https://github.com/owner/repo/...
    if raw.startswith("https://github.com/"):
        path = raw[len("https://github.com/"):]
        parts = path.strip("/").split("/")
        if len(parts) < 2:
            raise ValueError(f"Cannot parse GitHub URL: {raw}")
        owner = parts[0]
        repo = parts[1]
        # Try to find skill path
        rest = parts[2:]
        if rest and rest[0] in ("blob", "tree"):
            rest = rest[2:]  # remove blob/tree + branch
        path_suffix = "/".join(rest)
        if not path_suffix.upper().endswith("SKILL.MD"):
            path_suffix = path_suffix.rstrip("/") + "/SKILL.md"
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{path_suffix}"
        skill_name = parts[-1] if parts[-1].upper() != "SKILL.MD" else parts[-2]
        return raw_url, skill_name

    # Short format: owner/repo@skill-name
    if "@" in raw:
        repo_part, skill_name = raw.split("@", 1)
        parts = repo_part.split("/")
        if len(parts) != 2:
            raise ValueError(f"Expected owner/repo@skill format, got: {raw}")
        owner, repo = parts
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/skills/{skill_name}/SKILL.md"
        return raw_url, skill_name

    raise ValueError(
        f"Unrecognized input format: {raw}\n"
        "Expected one of:\n"
        "  owner/repo@skill-name\n"
        "  https://skills.sh/owner/repo/skill\n"
        "  https://raw.githubusercontent.com/..."
    )


def fetch_url(url: str) -> str:
    """Fetch content from URL."""
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"Skill not found at {url} (404). Check the owner/repo/skill-name.")
        raise ValueError(f"HTTP {e.code} fetching {url}: {e.reason}")
    except Exception as e:
        raise ValueError(f"Failed to fetch {url}: {e}")


def try_alternate_urls(base_url: str) -> str:
    """Try alternate URL patterns if the primary one fails."""
    # Extract parts from the primary URL
    # https://raw.githubusercontent.com/owner/repo/main/skills/skill-name/SKILL.md
    parts = base_url.split("/")
    try:
        gh_idx = parts.index("raw.githubusercontent.com")
        owner = parts[gh_idx + 1]
        repo = parts[gh_idx + 2]
        branch = parts[gh_idx + 3]
        rest = parts[gh_idx + 4:]
    except (ValueError, IndexError):
        raise ValueError(f"Cannot parse URL structure: {base_url}")

    skill_name = rest[-2] if rest[-1].upper() == "SKILL.MD" else rest[-1]

    alternates = [
        f"https://raw.githubusercontent.com/{owner}/{repo}/main/SKILL.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/main/{skill_name}.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/main/skills/{skill_name}.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/master/skills/{skill_name}/SKILL.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/master/SKILL.md",
    ]

    for url in alternates:
        try:
            content = fetch_url(url)
            print(f"  Found at alternate URL: {url}", file=sys.stderr)
            return content
        except ValueError:
            continue

    raise ValueError(f"Could not fetch skill from any URL pattern for {owner}/{repo}@{skill_name}")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML-like frontmatter from a markdown file."""
    if not content.startswith("---"):
        return {}, content

    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return {}, content

    fm_text = content[3:end_idx].strip()
    body = content[end_idx + 4:].lstrip("\n")

    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()

    return fm, body


def extract_when_to_use(body: str) -> tuple[str, str]:
    """
    Extract 'When to Use' section from body.
    Returns (when_to_use_text, body_without_section).
    """
    # Try various heading patterns
    patterns = [
        r"#{1,3}\s+When to Use This Skill\s*\n(.*?)(?=\n#{1,3}\s|\Z)",
        r"#{1,3}\s+When to Use\s*\n(.*?)(?=\n#{1,3}\s|\Z)",
        r"#{1,3}\s+Usage\s*\n(.*?)(?=\n#{1,3}\s|\Z)",
    ]

    for pattern in patterns:
        match = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
        if match:
            section_text = match.group(1).strip()
            # Clean up bullet points into a flat description
            lines = []
            for line in section_text.splitlines():
                line = line.strip().lstrip("-* ").strip()
                if line:
                    lines.append(line)
            description = " ".join(lines)
            # Remove the section from the body
            clean_body = body[:match.start()] + body[match.end():]
            clean_body = re.sub(r"\n{3,}", "\n\n", clean_body).strip()
            return description, clean_body

    return "", body


def build_description(skill_name: str, fm_description: str, when_to_use: str) -> str:
    """Build a self-contained OpenClaw description with trigger phrases."""
    base = fm_description or when_to_use or f"Use this skill for {skill_name.replace('-', ' ')} tasks."

    # Truncate if too long
    if len(base) > 300:
        base = base[:297] + "..."

    return base


def convert(content: str, skill_name: str) -> str:
    """Convert a skills.sh SKILL.md into OpenClaw format."""
    fm, body = parse_frontmatter(content)

    existing_name = fm.get("name", skill_name)
    existing_desc = fm.get("description", "")

    when_to_use, clean_body = extract_when_to_use(body)

    description = build_description(existing_name, existing_desc, when_to_use)

    # Build output
    output_lines = [
        "---",
        f"name: {existing_name}",
        f"description: {description}",
        "---",
        "",
        clean_body.strip(),
    ]

    return "\n".join(output_lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Convert a skills.sh skill into OpenClaw SKILL.md format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", help="skills.sh URL, owner/repo@skill, or raw GitHub URL")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    try:
        raw_url, skill_name = parse_input(args.input)
        print(f"Fetching: {raw_url}", file=sys.stderr)

        try:
            content = fetch_url(raw_url)
        except ValueError as e:
            print(f"Primary URL failed: {e}", file=sys.stderr)
            print("Trying alternate URL patterns...", file=sys.stderr)
            content = try_alternate_urls(raw_url)

        print(f"Fetched {len(content)} bytes for skill: {skill_name}", file=sys.stderr)

        converted = convert(content, skill_name)

        if args.output:
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            with open(args.output, "w") as f:
                f.write(converted)
            print(f"Written to: {args.output}", file=sys.stderr)
            print(f"Lines: {len(converted.splitlines())}", file=sys.stderr)
        else:
            print(converted)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
