#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


VALID_NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
SCAFFOLD_PATTERNS = [
    re.compile(r"^\[TODO:.*\]$", re.MULTILINE),
    re.compile(r"^##\s+\[TODO:.*\]$", re.MULTILINE),
    re.compile(r"Delete this entire .* section when done", re.IGNORECASE),
    re.compile(r"\[TODO: Replace with .*?\]", re.IGNORECASE),
]


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None, text
    return parts[0][4:], parts[1]


def parse_frontmatter(text):
    data = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def has_heading(body, heading):
    pattern = re.compile(rf"^#+\s+{re.escape(heading)}\s*$", re.IGNORECASE | re.MULTILINE)
    return bool(pattern.search(body))


def count_nonempty_lines(text):
    return sum(1 for line in text.splitlines() if line.strip())


def list_dir(path):
    if not path.exists() or not path.is_dir():
        return []
    return sorted(p for p in path.iterdir() if not p.name.startswith("."))


def parse_openai_yaml(path):
    if not path.exists():
        return {}
    data = {}
    current_section = None
    for raw_line in read_text(path).splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        if not raw_line.startswith(" "):
            if raw_line.endswith(":"):
                current_section = raw_line[:-1].strip()
                data[current_section] = {}
            continue
        if current_section != "interface":
            continue
        line = raw_line.strip()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[current_section][key.strip()] = value.strip().strip('"')
    return data


def contains_scaffold_leftovers(text):
    return any(pattern.search(text) for pattern in SCAFFOLD_PATTERNS)


def score_dimension(name, score, reasons, strengths, weaknesses):
    return {
        "name": name,
        "score": max(0, min(5, score)),
        "reasons": reasons,
        "strengths": strengths,
        "weaknesses": weaknesses,
    }


