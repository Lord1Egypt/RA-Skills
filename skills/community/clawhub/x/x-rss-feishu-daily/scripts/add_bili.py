"""批量添加 B站 UP主订阅（前置条件：BILIBILI_COOKIE 已配置进 rsshub 并重启）。

流程：建「B站」分类 → 逐个订阅 → 温和刷新 → 首批补推进群（新订阅不触发 webhook 的已知坑）。
用法：python add_bili.py
"""
import base64
import json
import time
import urllib.request

BASIC = "Basic " + base64.b64encode(f"{CONF['MINIFLUX_ADMIN_USERNAME']}:{CONF['MINIFLUX_ADMIN_PASSWORD']}".encode()).decode()
CONF = {}
for line in open("feishu.env", encoding="utf-8").read().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        CONF[k.strip()] = v.strip()

UIDS = ["316183842", "14848367", "1815948385", "341376543",
        "367678065", "14871346", "325864133", "385670211", "302188068",
        "65564239"]

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def miniflux(path, method="GET", payload=None):
    req = urllib.request.Request("http://127.0.0.1:8088" + path, method=method)
    req.add_header("Authorization", BASIC)
    if payload:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(payload).encode()
    try:
        b = opener.open(req, timeout=120).read()
        return json.loads(b) if b else {}
    except urllib.error.HTTPError as e:
        return {"http_error": e.code, "body": e.read().decode("utf-8", "ignore")[:150]}


def feishu(path, payload, token):
    req = urllib.request.Request("https://open.feishu.cn" + path,
                                 data=json.dumps(payload, ensure_ascii=False).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + token})
    return json.loads(opener.open(req, timeout=20).read().decode("utf-8", "ignore"))


def main():
    # 1. 分类
    cats = miniflux("/v1/categories")
    cat = next((c for c in cats if c["title"] == "B站"), None)
    if not cat:
        cat = miniflux("/v1/categories", "POST", {"title": "B站"})
    print("分类: B站 (id", cat["id"], ")")

    # 2. 前置检查：先试一个路由，若仍被风控则中止（Cookie 未生效）
    check = miniflux("/v1/feeds", "POST",
                     {"feed_url": "http://rsshub:1200/bilibili/user/video/316183842",
                      "category_id": cat["id"]})
    if check.get("feed_id"):
        print("✅ 前置检查通过：技术爬爬虾 已订阅 feed_id =", check["feed_id"])
        done_ids = [check["feed_id"]]
    else:
        print("❌ 前置检查失败（Cookie 未生效或被风控）：", json.dumps(check, ensure_ascii=False)[:200])
        raise SystemExit(1)

    # 2. 订阅其余 UP 主
    for uid in UIDS:
        if uid == "316183842":
            continue
        d = miniflux("/v1/feeds", "POST",
                     {"feed_url": f"http://rsshub:1200/bilibili/user/video/{uid}",
                      "category_id": cat["id"]})
        fid = d.get("feed_id")
        print(f"订阅 {uid} → feed_id={fid}", flush=True)
        if fid:
            done_ids.append(fid)
        time.sleep(2)

    # 3. 温和刷新 + 首批补推
    token = feishu("/open-apis/auth/v3/tenant_access_token/internal",
                   {"app_id": CONF["FEISHU_APP_ID"],
                    "app_secret": CONF["FEISHU_APP_SECRET"]})["tenant_access_token"]
    r = urllib.request.Request("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                               data=json.dumps({"app_id": CONF["FEISHU_APP_ID"],
                                                "app_secret": CONF["FEISHU_APP_SECRET"]}).encode(),
                               headers={"Content-Type": "application/json"})
    token = json.loads(opener.open(r, timeout=20).read().decode())["tenant_access_token"]

    for fid in done_ids:
        try:
            miniflux(f"/v1/feeds/{fid}/refresh", "PUT")
        except Exception as e:
            print(fid, "刷新失败:", e)
        time.sleep(2)

    print("\n=== 首批补推进群 ===")
    for fid in done_ids:
        f = miniflux(f"/v1/feeds/{fid}")
        d = miniflux(f"/v1/feeds/{fid}/entries?limit=10&order=published_at&direction=desc")
        entries = d.get("entries", [])
        if not entries:
            print(f"{f.get('title')}: 无条目（可能仍在抓取）")
            continue
        lines = []
        for i, e in enumerate(entries, 1):
            t = (e.get("title") or "(无标题)").strip().replace("\n", " ")[:100]
            lines.append(f"{i}. [{t}]({e.get('url', '')})")
        card = {"config": {"wide_screen_mode": True},
                "header": {"title": {"tag": "plain_text",
                           "content": f"新博主接入 · {f.get('title')} · {len(entries)} 条"},
                           "template": "turquoise"},
                "elements": [{"tag": "div", "text": {"tag": "lark_md",
                              "content": chr(10).join(lines)}}]}
        r = feishu("/open-apis/im/v1/messages?receive_id_type=chat_id",
                   {"receive_id": CONF["FEISHU_CHAT_ID"], "msg_type": "interactive",
                    "content": json.dumps(card, ensure_ascii=False)}, token)
        print(f"{f.get('title')} 补推 → code {r.get('code')} ({len(entries)} 条)")
        time.sleep(1)


if __name__ == "__main__":
    main()
