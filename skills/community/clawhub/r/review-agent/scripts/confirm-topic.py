#!/usr/bin/env python3
"""Generate the 'subject confirmation' message for a review session.

Purpose: AFTER ingest, BEFORE seven-axis scan. Agent reads normalized.md +
conversation.jsonl (for Requester's stated intent) and produces a short
confirmation message with 2-4 candidate topics for the Requester to pick from.

Uses OpenRouter (hermes .env) to call Sonnet 4.6 (or cheapest available) to
extract candidate topics. Falls back to a prompt template if no API available.

Usage:
  confirm-topic.py <session_dir> [--send]
    --send : DEPRECATED in v2 (openclaw). Subagent now sends the confirmation
             message via native feishu_chat tool. This flag is ignored and the
             message is always printed to stdout, which the subagent relays.
"""
import argparse
import json
import os
import re
import subprocess
import sys
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
from _platform import load_openrouter_key, workspace_root, resolve_responder_name


def call_openrouter(system_prompt, user_prompt, model=None):
    if model is None: model = get_main_agent_model()
    """Call OpenRouter chat completions with given messages."""
    api_key = load_openrouter_key()
    if not api_key:
        return None
    import urllib.request
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 800,
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
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"openrouter call failed: {e}", file=sys.stderr)
        return None


# Confirm-topic current stage block — injected into the shared persona template
CONFIRM_STAGE_BLOCK = """**你现在在流程的 Step 2：SUBJECT CONFIRMATION。**

这是你和 Requester 的第一次对话。任务是让他确认你对"他要讨论什么"的理解对不对，对齐完再进入 Step 3（七轴扫描）。

### 这一步你要做的

1. 读 Requester 的 IM 历史 + 他提交的 `normalized.md`
2. 推断他**实际**想和 {responder_name} 讨论的 2-4 个候选主题
3. 每个候选必须是"{responder_name} 能够 yes/no 或 A/B 选择的具体决策/反馈点"——不是宽泛话题。"一起聊聊 X"、"看看 X 如何"、"讨论 X 方向"不合格；必须是可动作的
4. 选项措辞要**贴合 {responder_name} 的 profile**（见 user prompt）——他 pet peeve 里写 "consider/maybe/perhaps/再梳理梳理 = 逃避"，选项里必须避免这类虚词

### 输出格式

输出必须包含三块：**自我介绍 + 流程说明（1 行）** → **主题确认 + 选项块（带 pass/custom 兜底）** → **下一步引导**。

```
你好，我是 {responder_name} 的 Review Agent。

【流程】我先和你对齐要讨论的主题 → 按 {responder_name} 的标准帮你过材料（挑问题 / 追问，不帮你写答案）→ 你修改后我产出一份可以直接给他的会前简报。全程最多 3 轮，完了他才会收到材料。

先对齐主题：你希望和 {responder_name} 讨论的是——

(a) <具体决策或反馈点 A>
(b) <具体决策或反馈点 B>
(c) <具体决策或反馈点 C>          ← 可选，最多写到 (c)
(p) pass · 先不走 review，回到普通聊天
(custom) 都不是——自己说具体是什么

回 a/b/c，或 p，或直接打字。
```

**注意**：`p` / `pass` / `custom` 都是识别关键字。Requester 回 "p"、"pass"、"跳过"、"skip" 都能识别为 pass。

### 流程说明行的写法纪律

- **言简意赅**：1-2 行，不要写成 6 步 SOP
- **让 Requester 知道两件事**：
  1. Agent 是挑刺者，不代劳——避免他期待 "agent 帮我写"
  2. Responder 在完成前看不到材料——让他放心迭代
- **不要拿 "四柱 / 六维度 / CSW" 等内部术语** 出来吓人——Requester 不需要知道

### 这一步严禁

- **不做** review、不给建议、不提修改——那是 Step 3 的事
- **不替** Requester 决定（只确认主题，不替他选）
- **不发墙** / 不用套话 / 不"great question"
- 选项**不能**写成"一起探讨 X"、"评估 X"、"研究 X"等形态
- 字数硬上限：中文 ≤ 350 字，英文 ≤ 180 words
"""


