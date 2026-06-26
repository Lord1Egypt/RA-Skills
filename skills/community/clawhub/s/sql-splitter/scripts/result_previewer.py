#!/usr/bin/env python3
"""
SQL 拆分工具 - 结果预览和对比模块
提供可视化查看拆分结果的功能
"""

import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import difflib


@dataclass
class FileDiff:
    """文件差异"""
    file_path: str
    original_size: int
    split_size: int
    size_diff: int
    line_count: int
    object_type: Optional[str] = None
    object_name: Optional[str] = None


@dataclass
class PreviewResult:
    """预览结果"""
    original_file: str
    output_dir: str
    total_files: int
    total_size: int
    file_diffs: List[FileDiff]
    stats: Dict[str, int]


class ResultPreviewer:
    """结果预览器"""

    def __init__(self):
        """初始化预览器"""
        pass

    def preview_split_result(self, original_file: str, output_dir: str) -> PreviewResult:
        """
        预览拆分结果

        Args:
            original_file: 原始文件
            output_dir: 输出目录

        Returns:
            预览结果
        """
        original_path = Path(original_file)
        output_path = Path(output_dir)

        if not original_path.exists():
            raise ValueError(f"原始文件不存在: {original_file}")

        if not output_path.exists():
            raise ValueError(f"输出目录不存在: {output_dir}")

        # 获取原始文件信息
        original_size = original_path.stat().st_size

        # 获取拆分后的文件
        file_diffs = []
        total_size = 0
        stats = {}

        for split_file in sorted(output_path.glob("*.sql")):
            file_size = split_file.stat().st_size
            total_size += file_size

            # 计算行数
            line_count = self._count_lines(split_file)

            # 解析对象类型和名称
            object_type, object_name = self._parse_object_info(split_file)

            # 更新统计
            if object_type:
                stats[object_type] = stats.get(object_type, 0) + 1

            file_diffs.append(FileDiff(
                file_path=str(split_file),
                original_size=original_size,
                split_size=file_size,
                size_diff=file_size - original_size,
                line_count=line_count,
                object_type=object_type,
                object_name=object_name
            ))

        return PreviewResult(
            original_file=original_file,
            output_dir=output_dir,
            total_files=len(file_diffs),
            total_size=total_size,
            file_diffs=file_diffs,
            stats=stats
        )

    def _count_lines(self, file_path: Path) -> int:
        """
        计算文件行数

        Args:
            file_path: 文件路径

        Returns:
            行数
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def _parse_object_info(self, file_path: Path) -> Tuple[Optional[str], Optional[str]]:
        """
        解析对象信息

        Args:
            file_path: 文件路径

        Returns:
            (对象类型, 对象名称)
        """
        filename = file_path.stem

        # 从文件名解析
        # 格式: {type}_{name}.sql
        parts = filename.split('_', 1)
        if len(parts) == 2:
            return parts[0], parts[1]

        return None, None

    def format_preview(self, preview: PreviewResult) -> str:
        """
        格式化预览结果

        Args:
            preview: 预览结果

        Returns:
            格式化的文本
        """
        lines = [
            "=" * 80,
            "SQL 拆分结果预览",
            "=" * 80,
            f"原始文件: {preview.original_file}",
            f"输出目录: {preview.output_dir}",
            f"拆分文件数: {preview.total_files}",
            f"总大小: {self._format_size(preview.total_size)}",
            "",
            "统计信息:",
        ]

        for obj_type, count in sorted(preview.stats.items()):
            lines.append(f"  {obj_type}: {count}")

        lines.append("")
        lines.append("文件列表:")
        lines.append("-" * 80)

        for diff in preview.file_diffs:
            lines.append(f"文件: {Path(diff.file_path).name}")
            lines.append(f"  大小: {self._format_size(diff.split_size)}")
            lines.append(f"  行数: {diff.line_count}")
            if diff.object_type:
                lines.append(f"  类型: {diff.object_type}")
            if diff.object_name:
                lines.append(f"  名称: {diff.object_name}")
            lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)

    def _format_size(self, size: int) -> str:
        """
        格式化文件大小

        Args:
            size: 字节数

        Returns:
            格式化的大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

    def compare_with_original(self, original_file: str, output_dir: str) -> str:
        """
        与原始文件对比

        Args:
            original_file: 原始文件
            output_dir: 输出目录

        Returns:
            对比结果
        """
        original_path = Path(original_file)
        output_path = Path(output_dir)

        # 读取原始文件
        try:
            with open(original_path, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
        except Exception as e:
            return f"无法读取原始文件: {e}"

        # 读取所有拆分文件
        split_lines = []
        for split_file in sorted(output_path.glob("*.sql")):
            try:
                with open(split_file, 'r', encoding='utf-8') as f:
                    split_lines.extend(f.readlines())
            except Exception as e:
                return f"无法读取拆分文件 {split_file}: {e}"

        # 对比
        diff = difflib.unified_diff(
            original_lines,
            split_lines,
            fromfile=original_path.name,
            tofile=f"{output_path.name} (合并)",
            lineterm=''
        )

        diff_text = "\n".join(diff)

        if not diff_text:
            return "文件内容完全一致"

        return diff_text

    def generate_summary_table(self, preview: PreviewResult) -> str:
        """
        生成摘要表格

        Args:
            preview: 预览结果

        Returns:
            表格字符串
        """
        lines = [
            "┌" + "─" * 78 + "┐",
            "│" + " " * 20 + "SQL 拆分结果摘要" + " " * 38 + "│",
            "├" + "─" * 78 + "┤",
            f"│ 原始文件: {preview.original_file.ljust(60)} │",
            f"│ 输出目录: {preview.output_dir.ljust(60)} │",
            f"│ 拆分文件数: {str(preview.total_files).ljust(60)} │",
            f"│ 总大小: {self._format_size(preview.total_size).ljust(60)} │",
            "├" + "─" * 78 + "┤",
            "│ 统计信息:" + " " * 68 + "│",
        ]

        for obj_type, count in sorted(preview.stats.items()):
            lines.append(f"│   {obj_type}: {str(count).ljust(60)} │")

        lines.append("├" + "─" * 78 + "┤")
        lines.append("│ 文件列表:" + " " * 68 + "│")

        for diff in preview.file_diffs:
            filename = Path(diff.file_path).name
            size_str = self._format_size(diff.split_size)
            lines.append(f"│   {filename.ljust(40)} {size_str.ljust(15)} {str(diff.line_count).ljust(10)} 行 │")

        lines.append("└" + "─" * 78 + "┘")

        return "\n".join(lines)


def main():
    """测试函数"""
    previewer = ResultPreviewer()

    # 测试预览
    print("测试预览功能:")
    try:
        preview = previewer.preview_split_result(
            original_file="/test/input.sql",
            output_dir="/test/output"
        )
        print(previewer.format_preview(preview))
        print("\n")
        print(previewer.generate_summary_table(preview))
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    main()
