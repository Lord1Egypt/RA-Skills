#!/usr/bin/env python3
"""
单条（或批量）笔记内容提取脚本。
从 output/search_urls_*.json 或 --url 参数读取链接，逐条提取：
  1. Agent 提取正文（标题、文字、互动数据）
  2. Playwright 滚动评论区
  3. Agent 提取评论
结果保存 output/notes/xhs_note_{timestamp}.json，路径写入 status.md。

用法:
  python scripts/extract_note.py                         # 自动读取最新 search_urls_*.json
  python scripts/extract_note.py --url "https://..."
  python scripts/extract_note.py --urls-file output/search_urls_20260309_120000.json
"""

import sys
import json
import asyncio
import random
import argparse
import logging
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field
from agentbay import ExtractOptions

sys.path.insert(0, str(Path(__file__).parent))
from common import (
    load_config, save_config, write_status, setup_env, validate_agentbay_env, setup_logging,
    create_or_reuse_session, get_cdp_url, scroll_comment_area,
    cleanup, OUTPUT_DIR,
)
from playwright.async_api import async_playwright

# 模块级 logger，setup_logging() 调用后自动生效
log = logging.getLogger("xhs")


# ── Pydantic 数据结构 ────────────────────────────────────────────
class CommentInfo(BaseModel):
    level: str = Field(default="一级评论", description="评论级别：'一级评论' 或 '二级评论'")
    text: str = Field(default="", description="评论文字内容，字段名必须为 text")
    like_count: int = Field(default=0, description="点赞次数，字段名必须为 like_count")


class NoteContent(BaseModel):
    title: str = Field(default="", description="笔记标题，字段名必须为 title")
    content_text: str = Field(default="", description="正文文字（不含标题），字段名必须为 content_text")
    author: str = Field(default="", description="作者昵称，字段名必须为 author")
    like_count: int = Field(default=0, description="点赞次数，字段名必须为 like_count")
    collect_count: int = Field(default=0, description="收藏次数，字段名必须为 collect_count")
    comment_count: int = Field(default=0, description="评论总数，字段名必须为 comment_count")


class NoteWithComments(BaseModel):
    """合并的笔记内容 + 评论 schema，用于一次性提取"""
    title: str = Field(default="", description="笔记标题")
    content_text: str = Field(default="", description="正文文字（不含标题）")
    author: str = Field(default="", description="作者昵称")
    like_count: int = Field(default=0, description="点赞次数")
    collect_count: int = Field(default=0, description="收藏次数")
    comment_count: int = Field(default=0, description="评论总数")
    comments: list[CommentInfo] = Field(default_factory=list, description="所有评论列表")


class XhsNoteData(BaseModel):
    url: str = Field(default="")
    title: str = Field(default="")
    content_text: str = Field(default="")
    author: str = Field(default="")
    like_count: int = Field(default=0)
    collect_count: int = Field(default=0)
    comment_count: int = Field(default=0)
    comments: list[CommentInfo] = Field(default_factory=list)


# ── 核心提取函数 ─────────────────────────────────────────────────
async def extract_one_note(session, page, url: str, scroll_rounds: int) -> XhsNoteData:
    """提取单条笔记内容 + 评论，返回 XhsNoteData。"""
    agent = session.browser.operator

    # ── 步骤 1：滚动评论区 ──────────────────────────────────────
    log.info("  📜 步骤1: 滚动评论区...")
    try:
        await scroll_comment_area(page, scroll_rounds=scroll_rounds)
    except Exception as e:
        log.warning(f"  滚动异常: {e}")

    # ── 步骤 2：一次性提取正文 + 评论 ─────────────────────────────
    log.info("  📄 步骤2: 提取正文+评论...")
    note_data = NoteWithComments()
    extract_elapsed = 0.0
    try:
        start_time = asyncio.get_event_loop().time()
        ok, result = await agent.extract(
            options=ExtractOptions[NoteWithComments](
                instruction=(
                    "提取当前小红书笔记详情页的完整内容，包括：\n"
                    "【正文区域】笔记标题(title)、正文文字(content_text，不含标题)、"
                    "作者昵称(author)、点赞次数(like_count)、收藏次数(collect_count)、评论总数(comment_count)。\n"
                    "【评论区域】所有可见评论(comments)，每条评论包含："
                    "评论级别(level，填'一级评论'或'二级评论')、评论文字(text)、评论点赞次数(like_count)。\n"
                    "缺失字段用空字符串或0填充，不需要提取任何图片。"
                ),
                schema=NoteWithComments,
                use_text_extract=True,
                use_vision=False,
            ),
            page=page,
        )
        extract_elapsed = asyncio.get_event_loop().time() - start_time
        log.info(f"  ⏱ 提取耗时: {extract_elapsed:.1f}s")
        if ok and result:
            note_data = result
            log.info(f"  标题: {note_data.title}")
            log.info(f"  作者: {note_data.author}  👍{note_data.like_count}  ⭐{note_data.collect_count}  💬{note_data.comment_count}")
            log.info(f"  共提取 {len(note_data.comments)} 条评论")
            for c in note_data.comments[:5]:
                log.info(f"    [{c.level}] {c.text[:50]}  👍{c.like_count}")
        else:
            log.warning("  提取失败，使用空数据")
    except Exception as e:
        log.warning(f"  提取异常: {e}")

    log.info(f"  ⏱ 任务总耗时: {extract_elapsed:.1f}s")

    return XhsNoteData(
        url=url,
        title=note_data.title,
        content_text=note_data.content_text,
        author=note_data.author,
        like_count=note_data.like_count,
        collect_count=note_data.collect_count,
        comment_count=note_data.comment_count,
        comments=note_data.comments,
    )


