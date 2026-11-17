import os

import douyin_transcript as dt


def test_safe_name_strips_illegal_chars():
    # 非法文件名字符应被替换为下划线并收尾
    out = dt.safe_name('标题/带:非法*字符?<>|#')
    for ch in '/\\:*?"<>|#':
        assert ch not in out


def test_safe_name_truncates_to_limit():
    out = dt.safe_name("啊" * 100, limit=40)
    assert len(out) <= 40


def test_safe_name_empty_falls_back():
    assert dt.safe_name("###") == "douyin_video"
    assert dt.safe_name("") == "douyin_video"


def test_load_env_env_var_overrides(monkeypatch):
    # 环境变量应被 load_env 收集（优先于 .env）
    monkeypatch.setenv("OSS_BUCKET", "test-bucket-xyz")
    cfg = dt.load_env()
    assert cfg.get("OSS_BUCKET") == "test-bucket-xyz"


def test_load_env_only_known_keys_from_environ(monkeypatch):
    # 非本脚本关心的键不应被从环境收集进来
    monkeypatch.setenv("SOME_UNRELATED_KEY", "leak")
    cfg = dt.load_env()
    assert "SOME_UNRELATED_KEY" not in cfg
