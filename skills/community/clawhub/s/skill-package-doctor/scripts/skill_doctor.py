#!/usr/bin/env python3
import argparse
import html
import json
import re
from pathlib import Path
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(description="Audit a ClawHub/Codex/Claude skill package.")
    parser.add_argument("target", help="Skill folder or SKILL.md file")
    parser.add_argument("--json-out")
    parser.add_argument("--markdown-out")
    parser.add_argument("--svg-out")
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        raise SystemExit(f"Target does not exist: {target}")

    root = target if target.is_dir() else target.parent
    skill_path = root / "SKILL.md" if target.is_dir() else target
    if not skill_path.exists():
        raise SystemExit(f"No SKILL.md found at: {skill_path}")

    skill_md = skill_path.read_text(encoding="utf-8")
    files = list_files(root) if target.is_dir() else [skill_path.name]
    audit = audit_skill(skill_md, files)

    if args.json_out:
        write(args.json_out, json.dumps(audit, indent=2) + "\n")
    if args.markdown_out:
        write(args.markdown_out, render_markdown(audit))
    if args.svg_out:
        write(args.svg_out, render_svg(audit))

    print(json.dumps(audit, indent=2))
    if args.fail_on_error and not audit["ok"]:
        raise SystemExit(1)


def list_files(root):
    files = []
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith((".git/", "node_modules/", "dist/")) or "/__pycache__/" in f"/{rel}" or rel.endswith(".pyc"):
            continue
        files.append(rel)
    return sorted(files)


def audit_skill(skill_md, files):
    frontmatter, body = parse_frontmatter(skill_md)
    findings = []
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", body)
    body_words = len([word for word in words if len(word) > 1])
    heading_count = len(re.findall(r"(?m)^#{1,3}\s+\S", body))
    bullet_count = len(re.findall(r"(?m)^[-*]\s+\S", body))
    has_skill_md = "SKILL.md" in files
    has_scripts = any(file.startswith("scripts/") for file in files)
    has_references = any(file.startswith("references/") for file in files)
    has_agents = "agents/openai.yaml" in files

    if not frontmatter:
        finding(findings, "error", "missing-frontmatter", "Missing frontmatter", "Add YAML frontmatter with name and description.")
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
        finding(findings, "error", "bad-name", "Bad skill name", "Use a lower-case slug such as repo-release-doctor.")
    if len(description) < 20:
        finding(findings, "error", "thin-description", "Description is too short", "State the task, input, and output in plain words.")
    if body_words < 80:
        finding(findings, "error", "thin-body", "Skill body is too short", "Add concrete workflow, rules, and validation steps.")
    if heading_count < 2:
        finding(findings, "error", "few-headings", "Not enough headings", "Add sections for When To Use and Workflow.")
    if bullet_count < 3:
        finding(findings, "error", "few-bullets", "Not enough concrete bullets", "Add specific operating rules.")
    if not has_skill_md:
        finding(findings, "error", "missing-skill-md", "SKILL.md is not in the package", "Add SKILL.md at the package root.")
    if not re.search(r"(?im)^##\s+(when\s+to\s+use|use\s+this\s+skill\s+when)\b", body):
        finding(findings, "warning", "missing-when-to-use", "No clear trigger section", "Add a When To Use section.")
    if not re.search(r"(?i)(verify|validate|test|check|review)", body):
        finding(findings, "warning", "missing-validation", "No validation loop", "Add a check or review step.")
    if has_scripts and not re.search(r"(?i)(scripts/|python|node|bundled script)", body):
        finding(findings, "warning", "scripts-not-explained", "Scripts are not explained", "Tell the agent when to run scripts.")
    if has_references and not re.search(r"(?i)(references/|reference file|source manifest)", body):
        finding(findings, "warning", "references-not-explained", "References are not explained", "Tell the agent when to read references.")
    if not has_agents:
        finding(findings, "info", "missing-ui-metadata", "No agents/openai.yaml metadata", "Add UI metadata for marketplace cards.")

    for line in unsafe_lines(body):
        finding(findings, "error", "unsafe-instruction", "Potential unsafe instruction", f"Remove this unsafe line: `{md_escape(line)}`.")

    if not any(item["severity"] == "error" for item in findings):
        finding(findings, "pass", "no-blocking-errors", "No blocking errors", "The package has no obvious publish blockers.")

    score = 100
    for item in findings:
        score -= {"error": 22, "warning": 8, "info": 2, "pass": 0}[item["severity"]]
    score = max(0, min(100, score))
    ok = score >= 80 and not any(item["severity"] == "error" for item in findings)
    if ok and score >= 90:
        grade = "publish-ready"
    elif ok:
        grade = "ship-after-small-fixes"
    elif score >= 50:
        grade = "needs-work"
    else:
        grade = "do-not-publish"

    return {
        "ok": ok,
        "score": score,
        "grade": grade,
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "name": name,
            "description": description,
            "homepage": frontmatter.get("homepage", ""),
            "version": frontmatter.get("version", ""),
        },
        "signals": {
            "bodyWords": body_words,
            "headingCount": heading_count,
            "bulletCount": bullet_count,
            "fileCount": len(files),
            "hasScripts": has_scripts,
            "hasReferencesDir": has_references,
            "hasAgentsMetadata": has_agents,
        },
        "findings": findings,
    }


