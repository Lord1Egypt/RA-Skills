"""parsers.py 单元测试 — 用 stdlib unittest，零外部依赖。

跑法：
    cd <skill 根>
    python3 -m unittest tests.test_parsers -v
"""

import sys
import unittest
from pathlib import Path

# 让测试能 import 包
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine.parsers import (
    parse_note,
    parse_comments,
    clean_tag,
    _safe_int,
    _extract_hashtags,
    _extract_image_urls,
    _extract_video_url,
)


# ─── parse_note ────────────────────────────────────

def _make_video_response(**overrides):
    """造一个最小可用的 video 笔记 API 响应。"""
    note = {
        "type": "video",
        "title": "测试标题",
        "desc": "测试描述",
        "video": {
            "url": "https://cdn.example.com/v.mp4",
            "duration": 30,
            "width": 720,
            "height": 1280,
        },
        "hash_tag": [
            {"name": "深圳新中式[话题]"},
            {"name": "国风穿搭"},
        ],
        "topics": [{"name": "深圳新中式"}],
        "liked_count": 100,
        "collected_count": 80,
        "comments_count": 20,
        "shared_count": 5,
        "view_count": 0,
        "time": 1700000000000,
        "ip_location": "广东",
        "user": {"nickname": "测试账号", "userid": "u1", "red_id": "r1"},
    }
    note.update(overrides)
    return {"data": {"data": [{"note_list": [note]}]}}


class TestParseNote(unittest.TestCase):

    def test_basic_video_parsing(self):
        n = parse_note(_make_video_response(), "test_id")
        self.assertEqual(n.note_id, "test_id")
        self.assertEqual(n.type, "video")
        self.assertEqual(n.title, "测试标题")
        self.assertEqual(n.video_url, "https://cdn.example.com/v.mp4")
        self.assertEqual(n.video_duration, 30)
        self.assertEqual(n.liked_count, 100)
        self.assertEqual(n.collect_to_like_ratio, 0.8)
        # hash_tag 渲染标记被清理
        self.assertEqual(n.hashtags, ["深圳新中式", "国风穿搭"])
        self.assertEqual(n.author_nickname, "测试账号")

    def test_collect_to_like_ratio_zero_division(self):
        resp = _make_video_response(liked_count=0, collected_count=10)
        n = parse_note(resp, "test_id")
        self.assertEqual(n.collect_to_like_ratio, 0.0)

    def test_unsupported_type_raises(self):
        resp = _make_video_response(type="unknown_type")
        with self.assertRaises(ValueError) as ctx:
            parse_note(resp, "test_id")
        self.assertIn("Unsupported note type", str(ctx.exception))

    def test_malformed_response_raises(self):
        with self.assertRaises(ValueError):
            parse_note({"data": {}}, "test_id")
        with self.assertRaises(ValueError):
            parse_note({}, "test_id")

    def test_image_post(self):
        resp = _make_video_response(
            type="normal",
            video=None,
            images_list=[
                {"url_default": "https://x.com/1.jpg"},
                {"url_default": "https://x.com/2.jpg"},
            ],
        )
        n = parse_note(resp, "img_id")
        self.assertEqual(n.type, "normal")
        self.assertEqual(n.image_urls, ["https://x.com/1.jpg", "https://x.com/2.jpg"])
        self.assertIsNone(n.video_url)


# ─── helpers ──────────────────────────────────────

class TestHelpers(unittest.TestCase):

    def test_safe_int(self):
        self.assertEqual(_safe_int(None), 0)
        self.assertEqual(_safe_int("123"), 123)
        self.assertEqual(_safe_int(123), 123)
        self.assertEqual(_safe_int(123.7), 123)
        self.assertEqual(_safe_int("abc"), 0)
        self.assertEqual(_safe_int([]), 0)

    def test_clean_tag(self):
        self.assertEqual(clean_tag("深圳新中式[话题]"), "深圳新中式")
        self.assertEqual(clean_tag("[话题]深圳新中式[话题]"), "深圳新中式")
        self.assertEqual(clean_tag("纯文本"), "纯文本")
        self.assertEqual(clean_tag("   留白  "), "留白")

    def test_extract_hashtags_handles_dirty_data(self):
        note = {"hash_tag": [
            {"name": "正常"},
            {"name": "带标记[话题]"},
            {"name": ""},                   # 空名应过滤
            "字符串而非 dict",                # 非 dict 应过滤
            {"no_name_field": "x"},          # 缺 name 应过滤
        ]}
        self.assertEqual(_extract_hashtags(note), ["正常", "带标记"])

    def test_extract_image_urls_field_name_fallback(self):
        # 测试 4 种字段名都能识别
        for field in ("images_list", "image_list", "images", "imageList"):
            note = {field: [{"url_default": "x"}]}
            self.assertEqual(_extract_image_urls(note), ["x"], f"failed for {field}")

    def test_extract_video_url_fallback_chain(self):
        # 优先 video.url
        self.assertEqual(_extract_video_url({"video": {"url": "primary"}}), "primary")
        # 退化到 master_url
        note = {"video": {"media": {"stream": {"h264": [{"master_url": "stream_url"}]}}}}
        self.assertEqual(_extract_video_url(note), "stream_url")
        # 顶层 fallback
        self.assertEqual(_extract_video_url({"videoUrl": "alt"}), "alt")
        # 都没有
        self.assertIsNone(_extract_video_url({}))


# ─── parse_comments ────────────────────────────────

class TestParseComments(unittest.TestCase):

    def test_pinned_detection(self):
        resp = {"data": {"data": {"comments": [
            {"id": "1", "content": "正常评论", "user": {"nickname": "u1"}, "score": 0},
            {"id": "2", "content": "请认准本账号的回复", "user": {"nickname": "u2"}, "score": 0},
            {"id": "3", "content": "其他的回复都是骗子", "user": {"nickname": "u3"}, "score": 0},
            {"id": "4", "content": "高分服务端置顶", "user": {"nickname": "u4"}, "score": 5_000_000},
        ]}}}
        comments = parse_comments(resp)
        self.assertEqual(len(comments), 4)
        self.assertFalse(comments[0].is_pinned)
        self.assertTrue(comments[1].is_pinned)
        self.assertTrue(comments[2].is_pinned)
        self.assertTrue(comments[3].is_pinned)

    def test_empty_response(self):
        self.assertEqual(parse_comments({}), [])
        self.assertEqual(parse_comments({"data": {}}), [])
        self.assertEqual(parse_comments({"data": {"data": {"comments": []}}}), [])


if __name__ == "__main__":
    unittest.main()
