#!/usr/bin/env python3
"""qa-step.py — one step of the Review Q&A loop.

Called by the Orchestrator (hermes main agent) when a Requester sends a message
while their session is in REVIEW-ACTIVE mode (active_session.json present).

Does all the work deterministically:
  1. Identifies current annotation being discussed (via cursor.json)
  2. Uses LLM to classify Requester's reply intent wrt that annotation:
     accepted / rejected+reason / modified / question / skip / force-close
  3. Updates annotation status + cursor; if rejected, appends dissent.md
  4. If pending empty AND CSW gate met → emit "ready for close" message
  5. Otherwise advance cursor, compose next finding, emit it as reply text
  6. Prints the reply text to stdout — v2 subagent reads it and sends via
     native feishu_chat tool

Usage:
  qa-step.py <session_id> "<requester message>"

Output:
  stdout: the reply text to send to Requester via Lark
  exit code 0 = success; 2 = session not found; 3 = LLM error
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Optional


SKILL_DIR = Path(__file__).parent.parent


def load_env_key(env_path, key):
    if not Path(env_path).exists():
        return None
    for line in Path(env_path).read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip()
    return None


sys.path.insert(0, str(Path(__file__).parent))
from _model import get_main_agent_model


def call_openrouter(system_prompt, user_prompt, model=None, max_tokens=800):
    if model is None: model = get_main_agent_model()
    api_key = load_openrouter_key()
    if not api_key:
        return None, "no OPENROUTER_API_KEY"
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
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, str(e)


def load_persona(responder_name: str, current_stage_block: str) -> str:
    persona_path = SKILL_DIR / "references" / "agent_persona.md"
    text = persona_path.read_text()
    text = text.replace("{current_stage_block}", current_stage_block)
    text = text.replace("{responder_name}", responder_name)
    return text


CLASSIFY_SYSTEM_TEMPLATE = """你现在处于 Q&A loop 的分类 + 回复阶段。

刚才你向 Requester 发了一条 finding（在 user prompt 里），现在他回复了（也在 user prompt 里）。你需要：

## 1. 分类 Requester 回复的意图（严格六选一）

识别快捷回复：
- 单字母 `a` / `A` → accepted
- 单字母 `b` / `B` + 理由 → rejected
- 单字母 `b` / `B` 无理由 → rejected（但 reason 为空，需要问一句）
- 单字母 `c` / `C` + 替代内容 → modified
- 单字母 `p` / `P` → skip
- `pass` / `跳过` / `skip` / `next` / `先跳` → skip
- `custom` / 直接打字 > 20 字 → 按内容语义分类（accepted / rejected / modified / question / force-close）
- `force-close` / `结束` / `停` / `不改了` → force-close
- 问澄清（`什么意思？` / `你能举例吗？`）→ question

类别：
- `accepted`: 接受建议，会改
- `rejected`: 不同意，带理由
- `modified`: 提出不同的改法
- `question`: 想澄清 finding 的含义
- `skip`: 跳过这条，看下一条
- `force-close`: 立即结束 session

## 2. 产出下一条 IM 回复（字符数 ≤ 350 中文 / 180 英文）

每条回复**必须**以下面这个固定结构结尾的选项块结束（除非是 force-close 的 case）：

```
(a) accept · 按建议改
(b) reject · 不同意（说一下理由）
(c) modify · 我要改成另外的版本 xxx
(p) pass · 跳过这条
(custom) 其他——直接打字
```

**针对各 intent 的具体响应**（选项块之前的正文）：

- `accepted` → "✓ 收到。" 加一空行，发下一条 finding（从 cursor.pending 取第一个，包含 pillar/severity/issue/suggest）+ 选项块
- `rejected` 且有理由 → "收到异议，已进 dissent log 给 {responder_name} 看。" 空行 + 下一条 finding + 选项块
- `rejected` 无理由 → "不同意可以，但先给一句理由，我记进 dissent log。" + 不推进 cursor，但仍附选项块让他方便反应
- `modified` → "收到修改版。" 空行 + 下一条 finding + 选项块
- `question` → Socratic 答复澄清（2-3 句），不推进 cursor；末尾仍附选项块让他选
- `skip` → "⊘ 跳过。" 空行 + 下一条 + 选项块
- `force-close` 无理由 → "结束前给一句理由？" 不关闭，不加选项块
- `force-close` 有理由 → "收到，即将关闭。" 不加选项块

