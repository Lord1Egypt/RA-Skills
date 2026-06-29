"""Corpus management: local, hybrid, batch, glob, URL-as-md, PDF, image, legacy compat."""
from __future__ import annotations

import json
import http.server
import os
import socket
import socketserver
import threading
import urllib.request
from pathlib import Path

import research_mode_control_commands as control_commands

from .helpers import assert_eq, assert_in, assert_true, json_out, run


class _FixtureHttpServer:
    def __init__(self, root: Path):
        self.root = root
        self.httpd: socketserver.TCPServer | None = None
        self.thread: threading.Thread | None = None

    def __enter__(self) -> str:
        root = self.root

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(root), **kwargs)

            def log_message(self, format: str, *args) -> None:
                return

        self.httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
        port = int(self.httpd.server_address[1])
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        return f"http://127.0.0.1:{port}"

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.httpd is not None:
            self.httpd.shutdown()
            self.httpd.server_close()
        if self.thread is not None:
            self.thread.join(timeout=5)


class _RedirectHttpServer:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.httpd: socketserver.TCPServer | None = None
        self.thread: threading.Thread | None = None

    def __enter__(self) -> str:
        target_url = self.target_url

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                self.send_response(302)
                self.send_header("Location", target_url)
                self.end_headers()

            def log_message(self, format: str, *args) -> None:
                return

        self.httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
        port = int(self.httpd.server_address[1])
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        return f"http://attacker.test:{port}"

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.httpd is not None:
            self.httpd.shutdown()
            self.httpd.server_close()
        if self.thread is not None:
            self.thread.join(timeout=5)


