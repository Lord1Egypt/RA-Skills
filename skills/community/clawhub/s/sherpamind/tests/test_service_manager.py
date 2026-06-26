from pathlib import Path

from sherpamind.service_manager import unit_contents


def test_unit_contents_contains_service_run(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv('SHERPAMIND_WORKSPACE_ROOT', str(tmp_path))
    text = unit_contents()
    assert 'ExecStart=' in text
    assert 'service-run' in text
    assert 'SHERPAMIND_WORKSPACE_ROOT=' in text
    assert 'EnvironmentFile=' not in text
