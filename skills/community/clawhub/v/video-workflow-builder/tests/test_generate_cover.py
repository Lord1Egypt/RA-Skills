import importlib.util
import os

_SPEC = importlib.util.spec_from_file_location(
    "generate_cover",
    os.path.join(os.path.dirname(__file__), "..", "scripts", "generate_cover.py"),
)
gc = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(gc)


def test_platform_sizes_cover_all_five_platforms():
    for p in ["douyin", "bilibili", "xiaohongshu", "shipinhao", "baijiahao"]:
        assert p in gc.PLATFORM_SIZES
        assert "x" in gc.PLATFORM_SIZES[p]


def test_resolve_size_uses_platform_default():
    assert gc.resolve_size("bilibili", None) == gc.PLATFORM_SIZES["bilibili"]


def test_resolve_size_override_wins():
    assert gc.resolve_size("douyin", "512x512") == "512x512"


def test_load_api_key_prefers_env(monkeypatch):
    monkeypatch.setenv("LLM_GATEWAY_API_KEY", "env-key-123")
    assert gc._load_api_key() == "env-key-123"
