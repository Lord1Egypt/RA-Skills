#!/usr/bin/env python3
"""Tests for relic scripts."""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pytest

# Import scripts
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import apply_proposal
import capture_note
import distill_facets
import init_relic
import propose_update
import render_export
import vault_paths

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def temp_vault(monkeypatch: pytest.MonkeyPatch):
    """Create a temporary vault directory for testing."""
    temp_dir = tempfile.mkdtemp()
    vault_path = Path(temp_dir) / 'vault'
    vault_path.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(init_relic, 'VAULT', vault_path)
    monkeypatch.setattr(capture_note, 'VAULT', vault_path)
    monkeypatch.setattr(distill_facets, 'VAULT', vault_path)
    monkeypatch.setattr(propose_update, 'VAULT', vault_path)
    monkeypatch.setattr(apply_proposal, 'VAULT', vault_path)
    monkeypatch.setattr(render_export, 'VAULT', vault_path)

    monkeypatch.setattr(capture_note, 'INBOX', vault_path / 'inbox.ndjson')
    monkeypatch.setattr(capture_note, 'MANIFEST', vault_path / 'manifest.json')
    monkeypatch.setattr(distill_facets, 'INBOX', vault_path / 'inbox.ndjson')
    monkeypatch.setattr(distill_facets, 'FACETS', vault_path / 'facets.json')
    monkeypatch.setattr(distill_facets, 'SELF_MODEL', vault_path / 'self-model.md')
    monkeypatch.setattr(distill_facets, 'VOICE', vault_path / 'voice.md')
    monkeypatch.setattr(distill_facets, 'GOALS', vault_path / 'goals.md')
    monkeypatch.setattr(distill_facets, 'RELATIONSHIPS', vault_path / 'relationships.md')
    monkeypatch.setattr(distill_facets, 'MANIFEST', vault_path / 'manifest.json')
    monkeypatch.setattr(propose_update, 'FACETS', vault_path / 'facets.json')
    monkeypatch.setattr(propose_update, 'SELF_MODEL', vault_path / 'self-model.md')
    monkeypatch.setattr(propose_update, 'PROPOSALS', vault_path / 'evolution' / 'proposals')
    monkeypatch.setattr(apply_proposal, 'PROPOSALS', vault_path / 'evolution' / 'proposals')
    monkeypatch.setattr(apply_proposal, 'ACCEPTED', vault_path / 'evolution' / 'accepted')
    monkeypatch.setattr(apply_proposal, 'SNAPSHOTS', vault_path / 'snapshots')
    monkeypatch.setattr(apply_proposal, 'SELF_MODEL', vault_path / 'self-model.md')
    monkeypatch.setattr(apply_proposal, 'FACETS', vault_path / 'facets.json')
    monkeypatch.setattr(render_export, 'FACETS', vault_path / 'facets.json')
    monkeypatch.setattr(render_export, 'SELF_MODEL', vault_path / 'self-model.md')
    monkeypatch.setattr(render_export, 'VOICE', vault_path / 'voice.md')
    monkeypatch.setattr(render_export, 'GOALS', vault_path / 'goals.md')
    monkeypatch.setattr(render_export, 'OUT', vault_path / 'exports' / 'agent-prompt.md')

    yield vault_path

    shutil.rmtree(temp_dir, ignore_errors=True)


