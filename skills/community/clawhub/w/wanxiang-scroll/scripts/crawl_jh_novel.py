#!/usr/bin/env python3
"""
聚合小说搜索下载脚本 - 独立版本

从 novel.pansd.xyz 搜索和下载小说
API 来源：https://novel.pansd.xyz
支持平台：刺猬猫、起点、faloo、番茄小说等多个平台
"""

import os
import re
import json
import argparse
import asyncio
import aiohttp
from datetime import datetime
from typing import Optional, List, Dict


class JhNovelCrawler:
    """聚合小说爬虫"""

    def __init__(self, output_dir: str = "./novel_data/jh"):
        self.base_url = "https://novel.pansd.xyz"
        self.output_dir = output_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        os.makedirs(output_dir, exist_ok=True)

    async def _make_request(self, session: aiohttp.ClientSession, url: str, timeout: int = 15) -> dict:
        """发送异步 HTTP 请求"""
        try:
            async with session.get(url, timeout=timeout) as response:
                return await response.json()
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            raise

    async def _make_post_request(self, session: aiohttp.ClientSession, url: str, data: dict, timeout: int = 30) -> dict:
        """发送异步 POST 请求"""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Origin': 'https://novel.pansd.xyz',
                'Referer': 'https://novel.pansd.xyz/',
                'User-Agent': self.headers['User-Agent'],
            }
            async with session.post(url, json=data, headers=headers, timeout=timeout) as response:
                return await response.json()
        except Exception as e:
            print(f"❌ POST 请求失败: {e}")
            raise

    async def search(self, keyword: str, limit: int = 20) -> List[Dict]:
        """搜索小说"""
        print(f"🔍 搜索关键词: {keyword}")

        search_url = f"{self.base_url}/api/search?keyword={keyword}&limit={limit}"

        async with aiohttp.ClientSession() as session:
            result = await self._make_request(session, search_url)

        if not isinstance(result, dict):
            print("❌ 搜索失败：返回数据格式错误")
            return []

        data = result.get("results", [])
        if not data:
            print("❌ 未找到匹配的小说")
            return []

        print(f"\n📚 找到 {len(data)} 本小说:\n")
        print("-" * 80)

        for i, book in enumerate(data[:limit], 1):
            title = book.get("title", "未知")
            author = book.get("author", "未知")
            site = book.get("site", "未知")
            book_id = book.get("book_id", "")
            latest_chapter = book.get("latest_chapter", "未知")

            print(f"{i}. {title}")
            print(f"   作者: {author} | 来源: {site}")
            print(f"   最新章节: {latest_chapter}")
            print(f"   下载ID: {site}|{book_id}")
            print("-" * 80)

        return data[:limit]

    async def download(self, book_info: str) -> Optional[str]:
        """下载整本小说

        Args:
            book_info: 格式为 "来源|书籍ID"，如 "ciyuanji|27427"

        Returns:
            下载文件的路径，失败返回 None
        """
        if "|" not in book_info:
            print("❌ 书籍信息格式错误，应为：来源|书籍ID")
            return None

        site, book_id = book_info.split("|", 1)
        book_id = str(book_id).strip()

        print(f"📖 开始下载: site={site}, book_id={book_id}")

        async with aiohttp.ClientSession() as session:
            # 获取书籍详情
            detail_url = f"{self.base_url}/api/book_info/{site}/{book_id}"
            print(f"📖 获取书籍详情...")

            try:
                detail_result = await self._make_request(session, detail_url)
            except Exception as e:
                print(f"❌ 获取书籍详情失败: {e}")
                return None

            if not isinstance(detail_result, dict):
                print("❌ 获取书籍详情失败：数据格式错误")
                return None

            book_name = detail_result.get("book_name", "未知书籍")
            author = detail_result.get("author", "未知作者")
            summary = detail_result.get("summary", "无简介")

            print(f"📖 书名: {book_name}")
            print(f"✍  作者: {author}")

            # 提取章节
            volumes = detail_result.get("volumes", [])
            if not volumes:
                print("❌ 未找到章节信息")
                return None

            all_chapters = []
            for volume in volumes:
                chapters = volume.get("chapters", [])
                for chapter in chapters:
                    all_chapters.append({
                        "title": chapter.get("title", "未知章节"),
                        "chapter_id": chapter.get("chapterId", ""),
                        "url": chapter.get("url", "")
                    })

            if not all_chapters:
                print("❌ 未找到章节信息")
                return None

            print(f"📖 总章节数: {len(all_chapters)}")

            # 并发获取所有章节内容
            batch_size = 50
            all_content = []
            total_chapters = len(all_chapters)

            for batch_start in range(0, total_chapters, batch_size):
                batch_end = min(batch_start + batch_size, total_chapters)
                batch = all_chapters[batch_start:batch_end]
                print(f"📖 下载第 {batch_start+1}-{batch_end}/{total_chapters} 章...")

                async def fetch_chapter(chapter_data: dict) -> Optional[Dict]:
                    chapter_id = chapter_data["chapter_id"]
                    chapter_title = chapter_data["title"]

                    if not chapter_id:
                        return None

                    chapter_url = f"{self.base_url}/api/chapter/{site}/{book_id}/{chapter_id}"
                    try:
                        chapter_result = await self._make_request(session, chapter_url, timeout=10)

                        if not isinstance(chapter_result, dict):
                            return None

                        content = chapter_result.get("content", "")
                        if not content:
                            return None

                        return {
                            "title": chapter_title,
                            "content": content
                        }
                    except Exception:
                        return None

                tasks = [fetch_chapter(chapter) for chapter in batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for result in results:
                    if isinstance(result, dict) and result:
                        all_content.append(result)

                print(f"✅ 已获取 {len(all_content)}/{total_chapters} 章内容")

            if not all_content:
                print("❌ 未获取到任何章节内容")
                return None

            # 合并所有章节内容
            full_content = f"{book_name}\n作者: {author}\n来源: {site}\n\n"
            if summary:
                full_content += f"简介:\n{summary}\n\n"
            full_content += "=" * 60 + "\n\n"

            for chapter in all_content:
                title = chapter["title"]
                content = chapter["content"]
                full_content += "\n" + "=" * 40 + "\n"
                full_content += f"{title}\n"
                full_content += "=" * 40 + "\n\n"
                full_content += f"{content}\n\n"

            # 保存到文件
            filename = f"{book_name} - {author}.txt"
            filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

            print(f"\n✅ 下载完成！")
            print(f"📄 文件: {filepath}")
            print(f"📊 总字数: {len(full_content):,}")

            return filepath

    async def download_from_link(self, book_url: str) -> Optional[str]:
        """通过链接解析并下载小说

        Args:
            book_url: 小说链接，如 https://www.ciweimao.com/book/100472065

        Returns:
            下载文件的路径，失败返回 None
        """
        print(f"🔗 解析链接: {book_url}")

        async with aiohttp.ClientSession() as session:
            # 解析链接
            resolve_url = f"{self.base_url}/api/misc/resolve_url"
            resolve_data = {"url": book_url}

            try:
                resolve_result = await self._make_post_request(session, resolve_url, resolve_data)
            except Exception as e:
                print(f"❌ 链接解析失败: {e}")
                return None

            if not isinstance(resolve_result, dict) or not resolve_result.get("success"):
                print("❌ 链接解析失败，请检查链接是否正确")
                return None

            site = resolve_result.get("site", "")
            book_id = resolve_result.get("book_id", "")

            if not site or not book_id:
                print("❌ 无法从链接中提取书籍信息")
                return None

            print(f"✅ 解析成功: {site} - {book_id}")

            # 使用 download 方法下载
            return await self.download(f"{site}|{book_id}")


async def main():
    parser = argparse.ArgumentParser(
        description="聚合小说搜索下载脚本",
        epilog=""
    )
    parser.add_argument("action", choices=["search", "download", "link"], help="操作类型")
    parser.add_argument("query", nargs="?", help="搜索关键词或书籍信息")
    parser.add_argument("--output", "-o", default="./novel_data/jh", help="输出目录")
    parser.add_argument("--limit", "-l", type=int, default=20, help="搜索结果数量限制")

    args = parser.parse_args()

    print("=" * 60)
    print("📖 聚合小说搜索下载脚本")
    print("=" * 60)

    crawler = JhNovelCrawler(output_dir=args.output)

    if args.action == "search":
        if not args.query:
            print("❌ 请提供搜索关键词")
            return
        await crawler.search(args.query, args.limit)

    elif args.action == "download":
        if not args.query:
            print("❌ 请提供书籍信息（格式：来源|书籍ID）")
            return
        await crawler.download(args.query)

    elif args.action == "link":
        if not args.query:
            print("❌ 请提供小说链接")
            return
        await crawler.download_from_link(args.query)


if __name__ == "__main__":
    asyncio.run(main())
