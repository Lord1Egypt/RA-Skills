#!/usr/bin/env python3
"""scan.py — four-pillar + responder-simulation review scanner.

Runs after ingest + subject confirmation. Reads session's frozen profile +
normalized.md + conversation, produces annotations.jsonl via two LLM layers:

  Layer A: Four-pillar scan (Background / Materials / Framework / Intent)
  Layer B: Responder simulation ("if {responder_name} read this, what would
           they ask?" — top 5 questions from their profile perspective)

Merged findings are written to annotations.jsonl with source field distinguishing
the two layers. Cursor is set to the first BLOCKER.

Usage:
  scan.py <session_dir> [--model <openrouter_model>] [--dry-run]
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path


def load_env_key(env_path, key):
    if not Path(env_path).exists():
        return None
    for line in Path(env_path).read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip()
    return None


sys.path.insert(0, str(Path(__file__).parent))
from _model import get_main_agent_model


def call_openrouter(system_prompt, user_prompt, model=None, max_tokens=3000):
    if model is None: model = get_main_agent_model()
    api_key = load_openrouter_key()
    if not api_key:
        return None, "no OPENROUTER_API_KEY in ~/.openclaw/openclaw.json (or ~/.hermes/.env legacy)"
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
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, str(e)


# Import the persona template loader
SKILL_DIR = Path(__file__).parent.parent


def load_persona(responder_name: str, current_stage_block: str) -> str:
    """Assemble full system prompt from persona + stage block via pure .replace()
    (no .format() — JSON examples in stage blocks have {} that would break .format).
    """
    persona_path = SKILL_DIR / "references" / "agent_persona.md"
    text = persona_path.read_text()
    text = text.replace("{current_stage_block}", current_stage_block)
    text = text.replace("{responder_name}", responder_name)
    return text


FOUR_PILLAR_STAGE_BLOCK = """**你现在在流程的 Step 3 Layer A：FOUR-PILLAR SCAN。**

主题已经和 Requester 对齐完了（见 `subject_confirm_draft.md` 或 conversation.jsonl 里他的选择）。接下来对他提交的材料 + 意图表达做**四柱扫描**，产 structured findings。

### 输出要求（严格 JSON）

输出一个 JSON 数组，每个元素是一个 finding 对象：

```json
[
  {{
    "pillar": "Intent" | "Background" | "Materials" | "Framework",
    "severity": "BLOCKER" | "IMPROVEMENT" | "NICE-TO-HAVE",
    "anchor": {{
      "source": "normalized.md" | "conversation.jsonl" | "intent",
      "snippet": "原文片段 ≤120 字"
    }},
    "issue": "一句话描述问题（中文）",
    "suggest": "具体建议，动词开头，含替换文本或精确追问"
  }},
  ...
]
```

### 扫描规则

**Pillar 4 (Intent) — 永远 BLOCKER** 如果 ask 含糊 / 把功课推给 Responder / 用"讨论"代替决策请求。

**Pillar 3 (Framework)**：讨论变量和判断类型明确了吗？如果 Requester 想让 Responder 选但没说按什么维度 → IMPROVEMENT；完全开放 → BLOCKER。

**Pillar 2 (Materials)**：Responder 最可能追的 top-3 问题都有答案吗？数据有源+日期吗？内外部锚点齐吗？按 Responder profile 校准阈值（如 profile 里写"6 个月陈旧 = BLOCKER"，就按这个硬卡）。

**Pillar 1 (Background)**：Responder 能不看背景补齐就进入讨论吗？

### 严禁
- 发明 pillar 之外的分类
- 空洞 suggest（"需要更清晰""补充信息"）
- 一次超过 8 条 NICE-TO-HAVE（批量进 JSONL 但本轮对话不发）
- 给 Responder 派活的建议（违反 no-boss-burden）

### 输出只有 JSON 数组

不要解释、不要前后加 prose。严格输出一个 `[...]`。"""


SIMULATION_STAGE_BLOCK = """**你现在在流程的 Step 3 Layer B：RESPONDER SIMULATION。**

你不是 Review Agent 了——你现在**扮演 {responder_name} 本人**。

### 任务

基于你的 profile（在 user prompt 里）+ 你平时的思考方式，读完 Requester 提交的材料。然后，如果 Requester 明天就把这份材料拿给你开会，**你最关心、最想追问的前 5 个问题是什么？** 按你自己的 priority 排（1 最要紧）。

### 硬规则

- 站在 {responder_name} 的视角，不是 Review Agent 的视角
- 问题必须是**你自己在实际会议中会说出来的那种**——具体、尖锐、带个人风格
- Pet peeves 触发的问题优先（profile 里写了"14 天内 3 个用户"的，就问这个）
- 避免通用问题（"你做过调研吗"）——太泛

### 输出格式（严格 JSON）

```json
{
  "responder_questions": [
    {"priority": 1, "question": "..."},
    {"priority": 2, "question": "..."}
  ]
}
```

