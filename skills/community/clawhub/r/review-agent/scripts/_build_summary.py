#!/usr/bin/env python3
"""Build summary.md (decision-ready 6-section brief, LLM-synthesized) +
summary_audit.md (raw pillar-grouped audit trail) from a closed session.

summary.md is what the Responder actually reads.
summary_audit.md is the full backing data for anyone who wants to dig in.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path


PILLARS = ["Background", "Materials", "Framework", "Intent"]
AXIS_TO_PILLAR = {
    "BLUF": "Intent",
    "Decision Readiness": "Intent",
    "Completeness": "Framework",
    "Assumptions": "Materials",
    "Evidence": "Materials",
    "Red Team": "Materials",
    "Stakeholder": "Materials",
}
PILLAR_LABELS = {
    "Background": "背景 (Background)",
    "Materials":  "资料 (Materials)",
    "Framework":  "框架 (Framework)",
    "Intent":     "意图 (Intent / CSW Gate)",
}
SKILL_DIR = Path(__file__).parent.parent


def pillar_of(a):
    if a.get("pillar") in PILLARS:
        return a["pillar"]
    return AXIS_TO_PILLAR.get(a.get("axis", ""), "Materials")


def load_jsonl(path):
    if not os.path.exists(path): return []
    out = []
    for line in open(path):
        line = line.strip()
        if not line: continue
        try: out.append(json.loads(line))
        except json.JSONDecodeError: pass
    return out


def group_by_pillar(items):
    g = {p: [] for p in PILLARS}
    for a in items:
        g[pillar_of(a)].append(a)
    return g


# ─────────────────────────────────────────────────────────────
# Audit-trail summary (legacy 4-pillar grouped)
# ─────────────────────────────────────────────────────────────

def build_audit_summary(sd: Path) -> str:
    meta = json.load(open(sd / "meta.json"))
    ann = load_jsonl(sd / "annotations.jsonl")

    accepted = [a for a in ann if a.get("status") == "accepted"]
    modified = [a for a in ann if a.get("status") == "modified"]
    rejected = [a for a in ann if a.get("status") == "rejected"]
    unresolvable = [a for a in ann if a.get("status") == "unresolvable"]
    still_open = [a for a in ann if a.get("status") == "open"]

    per_pillar_verdict = {}
    for p in PILLARS:
        items = [a for a in ann if pillar_of(a) == p]
        if not items:
            per_pillar_verdict[p] = "pass (no findings)"
        elif any(a.get("status") == "open" and a.get("severity") == "BLOCKER" for a in items):
            per_pillar_verdict[p] = "fail"
        elif any(a.get("status") == "unresolvable" for a in items):
            per_pillar_verdict[p] = "unresolvable"
        else:
            per_pillar_verdict[p] = "pass"

    final_dir = sd / "final"
    final_files = sorted([f.name for f in final_dir.iterdir() if f.is_file()]) if final_dir.exists() else []

    lines = [f"# Audit Trail — {meta.get('subject','')}", ""]
    lines.append(f"**Session**: `{meta['session_id']}`  ")
    lines.append(f"**Termination**: {meta.get('termination','?')}" +
                 (f" (reason: {meta.get('forced_reason','')})" if meta.get("forced_reason") else "") + "  ")
    lines.append(f"**Rounds**: {meta.get('round', 0)}")
    lines.append("")

    lines.append("## 四柱状态")
    lines.append("| 柱 | 状态 | 详情 |")
    lines.append("|---|---|---|")
    for p in PILLARS:
        status = per_pillar_verdict[p]
        items_here = [a for a in ann if pillar_of(a) == p]
        n_open = sum(1 for a in items_here if a.get("status") == "open")
        n_ok = sum(1 for a in items_here if a.get("status") in ("accepted","modified"))
        n_rej = sum(1 for a in items_here if a.get("status") == "rejected")
        lines.append(f"| **{PILLAR_LABELS[p]}** | **{status}** | "
                     f"{len(items_here)} findings · {n_ok} close · {n_open} open · {n_rej} dissent |")
    lines.append("")

    lines.append(f"## 最终材料"); lines.append("")
    if final_files:
        for fn in final_files: lines.append(f"- `final/{fn}`")
    else:
        lines.append("_(无)_")
    lines.append("")

    # Accepted
    lines.append(f"## 已接受 ({len(accepted)})"); lines.append("")
    for p in PILLARS:
        ps = [a for a in accepted if pillar_of(a) == p]
        if ps:
            lines.append(f"### {PILLAR_LABELS[p]}")
            for a in ps:
                src = " _(from simulation)_" if a.get("source") == "responder_simulation" else ""
                lines.append(f"- [{a.get('severity','?')}] {a.get('issue','')}{src}")
                lines.append(f"  → {a.get('suggest','')}")
            lines.append("")

    # Modified
    if modified:
        lines.append(f"## 被 Requester 改成其他版本 ({len(modified)})"); lines.append("")
        for a in modified:
            lines.append(f"- [{pillar_of(a)}] {a.get('issue','')}")
            lines.append(f"  - reviewer: _{a.get('suggest','')}_")
            lines.append(f"  - requester: _{a.get('reply','')}_")
        lines.append("")

    # Dissent
    if rejected:
        lines.append(f"## 保留异议 ({len(rejected)})"); lines.append("")
        for p in PILLARS:
            ps = [a for a in rejected if pillar_of(a) == p]
            if ps:
                lines.append(f"### {PILLAR_LABELS[p]}")
                for a in ps:
                    lines.append(f"- {a.get('issue','')}")
                    lines.append(f"  - reviewer 建议: _{a.get('suggest','')}_")
                    lines.append(f"  - requester 理由: _{a.get('reply','')}_")
                lines.append("")

    # Unresolvable
    if unresolvable:
        lines.append(f"## 未闭合（进入讨论）({len(unresolvable)})"); lines.append("")
        for a in unresolvable:
            lines.append(f"- **{a.get('issue','')}**")
            reason = a.get("unresolvable_reason", a.get("reply",""))
            if reason: lines.append(f"  - 未闭合原因: {reason}")
        lines.append("")

    # Simulation questions
    sim = [a for a in ann if a.get("source") == "responder_simulation"]
    if sim:
        lines.append(f"## Responder 模拟追问 ({len(sim)})"); lines.append("")
        for a in sorted(sim, key=lambda x: x.get("priority", 99)):
            lines.append(f"- **[{pillar_of(a)}]** {a.get('simulated_question', a.get('issue',''))}")
            lines.append(f"  - 状态: {a.get('status','open')}" +
                        (f" — {a.get('reply','')}" if a.get("reply") else ""))
        lines.append("")

    if still_open:
        lines.append(f"## ⚠ 关闭时仍未解决 ({len(still_open)})"); lines.append("")
        for a in still_open:
            lines.append(f"- [{pillar_of(a)}/{a.get('severity','?')}] {a.get('issue','')}")
        lines.append("")

    lines.append("---")
    lines.append(f"_Generated at {datetime.now().astimezone().isoformat(timespec='seconds')}_")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Decision-ready brief (LLM-synthesized, what Responder actually reads)
# ─────────────────────────────────────────────────────────────

BRIEF_SYNTHESIS_STAGE_BLOCK = """**你现在在流程的最后一步：SUMMARY SYNTHESIS（生成给 {responder_name} 的会前简报）。**

