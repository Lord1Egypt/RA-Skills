#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from youtube_video_to_blog_converter import ValidationError, run, validate_payload


TRANSCRIPT = (
    "今天我们讨论如何在AI时代提升产品研发效率。"
    "第一步是明确目标，避免无效迭代。"
    "第二步是建立可复用模板和自动化流程。"
    "第三步是通过数据回路持续优化。"
    "最后，团队协作和反馈机制决定长期上限。"
)

BASE_PAYLOAD = {
    "user_id": "u004",
    "video_title": "AI研发效率实战",
    "transcript": TRANSCRIPT,
    "video_url": "https://youtube.com/watch?v=test",
}


class YoutubeVideoToBlogConverterTest(unittest.TestCase):
    def test_validate_payload_success(self):
        result = validate_payload(BASE_PAYLOAD)
        self.assertEqual(result["video_title"], "AI研发效率实战")

    def test_validate_payload_invalid_url(self):
        payload = dict(BASE_PAYLOAD)
        payload["video_url"] = "ftp://invalid"
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_run_free_success(self):
        result = run(BASE_PAYLOAD)
        self.assertTrue(result["success"])
        self.assertIn("## 核心观点", result["blog_draft"]["markdown"])

    def test_run_premium_upgrade_required(self):
        payload = dict(BASE_PAYLOAD)
        payload["tier"] = "premium"
        result = run(payload)
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "PREMIUM_UPGRADE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
