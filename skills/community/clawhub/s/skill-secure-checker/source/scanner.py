#!/usr/bin/env python3
"""
Core security scanner engine
Scans Python code files for security vulnerabilities
"""

import os
import re
import ast
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Severity weights for risk score calculation
SEVERITY_WEIGHTS = {
    "low": 1,
    "medium": 5,
    "high": 20,
    "critical": 50
}

class SecurityScanner:
    def __init__(self, skill_path: str, virustotal_api_key: Optional[str] = None,
                 severity_threshold: str = "low", verbose: bool = False):
        self.skill_path = Path(skill_path).resolve()
        self.virustotal_api_key = virustotal_api_key
        self.severity_threshold = severity_threshold
        self.verbose = verbose
        self.issues = []
        self.files_scanned = 0
        self.lines_scanned = 0

    def scan(self) -> Dict[str, Any]:
        """Main scanning entry point"""
        if not self.skill_path.exists():
            raise FileNotFoundError(f"Skill path does not exist: {self.skill_path}")

        # Scan Python files
        py_files = list(self.skill_path.rglob("*.py"))
        for py_file in py_files:
            self._scan_file(py_file)

        # Scan configuration files for secrets
        config_files = list(self.skill_path.rglob("*.json")) + list(self.skill_path.rglob("*.yaml")) + list(self.skill_path.rglob("*.yml"))
        for cfg_file in config_files:
            self._scan_config_file(cfg_file)

        # Check for hardcoded secrets in any text file
        text_files = [f for f in self.skill_path.rglob("*") if f.is_file() and f.suffix in ['.txt', '.md', '.sh', '.env', '.cfg', '.ini']]
        for txt_file in text_files[:10]:  # Limit to avoid scanning too many files
            self._scan_text_file(txt_file)

        # Optional VirusTotal scan
        if self.virustotal_api_key:
            self._scan_with_virustotal(py_files[:5])  # Limit to first 5 files

        return self._generate_report()

    def _scan_file(self, filepath: Path):
        """Scan a single Python file"""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Could not read {filepath}: {e}")
            return

        self.files_scanned += 1
        self.lines_scanned += len(content.splitlines())

        # Parse AST first for structural analysis
        try:
            tree = ast.parse(content)
            self._scan_ast(tree, filepath, content)
        except SyntaxError as e:
            self._add_issue(
                file=str(filepath.relative_to(self.skill_path)),
                line=e.lineno or 1,
                severity="low",
                issue_type="syntax_error",
                message=f"Syntax error in Python file: {e.msg}",
                snippet=content.splitlines()[e.lineno-1] if e.lineno and e.lineno <= len(content.splitlines()) else ""
            )

        # Regex-based scanning (complementary)
        self._scan_regex(content, filepath)

    def _scan_ast(self, tree: ast.AST, filepath: Path, full_content: str):
        """AST-based security analysis"""
        for node in ast.walk(tree):
            # Check for eval/exec calls
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node.func)
                if func_name in ['eval', 'exec', 'compile', '__import__']:
                    snippet = full_content.splitlines()[node.lineno-1] if node.lineno else ""
                    self._add_issue(
                        file=str(filepath.relative_to(self.skill_path)),
                        line=node.lineno,
                        severity="high" if func_name in ['eval', 'exec'] else "medium",
                        issue_type="dangerous_function",
                        message=f"Dangerous function '{func_name}' used - potential code injection risk",
                        snippet=snippet.strip()
                    )

                # Check for subprocess with shell=True
                if func_name == 'Popen' and isinstance(node.func, ast.Attribute):
                    if (isinstance(node.func.value, ast.Name) and node.func.value.id == 'subprocess'):
                        has_shell_true = any(
                            kw.arg == 'shell' and isinstance(kw.value, ast.Constant) and kw.value.value is True
                            for kw in node.keywords
                        )
                        if has_shell_true:
                            snippet = full_content.splitlines()[node.lineno-1] if node.lineno else ""
                            self._add_issue(
                                file=str(filepath.relative_to(self.skill_path)),
                                line=node.lineno,
                                severity="high",
                                issue_type="dangerous_function",
                                message="subprocess.Popen with shell=True - command injection risk",
                                snippet=snippet.strip()
                            )

            # Check for pickle.loads
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if (node.func.attr == 'loads' and isinstance(node.func.value, ast.Name) and
                    node.func.value.id == 'pickle'):
                    snippet = full_content.splitlines()[node.lineno-1] if node.lineno else ""
                    self._add_issue(
                        file=str(filepath.relative_to(self.skill_path)),
                        line=node.lineno,
                        severity="high",
                        issue_type="dangerous_function",
                        message="pickle.loads() - arbitrary code execution risk",
                        snippet=snippet.strip()
                    )

            # Check for os.system
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if (node.func.attr == 'system' and isinstance(node.func.value, ast.Name) and
                    node.func.value.id == 'os'):
                    snippet = full_content.splitlines()[node.lineno-1] if node.lineno else ""
                    self._add_issue(
                        file=str(filepath.relative_to(self.skill_path)),
                        line=node.lineno,
                        severity="high",
                        issue_type="dangerous_function",
                        message="os.system() - command execution risk",
                        snippet=snippet.strip()
                    )

    def _scan_regex(self, content: str, filepath: Path):
        """Regex-based pattern matching for secrets and other issues"""
        lines = content.splitlines()

        # Hardcoded secret patterns
        secret_patterns = [
            (r'(?i)(api[_-]?key|secret|password|token|credentials?)\s*=\s*["\'][^"\']{20,}["\']', 'hardcoded_secret', 'high'),
            (r'(?i)sk-[-a-zA-Z0-9]{20,}', 'hardcoded_secret', 'critical'),  # OpenAI key pattern
            (r'AIza[0-9A-Za-z\\-_]{35}', 'hardcoded_secret', 'critical'),  # Google API key
            (r'ghp_[0-9a-zA-Z]{36}', 'hardcoded_secret', 'critical'),  # GitHub PAT
            (r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}', 'hardcoded_secret', 'critical'),  # JWT
        ]

        for line_num, line in enumerate(lines, 1):
            for pattern, issue_type, severity in secret_patterns:
                if re.search(pattern, line):
                    # Skip if it's a comment or docstring
                    stripped = line.strip()
                    if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                        continue
                    self._add_issue(
                        file=str(filepath.relative_to(self.skill_path)),
                        line=line_num,
                        severity=severity,
                        issue_type=issue_type,
                        message="Potential hardcoded secret detected",
                        snippet=line.strip()[:80]
                    )
                    break  # Only report once per line

        # Check for HTTP URLs (should be HTTPS)
        for line_num, line in enumerate(lines, 1):
            if 'http://' in line and 'https://' not in line:
                self._add_issue(
                    file=str(filepath.relative_to(self.skill_path)),
                    line=line_num,
                    severity="medium",
                    issue_type="insecure_communication",
                    message="HTTP URL found - should use HTTPS",
                    snippet=line.strip()[:80]
                )

        # Check for path traversal patterns
        if '../' in content or '..\\' in content:
            for line_num, line in enumerate(lines, 1):
                if re.search(r'\.\.[/\\]', line):
                    self._add_issue(
                        file=str(filepath.relative_to(self.skill_path)),
                        line=line_num,
                        severity="medium",
                        issue_type="path_traversal",
                        message="Path traversal pattern detected - ensure input validation",
                        snippet=line.strip()[:80]
                    )

    def _scan_config_file(self, filepath: Path):
        """Scan config files for secrets"""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except:
            return

        lines = content.splitlines()
        secret_keywords = ['api_key', 'secret', 'password', 'token', 'private_key']

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//'):
                continue

            for keyword in secret_keywords:
                if keyword in line.lower():
                    # Check if it contains a value
                    if ':' in line or '=' in line:
                        self._add_issue(
                            file=str(filepath.relative_to(self.skill_path)),
                            line=line_num,
                            severity="medium",
                            issue_type="config_secret",
                            message=f"Potential secret in config file: {keyword}",
                            snippet=line.strip()[:80]
                        )
                        break

    def _scan_text_file(self, filepath: Path):
        """Scan text files for obvious secrets"""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except:
            return

        # Simple pattern: long base64-like strings or high entropy
        for line_num, line in enumerate(content.splitlines(), 1):
            # Look for strings that look like API keys (20+ alphanumeric chars)
            if re.search(r'[A-Za-z0-9+/]{40,}=*', line) and any(kw in line.lower() for kw in ['key', 'secret', 'token']):
                self._add_issue(
                    file=str(filepath.relative_to(self.skill_path)),
                    line=line_num,
                    severity="medium",
                    issue_type="potential_secret",
                    message="Long encoded string with key-like name",
                    snippet=line.strip()[:80]
                )

    def _scan_with_virustotal(self, files: List[Path]):
        """Optional VirusTotal file reputation check"""
        # Placeholder for future implementation
        # Will need: requests library, API key management, rate limit handling
        if self.verbose:
            print(f"🔍 VirusTotal scan requested but not yet implemented (future version)")
        pass

    def _add_issue(self, file: str, line: int, severity: str, issue_type: str, message: str, snippet: str = ""):
        """Add a security issue to the findings"""
        self.issues.append({
            "file": file,
            "line": line,
            "severity": severity,
            "type": issue_type,
            "message": message,
            "snippet": snippet
        })

    def _get_func_name(self, node: ast.AST) -> str:
        """Extract function name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return "unknown"

    def _generate_report(self) -> Dict[str, Any]:
        """Generate summary report"""
        # Calculate risk score
        score = sum(SEVERITY_WEIGHTS.get(issue["severity"], 0) for issue in self.issues)

        # Determine risk level based on max severity present
        severities = [issue["severity"] for issue in self.issues]
        if "critical" in severities:
            risk_level = "critical"
        elif "high" in severities:
            risk_level = "high"
        elif "medium" in severities:
            risk_level = "medium"
        else:
            risk_level = "low"

        # Filter by threshold
        threshold_weight = SEVERITY_WEIGHTS[self.severity_threshold]
        filtered_issues = [
            issue for issue in self.issues
            if SEVERITY_WEIGHTS.get(issue["severity"], 0) >= threshold_weight
        ]

        return {
            "skill": self.skill_path.name,
            "scan_time": datetime.utcnow().isoformat() + "Z",
            "total_files": self.files_scanned,
            "total_lines": self.lines_scanned,
            "findings": len(filtered_issues),
            "risk_score": min(score, 100),  # Cap at 100
            "risk_level": risk_level,
            "issues": filtered_issues,
            "configuration": {
                "severity_threshold": self.severity_threshold,
                "virustotal_enabled": self.virustotal_api_key is not None
            }
        }