class TestInitRelic:
    """Tests for init_relic.py."""

    def test_init_creates_vault_structure(self, temp_vault: Path):
        """Should create all required directories and files."""
        init_relic.init()

        assert temp_vault.exists()
        assert (temp_vault / 'manifest.json').exists()
        assert (temp_vault / 'inbox.ndjson').exists()
        assert (temp_vault / 'facets.json').exists()
        assert (temp_vault / 'self-model.md').exists()
        assert (temp_vault / 'voice.md').exists()
        assert (temp_vault / 'goals.md').exists()
        assert (temp_vault / 'relationships.md').exists()
        assert (temp_vault / 'evolution' / 'proposals').exists()
        assert (temp_vault / 'evolution' / 'accepted').exists()
        assert (temp_vault / 'evolution' / 'rejected').exists()
        assert (temp_vault / 'snapshots').exists()
        assert (temp_vault / 'exports').exists()

    def test_init_manifest_valid_json(self, temp_vault: Path):
        """Manifest should be valid JSON with required fields."""
        init_relic.init()

        manifest = json.loads((temp_vault / 'manifest.json').read_text())
        assert manifest['name'] == 'relic'
        assert 'createdAt' in manifest
        assert 'updatedAt' in manifest
        assert manifest['mode'] == 'local-first'

    def test_init_preserves_existing_files(self, temp_vault: Path):
        """Should not overwrite existing vault files on re-run."""
        init_relic.init()

        manifest_path = temp_vault / 'manifest.json'
        self_model_path = temp_vault / 'self-model.md'
        facets_path = temp_vault / 'facets.json'

        original_manifest = manifest_path.read_text()
        self_model_path.write_text('# Custom self model\n', encoding='utf-8')
        facets_path.write_text('{"preferences": ["custom"]}\n', encoding='utf-8')

        init_relic.init()

        assert manifest_path.read_text() == original_manifest
        assert self_model_path.read_text(encoding='utf-8') == '# Custom self model\n'
        assert facets_path.read_text(encoding='utf-8') == '{"preferences": ["custom"]}\n'

    def test_init_backfills_missing_files_only(self, temp_vault: Path):
        """Should create missing files without touching existing ones."""
        init_relic.init()

        voice_path = temp_vault / 'voice.md'
        goals_path = temp_vault / 'goals.md'
        voice_path.write_text('# Custom voice\n', encoding='utf-8')
        goals_path.unlink()

        init_relic.init()

        assert voice_path.read_text(encoding='utf-8') == '# Custom voice\n'
        assert goals_path.exists()


