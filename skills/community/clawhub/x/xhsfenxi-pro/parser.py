"""
解析器：从拦截到的 API JSON 或 DOM 中提取结构化数据
兼容两种来源：API JSON（优先）和 DOM fallback
"""
from __future__ import annotations
from typing import List, Optional
from .models import Note, Comment, UserProfile


def parse_note_from_api(raw: dict) -> Note:
    """从 API JSON 解析笔记"""
    note_card = raw.get("note_card") or raw
    basic = note_card.get("basic_info") or {}
    interact = note_card.get("interact_info") or {}
    user = note_card.get("user") or {}

    note = Note()
    note.id = (
        raw.get("id")
        or note_card.get("note_id")
        or basic.get("note_id", "")
    )
    note.title = (
        note_card.get("display_title")
        or note_card.get("title")
        or basic.get("title", "")
    )
    note.content = note_card.get("desc") or basic.get("desc", "")
    note.author = user.get("nickname", "")
    note.author_id = user.get("user_id", "")
    note.likes = str(interact.get("liked_count", ""))
    note.collects = str(interact.get("collected_count", ""))
    note.comments_count = str(interact.get("comment_count", ""))
    note.type = "video" if note_card.get("type") == "video" else "normal"

    # 图片
    image_list = note_card.get("image_list") or []
    note.images = [img.get("url", "") for img in image_list if img.get("url")]

    # 标签
    tag_list = note_card.get("tag_list") or []
    note.tags = [t.get("name", "") for t in tag_list if t.get("name")]

    note.raw = raw
    return note


def parse_search_response(api_cache: dict) -> List[Note]:
    """从拦截的搜索 API 响应中提取笔记列表"""
    notes = []
    for url, data in api_cache.items():
        if "search" not in url:
            continue
        items = (
            data.get("data", {}).get("items")
            or data.get("items")
            or []
        )
        for item in items:
            note_raw = item.get("note_card") or item
            if not note_raw:
                continue
            n = parse_note_from_api({"id": item.get("id", ""), "note_card": note_raw})
            xsec = item.get("xsec_token", "")
            note_id = item.get("id") or note_raw.get("note_id") or n.id
            if note_id:
                n.url = f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec}&xsec_source=pc_search"
            notes.append(n)
    return notes


def parse_user_notes_response(api_cache: dict) -> List[Note]:
    """从拦截的用户主页 API 响应中提取笔记列表"""
    notes = []
    for url, data in api_cache.items():
        if "user_posted" not in url and "user/notes" not in url:
            continue
        items = (
            data.get("data", {}).get("notes")
            or data.get("notes")
            or []
        )
        for item in items:
            n = parse_note_from_api(item)
            note_id = n.id or item.get("note_id", "")
            if note_id:
                n.url = f"https://www.xiaohongshu.com/explore/{note_id}"
            notes.append(n)
    return notes


def parse_note_detail_response(api_cache: dict) -> Optional[Note]:
    """从拦截的笔记详情 API 响应中提取单篇笔记"""
    for url, data in api_cache.items():
        if "feed" not in url and "note/detail" not in url:
            continue
        items = data.get("data", {}).get("items") or []
        for item in items:
            note_card = item.get("note_card") or {}
            if note_card:
                n = parse_note_from_api({"note_card": note_card})
                # 评论
                comments_data = data.get("data", {}).get("comments") or []
                for c in comments_data:
                    comment = Comment(
                        user=c.get("user_info", {}).get("nickname", ""),
                        text=c.get("content", ""),
                        likes=str(c.get("like_count", "")),
                        time=c.get("create_time", ""),
                    )
                    n.comments.append(comment)
                return n
    return None


def parse_comment_page_response(api_cache: dict) -> List[Comment]:
    """从 v2/comment/page API 解析评论列表"""
    comments = []
    for url, data in api_cache.items():
        if "comment" not in url:
            continue
        items = (
            data.get("data", {}).get("comments")
            or data.get("comments")
            or []
        )
        for c in items:
            user_info = c.get("user_info") or {}
            comment = Comment(
                user=user_info.get("nickname", ""),
                text=c.get("content", ""),
                likes=str(c.get("like_count", "")),
                time=str(c.get("create_time", "")),
            )
            comments.append(comment)
    return comments


def parse_dom_notes(browser) -> List[Note]:
    """DOM fallback：从页面元素中提取笔记（API 拦截失败时使用）"""
    notes = []
    selectors = ["section.note-item", ".note-item", "[class*='note-item']"]
    items = []
    for sel in selectors:
        items = browser.find_elements(sel)
        if items:
            break

    for item in items:
        note = Note()
        for sel in ["a.title span", ".title span", "span.title"]:
            try:
                note.title = item.find_element("css selector", sel).text.strip()
                break
            except Exception:
                pass
        try:
            note.url = item.find_element("css selector", "a.cover").get_attribute("href")
        except Exception:
            pass
        try:
            note.likes = item.find_element("css selector", "span.count").text.strip()
        except Exception:
            pass
        try:
            item.find_element("css selector", ".play-icon")
            note.type = "video"
        except Exception:
            note.type = "normal"

        if note.title or note.url:
            notes.append(note)
    return notes
