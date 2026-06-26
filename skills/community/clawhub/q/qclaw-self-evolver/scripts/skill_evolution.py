#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能自进化模块
从任务历史自动发现可固化的技能候选

触发条件（满足任一）：
  - 同一任务类型出现 ≥ 3 次
  - 用户明确说「把它做成技能」「记下来以后用」
  - cron 定期扫描发现高价值重复任务

生成结果：
  skills/[name]-skill/SKILL.md
"""

import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path

def _resolve_workspace():
    return os.path.expanduser(os.environ.get("QW_WORKSPACE", "~/.qclaw/workspace"))

WORKSPACE   = _resolve_workspace()
SKILLS_DIR  = os.path.join(WORKSPACE, "skills")
os.makedirs(SKILLS_DIR, exist_ok=True)

# ============================================================
# 技能候选关键词
# ============================================================
SKILL_TRIGGERS = [
    "研究", "开发", "分析", "优化", "自动化",
    "监控", "集成", "部署", "测试", "重构",
    "整理", "搜索", "查询", "生成", "创建",
    "做成技能", "记下来", "固化", "形成技能",
]

# ============================================================
# 检测技能候选
# ============================================================
def detect_skill_candidates(text: str) -> list:
    """从文本中检测可能的技能候选"""
    if not text:
        return []
    found = [kw for kw in SKILL_TRIGGERS if kw in text]
    return found

# ============================================================
# 生成新技能
# ============================================================
def generate_skill(name: str, description: str, trigger_phrases: list,
                   skill_type: str = "task-automation") -> str:
    """
    生成一个新的 skill SKILL.md 文件
    返回生成的路径
    """
    skill_dir = os.path.join(SKILLS_DIR, f"{_slugify(name)}-skill")
    os.makedirs(skill_dir, exist_ok=True)

    skill_md = f"""# {name}

**类型：** {skill_type}
**生成时间：** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**触发词：** {', '.join(trigger_phrases) if trigger_phrases else '（待添加）'}
**状态：** 实验性（待验证效果）

---

## 描述

{description}

---

## 触发条件

> 当用户提到以下内容时，触发本技能：

{"".join(f"- {t}\n" for t in trigger_phrases)}

---

## 使用方法

（待填写：具体使用步骤）

---

## 注意事项

- 本技能为自动生成，效果待验证
- 使用 3 次后评估效果
- 如需改进请联系维护者

---

*本技能由 self-evolver 自动生成 · {datetime.now().strftime("%Y-%m-%d")}*
"""
    skill_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(skill_md)

    # 更新 references/index.md（方便查找）
    index_path = os.path.join(SKILLS_DIR, "_auto_generated_index.md")
    with open(index_path, "a", encoding="utf-8") as f:
        f.write(f"- [{name}]({_slugify(name)}-skill/SKILL.md) — {description[:50]}\n")

    return skill_path

# ============================================================
# 扫描并生成建议
# ============================================================
def scan_and_suggest() -> list:
    """扫描 skills 目录，返回可进化的技能候选"""
    suggestions = []
    skill_dirs = [
        d for d in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, d)) and d.endswith("-skill")
    ]

    for s in skill_dirs:
        skill_path = os.path.join(SKILLS_DIR, s, "SKILL.md")
        if os.path.exists(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "实验性" in content or "待验证" in content:
                suggestions.append({
                    "name": s,
                    "path": skill_path,
                    "status": "实验性",
                    "suggestion": "建议使用 3 次后评估是否提升为正式技能"
                })

    return suggestions

# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="技能自进化")
    parser.add_argument("--name",   help="技能名称")
    parser.add_argument("--desc",   help="技能描述")
    parser.add_argument("--type",   default="task-automation", help="技能类型")
    parser.add_argument("--triggers", nargs="+", help="触发关键词")
    parser.add_argument("--scan",   action="store_true", help="扫描现有技能")
    args = parser.parse_args()

    if args.scan:
        suggestions = scan_and_suggest()
        if suggestions:
            print(f"发现 {len(suggestions)} 个可进化的技能：")
            for s in suggestions:
                print(f"  - {s['name']}: {s['suggestion']}")
        else:
            print("没有发现可进化的技能候选")
        return

    if args.name:
        path = generate_skill(
            name=args.name,
            description=args.desc or "（无描述）",
            trigger_phrases=args.triggers or [],
            skill_type=args.type
        )
        print(f"✅ 技能已生成：{path}")
        return

    # 默认：扫描
    suggestions = scan_and_suggest()
    print(f"📊 技能自进化扫描结果：")
    print(f"   自生成技能：{len(suggestions)} 个")
    if suggestions:
        for s in suggestions:
            print(f"   → {s['name']}: {s['status']}")

def _slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

if __name__ == "__main__":
    main()
