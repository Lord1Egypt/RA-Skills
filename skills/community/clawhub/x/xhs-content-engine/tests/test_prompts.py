"""prompts.py 单元测试 — 模板渲染。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine.prompts import (
    system_for_brand,
    prompt_script,
    prompt_caption,
    prompt_cover_text,
    prompt_desc,
    prompt_tags,
    prompt_seedance_video,
)


class TestSystemPrompt(unittest.TestCase):

    def test_full_context(self):
        msg = system_for_brand(
            brand_voice="温和克制",
            brand_story="17 年女装",
            audience="35+ 高审美女性",
            taboo="不用最/绝对",
        )
        for piece in ["温和克制", "17 年女装", "35+ 高审美女性", "不用最/绝对"]:
            self.assertIn(piece, msg)

    def test_partial_context_skips_empty_sections(self):
        msg = system_for_brand(brand_voice="只有这个")
        self.assertIn("只有这个", msg)
        self.assertNotIn("Brand Story", msg)
        self.assertNotIn("目标客群", msg)

    def test_empty_context_still_renders_base(self):
        msg = system_for_brand()
        self.assertIn("brand-voice", msg.lower())
        self.assertIn("禁忌词", msg)


class TestPromptScript(unittest.TestCase):

    def test_video_type(self):
        p = prompt_script("拆解卡内容", "羊绒大衣", "8 张多角度", "video", 1)
        self.assertIn("video", p)
        self.assertIn("分镜", p)
        self.assertIn("羊绒大衣", p)

    def test_image_type(self):
        p = prompt_script("拆解卡", "首饰", "", "image", 8)
        self.assertIn("image", p)
        self.assertIn("8", p)
        self.assertIn("封面", p)  # 图组规划应提到封面

    def test_script_type(self):
        p = prompt_script("拆解卡", "服装", "", "script", 1)
        self.assertIn("script", p)
        self.assertIn("拍摄指引", p)

    def test_no_product_usp_falls_back(self):
        p = prompt_script("拆解卡", "", "", "video", 1)
        self.assertIn("agent", p.lower())  # 应有 fallback 提示


class TestSimplePrompts(unittest.TestCase):

    def test_caption_includes_script(self):
        script = "镜头 1: 全景\n镜头 2: 特写"
        p = prompt_caption(script)
        self.assertIn(script, p)
        self.assertIn("字幕", p)

    def test_cover_text_includes_script(self):
        p = prompt_cover_text("scriptmd", "deconmd", "")
        self.assertIn("封面", p)
        self.assertIn("emoji", p)

    def test_desc_includes_truncation(self):
        long_decon = "X" * 5000
        p = prompt_desc("scriptmd", long_decon)
        # desc 应只用 deconstruction 的前 2000 字
        self.assertIn("X" * 100, p)
        # 不应全文 5000 字都进 prompt
        self.assertLess(p.count("X"), 3000)

    def test_tags_includes_count_guidance(self):
        p = prompt_tags("desc", "decon")
        self.assertIn("10-15", p)
        self.assertIn("hashtag", p.lower())

    def test_seedance_format(self):
        p = prompt_seedance_video("script", "decon")
        self.assertIn("Shot type", p)
        self.assertIn("Camera movement", p)
        self.assertIn("Duration", p)


if __name__ == "__main__":
    unittest.main()