# ── 主入口 ────────────────────────────────────────────────────────
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="", help="单条笔记 URL")
    parser.add_argument("--urls-file", type=str, default="", help="search_urls_*.json 文件路径")
    args = parser.parse_args()

    setup_logging("extract_note")

    cfg = load_config()
    setup_env(cfg)

    ok, err = validate_agentbay_env(cfg)
    if not ok:
        log.error(f"❌ 环境检查失败: {err}")
        write_status("error", {"说明": err})
        sys.exit(1)

    scroll_rounds = cfg.get("scroll_rounds", 10)

    urls: list[str] = []
    if args.url:
        urls = [args.url]
    elif args.urls_file:
        data = json.loads(Path(args.urls_file).read_text(encoding="utf-8"))
        urls = data.get("urls", [])
    else:
        search_urls_dir = OUTPUT_DIR / "searchUrls"
        # 时间戳文件（search_urls_YYYYMMDD_*.json）优先，无则 fallback 到 default
        timestamped = sorted(search_urls_dir.glob("search_urls_2*.json"), reverse=True)
        candidates = timestamped or list(search_urls_dir.glob("search_urls_default.json"))
        if candidates:
            data = json.loads(candidates[0].read_text(encoding="utf-8"))
            urls = data.get("urls", [])
            log.info(f"自动读取: {candidates[0].name}")

    if not urls:
        log.error("❌ 未找到可提取的 URL，请先运行 search_notes.py 或指定 --url")
        sys.exit(1)

    log.info(f"共 {len(urls)} 条笔记待提取")

    agent_bay, session, is_reused = await create_or_reuse_session(cfg)
    cfg["session_id"] = session.session_id
    save_config(cfg)
    cdp_url = await get_cdp_url(session, is_reused, cfg)

    notes_dir = OUTPUT_DIR / "notes"  # 笔记详情统一存放目录
    notes_dir.mkdir(parents=True, exist_ok=True)
    saved_files: list[str] = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(cdp_url)
            default_context = browser.contexts[0]

            for idx, url in enumerate(urls):
                log.info(f"\n[{idx + 1}/{len(urls)}] {url}")
                try:
                    pages = default_context.pages
                    if pages:
                        for p_extra in pages[:-1]:
                            await p_extra.close()
                        page = pages[-1]
                    else:
                        page = await default_context.new_page()
                    await page.goto(url, timeout=60000)
                    await asyncio.sleep(random.uniform(1.5, 2.5))

                    note_data = await extract_one_note(session, page, url, scroll_rounds)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    out_path = notes_dir / f"xhs_note_{timestamp}.json"
                    out_path.write_text(
                        json.dumps(note_data.model_dump(), ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    saved_files.append(str(out_path))
                    log.info(f"  ✅ 已保存: {out_path}")
                except Exception as e:
                    log.error(f"  ❌ 提取出错: {e}", exc_info=True)

                await asyncio.sleep(random.uniform(1, 2))

    finally:
        await cleanup(agent_bay, session)
        cfg["session_id"] = ""
        save_config(cfg)
        log.info("✅ Session 已释放，登录 Cookie 已保留（下次运行无需重新登录）")

    log.info(f"\n✅ 全部完成，共保存 {len(saved_files)} 条笔记")
    write_status(
        "extract_done",
        {
            "笔记总数": len(urls),
            "已保存": len(saved_files),
            "保存目录": str(notes_dir),
            "文件列表": "\n  " + "\n  ".join(saved_files) if saved_files else "无",
        },
    )

if __name__ == "__main__":
    asyncio.run(main())