def build_confirm_system(responder_name: str) -> str:
    """Build full system prompt = shared persona + current stage block.
    Uses pure .replace() (not .format) — stage blocks contain literal {} from JSON examples.
    """
    persona_path = Path(__file__).parent.parent / "references" / "agent_persona.md"
    try:
        persona = persona_path.read_text()
    except FileNotFoundError:
        persona = ""
    stage = CONFIRM_STAGE_BLOCK.replace("{responder_name}", responder_name)
    full = persona.replace("{current_stage_block}", stage)
    full = full.replace("{responder_name}", responder_name)
    return full


def resolve_responder(sd: Path):
    """Return (responder_name, responder_profile_content)."""
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
    # Prefer frozen profile in session (source of truth for this session)
    if (sd / "profile.md").exists():
        profile = (sd / "profile.md").read_text()
    return name, profile


def build_user_prompt(session_dir: Path, responder_name: str, responder_profile: str):
    sd = session_dir
    normalized = (sd / "normalized.md").read_text() if (sd / "normalized.md").exists() else "(no material)"
    intent_lines = []
    conv = sd / "conversation.jsonl"
    if conv.exists():
        for line in conv.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("role") == "requester":
                    t = entry.get("text", "")
                    if t and len(t) < 500:
                        intent_lines.append(f"[{entry.get('ts','?')}] {t}")
            except json.JSONDecodeError:
                pass

    return f"""# 本次会话上下文

## Responder = {responder_name}

### {responder_name} 的 profile（他的标准 / pet peeves / 决策风格）
```
{responder_profile[:3500] or '(no profile — use generic professional defaults)'}
{'...(truncated)' if len(responder_profile) > 3500 else ''}
```

## Requester IM 历史（时间顺序）
{chr(10).join(intent_lines) or '(no IM history yet)'}

## Requester 提交的材料（normalized.md）
{normalized[:8000]}
{'...(truncated)' if len(normalized) > 8000 else ''}

---
现在按 system 指示产出确认消息——注意候选选项的措辞要贴合 {responder_name} profile 里的决策风格（比如他 pet peeve 里写 "consider/maybe/perhaps 是逃避"，选项里就避免这类词）。"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session_dir")
    ap.add_argument("--send", action="store_true",
                    help="DEPRECATED in v2 — ignored. Subagent reads stdout and sends via native feishu_chat tool.")
    ap.add_argument("--model", default=None,
                    help="override model id (OpenRouter format); default: follow ~/.openclaw/openclaw.json model.default")
    args = ap.parse_args()

    sd = Path(args.session_dir)
    if not sd.is_dir():
        print(f"error: {sd} not a directory", file=sys.stderr)
        sys.exit(2)

    responder_name, responder_profile = resolve_responder(sd)
    system_prompt = build_confirm_system(responder_name)
    user_prompt = build_user_prompt(sd, responder_name, responder_profile)
    reply = call_openrouter(system_prompt, user_prompt, model=args.model)

    if not reply:
        print("=== FALLBACK (no API available) ===\n", file=sys.stderr)
        print("SYSTEM PROMPT:\n", system_prompt, file=sys.stderr)
        print("\nUSER PROMPT:\n", user_prompt, file=sys.stderr)
        sys.exit(3)

    # Save to session for audit
    (sd / "subject_confirm_draft.md").write_text(reply)

    # Log outbound to conversation.jsonl regardless of --send (v2: subagent
    # sends to Lark itself by piping our stdout through feishu_chat)
    from datetime import datetime
    conv = sd / "conversation.jsonl"
    with open(conv, "a") as f:
        f.write(json.dumps({
            "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
            "role": "reviewer",
            "source": "stdout_for_subagent",
            "stage": "subject_confirmation",
            "text": reply
        }, ensure_ascii=False) + "\n")

    # Always print — subagent pipes this to feishu_chat. --send is ignored in v2.
    print(reply)


if __name__ == "__main__":
    main()