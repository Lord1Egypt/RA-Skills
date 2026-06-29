#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Verify - AI 产出预检工具
原创实现，受 Claude Code VerificationAgent 设计模式启发。
检查：敏感信息泄露、链接可达性、内容完整性、格式合规。
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import re
import os
import json
from pathlib import Path
from datetime import datetime

# ── 敏感信息模式 ──────────────────────────────────
SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|apikey|secret|token|password|passwd)\s*[:=]\s*["\']?.{8,}["\']?', '可能的密钥/密码泄露'),
    (r'\b(?:sk-[a-zA-Z0-9]{20,}|pk-[a-zA-Z0-9]{20,})\b', 'OpenAI API Key 格式'),
    (r'(?i)(BEGIN\s+(RSA|EC|DSA|PRIVATE|OPENSSH)\s+KEY)', '私钥内容'),
    (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'IP 地址（可能是内网）'),
    (r'(?i)(AKIA[0-9A-Z]{16})', 'AWS Access Key'),
    (r'(?:-----BEGIN[ \t]+.*?-----)', 'PEM 格式密钥'),
    (r'(?i)(password|pwd|passwd)\s*[=:]\s*\S+', '密码字段'),
]

# ── 未完成标记 ──────────────────────────────────
UNFINISHED_PATTERNS = [
    (r'(?i)\bTODO\b', '未完成的 TODO'),
    (r'(?i)\bFIXME\b', '未修复的 FIXME'),
    (r'(?i)\bHACK\b', '临时方案 HACK'),
    (r'(?i)\bXXX\b', '标记 XXX'),
    (r'未完待续', '内容未完成'),
    (r'…$', '以省略号结尾（可能截断）'),
]

# ── 内网 IP 范围 ──────────────────────────────────
PRIVATE_IPS = re.compile(r'\b(?:'
    r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    r'|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}'
    r'|192\.168\.\d{1,3}\.\d{1,3}'
    r'|127\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    r'|localhost'
    r')\b'
)

SEVERITY_COLORS = {
    'CRITICAL': '\033[91m',  # Red
    'ERROR': '\033[93m',     # Yellow
    'WARNING': '\033[94m',   # Blue
    'INFO': '\033[92m',      # Green
    'RESET': '\033[0m',
}

def color(severity, text):
    c = SEVERITY_COLORS.get(severity, '')
    return f"{c}{text}{SEVERITY_COLORS['RESET']}"


def check_secrets(content, filename):
    """检查敏感信息泄露"""
    issues = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for pattern, desc in SECRET_PATTERNS:
            if re.search(pattern, line):
                # 排除测试文件和示例
                if 'example' in filename.lower() or 'test' in filename.lower():
                    continue
                issues.append({
                    'severity': 'CRITICAL' if '密钥' in desc or 'Key' in desc or '私钥' in desc else 'WARNING',
                    'line': i,
                    'description': desc,
                    'match': line.strip()[:80],
                })
    return issues


def check_unfinished(content):
    """检查未完成内容"""
    issues = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        for pattern, desc in UNFINISHED_PATTERNS:
            if re.search(pattern, line):
                issues.append({
                    'severity': 'ERROR',
                    'line': i,
                    'description': desc,
                    'match': line.strip()[:80],
                })
    return issues


def check_links(content):
    """检查 Markdown 链接格式"""
    issues = []
    # 检查 Markdown 链接语法
    md_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]*)\)')
    for match in md_link_pattern.finditer(content):
        url = match.group(2)
        text = match.group(1)
        line_no = content[:match.start()].count('\n') + 1

        if not url or url.strip() == '':
            issues.append({
                'severity': 'ERROR',
                'line': line_no,
                'description': '空链接',
                'match': f'[{text}]()',
            })
        elif url.startswith('http'):
            issues.append({
                'severity': 'INFO',
                'line': line_no,
                'description': f'链接需要验证可达性: {url[:60]}',
                'match': f'[{text}]({url[:40]}...)',
            })

    return issues


