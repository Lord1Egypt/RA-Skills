#!/usr/bin/env python3
"""
Scan skill folder for sensitive data before publishing to ClawHub.
扫描技能文件夹中的敏感数据，在发布到 ClawHub 之前检查。

Usage / 用法:
    python3 scan_sensitive.py /path/to/skill-folder
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Patterns for sensitive data / 敏感数据匹配模式
SENSITIVE_PATTERNS = [
    # MAC addresses (not generic AA:BB:CC:DD:EE:FF)
    (r'(?i)(?<!AA:BB:CC:DD:EE:FF)([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}', 'MAC address / MAC 地址'),
    
    # IP addresses (private ranges, exclude common examples)
    (r'\b(192\.168\.\d{1,3}\.\d{1,3})\b', 'Private IP address / 私有 IP 地址'),
    (r'\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', 'Private IP address / 私有 IP 地址'),
    (r'\b(172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b', 'Private IP address / 私有 IP 地址'),
    
    # API keys and tokens
    (r'(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*["\']?[^\s"\'<>]+', 'API key/Token/Password / API密钥/令牌/密码'),
    (r'(?i)(sk-[a-zA-Z0-9]{20,})', 'API key (OpenAI style) / API 密钥'),
    (r'(?i)(clh_[a-zA-Z0-9]{20,})', 'ClawHub API token / ClawHub API 令牌'),
    
    # Phone numbers
    (r'\b\+?[1-9]\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{4}\b', 'Phone number / 电话号码'),
    
    # Email addresses
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'Email address / 邮箱地址'),
]

# Whitelist patterns (safe to include) / 白名单模式（安全可包含）
WHITELIST = [
    r'192\.168\.1\.\d+',  # Common example subnet / 常见示例子网
    r'example\.com',
    r'user@example',
    r'YOUR_',
    r'xxx',
    r'placeholder',
    r'AA:BB:CC:DD:EE:FF',
]


def is_whitelisted(text: str) -> bool:
    """Check if text matches whitelist patterns."""
    for pattern in WHITELIST:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def scan_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """Scan a file for sensitive data patterns.
    
    Returns list of (line_number, matched_text, pattern_name)
    """
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception:
        return findings
    
    for line_num, line in enumerate(lines, 1):
        for pattern, name in SENSITIVE_PATTERNS:
            matches = re.finditer(pattern, line)
            for match in matches:
                matched_text = match.group(0)
                if not is_whitelisted(matched_text):
                    findings.append((line_num, matched_text, name))
    
    return findings


def scan_folder(folder_path: Path) -> dict:
    """Scan all files in a folder for sensitive data.
    
    Returns dict: {file_path: [(line_num, matched_text, pattern_name), ...]}
    """
    results = {}
    
    for root, dirs, files in os.walk(folder_path):
        # Skip hidden directories and common non-text dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
        
        for file in files:
            if file.startswith('.'):
                continue
            
            file_path = Path(root) / file
            
            # Only scan text files
            text_extensions = {'.md', '.json', '.py', '.sh', '.txt', '.yaml', '.yml', '.toml', '.js', '.ts'}
            if file_path.suffix.lower() not in text_extensions:
                continue
            
            findings = scan_file(file_path)
            if findings:
                results[file_path] = findings
    
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage / 用法: python3 scan_sensitive.py <skill-folder>")
        print("\nScans skill folder for sensitive data before publishing.")
        print("在发布前扫描技能文件夹中的敏感数据。")
        return 1
    
    folder = Path(sys.argv[1])
    if not folder.exists():
        print(f"Error / 错误: Folder not found / 文件夹不存在: {folder}")
        return 1
    
    print(f"Scanning / 正在扫描: {folder}")
    print("-" * 50)
    
    results = scan_folder(folder)
    
    if not results:
        print("\n✓ No sensitive data found / 未发现敏感数据")
        print("  Safe to publish / 可以安全发布")
        return 0
    
    print("\n⚠ Sensitive data found / 发现敏感数据:\n")
    
    for file_path, findings in results.items():
        rel_path = file_path.relative_to(folder)
        print(f"📄 {rel_path}")
        for line_num, matched_text, pattern_name in findings:
            print(f"   Line {line_num}: {pattern_name}")
            print(f"   → {matched_text}")
        print()
    
    print("Please replace with generic values before publishing.")
    print("请在发布前替换为通用值。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
