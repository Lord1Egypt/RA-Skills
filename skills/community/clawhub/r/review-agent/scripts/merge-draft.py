#!/usr/bin/env python3
"""merge-draft.py — generate final/revised.md from accepted findings.

Called after Q&A loop finishes (all annotations processed) and before final-gate.
Only runs in `suggest` mode (the default per admin_style.md). In `none` mode,
Requester is expected to upload their own revised draft to final/ manually.

Logic:
  1. Read normalized.md (original material)
  2. Read annotations.jsonl, filter to status=accepted OR modified
  3. LLM call: apply each finding's suggested fix to the material; for modified,
     use Requester's alternative text
  4. Output final/revised.md + diff summary
  5. Optionally send diff preview to Requester via Lark for final confirm

Usage:
  merge-draft.py <session_dir> [--model <openrouter>] [--send-preview]
"""
import argparse
import json
import os
import sys
import urllib.request
from _platform import load_openrouter_key, workspace_root, resolve_responder_name
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


def call_openrouter(system_prompt, user_prompt, model, max_tokens=4000):
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
        "temperature": 0.1,
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


MERGE_STAGE_BLOCK = """**你现在在 Step 5：DOCUMENT MERGE。**

Q&A 已经跑完——Requester 对 findings 做了回复（accepted / rejected / modified）。你的任务是基于**已经接受**或 Requester **自行修改**的 findings，把原始材料（normalized.md）重写成一份 **final/revised.md**，让 {responder_name} 可以直接读。

### 规则

1. 严格基于原材料 + accepted/modified 的 suggestions 做**最小化修改**。不要自己加内容 {responder_name} 和 Requester 都没讨论过的
2. 保留原材料的核心数据、数字、用户自己写的核心观点——你只是按 accepted findings 应用修改
3. 对于 **modified** 的 finding，用 Requester 提供的替代版本（reply 字段）
4. 对于 **rejected** 的 finding，**忽略**（Requester 已经拒绝）
5. 结构上向"{responder_name} 读起来高效"靠拢：BLUF → 背景 → 选项/分析 → 推荐 → 假设 → 风险 → 请求
6. 长度控制：≤ 1500 字中文 / 600 字英文（6-pager 级别）
7. 保持 Requester 的语言风格（中文/英文/混合）

### 输出格式（严格）

输出三部分，用 `---SECTION---` 分隔：

```
---REVISED---
<最终修订版 brief 的 markdown 正文>
---CHANGE-LOG---
<一段 100-200 字总结：应用了哪些 findings、哪些跳过、为什么>
---DIFF-HIGHLIGHTS---
<3-5 条 bullet：最关键的三五处改动，用"原：... → 新：..."形式让 Requester 一眼看到>
```

不要加其他 prose 或代码围栏。严格输出这三节。"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session_dir")
    ap.add_argument("--model", default=None,
                    help="override model id; default: follow ~/.openclaw/openclaw.json main agent model")
    ap.add_argument("--send-preview", action="store_true",
                   help="send the DIFF-HIGHLIGHTS to Requester via Lark for confirmation")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sd = Path(args.session_dir)
    if not sd.is_dir():
        print(f"error: {sd} not a directory", file=sys.stderr)
        sys.exit(2)

    # Resolve model from hermes config if not overridden
    if args.model is None:
        sys.path.insert(0, str(Path(__file__).parent))
        from _model import get_main_agent_model
        args.model = get_main_agent_model()

    # Load material + annotations
    normalized = (sd / "normalized.md").read_text() if (sd / "normalized.md").exists() else ""
    if not normalized:
        print(f"error: no normalized.md in {sd}", file=sys.stderr)
        sys.exit(2)
    anns = [json.loads(l) for l in (sd / "annotations.jsonl").read_text().splitlines() if l.strip()]
    accepted_or_modified = [a for a in anns if a.get("status") in ("accepted", "modified")]
    if not accepted_or_modified:
        print("warn: no accepted/modified findings — nothing to merge. skipping.", file=sys.stderr)
        sys.exit(0)

    # Responder + profile for persona
    name, profile = "上级", ""
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

    # Build prompts
    system = load_persona(name, MERGE_STAGE_BLOCK)
    # Summarize findings for the user prompt
    findings_summary = []
    for a in accepted_or_modified:
        desc = f"- [{a.get('pillar','?')} · {a.get('severity','?')} · {a.get('status','?')}] {a.get('issue','')}"
        if a.get("status") == "accepted":
            desc += f"\n  → Apply: {a.get('suggest','')}"
        elif a.get("status") == "modified":
            desc += f"\n  → Use Requester's version: {a.get('reply','')}"
        findings_summary.append(desc)

    user_prompt = f"""# 原始材料 (normalized.md)

