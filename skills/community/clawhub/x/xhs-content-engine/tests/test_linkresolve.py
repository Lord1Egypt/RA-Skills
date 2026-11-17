"""linkresolve.py 单元测试。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from content_engine.linkresolve import resolve_xhs_link


class TestResolveXhsLink(unittest.TestCase):

    def test_bare_note_id(self):
        nid = "665ea88c0000000003031383"
        note_id, url = resolve_xhs_link(nid)
        self.assertEqual(note_id, nid)
        self.assertIn(nid, url)

    def test_long_explore_url(self):
        url = "https://www.xiaohongshu.com/explore/665ea88c0000000003031383?xsec_token=xxx"
        note_id, _ = resolve_xhs_link(url)
        self.assertEqual(note_id, "665ea88c0000000003031383")

    def test_long_discovery_url(self):
        url = "https://www.xiaohongshu.com/discovery/item/665ea88c0000000003031383"
        note_id, _ = resolve_xhs_link(url)
        self.assertEqual(note_id, "665ea88c0000000003031383")

    def test_share_text_with_embedded_url(self):
        text = "看看这条 https://www.xiaohongshu.com/explore/665ea88c0000000003031383?x=1 不错"
        note_id, _ = resolve_xhs_link(text)
        self.assertEqual(note_id, "665ea88c0000000003031383")

    def test_no_link_raises(self):
        with self.assertRaises(ValueError):
            resolve_xhs_link("纯文本没链接")
        with self.assertRaises(ValueError):
            resolve_xhs_link("")


if __name__ == "__main__":
    unittest.main()
