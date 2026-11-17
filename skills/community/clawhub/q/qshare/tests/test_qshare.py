import socket
import time
import urllib.request
from io import StringIO
from http.server import HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn
from types import SimpleNamespace

import pytest

from qshare.cli import (
    build_download_url,
    build_parser,
    extract_trycloudflare_url,
    find_available_port,
    get_bundled_cloudflared_binary,
    install_cloudflared_binary,
    launch_trycloudflare_tunnel,
    parse_duration,
    run_share,
    should_run_in_background,
)


def test_share_handler_ignores_cancelled_download(monkeypatch):
    from qshare.cli import ShareHandler

    class Parent:
        def copyfile(self, source, outputfile):
            raise ConnectionResetError("client cancelled")

    monkeypatch.setattr("qshare.cli.SimpleHTTPRequestHandler.copyfile", Parent.copyfile)
    handler = object.__new__(ShareHandler)

    handler.copyfile(object(), object())


def test_share_server_suppresses_client_disconnect_errors(monkeypatch, capsys):
    from qshare.cli import ShareHTTPServer

    server = object.__new__(ShareHTTPServer)
    error = ConnectionResetError("client cancelled")
    monkeypatch.setattr("qshare.cli.sys.exc_info", lambda: (ConnectionResetError, error, None))
    ShareHTTPServer.handle_error(server, object(), ("127.0.0.1", 1))
    assert capsys.readouterr().err == ""


def test_share_server_uses_python_36_compatible_threading_base():
    from qshare.cli import ShareHTTPServer

    assert issubclass(ShareHTTPServer, ThreadingMixIn)
    assert issubclass(ShareHTTPServer, HTTPServer)


def test_share_server_continues_after_client_cancels_download(tmp_path):
    from qshare.cli import find_available_port, start_local_http_server, stop_local_http_server

    file_path = tmp_path / "large-file.bin"
    file_path.write_bytes(b"x" * (2 * 1024 * 1024))
    port = find_available_port()
    server, thread = start_local_http_server(file_path, port)
    try:
        client = socket.create_connection(("127.0.0.1", port))
        client.sendall(b"GET /large-file.bin HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n")
        client.recv(1024)
        client.close()
        time.sleep(0.1)

        with urllib.request.urlopen("http://127.0.0.1:{}/large-file.bin".format(port)) as response:
            assert response.read() == file_path.read_bytes()
        assert thread.is_alive()
    finally:
        stop_local_http_server(server)
        thread.join(timeout=2)


def test_parse_duration_accepts_common_units():
    assert parse_duration("30m") == 1800
    assert parse_duration("90s") == 90
    assert parse_duration("2h") == 7200
    assert parse_duration("120") == 120


def test_parse_duration_rejects_invalid_values():
    with pytest.raises(ValueError):
        parse_duration("abc")
    with pytest.raises(ValueError):
        parse_duration("-5m")


def test_build_parser_defaults_to_two_hours():
    args = build_parser().parse_args(["demo.txt"])
    assert args.ttl == "2h"
    assert not hasattr(args, "daemon")


def test_build_parser_defaults_to_cnb_upload():
    args = build_parser().parse_args(["demo.txt"])
    assert args.cf is False
    assert args.cnb is False


def test_build_parser_accepts_cf_flag():
    args = build_parser().parse_args(["demo.txt", "--cf"])
    assert args.cf is True


def test_should_run_in_background_accepts_d_choice():
    assert should_run_in_background("d") is True
    assert should_run_in_background(" D ") is True
    assert should_run_in_background("") is False
    assert should_run_in_background("n") is False


def test_run_share_does_not_stop_server_when_detached(monkeypatch, tmp_path):
    file_path = tmp_path / "demo.txt"
    file_path.write_text("demo")
    server = object()
    thread = type("Thread", (), {"is_alive": lambda self: False})()
    stop_called = {"value": False}

    monkeypatch.setattr("qshare.cli.start_local_http_server", lambda *_args, **_kwargs: (server, thread))
    monkeypatch.setattr(
        "qshare.cli.launch_trycloudflare_tunnel",
        lambda *_args, **_kwargs: (type("Proc", (), {"poll": lambda self: None})(), "https://abc.trycloudflare.com"),
    )
    monkeypatch.setattr("qshare.cli.ask_background_mode", lambda: True)
    monkeypatch.setattr("qshare.cli.detach_existing_process", lambda *_args, **_kwargs: True)
    monkeypatch.setattr("qshare.cli.start_background_process", lambda *_args, **_kwargs: 0)
    monkeypatch.setattr("qshare.cli.stop_local_http_server", lambda *_args, **_kwargs: stop_called.__setitem__("value", True))

    result = run_share(str(file_path), ttl_seconds=60, port=12345)

    assert result == 0
    assert stop_called["value"] is False


