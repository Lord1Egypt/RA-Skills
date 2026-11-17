"""
微信聊天记录分析脚本 V3
用法:
  python analyze_chat.py --chat "联系人昵称" --limit 500     # 历史分析
  python analyze_chat.py --chat "联系人" --limit 30 --mode realtime  # 实时分析
  python analyze_chat.py --whoishot                          # 扫活跃会话
  python analyze_chat.py --feedback <suggestion_id> <rating>  # 反馈记录

改进：V3 - 回复间隔分析 | 公众号过滤 | 趋势对比 | 导出缓存 | Python自动检测 | 反馈闭环
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time as time_module
from collections import defaultdict
from datetime import datetime, timedelta


# ─── 路径工具 ───────────────────────────────────────────────────────────
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")
CACHE_FILE = os.path.join(DATA_DIR, "export_cache.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.json")

OFFICIAL_WXID_PREFIXES = ("gh_",)
OFFICIAL_WXID_EXACT = ("brandsessionholder", "brandservicesessionholder", "notifymessage", "weixin")
CACHE_TTL = 60  # 导出缓存有效期（秒）


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def find_python():
    """自动检测可用的 Python 解释器"""
    for name in ["python3", "python"]:
        p = shutil.which(name)
        if p:
            return p
    # QClaw inner Python
    qclaw_py = shutil.which("python", path=os.path.join(os.environ.get("LOCALAPPDATA", ""), "qclaw"))
    if qclaw_py:
        return qclaw_py
    # Common install paths
    candidates = [
        os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Programs", "Python",
                     f"Python{ver}", "python.exe")
        for ver in ["312", "311", "310", "39", "38"]
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return "python"


def find_wechat_cli():
    """自动检测 wechat-cli"""
    exe = shutil.which("wechat-cli")
    if exe:
        return exe
    # Try alongside discovered Python
    py_dir = os.path.dirname(find_python())
    scripts = os.path.join(py_dir, "Scripts", "wechat-cli.exe")
    if os.path.exists(scripts):
        return scripts
    return "wechat-cli"


# ─── CLI 调用（文件中转，防 cp1252） ────────────────────────────────────

def run_cli_to_file(args):
    """运行 wechat-cli，输出写入临时文件，返回内容字符串"""
    exe = find_wechat_cli()
    ident = hashlib.md5(str(args).encode()).hexdigest()[:8]
    temp_path = os.path.join(tempfile.gettempdir(), f"_wct_{os.getpid()}_{ident}.txt")
    cmd = [exe] + args
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    with open(temp_path, "w", encoding="utf-8") as f:
        r = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE,
                           text=True, encoding="utf-8", errors="replace",
                           env=env)
    with open(temp_path, "r", encoding="utf-8") as f:
        content = f.read()
    try:
        os.unlink(temp_path)
    except OSError:
        pass
    stderr_text = r.stderr or ""
    if r.returncode != 0 and "消息数量" not in content and "消息数量" not in stderr_text:
        print(f"[WARN] wechat-cli 返回码 {r.returncode}", file=sys.stderr)
    return content, stderr_text


# ─── 导出缓存 ──────────────────────────────────────────────────────────

def _cache_key(chat_target, limit):
    return f"{chat_target}|{limit}"


def get_cached_export(chat_target, limit):
    """检查是否有未过期的导出缓存"""
    ensure_data_dir()
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    key = _cache_key(chat_target, limit)
    entry = cache.get(key)
    if not entry:
        return None
    if time_module.time() - entry.get("ts", 0) > CACHE_TTL:
        return None
    return entry.get("raw")


def set_cached_export(chat_target, limit, raw_content):
    """保存导出缓存"""
    ensure_data_dir()
    key = _cache_key(chat_target, limit)
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
        else:
            cache = {}
    except (json.JSONDecodeError, OSError):
        cache = {}
    cache[key] = {"ts": time_module.time(), "raw": raw_content}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)


# ─── 联系人 ────────────────────────────────────────────────────────────

def search_contacts(keyword):
    """搜索联系人，返回 [(remark, wxid, nick_name), ...]"""
    raw, _ = run_cli_to_file(["contacts", "--query", keyword])
    if not raw or not raw.strip():
        return []
    try:
        data = json.loads(raw)
        results = []
        for c in data:
            remark = c.get("remark", "")
            nick = c.get("nick_name", "")
            username = c.get("username", "")
            results.append((remark or nick or username, username, nick))
        return results
    except (json.JSONDecodeError, TypeError):
        return []


def is_official_account(session):
    """判断是否是公众号/服务号/订阅号"""
    chat = session.get("chat", "")
    wxid = session.get("username", "")
    if wxid.startswith(OFFICIAL_WXID_PREFIXES):
        return True
    if wxid in OFFICIAL_WXID_EXACT:
        return True
    if "@placeholder" in chat:
        return True
    return False


# ─── 导出 ──────────────────────────────────────────────────────────────

def export_chat(chat_target, limit=500):
    """导出聊天记录（带缓存）"""
    cached = get_cached_export(chat_target, limit)
    if cached:
        print(f"[缓存] 使用最近 {CACHE_TTL}s 内的缓存", file=sys.stderr)
        return cached, "(cached)"
    raw, stderr = run_cli_to_file([
        "export", chat_target,
        "--format", "markdown",
        "--limit", str(limit),
    ])
    if raw and len(raw.strip()) >= 30:
        set_cached_export(chat_target, limit, raw)
    return raw, stderr


def resolve_contact(name_or_wxid, limit=500):
    """尝试用名字导出；失败则自动搜 wxid。返回 (最终调用名, 原始内容)"""
    raw, stderr = export_chat(name_or_wxid, limit)
    if raw and len(raw.strip()) >= 30:
        return name_or_wxid, raw

    print(f"直接导出失败，尝试搜索联系人...", file=sys.stderr)
    contacts = search_contacts(name_or_wxid)
    if not contacts:
        print(f"未找到联系人 [{name_or_wxid}]", file=sys.stderr)
        print(f"\n请用以下命令确认联系人名称：", file=sys.stderr)
        print(f"  wechat-cli sessions --limit 20 --format text > temp.txt", file=sys.stderr)
        print(f"  wechat-cli contacts --query \"<关键词>\" > temp.txt", file=sys.stderr)
        return None, None

    if len(contacts) == 1:
        remark, wxid, nick = contacts[0]
        print(f"找到联系人: [{remark}] (wxid: {wxid})", file=sys.stderr)
        raw, stderr = export_chat(wxid, limit)
        return wxid, raw
    else:
        print(f"找到多个联系人:", file=sys.stderr)
        for i, (remark, wxid, nick) in enumerate(contacts):
            print(f"  [{i}] {remark} | wxid: {wxid} | 昵称: {nick}", file=sys.stderr)
        idx = input("请选择序号: ").strip()
        try:
            remark, wxid, nick = contacts[int(idx)]
            raw, stderr = export_chat(wxid, limit)
            return wxid, raw
        except (ValueError, IndexError):
            print("无效选择", file=sys.stderr)
            return None, None


# ─── 解析 ──────────────────────────────────────────────────────────────

def parse_messages(markdown_text):
    """解析 markdown 聊天记录"""
    messages = []
    body = False
    for line in markdown_text.split("\n"):
        stripped = line.strip()
        if not body:
            if stripped == "---":
                body = True
            continue
        if not stripped.startswith("-"):
            continue
        content = stripped[1:].strip()
        m = re.match(r"\[([^\]]+)\]\s*([^:]+):\s*(.*)", content)
        if m:
            time_str, sender, msg = m.groups()
            messages.append({
                "time_str": time_str.strip(),
                "sender": sender.strip(),
                "content": msg.strip(),
                "timestamp": None,
            })
    return messages


def parse_timestamps(messages):
    """尝试解析消息时间戳"""
    for m in messages:
        ts = None
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]:
            try:
                ts = datetime.strptime(m["time_str"].strip(), fmt)
                break
            except ValueError:
                continue
        m["timestamp"] = ts


# ─── 分析引擎 ──────────────────────────────────────────────────────────

def compute_reply_intervals(messages):
    """
    计算回复间隔。
    返回 dict:
      total_pairs: 总对话轮次
      pairs_by_replier: {replier: [间隔秒数, ...]}
      gaps: [{"replier", "reply_to", "interval_sec", "reply_content"}, ...]
    """
    timed = [m for m in messages if m["timestamp"]]
    if len(timed) < 2:
        return {"total_pairs": 0, "pairs_by_replier": {}, "gaps": []}

    timed.sort(key=lambda m: m["timestamp"])
    # 按发送时间分"轮"：同一人的连续发送算同一轮
    pairs = []  # [(sender, receiver, ts_start, ts_end, content), ...]
    prev_sender = None
    prev_ts = None
    prev_content = ""

    for m in timed:
        if prev_sender is not None and m["sender"] != prev_sender:
            # 对方回复了
            delta = (m["timestamp"] - prev_ts).total_seconds()
            pairs.append((m["sender"], prev_sender, delta, m["content"]))
        prev_sender = m["sender"]
        prev_ts = m["timestamp"]
        prev_content = m["content"]

    # 按回复者分组
    by_replier = defaultdict(list)
    gap_details = []
    for replier, reply_to, sec, content in pairs:
        by_replier[replier].append(sec)
        gap_details.append({
            "replier": replier,
            "reply_to": reply_to,
            "interval_sec": round(sec, 1),
            "interval_label": format_interval(sec),
            "reply_content": content[:60],
        })

    return {
        "total_pairs": len(pairs),
        "pairs_by_replier": dict(by_replier),
        "gaps": gap_details,
    }


def format_interval(sec):
    if sec < 60:
        return f"{int(sec)}秒"
    elif sec < 3600:
        return f"{int(sec // 60)}分{int(sec % 60)}秒"
    else:
        return f"{int(sec // 3600)}小时{int((sec % 3600) // 60)}分"


def interval_stats(sec_list):
    if not sec_list:
        return {"avg": None, "min": None, "max": None, "median": None, "count": 0}
    s = sorted(sec_list)
    n = len(s)
    return {
        "avg": round(sum(s) / n, 1),
        "min": round(s[0], 1),
        "max": round(s[-1], 1),
        "median": round(s[n // 2], 1) if n % 2 == 1 else round((s[n // 2 - 1] + s[n // 2]) / 2, 1),
        "count": n,
    }


def analyze(messages):
    """全量统计 + 回复间隔"""
    if not messages:
        return {}

    parse_timestamps(messages)

    senders = defaultdict(lambda: {"count": 0, "chars": 0})
    media_kw = ["[图片]", "[表情]", "[语音]", "[视频]", "[红包]", "[文件]"]
    for m in messages:
        s = m["sender"]
        senders[s]["count"] += 1
        senders[s]["chars"] += len(m["content"])
        m["is_media"] = any(kw in m["content"] for kw in media_kw)

    media_count = sum(1 for m in messages if m.get("is_media"))

    valid = [m["timestamp"] for m in messages if m["timestamp"]]
    first = min(valid) if valid else None
    last = max(valid) if valid else None
    days = (last - first).days + 1 if first and last else 1

    hour_dist = defaultdict(int)
    for m in messages:
        if m["timestamp"]:
            hour_dist[m["timestamp"].hour] += 1

    # 回复间隔分析（Fix 1）
    intervals = compute_reply_intervals(messages)
    interval_summary = {}
    for replier, secs in intervals["pairs_by_replier"].items():
        interval_summary[replier] = interval_stats(secs)

    return {
        "total": len(messages),
        "senders": dict(senders),
        "media_count": media_count,
        "first_time": first,
        "last_time": last,
        "days_span": days,
        "avg_per_day": round(len(messages) / max(days, 1), 1),
        "hour_dist": dict(hour_dist),
        "intervals": intervals,
        "interval_summary": interval_summary,
    }


# ─── 趋势分析（Fix 3） ────────────────────────────────────────────────

def load_history():
    ensure_data_dir()
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_history(contact_id, date_str, stats_snapshot):
    history = load_history()
    if contact_id not in history:
        history[contact_id] = []
    history[contact_id].append({"date": date_str, "stats": stats_snapshot})
    # 每条联系人最多保存 10 条快照
    history[contact_id] = history[contact_id][-10:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, default=str)


def build_trend_section(contact_id, current_stats):
    """与上次分析比较，返回趋势文本"""
    history = load_history()
    snapshots = history.get(contact_id, [])
    if len(snapshots) < 1:
        return "", False

    last = snapshots[-1]["stats"]
    prev_total = last.get("total", 0)
    curr_total = current_stats["total"]

    parts = []
    # 消息量变化
    if prev_total > 0 and curr_total != prev_total:
        diff = curr_total - prev_total
        pct = round(diff / prev_total * 100, 1)
        direction = "↑" if diff > 0 else "↓"
        parts.append(f"消息量对比上次: {prev_total}条 → {curr_total}条 {direction}{abs(pct)}%")

    # 回复间隔变化
    prev_intervals = last.get("interval_summary", {})
    curr_intervals = current_stats.get("interval_summary", {})
    for replier in set(list(prev_intervals.keys()) + list(curr_intervals.keys())):
        p_avg = prev_intervals.get(replier, {}).get("avg")
        c_avg = curr_intervals.get(replier, {}).get("avg")
        if p_avg and c_avg and abs(c_avg - p_avg) > 5:
            direction = "↑（变慢）" if c_avg > p_avg else "↓（变快）"
            parts.append(f"{replier} 平均回复: {p_avg:.0f}s → {c_avg:.0f}s {direction}")

    # 天数跨度
    prev_days = last.get("days_span", 0)
    curr_days = current_stats.get("days_span", 0)
    if prev_days > 0 and curr_days > prev_days:
        parts.append(f"聊天覆盖天数: {prev_days}d → {curr_days}d ↑{curr_days - prev_days}d")

    return "\n".join(parts), len(parts) > 0


# ─── 反馈闭环（Fix 7） ────────────────────────────────────────────────

def record_feedback(suggestion_id, rating):
    """记录对某条建议的反馈"""
    ensure_data_dir()
    try:
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                fb = json.load(f)
        else:
            fb = []
    except (json.JSONDecodeError, OSError):
        fb = []
    fb.append({
        "id": suggestion_id,
        "rating": rating,
        "ts": time_module.time(),
    })
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(fb, f, ensure_ascii=False)
    print(f"已记录反馈: {suggestion_id} → {rating}")


# ─── 活跃会话扫描（Fix 2: 公众号过滤） ────────────────────────────────

def who_is_hot(min_minutes=5, limit=50):
    """扫描当前活跃的私聊会话（已过滤公众号）"""
    raw, _ = run_cli_to_file(["sessions", "--limit", str(limit), "--format", "json"])
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        print("[who is hot] 无法解析 sessions 数据", file=sys.stderr)
        return []

    now = time_module.time()
    results = []
    for s in data:
        if is_official_account(s):
            continue
        if s.get("is_group", False):
            continue
        ts = s.get("timestamp", 0)
        unread = s.get("unread", 0)
        if unread > 0 or (ts > now - min_minutes * 60):
            last_msg = s.get("last_message", "")[:50]
            results.append({
                "chat": s.get("chat", ""),
                "wxid": s.get("username", ""),
                "unread": unread,
                "active_minutes_ago": round((now - ts) / 60, 1) if ts else None,
                "last_message": last_msg,
            })
    return results


# ─── 输出 ──────────────────────────────────────────────────────────────

def write_utf8(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_report(stats):
    """构建分析报告（不含原始聊天记录，仅统计）"""
    lines = []

    # ── 基础统计 ──
    lines.append(f"**总消息数：** {stats['total']} 条")
    if stats["first_time"]:
        lines.append(f"**聊天跨度：** {stats['first_time'].strftime('%Y-%m-%d')} ~ {stats['last_time'].strftime('%Y-%m-%d')}（约 {stats['days_span']} 天）")
    lines.append(f"**日均消息：** {stats['avg_per_day']} 条")
    lines.append(f"**含媒体消息：** {stats['media_count']} 条\n")

    # ── 消息分布 ──
    lines.append("## 消息分布")
    for sender, data in stats["senders"].items():
        pct = data["count"] / stats["total"] * 100
        lines.append(f"- **{sender}**：{data['count']} 条（{pct:.1f}%）| 总字数 {data['chars']}")
    lines.append("")

    # ── 时段分布 ──
    buckets = {"凌晨(0-6)": 0, "上午(6-12)": 0, "下午(12-18)": 0, "晚上(18-24)": 0}
    for h, cnt in stats["hour_dist"].items():
        if 0 <= h < 6:
            buckets["凌晨(0-6)"] += cnt
        elif 6 <= h < 12:
            buckets["上午(6-12)"] += cnt
        elif 12 <= h < 18:
            buckets["下午(12-18)"] += cnt
        else:
            buckets["晚上(18-24)"] += cnt
    lines.append("## 聊天时段分布")
    for period, cnt in buckets.items():
        if stats["total"] > 0:
            lines.append(f"- {period}：{cnt} 条（{cnt / stats['total'] * 100:.1f}%）")
    lines.append("")

    # ── 回复间隔分析（Fix 1） ──
    lines.append("## 回复间隔分析")
    summary = stats.get("interval_summary", {})
    if summary:
        for replier, s in summary.items():
            if s["count"] > 0:
                lines.append(
                    f"- **{replier}** 回复对方：平均 {s['avg']:.0f}s | 中位数 {s['median']:.0f}s | "
                    f"最快 {s['min']:.0f}s | 最慢 {s['max']:.0f}s | 共 {s['count']} 次"
                )
    else:
        lines.append("- 数据不足，无法分析回复间隔")
    lines.append("")

    # ── 回复节奏快照（最近 10 轮） ──
    gaps = stats.get("intervals", {}).get("gaps", [])
    if gaps:
        lines.append("### 最近回复节奏")
        for g in gaps[-10:]:
            icon = "⚡" if g["interval_sec"] < 60 else "🕐" if g["interval_sec"] < 300 else "🐢"
            lines.append(f"- {icon} **{g['replier']}** 隔 {g['interval_label']} 回复 {g['reply_to']}：{g['reply_content']}")
    lines.append("")

    return "\n".join(lines)


# ─── 主流程 ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="微信聊天记录分析 V3")
    parser.add_argument("--chat", help="联系人昵称 或 wxid")
    parser.add_argument("--limit", type=int, default=500, help="消息上限")
    parser.add_argument("--output", help="输出文件路径（可选）")
    parser.add_argument("--whoishot", action="store_true", help="扫描当前活跃私聊")
    parser.add_argument("--mode", choices=["history", "realtime"], default="history",
                        help="分析模式：history(历史)/realtime(实时)")
    parser.add_argument("--feedback", nargs=2, metavar=("ID", "RATING"),
                        help="记录反馈：建议ID + 评价(好/中/差)")
    parser.add_argument("--include-raw", action="store_true", default=True,
                        help="输出中包含原始聊天记录（默认包含）")
    args = parser.parse_args()

    # ── 反馈模式 ──
    if args.feedback:
        record_feedback(args.feedback[0], args.feedback[1])
        return

    # ── whoishot 模式 ──
    if args.whoishot:
        hot = who_is_hot()
        out_path = args.output or os.path.join(tempfile.gettempdir(), f"_wct_report_{os.getpid()}.md")
        if not hot:
            lines = ["# 当前活跃私聊\n", "**当前没有活跃私聊**（最近5分钟无消息 / 无未读）"]
        else:
            lines = ["# 当前活跃私聊\n"]
            for c in hot:
                note = "[未读]" if c["unread"] > 0 else f"[{c['active_minutes_ago']}分钟前]"
                lines.append(f"- **{c['chat']}** {note} {c['last_message']}")
        write_utf8(out_path, "\n".join(lines))
        print(out_path)
        return

    # ── 聊天分析模式 ──
    if not args.chat:
        print("请指定 --chat 或使用 --whoishot", file=sys.stderr)
        sys.exit(1)

    out_path = args.output or os.path.join(tempfile.gettempdir(), f"_wct_report_{os.getpid()}.md")

    # 实时模式：limit 上限 30
    effective_limit = min(args.limit, 30) if args.mode == "realtime" else args.limit
    print(f"正在导出 [{args.chat}] 的聊天记录（{args.mode}模式，{effective_limit}条）...", file=sys.stderr)

    export_target, raw = resolve_contact(args.chat, effective_limit)
    if not raw or len(raw.strip()) < 30:
        print("❌ 导出失败，无数据", file=sys.stderr)
        sys.exit(1)

    messages = parse_messages(raw)
    print(f"解析到 {len(messages)} 条消息", file=sys.stderr)

    stats = analyze(messages)
    today = datetime.now().strftime("%Y-%m-%d")

    # 趋势对比
    trend_text, has_trend = build_trend_section(export_target, stats)
    save_history(export_target, today, {
        "total": stats["total"],
        "days_span": stats["days_span"],
        "interval_summary": {k: v for k, v in stats.get("interval_summary", {}).items()},
    })

    # 构建输出
    lines = []
    lines.append(f"# {export_target} 聊天分析报告")
    if args.mode == "realtime":
        lines.append(f"**模式：** 实时分析（最近 {effective_limit} 条）\n")
    lines.append("")

    if has_trend:
        lines.append("> 📊 **趋势变化**\n> " + trend_text.replace("\n", "\n> "))
        lines.append("")

    lines.append(build_report(stats))

    # 回复建议锚定（Fix 4）：为 AI 准备上下文
    last_msg_time = "未知"
    interval_summary = stats.get("interval_summary", {})
    avg_reply_str = " | ".join(
        f"{r}: {s['avg']:.0f}s" for r, s in interval_summary.items() if s["avg"]
    )
    if stats["last_time"]:
        last_msg_time = stats["last_time"].strftime("%Y-%m-%d %H:%M")
    lines.append("## ⏱ 回复建议时间上下文")
    lines.append(f"- 最后消息时间：{last_msg_time}")
    lines.append(f"- 平均回复间隔：{avg_reply_str or '数据不足'}")
    lines.append(f"- 活跃天数：{stats['days_span']} 天")
    lines.append("")

    if args.include_raw:
        lines.append("\n--- 原始聊天记录 ---")
        lines.append(raw)
        lines.append("--- 原始聊天记录结束 ---")

    write_utf8(out_path, "\n".join(lines))
    print(out_path)


if __name__ == "__main__":
    main()
