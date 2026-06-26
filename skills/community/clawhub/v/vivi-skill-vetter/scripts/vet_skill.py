#!/usr/bin/env python3
"""
Skill Security Vetting Script

Scans a skill directory for potential security issues before installation.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    CRITICAL = "🚨 CRITICAL"
    WARNING = "⚠️ WARNING"
    INFO = "ℹ️ INFO"
    BOUNDARY = "🚧 BOUNDARY"  # 三区边界检测


class BoundaryZone(Enum):
    """三区安全边界定义"""
    MY_FILES = "🚫 MY FILES"      # 禁区 - 私人数据
    SHARED_FILES = "✅ SHARED FILES"  # 协作区 - 共享文件
    AGENT_BRAIN = "🧠 AGENT BRAIN"   # 代理记忆区


@dataclass
class BoundaryFinding:
    """边界违规发现"""
    zone: BoundaryZone
    path: str
    file: str
    line: int
    context: str
    description: str
    recommendation: str  # 建议用户如何处理


@dataclass
class Finding:
    severity: Severity
    category: str
    file: str
    line: int
    pattern: str
    context: str
    description: str


@dataclass
class VetResult:
    critical: List[Finding] = field(default_factory=list)
    warnings: List[Finding] = field(default_factory=list)
    info: List[Finding] = field(default_factory=list)
    boundary: List[BoundaryFinding] = field(default_factory=list)  # 三区边界违规
    
    def add(self, finding: Finding):
        if finding.severity == Severity.CRITICAL:
            self.critical.append(finding)
        elif finding.severity == Severity.WARNING:
            self.warnings.append(finding)
        else:
            self.info.append(finding)


# Critical patterns - block installation
CRITICAL_PATTERNS = [
    # Remote code execution
    (r'curl\s+[^|]*\|\s*(bash|sh|zsh|fish)', "Remote code execution via curl | shell"),
    (r'wget\s+[^|]*\|\s*(bash|sh|zsh|fish)', "Remote code execution via wget | shell"),
    (r'curl\s+.*\|\s*sh', "Remote code execution via curl | sh"),
    
    # Eval and exec with dynamic content
    (r'eval\s*\(["\']?\$', "Dynamic eval with variable"),
    (r'exec\s*\(["\']?\$', "Dynamic exec with variable"),
    (r'exec\s*\(["\']?`', "Dynamic exec with command substitution"),
    
    # Privilege escalation
    (r'\bsudo\b(?!\s+ls\b|\s+cat\b|\s+head\b)', "Sudo usage (potential privilege escalation)"),
    (r'chmod\s+777\b', "Overly permissive file permissions (777)"),
    (r'chown\s+root\b', "Changing ownership to root"),
    
    # Data exfiltration
    (r'curl\s+.*-d\s+@/etc/passwd', "Exfiltrating /etc/passwd"),
    (r'curl\s+.*-d\s+.*\.ssh', "Exfiltrating SSH keys"),
    (r'nc\s+.*-e\s+/bin/(sh|bash)', "Reverse shell via netcat"),
    
    # System destruction
    (r'rm\s+-rf\s+/(?!\w)', "Dangerous rm -rf targeting root"),
    (r'rm\s+-rf\s+~(?!\w)', "Dangerous rm -rf targeting home"),
    (r'rm\s+-rf\s+\*', "Dangerous rm -rf * pattern"),
    (r':\(\)\s*\{\s*:\|:&\s*\};:', "Fork bomb"),
    
    # Hidden execution
    (r'base64\.b64decode\s*\(["\'][A-Za-z0-9+/=]+["\']\)\s*\)', "Decoding and executing hidden base64"),
    (r'exec\s*\(\s*base64', "Executing base64 decoded content"),
]

# Warning patterns - review carefully
WARNING_PATTERNS = [
    # Environment access (using escaped dollar sign pattern)
    (r'[\$]HOME\b', "HOME environment variable access"),
    (r'[\$]USER\b', "USER environment variable access"),
    (r'~/.ssh/', "SSH directory access"),
    (r'~/.bashrc', "Shell config access"),
    (r'~/.zshrc', "Shell config access"),
    (r'~/.config/', "Config directory access"),
    
    # Network operations
    (r'\bcurl\b', "HTTP request via curl"),
    (r'\bwget\b', "HTTP request via wget"),
    (r'\bnc\b(?!\s+static)', "Netcat usage (potential backdoor)"),
    (r'requests\.(get|post|put|delete)\s*\(', "HTTP request via Python requests"),
    (r'urllib\.request\.', "HTTP request via urllib"),
    (r'socket\.socket\s*\(', "Raw socket usage"),
    
    # Package installation
    (r'pip\s+install', "pip package installation"),
    (r'npm\s+install', "npm package installation"),
    (r'yarn\s+add', "yarn package installation"),
    (r'brew\s+install', "Homebrew package installation"),
    (r'apt\s+install', "apt package installation"),
    
    # Hidden files
    (r'\btouch\s+\.', "Creating hidden files"),
    (r'\bmkdir\s+\.', "Creating hidden directories"),
    (r'/\.(?!git|github|gitignore|env\.example)', "Hidden file/directory access"),
    
    # Obfuscation
    (r'base64\.b64decode', "Base64 decoding"),
    (r'__import__\s*\(', "Dynamic module import"),
    (r'getattr\s*\([^)]*\s*\+\s*', "Dynamic attribute access with string concat"),
    
    # External code
    (r'subprocess\.(call|run|Popen)\s*\([^)]*shell\s*=\s*True', "Shell command with shell=True"),
    (r'os\.system\s*\(', "os.system command execution"),
    (r'os\.popen\s*\(', "os.popen command execution"),
]

# Info patterns - notable but usually safe
INFO_PATTERNS = [
    (r'open\s*\([^)]*[\'"]w[\'"]', "File write operation"),
    (r'open\s*\([^)]*[\'"]a[\'"]', "File append operation"),
    (r'shutil\.(rmtree|move|copy)', "File system operations"),
    (r'json\.loads?\s*\(', "JSON parsing"),
    (r'yaml\.safe_load\s*\(', "YAML parsing"),
    (r'os\.environ', "Environment variable access"),
    (r'[\$]HOME/(?!\.(?:ssh|config|bashrc|zshrc))', "Home directory access"),
]

# 三区边界检测模式
BOUNDARY_MY_FILES = [
    # SSH 和密钥
    (r'~/.ssh/', "SSH 密钥目录 - MY FILES 禁区"),
    (r'~/.gnupg/', "GPG 密钥目录 - MY FILES 禁区"),
    (r'id_rsa', "RSA 私钥文件 - MY FILES 禁区"),
    (r'id_ed25519', "Ed25519 私钥文件 - MY FILES 禁区"),
    (r'\.pem\b', "PEM 证书文件 - MY FILES 禁区"),
    
    # 私人配置
    (r'~/.config/', "用户配置目录 - MY FILES 禁区"),
    (r'~/.bashrc', "Shell 配置 - MY FILES 禁区"),
    (r'~/.zshrc', "Shell 配置 - MY FILES 禁区"),
    (r'~/.gitconfig', "Git 配置 - MY FILES 禁区"),
    
    # 私人文件
    (r'~/Documents/', "私人文档目录 - MY FILES 禁区"),
    (r'~/Desktop/', "桌面目录 - MY FILES 禁区"),
    (r'~/Library/', "macOS Library - MY FILES 禁区"),
    (r'Dropbox/', "个人 Dropbox - MY FILES 禁区"),
    
    # 系统文件
    (r'/etc/passwd', "系统密码文件 - MY FILES 禁区"),
    (r'/etc/shadow', "系统密码文件 - MY FILES 禁区"),
    (r'/etc/hosts', "系统 hosts 文件 - MY FILES 禁区"),
]

BOUNDARY_SHARED_FILES = [
    # OpenClaw 工作区
    (r'\.openclaw/workspace/', "OpenClaw 工作区 - SHARED FILES 协作区"),
    (r'Projects/', "项目目录 - SHARED FILES 协作区"),
]

BOUNDARY_AGENT_BRAIN = [
    # 代理记忆区
    (r'MEMORY\.md', "代理长期记忆 - AGENT BRAIN"),
    (r'memory/\d{4}-\d{2}-\d{2}\.md', "代理日记 - AGENT BRAIN"),
    (r'AGENTS\.md', "代理配置 - AGENT BRAIN"),
    (r'IDENTITY\.md', "代理身份 - AGENT BRAIN"),
    (r'USER\.md', "用户配置 - AGENT BRAIN"),
]

# Three-Zone Security Boundary patterns
# 检测到访问禁区时，告知用户让用户判断

ZONE_MY_FILES = [
    # SSH and GPG keys
    (r'~?/\.ssh/', "🚫 MY FILES: SSH key directory"),
    (r'~?/\.gnupg/', "🚫 MY FILES: GPG key directory"),
    (r'id_rsa', "🚫 MY FILES: SSH private key"),
    (r'id_ed25519', "🚫 MY FILES: SSH private key"),
    
    # Private documents
    (r'~/Documents/', "🚫 MY FILES: Personal Documents folder"),
    (r'~/Desktop/', "🚫 MY FILES: Desktop folder"),
    (r'~/Library/', "🚫 MY FILES: macOS Library"),
    
    # System files
    (r'/etc/passwd', "🚫 MY FILES: System password file"),
    (r'/etc/shadow', "🚫 MY FILES: System shadow file"),
    (r'/etc/hosts', "🚫 MY FILES: System hosts file"),
    
    # Personal services
    (r'Dropbox/', "🚫 MY FILES: Personal Dropbox"),
    (r'iCloud', "🚫 MY FILES: iCloud storage"),
    
    # Credentials
    (r'\.env(?!\.example)', "🚫 MY FILES: Environment/credentials file"),
    (r'credentials\.json', "🚫 MY FILES: Credentials file"),
    (r'secrets?\.(json|yaml|yml|txt)', "🚫 MY FILES: Secrets file"),
]

ZONE_SHARED_FILES = [
    # OpenClaw workspace (shared collaboration)
    (r'\.openclaw/workspace/', "✅ SHARED FILES: OpenClaw workspace"),
    (r'~/Projects/', "✅ SHARED FILES: Projects folder"),
    
    # Common shared locations
    (r'/tmp/', "✅ SHARED FILES: Temporary directory"),
    (r'shared/', "✅ SHARED FILES: Shared folder"),
]

ZONE_AGENT_BRAIN = [
    # Agent's memory and learning
    (r'MEMORY\.md', "🧠 AGENT BRAIN: Long-term memory"),
    (r'memory/\d{4}-\d{2}-\d{2}\.md', "🧠 AGENT BRAIN: Daily notes"),
    (r'AGENTS\.md', "🧠 AGENT BRAIN: Agent configuration"),
    (r'IDENTITY\.md', "🧠 AGENT BRAIN: Agent identity"),
    (r'USER\.md', "🧠 AGENT BRAIN: User profile"),
    (r'HEARTBEAT\.md', "🧠 AGENT BRAIN: Heartbeat config"),
    (r'TOOLS\.md', "🧠 AGENT BRAIN: Tool notes"),
]


def find_files(skill_dir: Path) -> List[Path]:
    """Find all relevant files in skill directory"""
    files = []
    
    # Include common file types
    extensions = {'.py', '.sh', '.bash', '.zsh', '.js', '.ts', '.md', '.json', '.yaml', '.yml'}
    
    for ext in extensions:
        files.extend(skill_dir.rglob(f'*{ext}'))
    
    # Include files without extension that might be scripts
    for f in skill_dir.rglob('*'):
        if f.is_file() and f.suffix == '':
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')[:100]
                if content.startswith('#!'):
                    files.append(f)
            except:
                pass
    
    return sorted(set(files))


def scan_file(file_path: Path, patterns: List[Tuple[str, str]], severity: Severity) -> List[Finding]:
    """Scan a file for patterns"""
    findings = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.splitlines()
    except Exception as e:
        return findings
    
    for pattern, description in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        
        for i, line in enumerate(lines, 1):
            if regex.search(line):
                # Get some context
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 1)
                context = '\n'.join(lines[context_start:context_end])
                
                finding = Finding(
                    severity=severity,
                    category="security",
                    file=str(file_path),
                    line=i,
                    pattern=pattern,
                    context=context,
                    description=description
                )
                findings.append(finding)
    
    return findings


def check_skill_md(skill_dir: Path) -> List[str]:
    """Check SKILL.md validity"""
    issues = []
    skill_md = skill_dir / "SKILL.md"
    
    if not skill_md.exists():
        issues.append("SKILL.md not found - not a valid skill directory")
        return issues
    
    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        issues.append(f"Could not read SKILL.md: {e}")
        return issues
    
    # Check frontmatter
    if not content.startswith('---'):
        issues.append("SKILL.md missing YAML frontmatter")
        return issues
    
    # Check required fields
    if 'name:' not in content.split('---')[1] if '---' in content else '':
        issues.append("SKILL.md missing 'name' in frontmatter")
    
    if 'description:' not in content.split('---')[1] if '---' in content else '':
        issues.append("SKILL.md missing 'description' in frontmatter")
    
    return issues


def scan_boundary_zones(file_path: Path) -> List[Finding]:
    """Scan for three-zone security boundary access"""
    findings = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.splitlines()
    except Exception:
        return findings
    
    # Check MY FILES zone (most critical)
    for pattern, description in ZONE_MY_FILES:
        regex = re.compile(pattern, re.IGNORECASE)
        
        for i, line in enumerate(lines, 1):
            if regex.search(line):
                # Skip if it's in a comment explaining the pattern (not actual usage)
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//'):
                    continue
                
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 1)
                context = '\n'.join(lines[context_start:context_end])
                
                finding = Finding(
                    severity=Severity.CRITICAL,  # 升级为 CRITICAL 以引起注意
                    category="boundary_zone",
                    file=str(file_path),
                    line=i,
                    pattern=pattern,
                    context=context,
                    description=f"{description} - 请用户确认是否允许此访问"
                )
                findings.append(finding)
    
    # Check SHARED FILES zone (usually safe, just info)
    for pattern, description in ZONE_SHARED_FILES:
        regex = re.compile(pattern, re.IGNORECASE)
        
        for i, line in enumerate(lines, 1):
            if regex.search(line):
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 1)
                context = '\n'.join(lines[context_start:context_end])
                
                finding = Finding(
                    severity=Severity.INFO,
                    category="boundary_zone",
                    file=str(file_path),
                    line=i,
                    pattern=pattern,
                    context=context,
                    description=description
                )
                findings.append(finding)
    
    # Check AGENT BRAIN zone (normal for agent)
    for pattern, description in ZONE_AGENT_BRAIN:
        regex = re.compile(pattern, re.IGNORECASE)
        
        for i, line in enumerate(lines, 1):
            if regex.search(line):
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 1)
                context = '\n'.join(lines[context_start:context_end])
                
                finding = Finding(
                    severity=Severity.INFO,
                    category="boundary_zone",
                    file=str(file_path),
                    line=i,
                    pattern=pattern,
                    context=context,
                    description=description
                )
                findings.append(finding)
    
    return findings


def vet_skill(skill_dir: str, verbose: bool = False) -> VetResult:
    """Main vetting function"""
    skill_path = Path(skill_dir).resolve()
    
    if not skill_path.exists():
        print(f"Error: Directory not found: {skill_path}")
        sys.exit(1)
    
    if not skill_path.is_dir():
        print(f"Error: Not a directory: {skill_path}")
        sys.exit(1)
    
    result = VetResult()
    
    # Check SKILL.md
    skill_md_issues = check_skill_md(skill_path)
    for issue in skill_md_issues:
        result.add(Finding(
            severity=Severity.WARNING,
            category="structure",
            file="SKILL.md",
            line=0,
            pattern="",
            context="",
            description=issue
        ))
    
    # Find all files
    files = find_files(skill_path)
    
    if verbose:
        print(f"Scanning {len(files)} files...")
    
    # Scan for patterns
    for file_path in files:
        rel_path = file_path.relative_to(skill_path)
        
        # Skip common non-security files
        if file_path.name in ['license.txt', 'LICENSE', 'README.md']:
            continue
        
        # Critical patterns
        for finding in scan_file(file_path, CRITICAL_PATTERNS, Severity.CRITICAL):
            finding.file = str(rel_path)
            result.add(finding)
        
        # Warning patterns
        for finding in scan_file(file_path, WARNING_PATTERNS, Severity.WARNING):
            finding.file = str(rel_path)
            result.add(finding)
        
        # Three-zone boundary detection
        for finding in scan_boundary_zones(file_path):
            finding.file = str(rel_path)
            result.add(finding)
        
        # Info patterns
        if verbose:
            for finding in scan_file(file_path, INFO_PATTERNS, Severity.INFO):
                finding.file = str(rel_path)
                result.add(finding)
    
    return result


def format_output(result: VetResult, verbose: bool = False) -> str:
    """Format vetting result as readable output"""
    lines = []
    lines.append("=" * 60)
    lines.append("SKILL SECURITY VETTING REPORT")
    lines.append("=" * 60)
    lines.append("")
    
    # Critical issues
    if result.critical:
        lines.append(f"🚨 CRITICAL ISSUES ({len(result.critical)})")
        lines.append("-" * 40)
        for f in result.critical:
            lines.append(f"")
            lines.append(f"  File: {f.file}:{f.line}")
            lines.append(f"  Issue: {f.description}")
            if verbose:
                lines.append(f"  Pattern: {f.pattern}")
                lines.append(f"  Context:")
                for line in f.context.split('\n'):
                    lines.append(f"    {line}")
        lines.append("")
    
    # Warnings
    if result.warnings:
        lines.append(f"⚠️ WARNINGS ({len(result.warnings)})")
        lines.append("-" * 40)
        for f in result.warnings:
            lines.append(f"  • {f.file}:{f.line} - {f.description}")
        lines.append("")
    
    # Info
    if verbose and result.info:
        lines.append(f"ℹ️ INFO ({len(result.info)})")
        lines.append("-" * 40)
        for f in result.info:
            lines.append(f"  • {f.file}:{f.line} - {f.description}")
        lines.append("")
    
    # Summary
    lines.append("=" * 60)
    lines.append("SUMMARY")
    lines.append("=" * 60)
    
    if result.critical:
        lines.append("")
        lines.append("🚨 VERDICT: BLOCK")
        lines.append("   This skill contains CRITICAL security issues.")
        lines.append("   DO NOT INSTALL.")
    elif result.warnings:
        lines.append("")
        lines.append("⚠️ VERDICT: CAUTION")
        lines.append("   This skill has warnings that require review.")
        lines.append("   Review each warning before installing.")
        lines.append("")
        lines.append("   Questions to ask:")
        lines.append("   1. Is the skill from a trusted source?")
        lines.append("   2. Are the flagged patterns necessary for the skill's purpose?")
        lines.append("   3. Is there a safer alternative skill?")
    else:
        lines.append("")
        lines.append("✅ VERDICT: PASS")
        lines.append("   No critical issues or warnings found.")
        lines.append("   Safe to install (always verify source).")
    
    lines.append("")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Vet a skill for security issues before installation'
    )
    parser.add_argument('skill_dir', help='Path to skill directory')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Show detailed output including info-level findings')
    parser.add_argument('-o', '--output', help='Output file for report')
    parser.add_argument('-j', '--json', action='store_true',
                        help='Output as JSON')
    
    args = parser.parse_args()
    
    result = vet_skill(args.skill_dir, args.verbose)
    
    if args.json:
        output = json.dumps({
            'critical': len(result.critical),
            'warnings': len(result.warnings),
            'info': len(result.info),
            'verdict': 'BLOCK' if result.critical else ('CAUTION' if result.warnings else 'PASS'),
            'findings': {
                'critical': [
                    {'file': f.file, 'line': f.line, 'description': f.description}
                    for f in result.critical
                ],
                'warnings': [
                    {'file': f.file, 'line': f.line, 'description': f.description}
                    for f in result.warnings
                ],
                'info': [
                    {'file': f.file, 'line': f.line, 'description': f.description}
                    for f in result.info
                ] if args.verbose else []
            }
        }, indent=2)
    else:
        output = format_output(result, args.verbose)
    
    if args.output:
        Path(args.output).write_text(output)
        print(f"Report saved to: {args.output}")
    else:
        print(output)
    
    # Exit with appropriate code
    if result.critical:
        sys.exit(2)
    elif result.warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()