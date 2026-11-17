#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a7w-bridge 纯逻辑自测：全部离线，不发网络请求。

运行：python -X utf8 scripts/selftest.py -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7w_bridge as B  # noqa: E402


class TestEnvelope(unittest.TestCase):
    def test_unwrap_dict_data(self):
        self.assertEqual(B.unwrap({"code": 1, "data": {"a": 1}}), {"a": 1})

    def test_unwrap_list_data(self):
        """实测 /api/v1/apps 的 data 是 list，不是 dict。"""
        self.assertEqual(B.unwrap({"code": 1, "data": [1, 2]}), [1, 2])

    def test_unwrap_passthrough(self):
        self.assertEqual(B.unwrap({"a": 1}), {"a": 1})

    def test_unwrap_result_nested(self):
        """实测 voice_tts 真实结构是 data.result.*，与 api_doc 不一致。"""
        p = {"code": 1, "data": {"result": {"audio_url": "u", "format": "mp3"},
                                 "usage": {"actual_points": 1}}}
        self.assertEqual(B.unwrap_result(p)["audio_url"], "u")

    def test_unwrap_result_flat_fallback(self):
        p = {"code": 1, "data": {"audio_url": "u"}}
        self.assertEqual(B.unwrap_result(p)["audio_url"], "u")

    def test_app_list_from_list(self):
        self.assertEqual(B.app_list({"data": [{"code": "x"}]}), [{"code": "x"}])

    def test_app_list_from_dict(self):
        self.assertEqual(B.app_list({"data": {"apps": [{"code": "x"}]}}), [{"code": "x"}])

    def test_ok_of(self):
        self.assertTrue(B.ok_of({"code": 1}))
        self.assertTrue(B.ok_of({"code": "200"}))
        self.assertFalse(B.ok_of({"code": 0}))


class TestFindUrls(unittest.TestCase):
    def test_nested_result(self):
        r = {"result": {"images": [{"url": "https://a/1.png"}]}}
        self.assertEqual(B.find_urls(r), ["https://a/1.png"])

    def test_audio_url(self):
        self.assertEqual(B.find_urls({"result": {"audio_url": "https://a/x.mp3"}}),
                         ["https://a/x.mp3"])

    def test_ignores_non_url_values(self):
        self.assertEqual(B.find_urls({"note": "https://not-a-product"}), [])


class TestSpeechMapping(unittest.TestCase):
    def test_text_and_format(self):
        p = B.map_speech({"input": "你好", "response_format": "mp3"})
        self.assertEqual(p["text"], "你好")
        self.assertEqual(p["format"], "mp3")

    def test_builtin_voice_not_mapped(self):
        p = B.map_speech({"input": "x", "voice": "alloy"})
        self.assertNotIn("reference_id", p)

    def test_custom_voice_mapped(self):
        p = B.map_speech({"input": "x", "voice": "my-cloned-voice"})
        self.assertEqual(p["reference_id"], "my-cloned-voice")

    def test_speed_mapped_to_prosody(self):
        p = B.map_speech({"input": "x", "speed": 1.25})
        self.assertEqual(p["prosody"]["speed"], 1.25)


class TestImageMapping(unittest.TestCase):
    def test_generate_defaults(self):
        p = B.map_image({"prompt": "cat"}, "generate")
        self.assertEqual(p["action"], "generate")
        self.assertEqual(p["prompt"], "cat")

    def test_size_maps_to_resolution(self):
        self.assertEqual(B.map_image({"prompt": "x", "size": "1024x1024"}, "generate")["resolution"], "1K")
        self.assertEqual(B.map_image({"prompt": "x", "size": "1792x1024"}, "generate")["resolution"], "2K")

    def test_edit_requires_image_urls(self):
        p = B.map_image({"prompt": "x", "image_urls": ["https://a/i.png"]}, "edit")
        self.assertEqual(p["action"], "edit")
        self.assertEqual(p["image_urls"], ["https://a/i.png"])


class TestSubtitle(unittest.TestCase):
    """网关 ignore_timestamps=false 返回**词级**片段，需要合并成字幕行。"""

    WORDS = [{"start": 0.0, "end": 0.2, "text": "今"},
             {"start": 0.2, "end": 0.4, "text": "天"},
             {"start": 0.4, "end": 0.6, "text": "好"},
             {"start": 0.6, "end": 0.8, "text": "。"},
             {"start": 0.8, "end": 1.0, "text": "再"},
             {"start": 1.0, "end": 1.2, "text": "见"}]

    def test_group_breaks_on_punctuation(self):
        cues = B.group_segments(self.WORDS)
        self.assertEqual(len(cues), 2)
        self.assertEqual(cues[0]["text"], "今天好。")
        self.assertEqual(cues[1]["text"], "再见")

    def test_group_breaks_on_max_chars(self):
        words = [{"start": i * 0.1, "end": i * 0.1 + 0.1, "text": "字"} for i in range(30)]
        cues = B.group_segments(words, max_chars=10)
        self.assertTrue(all(len(c["text"]) <= 10 for c in cues))
        self.assertGreater(len(cues), 1)

    def test_empty_segments(self):
        self.assertEqual(B.group_segments([]), [])

    def test_srt_format(self):
        srt = B.to_srt(B.group_segments(self.WORDS))
        self.assertIn("00:00:00,000 --> 00:00:00,800", srt)
        self.assertTrue(srt.startswith("1\n"))
        self.assertIn("今天好。", srt)

    def test_vtt_format(self):
        vtt = B.to_vtt(B.group_segments(self.WORDS))
        self.assertTrue(vtt.startswith("WEBVTT"))
        self.assertIn("00:00:00.000 --> 00:00:00.800", vtt)

    def test_timestamp_helper_precedence(self):
        """回归：曾写成 "%H:%M:%S" % (a,b,c).replace(...) → 对元组调 replace 崩掉。"""
        self.assertEqual(B._ts(3661.5), "01:01:01,500")
        self.assertEqual(B._ts(0), "00:00:00,000")
        self.assertEqual(B._ts(1.25, "."), "00:00:01.250")


class TestMultipart(unittest.TestCase):
    def test_roundtrip_and_field_rename(self):
        body, ct = B.build_multipart([("audio", "a.mp3", "audio/mpeg", b"BINARY")])
        parts = B.parse_multipart(body, ct)
        self.assertEqual(len(parts), 1)
        self.assertEqual(parts[0][0], "audio")
        self.assertEqual(parts[0][1], "a.mp3")
        self.assertEqual(parts[0][3], b"BINARY")

    def test_text_field_without_filename(self):
        body, ct = B.build_multipart([("language", None, "text/plain", b"zh")])
        parts = B.parse_multipart(body, ct)
        self.assertEqual(parts[0][0], "language")
        self.assertIsNone(parts[0][1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
