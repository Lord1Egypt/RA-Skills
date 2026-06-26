#!/usr/bin/env python3
"""
Skill Security Scanner
Scans OpenClaw skills for security vulnerabilities before installation.
"""

import os
import re
import sys
import json
import yaml
import zipfile
from pathlib import Path
from typing import List, Dict, Tuple

# Severity levels
CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"
INFO = "INFO"

# Security checks
CHECKS = {
    # Critical - Block installation
    CRITICAL: [
        {
            "name": "exec/eval with user input",
            "pattern": r'(exec|eval)\s*\([^)]*(?:request|input|user|arg|param|body|json|data|stdin)',
            "description": "Dynamic code execution with potentially unsanitized user input",
            "severity": CRITICAL
        },
        {
            "name": "Hardcoded credentials",
            "pattern": r'(password|secret|api_key|apikey|token)\s*=\s*["\'][^"\']{8,}["\']',
            "description": "Hardcoded credentials found - will be exposed to users",
            "severity": CRITICAL,
            "exclude_patterns": [
                r'your[-_](api|secret|password|token|key)',  # Placeholders
                r'op://',  # 1Password CLI URIs
                r'<[^>]+>',  # XML/HTML tags
                r'\{\{.*\}\}',  # Template variables
            ]
        },
        {
            "name": "Environment variable exfiltration",
            "pattern": r'(curl|wget|requests\.post|httpx)\s*\([^)]*os\.environ|os\.environ\[.*\]\s*(?:curl|wget|requests\.post|httpx)',
            "description": "Environment variables being sent to external servers",
            "severity": CRITICAL
        },
        {
            "name": "Shell injection via user input",
            "pattern": r'(subprocess|os\.system|os\.popen)\s*\([^)]*(?:request|input|user|arg|param|body|json|data|stdin)',
            "description": "Shell command execution with potentially unsanitized user input",
            "severity": CRITICAL
        },
        {
            "name": "Hidden network requests",
            "pattern": r'(requests|httpx|urllib)\.[a-z]+\s*\(\s*["\']https?://',
            "description": "Network requests to external servers - verify legitimacy",
            "severity": HIGH
        },
        {
            "name": "File exfiltration",
            "pattern": r'(open|read)\s*\([^)]*os\.environ|os\.environ\[.*\]\s*.*(?:open|read)',
            "description": "Reading files based on environment variables - potential data theft",
            "severity": CRITICAL
        },
        {
            "name": "Base64 encoded suspicious content",
            "pattern": r'import base64.*base64\.(b64decode|b85decode)',
            "description": "Encoded content detected - verify it does not hide malicious code",
            "severity": HIGH
        },
    ],
    # High - Warn and require confirmation
    HIGH: [
        {
            "name": "curl/wget without timeout",
            "pattern": r'(curl|wget)\s+[^>-]*(-m|--max-time)\s*(?![\d])',
            "description": "Network requests without timeout - may hang indefinitely",
            "severity": HIGH
        },
        {
            "name": "os.system/shell commands",
            "pattern": r'os\.system\s*\(|subprocess\.call\s*\(|subprocess\.run\s*\([^)]*shell\s*=\s*True',
            "description": "Shell command execution - verify commands are safe",
            "severity": HIGH
        },
        {
            "name": "Anonymous network connections",
            "pattern": r'socket\.connect\s*\(',
            "description": "Raw socket connections - verify destination is legitimate",
            "severity": HIGH
        },
        {
            "name": "Sensitive path access",
            "pattern": r'/(?:etc/passwd|etc/shadow|proc/|/sys/)',
            "description": "Access to sensitive system paths",
            "severity": HIGH
        },
    ],
    # Medium - Warn
    MEDIUM: [
        {
            "name": "eval usage",
            "pattern": r'\beval\s*\(',
            "description": "eval() usage - potential security risk if input is not sanitized",
            "severity": MEDIUM
        },
        {
            "name": "exec usage",
            "pattern": r'\bexec\s*\(',
            "description": "exec() usage - potential security risk if input is not sanitized",
            "severity": MEDIUM
        },
        {
            "name": "Dynamic import",
            "pattern": r'__import__|importlib',
            "description": "Dynamic module import - verify the module is trusted",
            "severity": MEDIUM
        },
        {
            "name": "Pickle deserialization",
            "pattern": r'pickle\.loads?|pickle\.load\s*\(',
            "description": "Pickle deserialization - can execute arbitrary code",
            "severity": MEDIUM
        },
        {
            "name": "YAML unsafe load",
            "pattern": r'yaml\.load\s*\([^)]*Loader\s*=\s*yaml\.Loader',
            "description": "Unsafe YAML loading - use yaml.safe_load instead",
            "severity": MEDIUM
        },
    ],
    # Low - Info
    LOW: [
        {
            "name": "Subprocess without capture",
            "pattern": r'subprocess\.(run|call|check_output)\s*\([^)]*(?:stdout|stderr)\s*=\s*None',
            "description": "Subprocess output not captured - may expose sensitive data",
            "severity": LOW
        },
        {
            "name": "Long timeout values",
            "pattern": r'timeout\s*=\s*[0-9]{5,}',
            "description": "Very long timeout value - may cause hanging",
            "severity": LOW
        },
    ],
    # Info
    INFO: [
        {
            "name": "No error handling",
            "pattern": r'except\s*:\s*pass\s*except\s*Exception\s*:\s*pass',
            "description": "Broad exception catching - may hide security issues",
            "severity": INFO
        },
        {
            "name": "Print sensitive data",
            "pattern": r'print\s*\([^)]*(?:password|secret|key|token)',
            "description": "Printing potentially sensitive information",
            "severity": INFO
        },
    ]
}


