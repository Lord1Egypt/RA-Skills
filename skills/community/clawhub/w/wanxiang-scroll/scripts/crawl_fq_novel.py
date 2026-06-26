#!/usr/bin/env python3
"""
番茄小说搜索下载脚本 - 独立版本

从番茄小说 API 搜索和下载小说
API 来源：https://sy.newapi.com.cn/docs
"""

import os
import re
import json
import argparse
import requests
from datetime import datetime
from typing import Optional, List, Dict


class FqNovelCrawler:
    """番茄小说爬虫"""

    def __init__(self, output_dir: str = "./novel_data/fq", api_base: str = ""):
        if api_base:
            cleaned_url = api_base.rstrip('/')
            if '/api' not in cleaned_url:
                self.base_url = f"{cleaned_url}/api"
            else:
                self.base_url = cleaned_url
        else:
            self.base_url = "https://sy.newapi.com.cn/api"

        self.output_dir = output_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        os.makedirs(output_dir, exist_ok=True)

        print(f"📡 API 地址: {self.base_url}")
        self._test_connection()

    def _test_connection(self):
        """测试 API 连通性"""
        try:
            test_url = f"{self.base_url}/device/status"
            response = requests.get(test_url, headers=self.headers, timeout=5)
            result = response.json()
            if isinstance(result, dict) and result.get('code') == 200:
                device_id = result.get('data', {}).get('device_id', 'N/A')
                print(f"✅ API 连接成功，设备ID: {device_id}")
            else:
                print(f"⚠ API 连接异常: code = {result.get('code', 'N/A')}")
        except Exception as e:
            print(f"⚠ API 连接测试失败: {e}")

    def _make_request(self, url: str, timeout: int = 15) -> dict:
        """发送 HTTP 请求"""
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            return response.json()
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            raise

    def search(self, keyword: str, limit: int = 20) -> List[Dict]:
        """搜索小说"""
        print(f"🔍 搜索关键词: {keyword}")

        search_url = f"{self.base_url}/search?keyword={keyword}&limit={limit}"

        try:
            result = self._make_request(search_url)
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []

        if not isinstance(result, dict):
            print("❌ 搜索失败：返回数据格式错误")
            return []

        data = result.get("data", [])
        if not data:
            print("❌ 未找到匹配的小说")
            return []

        print(f"\n📚 找到 {len(data)} 本小说:\n")
        print("-" * 80)

        for i, book in enumerate(data[:limit], 1):
            title = book.get("book_name", "未知")
            author = book.get("author", "未知")
            category = book.get("category", "未知")
            word_count = book.get("word_count", 0)
            chapter_count = book.get("chapter_count", 0)
            score = book.get("score", "N/A")
            status = book.get("status", "未知")
            book_id = book.get("book_id", "")

            if isinstance(word_count, (int, float)):
                if word_count >= 10000:
                    word_count_str = f"{word_count / 10000:.1f}万"
                else:
                    word_count_str = str(int(word_count))
            else:
                word_count_str = str(word_count)

            print(f"{i}. {title}")
            print(f"   作者: {author} | 分类: {category}")
            print(f"   字数: {word_count_str} | 章节: {chapter_count} | 评分: {score} | {status}")
            print(f"   书籍ID: {book_id}")
            print("-" * 80)

        return data[:limit]

    def download(self, book_id: str) -> Optional[str]:
        """下载整本小说

        Args:
            book_id: 书籍ID

        Returns:
            下载文件的路径，失败返回 None
        """
        book_id = str(book_id)
        print(f"📖 开始下载: book_id={book_id}")

        # 获取书籍详情
        detail_url = f"{self.base_url}/detail?book_id={book_id}"
        print(f"� 获取书籍详情...")

        try:
            detail_result = self._make_request(detail_url)
        except Exception as e:
            print(f"❌ 获取书籍详情失败: {e}")
            return None

        if detail_result.get("code") != 200:
            print(f"❌ 获取书籍详情失败: {detail_result.get('message', '未知错误')}")
            return None

        data_obj = detail_result.get("data", {})
        if not isinstance(data_obj, dict):
            print("❌ 获取书籍详情失败：数据格式错误")
            return None

        book_data = data_obj.get("data", {})
        if not isinstance(book_data, dict):
            print("❌ 获取书籍详情失败：数据格式错误")
            return None

        book_name = book_data.get("book_name", "未知书籍")
        author = book_data.get("author", "未知作者")

        print(f"📖 书名: {book_name}")
        print(f"✍  作者: {author}")

        # 获取章节目录
        dir_url = f"{self.base_url}/book?book_id={book_id}"

        try:
            dir_result = self._make_request(dir_url)
        except Exception as e:
            print(f"❌ 获取章节目录失败: {e}")
            return None

        if dir_result.get("code") != 200:
            print(f"❌ 获取章节目录失败: {dir_result.get('message', '未知错误')}")
            return None

        data_obj2 = dir_result.get("data", {})
        if not isinstance(data_obj2, dict):
            print("❌ 获取章节目录失败：数据格式错误")
            return None

        inner_data = data_obj2.get("data", {})
        if not isinstance(inner_data, dict):
            print("❌ 获取章节目录失败：数据格式错误")
            return None

        chapter_list_with_volume = inner_data.get("chapterListWithVolume", [])

        if not chapter_list_with_volume:
            print("❌ 未找到章节信息")
            return None

        all_chapters = []
        for volume_list in chapter_list_with_volume:
            all_chapters.extend(volume_list)

        if not all_chapters:
            print("❌ 未找到章节信息")
            return None

        print(f"� 总章节数: {len(all_chapters)}")

        # 批量获取章节内容
        batch_size = 30
        all_content = []

        for i in range(0, len(all_chapters), batch_size):
            batch = all_chapters[i:i + batch_size]
            item_ids = ",".join([c.get("itemId") for c in batch if c.get("itemId")])

            print(f"� 下载第 {i+1}-{i+len(batch)} 章...")

            batch_url = f"{self.base_url}/content?tab=批量&item_ids={item_ids}&book_id={book_id}"

            try:
                batch_result = self._make_request(batch_url)
            except Exception:
                continue

            if batch_result.get("code") != 200:
                continue

            chapters_data = batch_result.get("data", {}).get("chapters", [])
            if not chapters_data:
                continue

            def normalize_title(title: str) -> str:
                cn_nums = {
                    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
                }

                def cn_to_int(cn_str: str) -> int:
                    special_nums = {
                        '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
                        '十六': 16, '十七': 17, '十八': 18, '十九': 19,
                        '二十': 20, '三十': 30, '四十': 40, '五十': 50,
                        '六十': 60, '七十': 70, '八十': 80, '九十': 90, '一百': 100
                    }
                    if cn_str in special_nums:
                        return special_nums[cn_str]
                    if cn_str.startswith('一百零') and len(cn_str) >= 4 and cn_str[3] in cn_nums:
                        return 100 + cn_nums[cn_str[3]]
                    if (len(cn_str) == 3 and cn_str[0] in cn_nums
                            and cn_str[1] == '十' and cn_str[2] in cn_nums):
                        return cn_nums[cn_str[0]] * 10 + cn_nums[cn_str[2]]
                    if cn_str in cn_nums:
                        return cn_nums[cn_str]
                    return 0

                match = re.match(r'^第([一二三四五六七八九十百千万零]+)章', title)
                if match:
                    cn_num = match.group(1)
                    arabic_num = cn_to_int(cn_num)
                    if arabic_num > 0:
                        title = title.replace(f'第{cn_num}章', f'第{arabic_num}章', 1)
                return title

            title_map = {}
            for ch in chapters_data:
                norm_title = normalize_title(ch.get("title", ""))
                title_map[norm_title] = ch

            ordered_batch = []
            for chapter in batch:
                title = chapter.get("title")
                norm_title = normalize_title(title)
                if norm_title in title_map:
                    ordered_batch.append(title_map[norm_title])

            all_content.extend(ordered_batch)

            print(f"✅ 已获取 {len(all_content)} 章内容")

        if not all_content:
            print("❌ 未获取到任何章节内容")
            return None

        # 合并所有章节内容
        full_content = f"{book_name}\n作者: {author}\n\n"
        for chapter in all_content:
            title = chapter.get("title", "未知章节")
            content = chapter.get("content", "")
            if content:
                full_content += f"{'='*40}\n{title}\n{'='*40}\n\n{content}\n\n"

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

    def extract_book_id_from_url(self, url: str) -> Optional[str]:
        """从分享链接提取书籍ID"""
        if "changdunovel.com" in url:
            match = re.search(r'book_id=(\d+)', url)
            if match:
                return match.group(1)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="番茄小说搜索下载脚本",
        epilog=""
    )
    parser.add_argument("action", choices=["search", "download"], help="操作类型")
    parser.add_argument("query", nargs="?", help="搜索关键词或书籍ID")
    parser.add_argument("--output", "-o", default="./novel_data/fq", help="输出目录")
    parser.add_argument("--api", "-a", default="", help="自定义 API 地址")
    parser.add_argument("--limit", "-l", type=int, default=20, help="搜索结果数量限制")

    args = parser.parse_args()

    print("=" * 60)
    print("� 番茄小说搜索下载脚本")
    print("=" * 60)

    crawler = FqNovelCrawler(output_dir=args.output, api_base=args.api)

    if args.action == "search":
        if not args.query:
            print("❌ 请提供搜索关键词")
            return
        crawler.search(args.query, args.limit)

    elif args.action == "download":
        if not args.query:
            print("❌ 请提供书籍ID")
            return

        query = args.query

        if "changdunovel.com" in query:
            book_id = crawler.extract_book_id_from_url(query)
            if book_id:
                print(f"✅ 从链接提取书籍ID: {book_id}")
                query = book_id
            else:
                print("❌ 无法从链接中提取书籍ID")
                return

        crawler.download(query)


if __name__ == "__main__":
    main()
