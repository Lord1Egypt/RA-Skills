# -*- coding: utf-8 -*-
"""
scripts/integrations/thirdparty.py
第三方数据分析平台适配器骨架（千瓜 / 新红 / 蝉妈妈 / 灰豚 等）。
- 用途：搜索词量级、笔记榜单、评论导出、达人画像、投放监测 —— 补量级与趋势。
- 合规：需对应平台订阅账号；各平台 API 不同，本文件给出通用模板，
  通过 config.credentials.thirdparty_platform 指定具体平台，按其实文档填充。
"""
try:
    import requests
except ImportError:
    requests = None  # 真实调用前需 pip install requests
from source_base import DataSource, NoteRecord


class ThirdPartyAdapter(DataSource):
    name = "第三方数据平台"

    def __init__(self, config=None):
        super().__init__(config)
        self.platform = (self.config.get("credentials", {}).get("thirdparty_platform") or "千瓜")

    def authenticate(self):
        self.token = (self.config.get("credentials", {}).get("thirdparty_token")
                      or self.config.get("thirdparty_token"))
        self.base_url = (self.config.get("credentials", {}).get("thirdparty_base_url")
                         or self.config.get("thirdparty_base_url", ""))
        if not self.token or not self.base_url:
            raise RuntimeError(
                f"{self.platform} 需要 base_url 与 token（config.credentials.thirdparty_*）。请配置后重试。"
            )
        self.name = f"第三方:{self.platform}"
        return True

    def _map_note(self, raw, keyword, sort):
        # 第三方平台常含"是否合作/投放"标记，可直接映射到商业化浓度
        promo = raw.get("is_promotion") or raw.get("is_cooperation")
        comm = "paid" if promo else "unknown"
        return NoteRecord(
            keyword=keyword, sort=sort,
            note_id=str(raw.get("note_id") or ""),
            url=raw.get("url", ""),
            title=raw.get("title", ""),
            author=raw.get("author_name", ""),
            author_type="unknown",
            commercialization=comm,
            likes=int(raw.get("likes", 0) or 0),
            collects=int(raw.get("collects", 0) or 0),
            comments=int(raw.get("comments", 0) or 0),
            captured_at=__import__("datetime").date.today().isoformat(),
        )

    def search_notes(self, keyword, sort, limit=20):
        # TODO: 按所选平台 API 实现。示意：
        # resp = requests.get(f"{self.base_url}/api/notes/search",
        #                     headers={"Authorization": f"Bearer {self.token}"},
        #                     params={"keyword": keyword, "sort": sort, "size": limit})
        # return [self._map_note(x, keyword, sort) for x in resp.json()["data"]["list"]]
        raise NotImplementedError(
            f"{self.platform} adapter 为骨架：请按其 API 文档实现 search_notes 与字段映射。"
        )

    def get_note_detail(self, note_id):
        raise NotImplementedError("请按平台 API 填充 get_note_detail。")

    def get_comments(self, note_id, limit=30):
        raise NotImplementedError("请按平台 API 填充 get_comments。")

    def get_creator_profile(self, creator_id):
        raise NotImplementedError("请按平台 API 填充 get_creator_profile。")
