#!/usr/bin/env python3
"""
semantic-split Pipeline C — 双视角推理（智能体原生模式） v0.1.0

⚠️ 运行在智能体中，LLM 即智能体本身，不需要外部 API 配置。

工作方式：
  1. pipeline_c.py 构建结构化的推理上下文（5W2H + 约束 + 聚焦/发散 prompt）
  2. 输出 JSON 标记 `{"mode": "agent_reasoning", ...}`
  3. 智能体（WorkBuddy）读取该标记后，用自己的推理能力生成步骤
  4. 步骤回填到输出

层级：
  Pipeline C = 构建推理上下文（Python） → 智能体原生推理（Agent） → 解析步骤（Python）

用法:
  from pipeline_c import build_reasoning_context
  context = build_reasoning_context(five_w2h, constraints)
  # 输出 context，智能体读取后执行推理
"""

import json
import re

FOCUS_SYSTEM = """你是一个专注于生成保守、安全执行方案的任务规划专家。
你的职责是：
1. 严格遵守所有🔴硬约束
2. 对每个维度选择最窄/最保守/最直接的值
3. 只使用已验证、低学习成本的方法
4. 每个步骤不超过30分钟可完成
5. 输出JSON格式的步骤列表，每步骤含 name/action/milestone/depends_on/parallel_group/dependency_heat"""

DIVERGENT_SYSTEM = """你是一个专注于生成创新、大胆执行方案的任务规划专家。
你的职责是：
1. 对每个维度选择最宽/最大胆/最间接的值
2. 🔴硬约束可轻微突破，但必须标注风险并提供备用方案
3. 引入至少一个非惯用工具或方法
4. 包含"如果无限资源会怎么做"的变体
5. 输出JSON格式的步骤列表+创新点列表"""

INTEGRATION_SYSTEM = """你是一个任务规划整合专家。
你的职责是：
1. 以聚焦方案为骨架
2. 将发散方案的创新点嵌入聚焦方案对应步骤
3. 所有🌟步骤注明来源
4. 风险说明标注清楚
5. 输出单一的JSON步骤列表"""


