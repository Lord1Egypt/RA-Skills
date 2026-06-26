"""
skill-evolve-pro · Phase 1
核心进化引擎：整合 Reflect → Aggregate → Select → Update 四步
基于 SkillOpt/ReflACT 框架

API: DeepSeek, model=deepseek-v4-pro
"""

from __future__ import annotations

import json
import re
import sys
import time
from typing import Any
from dataclasses import dataclass

# ── 配置（优先读取 config.py，其次环境变量）─────────────────────────────────
try:
    from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL
except ImportError:
    import os
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
    if not DEEPSEEK_API_KEY:
        raise RuntimeError(
            "DEEPSEEK_API_KEY 未设置！请在 config.py 中填写，或设置环境变量 DEEPSEEK_API_KEY"
        )

# ── 慢更新保护区标记 ──────────────────────────────────────────────────────────

SLOW_UPDATE_START = "<!-- SLOW_UPDATE_START -->"
SLOW_UPDATE_END = "<!-- SLOW_UPDATE_END -->"


def _strip_slow_update_markers(text: str) -> str:
    return (text.replace(SLOW_UPDATE_START, "")
             .replace(SLOW_UPDATE_END, ""))


def _is_in_slow_update_region(skill: str, target: str) -> bool:
    start_idx = skill.find(SLOW_UPDATE_START)
    end_idx = skill.find(SLOW_UPDATE_END)
    if start_idx == -1 or end_idx == -1:
        return False
    target_idx = skill.find(target)
    if target_idx == -1:
        return False
    region_end = end_idx + len(SLOW_UPDATE_END)
    return start_idx <= target_idx < region_end


def _apply_single_edit(skill: str, edit: dict) -> tuple[str, dict]:
    """应用单条编辑操作，返回 (新技能, 报告)."""
    op = edit.get("op", "")
    content = _strip_slow_update_markers(edit.get("content", "").strip())
    target = edit.get("target", "")

    report: dict[str, Any] = {
        "op": op,
        "target": target[:200],
        "content_preview": content[:200],
        "status": "unknown",
    }

    if target and _is_in_slow_update_region(skill, target):
        report["status"] = "skipped_protected_slow_update_region"
        return skill, report

    if op == "append":
        su_start = skill.find(SLOW_UPDATE_START)
        if su_start != -1:
            before = skill[:su_start].rstrip()
            after = skill[su_start:]
            report["status"] = "applied_append_before_slow_update"
            return before + "\n\n" + content + "\n\n" + after, report
        report["status"] = "applied_append"
        return skill.rstrip() + "\n\n" + content + "\n", report

    if op == "insert_after":
        if not target or target not in skill:
            su_start = skill.find(SLOW_UPDATE_START)
            if su_start != -1:
                before = skill[:su_start].rstrip()
                after = skill[su_start:]
                report["status"] = "applied_insert_after_fallback_before_slow_update"
                return before + "\n\n" + content + "\n\n" + after, report
            report["status"] = "applied_insert_after_fallback_append"
            return skill.rstrip() + "\n\n" + content + "\n", report
        idx = skill.index(target) + len(target)
        newline = skill.find("\n", idx)
        insert_at = newline + 1 if newline != -1 else len(skill)
        report["status"] = "applied_insert_after"
        return skill[:insert_at] + "\n" + content + "\n" + skill[insert_at:], report

    if op == "replace":
        if not target:
            report["status"] = "skipped_replace_missing_target"
            return skill, report
        if target not in skill:
            report["status"] = "skipped_replace_target_not_found"
            return skill, report
        report["status"] = "applied_replace"
        return skill.replace(target, content, 1), report

    if op == "delete":
        if not target:
            report["status"] = "skipped_delete_missing_target"
            return skill, report
        if target not in skill:
            report["status"] = "skipped_delete_target_not_found"
            return skill, report
        report["status"] = "applied_delete"
        return skill.replace(target, "", 1), report

    report["status"] = "skipped_unknown_op"
    return skill, report


def apply_patch(skill: str, edits: list[dict]) -> tuple[str, list[dict]]:
    """顺序应用编辑列表，返回 (新技能, 报告列表)."""
    reports: list[dict] = []
    for idx, edit in enumerate(edits, 1):
        try:
            skill, report = _apply_single_edit(skill, edit)
            report["index"] = idx
        except Exception as exc:
            report = {
                "index": idx,
                "op": "",
                "target": "",
                "content_preview": "",
                "status": "error",
                "error": str(exc),
            }
        reports.append(report)
    return skill, reports


