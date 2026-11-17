"""lookup.py 单元测试。"""

import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine.lookup import (
    find_card_by_note_id,
    make_v2_card_dir,
    make_v2_generated_dir,
    _extract_note_ids_from_card,
    _write_stub_card,
)


# ─── helpers ───

def _write_card(parent: Path, name: str, note_id: str, is_v2: bool = False) -> Path:
    """造一个含 note_id 的拆解卡（v1 单文件 or v2 目录结构）。"""
    body = f"""# {name}

> note_id: `{note_id}`
> 参考链接: https://www.xiaohongshu.com/explore/{note_id}

正文略...
"""
    if is_v2:
        d = parent / name
        d.mkdir(parents=True)
        f = d / "deconstruction.md"
    else:
        f = parent / f"{name}.md"
    f.write_text(body)
    return f


# ─── tests ───

class TestExtractNoteIds(unittest.TestCase):

    def test_backtick_note_id(self):
        text = "> note_id: `665ea88c0000000003031383`\nbody"
        ids = _extract_note_ids_from_card(text)
        self.assertIn("665ea88c0000000003031383", ids)

    def test_explore_url(self):
        text = "https://www.xiaohongshu.com/explore/665ea88c0000000003031383?xsec=xxx"
        ids = _extract_note_ids_from_card(text)
        self.assertIn("665ea88c0000000003031383", ids)

    def test_discovery_url(self):
        text = "https://www.xiaohongshu.com/discovery/item/665ea88c0000000003031383"
        ids = _extract_note_ids_from_card(text)
        self.assertIn("665ea88c0000000003031383", ids)

    def test_no_note_id(self):
        text = "no hex here, just words"
        ids = _extract_note_ids_from_card(text)
        self.assertEqual(ids, set())


