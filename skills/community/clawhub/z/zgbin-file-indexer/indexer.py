#!/usr/bin/env python3
"""
文件索引管理核心模块
负责文件的添加、更新、删除标记和数据库管理
"""

import sqlite3
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# 默认数据库路径
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'file_index.db')

# 延迟导入 FileSearcher 以避免循环导入
def get_searcher():
    # 使用绝对导入，支持直接运行和模块导入两种方式
    try:
        from .searcher import FileSearcher
    except ImportError:
        from searcher import FileSearcher
    return FileSearcher

# 需要监控的目录
WATCH_DIRS = [
    '/home/t/.claude/projects/-home-t--openclaw-workspace/',
    '/home/t/cc_workspace/',
]


class FileIndexer:
    """文件索引管理类"""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """初始化索引管理器"""
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL,
                filename TEXT NOT NULL,
                file_type TEXT,
                description TEXT,
                content_summary TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                deleted_at TIMESTAMP,
                size INTEGER,
                tags TEXT
            )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_path ON files(path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON files(file_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_deleted ON files(deleted_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_filename ON files(filename)')

        conn.commit()
        conn.close()

    def _get_file_type(self, filepath: str) -> str:
        """根据文件扩展名判断文件类型"""
        ext = Path(filepath).suffix.lower()
        type_map = {
            '.py': 'python_script',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.json': 'config',
            '.yaml': 'config',
            '.yml': 'config',
            '.md': 'documentation',
            '.txt': 'text',
            '.sh': 'shell_script',
            '.bash': 'shell_script',
            '.sql': 'database',
            '.html': 'web',
            '.css': 'web',
            '.vue': 'vue_component',
            '.tsx': 'react_component',
            '.jsx': 'react_component',
        }
        return type_map.get(ext, 'other')

    def _extract_summary(self, filepath: str) -> str:
        """提取文件内容摘要（前 500 字符）"""
        try:
            # 跳过二进制文件
            with open(filepath, 'rb') as f:
                chunk = f.read(500)
                if b'\x00' in chunk:
                    return ''
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(500)
                return content.replace('\n', ' ').strip()
        except Exception:
            return ''

    def add_file(self, filepath: str, description: str = '', tags: List[str] = None) -> bool:
        """添加或更新文件索引"""
        if not os.path.exists(filepath):
            return False

        stat = os.stat(filepath)
        file_type = self._get_file_type(filepath)
        content_summary = self._extract_summary(filepath)
        now = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO files
                (path, filename, file_type, description, content_summary,
                 created_at, updated_at, deleted_at, size, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                filepath,
                os.path.basename(filepath),
                file_type,
                description,
                content_summary,
                now if not self._file_exists(cursor, filepath) else self._get_created_time(cursor, filepath),
                now,
                None,  # deleted_at = None means active
                stat.st_size,
                json.dumps(tags or [])
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding file {filepath}: {e}")
            return False
        finally:
            conn.close()

    def _file_exists(self, cursor, filepath: str) -> bool:
        """检查文件是否已存在"""
        cursor.execute('SELECT id FROM files WHERE path = ?', (filepath,))
        return cursor.fetchone() is not None

    def _get_created_time(self, cursor, filepath: str) -> str:
        """获取文件的创建时间"""
        cursor.execute('SELECT created_at FROM files WHERE path = ?', (filepath,))
        result = cursor.fetchone()
        return result[0] if result else datetime.now().isoformat()

    def mark_deleted(self, filepath: str) -> bool:
        """标记文件为已删除"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE files
                SET deleted_at = ?, updated_at = ?
                WHERE path = ?
            ''', (datetime.now().isoformat(), datetime.now().isoformat(), filepath))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error marking deleted {filepath}: {e}")
            return False
        finally:
            conn.close()

    def remove_file(self, filepath: str) -> bool:
        """从索引中完全移除文件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('DELETE FROM files WHERE path = ?', (filepath,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error removing file {filepath}: {e}")
            return False
        finally:
            conn.close()

    def get_file_info(self, filepath: str) -> Optional[Dict[str, Any]]:
        """获取文件信息"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM files WHERE path = ?', (filepath,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def scan_directory(self, dir_path: str) -> int:
        """扫描目录并添加所有文件到索引"""
        count = 0
        for root, dirs, files in os.walk(dir_path):
            # 跳过隐藏目录和常见非代码目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv', 'dist', 'build')]

            for filename in files:
                if filename.startswith('.'):
                    continue
                filepath = os.path.join(root, filename)
                ext = Path(filename).suffix.lower()
                # 只索引常见代码文件类型
                if ext in ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.md', '.sh', '.sql', '.html', '.css', '.vue', '.tsx', '.jsx']:
                    if self.add_file(filepath):
                        count += 1
        return count

    def get_active_files(self) -> List[Dict[str, Any]]:
        """获取所有活跃文件"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM files WHERE deleted_at IS NULL ORDER BY updated_at DESC')
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_stats(self) -> Dict[str, Any]:
        """获取索引统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM files WHERE deleted_at IS NULL')
        active_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM files WHERE deleted_at IS NOT NULL')
        deleted_count = cursor.fetchone()[0]

        cursor.execute('SELECT file_type, COUNT(*) FROM files WHERE deleted_at IS NULL GROUP BY file_type')
        type_counts = {row[0]: row[1] for row in cursor.fetchall()}

        conn.close()

        return {
            'active_files': active_count,
            'deleted_files': deleted_count,
            'by_type': type_counts
        }


def handle_file_created(filepath: str):
    """处理文件创建事件"""
    indexer = FileIndexer()
    if indexer.add_file(filepath):
        print(f"[FileIndexer] Added: {filepath}")
        return True
    return False


def handle_file_deleted(filepath: str):
    """处理文件删除事件"""
    indexer = FileIndexer()
    if indexer.mark_deleted(filepath):
        print(f"[FileIndexer] Marked deleted: {filepath}")
        return True
    return False


def handle_file_modified(filepath: str):
    """处理文件修改事件"""
    indexer = FileIndexer()
    if indexer.add_file(filepath):
        print(f"[FileIndexer] Updated: {filepath}")
        return True
    return False


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python indexer.py <command> [args]")
        print("Commands:")
        print("  add <filepath> - Add a file to index")
        print("  delete <filepath> - Mark file as deleted")
        print("  scan <dirpath> - Scan directory")
        print("  search <query> - Search files by keyword")
        print("  intent <query> - Get file recommendations by intent")
        print("  stats - Show statistics")
        sys.exit(1)

    command = sys.argv[1]
    indexer = FileIndexer()

    if command == 'add' and len(sys.argv) > 2:
        result = indexer.add_file(sys.argv[2])
        print(f"Added: {result}")

    elif command == 'delete' and len(sys.argv) > 2:
        result = indexer.mark_deleted(sys.argv[2])
        print(f"Marked deleted: {result}")

    elif command == 'scan' and len(sys.argv) > 2:
        count = indexer.scan_directory(sys.argv[2])
        print(f"Scanned {count} files")

    elif command == 'search' and len(sys.argv) > 2:
        FileSearcher = get_searcher()
        searcher = FileSearcher()
        results = searcher.search(sys.argv[2])
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif command == 'intent' and len(sys.argv) > 2:
        FileSearcher = get_searcher()
        searcher = FileSearcher()
        results = searcher.suggest_files(sys.argv[2])
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif command == 'stats':
        stats = indexer.get_stats()
        print(json.dumps(stats, indent=2))

    else:
        print("Unknown command or missing arguments")