**如果 pending 是空的**（最后一条 finding 已处理）：
- 正文："所有 finding 处理完。要我现在跑 final-gate 看能不能 close 吗？"
- 选项块改为：
  ```
  (a) ready · 可以 close，发 summary 给 {responder_name}
  (b) more · 想再迭代一轮
  (pass) 先挂着
  (custom) 其他
  ```

## 3. 输出格式（严格 JSON）

```
{
  "intent": "accepted" | "rejected" | "modified" | "question" | "skip" | "force-close",
  "reason": "Requester 给的理由（仅 rejected/force-close 时）",
  "modified_text": "Requester 的修改版本（仅 modified 时）",
  "advance_cursor": true | false,
  "append_to_dissent": true | false,
  "close_session": false | true,
  "reply_text": "要发给 Requester 的下一条 IM 正文（完整消息，含选项块）"
}
```

只输出 JSON，不要加任何 prose 或代码围栏。"""


def build_classify_user_prompt(sd: Path, requester_msg: str, current_annotation: dict,
                                next_finding: Optional[dict], responder_name: str,
                                responder_profile: str):
    # Last few conversation turns for context
    conv = sd / "conversation.jsonl"
    recent = []
    if conv.exists():
        for line in conv.read_text().splitlines()[-6:]:
            try:
                e = json.loads(line)
                role = e.get("role","?")
                text = e.get("text","")[:300]
                recent.append(f"[{role}] {text}")
            except: pass
    return f"""# 上下文

## Responder = {responder_name}

### Responder profile (摘要)
{responder_profile[:1500]}{'...' if len(responder_profile) > 1500 else ''}

## 最近对话（最后 6 轮）
{chr(10).join(recent) or '(none)'}

## 你上一条刚发的 finding
- pillar: {current_annotation.get('pillar','?')}
- severity: {current_annotation.get('severity','?')}
- source: {current_annotation.get('source','?')}
- issue: {current_annotation.get('issue','?')}
- suggest: {current_annotation.get('suggest','?')}
{f'- simulated_question: {current_annotation.get("simulated_question","")}' if current_annotation.get('source') == 'responder_simulation' else ''}

## Requester 刚回复
> {requester_msg}

## 下一条待发（如果 advance cursor）
{json.dumps(next_finding, ensure_ascii=False, indent=2) if next_finding else '(pending 空——所有 finding 已处理)'}

---

