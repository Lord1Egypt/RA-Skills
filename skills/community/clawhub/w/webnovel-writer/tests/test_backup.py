"""测试 backup.py"""
import tempfile
from pathlib import Path


def test_backup_novel_data(tmp_path):
    from scripts import backup as bk

    novel_dir = tmp_path / "novel"
    novel_dir.mkdir()
    (novel_dir / "character_states.json").write_text('{"test": 1}')
    (novel_dir / "追踪表.md").write_text("# 追踪")
    data_dir = novel_dir / "数据"
    data_dir.mkdir()
    (data_dir / "foreshadowing.json").write_text('{"threads": []}')

    output_dir = tmp_path / "backups"
    result = bk.backup_novel(str(novel_dir), str(output_dir))
    assert result is True
    # 检查备份文件存在（路径格式: novel_backup_时间戳）
    backup_dirs = list(output_dir.glob("novel_backup_*"))
    assert len(backup_dirs) == 1
    assert (backup_dirs[0] / "character_states.json").exists()


def test_backup_empty_novel(tmp_path):
    from scripts import backup as bk
    novel_dir = tmp_path / "empty"
    novel_dir.mkdir()
    result = bk.backup_novel(str(novel_dir))
    assert result is False


def test_backup_noexist():
    from scripts import backup as bk
    result = bk.backup_novel("/nonexistent/path/12345")
    assert result is False


def test_backup_excludes_text(tmp_path):
    from scripts import backup as bk

    novel_dir = tmp_path / "novel"
    novel_dir.mkdir()
    (novel_dir / "character_states.json").write_text('{}')
    正文 = novel_dir / "正文"
    正文.mkdir()
    (正文 / "第001章.md").write_text("小说正文" * 100)

    output_dir = tmp_path / "backups"
    bk.backup_novel(str(novel_dir), str(output_dir))
    backup_dirs = list(output_dir.glob("novel_backup_*"))
    assert len(backup_dirs) == 1
    # 正文不应该被备份
    assert not (backup_dirs[0] / "正文").exists()
    # JSON 应该被备份
    assert (backup_dirs[0] / "character_states.json").exists()


def test_backup_default_output(tmp_path):
    from scripts import backup as bk

    novel_dir = tmp_path / "novel"
    novel_dir.mkdir()
    (novel_dir / "character_states.json").write_text('{}')

    result = bk.backup_novel(str(novel_dir))
    assert result is True
    backups = novel_dir / "backups"
    assert backups.exists()