class TestFindCard(unittest.TestCase):

    def test_finds_v1_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            note_id = "665ea88c0000000003031383"
            card = _write_card(d, "AIC-001-test", note_id, is_v2=False)
            result = find_card_by_note_id(note_id, d)
            self.assertTrue(result.found)
            self.assertEqual(result.card_path, card)
            self.assertFalse(result.is_v2_structure)
            self.assertTrue(result.is_fresh)  # 新建的肯定 fresh

    def test_finds_v2_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            note_id = "665ea88c0000000003031383"
            card = _write_card(d, "AIC-001-test", note_id, is_v2=True)
            result = find_card_by_note_id(note_id, d)
            self.assertTrue(result.found)
            self.assertEqual(result.card_path, card)
            self.assertTrue(result.is_v2_structure)

    def test_not_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = find_card_by_note_id("doesnotexist000000000000", Path(tmp))
            self.assertFalse(result.found)
            self.assertIsNone(result.card_path)

    def test_freshness_old_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            note_id = "665ea88c0000000003031383"
            card = _write_card(d, "AIC-old", note_id)
            # 把 mtime 改到 30 天前
            old_time = time.time() - 30 * 86400
            import os
            os.utime(card, (old_time, old_time))
            result = find_card_by_note_id(note_id, d, freshness_days=7)
            self.assertTrue(result.found)
            self.assertFalse(result.is_fresh)
            self.assertGreaterEqual(result.age_days, 29)

    def test_skips_v1_v2_v3_backups(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            note_id = "665ea88c0000000003031383"
            # 主文件
            primary = _write_card(d, "AIC-001-test", note_id)
            # 备份不应被找到
            (d / "AIC-001-test.v1.md").write_text(f"backup with `{note_id}`")
            (d / "AIC-001-test.v2.md").write_text(f"backup with `{note_id}`")
            result = find_card_by_note_id(note_id, d)
            self.assertEqual(result.card_path, primary)

    def test_str_path_accepted(self):
        """验证：deconstructions_dir 传 str 也工作（不是 Path）"""
        with tempfile.TemporaryDirectory() as tmp:
            note_id = "665ea88c0000000003031383"
            _write_card(Path(tmp), "AIC-001-test", note_id)
            # 故意传 str
            result = find_card_by_note_id(note_id, tmp)
            self.assertTrue(result.found)


class TestMakeDirs(unittest.TestCase):

    def test_make_v2_card_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            decon_path = make_v2_card_dir(d, "AIC-001", "测试-标题")
            self.assertTrue(decon_path.parent.is_dir())
            self.assertEqual(decon_path.name, "deconstruction.md")
            self.assertIn("AIC-001", decon_path.parent.name)

    def test_make_v2_generated_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            card_dir = Path(tmp) / "AIC-001-test"
            card_dir.mkdir()
            gen_dir = make_v2_generated_dir(card_dir, "GEN-001", "video")
            self.assertTrue(gen_dir.is_dir())
            self.assertIn("GEN-001", gen_dir.name)
            self.assertIn("video", gen_dir.name)
            self.assertEqual(gen_dir.parent.name, "generated")

    def test_slug_safe_chars(self):
        with tempfile.TemporaryDirectory() as tmp:
            # title 含 emoji 和特殊符号
            decon = make_v2_card_dir(Path(tmp), "AIC-001", "✨深圳新中式｜把江南春色")
            # 应清理掉特殊符号
            self.assertNotIn("✨", decon.parent.name)
            self.assertNotIn("｜", decon.parent.name)

    def test_slug_truncated(self):
        with tempfile.TemporaryDirectory() as tmp:
            long_title = "a" * 100
            decon = make_v2_card_dir(Path(tmp), "AIC-001", long_title)
            # slug 截到 30 字
            self.assertLessEqual(len(decon.parent.name) - len("AIC-001-"), 30)


class TestWriteStubCard(unittest.TestCase):
    """auto-fallback 写 stub 卡（不调用 extract_xhs.py，仅测合成逻辑）。"""

    def _sample_note(self) -> dict:
        return {
            "note_id": "665ea88c0000000003031383",
            "author_nickname": "见花开",
            "title": "把江南春色穿在身上",
            "desc": "今年春天，做了一组真丝马甲。\n#新中式 #真丝马甲",
            "type": "video",
            "video_duration": 34,
            "liked_count": 330,
            "collected_count": 231,
            "comments_count": 133,
            "shared_count": 25,
            "ip_location": "广东",
            "time": 1714117200000,
            "hashtags": ["新中式", "真丝马甲"],
        }

    def test_creates_card_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            card_path = Path(tmp) / "AIC-AUTO-001" / "deconstruction.md"
            _write_stub_card(self._sample_note(), [], card_path, "AIC-AUTO-001")
            self.assertTrue(card_path.exists())

    def test_card_contains_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            card_path = Path(tmp) / "AIC-AUTO-001" / "deconstruction.md"
            _write_stub_card(self._sample_note(), [], card_path, "AIC-AUTO-001")
            text = card_path.read_text(encoding="utf-8")
            self.assertIn("见花开", text)
            self.assertIn("把江南春色穿在身上", text)
            self.assertIn("665ea88c0000000003031383", text)
            self.assertIn("330", text)  # likes
            self.assertIn("AUTO-STUB", text)  # 标记 stub 状态

    def test_card_includes_note_id_for_lookup(self):
        """关键：stub 卡必须包含 note_id 才能被 find_card_by_note_id 找到。"""
        with tempfile.TemporaryDirectory() as tmp:
            note = self._sample_note()
            card_path = Path(tmp) / "AIC-AUTO-001" / "deconstruction.md"
            _write_stub_card(note, [], card_path, "AIC-AUTO-001")
            # 现在用 find_card_by_note_id 应该能找到
            result = find_card_by_note_id(note["note_id"], Path(tmp))
            self.assertTrue(result.found)
            self.assertEqual(result.card_path, card_path)

    def test_card_includes_user_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            comments = [
                {"content": "好喜欢这个颜色", "is_pinned": False},
                {"content": "求链接", "is_pinned": False},
                {"content": "（置顶 自家广告）", "is_pinned": True},
            ]
            card_path = Path(tmp) / "AIC-AUTO-001" / "deconstruction.md"
            _write_stub_card(self._sample_note(), comments, card_path, "AIC-AUTO-001")
            text = card_path.read_text(encoding="utf-8")
            self.assertIn("好喜欢这个颜色", text)
            self.assertIn("求链接", text)
            # 置顶评论应过滤
            self.assertNotIn("自家广告", text)

    def test_card_handles_image_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            note = self._sample_note()
            note["type"] = "normal"  # XHS image type
            note["video_duration"] = 0
            card_path = Path(tmp) / "AIC-AUTO-001" / "deconstruction.md"
            _write_stub_card(note, [], card_path, "AIC-AUTO-001")
            text = card_path.read_text(encoding="utf-8")
            self.assertIn("图片", text)


if __name__ == "__main__":
    unittest.main()
