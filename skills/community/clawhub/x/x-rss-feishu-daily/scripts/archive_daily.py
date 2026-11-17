"""每日归档：把当天全部信息源写成一篇飞书文档，存入「RSS 信息源归档」文件夹。

数据来源：本地 Miniflux（不请求 X）。产出：文档 URL（同时发回群里一张带链接的卡）。
用法：python archive_daily.py [YYYY-MM-DD]   # 不带参数 = 今天（北京时间）
"""
import base64
import json
import sys
import time
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

BASIC = "Basic " + base64.b64encode(
    f'{CONF["MINIFLUX_ADMIN_USERNAME"]}:{CONF["MINIFLUX_ADMIN_PASSWORD"]}'.encode()
).decode()
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def feishu(path, payload=None, token=None, method=None):
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = "Bearer " + token
    req = urllib.request.Request(
        "https://open.feishu.cn" + path,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload else None,
        headers=h, method=method)
    return json.loads(_opener.open(req, timeout=30).read().decode("utf-8", "ignore"))


def miniflux(path):
    req = urllib.request.Request(
        CONF.get("MINIFLUX_URL_HOST", CONF["MINIFLUX_URL"]).rstrip("/") + path)
    req.add_header("Authorization", BASIC)
    return json.loads(_opener.open(req, timeout=30).read().decode("utf-8", "ignore"))


def fmt_time(iso):
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00")).astimezone(
            timezone(timedelta(hours=8)))
        return dt.strftime("%m-%d %H:%M")
    except Exception:
        return ""


def entry_line(i, e):
    title = (e.get("title") or "(无标题)").strip().replace("\n", " ")[:110]
    return f"{i}. [{title}]({e.get('url', '')}) {fmt_time(e.get('published_at', ''))}"


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now(
        timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    token = feishu("/open-apis/auth/v3/tenant_access_token/internal",
                   payload={"app_id": CONF["FEISHU_APP_ID"],
                            "app_secret": CONF["FEISHU_APP_SECRET"]})["tenant_access_token"]
    folder = CONF["ARCHIVE_FOLDER_TOKEN"]

    # 1. 建文档（幂等：同日文档已存在则复用）
    tenant = CONF["FEISHU_APP_ID"].split("_")[0]
    doc_url_base = "https://wcnz1iaoqxar.feishu.cn/docx/"
    doc_id = None
    fl = feishu(f"/open-apis/drive/v1/files?folder_token={folder}&page_size=50", token=token)
    for ffile in (fl.get("data") or {}).get("files") or []:
        if ffile.get("name") == f"RSS 信息源日报 · {date}" and ffile.get("type") == "docx":
            doc_id = ffile.get("token")
            print("复用已有文档:", doc_id)
            break
    if not doc_id:
        doc = feishu("/open-apis/docx/v1/documents",
                     payload={"folder_token": folder,
                              "title": f"RSS 信息源日报 · {date}"}, token=token)
        if doc.get("code") != 0:
            print("建文档失败:", json.dumps(doc, ensure_ascii=False)[:300])
            raise SystemExit(1)
        doc_id = doc["data"]["document"]["document_id"]
        print("文档已创建:", doc_id)
    doc_url = doc_url_base + doc_id

    # 2. 组装内容（每个源一个文本块）
    blocks = []
    blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {
        "content": f"信息源日报 · {date} · 共 {len(miniflux('/v1/feeds'))} 个订阅源",
        "text_element_style": {"bold": True}}}]}})
    for feed in miniflux("/v1/feeds"):
        d = miniflux(f"/v1/feeds/{feed['id']}/entries?limit=50&order=published_at&direction=desc")
        entries = d.get("entries", [])
        if not entries:
            continue
        sec = [{"block_type": 2, "text": {"elements": [{"text_run": {
            "content": f"◆ {feed['title']}（{len(entries)} 条）",
            "text_element_style": {"bold": True}}}]}}]
        for i, e in enumerate(entries, 1):
            t = (e.get("title") or "(无标题)").strip().replace("\n", " ")[:110]
            sec.append({"block_type": 2, "text": {"elements": [{"text_run": {
                "content": f"{i}. [{t}]({e.get('url', '')}) {fmt_time(e.get('published_at', ''))}"}}]}})
        blocks.extend(sec)

    # 3. 写入内容（每批最多 50 个块）
    for i in range(0, len(blocks), 40):
        r = feishu(f"/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
                   payload={"children": blocks[i:i + 40], "index": -1},
                   token=token)
        if r.get("code") != 0:
            print("写入失败:", json.dumps(r, ensure_ascii=False)[:200])
    print(f"已写入 {len(blocks)} 个内容块")

    # 4. 群里发归档卡
    card = {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text",
                             "content": f"📁 日报归档 · {date}"}, "template": "grey"},
        "elements": [
            {"tag": "div", "fields": [
                {"is_short": True, "text": {"tag": "lark_md",
                 "content": "**归档文档**\n[RSS 信息源日报 · " + date + "](" + doc_url + ")"}},
                {"is_short": True, "text": {"tag": "lark_md",
                 "content": "**内容**\n全部订阅源当日素材，按源分节"}}]},
            {"tag": "note", "elements": [{"tag": "plain_text",
             "content": "由 archive_daily.py 自动归档，历史文档都在云空间「RSS 信息源归档」文件夹"}]},
        ],
    }
    r = feishu("/open-apis/im/v1/messages?receive_id_type=chat_id",
               payload={"receive_id": CONF["FEISHU_CHAT_ID"], "msg_type": "interactive",
                        "content": json.dumps(card, ensure_ascii=False)}, token=token)
    print("归档卡 → code", r.get("code"))
    return doc_url


if __name__ == "__main__":
    main()
