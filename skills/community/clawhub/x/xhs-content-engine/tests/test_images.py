"""images.py 单元测试 — 主要测纯函数。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine.images import _guess_extension


class TestGuessExtension(unittest.TestCase):

    def test_simple_extensions(self):
        self.assertEqual(_guess_extension("https://x.com/a.png"), "png")
        self.assertEqual(_guess_extension("https://x.com/a.jpg"), "jpg")
        self.assertEqual(_guess_extension("https://x.com/a.webp"), "webp")
        self.assertEqual(_guess_extension("https://x.com/a.gif"), "gif")

    def test_jpeg_normalized_to_jpg(self):
        self.assertEqual(_guess_extension("https://x.com/a.jpeg"), "jpg")

    def test_query_string_ignored(self):
        # 关键回归：旧版用 substring 匹配，会误判
        self.assertEqual(_guess_extension("https://x.com/a.png?token=jpg.xxx"), "png")

    def test_misleading_path_segment(self):
        # 旧版会误判为 jpg（先命中），新版应识别真正的扩展名
        self.assertEqual(_guess_extension("https://x.com/a.com_pic.webp"), "webp")

    def test_no_extension_defaults_jpg(self):
        self.assertEqual(_guess_extension("https://x.com/uuid-without-ext"), "jpg")

    def test_only_query_no_path_extension(self):
        self.assertEqual(_guess_extension("https://x.com/img?ext=png"), "jpg")