只输出 JSON，不加解释。"""


def build_four_pillar_user_prompt(sd: Path, responder_name: str, responder_profile: str) -> str:
    normalized = (sd / "normalized.md").read_text() if (sd / "normalized.md").exists() else ""
    # Subject confirmation outcome (latest)
    confirmed_subject = "(not yet confirmed)"
    confirm_draft = sd / "subject_confirm_draft.md"
    if confirm_draft.exists():
        confirmed_subject = f"The confirm-topic stage produced this message:\n\n{confirm_draft.read_text()[:1500]}"
    # Requester's latest messages
    req_msgs = []
    conv = sd / "conversation.jsonl"
    if conv.exists():
        for line in conv.read_text().splitlines():
            try:
                e = json.loads(line)
                if e.get("role") == "requester":
                    req_msgs.append(f"[{e.get('ts','')}] {e.get('text','')[:400]}")
            except:
                pass
    return f"""# Review inputs

## Responder = {responder_name}

### {responder_name}'s profile.md (standards & pet peeves)
```
{responder_profile[:4000]}{'... (truncated)' if len(responder_profile) > 4000 else ''}
```

## Subject alignment (from earlier confirm-topic)
{confirmed_subject}

## Requester's IM messages (chronological)
{chr(10).join(req_msgs) or '(none)'}

## Normalized material (normalized.md)
```
{normalized[:8000]}
{'... (truncated)' if len(normalized) > 8000 else ''}
```

---

按 system 指示输出四柱扫描结果（严格 JSON 数组）。"""


def build_simulation_user_prompt(sd: Path, responder_name: str, responder_profile: str) -> str:
    normalized = (sd / "normalized.md").read_text() if (sd / "normalized.md").exists() else ""
    return f"""# 你的身份：{responder_name}

## 你的 profile（这是你自己写的对自己标准的描述）
```
{responder_profile[:4000]}{'... (truncated)' if len(responder_profile) > 4000 else ''}
```

## 刚才 Requester 递给你的材料
```
{normalized[:8000]}
{'... (truncated)' if len(normalized) > 8000 else ''}
```

---

