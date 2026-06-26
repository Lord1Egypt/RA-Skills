import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
PY = sys.executable


def run_script(script_name, *args, env=None):
    cmd = [PY, str(SCRIPTS / script_name), *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def test_get_sticker_outputs_zh_for_missing_library(tmp_path):
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(tmp_path / 'missing-lib')
    result = run_script('get_sticker.py', '--lang=zh', 'keyword', env=env)
    assert result.returncode == 1
    assert '表情包目录不存在' in result.stdout


def test_get_sticker_outputs_en_for_missing_library(tmp_path):
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(tmp_path / 'missing-lib')
    result = run_script('get_sticker.py', '--lang=en', 'keyword', env=env)
    assert result.returncode == 1
    assert 'Sticker library not found' in result.stdout


def test_get_sticker_exact_match(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'exact_name.gif').write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    result = run_script('get_sticker.py', '--lang=en', 'exact_name', env=env)
    assert result.returncode == 0
    assert str(library / 'exact_name.gif') in result.stdout


def test_get_sticker_partial_match(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'calm_approval.gif').write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    result = run_script('get_sticker.py', '--lang=en', 'approval', env=env)
    assert result.returncode == 0
    assert str(library / 'calm_approval.gif') in result.stdout


def test_get_sticker_lists_inventory_in_english(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'one.gif').write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    result = run_script('get_sticker.py', '--lang=en', env=env)
    assert result.returncode == 0
    assert 'Sticker library' in result.stdout
    assert 'one.gif' in result.stdout


def test_save_sticker_saves_latest_file(tmp_path):
    inbound = tmp_path / 'inbound'
    library = tmp_path / 'library'
    inbound.mkdir()
    sample = inbound / 'sample.gif'
    sample.write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    env['STICKER_MANAGER_INBOUND_DIR'] = str(inbound)
    result = run_script('save_sticker.py', '--lang=en', 'saved_name', env=env)
    assert result.returncode == 0
    assert (library / 'saved_name.gif').exists()
    assert 'Saved:' in result.stdout


def test_save_sticker_outputs_chinese(tmp_path):
    inbound = tmp_path / 'inbound'
    library = tmp_path / 'library'
    inbound.mkdir()
    sample = inbound / 'sample.gif'
    sample.write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    env['STICKER_MANAGER_INBOUND_DIR'] = str(inbound)
    result = run_script('save_sticker.py', '--lang=zh', '中文名', env=env)
    assert result.returncode == 0
    assert '已保存:' in result.stdout


def test_save_sticker_help_exits_without_writing(tmp_path):
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(tmp_path / 'library')
    env['STICKER_MANAGER_INBOUND_DIR'] = str(tmp_path / 'inbound')
    result = run_script('save_sticker.py', '--help', env=env)
    assert result.returncode == 0
    assert 'Usage:' in result.stdout
    assert not (tmp_path / 'library').exists()


def test_save_sticker_auto_returns_need_analysis(tmp_path):
    inbound = tmp_path / 'inbound'
    library = tmp_path / 'library'
    inbound.mkdir()
    (inbound / 'sample.gif').write_bytes(b'GIF89a' + b'x' * 6000)
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    env['STICKER_MANAGER_INBOUND_DIR'] = str(inbound)
    result = run_script('save_sticker_auto.py', '--lang=en', env=env)
    assert result.returncode == 2
    assert '__ANALYZE__:' in result.stdout
    assert '__QUALITY__:' in result.stdout


def test_save_sticker_auto_help_exits_without_writing(tmp_path):
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(tmp_path / 'library')
    env['STICKER_MANAGER_INBOUND_DIR'] = str(tmp_path / 'inbound')
    result = run_script('save_sticker_auto.py', '--help', env=env)
    assert result.returncode == 0
    assert 'Usage:' in result.stdout
    assert not (tmp_path / 'library').exists()


def test_save_sticker_auto_rejects_low_quality_without_force(tmp_path):
    inbound = tmp_path / 'inbound'
    library = tmp_path / 'library'
    inbound.mkdir()
    (inbound / 'tiny.gif').write_bytes(b'GIF89a' + b'x' * 100)
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    env['STICKER_MANAGER_INBOUND_DIR'] = str(inbound)
    result = run_script('save_sticker_auto.py', '--lang=en', 'low_quality', env=env)
    assert result.returncode == 1
    assert 'quality is too low' in result.stdout


def test_save_sticker_auto_force_saves_low_quality(tmp_path):
    inbound = tmp_path / 'inbound'
    library = tmp_path / 'library'
    inbound.mkdir()
    (inbound / 'tiny.gif').write_bytes(b'GIF89a' + b'x' * 100)
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    env['STICKER_MANAGER_INBOUND_DIR'] = str(inbound)
    result = run_script('save_sticker_auto.py', '--lang=en', 'forced', '--force', env=env)
    assert result.returncode == 0
    assert (library / 'forced.gif').exists()


def test_manage_sticker_rename_and_delete(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    sticker = library / 'hello.gif'
    sticker.write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)

    rename_result = run_script('manage_sticker.py', '--lang=en', 'rename', 'hello', 'world', env=env)
    assert rename_result.returncode == 0
    assert (library / 'world.gif').exists()

    delete_result = run_script('manage_sticker.py', '--lang=en', 'delete', 'world', env=env)
    assert delete_result.returncode == 0
    assert not (library / 'world.gif').exists()


def test_manage_clean_removes_low_quality_files(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'tiny.gif').write_bytes(b'GIF89a' + b'x' * 10)
    (library / 'ok.gif').write_bytes(b'GIF89a' + b'x' * 5000)
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    result = run_script('manage_sticker.py', '--lang=en', 'clean', env=env)
    assert result.returncode == 0
    assert 'Removed 1 low-quality stickers' in result.stdout
    assert not (library / 'tiny.gif').exists()
    assert (library / 'ok.gif').exists()


def test_manage_clean_outputs_chinese_when_no_files_removed(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'ok.gif').write_bytes(b'GIF89a' + b'x' * 5000)
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    result = run_script('manage_sticker.py', '--lang=zh', 'clean', env=env)
    assert result.returncode == 0
    assert '没有低质量表情包需要清理' in result.stdout


def test_semantic_prepare_model_payload(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'sample.gif').write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)

    tag_result = run_script(
        'sticker_semantic.py',
        '--lang=en',
        'tag',
        'sample',
        'happy,calm',
        'meeting,success',
        'approval,done',
        'A calm approval reaction image.',
        env=env,
    )
    assert tag_result.returncode == 0

    payload_result = run_script('sticker_semantic.py', 'prepare-model', 'we fixed it', env=env)
    assert payload_result.returncode == 0
    payload = json.loads(payload_result.stdout)
    assert payload['context'] == 'we fixed it'
    assert payload['candidates'][0]['description'] == 'A calm approval reaction image.'


