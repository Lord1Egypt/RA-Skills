"""把 XHS 爬虫接口原始 JSON 转成结构化 dataclass。

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
    """把 agent.delu.cn get_note_info 响应转成 NoteData。

    支持两类结构：
    - 旧版嵌套结构：data.data[0].note_list[0]
    - 新接口常见结构：note / data.note / data.data.note / data 本身

    Raises:
        ValueError: API 响应结构不对或缺关键字段。
    """
    n = _extract_note_object(api_response)

    note_type = _normalize_note_type(n)
    if note_type not in ("video", "normal"):
        # 视频 / 图文之外的类型暂不支持
        raise ValueError(f"Unsupported note type: {n.get('type') or n.get('note_type')!r}")

    stats = _first_dict(n, ("interact_info", "interaction", "stats", "counts"))
    author = _first_dict(n, ("user", "author", "user_info", "userInfo"))

    return NoteData(
        note_id=note_id,
        type=note_type,
        title=_pick_str(n, ("title", "display_title", "name")),
        desc=_pick_str(n, ("desc", "description", "content", "text")),
        # 视频
        video_url=_extract_video_url(n) if note_type == "video" else None,
        video_duration=_safe_int(_pick_nested(n, ("video.duration", "video_info.duration", "duration"))),
        video_width=_safe_int(_pick_nested(n, ("video.width", "video_info.width", "width"))),
        video_height=_safe_int(_pick_nested(n, ("video.height", "video_info.height", "height"))),
        # 图文
        image_urls=_extract_image_urls(n),
        # 标签
        hashtags=_extract_hashtags(n),
        topics=_extract_topics(n),
        # 互动
        liked_count=_safe_int(_pick_value(n, stats, ("liked_count", "like_count", "likes"))),
        collected_count=_safe_int(_pick_value(n, stats, ("collected_count", "collect_count", "favorite_count", "collects"))),
        comments_count=_safe_int(_pick_value(n, stats, ("comments_count", "comment_count", "comment_num", "comments"))),
        shared_count=_safe_int(_pick_value(n, stats, ("shared_count", "share_count", "shares"))),
        view_count=_safe_int(_pick_value(n, stats, ("view_count", "view_num", "views"))),
        # meta
        time=_safe_int(_pick_value(n, {}, ("time", "timestamp", "publish_time", "create_time"))),
        ip_location=_pick_str(n, ("ip_location", "ipLocation", "location")),
        # author
        author_nickname=_pick_str(author, ("nickname", "name", "user_name")),
        author_userid=_pick_str(author, ("userid", "user_id", "id")),
        author_red_id=_pick_str(author, ("red_id", "redId", "redid")),
    )


def _looks_like_note(value) -> bool:
    return isinstance(value, dict) and any(
        key in value
        for key in (
            "title",
            "display_title",
            "desc",
            "description",
            "video",
            "video_info",
            "images",
            "image_list",
            "images_list",
            "note_id",
            "id",
        )
    )


def _extract_note_object(api_response: dict) -> dict:
    candidates = []
    data = api_response.get("data") if isinstance(api_response, dict) else None
    nested = data.get("data") if isinstance(data, dict) else None

    if isinstance(api_response, dict):
        candidates.extend([
            api_response.get("note"),
            api_response.get("note_detail"),
            api_response,
        ])
    if isinstance(data, dict):
        candidates.extend([
            data.get("note"),
            data.get("note_detail"),
            data.get("note_info"),
            data,
        ])
        note_list = data.get("note_list")
        if isinstance(note_list, list) and note_list:
            candidates.append(note_list[0])
    if isinstance(nested, dict):
        candidates.extend([
            nested.get("note"),
            nested.get("note_detail"),
            nested.get("note_info"),
            nested,
        ])
        note_list = nested.get("note_list")
        if isinstance(note_list, list) and note_list:
            candidates.append(note_list[0])
    if isinstance(nested, list) and nested:
        first = nested[0]
        if isinstance(first, dict):
            note_list = first.get("note_list")
            if isinstance(note_list, list) and note_list:
                candidates.append(note_list[0])
            candidates.append(first)

    for candidate in candidates:
        if _looks_like_note(candidate):
            return candidate
    raise ValueError("Unexpected API response shape: note object not found")


def _normalize_note_type(note: dict) -> str:
    raw_value = note.get("type") or note.get("note_type") or note.get("noteType")
    raw = str(raw_value or "").lower()
    if raw in ("video", "视频", "1"):
        return "video"
    if raw in ("normal", "image", "images", "图文", "图片", "0"):
        return "normal"
    if raw:
        return raw
    if _extract_video_url(note):
        return "video"
    if _extract_image_urls(note):
        return "normal"
    return raw


def _first_dict(source: dict, keys: tuple[str, ...]) -> dict:
    for key in keys:
        value = source.get(key)
        if isinstance(value, dict):
            return value
    return {}


def _pick_str(source: dict, keys: tuple[str, ...]) -> str:
    value = _pick_value(source, {}, keys)
    return "" if value is None else str(value).strip()


def _pick_value(primary: dict, secondary: dict, keys: tuple[str, ...]):
    for key in keys:
        if key in primary and primary.get(key) is not None:
            return primary.get(key)
        if key in secondary and secondary.get(key) is not None:
            return secondary.get(key)
    return None


def _pick_nested(source: dict, paths: tuple[str, ...]):
    for path in paths:
        current = source
        for part in path.split("."):
            if not isinstance(current, dict) or part not in current:
                current = None
                break
            current = current.get(part)
        if current is not None:
            return current
    return None


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
    v = note.get("video", {}) or note.get("video_info", {}) or {}
    # 常见路径，按优先级 try
    if url := v.get("url"):
        return url
    # XHS 老版本可能的路径：video.media.stream.h264[0].master_url
    try:
        return v["media"]["stream"]["h264"][0]["master_url"]
    except (KeyError, IndexError, TypeError):
        pass
    for stream_key in ("h264", "h265", "av1"):
        try:
            streams = v["media"]["stream"][stream_key]
            if isinstance(streams, list) and streams:
                if url := streams[0].get("master_url") or streams[0].get("url"):
                    return url
        except (KeyError, IndexError, TypeError):
            pass
    for key in ("videoUrl", "video_url", "mediaUrl", "video_url_default", "url"):
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
        or note.get("image_urls")
        or note.get("imageUrls")
        or note.get("pictures")
        or []
    )
    out: list[str] = []
    for img in candidates:
        if isinstance(img, str):
            out.append(img)
        elif isinstance(img, dict):
            url = (
                img.get("url_default")
                or img.get("url")
                or img.get("urlDefault")
                or img.get("origin_url")
                or img.get("original")
                or img.get("src")
                or ""
            )
            if not url and isinstance(img.get("url_list"), list) and img["url_list"]:
                url = img["url_list"][0]
            if url:
                out.append(url)
    return out


_TAG_MARKER_RE = re.compile(r"\[话题\]")


def clean_tag(s: str) -> str:
    """清掉 XHS 渲染标记 [话题]。"""
    return _TAG_MARKER_RE.sub("", s).strip()


def _extract_hashtags(note: dict) -> list[str]:
    """从 hash_tag / tags / tag_list 提取所有标签（已清理）。"""
    out: list[str] = []
    sources = (
        (note.get("hash_tag") or note.get("hashTags") or [], False),
        (note.get("tags") or note.get("tag_list") or [], True),
    )
    for items, allow_strings in sources:
        for h in items:
            if isinstance(h, str) and allow_strings:
                cleaned = clean_tag(h)
                if cleaned:
                    out.append(cleaned)
            if isinstance(h, dict):
                name = h.get("name") or h.get("tag_name") or h.get("text") or ""
                if name:
                    cleaned = clean_tag(name)
                    if cleaned:
                        out.append(cleaned)
    return out


def _extract_topics(note: dict) -> list[str]:
    """从 topics[].name 提取算法精选 topic（通常 1-2 个）。"""
    out: list[str] = []
    for t in (note.get("topics") or note.get("topic_list") or []):
        if isinstance(t, str):
            out.append(clean_tag(t))
        if isinstance(t, dict):
            name = t.get("name") or t.get("topic_name") or t.get("text") or ""
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
    raw_comments = _extract_comment_list(api_response)
    out: list[Comment] = []
    for c in raw_comments:
        if not isinstance(c, dict):
            continue
        u = c.get("user") or c.get("author") or c.get("user_info") or {}
        content = (
            c.get("content")
            or c.get("text")
            or c.get("desc")
            or c.get("comment_content")
            or ""
        )
        is_pinned = (
            any(p in content for p in _PINNED_PATTERNS)
            or bool(c.get("is_pinned") or c.get("pinned"))
            or _safe_int(c.get("score")) > 1_000_000  # 服务端高 score = 置顶
        )
        out.append(Comment(
            id=str(c.get("id") or c.get("comment_id") or ""),
            content=content,
            like_count=_safe_int(c.get("like_count") or c.get("liked_count") or c.get("likes")),
            user_nickname=u.get("nickname") or u.get("name") or "",
            user_red_id=u.get("red_id") or u.get("redId") or "",
            ip_location=c.get("ip_location") or c.get("ipLocation") or "",
            sub_count=_safe_int(c.get("sub_comment_count") or c.get("sub_count") or c.get("reply_count")),
            is_pinned=is_pinned,
        ))
    return out


def _extract_comment_list(api_response: dict) -> list:
    data = api_response.get("data") if isinstance(api_response, dict) else None
    nested = data.get("data") if isinstance(data, dict) else None
    candidates = []
    if isinstance(api_response, dict):
        candidates.extend([
            api_response.get("comments"),
            api_response.get("comment_list"),
            api_response.get("items"),
            api_response.get("list"),
        ])
    if isinstance(data, dict):
        candidates.extend([
            data.get("comments"),
            data.get("comment_list"),
            data.get("items"),
            data.get("list"),
        ])
    if isinstance(nested, dict):
        candidates.extend([
            nested.get("comments"),
            nested.get("comment_list"),
            nested.get("items"),
            nested.get("list"),
        ])
    for candidate in candidates:
        if isinstance(candidate, list):
            return candidate
    return []


# ---------------- 注：评论语义分类 ----------------
# 历史版本曾有 _KEYWORD_PATTERNS + extract_keywords() 用 regex 把评论分类成
# "问/求/夸/异议"。已删除——理由：
#   1. 语言无穷变体（"怎么卖" / "啥价" / "贵不贵" / "多少米"），regex 永远漏抓
#   2. regex 分不清语义（"价格不是问题" 不是询价；"不是真丝吗" 不是异议）
#   3. agent 本身是 LLM，比 regex 强 100 倍，让它在 Step 5c 直接读 comments.json
#      做分类，零维护成本，零盲点
#
# 详见 SKILL.md Step 5c。