按 system 指示，输出你读完后最想追问的 top 5 问题（严格 JSON）。"""


# Shared lenient parser
sys.path.insert(0, str(Path(__file__).parent))
from _json_repair import parse_lenient_json
from _platform import load_openrouter_key, workspace_root, resolve_responder_name

def parse_json_strict(text, expected_type):
    """Backward-compat shim — route to _json_repair.parse_lenient_json."""
    return parse_lenient_json(text, expected=expected_type)


def resolve_responder(sd: Path):
    name = "上级"
    profile = ""
    try:
        m = json.load(open(sd / "meta.json"))
        resp_oid = m.get("responder_open_id")
        if resp_oid:
            root = Path(os.environ.get("REVIEW_AGENT_ROOT", Path.home() / ".review-agent"))
            rm = root / "users" / resp_oid / "meta.json"
            if rm.exists():
                name = json.load(open(rm)).get("display_name") or name
    except Exception:
        pass
    if (sd / "profile.md").exists():
        profile = (sd / "profile.md").read_text()
    return name, profile


def emit_finding_id(idx, layer):
    prefix = "p" if layer == "four_pillar_scan" else "r"
    return f"{prefix}{idx+1}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session_dir")
    ap.add_argument("--model", default=None,
                    help="override model id; default: follow ~/.openclaw/openclaw.json main agent model")
    ap.add_argument("--dry-run", action="store_true",
                   help="print annotations but do not write files")
    ap.add_argument("--skip-simulation", action="store_true",
                   help="run only Layer A (four-pillar)")
    ap.add_argument("--top-n", type=int, default=None,
                   help="cap the Q&A loop to the top N most important findings "
                        "(default: 5, override via REVIEW_AGENT_TOP_N env)")
    args = ap.parse_args()

    sd = Path(args.session_dir)
    if not sd.is_dir():
        print(f"error: {sd} not a directory", file=sys.stderr)
        sys.exit(2)

    responder_name, responder_profile = resolve_responder(sd)

    # ─── Layer A: Four-pillar scan ─────────────────────────────
    print(f"[scan] Layer A: four-pillar scan against {responder_name}'s profile…", file=sys.stderr)
    system_a = load_persona(responder_name, FOUR_PILLAR_STAGE_BLOCK)
    user_a = build_four_pillar_user_prompt(sd, responder_name, responder_profile)
    reply_a, err_a = call_openrouter(system_a, user_a, args.model)
    if not reply_a:
        print(f"error: four-pillar scan failed: {err_a}", file=sys.stderr)
        sys.exit(3)
    pillar_findings, perr = parse_json_strict(reply_a, "array")
    if pillar_findings is None:
        print(f"error: could not parse four-pillar response: {perr}", file=sys.stderr)
        print(f"raw reply (first 500):\n{reply_a[:500]}", file=sys.stderr)
        sys.exit(4)
    print(f"[scan] Layer A produced {len(pillar_findings)} findings", file=sys.stderr)

    # ─── Layer B: Responder simulation ─────────────────────────
    sim_questions = []
    if not args.skip_simulation:
        print(f"[scan] Layer B: responder simulation ({responder_name})…", file=sys.stderr)
        sim_stage = SIMULATION_STAGE_BLOCK.replace("{responder_name}", responder_name)
        system_b = load_persona(responder_name, sim_stage)
        user_b = build_simulation_user_prompt(sd, responder_name, responder_profile)
        reply_b, err_b = call_openrouter(system_b, user_b, args.model, max_tokens=1500)
        if reply_b:
            parsed, perr = parse_json_strict(reply_b, "object")
            if parsed and "responder_questions" in parsed:
                sim_questions = parsed["responder_questions"]
                print(f"[scan] Layer B produced {len(sim_questions)} simulated questions", file=sys.stderr)
            else:
                print(f"[scan] Layer B parse failed: {perr}", file=sys.stderr)
        else:
            print(f"[scan] Layer B call failed: {err_b}", file=sys.stderr)

    # ─── Merge into annotations.jsonl ─────────────────────────
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    annotations = []

    # Determine current round (if resuming)
    meta_path = sd / "meta.json"
    meta = json.load(open(meta_path)) if meta_path.exists() else {}
    round_num = meta.get("round", 0) + 1 if meta.get("round") else 1

    for i, f in enumerate(pillar_findings):
        annotations.append({
            "id": emit_finding_id(i, "four_pillar_scan"),
            "round": round_num,
            "created_at": now,
            "source": "four_pillar_scan",
            "pillar": f.get("pillar", "?"),
            "severity": f.get("severity", "IMPROVEMENT"),
            "anchor": f.get("anchor", {}),
            "issue": f.get("issue", ""),
            "suggest": f.get("suggest", ""),
            "status": "open",
        })

    for i, q in enumerate(sim_questions):
        # Simulation findings are always tied to Pillar 2 (Materials) or 4 (Intent) by heuristic;
        # default to "Materials" since most simulated questions probe for evidence/specifics.
        # LLM can be taught to tag, but for v0, default to Materials/IMPROVEMENT unless the
        # question explicitly asks for the ask/decision → Intent/BLOCKER.
        text = q.get("question", "")
        pillar = "Materials"
        severity = "IMPROVEMENT"
        lowered = text.lower()
        if any(k in lowered for k in ["决定", "批准", "ask", "pick", "yes/no", "approve", "decide"]):
            pillar = "Intent"
            severity = "BLOCKER"
        annotations.append({
            "id": emit_finding_id(i, "responder_simulation"),
            "round": round_num,
            "created_at": now,
            "source": "responder_simulation",
            "pillar": pillar,
            "severity": severity,
            "simulated_question": text,
            "priority": q.get("priority", i+1),
            "anchor": {"source": "responder_simulation", "snippet": text[:120]},
            "issue": f"[{responder_name} 模拟问题] {text}",
            "suggest": f"请回答 / 补上这个问题的答案在材料里",
            "status": "open",
        })

    if args.dry_run:
        print(json.dumps(annotations, indent=2, ensure_ascii=False))
        return

    # Write
    with open(sd / "annotations.jsonl", "w") as f:
        for a in annotations:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")

    # Cap the Q&A loop to the top-N most important findings. Default 5 —
    # override with REVIEW_AGENT_TOP_N env or --top-n flag.
    top_n = int(os.environ.get("REVIEW_AGENT_TOP_N", "5"))
    if args.top_n is not None:
        top_n = args.top_n

    blockers = [a["id"] for a in annotations if a["severity"] == "BLOCKER"]
    improvements = [a["id"] for a in annotations if a["severity"] == "IMPROVEMENT"]
    nice = [a["id"] for a in annotations if a["severity"] == "NICE-TO-HAVE"]
    ordered = blockers + improvements + nice

    # Split into the active Q&A set (top_n) and deferred (rest). Remainder
    # stays in annotations.jsonl with status=open; qa-step.py won't surface
    # them unless Requester explicitly asks "keep going" after the top-N.
    active = ordered[:top_n]
    deferred = ordered[top_n:]
    cursor = {
        "current_id": active[0] if active else None,
        "pending": active[1:],
        "deferred": deferred,
        "done": [],
        "total_found": len(ordered),
        "top_n": top_n,
    }
    json.dump(cursor, open(sd / "cursor.json", "w"), indent=2, ensure_ascii=False)

    # Update meta round
    meta["round"] = round_num
    meta["last_activity_at"] = now
    json.dump(meta, open(meta_path, "w"), indent=2, ensure_ascii=False)

    print(f"[scan] wrote {len(annotations)} findings to {sd/'annotations.jsonl'}")
    print(f"[scan] cursor: {cursor['current_id']} (next: {cursor['pending'][:3]}…)")
    print(f"[scan] pillars: " + ", ".join(
        f"{p}={sum(1 for a in annotations if a['pillar']==p)}"
        for p in ["Intent", "Background", "Materials", "Framework"]
    ))


if __name__ == "__main__":
    main()