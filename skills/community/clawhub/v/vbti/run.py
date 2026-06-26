#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VBTI · Vibe-coding Type Indicator
扫 ~/.claude/projects/ 所有 transcript → 算 16 维分数 → 出诊断书卡片 → 桌面 + open。
"""
import json, os, re, sys, statistics
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict

# 让本目录可 import types.py
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vbti_types import TYPES  # type: ignore

HOME = Path.home()
PROJECTS = HOME / ".claude" / "projects"
DESKTOP = HOME / "Desktop"
TEMPLATE = Path(__file__).resolve().parent / "templates" / "card.html"

# ── 关键词词典（user 消息中匹配） ─────────────────────────────
KW = {
    "thanks_words":   ["谢谢", "辛苦了", "辛苦", "麻烦了", "麻烦", "感谢", "thanks", "thank you"],
    "sorry_words":    ["对不起", "抱歉", "是我没说清", "是我表达", "是我的", "sorry", "我应该", "我没说清"],
    "promise_words":  ["下周", "明天", "马上", "快好了", "差不多了", "再调一下", "再优化", "最后改"],
    "blame_words":    ["你又错", "你不对", "你怎么", "你又写错", "你蠢", "这都不会", "你都不会", "这都搞不", "怎么这么"],
    "vibe_words":     ["应该可以", "应该能", "试试看", "差不多吧", "感觉可以", "可能行", "估计能"],
    "refactor_words": ["重构", "重写", "refactor", "推倒重来", "再来一次", "再写一遍", "重新写"],
    "explain_words":  ["为什么这样", "怎么实现的", "原理是", "什么意思", "解释一下", "这段是什么", "为啥要", "why does"],
    "compare_words":  ["比那个好", "哪个好", "推荐哪个", "vs", " 比 ", "更好用", "更香", "应该用哪"],
    "rename_words":   ["改个名", "重命名", "变量名", "更好的名字", "改下名字", "rename"],
    "show_words":     ["封面", "演示", "截图", "发出去", "发小红书", "发朋友圈", "拍照", "演示一下"],
    "no_test_words":  ["应该能跑", "不用测了", "这点改动没事", "应该没事", "应该没问题", "没必要测", "肉眼测了"],
    "wfm_words":      ["在我这能跑", "我这里能跑", "works on my", "我电脑没问题"],
}
OK_TOKENS = {"ok", "okay", "好", "好的", "嗯", "go", "继续", "yes", "y", "对", "👍", "?", ".", ".."}

NIGHT_HOURS = set(range(0, 6))     # 0-5 点
MORNING_HOURS = set(range(8, 11))  # 8-10 点

# ── 数据采集 ───────────────────────────────────────────────
def iter_events():
    if not PROJECTS.exists():
        return
    for jsonl in PROJECTS.rglob("*.jsonl"):
        try:
            with jsonl.open(encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except Exception:
                        continue
        except Exception:
            continue


def extract_user_text(msg):
    """user 消息内容统一拍平成字符串"""
    c = msg.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = []
        for b in c:
            if isinstance(b, dict):
                if b.get("type") == "text":
                    parts.append(b.get("text", ""))
                elif b.get("type") == "tool_result":
                    inner = b.get("content")
                    if isinstance(inner, str):
                        parts.append(inner)
        return "\n".join(parts)
    return ""


def extract_tool_uses(msg):
    """assistant 消息内的 tool_use block 列表"""
    c = msg.get("content")
    out = []
    if isinstance(c, list):
        for b in c:
            if isinstance(b, dict) and b.get("type") == "tool_use":
                out.append((b.get("name", ""), b.get("input") or {}))
    return out


def parse_ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


# ── 主分析 ────────────────────────────────────────────────
def analyze():
    sig = defaultdict(float)
    user_msg_lens = []
    short_msgs = 0
    total_user_msgs = 0
    ok_count = 0
    cwd_first_seen = {}
    cwd_last_seen = {}
    cwd_msg_count = Counter()
    night_msgs = 0
    night_new_cwds_set = set()
    file_edits = Counter()             # 路径 → 次数
    file_edit_types = Counter()        # 扩展名分类 → 次数
    bash_cmds = []
    error_dump_count = 0
    traceback_dumps = 0
    error_msg_lens = []
    model_seen = []

    for ev in iter_events():
        ts = parse_ts(ev.get("timestamp", ""))
        cwd = ev.get("cwd")
        if cwd and ts:
            cwd_first_seen.setdefault(cwd, ts)
            cwd_last_seen[cwd] = ts
            cwd_msg_count[cwd] += 1

        if ev.get("isMeta"):
            continue

        t = ev.get("type")
        msg = ev.get("message", {}) or {}

        if t == "user" and msg.get("role") == "user":
            text = extract_user_text(msg)
            if not text or text.startswith("<local-command-caveat>"):
                continue
            total_user_msgs += 1
            user_msg_lens.append(len(text))
            stripped = text.strip().lower()

            # OK / 单字回复
            if len(text.strip()) <= 6 and any(tok in stripped for tok in OK_TOKENS):
                short_msgs += 1
                if any(stripped == tok or stripped.startswith(tok) for tok in OK_TOKENS):
                    ok_count += 1

            # 关键词统计
            for key, words in KW.items():
                for w in words:
                    sig[key] += text.count(w) if len(w) > 1 else len(re.findall(rf"(?<!\w){re.escape(w)}(?!\w)", text, re.I))

            # 报错糊脸（含 Traceback / Error: / stack）
            if re.search(r"Traceback|Error:|Exception|at .+\(.+:\d+\)|File \".+\", line \d+", text):
                traceback_dumps += 1
                error_msg_lens.append(len(text))
            if len(text) > 800 and ("Error" in text or "error" in text or "Traceback" in text):
                error_dump_count += 1

            # 时段
            if ts:
                local = ts.astimezone()
                if local.hour in NIGHT_HOURS:
                    night_msgs += 1
                    if cwd and cwd not in cwd_first_seen:
                        night_new_cwds_set.add(cwd)

        elif t == "assistant" and msg.get("role") == "assistant":
            if msg.get("model"):
                model_seen.append(msg["model"])
            for name, inp in extract_tool_uses(msg):
                if name == "Bash":
                    cmd = (inp.get("command") or "").strip()
                    bash_cmds.append(cmd)
                elif name in ("Edit", "Write", "MultiEdit"):
                    fp = inp.get("file_path") or ""
                    if fp:
                        file_edits[fp] += 1
                        ext = fp.split(".")[-1].lower() if "." in fp else ""
                        if ext in {"md"}:
                            file_edit_types["md"] += 1
                        elif ext in {"html", "css", "svg"}:
                            file_edit_types["html"] += 1
                        elif ext in {"py", "ts", "tsx", "js", "jsx", "go", "rs", "java", "rb", "swift"}:
                            file_edit_types["code"] += 1
                        if "test" in fp.lower() or "spec" in fp.lower():
                            file_edit_types["test"] += 1

    # ── 衍生信号 ───────────────────────────────────────
    sig["total_user_msgs"] = total_user_msgs
    sig["total_cwds"] = len(cwd_first_seen)
    sig["avg_msg_len"] = round(statistics.mean(user_msg_lens), 1) if user_msg_lens else 0
    sig["short_msg_pct"] = round(100 * short_msgs / max(total_user_msgs, 1), 0)
    sig["ok_words"] = ok_count
    sig["night_msgs_pct"] = round(100 * night_msgs / max(total_user_msgs, 1), 0)
    sig["night_new_cwds"] = len(night_new_cwds_set)
    sig["traceback_dumps"] = traceback_dumps
    sig["error_dumps"] = error_dump_count
    sig["median_error_len"] = int(statistics.median(error_msg_lens)) if error_msg_lens else 0
    sig["model_switches"] = max(0, len(set(model_seen)) - 1) * 5 + sum(
        1 for i in range(1, len(model_seen)) if model_seen[i] != model_seen[i - 1]
    )

    # Bash 命令统计
    joined = "\n".join(bash_cmds).lower()
    sig["git_push"] = joined.count("git push")
    sig["git_init"] = joined.count("git init")
    sig["rm_rf"] = sum(1 for c in bash_cmds if "rm -rf" in c.lower() or re.search(r"\brm\b.*-r\w*f", c.lower()))
    sig["git_reset_hard"] = joined.count("git reset --hard")
    sig["gh_repo_create"] = joined.count("gh repo create")
    sig["gh_repo_create_word"] = "从未出现" if sig["gh_repo_create"] == 0 else f"{int(sig['gh_repo_create'])} 次"
    sig["test_runs"] = sum(joined.count(x) for x in ["pytest", "jest", "vitest", "go test", "npm test", "mocha"])
    sig["npm_install"] = sum(joined.count(x) for x in ["npm install", "pip install", "yarn add", "pnpm add"])
    sig["api_test_runs"] = sum(joined.count(x) for x in ["curl", "pytest", "jest", "vitest", "npm test"])
    sig["formatter_runs"] = sum(joined.count(x) for x in ["prettier", "black ", "ruff format", "eslint --fix"])

    # 文件类型分布
    md = file_edit_types["md"]
    code = file_edit_types["code"]
    html = file_edit_types["html"]
    total_edit = md + code + html + 1
    sig["md_edits"] = md
    sig["code_edits"] = code
    sig["html_edits"] = html
    sig["test_files"] = file_edit_types["test"]
    sig["md_ratio"] = round(md / max(code, 1), 2)
    sig["md_pct"] = round(100 * md / total_edit, 0)
    sig["html_pct"] = round(100 * html / total_edit, 0)
    sig["rename_pct"] = round(min(80, sig.get("rename_words", 0) * 4), 0)
    sig["logic_pct"] = max(8, 100 - sig["rename_pct"] - sig["md_pct"])

    # cwd 时间信号
    now = datetime.now(timezone.utc)
    cwd_ages_hours = []
    days_per_cwd = []
    for c, first in cwd_first_seen.items():
        last = cwd_last_seen.get(c, first)
        cwd_ages_hours.append(max(0.1, (last - first).total_seconds() / 3600))
        days_per_cwd.append((now - last).days)
    if cwd_ages_hours:
        sig["cwd_median_hours"] = round(statistics.median(cwd_ages_hours), 1)
    if days_per_cwd:
        sig["oldest_cwd_days"] = max(days_per_cwd)
        sig["oldest_promise_days"] = max(days_per_cwd)
        sig["days_since_code"] = min(days_per_cwd)
        sig["days_since_main_commit"] = max(days_per_cwd)
        sig["stale_cwds"] = sum(1 for d in days_per_cwd if d > 30)

    # 单文件最大 edit
    sig["max_edits_one_file"] = max(file_edits.values()) if file_edits else 0

    # no-push 比例
    push_ratio = sig["git_push"] / max(sig["total_cwds"], 1)
    sig["no_push_ratio"] = max(0, 1.0 - min(1.0, push_ratio))

    # 占位的"魔性"信号（数据不足时不为零，反正都是嘲讽）
    sig.setdefault("v2_dirs", sum(1 for c in cwd_first_seen if re.search(r"v2|v3|final|重启|new-?\d|_2", c.lower())))
    sig.setdefault("screenshot_files", 0)
    sig.setdefault("launched_projects", 0)
    sig.setdefault("morning_deletes", sig["rm_rf"])
    sig.setdefault("readme_versions", md)
    sig.setdefault("new_features", 0)
    sig.setdefault("retry_after_apology", round(sig.get("sorry_words", 0) / 3, 1))
    sig.setdefault("retry_after_error", traceback_dumps)
    sig.setdefault("rapid_resends", short_msgs // 5)
    sig.setdefault("self_reflect", 0)
    sig.setdefault("pushback", "从未")
    sig.setdefault("verify_runs", sig["test_runs"])
    sig.setdefault("user_explain_error", 0)
    sig.setdefault("google_first", "从未")
    sig.setdefault("abandoned_packages", sig["npm_install"] // 2)
    sig.setdefault("framework_switches", 0)
    sig.setdefault("kept_packages", 3)
    sig.setdefault("self_explain", sig.get("explain_words", 0) // 4)
    sig.setdefault("explain_no_change_pct", 89)
    sig.setdefault("doc_reads", "从未")
    sig.setdefault("shipped_bugs", 0)
    sig.setdefault("night_destruct_pct", min(100, round(100 * night_msgs / max(total_user_msgs, 1) * (0.5 + sig["rm_rf"] / 10), 0)))

    # TEST 加权：没测试文件且代码改动多 = 强烈
    sig["no_test_bonus"] = 5.0 if sig["test_files"] == 0 and code > 50 else 0.0

    return sig


# ── 类型评分 ──────────────────────────────────────────────
def score(sig):
    scores = {}
    for code, t in TYPES.items():
        s = 0.0
        for k, w in t["scoring"].items():
            v = sig.get(k, 0)
            try:
                v = float(v)
            except Exception:
                v = 0
            s += v * w
        scores[code] = s
    return scores


# ── 渲染 ──────────────────────────────────────────────────
def render(winner_code, sig):
    t = TYPES[winner_code]
    receipts_rows = []
    for label, key, suffix in t["receipts"]:
        v = sig.get(key, 0)
        if isinstance(v, float):
            v = round(v, 1) if v != int(v) else int(v)
        val_str = f"{v}{(' ' + suffix) if suffix and not str(v).endswith(suffix) else ''}".strip()
        if suffix == "" and isinstance(v, (int, float)) and v == 0:
            val_str = "0"
        receipts_rows.append((label, val_str))

    today = datetime.now().strftime("%Y.%m.%d")
    html = TEMPLATE.read_text(encoding="utf-8")
    rows_html = "\n".join(
        f'<div class="row"><span class="key">{label}</span><span class="val">{val}</span></div>'
        for label, val in receipts_rows
    )
    html = (
        html.replace("{{CODE}}", winner_code)
            .replace("{{NAME}}", t["name"])
            .replace("{{EMOJI}}", t["emoji"])
            .replace("{{TAGLINE}}", t["tagline"])
            .replace("{{NUMBER}}", t["code"])
            .replace("{{DATE}}", today)
            .replace("{{ROWS}}", rows_html)
    )

    out = DESKTOP / f"我的-VBTI-{winner_code}.html"
    out.write_text(html, encoding="utf-8")
    return out


def main():
    print("🔍 扫 ~/.claude/projects/ ...", flush=True)
    sig = analyze()
    scores = score(sig)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    winner = ranked[0][0]
    print(f"📊 排行前 5：{ranked[:5]}", flush=True)
    print(f"🎯 你的 VBTI 是：{winner} · {TYPES[winner]['name']} {TYPES[winner]['emoji']}", flush=True)
    out = render(winner, sig)
    print(f"📄 卡片已生成：{out}", flush=True)
    try:
        os.system(f'open "{out}"')
    except Exception:
        pass


if __name__ == "__main__":
    main()