class TestCaptureNote:
    """Tests for capture_note.py."""

    def test_capture_creates_record(self, temp_vault: Path):
        """Should create a valid observation record."""
        init_relic.init()

        record = capture_note.capture(
            text='Test observation',
            obs_type='preference',
            confidence=0.9,
        )

        assert record['text'] == 'Test observation'
        assert record['type'] == 'preference'
        assert record['confidence'] == 0.9
        assert 'id' in record
        assert 'ts' in record

    def test_capture_with_tags(self, temp_vault: Path):
        """Should capture tags correctly."""
        init_relic.init()

        record = capture_note.capture(
            text='Test with tags',
            obs_type='value',
            tags=['test1', 'test2'],
            confidence=0.85,
        )

        assert 'test1' in record['tags']
        assert 'test2' in record['tags']

    def test_capture_updates_manifest(self, temp_vault: Path):
        """Should update manifest updatedAt timestamp."""
        init_relic.init()

        manifest_before = json.loads((temp_vault / 'manifest.json').read_text())
        ts_before = manifest_before['updatedAt']

        capture_note.capture(text='Another test', obs_type='goal')

        manifest_after = json.loads((temp_vault / 'manifest.json').read_text())
        ts_after = manifest_after['updatedAt']

        assert ts_before
        assert ts_after
        assert ts_after != ts_before

    def test_capture_append_only(self, temp_vault: Path):
        """Should append to inbox, not overwrite."""
        init_relic.init()

        capture_note.capture(text='First observation', obs_type='reflection')
        capture_note.capture(text='Second observation', obs_type='reflection')

        inbox = (temp_vault / 'inbox.ndjson').read_text()
        records = [json.loads(line) for line in inbox.strip().split('\n') if line]

        assert len(records) >= 2
        assert records[0]['text'] == 'First observation'
        assert records[1]['text'] == 'Second observation'

    def test_capture_rejects_empty_text(self, temp_vault: Path):
        """Should reject empty observation text."""
        init_relic.init()

        with pytest.raises(ValueError, match='text must be a non-empty string'):
            capture_note.capture(text='   ', obs_type='value')

    def test_capture_rejects_unknown_type(self, temp_vault: Path):
        """Should reject unsupported observation types."""
        init_relic.init()

        with pytest.raises(ValueError, match='obs_type must be one of'):
            capture_note.capture(text='Test observation', obs_type='fact')

    def test_capture_rejects_invalid_tags(self, temp_vault: Path):
        """Should reject malformed tag collections."""
        init_relic.init()

        with pytest.raises(ValueError, match='tags must be a list of non-empty strings'):
            capture_note.capture(text='Tagged observation', obs_type='value', tags=['ok', ''])

    def test_capture_accepts_boundary_confidence_values(self, temp_vault: Path):
        """Should accept 0.0 and 1.0 confidence values."""
        init_relic.init()

        low = capture_note.capture(text='Low confidence note', obs_type='reflection', confidence=0.0)
        high = capture_note.capture(text='High confidence note', obs_type='reflection', confidence=1.0)

        assert low['confidence'] == 0.0
        assert high['confidence'] == 1.0

    def test_capture_repairs_invalid_manifest(self, temp_vault: Path):
        """Should recover from malformed manifest JSON and still capture."""
        init_relic.init()
        (temp_vault / 'manifest.json').write_text('{invalid json', encoding='utf-8')

        record = capture_note.capture(text='Recovered capture', obs_type='value', confidence=0.8)
        manifest = json.loads((temp_vault / 'manifest.json').read_text(encoding='utf-8'))

        assert record['text'] == 'Recovered capture'
        assert manifest['name'] == 'relic'
        assert 'updatedAt' in manifest

    def test_capture_rejects_invalid_confidence(self, temp_vault: Path):
        """Should reject confidence values outside the supported range."""
        init_relic.init()

        with pytest.raises(ValueError, match='confidence must be between 0 and 1'):
            capture_note.capture(text='Test observation', obs_type='value', confidence=1.5)

        with pytest.raises(ValueError, match='confidence must be between 0 and 1'):
            capture_note.capture(text='Test observation', obs_type='value', confidence=-0.1)