def test_run_share_uses_existing_process_when_detached(monkeypatch, tmp_path):
    file_path = tmp_path / "demo.txt"
    file_path.write_text("demo")
    server = object()
    thread = type("Thread", (), {"is_alive": lambda self: False})()
    detached_server = {"value": None}

    monkeypatch.setattr("qshare.cli.start_local_http_server", lambda *_args, **_kwargs: (server, thread))
    monkeypatch.setattr(
        "qshare.cli.launch_trycloudflare_tunnel",
        lambda *_args, **_kwargs: (type("Proc", (), {"poll": lambda self: None})(), "https://abc.trycloudflare.com"),
    )
    monkeypatch.setattr("qshare.cli.ask_background_mode", lambda: True)
    monkeypatch.setattr(
        "qshare.cli.detach_existing_process",
        lambda value: detached_server.__setitem__("value", value) or True,
    )
    monkeypatch.setattr(
        "qshare.cli.start_background_process",
        lambda *_args, **_kwargs: pytest.fail("should not start a replacement process"),
    )

    assert run_share(str(file_path), ttl_seconds=60, port=12345) == 0
    assert detached_server["value"] is server


def test_background_child_does_not_prompt_to_detach_again(monkeypatch, tmp_path, capsys):
    file_path = tmp_path / "demo.txt"
    file_path.write_text("demo")
    server = object()
    thread = type("Thread", (), {"is_alive": lambda self: False})()
    asked = {"value": False}
    qr_urls = []

    monkeypatch.setenv("QSHARE_BACKGROUND_CHILD", "1")
    monkeypatch.setattr("qshare.cli.start_local_http_server", lambda *_args, **_kwargs: (server, thread))
    monkeypatch.setattr(
        "qshare.cli.launch_trycloudflare_tunnel",
        lambda *_args, **_kwargs: (type("Proc", (), {"poll": lambda self: 0})(), "https://abc.trycloudflare.com"),
    )
    monkeypatch.setattr("qshare.cli.ask_background_mode", lambda: asked.__setitem__("value", True))
    monkeypatch.setattr("qshare.cli.print_qr_code", lambda url: qr_urls.append(url) or print("QR CODE"))

    assert run_share(str(file_path), ttl_seconds=60, port=12345) == 0
    assert asked["value"] is False
    assert qr_urls == ["https://abc.trycloudflare.com/demo.txt"]
    output = capsys.readouterr().out
    assert output.index("PUBLIC FILE URL:") < output.index("QR CODE")


def test_run_share_keeps_public_url_when_qr_code_fails(monkeypatch, tmp_path, capsys):
    file_path = tmp_path / "demo.txt"
    file_path.write_text("demo")
    server = object()
    thread = type("Thread", (), {"is_alive": lambda self: False})()

    monkeypatch.setenv("QSHARE_BACKGROUND_CHILD", "1")
    monkeypatch.setattr("qshare.cli.start_local_http_server", lambda *_args, **_kwargs: (server, thread))
    monkeypatch.setattr(
        "qshare.cli.launch_trycloudflare_tunnel",
        lambda *_args, **_kwargs: (type("Proc", (), {"poll": lambda self: 0})(), "https://abc.trycloudflare.com"),
    )
    monkeypatch.setattr("qshare.cli._load_qrcode", lambda: (_ for _ in ()).throw(ImportError("broken qrcode")))
    monkeypatch.setattr("qshare.cli.maybe_open_qr_in_browser", lambda url: None)

    assert run_share(str(file_path), ttl_seconds=60, port=12345) == 0

    captured = capsys.readouterr()
    assert "PUBLIC FILE URL: https://abc.trycloudflare.com/demo.txt" in captured.out
    assert "QR code unavailable: broken qrcode" in captured.err


