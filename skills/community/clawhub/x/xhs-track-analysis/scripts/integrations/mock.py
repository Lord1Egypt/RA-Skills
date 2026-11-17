# -*- coding: utf-8 -*-
"""
scripts/integrations/mock.py
演示用 Mock 适配器：无需任何凭证即可跑通整条管线（归一化→CSV/MD），
用于验证 A 方案架构与下游衔接。真实接入时把 config.source 改为 pgy/juguang/thirdparty 并实现对应 adapter。
"""
from source_base import DataSource, NoteRecord
import datetime


class MockAdapter(DataSource):
    name = "Mock(演示)"

    def authenticate(self):
        return True

    def _mk(self, keyword, sort, i):
        return NoteRecord(
            keyword=keyword, sort=sort,
            note_id=f"mock_{keyword}_{sort}_{i}",
            url=f"https://www.xiaohongshu.com/explore/mock_{i}",
            title=f"[{keyword}] 示例笔记 {i}（{sort}）",
            author=f"达人{i}",
            author_type="self" if i % 2 else "third_party",
            commercialization=["natural", "suspected_promo", "paid", "unknown"][i % 4],
            likes=1000 * (i + 1), collects=800 * (i + 1), comments=200 * (i + 1),
            comment_sample=[f"示例评论{i}-向往状态", f"示例评论{i}-追问选择"],
            captured_at=datetime.date.today().isoformat(),
        )

    def search_notes(self, keyword, sort, limit=20):
        return [self._mk(keyword, sort, i) for i in range(min(limit, 5))]

    def get_note_detail(self, note_id):
        return NoteRecord(note_id=note_id, title="mock detail", captured_at=datetime.date.today().isoformat())

    def get_comments(self, note_id, limit=30):
        return [{"text": f"mock comment {j}"} for j in range(min(limit, 5))]

    def get_creator_profile(self, creator_id):
        return {"creator_id": creator_id, "followers": 100000}
