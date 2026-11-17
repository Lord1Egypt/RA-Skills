#!/root/venv/bin/python
# -*- coding: utf-8 -*-
"""today-trending — 微博 / 抖音 / 百度 热搜一键拉取"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

from curl_cffi.requests import AsyncSession
from lxml import etree

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/141.0.0.0 Safari/537.36"
)
PLATFORMS = ("weibo", "douyin", "baidu")

URL_TEMPLATES = {
    "weibo":  "https://s.weibo.com/weibo?q={}",
    "douyin": "https://www.douyin.com/search?keyword={}",
    "baidu":  "https://www.baidu.com/s?wd={}",
}

# ---------- 抓取 ----------

async def fetch_weibo(session: AsyncSession) -> list[dict]:
    headers = {
        "referer": "https://weibo.com/hot/search",
        "user-agent": USER_AGENT,
        "x-requested-with": "XMLHttpRequest",
    }
    data = (await session.get("https://weibo.com/ajax/side/hotSearch", headers=headers)).json()
    return [
        {"word": i["word"], "hot_value": round(int(i["num"]) / 10000, 2)}
        for i in data["data"]["realtime"][:20]
    ]


async def fetch_douyin(session: AsyncSession) -> list[dict]:
    url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
    data = (await session.get(url, headers={"user-agent": USER_AGENT})).json()
    return [
        {"word": i["word"], "hot_value": round(int(i["hot_value"]) / 10000, 2)}
        for i in data["word_list"][:20]
    ]


async def fetch_baidu(session: AsyncSession) -> list[dict]:
    url = "https://top.baidu.com/board?tab=realtime"
    html = etree.HTML((await session.get(url, headers={"user-agent": USER_AGENT})).text)
    items = html.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div[*]')[1:21]
    out = []
    for item in items:
        word = item.xpath("string(div[2]/a/div[1])").strip()
        if not word:
            continue
        num = int(item.xpath("string(div[1]/div[2])")) / 10000
        out.append({"word": word, "hot_value": round(num, 2)})
    return out


FETCHERS = {"weibo": fetch_weibo, "douyin": fetch_douyin, "baidu": fetch_baidu}


def url_for(platform: str, word: str) -> str:
    return URL_TEMPLATES[platform].format(urllib.parse.quote(word, safe=""))


async def fetch_all(only: str | None = None) -> dict[str, list[dict]]:
    targets = [only] if only else list(PLATFORMS)

    # 所有平台共用一个 session:复用 TLS 指纹 & 连接池
    async with AsyncSession(impersonate="chrome", timeout=20) as session:

        async def run(name: str) -> tuple[str, list[dict]]:
            try:
                return name, await FETCHERS[name](session)
            except Exception as e:
                print(f"❌ {name} 抓取失败: {e}", file=sys.stderr)
                return name, []

        pairs = await asyncio.gather(*(run(n) for n in targets))

    return dict(pairs)


# ---------- CLI ----------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="微博 / 抖音 / 百度 热搜一键拉取")
    parser.add_argument("--platform", choices=PLATFORMS,
                        help="只抓一个平台;不传则三平台并发")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    start = time.monotonic()
    results = asyncio.run(fetch_all(args.platform))
    elapsed_ms = int((time.monotonic() - start) * 1000)

    out: dict[str, list[dict]] = {}
    for platform, items in results.items():
        for rank, item in enumerate(items, 1):
            item["rank"] = rank
            item["url"] = url_for(platform, item["word"])
        out[platform] = items

    final_out = {
        "meta": {
            "fetched_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
            "elapsed_ms": elapsed_ms,
            "platforms": {p: ("ok" if results.get(p) else "failed") for p in PLATFORMS},
        },
        **out,
    }
    print(json.dumps(final_out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()