def test_find_available_port_skips_occupied_ports():
    occupied = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    occupied.bind(("127.0.0.1", 0))
    occupied.listen(1)
    taken_port = occupied.getsockname()[1]

    port = find_available_port(used_ports={taken_port}, start_port=10000, end_port=10100)

    assert port != taken_port
    assert 10000 <= port <= 10100

    occupied.close()


def test_extract_trycloudflare_url_from_cloudflared_output():
    log = """2025-03-04T10:00:00Z INF Quick Tunnel URL: https://abc123.trycloudflare.com"""
    assert extract_trycloudflare_url(log) == "https://abc123.trycloudflare.com"


def test_extract_trycloudflare_url_rejects_cloudflare_api_url():
    assert extract_trycloudflare_url("https://api.trycloudflare.com") is None
    assert extract_trycloudflare_url("http://department.trycloudflare.com") is None


def test_tunnel_retries_after_cloudflare_api_url(monkeypatch):
    class Output:
        def __init__(self, lines):
            self.lines = iter(lines)

        def readline(self):
            return next(self.lines, "")

    class Process:
        def __init__(self, lines):
            self.stdout = Output(lines)

        def poll(self):
            return 0

    processes = [
        Process(["https://api.trycloudflare.com\n"]),
        Process(["https://api.trycloudflare.com\n"]),
        Process(["https://department.trycloudflare.com\n"]),
    ]
    monkeypatch.setattr("qshare.cli.ensure_cloudflared", lambda: "cloudflared")
    monkeypatch.setattr("qshare.cli.subprocess.Popen", lambda *_args, **_kwargs: processes.pop(0))

    process, url = launch_trycloudflare_tunnel("http://127.0.0.1:20000/file", timeout_seconds=30)

    assert url == "https://department.trycloudflare.com"
    assert process.poll() == 0


def test_print_qr_code_renders_the_public_url(monkeypatch):
    calls = []

    class QRCode:
        def __init__(self, **kwargs):
            calls.append(("init", kwargs))

        def add_data(self, value):
            calls.append(("data", value))

        def make(self, **kwargs):
            calls.append(("make", kwargs))

        def print_ascii(self, **kwargs):
            calls.append(("print", kwargs))

    qrcode = SimpleNamespace(QRCode=QRCode, constants=SimpleNamespace(ERROR_CORRECT_M="M"))
    monkeypatch.setattr("qshare.cli._load_qrcode", lambda: qrcode)

    from qshare.cli import print_qr_code

    print_qr_code("https://department.trycloudflare.com/file.zip")

    assert calls[0][1]["border"] == 4
    assert calls[0][1]["error_correction"] == qrcode.constants.ERROR_CORRECT_M
    assert ("data", "https://department.trycloudflare.com/file.zip") in calls
    assert ("print", {"invert": True}) in calls


def test_print_qr_code_renders_in_terminal_on_windows(monkeypatch):
    # Windows CMD now shows the same terminal QR as other platforms; the
    # browser page is a separate opt-in step.
    printed = []

    class QRCode:
        def __init__(self, **kwargs):
            pass

        def add_data(self, value):
            pass

        def make(self, **kwargs):
            pass

        def print_ascii(self, **kwargs):
            printed.append(kwargs)

    qrcode = SimpleNamespace(QRCode=QRCode, constants=SimpleNamespace(ERROR_CORRECT_M="M"))
    monkeypatch.setattr("qshare.cli._load_qrcode", lambda: qrcode)
    monkeypatch.setattr("qshare.cli.os.name", "nt")
    monkeypatch.setattr(
        "qshare.cli.webbrowser.open",
        lambda target: pytest.fail("terminal QR must not open a browser"),
    )

    from qshare.cli import print_qr_code

    print_qr_code("https://department.trycloudflare.com/file.zip")
    assert printed == [{"invert": True}]


