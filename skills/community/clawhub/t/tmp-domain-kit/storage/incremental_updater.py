"""
增量更新器 - 监听 storage/ 目录变化，自动更新索引
使用文件 mtime 检测变化，纯 Python 实现（无 watchdog 依赖）
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, Set, Optional
from datetime import datetime

from retrieval.index_manager import IndexManager


class IncrementalUpdater:
    """增量索引更新器"""

    def __init__(self, storage_path: str):
        """
        Args:
            storage_path: 存储目录路径
        """
        self.storage_path = Path(storage_path)
        self.entities_file = self.storage_path / "entities.jsonl"
        self.relations_file = self.storage_path / "relations.jsonl"
        self.state_file = self.storage_path / ".updater_state.json"

        # 文件状态追踪
        self._file_states: Dict[str, float] = {}  # file_path → mtime
        self._line_counts: Dict[str, int] = {}    # file_path → line_count

        # 索引管理器
        self.index = IndexManager(storage_path)

        # 加载上次状态
        self._load_state()

    def _load_state(self):
        """加载上次运行时的文件状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                self._file_states = state.get('file_states', {})
                self._line_counts = state.get('line_counts', {})
            except (json.JSONDecodeError, IOError):
                self._file_states = {}
                self._line_counts = {}

    def _save_state(self):
        """保存当前文件状态"""
        state = {
            'file_states': self._file_states,
            'line_counts': self._line_counts,
            'last_check': datetime.now().isoformat()
        }
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def check_changes(self) -> Dict[str, str]:
        """
        检查文件变化。

        Returns:
            {"entities.jsonl": "modified"/"new"/"unchanged", ...}
        """
        changes = {}

        for filename in ['entities.jsonl', 'relations.jsonl']:
            filepath = self.storage_path / filename
            if not filepath.exists():
                continue

            current_mtime = os.path.getmtime(filepath)
            prev_mtime = self._file_states.get(filename, 0)

            if prev_mtime == 0:
                changes[filename] = "new"
            elif current_mtime > prev_mtime:
                changes[filename] = "modified"
            else:
                changes[filename] = "unchanged"

        return changes

    def update_index(self) -> Dict[str, int]:
        """
        检查变化并更新索引。

        Returns:
            {"new_entities": N, "new_relations": N, "rebuilt": bool}
        """
        changes = self.check_changes()
        result = {"new_entities": 0, "new_relations": 0, "rebuilt": False}

        # 如果任何文件有变化，全量重建索引（简单可靠）
        has_changes = any(v != "unchanged" for v in changes.values())

        if has_changes:
            # 重建索引
            self.index._rebuild_indices()
            result["rebuilt"] = True

            # 统计新增
            if changes.get('entities.jsonl') in ('new', 'modified'):
                current_count = self._count_lines(self.entities_file)
                prev_count = self._line_counts.get('entities.jsonl', 0)
                result["new_entities"] = max(0, current_count - prev_count)

            if changes.get('relations.jsonl') in ('new', 'modified'):
                current_count = self._count_lines(self.relations_file)
                prev_count = self._line_counts.get('relations.jsonl', 0)
                result["new_relations"] = max(0, current_count - prev_count)

            # 更新状态
            for filename in ['entities.jsonl', 'relations.jsonl']:
                filepath = self.storage_path / filename
                if filepath.exists():
                    self._file_states[filename] = os.path.getmtime(filepath)
                    self._line_counts[filename] = self._count_lines(filepath)

            self._save_state()

        return result

    def _count_lines(self, filepath: Path) -> int:
        """统计文件非空行数"""
        if not filepath.exists():
            return 0
        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    count += 1
        return count

    def watch_once(self) -> Dict[str, int]:
        """执行一次检查+更新"""
        return self.update_index()

    def watch_loop(self, interval: float = 5.0, max_iterations: int = None):
        """
        持续监听模式（可选用于后台服务）。

        Args:
            interval: 检查间隔（秒）
            max_iterations: 最大迭代次数（None=无限）
        """
        iteration = 0
        print(f"[IncrementalUpdater] 开始监听 {self.storage_path}")
        print(f"  检查间隔: {interval}s")

        while True:
            result = self.watch_once()
            if result.get('rebuilt'):
                print(f"[{datetime.now().isoformat()}] 索引更新: "
                      f"+{result['new_entities']} 实体, "
                      f"+{result['new_relations']} 关系")

            iteration += 1
            if max_iterations and iteration >= max_iterations:
                break

            time.sleep(interval)

        print(f"[IncrementalUpdater] 监听结束 (共 {iteration} 次检查)")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    storage_path = str(Path(__file__).parent.parent / "storage")
    updater = IncrementalUpdater(storage_path)

    # 单次检查
    result = updater.watch_once()
    print(f"检查结果: {result}")
    print(f"索引统计: {updater.index.get_stats()}")
