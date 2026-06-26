#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感信息清理脚本
扫描并替换技能包中的所有敏感信息（API keys, tokens, secrets 等）
"""

import os
import re
import json
from pathlib import Path
from typing import List, Tuple

# 敏感信息模式
SENSITIVE_PATTERNS = [
    # API Keys
    (r'sk-[a-zA-Z0-9]{32,}', 'sk-your-api-key-here'),
    (r'sk-sp-[a-f0-9]{32}', 'sk-sp-your-bailian-coding-key'),
    (r'sk-b3c2[a-f0-9]{28}', 'sk-your-bailian-key'),
    
    # 微信相关
    (r'wx[a-f0-9]{16}', 'your-wechat-appid'),
    (r'[a-f0-9]{32}', 'your-wechat-appsecret'),  # 谨慎使用，可能误伤
    
    # Volcengine
    (r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', 'your-uuid-here'),
    
    # 其他常见模式
    (r'(?i)api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9]{20,}["\']?', 'api_key: "your-api-key-here"'),
]

# 需要检查的文件扩展名
TARGET_EXTENSIONS = {'.py', '.json', '.yaml', '.yml', '.md', '.txt', '.env'}

# 需要跳过的目录
SKIP_DIRS = {'venv', '__pycache__', '.git', 'node_modules', '.venv'}


def is_sensitive_file(file_path: Path) -> bool:
    """判断文件是否可能包含敏感信息"""
    name = file_path.name.lower()
    return any(keyword in name for keyword in [
        'token', 'cache', 'secret', 'credential', 'config', 'env', 'key'
    ])


def scan_for_secrets(file_path: Path) -> List[Tuple[str, int]]:
    """扫描文件中的敏感信息"""
    secrets = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # 跳过注释和示例
                if line.strip().startswith('#') or 'your-' in line.lower() or 'example' in line.lower():
                    continue
                
                # 检查常见敏感模式
                patterns = [
                    (r'sk-[a-zA-Z0-9]{20,}', 'API Key'),
                    (r'wx[a-f0-9]{16}', 'WeChat AppID'),
                ]
                
                for pattern, secret_type in patterns:
                    if re.search(pattern, line):
                        secrets.append((secret_type, line_num))
    
    except Exception as e:
        print(f"  ⚠️ 读取失败：{e}")
    
    return secrets


def clean_file(file_path: Path, dry_run: bool = True) -> bool:
    """清理文件中的敏感信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # 替换敏感模式
        for pattern, replacement in SENSITIVE_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                changes.append(f"{pattern} -> {replacement} ({len(matches)} 处)")
                content = re.sub(pattern, replacement, content)
        
        if content != original:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ 已清理：{len(changes)} 个敏感信息")
            else:
                print(f"  🔍 发现敏感信息：")
                for change in changes:
                    print(f"     - {change}")
            return True
        
        return False
    
    except Exception as e:
        print(f"  ❌ 处理失败：{e}")
        return False


def main():
    base_dir = Path('/Users/brucesong/.openclaw/workspace/Bruce/wechat-mp-publish')
    
    print("=" * 60)
    print("敏感信息清理扫描")
    print("=" * 60)
    print(f"扫描目录：{base_dir}")
    print()
    
    # 扫描所有文件
    files_scanned = 0
    files_with_secrets = 0
    
    for root, dirs, files in os.walk(base_dir):
        # 跳过不需要的目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            
            # 检查扩展名
            if file_path.suffix not in TARGET_EXTENSIONS:
                continue
            
            files_scanned += 1
            
            # 扫描敏感信息
            secrets = scan_for_secrets(file_path)
            
            if secrets:
                files_with_secrets += 1
                print(f"\n📄 {file_path.relative_to(base_dir)}")
                for secret_type, line_num in secrets:
                    print(f"   行 {line_num}: {secret_type}")
    
    print()
    print("=" * 60)
    print(f"扫描完成")
    print(f"  总文件数：{files_scanned}")
    print(f"  包含敏感信息的文件：{files_with_secrets}")
    print("=" * 60)


if __name__ == '__main__':
    main()
