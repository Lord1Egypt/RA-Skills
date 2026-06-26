# -*- coding: utf-8 -*-
"""
skill-evolve-pro · Phase 3
skill_reflect.py — 反思生成模块

基于 RolloutResult 列表，调用 DeepSeek API 生成编辑建议（RawPatch）。
包含：错误分析师（失败轨迹）+ 成功分析师（成功轨迹）+ 聚合器。
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Callable

# ── Target 归一化（模糊匹配）───────────────────────────────────────────────

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


def _normalize_target(raw_target: str, skill_content: str = "") -> dict:
    """
    对 DeepSeek 返回的 target 做归一化处理，返回包含以下键的 dict：
    - original: 原始 target
    - normalized: 归一化后（去 emoji + 去 markdown + 去空白）
    - core_keywords: 核心关键词列表
    - anchor: 在文档中匹配的锚点（最近的章节标题）

    策略：
    1. 去掉 emoji
    2. 去掉 markdown 标记
    3. 去掉多余空白
    4. 提取核心关键词
    5. 在文档中搜索核心关键词，找到最近的章节标题作为锚点
    """
    if not raw_target:
        return {"original": "", "normalized": "", "core_keywords": [], "anchor": ""}

    original = raw_target.strip()

    # Step 1: 去掉 emoji
    text = _EMOJI_RE.sub("", original)

    # Step 2: 去掉 markdown 标记
    text = _MD_MARKUP_RE.sub("", text)

    # Step 3: 去掉多余空白
    normalized = " ".join(text.split())

    # Step 4: 提取核心关键词
    words = [w for w in re.split(r"[\s\-–—:,，。;；]+", normalized) if len(w) >= 2]
    core_keywords = words[:5]

    # Step 5: 在文档中搜索，找最近章节标题作为锚点
    anchor = _find_anchor_in_doc(normalized, core_keywords, skill_content)

    return {
        "original": original,
        "normalized": normalized,
        "core_keywords": core_keywords,
        "anchor": anchor,
    }


def _find_anchor_in_doc(normalized: str, core_keywords: list[str], skill_content: str) -> str:
    """
    在文档中搜索核心关键词，找到最近的章节标题作为锚点。
    返回最近章节标题（如果找不到则返回空字符串）。
    """
    if not skill_content:
        return ""

    search_texts = ([normalized] if normalized else []) + core_keywords[:3]
    best_anchor = ""
    best_distance = float("inf")

    lines = skill_content.splitlines()
    heading_indices: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            heading_indices.append((i, stripped.lstrip("#").strip()))

    if not heading_indices:
        return ""

    for search_text in search_texts:
        if not search_text or len(search_text) < 2:
            continue

        idx = skill_content.find(search_text)
        if idx == -1:
            continue

        line_offset = skill_content[:idx].count("\n")

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


def _resolve_target(raw_target: str, skill_content: str) -> str:
    """
    将 raw target 解析为文档锚点。
    优先用 anchor，其次用 normalized，最差保留原始。
    """
    if not raw_target:
        return ""
    info = _normalize_target(raw_target, skill_content)
    if info["anchor"]:
        return info["anchor"]
    if info["normalized"] and len(info["normalized"]) >= 3:
        return info["normalized"]
    return raw_target

# ── API 配置（优先读取 config.py，其次环境变量）──────────────────────────
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

# ── System Prompt ────────────────────────────────────────────────────────
SYSTEM_PROMPT = "You are an AI assistant that outputs JSON only. No markdown. No explanation. Pure JSON."

# Template for building user prompt — uses {t} for trajectory content (to avoid format conflicts)
_REFLECT_USER_PROMPT_TPL = """## Skill Document
```markdown
{skill}
```

## Trajectories
{t}

## Output
Respond with JSON only: {{"edits": [{{"op": "...", "content": "...", "target": "...", "reason": "...", "priority": "..."}}], "reasoning": "...", "summary": "..."}}"""

# ── Prompt 模板 ──────────────────────────────────────────────────────────
REFLECT_USER_PROMPT = """## Current Skill Document (SKILL.md)
```markdown
{skill_content}
```

## Rollout Trajectories
{trajectories_text}

## Your Analysis Task
Analyze the trajectories above and generate edit suggestions for the skill document.

{focus_instruction}