def build_reasoning_context(five_w2h: dict, constraints: list = None,
                             structure_analysis: dict = None,
                             template_matches: list = None) -> dict:
    """
    构建双视角推理的完整上下文。
    包含结构分析 + 模板匹配，用于增强 LLM 思考深度。

    返回格式:
    {
      "mode": "agent_reasoning",
      "type": "dual_perspective",
      "context": { ... 5W2H + 约束 + prompt + 结构分析 + 模板参考 },
      "sub_steps": [...]
    }
    """
    # ── 任务描述（5W2H + 约束） ──
    parts = ["## 任务描述"]
    dim_labels = [
        ("目的", "why"), ("行为", "what"), ("执行方", "who"),
        ("地点", "where"), ("时间", "when"), ("方法", "how"), ("度量", "how_much"),
    ]
    for label, key in dim_labels:
        val = five_w2h.get(key, {})
        if val and val.get("value"):
            parts.append(f"- {label}: {val['value']}")
        else:
            parts.append(f"- {label}: (未指定)")

    constraint_summary = []
    if constraints:
        parts.append("\n## 约束")
        for c in constraints:
            level = c.get("level", "none")
            kw = c.get("keyword", "")
            domain = c.get("domain", "")
            flag = "🔴" if level == "critical" else "🟡" if level == "soft" else "⚪"
            parts.append(f"- {flag} {level} ({domain}): {kw}")
            constraint_summary.append({"level": level, "keyword": kw, "domain": domain})

    # ── 结构分析增强（增强思考深度） ──
    structure_section = ""
    if structure_analysis:
        sa_parts = []
        ner = structure_analysis.get("ner", [])
        if ner:
            sa_parts.append(f"  实体: {', '.join([f'{t}({l})' for t,l in ner[:8]])}")
        verbs = structure_analysis.get("verbs", [])
        if verbs:
            sa_parts.append(f"  动词: {', '.join([v[0] for v in verbs[:6]])}")
        dep = structure_analysis.get("dep", [])
        if dep:
            sa_parts.append(f"  依存关系: {', '.join([f'{s}->{o}({r})' for s,o,r in dep[:6]])}")
        if sa_parts:
            structure_section = "\n".join(sa_parts)

    # ── 模板匹配参考（few-shot 增强） ──
    templates_section = ""
    if template_matches:
        tm_parts = ["## 相似历史案例参考"]
        for m in template_matches[:3]:
            name = m.get("name", m.get("id", "?"))
            score = m.get("score", 0)
            tm_parts.append(f"- [{name}] (相似度 {score:.2f})")
        templates_section = "\n".join(tm_parts)

    return {
        "mode": "agent_reasoning",
        "type": "dual_perspective",
        "context": {
            "task": "\n".join(parts),
            "five_w2h": {k: v.get("value", "") if isinstance(v, dict) else v for k, v in five_w2h.items() if isinstance(v, dict)},
            "constraints": constraint_summary,
            "structure_analysis": structure_section,
            "template_references": templates_section,
            "_note": "structure_analysis 和 template_references 已作为增强输入，智能体阅读后可直接提升推理质量",
        },
        "prompts": {
            "focus": {
                "system": FOCUS_SYSTEM,
                "description": "生成保守聚焦方案",
                "steps_name": "聚焦方案步骤",
            },
            "divergent": {
                "system": DIVERGENT_SYSTEM,
                "description": "生成创新发散方案",
                "steps_name": "发散方案步骤+创新点",
            },
            "integration": {
                "system": INTEGRATION_SYSTEM,
                "description": "将聚焦+发散整合为单一方案",
                "steps_name": "最终整合步骤",
            },
        },
        "sub_steps": [
            {"id": "focus", "name": "生成聚焦方案", "requires_agent": True},
            {"id": "diverge", "name": "生成发散方案", "requires_agent": True},
            {"id": "integrate", "name": "整合为单一方案", "requires_agent": True},
        ],
    }


def build_wp_context(steps: list) -> dict:
    """
    构建 WP 分解上下文。
    返回 JSON，智能体读取后执行 WP 分解。
    """
    return {
        "mode": "agent_reasoning",
        "type": "wp_decomposition",
        "context": {
            "steps": steps[:10],
            "rule": "每个WP 2-4小时，每3-5个WP一个检查点，格式 WP{n}: [任务] (预计耗时，前置：WP{x})",
        },
    }


# ============================================================
# 步骤解析
# ============================================================

def parse_steps_from_agent(steps_json: str) -> list:
    """
    智能体完成推理后，解析结果 JSON 为步骤列表。
    """
    try:
        data = json.loads(steps_json)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            # 尝试从常见 key 提取
            for key in ("steps", "results", "items", "plan"):
                if key in data and isinstance(data[key], list):
                    return data[key]
            return [data]
    except (json.JSONDecodeError, TypeError):
        pass

    # 尝试从文本中提取 ```json ... ``` 块
    code_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', steps_json, re.DOTALL)
    if code_match:
        try:
            return json.loads(code_match.group(1))
        except json.JSONDecodeError:
            pass

    return []


def decompose_wps(steps: list) -> list:
    """WP 分解（脚本级，无需 LLM）"""
    from pipeline_b import wps_decompose as _wps
    return _wps(steps) if steps else []


if __name__ == "__main__":
    test_w2h = {
        "what": {"value": "制作PPT", "source": "regex"},
        "why": {},
        "who": {"value": "用户", "source": "regex"},
        "when": {"value": "下周", "source": "regex"},
        "how": {"value": "公司模板", "source": "regex"},
    }
    ctx = build_reasoning_context(test_w2h)
    print(json.dumps(ctx, ensure_ascii=False, indent=2))
