"""共享测试固件：临时章节文件生成器"""
import os
import sys
from pathlib import Path
import pytest

# 确保能导入 scripts/ 下的模块
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

@pytest.fixture
def chapters_dir(tmp_path):
    """创建临时正文目录并返回路径"""
    d = tmp_path / "chapters"
    d.mkdir()
    return d

def write_chapter(chapters_dir, num, content, title="", suffix=".md", filename=None):
    """辅助函数：写一个章节文件"""
    fname = filename or f"第{num:03d}章{title}.md"
    fpath = chapters_dir / fname
    fpath.write_text(content, encoding='utf-8')
    return fpath

@pytest.fixture
def write_chapter_fixture(chapters_dir):
    """返回写章节的辅助函数"""
    def _write(num, content, title="", suffix=".md", filename=None):
        return write_chapter(chapters_dir, num, content, title, suffix, filename)
    return _write

@pytest.fixture
def outline_dir(tmp_path):
    """创建临时大纲目录"""
    d = tmp_path / "outline"
    d.mkdir()
    return d
