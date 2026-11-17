#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Official-domain news/RSS search shared by scene-specific wool scripts.

数据源：Bing Web 搜索 RSS（国内可直连，实测 ~0.7s 可达）。
注意：Bing 不严格认 `site:` 限定，故查询只带关键词，结果取回后按
「官方域名 + 权威聚合站」白名单对 link 的 host 做后缀匹配过滤。
若官方/权威域结果偏少（<3 条），自动补充「命中关键词但非官方域」的结果并标 ⚠，
保证永不空输出。
"""
import argparse, json, os, sys, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime

def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; WorkBuddyCoupon/1.0)"})
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        if not (os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")):
            raise
        with urllib.request.build_opener().open(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")

def _host_ok(link, whitelist):
    """link 的 host 是否命中白名单（支持 www. 前缀与子域后缀匹配）。"""
    try:
        host = urllib.parse.urlparse(link).netloc.lower()
    except Exception:
        return False
    if host.startswith("www."):
        host = host[4:]
    for d in whitelist:
        d = (d or "").lower().strip()
        if not d:
            continue
        if host == d or host.endswith("." + d):
            return True
    return False

def search(scene, query, domains, relevant, limit=8, authoritative=None):
    terms = query.strip() or scene["default"]
    whitelist = list(domains) + list(authoritative or [])
    # Bing 不认 site: 限定，故只带关键词；结果靠 host 白名单后置过滤
    q = terms
    url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": q, "format": "rss", "mkt": "zh-CN"})
    root = ET.fromstring(http_get(url))
    all_items = []
    for item in root.findall("./channel/item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        if not link:
            continue
        pub = item.findtext("pubDate", "").strip()
        host = urllib.parse.urlparse(link).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        all_items.append({"title": title, "source": host, "url": link,
                          "published": pub, "official": _host_ok(link, whitelist)})
    # 第一优先：官方/权威域命中
    official = [c for c in all_items if c["official"]]
    if relevant:
        off_rel = [c for c in official if any(k in c["title"] for k in relevant)]
        if off_rel:
            official = off_rel
    results = list(official)
    # 兜底：官方结果偏少时，补充「命中关键词但非官方域」的结果，标 ⚠
    if len(results) < 3 and relevant:
        seen = {id(c) for c in results}
        supp = [c for c in all_items
                if (not c["official"]) and any(k in c["title"] for k in relevant)
                and id(c) not in seen]
        results += supp
    results = results[:limit]
    for c in results:
        if not c["official"]:
            c["source"] = "⚠" + c["source"]
    return {"scene": scene["name"], "query": terms,
            "feed": "Bing Web RSS（国内可直连）+ 官方/权威站 host 过滤（不足时补⚠非官方）",
            "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "items": results}

def main(scene, domains, relevant, authoritative=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=scene["name"] + " 官方活动检索")
    p.add_argument("query", nargs="*", help="关键词，不填则使用场景默认词")
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(); q = " ".join(a.query)
    try:
        data = search(scene, q, domains, relevant, max(1, min(20, a.limit)), authoritative)
    except Exception as e:
        print("检索失败：" + str(e), file=sys.stderr); return 2
    if a.json:
        print(json.dumps(data, ensure_ascii=False, indent=2)); return 0
    print(f'{data["scene"]}｜查询：{data["query"]}｜{data["checked_at"]}')
    print("数据：" + data["feed"])
    if not data["items"]:
        print("未检索到结果；可换关键词或直接打开官方活动页。"); return 0
    for i, item in enumerate(data["items"], 1):
        print("\n{}. {}\n   来源：{}｜{}\n   {}".format(i, item["title"], item["source"], item["published"], item["url"]))
    return 0


# ── 引流信息（固定输出，prepare_release.py 自动补齐）─────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _print_leadgen()
