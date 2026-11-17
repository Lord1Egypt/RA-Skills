"""飞书推送中转：接收 Miniflux Webhook(new_entries)，组装卡片发到飞书群。

仅用标准库。配置从同目录 feishu.env 读取（KEY=VALUE）。
"""
import base64
import datetime
import email.utils
import html
import json
import os
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
CONF = {}
with open(os.path.join(BASE, "feishu.env"), encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            CONF[k.strip()] = v.strip()

FEISHU_CHAT_ID = CONF["FEISHU_CHAT_ID"]
MINIFLUX_URL = CONF["MINIFLUX_URL"].rstrip("/")
REPORT_BOT_NAME = CONF.get("REPORT_BOT_NAME", "")
REPORT_BOT_OPEN_ID = CONF.get("REPORT_BOT_OPEN_ID", "")
REPORT_COOLDOWN_H = float(CONF.get("REPORT_TRIGGER_COOLDOWN_H", "20"))
REPORT_DM_TARGET = CONF.get("REPORT_DM_TARGET", "")
SCHEDULE_TIMES = [s.strip() for s in CONF.get("SCHEDULE_TIMES", "").split(",") if s.strip()]
SCHED_STATE = os.path.join(BASE, ".sched_state.json")
BJTZ = datetime.timezone(datetime.timedelta(hours=8))
MONITOR_ENABLED = CONF.get("MONITOR", "1") == "1"
MONITOR_INTERVAL = int(CONF.get("MONITOR_INTERVAL_SEC", "1800"))
MON = {"streak": 0, "alerted": False}
MINIFLUX_BASIC = "Basic " + base64.b64encode(
    f'{CONF["MINIFLUX_ADMIN_USERNAME"]}:{CONF["MINIFLUX_ADMIN_PASSWORD"]}'.encode()).decode()
UT_PATH = os.path.join(BASE, "user_token.json")
_state_path = os.path.join(BASE, ".report_state.json")
BASIC = "Basic " + base64.b64encode(
    f'{CONF["MINIFLUX_ADMIN_USERNAME"]}:{CONF["MINIFLUX_ADMIN_PASSWORD"]}'.encode()
).decode()

FB_ENABLED = CONF.get("FOLLOW_BUILDERS", "") == "1"
FB_PROXY = CONF.get("FB_PROXY", "http://host.docker.internal:7891")
FB_SOURCES = [
    ("fb_x", "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json"),
    ("fb_podcasts", "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json"),
    ("fb_blogs", "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-blogs.json"),
]

_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
opener = _opener
_token = {"value": None, "expire_at": 0.0}
_lock = threading.Lock()
_titles = {"map": {}, "at": 0.0}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def get_token():
    with _lock:
        if _token["value"] and time.time() < _token["expire_at"] - 300:
            return _token["value"]
        req = urllib.request.Request(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            data=json.dumps(
                {"app_id": CONF["FEISHU_APP_ID"], "app_secret": CONF["FEISHU_APP_SECRET"]}
            ).encode(),
            headers={"Content-Type": "application/json"},
        )
        d = json.load(urllib.request.urlopen(req, timeout=15))
        if d.get("code") != 0:
            raise RuntimeError(f"get token failed: {d}")
        _token["value"] = d["tenant_access_token"]
        _token["expire_at"] = time.time() + d.get("expire", 7200)
        return _token["value"]


def send_card(card):
    payload = {
        "receive_id": FEISHU_CHAT_ID,
        "msg_type": "interactive",
        "content": json.dumps(card, ensure_ascii=False),
    }
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + get_token(),
        },
    )
    d = json.load(urllib.request.urlopen(req, timeout=15))
    if d.get("code") != 0:
        raise RuntimeError(f"send card failed: {d}")
    return d


def feed_title_map():
    if time.time() - _titles["at"] > 3600:
        try:
            req = urllib.request.Request(
                MINIFLUX_URL + "/v1/feeds", headers={"Authorization": BASIC}
            )
            feeds = json.load(urllib.request.urlopen(req, timeout=10))
            _titles["map"] = {f["id"]: f["title"] for f in feeds}
            _titles["at"] = time.time()
            log("feed 标题已刷新:", _titles["map"])
        except Exception as e:
            log("刷新 feed 标题失败:", e)
    return _titles["map"]


