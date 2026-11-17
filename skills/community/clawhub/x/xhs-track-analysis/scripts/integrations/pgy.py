# -*- coding: utf-8 -*-
"""
scripts/integrations/pgy.py
蒲公英（小红书官方商业平台）适配器骨架。
- 用途：达人搜索、笔记数据、合作报价、粉丝画像 —— 达人侧事实数据首选。
- 合规：需品牌自有蒲公英账号与授权；以官方开放平台文档为准。
- 本文件为骨架：authenticate 可用，search_notes 等方法给出"请求→字段映射"模板，
  真实 endpoint 与字段名请按蒲公英官方 API 文档填充。
"""
try:
    import requests
except ImportError:
    requests = None  # 真实调用前需 pip install requests
from source_base import DataSource, NoteRecord


class PgyAdapter(DataSource):
    name = "蒲公英(官方)"

    def authenticate(self):
        self.token = (self.config.get("credentials", {}).get("pgy_token")
                      or self.config.get("pgy_token"))
        if not self.token:
            raise RuntimeError("蒲公英需要品牌自有 token（config.credentials.pgy_token）。请配置后重试。")
        self.base_url = self.config.get("pgy_base_url", "https://open.xiaohongshu.com")
        return True

    # ---- 字段映射模板：把平台原始 JSON 映射为 NoteRecord ----
    def _map_note(self, raw: dict, keyword: str, sort: str) -> NoteRecord:
        return NoteRecord(
            keyword=keyword, sort=sort,
            note_id=str(raw.get("note_id") or raw.get("id") or ""),
            url=raw.get("url", ""),
            title=raw.get("title", ""),
            author=raw.get("author_name", raw.get("nickname", "")),
            author_type="self",  # 蒲公英多为达人本人数据
            commercialization="unknown",  # 平台通常不直接给，需结合内容判断
            likes=int(raw.get("likes", 0) or 0),
            collects=int(raw.get("collects", 0) or 0),
            comments=int(raw.get("comments", 0) or 0),
            captured_at=__import__("datetime").date.today().isoformat(),
        )

    def search_notes(self, keyword, sort, limit=20):
        # TODO: 按蒲公英「笔记搜索」接口实现。示意：
        # resp = requests.get(f"{self.base_url}/api/...",
        #                     headers={"Authorization": f"Bearer {self.token}"},
        #                     params={"keyword": keyword, "sort": sort, "page_size": limit})
        # return [self._map_note(x, keyword, sort) for x in resp.json()["data"]["notes"]]
        raise NotImplementedError(
            "蒲公英 adapter 为骨架：请按官方 API 文档实现 search_notes 的请求与字段映射。"
        )

    def get_note_detail(self, note_id):
        raise NotImplementedError("请按官方 API 填充 get_note_detail。")

    def get_comments(self, note_id, limit=30):
        raise NotImplementedError("请按官方 API 填充 get_comments。")

    def get_creator_profile(self, creator_id):
        raise NotImplementedError("请按官方 API 填充 get_creator_profile（粉丝/领域/报价）。")