# ── DeepSeek API 调用 ──────────────────────────────────────────────────────────

def _chat(
    messages: list[dict],
    max_completion_tokens: int = 64000,
    temperature: float = 0.7,
    retry: int = 3,
) -> str:
    import urllib.request
    import urllib.error

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_completion_tokens,
        "temperature": temperature,
    }

    for attempt in range(retry):
        try:
            req = urllib.request.Request(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if attempt == retry - 1:
                body = e.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"DeepSeek HTTP {e.code}: {body}") from e
        except Exception as e:
            if attempt == retry - 1:
                raise RuntimeError(f"DeepSeek API error: {e}") from e
        time.sleep(1)


def extract_json(text: str) -> dict | None:
    """从 LLM 输出中提取 JSON。"""
    text = text.strip()
    fences = ["```json", "```"]
    for fence in fences:
        if text.startswith(fence):
            end = text[len(fence):].find("```")
            if end != -1:
                text = text[len(fence):end + len(fence)].strip()
            else:
                text = text[len(fence):].strip()
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        return None


# ── Step ② Reflect ────────────────────────────────────────────────────────────

REFLECT_SYSTEM = """你是一位 AI 技能优化专家。你的任务是对失败轨迹进行深入分析，生成具体、可操作的修改建议，帮助改进技能文档（SKILL.md）。

分析维度：
1. 失败模式识别：是什么类型的错误（上下文缺失、步骤遗漏、格式错误、逻辑错误…）
2. 技能缺陷定位：技能文档中哪个部分导致了该失败
3. 改进建议生成：具体告诉 AI 应该如何修改 SKILL.md

每条建议需包含：
- type: add_rule | modify_step | fix_context | rewrite_section | add_example
- title: 简短标题（≤15字）
- instruction: 具体修改指令（要明确告诉 AI 改什么、怎么改）
- priority_hint: high | medium | low
- target: 要修改的目标文本片断（如果能定位到的话，可以为空字符串）

返回格式（严格 JSON）：
{
  "revise_suggestions": [
    {
      "type": "...",
      "title": "...",
      "instruction": "...",
      "priority_hint": "high|medium|low",
      "target": "..."
    }
  ],
  "analysis_summary": "整体分析摘要（100字以内）"
}"""


def run_reflect(trajectories: list[dict]) -> dict:
    """对失败轨迹执行 Reflect 阶段，生成修改建议。"""
    formatted = []
    for i, traj in enumerate(trajectories, 1):
        task = traj.get("task_description", traj.get("question", ""))[:300]
        fail_reason = traj.get("fail_reason", "unknown")[:300]
        predicted = traj.get("predicted_answer", "")[:200]
        reference = traj.get("reference_text", "")[:200]
        formatted.append(
            f"--- 轨迹 {i} ---\n"
            f"任务: {task}\n"
            f"失败原因: {fail_reason}\n"
            f"预测答案: {predicted}\n"
            f"参考答案: {reference}"
        )

    user = (
        "以下是失败轨迹列表，每条包含任务描述、失败原因、预测答案和参考答案：\n\n"
        + "\n\n".join(formatted)
        + "\n\n请分析以上轨迹，生成改进 SKILL.md 的具体建议。返回严格 JSON 格式。"
    )

    response = _chat(
        messages=[
            {"role": "system", "content": REFLECT_SYSTEM},
            {"role": "user", "content": user},
        ],
        max_completion_tokens=16384,
    )

    result = extract_json(response)
    if result is None:
        return {"revise_suggestions": [], "analysis_summary": "JSON 解析失败"}

    return {
        "revise_suggestions": result.get("revise_suggestions", []),
        "analysis_summary": result.get("analysis_summary", ""),
    }


# ── Step ③ Aggregate ──────────────────────────────────────────────────────────