class TestDistillFacets:
    """Tests for distill_facets.py."""

    def test_distill_creates_facets(self, temp_vault: Path):
        """Should create facets.json from observations."""
        init_relic.init()
        capture_note.capture(text='Prefers clean code', obs_type='preference')
        capture_note.capture(text='Values testing', obs_type='value')

        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text())
        assert len(facets['preferences']) >= 1
        assert len(facets['values']) >= 1

    def test_distill_creates_self_model(self, temp_vault: Path):
        """Should create self-model.md narrative."""
        init_relic.init()
        capture_note.capture(text='Test value', obs_type='value', confidence=0.95)

        distill_facets.main()

        self_model = (temp_vault / 'self-model.md').read_text()
        assert '# Self Model' in self_model
        assert 'Test value' in self_model

    def test_distill_creates_voice_profile(self, temp_vault: Path):
        """Should create voice.md with tone observations."""
        init_relic.init()
        capture_note.capture(text='Prefers concise communication', obs_type='tone')

        distill_facets.main()

        voice = (temp_vault / 'voice.md').read_text()
        assert '# Voice Profile' in voice
        assert 'concise communication' in voice

    def test_distill_detects_patterns(self, temp_vault: Path):
        """Should detect recurring patterns from tags."""
        init_relic.init()
        capture_note.capture(text='Value 1', obs_type='value', tags=['testing'])
        capture_note.capture(text='Value 2', obs_type='value', tags=['testing'])
        capture_note.capture(text='Value 3', obs_type='value', tags=['security'])

        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text())
        assert 'stats' in facets

    def test_distill_preserves_distinct_similar_observations(self, temp_vault: Path):
        """Should preserve distinct observations instead of merging by heuristic similarity."""
        init_relic.init()
        capture_note.capture(text='Prefers concise direct feedback', obs_type='preference')
        capture_note.capture(text='Prefers concise status updates', obs_type='preference')

        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text())
        assert 'Prefers concise direct feedback' in facets['preferences']
        assert 'Prefers concise status updates' in facets['preferences']

    def test_distill_filters_records_without_usable_text(self, temp_vault: Path):
        """Should ignore records with empty or missing text during distillation."""
        init_relic.init()

        inbox = temp_vault / 'inbox.ndjson'
        inbox.write_text(
            '\n'.join([
                json.dumps({'text': 'Values testing', 'type': 'value', 'confidence': 0.9}),
                json.dumps({'text': '', 'type': 'value', 'confidence': 0.8}),
                json.dumps({'type': 'value', 'confidence': 0.7}),
                json.dumps({'text': None, 'type': 'value', 'confidence': 0.6}),
            ]) + '\n',
            encoding='utf-8',
        )

        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text())
        self_model = (temp_vault / 'self-model.md').read_text()

        assert facets['values'] == ['Values testing']
        assert 'Values testing' in self_model
        assert '- None' not in self_model

    def test_distill_uses_relic_vault_env_path(self, temp_vault: Path, monkeypatch: pytest.MonkeyPatch):
        """Should honor RELIC_VAULT_PATH when resolving vault files."""
        env_vault = temp_vault / 'env-vault'
        env_vault.mkdir(parents=True, exist_ok=True)
        (env_vault / 'inbox.ndjson').write_text(
            json.dumps({'text': 'Env scoped value', 'type': 'value', 'confidence': 0.9}) + '\n',
            encoding='utf-8',
        )
        (env_vault / 'manifest.json').write_text(
            json.dumps({'name': 'relic', 'version': 1, 'createdAt': 'x', 'updatedAt': 'x', 'mode': 'local-first'}),
            encoding='utf-8',
        )

        monkeypatch.setenv('RELIC_VAULT_PATH', str(env_vault))
        monkeypatch.setattr(distill_facets, 'VAULT', env_vault)
        monkeypatch.setattr(distill_facets, 'INBOX', env_vault / 'inbox.ndjson')
        monkeypatch.setattr(distill_facets, 'FACETS', env_vault / 'facets.json')
        monkeypatch.setattr(distill_facets, 'SELF_MODEL', env_vault / 'self-model.md')
        monkeypatch.setattr(distill_facets, 'VOICE', env_vault / 'voice.md')
        monkeypatch.setattr(distill_facets, 'GOALS', env_vault / 'goals.md')
        monkeypatch.setattr(distill_facets, 'RELATIONSHIPS', env_vault / 'relationships.md')
        monkeypatch.setattr(distill_facets, 'MANIFEST', env_vault / 'manifest.json')

        distill_facets.main()

        facets = json.loads((env_vault / 'facets.json').read_text())
        assert facets['values'] == ['Env scoped value']

    def test_distill_skips_invalid_ndjson_lines(self, temp_vault: Path):
        """Should continue distilling when inbox contains malformed lines."""
        init_relic.init()

        inbox = temp_vault / 'inbox.ndjson'
        inbox.write_text(
            '\n'.join([
                json.dumps({'text': 'Values testing', 'type': 'value', 'confidence': 0.9}),
                '{invalid json',
                json.dumps({'text': 'Prefers concise updates', 'type': 'preference', 'confidence': 0.8}),
            ]) + '\n',
            encoding='utf-8',
        )

        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text(encoding='utf-8'))
        self_model = (temp_vault / 'self-model.md').read_text(encoding='utf-8')

        assert facets['values'] == ['Values testing']
        assert facets['preferences'] == ['Prefers concise updates']
        assert 'Values testing' in self_model
        assert 'Prefers concise updates' in self_model

    def test_distill_filters_semantic_noise_records(self, temp_vault: Path):
        """Should drop valid-shaped legacy records that are clearly tool or prompt junk."""
        init_relic.init()

        inbox = temp_vault / 'inbox.ndjson'
        inbox.write_text(
            '\n'.join([
                json.dumps({'text': 'Prefers concise updates', 'type': 'preference', 'confidence': 0.9}),
                json.dumps({'text': 'fixed:\\n\\n1', 'type': 'preference', 'confidence': 0.8}),
                json.dumps({'text': 'cannot read the spec or interact with workspace notes\\n\\n**options to proceed:**\\n\\n1', 'type': 'preference', 'confidence': 0.8}),
                json.dumps({'text': "see we're now in a new workspace at `/users/yexiaodong/intent/workspaces/project-build/repo` which appears to be a fresh repo with just a readme and", 'type': 'preference', 'confidence': 0.8}),
            ]) + '\n',
            encoding='utf-8',
        )

        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text())
        self_model = (temp_vault / 'self-model.md').read_text()

        assert facets['preferences'] == ['Prefers concise updates']
        assert 'fixed:\\n\\n1' not in self_model
        assert 'cannot read the spec' not in self_model
        assert '/users/yexiaodong/intent/workspaces' not in self_model

    def test_distill_filters_workspace_permission_fragments(self, temp_vault: Path):
        """Should drop workspace and permission fragments that still look like normal sentences."""
        init_relic.init()

        inbox = temp_vault / 'inbox.ndjson'
        inbox.write_text(
            '\n'.join([
                json.dumps({'text': 'Prefers concise updates', 'type': 'preference', 'confidence': 0.9}),
                json.dumps({'text': 'can coordinate properly (read spec, create tasks, delegate)\\n2', 'type': 'preference', 'confidence': 0.8}),
                json.dumps({'text': 'can read/write files in this repo path directly, but this bypasses the workspace coordination system\\n3', 'type': 'preference', 'confidence': 0.8}),
                json.dumps({'text': 'value simplicity in code\\")\\n3', 'type': 'value', 'confidence': 0.8}),
            ]) + '\n',
            encoding='utf-8',
        )

        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text())

        assert facets['preferences'] == ['Prefers concise updates']
        assert facets['values'] == []

    def test_distill_normalizes_malformed_legacy_tags_and_confidence(self, temp_vault: Path):
        """Should tolerate malformed historical tags/confidence instead of crashing."""
        init_relic.init()

        inbox = temp_vault / 'inbox.ndjson'
        inbox.write_text(
            '\n'.join([
                json.dumps({'text': 'Values reliable tools', 'type': 'value', 'tags': 'testing', 'confidence': 'high'}),
                json.dumps({'text': 'Prefers concise communication', 'type': 'preference', 'tags': ['communication', ''], 'confidence': 0.9}),
                json.dumps({'text': 'Tone matters', 'type': 'tone', 'tags': None, 'confidence': True}),
            ]) + '\n',
            encoding='utf-8',
        )

        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text())
        self_model = (temp_vault / 'self-model.md').read_text()
        voice = (temp_vault / 'voice.md').read_text()

        assert facets['values'] == ['Values reliable tools']
        assert facets['preferences'] == ['Prefers concise communication']
        assert 'Values reliable tools' in self_model
        assert 'Prefers concise communication' in voice