按 system 指示分类并产出下一条 IM。
"""


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


# Shared lenient parser — handles markdown fences, newlines, inner quotes,
# trailing commas, line comments. Single point of repair across all scripts.
sys.path.insert(0, str(Path(__file__).parent))
from _json_repair import parse_lenient_json
from _platform import load_openrouter_key, workspace_root, resolve_responder_name

def parse_json_strict(text):
    return parse_lenient_json(text, expected="object")


def find_session_dir(session_id: str) -> Optional[Path]:
    """v2: session lives in <workspace>/sessions/<session_id>/. The workspace
    is the subagent's cwd (overridable via REVIEW_AGENT_WORKSPACE for tests).
    Also accepts a full relative/absolute path for backward compat."""
    # If caller passed a path, honor it
    p = Path(session_id)
    if p.is_absolute() and p.is_dir():
        return p
    if (Path.cwd() / session_id).is_dir() and "/" in session_id:
        return (Path.cwd() / session_id).resolve()
    # Resolve workspace
    ws = Path(os.environ.get("REVIEW_AGENT_WORKSPACE", Path.cwd())).resolve()
    candidate = ws / "sessions" / session_id
    if candidate.is_dir():
        return candidate
    # Legacy v1 fallback (for migration phase)
    legacy_root = Path(os.environ.get("REVIEW_AGENT_ROOT", Path.home() / ".review-agent"))
    if legacy_root.exists():
        for p in (legacy_root / "users").glob(f"*/sessions/{session_id}"):
            if p.is_dir():
                return p
    return None


def load_annotations(sd: Path):
    path = sd / "annotations.jsonl"
    if not path.exists(): return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def write_annotations(sd: Path, anns: list):
    with open(sd / "annotations.jsonl", "w") as f:
        for a in anns:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")


def update_annotation(anns: list, id_: str, updates: dict):
    for a in anns:
        if a.get("id") == id_:
            a.update(updates)
            a["replied_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
            break


def append_dissent(sd: Path, annotation: dict, reason: str):
    with open(sd / "dissent.md", "a") as f:
        f.write(f"\n## {annotation.get('id','?')} — [{annotation.get('pillar','?')}] {annotation.get('severity','?')}\n")
        f.write(f"**Issue**: {annotation.get('issue','')}\n\n")
        f.write(f"**Reviewer suggested**: {annotation.get('suggest','')}\n\n")
        f.write(f"**Requester 拒绝理由**: {reason}\n")


def append_conversation(sd: Path, role: str, text: str, **extra):
    entry = {
        "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
        "role": role,
        **extra,
        "text": text,
    }
    with open(sd / "conversation.jsonl", "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def handle_scope_decision(sd: Path, msg: str, anns: list, meta: dict):
    """When status == awaiting_scope_decision, parse Requester's coverage choice.

    Returns: prints the first finding to stdout, transitions session to qa_active.
    Coverage rules:
      - 'a' or default → min(3, BLOCKER count)
      - 'b' or '5' → 5
      - 'c' or 'all' → all
      - 'p' / 'pass' → close session
      - explicit number N → top N
      - explicit ids 'p1 p3 r2' → that subset
    """
    m = msg.strip().lower()
    total = len(anns)
    blockers = [a for a in anns if a.get("severity") == "BLOCKER"]
    improvements = [a for a in anns if a.get("severity") == "IMPROVEMENT"]
    nice = [a for a in anns if a.get("severity") == "NICE-TO-HAVE"]
    ordered = blockers + improvements + nice
    default_k = min(3, len(blockers)) if blockers else min(3, total)

    # Log inbound
    append_conversation(sd, "requester", msg, source="lark_dm", stage="scope_decision")

    # Parse intent
    selected_ids = []
    close_now = False
    reply_prefix = ""

    if m in ("p", "pass", "跳过", "skip", "不 review", "不review"):
        close_now = True
        reply_prefix = "好，跳过 review。如果以后想继续，重新发材料即可。"
    elif m in ("a", "default", "默认"):
        selected_ids = [a["id"] for a in ordered[:default_k]]
        reply_prefix = f"好，先带你过最关键的 {default_k} 条。"
    elif m in ("b", "5"):
        k = min(5, total)
        selected_ids = [a["id"] for a in ordered[:k]]
        reply_prefix = f"好，覆盖前 {k} 条。"
    elif m in ("c", "all", "全部"):
        selected_ids = [a["id"] for a in ordered]
        reply_prefix = f"好，{total} 条全过。"
    else:
        # Try parsing as number
        n_match = re.match(r"^\s*(\d+)\s*$", m)
        if n_match:
            k = min(int(n_match.group(1)), total)
            selected_ids = [a["id"] for a in ordered[:k]]
            reply_prefix = f"好，前 {k} 条。"
        else:
            # Try parsing as explicit IDs
            id_tokens = re.findall(r"[prms]\d+", m)
            existing_ids = {a["id"] for a in anns}
            valid_ids = [t for t in id_tokens if t in existing_ids]
            if valid_ids:
                selected_ids = valid_ids
                reply_prefix = f"好，按你指定的 {len(valid_ids)} 条来。"
            else:
                # Fallback: default
                selected_ids = [a["id"] for a in ordered[:default_k]]
                reply_prefix = f"没看懂具体数量，默认先过最关键的 {default_k} 条。"

    # Apply scope
    if close_now:
        # Close session without Q&A
        meta["status"] = "closed"
        meta["termination"] = "forced_by_briefer"
        meta["forced_reason"] = "Requester passed at scope decision"
        meta["closed_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
        json.dump(meta, open(sd / "meta.json", "w"), indent=2, ensure_ascii=False)
        # Clear active_session pointer
        req_oid = meta.get("requester_open_id", "")
        root = Path(os.environ.get("REVIEW_AGENT_ROOT", Path.home() / ".review-agent"))
        pointer = root / "users" / req_oid / "active_session.json"
        if pointer.exists(): pointer.unlink()
        append_conversation(sd, "reviewer", reply_prefix, source="lark_dm_out",
                           stage="scope_passed_close")
        print(reply_prefix)
        print("[qa-step] scope_decision=pass → session closed", file=sys.stderr)
        return

    # Mark non-selected as deferred-by-scope (stays visible in summary but not in Q&A cursor)
    selected_set = set(selected_ids)
    for a in anns:
        if a["id"] not in selected_set:
            a["status"] = "deferred_by_scope"
            a["scope_note"] = "not selected in initial coverage decision"
    write_annotations(sd, anns)

    # Set cursor to selected findings
    cursor = {
        "current_id": selected_ids[0] if selected_ids else None,
        "pending": selected_ids[1:],
        "done": [],
    }
    json.dump(cursor, open(sd / "cursor.json", "w"), indent=2, ensure_ascii=False)

    # Transition status
    meta["status"] = "qa_active"
    meta["last_activity_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    meta["scope_selected"] = selected_ids
    json.dump(meta, open(sd / "meta.json", "w"), indent=2, ensure_ascii=False)

    # Compose first-finding message
    first = next((a for a in anns if a["id"] == cursor["current_id"]), None)
    if not first:
        print(reply_prefix + "\n(内部错误：找不到选中的 finding)")
        return
    pillar = first.get("pillar", "?")
    sev = first.get("severity", "?")
    issue_text = first.get("simulated_question") or first.get("issue", "")
    suggest = first.get("suggest", "")
    src_tag = "（Responder 视角模拟的追问）" if first.get("source") == "responder_simulation" else ""

    options = """
