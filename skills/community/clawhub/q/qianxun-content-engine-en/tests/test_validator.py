"""validator.py 单元测试。

覆盖：
- 各文件单项 validator 的硬错 / 软错判定
- validate_workspace 整体流程（image / video / script 类型）
- 禁忌词从 graph 提取
- ValidationReport 渲染
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine.validator import (
    DEFAULT_BANNED_WORDS,
    Issue,
    ValidationReport,
    extract_taboo_words_from_graph,
    validate_cover_text,
    validate_desc,
    validate_image,
    validate_script,
    validate_tags,
    validate_text_file,
    validate_workspace,
)


# ─── helpers ───

def _make_workspace(
    tmp: Path,
    *,
    script: str = "# 图组规划\n\n## 整组叙事\n本组共 6 张图，三层结构：建立场景 → 展开细节 → 收尾呼应。" * 5,
    cover_txt: str = "把一朵花绣进春天里",
    desc: str = "今年春天，把江南穿在身上。\n\n真丝马甲叠搭立体绣衬衫，一针一线都是春天的样子。\n#新中式 #真丝马甲 #立体绣 #春日穿搭 #国风女装",
    tags: str = "#新中式 #真丝 #立体绣 #春日穿搭 #国风女装 #汉服 #中式美学",
    cover_png_size: int = 200_000,
    frame_count: int = 1,
    frame_size: int = 200_000,
    caption: str = "把一朵花绣进春天里",
    seedance: str = "shot type: medium close-up\nsubject: silk vest detail\nsetting: soft natural light\ncamera movement: slow push-in\nmood: serene\nduration: 4s\n" * 3,
) -> Path:
    gen_dir = tmp / "GEN-001-image"
    gen_dir.mkdir()
    (gen_dir / "script.md").write_text(script, encoding="utf-8")
    (gen_dir / "cover.txt").write_text(cover_txt, encoding="utf-8")
    (gen_dir / "desc.txt").write_text(desc, encoding="utf-8")
    (gen_dir / "tags.txt").write_text(tags, encoding="utf-8")
    (gen_dir / "caption.txt").write_text(caption, encoding="utf-8")
    (gen_dir / "seedance-prompt.md").write_text(seedance, encoding="utf-8")
    (gen_dir / "cover.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * cover_png_size)
    frames = gen_dir / "frames"
    frames.mkdir()
    for i in range(1, frame_count + 1):
        (frames / f"frame_{i:03d}.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * frame_size)
    return gen_dir


# ─── validate_text_file ───

class TestValidateTextFile(unittest.TestCase):

    def test_missing_file_is_hard(self):
        issues = validate_text_file(Path("/nonexistent/path.txt"), "x.txt")
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].severity, "hard")
        self.assertIn("不存在", issues[0].message)

    def test_empty_file_is_hard(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "x.txt"
            f.write_text("   \n   ", encoding="utf-8")
            issues = validate_text_file(f, "x.txt")
            self.assertTrue(any(i.severity == "hard" and "空" in i.message for i in issues))

    def test_taboo_word_is_hard(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "x.txt"
            f.write_text("这是最棒的产品", encoding="utf-8")
            issues = validate_text_file(f, "x.txt")
            self.assertTrue(any(i.severity == "hard" and "禁忌" in i.message for i in issues))

    def test_clean_text_no_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "x.txt"
            f.write_text("普通文案，没有任何敏感词", encoding="utf-8")
            issues = validate_text_file(f, "x.txt")
            self.assertEqual(issues, [])

    def test_extra_banned_words_applied(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "x.txt"
            f.write_text("含品牌专属禁词：山寨", encoding="utf-8")
            issues = validate_text_file(
                f, "x.txt", banned_words=DEFAULT_BANNED_WORDS + ("山寨",),
            )
            self.assertTrue(any("山寨" in i.message for i in issues))


# ─── validate_desc ───

class TestValidateDesc(unittest.TestCase):

    def test_short_desc_is_soft(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "desc.txt"
            f.write_text("太短了", encoding="utf-8")
            issues = validate_desc(f)
            self.assertTrue(any(i.severity == "soft" and "短" in i.message for i in issues))

    def test_long_desc_is_soft(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "desc.txt"
            f.write_text("a" * 2000, encoding="utf-8")
            issues = validate_desc(f)
            self.assertTrue(any(i.severity == "soft" and "长" in i.message for i in issues))

    def test_emoji_excess_is_soft(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "desc.txt"
            text = "正常长度的文案" * 10 + "🌸🌿🌷🌹🍃🌱"  # 6 emoji
            f.write_text(text, encoding="utf-8")
            issues = validate_desc(f)
            self.assertTrue(any("emoji" in i.message for i in issues))


# ─── validate_tags ───

class TestValidateTags(unittest.TestCase):

    def test_too_few_tags_is_hard(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "tags.txt"
            f.write_text("#a #b #c", encoding="utf-8")
            issues = validate_tags(f)
            self.assertTrue(any(i.severity == "hard" and "太少" in i.message for i in issues))

    def test_too_many_tags_is_soft(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "tags.txt"
            tags_str = " ".join(f"#tag{i}" for i in range(25))
            f.write_text(tags_str, encoding="utf-8")
            issues = validate_tags(f)
            self.assertTrue(any(i.severity == "soft" and "偏多" in i.message for i in issues))

    def test_normal_tags_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "tags.txt"
            f.write_text("#新中式 #真丝 #立体绣 #春日穿搭 #国风女装 #汉服", encoding="utf-8")
            issues = validate_tags(f)
            hard = [i for i in issues if i.severity == "hard"]
            self.assertEqual(hard, [])

    def test_missing_tags_file_is_hard(self):
        issues = validate_tags(Path("/nonexistent/tags.txt"))
        self.assertTrue(any(i.severity == "hard" for i in issues))


# ─── validate_cover_text ───

class TestValidateCoverText(unittest.TestCase):

    def test_single_short_line_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "cover.txt"
            f.write_text("把一朵花绣进春天", encoding="utf-8")
            issues = validate_cover_text(f)
            self.assertEqual(issues, [])

    def test_multi_line_is_soft(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "cover.txt"
            f.write_text("第一行\n第二行\n第三行", encoding="utf-8")
            issues = validate_cover_text(f)
            self.assertTrue(any(i.severity == "soft" and "行" in i.message for i in issues))

    def test_too_long_is_soft(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "cover.txt"
            f.write_text("a" * 50, encoding="utf-8")
            issues = validate_cover_text(f)
            self.assertTrue(any(i.severity == "soft" and "长" in i.message for i in issues))


# ─── validate_image ───

class TestValidateImage(unittest.TestCase):

    def test_missing_image_is_hard(self):
        issues = validate_image(Path("/nonexistent/cover.png"), "cover.png")
        self.assertTrue(any(i.severity == "hard" and "不存在" in i.message for i in issues))

    def test_tiny_image_is_hard(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "cover.png"
            f.write_bytes(b"x" * 1000)  # 1KB
            issues = validate_image(f, "cover.png")
            self.assertTrue(any(i.severity == "hard" and "过小" in i.message for i in issues))

    def test_normal_image_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "cover.png"
            f.write_bytes(b"x" * 200_000)  # 200KB
            issues = validate_image(f, "cover.png")
            self.assertEqual(issues, [])


# ─── validate_workspace（整体）───

class TestValidateWorkspace(unittest.TestCase):

    def test_clean_image_workspace_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            gen_dir = _make_workspace(Path(tmp))
            report = validate_workspace(gen_dir, "image")
            self.assertFalse(report.has_hard_errors, msg=str(report.hard))
            self.assertGreater(len(report.files_checked), 0)

    def test_video_requires_caption_and_seedance(self):
        with tempfile.TemporaryDirectory() as tmp:
            gen_dir = _make_workspace(Path(tmp))
            # 删除 video 必有的两个
            (gen_dir / "caption.txt").unlink()
            (gen_dir / "seedance-prompt.md").unlink()
            report = validate_workspace(gen_dir, "video")
            files = [i.file for i in report.hard]
            self.assertIn("caption.txt", files)
            self.assertIn("seedance-prompt.md", files)

    def test_taboo_in_desc_triggers_hard(self):
        with tempfile.TemporaryDirectory() as tmp:
            gen_dir = _make_workspace(
                Path(tmp),
                desc="这是最好的产品" + "正常文案" * 30 + " #新中式 #真丝 #立体绣 #春日穿搭 #国风女装",
            )
            report = validate_workspace(gen_dir, "image")
            desc_hard = [i for i in report.hard if i.file == "desc.txt"]
            self.assertTrue(any("禁忌" in i.message for i in desc_hard))

    def test_too_few_tags_triggers_hard(self):
        with tempfile.TemporaryDirectory() as tmp:
            gen_dir = _make_workspace(Path(tmp), tags="#只有一个")
            report = validate_workspace(gen_dir, "image")
            self.assertTrue(any(i.file == "tags.txt" for i in report.hard))

    def test_missing_frames_dir_is_hard_for_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            gen_dir = _make_workspace(Path(tmp))
            # 删除 frames 目录
            for f in (gen_dir / "frames").iterdir():
                f.unlink()
            (gen_dir / "frames").rmdir()
            report = validate_workspace(gen_dir, "image")
            self.assertTrue(any(i.file == "frames/" for i in report.hard))

    def test_extra_banned_words_applied_to_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            gen_dir = _make_workspace(
                Path(tmp),
                desc="含品牌专属禁词：山寨" + "正常文案" * 30 + " #新中式 #真丝 #立体绣 #春日穿搭 #国风女装",
            )
            report = validate_workspace(gen_dir, "image", extra_banned_words=("山寨",))
            self.assertTrue(any("山寨" in i.message for i in report.hard))


# ─── ValidationReport 渲染 ───

class TestValidationReport(unittest.TestCase):

    def test_summary_line_clean(self):
        r = ValidationReport(files_checked=["a.txt", "b.txt"])
        self.assertIn("passed", r.summary_line())

    def test_summary_line_with_errors(self):
        r = ValidationReport(
            hard=[Issue("hard", "x", "msg")],
            soft=[Issue("soft", "y", "msg2")],
            files_checked=["x", "y"],
        )
        line = r.summary_line()
        self.assertIn("1 hard", line)
        self.assertIn("1 soft", line)

    def test_to_markdown_clean(self):
        r = ValidationReport(files_checked=["a"])
        md = r.to_markdown()
        self.assertIn("通过质检", md)

    def test_to_markdown_with_issues(self):
        r = ValidationReport(
            hard=[Issue("hard", "desc.txt", "含禁忌词", "重跑")],
            soft=[Issue("soft", "cover.txt", "偏长", "精简")],
            files_checked=["desc.txt", "cover.txt"],
        )
        md = r.to_markdown()
        self.assertIn("Hard errors", md)
        self.assertIn("Soft warnings", md)
        self.assertIn("含禁忌词", md)
        self.assertIn("偏长", md)


# ─── extract_taboo_words_from_graph ───

class TestExtractTabooWords(unittest.TestCase):

    def test_extracts_bullet_words(self):
        text = """# 禁忌词

- 山寨
- 假货
- 抄袭
"""
        words = extract_taboo_words_from_graph(text)
        self.assertIn("山寨", words)
        self.assertIn("假货", words)
        self.assertIn("抄袭", words)

    def test_handles_empty(self):
        self.assertEqual(extract_taboo_words_from_graph(""), [])

    def test_skips_long_phrases(self):
        # 超过 8 字的不视为禁忌词
        text = "- 这是一个非常非常长的句子根本不是禁忌词"
        words = extract_taboo_words_from_graph(text)
        self.assertEqual(words, [])


if __name__ == "__main__":
    unittest.main()