你的产出是一份**决策-ready 的预读文档**。{responder_name} 读完这份文档（≤ 5 分钟）就能进入会议做决定，不需要再翻原材料。

保持"**挑刺者**"的视角——不软化 dissent，不隐藏 open items，不美化响应质量。

### 必需的六节结构（严格按此输出）

```
# 会前简报 — <subject>

_Requester: <name>（<open_id>) · Rounds: N · 产出时间: <timestamp>_

## 1. 议题摘要

**一句话**：<20-40 字，概括核心讨论内容>

**三行背景**：
- <why now / 为什么现在提>
- <what's at stake / 关键的利害>
- <where it stands / 当前状态>

## 2. 核心数据

<从材料中提取的关键数字，高亮形式。有来源的标来源+日期；无来源的**明确标注"未给出来源"**作为风险信号>

例如：
- **DAU**: 12K (2026-03 内部统计) → 较 2026-01 增长 40%
- **月运营成本**: $2.5K (Stripe 账单，2026-04) _<未给出预估_>
- **竞品对标**: Exa.ai 定价 $0.005/query (官网, 未验证)

## 3. 团队自检结果

共 N 条 findings 被挑战。Requester 响应：

| 类型 | 数量 | 简述 |
|---|---|---|
| 接受并修改 | X | <2-3 个最关键的简述> |
| 保留异议 | Y | <列出异议点，标注 reviewer 和 requester 各自的立场> |
| 无解 | Z | <哪些进入会议讨论> |

**Agent 对响应质量的判断**：<强 / 中 / 弱 / 对抗性>——<具体理由，例如"结构性 BLOCKER 全部接受但数据性问题被软性规避">

## 4. 待决策事项

**主 ask**：<一句话，{responder_name} 被要求做什么具体决定>

**需要讨论才能定的开放项**（从 unresolvable + dissent 合成，≤3 条，每条带判断框架）：
1. <事项> — 若倾向 A 则 ..., 若倾向 B 则 ...
2. ...

## 5. 建议时间分配

| 议题 | 建议时长 | 原因 |
|---|---|---|
| 核心 ask 拍板 | N 分钟 | <简述为何够/不够> |
| 开放项 1 | N 分钟 | <> |
| ... | | |

**总会议时长**：X 分钟（Requester 的原请求时长 + agent 建议调整）

## 6. 风险提示（Agent 认为团队可能遗漏或低估的点）

从六维度挑战 + Responder 模拟里 agent 认为**即使这次 review 后仍没被充分处理**的点。≤3 条：

- **<维度（如：逻辑自洽性/风险评估/...）>**：<具体盲点>。Agent 建议你开会时追问：<Socratic 追问>
- ...

## 7. 未深入讨论的 finding（按 Requester scope 选择留到这里的）

<如果 annotations 里有 `status: "deferred_by_scope"` 的条目，列出来，带 pillar + 一句话 issue。让 Responder 看到除了本次 review 覆盖的范围外，agent 还挑出了 N 条问题但 Requester 选择不展开。Responder 如果觉得需要深入，可以回 bot 触发追问（见下）。>

## Responder 的追问入口

如果你觉得当前 brief 还可以再挖一挖（例如深入第 7 节的那些未讨论 finding），在 Lark DM 里回本消息：

- `more` · 让 agent 再追问 Requester 一轮（默认再覆盖 3 条未讨论的）
- `more N` · 具体指定再多少条（如 `more 5`）
- `deepen <finding-id>` · 针对某一条具体深挖（如 `deepen p7`）

没有追问需求就直接用这份 brief 开会。

---

_Full audit trail: `summary_audit.md` · Dissent log: `dissent.md` · 完整对话: `conversation.jsonl` · 定稿材料: `final/`_
```

