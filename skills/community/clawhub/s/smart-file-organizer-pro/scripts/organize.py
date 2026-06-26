#!/usr/bin/env python3
"""
智能文件整理助手 Pro v2.0
增强版文件整理工具，支持多模式预设、进度显示、操作历史等
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional
import concurrent.futures
import threading

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
    UNDERLINE = '\033[4m'

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
        Colors.UNDERLINE = ''

# 检测是否支持彩色输出
if not sys.stdout.isatty() or os.name == 'nt':
    Colors.disable()

class ProgressBar:
    """简单的进度条显示"""

    def __init__(self, total: int, width: int = 50):
        self.total = total
        self.width = width
        self.current = 0
        self.lock = threading.Lock()

    def update(self, n: int = 1):
        with self.lock:
            self.current += n
            self._display()

    def _display(self):
        if self.total == 0:
            return

        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = '█' * filled + '░' * (self.width - filled)
        sys.stdout.write(f'\r[{bar}] {percent:.1%} ({self.current}/{self.total})')
        sys.stdout.flush()

    def finish(self):
        with self.lock:
            print()  # 换行

class SmartFileOrganizerPro:
    """智能文件整理助手 Pro"""

    # 预设模式配置
    PRESETS = {
        'simple': {'分类': True, '重命名': False, '去重': False, '归档': False},
        'standard': {'分类': True, '重命名': True, '去重': True, '归档': False},
        'deep': {'分类': True, '重命名': True, '去重': True, '归档': True},
        'archive': {'分类': False, '重命名': False, '去重': False, '归档': True}
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config = self._load_default_config()
        self.stats = {
            "total_files": 0,
            "organized_files": 0,
            "renamed_files": 0,
            "duplicates_found": 0,
            "duplicates_removed": 0,
            "errors": 0,
            "skipped": 0,
            "start_time": datetime.now(),
            "end_time": None
        }
        self.log = []
        self.progress_bar: Optional[ProgressBar] = None
        self.lock = threading.Lock()
        self.file_hashes = {}
        self.duplicates_cache = {}

        # 加载用户配置
        if config_path:
            self._load_user_config(config_path)

    def _load_default_config(self) -> dict:
        """加载默认配置"""
        config_path = Path(__file__).parent.parent / "config.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # 如果配置文件不存在，返回最小配置
            return {
                "version": "2.0.0",
                "mode": "standard",
                "分类设置": {},
                "重命名规则": {"启用": True},
                "归档设置": {"启用": False},
                "重复文件检测": {"启用": True},
                "安全设置": {
                    "预览模式": False,
                    "自动备份": True,
                    "跳过系统文件": True,
                    "跳过隐藏文件": True,
                    "最大文件大小MB": 1024
                },
                "性能设置": {
                    "最大工作线程": 4,
                    "显示进度": True
                },
                "输出设置": {
                    "详细程度": "normal",
                    "彩色输出": True,
                    "生成报告": True
                }
            }

    def _load_user_config(self, config_path: str) -> bool:
        """加载用户配置文件"""
        config_file = Path(config_path)
        if not config_file.exists():
            self.print_error(f"配置文件不存在: {config_path}")
            return False

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                self._deep_update(self.config, user_config)
            self.print_success(f"配置文件加载成功: {config_path}")
            return True
        except json.JSONDecodeError as e:
            self.print_error(f"配置文件格式错误: {e}")
            return False
        except Exception as e:
            self.print_error(f"配置文件读取失败: {e}")
            return False

    def _deep_update(self, base: dict, update: dict):
        """深度更新字典"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value

    def print_header(self, text: str):
        """打印标题"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'━' * 50}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  {text}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'━' * 50}{Colors.ENDC}\n")

    def print_success(self, text: str):
        """打印成功消息"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

    def print_error(self, text: str):
        """打印错误消息"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

    def print_warning(self, text: str):
        """打印警告消息"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

    def print_info(self, text: str):
        """打印信息消息"""
        print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

    def get_file_category(self, filepath: Path) -> Tuple[str, str]:
        """获取文件分类"""
        suffix = filepath.suffix.lower()

        for category_name, category_config in self.config.get("分类设置", {}).items():
            if isinstance(category_config, dict) and "扩展名" in category_config:
                if suffix in category_config["扩展名"]:
                    folder = category_config.get("文件夹", category_name)
                    icon = category_config.get("图标", "📁")
                    return folder, icon

        return "Others", "📁"

    def calculate_file_hash(self, filepath: Path, chunk_size: int = 8192) -> Optional[str]:
        """计算文件哈希值"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            with self.lock:
                self.log_error(f"计算哈希失败 {filepath}: {e}")
            return None

    def is_duplicate(self, filepath: Path, file_hash: str) -> bool:
        """检查是否为重复文件"""
        with self.lock:
            if file_hash in self.file_hashes:
                return True
            self.file_hashes[file_hash] = str(filepath)
        return False

    def generate_new_filename(self, filepath: Path, category: str, index: int) -> str:
        """生成新文件名"""
        if not self.config["重命名规则"]["启用"]:
            return filepath.name

        stat = filepath.stat()
        created_date = datetime.fromtimestamp(stat.st_ctime)

        # 格式化日期
        date_format = self.config["重命名规则"].get("日期格式", "YYYYMMDD")
        date_str = created_date.strftime("%Y%m%d")
        time_str = created_date.strftime("%H%M%S")

        # 选择命名模式
        if category == "Pictures":
            pattern = self.config["重命名规则"].get("图片模式", "IMG_{YYYYMMDD}_{序号}")
        elif category == "Videos":
            pattern = self.config["重命名规则"].get("视频模式", "VID_{YYYYMMDD}_{序号}")
        elif category == "Documents":
            pattern = self.config["重命名规则"].get("文档模式", "DOC_{标题}_{YYYYMMDD}")
            # 提取标题
            title = self._extract_title(filepath.stem)
        else:
            pattern = self.config["重命名规则"].get("通用模式", "FILE_{YYYYMMDD}_{序号}")

        # 替换模板变量
        new_name = pattern
        new_name = new_name.replace("{YYYYMMDD}", date_str)
        new_name = new_name.replace("{YYYY}", str(created_date.year))
        new_name = new_name.replace("{MM}", f"{created_date.month:02d}")
        new_name = new_name.replace("{DD}", f"{created_date.day:02d}")
        new_name = new_name.replace("{HHMMSS}", time_str)
        new_name = new_name.replace("{序号}", f"{index:04d}")

        if "{标题}" in pattern:
            new_name = new_name.replace("{标题}", title[:30])

        return new_name + filepath.suffix

    def _extract_title(self, filename: str) -> str:
        """从文件名提取标题"""
        # 移除常见前缀和后缀
        prefixes = ["copy", "副本", "new", "latest", "final", "draft"]
        suffixes = ["v1", "v2", "version", "old", "new", "temp"]

        title = filename
        # 移除数字序列
        title = re.sub(r'\d+', '', title)
        # 移除特殊字符
        title = re.sub(r'[_-]+', ' ', title)
        # 移除常见前后缀
        words = title.lower().split()
        words = [w for w in words if w not in prefixes + suffixes]
        title = ' '.join(words)
        # 首字母大写
        title = title.title() if title else "Document"

        return title if title.strip() else "File"

    def create_archive_structure(self, base_path: Path, file_date: datetime) -> Path:
        """创建归档目录结构"""
        date_format = self.config["归档设置"].get("日期格式", "YYYY/MM/DD")

        # 转换日期格式
        archive_path = date_format
        archive_path = archive_path.replace("YYYY", str(file_date.year))
        archive_path = archive_path.replace("MM", f"{file_date.month:02d}")
        archive_path = archive_path.replace("DD", f"{file_date.day:02d}")

        full_path = base_path / "Archive" / archive_path
        return full_path

    def is_file_safe(self, filepath: Path) -> bool:
        """检查文件是否安全可处理"""
        # 跳过备份目录
        if "Backup" in filepath.parts or ".history" in filepath.parts:
            return False

        # 跳过系统文件
        if self.config["安全设置"]["跳过系统文件"]:
            system_files = [".DS_Store", "Thumbs.db", "desktop.ini", ".git"]
            if filepath.name.lower() in system_files:
                return False

        # 跳过隐藏文件
        if self.config["安全设置"]["跳过隐藏文件"] and filepath.name.startswith("."):
            return False

        # 检查文件大小
        try:
            max_size = self.config["安全设置"]["最大文件大小MB"]
            file_size_mb = filepath.stat().st_size / (1024 * 1024)
            if file_size_mb > max_size:
                with self.lock:
                    self.stats["skipped"] += 1
                    self.print_warning(f"跳过大文件: {filepath.name} ({file_size_mb:.1f}MB)")
                return False
        except:
            pass

        return True

    def backup_file(self, filepath: Path, backup_dir: Path) -> Optional[Path]:
        """备份文件"""
        try:
            backup_path = backup_dir / filepath.name
            counter = 1
            while backup_path.exists():
                stem = filepath.stem
                backup_path = backup_dir / f"{stem}_{counter}{filepath.suffix}"
                counter += 1

            shutil.copy2(filepath, backup_path)
            return backup_path
        except Exception as e:
            with self.lock:
                self.log_error(f"备份失败 {filepath}: {e}")
            return None

    def process_file(self, filepath: Path, base_path: Path, mode: dict,
                     preview: bool) -> bool:
        """处理单个文件"""
        if not self.is_file_safe(filepath):
            return False

        try:
            # 计算哈希（用于重复检测）
            file_hash = None
            if mode["去重"] and self.config["重复文件检测"]["启用"]:
                file_hash = self.calculate_file_hash(filepath)
                if file_hash and self.is_duplicate(filepath, file_hash):
                    with self.lock:
                        self.stats["duplicates_found"] += 1
                        self.log_operation(f"发现重复: {filepath.name}")

                        # 处理重复文件
                        if not preview:
                            action = self.config["重复文件检测"].get("处理方式", "move")
                            if action == "delete":
                                filepath.unlink()
                                self.stats["duplicates_removed"] += 1
                            elif action == "move":
                                dup_dir = base_path / "Duplicates"
                                dup_dir.mkdir(exist_ok=True)
                                shutil.move(str(filepath), str(dup_dir / filepath.name))
                    return True

            # 获取分类
            category, icon = self.get_file_category(filepath)

            # 归档模式
            if mode["归档"] and self.config["归档设置"]["启用"]:
                stat = filepath.stat()
                file_date = datetime.fromtimestamp(stat.st_ctime)
                target_dir = self.create_archive_structure(base_path, file_date)

                if not preview:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    target_path = target_dir / filepath.name
                else:
                    target_path = target_dir / filepath.name

                if preview:
                    with self.lock:
                        self.log_operation(f"[预览] {filepath.name} → Archive/{file_date.strftime('%Y/%m/%d')}/")
                else:
                    # 备份
                    if self.config["安全设置"]["自动备份"]:
                        backup_dir = base_path / "Backup"
                        backup_dir.mkdir(exist_ok=True)
                        self.backup_file(filepath, backup_dir)

                    # 移动文件
                    shutil.move(str(filepath), str(target_path))
                    with self.lock:
                        self.stats["organized_files"] += 1
                        self.log_operation(f"移动: {filepath.name} → Archive/{file_date.strftime('%Y/%m/%d')}/")

                return True

            # 分类模式
            if mode["分类"]:
                target_dir = base_path / category

                # 生成新文件名
                new_filename = filepath.name
                if mode["重命名"] and self.config["重命名规则"]["启用"]:
                    with self.lock:
                        new_filename = self.generate_new_filename(
                            filepath, category, self.stats["organized_files"] + 1
                        )
                        self.stats["renamed_files"] += 1

                target_path = target_dir / new_filename

                # 处理文件名冲突
                if target_path.exists() and target_path != filepath:
                    counter = 1
                    stem = target_path.stem
                    while target_path.exists():
                        target_path = target_dir / f"{stem}_copy{counter}{filepath.suffix}"
                        counter += 1

                if preview:
                    with self.lock:
                        self.log_operation(f"[预览] {icon} {filepath.name} → {category}/{new_filename}")
                else:
                    # 创建目标目录
                    target_dir.mkdir(exist_ok=True)

                    # 备份
                    if self.config["安全设置"]["自动备份"]:
                        backup_dir = base_path / "Backup"
                        backup_dir.mkdir(exist_ok=True)
                        self.backup_file(filepath, backup_dir)

                    # 移动文件
                    shutil.move(str(filepath), str(target_path))
                    with self.lock:
                        self.stats["organized_files"] += 1
                        self.log_operation(f"{icon} 移动: {filepath.name} → {category}/{new_filename}")

                return True

        except Exception as e:
            with self.lock:
                self.stats["errors"] += 1
                self.log_error(f"处理失败 {filepath}: {e}")
            return False

        return False

    def scan_directory(self, directory_path: Path) -> List[Path]:
        """扫描目录获取所有文件"""
        files = []
        try:
            for item in directory_path.rglob("*"):
                if item.is_file():
                    files.append(item)
        except Exception as e:
            self.print_error(f"扫描目录失败: {e}")
        return files

    def organize_directory(self, directory_path: str, mode: str = "standard",
                          preview: bool = False, verbose: bool = False) -> bool:
        """整理目录"""
        # 打印标题
        self.print_header("🗂️ 智能文件整理助手 Pro v2.0")

        try:
            dir_path = Path(directory_path).resolve()
        except Exception as e:
            self.print_error(f"路径解析失败: {e}")
            return False

        if not dir_path.exists():
            self.print_error(f"目录不存在: {dir_path}")
            return False

        if not dir_path.is_dir():
            self.print_error(f"路径不是目录: {dir_path}")
            return False

        # 获取模式配置
        mode_config = self.PRESETS.get(mode, self.PRESETS['standard'])

        # 打印配置信息
        print(f"{Colors.OKCYAN}📁 目标目录:{Colors.ENDC} {dir_path}")
        print(f"{Colors.OKCYAN}📋 整理模式:{Colors.ENDC} {mode.upper()}")
        print(f"{Colors.OKCYAN}⚙️  预览模式:{Colors.ENDC} {'是' if preview else '否'}")
        print(f"{Colors.OKCYAN}🔄 功能配置:{Colors.ENDC}")
        for key, value in mode_config.items():
            status = f"{Colors.OKGREEN}启用{Colors.ENDC}" if value else f"{Colors.WARNING}禁用{Colors.ENDC}"
            print(f"   • {key}: {status}")
        print()

        # 扫描文件
        print(f"{Colors.OKCYAN}⏳ 正在扫描文件...{Colors.ENDC}")
        files = self.scan_directory(dir_path)
        self.stats["total_files"] = len(files)

        print(f"{Colors.OKGREEN}✓ 扫描完成{Colors.ENDC}")
        print(f"   总文件数: {len(files)}")
        print()

        # 分类统计
        category_count = defaultdict(int)
        for f in files:
            cat, _ = self.get_file_category(f)
            category_count[cat] += 1

        if verbose:
            print(f"{Colors.OKCYAN}📊 文件分类统计:{Colors.ENDC}")
            for cat, count in sorted(category_count.items()):
                icon = "📁"
                for cat_config in self.config.get("分类设置", {}).values():
                    if isinstance(cat_config, dict) and cat_config.get("文件夹") == cat:
                        icon = cat_config.get("图标", "📁")
                        break
                print(f"   {icon} {cat}: {count} 个文件")
            print()

        # 创建进度条
        if self.config["性能设置"]["显示进度"] and not preview:
            self.progress_bar = ProgressBar(len(files))

        # 处理文件
        print(f"{Colors.OKCYAN}⏳ 开始整理...{Colors.ENDC}\n")

        use_threads = self.config["性能设置"]["最大工作线程"] > 1

        if use_threads and not preview:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.config["性能设置"]["最大工作线程"]
            ) as executor:
                futures = [
                    executor.submit(self.process_file, f, dir_path, mode_config, preview)
                    for f in files
                ]
                for future in concurrent.futures.as_completed(futures):
                    if self.progress_bar:
                        self.progress_bar.update(1)
        else:
            for f in files:
                self.process_file(f, dir_path, mode_config, preview)
                if self.progress_bar:
                    self.progress_bar.update(1)

        if self.progress_bar:
            self.progress_bar.finish()

        self.stats["end_time"] = datetime.now()

        # 打印总结
        self.print_summary(preview)

        # 保存历史
        if not preview:
            self._save_history(dir_path, mode)

        return True

    def print_summary(self, preview: bool):
        """打印整理总结"""
        print()
        print(f"{Colors.BOLD}{'━' * 50}{Colors.ENDC}")
        print(f"{Colors.BOLD}📊 整理完成总结{Colors.ENDC}")
        print(f"{Colors.BOLD}{'━' * 50}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}📁 总文件数:{Colors.ENDC} {self.stats['total_files']}")
        print(f"{Colors.OKGREEN}✓ 已整理:{Colors.ENDC} {self.stats['organized_files']}")
        print(f"{Colors.WARNING}📝 已重命名:{Colors.ENDC} {self.stats['renamed_files']}")
        print(f"{Colors.WARNING}🔍 发现重复:{Colors.ENDC} {self.stats['duplicates_found']}")
        print(f"{Colors.WARNING}🗑️  移除重复:{Colors.ENDC} {self.stats['duplicates_removed']}")
        print(f"{Colors.FAIL}✗ 错误数:{Colors.ENDC} {self.stats['errors']}")
        print(f"{Colors.OKCYAN}⏭️  跳过数:{Colors.ENDC} {self.stats['skipped']}")

        # 计算耗时
        if self.stats["end_time"]:
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
            print(f"{Colors.OKCYAN}⏰ 耗时:{Colors.ENDC} {duration:.2f} 秒")

        print(f"{Colors.BOLD}{'━' * 50}{Colors.ENDC}")

        if preview:
            print(f"\n{Colors.WARNING}💡 这是预览模式，未执行实际操作{Colors.ENDC}")
            print(f"{Colors.WARNING}   要执行整理，请移除 --preview 参数{Colors.ENDC}")

    def log_operation(self, message: str):
        """记录操作"""
        if self.config["输出设置"]["详细程度"] == "verbose":
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"  [{timestamp}] {message}")

        self.log.append(message)

    def log_error(self, message: str):
        """记录错误"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        error_msg = f"[{timestamp}] ✗ {message}"
        self.log.append(error_msg)
        if self.config["输出设置"]["详细程度"] in ["verbose", "normal"]:
            print(f"  {Colors.FAIL}{error_msg}{Colors.ENDC}")

    def _save_history(self, directory: Path, mode: str):
        """保存操作历史"""
        try:
            history_dir = directory / ".history"
            history_dir.mkdir(exist_ok=True)

            history_file = history_dir / f"organize_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            history_data = {
                "timestamp": datetime.now().isoformat(),
                "mode": mode,
                "stats": self.stats,
                "log": self.log,
                "config": {
                    "mode": mode,
                    "rename": self.config["重命名规则"]["启用"],
                    "deduplicate": self.config["重复文件检测"]["启用"]
                }
            }

            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)

            # 生成报告
            if self.config["输出设置"]["生成报告"]:
                self._generate_report(directory)

        except Exception as e:
            self.print_error(f"保存历史失败: {e}")

    def _generate_report(self, directory: Path):
        """生成整理报告"""
        try:
            report_dir = directory / "Reports"
            report_dir.mkdir(exist_ok=True)

            report_file = report_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("智能文件整理助手 Pro - 整理报告\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"模式: {self.config.get('mode', 'standard')}\n\n")
                f.write("统计信息:\n")
                f.write("-" * 30 + "\n")
                for key, value in self.stats.items():
                    if key != "start_time" and key != "end_time":
                        f.write(f"{key}: {value}\n")

                f.write("\n操作日志:\n")
                f.write("-" * 30 + "\n")
                for entry in self.log[-100:]:  # 最多保存100条
                    f.write(f"{entry}\n")

            self.print_success(f"报告已保存: {report_file}")

        except Exception as e:
            self.print_error(f"生成报告失败: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="智能文件整理助手 Pro v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  简洁模式:   python3 organize.py --path . --mode simple
  标准模式:   python3 organize.py --path . --mode standard
  深度模式:   python3 organize.py --path . --mode deep
  归档模式:   python3 organize.py --path ~/Pictures --mode archive
  预览模式:   python3 organize.py --path . --mode standard --preview
  自定义配置: python3 organize.py --path . --config my_config.json
        """
    )

    parser.add_argument("--path", default=".", help="要整理的目录路径（默认：当前目录）")
    parser.add_argument("--mode", choices=['simple', 'standard', 'deep', 'archive'],
                       default='standard', help="整理模式（默认：standard）")
    parser.add_argument("--preview", action="store_true", help="预览模式，不实际执行")
    parser.add_argument("--config", help="自定义配置文件路径")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")

    args = parser.parse_args()

    # 创建整理器
    organizer = SmartFileOrganizerPro(args.config)

    # 执行整理
    success = organizer.organize_directory(
        directory_path=args.path,
        mode=args.mode,
        preview=args.preview,
        verbose=args.verbose
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
