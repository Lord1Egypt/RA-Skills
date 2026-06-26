#!/usr/bin/env python3
"""
关键词搜索脚本。
从 config.json 读取 keywords，在小红书搜索并收集笔记详情页 URL。
结果写入 output/search_urls_{timestamp}.json，路径同步写入 status.md。

用法:
  python scripts/search_notes.py
  python scripts/search_notes.py --keywords "比亚迪,BYD,腾势"
"""

import sys
import json
import asyncio
import random
import argparse
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
from common import (
    load_config, save_config, write_status, setup_env, validate_agentbay_env, setup_logging,
    create_or_reuse_session, get_cdp_url, cleanup,
    OUTPUT_DIR,
)
from playwright.async_api import async_playwright

# 模块级 logger，setup_logging() 调用后自动生效
log = logging.getLogger("xhs")


async def search_single_keyword(context, keyword: str, max_results: int) -> list[str]:
    urls = []
    try:
        page = await context.new_page()
        await page.goto(f"https://www.xiaohongshu.com/search_result?keyword={quote(keyword)}")
        await asyncio.sleep(2)

        for _ in range(4):
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(random.uniform(0.8, 1.2))

        links = await page.query_selector_all('a.cover.mask.ld')
        log.info(f"  [{keyword}] 找到 {len(links)} 个链接")
        for idx, link in enumerate(links):
            if idx >= max_results:
                break
            href = await link.get_attribute('href')
            if href:
                urls.append(f"https://www.xiaohongshu.com{href}")

        await asyncio.sleep(0.5)
        await page.close()
    except Exception as e:
        log.warning(f"  [{keyword}] 搜索出错: {e}")
    return urls


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", type=str, default="", help="逗号分隔的关键词")
    args = parser.parse_args()

    setup_logging("search_notes")

    cfg = load_config()
    setup_env(cfg)

    ok, err = validate_agentbay_env(cfg)
    if not ok:
        log.error(f"❌ 环境检查失败: {err}")
        write_status("error", {"说明": err})
        sys.exit(1)

    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else cfg.get("keywords", [])
    if not keywords:
        log.error("❌ 未指定关键词，请在 config.json 的 keywords 字段配置或通过 --keywords 传入")
        sys.exit(1)

    max_per_kw = cfg.get("max_notes_per_keyword", 3)

    agent_bay, session, is_reused = await create_or_reuse_session(cfg)
    cfg["session_id"] = session.session_id
    save_config(cfg)
    cdp_url = await get_cdp_url(session, is_reused, cfg)

    all_urls = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(cdp_url)
            default_context = browser.contexts[0]

            for kw in keywords:
                log.info(f"🔍 搜索关键词: {kw}（最多 {max_per_kw} 条）")
                urls = await search_single_keyword(default_context, kw, max_per_kw)
                all_urls.extend(urls)
                log.info(f"  累计 {len(all_urls)} 条链接")
                await asyncio.sleep(random.uniform(2, 4))

            await browser.close()
    finally:
        log.info("✅ 搜索完成，session 保留供后续 extract 复用")

    all_urls = list(dict.fromkeys(all_urls))
    search_urls_dir = OUTPUT_DIR / "searchUrls"
    search_urls_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = search_urls_dir / f"search_urls_{timestamp}.json"
    output_path.write_text(
        json.dumps({"keywords": keywords, "urls": all_urls, "count": len(all_urls)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log.info(f"✅ 共收集 {len(all_urls)} 条笔记链接，已保存: {output_path}")

    write_status(
        "search_done",
        {
            "关键词": "、".join(keywords),
            "笔记链接数": len(all_urls),
            "结果文件": str(output_path),
            "说明": "运行 extract_note.py 提取笔记内容（会自动新建 session，登录状态已保留）",
        },
    )


if __name__ == "__main__":
    asyncio.run(main())
