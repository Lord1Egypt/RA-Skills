from pathlib import Path

import pytest

from wiznote_helper import (
    extract_html_body,
    mirror_output_path,
    normalize_category_root,
    note_list_path,
    parse_login_result,
    resolve_category,
)


def test_parse_login_result_extracts_token_and_kb_info():
    payload = {
        "returnCode": 200,
        "result": {
            "token": "tok",
            "kbServer": "https://notes.example.com",
            "kbGuid": "kb-1",
        },
    }

    result = parse_login_result(payload)

    assert result.token == "tok"
    assert result.kb_server == "https://notes.example.com"
    assert result.kb_guid == "kb-1"


def test_parse_login_result_raises_on_non_200():
    payload = {"returnCode": 31002, "returnMessage": "invalid credentials"}

    with pytest.raises(ValueError, match="31002"):
        parse_login_result(payload)


def test_parse_login_result_raises_on_missing_fields():
    payload = {"returnCode": 200, "result": {"token": "tok"}}

    with pytest.raises(ValueError, match="kbServer"):
        parse_login_result(payload)


def test_normalize_category_root_adds_trailing_slash():
    assert normalize_category_root("/team/docs") == "/team/docs/"


def test_normalize_category_root_rejects_relative_paths():
    with pytest.raises(ValueError, match="absolute"):
        normalize_category_root("team/docs")


def test_resolve_category_appends_relative_path():
    assert resolve_category("/team/docs/", "plans/2026/") == "/team/docs/plans/2026/"


def test_resolve_category_accepts_absolute_child_path():
    assert resolve_category("/team/docs/", "/team/docs/plans/") == "/team/docs/plans/"


def test_resolve_category_rejects_paths_outside_root():
    with pytest.raises(ValueError, match="outside category root"):
        resolve_category("/team/docs/", "/other/docs/")


def test_note_list_path_encodes_category_and_paging():
    path = note_list_path("kb-1", "/team/docs/", start=50, count=25)

    assert path == "/ks/note/list/category/kb-1?start=50&count=25&category=%2Fteam%2Fdocs%2F&orderBy=modified&ascending=desc"


def test_mirror_output_path_preserves_relative_category_and_note_name(tmp_path: Path):
    out = mirror_output_path(tmp_path, "/team/docs/", "/team/docs/plans/", "Skill Design")

    assert out == tmp_path / "docs" / "wiznote-mirror" / "plans" / "Skill-Design.md"


def test_mirror_output_path_rejects_category_traversal(tmp_path: Path):
    with pytest.raises(ValueError, match="outside category root"):
        mirror_output_path(tmp_path, "/team/docs/", "/team/docs/../../secret/", "Skill Design")


def test_mirror_output_path_rejects_unsafe_title(tmp_path: Path):
    with pytest.raises(ValueError, match="Unsafe note title"):
        mirror_output_path(tmp_path, "/team/docs/", "/team/docs/plans/", "../README")


def test_mirror_output_path_allows_unicode_title(tmp_path: Path):
    out = mirror_output_path(tmp_path, "/team/docs/", "/team/docs/plans/", "设计文档")

    assert out == tmp_path / "docs" / "wiznote-mirror" / "plans" / "设计文档.md"


def test_extract_html_body_prefers_body_content():
    html = "<html><head><title>x</title></head><body><h1>Hello</h1><p>World</p></body></html>"

    assert extract_html_body(html) == "<h1>Hello</h1><p>World</p>"


def test_extract_html_body_handles_mixed_case_and_attributes():
    html = '<HTML><BODY class="note-body"><div>Mixed</div></BODY></HTML>'

    assert extract_html_body(html) == "<div>Mixed</div>"


def test_extract_html_body_ignores_body_like_text_before_real_body():
    html = '<html><head><script>var tpl = "<body fake>";</script></head><body><p>Real</p></body></html>'

    assert extract_html_body(html) == "<p>Real</p>"


def test_extract_html_body_returns_original_html_when_body_missing():
    html = "<html><div>No body wrapper</div></html>"

    assert extract_html_body(html) == html
