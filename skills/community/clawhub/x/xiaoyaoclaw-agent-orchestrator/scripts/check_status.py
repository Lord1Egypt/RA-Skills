# -*- coding: utf-8 -*-
"""解析 sessions_list 输出，汇总子任务状态（零 token 确定性操作）。

用法:
    python check_status.py <sessions_list_json_file> [--task KEY...] [--json]

说明:
    - 输入：sessions_list 工具的输出 JSON（保存到文件后传入）
    - 也可从 stdin 读取：cat sessions.json | python check_status.py -
    - 输出：每会话一行（key / kind / updatedAt / 状态判定）
    - 状态判定只看**本次派发运行**：最后一条 user（派发提示）之后的 **assistant** 消息；
      用户消息 / 工具结果 / system 提示一律不参与判定（避免误判完成或失败）
    - 状态判定规则：
        [DONE]    本次运行的 assistant 回复**最后一行恰为** [DONE]（结构化 status=done 亦可）
        [FAILED]  本次运行的 assistant 回复**最后一行恰为** [FAILED]（结构化 status=failed 亦可）
        [RUNNING] updatedAt 在 recent_minutes 内（默认 10 分钟）且有活动
        [STALE]   updatedAt 超过 recent_minutes（疑似卡住/超时，需人工查 history）
        [IDLE]    无消息历史
    - 标记必须精确匹配（独占最后一行）；正文里提到 [DONE] 不算完成
    - 只读分析，零外部依赖，Windows / macOS 双平台通用

示例:
    python check_status.py sessions.json
    python check_status.py sessions.json --task agent:xiaoguang:direct:ou_xxx
    python check_status.py sessions.json --recent-minutes 15 --json
"""
import argparse
import json
import sys
import time

DONE_MARK = "[DONE]"
FAILED_MARK = "[FAILED]"


# 只认这类角色发言（子 agent 的回复）
ASSISTANT_ROLES = ("assistant", "agent")
# 派发提示所在角色：其后的消息才算「本次运行」
DISPATCH_ROLES = ("user", "human")


def _text_of(content):
    """把 message.content 归一成纯文本（兼容字符串 / 块数组）。"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(str(c.get("text", "")) for c in content if isinstance(c, dict))
    return ""


def extract_messages_text(messages):
    """提取**本次派发运行**里最后一条 assistant 文本。

    两个限制（原先都没有，导致误判）：
      1. **只认 assistant / agent 角色** —— 用户消息、工具结果、system 提示
         都不代表子 agent 的产出，不能用来判定完成/失败
      2. **只取最后一条派发提示之后的消息** —— 排除更早几轮运行的历史回复，
         避免拿上一次任务的 [DONE] 当本次结论
    """
    if not messages:
        return ""
    start = 0
    for i, m in enumerate(messages):
        if isinstance(m, dict) and str(m.get("role", "")).lower() in DISPATCH_ROLES:
            start = i + 1
    for m in reversed(messages[start:]):
        if not isinstance(m, dict):
            continue
        if str(m.get("role", "")).lower() not in ASSISTANT_ROLES:
            continue
        text = _text_of(m.get("content", ""))
        if text.strip():
            return text.strip()
    return ""


def has_terminal_marker(text, mark):
    """标记必须**独占最后一行**（精确匹配），不接受正文里任意位置出现。

    理由：正文里提到 "[DONE]"（讨论格式、引用别人输出）不应被当成完成信号；
    只认「最后一行就是这个标记」的显式收尾。
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return bool(lines) and lines[-1] == mark


def judge(session, recent_minutes):
    """判定单会话状态（结构化状态优先，文本标记次之）。"""
    messages = session.get("messages") or []
    if not messages:
        return "IDLE", ""      # 无消息历史：既未派发也无产出，不能算 RUNNING
    last_text = extract_messages_text(messages)
    updated = session.get("updatedAt") or 0
    now_ms = time.time() * 1000
    fresh = (now_ms - updated) < recent_minutes * 60 * 1000

    # 1) 结构化状态（若 sessions_list 直接给了）优先
    structured = str(session.get("status") or "").lower()
    if structured in ("done", "completed", "success"):
        return "DONE", f"(structured status: {structured}) {last_text[-160:]}".strip()
    if structured in ("failed", "error", "aborted"):
        return "FAILED", f"(structured status: {structured}) {last_text[-160:]}".strip()

    # 2) 文本标记：精确的最后一行
    if has_terminal_marker(last_text, DONE_MARK):
        return "DONE", last_text[-200:]
    if has_terminal_marker(last_text, FAILED_MARK):
        return "FAILED", last_text[-200:]

    if updated and fresh:
        return "RUNNING", last_text[-200:]
    if updated:
        return "STALE", last_text[-200:]
    return "IDLE", ""


def main():
    ap = argparse.ArgumentParser(description="Summarize sub-task status from sessions_list output")
    ap.add_argument("input", help="sessions_list JSON 文件，或 - 读 stdin")
    ap.add_argument("--task", action="append", default=None,
                    help="只显示指定 sessionKey（可多次）")
    ap.add_argument("--recent-minutes", type=int, default=10,
                    help="RUNNING 判定窗口（默认 10 分钟）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        with open(args.input, "r", encoding="utf-8-sig") as f:
            raw = f.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[FAIL] invalid JSON: {e}")
        sys.exit(1)

    sessions = data if isinstance(data, list) else data.get("sessions") or data.get("items") or []
    if not isinstance(sessions, list):
        print("[FAIL] cannot find session list in input")
        sys.exit(1)

    task_filter = set(args.task or [])
    rows = []
    for s in sessions:
        key = s.get("key") or s.get("sessionKey") or ""
        if task_filter and key not in task_filter:
            continue
        status, tail = judge(s, args.recent_minutes)
        updated = s.get("updatedAt") or 0
        age_min = int((time.time() * 1000 - updated) / 60000) if updated else -1
        rows.append({
            "key": key,
            "kind": s.get("kind", ""),
            "updatedAgeMin": age_min,
            "status": status,
            "tail": tail,
        })

    if args.json:
        print(json.dumps({"count": len(rows), "rows": rows}, ensure_ascii=False, indent=2))
    else:
        for r in rows:
            print(f"[{r['status']:7s}] {r['key']}  (updated {r['updatedAgeMin']}m ago)")
            if r["tail"]:
                print(f"         {r['tail']}")
        if not rows:
            print("(no matching sessions)")

    failed = [r for r in rows if r["status"] == "FAILED"]
    sys.exit(2 if failed else 0)


if __name__ == "__main__":
    main()
