# -*- coding: utf-8 -*-
"""
skill-evolve-pro · Phase 7
slow_update.py — 跨 epoch 慢更新模块

核心功能：
- 在 epoch 边界（round 归零时）触发
- 对比当前 epoch 与上一 epoch 的 trajectory_stats 变化
- 分析 edit_history 中哪些编辑持续有效/无效
- 调用 DeepSeek 生成长期 guidance
- 写入 SLOW_UPDATE 保护区（受保护的长期指导区域）

Protected Region 标记：
  <!-- SLOW_UPDATE_START --> ... <!-- SLOW_UPDATE_END -->

触发条件：
- epoch 完成时（round 归零新一轮开始）
- 或手动调用 slow_update()
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ── 路径配置 ─────────────────────────────────────────────────────────────
# 指向 scripts 父目录（即 skill-evolve-pro 根目录）
SELF_DIR = Path(__file__).parent
SKILL_DIR = SELF_DIR.parent
SKILL_MD = SKILL_DIR / "SKILL.md"

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

# ── Protected Region 标记 ────────────────────────────────────────────────
SLOW_UPDATE_START = "<!-- SLOW_UPDATE_START -->"
SLOW_UPDATE_END = "<!-- SLOW_UPDATE_END -->"

# ── System Prompt ────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are an AI assistant that outputs JSON only. No markdown. No explanation. Pure JSON."
)

# ── Slow Update Prompt ────────────────────────────────────────────────────
SLOW_UPDATE_USER_PROMPT = """## Current Skill Document (SKILL.md)
```markdown
{skill_content}
```

## Previous Slow Update Guidance
{prev_slow_update}

## Evolution History (all epochs)
- Current epoch: {epoch}
- Round: {round}
- Trajectory Stats (cumulative):
  {trajectory_stats}

## Edit History (last 5 rounds)
{edit_history}

## Your Analysis Task
Analyze the evolution history above and generate long-term guidance for the skill.

Consider:
1. Trends in hard_success / hard_fail across rounds (improving or degrading?)
2. Which edit patterns (if any) consistently pass the gate and help
3. Which edit patterns are repeatedly rejected or cause regressions
4. Persistent failure modes — same problem happening across multiple rounds
5. What principles should be preserved as long-term guidance

Return a valid JSON object only (no markdown code blocks, no extra text):

