import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

class SkillAuditor:
    def __init__(self, config_path: str = None):
        """
        Initialize the SkillAuditor with security rules
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            # Default configuration
            self.config = {
                "security_rules": {
                    "forbidden_patterns": [
                        {
                            "pattern": "exec\\(.*\\)",
                            "severity": "critical",
                            "description": "Dynamic code execution"
                        },
                        {
                            "pattern": "eval\\(.*\\)",
                            "severity": "critical",
                            "description": "Code evaluation function"
                        },
                        {
                            "pattern": "importlib\\.",
                            "severity": "high",
                            "description": "Dynamic module loading"
                        },
                        {
                            "pattern": "subprocess\\.",
                            "severity": "high",
                            "description": "System command execution"
                        },
                        {
                            "pattern": "os\\.system",
                            "severity": "high",
                            "description": "System command execution"
                        },
                        {
                            "pattern": "os\\.popen",
                            "severity": "high",
                            "description": "System command execution"
                        },
                        {
                            "pattern": "open\\([^,]*,[^,]*['\\\"]w[^\\\"]*['\\\"]",
                            "severity": "medium",
                            "description": "File write operation"
                        },
                        {
                            "pattern": "requests\\.post",
                            "severity": "medium",
                            "description": "External data transmission"
                        },
                        {
                            "pattern": "socket\\.",
                            "severity": "medium",
                            "description": "Network socket operations"
                        }
                    ],
                    "suspicious_patterns": [
                        {
                            "pattern": ".*password.*",
                            "severity": "medium",
                            "description": "Contains password in code"
                        },
                        {
                            "pattern": ".*token.*",
                            "severity": "medium",
                            "description": "Contains token in code"
                        },
                        {
                            "pattern": ".*secret.*",
                            "severity": "medium",
                            "description": "Contains secret in code"
                        }
                    ]
                },
                "allowed_imports": [
                    "json",
                    "os",
                    "sys",
                    "re",
                    "urllib",
                    "pathlib",
                    "datetime",
                    "time",
                    "base64",
                    "hashlib"
                ]
            }

    def scan_file(self, file_path: str) -> List[Dict]:
        """
        Scan a single file for security issues
        """
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # If it's not a text file, skip it
            return issues
        except Exception:
            # If we can't read the file for any reason, skip it
            return issues

        # Check for forbidden patterns
        for rule in self.config["security_rules"]["forbidden_patterns"]:
            matches = re.finditer(rule["pattern"], content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    "file": file_path,
                    "line": content.count('\n', 0, match.start()) + 1,
                    "pattern": rule["pattern"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "matched_text": match.group(0)
                })

        # Check for suspicious patterns
        for rule in self.config["security_rules"]["suspicious_patterns"]:
            matches = re.finditer(rule["pattern"], content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    "file": file_path,
                    "line": content.count('\n', 0, match.start()) + 1,
                    "pattern": rule["pattern"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "matched_text": match.group(0)
                })

        return issues

    def scan_skill_directory(self, skill_path: str) -> Dict:
        """
        Scan an entire skill directory for security issues
        """
        all_issues = []
        skill_path = Path(skill_path)
        
        # Check all Python and shell files in the skill directory
        for file_path in skill_path.rglob("*"):
            if file_path.is_file() and (file_path.suffix in ['.py', '.sh', '.js', '.ts', '.json', '.yaml', '.yml'] or 
                                       file_path.name in ['SKILL.md', 'skill.json']):
                issues = self.scan_file(str(file_path))
                all_issues.extend(issues)

        # Analyze imports in Python files
        import_issues = self._check_imports(skill_path)
        all_issues.extend(import_issues)

        # Group issues by severity
        critical_issues = [issue for issue in all_issues if issue["severity"] == "critical"]
        high_issues = [issue for issue in all_issues if issue["severity"] == "high"]
        medium_issues = [issue for issue in all_issues if issue["severity"] == "medium"]

        return {
            "skill_path": str(skill_path),
            "total_issues": len(all_issues),
            "critical_issues": critical_issues,
            "high_issues": high_issues,
            "medium_issues": medium_issues,
            "all_issues": all_issues
        }

    def _check_imports(self, skill_path: Path) -> List[Dict]:
        """
        Check for potentially dangerous imports in Python files
        """
        issues = []
        
        for py_file in skill_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all import statements
                import_matches = re.findall(r'^\s*(import|from)\s+([a-zA-Z_][a-zA-Z0-9_.]*)', content, re.MULTILINE)
                
                for import_type, module_name in import_matches:
                    # Extract just the main module name (before any dots)
                    main_module = module_name.split('.')[0]
                    
                    if main_module not in self.config["allowed_imports"]:
                        issues.append({
                            "file": str(py_file),
                            "line": -1,  # We don't track line numbers here
                            "pattern": f"import {module_name}",
                            "severity": "medium",
                            "description": f"Potentially dangerous import: {module_name}",
                            "matched_text": f"{import_type} {module_name}"
                        })
            except Exception:
                # If we can't read the file, skip it
                continue
        
        return issues

    def generate_report(self, scan_result: Dict) -> str:
        """
        Generate a human-readable security report
        """
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("SKILL SECURITY AUDIT REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Skill Path: {scan_result['skill_path']}")
        report_lines.append(f"Total Issues Found: {scan_result['total_issues']}")
        report_lines.append("")

        if scan_result['critical_issues']:
            report_lines.append("CRITICAL ISSUES (IMMEDIATE ATTENTION REQUIRED):")
            report_lines.append("-" * 50)
            for issue in scan_result['critical_issues']:
                report_lines.append(f"File: {issue['file']}")
                report_lines.append(f"Severity: {issue['severity'].upper()}")
                report_lines.append(f"Description: {issue['description']}")
                report_lines.append(f"Matched: {issue['matched_text']}")
                if issue['line'] != -1:
                    report_lines.append(f"Line: {issue['line']}")
                report_lines.append("")
        
        if scan_result['high_issues']:
            report_lines.append("HIGH RISK ISSUES:")
            report_lines.append("-" * 30)
            for issue in scan_result['high_issues']:
                report_lines.append(f"File: {issue['file']}")
                report_lines.append(f"Severity: {issue['severity'].upper()}")
                report_lines.append(f"Description: {issue['description']}")
                report_lines.append(f"Matched: {issue['matched_text']}")
                if issue['line'] != -1:
                    report_lines.append(f"Line: {issue['line']}")
                report_lines.append("")

        if scan_result['medium_issues']:
            report_lines.append("MEDIUM RISK ISSUES:")
            report_lines.append("-" * 30)
            for issue in scan_result['medium_issues']:
                report_lines.append(f"File: {issue['file']}")
                report_lines.append(f"Severity: {issue['severity'].upper()}")
                report_lines.append(f"Description: {issue['description']}")
                report_lines.append(f"Matched: {issue['matched_text']}")
                if issue['line'] != -1:
                    report_lines.append(f"Line: {issue['line']}")
                report_lines.append("")

        if not scan_result['all_issues']:
            report_lines.append("NO SECURITY ISSUES FOUND")
            report_lines.append("This skill appears to be secure based on the current audit rules.")

        report_lines.append("=" * 60)
        return "\n".join(report_lines)