def aggregate_suggestions(raw_patches: list[dict]) -> dict:
    """合并多条建议，去重并按优先级排序。"""
    all_suggestions: list[dict] = []
    for patch in raw_patches:
        all_suggestions.extend(patch.get("revise_suggestions", []))

    order = {"high": 0, "medium": 1, "low": 2, "": 3}
    all_suggestions.sort(
        key=lambda s: (
            order.get(str(s.get("priority_hint", "")).lower(), 3),
            0 if s.get("target") else 1,
        )
    )

    seen: set[tuple[str, str]] = set()
    deduped: list[dict] = []
    for s in all_suggestions:
        key = (str(s.get("type", "")), str(s.get("target", ""))[:100])
        if key not in seen:
            seen.add(key)
            deduped.append(s)

    return {
        "edits": deduped,
        "reasoning": (
            f"聚合了 {len(all_suggestions)} 条建议，去重后 {len(deduped)} 条。"
            f"分析摘要: {raw_patches[0].get('analysis_summary', '') if raw_patches else ''}"
        ),
    }


# ── Step ④ Select (Clip) ─────────────────────────────────────────────────────

SELECT_SYSTEM = """你是一个严格的技能优化评审。你需要对候选编辑进行重要性排序，选出最有影响力的 top-L 条。

评分标准：
1. 影响范围：该编辑能修复多少失败轨迹
2. 精确度：target 是否精确定位了问题
3. 完整性：修改后是否能从根本上避免该类错误

返回格式（严格 JSON）：
{
  "selected_indices": [优先顺序的0基索引列表],
  "ranking_reasoning": "排序理由简述"
}"""


def rank_and_select(
    skill_content: str,
    patch: dict,
    max_edits: int,
) -> dict:
    """编辑预算裁剪 + 重要性排序。"""
    edits = patch.get("edits", [])
    if len(edits) <= max_edits:
        return patch

    edits_desc: list[str] = []
    for i, edit in enumerate(edits):
        edits_desc.append(
            f"[{i}] type={edit.get('type','?')} "
            f"target={str(edit.get('target', ''))[:100]!r} "
            f"instruction={str(edit.get('instruction', ''))[:200]!r}"
        )

    user = (
        f"## 当前技能文档（前1000字）\n{skill_content[:1000]}\n\n"
        f"## 编辑池（{len(edits)} 条，预算={max_edits}）\n"
        + "\n".join(edits_desc)
        + f"\n\n请选出最重要的 {max_edits} 条编辑（0基索引），按优先级从高到低排列。返回严格 JSON。"
    )

    try:
        response = _chat(
            messages=[
                {"role": "system", "content": SELECT_SYSTEM},
                {"role": "user", "content": user},
            ],
            max_completion_tokens=2048,
        )
        result = extract_json(response)
        if result and "selected_indices" in result:
            indices = result["selected_indices"]
            selected: list[dict] = []
            seen: set[int] = set()
            for idx in indices:
                if isinstance(idx, int) and 0 <= idx < len(edits) and idx not in seen:
                    selected.append(edits[idx])
                    seen.add(idx)
                    if len(selected) >= max_edits:
                        break
            if selected:
                return {
                    "edits": selected,
                    "reasoning": patch.get("reasoning", "")
                    + f" [LLM-ranked: 选中 {len(selected)}/{len(edits)} 条编辑]",
                    "ranking_details": result,
                }
    except Exception:
        pass

    return {
        "edits": edits[:max_edits],
        "reasoning": patch.get("reasoning", "")
        + f" [fallback truncated {len(edits)}->{max_edits}]",
    }


# ── Target 归一化（模糊匹配）─────────────────────────────────────────────────

# 所有 Unicode emoji 范围（简化版，覆盖常用 emoji）
_EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # enclosed characters
    "\U00002600-\U000026FF"  # misc symbols
    "\U00002700-\U000027BF"  # dingbats
    "]+"
)
# Markdown 标记：## ### ** __ ~~ ` > - [ ]()
_MD_MARKUP_RE = re.compile(
    r"(?:#+\s*|\*\*+|__+|~~+|`+|>+\s*|-\s+|\[\^?[^\]]*\]?\([^)]*\)|"
    r"\[\^?[^\]]*\]|\{[^\}]*\})"
)


@dataclass
class NormalizedTarget:
    """归一化后的 target 及其元信息"""
    original: str       # 原始 target（来自 DeepSeek）
    normalized: str     # 归一化后（去 emoji + 去 markdown + 去空白）
    core_keywords: list[str]  # 核心关键词列表
    anchor: str        # 在文档中匹配的锚点（最近的章节标题）


