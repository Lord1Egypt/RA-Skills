"""把 TikHub 原始 JSON 转成结构化 dataclass。

职责边界：
- 本模块只做**结构化解析**（API JSON → dataclass）
- 评论的"问/求/夸/异议"语义分类不在这里做——交给 agent 在 Step 5c 直接读
  comments.json 自己分类（LLM 比 regex 更准、零维护成本）
"""

from __future__ import annotations
import re

from .models import NoteData, Comment


# ---------------- Note parsing ----------------

def parse_note(api_response: dict, note_id: str) -> NoteData:
    """把 TikHub get_note_info 响应转成 NoteData。

    Raises:
        ValueError: API 响应结构不对或缺关键字段。
    """
    try:
        n = api_response["data"]["data"][0]["note_list"][0]
    except (KeyError, IndexError, TypeError) as e:
        raise ValueError(f"Unexpected API response shape: {e}") from e

    note_type = n.get("type", "")
    if note_type not in ("video", "normal"):
        # 视频 / 图文之外的类型暂不支持
        raise ValueError(f"Unsupported note type: {note_type!r}")

    return NoteData(
        note_id=note_id,
        type=note_type,
        title=n.get("title", "") or "",
        desc=n.get("desc", "") or "",
        # 视频
        video_url=_extract_video_url(n) if note_type == "video" else None,
        video_duration=_safe_int((n.get("video") or {}).get("duration")),
        video_width=_safe_int((n.get("video") or {}).get("width")),
        video_height=_safe_int((n.get("video") or {}).get("height")),
        # 图文
        image_urls=_extract_image_urls(n),
        # 标签
        hashtags=_extract_hashtags(n),
        topics=_extract_topics(n),
        # 互动
        liked_count=_safe_int(n.get("liked_count")),
        collected_count=_safe_int(n.get("collected_count")),
        comments_count=_safe_int(n.get("comments_count")),
        shared_count=_safe_int(n.get("shared_count")),
        view_count=_safe_int(n.get("view_count")),
        # meta
        time=_safe_int(n.get("time")),
        ip_location=n.get("ip_location", "") or "",
        # author
        author_nickname=(n.get("user") or {}).get("nickname", "") or "",
        author_userid=(n.get("user") or {}).get("userid", "") or "",
        author_red_id=(n.get("user") or {}).get("red_id", "") or "",
    )


def _safe_int(v) -> int:
    """把可能是 None / str / float 的值转 int，失败返回 0。"""
    if v is None:
        return 0
    try:
        return int(v)
    except (ValueError, TypeError):
        return 0


def _extract_video_url(note: dict) -> str | None:
    """从多种可能的字段位置提取视频 URL。"""
    v = note.get("video", {}) or {}
    # 常见路径，按优先级 try
    if url := v.get("url"):
        return url
    # XHS 老版本可能的路径：video.media.stream.h264[0].master_url
    try:
        return v["media"]["stream"]["h264"][0]["master_url"]
    except (KeyError, IndexError, TypeError):
        pass
    for key in ("videoUrl", "video_url", "mediaUrl"):
        if url := note.get(key):
            return url
    return None


def _extract_image_urls(note: dict) -> list[str]:
    """提取图文笔记的所有图片 URL。

    XHS 字段名不一致：images_list / image_list / images / imageList 都见过。
    """
    candidates = (
        note.get("images_list")
        or note.get("image_list")
        or note.get("images")
        or note.get("imageList")
        or []
    )
    out: list[str] = []
    for img in candidates:
        if isinstance(img, str):
            out.append(img)
        elif isinstance(img, dict):
            url = img.get("url_default") or img.get("url") or img.get("urlDefault") or ""
            if url:
                out.append(url)
    return out


_TAG_MARKER_RE = re.compile(r"\[话题\]")


def clean_tag(s: str) -> str:
    """清掉 XHS 渲染标记 [话题]。"""
    return _TAG_MARKER_RE.sub("", s).strip()


def _extract_hashtags(note: dict) -> list[str]:
    """从 hash_tag[].name 提取所有标签（已清理）。"""
    out: list[str] = []
    for h in (note.get("hash_tag") or []):
        if isinstance(h, dict):
            name = h.get("name", "")
            if name:
                cleaned = clean_tag(name)
                if cleaned:
                    out.append(cleaned)
    return out


def _extract_topics(note: dict) -> list[str]:
    """从 topics[].name 提取算法精选 topic（通常 1-2 个）。"""
    out: list[str] = []
    for t in (note.get("topics") or []):
        if isinstance(t, dict):
            name = t.get("name", "")
            if name:
                out.append(clean_tag(name))
    return out


# ---------------- Comment parsing ----------------

# 启发式：商家置顶评论的特征关键词
_PINNED_PATTERNS = (
    "认准本账号",
    "请不要上当受骗",
    "其他的回复都是骗子",
    "客服回复",
)


def parse_comments(api_response: dict) -> list[Comment]:
    """把评论 API 响应转成 Comment 列表。"""
    inner = api_response.get("data", {})
    if isinstance(inner, dict):
        inner = inner.get("data", {})
    if not isinstance(inner, dict):
        return []

    raw_comments = inner.get("comments", []) or []
    out: list[Comment] = []
    for c in raw_comments:
        if not isinstance(c, dict):
            continue
        u = c.get("user", {}) or {}
        content = c.get("content", "") or ""
        is_pinned = (
            any(p in content for p in _PINNED_PATTERNS)
            or _safe_int(c.get("score")) > 1_000_000  # 服务端高 score = 置顶
        )
        out.append(Comment(
            id=c.get("id", "") or "",
            content=content,
            like_count=_safe_int(c.get("like_count")),
            user_nickname=u.get("nickname", "") or "",
            user_red_id=u.get("red_id", "") or "",
            ip_location=c.get("ip_location", "") or "",
            sub_count=_safe_int(c.get("sub_comment_count")),
            is_pinned=is_pinned,
        ))
    return out


# ---------------- 注：评论语义分类 ----------------
# 历史版本曾有 _KEYWORD_PATTERNS + extract_keywords() 用 regex 把评论分类成
# "问/求/夸/异议"。已删除——理由：
#   1. 语言无穷变体（"怎么卖" / "啥价" / "贵不贵" / "多少米"），regex 永远漏抓
#   2. regex 分不清语义（"价格不是问题" 不是询价；"不是真丝吗" 不是异议）
#   3. agent 本身是 LLM，比 regex 强 100 倍，让它在 Step 5c 直接读 comments.json
#      做分类，零维护成本，零盲点
#
# 详见 SKILL.md Step 5c。
