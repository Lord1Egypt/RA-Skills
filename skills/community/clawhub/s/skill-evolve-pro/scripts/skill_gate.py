# -*- coding: utf-8 -*-
"""
skill-evolve-pro · Phase 5
skill_gate.py — 验证门控模块

三大验证维度：
1. Uniqueness Check   — 检查 edit target 是否在文档中唯一（防止模糊编辑）
2. Improvement Check  — 模拟执行失败轨迹，验证编辑是否真的改善问题
3. Safety Check      — 检查危险内容、保护区破坏、禁止操作

GateResult: { passed, decisions, reasoning, concerns }
    decisions: list of { index, action, reason }
        action = "accept" | "reject" | "revise"
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

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

# ── 常量 ────────────────────────────────────────────────────────────────
SLOW_UPDATE_START = "<!-- SLOW_UPDATE_START -->"
SLOW_UPDATE_END = "<!-- SLOW_UPDATE_END -->"

FORBIDDEN_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{16,}", re.I),
    re.compile(r"sk-[a-zA-Z0-9]{48,}", re.I),
    re.compile(r"(?i)bearer\s+[a-zA-Z0-9_\-]{20,}", re.I),
]

FORBIDDEN_DELETE_TOPICS = [
    "绝对禁止",
    "红线",
    "安全字段",
    "禁止修改",
]

# ── GateResult ──────────────────────────────────────────────────────────
@dataclass
class GateResult:
    """
    验证门控结果

    Attributes
    ----------
    passed : bool
        整体是否通过验证
    decisions : list[dict]
        每条编辑的决策: [{"index": 1, "action": "accept", "reason": "..."}]
        action ∈ {"accept", "reject", "revise"}
    reasoning : str
        整体验证推理说明
    concerns : list[str]
        潜在问题列表（warning，不直接导致拒绝）
    improvement_hints : str
        改进建议（供人工审查）
    """
    passed: bool = False
    decisions: list = field(default_factory=list)
    reasoning: str = ""
    concerns: list = field(default_factory=list)
    improvement_hints: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ── 维度1: Uniqueness Check ─────────────────────────────────────────────
def check_uniqueness(skill: str, edits: list) -> list[dict]:
    """
    检查每条 edit 的 target 是否在文档中唯一。

    Returns
    -------
    list[dict]
        每条编辑的唯一性结果:
        { "index": int, "action": "accept"|"reject"|"revise",
          "reason": str, "count": int }
    """
    results = []
    for i, edit in enumerate(edits, 1):
        op = edit.get("op", "")
        target = edit.get("target", "").strip()

        # 不需要 target 的操作天然通过唯一性检查
        if op in ("append",) or not target:
            results.append({
                "index": i,
                "action": "accept",
                "reason": "append 操作不需要 target，无需唯一性检查",
                "count": 1,
            })
            continue

        # 统计 target 在文档中出现的次数
        count = skill.count(target)
        if count == 0:
            results.append({
                "index": i,
                "action": "reject",
                "reason": f"target 在文档中未找到（count=0），无法执行 {op} 操作",
                "count": 0,
            })
        elif count == 1:
            results.append({
                "index": i,
                "action": "accept",
                "reason": f"target 在文档中唯一出现（count=1）",
                "count": 1,
            })
        else:
            # count > 1: 模糊编辑，自动改为 revise
            results.append({
                "index": i,
                "action": "revise",
                "reason": f"target 在文档中出现 {count} 次（不唯一），需要精确匹配",
                "count": count,
            })

    return results


# ── 维度2: Improvement Check ─────────────────────────────────────────────
def _call_deepseek_improvement(
    skill_before: str,
    skill_after: str,
    rollouts: list,
    edits: list,
) -> dict:
    """
    调用 DeepSeek 模拟执行失败轨迹，验证编辑是否真的改善问题。

    Returns
    -------
    dict
        { "verdict": "pass"|"fail", "reasoning": str, "concerns": list[str],
          "edit_verdicts": list[dict] }
    """
    # 构建失败轨迹描述
    trajectory_lines = []
    for i, r in enumerate(rollouts, 1):
        hard = float(r.get("hard", 0))
        soft = float(r.get("soft", 0))
        fail_reason = r.get("fail_reason", "")
        task_type = r.get("task_type", "unknown")
        status = "SUCCESS" if hard >= 1.0 else "FAILURE"
        trajectory_lines.append(
            f"Trajectory {i} [{status}] type={task_type} "
            f"hard={hard} soft={soft} fail_reason={fail_reason or 'none'}"
        )
    t = "\n".join(trajectory_lines)

    edits_desc = []
    for i, e in enumerate(edits, 1):
        edits_desc.append(
            f"[Edit{i}] op={e.get('op')} "
            f"target={e.get('target', '')[:80]!r} "
            f"content={e.get('content', '')[:120]!r}"
        )
    edits_text = "\n".join(edits_desc)

    system_prompt = (
        "You are a skill verification expert. Given a SKILL.md and failure trajectories, "
        "determine: "
        "1. If AI strictly follows SKILL.md, will it avoid this failure? "
        "2. Did the edits introduce new failure risks? "
        "Reply with JSON only. No markdown."
    )

    user_prompt = f"""## Skill Before Edit