class TestProposeUpdate:
    """Tests for propose_update.py."""

    def test_propose_creates_proposal(self, temp_vault: Path):
        """Should create a timestamped proposal file."""
        init_relic.init()
        capture_note.capture(text='Test value', obs_type='value')

        propose_update.propose()

        proposals_dir = temp_vault / 'evolution' / 'proposals'
        assert proposals_dir.exists()
        proposals = list(proposals_dir.glob('*.json'))
        assert len(proposals) >= 1

    def test_proposal_has_required_fields(self, temp_vault: Path):
        """Proposal should have id, summary, rationale, changes."""
        init_relic.init()
        capture_note.capture(text='Test', obs_type='value')

        propose_update.propose()

        proposals_dir = temp_vault / 'evolution' / 'proposals'
        proposal_file = list(proposals_dir.glob('*.json'))[-1]
        proposal = json.loads(proposal_file.read_text())

        assert 'id' in proposal
        assert 'summary' in proposal
        assert 'rationale' in proposal
        assert 'changes' in proposal


class TestApplyProposal:
    """Tests for apply_proposal.py."""

    def test_apply_moves_proposal_to_accepted(self, temp_vault: Path):
        """Should move proposal to accepted directory."""
        init_relic.init()
        capture_note.capture(text='Test', obs_type='value')
        propose_update.propose()

        proposals_dir = temp_vault / 'evolution' / 'proposals'
        proposal_file = list(proposals_dir.glob('*.json'))[-1]
        proposal_id = proposal_file.stem

        apply_proposal.apply(proposal_id)

        accepted_dir = temp_vault / 'evolution' / 'accepted'
        accepted_file = accepted_dir / f'{proposal_id}.json'
        assert accepted_file.exists()
        assert not proposal_file.exists()

    def test_apply_creates_snapshot(self, temp_vault: Path):
        """Should create snapshot before applying."""
        init_relic.init()
        capture_note.capture(text='Test', obs_type='value')
        propose_update.propose()

        proposals_dir = temp_vault / 'evolution' / 'proposals'
        proposal_file = list(proposals_dir.glob('*.json'))[-1]
        proposal_id = proposal_file.stem

        apply_proposal.apply(proposal_id)

        snapshots_dir = temp_vault / 'snapshots'
        snapshots = list(snapshots_dir.iterdir())
        assert len(snapshots) >= 1
        snapshot = snapshots[0]
        assert (snapshot / 'self-model.md').exists()

    def test_apply_rejects_path_traversal_ids(self, temp_vault: Path):
        """Should reject proposal IDs that escape the proposals directory."""
        init_relic.init()

        with pytest.raises(ValueError):
            apply_proposal.apply('../outside')


