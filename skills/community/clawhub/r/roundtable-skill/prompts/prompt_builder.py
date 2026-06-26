#!/usr/bin/env python3
"""
Prompt Builder - 从 framework.md 模板读取并构建各轮次 prompt

职责：
1. 读取 prompts/framework.md 中的模板
2. 注入上下文（讨论历史、Agent 角色等）
3. 返回完整 prompt 字符串

解耦目标：
- roundtable_engine.py 不再硬编码 400+ 行 prompt 字符串
- 修改提示词只需改 framework.md，不碰 Python 代码
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any


_PROMPTS_DIR = Path(__file__).parent

# Round 对应的 section header 映射表
_ROUND_MARKERS = {
    "R1": "R1 轮",
    "R2": "R2 轮",
    "R3": "R3 轮",
    "R4": "R4 轮",
    "R5": "R5 轮",
}


def _load_framework() -> str:
    """加载 prompts/framework.md 全文"""
    path = _PROMPTS_DIR / "framework.md"
    if not path.exists():
        raise FileNotFoundError(f"模板文件不存在：{path}")
    return path.read_text(encoding="utf-8")


def _extract_section(text: str, marker: str) -> str:
    """从 framework.md 中提取指定轮次的 prompt 模板"""
    # 查找 marker 所在行
    lines = text.split("\n")
    start_idx = None
    for i, line in enumerate(lines):
        if marker in line and line.strip().startswith("###"):
            start_idx = i
            break
    if start_idx is None:
        raise ValueError(f"未找到标记：{marker}")

    # 从下一行的 "```markdown" 开始，到下一个 "```" 结束
    code_start = None
    for i in range(start_idx, len(lines)):
        if lines[i].strip() == "```markdown":
            code_start = i + 1
            break
    if code_start is None:
        raise ValueError(f"在 {marker} 附近未找到 ```markdown 块")

    code_end = None
    for i in range(code_start, len(lines)):
        if lines[i].strip() == "```":
            code_end = i
            break
    if code_end is None:
        raise ValueError(f"在 {marker} 的代码块未找到结束 ```")

    return "\n".join(lines[code_start:code_end])


def _role_to_industry(agent_id: str) -> str:
    """根据 agent_id 返回行业/角色描述"""
    aid_lower = agent_id.lower()
    if "engineering" in aid_lower or "dev" in aid_lower or "code" in aid_lower:
        return "工程"
    if "test" in aid_lower:
        return "测试/QA"
    if "design" in aid_lower or "ux" in aid_lower:
        return "UX/UI 设计"
    if "product" in aid_lower or "pm" in aid_lower:
        return "产品"
    if "security" in aid_lower:
        return "安全"
    if "marketing" in aid_lower or "market" in aid_lower:
        return "市场营销"
    return "行业"


def build_prompt(
    agent_id: str,
    topic: str,
    round_name: str,
    mode: str,
    context: Optional[Dict[str, List[Any]]] = None,
) -> str:
    """
    构建指定轮次的 prompt

    Args:
        agent_id: Agent 标识符
        topic: 讨论主题
        round_name: 轮次名称（R1, R2, R3, R4, R5）
        mode: 讨论模式（pre-ac, post-ac）
        context: 历史讨论结果 {round_name: [AgentResult, ...]}

    Returns:
        完整的 prompt 字符串
    """
    frame = _load_framework()

    # 提取模板
    marker = _ROUND_MARKERS.get(round_name)
    if not marker:
        raise ValueError(f"不支持的轮次：{round_name}")
    template = _extract_section(frame, marker)

    # 轮次特有替换
    template = template.replace("{topic}", topic)
    template = template.replace("{role}", _role_to_industry(agent_id))

    # R5 替换 full_discussion_history
    if round_name == "R5":
        history = _build_context_summary(context)
        template = template.replace("{full_discussion_history}", history)

    # 非 R5 轮次：如果是 R2-R4 需要注入context，交给 engine 的旧逻辑兼容
    # engine 层改为调用 prompt_builder 后，自己追加上下文摘要

    # 行业特定内容占位（留给 engine 层填充）
    template = template.replace("{industry_specific_content}", "(请从专业角度展开)"

) if "{industry_specific_content}" in template else template

    return template


def _build_context_summary(context: Optional[Dict]) -> str:
    """构建 R5 所需的完整讨论历史摘要"""
    if not context:
        return "（无历史讨论内容）"

    summary_lines = []
    for round_name in ["R1", "R2", "R3", "R4"]:
        results = context.get(round_name, [])
        for result in results:
            if not result.success:
                continue
            content_preview = (result.content[:200] + "...") if len(result.content) > 200 else result.content
            summary_lines.append(f"### {result.agent_id} ({round_name})\n{content_preview}\n")

    return "\n".join(summary_lines) if summary_lines else "（无历史讨论内容）"


def build_fallback_prompt(agent_id: str, topic: str, round_name: str, mode: str) -> str:
    """
    如果框架模板读取失败，使用极简 fallback 提示词
    """
    role = _role_to_industry(agent_id)
    return f"""# RoundTable 多 Agent 深度讨论

## 你的角色
你是一位资深 {role} 专家。

## 讨论主题
{topic}

## 当前轮次
{round_name}

请从你的专业角度，对主题进行深度分析。要求：
1. 提供具体的技术细节、数据支持或案例说明
2. 敢于质疑，识别方案中的漏洞和风险
3. 使用 Markdown 格式输出（标题、表格、列表等）
4. 内容充实，至少 500 字
"""


if __name__ == "__main__":
    # 测试
    print(build_prompt("engineering", "测试主题", "R1", "pre-ac"))
