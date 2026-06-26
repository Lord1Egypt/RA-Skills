#!/usr/bin/env python3
"""
Audit a skill against the agentskills.io Specification.

Performs the mechanical (Dimension 1) checks the agentskills.io validator would
catch, plus a few body-level checks. Does NOT cover Best Practices (Dimension 2)
or Description Optimization (Dimension 3) — those require LLM judgment. See
references/specification-checklist.md for the full spec checklist.

Usage:
    python audit_skill.py <path-to-skill-directory>
    python audit_skill.py <path-to-skill-directory> --json
    python audit_skill.py <path-to-skill-directory> --strict

Exit codes:
    0 — no blockers, no majors
    1 — one or more majors (or strict mode and any warning)
    2 — one or more blockers
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# Allowed frontmatter keys per the agentskills.io Specification
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}

# Recommended body length per the spec
RECOMMENDED_BODY_LINES = 500
# Hard description length limit
MAX_DESCRIPTION_CHARS = 1024
# Hard name length limit
MAX_NAME_CHARS = 64
# Hard compatibility length limit
MAX_COMPATIBILITY_CHARS = 500

# Severity levels, ordered
BLOCKER = "BLOCKER"
MAJOR = "MAJOR"
MINOR = "MINOR"
NIT = "NIT"


def add_finding(findings, severity, code, message, evidence=None, fix=None):
    findings.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "evidence": evidence,
            "fix": fix,
        }
    )


def audit_skill(skill_path: Path) -> dict:
    findings = []
    info = {
        "skill_path": str(skill_path),
        "skill_md_exists": False,
        "frontmatter": None,
        "body_lines": 0,
        "body_chars": 0,
        "referenced_files": [],
    }

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        add_finding(
            findings,
            BLOCKER,
            "FILE_MISSING",
            "SKILL.md not found at skill root.",
            evidence=str(skill_md),
            fix="Create a SKILL.md file at the skill root with the required frontmatter and instructions.",
        )
        return _result(findings, info)

    info["skill_md_exists"] = True
    content = skill_md.read_text(encoding="utf-8")

    # --- Frontmatter shape ------------------------------------------------
    if not content.startswith("---"):
        add_finding(
            findings,
            BLOCKER,
            "FRONTMATTER_MISSING",
            "SKILL.md does not start with YAML frontmatter (must begin with '---' on line 1).",
            fix="Add a YAML frontmatter block at the top of the file.",
        )
        return _result(findings, info)

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        add_finding(
            findings,
            BLOCKER,
            "FRONTMATTER_INVALID",
            "YAML frontmatter is not properly closed with a '---' fence.",
            fix="Ensure the frontmatter opens with '---' on line 1 and closes with '---' with no other '---' fences in the file.",
        )
        return _result(findings, info)

    frontmatter_text = match.group(1)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        add_finding(
            findings,
            BLOCKER,
            "FRONTMATTER_YAML_INVALID",
            f"YAML parse error: {e}",
        )
        return _result(findings, info)

    if not isinstance(frontmatter, dict):
        add_finding(
            findings,
            BLOCKER,
            "FRONTMATTER_NOT_DICT",
            "Frontmatter must be a YAML dictionary (key: value pairs).",
        )
        return _result(findings, info)

    info["frontmatter"] = frontmatter

    # --- Unexpected keys --------------------------------------------------
    unexpected = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        add_finding(
            findings,
            MAJOR,
            "FRONTMATTER_UNEXPECTED_KEYS",
            f"Unexpected frontmatter key(s): {', '.join(sorted(unexpected))}.",
            evidence=f"Found keys: {sorted(frontmatter.keys())}",
            fix=(
                f"Allowed keys are: {', '.join(sorted(ALLOWED_FRONTMATTER_KEYS))}. "
                f"Remove or rename the unexpected key(s)."
            ),
        )

    # --- name -------------------------------------------------------------
    if "name" not in frontmatter:
        add_finding(
            findings,
            BLOCKER,
            "NAME_MISSING",
            "Required field 'name' is missing from frontmatter.",
        )
    else:
        name = frontmatter["name"]
        if not isinstance(name, str):
            add_finding(
                findings,
                BLOCKER,
                "NAME_NOT_STRING",
                f"'name' must be a string, got {type(name).__name__}.",
            )
        else:
            name = name.strip()
            if not name:
                add_finding(findings, BLOCKER, "NAME_EMPTY", "'name' is empty.")
            else:
                if len(name) > MAX_NAME_CHARS:
                    add_finding(
                        findings,
                        BLOCKER,
                        "NAME_TOO_LONG",
                        f"'name' is {len(name)} chars; max is {MAX_NAME_CHARS}.",
                        evidence=f"name: {name!r}",
                    )
                if not re.match(r"^[a-z0-9-]+$", name):
                    add_finding(
                        findings,
                        BLOCKER,
                        "NAME_NOT_KEBAB",
                        "'name' must be kebab-case (lowercase a-z, digits, and hyphens only).",
                        evidence=f"name: {name!r}",
                        fix="Rename to lowercase letters, digits, and single hyphens.",
                    )
                if name.startswith("-") or name.endswith("-") or "--" in name:
                    add_finding(
                        findings,
                        BLOCKER,
                        "NAME_HYPHEN_POSITION",
                        "'name' cannot start or end with '-' or contain '--'.",
                        evidence=f"name: {name!r}",
                    )
                # Spec rule: name must match the parent directory
                if skill_path.name != name:
                    add_finding(
                        findings,
                        BLOCKER,
                        "NAME_DIR_MISMATCH",
                        f"'name' ({name!r}) does not match the parent directory name ({skill_path.name!r}).",
                        evidence=f"dir: {skill_path.name!r}  name: {name!r}",
                        fix=(
                            f"Either rename the directory to {name!r} or change the frontmatter "
                            f"to match the directory. The agentskills.io spec requires these to match."
                        ),
                    )

    # --- description ------------------------------------------------------
    if "description" not in frontmatter:
        add_finding(
            findings,
            BLOCKER,
            "DESCRIPTION_MISSING",
            "Required field 'description' is missing from frontmatter.",
        )
    else:
        description = frontmatter["description"]
        if not isinstance(description, str):
            add_finding(
                findings,
                BLOCKER,
                "DESCRIPTION_NOT_STRING",
                f"'description' must be a string, got {type(description).__name__}.",
            )
        else:
            description = description.strip()
            if not description:
                add_finding(findings, BLOCKER, "DESCRIPTION_EMPTY", "'description' is empty.")
            else:
                if len(description) > MAX_DESCRIPTION_CHARS:
                    add_finding(
                        findings,
                        BLOCKER,
                        "DESCRIPTION_TOO_LONG",
                        f"'description' is {len(description)} chars; max is {MAX_DESCRIPTION_CHARS}.",
                        evidence=f"length: {len(description)}",
                    )
                if "<" in description or ">" in description:
                    add_finding(
                        findings,
                        BLOCKER,
                        "DESCRIPTION_ANGLE_BRACKETS",
                        "'description' cannot contain '<' or '>' characters.",
                        evidence=f"contains {'<' if '<' in description else '>'}",
                    )

    # --- compatibility (optional) ----------------------------------------
    if "compatibility" in frontmatter:
        comp = frontmatter["compatibility"]
        if not isinstance(comp, str):
            add_finding(
                findings,
                MAJOR,
                "COMPATIBILITY_NOT_STRING",
                f"'compatibility' must be a string, got {type(comp).__name__}.",
            )
        elif len(comp) > MAX_COMPATIBILITY_CHARS:
            add_finding(
                findings,
                MAJOR,
                "COMPATIBILITY_TOO_LONG",
                f"'compatibility' is {len(comp)} chars; max is {MAX_COMPATIBILITY_CHARS}.",
            )

    # --- Body checks ------------------------------------------------------
    body = content[match.end():]
    body_lines = body.count("\n") + 1
    info["body_lines"] = body_lines
    info["body_chars"] = len(body)

    if body_lines > RECOMMENDED_BODY_LINES:
        add_finding(
            findings,
            MINOR,
            "BODY_TOO_LONG",
            f"SKILL.md body is {body_lines} lines; the spec recommends under {RECOMMENDED_BODY_LINES}.",
            evidence=f"line count: {body_lines}",
            fix=(
                "Move detailed reference material to references/ with explicit 'read X when Y' triggers. "
                "Keep SKILL.md focused on the core workflow."
            ),
        )

    # Detect additional '---' fences in the body (a common validator trap)
    additional_fences = len(re.findall(r"^---$", body, re.MULTILINE))
    if additional_fences > 0:
        add_finding(
            findings,
            MAJOR,
            "BODY_HAS_HR_FENCES",
            (
                f"Body contains {additional_fences} additional '---' line(s). "
                "Some validators stop at the first '---' they see and may misread the file."
            ),
            fix="Replace '---' horizontal rules in the body with '***' or another marker.",
        )

    # Find file references (markdown links and bare paths)
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    bare_re = re.compile(r"(?<!\()((?:scripts|references|assets)/[A-Za-z0-9._/-]+)")
    refs = set()
    for m in link_re.finditer(body):
        path = m.group(1).split("#", 1)[0]
        if path and not path.startswith(("http://", "https://", "#")):
            refs.add(path)
    for m in bare_re.finditer(body):
        refs.add(m.group(1))
    refs = sorted(refs)
    info["referenced_files"] = refs

    # Warn on deeply-nested references (more than one level deep from skill root)
    for r in refs:
        parts = r.split("/")
        if len(parts) > 2:
            add_finding(
                findings,
                NIT,
                "REF_DEEPLY_NESTED",
                f"Reference '{r}' is more than one level deep from SKILL.md.",
                fix="Flatten the reference path or use a single-level indirection.",
            )

    # Verify referenced files exist
    for r in refs:
        if (skill_path / r).exists():
            continue
        add_finding(
            findings,
            MAJOR,
            "REF_MISSING",
            f"Referenced file does not exist: {r}",
            evidence=f"expected: {skill_path / r}",
            fix="Create the referenced file, or update SKILL.md to point to the correct path.",
        )

    return _result(findings, info)


def _result(findings, info):
    severity_order = {BLOCKER: 0, MAJOR: 1, MINOR: 2, NIT: 3}
    findings.sort(key=lambda f: (severity_order.get(f["severity"], 99), f["code"]))
    summary = {
        "blockers": sum(1 for f in findings if f["severity"] == BLOCKER),
        "majors": sum(1 for f in findings if f["severity"] == MAJOR),
        "minors": sum(1 for f in findings if f["severity"] == MINOR),
        "nits": sum(1 for f in findings if f["severity"] == NIT),
        "total": len(findings),
    }
    return {"findings": findings, "summary": summary, "info": info}


def _print_human(result, strict):
    info = result["info"]
    summary = result["summary"]
    print(f"\nSkill audit: {info['skill_path']}")
    print(f"  SKILL.md exists: {info['skill_md_exists']}")
    if info["frontmatter"]:
        name = info["frontmatter"].get("name", "<missing>")
        print(f"  name: {name}")
    if info["body_lines"]:
        print(f"  body lines: {info['body_lines']}")
    if info["referenced_files"]:
        print(f"  referenced files: {len(info['referenced_files'])}")

    print(
        f"\n  Summary: {summary['blockers']} blockers, {summary['majors']} majors, "
        f"{summary['minors']} minors, {summary['nits']} nits"
    )

    if not result["findings"]:
        print("\n  ✓ No issues found.")
        return

    print()
    for f in result["findings"]:
        print(f"  [{f['severity']}] {f['code']}: {f['message']}")
        if f.get("evidence"):
            print(f"      evidence: {f['evidence']}")
        if f.get("fix"):
            print(f"      fix: {f['fix']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Audit a skill against the agentskills.io Specification."
    )
    parser.add_argument("path", help="Path to the skill directory")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings (minor/nit) as failures for the exit code",
    )
    args = parser.parse_args()

    skill_path = Path(args.path)
    if not skill_path.is_dir():
        print(f"Error: {skill_path} is not a directory", file=sys.stderr)
        sys.exit(2)

    result = audit_skill(skill_path)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        _print_human(result, args.strict)

    summary = result["summary"]
    if summary["blockers"] > 0:
        sys.exit(2)
    if summary["majors"] > 0:
        sys.exit(1)
    if args.strict and (summary["minors"] > 0 or summary["nits"] > 0):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
