#!/usr/bin/env python3
"""
龙虾记忆系统 - 索引生成脚本
从 MEMORY.md 生成精简索引，减少 token 消耗
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


def extract_index(memory_md_path: Path) -> dict:
    """从 MEMORY.md 提取索引信息"""
    content = memory_md_path.read_text(encoding="utf-8")
    
    index = {
        "user_profile": {},
        "ai_identity": {},
        "decisions": [],
        "errors": [],
        "todos": [],
        "stats": {
            "total_decisions": 0,
            "total_errors": 0,
            "total_todos": 0,
        }
    }
    
    lines = content.split("\n")
    
    # 提取用户档案
    in_user_section = False
    for i, line in enumerate(lines):
        if "## 👤 用户档案" in line or "## 用户档案" in line:
            in_user_section = True
            continue
        if in_user_section and (line.startswith("## ") or line.startswith("---")):
            in_user_section = False
        if in_user_section and line.strip().startswith("- "):
            # 匹配 "- **key：** value" 或 "- **key:** value"
            match = re.match(r"-\s*\*\*(.+?)(?:：|\:)\*\*\s*(.+)", line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                index["user_profile"][key] = value
    
    # 提取 AI 身份
    in_ai_section = False
    for i, line in enumerate(lines):
        if "## 🤖 AI身份" in line or "## AI身份" in line:
            in_ai_section = True
            continue
        if in_ai_section and (line.startswith("## ") or line.startswith("---")):
            in_ai_section = False
        if in_ai_section and line.strip().startswith("- "):
            match = re.match(r"-\s*\*\*(.+?)(?:：|\:)\*\*\s*(.+)", line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                index["ai_identity"][key] = value
    
    # 提取决策（最近3条）
    # 匹配 ### [日期] 标题 后面的 - **决策内容：** xxx
    decision_pattern = r"### \[(\d{4}-\d{2}-\d{2})\]\s*(.+?)(?:\n|$)"
    decisions = re.findall(decision_pattern, content)
    for date, title in decisions[:3]:
        index["decisions"].append({"date": date, "title": title.strip()})
    index["stats"]["total_decisions"] = len(decisions)
    
    # 提取待处理事项
    todo_pattern = r"- \[ \]\s*(.+)"
    todos = re.findall(todo_pattern, content)
    index["todos"] = [t.strip() for t in todos[:5]]
    index["stats"]["total_todos"] = len(todos)
    
    return index


def generate_index_md(index: dict) -> str:
    """生成精简索引 Markdown"""
    lines = [
        "# 记忆索引（精简版）",
        "",
        "> 此文件仅保留核心索引，减少 token 消耗。详情见 MEMORY.md",
        "",
        "---",
        "",
        "## 👤 用户档案",
        "",
    ]
    
    for key, value in index["user_profile"].items():
        lines.append(f"- **{key}：** {value}")
    
    lines.extend([
        "",
        "---",
        "",
        "## 🤖 AI身份",
        "",
    ])
    
    for key, value in index["ai_identity"].items():
        lines.append(f"- **{key}：** {value}")
    
    lines.extend([
        "",
        "---",
        "",
        "## 📌 快速索引",
        "",
        "| 类别 | 数量 | 状态 |",
        "|------|------|------|",
        f"| 重要决策 | {index['stats']['total_decisions']} | ✅ |",
        f"| 错误教训 | {index['stats']['total_errors']} | ⚠️ |",
        f"| 待处理 | {index['stats']['total_todos']} | 📋 |",
        "",
        "---",
        "",
        "## 🎯 最近决策",
        "",
    ])
    
    for d in index["decisions"]:
        lines.append(f"- **[{d['date']}]** {d['title']}")
    
    if not index["decisions"]:
        lines.append("_暂无_")
    
    lines.extend([
        "",
        "---",
        "",
        "## 📋 待处理",
        "",
    ])
    
    for t in index["todos"]:
        lines.append(f"- [ ] {t}")
    
    if not index["todos"]:
        lines.append("_暂无_")
    
    lines.extend([
        "",
        "---",
        "",
        f"_更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        "",
        "_此文件为精简索引，详情请查看 MEMORY.md_",
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成记忆索引")
    parser.add_argument("--workspace", default="~/.openclaw/workspace", help="工作空间路径")
    parser.add_argument("--output", help="输出文件路径（默认：memory/MEMORY_INDEX.md）")
    args = parser.parse_args()
    
    workspace = Path(args.workspace).expanduser()
    memory_md = workspace / "MEMORY.md"
    
    if not memory_md.exists():
        print(f"❌ MEMORY.md 不存在: {memory_md}")
        return
    
    print("🔍 提取索引信息...")
    index = extract_index(memory_md)
    
    print(f"   用户档案：{len(index['user_profile'])} 项")
    print(f"   AI 身份：{len(index['ai_identity'])} 项")
    print(f"   决策：{index['stats']['total_decisions']} 条")
    print(f"   待处理：{index['stats']['total_todos']} 条")
    
    output_path = Path(args.output) if args.output else workspace / "memory" / "MEMORY_INDEX.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    index_md = generate_index_md(index)
    output_path.write_text(index_md, encoding="utf-8")
    
    # 计算节省的 token
    original_size = memory_md.stat().st_size
    index_size = output_path.stat().st_size
    savings = (1 - index_size / original_size) * 100
    
    print(f"\n✅ 索引已生成: {output_path}")
    print(f"   原始大小：{original_size / 1024:.1f} KB")
    print(f"   索引大小：{index_size / 1024:.1f} KB")
    print(f"   节省 token：约 {savings:.0f}%")


if __name__ == "__main__":
    main()
