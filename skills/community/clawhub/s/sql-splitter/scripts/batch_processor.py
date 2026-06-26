#!/usr/bin/env python3
"""
SQL 拆分工具 - 批量并行处理模块
支持同时处理多个 SQL 文件，提升处理速度
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
import time

# 导入核心模块
from split_sql_v21 import split_sql_file, SQLDialect
from error_handler import SplitResult
from checkpoint import CheckpointManager, CheckpointData


@dataclass
class BatchTask:
    """批量任务"""
    input_file: str
    output_dir: str
    dialect: Optional[SQLDialect]
    options: Dict[str, any]
    status: str = "pending"  # pending, processing, completed, failed
    result: Optional[SplitResult] = None
    error: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


@dataclass
class BatchResult:
    """批量处理结果"""
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    total_files: int
    total_time: float
    tasks: List[BatchTask]
    start_time: str
    end_time: str

    def get_summary(self) -> str:
        """获取摘要"""
        lines = [
            f"批量处理完成",
            f"总任务数: {self.total_tasks}",
            f"成功: {self.completed_tasks}",
            f"失败: {self.failed_tasks}",
            f"总文件数: {self.total_files}",
            f"总耗时: {self.total_time:.2f} 秒",
        ]
        return "\n".join(lines)


class BatchProcessor:
    """批量处理器"""

    def __init__(self, max_workers: int = 4, use_checkpoint: bool = True):
        """
        初始化批量处理器

        Args:
            max_workers: 最大并发数
            use_checkpoint: 是否使用断点续传
        """
        self.max_workers = max_workers
        self.use_checkpoint = use_checkpoint
        self.checkpoint_manager = CheckpointManager() if use_checkpoint else None
        self.progress_callback: Optional[Callable[[int, int, str], None]] = None

    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        设置进度回调函数

        Args:
            callback: 回调函数，参数为 (completed, total, message)
        """
        self.progress_callback = callback

    def process_files(self, files: List[Dict[str, any]],
                     output_base_dir: str,
                     dialect: Optional[SQLDialect] = None,
                     options: Optional[Dict[str, any]] = None) -> BatchResult:
        """
        批量处理文件

        Args:
            files: 文件列表，每个元素为 {'input_file': str, 'output_dir': str}
            output_base_dir: 输出基础目录
            dialect: SQL方言
            options: 选项

        Returns:
            批量处理结果
        """
        if options is None:
            options = {}

        start_time = time.time()
        start_time_str = datetime.now().isoformat()

        # 创建任务列表
        tasks = []
        for file_info in files:
            input_file = file_info['input_file']
            output_dir = file_info.get('output_dir',
                                       str(Path(output_base_dir) / Path(input_file).stem))

            task = BatchTask(
                input_file=input_file,
                output_dir=output_dir,
                dialect=dialect,
                options=options
            )
            tasks.append(task)

        # 处理任务
        completed_count = 0
        failed_count = 0
        total_files = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_task = {}
            for task in tasks:
                future = executor.submit(self._process_single_task, task)
                future_to_task[future] = task

            # 等待任务完成
            for future in as_completed(future_to_task):
                task = future_to_task[future]

                try:
                    result = future.result()
                    task.result = result
                    task.status = "completed" if result.success else "failed"
                    task.end_time = datetime.now().isoformat()

                    if result.success:
                        completed_count += 1
                        total_files += result.total
                    else:
                        failed_count += 1
                        task.error = "处理失败"

                except Exception as e:
                    task.status = "failed"
                    task.error = str(e)
                    task.end_time = datetime.now().isoformat()
                    failed_count += 1

                completed_count += 1

                # 调用进度回调
                if self.progress_callback:
                    self.progress_callback(completed_count, len(tasks), f"处理: {Path(task.input_file).name}")

        end_time = time.time()
        end_time_str = datetime.now().isoformat()

        return BatchResult(
            total_tasks=len(tasks),
            completed_tasks=completed_count,
            failed_tasks=failed_count,
            total_files=total_files,
            total_time=end_time - start_time,
            tasks=tasks,
            start_time=start_time_str,
            end_time=end_time_str
        )

    def _process_single_task(self, task: BatchTask) -> SplitResult:
        """
        处理单个任务

        Args:
            task: 任务

        Returns:
            拆分结果
        """
        task.status = "processing"
        task.start_time = datetime.now().isoformat()

        # 检查是否有检查点
        if self.use_checkpoint and self.checkpoint_manager:
            checkpoint = self.checkpoint_manager.load_checkpoint(task.input_file)
            if checkpoint and checkpoint.status == 'completed':
                # 已完成，跳过
                task.status = "completed"
                task.end_time = datetime.now().isoformat()
                return SplitResult(
                    success=True,
                    output_dir=checkpoint.output_dir,
                    files_created=checkpoint.processed_files,
                    errors=[],
                    warnings=[],
                    stats={},
                    total=checkpoint.processed_objects,
                    dry_run=False
                )

        # 执行拆分
        result = split_sql_file(
            task.input_file,
            task.output_dir,
            dialect=task.dialect,
            verbose=task.options.get('verbose', True),
            dry_run=task.options.get('dry_run', False),
            show_progress=task.options.get('show_progress', False),
            no_merge=task.options.get('no_merge', False)
        )

        # 保存检查点
        if self.use_checkpoint and self.checkpoint_manager:
            checkpoint = self.checkpoint_manager.create_checkpoint(
                task.input_file,
                task.output_dir,
                task.dialect.value if task.dialect else "auto",
                result.total
            )
            checkpoint.status = 'completed' if result.success else 'failed'
            checkpoint.processed_files = result.files_created
            checkpoint.processed_objects = result.total
            self.checkpoint_manager.save_checkpoint(checkpoint)

        return result

    def process_directory(self, input_dir: str, output_base_dir: str,
                         pattern: str = "*.sql",
                         dialect: Optional[SQLDialect] = None,
                         options: Optional[Dict[str, any]] = None) -> BatchResult:
        """
        处理目录中的所有文件

        Args:
            input_dir: 输入目录
            output_base_dir: 输出基础目录
            pattern: 文件匹配模式
            dialect: SQL方言
            options: 选项

        Returns:
            批量处理结果
        """
        input_path = Path(input_dir)
        if not input_path.exists():
            raise ValueError(f"目录不存在: {input_dir}")

        # 查找所有匹配的文件
        files = []
        for sql_file in input_path.glob(pattern):
            files.append({
                'input_file': str(sql_file),
                'output_dir': str(Path(output_base_dir) / sql_file.stem)
            })

        if not files:
            raise ValueError(f"未找到匹配的文件: {pattern}")

        return self.process_files(files, output_base_dir, dialect, options)


def main():
    """测试函数"""
    # 创建批量处理器
    processor = BatchProcessor(max_workers=2)

    # 设置进度回调
    def progress_callback(completed, total, message):
        print(f"[{completed}/{total}] {message}")

    processor.set_progress_callback(progress_callback)

    # 测试处理单个文件
    print("测试处理单个文件:")
    files = [
        {'input_file': '/test/input.sql', 'output_dir': '/test/output'}
    ]

    try:
        result = processor.process_files(files, '/test/output')
        print(result.get_summary())
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    main()