def _normalize_target(raw_target: str, skill_content: str) -> NormalizedTarget:
    """
    对 DeepSeek 返回的 target 做归一化处理：

    1. 去掉 emoji
    2. 去掉 markdown 标记（##、###、**、__、~~、`、>、-、[]() 等）
    3. 去掉多余空白
    4. 在文档中搜索核心关键词，找到最近的章节标题作为锚点
    """
    if not raw_target:
        return NormalizedTarget(original="", normalized="", core_keywords=[], anchor="")

    original = raw_target.strip()

    # Step 1: 去掉 emoji
    text = _EMOJI_RE.sub("", original)

    # Step 2: 去掉 markdown 标记
    text = _MD_MARKUP_RE.sub("", text)

    # Step 3: 去掉多余空白
    normalized = " ".join(text.split())

    # Step 4: 提取核心关键词（取 normalized 中长度>=2 的词）
    words = [w for w in re.split(r"[\s\-–—:,，。;；]+", normalized) if len(w) >= 2]
    core_keywords = words[:5]  # 最多取前5个

    # Step 5: 在文档中搜索核心关键词，找到最近的章节标题
    anchor = _find_anchor_in_doc(normalized, core_keywords, skill_content)

    return NormalizedTarget(
        original=original,
        normalized=normalized,
        core_keywords=core_keywords,
        anchor=anchor,
    )


def _find_anchor_in_doc(normalized: str, core_keywords: list[str], skill_content: str) -> str:
    """
    在文档中搜索核心关键词，找到最近的章节标题作为锚点。

    策略：
    1. 先用归一化后的完整 target 在文档中搜索
    2. 如果找不到，尝试用核心关键词逐个搜索
    3. 找到匹配后，找到最近的章节标题（## 或 ### 开头的行）
    4. 返回最近的章节标题行
    """
    if not normalized and not core_keywords:
        return ""

    # 先用 normalized 精确搜索
    search_texts = [normalized] if normalized else []
    search_texts.extend(core_keywords[:3])

    best_anchor = ""
    best_distance = float("inf")

    lines = skill_content.splitlines()
    # 找出所有章节标题行
    heading_indices: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            heading_indices.append((i, stripped.lstrip("#").strip()))

    for search_text in search_texts:
        if not search_text or len(search_text) < 2:
            continue

        # 在文档中搜索 search_text
        idx = skill_content.find(search_text)
        if idx == -1:
            continue

        # 计算 search_text 所在行
        line_offset = skill_content[:idx].count("\n")

        # 找最近的章节标题（向后优先，向前次之）
        nearest_heading = ""
        min_dist = float("inf")

        for h_idx, h_text in heading_indices:
            dist = abs(h_idx - line_offset)
            if dist < min_dist:
                min_dist = dist
                nearest_heading = h_text

        if nearest_heading and min_dist < best_distance:
            best_distance = min_dist
            best_anchor = nearest_heading

    return best_anchor


def _target_to_anchor(target: str, skill_content: str) -> str:
    """
    将 target 字符串转换为文档锚点。
    返回最近章节标题（如果找不到则返回原始 target）。
    """
    nt = _normalize_target(target, skill_content)
    # 如果 anchor 不为空，用 anchor；否则用 normalized；都不行则保留原始
    if nt.anchor:
        return nt.anchor
    if nt.normalized and len(nt.normalized) >= 3:
        return nt.normalized
    return target


# ── 建议 → Edit 格式转换 ─────────────────────────────────────────────────────

def suggestions_to_edits(suggestions: list[dict], skill_content: str = "") -> list[dict]:
    """
    将 ReviseSuggestions 转换为 Edit 格式（4种原子操作）。

    Parameters
    ----------
    suggestions : list[dict]
        DeepSeek 返回的修订建议列表
    skill_content : str
        当前技能文档内容（用于 target 归一化和锚点查找）

    Notes
    -----
    每个 edit 的 target 会经过归一化处理：
    - 去掉 emoji 和 markdown 标记
    - 在文档中搜索核心关键词，找到最近的章节标题作为锚点
    """
    op_map: dict[str, str] = {
        "add_rule": "append",
        "add_example": "append",
        "modify_step": "replace",
        "rewrite_section": "replace",
        "fix_context": "insert_after",
    }
    edits: list[dict] = []
    for s in suggestions:
        op = op_map.get(str(s.get("type", "")), "append")
        raw_target = str(s.get("target", ""))

        # 对 target 做归一化处理（模糊匹配）
        if skill_content and raw_target:
            anchor = _target_to_anchor(raw_target, skill_content)
            resolved_target = anchor
        else:
            resolved_target = raw_target

        edits.append({
            "op": op,
            "content": str(s.get("instruction", "")),
            "target": resolved_target,
            "original_target": raw_target,  # 保留原始 target 用于调试
            "source_type": "failure",
        })
    return edits


