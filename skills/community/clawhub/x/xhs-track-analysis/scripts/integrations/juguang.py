# -*- coding: utf-8 -*-
"""
scripts/integrations/juguang.py
聚光（小红书官方广告/商业平台）适配器骨架。
- 用途：搜索词规划、行业大盘、关键词热度 —— 需求侧量级与趋势。
- 合规：需品牌自有聚光账号；以官方文档为准。
"""
try:
    import requests
except ImportError:
    requests = None  # 真实调用前需 pip install requests
from source_base import DataSource, NoteRecord


class JuguangAdapter(DataSource):
    name = "聚光(官方)"

    def authenticate(self):
        self.token = (self.config.get("credentials", {}).get("juguang_token")
                      or self.config.get("juguang_token"))
        if not self.token:
            raise RuntimeError("聚光需要品牌自有 token（config.credentials.juguang_token）。请配置后重试。")
        self.base_url = self.config.get("juguang_base_url", "https://juguang.xiaohongshu.com")
        return True

    def _map_note(self, raw, keyword, sort):
        return NoteRecord(
            keyword=keyword, sort=sort,
            note_id=str(raw.get("note_id") or ""),
            url=raw.get("url", ""),
            title=raw.get("title", ""),
            author=raw.get("author_name", ""),
            author_type="unknown",
            commercialization="unknown",
            likes=int(raw.get("likes", 0) or 0),
            collects=int(raw.get("collects", 0) or 0),
            comments=int(raw.get("comments", 0) or 0),
            captured_at=__import__("datetime").date.today().isoformat(),
        )

    def search_notes(self, keyword, sort, limit=20):
        # TODO: 聚光「搜索词/笔记」接口。示意：
        # resp = requests.get(f"{self.base_url}/api/keyword/notes",
        #                     headers={"Authorization": f"Bearer {self.token}"},
        #                     params={"keyword": keyword, "sort": sort})
        # return [self._map_note(x, keyword, sort) for x in resp.json()["data"]]
        raise NotImplementedError("聚光 adapter 为骨架：请按官方 API 文档实现 search_notes。")

    def get_note_detail(self, note_id):
        raise NotImplementedError("请按官方 API 填充 get_note_detail。")

    def get_comments(self, note_id, limit=30):
        raise NotImplementedError("请按官方 API 填充 get_comments。")

    def get_creator_profile(self, creator_id):
        raise NotImplementedError("请按官方 API 填充 get_creator_profile。")
