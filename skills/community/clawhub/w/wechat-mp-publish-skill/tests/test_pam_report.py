#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 PAM 行业报告生成
"""

import sys
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
sys.path.insert(0, str(Path(__file__).parent))

from scheduled_pam_report import generate_pam_industry_report

print("=" * 70)
print("📊 特权账号管理（PAM）行业深度报告预览")
print("=" * 70)

# 生成报告
content = generate_pam_industry_report()

# 统计
print(f"\n📝 报告统计:")
print(f"   总字数：{len(content)} 字")
print(f"   预计配图：{len(content) // 400} 张")

# 预览目录
print(f"\n📑 报告目录:")
for line in content.split('\n'):
    if line.startswith('#'):
        print(f"   {line}")

# 预览前 1000 字
print(f"\n📖 内容预览（前 1000 字）:")
print(content[:1000])
print("\n...（内容继续）...")

print("\n" + "=" * 70)
print("✅ PAM 行业报告已准备就绪！")
print("=" * 70)
