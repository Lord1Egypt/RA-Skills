"""Tests for discover_sources.py."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
PY = sys.executable

sys.path.insert(0, str(SCRIPTS))

import discover_sources


def run_script(*args):
    cmd = [PY, str(SCRIPTS / 'discover_sources.py'), *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def extract_json_payload(stdout: str) -> dict:
    return json.loads(stdout[stdout.index('{'):])


def test_discover_url_without_fetch_keeps_pending_status():
    result = run_script('--lang=en', 'https://example.com/test.gif')

    assert result.returncode == 0
    payload = extract_json_payload(result.stdout)
    assert payload['total'] == 1
    assert payload['urls'][0]['status'] == 'pending'


def test_discover_page_error_is_not_reported_as_success(tmp_path):
    result = discover_sources.discover_from_pages(['https://example.invalid/gallery'], 'en')

    assert result == []
