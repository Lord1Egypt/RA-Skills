#!/usr/bin/env python3
"""Security scan for the skill - checks for common security issues.

Usage:
    python3 scripts/security_scan.py [SKILL_DIR]
"""

import os
import re
import sys
from pathlib import Path


def scan_for_secrets(skill_dir):
    """Scan for potential secrets/credentials."""
    issues = []

    # Patterns to check
    secret_patterns = [
        (r'api[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', "Potential API key"),
        (r'secret\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', "Potential secret"),
        (r'token\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', "Potential token"),
        (r'password\s*[=:]\s*["\'][^"\']+["\']', "Potential password"),
        (r'sk-[a-zA-Z0-9]{20,}', "Potential OpenAI API key"),
        (r'ghp_[a-zA-Z0-9]{36}', "Potential GitHub token"),
        (r'AKIA[0-9A-Z]{16}', "Potential AWS access key"),
    ]

    # Files to exclude from scanning (this script itself)
    exclude_files = {'security_scan.py', 'validate.py'}

    for root, dirs, files in os.walk(skill_dir):
        # Skip hidden directories and common non-source dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

        for file in files:
            if file in exclude_files:
                continue
            if file.endswith(('.py', '.sh', '.md', '.json', '.yaml', '.yml')):
                filepath = Path(root) / file
                try:
                    content = filepath.read_text(encoding="utf-8")
                    for pattern, description in secret_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            issues.append({
                                'file': filepath.relative_to(skill_dir),
                                'line': line_num,
                                'type': description,
                                'match': match.group()[:50] + "..." if len(match.group()) > 50 else match.group()
                            })
                except Exception:
                    pass

    return issues


def scan_for_injection_risks(skill_dir):
    """Scan for potential injection vulnerabilities."""
    issues = []

    # Files to exclude from scanning
    exclude_files = {'security_scan.py', 'validate.py'}

    # Check Python files for risky patterns
    risky_patterns = [
        (r'eval\s*\(', "Use of eval()"),
        (r'exec\s*\(', "Use of exec()"),
        (r'os\.system\s*\(', "Use of os.system()"),
        (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', "subprocess with shell=True"),
        (r'input\s*\([^)]*\)\s*\)', "Potential code injection"),
    ]

    for py_file in Path(skill_dir).rglob("*.py"):
        if py_file.name.startswith('test_') or py_file.name in exclude_files:
            continue

        try:
            content = py_file.read_text(encoding="utf-8")
            for pattern, description in risky_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append({
                        'file': py_file.relative_to(skill_dir),
                        'line': line_num,
                        'type': description,
                    })
        except Exception:
            pass

    return issues


def scan_file_permissions(skill_dir):
    """Check for executable scripts that shouldn't be."""
    issues = []

    # Files that are allowed to be executable
    allowed_executable = {'install.sh'}

    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file in allowed_executable:
                continue
            filepath = Path(root) / file
            if filepath.suffix in ['.json', '.md', '.yaml', '.yml']:
                # Check if file is executable
                if os.access(filepath, os.X_OK):
                    issues.append({
                        'file': filepath.relative_to(skill_dir),
                        'type': 'File has execute permission (unnecessary)'
                    })

    return issues


def main():
    if len(sys.argv) > 1:
        skill_dir = sys.argv[1]
    else:
        skill_dir = Path(__file__).parent.parent

    skill_dir = Path(skill_dir).resolve()

    print(f"Security scanning: {skill_dir}")
    print("=" * 50)

    all_issues = []

    scanners = [
        ("Secrets/Credentials", scan_for_secrets),
        ("Injection Risks", scan_for_injection_risks),
        ("File Permissions", scan_file_permissions),
    ]

    for name, scanner in scanners:
        issues = scanner(skill_dir)
        for issue in issues:
            issue['category'] = name
        all_issues.extend(issues)

    # Print results
    if all_issues:
        print("\n🔒 Security Issues Found:")
        for issue in all_issues:
            location = f"{issue['file']}"
            if 'line' in issue:
                location += f":{issue['line']}"

            print(f"\n  [{issue['category']}] {issue['type']}")
            print(f"    Location: {location}")
            if 'match' in issue:
                print(f"    Match: {issue['match']}")

        print(f"\n⚠️  Found {len(all_issues)} potential issue(s)")
        print("   Please review and fix if necessary")
        return 1
    else:
        print("\n✅ No security issues detected")
        return 0


if __name__ == "__main__":
    sys.exit(main())
