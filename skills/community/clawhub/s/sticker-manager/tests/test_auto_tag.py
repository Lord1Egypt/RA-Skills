"""Tests for auto-tag functionality in sticker_semantic.py."""
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


def test_auto_tag_single_file(tmp_path):
    """Test auto-tag for a single image file."""
    library = tmp_path / 'library'
    library.mkdir()
    test_image = library / 'test.gif'
    test_image.write_bytes(b'GIF89a' + b'x' * 10000)
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'auto-tag', str(test_image), env=env)
    
    assert result.returncode == 0
    assert '__AUTO_TAG__:' in result.stdout
    
    # Parse the output
    output_lines = result.stdout.strip().split('\n')
    for line in output_lines:
        if line.startswith('__AUTO_TAG__:'):
            data = json.loads(line.split(':', 1)[1])
            assert 'name' in data
            assert 'vision_plan' in data
            break


def test_auto_tag_directory(tmp_path):
    """Test auto-tag for a directory of images."""
    library = tmp_path / 'library'
    library.mkdir()
    
    (library / 'sticker1.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    (library / 'sticker2.png').write_bytes(b'\x89PNG' + b'x' * 10000)
    (library / 'not_image.txt').write_text('not an image')  # Should be ignored
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'auto-tag-dir', str(library), env=env)
    
    assert result.returncode == 0
    assert '__AUTO_TAG__:' in result.stdout
    # Should have 2 auto-tag outputs (one per image)
    assert result.stdout.count('__AUTO_TAG__:') >= 2


def test_auto_tag_vision_plan_structure(tmp_path):
    """Test that auto-tag generates proper vision plan structure."""
    library = tmp_path / 'library'
    library.mkdir()
    test_image = library / 'test.gif'
    test_image.write_bytes(b'GIF89a' + b'x' * 10000)
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'auto-tag', str(test_image), env=env)
    
    assert result.returncode == 0
    
    # Find and parse the vision plan
    for line in result.stdout.split('\n'):
        if line.startswith('__AUTO_TAG__:'):
            data = json.loads(line.split(':', 1)[1])
            vision_plan = data.get('vision_plan', {})
            
            # Check vision plan structure
            assert 'image_path' in vision_plan
            assert 'models' in vision_plan
            assert 'prompt' in vision_plan
            break


def test_auto_tag_nonexistent_file(tmp_path):
    """Test auto-tag for non-existent file."""
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'auto-tag', '/nonexistent/image.gif', env=env)
    
    assert result.returncode == 1


def test_auto_tag_empty_directory(tmp_path):
    """Test auto-tag for empty directory."""
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'auto-tag-dir', str(library), env=env)
    
    # Should return 1 for empty directory
    assert result.returncode == 1 or 'No image files found' in result.stdout


def test_auto_tag_chinese_language(tmp_path):
    """Test auto-tag with Chinese language output."""
    library = tmp_path / 'library'
    library.mkdir()
    test_image = library / 'test.gif'
    test_image.write_bytes(b'GIF89a' + b'x' * 10000)
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=zh', 'auto-tag', str(test_image), env=env)
    
    assert result.returncode == 0
    # Vision plan should indicate Chinese language
    for line in result.stdout.split('\n'):
        if line.startswith('__AUTO_TAG__:'):
            data = json.loads(line.split(':', 1)[1])
            vision_plan = data.get('vision_plan', {})
            assert vision_plan.get('language') == 'zh'
            break


def test_auto_tag_supports_all_image_formats(tmp_path):
    """Test that auto-tag supports all image formats."""
    library = tmp_path / 'library'
    library.mkdir()
    
    # Create files with all supported extensions
    formats = {
        'test.jpg': b'\xff\xd8\xff' + b'x' * 10000,
        'test.jpeg': b'\xff\xd8\xff' + b'x' * 10000,
        'test.png': b'\x89PNG' + b'x' * 10000,
        'test.webp': b'RIFF' + b'x' * 10000,
        'test.gif': b'GIF89a' + b'x' * 10000,
    }
    
    for filename, content in formats.items():
        (library / filename).write_bytes(content)
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'auto-tag-dir', str(library), env=env)
    
    assert result.returncode == 0
    # Should have auto-tag output for each image
    assert result.stdout.count('__AUTO_TAG__:') >= len(formats)