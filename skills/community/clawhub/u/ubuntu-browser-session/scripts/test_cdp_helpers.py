#!/usr/bin/env python3
import json
import re
import socket
import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CDP_EVAL = BASE_DIR / 'cdp-eval.py'
CDP_SNAPSHOT = BASE_DIR / 'cdp-snapshot.py'

HTML = '''<!doctype html>
<html>
  <head><title>Forum Example</title></head>
  <body>
    <nav>
      <a href="/latest">Latest</a>
      <a href="/categories">Categories</a>
      <a href="https://forum.example/hidden-topic" style="display:none">Second Topic</a>
    </nav>
    <main role="main">
      <div class="result-card" data-topic-id="101">
        <h2><a href="https://forum.example/questions/101">First Topic</a></h2>
        <p>Snippet one</p>
      </div>
      <div class="result-card" data-topic-id="102">
        <h2><a href="https://forum.example/questions/102">Second Topic</a></h2>
        <p>Snippet two</p>
      </div>
    </main>
  </body>
</html>'''


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def pick_free_port() -> int:
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return int(sock.getsockname()[1])


def runtime_port(run_dir: Path) -> int:
    status = run(str(BASE_DIR / 'browser-runtime.sh'), 'status', '--run-dir', str(run_dir))
    match = re.search(r'^cdp_port: (\d+)$', status, re.MULTILINE)
    assert match, status
    return int(match.group(1))


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        html_path = Path(td) / 'index.html'
        html_path.write_text(HTML, encoding='utf-8')
        profile_dir = Path(td) / 'profile'
        run_dir = Path(td) / 'run'
        requested_port = pick_free_port()

        subprocess.check_call([
            str(BASE_DIR / 'browser-runtime.sh'), 'start',
            '--url', html_path.as_uri(),
            '--origin', 'https://forum.example',
            '--profile-dir', str(profile_dir),
            '--run-dir', str(run_dir),
            '--mode', 'headless',
            '--session-key', 'test',
            '--cdp-port', str(requested_port),
        ])
        try:
            port = runtime_port(run_dir)
            assert port == requested_port, port

            snapshot_raw = run('python3', str(CDP_SNAPSHOT), '--port', str(port), '--format', 'topic-links')
            snapshot = json.loads(snapshot_raw)
            links = json.loads(snapshot['content'])
            assert len(links) == 2, links
            assert links[0]['text'] == 'First Topic', links
            assert links[0]['href'] == 'https://forum.example/questions/101', links
            assert links[0]['topicId'] == '101', links
            assert 'Snippet one' in links[0]['meta'], links

            click_raw = run('python3', str(CDP_EVAL), '--port', str(port), '--click-link-text', 'Second Topic')
            click = json.loads(click_raw)
            assert click['clicked'] is True, click
            assert click['href'] == 'https://forum.example/questions/102', click
        finally:
            subprocess.call([
                str(BASE_DIR / 'browser-runtime.sh'), 'stop',
                '--run-dir', str(run_dir),
            ])
    print('ok')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