# ── 核心进化循环 ──────────────────────────────────────────────────────────────

def run_evolve_cycle(
    skill_content: str,
    trajectories: list[dict],
    max_edits: int = 8,
    update_mode: str = "patch",
) -> dict:
    """
    执行完整的进化循环（Phase 1: Reflect → Aggregate → Select → Update）。

    Parameters
    ----------
    skill_content : str
        当前技能文档内容。
    trajectories : list[dict]
        失败轨迹列表（每条需含 fail_reason, task_description 等字段）。
    max_edits : int
        编辑预算上限（默认8）。
    update_mode : str
        "patch" 模式（当前仅支持 patch）。

    Returns
    -------
    dict
        {
            "new_skill": str,           # 进化后的技能文档
            "edit_reports": list[dict], # 每步编辑的执行报告
            "selected_edits": list,     # 被选中的编辑列表
            "aggregate_reasoning": str, # 聚合阶段的推理说明
            "reflect_summary": str,     # Reflect 阶段分析摘要
        }
    """
    # Step ②: Reflect
    reflect_result = run_reflect(trajectories)

    # Step ③: Aggregate
    aggregate_patch = aggregate_suggestions([reflect_result])
    aggregate_patch["edits"] = suggestions_to_edits(
        aggregate_patch.get("edits", []),
        skill_content=skill_content,  # 传入 skill_content 用于 target 归一化
    )

    # Step ④: Select (Clip)
    selected_patch = rank_and_select(skill_content, aggregate_patch, max_edits)

    # Step ⑤: Update
    edits = selected_patch.get("edits", [])
    new_skill, edit_reports = apply_patch(skill_content, edits)

    # 保护区恢复检查
    if SLOW_UPDATE_START in skill_content and SLOW_UPDATE_START not in new_skill:
        start = skill_content.find(SLOW_UPDATE_START)
        end = skill_content.find(SLOW_UPDATE_END) + len(SLOW_UPDATE_END)
        protected_block = skill_content[start:end]
        new_skill = new_skill.rstrip() + "\n\n" + protected_block

    return {
        "new_skill": new_skill,
        "edit_reports": edit_reports,
        "selected_edits": edits,
        "aggregate_reasoning": aggregate_patch.get("reasoning", ""),
        "reflect_summary": reflect_result.get("analysis_summary", ""),
    }


# ── CLI 入口 ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    from trajectory_loader import load_failed_trajectories

    if len(sys.argv) < 3:
        print("用法: python evolve_core.py <技能文件路径> <轨迹目录> [max_edits]")
        sys.exit(1)

    skill_path = sys.argv[1]
    traj_dir = sys.argv[2]
    max_edits = int(sys.argv[3]) if len(sys.argv) > 3 else 8

    with open(skill_path, encoding="utf-8") as f:
        skill_content = f.read()

    trajectories = load_failed_trajectories(traj_dir)
    if not trajectories:
        print("错误: 轨迹目录为空，请放入 failed_trajectory_*.json 文件")
        sys.exit(1)

    print(f"[skill-evolve-pro] 加载轨迹: {len(trajectories)} 条")
    print(f"[skill-evolve-pro] 启动进化循环 (max_edits={max_edits})...")

    result = run_evolve_cycle(skill_content, trajectories, max_edits=max_edits)

    print(f"[skill-evolve-pro] 进化完成！")
    print(f"  - Reflect 分析摘要: {result['reflect_summary']}")
    print(f"  - 选中编辑数: {len(result['selected_edits'])}")
    print(f"  - 实际应用编辑数: {sum(1 for r in result['edit_reports'] if r.get('status','').startswith('applied'))}")

    # 输出新技能到 stdout
    print("\n===== 进化后的技能文档 =====\n")
    print(result["new_skill"])
