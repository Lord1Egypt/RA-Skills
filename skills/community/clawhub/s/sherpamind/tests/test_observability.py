from pathlib import Path

from sherpamind.db import initialize_db
from sherpamind.observability import generate_runtime_status_artifacts


def test_generate_runtime_status_artifacts(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv('SHERPAMIND_WORKSPACE_ROOT', str(tmp_path))
    db = tmp_path / '.SherpaMind' / 'private' / 'data' / 'sherpamind.sqlite3'
    initialize_db(db)
    result = generate_runtime_status_artifacts(db)
    assert result['status'] == 'ok'
    out = Path(result['output_path'])
    assert out.exists()
    text = out.read_text()
    assert 'SherpaMind Runtime Status' in text
    assert 'Vector index status' in text
    assert 'Retrieval readiness' in text
