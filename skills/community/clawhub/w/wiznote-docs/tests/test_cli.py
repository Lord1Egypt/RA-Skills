from __future__ import annotations

import json
from urllib.error import URLError

import pytest

import wiznote_cli as cli


class FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


@pytest.fixture(autouse=True)
def clear_wiznote_env(monkeypatch):
    for key in ["WIZNOTE_BASE_URL", "WIZNOTE_USER", "WIZNOTE_PASSWORD"]:
        monkeypatch.delenv(key, raising=False)


def test_build_parser_supports_list_notes_command():
    parser = cli.build_parser()

    args = parser.parse_args(["list-notes", "--category-root", "/team/docs/", "--category", "plans/"])

    assert args.command == "list-notes"
    assert args.category_root == "/team/docs/"
    assert args.category == "plans/"


def test_load_credentials_prefers_explicit_values_over_env(monkeypatch):
    monkeypatch.setenv("WIZNOTE_BASE_URL", "http://env")
    monkeypatch.setenv("WIZNOTE_USER", "env-user")
    monkeypatch.setenv("WIZNOTE_PASSWORD", "env-pass")

    creds = cli.load_credentials(base_url="http://flag", user="flag-user", password="flag-pass")

    assert creds.base_url == "http://flag"
    assert creds.user == "flag-user"
    assert creds.password == "flag-pass"


def test_load_credentials_requires_all_values(monkeypatch):
    monkeypatch.setenv("WIZNOTE_BASE_URL", "http://env")
    monkeypatch.setenv("WIZNOTE_USER", "env-user")

    with pytest.raises(ValueError, match="WIZNOTE_PASSWORD"):
        cli.load_credentials()


def test_load_credentials_does_not_fall_back_to_env_for_explicit_empty_values(monkeypatch):
    monkeypatch.setenv("WIZNOTE_BASE_URL", "http://env")
    monkeypatch.setenv("WIZNOTE_USER", "env-user")
    monkeypatch.setenv("WIZNOTE_PASSWORD", "env-pass")

    with pytest.raises(ValueError, match="WIZNOTE_BASE_URL, WIZNOTE_USER, WIZNOTE_PASSWORD"):
        cli.load_credentials(base_url="", user="", password="")


def test_login_request_payload_uses_web_defaults():
    creds = cli.Credentials(base_url="http://wiz", user="user@example.com", password="secret")

    payload = cli.login_request_payload(creds)

    assert payload == {
        "userId": "user@example.com",
        "password": "secret",
        "autoLogin": True,
        "clientType": "web",
        "clientVersion": "4.0",
        "lang": "zh-cn",
    }


def test_note_list_request_builds_full_url_and_auth_header():
    request = cli.note_list_request(
        base_url="http://wiz/",
        kb_guid="kb-1",
        token="tok",
        category="/team/docs/",
        start=25,
        count=50,
    )

    assert request.url == (
        "http://wiz/ks/note/list/category/kb-1"
        "?start=25&count=50&category=%2Fteam%2Fdocs%2F&orderBy=modified&ascending=desc"
    )
    assert request.headers == {"X-Wiz-Token": "tok"}


def test_note_html_path_uses_download_endpoint_for_markdown_mirror():
    assert cli.note_html_path("kb-1", "doc-1") == "/ks/note/download/kb-1/doc-1"


def test_note_create_request_builds_full_url_json_headers_and_payload():
    request = cli.note_create_request(
        base_url="http://wiz/",
        kb_guid="kb-1",
        token="tok",
        title="Spec",
        category="/team/docs/",
        html="<p>Hello</p>",
    )

    assert request.url == "http://wiz/ks/note/create/kb-1"
    assert request.headers == {"X-Wiz-Token": "tok", "Content-type": "application/json"}
    assert json.loads(request.data.decode("utf-8")) == {
        "kbGuid": "kb-1",
        "title": "Spec",
        "category": "/team/docs/",
        "html": "<p>Hello</p>",
    }
    assert request.method == "POST"


def test_fetch_note_html_sends_auth_header_and_returns_text(monkeypatch):
    captured = {}

    class HtmlResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return b"<html><body><h1>Spec</h1></body></html>"

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["headers"] = dict(request.header_items())
        captured["timeout"] = timeout
        return HtmlResponse()

    monkeypatch.setattr(cli, "urlopen", fake_urlopen)

    html = cli.fetch_note_html(
        base_url="http://wiz",
        kb_guid="kb-1",
        doc_guid="doc-1",
        token="tok",
    )

    assert captured == {
        "url": "http://wiz/ks/note/download/kb-1/doc-1",
        "method": "GET",
        "headers": {"X-wiz-token": "tok"},
        "timeout": 10,
    }
    assert html == "<html><body><h1>Spec</h1></body></html>"


