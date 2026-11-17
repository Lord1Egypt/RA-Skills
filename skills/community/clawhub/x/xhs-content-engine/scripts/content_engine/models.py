"""Dataclasses for parsed XHS API responses.

所有 agent 看到的"干净结构"都在这里定义。原始 API JSON 不暴露。
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class NoteData:
    """一条 XHS 笔记的结构化元数据。"""

    note_id: str
    type: Literal["video", "normal"]
    title: str
    desc: str

    # 视频字段（type == "video" 时有效）
    video_url: str | None = None
    video_duration: int | None = None  # 秒
    video_width: int | None = None
    video_height: int | None = None

    # 图文字段（type == "normal" 时有效）
    image_urls: list[str] = field(default_factory=list)

    # 标签
    hashtags: list[str] = field(default_factory=list)  # 来自 hash_tag[]，已清理 [话题]
    topics: list[str] = field(default_factory=list)    # 来自 topics[]，算法精选

    # 互动数据（top-level）
    liked_count: int = 0
    collected_count: int = 0
    comments_count: int = 0
    shared_count: int = 0
    view_count: int = 0

    # 元信息
    time: int = 0  # unix ms
    ip_location: str = ""

    # 作者
    author_nickname: str = ""
    author_userid: str = ""
    author_red_id: str = ""

    @property
    def collect_to_like_ratio(self) -> float:
        """藏赞比 — XHS 上 >50% 视为高保存价值。"""
        if self.liked_count == 0:
            return 0.0
        return round(self.collected_count / self.liked_count, 2)


@dataclass
class Comment:
    """一条评论。"""

    id: str
    content: str
    like_count: int
    user_nickname: str
    user_red_id: str = ""
    ip_location: str = ""
    sub_count: int = 0  # 子评论数
    is_pinned: bool = False  # 启发式判断是否商家置顶（反诈骗 / 客服回复）

# 注：评论关键词分类（"问/求/夸/异议"）历史上有 Keyword dataclass，已删除。
# 理由：分类由 agent 在 Step 5c 直接读 comments.json 完成，比 regex 准确得多。