def test_semantic_model_strategy_outputs_model_payload(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'sample.gif').write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    run_script(
        'sticker_semantic.py',
        'tag',
        'sample',
        'happy,calm',
        'meeting,success',
        'approval,done',
        'A calm approval reaction image.',
        env=env,
    )
    result = run_script('sticker_semantic.py', '--lang=en', 'suggest', 'we finally fixed it', '--strategy=model', env=env)
    assert result.returncode == 0
    assert '__MODEL_MATCH__:' in result.stdout


def test_semantic_rules_fallback_returns_path(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'sample.gif').write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    run_script(
        'sticker_semantic.py',
        'tag',
        'sample',
        'happy,calm',
        'meeting,success',
        'approval,done',
        'A calm approval reaction image.',
        env=env,
    )
    result = run_script('sticker_semantic.py', '--lang=en', 'suggest', 'approval done', env=env)
    assert result.returncode == 0
    assert str(library / 'sample.gif') in result.stdout


def test_semantic_list_outputs_description(tmp_path):
    library = tmp_path / 'library'
    library.mkdir()
    (library / 'sample.gif').write_bytes(b'GIF89a-test-data')
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    run_script(
        'sticker_semantic.py',
        '--lang=zh',
        'tag',
        'sample',
        'happy,calm',
        'meeting,success',
        'approval,done',
        '一张平静认可的反应图。',
        env=env,
    )
    result = run_script('sticker_semantic.py', '--lang=zh', 'list', env=env)
    assert result.returncode == 0
    assert '表情包标签库' in result.stdout
    assert '一张平静认可的反应图。' in result.stdout
