#!/usr/bin/env python3
"""
SQL 拆分工具 - 断点续传模块
支持记录处理进度，中断后可以继续处理
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class CheckpointData:
    """检查点数据"""
    input_file: str
    output_dir: str
    dialect: str
    total_objects: int
    processed_objects: int
    processed_files: List[str]
    failed_objects: List[Dict[str, Any]]
    timestamp: str
    status: str  # 'in_progress', 'completed', 'failed', 'interrupted'

    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'CheckpointData':
        """从字典创建"""
        return cls(**data)


class CheckpointManager:
    """检查点管理器"""

    def __init__(self, checkpoint_dir: Optional[Path] = None):
        """
        初始化检查点管理器

        Args:
            checkpoint_dir: 检查点目录，默认为 ~/.sql_splitter_checkpoints
        """
        if checkpoint_dir is None:
            checkpoint_dir = Path.home() / ".sql_splitter_checkpoints"

        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def get_checkpoint_file(self, input_file: str) -> Path:
        """
        获取检查点文件路径

        Args:
            input_file: 输入文件路径

        Returns:
            检查点文件路径
        """
        # 使用文件路径的哈希作为文件名，避免路径过长
        file_hash = hashlib.md5(input_file.encode()).hexdigest()
        return self.checkpoint_dir / f"{file_hash}.checkpoint"

    def save_checkpoint(self, checkpoint: CheckpointData) -> bool:
        """
        保存检查点

        Args:
            checkpoint: 检查点数据

        Returns:
            是否保存成功
        """
        try:
            checkpoint_file = self.get_checkpoint_file(checkpoint.input_file)
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存检查点失败: {e}")
            return False

    def load_checkpoint(self, input_file: str) -> Optional[CheckpointData]:
        """
        加载检查点

        Args:
            input_file: 输入文件路径

        Returns:
            检查点数据，如果不存在则返回 None
        """
        try:
            checkpoint_file = self.get_checkpoint_file(input_file)
            if not checkpoint_file.exists():
                return None

            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 验证检查点文件是否匹配
            if data.get('input_file') != input_file:
                print(f"检查点文件不匹配: {data.get('input_file')} != {input_file}")
                return None

            return CheckpointData.from_dict(data)
        except Exception as e:
            print(f"加载检查点失败: {e}")
            return None

    def delete_checkpoint(self, input_file: str) -> bool:
        """
        删除检查点

        Args:
            input_file: 输入文件路径

        Returns:
            是否删除成功
        """
        try:
            checkpoint_file = self.get_checkpoint_file(input_file)
            if checkpoint_file.exists():
                checkpoint_file.unlink()
            return True
        except Exception as e:
            print(f"删除检查点失败: {e}")
            return False

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """
        列出所有检查点

        Returns:
            检查点列表
        """
        checkpoints = []

        for checkpoint_file in self.checkpoint_dir.glob("*.checkpoint"):
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    checkpoints.append({
                        'input_file': data.get('input_file'),
                        'output_dir': data.get('output_dir'),
                        'dialect': data.get('dialect'),
                        'total_objects': data.get('total_objects', 0),
                        'processed_objects': data.get('processed_objects', 0),
                        'timestamp': data.get('timestamp'),
                        'status': data.get('status'),
                        'progress': f"{data.get('processed_objects', 0)}/{data.get('total_objects', 0)}",
                        'checkpoint_file': str(checkpoint_file)
                    })
            except Exception as e:
                print(f"读取检查点失败 {checkpoint_file}: {e}")

        # 按时间排序
        checkpoints.sort(key=lambda x: x['timestamp'], reverse=True)
        return checkpoints

    def clear_old_checkpoints(self, days: int = 7) -> int:
        """
        清理旧的检查点

        Args:
            days: 保留天数

        Returns:
            删除的检查点数量
        """
        from datetime import timedelta

        cutoff_time = datetime.now() - timedelta(days=days)
        deleted_count = 0

        for checkpoint_file in self.checkpoint_dir.glob("*.checkpoint"):
            try:
                # 检查文件修改时间
                file_mtime = datetime.fromtimestamp(checkpoint_file.stat().st_mtime)
                if file_mtime < cutoff_time:
                    checkpoint_file.unlink()
                    deleted_count += 1
            except Exception as e:
                print(f"删除检查点失败 {checkpoint_file}: {e}")

        return deleted_count

    def create_checkpoint(self, input_file: str, output_dir: str,
                        dialect: str, total_objects: int) -> CheckpointData:
        """
        创建新检查点

        Args:
            input_file: 输入文件路径
            output_dir: 输出目录
            dialect: SQL方言
            total_objects: 总对象数

        Returns:
            检查点数据
        """
        return CheckpointData(
            input_file=input_file,
            output_dir=output_dir,
            dialect=dialect,
            total_objects=total_objects,
            processed_objects=0,
            processed_files=[],
            failed_objects=[],
            timestamp=datetime.now().isoformat(),
            status='in_progress'
        )

    def update_checkpoint(self, checkpoint: CheckpointData,
                        processed_file: Optional[str] = None,
                        failed_object: Optional[Dict[str, Any]] = None,
                        status: Optional[str] = None) -> CheckpointData:
        """
        更新检查点

        Args:
            checkpoint: 检查点数据
            processed_file: 已处理的文件
            failed_object: 失败的对象
            status: 状态

        Returns:
            更新后的检查点数据
        """
        if processed_file:
            checkpoint.processed_files.append(processed_file)
            checkpoint.processed_objects += 1

        if failed_object:
            checkpoint.failed_objects.append(failed_object)

        if status:
            checkpoint.status = status

        checkpoint.timestamp = datetime.now().isoformat()

        return checkpoint

    def get_resume_progress(self, input_file: str) -> Optional[Dict[str, Any]]:
        """
        获取恢复进度信息

        Args:
            input_file: 输入文件路径

        Returns:
            进度信息，如果不存在检查点则返回 None
        """
        checkpoint = self.load_checkpoint(input_file)
        if not checkpoint:
            return None

        progress = checkpoint.processed_objects / checkpoint.total_objects if checkpoint.total_objects > 0 else 0

        return {
            'input_file': checkpoint.input_file,
            'output_dir': checkpoint.output_dir,
            'dialect': checkpoint.dialect,
            'total_objects': checkpoint.total_objects,
            'processed_objects': checkpoint.processed_objects,
            'failed_objects': len(checkpoint.failed_objects),
            'progress': progress,
            'status': checkpoint.status,
            'timestamp': checkpoint.timestamp,
            'can_resume': checkpoint.status in ['in_progress', 'interrupted']
        }


def main():
    """测试函数"""
    manager = CheckpointManager()

    # 创建测试检查点
    checkpoint = manager.create_checkpoint(
        input_file="/test/input.sql",
        output_dir="/test/output",
        dialect="oracle",
        total_objects=100
    )

    # 更新检查点
    checkpoint = manager.update_checkpoint(checkpoint, processed_file="proc_test.sql")
    checkpoint = manager.update_checkpoint(checkpoint, processed_file="func_test.sql")

    # 保存检查点
    manager.save_checkpoint(checkpoint)

    # 列出检查点
    print("检查点列表:")
    for cp in manager.list_checkpoints():
        print(f"  {cp['input_file']}: {cp['progress']} ({cp['status']})")

    # 获取恢复进度
    resume_info = manager.get_resume_progress("/test/input.sql")
    if resume_info:
        print(f"\n恢复进度: {resume_info['progress']:.1%}")
        print(f"可以恢复: {resume_info['can_resume']}")

    # 删除检查点
    manager.delete_checkpoint("/test/input.sql")


if __name__ == "__main__":
    main()