def build_card(entries):
    titles = feed_title_map()
    lines = []
    for e in entries[:10]:
        name = titles.get(e.get("feed_id"), "X 博主")
        title = (e.get("title") or "(无标题)").strip().replace("\n", " ")[:120]
        url = e.get("url") or ""
        if url:
            lines.append(f"- **{name}**：[{title}]({url})")
        else:
            lines.append(f"- **{name}**：{title}")
    if len(entries) > 10:
        lines.append(f"…等共 {len(entries)} 条，其余去 Miniflux（http://localhost:8088）看")
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"X 更新 · {len(entries)} 条新推文"},
            "template": "blue",
        },
        "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}}],
    }


def user_token():
    """读取 user_token.json，按需用 refresh_token 续期（滚动更新）。失败返回 None。"""
    try:
        tk = json.load(open(UT_PATH, encoding="utf-8"))
    except Exception:
        return None
    if time.time() < tk.get("access_expire_at", 0) - 120:
        return tk["access_token"]
    try:
        req = urllib.request.Request(
            "https://open.feishu.cn/open-apis/authen/v2/oauth/token",
            data=json.dumps({"grant_type": "refresh_token",
                             # user_token.json 属小蓝虾(B)应用命名空间，须用 B 凭证刷新
                             "client_id": CONF.get("BOT_B_APP_ID", CONF["FEISHU_APP_ID"]),
                             "client_secret": CONF.get("BOT_B_APP_SECRET", CONF["FEISHU_APP_SECRET"]),
                             "refresh_token": tk["refresh_token"]}).encode(),
            headers={"Content-Type": "application/json"})
        r = json.loads(_opener.open(req, timeout=20).read().decode("utf-8", "ignore"))
    except Exception as e:
        log("user token 刷新异常:", e)
        return None
    if not r.get("access_token"):
        log("user token 刷新被拒:", json.dumps(r, ensure_ascii=False)[:200])
        return None
    now = time.time()
    tk.update({"access_token": r["access_token"],
               "refresh_token": r.get("refresh_token", tk["refresh_token"]),
               "access_expire_at": now + r.get("expires_in", 7200),
               "updated_at": now})
    json.dump(tk, open(UT_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log("user token 已续期")
    return tk["access_token"]


def trigger_report(force=False):
    """推送完成后触发日报。首选：以用户身份私聊小蓝虾；失败退回群内 @。"""
    if not REPORT_BOT_NAME:
        return
    last = 0.0
    try:
        last = json.load(open(_state_path, encoding="utf-8"))["last"]
    except Exception:
        pass
    if not force and time.time() - last < REPORT_COOLDOWN_H * 3600:
        log("日报点名冷却中，跳过")
        return
    # 首选：用户身份私聊（智能体对用户私聊必然响应）
    if REPORT_DM_TARGET:
        ut = user_token()
        if ut:
            payload = {"receive_id": REPORT_DM_TARGET, "msg_type": "text",
                       "content": json.dumps(
                           {"text": "请读取飞书群「RSS 推送」今天的最新推送卡片，整理一份今日日报并发回该群。"},
                           ensure_ascii=False)}
            try:
                req = urllib.request.Request(
                    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    headers={"Content-Type": "application/json",
                             "Authorization": "Bearer " + ut})
                d = json.loads(opener.open(req, timeout=20).read().decode("utf-8", "ignore"))
                if d.get("code") == 0:
                    json.dump({"last": time.time()}, open(_state_path, "w"))
                    log("✅ 已以用户身份私聊触发日报")
                    return
                log("私聊触发失败:", json.dumps(d, ensure_ascii=False)[:150])
            except Exception as e:
                log("私聊触发异常:", e)
    # 退化：群内 @ / 文本点名
    if REPORT_BOT_OPEN_ID:
        at = f'<at user_id="{REPORT_BOT_OPEN_ID}"></at> '
        text = {"text": f"{at} 请根据本群最新推送整理一份今日日报"}
    else:
        at = "@"
        text = {"text": f"{at}{REPORT_BOT_NAME} 请根据本群最新推送整理一份今日日报"}
    payload = {
        "receive_id": FEISHU_CHAT_ID,
        "msg_type": "text",
        "content": json.dumps(text, ensure_ascii=False),
    }
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + get_token(),
        },
    )
    d = json.loads(opener.open(req, timeout=20).read().decode("utf-8", "ignore"))
    if d.get("code") != 0:
        raise RuntimeError(f"trigger report failed: {d}")
    json.dump({"last": time.time()}, open(_state_path, "w"))
    log("已发送日报点名（群内 @）")



