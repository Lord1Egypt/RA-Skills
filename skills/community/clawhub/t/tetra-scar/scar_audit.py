#!/usr/bin/env python3
"""scar_audit.py — AI Agent Safety Audit Service.

Run tetra-scar analysis on any GitHub repository.
Scans for common agent failure patterns, generates audit report.

This is the product. Free tier: 1 repo scan. Paid: unlimited + detailed report.

Usage:
  python3 scar_audit.py --repo https://github.com/user/repo
  python3 scar_audit.py --local /path/to/project
  python3 scar_audit.py --demo
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Failure patterns that tetra-scar checks for
FAILURE_PATTERNS = {
    "no_error_handling": {
        "pattern": r"except\s*:\s*\n\s*pass",
        "severity": "HIGH",
        "description": "Bare except with pass — errors silently swallowed",
        "remedy": "Log the error or re-raise. Silent failures cascade.",
    },
    "hardcoded_secrets": {
        "pattern": r"(api_key|secret|password|token)\s*=\s*['\"][^'\"]{8,}['\"]",
        "severity": "CRITICAL",
        "description": "Hardcoded secret or API key in source code",
        "remedy": "Use environment variables or a secrets manager.",
    },
    "force_push": {
        "pattern": r"git\s+push\s+.*--force|git\s+push\s+-f",
        "severity": "HIGH",
        "description": "Force push in code — can destroy shared history",
        "remedy": "Use --force-with-lease or avoid force push entirely.",
    },
    "no_timeout": {
        "pattern": r"requests\.(get|post|put|delete)\([^)]*\)(?!.*timeout)",
        "severity": "MEDIUM",
        "description": "HTTP request without timeout — can hang indefinitely",
        "remedy": "Always set timeout parameter on HTTP requests.",
    },
    "sql_injection": {
        "pattern": r"f['\"].*SELECT.*\{.*\}|\".*SELECT.*\"\s*%\s*\(",
        "severity": "CRITICAL",
        "description": "Potential SQL injection via string formatting",
        "remedy": "Use parameterized queries.",
    },
    "infinite_retry": {
        "pattern": r"while\s+True:\s*\n.*try:.*\n.*except.*\n.*continue",
        "severity": "MEDIUM",
        "description": "Infinite retry loop without backoff or limit",
        "remedy": "Add max_retries and exponential backoff.",
    },
    "no_input_validation": {
        "pattern": r"def\s+\w+\(.*\):\s*\n\s*(?!.*(?:if|assert|validate|check))",
        "severity": "LOW",
        "description": "Function without input validation",
        "remedy": "Validate inputs at function boundaries.",
    },
    "delete_without_confirm": {
        "pattern": r"(shutil\.rmtree|os\.remove|\.delete\(\))",
        "severity": "HIGH",
        "description": "Destructive operation without confirmation",
        "remedy": "Add confirmation step or dry-run mode before destructive ops.",
    },
}


def scan_file(filepath: Path) -> list[dict]:
    """Scan a single file for failure patterns."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for name, pattern_info in FAILURE_PATTERNS.items():
        matches = list(re.finditer(pattern_info["pattern"], content, re.IGNORECASE))
        if matches:
            for m in matches[:3]:  # Max 3 findings per pattern per file
                line_num = content[:m.start()].count("\n") + 1
                findings.append({
                    "file": str(filepath),
                    "line": line_num,
                    "pattern": name,
                    "severity": pattern_info["severity"],
                    "description": pattern_info["description"],
                    "remedy": pattern_info["remedy"],
                    "match": m.group()[:80],
                })
    return findings


def scan_directory(path: str, extensions: set = None) -> list[dict]:
    """Scan all source files in a directory."""
    if extensions is None:
        extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".sh", ".yaml", ".yml"}
    
    root = Path(path)
    all_findings = []
    files_scanned = 0
    
    for f in root.rglob("*"):
        if f.suffix not in extensions:
            continue
        if any(skip in str(f) for skip in ["node_modules", ".git", "__pycache__", ".venv", "venv"]):
            continue
        findings = scan_file(f)
        all_findings.extend(findings)
        files_scanned += 1
    
    return all_findings, files_scanned


def generate_report(findings: list[dict], files_scanned: int, project_name: str) -> str:
    """Generate audit report."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    by_severity = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}
    for f in findings:
        by_severity[f["severity"]].append(f)
    
    score = 100
    score -= len(by_severity["CRITICAL"]) * 25
    score -= len(by_severity["HIGH"]) * 10
    score -= len(by_severity["MEDIUM"]) * 5
    score -= len(by_severity["LOW"]) * 2
    score = max(0, score)
    
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"
    
    report = f"""# AI Agent Safety Audit Report
## {project_name}
Generated: {ts} by Tetra scar-audit

### Summary
- Files scanned: {files_scanned}
- Total findings: {len(findings)}
- Critical: {len(by_severity["CRITICAL"])}
- High: {len(by_severity["HIGH"])}
- Medium: {len(by_severity["MEDIUM"])}
- Low: {len(by_severity["LOW"])}
- Safety Score: {score}/100 (Grade: {grade})

"""
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if by_severity[sev]:
            report += f"### {sev} ({len(by_severity[sev])})\n\n"
            for f in by_severity[sev][:10]:
                rel_path = f["file"].split("/")[-1]
                report += f"**{f['description']}**\n"
                report += f"  File: {rel_path}:{f['line']}\n"
                report += f"  Fix: {f['remedy']}\n\n"
    
    report += f"""---
*Powered by tetra-scar — scar memory for AI agents*
*github.com/aibenyclaude-coder/tetra-scar*
"""
    return report, score, grade


def clone_repo(url: str) -> str:
    """Clone a GitHub repo to temp directory."""
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix="scar_audit_")
    subprocess.run(["git", "clone", "--depth", "1", url, tmpdir],
                   capture_output=True, timeout=60)
    return tmpdir


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Agent Safety Audit")
    parser.add_argument("--repo", help="GitHub repo URL to audit")
    parser.add_argument("--local", help="Local directory to audit")
    parser.add_argument("--demo", action="store_true", help="Run demo audit on tetra-scar")
    parser.add_argument("--output", help="Save report to file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.demo:
        path = str(Path(__file__).parent.parent / "tetra-scar")
        project_name = "tetra-scar (demo)"
    elif args.repo:
        print(f"Cloning {args.repo}...")
        path = clone_repo(args.repo)
        project_name = args.repo.split("/")[-1]
    elif args.local:
        path = args.local
        project_name = Path(path).name
    else:
        parser.print_help()
        sys.exit(1)

    print(f"Scanning {path}...")
    findings, files_scanned = scan_directory(path)
    
    if args.json:
        print(json.dumps({"findings": findings, "files": files_scanned}, indent=2))
        return

    report, score, grade = generate_report(findings, files_scanned, project_name)
    print(report)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()
