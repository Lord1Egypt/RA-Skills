import json
import os
import subprocess
import sys
from pathlib import Path

from common import get_vision_models, build_vision_plan, t

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
PY = sys.executable


def run_script(script_name, *args, env=None):
    cmd = [PY, str(SCRIPTS / script_name), *args]
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def test_default_vision_models_present(monkeypatch):
    monkeypatch.delenv('STICKER_MANAGER_VISION_MODELS', raising=False)
    models = get_vision_models()
    assert 'bailian/kimi-k2.5' in models
    assert 'openai/gpt-5-mini' in models


def test_custom_vision_models_from_env(monkeypatch):
    monkeypatch.setenv('STICKER_MANAGER_VISION_MODELS', 'model-a, model-b')
    assert get_vision_models() == ['model-a', 'model-b']


def test_build_vision_plan_contains_fallback_message(monkeypatch):
    monkeypatch.setenv('STICKER_MANAGER_VISION_MODELS', 'model-a,model-b')
    plan = build_vision_plan('/tmp/demo.png', 'need doubt detection', 'zh')
    assert plan['image_path'] == '/tmp/demo.png'
    assert plan['models'] == ['model-a', 'model-b']
    assert '未能成功识别图片语义' in plan['fallback_message']


def test_vision_failure_message_english(monkeypatch):
    monkeypatch.setenv('STICKER_MANAGER_VISION_MODELS', 'model-a,model-b')
    msg = t('vision_failure', 'en', models='model-a, model-b')
    assert 'Failed to interpret the image semantically' in msg


def test_semantic_vision_plan_cli_outputs_json(tmp_path):
    image_path = tmp_path / 'demo.png'
    image_path.write_bytes(b'not-really-an-image')
    env = os.environ.copy()
    env['STICKER_MANAGER_VISION_MODELS'] = 'model-a,model-b'
    result = run_script('sticker_semantic.py', '--lang=en', 'vision-plan', str(image_path), 'find doubt emotion', env=env)
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload['image_path'] == str(image_path)
    assert payload['models'] == ['model-a', 'model-b']
    assert 'fallback_message' in payload