def parse_frontmatter(raw):
    if not raw.startswith("---\n"):
        return {}, raw
    end = raw.find("\n---", 4)
    if end == -1:
        return {}, raw
    block = raw[4:end]
    body = re.sub(r"^\n---[ \t]*\n?", "", raw[end:])
    fields = {}
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            continue
        value = match.group(2).strip()
        fields[match.group(1)] = value.strip("\"'")
    return fields, body


def unsafe_lines(raw):
    patterns = [
        r"\bignore (all )?(previous|system|developer) instructions\b",
        r"\b(reveal|print|dump|exfiltrate|send).{0,32}\b(secret|password|token|api key|private key)\b",
        r"\brm\s+-rf\s+/\b",
        r"\bsudo\s+rm\b",
        r"\bchmod\s+777\b",
        r"\bcurl\b.+\|\s*(sh|bash)\b",
        r"\bdisable (security|safety|sandbox)\b",
    ]
    out = []
    in_fence = False
    for line in raw.splitlines():
        clean = line.strip()
        if clean.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.startswith(("    ", "\t")) or line.lstrip().startswith(">"):
            continue
        if not clean or re.search(r"\b(do not|never|avoid|refuse)\b", clean, re.I):
            continue
        if any(re.search(pattern, clean, re.I) for pattern in patterns):
            out.append(clean)
    return out[:5]


def finding(findings, severity, item_id, title, fix):
    findings.append({"id": item_id, "severity": severity, "title": title, "fix": fix})


def render_markdown(audit):
    lines = [
        "# Skill Doctor Report",
        "",
        f"Status: **{'PASS' if audit['ok'] else 'NEEDS WORK'}**",
        f"Score: **{audit['score']}/100**",
        f"Grade: **{audit['grade']}**",
        f"Checked: {audit['checkedAt']}",
        "",
        "## Findings",
        "",
    ]
    for item in audit["findings"]:
        lines.append(f"- {item['severity'].upper()} {md_escape(item['title'])}: {md_escape(item['fix'])}")
    return "\n".join(lines) + "\n"


def render_svg(audit):
    name = html.escape(audit["metadata"]["name"] or "skill")[:34]
    status = "PASS" if audit["ok"] else "FIX"
    accent = "#00A676" if audit["ok"] else "#FFB000" if audit["score"] >= 60 else "#FF5F8F"
    errors = sum(1 for item in audit["findings"] if item["severity"] == "error")
    warnings = sum(1 for item in audit["findings"] if item["severity"] == "warning")
    return f'''<svg viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Skill Doctor proof card">
  <rect width="760" height="260" rx="8" fill="#121417"/>
  <path d="M0 198h760v62H0z" fill="#F7EFDA"/>
  <path d="M512 0h248v260H406z" fill="{accent}"/>
  <path d="M630 0h130v260H532z" fill="#4D35A3"/>
  <text x="32" y="58" fill="#F8FAF6" font-family="Inter,system-ui,sans-serif" font-size="34" font-weight="850">{name}</text>
  <text x="34" y="92" fill="#CFFFF0" font-family="Inter,system-ui,sans-serif" font-size="18" font-weight="780">Skill Package Doctor</text>
  {metric(36, 174, audit["score"], "Score")}
  {metric(198, 174, status, "Status")}
  {metric(360, 174, errors, "Errors")}
  {metric(522, 174, warnings, "Warnings")}
  <text x="34" y="232" fill="#372F28" font-family="Inter,system-ui,sans-serif" font-size="14" font-weight="800">checked locally</text>
</svg>'''


def metric(x, y, value, label):
    return f'''<text x="{x}" y="{y}" fill="#F8FAF6" font-family="Inter,system-ui,sans-serif" font-size="32" font-weight="900">{html.escape(str(value))}</text>
  <text x="{x}" y="{y + 25}" fill="#E7EBDC" font-family="Inter,system-ui,sans-serif" font-size="13" font-weight="760">{html.escape(label)}</text>'''


def md_escape(value):
    return html.escape(str(value), quote=False)


def write(path, text):
    out = Path(path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
