"""
XHS Expert - 内容采集器
搜索笔记采集、详情页采集、评论采集
"""

import asyncio
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

from xhs_client import XHSClient
from state_parser import StateParser, NoteCard, CommentItem


class CollectConfig:
    """采集配置"""
    def __init__(
        self,
        keyword: str = "",
        max_notes: int = 100,
        max_comments: int = 50,
        delay: float = 1.0,
        sort: str = "general",
        output_dir: Optional[Path] = None
    ):
        self.keyword = keyword
        self.max_notes = max_notes
        self.max_comments = max_comments
        self.delay = delay
        self.sort = sort
        self.output_dir = output_dir or (
            Path.home() / ".config" / "xiaohongshu" / "data"
        )


class FeedCollector:
    """
    内容采集器（API模式）

    支持：
    - 关键词搜索采集
    - 单笔记详情采集
    - 批量采集
    - 数据持久化
    """

    def __init__(
        self,
        client: XHSClient,
        config: Optional[CollectConfig] = None
    ):
        self.client = client
        self.config = config or CollectConfig()
        self.parser = StateParser()
        self._collected: List[NoteCard] = []

    async def collect_search(
        self,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[NoteCard]:
        """
        采集搜索结果

        参数：
            progress_callback: 进度回调 (current, total)
        """
        page = 1
        total_collected = 0

        while total_collected < self.config.max_notes:
            result = await self.client.search_notes(
                keyword=self.config.keyword,
                page=page,
                page_size=20,
                sort=self.config.sort
            )

            items = result.get("items", []) if isinstance(result, dict) else []

            if not items:
                break

            for item in items:
                if total_collected >= self.config.max_notes:
                    break

                try:
                    note_card = NoteCard.from_search_item(item)
                    self._collected.append(note_card)
                    total_collected += 1

                    if progress_callback:
                        progress_callback(total_collected, self.config.max_notes)

                except Exception:
                    continue

            if len(items) < 20:
                break

            page += 1
            await asyncio.sleep(self.config.delay)

        return self._collected

    async def collect_detail(
        self,
        note_id: str,
        xsec_token: str = "",
        include_comments: bool = True
    ) -> Dict[str, Any]:
        """
        采集笔记详情

        返回结构：
            {
                "note": NoteCard,
                "comments": List[CommentItem],
                "raw_data": dict
            }
        """
        result = await self.client.get_note_detail(note_id, xsec_token=xsec_token)

        if not result:
            return {}

        note_data = result.get("items", [{}])[0] if result.get("items") else {}
        note = NoteCard.from_search_item({"note_card": note_data.get("note_card", {})})

        comments = []
        if include_comments:
            comments = await self._collect_comments(note_id)

        return {
            "note": note,
            "comments": comments,
            "raw_data": result
        }

    async def _collect_comments(
        self,
        note_id: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[CommentItem]:
        """采集评论"""
        comments = []

        while len(comments) < self.config.max_comments:
            result = await self.client.get_comments(
                note_id=note_id,
                cursor=str(offset),
                count=limit
            )

            if not result:
                break

            for c in result.get("comments", []):
                try:
                    comments.append(CommentItem.from_dict(c))
                except Exception:
                    continue

            if not result.get("has_more"):
                break

            offset += limit
            await asyncio.sleep(self.config.delay)

        return comments[:self.config.max_comments]

    async def collect_user_notes(
        self,
        user_id: str,
        max_count: int = 50
    ) -> List[NoteCard]:
        """采集用户所有笔记"""
        notes = []
        cursor = ""

        while len(notes) < max_count:
            url = "https://edith.xiaohongshu.com/api/sns/web/v1/user_posted"
            data = {
                "user_id": user_id,
                "cursor": cursor,
                "num": 20,
                "image_formats": ["jpg", "webp", "avif"]
            }

            result = await self.client.request("POST", url, data)

            if not result:
                break

            for item in result.get("notes", []):
                try:
                    notes.append(NoteCard.from_search_item({"note_card": item}))
                except Exception:
                    continue

            cursor = result.get("cursor", "")
            if not cursor:
                break

            await asyncio.sleep(self.config.delay)

        return notes[:max_count]

    def save_to_file(self, filepath: Optional[Path] = None) -> Path:
        """保存采集结果到文件"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            keyword_safe = "".join(
                c if c.isalnum() else "_" for c in self.config.keyword
            )
            filepath = self.config.output_dir / f"{keyword_safe}_{timestamp}.json"

        filepath.parent.mkdir(parents=True, exist_ok=True)

        data = [asdict(note) for note in self._collected]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath

    def get_summary(self) -> Dict[str, Any]:
        """获取采集摘要"""
        if not self._collected:
            return {"total": 0}

        total_likes = sum(n.like_count for n in self._collected)
        total_collects = sum(n.collect_count for n in self._collected)
        total_comments = sum(n.comment_count for n in self._collected)
        n = len(self._collected)

        return {
            "total": n,
            "total_likes": total_likes,
            "total_collects": total_collects,
            "total_comments": total_comments,
            "avg_likes": total_likes // n,
            "avg_collects": total_collects // n,
        }


class BrowserCollector:
    """
    浏览器辅助采集器

    用于需要JavaScript渲染或登录态的场景。
    通过提取页面 __INITIAL_STATE__ 获取数据，比DOM更稳定。
    """

    def __init__(self, page):
        self.page = page
        self.parser = StateParser()

    async def collect_search_page(self) -> List[NoteCard]:
        """采集当前搜索页"""
        html = await self.page.content()
        self.parser.extract_from_html(html)
        return self.parser.extract_note_cards()

    async def collect_detail_page(self) -> Dict[str, Any]:
        """采集当前详情页"""
        html = await self.page.content()
        self.parser.extract_from_html(html)

        note = self.parser.extract_note_detail()
        comments = self.parser.extract_comments()
        xsec_token = self.parser.extract_xsec_token()

        return {
            "note": note,
            "comments": comments,
            "xsec_token": xsec_token
        }

    async def scroll_and_collect(
        self,
        scroll_count: int = 5,
        scroll_delay: float = 1.0
    ) -> List[NoteCard]:
        """滚动页面并采集（用于无限滚动的Feed流）"""
        all_notes = []

        for _ in range(scroll_count):
            await self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            await asyncio.sleep(scroll_delay)
            notes = await self.collect_search_page()
            all_notes.extend(notes)

        # 去重
        seen_ids = set()
        unique_notes = []
        for note in all_notes:
            if note.note_id not in seen_ids:
                seen_ids.add(note.note_id)
                unique_notes.append(note)

        return unique_notes
