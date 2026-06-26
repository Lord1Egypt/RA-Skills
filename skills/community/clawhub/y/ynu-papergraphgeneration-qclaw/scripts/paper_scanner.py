"""
paper_scanner.py - 论文全篇深度扫描
自动识别所有可可视化的部分，输出优先级排序的建议列表

能力：
  - 扫描论文全文（自动分块处理长论文）
  - 识别 5 类可图化内容：架构描述、算法流程、实验对比、概念动机、实验环境
  - 输出结构化 JSON：每项包含图类型、所在章节、优先级、具体理由
  - 支持用户确认后批量调用 Pipeline
"""

import json


# ============================================================
# 扫描 Prompt 模板
# ============================================================

SCAN_PROMPT_TEMPLATE = """你是一个学术论文图表规划专家。请深度分析以下论文章节，找出所有适合可视化的内容。

## 任务
逐段分析论文内容，识别出可以用学术插图展示的部分。对于每个可图化的内容，记录：
1. 它在论文的哪个部分（章节标题或段落位置）
2. 适合什么类型的图
3. 为什么要画这个图（它能帮助读者理解什么）
4. 优先级（1=最重要，必须画；2=推荐画；3=可选）

## 图类型定义
- **architecture**: 模型架构、系统框架、模块组成、数据流向。触发词：model, framework, architecture, module, component, pipeline, encoder, decoder, backbone, transformer, network, layer
- **flowchart**: 算法步骤、训练流程、推理流程、数据处理流程。触发词：algorithm, procedure, step, process, training, inference, iteration, pseudo-code, forward, backward
- **results**: 实验结果、性能对比、消融实验、排行榜。触发词：experiment, result, comparison, baseline, ablation, metric, accuracy, F1, BLEU, performance, table
- **teaser**: 研究动机、问题定义、核心创新、应用场景。触发词：motivation, problem, challenge, contribution, key insight, overview, we propose
- **environment**: 强化学习环境、Agent 交互、任务设定。触发词：environment, agent, state, action, reward, reinforcement, MDP, interaction

## 论文内容（片段 {chunk_idx}/{chunk_total}）
---
{paper_chunk}
---

## 输出格式（严格 JSON）
```json
[
  {{
    "figure_type": "architecture|flowchart|results|teaser|environment",
    "section": "章节标题或位置描述（如 Section 3: Methodology Overview）",
    "priority": 1,
    "reason": "为什么要画这个图",
    "suggested_title": "建议的图表标题（英文，适合 LaTeX caption）",
    "key_content_summary": "这段内容的核心要点（2-3 句话，用于后续 Prompt 生成）"
  }}
]
```

注意：
- 如果这个片段中没有可图化的内容，返回空数组 `[]`
- 不要重复：同一模块的描述只记录一次，即使出现在多个段落
- 优先关注描述具体结构的段落，忽略纯理论推导
- 只输出 JSON，不要任何解释文字
"""


SCAN_SUMMARY_PROMPT = """你是一个学术论文图表规划专家。以下是对同一篇论文多个片段的扫描结果，可能存在重复项。

请合并去重，按优先级排序（1 在前），输出最终的可视化建议列表。

## 原始扫描结果
{scan_results}

## 输出格式（严格 JSON）
```json
[
  {{
    "id": 1,
    "figure_type": "architecture|flowchart|results|teaser|environment",
    "section": "章节位置",
    "priority": 1,
    "reason": "理由",
    "suggested_title": "LaTeX caption 标题",
    "key_content_summary": "核心要点",
    "dependencies": []
  }}
]
```

规则：
- `id` 从 1 开始递增
- 同一内容只保留一个（合并重复项，保留信息更丰富的版本）
- `priority` 重新评估：architecture 通常优先级最高（读者第一眼看框架图）
- `dependencies` 标注依赖关系（如 teaser 图不依赖其他图，results 图依赖 architecture 图的理解）
- 最多保留 8 个建议（一篇论文通常 4-6 个图已经足够）
- 只输出 JSON
"""


# ============================================================
# 核心函数
# ============================================================

