"""Tests for batch_import.py."""
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


def test_batch_import_basic(tmp_path):
    """Test basic batch import from a directory."""
    # Create source directory with test images
    source_dir = tmp_path / 'source'
    source_dir.mkdir()
    (source_dir / 'sticker1.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    (source_dir / 'sticker2.png').write_bytes(b'\x89PNG' + b'x' * 15000)
    (source_dir / 'small.gif').write_bytes(b'GIF89a')  # Too small
    
    # Create target library
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('batch_import.py', '--lang=en', str(source_dir), '--target-dir', str(library), env=env)
    
    assert result.returncode == 0
    assert (library / 'sticker1.gif').exists()
    assert (library / 'sticker2.png').exists()
    assert not (library / 'small.gif').exists()  # Skipped due to size
    assert 'imported' in result.stdout.lower() or 'Import complete' in result.stdout


def test_batch_import_deduplication(tmp_path):
    """Test that duplicates are skipped."""
    source_dir = tmp_path / 'source'
    source_dir.mkdir()
    library = tmp_path / 'library'
    library.mkdir()
    
    # Create identical files
    content = b'GIF89a' + b'x' * 10000
    (source_dir / 'a.gif').write_bytes(content)
    
    # Import first
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    run_script('batch_import.py', str(source_dir), '--target-dir', str(library), env=env)
    
    # Create a duplicate with different name
    (source_dir / 'b.gif').write_bytes(content)
    (source_dir / 'a.gif').unlink()  # Remove original
    
    # Import again - should skip duplicate
    result = run_script('batch_import.py', '--lang=en', str(source_dir), '--target-dir', str(library), env=env)
    
    # Should have skipped the duplicate
    assert 'duplicate' in result.stdout.lower() or 'Skipped' in result.stdout
    assert '1 duplicates' in result.stdout


def test_batch_import_recursive(tmp_path):
    """Test recursive directory scanning."""
    source_dir = tmp_path / 'source'
    subdir = source_dir / 'subdir'
    subdir.mkdir(parents=True)
    
    # Use different content to avoid deduplication
    (source_dir / 'top.gif').write_bytes(b'GIF89a' + b'a' * 10000)
    (subdir / 'nested.gif').write_bytes(b'GIF89a' + b'b' * 10000)
    
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('batch_import.py', '--lang=en', str(source_dir), '--target-dir', str(library), '--recursive', env=env)
    
    assert result.returncode == 0
    assert (library / 'top.gif').exists()
    assert (library / 'nested.gif').exists()


def test_batch_import_non_recursive(tmp_path):
    """Test non-recursive directory scanning."""
    source_dir = tmp_path / 'source'
    subdir = source_dir / 'subdir'
    subdir.mkdir(parents=True)
    
    (source_dir / 'top.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    (subdir / 'nested.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('batch_import.py', '--lang=en', str(source_dir), '--target-dir', str(library), '--no-recursive', env=env)
    
    assert result.returncode == 0
    assert (library / 'top.gif').exists()
    assert not (library / 'nested.gif').exists()  # Not included due to non-recursive


def test_batch_import_output_report(tmp_path):
    """Test JSON output report generation."""
    source_dir = tmp_path / 'source'
    source_dir.mkdir()
    (source_dir / 'test.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    
    library = tmp_path / 'library'
    library.mkdir()
    report_file = tmp_path / 'report.json'
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('batch_import.py', '--lang=en', str(source_dir), '--target-dir', str(library), '--output', str(report_file), env=env)
    
    assert result.returncode == 0
    assert report_file.exists()
    
    report = json.loads(report_file.read_text())
    assert 'imported' in report
    assert report['summary']['imported_count'] >= 1


def test_batch_import_duplicate_count_in_report(tmp_path):
    """Test duplicate count is tracked in the JSON report."""
    source_dir = tmp_path / 'source'
    source_dir.mkdir()
    library = tmp_path / 'library'
    library.mkdir()
    report_file = tmp_path / 'report.json'

    content = b'GIF89a' + b'x' * 10000
    (library / 'existing.gif').write_bytes(content)
    (source_dir / 'incoming.gif').write_bytes(content)

    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)

    result = run_script(
        'batch_import.py',
        '--lang=en',
        str(source_dir),
        '--target-dir',
        str(library),
        '--output',
        str(report_file),
        env=env,
    )

    assert result.returncode == 1
    report = json.loads(report_file.read_text())
    assert len(report['duplicates']) == 1


def test_batch_import_auto_tag_plan(tmp_path):
    """Test auto-tag plan generation."""
    source_dir = tmp_path / 'source'
    source_dir.mkdir()
    (source_dir / 'test.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('batch_import.py', '--lang=en', str(source_dir), '--target-dir', str(library), '--auto-tag', env=env)
    
    assert result.returncode == 0
    assert '__AUTO_TAG_PLAN__:' in result.stdout


def test_batch_import_no_valid_dirs(tmp_path):
    """Test error when no valid source directories."""
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('batch_import.py', '--lang=en', '--target-dir', str(library), env=env)
    
    assert result.returncode == 1
    assert 'No valid source' in result.stdout or 'no_dirs' in result.stdout.lower()


def test_batch_import_sources_file(tmp_path):
    """Test reading source directories from file."""
    source_dir1 = tmp_path / 'source1'
    source_dir2 = tmp_path / 'source2'
    source_dir1.mkdir()
    source_dir2.mkdir()
    
    # Use different content to avoid deduplication
    (source_dir1 / 'a.gif').write_bytes(b'GIF89a' + b'a' * 10000)
    (source_dir2 / 'b.gif').write_bytes(b'GIF89a' + b'b' * 10000)
    
    sources_file = tmp_path / 'sources.txt'
    sources_file.write_text(f'{source_dir1}\n{source_dir2}\n')
    
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('batch_import.py', '--lang=en', '--sources-file', str(sources_file), '--target-dir', str(library), env=env)
    
    assert result.returncode == 0
    assert (library / 'a.gif').exists()
    assert (library / 'b.gif').exists()


def test_batch_import_chinese_output(tmp_path):
    """Test Chinese language output."""
    source_dir = tmp_path / 'source'
    source_dir.mkdir()
    (source_dir / 'test.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('batch_import.py', '--lang=zh', str(source_dir), '--target-dir', str(library), env=env)
    
    assert result.returncode == 0
    # Check for Chinese characters in output
    assert any(ord(c) > 127 for c in result.stdout)  # Has non-ASCII (Chinese)
