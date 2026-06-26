#!/usr/bin/env python3
"""Tests for relic capture hook."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from io import StringIO
from pathlib import Path

import pytest

# Add paths for imports
hooks_dir = str(Path(__file__).resolve().parents[1] / 'hooks')
scripts_dir = str(Path(__file__).resolve().parents[1] / 'scripts')
if hooks_dir not in sys.path:
    sys.path.insert(0, hooks_dir)
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# Import after path is set
import auto_capture
import capture_hook_mod as capture_hook
import distill_facets
import init_relic

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def temp_vault(monkeypatch: pytest.MonkeyPatch):
    """Create a temporary vault for testing."""
    temp_dir = tempfile.mkdtemp()
    vault_path = Path(temp_dir) / 'vault'
    vault_path.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(capture_hook, 'VAULT', vault_path)
    monkeypatch.setattr(capture_hook, 'INBOX', vault_path / 'inbox.ndjson')
    monkeypatch.setattr(capture_hook, 'MANIFEST', vault_path / 'manifest.json')
    monkeypatch.setattr(auto_capture, 'VAULT', vault_path)
    monkeypatch.setattr(auto_capture, 'INBOX', vault_path / 'inbox.ndjson')
    monkeypatch.setattr(auto_capture, 'MANIFEST', vault_path / 'manifest.json')
    monkeypatch.setattr(distill_facets, 'VAULT', vault_path)
    monkeypatch.setattr(distill_facets, 'INBOX', vault_path / 'inbox.ndjson')
    monkeypatch.setattr(distill_facets, 'FACETS', vault_path / 'facets.json')
    monkeypatch.setattr(distill_facets, 'SELF_MODEL', vault_path / 'self-model.md')
    monkeypatch.setattr(distill_facets, 'VOICE', vault_path / 'voice.md')
    monkeypatch.setattr(distill_facets, 'GOALS', vault_path / 'goals.md')
    monkeypatch.setattr(distill_facets, 'RELATIONSHIPS', vault_path / 'relationships.md')
    monkeypatch.setattr(distill_facets, 'MANIFEST', vault_path / 'manifest.json')
    monkeypatch.setattr(init_relic, 'VAULT', vault_path)

    yield vault_path

    shutil.rmtree(temp_dir, ignore_errors=True)


def run_auto_capture(monkeypatch: pytest.MonkeyPatch, payload: object) -> int:
    """Run auto_capture.main() with a mocked stdin payload."""
    stdin = StringIO(json.dumps(payload))
    monkeypatch.setattr(stdin, 'isatty', lambda: False)
    monkeypatch.setattr(sys, 'stdin', stdin)
    return auto_capture.main()


class TestCaptureHook:
    """Tests for capture_hook.py."""

    def test_capture_creates_record(self, temp_vault: Path):
        """Should capture observation via hook."""
        init_relic.init()

        result = capture_hook.main([
            '--text', 'I prefer dark mode',
            '--type', 'preference',
            '--confidence', '0.85',
        ])

        assert result == 0

        inbox = (temp_vault / 'inbox.ndjson').read_text()
        records = [json.loads(line) for line in inbox.strip().split('\n') if line]
        last = records[-1]

        assert last['text'] == 'I prefer dark mode'
        assert last['type'] == 'preference'
        assert last['source'] == 'conversation'
        assert 'hook' in last['meta']

    def test_capture_with_tags(self, temp_vault: Path):
        """Should capture tags via hook."""
        init_relic.init()

        result = capture_hook.main([
            '--text', 'I value simplicity',
            '--type', 'value',
            '--tags', 'design', 'minimalism',
        ])

        assert result == 0

        inbox = (temp_vault / 'inbox.ndjson').read_text()
        records = [json.loads(line) for line in inbox.strip().split('\n') if line]
        last = records[-1]

        assert 'design' in last['tags']
        assert 'minimalism' in last['tags']

    def test_skips_if_vault_not_initialized(self, monkeypatch: pytest.MonkeyPatch):
        """Should skip gracefully if vault doesn't exist."""
        missing_vault = Path('/tmp/nonexistent-relic-vault')
        monkeypatch.setattr(capture_hook, 'VAULT', missing_vault)

        result = capture_hook.main(['--text', 'Test'])

        assert result == 0

    def test_extract_observations_from_text(self):
        """Should extract observations using patterns."""
        text = 'I value clean code. I prefer dark mode. My goal is to ship fast.'
        observations = capture_hook.extract_observations_from_text(text)

        assert len(observations) >= 1

    def test_json_output(self, temp_vault: Path):
        """Should output valid JSON."""
        init_relic.init()

        result = subprocess.run([
            'python3', 'skill/relic/hooks/capture_hook_mod.py',
            '--text', 'Test output',
            '--type', 'reflection',
        ], capture_output=True, text=True, cwd='/Users/yexiaodong/.openclaw/workspace/projects/relic', env={**os.environ, 'RELIC_VAULT_PATH': str(temp_vault)})

        output = json.loads(result.stdout)
        assert output['status'] == 'success'
        assert output['captured'] >= 1

    def test_extracts_from_transcript_json(self, temp_vault: Path, monkeypatch: pytest.MonkeyPatch):
        """Should extract from the transcript field instead of the JSON wrapper."""
        init_relic.init()

        result = run_auto_capture(monkeypatch, {
            'transcript': 'I value durable systems. I prefer simple workflows. My goal is to ship relic.',
        })

        assert result == 0

        inbox = (temp_vault / 'inbox.ndjson').read_text()
        records = [json.loads(line) for line in inbox.strip().split('\n') if line]
        texts = [record['text'] for record in records]

        assert 'durable systems' in texts
        assert 'simple workflows' in texts
        assert 'ship relic' in texts

    def test_auto_capture_refreshes_self_model_after_successful_capture(self, temp_vault: Path, monkeypatch: pytest.MonkeyPatch):
        """Should automatically refresh derived model files after successful capture."""
        init_relic.init()

        before_self_model = (temp_vault / 'self-model.md').read_text(encoding='utf-8')

        result = run_auto_capture(monkeypatch, {
            'transcript': 'I value durable systems. I prefer concise answers. My goal is to keep relic working.',
        })

        assert result == 0

        self_model = (temp_vault / 'self-model.md').read_text(encoding='utf-8')
        facets = json.loads((temp_vault / 'facets.json').read_text(encoding='utf-8'))

        assert self_model != before_self_model
        assert 'durable systems' in self_model
        assert 'concise answers' in self_model
        assert 'keep relic working' in self_model
        assert 'durable systems' in facets['values']
        assert 'concise answers' in facets['preferences']
        assert 'keep relic working' in facets['goals']['active']

    def test_normalizes_untrusted_observation_fields(self):
        """Should clamp and normalize observation payloads before writing."""
        normalized = auto_capture.normalize_observation({
            'text': '  I value resilient systems.  ',
            'type': 'unknown',
            'tags': ['tag-a', '', 'tag-b'],
            'confidence': 5,
        })

        assert normalized is not None
        assert normalized['text'] == 'I value resilient systems.'
        assert normalized['type'] == 'reflection'
        assert normalized['tags'] == ['tag-a', 'tag-b']
        assert normalized['confidence'] == 1.0

    def test_persists_normalized_observation_payload(self, temp_vault: Path, monkeypatch: pytest.MonkeyPatch):
        """Should normalize direct observation payloads before writing them."""
        init_relic.init()

        result = run_auto_capture(monkeypatch, {
            'observations': [
                {
                    'text': '  I value resilient systems.  ',
                    'type': 'unknown',
                    'tags': ['tag-a', '', 'tag-b'],
                    'confidence': 5,
                }
            ]
        })

        assert result == 0

        inbox = (temp_vault / 'inbox.ndjson').read_text()
        records = [json.loads(line) for line in inbox.strip().split('\n') if line]
        last = records[-1]

        assert last['text'] == 'I value resilient systems.'
        assert last['type'] == 'reflection'
        assert last['tags'] == ['tag-a', 'tag-b']
        assert last['confidence'] == 1.0

    def test_skips_noisy_tool_transcript(self, temp_vault: Path, monkeypatch: pytest.MonkeyPatch):
        """Should ignore command output and permission-style transcript noise."""
        init_relic.init()

        result = run_auto_capture(monkeypatch, {
            'transcript': 'Exit code 1\nstdout: {}\nAllow this action?\ndangerouslyDisableSandbox\n/Users/yexiaodong/file.txt',
        })

        assert result == 0
        inbox = (temp_vault / 'inbox.ndjson').read_text()
        assert inbox == ''

    def test_noisy_transcript_does_not_refresh_self_model(self, temp_vault: Path, monkeypatch: pytest.MonkeyPatch):
        """Should leave derived model files untouched when nothing is captured."""
        init_relic.init()

        before_self_model = (temp_vault / 'self-model.md').read_text(encoding='utf-8')
        before_manifest = json.loads((temp_vault / 'manifest.json').read_text(encoding='utf-8'))
        before_facets = (temp_vault / 'facets.json').read_text(encoding='utf-8')

        result = run_auto_capture(monkeypatch, {
            'transcript': 'Exit code 1\nstdout: {}\nAllow this action?\ndangerouslyDisableSandbox\n/Users/yexiaodong/file.txt',
        })

        assert result == 0
        after_self_model = (temp_vault / 'self-model.md').read_text(encoding='utf-8')
        after_manifest = json.loads((temp_vault / 'manifest.json').read_text(encoding='utf-8'))
        after_facets = (temp_vault / 'facets.json').read_text(encoding='utf-8')

        assert after_self_model == before_self_model
        assert after_manifest['updatedAt'] == before_manifest['updatedAt']
        assert after_facets == before_facets

    def test_filters_noise_and_keeps_first_person_signal(self, temp_vault: Path, monkeypatch: pytest.MonkeyPatch):
        """Should keep durable first-person statements while dropping adjacent noise."""
        init_relic.init()

        result = run_auto_capture(monkeypatch, {
            'transcript': 'Allow this action?\nExit code 0\nI value reliable local tools.\nstdout: ignored\nI prefer concise answers.',
        })

        assert result == 0

        inbox = (temp_vault / 'inbox.ndjson').read_text()
        records = [json.loads(line) for line in inbox.strip().split('\n') if line]
        texts = [record['text'] for record in records]

        assert 'reliable local tools' in texts
        assert 'concise answers' in texts
        assert all('exit code' not in text for text in texts)
        assert all('allow this action' not in text for text in texts)


