"""测试 changelog.py"""
from unittest.mock import patch
from pathlib import Path


def test_show_no_error():
    from scripts import changelog as cl
    cl.show()


def test_add_entry(tmp_path):
    from scripts import changelog as cl
    fake_path = tmp_path / "CHANGELOG.md"
    with patch.object(cl, "CHANGELOG_PATH", fake_path):
        cl.add("3.0.0", "性能引擎")
    assert fake_path.exists()
    content = fake_path.read_text()
    assert "3.0.0" in content
    assert "性能引擎" in content


def test_entries_order():
    from scripts import changelog as cl
    original = cl.ENTRIES.copy()
    cl.ENTRIES.insert(0, ("9.9.9", "2099-01-01", "测试"))
    assert cl.ENTRIES[0][0] == "9.9.9"
    cl.ENTRIES = original
