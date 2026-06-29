#!/usr/bin/env python3
"""
reviewer.py - 节点内容评审器 v1.0

职责：
  AI 质量评审节点内容，关注合理性、逻辑性、流畅性
  不做强制规则判断，给出优化建议而非简单的通过/不通过

评审分层：
  第一层（程序兜底）：极端异常（空内容、乱码）→ 打回
  第二层（AI 评审）：质量评判 + 优化建议

用法：
  result = review_node(paper_name, node_id, content)
"""

import re
import sys
from typing import Any, Dict, List, Optional

try:
    from .state_manager_v2 import outline_load, outline_get_node
except ImportError:
    from state_manager_v2 import outline_load, outline_get_node


# ============================================================
# 第一层：程序兜底检查
# ============================================================

def program_check(content: str, node_id: str) -> Dict[str, Any]:
    """
    程序兜底检查，处理极端异常情况。
    返回 {passed: bool, reason: str}
    """
    if not content or len(content.strip()) < 10:
        return {
            "passed": False,
            "reason": "内容为空或字数极少，无法进行有效评审",
            "layer": "program"
        }

    # 检测乱码（连续非打印字符）
    if re.search(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', content):
        return {
            "passed": False,
            "reason": "内容包含乱码或不可见字符",
            "layer": "program"
        }

    # 检测连续重复字符（可能是生成异常）
    if re.search(r'(.)\1{10,}', content):
        return {
            "passed": False,
            "reason": "内容疑似生成异常（连续重复字符）",
            "layer": "program"
        }

    return {"passed": True, "reason": "", "layer": "program"}


# ============================================================
# AI 评审 Prompt 构建
# ============================================================

def build_review_prompt(node_id: str, node_title: str, content: str,
                       bridge_paragraph: Optional[str] = None,
                       word_count_range: tuple = None) -> str:
    """
    构建评审 prompt
    """
    prompt = f"""## 评审节点：{node_title}（{node_id}）

### 节点内容
---
{content}
---

### 评审要求

你是一位资深的 MBA 学术论文评审专家。请对上述内容进行质量评审，重点关注：

1. **逻辑性**：论证是否层层递进、因果关系是否清晰
2. **流畅性**：段落之间过渡是否自然、阅读是否顺畅
3. **衔接性**：与前文（bridge）是否自然衔接
4. **完整性**：内容是否完整、论述是否充分
5. **学术性**：用词是否规范、是否符合学术论文风格

### 输出格式

请按以下 JSON 格式输出评审结果：

{{
  "quality": "high" | "medium" | "low",
  "summary": "一段话总结本节内容的质量评估",
  "strengths": ["优点1", "优点2"],
  "weaknesses": ["问题1", "问题2"],
  "suggestions": ["优化建议1", "优化建议2"]
}}

### 注意事项
- quality = "high"：内容质量优秀，可直接进入下一节点
- quality = "medium"：有小幅优化空间，用户可选择是否修改
- quality = "low"：存在明显问题，建议修改后再进入下一节点
- 请严格按 JSON 格式输出，不要添加其他内容
"""

    if bridge_paragraph:
        prompt += f"\n\n### 前文衔接（Bridge）\n---\n{bridge_paragraph}\n---\n\n请特别关注内容是否与前文自然衔接。"

    if word_count_range:
        prompt += f"\n\n### 字数参考范围\n目标字数：{word_count_range[0]} - {word_count_range[1]} 字"

    return prompt


# ============================================================
# AI 评审（需注入 LLM）
# ============================================================

def ai_review(paper_name: str, node_id: str,
              llm_func: callable) -> Dict[str, Any]:
    """
    AI 质量评审。
    由调用方注入 llm_func。
    """
    # 获取节点信息
    node = outline_get_node(paper_name, node_id)
    if not node:
        return {
            "ok": False,
            "error": f"节点 {node_id} 不存在"
        }

    content = node.get("content", "")
    title = node.get("title", node_id)
    word_count_range = node.get("word_count_range", None)

    # 构建 bridge（从上下文获取）
    bridge = node.get("bridge_paragraph", None)

    # 构建 prompt
    prompt = build_review_prompt(node_id, title, content, bridge, word_count_range)

    try:
        response = llm_func(prompt)
    except Exception as e:
        return {
            "ok": False,
            "error": f"AI 评审调用失败: {str(e)}"
        }

    # 解析 JSON 响应
    try:
        # 尝试提取 JSON（可能在 markdown 代码块中）
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response)
    except Exception:
        return {
            "ok": False,
            "error": "AI 评审结果解析失败",
            "raw_response": response
        }

    return {
        "ok": True,
        "node_id": node_id,
        "quality": result.get("quality", "medium"),
        "summary": result.get("summary", ""),
        "strengths": result.get("strengths", []),
        "weaknesses": result.get("weaknesses", []),
        "suggestions": result.get("suggestions", [])
    }


