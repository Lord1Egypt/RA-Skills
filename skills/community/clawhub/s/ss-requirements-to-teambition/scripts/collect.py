#!/usr/bin/env python3
"""
SS 需求采集脚本 — 零 LLM 消耗
从 SaleSmartly 采集带指定标签的已结束会话，输出 JSON 供 AI 分析

用法: python3 collect.py
配置: 同目录下 config.json
输出: data/ss_sessions_YYYY-MM-DD.json
"""

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(line_buffering=True)
except AttributeError:
    pass

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"

if not CONFIG_PATH.exists():
    print("❌ 未找到 config.json，请先复制 config.example.json 并填入配置")
    print(f"   cp {SCRIPT_DIR / 'config.example.json'} {CONFIG_PATH}")
    sys.exit(1)

CONFIG = json.loads(CONFIG_PATH.read_text())
STATE_PATH = SCRIPT_DIR / "state.json"
OUTPUT_DIR = SCRIPT_DIR / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── SS API 客户端 ────────────────────────────────────
class SSClient:
    def __init__(self, api_key: str, project_id: str):
        import urllib.request
        import urllib.error
        self.api_key = api_key
        self.project_id = project_id
        self.base = "https://api.salesmartly.com"
        self._last_call = 0

    def _get(self, path: str, params: dict = None) -> dict:
        import urllib.request
        import urllib.parse
        elapsed = time.time() - self._last_call
        if elapsed < 0.2:
            time.sleep(0.2 - elapsed)

        url = f"{self.base}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)

        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("User-Agent", "SS-Requirements-Collector/1.0")

        self._last_call = time.time()
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ""
            print(f"   ⚠️ API 错误 {e.code}: {body[:200]}")
            return {}
        except Exception as e:
            print(f"   ⚠️ 请求失败: {e}")
            return {}


# ── 时间窗口 ──────────────────────────────────────────
def get_time_window():
    now = datetime.now()
    end_ts = int(now.timestamp())

    state = json.loads(STATE_PATH.read_text()) if STATE_PATH.exists() else {}
    last_run = state.get("lastRunAt")

    if last_run:
        start_ts = last_run
    else:
        start_ts = int((now - timedelta(hours=24)).timestamp())

    return start_ts, end_ts


def save_state(end_ts: int):
    STATE_PATH.write_text(json.dumps({"lastRunAt": end_ts}, ensure_ascii=False))


# ── 采集逻辑 ──────────────────────────────────────────
def fetch_sessions(client: SSClient, start_ts: int, end_ts: int) -> list:
    start_time = json.dumps({"start": start_ts, "end": end_ts})
    all_sessions = []
    page = 1

    while True:
        resp = client._get("/api/v2/get-session-list", {
            "session_status": "1",
            "start_time": start_time,
            "page": str(page),
            "page_size": "100",
        })
        sessions = resp.get("list", [])
        if not sessions:
            break
        all_sessions.extend(sessions)
        total = resp.get("total", 0)
        if page * 100 >= total:
            break
        page += 1

    return all_sessions


def filter_by_tags(sessions: list, tag_names: set) -> list:
    result = []
    for s in sessions:
        st = s.get("session_tags", "")
        if isinstance(st, str):
            try:
                st = json.loads(st)
            except (json.JSONDecodeError, TypeError):
                continue
        if isinstance(st, list):
            for t in st:
                names = t.get("tag_name", [])
                if any(name in tag_names for name in names):
                    result.append(s)
                    break
    return result


MAX_MESSAGE_PAGES = 5  # 最多拉 5 页（500 条），防止群聊会话消息爆炸


def fetch_messages(client: SSClient, session_id: str, start_ts: int, end_ts: int) -> list:
    """拉取会话消息，限制最大页数 + 客户端时间过滤"""
    resp = client._get("/api/v2/get-message-list", {
        "session_id": session_id,
        "page_size": "100",
    })
    messages = resp.get("list", [])
    total = resp.get("total", 0)

    page = 2
    while len(messages) < total and page <= MAX_MESSAGE_PAGES:
        resp = client._get("/api/v2/get-message-list", {
            "session_id": session_id,
            "page_size": "100",
            "page": str(page),
        })
        batch = resp.get("list", [])
        if not batch:
            break
        messages.extend(batch)
        page += 1

    if total > MAX_MESSAGE_PAGES * 100:
        print(f"   ⚠️ 消息过多（{total}条），仅拉取前 {MAX_MESSAGE_PAGES * 100} 条")

    # 客户端时间过滤：只保留时间窗口内的消息
    parsed = []
    filtered_out = 0
    for m in messages:
        send_time = m.get("send_time", 0)
        # send_time 可能是秒级或毫秒级时间戳，统一转秒
        if send_time > 1e12:
            send_time = send_time / 1000
        if send_time < start_ts or send_time > end_ts:
            filtered_out += 1
            continue

        content_raw = m.get("content", "")
        try:
            content_obj = json.loads(content_raw)
            text = content_obj.get("msg", content_raw)
        except (json.JSONDecodeError, TypeError):
            text = content_raw

        parsed.append({
            "sender_type": m.get("sender_type"),
            "sender": m.get("sender"),
            "text": text,
            "send_time": m.get("send_time"),
            "mid": m.get("mid"),
        })

    if filtered_out:
        print(f"   🔍 过滤 {filtered_out} 条时间窗口外消息，保留 {len(parsed)} 条")

    return parsed