### 写作纪律

- **不空洞**：每节都具体到数字 / 名字 / 片段。禁用"一些/很多/不错"这类模糊词
- **不软化 dissent**：第 3 节的 dissent 必须让 {responder_name} 看到 requester 的真实立场和理由，不包装
- **不隐藏风险**：第 6 节必须真的挑刺——如果 review 过程中某些点被轻易放过，这里要指出
- **时间分配基于实际复杂度**：dissent 多 / 数据缺得厉害 / open items 多 → 建议更多时间；否则简洁
- **保持挑刺者语气**：agent 的判断（第 3 节的响应质量判断、第 6 节的风险提示）要尖锐，不客套
- **语言**：跟随 Requester / 材料的语言。中文材料输出中文 brief

### 输出

严格按上面的 6 节结构输出 markdown。**不要添加 explanation 或 meta commentary**。直接输出 brief 本体。"""


def load_env_key(env_path, key):
    if not Path(env_path).exists(): return None
    for line in Path(env_path).read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip()
    return None


def call_openrouter(system_prompt, user_prompt, model, max_tokens=3000):
    api_key = load_openrouter_key()
    if not api_key: return None, "no OPENROUTER_API_KEY"
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "review-agent",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, str(e)


def load_persona(responder_name: str, stage_block: str) -> str:
    p = SKILL_DIR / "references" / "agent_persona.md"
    text = p.read_text()
    text = text.replace("{current_stage_block}", stage_block)
    text = text.replace("{responder_name}", responder_name)
    return text


def resolve_responder(sd: Path):
    name = "上级"; profile = ""
    try:
        m = json.load(open(sd / "meta.json"))
        resp_oid = m.get("responder_open_id")
        if resp_oid:
            root = Path(os.environ.get("REVIEW_AGENT_ROOT", Path.home() / ".review-agent"))
            rm = root / "users" / resp_oid / "meta.json"
            if rm.exists():
                name = json.load(open(rm)).get("display_name") or name
    except Exception: pass
    if (sd / "profile.md").exists():
        profile = (sd / "profile.md").read_text()
    return name, profile


def resolve_requester(sd: Path):
    name = "Requester"; oid = ""
    try:
        m = json.load(open(sd / "meta.json"))
        oid = m.get("requester_open_id", "")
        if oid:
            root = Path(os.environ.get("REVIEW_AGENT_ROOT", Path.home() / ".review-agent"))
            rm = root / "users" / oid / "meta.json"
            if rm.exists():
                name = json.load(open(rm)).get("display_name") or name
    except Exception: pass
    return name, oid


import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent))
from _model import get_main_agent_model
from _platform import load_openrouter_key, workspace_root, resolve_responder_name


def build_synthesis_brief(sd: Path, model: str = None) -> str:
    if model is None: model = get_main_agent_model()
    """LLM-synthesized 6-section decision brief. Falls back to audit if LLM fails."""
    meta = json.load(open(sd / "meta.json"))
    ann = load_jsonl(sd / "annotations.jsonl")
    responder_name, responder_profile = resolve_responder(sd)
    req_name, req_oid = resolve_requester(sd)

    # Load key artifacts for LLM to synthesize from
    normalized = (sd / "normalized.md").read_text() if (sd / "normalized.md").exists() else ""
    final_md = ""
    final_dir = sd / "final"
    if final_dir.exists():
        for f in final_dir.iterdir():
            if f.is_file() and f.suffix == ".md" and "revised" in f.name:
                final_md = f.read_text(); break
        if not final_md:
            for f in final_dir.iterdir():
                if f.is_file() and f.suffix == ".md":
                    final_md = f.read_text(); break

    dissent_md = (sd / "dissent.md").read_text() if (sd / "dissent.md").exists() else ""

    accepted = [a for a in ann if a.get("status") == "accepted"]
    modified = [a for a in ann if a.get("status") == "modified"]
    rejected = [a for a in ann if a.get("status") == "rejected"]
    unresolvable = [a for a in ann if a.get("status") == "unresolvable"]
    sim_findings = [a for a in ann if a.get("source") == "responder_simulation"]

    stage = BRIEF_SYNTHESIS_STAGE_BLOCK.replace("{responder_name}", responder_name)
    system = load_persona(responder_name, stage)

    user = f"""# 合成会前简报输入

