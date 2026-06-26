#!/usr/bin/env python3
"""
技能安全检查模块
检测危险代码模式
"""

import re
import sys
import json
import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DANGEROUS_PATTERNS = [
    (r'curl.*https?://[^\s"]+', '🚨', 'curl 到未知 URL', 'EXTREME'),
    (r'wget.*https?://[^\s"]+', '🚨', 'wget 到未知 URL', 'EXTREME'),
    (r'eval\(|exec\(', '🚨', 'eval 或 exec', 'EXTREME'),
    (r'sudo|su |runas', '🚨', '请求 sudo 权限', 'EXTREME'),
    (r'\.ssh[\\/]', '🔴', '访问 ssh 目录', 'HIGH'),
    (r'\.aws[\\/]', '🔴', '访问 aws 目录', 'HIGH'),
    (r'MEMORY\.md|USER\.md|SOUL\.md', '🔴', '访问个人记忆文件', 'HIGH'),
    (r'install.*pip |npm.*install', '🟡', '安装未知包', 'MEDIUM'),
    (r'delete.*file|rm.*-rf', '🟢', '删除文件', 'LOW'),
]

def parse_args():
    parser = argparse.ArgumentParser(description='技能安全检查')
    parser.add_argument('skill_path', help='技能目录路径')
    return parser.parse_args()

def scan_file(file_path):
    """扫描文件中的危险模式"""
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        for pattern, icon, desc, risk in DANGEROUS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append({'icon': icon, 'desc': desc, 'risk': risk})
    except Exception as e:
        logger.error(f"扫描失败: {e}")
    return issues

def main():
    args = parse_args()
    skill_path = Path(args.skill_path)

    all_issues = []
    for ext in ['*.md', '*.py', '*.sh', '*.js']:
        for file in skill_path.rglob(ext):
            if file.is_file():
                all_issues.extend(scan_file(file))

    if not all_issues:
        print("✅ 安全检查通过 - 无危险模式")
        sys.exit(0)

    print(f"⚠️ 发现 {len(all_issues)} 个问题:")
    for issue in all_issues[:5]:
        print(f"  {issue['icon']} {issue['desc']}")

    sys.exit(0)

if __name__ == '__main__':
    main()