class TestHookPackaging:
    """Tests for bundled OpenClaw hook packaging."""

    def test_bundled_hook_runtime_files_exist(self):
        """Package should ship the required hook runtime assets."""
        assert (PACKAGE_ROOT / 'hooks' / 'auto_capture.py').exists()
        assert (PACKAGE_ROOT / 'hooks' / 'openclaw' / 'HOOK.md').exists()
        assert (PACKAGE_ROOT / 'hooks' / 'openclaw' / 'handler.ts').exists()
        assert (PACKAGE_ROOT / 'hooks' / 'openclaw' / 'handler.js').exists()

    def test_hook_setup_docs_exist(self):
        """Package should document optional hook installation and verification."""
        assert (PACKAGE_ROOT / 'hooks' / 'hooks-config.md').exists()
        assert (PACKAGE_ROOT / 'references' / 'hooks-setup.md').exists()

    def test_auto_capture_uses_shared_vault_path_contract(self):
        """Python hook should resolve vault path through the shared helper."""
        source = (PACKAGE_ROOT / 'hooks' / 'auto_capture.py').read_text(encoding='utf-8')

        assert 'from vault_paths import get_vault_path' in source
        assert "VAULT = get_vault_path()" in source
        assert '/Users/yexiaodong/.openclaw/workspace/projects/relic/vault' not in source

    def test_hook_handlers_use_home_based_default_and_env_override(self):
        """Bundled JS/TS handlers should use HOME-based default path and RELIC_VAULT_PATH override."""
        handler_ts = (PACKAGE_ROOT / 'hooks' / 'openclaw' / 'handler.ts').read_text(encoding='utf-8')
        handler_js = (PACKAGE_ROOT / 'hooks' / 'openclaw' / 'handler.js').read_text(encoding='utf-8')

        for source in (handler_ts, handler_js):
            assert 'RELIC_VAULT_PATH' in source
            assert '.openclaw' in source
            assert 'projects' in source
            assert 'relic' in source
            assert '/Users/yexiaodong/.openclaw/workspace/projects/relic/vault' not in source


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
