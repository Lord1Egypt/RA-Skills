#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Optional


DEFAULT_TARGET_ROOT = Path.home() / ".openclaw" / "workspace" / "skills"
DEFAULT_FEEDBACK_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-feedback.jsonl"
SAFE_SKILL_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")

STOPWORDS = {
    "the", "and", "for", "that", "with", "from", "this", "have", "your", "will",
    "skill", "agent", "user", "users", "need", "needs", "should", "could",
    "please", "more", "better", "when", "what", "output", "task", "use",
}


def load_manifest(target_root: Path) -> dict:
    path = target_root / ".skill-forge-installs.json"
    if not path.exists():
        return {"installs": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def valid_skill_name(skill: str) -> bool:
    return bool(SAFE_SKILL_RE.fullmatch(skill)) and ".." not in skill


def contained_child(root: Path, child_name: str) -> Path:
    root = root.expanduser().resolve()
    candidate = (root / child_name).resolve()
    if candidate == root or root not in candidate.parents:
        raise ValueError(f"unsafe output path for skill: {child_name}")
    return candidate


def resolve_skill_source(skill: str, target_root: Path, source: str) -> Path:
    if source:
        return Path(source).expanduser().resolve()
    manifest = load_manifest(target_root)
    record = manifest.get("installs", {}).get(skill, {})
    if record.get("source"):
        return Path(record["source"]).expanduser().resolve()
    return (target_root / skill).expanduser().resolve()


def read_feedback(path: Path, skill: str, limit: int) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("skill") == skill:
            entries.append(entry)
    return entries[-limit:]


def slugish(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def clean_trigger(value: str) -> str:
    value = slugish(value)
    value = re.split(r"[.。;；\n]", value, maxsplit=1)[0]
    value = value.strip(" `\"'“”‘’")
    if len(value) > 64:
        return ""
    if len(value.split()) > 6:
        return ""
    return value


def explicit_trigger_suggestions(entries: list[dict]) -> list[str]:
    triggers = []
    patterns = [
        r"(?:trigger|trigger phrase|触发词|触发语)[:：]\s*([^。\n;；]+)",
        r"(?:when user says|用户说)[:：]\s*([^。\n;；]+)",
    ]
    for entry in entries:
        text = "\n".join(str(entry.get(key) or "") for key in ["feedback", "expected", "task"])
        for pattern in patterns:
            for match in re.findall(pattern, text, flags=re.IGNORECASE):
                value = clean_trigger(match)
                if value and value not in triggers:
                    triggers.append(value)
    return triggers[:8]


def keyword_suggestions(entries: list[dict], limit: int = 8) -> list[str]:
    text = " ".join(str(entry.get("feedback") or "") for entry in entries).lower()
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", text)
    counts = {}
    for word in words:
        if word in STOPWORDS:
            continue
        counts[word] = counts.get(word, 0) + 1
    return [word for word, _ in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:limit]]


def ensure_reference_link(skill_md: Path, reference_name: str) -> None:
    content = skill_md.read_text(encoding="utf-8")
    link = f"- `references/{reference_name}`"
    if link in content:
        return
    pattern = re.compile(r"(?ms)^(References:\n(?:- .*\n?)*)")
    match = pattern.search(content)
    if match:
        block = match.group(1).rstrip("\n") + "\n" + link + "\n"
        content = content[: match.start()] + block + content[match.end():]
    elif "## Resources" in content:
        content = re.sub(
            r"(?ms)(^## Resources\s*\n)",
            lambda m: m.group(1) + "\nReferences:\n" + link + "\n",
            content,
            count=1,
        )
    else:
        content = content.rstrip() + f"\n\n## Resources\n\nReferences:\n{link}\n"
    skill_md.write_text(content, encoding="utf-8")


def add_trigger_cues(skill_md: Path, triggers: list[str]) -> list[str]:
    if not triggers:
        return []
    content = skill_md.read_text(encoding="utf-8")
    existing = set(re.findall(r"(?m)^\s*-\s+`?([^`\n]+?)`?\s*$", content))
    to_add = [trigger for trigger in triggers if trigger not in existing]
    if not to_add:
        return []
    insertion = "\n".join(f"- `{trigger}`" for trigger in to_add)
    if "## Trigger Cues" in content:
        pattern = re.compile(
            r"(?ms)(## Trigger Cues.*?Use this skill when the user mentions:\n\n)(.*?)(\n## |\Z)"
        )
        new_content, replacements = pattern.subn(
            lambda match: match.group(1) + match.group(2).rstrip() + "\n" + insertion + match.group(3),
            content,
            count=1,
        )
        if replacements == 0:
            new_content = content.rstrip() + "\n" + insertion + "\n"
        content = new_content
    else:
        content += "\n\n## Trigger Cues\n\nUse this skill when the user mentions:\n\n" + insertion + "\n"
    skill_md.write_text(content, encoding="utf-8")
    return to_add


def write_evolution_reference(candidate: Path, entries: list[dict], triggers: list[str]) -> None:
    references = candidate / "references"
    references.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Evolution Feedback",
        "",
        "This file summarizes user and agent feedback used to propose a reviewed skill update.",
        "Do not expose hidden evaluation prompts or sensitive task details in user-facing output.",
        "",
        "## Suggested Trigger Additions",
        "",
    ]
    if triggers:
        lines.extend(f"- {trigger}" for trigger in triggers)
    else:
        lines.append("- None detected")
    lines.extend(["", "## Feedback Entries", ""])
    for index, entry in enumerate(entries, 1):
        lines.extend(
            [
                f"### Entry {index}",
                "",
                f"- created_at: {entry.get('created_at')}",
                f"- agent: {entry.get('agent')}",
                f"- rating: {entry.get('rating')}",
                f"- tags: {', '.join(entry.get('tags') or []) or 'none'}",
                f"- feedback: {entry.get('feedback')}",
                "",
            ]
        )
        if entry.get("expected"):
            lines.append(f"- expected: {entry.get('expected')}")
        if entry.get("actual"):
            lines.append(f"- actual: {entry.get('actual')}")
        if entry.get("task"):
            lines.append(f"- task: {entry.get('task')}")
        lines.append("")
    (references / "evolution-feedback.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def propose_update(args: argparse.Namespace) -> dict:
    skill = args.skill
    if not valid_skill_name(skill):
        return {
            "status": "invalid-skill-name",
            "skill": skill,
            "reason": "Skill names must be safe slugs: lowercase letters, digits, dots, underscores, or hyphens.",
        }
    target_root = Path(args.target_root).expanduser().resolve()
    feedback_file = Path(args.feedback_file).expanduser().resolve()
    source = resolve_skill_source(skill, target_root, args.source)
    if not (source / "SKILL.md").exists():
        return {"status": "missing-source", "skill": skill, "source": str(source)}

    entries = read_feedback(feedback_file, skill, args.feedback_limit)
    if not entries:
        return {"status": "no-feedback", "skill": skill, "feedback_file": str(feedback_file)}

    output_root = Path(args.output).expanduser().resolve()
    try:
        candidate = contained_child(output_root, skill)
    except ValueError as error:
        return {"status": "unsafe-output-path", "skill": skill, "reason": str(error)}
    if candidate.exists() or candidate.is_symlink():
        if candidate.is_symlink() or candidate.is_file():
            candidate.unlink()
        else:
            shutil.rmtree(candidate)
    shutil.copytree(source, candidate, symlinks=True)

    triggers = explicit_trigger_suggestions(entries)
    if not triggers:
        triggers.extend(item for item in keyword_suggestions(entries) if item not in triggers)
    triggers = triggers[:8]
    added_triggers = add_trigger_cues(candidate / "SKILL.md", triggers)
    write_evolution_reference(candidate, entries, triggers)
    ensure_reference_link(candidate / "SKILL.md", "evolution-feedback.md")

    return {
        "status": "proposed",
        "skill": skill,
        "source": str(source),
        "candidate": str(candidate),
        "feedback_used": len(entries),
        "trigger_suggestions": triggers,
        "triggers_added": added_triggers,
        "reference_added": "references/evolution-feedback.md",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a reviewed skill update candidate from feedback.")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--output", required=True, help="Output root for the update candidate.")
    parser.add_argument("--source", default="", help="Optional explicit source skill directory.")
    parser.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    parser.add_argument("--feedback-file", default=str(DEFAULT_FEEDBACK_FILE))
    parser.add_argument("--feedback-limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = propose_update(args)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result["status"])
    return 0 if result["status"] == "proposed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
