#!/usr/bin/env python3
"""
Context Lazy Loading 优化器

分析 prompt 复杂度，推荐只加载必要的上下文文件。
可生成优化的 AGENTS.md 模板，教 agent 按需加载。

纯本地运行，无网络请求，无副作用。
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 必须始终加载的文件 (身份/人格)
ALWAYS_LOAD = [
    "SOUL.md",
    "IDENTITY.md",
]

# 按触发词条件加载的文件
CONDITIONAL_FILES = {
    "AGENTS.md": ["workflow", "process", "流程", "怎么做", "如何"],
    "USER.md": ["user", "用户", "owner", "主人"],
    "TOOLS.md": ["tool", "工具", "ssh", "camera", "设备"],
    "MEMORY.md": ["remember", "recall", "记得", "回忆", "历史", "之前", "上次"],
}

# 简单对话时跳过的文件模式
SKIP_FOR_SIMPLE = [
    "docs/**/*.md",
    "memory/20*.md",
    "knowledge/**/*",
    "tasks/**/*",
]


def classify_prompt(prompt: str) -> tuple[str, str, str]:
    """分类 prompt 复杂度。

    Returns:
        (complexity, context_level, reasoning)
        complexity: "simple" | "medium" | "complex"
        context_level: "minimal" | "standard" | "full"
    """
    p = prompt.strip().lower()

    # 简单对话
    simple_patterns = [
        r"^(hi|hey|hello|yo|你好|嗨)[\s!！.。]*$",
        r"^(thanks|thank you|thx|谢谢|感谢)",
        r"^(ok|okay|sure|got it|好的|好|行|知道了|明白|收到)",
        r"^(yes|no|是|否|对|不)",
        r"^.{1,5}$",
    ]
    for pattern in simple_patterns:
        if re.search(pattern, p, re.IGNORECASE):
            return ("simple", "minimal", "简单对话/短消息")

    # 涉及记忆/历史
    if any(w in p for w in ["remember", "recall", "历史", "之前", "上次", "记得"]):
        return ("medium", "full", "需要记忆/历史上下文")

    # 复杂任务
    complex_words = ["design", "architect", "设计", "架构", "comprehensive",
                     "全面", "深入分析", "strategy", "策略", "规划"]
    if any(w in p for w in complex_words):
        return ("complex", "full", "复杂任务需要完整上下文")

    # 默认标准
    return ("medium", "standard", "标准工作请求")


def recommend(prompt: str, current_files: list[str] | None = None) -> dict:
    """推荐加载哪些文件。

    Args:
        prompt: 用户的消息
        current_files: 当前已加载的文件列表 (可选)

    Returns:
        dict with recommendations
    """
    complexity, context_level, reasoning = classify_prompt(prompt)
    p = prompt.strip().lower()

    # 始终加载
    recommended = set(ALWAYS_LOAD)

    if context_level == "minimal":
        pass  # 只加载身份文件

    elif context_level == "standard":
        # 按触发词加载
        for file, triggers in CONDITIONAL_FILES.items():
            if any(t in p for t in triggers):
                recommended.add(file)
        # 今天的记忆
        today = datetime.now().strftime("%Y-%m-%d")
        recommended.add(f"memory/{today}.md")

    elif context_level == "full":
        # 所有条件文件
        recommended.update(CONDITIONAL_FILES.keys())
        # 今天 + 昨天的记忆
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        recommended.add(f"memory/{today.strftime('%Y-%m-%d')}.md")
        recommended.add(f"memory/{yesterday.strftime('%Y-%m-%d')}.md")
        recommended.add("MEMORY.md")

    # 计算节省
    savings_percent = None
    if current_files:
        current_count = len(current_files)
        recommended_count = len(recommended)
        if current_count > 0:
            savings_percent = round(
                (current_count - recommended_count) / current_count * 100
            )

    return {
        "complexity": complexity,
        "context_level": context_level,
        "reasoning": reasoning,
        "recommended_files": sorted(recommended),
        "file_count": len(recommended),
        "savings_percent": savings_percent,
        "skip_patterns": SKIP_FOR_SIMPLE if context_level == "minimal" else [],
    }


def generate_agents_md() -> str:
    """生成优化的 AGENTS.md 内容。"""
    return """# AGENTS.md — Token 优化版

## 上下文加载策略

**原则: 最小加载，按需扩展**

### 每次会话必须加载 (仅 2 个文件)
1. `SOUL.md` — 身份/人格
2. `IDENTITY.md` — 角色定义

**到此为止。不要加载其他文件，除非下面的条件触发。**

### 按需加载

**当用户提到记忆/历史时:**
- `MEMORY.md`
- `memory/YYYY-MM-DD.md` (仅今天)

**当用户问工作流程时:**
- `AGENTS.md`

**当用户提到工具/设备时:**
- `TOOLS.md`

**当用户问自己时:**
- `USER.md`

### 永远不自动加载
- ❌ `docs/**/*.md` — 仅在明确引用时加载
- ❌ `memory/2026-*.md` (旧日志) — 仅在指定日期时加载
- ❌ `knowledge/**/*` — 仅在询问特定主题时加载

### 按对话类型的上下文策略

| 类型 | 示例 | 加载 | 节省 |
|------|------|------|------|
| 简单对话 | "hi", "谢谢", "好的" | SOUL.md + IDENTITY.md | **~80%** |
| 标准工作 | "写个函数", "看下日志" | + memory/TODAY.md | **~50%** |
| 复杂任务 | "设计架构", "分析历史" | + MEMORY.md + 相关 docs | **~30%** |

## 模型选择 (强制执行)

- 简单对话 → `zai-proxy/glm-4.7-flashx` (最便宜)
- 标准工作 → `zai-proxy/glm-4.7` (默认)
- 心跳 → `zai-proxy/glm-4.7-flashx` (强制)

## 禁止行为

❌ 启动时加载所有文件
❌ 重新读取未改变的文件
❌ 用默认模型处理 "hi"
❌ 每次心跳都检查所有内容
"""


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  context_optimizer.py recommend '<prompt>' [current_files...]")
        print("  context_optimizer.py generate-agents")
        print()
        print("示例:")
        print("  context_optimizer.py recommend 'hi'")
        print("  context_optimizer.py recommend '设计一个用户系统'")
        print("  context_optimizer.py generate-agents")
        sys.exit(1)

    command = sys.argv[1]

    if command == "recommend":
        if len(sys.argv) < 3:
            print("用法: context_optimizer.py recommend '<prompt>'")
            sys.exit(1)
        prompt = sys.argv[2]
        current_files = sys.argv[3:] if len(sys.argv) > 3 else None
        result = recommend(prompt, current_files)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "generate-agents":
        content = generate_agents_md()
        output_path = Path("AGENTS.md.optimized")
        output_path.write_text(content, encoding="utf-8")
        print(f"已生成优化的 AGENTS.md → {output_path}")
        print("请检查内容后替换你的 AGENTS.md")

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