{{"reasoning": "分析推理过程", "slow_content": "新的长期 guidance 内容（Markdown 格式）"}}"""


# ── State 加载（本地 import，避免循环依赖）────────────────────────────────
def _load_state_data(skill_id: str) -> Optional[dict]:
    """直接从 JSON 文件加载状态，绕过模块导入"""
    state_file = SKILL_DIR / "state" / f"{skill_id}.json"
    if not state_file.exists():
        return None
    return json.loads(state_file.read_text(encoding="utf-8"))


# ── API 调用 ─────────────────────────────────────────────────────────────
def _call_deepseek(system: str, user: str, max_tokens: int = 4096) -> str:
    """调用 DeepSeek Chat API"""
    import urllib.request
    import urllib.error

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }

    req = urllib.request.Request(
        DEEPSEEK_BASE_URL + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            if attempt < 2:
                continue
            raise RuntimeError(f"DeepSeek API call failed after 3 retries: {e}")


def _extract_json(text: str) -> Optional[dict]:
    """从 LLM 输出中提取 JSON"""
    # Try direct parse first
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    # Try to find JSON in code block
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    # Try to find raw JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0).strip())
        except json.JSONDecodeError:
            pass
    return None


# ── SLOW_UPDATE 保护区管理 ───────────────────────────────────────────────

def inject_slow_guidance(skill_content: str, guidance: str) -> str:
    """
    将 guidance 注入到 SLOW_UPDATE_START/END 保护区。
    如果保护区已存在则替换内容；否则追加到文档末尾。
    """
    # 先移除旧的保护区（确保只有一个）
    skill = _strip_slow_guidance(skill_content)

    block = (
        f"\n\n{SLOW_UPDATE_START}\n"
        f"{guidance.strip()}\n"
        f"{SLOW_UPDATE_END}\n"
    )
    return skill.rstrip() + block


def extract_slow_guidance(skill_content: str) -> str:
    """
    从技能文档中提取当前的 SLOW_UPDATE guidance。
    如果没有保护区，返回空字符串。
    """
    start = skill_content.find(SLOW_UPDATE_START)
    end = skill_content.find(SLOW_UPDATE_END)
    if start == -1 or end == -1:
        return ""
    inner_start = start + len(SLOW_UPDATE_START)
    return skill_content[inner_start:end].strip()


def _strip_slow_guidance(skill: str) -> str:
    """移除所有 SLOW_UPDATE 保护区（包括内容）"""
    while True:
        start = skill.find(SLOW_UPDATE_START)
        if start == -1:
            break
        end = skill.find(SLOW_UPDATE_END, start)
        if end == -1:
            # 孤立的开始标记，移除它
            skill = skill[:start] + skill[start + len(SLOW_UPDATE_START):]
            break
        skill = skill[:start] + skill[end + len(SLOW_UPDATE_END):]
    # 清理残留的结束标记
    skill = skill.replace(SLOW_UPDATE_END, "")
    # 折叠多余空行
    while "\n\n\n" in skill:
        skill = skill.replace("\n\n\n", "\n\n")
    return skill.rstrip()


def has_slow_guidance(skill_content: str) -> bool:
    """检查技能文档是否已有 SLOW_UPDATE 保护区"""
    return SLOW_UPDATE_START in skill_content and SLOW_UPDATE_END in skill_content


# ── 核心功能 ─────────────────────────────────────────────────────────────

def slow_update(skill_id: str, current_skill: str) -> dict:
    """
    跨 epoch 分析，生成长期 guidance。

    对比上一 epoch vs 当前 epoch 的：
    - trajectory_stats 变化（hard_success/hard_fail 趋势）
    - edit_history（哪些编辑持续有效/无效）
    - 持续失败的模式

    参数：
        skill_id: 技能标识符（如 "robot-evolve"）
        current_skill: 当前 SKILL.md 的完整内容

    返回：
        {
            "reasoning": str,       # DeepSeek 的分析推理
            "slow_content": str,   # 要写入 SLOW_UPDATE 保护区的新 guidance
            "epoch": int            # 当前 epoch 编号
        }
    """
    # 1. 加载状态
    state_data = _load_state_data(skill_id)
    if state_data is None:
        return {
            "reasoning": "状态文件不存在，无法执行 slow_update",
            "slow_content": "",
            "epoch": 1,
        }

    epoch = state_data.get("epoch", 1)
    round_num = state_data.get("round", 0)
    stats = state_data.get("trajectory_stats", {})
    edit_history = state_data.get("edit_history", [])

    # 2. 提取上一轮的 SLOW_UPDATE guidance
    prev_slow_update = extract_slow_guidance(current_skill)
    if prev_slow_update:
        prev_slow_text = prev_slow_update
    else:
        prev_slow_text = "(暂无 — 这是首次 slow_update)"

    # 3. 构建 trajectory_stats 文本
    total = stats.get("total", 0)
    hard_success = stats.get("hard_success", 0)
    hard_fail = stats.get("hard_fail", 0)
    soft_fail = stats.get("soft_fail", 0)
    success_rate = (hard_success / total * 100) if total > 0 else 0

    trajectory_stats_text = (
        f"  - total: {total}\n"
        f"  - hard_success: {hard_success}\n"
        f"  - hard_fail: {hard_fail}\n"
        f"  - soft_fail: {soft_fail}\n"
        f"  - success_rate: {success_rate:.1f}%"
    )

    # 4. 构建 edit_history 文本（最近 5 轮）
    edit_history_lines = []
    for entry in edit_history[-5:]:
        applied = entry.get("applied", 0)
        rejected = entry.get("rejected", 0)
        gate = entry.get("gate_passed", None)
        gate_str = "PASS" if gate else ("FAIL" if gate is False else "N/A")
        edit_history_lines.append(
            f"- Round {entry.get('round', '?')}: "
            f"applied={applied}, rejected={rejected}, gate={gate_str}"
        )

    if not edit_history_lines:
        edit_history_text = "(暂无编辑历史)"
    else:
        edit_history_text = "\n".join(edit_history_lines)

    # 5. 填充 prompt
    user_prompt = SLOW_UPDATE_USER_PROMPT.format(
        skill_content=current_skill[:6000],
        prev_slow_update=prev_slow_text,
        epoch=epoch,
        round=round_num,
        trajectory_stats=trajectory_stats_text,
        edit_history=edit_history_text,
    )

    # 6. 调用 DeepSeek
    try:
        raw_response = _call_deepseek(
            system=SYSTEM_PROMPT,
            user=user_prompt,
            max_tokens=4096,
        )
        parsed = _extract_json(raw_response)
        if parsed and parsed.get("slow_content"):
            reasoning = parsed.get("reasoning", "")
            slow_content = parsed["slow_content"]
        else:
            reasoning = "LLM 返回格式异常，未能解析 slow_content"
            slow_content = ""
    except Exception as e:
        reasoning = f"DeepSeek API 调用失败: {e}"
        slow_content = ""

    return {
        "reasoning": reasoning,
        "slow_content": slow_content,
        "epoch": epoch,
    }


def run_slow_update_and_inject(skill_id: str, skill_content: str) -> tuple[str, dict]:
    """
    执行完整的 slow_update 流程：
    1. 生成新的长期 guidance
    2. 注入到 SLOW_UPDATE 保护区
    3. 返回更新后的 SKILL.md 内容 + 分析结果

    返回：(new_skill_content, analysis_result)
    """
    result = slow_update(skill_id, skill_content)

    if result["slow_content"]:
        new_skill = inject_slow_guidance(skill_content, result["slow_content"])
    else:
        new_skill = skill_content

    return new_skill, result


# ── CLI 测试入口 ─────────────────────────────────────────────────────────
def main():
    """手动触发 slow_update 测试"""
    # 修复 Windows GBK 编码问题
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if len(sys.argv) < 2:
        skill_id = "robot-evolve"
    else:
        skill_id = sys.argv[1]

    print(f"[slow_update] skill_id={skill_id}")
    print(f"[slow_update] 读取 SKILL.md: {SKILL_MD}")

    if not SKILL_MD.exists():
        print(f"[slow_update] ERROR: SKILL.md not found: {SKILL_MD}")
        sys.exit(1)

    skill_content = SKILL_MD.read_text(encoding="utf-8")

    # 执行 slow_update
    print("[slow_update] Calling DeepSeek to generate guidance...")
    new_skill, result = run_slow_update_and_inject(skill_id, skill_content)

    print(f"\n{'='*60}")
    print(f"Epoch: {result['epoch']}")
    print(f"Reasoning:\n{result['reasoning']}")
    print(f"\nGenerated guidance:\n{result['slow_content']}")
    print(f"{'='*60}")

    # 始终写回 SKILL.md（包含新注入的 guidance）
    SKILL_MD.write_text(new_skill, encoding="utf-8")
    print(f"\n[OK] SKILL.md has been updated")

    # 验证注入
    extracted = extract_slow_guidance(new_skill)
    if extracted:
        print(f"[OK] SLOW_UPDATE region injected successfully")
        print(f"     Region content length: {len(extracted)} chars")
    else:
        print(f"[WARN] SLOW_UPDATE region is empty")


if __name__ == "__main__":
    main()
