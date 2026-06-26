"""Tests for context-recommend functionality in sticker_semantic.py."""
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


def setup_library_with_tags(library):
    """Set up a library with tagged stickers for testing."""
    library.mkdir(parents=True, exist_ok=True)
    
    # Create test images
    (library / 'happy.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    (library / 'sad.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    (library / 'angry.gif').write_bytes(b'GIF89a' + b'x' * 10000)
    
    # Create tags file
    tags = {
        'happy.gif': {
            'emotions': ['happy', 'joy', 'celebration'],
            'scenes': ['success', 'party'],
            'keywords': ['smile', 'laugh'],
            'description': 'A happy celebration sticker'
        },
        'sad.gif': {
            'emotions': ['sad', 'disappointed'],
            'scenes': ['failure', 'apology'],
            'keywords': ['cry', 'tears'],
            'description': 'A sad emotional sticker'
        },
        'angry.gif': {
            'emotions': ['angry', 'frustrated'],
            'scenes': ['conflict', 'argument'],
            'keywords': ['mad', 'upset'],
            'description': 'An angry reaction sticker'
        }
    }
    
    tags_file = library / '.tags.json'
    with open(tags_file, 'w', encoding='utf-8') as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)
    
    return library


def test_context_recommend_from_json_string(tmp_path):
    """Test context-recommend with JSON string input."""
    library = setup_library_with_tags(tmp_path / 'library')
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    # Pass chat history as JSON
    history = json.dumps([
        {'content': 'We finally did it! So happy!'},
        {'content': 'Great success!'},
    ])
    
    result = run_script('sticker_semantic.py', '--lang=en', 'context-recommend', history, env=env)
    
    assert result.returncode == 0
    assert '__CONTEXT_RECOMMEND__:' in result.stdout
    assert '__ANALYZE_HISTORY__:' in result.stdout


def test_context_recommend_from_file(tmp_path):
    """Test context-recommend with history file input."""
    library = setup_library_with_tags(tmp_path / 'library')
    
    # Create history file
    history_file = tmp_path / 'history.json'
    history = [
        {'content': 'I am so disappointed with the result'},
        {'content': 'This is really sad news'},
    ]
    history_file.write_text(json.dumps(history))
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'context-recommend', str(history_file), env=env)
    
    assert result.returncode == 0
    assert '__CONTEXT_RECOMMEND__:' in result.stdout


def test_context_recommend_text_file(tmp_path):
    """Test context-recommend with plain text file input."""
    library = setup_library_with_tags(tmp_path / 'library')
    
    # Create plain text history file
    history_file = tmp_path / 'history.txt'
    history_file.write_text('I am very angry about this situation\nThis is frustrating\n')
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'context-recommend', str(history_file), env=env)
    
    assert result.returncode == 0
    assert '__CONTEXT_RECOMMEND__:' in result.stdout


def test_context_recommend_top_n(tmp_path):
    """Test context-recommend with custom top_n parameter."""
    library = setup_library_with_tags(tmp_path / 'library')
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    history = json.dumps([{'content': 'Mixed emotions here'}])
    
    result = run_script('sticker_semantic.py', '--lang=en', 'context-recommend', history, '--top=2', env=env)
    
    assert result.returncode == 0
    assert '__CONTEXT_RECOMMEND__:' in result.stdout
    
    # Parse recommendation output
    for line in result.stdout.split('\n'):
        if line.startswith('__CONTEXT_RECOMMEND__'):
            data = json.loads(line.split(':', 1)[1])
            assert data['requested_top_n'] == 2
            break


def test_context_recommend_single_message(tmp_path):
    """Test context-recommend with single message."""
    library = setup_library_with_tags(tmp_path / 'library')
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    # Single text message
    result = run_script('sticker_semantic.py', '--lang=en', 'context-recommend', 'I am happy today!', env=env)
    
    assert result.returncode == 0
    assert '__CONTEXT_RECOMMEND__:' in result.stdout


def test_context_recommend_no_history(tmp_path):
    """Test context-recommend with empty history."""
    library = setup_library_with_tags(tmp_path / 'library')
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    result = run_script('sticker_semantic.py', '--lang=en', 'context-recommend', '[]', env=env)
    
    # Should handle empty gracefully
    assert 'No chat history' in result.stdout or result.returncode == 1


def test_context_recommend_no_stickers(tmp_path):
    """Test context-recommend when no tagged stickers exist."""
    library = tmp_path / 'library'
    library.mkdir()
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    history = json.dumps([{'content': 'Hello world'}])
    
    result = run_script('sticker_semantic.py', '--lang=en', 'context-recommend', history, env=env)
    
    # Should return 1 or handle gracefully
    assert result.returncode == 1 or 'no match' in result.stdout.lower() or result.stdout.strip() == ''


def test_context_recommend_chinese_language(tmp_path):
    """Test context-recommend with Chinese language output."""
    library = setup_library_with_tags(tmp_path / 'library')
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    history = json.dumps([{'content': '太开心了！'}])
    
    result = run_script('sticker_semantic.py', '--lang=zh', 'context-recommend', history, env=env)
    
    assert result.returncode == 0
    # Should have Chinese in output
    assert any(ord(c) > 127 for c in result.stdout)


def test_context_recommend_analyze_history_output(tmp_path):
    """Test that analyze history output has correct structure."""
    library = setup_library_with_tags(tmp_path / 'library')
    
    env = os.environ.copy()
    env['STICKER_MANAGER_DIR'] = str(library)
    
    history = json.dumps([
        {'content': 'First message'},
        {'content': 'Second message'},
    ])
    
    result = run_script('sticker_semantic.py', '--lang=en', 'context-recommend', history, env=env)
    
    assert result.returncode == 0
    
    # Parse and validate analyze history output
    for line in result.stdout.split('\n'):
        if line.startswith('__ANALYZE_HISTORY__:'):
            data = json.loads(line.split(':', 1)[1])
            assert 'task' in data
            assert 'history' in data
            assert 'extract' in data
            assert 'output_format' in data
            break