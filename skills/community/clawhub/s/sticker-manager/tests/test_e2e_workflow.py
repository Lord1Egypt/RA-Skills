"""End-to-end workflow tests for sticker-manager."""
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


class TestE2EBatchImportAndAutoTag:
    """End-to-end tests for batch import + auto-tag workflow."""
    
    def test_import_then_auto_tag(self, tmp_path):
        """Test complete workflow: import images, then auto-tag them."""
        # 1. Create source images
        source_dir = tmp_path / 'source'
        source_dir.mkdir()
        (source_dir / 'import1.gif').write_bytes(b'GIF89a' + b'x' * 10000)
        (source_dir / 'import2.png').write_bytes(b'\x89PNG' + b'x' * 10000)
        
        library = tmp_path / 'library'
        library.mkdir()
        
        env = os.environ.copy()
        env['STICKER_MANAGER_DIR'] = str(library)
        
        # 2. Batch import with auto-tag plan
        result = run_script(
            'batch_import.py',
            '--lang=en',
            str(source_dir),
            '--target-dir', str(library),
            '--auto-tag',
            env=env
        )
        
        assert result.returncode == 0
        assert (library / 'import1.gif').exists()
        assert (library / 'import2.png').exists()
        assert '__AUTO_TAG_PLAN__:' in result.stdout
        
        # 3. Verify auto-tag plan structure
        for line in result.stdout.split('\n'):
            if line.startswith('__AUTO_TAG_PLAN__:'):
                plan = json.loads(line.split(':', 1)[1])
                assert 'items' in plan
                assert len(plan['items']) >= 2
                break


class TestE2EDiscoverAndImport:
    """End-to-end tests for discover + import workflow."""
    
    def test_discover_local_directory(self, tmp_path):
        """Test discovering images from local directory."""
        source_dir = tmp_path / 'stickers'
        source_dir.mkdir()
        (source_dir / 'found1.gif').write_bytes(b'GIF89a' + b'x' * 10000)
        (source_dir / 'found2.jpg').write_bytes(b'\xff\xd8\xff' + b'x' * 10000)
        
        library = tmp_path / 'library'
        library.mkdir()
        
        env = os.environ.copy()
        env['STICKER_MANAGER_DIR'] = str(library)
        
        # 1. Discover
        discover_result = run_script(
            'discover_sources.py',
            '--lang=en',
            str(source_dir),
            '--output', str(tmp_path / 'discovered.json'),
            env=env
        )
        
        assert discover_result.returncode == 0
        
        # 2. Check discovered results
        discovered_file = tmp_path / 'discovered.json'
        assert discovered_file.exists()
        
        discovered = json.loads(discovered_file.read_text())
        assert discovered['total'] >= 2
        assert len(discovered['directories']) >= 2


class TestE2ESemanticWorkflow:
    """End-to-end tests for complete semantic workflow."""
    
    def test_tag_suggest_context_recommend(self, tmp_path):
        """Test complete semantic workflow: tag -> suggest -> context-recommend."""
        library = tmp_path / 'library'
        library.mkdir()
        
        # Create test sticker
        (library / 'celebrate.gif').write_bytes(b'GIF89a' + b'x' * 10000)
        
        env = os.environ.copy()
        env['STICKER_MANAGER_DIR'] = str(library)
        
        # 1. Tag the sticker
        tag_result = run_script(
            'sticker_semantic.py',
            '--lang=en',
            'tag',
            'celebrate',
            'happy,excited',
            'party,success',
            'celebration,win',
            'A celebration sticker for success moments',
            env=env
        )
        assert tag_result.returncode == 0
        
        # 2. Test suggest
        suggest_result = run_script(
            'sticker_semantic.py',
            '--lang=en',
            'suggest',
            'We won the game!',
            env=env
        )
        assert suggest_result.returncode == 0
        assert '__MODEL_MATCH__:' in suggest_result.stdout or 'celebrate' in suggest_result.stdout.lower()
        
        # 3. Test context-recommend
        history = json.dumps([
            {'content': 'Great news everyone!'},
            {'content': 'We finally succeeded!'},
        ])
        
        rec_result = run_script(
            'sticker_semantic.py',
            '--lang=en',
            'context-recommend',
            history,
            env=env
        )
        assert rec_result.returncode == 0
        assert '__CONTEXT_RECOMMEND__:' in rec_result.stdout