def fetch_customer(client: SSClient, chat_user_id: str, cf_key: str) -> dict:
    resp = client._get("/api/v2/get-contact-list", {
        "chat_user_id": chat_user_id,
        "page_size": "5",
    })
    contacts = resp.get("list", [])
    if not contacts:
        return {"name": "未知", "ss_project_id": ""}

    c = contacts[0]
    cf = c.get("custom_field", {})
    if isinstance(cf, str):
        try:
            cf = json.loads(cf)
        except (json.JSONDecodeError, TypeError):
            cf = {}
    if isinstance(cf, list):
        cf = {}

    ss_project_id = cf.get(cf_key, "") if isinstance(cf, dict) else ""

    return {
        "name": c.get("name", "未知"),
        "chat_user_id": c.get("chat_user_id", ""),
        "ss_project_id": str(ss_project_id) if ss_project_id else "",
    }


# ── 主流程 ────────────────────────────────────────────
def main():
    ss_cfg = CONFIG["ss"]
    tags = ss_cfg["tags"]
    tag_names = {t["name"] for t in tags}
    cf_key = ss_cfg["customFieldKey"]

    start_ts, end_ts = get_time_window()
    start_str = datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M")
    end_str = datetime.fromtimestamp(end_ts).strftime("%Y-%m-%d %H:%M")
    print(f"📅 时间窗口: {start_str} → {end_str}")

    client = SSClient(ss_cfg["apiKey"], ss_cfg["projectId"])

    # 1. 拉取会话
    print("🔍 拉取会话列表...")
    all_sessions = fetch_sessions(client, start_ts, end_ts)
    print(f"   共 {len(all_sessions)} 个会话")

    # 2. 过滤标签
    tagged = filter_by_tags(all_sessions, tag_names)
    tag_names_str = "、".join(t["name"] for t in tags)
    print(f"   🏷️ 含「{tag_names_str}」标签: {len(tagged)} 个")

    if not tagged:
        print("✅ 无匹配会话，结束")
        save_state(end_ts)
        return

    # 3. 拉取聊天记录 + 客户信息
    results = []
    for i, s in enumerate(tagged):
        sid = s.get("session_id", "?")
        cuid = s.get("chat_user_id", "")
        title = s.get("title", "")
        print(f"\n📝 [{i+1}/{len(tagged)}] {sid} ({title})")

        customer = fetch_customer(client, cuid, cf_key)
        print(f"   客户: {customer['name']} | SS项目ID: {customer['ss_project_id']}")

        messages = fetch_messages(client, sid, start_ts, end_ts)
        print(f"   消息: {len(messages)} 条（时间窗口内）")

        results.append({
            "session_id": sid,
            "chat_user_id": cuid,
            "title": title,
            "customer_name": customer["name"],
            "ss_project_id": customer["ss_project_id"],
            "start_time": s.get("start_time", 0),
            "end_time": s.get("end_time", 0),
            "msg_count": len(messages),
            "messages": messages,
        })

        time.sleep(0.3)

    # 4. 写入文件
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_path = OUTPUT_DIR / f"ss_sessions_{date_str}.json"
    output = {
        "meta": {
            "collected_at": datetime.now().isoformat(),
            "time_window": {"start": start_ts, "end": end_ts},
            "total_sessions": len(results),
        },
        "sessions": results,
    }
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\n💾 已写入: {out_path}")
    print(f"   {len(results)} 个会话, 共 {sum(r['msg_count'] for r in results)} 条消息")

    # 5. 保存状态
    save_state(end_ts)

    # 6. 清理过期数据
    cleanup_old_data()

    print("✅ 完成")


def cleanup_old_data(retention_days: int = 7):
    cutoff = datetime.now() - timedelta(days=retention_days)
    deleted = 0
    for f in OUTPUT_DIR.glob("ss_sessions_*.json"):
        try:
            date_str = f.stem.replace("ss_sessions_", "")
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date < cutoff:
                f.unlink()
                deleted += 1
        except (ValueError, OSError):
            pass
    if deleted:
        print(f"🗑️ 清理 {deleted} 个过期数据文件（>{retention_days}天）")


if __name__ == "__main__":
    main()