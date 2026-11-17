"""把当天已入库的推文完整重发到飞书群「RSS 推送」（每个博主一张全量卡片）。

用途：日报素材重推 / 人工回看。数据全部来自本地 Miniflux，不请求 X，无风控风险。
与 feishu-relay 的差别：relay 推增量且每卡截断 10 条；本脚本推全量，可重复运行。

用法：python push_daily.py
"""
import base64
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).parent
CONF = {}
for line in (BASE / "feishu.env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        CONF[k.strip()] = v.strip()

MINIFLUX_BASIC = "Basic " + base64.b64encode(
    f'{CONF["MINIFLUX_ADMIN_USERNAME"]}:{CONF["MINIFLUX_ADMIN_PASSWORD"]}'.encode()
).decode()

# 本机与飞书均为直连目标，显式绕过系统代理（避免 localhost 请求被代理吃掉返回 502）
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def feishu(path, payload=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(
        "https://open.feishu.cn" + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload else None,
        headers=headers,
    )
    return json.load(_opener.open(req, timeout=20))


def miniflux(path):
    req = urllib.request.Request(CONF.get("MINIFLUX_URL_HOST", CONF["MINIFLUX_URL"]).rstrip("/") + path)
    req.add_header("Authorization", MINIFLUX_BASIC)
    return json.load(_opener.open(req, timeout=30))


def fmt_time(iso):
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(
            timezone(timedelta(hours=8))
        )
        return dt.strftime("%m-%d %H:%M")
    except Exception:
        return ""


def main():
    token = feishu(
        "/open-apis/auth/v3/tenant_access_token/internal",
        payload={"app_id": CONF["FEISHU_APP_ID"], "app_secret": CONF["FEISHU_APP_SECRET"]},
    )["tenant_access_token"]

    skip_ids = {x.strip() for x in CONF.get("SKIP_FEED_IDS", "").split(",") if x.strip()}
    overview_ids = [
        x.strip()
        for x in CONF.get("OVERVIEW_FEED_IDS", CONF.get("OVERVIEW_FEED_ID", "")).split(",")
        if x.strip()
    ]
    feeds_list = miniflux("/v1/feeds")
    feed_titles = {f["id"]: f["title"] for f in feeds_list}
    for feed in feeds_list:
        if str(feed["id"]) in skip_ids:
            continue
        d = miniflux(
            f"/v1/feeds/{feed['id']}/entries?limit=50&order=published_at&direction=desc"
        )
        entries = d.get("entries", [])
        lines = []
        for i, e in enumerate(entries, 1):
            title = (e.get("title") or "(无标题)").strip().replace("\n", " ")
            t = fmt_time(e.get("published_at", ""))
            lines.append(f"{i}. [{title}]({e.get('url','')}) {t}")
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"今日推送全量 · {feed['title']} · {len(entries)} 条",
                },
                "template": "blue",
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(chunk)}}
                for chunk in (lines[i : i + 12] for i in range(0, len(lines), 12))
            ]
            + [
                {
                    "tag": "note",
                    "elements": [{"tag": "plain_text", "content": "推文全文见对应链接；本卡片由 push_daily.py 生成"}],
                }
            ],
        }
        resp = feishu(
            "/open-apis/im/v1/messages?receive_id_type=chat_id",
            payload={
                "receive_id": CONF["FEISHU_CHAT_ID"],
                "msg_type": "interactive",
                "content": json.dumps(card, ensure_ascii=False),
            },
            token=token,
        )
        print(feed["title"], "→ code", resp.get("code"), f"({len(entries)} 条)")

    # 总览卡片（可多个源：如 aihot 热点 + Follow Builders X 聚合）
    for overview_id in overview_ids:
        d = miniflux(
            f"/v1/feeds/{overview_id}/entries?limit=15&order=published_at&direction=desc"
        )
        entries = d.get("entries", [])
        lines = []
        for i, e in enumerate(entries, 1):
            title = (e.get("title") or "(无标题)").strip().replace(chr(10), " ")
            t = fmt_time(e.get("published_at", ""))
            lines.append(f"{i}. [{title}]({e.get('url','')}) {t}")
        feed_name = feed_titles.get(int(overview_id), f"feed {overview_id}")
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{feed_name} · 最近 {len(entries)} 条",
                },
                "template": "turquoise",
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(chunk)}}
                for chunk in (lines[i : i + 12] for i in range(0, len(lines), 12))
            ]
            + [
                {
                    "tag": "note",
                    "elements": [{"tag": "plain_text", "content": "仅保留最近 15 条，全文见对应链接"}],
                }
            ],
        }
        resp = feishu(
            "/open-apis/im/v1/messages?receive_id_type=chat_id",
            payload={
                "receive_id": CONF["FEISHU_CHAT_ID"],
                "msg_type": "interactive",
                "content": json.dumps(card, ensure_ascii=False),
            },
            token=token,
        )
        print(f"总览[{feed_name}] → code", resp.get("code"), f"({len(entries)} 条)")

    # 全量重发结束后，点名日报智能体（force：不受冷却限制）
    name = CONF.get("REPORT_BOT_NAME", "")
    if name:
        at = (
            f'<at user_id="{CONF["REPORT_BOT_OPEN_ID"]}"></at> '
            if CONF.get("REPORT_BOT_OPEN_ID")
            else "@"
        )
        body_text = (
            f"{at} 请根据本群最新推送整理一份今日日报"
            if CONF.get("REPORT_BOT_OPEN_ID")
            else f"{at}{name} 请根据本群最新推送整理一份今日日报"
        )
        resp = feishu(
            "/open-apis/im/v1/messages?receive_id_type=chat_id",
            payload={
                "receive_id": CONF["FEISHU_CHAT_ID"],
                "msg_type": "text",
                "content": json.dumps({"text": body_text}, ensure_ascii=False),
            },
            token=token,
        )
        print("日报点名 → code", resp.get("code"))


if __name__ == "__main__":
    main()