class TestE2ELanguageSupport:
    """End-to-end tests for language support across all features."""
    
    def test_chinese_workflow(self, tmp_path):
        """Test complete workflow with Chinese language."""
        library = tmp_path / 'library'
        library.mkdir()
        
        (library / '开心.gif').write_bytes(b'GIF89a' + b'x' * 10000)
        
        env = os.environ.copy()
        env['STICKER_MANAGER_DIR'] = str(library)
        
        # Tag in Chinese
        tag_result = run_script(
            'sticker_semantic.py',
            '--lang=zh',
            'tag',
            '开心',
            '开心,快乐',
            '庆祝,成功',
            '开心,笑',
            '一个开心庆祝的表情包',
            env=env
        )
        assert tag_result.returncode == 0
        assert '已添加标签' in tag_result.stdout
        
        # List tags
        list_result = run_script(
            'sticker_semantic.py',
            '--lang=zh',
            'list',
            env=env
        )
        assert '表情包标签库' in list_result.stdout


class TestE2EErrorHandling:
    """End-to-end tests for error handling."""
    
    def test_missing_library_dir(self, tmp_path):
        """Test operations with missing library directory."""
        env = os.environ.copy()
        env['STICKER_MANAGER_DIR'] = str(tmp_path / 'nonexistent')
        
        result = run_script('get_sticker.py', '--lang=en', 'test', env=env)
        assert result.returncode == 1
        assert 'not found' in result.stdout.lower() or '不存在' in result.stdout
    
    def test_invalid_source_directory(self, tmp_path):
        """Test batch import with invalid source directory."""
        library = tmp_path / 'library'
        library.mkdir()
        
        env = os.environ.copy()
        env['STICKER_MANAGER_DIR'] = str(library)
        
        result = run_script(
            'batch_import.py',
            '--lang=en',
            '/nonexistent/path',
            '--target-dir', str(library),
            env=env
        )
        # Should complete but report no files
        assert 'imported_count": 0' in result.stdout or result.returncode == 1


class TestE2EMultipleFormats:
    """End-to-end tests for multiple image format support."""
    
    def test_all_formats_workflow(self, tmp_path):
        """Test workflow with all supported image formats."""
        source_dir = tmp_path / 'source'
        source_dir.mkdir()
        
        # Create files in all supported formats with different names to avoid conflicts
        formats = {
            'image_jpg.jpg': b'\xff\xd8\xff' + b'x' * 10000,
            'image_jpeg.jpeg': b'\xff\xd8\xff' + b'y' * 10000,
            'image_png.png': b'\x89PNG' + b'x' * 10000,
            'image_webp.webp': b'RIFF' + b'x' * 10000,
            'image_gif.gif': b'GIF89a' + b'x' * 10000,
        }
        
        for filename, content in formats.items():
            (source_dir / filename).write_bytes(content)
        
        library = tmp_path / 'library'
        library.mkdir()
        
        env = os.environ.copy()
        env['STICKER_MANAGER_DIR'] = str(library)
        
        # Import all formats
        result = run_script(
            'batch_import.py',
            '--lang=en',
            str(source_dir),
            '--target-dir', str(library),
            env=env
        )
        
        assert result.returncode == 0
        
        # Verify all files imported
        for filename in formats:
            assert (library / filename).exists(), f'{filename} should exist'
        
        # Auto-tag all
        auto_tag_result = run_script(
            'sticker_semantic.py',
            '--lang=en',
            'auto-tag-dir',
            str(library),
            env=env
        )
        
        assert auto_tag_result.returncode == 0
        assert auto_tag_result.stdout.count('__AUTO_TAG__:') >= len(formats)