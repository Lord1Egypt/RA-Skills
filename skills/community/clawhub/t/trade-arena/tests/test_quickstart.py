from __future__ import annotations

import importlib.util
import io
import json
import sys
import zipfile
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "quickstart.py"


def load_quickstart_module():
    spec = importlib.util.spec_from_file_location("trade_arena_quickstart_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def quickstart(tmp_path, monkeypatch):
    module = load_quickstart_module()
    skill_root = tmp_path / "skill"
    skill_root.mkdir()
    config_file = skill_root / "config.json"
    skill_md = skill_root / "SKILL.md"
    strategy_file = skill_root / "strategy.md"
    legacy_strategy_file = skill_root / "strategy.MD"

    monkeypatch.setattr(module, "SKILL_ROOT", skill_root)
    monkeypatch.setattr(module, "CONFIG_FILE", config_file)
    monkeypatch.setattr(module, "SKILL_MD_FILE", skill_md)
    monkeypatch.setattr(module, "STRATEGY_FILE", strategy_file)
    monkeypatch.setattr(module, "LEGACY_STRATEGY_FILE", legacy_strategy_file)

    config_file.write_text(json.dumps(module.default_config(), ensure_ascii=False), encoding="utf-8")
    skill_md.write_text(
        "---\nname: trade-arena\nversion: 1.4.0\ndescription: test\n---\n",
        encoding="utf-8",
    )
    return module


class FakeResponse:
    def __init__(self, status_code=200, payload=None, content=b"", text="", headers=None):
        self.status_code = status_code
        self._payload = payload or {}
        self.content = content
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._payload



def test_load_config_handles_legacy_schema(quickstart):
    quickstart.CONFIG_FILE.write_text(
        json.dumps({"$schema": "https://json-schema.org", "properties": {"api_url": {}}}),
        encoding="utf-8",
    )

    config = quickstart.load_config()

    assert config["api_url"] == "stock.cocoloop.cn"
    assert config["setup_state"]["last_update_error"] == ""



def test_apply_skill_update_preserves_config_and_strategy(quickstart, monkeypatch):
    config = quickstart.load_config()
    config["token"] = "secret-token"
    quickstart.save_config(config, announce=False)
    quickstart.STRATEGY_FILE.write_text("# Strategy\n\n原策略\n", encoding="utf-8")

    archive_buf = io.BytesIO()
    with zipfile.ZipFile(archive_buf, "w") as zf:
        zf.writestr("config.json", '{"token":"should-not-overwrite"}')
        zf.writestr("strategy.md", "# should not overwrite\n")
        zf.writestr("notes.txt", "updated")
    archive_bytes = archive_buf.getvalue()

    monkeypatch.setattr(quickstart.requests, "get", lambda *args, **kwargs: FakeResponse(content=archive_bytes))

    updated = quickstart.apply_skill_update("https://example.com/skill.zip", "1.4.0", silent=True)

    assert updated is True
    assert quickstart.load_config()["token"] == "secret-token"
    assert quickstart.STRATEGY_FILE.read_text(encoding="utf-8") == "# Strategy\n\n原策略\n"
    assert (quickstart.SKILL_ROOT / "notes.txt").read_text(encoding="utf-8") == "updated"



def test_check_and_update_skill_reports_remote_update_without_auto_apply(quickstart, monkeypatch):
    monkeypatch.setattr(
        quickstart,
        "fetch_clawhub_release_metadata",
        lambda: {"version": "1.4.1", "hosted_url": "https://example.com/skill.zip"},
    )

    result = quickstart.check_and_update_skill(force=True, auto_apply=False, silent=True)

    assert result["checked"] is True
    assert result["has_update"] is True
    assert result["updated"] is False
    assert result["remote_version"] == "1.4.1"


def test_fetch_clawhub_release_metadata_parses_page_version_and_download(quickstart, monkeypatch):
    page_html = """
    <html>
      <head><meta property="og:image" content="https://clawhub.ai/og/skill.png?owner=catrefuse&slug=trade-arena&version=1.4.2"></head>
      <body><a href="https://example.com/api/v1/download?slug=trade-arena">Download zip</a></body>
    </html>
    """

    monkeypatch.setattr(
        quickstart.requests,
        "get",
        lambda url, **kwargs: FakeResponse(status_code=200, text=page_html) if url == quickstart.CLAW_HUB_SKILL_PAGE_URL else FakeResponse(),
    )

    metadata = quickstart.fetch_clawhub_release_metadata()

    assert metadata["version"] == "1.4.2"
    assert metadata["hosted_url"] == "https://example.com/api/v1/download?slug=trade-arena"


def test_fetch_clawhub_release_metadata_uses_download_header_when_page_version_missing(quickstart, monkeypatch):
    page_html = '<html><body><a href="https://example.com/api/v1/download?slug=trade-arena">Download zip</a></body></html>'

    def fake_get(url, **kwargs):
        if url == quickstart.CLAW_HUB_SKILL_PAGE_URL:
            return FakeResponse(status_code=200, text=page_html)
        return FakeResponse()

    monkeypatch.setattr(quickstart.requests, "get", fake_get)
    monkeypatch.setattr(
        quickstart.requests,
        "head",
        lambda *args, **kwargs: FakeResponse(
            status_code=200,
            headers={"content-disposition": 'attachment; filename="trade-arena-1.4.3.zip"'},
        ),
    )

    metadata = quickstart.fetch_clawhub_release_metadata()

    assert metadata["version"] == "1.4.3"
    assert metadata["hosted_url"] == "https://example.com/api/v1/download?slug=trade-arena"



def test_read_strategy_document_supports_legacy_name(quickstart):
    quickstart.LEGACY_STRATEGY_FILE.write_text("# Legacy Strategy\n", encoding="utf-8")

    valid, path, content = quickstart.read_strategy_document()

    assert valid is True
    assert path is not None
    assert path.name.lower() == "strategy.md"
    assert "Legacy Strategy" in content



def test_refresh_account_info_updates_market_accounts(quickstart, monkeypatch):
    config = quickstart.load_config()
    config["token"] = "token"
    quickstart.save_config(config, announce=False)

    monkeypatch.setattr(
        quickstart,
        "get_my_info",
        lambda _token: {
            "agent_id": "alpha",
            "accounts": {
                "us": {"id": "alpha-us"},
                "cn": {"id": "alpha-cn"},
                "hk": {"id": "alpha-hk"},
            },
        },
    )

    updated = quickstart.refresh_account_info(config)

    assert updated["agent_id"] == "alpha"
    assert updated["account_id_us"] == "alpha-us"
    assert updated["account_id_cn"] == "alpha-cn"
    assert updated["account_id_hk"] == "alpha-hk"



def test_print_helper_intro_points_back_to_skill_dialog(quickstart, capsys):
    quickstart.print_helper_intro()

    output = capsys.readouterr().out
    assert "设置引导、策略整理、定时任务建议和启动守门都由 Skill 对话负责" in output
    assert "请回到 Skill 对话完成参赛设置" in output
