#!/usr/bin/env python3
"""Tests for drift detection script."""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pytest
import sys

# Add paths for imports
scripts_dir = str(Path(__file__).resolve().parents[1] / 'scripts')
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

import drift_detection
import init_relic
import capture_note


@pytest.fixture
def temp_vault():
    """Create a temporary vault for testing."""
    temp_dir = tempfile.mkdtemp()
    vault_path = Path(temp_dir) / 'vault'
    vault_path.mkdir(parents=True, exist_ok=True)

    # Override paths
    drift_detection.VAULT = vault_path
    drift_detection.INBOX = vault_path / 'inbox.ndjson'
    drift_detection.FACETS = vault_path / 'facets.json'
    drift_detection.SELF_MODEL = vault_path / 'self-model.md'
    drift_detection.DRIFT_REPORT = vault_path / 'drift-report.md'
    capture_note.VAULT = vault_path
    capture_note.INBOX = vault_path / 'inbox.ndjson'
    capture_note.MANIFEST = vault_path / 'manifest.json'
    init_relic.VAULT = vault_path

    yield vault_path

    shutil.rmtree(temp_dir, ignore_errors=True)


class TestDriftDetection:
    """Tests for drift_detection.py."""

    def test_detect_drift_no_data(self, temp_vault: Path):
        """Should handle empty vault gracefully."""
        init_relic.init()

        result = drift_detection.detect_drift()
        assert result['status'] == 'no_data'

    def test_detect_drift_with_observations(self, temp_vault: Path):
        """Should detect drift with observations."""
        init_relic.init()
        capture_note.capture(text='I value testing', obs_type='value')
        capture_note.capture(text='I prefer dark mode', obs_type='preference')

        result = drift_detection.detect_drift()
        assert result['status'] == 'success'
        assert 'driftScore' in result
        assert 'reportPath' in result

    def test_drift_report_generated(self, temp_vault: Path):
        """Should generate drift report file."""
        init_relic.init()
        capture_note.capture(text='Test value', obs_type='value')

        drift_detection.detect_drift()

        assert (temp_vault / 'drift-report.md').exists()
        report = (temp_vault / 'drift-report.md').read_text()
        assert '# Drift Report' in report

    def test_extract_keywords(self):
        """Should extract meaningful keywords."""
        keywords = drift_detection.extract_keywords('I value clean code and testing')
        assert 'value' in keywords or 'clean' in keywords
        assert 'and' not in keywords  # stop word

    def test_detect_new_topics(self, temp_vault: Path):
        """Should detect new topics not in facets."""
        init_relic.init()
        capture_note.capture(text='I love quantum computing', obs_type='value', tags=['quantum'])

        recent = drift_detection.load_records()
        facets = drift_detection.load_facets()

        new_topics = drift_detection.detect_new_topics(recent, facets)
        assert len(new_topics) >= 1

    def test_detect_evolving_patterns(self, temp_vault: Path):
        """Should detect patterns from tags."""
        init_relic.init()
        capture_note.capture(text='Test 1', obs_type='value', tags=['testing'])
        capture_note.capture(text='Test 2', obs_type='value', tags=['testing'])
        capture_note.capture(text='Test 3', obs_type='value', tags=['testing'])

        recent = drift_detection.load_records()
        patterns = drift_detection.detect_evolving_patterns(recent)

        assert len(patterns) >= 1
        testing_pattern = next((p for p in patterns if p['tag'] == 'testing'), None)
        assert testing_pattern is not None
        assert testing_pattern['status'] == 'strengthening'

    def test_calculate_drift_score(self):
        """Should calculate drift metrics correctly."""
        score = drift_detection.calculate_drift_score(
            new_topics=[{'id': '1'}] * 6,
            contradictions=[],
            patterns=[{'status': 'strengthening'}] * 2 + [{'status': 'emerging'}] * 3
        )

        assert score['driftLevel'] == 'high'
        assert score['recommendation'] == 'distill'
        assert score['newTopicsCount'] == 6
        assert score['strengtheningPatterns'] == 2
        assert score['emergingPatterns'] == 3

    def test_main_outputs_json(self, temp_vault: Path):
        """Main should output valid JSON."""
        init_relic.init()
        capture_note.capture(text='Test', obs_type='value')

        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            drift_detection.main()
        output = f.getvalue()

        result = json.loads(output)
        assert result['status'] == 'success'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])