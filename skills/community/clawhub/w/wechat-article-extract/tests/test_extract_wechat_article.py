import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "extract_wechat_article.py"


SAMPLE_HTML = """
<!doctype html>
<html>
<head>
  <meta property="og:title" content="测试文章标题">
  <meta name="author" content="测试公众号">
  <script>var ct = "1770998400";</script>
</head>
<body>
  <div id="js_content">
    <p>第一段正文。</p>
    <img data-src="https://mmbiz.qpic.cn/example.png" style="width:50%;" data-w="1000">
    <p>第二段正文。</p>
    <table><tr><td>项目</td><td>内容</td></tr><tr><td>A</td><td>B</td></tr></table>
  </div>
  <script>console.log("after content")</script>
</body>
</html>
"""


class ExtractWechatArticleTests(unittest.TestCase):
    def test_extracts_json_from_saved_html(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = Path(tmpdir) / "article.html"
            html_path.write_text(SAMPLE_HTML, encoding="utf-8")
            output = subprocess.check_output(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--html-file",
                    str(html_path),
                    "--source-url",
                    "https://mp.weixin.qq.com/s/test",
                    "--format",
                    "json",
                ],
                text=True,
            )

        record = json.loads(output)
        self.assertEqual(record["title"], "测试文章标题")
        self.assertEqual(record["author"], "测试公众号")
        self.assertEqual(record["publishTime"], "2026-02-14 00:00")
        self.assertEqual(record["imageCount"], 1)
        self.assertIn("[[WECHAT_IMAGE_1]]", record["contentWithImageMarkers"])
        self.assertIn("| 项目 | 内容 |", record["contentWithImageMarkers"])

    def test_renders_markdown_from_saved_html(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = Path(tmpdir) / "article.html"
            html_path.write_text(SAMPLE_HTML, encoding="utf-8")
            output = subprocess.check_output(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--html-file",
                    str(html_path),
                    "--source-url",
                    "https://mp.weixin.qq.com/s/test",
                ],
                text=True,
            )

        self.assertIn("# 测试文章标题", output)
        self.assertIn("- Account: 测试公众号", output)
        self.assertIn("[[WECHAT_IMAGE_1]]", output)
        self.assertIn("https://mmbiz.qpic.cn/example.png", output)


if __name__ == "__main__":
    unittest.main()