# ===== Follow Builders：JSON → RSS 转换桥 =====
def _rfc822(iso):
    try:
        dt = datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        return email.utils.format_datetime(dt.astimezone(datetime.timezone.utc))
    except Exception:
        return ""


def _esc(s):
    return html.escape(str(s or ""), quote=True)


def _items_to_rss(title, link, items):
    rows = "".join(
        "<item><title>{t}</title><guid isPermaLink=\"false\">{g}</guid><link>{l}</link>"
        "<description>{d}</description><pubDate>{p}</pubDate></item>".format(
            t=_esc(i["title"]), g=_esc(i["guid"]), l=_esc(i["link"]),
            d=_esc(i["desc"]), p=_esc(i["pubDate"]))
        for i in items)
    return ("<?xml version=\"1.0\" encoding=\"UTF-8\"?><rss version=\"2.0\"><channel>"
            f"<title>{_esc(title)}</title><link>{_esc(link)}</link>"
            f"<description>{_esc(title)}</description>{rows}</channel></rss>")


def fb_build(kind, data):
    items = []
    if kind == "fb_x":
        for acc in data.get("x", []):
            for tw in acc.get("tweets", []):
                text = (tw.get("text") or "").strip().replace(chr(10), " ")
                items.append({
                    "title": f"{acc.get('name','')}：{text[:80]}",
                    "guid": f"fbx-{tw.get('id')}",
                    "link": tw.get("url") or f"https://x.com/{acc.get('handle')}",
                    "desc": text,
                    "pubDate": _rfc822(tw.get("createdAt"))})
    elif kind == "fb_podcasts":
        for ep in data.get("podcasts", []):
            items.append({
                "title": f"{ep.get('name','')}｜{ep.get('title','')}",
                "guid": f"fbp-{ep.get('guid') or ep.get('url')}",
                "link": ep.get("url") or "",
                "desc": (ep.get("transcript") or "")[:800],
                "pubDate": _rfc822(ep.get("publishedAt"))})
    elif kind == "fb_blogs":
        for b in data.get("blogs", []):
            items.append({
                "title": f"{b.get('name','')}｜{b.get('title','')}",
                "guid": f"fbb-{b.get('url')}",
                "link": b.get("url") or "",
                "desc": (b.get("description") or b.get("content") or "")[:800],
                "pubDate": _rfc822(b.get("publishedAt"))})
    items.sort(key=lambda i: i["pubDate"], reverse=True)
    names = {"fb_x": "Follow Builders · X", "fb_podcasts": "Follow Builders · 播客",
             "fb_blogs": "Follow Builders · 博客"}
    caps = {"fb_x": 80, "fb_podcasts": 30, "fb_blogs": 30}
    return _items_to_rss(names[kind], "https://github.com/zarazhangrui/follow-builders",
                         items[:caps[kind]])


def fb_refresh_once():
    op = urllib.request.build_opener(urllib.request.ProxyHandler(
        {"http": FB_PROXY, "https": FB_PROXY}))
    op.addheaders = [("User-Agent", "Mozilla/5.0 rss-stack")]
    for kind, url in FB_SOURCES:
        d = json.load(op.open(url, timeout=90))
        xml = fb_build(kind, d)
        open(os.path.join(BASE, kind + ".xml"), "w", encoding="utf-8").write(xml)
        log(f"FB {kind} 已转换（{xml.count('<item>')} 条）")


def fb_loop():
    while True:
        try:
            fb_refresh_once()
        except Exception as e:
            log("FB 刷新失败:", e)
        time.sleep(4 * 3600)




# ===== 定时调度：每天 SCHEDULE_TIMES 自动 总览卡→归档→私聊触发日报 =====
def _bjnow():
    return datetime.datetime.now(BJTZ)


def _sched_state():
    try:
        return json.load(open(SCHED_STATE, encoding="utf-8"))
    except Exception:
        return {"fired": {}, "last_overview": ""}


