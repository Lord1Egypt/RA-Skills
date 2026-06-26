import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
PY = sys.executable
sys.path.insert(0, str(SCRIPTS))
import collect_stickers


def run_collect(*args):
    cmd = [PY, str(SCRIPTS / 'collect_stickers.py'), *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_collect_single_thread_and_trim_to_target(tmp_path):
    sources = []
    for idx in range(5):
        path = tmp_path / f'source_{idx}.gif'
        path.write_bytes(b'GIF89a' + bytes([idx]) * (12000 + idx))
        sources.append(str(path))
    out_dir = tmp_path / 'out'
    result = run_collect(*sources, '--out-dir', str(out_dir), '--prefix', '测试', '--target-count', '3', '--workers', '4')
    assert result.returncode == 0
    assert 'EFFECTIVE_WORKERS=1' in result.stdout
    assert 'WORKERS_IGNORED=4' in result.stdout
    assert 'FINAL_COUNT=3' in result.stdout
    kept = list(out_dir.iterdir())
    assert len(kept) == 3


def test_collect_dedupes_and_reports_need_more(tmp_path):
    a = tmp_path / 'a.gif'
    b = tmp_path / 'b.gif'
    c = tmp_path / 'c.gif'
    a.write_bytes(b'GIF89a' + b'x' * 12000)
    b.write_bytes(b'GIF89a' + b'x' * 12000)
    c.write_bytes(b'GIF89a' + b'y' * 500)  # low quality
    out_dir = tmp_path / 'out'
    result = run_collect(str(a), str(b), str(c), '--out-dir', str(out_dir), '--prefix', '测试', '--target-count', '2')
    assert result.returncode == 2
    assert 'DUPLICATES=1' in result.stdout
    assert 'LOW_QUALITY=1' in result.stdout
    assert 'NEED_MORE=1' in result.stdout


def test_collect_can_disable_semantic_plan(tmp_path):
    source = tmp_path / 'single.gif'
    source.write_bytes(b'GIF89a' + b'z' * 15000)
    out_dir = tmp_path / 'out'
    result = run_collect(str(source), '--out-dir', str(out_dir), '--prefix', '测试', '--target-count', '1', '--no-semantic-plan')
    assert result.returncode == 0
    assert '__SEMANTIC_BATCH__:' not in result.stdout


def test_resolve_remote_source_prefers_giphy_gif(monkeypatch):
    page_url = 'https://giphy.com/gifs/example-crab-abc123'
    gif_url = 'https://media1.giphy.com/media/abc123/giphy.gif'
    webp_url = 'https://media1.giphy.com/media/abc123/giphy.webp'

    class Resp:
        status_code = 200
        text = f'<html><body>{webp_url} {gif_url}</body></html>'

        def raise_for_status(self):
            return None

    def fake_get(url, headers=None, timeout=30):
        assert url == page_url
        return Resp()

    monkeypatch.setattr(collect_stickers.requests, 'get', fake_get)
    resolved, forced_ext, meta = collect_stickers.resolve_remote_source(page_url)
    assert resolved == gif_url
    assert forced_ext == '.gif'
    assert meta['animated_preferred'] is True
    assert meta['resolver'] == 'giphy-page'


def test_collect_one_keeps_gif_extension_for_animated_remote(monkeypatch, tmp_path):
    gif_bytes = (b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x00\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;') * 300
    gif_url = 'https://media1.giphy.com/media/abc123/giphy.gif'
    page_url = 'https://giphy.com/gifs/example-crab-abc123'

    class Resp:
        def __init__(self, url):
            self.url = url
            self.status_code = 200
            if url == page_url:
                self.text = gif_url
                self.content = b''
                self.headers = {'Content-Type': 'text/html'}
            else:
                self.text = ''
                self.content = gif_bytes
                self.headers = {'Content-Type': 'image/gif'}

        def raise_for_status(self):
            return None

    def fake_get(url, headers=None, timeout=30):
        return Resp(url)

    monkeypatch.setattr(collect_stickers.requests, 'get', fake_get)
    result = collect_stickers.collect_one((1, page_url), 'crab', tmp_path, 10 * 1024)
    assert result['status'] == 'saved'
    assert result['name'].endswith('.gif')
    assert Path(result['path']).read_bytes().startswith(b'GIF89a')
    assert result['animated_preferred'] is True


def test_collect_rejects_static_fallback_when_reference_looks_animated(monkeypatch, tmp_path):
    page_url = 'https://example.com/crab.gif'
    static_webp = b'RIFF' + (20).to_bytes(4, 'little') + b'WEBPVP8 ' + b'x' * 64

    class Resp:
        status_code = 200
        text = ''
        content = static_webp
        headers = {'Content-Type': 'image/webp'}

        def raise_for_status(self):
            return None

    def fake_get(url, headers=None, timeout=30):
        return Resp()

    monkeypatch.setattr(collect_stickers.requests, 'get', fake_get)
    result = collect_stickers.collect_one((1, page_url), 'crab', tmp_path, 1)
    assert result['status'] == 'static_fallback_rejected'
    assert result['animation_reference'] is True
    assert result['animated_detected'] is False