def chunk_paper(paper_content: str, max_chars: int = 6000, overlap: int = 500) -> list:
    """
    将长论文分块，每块 max_chars 字符，overlap 字符重叠
    确保不会在句子中间截断
    """
    if len(paper_content) <= max_chars:
        return [paper_content]

    chunks = []
    start = 0
    while start < len(paper_content):
        end = start + max_chars

        if end < len(paper_content):
            # 在句号/换行处截断，避免断句
            best_break = end
            for sep in ["\n\n", ".\n", "\n", ". ", " "]:
                pos = paper_content.rfind(sep, start + max_chars // 2, end)
                if pos > start:
                    best_break = pos + len(sep)
                    break
            end = best_break

        chunks.append(paper_content[start:end])
        start = end - overlap

        if start >= len(paper_content):
            break

    return chunks


def scan_chunk(llm_call_fn, chunk: str, chunk_idx: int, chunk_total: int) -> list:
    """
    扫描单个分块，返回发现的可图化内容列表
    """
    prompt = SCAN_PROMPT_TEMPLATE.format(
        chunk_idx=chunk_idx,
        chunk_total=chunk_total,
        paper_chunk=chunk
    )

    try:
        raw = llm_call_fn(prompt)
        return _parse_scan_result(raw)
    except Exception as e:
        print(f"[Scanner] Chunk {chunk_idx} scan failed: {e}", flush=True)
        return []


def scan_paper(llm_call_fn, paper_content: str) -> list:
    """
    全篇扫描主入口

    Args:
        llm_call_fn: callable(str) -> str，LLM 调用函数
        paper_content: 论文全文

    Returns:
        list[dict]: 合并去重后的可视化建议列表
    """
    print(f"[Scanner] Scanning paper ({len(paper_content)} chars)...", flush=True)

    chunks = chunk_paper(paper_content)
    print(f"[Scanner] Split into {len(chunks)} chunks", flush=True)

    # 逐块扫描
    all_findings = []
    for i, chunk in enumerate(chunks, 1):
        print(f"[Scanner] Scanning chunk {i}/{len(chunks)}...", flush=True)
        findings = scan_chunk(llm_call_fn, chunk, i, len(chunks))
        all_findings.extend(findings)

    if not all_findings:
        print("[Scanner] No visualizable content found.", flush=True)
        return []

    print(f"[Scanner] Found {len(all_findings)} raw candidates, merging...", flush=True)

    # 合并去重
    merged = _merge_results(llm_call_fn, all_findings)

    # 按 id 排序
    merged.sort(key=lambda x: x.get("id", 999))

    print(f"[Scanner] Final: {len(merged)} visualization suggestions", flush=True)
    return merged


def format_scan_report(findings: list) -> str:
    """
    将扫描结果格式化为用户可读的报告
    """
    if not findings:
        return "No visualizable content identified in this paper."

    type_icon = {
        "architecture": "🏗️",
        "flowchart": "🔄",
        "results": "📊",
        "teaser": "💡",
        "environment": "🌍"
    }

    lines = [
        "## Paper Visualization Report",
        "",
        f"Identified **{len(findings)}** visualizable sections:",
        ""
    ]

    for item in findings:
        fid = item.get("id", "?")
        ftype = item.get("figure_type", "?")
        section = item.get("section", "?")
        priority = item.get("priority", "?")
        reason = item.get("reason", "")
        title = item.get("suggested_title", "")
        deps = item.get("dependencies", [])

        icon = type_icon.get(ftype, "📄")
        prio_label = {1: "**High**", 2: "Medium", 3: "Low"}.get(priority, str(priority))

        lines.append(f"### {icon} #{fid} [{ftype.upper()}] — {prio_label} Priority")
        lines.append(f"- **Section:** {section}")
        lines.append(f"- **Title:** {title}")
        lines.append(f"- **Reason:** {reason}")
        if deps:
            lines.append(f"- **Depends on:** #{', #'.join(str(d) for d in deps)}")
        lines.append("")

    lines.append("---")
    lines.append("**Select figures to generate.** Example replies:")
    lines.append("- `all` — Generate all")
    lines.append("- `1, 3, 5` — Generate specific figures")
    lines.append("- `1` — Generate only the first one")
    lines.append("- `none` — Cancel")

    return "\n".join(lines)


def parse_user_selection(user_input: str, total_count: int) -> list:
    """
    解析用户选择，返回要生成的 figure id 列表
    """
    user_input = user_input.strip().lower().replace("，", ",").replace(" ", "")

    if user_input in ("all", "全部"):
        return list(range(1, total_count + 1))

    if user_input in ("none", "取消", "cancel", "0"):
        return []

    try:
        ids = [int(x.strip()) for x in user_input.split(",") if x.strip()]
        return [i for i in ids if 1 <= i <= total_count]
    except ValueError:
        return []


# ============================================================
# 内部工具函数
# ============================================================

def _parse_scan_result(raw: str) -> list:
    """解析单个 chunk 的扫描结果 JSON"""
    json_start = raw.find("[")
    json_end = raw.rfind("]") + 1

    if json_start == -1 or json_end <= json_start:
        return []

    try:
        return json.loads(raw[json_start:json_end])
    except json.JSONDecodeError:
        return []


def _merge_results(llm_call_fn, findings: list) -> list:
    """用 LLM 合并去重扫描结果"""
    findings_json = json.dumps(findings, ensure_ascii=False, indent=2)
    prompt = SCAN_SUMMARY_PROMPT.format(scan_results=findings_json)

    try:
        raw = llm_call_fn(prompt)
        return _parse_scan_result(raw)
    except Exception as e:
        print(f"[Scanner] Merge failed, using raw results: {e}", flush=True)
        # fallback: 直接去重
        seen = set()
        unique = []
        for f in findings:
            key = f.get("section", "") + f.get("figure_type", "")
            if key not in seen:
                seen.add(key)
                f["id"] = len(unique) + 1
                unique.append(f)
        return unique
