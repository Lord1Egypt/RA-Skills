#!/usr/bin/env python3
"""
Security audit script for installed skills.
Detects potential poisoning patterns and auto-rejects high-risk skills.

Usage:
    python scripts/audit_skill.py --skill ./skills/<name> --output ./output/02-audit.md
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple


# High risk patterns - auto remove
HIGH_RISK_PATTERNS = [
    (r"rm\s+-rf\s+/", "Destructive: rm -rf /"),
    (r"rm\s+-rf\s+~", "Destructive: rm -rf ~"),
    (r"rm\s+-rf\s+\.\.", "Destructive: rm -rf parent directory"),
    (r"curl\s+[^|]+\|\s*bash", "Remote code execution: curl | bash"),
    (r"wget\s+[^|]+\|\s*bash", "Remote code execution: wget | bash"),
    (r"eval\s+\$\(", "Dynamic code execution: eval $(...)"),
    (r"base64\s+-d.*\|\s*(bash|sh|python)", "Obfuscated execution: base64 decode | bash"),
    (r">\s*/dev/sd[a-z]", "Disk destruction: write to disk device"),
    (r"mkfs\.\w+\s+/dev/", "Disk format: mkfs on device"),
    (r"dd\s+if=.*of=/dev/", "Disk destruction: dd to device"),
    (r":()\s*{\s*:\|:&\s*}", "Fork bomb"),
    (r"chmod\s+-R\s+777\s+/", "Unsafe permission: chmod 777 /"),
    (r"chown\s+.*\s+/", "System ownership change"),
    (r">\s*/etc/passwd", "System file modification: passwd"),
    (r">\s*/etc/shadow", "System file modification: shadow"),
    (r">\s*/etc/sudoers", "Privilege escalation: sudoers"),
    (r"curl\s+.*\.(pem|key|p12|pfx)", "Credential exfiltration: upload keys"),
    (r"cat\s+.*\.(pem|key|id_rsa)", "Credential access: read private keys"),
    (r"aws\s+.*\bsend\b", "Potential AWS data exfiltration"),
    (r"export\s+.*=.*\$\(", "Dynamic env variable with subshell"),
]

# File extensions to scan
SCAN_EXTENSIONS = [
    ".md", ".sh", ".py", ".js", ".ts", ".bash", ".zsh",
    ".ps1", ".bat", ".cmd", ".json", ".yaml", ".yml",
]


def scan_files(skill_path: Path) -> List[Tuple[Path, str]]:
    """Scan all files in skill directory."""
    files_content = []

    for ext in SCAN_EXTENSIONS:
        for file_path in skill_path.rglob(f"*{ext}"):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                files_content.append((file_path, content))
            except Exception:
                continue

    # Also scan files without extension
    for file_path in skill_path.rglob("*"):
        if file_path.is_file() and file_path.suffix == "":
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if content:  # Only add non-empty files
                    files_content.append((file_path, content))
            except Exception:
                continue

    return files_content


def check_high_risk(content: str) -> List[Tuple[str, str, int]]:
    """Check for high risk patterns. Returns list of (pattern_name, matched_text, line_number).

    Note: This function skips lines that appear to be comments or documentation
    (lines starting with #, //, or enclosed in code blocks).
    """
    findings = []

    # Split content into lines for filtering
    lines = content.split('\n')
    code_only_lines = []
    line_number_map = {}  # Maps new_line_index -> original_line_number

    in_code_block = False
    new_idx = 0
    for orig_idx, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track markdown code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip comment lines (not in code blocks)
        if not in_code_block:
            # Skip lines that look like comments or documentation
            if stripped.startswith('#') or stripped.startswith('//'):
                continue
            # Skip lines in markdown quotes/blocks
            if stripped.startswith('|') or stripped.startswith('>'):
                continue

        code_only_lines.append(line)
        line_number_map[new_idx] = orig_idx
        new_idx += 1

    # Rejoin for pattern matching
    code_content = '\n'.join(code_only_lines)

    for pattern, description in HIGH_RISK_PATTERNS:
        matches = re.finditer(pattern, code_content, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            # Find line number in filtered content, then map to original
            filtered_line_num = code_content[:match.start()].count('\n')
            original_line_num = line_number_map.get(filtered_line_num, filtered_line_num + 1)
            findings.append((description, match.group(), original_line_num))

    return findings


def generate_report(
    skill_name: str,
    skill_path: Path,
    files_scanned: List[Tuple[Path, str]],
    findings: List[Tuple[str, str, int]],
    output_path: Path
) -> str:
    """Generate audit report in markdown format."""

    lines = [
        "# Security Audit Report",
        "",
        f"## Skill: {skill_name}",
        f"## Path: `{skill_path}`",
        "",
        "## Files Scanned",
    ]

    for file_path, _ in files_scanned:
        rel_path = file_path.relative_to(skill_path)
        lines.append(f"- `{rel_path}`")

    lines.extend(["", "## Findings", ""])

    if not findings:
        lines.extend([
            "### Result: GREEN PASS",
            "",
            "No high-risk patterns detected.",
            "",
            "## Action",
            "Continue to Phase 3 (Deep Inspection).",
        ])
        result = "PASS"
    else:
        lines.extend([
            "### Result: RED REJECT",
            "",
            f"Found {len(findings)} high-risk pattern(s):",
            "",
            "| Line | Risk | Matched Content |",
            "|------|------|-----------------|",
        ])

        for description, matched, line_num in findings:
            # Truncate long matches
            display_match = matched[:50] + "..." if len(matched) > 50 else matched
            display_match = display_match.replace("|", "\\|")
            lines.append(f"| {line_num} | {description} | `{display_match}` |")

        lines.extend([
            "",
            "## Action",
            "```bash",
            f"rm -rf {skill_path}",
            "```",
            "",
            "Select an alternative skill from candidates.",
        ])
        result = "REJECT"

    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")

    return result


def audit_skill(skill_path: str, output_path: str) -> Tuple[str, str]:
    """
    Main audit function.

    Returns:
        Tuple of (result, message)
        - result: "PASS" or "REJECT"
        - message: Description of result
    """
    skill_path = Path(skill_path)
    output_path = Path(output_path)

    if not skill_path.exists():
        return "ERROR", f"Skill path not found: {skill_path}"

    skill_name = skill_path.name

    # Scan all files
    files_content = scan_files(skill_path)

    if not files_content:
        return "ERROR", f"No scannable files found in: {skill_path}"

    # Check for high risk patterns
    all_findings = []
    for file_path, content in files_content:
        findings = check_high_risk(content)
        for desc, matched, line_num in findings:
            rel_path = file_path.relative_to(skill_path)
            all_findings.append((f"{desc} (in {rel_path}:{line_num})", matched, line_num))

    # Generate report
    result = generate_report(
        skill_name,
        skill_path,
        files_content,
        all_findings,
        output_path
    )

    if result == "PASS":
        return "PASS", f"Skill '{skill_name}' passed security audit."
    else:
        return "REJECT", f"Skill '{skill_name}' rejected due to {len(all_findings)} high-risk pattern(s)."


def main():
    parser = argparse.ArgumentParser(description="Audit installed skill for security risks")
    parser.add_argument("--skill", required=True, help="Path to skill directory")
    parser.add_argument("--output", required=True, help="Output path for audit report")
    args = parser.parse_args()

    result, message = audit_skill(args.skill, args.output)

    print(f"[{result}] {message}")
    print(f"Report: {args.output}")

    # Exit with error code if rejected
    if result == "REJECT":
        exit(1)


if __name__ == "__main__":
    main()
