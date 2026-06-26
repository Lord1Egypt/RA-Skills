#!/usr/bin/env python3
"""
目录分析脚本
分析目录内容并提供智能整理建议
"""

import os
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple

# ANSI 颜色代码
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def disable():
        Colors.HEADER = ''
        Colors.OKBLUE = ''
        Colors.OKCYAN = ''
        Colors.OKGREEN = ''
        Colors.WARNING = ''
        Colors.FAIL = ''
        Colors.ENDC = ''
        Colors.BOLD = ''

if not sys.stdout.isatty() or os.name == 'nt':
    Colors.disable()


class DirectoryAnalyzer:
    """目录分析器"""

    # 默认文件分类
    FILE_CATEGORIES = {
        '图片': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.raw', '.heic', '.tiff'},
        '文档': {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.rtf'},
        '视频': {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v', '.webm'},
        '音频': {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma'},
        '压缩包': {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'},
        '代码': {'.py', '.js', '.java', '.cpp', '.c', '.h', '.html', '.css', '.json', '.xml', '.php'},
        '可执行': {'.exe', '.msi', '.app', '.dmg', '.deb', '.rpm', '.apk'},
    }

    def __init__(self, directory_path: str):
        self.directory = Path(directory_path).resolve()
        self.files = []
        self.file_info = defaultdict(lambda: {
            'count': 0,
            'total_size': 0,
            'files': []
        })
        self.duplicates = defaultdict(list)
        self.size_distribution = Counter()

    def scan_directory(self) -> bool:
        """扫描目录"""
        if not self.directory.exists():
            print(f"{Colors.FAIL}目录不存在: {self.directory}{Colors.ENDC}")
            return False

        if not self.directory.is_dir():
            print(f"{Colors.FAIL}路径不是目录: {self.directory}{Colors.ENDC}")
            return False

        print(f"{Colors.OKCYAN}正在扫描目录: {self.directory}{Colors.ENDC}")

        try:
            for item in self.directory.rglob("*"):
                if item.is_file():
                    self.files.append(item)
                    self._analyze_file(item)
        except Exception as e:
            print(f"{Colors.FAIL}扫描失败: {e}{Colors.ENDC}")
            return False

        print(f"{Colors.OKGREEN}扫描完成: 找到 {len(self.files)} 个文件{Colors.ENDC}")
        return True

    def _analyze_file(self, filepath: Path):
        """分析单个文件"""
        try:
            # 获取文件大小
            size = filepath.stat().st_size
            self.size_distribution[self._get_size_category(size)] += 1

            # 获取文件分类
            category = self._get_file_category(filepath)
            self.file_info[category]['count'] += 1
            self.file_info[category]['total_size'] += size
            self.file_info[category]['files'].append(filepath)

            # 检测可能的重复（基于文件名和大小）
            key = f"{filepath.name}_{size}"
            self.duplicates[key].append(filepath)

        except Exception as e:
            pass  # 忽略无法读取的文件

    def _get_file_category(self, filepath: Path) -> str:
        """获取文件分类"""
        suffix = filepath.suffix.lower()
        for category, extensions in self.FILE_CATEGORIES.items():
            if suffix in extensions:
                return category
        return '其他'

    def _get_size_category(self, size: int) -> str:
        """获取文件大小分类"""
        mb = size / (1024 * 1024)
        if mb < 0.1:
            return '小文件 (<100KB)'
        elif mb < 1:
            return '小文件 (100KB-1MB)'
        elif mb < 10:
            return '中文件 (1-10MB)'
        elif mb < 100:
            return '大文件 (10-100MB)'
        else:
            return '超大文件 (>100MB)'

    def generate_report(self):
        """生成分析报告"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  目录分析报告{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'━' * 60}{Colors.ENDC}\n")

        # 总体统计
        print(f"{Colors.OKCYAN}📊 总体统计:{Colors.ENDC}")
        print(f"   总文件数: {len(self.files)}")

        total_size = sum(info['total_size'] for info in self.file_info.values())
        print(f"   总大小: {self._format_size(total_size)}")
        print()

        # 文件分类统计
        print(f"{Colors.OKCYAN}📁 文件分类:{Colors.ENDC}")
        for category, info in sorted(self.file_info.items(),
                                     key=lambda x: x[1]['count'],
                                     reverse=True):
            percentage = (info['count'] / len(self.files) * 100) if self.files else 0
            print(f"   • {category}: {info['count']} 个 "
                  f"({percentage:.1f}%) - {self._format_size(info['total_size'])}")
        print()

        # 文件大小分布
        print(f"{Colors.OKCYAN}📏 文件大小分布:{Colors.ENDC}")
        for size_cat, count in sorted(self.size_distribution.items(),
                                      key=lambda x: x[1],
                                      reverse=True):
            percentage = (count / len(self.files) * 100) if self.files else 0
            bar_length = int(percentage / 2)
            bar = '█' * bar_length + '░' * (50 - bar_length)
            print(f"   [{bar}] {size_cat}: {count} ({percentage:.1f}%)")
        print()

        # 智能建议
        self._generate_suggestions()

        # 重复文件检测
        self._check_duplicates()

    def _generate_suggestions(self):
        """生成智能建议"""
        print(f"{Colors.BOLD}{Colors.HEADER}💡 智能建议:{Colors.ENDC}")

        suggestions = []

        # 检查是否有大量图片
        image_count = self.file_info.get('图片', {}).get('count', 0)
        if image_count > 100:
            suggestions.append({
                'type': 'archive',
                'message': f'检测到 {image_count} 个图片文件，建议使用归档模式按日期整理',
                'command': 'python3 organize.py --path . --mode archive --date-format YYYY/MM/DD'
            })

        # 检查是否有大量文档
        doc_count = self.file_info.get('文档', {}).get('count', 0)
        if doc_count > 50:
            suggestions.append({
                'type': 'organize',
                'message': f'检测到 {doc_count} 个文档文件，建议使用标准模式整理',
                'command': 'python3 organize.py --path . --mode standard'
            })

        # 检查是否有大文件
        large_file_count = self.size_distribution.get('超大文件 (>100MB)', 0)
        if large_file_count > 0:
            suggestions.append({
                'type': 'warning',
                'message': f'检测到 {large_file_count} 个超大文件(>100MB)，请谨慎处理',
                'command': None
            })

        # 检查文件总数
        if len(self.files) > 1000:
            suggestions.append({
                'type': 'performance',
                'message': f'文件数量较多({len(self.files)}个)，建议使用深度模式并启用进度显示',
                'command': 'python3 organize.py --path . --mode deep --verbose'
            })

        # 检查是否有特定类型文件需要特殊处理
        archive_count = self.file_info.get('压缩包', {}).get('count', 0)
        if archive_count > 10:
            suggestions.append({
                'type': 'custom',
                'message': f'检测到 {archive_count} 个压缩包，建议先解压再整理',
                'command': None
            })

        # 显示建议
        if not suggestions:
            print(f"   {Colors.WARNING}暂无特别建议，使用标准模式即可{Colors.ENDC}")
        else:
            for i, suggestion in enumerate(suggestions, 1):
                icon = {
                    'archive': '📅',
                    'organize': '🗂️',
                    'warning': '⚠️',
                    'performance': '⚡',
                    'custom': '💡'
                }.get(suggestion['type'], 'ℹ️')

                print(f"   {icon} {suggestion['message']}")
                if suggestion['command']:
                    print(f"      {Colors.OKCYAN}$ {suggestion['command']}{Colors.ENDC}")

        print()

    def _check_duplicates(self):
        """检查可能的重复文件"""
        potential_duplicates = [files for files in self.duplicates.values()
                               if len(files) > 1]

        if potential_duplicates:
            print(f"{Colors.BOLD}{Colors.HEADER}🔍 可能的重复文件:{Colors.ENDC}")
            print(f"   检测到 {len(potential_duplicates)} 组可能重复的文件")
            print(f"   (基于文件名和大小判断)")

            # 显示前5组
            for i, files in enumerate(potential_duplicates[:5], 1):
                if len(files) > 1:
                    filename = files[0].name
                    locations = [f.parent.name for f in files]
                    print(f"   {i}. {filename}")
                    print(f"      位置: {', '.join(locations)}")

            if len(potential_duplicates) > 5:
                print(f"   ... 还有 {len(potential_duplicates) - 5} 组")

            print()
            print(f"   {Colors.OKCYAN}建议: 运行去重操作{Colors.ENDC}")
            print(f"   {Colors.OKCYAN}$ python3 organize.py --path . --mode deep --deduplicate{Colors.ENDC}")
        else:
            print(f"{Colors.OKGREEN}✓ 未发现明显重复文件{Colors.ENDC}")

        print()

    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="目录分析 - 分析目录内容并提供智能整理建议",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  分析当前目录: python3 analyze.py
  分析指定目录: python3 analyze.py --path ~/Downloads
  输出JSON格式: python3 analyze.py --path . --json
        """
    )

    parser.add_argument("--path", default=".", help="要分析的目录路径（默认：当前目录）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")

    args = parser.parse_args()

    analyzer = DirectoryAnalyzer(args.path)

    if not analyzer.scan_directory():
        sys.exit(1)

    if args.json:
        # TODO: 实现JSON输出
        print("JSON输出功能开发中...")
    else:
        analyzer.generate_report()


if __name__ == "__main__":
    main()