def test_corpus_local(root: Path) -> None:
    corpus_source = root / "corpus-source.txt"
    corpus_source.write_text("local corpus selftest\n", encoding="utf-8")
    created = json_out(run("create", "--root", str(root), "--id", "task-corpus", "--goal", "Self-test local corpus path", "--corpus-mode", "local"))
    assert_eq(created["corpus_mode"], "local", "create should expose corpus_mode")
    attached = json_out(run("attach-input", "--root", str(root), "--id", "task-corpus", "--file", str(corpus_source), "--label", "seed", "--note", "local fixture"))
    assert_eq(attached["corpus_mode"], "local", "attach-input should preserve local corpus mode")
    assert_eq(len(attached["corpus_entries"]), 1, "attach-input should register one corpus file")
    attached_note = json_out(run("attach-note", "--root", str(root), "--id", "task-corpus", "--title", "Operator note", "--text", "# Inline note\n\nRemember this local lead.", "--label", "inline", "--note", "operator context"))
    assert_eq(attached_note["corpus_mode"], "local", "attach-note should preserve local corpus mode")
    assert_true(attached_note["path"].endswith("operator-note.md"), "attach-note should generate a slugged note path")
    note_path = root / "task-corpus" / attached_note["path"]
    assert_true(note_path.exists() and "Remember this local lead." in note_path.read_text(encoding="utf-8"), "attach-note should materialize the note file in corpus")
    assert_eq(len(attached_note["corpus_entries"]), 2, "attach-note should append a second corpus entry")
    lease = json_out(run("begin", "--root", str(root), "--id", "task-corpus"))
    assert_eq(lease["corpus"]["mode"], "local", "begin work order should expose corpus mode")
    assert_true(any(e.get("path") == "input/corpus/corpus-source.txt" and e.get("label") == "seed" and e.get("note") == "local fixture" for e in lease["corpus"]["entries"]), "begin work order should expose attached corpus entry with metadata")
    assert_true(any(e.get("path") == attached_note["path"] and e.get("label") == "inline" and e.get("note") == "operator context" for e in lease["corpus"]["entries"]), "begin work order should expose attached inline note with metadata")
    assert_true(lease["paths"]["corpus_manifest_path"].endswith("/input/corpus-manifest.json"), "begin work order should expose corpus manifest path")
    status = json_out(run("status", "--root", str(root), "--id", "task-corpus", "--format", "json"))
    assert_eq(status["corpus"]["mode"], "local", "status json should expose corpus mode")
    assert_true(status["artifacts"]["corpus_dir"].endswith("/input/corpus"), "status json should expose corpus_dir")
    summary_text = run("summary", "--root", str(root), "--id", "task-corpus", "--format", "text").stdout
    assert_in("Corpus: mode=local, files=2", summary_text, "summary text should expose corpus mode and file count")
    assert_in("Corpus manifest:", summary_text, "summary text should expose corpus manifest path")
    playbook = (root / "task-corpus" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in("## Corpus", playbook, "playbook should include corpus section")
    assert_in("Mode: `local`", playbook, "playbook should include corpus section")
    prompt = run("render-prompt", "--root", str(root), "--id", "task-corpus").stdout
    assert_in("corpus.mode / corpus.entries", prompt, "worker prompt should mention corpus guidance")
    assert_in("paths.corpus_dir", prompt, "worker prompt should mention corpus guidance")
    run("fail", "--root", str(root), "--id", "task-corpus", "--run-id", lease["run_id"], "--error", "cleanup after corpus lease inspection")
    summary_after_fail = run("summary", "--root", str(root), "--id", "task-corpus", "--format", "text").stdout
    assert_in("Recent run outcomes (1):", summary_after_fail, "summary text should expose recent run outcomes with normalized reasons from runs.tsv")
    assert_in("outcome=failed", summary_after_fail, "summary text should expose recent run outcomes with normalized reasons from runs.tsv")
    assert_in("reason=retry:worker-error", summary_after_fail, "summary text should expose recent run outcomes with normalized reasons from runs.tsv")
    playbook_after_fail = (root / "task-corpus" / "task-playbook.md").read_text(encoding="utf-8")
    assert_in("## Recent run outcomes", playbook_after_fail, "playbook should expose recent run outcomes with normalized reasons")
    assert_in("reason=retry:worker-error", playbook_after_fail, "playbook should expose recent run outcomes with normalized reasons")


def test_corpus_hybrid_dedup(root: Path) -> None:
    dup_dir = root / "dup-src"
    dup_dir.mkdir(parents=True, exist_ok=True)
    dup_a = dup_dir / "same.txt"
    dup_b_dir = dup_dir / "other"
    dup_b_dir.mkdir(parents=True, exist_ok=True)
    dup_b = dup_b_dir / "same.txt"
    dup_a.write_text("first duplicate\n", encoding="utf-8")
    dup_b.write_text("second duplicate\n", encoding="utf-8")
    created = json_out(run("create", "--root", str(root), "--id", "task-hybrid", "--goal", "Self-test hybrid corpus path", "--corpus-mode", "hybrid"))
    assert_eq(created["corpus_mode"], "hybrid", "create should expose hybrid corpus mode")
    attached1 = json_out(run("attach-input", "--root", str(root), "--id", "task-hybrid", "--file", str(dup_a), "--file", str(dup_b)))
    assert_eq(attached1["corpus_mode"], "hybrid", "attach-input should preserve hybrid corpus mode")
    assert_eq(len(attached1["corpus_entries"]), 2, "attach-input should register both duplicate-named files")
    paths = {e["path"] for e in attached1["corpus_entries"]}
    assert_in("input/corpus/same.txt", paths, "duplicate corpus file names should be auto-renamed deterministically")
    assert_in("input/corpus/same-2.txt", paths, "duplicate corpus file names should be auto-renamed deterministically")
    attached2 = json_out(run("attach-input", "--root", str(root), "--id", "task-hybrid", "--file", str(dup_a)))
    assert_eq(len(attached2["corpus_entries"]), 3, "repeated attach should append a new uniquely named copy")
    lease = json_out(run("begin", "--root", str(root), "--id", "task-hybrid"))
    assert_eq(lease["corpus"]["mode"], "hybrid", "begin work order should expose hybrid mode")
    assert_true(any("hybrid" in item.lower() for item in lease["execution_guidance"]), "execution guidance should mention hybrid behavior")


def test_corpus_batch_dir(root: Path) -> None:
    batch_dir = root / "batch-src"
    (batch_dir / "nested").mkdir(parents=True, exist_ok=True)
    (batch_dir / "a.txt").write_text("batch file a\n", encoding="utf-8")
    (batch_dir / "nested" / "b.txt").write_text("batch file b\n", encoding="utf-8")
    run("create", "--root", str(root), "--id", "task-batch", "--goal", "Batch dir test", "--corpus-mode", "hybrid")
    attached = json_out(run("attach-input", "--root", str(root), "--id", "task-batch", "--dir", str(batch_dir), "--label", "batch", "--note", "recursive import"))
    assert_eq(len(attached["attached"]), 2, "attach-input --dir should attach all files from the directory recursively")
    paths = {e["path"] for e in attached["attached"]}
    assert_in("input/corpus/batch-src/a.txt", paths, "attach-input --dir should preserve directory structure under corpus")
    assert_in("input/corpus/batch-src/nested/b.txt", paths, "attach-input --dir should preserve directory structure under corpus")
    assert_true(all(e.get("label") == "batch" and e.get("note") == "recursive import" for e in attached["attached"]), "attach-input --dir should propagate label/note metadata to imported files")


def test_corpus_batch_dir_skips_symlink_files(root: Path) -> None:
    batch_dir = root / "batch-symlink-src"
    batch_dir.mkdir(parents=True, exist_ok=True)
    (batch_dir / "safe.txt").write_text("safe\n", encoding="utf-8")
    outside = root.parent / "outside-corpus-secret.txt"
    outside.write_text("secret\n", encoding="utf-8")
    os.symlink(outside, batch_dir / "secret-link.txt")

    run("create", "--root", str(root), "--id", "task-batch-symlink", "--goal", "Batch dir symlink test", "--corpus-mode", "local")
    attached = json_out(run("attach-input", "--root", str(root), "--id", "task-batch-symlink", "--dir", str(batch_dir)))

    paths = {e["path"] for e in attached["attached"]}
    assert_eq(len(attached["attached"]), 1, "attach-input --dir should attach only regular files")
    assert_in("input/corpus/batch-symlink-src/safe.txt", paths, "safe regular file should still be attached")
    assert_eq(len(attached.get("skipped") or []), 1, "attach-input --dir should report skipped symlink inputs")
    assert_in("symlink", attached["skipped"][0]["reason"], "skipped symlink should explain why it was ignored")
    assert_true(
        not (root / "task-batch-symlink" / "input" / "corpus" / "batch-symlink-src" / "secret-link.txt").exists(),
        "symlink target should not be copied into corpus",
    )


def test_corpus_glob(root: Path) -> None:
    glob_dir = root / "glob-src"
    (glob_dir / "nested").mkdir(parents=True, exist_ok=True)
    (glob_dir / "a.md").write_text("glob a\n", encoding="utf-8")
    (glob_dir / "nested" / "b.md").write_text("glob b\n", encoding="utf-8")
    (glob_dir / "nested" / "ignore.txt").write_text("ignore\n", encoding="utf-8")
    run("create", "--root", str(root), "--id", "task-glob", "--goal", "Controlled glob import", "--corpus-mode", "local")
    attached = json_out(run("attach-input", "--root", str(root), "--id", "task-glob", "--glob", str(glob_dir / "**" / "*.md"), "--label", "glob", "--note", "controlled import"))
    assert_eq(attached["corpus_mode"], "local", "attach-input --glob should preserve corpus mode")
    assert_eq(len(attached["attached"]), 2, "attach-input --glob should import only matching files")
    paths = {e["path"] for e in attached["attached"]}
    assert_in("input/corpus/glob-src/a.md", paths, "attach-input --glob should preserve anchor-relative structure")
    assert_in("input/corpus/glob-src/nested/b.md", paths, "attach-input --glob should preserve anchor-relative structure")
    assert_true(all(e.get("label") == "glob" and e.get("note") == "controlled import" for e in attached["attached"]), "attach-input --glob should propagate label/note metadata")


def test_corpus_glob_skips_symlink_files(root: Path) -> None:
    glob_dir = root / "glob-symlink-src"
    glob_dir.mkdir(parents=True, exist_ok=True)
    (glob_dir / "safe.md").write_text("safe\n", encoding="utf-8")
    outside = root.parent / "outside-glob-secret.md"
    outside.write_text("secret\n", encoding="utf-8")
    os.symlink(outside, glob_dir / "secret-link.md")

    run("create", "--root", str(root), "--id", "task-glob-symlink", "--goal", "Glob symlink test", "--corpus-mode", "local")
    attached = json_out(run("attach-input", "--root", str(root), "--id", "task-glob-symlink", "--glob", str(glob_dir / "**" / "*.md")))

    paths = {e["path"] for e in attached["attached"]}
    assert_eq(len(attached["attached"]), 1, "attach-input --glob should attach only regular files")
    assert_in("input/corpus/glob-symlink-src/safe.md", paths, "safe glob match should still be attached")
    assert_eq(len(attached.get("skipped") or []), 1, "attach-input --glob should report skipped symlink inputs")
    assert_in("symlink", attached["skipped"][0]["reason"], "skipped glob symlink should explain why it was ignored")


def test_fetch_url_as_markdown_allows_public_https_with_fake_transport(root: Path) -> None:
    class FakeHeaders:
        def get_content_type(self) -> str:
            return "text/html"

        def get_content_charset(self) -> str:
            return "utf-8"

    class FakeResponse:
        headers = FakeHeaders()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def read(self) -> bytes:
            return b"<html><head><title>Fixture article</title></head><body><p>First paragraph.</p></body></html>"

        def geturl(self) -> str:
            return "https://example.com/article.html"

    class FakeOpener:
        def open(self, request, timeout):
            return FakeResponse()

    original_build_opener = control_commands.urllib.request.build_opener
    original_socket = getattr(control_commands, "socket", None)
    original_getaddrinfo = socket.getaddrinfo
    try:
        control_commands.urllib.request.build_opener = lambda *handlers: FakeOpener()
        control_commands.socket = socket
        socket.getaddrinfo = lambda host, port, *args, **kwargs: [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", port))
        ]
        title, markdown = control_commands._fetch_url_as_markdown(
            "https://example.com/article.html",
            title=None,
            max_chars=20000,
            timeout_seconds=1,
        )
    finally:
        control_commands.urllib.request.build_opener = original_build_opener
        socket.getaddrinfo = original_getaddrinfo
        if original_socket is None:
            delattr(control_commands, "socket")
        else:
            control_commands.socket = original_socket

    assert_eq(title, "Fixture article", "fetch helper should derive title from public HTTPS HTML")
    assert_in("Source URL: https://example.com/article.html", markdown, "fetch helper should retain source URL")
    assert_in("First paragraph.", markdown, "fetch helper should include extracted body")


def test_corpus_url_as_md_rejects_loopback_http(root: Path) -> None:
    url_html = root / "url-source.html"
    url_html.write_text(
        '<html><head><title>Fixture article</title></head><body><p>Local paragraph.</p></body></html>',
        encoding="utf-8",
    )
    run("create", "--root", str(root), "--id", "task-url-loopback-reject", "--goal", "Reject loopback URL", "--corpus-mode", "local")
    with _FixtureHttpServer(root) as base_url:
        result = run(
            "attach-url-as-md",
            "--root",
            str(root),
            "--id",
            "task-url-loopback-reject",
            "--url",
            f"{base_url}/url-source.html",
            check=False,
        )

    assert_eq(result.returncode, 2, "attach-url-as-md should reject loopback HTTP URLs")
    assert_in("blocked local or private host", result.stderr.lower(), "loopback rejection should explain URL safety policy")


def test_fetch_url_as_markdown_rejects_redirect_to_loopback(root: Path) -> None:
    internal = root / "internal.html"
    internal.write_text(
        "<html><head><title>Internal</title></head><body>loopback secret</body></html>",
        encoding="utf-8",
    )

    original_getaddrinfo = socket.getaddrinfo
    original_opener = urllib.request._opener
    attacker_lookup_count = 0

    def patched_getaddrinfo(host: str, port: int, *args, **kwargs):
        nonlocal attacker_lookup_count
        if host == "attacker.test":
            attacker_lookup_count += 1
            if attacker_lookup_count == 1:
                return [
                    (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", port))
                ]
            return original_getaddrinfo("127.0.0.1", port, *args, **kwargs)
        return original_getaddrinfo(host, port, *args, **kwargs)

    try:
        original_build_opener = control_commands.urllib.request.build_opener

        def build_test_opener(*handlers):
            return original_build_opener(
                control_commands.urllib.request.ProxyHandler({}),
                *handlers,
            )

        control_commands.urllib.request.build_opener = build_test_opener
        urllib.request.install_opener(
            urllib.request.build_opener(urllib.request.ProxyHandler({}))
        )
        socket.getaddrinfo = patched_getaddrinfo
        with _FixtureHttpServer(root) as internal_base_url:
            with _RedirectHttpServer(f"{internal_base_url}/internal.html") as redirect_url:
                try:
                    control_commands._fetch_url_as_markdown(
                        f"{redirect_url}/start",
                        title=None,
                        max_chars=20000,
                        timeout_seconds=2,
                    )
                except control_commands.ValidationError as exc:
                    assert_in(
                        "blocked local or private host",
                        str(exc).lower(),
                        "redirect to loopback should explain URL safety policy",
                    )
                else:
                    raise AssertionError("redirect to loopback should be rejected")
    finally:
        socket.getaddrinfo = original_getaddrinfo
        control_commands.urllib.request.build_opener = original_build_opener
        urllib.request.install_opener(original_opener)


def test_corpus_url_as_md_rejects_local_file_scheme(root: Path) -> None:
    local_file = root / "local-secret.txt"
    local_file.write_text("should not be fetched through file url\n", encoding="utf-8")
    run("create", "--root", str(root), "--id", "task-url-file-reject", "--goal", "Reject local file URL", "--corpus-mode", "local")
    result = run(
        "attach-url-as-md",
        "--root",
        str(root),
        "--id",
        "task-url-file-reject",
        "--url",
        local_file.resolve().as_uri(),
        check=False,
    )
    assert_eq(result.returncode, 2, "attach-url-as-md should reject file:// URLs")
    assert_in("only supports http:// and https://", result.stderr, "attach-url-as-md should explain supported URL schemes")


def test_corpus_pdf(root: Path) -> None:
    pdf_source = root / "fixture.pdf"
    pdf_source.write_bytes(b"%PDF-1.4\n%fake fixture\n1 0 obj\n<<>>\nendobj\n")
    run("create", "--root", str(root), "--id", "task-pdf", "--goal", "Attach PDF fixture", "--corpus-mode", "local")
    attached = json_out(run("attach-pdf", "--root", str(root), "--id", "task-pdf", "--file", str(pdf_source), "--label", "pdf", "--note", "fixture pdf"))
    assert_eq(attached["corpus_mode"], "local", "attach-pdf should preserve corpus mode")
    assert_eq(len(attached["attached"]), 1, "attach-pdf should register one PDF entry")
    entry = attached["attached"][0]
    assert_true(entry["path"].endswith("fixture.pdf") and entry.get("content_hint") == "pdf", "attach-pdf should preserve pdf name and mark content_hint")
    lease = json_out(run("begin", "--root", str(root), "--id", "task-pdf"))
    assert_true(any(e.get("path") == entry["path"] and e.get("content_hint") == "pdf" and e.get("label") == "pdf" for e in lease["corpus"]["entries"]), "begin work order should expose attached pdf with metadata")


def test_corpus_image(root: Path) -> None:
    run("create", "--root", str(root), "--id", "task-image", "--goal", "Image attachment metadata", "--corpus-mode", "local")
    image_source = root / "fixture.png"
    image_source.write_bytes(b"\x89PNG\r\n\x1a\n" + b"selftest-image-payload")
    attached = json_out(run("attach-input", "--root", str(root), "--id", "task-image", "--file", str(image_source), "--label", "image", "--note", "fixture png"))
    assert_eq(attached["corpus_mode"], "local", "attach-input image should preserve corpus mode")
    entry = attached["attached"][0]
    assert_true(entry["path"].endswith("fixture.png") and entry.get("content_hint") == "image", "attach-input should mark image files with content_hint=image")
    lease = json_out(run("begin", "--root", str(root), "--id", "task-image"))
    assert_true(any(e.get("path") == entry["path"] and e.get("content_hint") == "image" and e.get("label") == "image" for e in lease["corpus"]["entries"]), "begin work order should expose attached image with metadata")


def test_corpus_legacy_compat(root: Path) -> None:
    run("create", "--root", str(root), "--id", "task-legacy", "--goal", "Legacy state compatibility")
    state_path = root / "task-legacy" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.pop("corpus", None)
    state.pop("completion", None)
    artifacts = state.get("artifacts") or {}
    artifacts.pop("task_playbook_path", None)
    artifacts.pop("runs_path", None)
    state["artifacts"] = artifacts
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    status = json_out(run("status", "--root", str(root), "--id", "task-legacy", "--format", "json"))
    assert_eq(status["status"], "idle", "legacy task status should still render")
    assert_eq(status["corpus"]["mode"], "web", "legacy state without corpus should default to web mode")
    summary = run("summary", "--root", str(root), "--id", "task-legacy", "--format", "text").stdout
    assert_in("Corpus: mode=web, files=0", summary, "legacy summary should render default corpus block")


def test_corpus_mode_override(root: Path) -> None:
    run("create", "--root", str(root), "--id", "task-corpus-web", "--goal", "Corpus mode override test")
    source = root / "corpus-web.txt"
    source.write_text("web to hybrid\n", encoding="utf-8")
    attached = json_out(run("attach-input", "--root", str(root), "--id", "task-corpus-web", "--file", str(source), "--corpus-mode", "hybrid"))
    assert_eq(attached["corpus_mode"], "hybrid", "attach-input should allow explicit corpus-mode override")
    status = json_out(run("status", "--root", str(root), "--id", "task-corpus-web", "--format", "json"))
    assert_eq(status["corpus"]["mode"], "hybrid", "status should reflect corpus-mode override")
