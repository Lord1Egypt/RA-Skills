"""测试 config_manager.py"""
from unittest.mock import patch
from pathlib import Path


def test_register_and_list(tmp_path):
    from scripts import config_manager as cm
    fake_config = tmp_path / "config.json"
    with patch.object(cm, "CONFIG_PATH", fake_config):
        novel_dir = tmp_path / "mynovel"
        novel_dir.mkdir()
        cm.register_novel("测试小说", str(novel_dir))
        cfg = cm.load_config()
        assert "测试小说" in cfg["novels"]
        assert cfg["active_novel"] == "测试小说"


def test_set_active(tmp_path):
    from scripts import config_manager as cm
    fake_config = tmp_path / "config.json"
    with patch.object(cm, "CONFIG_PATH", fake_config):
        d1 = tmp_path / "n1"
        d2 = tmp_path / "n2"
        d1.mkdir(); d2.mkdir()
        cm.register_novel("小说A", str(d1))
        cm.register_novel("小说B", str(d2))
        cm.set_active("小说A")
        name, path = cm.get_active()
        assert name == "小说A"


def test_load_default(tmp_path):
    from scripts import config_manager as cm
    fake_config = tmp_path / "config.json"
    with patch.object(cm, "CONFIG_PATH", fake_config):
        cfg = cm.load_config()
        assert "version" in cfg
        assert "defaults" in cfg
        assert "max_chapter_words" in cfg["defaults"]


def test_list_novels_empty(tmp_path):
    from scripts import config_manager as cm
    fake_config = tmp_path / "config.json"
    with patch.object(cm, "CONFIG_PATH", fake_config):
        # 不应崩溃
        cm.list_novels()