def test_maybe_open_qr_in_browser_prompts_last_on_windows(monkeypatch, tmp_path):
    class QRCode:
        def __init__(self, **kwargs):
            pass

        def add_data(self, value):
            pass

        def make(self, **kwargs):
            pass

        def get_matrix(self):
            return [[True, False], [False, True]]

        def print_ascii(self, **kwargs):
            raise AssertionError("the browser page must not re-render the terminal QR")

    qrcode = SimpleNamespace(QRCode=QRCode, constants=SimpleNamespace(ERROR_CORRECT_M="M"))
    monkeypatch.setattr("qshare.cli._load_qrcode", lambda: qrcode)
    monkeypatch.setattr("qshare.cli.tempfile.gettempdir", lambda: str(tmp_path))
    opened = []
    monkeypatch.setattr("qshare.cli.webbrowser.open", lambda target: opened.append(target) or True)
    answers = []
    monkeypatch.setattr("builtins.input", lambda value: answers.append(value) or "")

    from qshare.cli import maybe_open_qr_in_browser

    url = "https://department.trycloudflare.com/file.zip"
    # The default (empty answer) opens the browser page.
    with monkeypatch.context() as windows:
        windows.setattr("qshare.cli.os.name", "nt")
        maybe_open_qr_in_browser(url)
    # Decode the file URI using the actual host platform's path rules.
    assert opened and opened[0].startswith("file:")
    from urllib.parse import urlparse
    from urllib.request import url2pathname

    page_path = url2pathname(urlparse(opened[0]).path)
    with open(page_path, encoding="utf-8") as handle:
        page = handle.read()
    # The browser page must show the download link above the QR code,
    # offer a one-click copy button, and keep the button in place after
    # its text changes to the copied state.
    assert url in page
    assert "copyLink" in page
    assert "<svg" in page
    assert page.index("<p id=\"link\">") < page.index("<svg")
    assert 'id="copy"' in page
    assert "white-space: nowrap" in page
    assert "min-width: 220px" in page


