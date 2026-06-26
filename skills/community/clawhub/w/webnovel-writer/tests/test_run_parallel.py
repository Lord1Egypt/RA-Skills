"""测试 run_parallel.py"""
import json
import tempfile
from pathlib import Path


def test_file_hash(tmp_path):
    import scripts.run_parallel as rp
    f = tmp_path / "test.txt"
    f.write_text("hello")
    h1 = rp._file_hash(str(f))
    h2 = rp._file_hash(str(f))
    assert h1 == h2
    assert len(h1) == 64  # SHA256 hex


def test_file_hash_changes(tmp_path):
    import scripts.run_parallel as rp
    f = tmp_path / "test.txt"
    f.write_text("hello")
    h1 = rp._file_hash(str(f))
    f.write_text("world")
    h2 = rp._file_hash(str(f))
    assert h1 != h2


def test_ensure_db(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import scripts.run_parallel as rp
    db_path = tmp_path / ".cache" / "novel_writer_cache.db"
    # 覆盖默认路径
    rp.DB_PATH = db_path
    conn = rp._ensure_db()
    assert db_path.exists()
    # 表应该已创建
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    assert "cache" in table_names
    conn.close()


def test_cache_set_and_get(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import scripts.run_parallel as rp
    db_path = tmp_path / ".cache" / "test.db"
    rp.DB_PATH = db_path
    conn = rp._ensure_db()

    # 存缓存
    rp._set_cache(conn, "test_script", "/fake/path.md", "abc123", {"result": "ok"})
    # 取缓存
    cached = rp._get_cached(conn, "test_script", "/fake/path.md", "abc123")
    assert cached == {"result": "ok"}
    # 不同 hash 不命中
    miss = rp._get_cached(conn, "test_script", "/fake/path.md", "wrong_hash")
    assert miss is None
    conn.close()


def test_get_changed_files(tmp_path):
    import scripts.run_parallel as rp
    d = tmp_path / "novel"
    d.mkdir()
    (d / "第001章.md").write_text("内容")
    (d / "第002章.md").write_text("内容")
    (d / "other.txt").write_text("忽略")

    files = rp.get_changed_files(str(d))
    assert len(files) == 2


def test_clear_cache(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import scripts.run_parallel as rp
    db_path = tmp_path / ".cache" / "test.db"
    rp.DB_PATH = db_path
    rp._ensure_db()
    assert db_path.exists()
    rp.clear_cache()
    assert not db_path.exists()


def test_cache_stats_empty(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import scripts.run_parallel as rp
    rp.DB_PATH = tmp_path / "noexist.db"
    # 不崩溃就行
    rp.cache_stats()
