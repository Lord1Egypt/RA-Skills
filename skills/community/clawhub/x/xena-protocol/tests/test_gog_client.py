"""gog_client wraps the `gog` CLI. Tests mock subprocess; real gog integration
reserved for manual e2e."""

import base64
import json
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from bin.gog_client import (
    GogClient,
    GogError,
    is_gog_installed,
    verify_auth,
)


def _run(stdout: str, returncode: int = 0) -> MagicMock:
    m = MagicMock()
    m.stdout = stdout
    m.stderr = ""
    m.returncode = returncode
    return m


# is_gog_installed
def test_is_gog_installed_true():
    with patch("bin.gog_client.shutil.which", return_value="/usr/local/bin/gog"):
        assert is_gog_installed() is True


def test_is_gog_installed_false():
    with patch("bin.gog_client.shutil.which", return_value=None):
        assert is_gog_installed() is False


# verify_auth — calls `gog auth list` and checks the given account is there
def test_verify_auth_finds_account():
    out = json.dumps([
        {"email": "you@gmail.com", "services": ["gmail", "calendar"]},
        {"email": "other@gmail.com", "services": ["gmail"]},
    ])
    with patch("subprocess.run", return_value=_run(out)):
        assert verify_auth("you@gmail.com") is True


def test_verify_auth_missing_account():
    out = json.dumps([{"email": "other@gmail.com", "services": ["gmail"]}])
    with patch("subprocess.run", return_value=_run(out)):
        assert verify_auth("you@gmail.com") is False


def test_verify_auth_gog_error_returns_false():
    with patch("subprocess.run", side_effect=FileNotFoundError):
        assert verify_auth("you@gmail.com") is False


# GogClient.list_unread
def test_list_unread_parses_message_ids():
    out = json.dumps([
        {"id": "msg1", "threadId": "t1", "snippet": "Hello"},
        {"id": "msg2", "threadId": "t2", "snippet": "Invoice"},
    ])
    with patch("subprocess.run", return_value=_run(out)) as run:
        client = GogClient(account="you@gmail.com")
        messages = client.list_unread()
        assert [m["id"] for m in messages] == ["msg1", "msg2"]

    args = run.call_args.args[0]
    assert args[0] == "gog"
    assert "gmail" in args
    assert "you@gmail.com" in args
    # json flag present
    assert "--json" in args


def test_list_unread_custom_query():
    out = json.dumps([])
    with patch("subprocess.run", return_value=_run(out)) as run:
        GogClient(account="x@y.com").list_unread(query="is:unread newer_than:1d", max_results=5)
    args = run.call_args.args[0]
    assert "is:unread newer_than:1d" in args
    assert "5" in args  # max


def test_list_unread_empty_result():
    with patch("subprocess.run", return_value=_run("[]")):
        assert GogClient(account="x@y.com").list_unread() == []


def test_list_unread_wrapped_messages_shape():
    # Current real gog output wraps results under a `messages` key.
    out = json.dumps({
        "messages": [{"id": "m1", "threadId": "t1"}, {"id": "m2", "threadId": "t2"}],
        "nextPageToken": "abc",
    })
    with patch("subprocess.run", return_value=_run(out)):
        messages = GogClient(account="x@y.com").list_unread()
    assert [m["id"] for m in messages] == ["m1", "m2"]


def test_list_unread_wrapped_empty_messages():
    out = json.dumps({"messages": []})
    with patch("subprocess.run", return_value=_run(out)):
        assert GogClient(account="x@y.com").list_unread() == []


def test_list_unread_raises_on_nonzero_exit():
    with patch("subprocess.run", return_value=_run("bad output", returncode=1)):
        with pytest.raises(GogError):
            GogClient(account="x@y.com").list_unread()


# fetch_mime
def test_fetch_mime_decodes_base64url():
    raw_bytes = b"From: test\r\nSubject: hi\r\n\r\nbody"
    b64 = base64.urlsafe_b64encode(raw_bytes).decode().rstrip("=")
    out = json.dumps({"id": "msg1", "raw": b64})
    with patch("subprocess.run", return_value=_run(out)) as run:
        client = GogClient(account="x@y.com")
        result = client.fetch_mime("msg1")
    assert result == raw_bytes
    args = run.call_args.args[0]
    assert "msg1" in args
    assert "raw" in args


def test_fetch_mime_missing_raw_field_raises():
    out = json.dumps({"id": "msg1"})  # no raw field
    with patch("subprocess.run", return_value=_run(out)):
        with pytest.raises(GogError, match="raw"):
            GogClient(account="x@y.com").fetch_mime("msg1")


def test_fetch_mime_wrapped_message_shape():
    # Current real gog output nests under `message`.
    raw_bytes = b"From: test\r\nSubject: hi\r\n\r\nbody"
    b64 = base64.urlsafe_b64encode(raw_bytes).decode().rstrip("=")
    out = json.dumps({"headers": {"from": "test"}, "message": {"id": "m1", "raw": b64}})
    with patch("subprocess.run", return_value=_run(out)):
        assert GogClient(account="x@y.com").fetch_mime("m1") == raw_bytes


# mark_read
def test_mark_read_calls_modify_with_remove_unread():
    with patch("subprocess.run", return_value=_run("{}")) as run:
        GogClient(account="x@y.com").mark_read("msg1")
    args = run.call_args.args[0]
    assert "msg1" in args
    assert "UNREAD" in args


# search
def test_search_returns_list():
    out = json.dumps([{"id": "a"}, {"id": "b"}])
    with patch("subprocess.run", return_value=_run(out)):
        results = GogClient(account="x@y.com").search("from:bob@scam.xyz")
    assert len(results) == 2
