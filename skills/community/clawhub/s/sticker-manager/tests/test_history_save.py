import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
PY = sys.executable


def run_script(script_name, *args, env=None):
    cmd = [PY, str(SCRIPTS / script_name), *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def make_env(tmp_path):
    inbound = tmp_path / 'inbound'
    library = tmp_path / 'library'
    inbound.mkdir()
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    env['STICKER_MANAGER_INBOUND_DIR'] = str(inbound)
    return inbound, library, env


def test_list_history_shows_recent_media(tmp_path):
    inbound, _library, env = make_env(tmp_path)
    (inbound / 'older.gif').write_bytes(b'GIF89a' + b'a' * 50)
    (inbound / 'newer.gif').write_bytes(b'GIF89a' + b'b' * 60)
    result = run_script('save_sticker.py', '--lang=en', '--list-history', env=env)
    assert result.returncode == 0
    assert 'Recent media' in result.stdout
    assert 'older.gif' in result.stdout
    assert 'newer.gif' in result.stdout


def test_save_by_history_index(tmp_path):
    inbound, library, env = make_env(tmp_path)
    (inbound / 'first.gif').write_bytes(b'GIF89a' + b'a' * 50)
    (inbound / 'second.gif').write_bytes(b'GIF89a' + b'b' * 60)
    result = run_script('save_sticker.py', '--lang=en', '--history-index=2', 'from_history', env=env)
    assert result.returncode == 0
    assert (library / 'from_history.gif').exists()


def test_save_by_source_filename(tmp_path):
    inbound, library, env = make_env(tmp_path)
    (inbound / 'picked.gif').write_bytes(b'GIF89a' + b'c' * 80)
    result = run_script('save_sticker.py', '--lang=en', '--source=picked.gif', 'picked_saved', env=env)
    assert result.returncode == 0
    assert (library / 'picked_saved.gif').exists()


def test_save_history_empty_message(tmp_path):
    _inbound, _library, env = make_env(tmp_path)
    result = run_script('save_sticker.py', '--lang=zh', '--history-index=1', 'name', env=env)
    assert result.returncode == 1
    assert '历史媒体为空' in result.stdout


def test_save_auto_supports_history_index(tmp_path):
    inbound, library, env = make_env(tmp_path)
    first = inbound / 'first.gif'
    second = inbound / 'second.gif'
    first.write_bytes(b'GIF89a' + b'a' * 6000)
    second.write_bytes(b'GIF89a' + b'b' * 7000)

    now = time.time()
    os.utime(first, (now - 10, now - 10))
    os.utime(second, (now, now))

    result = run_script('save_sticker_auto.py', '--lang=en', '--history-index=2', 'history_auto', env=env)
    assert result.returncode == 0
    assert (library / 'history_auto.gif').exists()