# ============================================================
# 简化版：返回 prompt（供外部调用 LLM）
# ============================================================

def review_node_prompt(paper_name: str, node_id: str) -> Optional[str]:
    """
    返回评审 prompt，供调用方注入 LLM。
    返回 None 表示节点不存在或内容异常。
    """
    node = outline_get_node(paper_name, node_id)
    if not node:
        return None

    content = node.get("content", "")
    title = node.get("title", node_id)
    word_count_range = node.get("word_count_range", None)
    bridge = node.get("bridge_paragraph", None)

    return build_review_prompt(node_id, title, content, bridge, word_count_range)


def parse_review_response(response: str) -> Dict[str, Any]:
    """
    解析 AI 评审响应，返回结构化结果。
    """
    try:
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response)
        return {"ok": True, **result}
    except Exception as e:
        return {
            "ok": False,
            "error": f"解析失败: {str(e)}",
            "raw": response
        }


# ============================================================
# 便捷入口：单次调用完成评审
# ============================================================

def review_node(paper_name: str, node_id: str,
                llm_func: callable) -> Dict[str, Any]:
    """
    便捷入口：第一层兜底 + AI 评审。
    llm_func: (prompt: str) -> str
    """
    # 获取节点内容
    node = outline_get_node(paper_name, node_id)
    if not node:
        return {
            "ok": False,
            "passed": False,
            "layer": "program",
            "reason": f"节点 {node_id} 不存在"
        }

    content = node.get("content", "")

    # 第一层：程序兜底
    program_result = program_check(content, node_id)
    if not program_result["passed"]:
        return {
            "ok": True,
            "passed": False,
            "layer": "program",
            "reason": program_result["reason"],
            "suggestions": []
        }

    # 第二层：AI 评审
    ai_result = ai_review(paper_name, node_id, llm_func)
    return {
        "ok": ai_result.get("ok", False),
        "passed": ai_result.get("ok", False) and ai_result.get("quality") != "low",
        "layer": "ai",
        "quality": ai_result.get("quality", "medium"),
        "summary": ai_result.get("summary", ""),
        "strengths": ai_result.get("strengths", []),
        "weaknesses": ai_result.get("weaknesses", []),
        "suggestions": ai_result.get("suggestions", []),
        "error": ai_result.get("error", "")
    }


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"用法: {sys.argv[0]} <paper_name> <node_id>", file=sys.stderr)
        print("（CLI 模式仅供调试，实际调用需注入 LLM）", file=sys.stderr)
        sys.exit(1)

    paper_name = sys.argv[1]
    node_id = sys.argv[2]

    prompt = review_node_prompt(paper_name, node_id)
    if not prompt:
        print(f"节点 {node_id} 不存在", file=sys.stderr)
        sys.exit(1)

    print("=== 评审 Prompt ===")
    print(prompt)
    print("\n请手动调用 LLM 并使用 parse_review_response() 解析结果")