def audit_skill(skill_path):
    skill_path = skill_path.resolve()
    result = {
        "skill_path": str(skill_path),
        "critical_blockers": [],
        "dimensions": [],
        "strengths": [],
        "weaknesses": [],
        "recommended_fixes": [],
    }

    if not skill_path.exists() or not skill_path.is_dir():
        result["critical_blockers"].append("Target path does not exist or is not a directory.")
        result["verdict"] = "Not Qualified"
        result["total_score"] = 0
        return result

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        result["critical_blockers"].append("Missing required file: SKILL.md")
        result["verdict"] = "Not Qualified"
        result["total_score"] = 0
        return result

    skill_text = read_text(skill_md)
    frontmatter_text, body = split_frontmatter(skill_text)
    frontmatter = {}
    if frontmatter_text is None:
        result["critical_blockers"].append("SKILL.md is missing valid YAML frontmatter delimited by ---")
    else:
        try:
            frontmatter = parse_frontmatter(frontmatter_text)
        except ValueError as exc:
            result["critical_blockers"].append(str(exc))

    folder_name = skill_path.name
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    frontmatter_keys = set(frontmatter.keys())
    body_lines = count_nonempty_lines(body)

    scripts = list_dir(skill_path / "scripts")
    references = list_dir(skill_path / "references")
    assets = list_dir(skill_path / "assets")
    agents_yaml = skill_path / "agents" / "openai.yaml"
    openai_yaml = parse_openai_yaml(agents_yaml)

    structure_score = 5
    structure_reasons = []
    structure_strengths = []
    structure_weaknesses = []

    if frontmatter_text is None or not frontmatter:
        structure_score = 0
    if not name:
        structure_score -= 2
        result["critical_blockers"].append("Frontmatter is missing the required name field.")
        structure_weaknesses.append("Missing `name` in frontmatter.")
    if not description:
        structure_score -= 2
        result["critical_blockers"].append("Frontmatter is missing the required description field.")
        structure_weaknesses.append("Missing `description` in frontmatter.")
    if frontmatter_keys and frontmatter_keys != {"name", "description"}:
        structure_score -= 1
        structure_weaknesses.append("Frontmatter contains keys beyond `name` and `description`.")
    if name and name != folder_name:
        structure_score -= 1
        structure_weaknesses.append("Frontmatter `name` does not match the folder name.")
    if name and not VALID_NAME_RE.match(name):
        structure_score -= 2
        result["critical_blockers"].append("Skill name must use lowercase letters, digits, and hyphens only.")
        structure_weaknesses.append("Skill name does not follow naming rules.")
    if contains_scaffold_leftovers(skill_text):
        structure_score -= 2
        result["critical_blockers"].append("Skill still contains unresolved scaffold or template text.")
        structure_weaknesses.append("Template leftovers remain in the skill.")
    if structure_score >= 4:
        structure_strengths.append("Required skill structure is present and mostly clean.")
    structure_reasons.append(f"Detected folder `{folder_name}` with {body_lines} non-empty body lines.")

    result["dimensions"].append(score_dimension("structure", structure_score, structure_reasons, structure_strengths, structure_weaknesses))

    triggering_score = 5
    triggering_reasons = []
    triggering_strengths = []
    triggering_weaknesses = []

    desc_words = len(description.split())
    desc_lower = description.lower()
    if not description:
        triggering_score = 0
    else:
        if desc_words < 12:
            triggering_score -= 2
            triggering_weaknesses.append("Description is too short to explain triggering well.")
        if "use when" not in desc_lower and "when codex" not in desc_lower:
            triggering_score -= 2
            result["critical_blockers"].append("Description does not clearly state when the skill should be used.")
            triggering_weaknesses.append("Description lacks explicit trigger wording such as `Use when ...`.")
        if "," not in description and ":" not in description and "(" not in description:
            triggering_score -= 1
            triggering_weaknesses.append("Description may be too generic and lacks concrete trigger detail.")
        if triggering_score >= 4:
            triggering_strengths.append("Description explains both capability and likely usage context.")
        triggering_reasons.append(f"Description length: {desc_words} words.")

    result["dimensions"].append(score_dimension("triggering", triggering_score, triggering_reasons, triggering_strengths, triggering_weaknesses))

    workflow_score = 5
    workflow_reasons = []
    workflow_strengths = []
    workflow_weaknesses = []

    has_workflow = has_heading(body, "Workflow")
    has_overview = has_heading(body, "Overview")
    numbered_steps = len(re.findall(r"^\d+\.\s", body, re.MULTILINE))
    if not has_overview:
        workflow_score -= 1
        workflow_weaknesses.append("Body lacks a clear overview section.")
    if not has_workflow and numbered_steps < 3:
        workflow_score -= 2
        result["critical_blockers"].append("Skill body does not provide a concrete workflow or equivalent execution steps.")
        workflow_weaknesses.append("Instructions are not action-oriented enough.")
    if has_workflow or numbered_steps >= 3:
        workflow_strengths.append("Body gives a usable execution path.")
    workflow_reasons.append(f"Detected {numbered_steps} numbered steps.")

    result["dimensions"].append(score_dimension("workflow", workflow_score, workflow_reasons, workflow_strengths, workflow_weaknesses))

    pd_score = 5
    pd_reasons = []
    pd_strengths = []
    pd_weaknesses = []

    if body_lines > 220 and not references:
        pd_score -= 2
        pd_weaknesses.append("Long SKILL.md without a references folder may be overloading the body.")
    if body_lines > 350:
        pd_score -= 1
        pd_weaknesses.append("SKILL.md is becoming large enough to hurt context efficiency.")
    if references or scripts:
        pd_strengths.append("Uses bundled resources to keep reusable detail outside the main body.")
    if scripts and "scripts/" not in body:
        pd_score -= 1
        pd_weaknesses.append("Scripts exist but are not explained in SKILL.md.")
    if references and "references/" not in body and "references/" not in skill_text:
        pd_score -= 1
        pd_weaknesses.append("References exist but are not surfaced in SKILL.md.")
    pd_reasons.append(f"Detected {len(scripts)} scripts and {len(references)} reference files.")

    result["dimensions"].append(score_dimension("progressive_disclosure", pd_score, pd_reasons, pd_strengths, pd_weaknesses))

    resources_score = 5
    resources_reasons = []
    resources_strengths = []
    resources_weaknesses = []

    for dirname, items in [("scripts", scripts), ("references", references), ("assets", assets)]:
        dir_path = skill_path / dirname
        if dir_path.exists() and not items:
            resources_score -= 1
            resources_weaknesses.append(f"`{dirname}/` exists but is empty.")
    if scripts:
        resources_strengths.append("Includes executable support for repeatable checks or workflows.")
    if references:
        resources_strengths.append("Includes reference material that can support richer judgment.")
    if not scripts and not references and body_lines > 120:
        resources_score -= 1
        resources_weaknesses.append("Skill may benefit from pulling reusable detail into scripts or references.")
    resources_reasons.append(f"Resource counts: scripts={len(scripts)}, references={len(references)}, assets={len(assets)}.")

    result["dimensions"].append(score_dimension("resources", resources_score, resources_reasons, resources_strengths, resources_weaknesses))

    examples_score = 5
    examples_reasons = []
    examples_strengths = []
    examples_weaknesses = []

    has_examples = has_heading(body, "Trigger Examples") or has_heading(body, "Examples")
    has_output_shape = has_heading(body, "Output Shape")
    if not has_examples:
        examples_score -= 2
        examples_weaknesses.append("Skill does not show example prompts or trigger examples.")
    if not has_output_shape:
        examples_score -= 1
        examples_weaknesses.append("Skill does not define an expected output shape.")
    if has_examples:
        examples_strengths.append("Examples make invocation intent easier to understand.")
    if has_output_shape:
        examples_strengths.append("Output shape helps produce consistent results.")
    examples_reasons.append(f"Examples section: {has_examples}; output shape: {has_output_shape}.")

    result["dimensions"].append(score_dimension("examples_and_outputs", examples_score, examples_reasons, examples_strengths, examples_weaknesses))

    maintainability_score = 5
    maintainability_reasons = []
    maintainability_strengths = []
    maintainability_weaknesses = []

    if body_lines > 280:
        maintainability_score -= 1
        maintainability_weaknesses.append("Long body will be harder to maintain and scan.")
    if agents_yaml.exists():
        interface = openai_yaml.get("interface", {})
        default_prompt = interface.get("default_prompt", "")
        if default_prompt and f"${folder_name}" not in default_prompt:
            maintainability_score -= 1
            maintainability_weaknesses.append("agents/openai.yaml default_prompt does not mention the skill name.")
        else:
            maintainability_strengths.append("agents/openai.yaml appears aligned with the skill name.")
    if contains_scaffold_leftovers(skill_text):
        maintainability_score -= 2
    if maintainability_score >= 4:
        maintainability_strengths.append("Skill is concise enough to iterate on safely.")
    maintainability_reasons.append(f"Body length and metadata alignment checked for `{folder_name}`.")

    result["dimensions"].append(score_dimension("maintainability", maintainability_score, maintainability_reasons, maintainability_strengths, maintainability_weaknesses))

    total_score = sum(item["score"] for item in result["dimensions"])
    result["total_score"] = total_score

    for item in result["dimensions"]:
        result["strengths"].extend(item["strengths"])
        result["weaknesses"].extend(item["weaknesses"])

    if result["critical_blockers"] or total_score < 16:
        verdict = "Not Qualified"
    elif total_score < 24:
        verdict = "Borderline"
    else:
        verdict = "Qualified"
    result["verdict"] = verdict

    recommended = []
    if result["critical_blockers"]:
        recommended.extend(result["critical_blockers"][:3])
    if any("Description" in weak or "description" in weak for weak in result["weaknesses"]):
        recommended.append("Rewrite the frontmatter description so it clearly states both capability and trigger conditions.")
    if any("workflow" in weak.lower() or "action-oriented" in weak.lower() for weak in result["weaknesses"]):
        recommended.append("Add a concrete workflow with numbered steps that another Codex instance can execute.")
    if any("output shape" in weak.lower() for weak in result["weaknesses"]):
        recommended.append("Add an Output Shape section so results stay consistent across uses.")
    if any("empty" in weak.lower() or "not explained" in weak.lower() for weak in result["weaknesses"]):
        recommended.append("Remove confusing unused resource folders or document them from SKILL.md.")
    if not recommended and verdict != "Qualified":
        recommended.append("Tighten the wording and add clearer examples so the skill triggers and executes more reliably.")
    result["recommended_fixes"] = dedupe(recommended)

    result["strengths"] = dedupe(result["strengths"])
    result["weaknesses"] = dedupe(result["weaknesses"])
    result["critical_blockers"] = dedupe(result["critical_blockers"])
    return result