def _mf(path):
    req = urllib.request.Request(
        CONF["MINIFLUX_URL"].rstrip("/") + path,
        headers={"Authorization": MINIFLUX_BASIC})
    return json.loads(_opener.open(req, timeout=30).read().decode("utf-8", "ignore"))


def _push_overview_since(since_iso):
    """OVERVIEW_FEED_IDS 各源自 since 的新条目推总览卡。返回推送条数。"""
    n = 0
    titles = {f["id"]: f["title"] for f in _mf("/v1/feeds")}
    for oid in [x.strip() for x in CONF.get("OVERVIEW_FEED_IDS", "").split(",") if x.strip()]:
        try:
            d = _mf(f"/v1/feeds/{oid}/entries?limit=50&order=published_at&direction=desc")
        except Exception as e:
            log("总览源读取失败:", e)
            continue
        entries = [e for e in (d.get("entries") or []) if e.get("published_at", "") > since_iso]
        if not entries:
            continue
        entries = entries[:15]
        lines = []
        for i, e in enumerate(entries, 1):
            t = (e.get("title") or "(无标题)").strip().replace(chr(10), " ")[:100]
            lines.append(f"{i}. [{t}]({e.get('url', '')})")
        name = titles.get(int(oid), f"总览源 {oid}")
        card = {"config": {"wide_screen_mode": True},
                "header": {"title": {"tag": "plain_text",
                                     "content": f"{name} · 最新 {len(entries)} 条"},
                           "template": "turquoise"},
                "elements": [{"tag": "div", "text": {"tag": "lark_md",
                              "content": chr(10).join(lines)}}]}
        try:
            send_card(card)
            n += len(entries)
            log(f"总览[{name}] 已推 {len(entries)} 条")
        except Exception as e:
            log("总览卡发送失败:", e)
    return n