class TestRenderExport:
    """Tests for render_export.py."""

    def test_render_creates_agent_prompt(self, temp_vault: Path):
        """Should create agent-prompt.md export."""
        init_relic.init()
        capture_note.capture(text='Test value', obs_type='value')
        distill_facets.main()

        render_export.main()

        export = temp_vault / 'exports' / 'agent-prompt.md'
        assert export.exists()

    def test_export_contains_self_model(self, temp_vault: Path):
        """Export should contain distilled self model."""
        init_relic.init()
        capture_note.capture(text='Prefers testing', obs_type='preference')
        distill_facets.main()

        render_export.main()

        export = (temp_vault / 'exports' / 'agent-prompt.md').read_text()
        assert '# Relic Agent Prompt' in export
        assert 'Prefers testing' in export

    def test_export_contains_facets_json(self, temp_vault: Path):
        """Export should include facets as JSON block."""
        init_relic.init()
        capture_note.capture(text='Test', obs_type='value')
        distill_facets.main()

        render_export.main()

        export = (temp_vault / 'exports' / 'agent-prompt.md').read_text()
        assert '```json' in export
        assert 'values' in export

    def test_distill_writes_relationships_doc(self, temp_vault: Path):
        """Should render captured relationships into relationships.md."""
        init_relic.init()
        capture_note.capture(text='Collaborates closely with the OpenClaw team', obs_type='relationship')

        distill_facets.main()

        relationships = (temp_vault / 'relationships.md').read_text()
        assert 'Collaborates closely with the OpenClaw team' in relationships

    def test_full_workflow(self, temp_vault: Path):
        """Complete workflow: init -> capture -> distill -> propose -> apply -> export."""
        init_relic.init()
        assert (temp_vault / 'manifest.json').exists()

        capture_note.capture(text='Values immutability', obs_type='value', tags=['code-quality'])
        capture_note.capture(text='Prefers small files', obs_type='preference', tags=['code-quality'])
        capture_note.capture(text='Goal: build great software', obs_type='goal')

        distill_facets.main()

        self_model = (temp_vault / 'self-model.md').read_text()
        assert 'immutability' in self_model.lower() or 'Values' in self_model

        propose_update.propose()
        proposals = list((temp_vault / 'evolution' / 'proposals').glob('*.json'))
        assert len(proposals) >= 1

        proposal_id = proposals[0].stem
        apply_proposal.apply(proposal_id)
        assert (temp_vault / 'evolution' / 'accepted' / f'{proposal_id}.json').exists()

        render_export.main()
        export = (temp_vault / 'exports' / 'agent-prompt.md').read_text()
        assert '# Relic Agent Prompt' in export

    def test_multiple_distill_cycles(self, temp_vault: Path):
        """Should handle multiple distillation cycles without errors."""
        init_relic.init()

        capture_note.capture(text='First observation', obs_type='value')
        distill_facets.main()

        capture_note.capture(text='Second observation', obs_type='preference')
        distill_facets.main()

        capture_note.capture(text='Third observation', obs_type='goal')
        distill_facets.main()

        facets = json.loads((temp_vault / 'facets.json').read_text())
        assert len(facets['values']) >= 1
        assert len(facets['preferences']) >= 1