def dedupe(items):
    seen = set()
    output = []
    for item in items:
        if item not in seen:
            output.append(item)
            seen.add(item)
    return output


def render_text_report(report):
    lines = []
    lines.append(f"Skill: {report['skill_path']}")
    lines.append(f"Verdict: {report['verdict']}")
    lines.append(f"Total score: {report['total_score']}/35")
    if report["critical_blockers"]:
        lines.append("Critical blockers:")
        for item in report["critical_blockers"]:
            lines.append(f"- {item}")
    lines.append("Dimensions:")
    for item in report["dimensions"]:
        lines.append(f"- {item['name']}: {item['score']}/5")
        for reason in item["reasons"]:
            lines.append(f"  reason: {reason}")
        for strength in item["strengths"]:
            lines.append(f"  good: {strength}")
        for weakness in item["weaknesses"]:
            lines.append(f"  bad: {weakness}")
    if report["strengths"]:
        lines.append("Strengths:")
        for item in report["strengths"]:
            lines.append(f"- {item}")
    if report["weaknesses"]:
        lines.append("Weaknesses:")
        for item in report["weaknesses"]:
            lines.append(f"- {item}")
    if report["recommended_fixes"]:
        lines.append("Recommended fixes:")
        for item in report["recommended_fixes"]:
            lines.append(f"- {item}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit a Codex skill for quality and compliance.")
    parser.add_argument("skill_path", help="Path to the target skill folder")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    report = audit_skill(Path(args.skill_path))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text_report(report))


if __name__ == "__main__":
    main()
