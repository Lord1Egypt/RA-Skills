#!/usr/bin/env python3
"""小红书对标账号采集器 — 接口用 tikhub.io,字段模型参考 feedhunter。

用法:
    TIKHUB_TOKEN=... python3 fetch_xhs.py <user_id> <输出目录名> [最多页数]

拉取指定用户主页全部笔记,按互动排序,导出 notes.json + summary.md,
并下载头部笔记封面到 covers/ 供风格拆解。
"""
import os, sys, json, time, urllib.request, urllib.parse

TOKEN = os.environ["TIKHUB_TOKEN"]
BASE = "https://api.tikhub.io/api/v1/xiaohongshu/app_v2"


def api_get(path, **params):
    url = f"{BASE}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    })
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            last = e
            time.sleep(2 ** attempt)
    raise last


def fetch_all_notes(user_id, max_pages=5):
    """翻页拉取用户主页笔记。"""
    notes, cursor, page = [], "", 0
    while page < max_pages:
        resp = api_get("get_user_posted_notes", user_id=user_id, cursor=cursor)
        inner = resp.get("data", {}).get("data", {})
        batch = inner.get("notes", [])
        if not batch:
            break
        notes.extend(batch)
        page += 1
        if not inner.get("has_more"):
            break
        cursor = batch[-1].get("cursor", "")
        if not cursor:
            break
        time.sleep(1)
    return notes


def slim(n):
    """参考 feedhunter note_converter 抽取关键字段。"""
    imgs = n.get("images_list", []) or []
    cover = imgs[0].get("url") or imgs[0].get("url_size_large", "") if imgs else ""
    return {
        "id": n.get("id"),
        "title": n.get("display_title") or n.get("title") or "",
        "desc": n.get("desc") or "",
        "type": n.get("type"),
        "likes": int(n.get("likes") or 0),
        "collected": int(n.get("collected_count") or 0),
        "comments": int(n.get("comments_count") or 0),
        "shares": int(n.get("share_count") or 0),
        "create_time": n.get("create_time"),
        "is_goods_note": n.get("is_goods_note", False),
        "image_count": len(imgs),
        "cover": cover,
        "image_urls": [i.get("url") or i.get("url_size_large", "") for i in imgs],
    }


def main():
    user_id = sys.argv[1]
    outname = sys.argv[2]
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    outdir = os.path.join(os.path.dirname(__file__), "..", "账号数据", outname)
    os.makedirs(os.path.join(outdir, "covers"), exist_ok=True)

    info = api_get("get_user_info", user_id=user_id).get("data", {})
    raw = fetch_all_notes(user_id, max_pages)
    slimmed = [slim(n) for n in raw]
    slimmed.sort(key=lambda x: x["likes"] + x["collected"], reverse=True)

    json.dump({"user_info": info, "notes": slimmed},
              open(os.path.join(outdir, "notes.json"), "w"),
              ensure_ascii=False, indent=2)

    # summary.md
    lines = [f"# 对标账号采集:{outname}", "",
             f"> 共 {len(slimmed)} 篇,按 点赞+收藏 排序", "",
             "| # | 标题 | 赞 | 藏 | 评 | 转 | 图数 | 类型 |",
             "|---|---|---|---|---|---|---|---|"]
    for i, n in enumerate(slimmed, 1):
        t = n["title"].replace("|", "\\|").replace("\n", " ")[:40]
        lines.append(f"| {i} | {t} | {n['likes']} | {n['collected']} | {n['comments']} | {n['shares']} | {n['image_count']} | {n['type']} |")
    open(os.path.join(outdir, "summary.md"), "w").write("\n".join(lines) + "\n")

    # 下载头部 12 篇封面
    for i, n in enumerate(slimmed[:12], 1):
        if not n["cover"]:
            continue
        try:
            req = urllib.request.Request(n["cover"], headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read()
            ext = ".webp" if "webp" in n["cover"] else ".jpg"
            open(os.path.join(outdir, "covers", f"{i:02d}{ext}"), "wb").write(data)
        except Exception as e:
            print(f"  封面{i}下载失败: {e}")

    print(f"完成:{len(slimmed)} 篇 -> {outdir}/  (notes.json, summary.md, covers/)")


if __name__ == "__main__":
    main()
