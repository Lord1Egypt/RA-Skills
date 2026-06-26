#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-Improving Enhancement - 初始化工具
初始化记忆系统目录结构
"""

import sys
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def init():
    """初始化记忆系统"""
    base_dir = Path.home() / "self-improving"
    
    print("=" * 60)
    print("🧠 Self-Improving Enhancement 初始化")
    print("=" * 60)
    print()
    
    # 创建目录结构
    dirs = [
        base_dir,
        base_dir / "projects",
        base_dir / "domains",
        base_dir / "archive",
        base_dir / "chat-logs",  # V2.0 新增：完整聊天记录
    ]
    
    for d in dirs:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            print(f"[✓] 创建目录：{d}")
        else:
            print(f"[✓] 目录已存在：{d}")
    
    # 创建 memory.md（如果不存在）
    memory_md = base_dir / "memory.md"
    if not memory_md.exists():
        memory_md.write_text("""# HOT Memory - 核心记忆

## 用户偏好

<!-- 这里会自动记录用户的核心偏好 -->

## 使用规则

1. 保持 ≤100 行
2. 只记录确认的偏好
3. 定期回顾更新
""", encoding='utf-8')
        print(f"[✓] 创建 memory.md")
    
    # 创建 corrections.md（如果不存在）
    corrections_md = base_dir / "corrections.md"
    if not corrections_md.exists():
        corrections_md.write_text("""# Corrections Log - 纠正记录

<!-- 自动记录用户的纠正，定期回顾并提升到 memory.md -->

""", encoding='utf-8')
        print(f"[✓] 创建 corrections.md")
    
    # 创建 heartbeat-state.json
    heartbeat_json = base_dir / "heartbeat-state.json"
    if not heartbeat_json.exists():
        import json
        heartbeat_json.write_text(json.dumps({
            "lastReview": None,
            "lastCompact": None,
            "totalCorrections": 0,
            "totalPromotions": 0
        }, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"[✓] 创建 heartbeat-state.json")
    
    print()
    print("=" * 60)
    print("✅ 初始化完成！")
    print("=" * 60)
    print()
    print("记忆系统已就绪，位置：")
    print(f"  {base_dir}")
    print()
    print("下一步:")
    print("  1. 正常使用，自动学习纠正")
    print("  2. 运行 stats.py 查看统计")
    print("  3. 定期运行 review.py 回顾")


if __name__ == "__main__":
    init()