Return a valid JSON object only (no markdown code blocks, no extra text)."""


def _build_reflect_prompt(
    skill_content: str,
    rollouts: list[dict],
    fail_only: bool = False,
) -> str:
    """构建发送给 DeepSeek 的反思 prompt"""
    fail_count = sum(1 for r in rollouts if float(getattr(r, 'hard', 0)) < 1.0)
    success_count = len(rollouts) - fail_count

    lines = []
    for i, r in enumerate(rollouts, 1):
        hard = float(getattr(r, 'hard', 0))
        soft = float(getattr(r, 'soft', 0))
        fail_reason = getattr(r, 'fail_reason', "")
        task_type = getattr(r, 'task_type', 'unknown')
        task_desc = getattr(r, 'task_description', getattr(r, 'user_message', ''))
        feedback = getattr(r, 'feedback', "")
        user_msg = getattr(r, 'user_message', '')
        status = "SUCCESS" if hard >= 1.0 else "FAILURE"
        lines.append(
            f"Trajectory {i} [{status}] "
            f"type={task_type} hard={hard} soft={soft} "
            f"reason={fail_reason or 'none'} "
            f"feedback={feedback or 'none'}"
        )
    t = "\n".join(lines)

    if fail_only:
        focus = f"FAILURES ({fail_count} trajectories). Find root causes and propose fixes."
    else:
        focus = f"All trajectories: {fail_count} failures + {success_count} successes."

    return _REFLECT_USER_PROMPT_TPL.format(
        skill=_truncate_skill(skill_content),
        t=f"{focus}\n{t}",
    )


def _truncate_skill(skill: str, max_chars: int = 8000) -> str:
    """截断过长的 skill 内容以节省 token"""
    if len(skill) <= max_chars:
        return skill
    return skill[:max_chars] + "\n\n[... SKILL.md 内容已截断 ...]"


# ── DeepSeek API 调用 ───────────────────────────────────────────────────
def _call_deepseek(
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 2048,
) -> str:
    """调用 DeepSeek Chat API"""
    import urllib.request
    import urllib.error

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{DEEPSEEK_BASE_URL}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
            "Accept-Encoding": "identity",
        },
        method="POST",
    )
    # Use system proxy (respects Windows proxy settings / clash gateway)
    proxy_handler = urllib.request.ProxyHandler()
    opener = urllib.request.build_opener(proxy_handler)

    try:
        with opener.open(req, timeout=60) as resp:
            body = resp.read()
            # Handle gzip encoding if present
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip
                body = gzip.decompress(body)
            result = json.loads(body.decode("utf-8"))
            choice = result["choices"][0]["message"]
            # deepseek-v4-pro may use reasoning_content (CoT) instead of content
            content = choice.get("content") or choice.get("reasoning_content") or ""
            return content.strip()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepSeek API HTTP {e.code}: {error_body}")
    except Exception as e:
        raise RuntimeError(f"DeepSeek API call failed: {e}")


def _extract_json(text: str) -> Optional[dict]:
    """从 LLM 输出中提取 JSON，并规范化字段名"""
    # 尝试去掉 markdown 代码块
    text = re.sub(r"^```json\s*", "", text.strip())
    text = re.sub(r"^\s*```\s*$", "", text.strip(), flags=re.MULTILINE)

    # 尝试直接解析
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        pass
    else:
        return _normalize_result(result)

    # 尝试在文本中找 JSON 对象
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            result = json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
        else:
            return _normalize_result(result)

    return None


def _normalize_result(result: dict) -> dict:
    """规范化 LLM 返回的字段名，兼容不同 schema"""
    # 处理外层包装：{"raw_patch": {"edits": [...]}} 或 {"patch": {"edits": [...]}}
    for wrapper_key in ("raw_patch", "patch", "result", "analysis"):
        if wrapper_key in result and isinstance(result[wrapper_key], dict):
            inner = result[wrapper_key]
            if "edits" in inner:
                result = inner
                break

    # 兼容 LLM 返回的不同字段名
    if "edits" in result and isinstance(result["edits"], list):
        normalized_edits = []
        for edit in result["edits"]:
            if not isinstance(edit, dict):
                continue
            # 字段名映射
            op = edit.get("op") or edit.get("type") or "append"
            content = edit.get("content") or edit.get("instruction") or ""
            target = edit.get("target") or ""
            reason = edit.get("reason") or edit.get("title") or ""
            priority = edit.get("priority") or edit.get("priority_hint") or "medium"
            support_count = edit.get("support_count") or 1

            normalized_edits.append({
                "op": op,
                "content": content,
                "target": target,
                "reason": reason,
                "priority": priority,
                "support_count": support_count,
            })
        result = dict(result)
        result["edits"] = normalized_edits
    return result


# ── RawPatch 数据类 ─────────────────────────────────────────────────────
@dataclass
class RawPatch:
    """
    反思阶段输出的原始 patch。

    Attributes
    ----------
    edits : list[dict]
        每条编辑含 op/target/content/reason/priority/fail_count
    reasoning : str
        聚合推理说明
    summary : str
        反思摘要
    """
    edits: list[dict] = field(default_factory=list)
    reasoning: str = ""
    summary: str = ""

    def to_dict(self) -> dict:
        return {
            "edits": self.edits,
            "reasoning": self.reasoning,
            "summary": self.summary,
        }


# ── 核心反思函数 ─────────────────────────────────────────────────────────
def reflect(skill_content: str, rollouts: list[dict]) -> dict:
    """
    对失败轨迹进行错误分析，生成编辑建议。

    Parameters
    ----------
    skill_content : str
        当前 SKILL.md 内容
    rollouts : list[dict]
        RolloutResult 列表（dict 格式），每条含：
        id, task_type, task_description, hard, soft, fail_reason, feedback, user_message

    Returns
    -------
    dict
        RawPatch: {
            "edits": [...],   # 每条编辑含 op/target/content/reason/priority
            "reasoning": str, # 聚合推理说明
            "summary": str    # 反思摘要
        }

    Notes
    -----
    - 对 hard < 1.0 的轨迹：调用 LLM 进行错误分析，生成针对性 edit
    - 对 soft >= 0.5 的轨迹：调用 LLM 提取可推广的成功经验
    - 按 fail_count 降序排列 edits
    - 合并相同类型的 edits
    """
    if not rollouts:
        return {
            "edits": [],
            "reasoning": "No trajectories provided.",
            "summary": "无轨迹数据，跳过反思。"
        }

    # 分离失败和成功轨迹
    failures = [r for r in rollouts if float(getattr(r, 'hard', 0)) < 1.0]
    successes = [
        r for r in rollouts
        if float(getattr(r, 'hard', 0)) >= 1.0 and float(getattr(r, 'soft', 0)) >= 0.5
    ]

    all_edits: list[dict] = []
    reasonings: list[str] = []
    summaries: list[str] = []

    # ── 1. 错误分析师：对失败轨迹生成编辑建议 ─────────────────────────────
    if failures:
        try:
            result = _reflect_single(
                skill_content=skill_content,
                rollouts=failures,
                fail_only=True,
            )
            if result:
                all_edits.extend(result.get("edits", []))
                if result.get("reasoning"):
                    reasonings.append(f"[失败分析] {result['reasoning']}")
                if result.get("summary"):
                    summaries.append(result["summary"])
        except Exception as e:
            print(f"[skill_reflect] Failure analysis error: {e}", file=sys.stderr)

    # ── 2. 成功分析师：对成功轨迹提取保护性建议 ───────────────────────────
    if successes:
        try:
            result = _reflect_single(
                skill_content=skill_content,
                rollouts=successes,
                fail_only=False,
            )
            if result:
                # 成功轨迹的 edits 降级为 low priority
                for edit in result.get("edits", []):
                    edit["priority"] = "low"
                    all_edits.append(edit)
                if result.get("reasoning"):
                    reasonings.append(f"[成功分析] {result['reasoning']}")
                if result.get("summary"):
                    summaries.append(result["summary"])
        except Exception as e:
            print(f"[skill_reflect] Success analysis error: {e}", file=sys.stderr)

    # ── 3. 聚合：去重 + 按 priority 排序 ─────────────────────────────────
    aggregated_edits = _aggregate_edits(all_edits)

    # ── 4. Target 归一化（模糊匹配）───────────────────────────────────────
    # 对每个 edit 的 target 做归一化处理：
    # - 去掉 emoji
    # - 去掉 markdown 标记
    # - 在文档中搜索核心关键词，找到最近的章节标题作为锚点
    normalized_edits: list[dict] = []
    for edit in aggregated_edits:
        raw_target = edit.get("target", "")
        if raw_target:
            resolved = _resolve_target(raw_target, skill_content)
            edit = dict(edit)
            edit["original_target"] = raw_target  # 保留原始值
            edit["target"] = resolved
        normalized_edits.append(edit)
    aggregated_edits = normalized_edits

    # 按 priority 排序（high > medium > low），同优先级按 fail_count 降序
    priority_order = {"high": 0, "medium": 1, "low": 2}
    aggregated_edits.sort(
        key=lambda e: (
            priority_order.get(e.get("priority", "low"), 2),
            -(e.get("fail_count", 0))
        )
    )

    return {
        "edits": aggregated_edits,
        "reasoning": "\n\n".join(reasonings) if reasonings else "无推理说明",
        "summary": " | ".join(summaries) if summaries else "无摘要",
    }


def _reflect_single(
    skill_content: str,
    rollouts: list[dict],
    fail_only: bool = False,
) -> Optional[dict]:
    """调用 DeepSeek API 对一组轨迹进行单次反思分析"""
    user_prompt = _build_reflect_prompt(skill_content, rollouts, fail_only=fail_only)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    response_text = _call_deepseek(messages, temperature=0.3, max_tokens=2048)
    result = _extract_json(response_text)

    if not result:
        print(
            f"[skill_reflect] Failed to parse LLM response: {response_text[:200]}",
            file=sys.stderr,
        )
        return None

    return result


def _aggregate_edits(edits: list[dict]) -> list[dict]:
    """
    聚合编辑建议：
    1. 合并相同 target + op 的编辑（取更高 priority）
    2. 合并内容相似的编辑（编辑去重）
    3. 统计每条编辑的 fail_count（来自多少条失败轨迹支持）
    """
    if not edits:
        return []

    # 为每条编辑添加 fail_count（默认 1，兼容 support_count 字段名）
    for e in edits:
        e["fail_count"] = e.get("fail_count") or e.get("support_count") or 1

    # 按 target + op 分组去重
    seen: dict[str, dict] = {}
    for edit in edits:
        key = (edit.get("op", ""), edit.get("target", "")[:100])
        key_str = json.dumps(key, ensure_ascii=False)

        if key_str in seen:
            existing = seen[key_str]
            # 保留更高 priority
            p_order = {"high": 0, "medium": 1, "low": 2}
            old_p = p_order.get(existing.get("priority", "low"), 2)
            new_p = p_order.get(edit.get("priority", "low"), 2)
            if new_p < old_p:
                existing["priority"] = edit["priority"]
            # 累加 fail_count
            existing["fail_count"] = existing.get("fail_count", 1) + edit.get("fail_count", 1)
            # 内容更长则更新 content
            if len(edit.get("content", "")) > len(existing.get("content", "")):
                existing["content"] = edit["content"]
            # 合并 reason
            if edit.get("reason") and edit["reason"] not in (existing.get("reason") or ""):
                existing["reason"] = (existing.get("reason") or "") + " + " + edit["reason"]
        else:
            seen[key_str] = dict(edit)

    return list(seen.values())


# ── 便捷封装：单条轨迹反思 ───────────────────────────────────────────────
def reflect_single(skill_content: str, rollout: dict) -> dict:
    """
    对单条轨迹进行反思分析（便捷封装）。

    Parameters
    ----------
    skill_content : str
        当前 SKILL.md 内容
    rollout : dict
        单条 RolloutResult dict

    Returns
    -------
    dict
        RawPatch dict
    """
    return reflect(skill_content, [rollout])


# ── CLI 测试入口 ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="skill_reflect.py — Phase 3 反思生成模块")
    parser.add_argument(
        "--skill", "-s",
        default=str(Path(__file__).parent.parent / "SKILL.md"),
        help="SKILL.md 路径",
    )
    parser.add_argument(
        "--rollouts", "-r",
        default=str(
            Path(__file__).parent.parent.parent.parent.parent
            / "temp" / "trajectories_demo.json"
        ),
        help="轨迹 JSON 文件路径",
    )
    args = parser.parse_args()

    skill_content = Path(args.skill).read_text(encoding="utf-8")
    rollouts = json.loads(Path(args.rollouts).read_text(encoding="utf-8"))

    print(f"[skill_reflect] Loaded {len(rollouts)} trajectories")
    print(f"[skill_reflect] Calling DeepSeek API ...")

    result = reflect(skill_content, rollouts)

    print("\n" + "=" * 60)
    print("reflect() RESULT")
    print("=" * 60)

    print("\n--- edits 列表（每条含 op/target/content/reason）---")
    for i, edit in enumerate(result["edits"], 1):
        print(f"\n[Edit {i}]")
        print(f"  op:       {edit.get('op')}")
        print(f"  target:   {edit.get('target', '(无)')[:80]!r}")
        print(f"  content:  {edit.get('content', '(无)')[:120]!r}")
        print(f"  reason:   {edit.get('reason', '')}")
        print(f"  priority: {edit.get('priority')}")
        print(f"  fail_count: {edit.get('fail_count', 'N/A')}")

    print(f"\n--- aggregate 后的 edits 数量 ---")
    print(f"  聚合前原始 edits: {len(result.get('edits', []))} 条")
    agg = _aggregate_edits(result.get("edits", []))
    print(f"  聚合后 edits:    {len(agg)} 条")

    print(f"\n--- reasoning ---")
    print(result.get("reasoning", ""))

    print(f"\n--- summary ---")
    print(result.get("summary", ""))

    print(f"\n✅ DeepSeek API 调用正常完成")