```
{normalized[:12000]}
{'... (truncated)' if len(normalized) > 12000 else ''}
```

# {name} 的标准（摘自 profile.md）

```
{profile[:2000]}{'...' if len(profile) > 2000 else ''}
```

# 已 accepted / modified 的 findings ({len(accepted_or_modified)} 条)

{chr(10).join(findings_summary)}

---

按 system 指示产出 REVISED + CHANGE-LOG + DIFF-HIGHLIGHTS 三节。"""

    reply, err = call_openrouter(system, user_prompt, args.model)
    if not reply:
        print(f"error: LLM call failed: {err}", file=sys.stderr)
        sys.exit(3)

    # Parse the three sections
    def extract(marker, text):
        m = text.find(f"---{marker}---")
        if m < 0: return ""
        start = m + len(f"---{marker}---")
        # find next ---...--- after
        import re
        nxt = re.search(r"---[A-Z-]+---", text[start:])
        end = start + nxt.start() if nxt else len(text)
        return text[start:end].strip()

    revised = extract("REVISED", reply)
    change_log = extract("CHANGE-LOG", reply)
    diff_highlights = extract("DIFF-HIGHLIGHTS", reply)

    if not revised:
        print(f"error: LLM did not return REVISED section. raw: {reply[:500]}", file=sys.stderr)
        sys.exit(3)

    if args.dry_run:
        print("─── REVISED ───\n" + revised)
        print("\n─── CHANGE-LOG ───\n" + change_log)
        print("\n─── DIFF-HIGHLIGHTS ───\n" + diff_highlights)
        return

    # Write outputs
    final_dir = sd / "final"
    final_dir.mkdir(exist_ok=True)
    (final_dir / "revised.md").write_text(revised)
    (final_dir / "revised_changelog.md").write_text(
        f"# Change Log\n\n{change_log}\n\n## Diff Highlights\n\n{diff_highlights}\n\n---\n_Generated by merge-draft.py at {datetime.now().astimezone().isoformat(timespec='seconds')}_\n"
    )
    print(f"wrote {final_dir / 'revised.md'}")
    print(f"wrote {final_dir / 'revised_changelog.md'}")

    # v2: always produce the preview text. The subagent reads our stdout and
    # decides whether to relay it to Lark via native feishu_chat.
    if args.send_preview:
        preview = f"""我基于你接受的改法生成了修订版 brief。

**核心改动**：
{diff_highlights}

完整版本在 session 里：`final/revised.md`。如果 OK，回 "可以" / "confirm"，我就跑 final-gate 准备发给 {name}。
如果要我再改某处，告诉我具体哪里。"""
        # Log outbound intent to conversation
        with open(sd / "conversation.jsonl", "a") as f:
            f.write(json.dumps({
                "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
                "role": "reviewer",
                "source": "stdout_for_subagent",
                "stage": "merge_diff_preview",
                "text": preview,
            }, ensure_ascii=False) + "\n")
        # Print preview so the subagent can relay via feishu_chat
        print("---PREVIEW---")
        print(preview)


if __name__ == "__main__":
    main()