def test_maybe_open_qr_in_browser_skipped_when_user_answers_n(monkeypatch, capsys):
    monkeypatch.setattr("qshare.cli.os.name", "nt")
    monkeypatch.setattr(
        "qshare.cli._show_qr_page_windows",
        lambda url: pytest.fail("answering n must not open the browser page"),
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    from qshare.cli import maybe_open_qr_in_browser

    maybe_open_qr_in_browser("https://department.trycloudflare.com/file.zip")
    assert "已跳过浏览器二维码页面" in capsys.readouterr().out


def test_maybe_open_qr_in_browser_noop_on_unix(monkeypatch):
    monkeypatch.setattr("qshare.cli.os.name", "posix")
    monkeypatch.setattr(
        "qshare.cli.ask_open_qr_in_browser",
        lambda: pytest.fail("Unix terminals must not be asked to open a browser"),
    )

    from qshare.cli import maybe_open_qr_in_browser

    maybe_open_qr_in_browser("https://department.trycloudflare.com/file.zip")


def test_confirm_delete_cnb_file_defaults_to_delete(monkeypatch):
    from qshare.cli import confirm_delete_cnb_file

    monkeypatch.setattr("builtins.input", lambda _prompt: "")
    assert confirm_delete_cnb_file() is True
    monkeypatch.setattr("builtins.input", lambda _prompt: "\n")
    assert confirm_delete_cnb_file() is True
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")
    assert confirm_delete_cnb_file() is False
    monkeypatch.setattr("builtins.input", lambda _prompt: "NO")
    assert confirm_delete_cnb_file() is False
    monkeypatch.setattr("builtins.input", lambda _prompt: "y")
    assert confirm_delete_cnb_file() is True


def test_confirm_delete_cnb_file_uses_english_fallback_for_ascii_stdout(monkeypatch):
    from qshare.cli import confirm_delete_cnb_file

    class ASCIIStream(StringIO):
        encoding = "ascii"

    prompt = []
    monkeypatch.setattr("qshare.cli.sys.stdout", ASCIIStream())
    monkeypatch.setattr("builtins.input", lambda value: prompt.append(value) or "n")

    assert confirm_delete_cnb_file() is False
    assert prompt == ["Delete the uploaded file from CNB? [Y/n]: "]


def test_delete_cnb_assets_removes_matching_assets(monkeypatch):
    from qshare import cnb

    releases = [
        {
            "tag_name": "2026-10-10",
            "id": 7,
            "assets": [
                {"id": 11, "name": "demo.zip", "browser_download_url": "u"},
                {"id": 12, "name": "other.zip", "browser_download_url": "u"},
            ],
        },
        {"tag_name": "2026-10-09", "id": 8, "assets": [{"id": 13, "name": "demo.zip"}]},
    ]
    calls = []

    def fake_request_json(url, method="GET", payload=None):
        calls.append((url, method))
        return releases if method == "GET" else {}

    monkeypatch.setattr(cnb, "request_json", fake_request_json)

    assert cnb.delete_cnb_assets("2026-10-10", "demo.zip") == 1
    assert calls == [
        ("https://api.cnb.cool/steinveni/qshare/-/releases", "GET"),
        ("https://api.cnb.cool/steinveni/qshare/-/releases/7/assets/11", "DELETE"),
    ]


def test_run_cnb_upload_uploads_without_confirmation_then_prompts_delete(monkeypatch, tmp_path, capsys):
    from qshare.cli import run_cnb_upload

    file_path = tmp_path / "demo.zip"
    file_path.write_text("data")
    prompts = []
    delete_calls = []

    monkeypatch.setattr(
        "qshare.cnb.upload_to_cnb",
        lambda path: ("https://e.cnb.cool/demo.zip", "2026-10-10"),
    )
    monkeypatch.setattr("qshare.cnb.delete_cnb_assets", lambda tag, name: delete_calls.append((tag, name)) or 1)
    monkeypatch.setattr("qshare.cli.print_qr_code", lambda url: None)
    browser_prompts = []
    monkeypatch.setattr(
        "qshare.cli.maybe_open_qr_in_browser",
        lambda url: browser_prompts.append(url),
    )
    monkeypatch.setattr("builtins.input", lambda value: prompts.append(value) or "")

    assert run_cnb_upload(str(file_path)) == 0

    output = capsys.readouterr().out
    # No pre-upload confirmation prompt; only the post-upload delete prompt.
    assert prompts == ["上传完成。是否删除 CNB 上的该文件？输入 n 保留 / Delete the uploaded file from CNB? [Y/n]: "]
    assert "PUBLIC FILE URL: https://e.cnb.cool/demo.zip" in output
    # Answering nothing accepts the default: delete the uploaded file on CNB.
    assert delete_calls == [("2026-10-10", "demo.zip")]
    # The local file is never touched by the CNB channel.
    assert file_path.exists()
    # The CNB asset was deleted, so the QR page would show a dead link:
    # the browser page must not be offered.
    assert browser_prompts == []


def test_run_cnb_upload_keeps_cnb_file_when_user_answers_n(monkeypatch, tmp_path, capsys):
    from qshare.cli import run_cnb_upload

    file_path = tmp_path / "demo.zip"
    file_path.write_text("data")

    monkeypatch.setattr(
        "qshare.cnb.upload_to_cnb",
        lambda path: ("https://e.cnb.cool/demo.zip", "2026-10-10"),
    )
    monkeypatch.setattr(
        "qshare.cnb.delete_cnb_assets",
        lambda tag, name: pytest.fail("should not delete the CNB asset"),
    )
    monkeypatch.setattr("qshare.cli.print_qr_code", lambda url: None)
    browser_prompts = []
    monkeypatch.setattr(
        "qshare.cli.maybe_open_qr_in_browser",
        lambda url: browser_prompts.append(url),
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    assert run_cnb_upload(str(file_path)) == 0
    assert "已保留 CNB 上的文件" in capsys.readouterr().out
    # The file stays on CNB, so the browser QR page is still offered.
    assert browser_prompts == ["https://e.cnb.cool/demo.zip"]

    file_path = tmp_path / "demo.zip"
    file_path.write_text("data")

    monkeypatch.setattr(
        "qshare.cnb.upload_to_cnb",
        lambda path: ("https://e.cnb.cool/demo.zip", "2026-10-10"),
    )
    monkeypatch.setattr(
        "qshare.cnb.delete_cnb_assets",
        lambda tag, name: pytest.fail("should not delete the CNB asset"),
    )
    monkeypatch.setattr("qshare.cli.print_qr_code", lambda url: None)
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    assert run_cnb_upload(str(file_path)) == 0


@pytest.mark.parametrize("answer", ["", "y", "n"])
def test_run_cnb_upload_windows_only_prompts_for_browser_when_file_kept(monkeypatch, tmp_path, answer):
    from qshare.cli import run_cnb_upload

    file_path = tmp_path / "demo.zip"
    file_path.write_text("data")
    prompts = []
    delete_calls = []
    answers = iter([answer, "n"])

    def fake_input(prompt):
        prompts.append(prompt)
        return next(answers)

    monkeypatch.setattr("qshare.cli.os", SimpleNamespace(name="nt"))
    monkeypatch.setattr("qshare.cnb.upload_to_cnb", lambda path: ("https://e.cnb.cool/demo.zip", "2026-10-10"))
    monkeypatch.setattr("qshare.cnb.delete_cnb_assets", lambda tag, name: delete_calls.append((tag, name)) or 1)
    monkeypatch.setattr("qshare.cli.print_qr_code", lambda url: None)
    monkeypatch.setattr(
        "qshare.cli._show_qr_page_windows",
        lambda url: pytest.fail("the browser must not open after deletion or answering n"),
    )
    monkeypatch.setattr("builtins.input", fake_input)

    assert run_cnb_upload(str(file_path)) == 0
    assert "Delete the uploaded file from CNB?" in prompts[0]
    if answer == "n":
        assert delete_calls == []
        assert len(prompts) == 2
        assert "Open the QR page in your browser?" in prompts[1]
    else:
        assert delete_calls == [("2026-10-10", "demo.zip")]
        assert len(prompts) == 1


def test_install_cloudflared_binary_copies_bundled_binary(monkeypatch, tmp_path, capsys):
    bundled = tmp_path / "bundled-cloudflared"
    bundled.write_bytes(b"cloudflared")
    monkeypatch.setattr("qshare.cli.Path.home", lambda: tmp_path)
    monkeypatch.setattr("qshare.cli.get_bundled_cloudflared_binary", lambda: bundled)

    installed = install_cloudflared_binary()

    assert Path(installed).read_bytes() == b"cloudflared"
    assert "Installing the binary bundled with qshare" in capsys.readouterr().out


def test_get_bundled_cloudflared_binary_requires_platform_wheel(monkeypatch, tmp_path):
    monkeypatch.setattr("qshare.cli.Path.resolve", lambda self: tmp_path / "cli.py")

    with pytest.raises(RuntimeError, match="no bundled cloudflared binary"):
        get_bundled_cloudflared_binary()


def test_build_download_url_joins_base_and_filename():
    assert build_download_url("https://abc.trycloudflare.com", "demo.zip") == "https://abc.trycloudflare.com/demo.zip"
    assert build_download_url("https://abc.trycloudflare.com/", "/demo.zip") == "https://abc.trycloudflare.com/demo.zip"


def test_parser_accepts_cnb_flag():
    args = build_parser().parse_args(["sample.zip", "--cnb"])
    assert args.cnb is True


def test_cnb_confirmation_requires_y(monkeypatch):
    from qshare.cli import confirm_cnb_upload

    monkeypatch.setattr("builtins.input", lambda _prompt: "yes")
    assert confirm_cnb_upload() is False
    monkeypatch.setattr("builtins.input", lambda _prompt: "Y")
    assert confirm_cnb_upload() is True


def test_privacy_warning_uses_english_fallback_for_ascii_stdout(monkeypatch):
    from qshare.cli import print_privacy_warning

    class ASCIIStream(StringIO):
        encoding = "ascii"

    stream = ASCIIStream()
    monkeypatch.setattr("qshare.cli.sys.stdout", stream)

    print_privacy_warning()

    output = stream.getvalue()
    assert "IMPORTANT SECURITY WARNING" in output
    assert "Encrypt private files before transferring them." in output
    assert "重要安全提示" not in output


def test_cnb_confirmation_uses_english_fallback_for_ascii_stdout(monkeypatch):
    from qshare.cli import confirm_cnb_upload

    class ASCIIStream(StringIO):
        encoding = "ascii"

    prompt = []
    monkeypatch.setattr("qshare.cli.sys.stdout", ASCIIStream())
    monkeypatch.setattr("builtins.input", lambda value: prompt.append(value) or "n")

    assert confirm_cnb_upload() is False
    assert prompt == ["Confirm upload to CNB (y/N): "]