class TestPackaging:
    """Tests for ClawHub/OpenClaw package readiness."""

    def test_default_vault_path_uses_home_directory(self, monkeypatch: pytest.MonkeyPatch):
        """Default vault path should resolve from HOME, not a hardcoded machine path."""
        expected = Path('/tmp/relic-home') / '.openclaw' / 'workspace' / 'projects' / 'relic' / 'vault'

        monkeypatch.delenv('RELIC_VAULT_PATH', raising=False)
        monkeypatch.setattr(Path, 'home', staticmethod(lambda: Path('/tmp/relic-home')))

        resolved = vault_paths.get_default_vault_path()

        assert resolved == expected
        assert '/Users/yexiaodong/' not in str(resolved)

    def test_relic_vault_path_env_override_wins(self, monkeypatch: pytest.MonkeyPatch):
        """RELIC_VAULT_PATH should override the default vault path."""
        override = Path('/tmp/custom-relic-vault')

        monkeypatch.setenv('RELIC_VAULT_PATH', str(override))
        monkeypatch.setattr(Path, 'home', staticmethod(lambda: Path('/tmp/ignored-home')))

        assert vault_paths.get_vault_path() == override.resolve()

    def test_relic_vault_path_resolves_relative_override(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
        """Relative RELIC_VAULT_PATH values should resolve to an absolute path."""
        relative_vault = Path('relative-vault')

        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv('RELIC_VAULT_PATH', str(relative_vault))

        assert vault_paths.get_vault_path() == (tmp_path / relative_vault).resolve()

    def test_package_metadata_files_exist_for_clawhub_readiness(self):
        """Package root should contain the expected publishable metadata and docs."""
        assert (PACKAGE_ROOT / 'SKILL.md').exists()
        assert (PACKAGE_ROOT / 'README.md').exists()
        assert (PACKAGE_ROOT / '_meta.json').exists()
        assert (PACKAGE_ROOT / '.clawhub' / 'origin.json').exists()
        assert (PACKAGE_ROOT / 'references' / 'openclaw-integration.md').exists()
        assert (PACKAGE_ROOT / 'references' / 'hooks-setup.md').exists()

    def test_package_does_not_publish_vault_directory(self):
        """Private vault state should stay outside the publishable package root."""
        assert not (PACKAGE_ROOT / 'vault').exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
