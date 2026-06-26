#!/usr/bin/env python3
"""
skills_guard.py - Skill 安全扫描器

参考 Hermes Agent 的 skills_guard 机制：
- Agent 创建的 Skill 同样需要安全扫描
- 扫描威胁模式、凭证泄露、破坏性命令
- 支持 allow/ask/block 三种结果

用途：
    - Skill 创建前的安全审核
    - 第三方 Skill 的安全检查
    - 防止恶意 Skill 注入
"""

import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ============================================================================
# 威胁模式库（参考 Hermes Agent）
# ============================================================================

DANGEROUS_PATTERNS = [
    # 凭证窃取
    (r'api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}', 'hardcoded_api_key'),
    (r'secret[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}', 'hardcoded_secret'),
    (r'token\s*[=:]\s*["\']?[a-zA-Z0-9_-]{20,}', 'hardcoded_token'),
    (r'password\s*[=:]\s*["\']?[^"\'\s]{8,}', 'hardcoded_password'),
    
    # 凭证环境变量泄露
    (r'\$\{?\w*(API|KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL|API_KEY|APISECRET)', 'env_var_exposure'),
    (r'import\s+os.*getenv.*(KEY|TOKEN|SECRET|PASSWORD)', 'env_var_access'),
    
    # 破坏性命令
    (r'rm\s+-rf\s+/', 'destructive_rm_root'),
    (r'rm\s+-rf\s+\.', 'destructive_rm_local'),
    (r'dd\s+.*of=/dev/', 'destructive_dd'),
    (r'mkfs\.', 'destructive_mkfs'),
    (r':(){ :|:& };:', 'fork_bomb'),
    
    # 提示注入
    (r'ignore\s+(previous|all|above|prior)\s+instructions', 'prompt_injection'),
    (r'disregard\s+(your|all|any)\s+(instructions|rules)', 'disregard_rules'),
    (r'you\s+are\s+a\s+(jailbreak|evil|malicious)', 'jailbreak_attempt'),
    
    # 网络安全
    (r'curl\s+.*\$\{?\w*(KEY|TOKEN|SECRET|PASSWORD)', 'curl_credential_exposure'),
    (r'wget\s+.*\$\{?\w*(KEY|TOKEN|SECRET|PASSWORD)', 'wget_credential_exposure'),
    (r'requests\.[a-z]+\(.*\$.*(?:key|token|secret)', 'requests_credential_exposure'),
    
    # 恶意代码模式
    (r'eval\s*\(', 'dangerous_eval'),
    (r'exec\s*\(', 'dangerous_exec'),
    (r'subprocess\..*shell\s*=\s*True', 'shell_injection'),
    (r'os\.system\s*\(', 'os_system_call'),
    
    # 加密货币相关（Hermes 标记为可疑）
    (r'crypto\.(wallet|transfer|send)', 'crypto_operation'),
    (r'bitcoin|ethereum|wallet.*private', 'crypto_keyword'),
    (r'web3\.|etherscan|smart.?contract', 'web3_keyword'),
]

# 高危模式 - 直接阻止
HIGH_SEVERITY = {
    'hardcoded_api_key', 'hardcoded_secret', 'hardcoded_token', 'hardcoded_password',
    'destructive_rm_root', 'destructive_dd', 'fork_bomb', 'shell_injection',
    'prompt_injection', 'jailbreak_attempt',
}

# 中危模式 - 警告
MEDIUM_SEVERITY = {
    'env_var_exposure', 'env_var_access', 'curl_credential_exposure',
    'destructive_rm_local', 'eval', 'exec', 'os_system_call',
}


@dataclass
class ScanResult:
    """扫描结果"""
    allowed: bool  # True if allowed, False if blocked
    reason: Optional[str]  # None/ask/block
    findings: List[Dict[str, str]]  # [{pattern, line, severity}]
    blocked_patterns: List[str]  # 高危模式列表


def scan_file(file_path: Path) -> List[Dict[str, str]]:
    """扫描单个文件"""
    findings = []
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern, pattern_id in DANGEROUS_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    severity = 'high' if pattern_id in HIGH_SEVERITY else 'medium'
                    findings.append({
                        'pattern_id': pattern_id,
                        'line': str(i),
                        'content': line.strip()[:100],
                        'severity': severity,
                    })
    except Exception as e:
        logger.warning(f"Failed to scan {file_path}: {e}")
    
    return findings


def scan_skill(skill_dir: Path, source: str = "unknown") -> ScanResult:
    """
    扫描整个 Skill 目录。
    
    Args:
        skill_dir: Skill 目录路径
        source: 来源标记（agent-created/hub/installed）
    
    Returns:
        ScanResult: 包含 allowed、reason、findings
    """
    all_findings = []
    
    # 扫描所有文件
    for file_path in skill_dir.rglob('*'):
        if file_path.is_file() and not file_path.name.startswith('.'):
            findings = scan_file(file_path)
            for f in findings:
                f['file'] = str(file_path.relative_to(skill_dir))
            all_findings.extend(findings)
    
    # 检查是否有高危模式
    high_severity_findings = [f for f in all_findings if f['severity'] == 'high']
    
    if high_severity_findings:
        return ScanResult(
            allowed=False,
            reason='high_severity_patterns',
            findings=all_findings,
            blocked_patterns=[f['pattern_id'] for f in high_severity_findings],
        )
    
    # 检查是否有中危模式
    medium_findings = [f for f in all_findings if f['severity'] == 'medium']
    
    if medium_findings:
        return ScanResult(
            allowed=None,  # ask
            reason='medium_severity_patterns',
            findings=all_findings,
            blocked_patterns=[],
        )
    
    return ScanResult(
        allowed=True,
        reason=None,
        findings=all_findings,
        blocked_patterns=[],
    )


def should_allow_install(result: ScanResult) -> Tuple[bool, Optional[str]]:
    """
    根据扫描结果决定是否允许安装。
    
    Returns:
        (allowed, reason) - allowed: True/False/None(ask)
    """
    if result.allowed == False:
        return False, result.reason
    elif result.allowed is None:
        return None, result.reason
    else:
        return True, None


def format_scan_report(result: ScanResult) -> str:
    """格式化扫描报告"""
    lines = ["Security Scan Report", "=" * 40]
    
    if not result.findings:
        lines.append("✅ No threats found")
        return "\n".join(lines)
    
    lines.append(f"Found {len(result.findings)} potential issue(s):\n")
    
    for f in result.findings:
        severity_marker = "🔴" if f['severity'] == 'high' else "🟡"
        lines.append(f"  {severity_marker} [{f['pattern_id']}]")
        lines.append(f"     File: {f['file']}:{f['line']}")
        lines.append(f"     {f['content'][:80]}")
        lines.append("")
    
    return "\n".join(lines)


# ============================================================================
# CLI 入口
# ============================================================================

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: skills_guard.py <skill-dir>")
        sys.exit(1)
    
    skill_dir = Path(sys.argv[1])
    if not skill_dir.exists():
        print(f"Directory not found: {skill_dir}")
        sys.exit(1)
    
    print(f"Scanning skill: {skill_dir.name}")
    print()
    
    result = scan_skill(skill_dir)
    print(format_scan_report(result))
    print()
    
    allowed, reason = should_allow_install(result)
    if allowed == True:
        print("✅ ALLOWED - Skill can be installed")
    elif allowed == False:
        print(f"🔴 BLOCKED - {reason}")
        sys.exit(1)
    else:
        print(f"🟡 ASK - {reason}")
        print("   Skill can be installed with warnings")


if __name__ == "__main__":
    main()
