#!/usr/bin/env python3
"""
使用浏览器模拟小红书搜索
解决API搜索不到但网页能搜到的问题
"""

import asyncio
import json
import re
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from config import (
    XHS_USER_DATA_DIR,
    BROWSER_VIEWPORT_WIDTH,
    BROWSER_VIEWPORT_HEIGHT,
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
)

# 初始化日志
LOG_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


class XhsBrowserSearch:
    """使用浏览器搜索小红书"""

    def __init__(self):
        self.user_data_dir = XHS_USER_DATA_DIR

    async def search(self, keyword: str, max_notes: int = 5) -> List[Dict]:
        """
        使用浏览器搜索小红书笔记
        
        Args:
            keyword: 搜索关键词
            max_notes: 最多获取笔记数
            
        Returns:
            list: 笔记列表
        """
        if not PLAYWRIGHT_AVAILABLE:
            log.error("Playwright 未安装")
            return []

        log.info(f"使用浏览器搜索: {keyword}")
        
        results = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.user_data_dir),
                headless=True,
                viewport={
                    "width": BROWSER_VIEWPORT_WIDTH,
                    "height": BROWSER_VIEWPORT_HEIGHT
                },
                args=[
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
            )

            page = await browser.new_page()

            try:
                # 访问搜索结果页
                search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes"
                log.info(f"打开搜索页面: {search_url}")
                
                await page.goto(search_url, timeout=30000, wait_until="networkidle")
                await page.wait_for_timeout(5000)  # 等待页面加载

                # 提取笔记数据
                # 小红书搜索结果是动态加载的，需要从页面中提取
                log.info("正在提取笔记数据...")
                
                # 等待笔记卡片出现
                try:
                    await page.wait_for_selector("[class*='note-item']", timeout=10000)
                except:
                    log.warning("未找到笔记元素，尝试其他选择器")
                
                # 获取页面内容
                page_content = await page.content()
                
                # 尝试从页面中提取笔记ID
                # 小红书笔记链接格式: /explore/xxxxxxxx
                note_ids = re.findall(r'/explore/([a-zA-Z0-9]+)', page_content)
                note_ids = list(set(note_ids))  # 去重
                
                log.info(f"找到 {len(note_ids)} 个笔记ID")
                
                # 直接从搜索结果页提取笔记信息（避免反爬）
                log.info("从搜索结果页提取笔记信息...")
                
                # 执行 JavaScript 提取页面数据
                notes_data = await page.evaluate("""() => {
                    const notes = [];
                    // 尝试多种选择器找到笔记卡片
                    const cards = document.querySelectorAll('[class*="note"], [class*="feed"], .note-item, article');
                    
                    cards.forEach(card => {
                        // 提取标题
                        const titleEl = card.querySelector('a[title], .title, h3, h4');
                        const title = titleEl ? titleEl.textContent || titleEl.getAttribute('title') || '' : '';
                        
                        // 提取链接
                        const linkEl = card.querySelector('a[href*="/explore/"]');
                        let link = '';
                        let noteId = '';
                        if (linkEl) {
                            link = linkEl.href;
                            const match = link.match(/\/explore\/([a-zA-Z0-9]+)/);
                            if (match) noteId = match[1];
                        }
                        
                        // 提取作者
                        const authorEl = card.querySelector('[class*="author"], [class*="user"], .nickname');
                        const author = authorEl ? authorEl.textContent.trim() : '';
                        
                        // 提取点赞数
                        const likeEl = card.querySelector('[class*="like"], [class*="count"]');
                        const likes = likeEl ? likeEl.textContent.trim() : '0';
                        
                        if (noteId && title) {
                            notes.push({
                                noteId: noteId,
                                title: title.trim(),
                                author: author,
                                likes: likes,
                                link: link
                            });
                        }
                    });
                    
                    return notes;
                }""")
                
                log.info(f"从页面提取到 {len(notes_data)} 条笔记信息")
                
                # 构建结果
                for i, note in enumerate(notes_data[:max_notes], 1):
                    results.append({
                        "笔记ID": note['noteId'],
                        "笔记链接": note['link'] or f"https://www.xiaohongshu.com/explore/{note['noteId']}",
                        "标题": note['title'],
                        "内容": "",
                        "作者昵称": note['author'],
                        "点赞数": note['likes'],
                        "笔记类型": "图文",
                    })
                
                await browser.close()
                
            except Exception as e:
                log.error(f"搜索过程出错: {e}")
                await browser.close()
                raise

        log.info(f"浏览器搜索完成，共获取 {len(results)} 条笔记")
        return results

    async def _get_note_detail(self, page, note_id: str) -> Optional[Dict]:
        """
        获取笔记详情
        
        Args:
            page: Playwright page 对象
            note_id: 笔记ID
            
        Returns:
            dict: 笔记数据
        """
        try:
            note_url = f"https://www.xiaohongshu.com/explore/{note_id}"
            await page.goto(note_url, timeout=30000)
            await page.wait_for_timeout(3000)
            
            # 提取页面数据
            # 尝试从页面中提取标题、作者等信息
            title = await page.title()
            
            # 获取页面URL中的xsec_token
            current_url = page.url
            xsec_match = re.search(r'xsec_token=([^&]+)', current_url)
            xsec_token = xsec_match.group(1) if xsec_match else ""
            
            return {
                "笔记ID": note_id,
                "笔记链接": f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_search",
                "标题": title.replace(" - 小红书", "").strip() if title else "",
                "内容": "",  # 浏览器模式暂时无法获取完整内容
                "作者昵称": "",
                "点赞数": "0",
                "笔记类型": "图文",
            }
            
        except Exception as e:
            log.error(f"获取笔记详情失败 {note_id}: {e}")
            return None


async def search_with_browser(keyword: str, max_notes: int = 5) -> List[Dict]:
    """
    便捷函数：使用浏览器搜索
    
    Args:
        keyword: 搜索关键词
        max_notes: 最多获取笔记数
        
    Returns:
        list: 笔记列表
    """
    searcher = XhsBrowserSearch()
    return await searcher.search(keyword, max_notes)


if __name__ == "__main__":
    import sys
    
    keyword = sys.argv[1] if len(sys.argv) > 1 else "中间带新燕宝"
    
    print(f"🔍 使用浏览器搜索: {keyword}")
    print("-" * 50)
    
    results = asyncio.run(search_with_browser(keyword, max_notes=3))
    
    print(f"\n{'='*50}")
    print(f"共获取 {len(results)} 条笔记")
    
    if results:
        for i, note in enumerate(results, 1):
            print(f"\n[{i}] {note['标题']}")
            print(f"    链接: {note['笔记链接']}")
    else:
        print(f"\n⚠️ 未找到关键词「{keyword}」的相关笔记")