```markdown
{skill_before[:6000]}
```

## Skill After Edit
```markdown
{skill_after[:6000]}
```

## Proposed Edits
{edits_text}

## Failure Trajectories
{t}

## Your Task
Analyze each edit against the failure trajectories:
1. For each edit, judge if it would prevent the identified failure
2. Check if any edit introduces new risks or contradictions
3. Determine overall whether the skill improved

Output JSON:
{{
  "verdict": "pass|fail",
  "reasoning": "overall analysis",
  "concerns": ["issue 1", "issue 2"],
  "edit_verdicts": [
    {{"index": 1, "verdict": "pass|fail", "reason": "..."}},
    ...
  ]
}}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2048,
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
    proxy_handler = urllib.request.ProxyHandler()
    opener = urllib.request.build_opener(proxy_handler)

    try:
        with opener.open(req, timeout=60) as resp:
            body = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip
                body = gzip.decompress(body)
            result = json.loads(body.decode("utf-8"))
            content = (
                result["choices"][0]["message"].get("content")
                or result["choices"][0]["message"].get("reasoning_content")
                or ""
            )
            return _extract_json(content) or {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepSeek API HTTP {e.code}: {error_body}")
    except Exception as e:
        raise RuntimeError(f"DeepSeek API call failed: {e}")


def _extract_json(text: str) -> Optional[dict]:
    """从 LLM 输出中提取 JSON"""
    text = re.sub(r"^```json\s*", "", text.strip())
    text = re.sub(r"^\s*```\s*$", "", text.strip(), flags=re.MULTILINE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return None


# ── 维度3: Safety Check ─────────────────────────────────────────────────
def check_safety(
    skill_before: str,
    skill_after: str,
    edits: list,
) -> list[dict]:
    """
    安全检查：禁止内容泄露、SLOW_UPDATE 保护区破坏、危险操作。

    Returns
    -------
    list[dict]
        每条编辑的安全检查结果:
        { "index": int, "action": "accept"|"reject",
          "reason": str, "safety_issues": list[str] }
    """
    results = []
    su_start_before = skill_before.find(SLOW_UPDATE_START)
    su_end_before = skill_before.find(SLOW_UPDATE_END)

    for i, edit in enumerate(edits, 1):
        op = edit.get("op", "")
        content = edit.get("content", "")
        target = edit.get("target", "")
        safety_issues: list[str] = []
        action = "accept"

        # 1. 禁止内容泄露检查
        if content:
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(content):
                    safety_issues.append("检测到疑似 API 密钥/密码泄露内容")
                    action = "reject"

        # 2. 检查 replace/delete 是否破坏了 SLOW_UPDATE 区域
        if op in ("replace", "delete") and target:
            if su_start_before != -1 and su_end_before != -1:
                target_idx = skill_before.find(target)
                if target_idx != -1 and su_start_before <= target_idx < su_end_before + len(SLOW_UPDATE_END):
                    safety_issues.append("target 落在 SLOW_UPDATE 保护区，replace/delete 被禁止")
                    action = "reject"

        # 3. 检查是否误删禁止相关段落（delete 操作）
        if op == "delete" and target:
            for forbidden_topic in FORBIDDEN_DELETE_TOPICS:
                if target.strip() and target.strip() in skill_before:
                    idx = skill_before.find(target)
                    context_window = skill_before[max(0, idx - 200):idx + len(target) + 200]
                    if forbidden_topic in context_window and len(target) < 50:
                        safety_issues.append(
                            f"删除内容可能涉及「{forbidden_topic}」相关规则，"
                            "存在破坏安全护栏的风险"
                        )
                        action = "reject"

        # 4. 检查 append 内容是否包含危险内容
        if op == "append" and content:
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(content):
                    safety_issues.append("append 内容包含疑似凭证泄露")
                    action = "reject"

        results.append({
            "index": i,
            "action": action,
            "reason": "; ".join(safety_issues) if safety_issues else "通过安全检查",
            "safety_issues": safety_issues,
        })

    return results


# ── 核心: gate_validate ─────────────────────────────────────────────────
def gate_validate(
    skill_before: str,
    skill_after: str,
    edits: list,
    rollouts: list,
) -> GateResult:
    """
    验证编辑后的技能是否真的改善了问题。

    三大验证维度：
    1. Uniqueness Check  — target 是否在文档中唯一
    2. Improvement Check  — 模拟执行失败轨迹，验证改善效果
    3. Safety Check       — 危险内容、保护区域

    Parameters
    ----------
    skill_before : str
        编辑前的 SKILL.md 内容
    skill_after : str
        编辑后的 SKILL.md 内容（由 apply_patch 生成）
    edits : list[dict]
        原始编辑列表，每条含 op/target/content/reason
    rollouts : list[dict]
        失败轨迹列表（用于 improvement check）

    Returns
    -------
    GateResult
        passed: bool
        decisions: list of { index, action, reason }
        reasoning: str
        concerns: list[str]
        improvement_hints: str
    """
    decisions: list[dict] = []
    concerns: list[str] = []

    # ── 维度1: Uniqueness Check ────────────────────────────────────────
    uniqueness_results = check_uniqueness(skill_before, edits)

    # ── 维度2: Improvement Check（调用 DeepSeek）────────────────────────
    improvement_result: Optional[dict] = None
    if rollouts:
        try:
            improvement_result = _call_deepseek_improvement(
                skill_before, skill_after, rollouts, edits
            )
        except Exception as e:
            concerns.append(f"DeepSeek improvement check 调用失败: {e}，采用保守策略（部分拒绝）")
            improvement_result = None
    else:
        concerns.append("无失败轨迹（rollouts 为空），跳过 improvement check")

    # ── 维度3: Safety Check ───────────────────────────────────────────
    safety_results = check_safety(skill_before, skill_after, edits)

    # ── 综合决策 ───────────────────────────────────────────────────────
    for i, edit in enumerate(edits, 1):
        uniqueness = uniqueness_results[i - 1]
        safety = safety_results[i - 1]

        # 从 improvement_result 获取该编辑的 verdict
        edit_verdict = "unknown"
        improvement_reason = ""
        if improvement_result and improvement_result.get("edit_verdicts"):
            for ev in improvement_result["edit_verdicts"]:
                if ev.get("index") == i:
                    edit_verdict = ev.get("verdict", "unknown")
                    improvement_reason = ev.get("reason", "")
                    break

        # 三维度综合裁定
        # 优先级: reject > revise > accept
        reject_reasons = []
        if uniqueness["action"] == "reject":
            reject_reasons.append(f"[Uniqueness] {uniqueness['reason']}")
        if safety["action"] == "reject":
            reject_reasons.append(f"[Safety] {safety['reason']}")
        if improvement_result and edit_verdict == "fail":
            reject_reasons.append(f"[Improvement] {improvement_reason}")

        if reject_reasons:
            action = "reject"
            reason = " | ".join(reject_reasons)
        elif uniqueness["action"] == "revise":
            action = "revise"
            reason = (
                f"[Uniqueness] {uniqueness['reason']}。"
                f"| [Safety] {safety['reason']}"
                + (f"| [Improvement] {improvement_reason}" if improvement_reason else "")
            )
        else:
            action = "accept"
            reason = (
                f"[Uniqueness] {uniqueness['reason']}"
                f" | [Safety] {safety['reason']}"
                + (f" | [Improvement] {improvement_reason}" if improvement_reason else "")
            )

        decisions.append({
            "index": i,
            "action": action,
            "reason": reason,
            "op": edit.get("op", ""),
            "target": edit.get("target", "")[:80],
            "uniqueness_count": uniqueness.get("count", 1),
            "edit_verdict": edit_verdict,
            "safety_issues": safety.get("safety_issues", []),
        })

    # ── 整体裁定 ───────────────────────────────────────────────────────
    rejected = [d for d in decisions if d["action"] == "reject"]
    revised = [d for d in decisions if d["action"] == "revise"]
    accepted = [d for d in decisions if d["action"] == "accept"]

    if rejected:
        passed = False
        reasoning = (
            f"Gate 检查未通过：{len(rejected)} 条编辑被拒绝，"
            f"{len(revised)} 条需修订，{len(accepted)} 条通过。"
        )
        if improvement_result:
            reasoning += f" DeepSeek verdict={improvement_result.get('verdict', 'unknown')}"
            if improvement_result.get("concerns"):
                concerns.extend(improvement_result["concerns"])
        if improvement_result and improvement_result.get("reasoning"):
            reasoning += f" 分析：{improvement_result['reasoning'][:300]}"
    elif revised:
        passed = True  # 有 revise 但无 reject，整体通过但需关注
        reasoning = (
            f"Gate 检查通过（但需修订）：{len(revised)} 条编辑需要精确化，"
            f"{len(accepted)} 条直接通过。"
        )
        if improvement_result:
            reasoning += f" DeepSeek verdict={improvement_result.get('verdict', 'unknown')}"
    else:
        passed = True
        reasoning = (
            f"Gate 检查完全通过：{len(accepted)}/{len(decisions)} 条编辑全部验证通过。"
        )
        if improvement_result:
            reasoning += f" DeepSeek verdict={improvement_result.get('verdict', 'unknown')}"
            if improvement_result.get("reasoning"):
                reasoning += f" 分析：{improvement_result['reasoning'][:200]}"

    # 收集 improvement_hints
    improvement_hints = ""
    if improvement_result and improvement_result.get("concerns"):
        improvement_hints = "; ".join(improvement_result["concerns"])

    return GateResult(
        passed=passed,
        decisions=decisions,
        reasoning=reasoning,
        concerns=concerns,
        improvement_hints=improvement_hints,
    )


# ── CLI 测试入口 ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="skill_gate.py — Phase 5 验证门控模块")
    parser.add_argument("--skill", "-s", default=None, help="SKILL.md 路径")
    parser.add_argument("--edits", "-e", default=None, help="edits JSON 路径")
    parser.add_argument("--rollouts", "-r", default=None, help="rollouts JSON 路径")
    args = parser.parse_args()

    # Load SKILL.md
    if args.skill:
        skill_path = Path(args.skill)
    else:
        try:
            from config import DEFAULT_TARGET_SKILL_DIR
            skill_path = DEFAULT_TARGET_SKILL_DIR / "SKILL.md"
        except ImportError:
            import os
            WORKSPACE = Path(os.environ.get(
                "OPENCLAW_WORKSPACE",
                os.path.join(os.path.expanduser("~"), ".jvs", "workspace")
            ))
            skill_path = WORKSPACE / "skills" / "robot-evolve" / "SKILL.md"
    skill_before = skill_path.read_text(encoding="utf-8")
    print(f"[skill_gate] Read SKILL.md: {skill_path} ({len(skill_before)} chars)")

    # Load edits (Phase 4 的 4 条 edits)
    if args.edits:
        edits_path = Path(args.edits)
        data = json.loads(edits_path.read_text(encoding="utf-8"))
        edits = data if isinstance(data, list) else data.get("edits", [])
    else:
        edits = [
            {
                "op": "replace",
                "target": "1. **MMX命令规范**：任何搜索必须使用 `npx mmx search` 命令，路径格式为 `npx mmx search query --q \"关键词\"`，严禁使用其他替代命令或绕路格式。",
                "content": "1. **MMX命令规范**：任何搜索必须使用 `npx mmx search` 命令，路径格式为 `npx mmx search query --q \"关键词\"`，严禁使用其他替代命令或绕路格式。\n\n2. **搜索沉心模式**：遇到错误或决断问题时，至少进行 3 次搜索内容检查，再给出回答。\n\n3. **产品参数核实**：涉及硬件规格、芯片型号等信息时，必须调用搜索获取最新官方网站数据或权威评测，禁止凭模型内部知识直接作答。",
                "reason": "Add search depth rule and product parameter verification rule",
                "priority": "high",
                "fail_count": 2,
            },
            {
                "op": "append",
                "target": "",
                "content": "\n\n---\n\n## 进化记录\n\n| 日期 | round | 轨迹统计 | 应用编辑数 | Gate通过 |\n|------|-------|---------|-----------|---------|\n| - | - | total=0 hard_success=0 hard_fail=0 | - | - |\n\n进化记录由 `skill-evolve-pro` Phase 6 自动维护。",
                "reason": "Add evolution record table for tracking history",
                "priority": "medium",
                "fail_count": 1,
            },
            {
                "op": "replace",
                "target": "1. **禁止修改安全字段**：`gateway.bind`、`gateway.auth`、`tailscale.expose`",
                "content": "1. **禁止修改安全字段**：`gateway.bind`、`gateway.auth`、`tailscale.expose`、`agent.model`",
                "reason": "Add agent.model to forbidden modification list",
                "priority": "medium",
                "fail_count": 1,
            },
            {
                "op": "insert_after",
                "target": "### L0 级别（无需告知）",
                "content": "#### L0 自我检查清单\n- [ ] 工作区文件完整（SOUL.md、AGENTS.md、MEMORY.md 存在）\n- [ ] `memory/` 目录可写\n- [ ] 无异常长度的会话状态文件",
                "reason": "Add L0 self-check checklist before executing L0 actions",
                "priority": "low",
                "fail_count": 0,
            },
        ]

    print(f"[skill_gate] Loaded {len(edits)} edits")

    # Load rollouts
    if args.rollouts:
        rollouts_path = Path(args.rollouts)
        rollouts = json.loads(rollouts_path.read_text(encoding="utf-8"))
    else:
        rollouts = [
            {
                "id": "session_001",
                "hard": 0,
                "soft": 0.3,
                "fail_reason": "搜索结果幻觉，未核实产品参数",
                "task_type": "search",
                "task_description": "用户询问某产品参数，AI 凭内部知识作答但错误",
            },
            {
                "id": "session_002",
                "hard": 0,
                "soft": 0.5,
                "fail_reason": "MMX 命令格式错误导致搜索失败",
                "task_type": "search",
                "task_description": "用户要求搜索信息，AI 用错误命令格式",
            },
        ]

    print(f"[skill_gate] Loaded {len(rollouts)} rollouts")

    # Apply edits to get skill_after
    from skill_apply import apply_all_edits
    skill_after, edit_reports = apply_all_edits(skill_before, edits)
    print(f"[skill_gate] Applied {len(edit_reports)} edits, skill_after length: {len(skill_after)}")

    # Run gate validation
    print(f"\n{'='*70}")
    print("gate_validate() — Phase 5 Gate Results")
    print(f"{'='*70}")

    gate_result = gate_validate(skill_before, skill_after, edits, rollouts)

    # Print per-edit decisions
    print(f"\n### Per-Edit Decisions (passed={gate_result.passed})")
    print(f"{'-'*70}")
    for d in gate_result.decisions:
        tag = {"accept": "[OK]", "reject": "[NO]", "revise": "[WARN]"}.get(d["action"], "[?]")
        uniqueness_info = f"(count={d.get('uniqueness_count', 1)})"
        print(f"  [{d['index']}] {tag} {d['action'].upper():8s} {uniqueness_info}")
        print(f"       op={d['op']:15s}  target={d.get('target', '(none)')[:50]!r}")
        print(f"       reason: {d['reason'][:120]}")
        if d.get("safety_issues"):
            print(f"       safety_issues: {d['safety_issues']}")
        if d.get("edit_verdict") != "unknown":
            print(f"       improvement_verdict: {d['edit_verdict']}")

    # Print overall result
    print(f"\n### Overall Result")
    print(f"{'-'*70}")
    status_tag = "[PASSED]" if gate_result.passed else "[FAILED]"
    print(f"  Gate: {status_tag}")
    print(f"  Reasoning: {gate_result.reasoning[:300]}")
    if gate_result.concerns:
        print(f"  Concerns ({len(gate_result.concerns)}):")
        for c in gate_result.concerns:
            print(f"    - {c}")
    if gate_result.improvement_hints:
        print(f"  Improvement Hints: {gate_result.improvement_hints}")

    # Summary
    accepted = [d for d in gate_result.decisions if d["action"] == "accept"]
    rejected = [d for d in gate_result.decisions if d["action"] == "reject"]
    revised = [d for d in gate_result.decisions if d["action"] == "revise"]
    print(f"\n  Summary: {len(accepted)} accept | {len(revised)} revise | {len(rejected)} reject")

    print(f"\n{'='*70}")
    print("[DONE] skill_gate.py test complete")