(a) accept · 按建议改
(b) reject · 不同意（说一下理由）
(c) modify · 我要改成另外的版本 xxx
(p) pass · 跳过这条
(custom) 其他——直接打字"""

    if first.get("source") == "responder_simulation":
        body = f"{reply_prefix}\n\n**第 1 条 · {pillar} · {sev}**{src_tag}\n\n{issue_text}\n{options}"
    else:
        body = f"{reply_prefix}\n\n**第 1 条 · {pillar} · {sev}**\n\n{issue_text}\n\n建议：{suggest}\n{options}"

    append_conversation(sd, "reviewer", body, source="lark_dm_out",
                       stage="first_finding_after_scope", finding_id=cursor["current_id"])
    print(body)
    print(f"[qa-step] scope_decision={len(selected_ids)}_selected cursor={cursor['current_id']}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session_id")
    ap.add_argument("message", help="requester's latest Lark message text")
    ap.add_argument("--model", default=None,
                    help="override model id; default: follow ~/.openclaw/openclaw.json main agent model")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sd = find_session_dir(args.session_id)
    if not sd:
        print(f"error: session {args.session_id} not found", file=sys.stderr)
        sys.exit(2)

    responder_name, responder_profile = resolve_responder(sd)
    anns = load_annotations(sd)
    if not anns:
        print(f"error: no annotations in {sd}/annotations.jsonl — run scan.py first",
              file=sys.stderr)
        sys.exit(2)

    # Legacy: if any session is stuck in scope-decision (shouldn't happen now that
    # confirm-and-scan auto-scopes), apply default scope silently and continue.
    meta = json.load(open(sd / "meta.json"))
    if meta.get("status") == "awaiting_scope_decision":
        # Silently auto-scope to top 3 (same as confirm-and-scan default) and
        # treat this message as a normal Q&A reply on the first finding.
        handle_scope_decision(sd, "a", anns, meta)   # "a" = default scope = top 3
        # Reload state
        anns = load_annotations(sd)
        meta = json.load(open(sd / "meta.json"))

    cursor = json.load(open(sd / "cursor.json"))
    current_id = cursor.get("current_id")
    pending = cursor.get("pending", [])

    if not current_id:
        print(f"error: cursor has no current_id — nothing to respond about",
              file=sys.stderr)
        sys.exit(2)

    # Snapshot first-turn state BEFORE mutating cursor, so we can add a
    # "found N total, walking the top-K" preamble on the very first reply.
    is_first_turn = len(cursor.get("done", [])) == 0
    total_found = cursor.get("total_found", len(anns))
    top_n_cap = cursor.get("top_n", 5)
    deferred_count = total_found - top_n_cap

    current_ann = next((a for a in anns if a.get("id") == current_id), None)
    if not current_ann:
        print(f"error: cursor points to {current_id} but not in annotations", file=sys.stderr)
        sys.exit(2)

    next_id = pending[0] if pending else None
    next_ann = next((a for a in anns if a.get("id") == next_id), None) if next_id else None

    # Log the requester's message immediately so we don't lose it
    append_conversation(sd, "requester", args.message, source="lark_dm",
                       replying_to=current_id)

    # LLM classify + compose
    system = CLASSIFY_SYSTEM_TEMPLATE
    user_prompt = build_classify_user_prompt(
        sd, args.message, current_ann, next_ann, responder_name, responder_profile
    )
    reply, err = call_openrouter(system, user_prompt, args.model)
    if not reply:
        print(f"error: LLM call failed: {err}", file=sys.stderr)
        sys.exit(3)
    parsed, perr = parse_json_strict(reply)
    if not parsed:
        print(f"error: could not parse LLM reply: {perr}", file=sys.stderr)
        print(f"raw: {reply[:500]}", file=sys.stderr)
        sys.exit(3)

    intent = parsed.get("intent", "question")
    reason = parsed.get("reason")
    modified_text = parsed.get("modified_text")
    advance = parsed.get("advance_cursor", False)
    to_dissent = parsed.get("append_to_dissent", False)
    close_sig = parsed.get("close_session", False)
    reply_text = parsed.get("reply_text", "").strip()

    if args.dry_run:
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
        return

    # Apply updates
    if intent == "accepted":
        update_annotation(anns, current_id, {"status": "accepted"})
    elif intent == "rejected" and reason:
        update_annotation(anns, current_id, {"status": "rejected", "reply": reason})
        if to_dissent:
            append_dissent(sd, current_ann, reason)
    elif intent == "modified" and modified_text:
        update_annotation(anns, current_id, {"status": "modified", "reply": modified_text})
    elif intent == "skip":
        pass  # cursor advance only, no status change

    write_annotations(sd, anns)

    # Update cursor
    if advance:
        cursor["done"].append(current_id)
        cursor["current_id"] = pending[0] if pending else None
        cursor["pending"] = pending[1:]

        # If we just ran out of pending BUT have deferred findings, append a
        # closing hint to reply_text letting the Requester opt-in to continue.
        if not cursor["current_id"] and cursor.get("deferred"):
            nxt = cursor["deferred"]
            reply_text = reply_text.rstrip() + (
                f"\n\n---\n\n前 {cursor.get('top_n', 5)} 条已过完。"
                f"还有 {len(nxt)} 条 deferred 的问题（优先级较低），回 `more` 继续，"
                f"或 `done` 结束进入 merge+final-gate。"
            )

    # Support explicit "more" — pull deferred into pending on demand
    msg_lower = args.message.strip().lower()
    if msg_lower in ("more", "继续", "more please", "下一批") and cursor.get("deferred"):
        cursor["pending"] = cursor["deferred"] + cursor.get("pending", [])
        cursor["current_id"] = cursor["pending"][0] if cursor["pending"] else None
        cursor["pending"] = cursor["pending"][1:]
        cursor["deferred"] = []

    json.dump(cursor, open(sd / "cursor.json", "w"), indent=2, ensure_ascii=False)

    # Update meta last_activity
    meta = json.load(open(sd / "meta.json"))
    meta["last_activity_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    json.dump(meta, open(sd / "meta.json", "w"), indent=2, ensure_ascii=False)

    # First-turn preamble: if this was the first reply AND scan found more
    # than top_n issues, tell the Requester what they're seeing.
    if is_first_turn and total_found > top_n_cap:
        preamble = (
            f"我扫到 {total_found} 条问题。先带你过最关键的 {top_n_cap} 条"
            f"——过完再看剩下 {deferred_count} 条要不要继续。\n\n---\n\n"
        )
        reply_text = preamble + reply_text

    # Log outbound
    append_conversation(sd, "reviewer", reply_text, source="lark_dm_out",
                       intent_classified=intent,
                       finding_id=current_id if not advance else (cursor.get("current_id") or ""))

    # Output contract (to prevent context pollution of main agent):
    #   stdout = IM reply text ONLY (subagent relays via native feishu_chat tool)
    #   stderr = minimal progress markers ONLY (no session content)
    print(reply_text)
    # Status markers on stderr — no session internals, only lifecycle signals
    print(f"[qa-step] intent={intent} cursor_advance={advance}", file=sys.stderr)
    if close_sig or not cursor.get("current_id"):
        print("[qa-step] ALL_FINDINGS_PROCESSED — run close-session.sh next", file=sys.stderr)


if __name__ == "__main__":
    main()