## Session meta
```json
{json.dumps({k: meta.get(k) for k in ['session_id','subject','round','created_at','closed_at','termination','forced_reason','tags']}, ensure_ascii=False, indent=2)}
```

## Responder = {responder_name}
### Responder profile (标准 / pet peeves，摘)
```
{responder_profile[:2000]}{'...' if len(responder_profile) > 2000 else ''}
```

## Requester: {req_name} ({req_oid})

## 定稿材料 (final/revised.md 或 normalized.md)
```
{(final_md or normalized)[:6000]}
{'... (truncated)' if len(final_md or normalized) > 6000 else ''}
```

## Findings summary

### 已接受 ({len(accepted)})
{json.dumps([{'pillar': a.get('pillar'), 'severity': a.get('severity'), 'issue': a.get('issue'), 'suggest': a.get('suggest')} for a in accepted], ensure_ascii=False, indent=2)[:2000]}

### 修改 ({len(modified)})
{json.dumps([{'pillar': a.get('pillar'), 'issue': a.get('issue'), 'requester_version': a.get('reply','')} for a in modified], ensure_ascii=False, indent=2)[:1500]}

### 保留异议 / dissent ({len(rejected)})
{json.dumps([{'pillar': a.get('pillar'), 'severity': a.get('severity'), 'issue': a.get('issue'), 'reviewer_suggest': a.get('suggest'), 'requester_reason': a.get('reply','')} for a in rejected], ensure_ascii=False, indent=2)[:2500]}

### 无解 / unresolvable ({len(unresolvable)})
{json.dumps([{'pillar': a.get('pillar'), 'issue': a.get('issue'), 'reason': a.get('unresolvable_reason', a.get('reply',''))} for a in unresolvable], ensure_ascii=False, indent=2)[:1500]}

### Responder 模拟追问 (共 {len(sim_findings)}，按 priority)
{json.dumps([{'pillar': a.get('pillar'), 'priority': a.get('priority'), 'question': a.get('simulated_question',''), 'status': a.get('status')} for a in sorted(sim_findings, key=lambda x: x.get('priority', 99))], ensure_ascii=False, indent=2)[:2500]}

### Dissent log (raw)
```
{dissent_md[:1500]}{'...' if len(dissent_md) > 1500 else ''}
```

---

按 system 指示产出 6 节会前简报。直接输出 markdown，不加其他 prose。"""

    reply, err = call_openrouter(system, user, model)
    if not reply:
        return f"""# ⚠ Summary synthesis failed

{err}

## Fallback: see summary_audit.md for raw pillar-grouped audit.
"""
    return reply.strip()


def main(session_dir):
    sd = Path(session_dir)
    # 1. Audit trail (deterministic)
    audit = build_audit_summary(sd)
    (sd / "summary_audit.md").write_text(audit)
    print(f"wrote {sd / 'summary_audit.md'}")

    # 2. Decision brief (LLM synthesized) — primary
    brief = build_synthesis_brief(sd)
    (sd / "summary.md").write_text(brief)
    print(f"wrote {sd / 'summary.md'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: _build_summary.py <session_dir>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])