def test_create_note_sends_json_request_and_parses_response(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["headers"] = dict(request.header_items())
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return FakeResponse({"returnCode": 200, "result": {"docGuid": "doc-1"}})

    monkeypatch.setattr(cli, "urlopen", fake_urlopen)

    payload = cli.create_note(
        base_url="http://wiz",
        kb_guid="kb-1",
        token="tok",
        title="Spec",
        category="/team/docs/",
        html="<p>Hello</p>",
    )

    assert captured == {
        "url": "http://wiz/ks/note/create/kb-1",
        "method": "POST",
        "headers": {"Content-type": "application/json", "X-wiz-token": "tok"},
        "body": {
            "kbGuid": "kb-1",
            "title": "Spec",
            "category": "/team/docs/",
            "html": "<p>Hello</p>",
        },
        "timeout": 10,
    }
    assert payload == {"returnCode": 200, "result": {"docGuid": "doc-1"}}


def test_save_note_sends_json_request_and_parses_response(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["headers"] = dict(request.header_items())
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return FakeResponse({"returnCode": 200, "result": {"docGuid": "doc-1"}})

    monkeypatch.setattr(cli, "urlopen", fake_urlopen)

    payload = cli.save_note(
        base_url="http://wiz",
        kb_guid="kb-1",
        doc_guid="doc-1",
        token="tok",
        title="Spec",
        category="/team/docs/",
        html="<p>Hello</p>",
    )

    assert captured == {
        "url": "http://wiz/ks/note/save/kb-1/doc-1",
        "method": "PUT",
        "headers": {"Content-type": "application/json", "X-wiz-token": "tok"},
        "body": {
            "kbGuid": "kb-1",
            "docGuid": "doc-1",
            "title": "Spec",
            "category": "/team/docs/",
            "html": "<p>Hello</p>",
        },
        "timeout": 10,
    }
    assert payload == {"returnCode": 200, "result": {"docGuid": "doc-1"}}


def test_login_sends_json_request_and_parses_response(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["headers"] = dict(request.header_items())
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return FakeResponse(
            {
                "returnCode": 200,
                "result": {
                    "token": "tok",
                    "kbServer": "https://notes.example.com",
                    "kbGuid": "kb-1",
                },
            }
        )

    monkeypatch.setattr(cli, "urlopen", fake_urlopen)

    result = cli.login(cli.Credentials(base_url="http://wiz", user="user@example.com", password="secret"))

    assert captured == {
        "url": "http://wiz/as/user/login?clientType=web&clientVersion=4.0&lang=zh-cn",
        "method": "POST",
        "headers": {"Content-type": "application/json"},
        "body": {
            "userId": "user@example.com",
            "password": "secret",
            "autoLogin": True,
            "clientType": "web",
            "clientVersion": "4.0",
            "lang": "zh-cn",
        },
        "timeout": 10,
    }
    assert result.token == "tok"
    assert result.kb_server == "https://notes.example.com"
    assert result.kb_guid == "kb-1"


def test_fetch_note_list_sends_auth_header_and_returns_payload(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["headers"] = dict(request.header_items())
        captured["timeout"] = timeout
        return FakeResponse({"result": [{"docGuid": "doc-1", "title": "Spec"}]})

    monkeypatch.setattr(cli, "urlopen", fake_urlopen)

    payload = cli.fetch_note_list(
        base_url="http://wiz",
        kb_guid="kb-1",
        token="tok",
        category="/team/docs/",
        start=0,
        count=10,
    )

    assert captured == {
        "url": "http://wiz/ks/note/list/category/kb-1?start=0&count=10&category=%2Fteam%2Fdocs%2F&orderBy=modified&ascending=desc",
        "method": "GET",
        "headers": {"X-wiz-token": "tok"},
        "timeout": 10,
    }
    assert payload == {"result": [{"docGuid": "doc-1", "title": "Spec"}]}


def test_login_wraps_transport_errors(monkeypatch):
    def fake_urlopen(request, timeout):
        raise URLError("offline")

    monkeypatch.setattr(cli, "urlopen", fake_urlopen)

    with pytest.raises(ValueError, match="WizNote login request failed"):
        cli.login(cli.Credentials(base_url="http://wiz", user="user@example.com", password="secret"))


def test_fetch_note_list_wraps_invalid_json(monkeypatch):
    class InvalidJsonResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return b"not-json"

    def fake_urlopen(request, timeout):
        return InvalidJsonResponse()

    monkeypatch.setattr(cli, "urlopen", fake_urlopen)

    with pytest.raises(ValueError, match="WizNote note list returned invalid JSON"):
        cli.fetch_note_list(base_url="http://wiz", kb_guid="kb-1", token="tok", category="/team/docs/")