def check_format(content, filename):
    """检查格式"""
    issues = []

    # 检查编码
    try:
        content.encode('utf-8')
    except UnicodeEncodeError:
        issues.append({
            'severity': 'ERROR',
            'line': 0,
            'description': '非 UTF-8 编码',
            'match': filename,
        })

    # Markdown 特定检查
    if filename.endswith('.md'):
        has_title = bool(re.search(r'^#\s+', content, re.MULTILINE))
        if not has_title:
            issues.append({
                'severity': 'WARNING',
                'line': 0,
                'description': 'Markdown 缺少标题',
                'match': filename,
            })

    return issues


def check_local_ips(content):
    """检查内网 IP 泄露"""
    issues = []
    matches = PRIVATE_IPS.finditer(content)
    for match in matches:
        line_no = content[:match.start()].count('\n') + 1
        issues.append({
            'severity': 'WARNING',
            'line': line_no,
            'description': f'内网地址: {match.group()}',
            'match': match.group(),
        })
    return issues


def run_all_checks(filepath):
    """运行全部检查"""
    path = Path(filepath)
    if not path.exists():
        print(f"\n❌ 文件不存在: {filepath}")
        return False

    content = path.read_text(encoding='utf-8', errors='replace')
    filename = path.name

    print(f"\n{'='*60}")
    print(f"📋 检查: {filename}")
    print(f"{'='*60}\n")

    all_issues = []
    all_issues.extend(check_secrets(content, filename))
    all_issues.extend(check_unfinished(content))
    all_issues.extend(check_links(content))
    all_issues.extend(check_format(content, filename))
    all_issues.extend(check_local_ips(content))

    if not all_issues:
        print(" ✅ 全部通过，未发现问题")
        return True

    # 按严重级别排序
    severity_order = {'CRITICAL': 0, 'ERROR': 1, 'WARNING': 2, 'INFO': 3}
    all_issues.sort(key=lambda x: severity_order.get(x['severity'], 99))

    has_critical = False
    for issue in all_issues:
        sev = issue['severity']
        loc = f"第{issue['line']}行" if issue['line'] > 0 else "文件级"
        print(f"  {color(sev, f'[{sev:8}]')} {loc:10} {issue['description']}")
        if issue['match']:
            print(f"           └─ {issue['match'][:70]}")
        if sev == 'CRITICAL':
            has_critical = True

    print(f"\n{'─'*60}")
    critical = sum(1 for i in all_issues if i['severity'] == 'CRITICAL')
    errors = sum(1 for i in all_issues if i['severity'] == 'ERROR')
    warnings = sum(1 for i in all_issues if i['severity'] == 'WARNING')
    print(f"  发现: {color('CRITICAL', str(critical))} CRITICAL, "
          f"{color('ERROR', str(errors))} ERROR, "
          f"{color('WARNING', str(warnings))} WARNING")
    print(f"{'─'*60}")

    return not has_critical


def main():
    if len(sys.argv) < 3:
        print("用法: python verify.py <check|links|secrets|all> <file>")
        print("示例:")
        print("  python verify.py all article.md")
        print("  python verify.py secrets config.json")
        sys.exit(1)

    command = sys.argv[1]
    filepath = sys.argv[2]

    if command == 'all':
        success = run_all_checks(filepath)
    elif command == 'secrets':
        path = Path(filepath)
        content = path.read_text(encoding='utf-8', errors='replace')
        issues = check_secrets(content, path.name)
        for i in issues:
            print(f"[{i['severity']}] 第{i['line']}行: {i['description']}")
        success = not any(i['severity'] == 'CRITICAL' for i in issues)
    elif command == 'links':
        path = Path(filepath)
        content = path.read_text(encoding='utf-8', errors='replace')
        issues = check_links(content)
        for i in issues:
            print(f"[{i['severity']}] 第{i['line']}行: {i['description']}")
        success = True
    elif command == 'check':
        success = run_all_checks(filepath)
    else:
        print(f"未知命令: {command}")
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