def scheduled_slot_job(slot, is_last):
    st = _sched_state()
    since = st.get("last_overview") or (_bjnow().strftime("%Y-%m-%d") + "T00:00:00+08:00")
    _push_overview_since(since)
    st["last_overview"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(st, open(SCHED_STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    doc_url = ""
    if is_last:
        try:
            import archive_daily
            doc_url = archive_daily.main() or ""
        except Exception as e:
            log("定时归档失败:", e)
    ut = user_token()
    if ut and REPORT_DM_TARGET:
        msg = (f"现在是每日 {slot} 场次：请读取飞书群「RSS 推送」今天的最新推送卡片"
               f"（8 位博主动态、AI 热点总览、Follow Builders），整理一份日报发回该群。")
        if doc_url:
            msg += f" 归档文档：{doc_url}"
        try:
            req = urllib.request.Request(
                "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
                data=json.dumps({"receive_id": REPORT_DM_TARGET, "msg_type": "text",
                                 "content": json.dumps({"text": msg}, ensure_ascii=False)}).encode("utf-8"),
                headers={"Content-Type": "application/json", "Authorization": "Bearer " + ut})
            d = json.loads(opener.open(req, timeout=20).read().decode("utf-8", "ignore"))
            log(f"定时触发[{slot}]:", "✅ 已私聊小蓝虾" if d.get("code") == 0
                else json.dumps(d, ensure_ascii=False)[:150])
        except Exception as e:
            log("定时私聊触发失败:", e)


def scheduler_loop():
    log("定时调度已启用:", SCHEDULE_TIMES)
    while True:
        try:
            now = _bjnow()
            today = now.strftime("%Y-%m-%d")
            hm = now.strftime("%H:%M")
            st = _sched_state()
            fired = st.get("fired", {}).get(today, [])
            due = [s for s in SCHEDULE_TIMES if hm >= s and s not in fired]
            if due:
                slot = max(due)
                is_last = slot == max(SCHEDULE_TIMES)
                log(f"到达定时点 {slot}，执行场次任务")
                scheduled_slot_job(slot, is_last)
                st.setdefault("fired", {})[today] = sorted(set(fired + due))
                json.dump(st, open(SCHED_STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        except Exception as e:
            log("调度循环异常:", e)
        time.sleep(45)



# ===== 抓取通道监控：X 源连续失败自动告警 / 恢复通知 =====
def _failing_x_feeds():
    out = []
    for f in _mf("/v1/feeds"):
        if "/twitter/" not in (f.get("feed_url") or ""):
            continue
        if (f.get("parsing_error_count") or 0) > 0:
            out.append((f.get("title", "?"),
                        (f.get("parsing_error_message") or "unknown")[:80]))
    return out


def _alert_card(failing):
    rows = chr(10).join(f"· {t}：{m}" for t, m in failing)
    e1 = {"tag": "div", "text": {"tag": "lark_md",
         "content": "**异常源：**" + rows}}
    e2 = {"tag": "div", "text": {"tag": "lark_md",
         "content": "**常见原因与恢复：** 1) X 的 auth_token 失效 → 重新取 token 填入 rss-stack/.env 后执行 docker compose up -d rsshub；2) Clash 代理断开 → 检查 7891；3) 电脑重启后稍等 Docker 就绪"}}
    e3 = {"tag": "note", "elements": [{"tag": "plain_text",
          "content": "本告警由抓取通道监控自动发出，恢复后会再发 ✅ 通知"}]}
    return {"config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text",
                       "content": "⚠️ X 抓取通道异常，推送已暂停"},
                       "template": "red"},
            "elements": [e1, e2, e3]}


def _recovery_card():
    return {"config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text",
                       "content": "✅ X 抓取通道已恢复"},
                       "template": "green"},
            "elements": [{"tag": "div", "text": {"tag": "lark_md",
                         "content": "全部订阅源恢复正常，推送继续。"}}]}


def monitor_once():
    failing = _failing_x_feeds()
    if len(failing) >= 3:
        MON["streak"] += 1
    else:
        if MON["alerted"]:
            try:
                send_card(_recovery_card())
                log("已发送恢复通知")
            except Exception as e:
                log("恢复通知失败:", e)
            MON["alerted"] = False
        MON["streak"] = 0
    if MON["streak"] >= 2 and not MON["alerted"]:
        try:
            send_card(_alert_card(failing))
            MON["alerted"] = True
            MON["streak"] = 0
            log("⚠️ 已发送抓取异常告警")
        except Exception as e:
            log("告警发送失败:", e)


def monitor_loop():
    log("抓取监控已启用，间隔", MONITOR_INTERVAL, "秒")
    while True:
        try:
            monitor_once()
        except Exception as e:
            log("监控循环异常:", e)
        time.sleep(MONITOR_INTERVAL)


class Handler(BaseHTTPRequestHandler):
    def _reply(self, code, body=b""):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/feeds/"):
            name = self.path.split("/feeds/", 1)[1].split("?")[0]
            p = os.path.join(BASE, name)
            if name in ("fb_x.xml", "fb_podcasts.xml", "fb_blogs.xml") and os.path.exists(p):
                data = open(p, "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "application/xml; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
        self._reply(200, b"ok")

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception as e:
            log("bad json:", e)
            return self._reply(400)
        entries = data.get("entries") or []
        if not entries:
            log("忽略无 entries 的事件:", data.get("type") or data.get("event"))
            return self._reply(200)
        skip_ids = {int(x) for x in CONF.get("SKIP_FEED_IDS", "").split(",") if x.strip().isdigit()}
        if skip_ids:
            filtered = [e for e in entries if e.get("feed_id") not in skip_ids]
            if len(filtered) < len(entries):
                log(f"跳过总览源条目 {len(entries)-len(filtered)} 条")
            entries = filtered
        if not entries:
            return self._reply(200)
        try:
            send_card(build_card(entries))
            log(f"已推送 {len(entries)} 条到飞书")
            self._reply(200)
            try:
                trigger_report()
            except Exception as e:
                log("日报点名失败:", e)
        except Exception as e:
            log("推送失败:", e)
            self._reply(500)


if __name__ == "__main__":
    log("feishu-relay 启动，目标群:", FEISHU_CHAT_ID)
    if FB_ENABLED:
        threading.Thread(target=fb_loop, daemon=True).start()
        log("Follow Builders 桥已启用")
    if SCHEDULE_TIMES:
        threading.Thread(target=scheduler_loop, daemon=True).start()
    if MONITOR_ENABLED:
        threading.Thread(target=monitor_loop, daemon=True).start()
    feed_title_map()
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