class SkillScanner:
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.issues: List[Dict] = []
        
    def scan_file(self, filepath: Path, content: str) -> None:
        """Scan a single file for security issues."""
        for severity_level, checks in CHECKS.items():
            for check in checks:
                matches = re.finditer(check["pattern"], content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    # Check if this match should be excluded (false positive)
                    match_text = match.group()
                    exclude_patterns = check.get("exclude_patterns", [])
                    is_excluded = False
                    
                    for exclude_pattern in exclude_patterns:
                        if re.search(exclude_pattern, match_text, re.IGNORECASE):
                            is_excluded = True
                            break
                    
                    if is_excluded:
                        continue
                    
                    # Calculate line number
                    line_num = content[:match.start()].count('\n') + 1
                    
                    self.issues.append({
                        "severity": severity_level,
                        "file": str(filepath.relative_to(self.skill_path)),
                        "line": line_num,
                        "check": check["name"],
                        "description": check["description"],
                        "match": match.group()[:100]
                    })
    
    def scan_skill(self) -> Tuple[List[Dict], Dict]:
        """Scan the entire skill for security issues."""
        self.issues = []
        
        # Check if it's a .skill file (zip) or directory
        if self.skill_path.suffix == '.skill':
            with zipfile.ZipFile(self.skill_path, 'r') as zf:
                for name in zf.namelist():
                    if name.endswith(('.py', '.sh', '.js', '.ts', '.yaml', '.yml', '.json', '.md')):
                        try:
                            content = zf.read(name).decode('utf-8', errors='ignore')
                            # Create a fake Path object for the zip file
                            fake_path = Path(name)
                            self.scan_file(fake_path, content)
                        except Exception:
                            pass
        elif self.skill_path.is_file():
            # Scan a single file
            try:
                content = self.skill_path.read_text(encoding='utf-8', errors='ignore')
                self.scan_file(self.skill_path, content)
            except Exception:
                pass
        else:
            # Scan directory
            for filepath in self.skill_path.rglob('*'):
                if filepath.is_file() and not filepath.name.startswith('.'):
                    try:
                        content = filepath.read_text(encoding='utf-8', errors='ignore')
                        self.scan_file(filepath, content)
                    except Exception:
                        pass
        
        return self.issues, self.get_summary()
    
    def get_summary(self) -> Dict:
        """Get a summary of issues by severity."""
        summary = {CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0, INFO: 0}
        for issue in self.issues:
            summary[issue["severity"]] += 1
        return summary
    
    def should_block_install(self) -> bool:
        """Determine if installation should be blocked."""
        for issue in self.issues:
            if issue["severity"] == CRITICAL:
                return True
        return False
    
    def get_recommendation(self) -> str:
        """Get installation recommendation."""
        if self.should_block_install():
            return "BLOCK"
        elif any(i["severity"] == HIGH for i in self.issues):
            return "WARN"
        elif self.issues:
            return "CAUTION"
        else:
            return "ALLOW"


def print_report(issues: List[Dict], summary: Dict, recommendation: str) -> None:
    """Print a formatted security report."""
    print("\n" + "=" * 60)
    print("🔒 SKILL SECURITY SCAN REPORT")
    print("=" * 60)
    
    print("\n📊 SUMMARY:")
    print(f"   {'🔴 CRITICAL':<15} {summary[CRITICAL]}")
    print(f"   {'🟠 HIGH':<15} {summary[HIGH]}")
    print(f"   {'🟡 MEDIUM':<15} {summary[MEDIUM]}")
    print(f"   {'🔵 LOW':<15} {summary[LOW]}")
    print(f"   {'⚪ INFO':<15} {summary[INFO]}")
    
    print("\n📋 RECOMMENDATION:")
    if recommendation == "BLOCK":
        print("   🚫 **BLOCK INSTALLATION** - Critical security issues found")
    elif recommendation == "WARN":
        print("   ⚠️  **WARN** - High risk issues detected, review before installing")
    elif recommendation == "CAUTION":
        print("   ⚡ **CAUTION** - Minor issues found, install at your own risk")
    else:
        print("   ✅ **ALLOW** - No major security issues detected")
    
    if issues:
        print("\n📝 DETAILED ISSUES:")
        # Group by severity
        for severity in [CRITICAL, HIGH, MEDIUM, LOW, INFO]:
            severity_issues = [i for i in issues if i["severity"] == severity]
            if severity_issues:
                emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "⚪"}.get(severity, "•")
                print(f"\n{emoji} {severity}:")
                for issue in severity_issues[:10]:  # Limit to 10 per severity
                    print(f"   • {issue['file']}:{issue['line']}")
                    print(f"     {issue['check']}")
                    print(f"     → {issue['description']}")
                if len(severity_issues) > 10:
                    print(f"   ... and {len(severity_issues) - 10} more")
    
    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 skill_audit.py <skill-path-or-file.skill>")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    
    if not os.path.exists(skill_path):
        print(f"Error: {skill_path} not found")
        sys.exit(1)
    
    scanner = SkillScanner(skill_path)
    issues, summary = scanner.scan_skill()
    recommendation = scanner.get_recommendation()
    
    print_report(issues, summary, recommendation)
    
    # Exit code based on recommendation
    if recommendation == "BLOCK":
        sys.exit(2)
    elif recommendation == "WARN":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
