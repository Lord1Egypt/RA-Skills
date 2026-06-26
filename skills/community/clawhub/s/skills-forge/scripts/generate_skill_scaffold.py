#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


from templates.profile_packs import PROFILE_HINTS, PROFILE_PACKS

GENERIC_TRIGGERS = {
    "reusable", "structure", "reminders", "recurring", "workflow", "workflows",
    "tasks", "task", "helper", "support", "guidance", "notes", "output",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-")


def titleize(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def infer_template(skill_name: str, goal: str, triggers: list[str]) -> str:
    text = " ".join([skill_name, goal, *triggers]).lower()
    scores = {
        name: sum(1 for hint in hints if hint in text)
        for name, hints in PROFILE_HINTS.items()
    }
    best = max(scores.items(), key=lambda item: item[1])
    return best[0] if best[1] else "workflow"


def clean_triggers(skill_name: str, triggers: list[str]) -> list[str]:
    cleaned = []
    skill_parts = set(skill_name.split("-"))
    for trigger in triggers:
        value = trigger.strip()
        slug = slugify(value)
        if not slug or slug == skill_name:
            continue
        if slug in GENERIC_TRIGGERS:
            continue
        if slug in skill_parts and len(skill_parts) > 1:
            continue
        if value not in cleaned:
            cleaned.append(value)
    if cleaned:
        return cleaned[:8]
    return [part for part in skill_name.split("-") if part not in GENERIC_TRIGGERS][:8]


def enrich_triggers(skill_name: str, triggers: list[str], template: str) -> list[str]:
    """Return up to 8 trigger phrases for the SKILL.md bullet list.

    User-supplied triggers always take precedence. Profile-default triggers are
    only mixed in when the user under-specified (fewer than 5 triggers); they
    top up to ~8 so the bullet list is rich enough for the validator's
    5-trigger gate without flooding well-specified user inputs.
    """
    pack = PROFILE_PACKS[template]
    merged = []
    seen = set()
    for trigger in triggers:
        value = trigger.strip()
        slug = slugify(value)
        if not slug or slug == skill_name or slug in GENERIC_TRIGGERS or slug in seen:
            continue
        merged.append(value)
        seen.add(slug)
    if len(merged) >= 5:
        return merged[:12]
    target = 8
    for trigger in pack.get("default_triggers", []):
        if len(merged) >= target:
            break
        value = trigger.strip()
        slug = slugify(value)
        if not slug or slug == skill_name or slug in GENERIC_TRIGGERS or slug in seen:
            continue
        merged.append(value)
        seen.add(slug)
    return merged or [skill_name.replace("-", " ")]


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def short_description(display_name: str, template: str) -> str:
    value = PROFILE_PACKS[template].get("interface", {}).get(
        "short_description",
        f"Use {display_name} workflow guidance",
    )
    if len(value) > 64:
        value = f"{display_name} workflow helper"
    return value[:64].rstrip()


def default_prompt(display_name: str, template: str) -> str:
    return PROFILE_PACKS[template].get("interface", {}).get(
        "default_prompt",
        f"Use the {display_name} skill workflow.",
    )


def build_description(skill_name: str, goal: str, user_triggers: list[str], all_triggers: list[str], template: str) -> str:
    context = "operating workflow" if template == "workflow" else f"{template.replace('-', ' ')} skill"
    surface_triggers = user_triggers if user_triggers else all_triggers
    trigger_text = ", ".join(surface_triggers[:8])
    description = (
        f"{goal} Use when the user asks for {trigger_text or titleize(skill_name)}, "
        f"or when an agent needs a reusable {context} with bundled references, "
        "quality gates, and clear output contracts."
    )
    return description[:1020].rstrip()


def build_skill_md(skill_name: str, goal: str, user_triggers: list[str], all_triggers: list[str], template: str) -> str:
    pack = PROFILE_PACKS[template]
    display_name = titleize(skill_name)
    description = build_description(skill_name, goal, user_triggers, all_triggers, template)
    trigger_bullets = "\n".join(f"- `{item}`" for item in all_triggers) or "- `repeatable workflow`"
    workflow_steps = "\n".join(f"{index}. {step}" for index, step in enumerate(pack["workflow"], 1))
    contract_bullets = "\n".join(f"- {item}" for item in pack["output_contract"])
    profile_quality = "\n".join(f"- {item}" for item in pack.get("quality_gates", []))
    resource_policy = "\n".join(f"- {item}" for item in pack.get("resource_policy", []))
    reference_bullets = "\n".join(f"- `references/{name}`" for name in pack["references"])
    script_bullets = ""
    if pack.get("scripts"):
        script_bullets = "\n\nScripts:\n" + "\n".join(f"- `scripts/{name}`" for name in pack["scripts"])

    return f"""---
name: {skill_name}
description: {description}
---

# {display_name}

## Trigger Cues

Use this skill when the user mentions:

{trigger_bullets}

## Core Workflow

{workflow_steps}

## Resource Loading

Keep `SKILL.md` lean. Load bundled resources only when the task needs that detail.

{resource_policy}

## Execution Mode

{pack.get("freedom_level", "medium freedom: adapt to context while preserving the workflow and quality gates.")}

## Output Contract

The final answer or artifact should include:

{contract_bullets}

## Quality Gates

- Do not invent facts, credentials, sources, or external results.
- Prefer stable structure over one-off prose.
- State assumptions when the user has not provided enough context.
- Use bundled references before writing from memory.
- Keep the output directly usable by the target agent or user.
{profile_quality}

## Resources

References:
{reference_bullets}{script_bullets}
"""


def write_candidate(skill_dir: Path, skill_name: str, goal: str, user_triggers: list[str], all_triggers: list[str], template: str) -> None:
    pack = PROFILE_PACKS[template]
    display_name = titleize(skill_name)
    (skill_dir / "agents").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)

    skill_md = build_skill_md(skill_name, goal, user_triggers, all_triggers, template)
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    openai_yaml = "\n".join(
        [
            "interface:",
            f"  display_name: {yaml_quote(display_name)}",
            f"  short_description: {yaml_quote(short_description(display_name, template))}",
            f"  default_prompt: {yaml_quote(default_prompt(display_name, template))}",
            "",
        ]
    )
    (skill_dir / "agents" / "openai.yaml").write_text(openai_yaml, encoding="utf-8")

    for name, content in pack["references"].items():
        (skill_dir / "references" / name).write_text(content.strip() + "\n", encoding="utf-8")

    if pack.get("scripts"):
        (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)
        for name, content in pack["scripts"].items():
            path = skill_dir / "scripts" / name
            path.write_text(content, encoding="utf-8")
            path.chmod(0o755)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a milestone-quality skill candidate.")
    parser.add_argument("--skill-name", required=True, help="Hyphen-case or natural-language skill name.")
    parser.add_argument("--output", required=True, help="Directory where the generated skill should be created.")
    parser.add_argument("--goal", required=True, help="One-sentence purpose of the skill.")
    parser.add_argument("--triggers", required=True, help="Comma-separated trigger words or phrases.")
    parser.add_argument(
        "--template",
        choices=["auto", "academic", "product", "integration", "script", "workflow"],
        default="auto",
        help="Template profile to use.",
    )
    args = parser.parse_args()

    skill_name = slugify(args.skill_name)
    raw_triggers = [item.strip() for item in args.triggers.split(",") if item.strip()]
    user_triggers = clean_triggers(skill_name, raw_triggers)
    template = args.template
    if template == "auto":
        template = infer_template(skill_name, args.goal, user_triggers)
    all_triggers = enrich_triggers(skill_name, user_triggers, template)

    output_root = Path(args.output).expanduser().resolve()
    skill_dir = output_root / skill_name
    write_candidate(skill_dir, skill_name, args.goal.strip(), user_triggers, all_triggers, template)
    print(f"{skill_dir} template={template}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
