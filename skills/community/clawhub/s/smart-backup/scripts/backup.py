#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Smart Backup - 智能备份脚本
自动感知：跳过大型文件、可下载/可编译生成的文件、临时文件和符号链接
"""

import argparse
import json
import os
import platform
import stat
import sys
import tarfile
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Windows 控制台 UTF-8 编码
if platform.system() == "Windows":
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    except (AttributeError, OSError):
        pass

# ── 默认配置 ──────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "config_directory": "",           # .openclaw 配置目录，留空自动检测
    "workspace_directory": "",        # OpenClaw 工作空间，留空自动检测
    "output_directory": "",           # 备份输出目录，留空使用默认值
    "filename_prefix": "openclaw-backup",
    "max_backups": 30,                # 保留最近 N 个，0=不限制
    "max_file_size_mb": 100,          # 超过此大小的文件单独报告（0=不限制）
    "skip_large_files": False,        # True=直接跳过超大文件，False=仅报告
    "compression_level": 6,           # gzip 压缩级别 1-9
    "excluded_extensions": [
        "log", "tmp", "pyc", "pyo", "pid", "bak",
        "swp", "swo", "cache", "lock", "db-journal", "db-wal"
    ],
    "excluded_folders": [
        # 临时/日志
        "tmp", "temp", "logs", "backup", "backups",
        # 版本控制
        ".git", ".svn", ".hg",
        # Python
        "__pycache__", ".venv", "venv", ".tox", ".pytest_cache",
        "*.egg-info", ".mypy_cache", "htmlcov",
        # Node.js
        "node_modules", ".npm", ".nvm",
        # 构建产物（可重新生成）
        "dist", "build", ".next", ".nuxt", "out", "target", "bin", "obj",
        # 包管理器缓存（可重新下载）
        ".nuget", ".cargo", ".gradle", ".m2", ".yarn", ".pnpm-store",
        # OpenClaw 特有
        "skills-backup", "skills-backup-*",
        ".browser-profile", ".browser_data",
        ".Trash", ".trash", ".clawhub",
        "flows", "completions", "delivery-queue", ".dreams",
        # IDE
        ".idea", ".vscode", ".vs", "*.code-workspace",
        # 其他缓存
        ".cache", ".dart_tool", ".flutter-plugins", ".flutter-plugins-dependencies",
    ],
    "excluded_files": [
        ".DS_Store", "Thumbs.db", "desktop.ini",
        ".env.local", ".env.development", ".env.production",
        "*.local", "*.secret", "*.key", "*.pem", "*.crt"
    ],
    "excluded_by_content": [
        # 根据文件内容特征排除（如包含特定 shebang 或 header）
    ],
    # 大型可下载文件特征（自动感知）
    "large_downloadable_patterns": [
        "*.whl", "*.tar.gz", "*.zip", "*.rar", "*.7z",
        "*.dmg", "*.exe", "*.msi", "*.pkg", "*.deb", "*.rpm",
        "*.so", "*.dll", "*.dylib", "*.a", "*.lib",
        "*.bin", "*.dat"
    ],
}

# ── 颜色输出 ──────────────────────────────────────────────────────────

_COLOR_ATTRS = ["RESET", "BOLD", "DIM", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"]

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    @classmethod
    def disable(cls):
        for attr in _COLOR_ATTRS:
            if hasattr(cls, attr):
                setattr(cls, attr, "")


if platform.system() == "Windows" and not os.environ.get("FORCE_COLOR"):
    Colors.disable()


def info(msg: str):
    print(f"{Colors.CYAN}[INFO]{Colors.RESET} {msg}")


def warn(msg: str):
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {msg}", file=sys.stderr)


def error(msg: str):
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {msg}", file=sys.stderr)


def success(msg: str):
    print(f"{Colors.GREEN}[OK]{Colors.RESET} {msg}")


def dim(msg: str):
    print(f"{Colors.DIM}{msg}{Colors.RESET}")


# ── 路径检测 ──────────────────────────────────────────────────────────

def detect_config_directory() -> Optional[Path]:
    """自动检测 .openclaw 配置目录"""
    candidates = []

    home = Path.home()
    candidates.append(home / ".openclaw")

    # Windows 常见位置
    if platform.system() == "Windows":
        candidates.append(Path(os.environ.get("USERPROFILE", "")) / ".openclaw")
        candidates.append(Path(os.environ.get("LOCALAPPDATA", "")) / "OpenClaw")
        candidates.append(Path("C:/Users") / os.environ.get("USERNAME", "") / ".openclaw")
    else:
        candidates.append(home / ".config" / "openclaw")
        candidates.append(home / ".local" / "share" / "openclaw")

    for path in candidates:
        if path.exists() and path.is_dir():
            return path.resolve()

    return None


def detect_workspace_directory() -> Optional[Path]:
    """自动检测 OpenClaw 工作空间目录"""
    candidates = []

    home = Path.home()
    candidates.append(Path("D:/Personal/OpenClaw"))
    candidates.append(home / "OpenClaw")
    candidates.append(home / "openclaw")
    candidates.append(home / "Documents" / "OpenClaw")
    candidates.append(Path("/home") / os.environ.get("USER", "") / "openclaw")

    for path in candidates:
        if path.exists() and path.is_dir():
            return path.resolve()

    return None


def detect_openclaw_command() -> Optional[Path]:
    """在 PATH 中查找 openclaw 命令"""
    import shutil
    cmd = shutil.which("openclaw") or shutil.which("openclaw.cmd") or shutil.which("openclaw.exe")
    if cmd:
        return Path(cmd).resolve()
    return None


# ── 排除规则 ──────────────────────────────────────────────────────────

class SmartExclusionFilter:
    """智能排除过滤器：支持扩展名、文件夹名、文件名和通配符"""

    def __init__(self, config: dict):
        self.exts: Set[str] = set(e.lower().lstrip(".") for e in config.get("excluded_extensions", []))
        self.folders: List[str] = [f.lower() for f in config.get("excluded_folders", [])]
        self.files: Set[str] = set(f.lower() for f in config.get("excluded_files", []))
        self.max_size = config.get("max_file_size_mb", 100) * 1024 * 1024
        self.skip_large = config.get("skip_large_files", False)
        self.downloadable_patterns: List[str] = [p.lower() for p in config.get("large_downloadable_patterns", [])]

        # 编译文件夹通配符
        self.folder_exact: Set[str] = set()
        self.folder_wildcard: List[str] = []
        for f in self.folders:
            if "*" in f:
                self.folder_wildcard.append(f)
            else:
                self.folder_exact.add(f)

        # 统计
        self.stats: Dict[str, int] = {
            "by_extension": 0,
            "by_folder": 0,
            "by_filename": 0,
            "by_symlink": 0,
            "by_size": 0,
            "by_downloadable": 0,
            "total_skipped": 0,
        }
        self.large_files: List[Tuple[str, int]] = []
        self.skipped_downloadable: List[str] = []

    def is_excluded(self, file_path: Path, relative_to: Optional[Path] = None) -> bool:
        """判断文件是否应被排除"""
        file_path = file_path.resolve()
        name = file_path.name
        name_lower = name.lower()
        ext = file_path.suffix.lower().lstrip(".")

        # 1. 符号链接/联接点
        try:
            if file_path.is_symlink() or self._is_junction(file_path):
                self.stats["by_symlink"] += 1
                self.stats["total_skipped"] += 1
                return True
        except OSError:
            pass

        # 2. 检查扩展名
        if ext and ext in self.exts:
            self.stats["by_extension"] += 1
            self.stats["total_skipped"] += 1
            return True

        # 3. 检查文件名
        if name_lower in self.files:
            self.stats["by_filename"] += 1
            self.stats["total_skipped"] += 1
            return True

        # 4. 检查路径中的文件夹
        for part in file_path.parts:
            part_lower = part.lower()
            if part_lower in self.folder_exact:
                self.stats["by_folder"] += 1
                self.stats["total_skipped"] += 1
                return True
            for pattern in self.folder_wildcard:
                if self._wildcard_match(part_lower, pattern):
                    self.stats["by_folder"] += 1
                    self.stats["total_skipped"] += 1
                    return True

        # 5. 检查大型可下载文件特征
        for pattern in self.downloadable_patterns:
            if self._wildcard_match(name_lower, pattern):
                self.stats["by_downloadable"] += 1
                self.stats["total_skipped"] += 1
                self.skipped_downloadable.append(str(file_path))
                return True

        # 6. 检查文件大小
        try:
            size = file_path.stat().st_size
            if self.max_size > 0 and size > self.max_size:
                self.large_files.append((str(file_path), size))
                self.stats["by_size"] += 1
                self.stats["total_skipped"] += 1
                if self.skip_large:
                    return True
        except OSError:
            pass

        return False

    def _is_junction(self, path: Path) -> bool:
        """Windows 联接点检测"""
        if platform.system() != "Windows":
            return False
        try:
            return path.exists() and path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT != 0
        except (AttributeError, OSError):
            return False

    def _wildcard_match(self, text: str, pattern: str) -> bool:
        """简单通配符匹配（仅支持 *）"""
        if pattern == "*":
            return True
        if pattern.startswith("*") and pattern.endswith("*"):
            return pattern[1:-1] in text
        if pattern.startswith("*"):
            return text.endswith(pattern[1:])
        if pattern.endswith("*"):
            return text.startswith(pattern[:-1])
        return text == pattern

    def print_stats(self):
        """打印排除统计"""
        s = self.stats
        info(f"排除统计: 扩展名={s['by_extension']}, 文件夹={s['by_folder']}, "
             f"文件名={s['by_filename']}, 符号链接={s['by_symlink']}, "
             f"大型文件={s['by_size']}, 可下载={s['by_downloadable']}, 总计={s['total_skipped']}")

        if self.large_files:
            info(f"发现 {len(self.large_files)} 个超过 {self.max_size // 1024 // 1024}MB 的文件:")
            for path, size in sorted(self.large_files, key=lambda x: -x[1])[:20]:
                warn(f"  {format_size(size):>10}  {path}")
            if len(self.large_files) > 20:
                dim(f"  ... 还有 {len(self.large_files) - 20} 个")

        if self.skipped_downloadable:
            info(f"跳过的可下载/可编译文件: {len(self.skipped_downloadable)} 个")


def format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


# ── 备份核心 ──────────────────────────────────────────────────────────

def collect_files(source_dirs: List[Path], filter_: SmartExclusionFilter, dry_run: bool = False) -> List[Path]:
    """收集所有需要备份的文件"""
    files: List[Path] = []
    total_size = 0

    for source_dir in source_dirs:
        if not source_dir.exists():
            warn(f"源目录不存在，跳过: {source_dir}")
            continue

        info(f"扫描目录: {source_dir}")
        count = 0
        dir_size = 0

        for root, dirs, filenames in os.walk(source_dir, followlinks=False):
            root_path = Path(root)

            # 跳过符号链接目录
            dirs_to_remove = []
            for d in dirs:
                dir_path = root_path / d
                try:
                    if dir_path.is_symlink() or filter_._is_junction(dir_path):
                        dirs_to_remove.append(d)
                        filter_.stats["by_symlink"] += 1
                except OSError:
                    dirs_to_remove.append(d)

            for d in dirs_to_remove:
                dirs.remove(d)

            # 根据排除规则过滤子目录
            dirs[:] = [d for d in dirs if not filter_._wildcard_match(d.lower(), "*") or
                       not any(filter_._wildcard_match(d.lower(), p) for p in filter_.folder_wildcard + list(filter_.folder_exact))]
            # 更精确的目录排除
            remaining = []
            for d in dirs:
                d_lower = d.lower()
                excluded = False
                if d_lower in filter_.folder_exact:
                    excluded = True
                else:
                    for pattern in filter_.folder_wildcard:
                        if filter_._wildcard_match(d_lower, pattern):
                            excluded = True
                            break
                if not excluded:
                    remaining.append(d)
            dirs[:] = remaining

            for filename in filenames:
                file_path = root_path / filename
                if filter_.is_excluded(file_path):
                    continue
                files.append(file_path)
                try:
                    size = file_path.stat().st_size
                    total_size += size
                    dir_size += size
                except OSError:
                    pass
                count += 1

        info(f"  找到 {count} 个文件 ({format_size(dir_size)})")

    info(f"共计 {len(files)} 个文件，原始大小 {format_size(total_size)}")
    return files


def create_tar_gz(
    files: List[Path],
    source_dirs: List[Path],
    output_file: Path,
    filter_: SmartExclusionFilter,
    compression: int = 6,
    dry_run: bool = False
) -> Tuple[bool, int, int]:
    """创建 tar.gz 备份文件，返回 (成功, 文件数, 写入字节数)"""

    if dry_run:
        info(f"[DRY-RUN] 将备份 {len(files)} 个文件到 {output_file}")
        filter_.print_stats()
        for f in files[:50]:
            dim(f"  {f}")
        if len(files) > 50:
            dim(f"  ... 还有 {len(files) - 50} 个文件")
        return True, len(files), 0

    output_file.parent.mkdir(parents=True, exist_ok=True)
    info(f"正在创建备份: {output_file}")

    file_count = 0
    written_bytes = 0
    errors = 0

    try:
        with tarfile.open(output_file, f"w:gz", compresslevel=compression) as tar:
            for file_path in files:
                try:
                    # 保留绝对路径（将盘符分隔符替换为下划线，如 C:\ → C_\/）
                    arcname = normalize_tar_path(file_path)
                    tar.add(file_path, arcname=arcname)
                    file_count += 1
                    written_bytes += file_path.stat().st_size

                    # 每1000个文件显示一次进度
                    if file_count % 1000 == 0:
                        info(f"  已处理 {file_count} 个文件...")

                except PermissionError as e:
                    warn(f"权限不足，跳过: {file_path} - {e}")
                    errors += 1
                except OSError as e:
                    warn(f"无法读取，跳过: {file_path} - {e}")
                    errors += 1
    except KeyboardInterrupt:
        warn("用户中断，正在清理...")
        if output_file.exists():
            output_file.unlink()
        raise
    except Exception as e:
        error(f"创建备份失败: {e}")
        if output_file.exists():
            output_file.unlink()
        return False, 0, 0

    actual_size = output_file.stat().st_size
    filter_.print_stats()
    success(f"备份完成: {output_file}")
    info(f"  文件数: {file_count}, 原始大小: {format_size(written_bytes)}, "
         f"压缩后: {format_size(actual_size)}, 压缩率: {actual_size / written_bytes * 100:.1f}%" if written_bytes > 0 else "")
    if errors > 0:
        warn(f"  跳过 {errors} 个文件（权限/读取错误）")

    return True, file_count, actual_size


def normalize_tar_path(path: Path) -> str:
    """将路径标准化为 tar 归档名，保留绝对路径"""
    abs_path = str(path.resolve())
    if len(abs_path) >= 2 and abs_path[1] == ":":
        # Windows 盘符: C:\ → C_/
        abs_path = abs_path[0] + "_/" + abs_path[2:]
    return abs_path.replace("\\", "/")


def cleanup_old_backups(output_dir: Path, prefix: str, max_backups: int):
    """清理过期备份"""
    if max_backups <= 0:
        return

    if not output_dir.exists():
        return

    pattern = f"{prefix}-*.tar.gz"
    backups = sorted(output_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)

    if len(backups) <= max_backups:
        info(f"当前 {len(backups)} 个备份，未超过限制 {max_backups}")
        return

    to_delete = backups[max_backups:]
    for file in to_delete:
        try:
            file.unlink()
            info(f"已删除过期备份: {file.name}")
        except OSError as e:
            warn(f"删除备份失败: {file.name} - {e}")


# ── 配置文件 ──────────────────────────────────────────────────────────

def get_config_path() -> Path:
    """获取配置文件路径 - 保存在技能所在文件夹"""
    # 脚本位于 scripts/backup.py，技能根目录为其父目录
    skill_dir = Path(__file__).parent.parent.resolve()
    return skill_dir / "backup.json"


def load_config(path: Path) -> dict:
    """加载配置文件"""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
            # 合并默认配置和用户配置
            config = DEFAULT_CONFIG.copy()
            config.update(user_config)
            info(f"已加载配置文件: {path}")
            return config
        except json.JSONDecodeError as e:
            warn(f"配置文件格式错误: {e}，使用默认配置")
        except Exception as e:
            warn(f"加载配置文件失败: {e}，使用默认配置")

    # 创建默认配置文件
    save_config(path, DEFAULT_CONFIG)
    info(f"已创建默认配置文件: {path}")
    return DEFAULT_CONFIG.copy()


def save_config(path: Path, config: dict):
    """保存配置文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


# ── 智能感知报告 ──────────────────────────────────────────────────────

def print_smart_report(files: List[Path], filter_: SmartExclusionFilter):
    """打印智能感知报告"""
    print()
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  OpenClaw Smart Backup - 智能感知报告{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print()

    # 文件类型分布
    ext_counts: Dict[str, int] = {}
    ext_sizes: Dict[str, int] = {}
    for f in files:
        ext = f.suffix.lower() or "(无扩展名)"
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
        try:
            ext_sizes[ext] = ext_sizes.get(ext, 0) + f.stat().st_size
        except OSError:
            pass

    info("备份文件类型分布 (Top 10):")
    for ext, count in sorted(ext_counts.items(), key=lambda x: -x[1])[:10]:
        size = format_size(ext_sizes.get(ext, 0))
        print(f"  {ext:12} {count:>6} 个  ({size})")

    print()
    info("智能排除说明:")
    print(f"  - 日志/临时文件 (.log, .tmp)            → 运行时生成，无需备份")
    print(f"  - 版本控制目录 (.git)                   → 远程已托管，无需备份")
    print(f"  - Python缓存 (__pycache__, .pyc)        → 可重新编译")
    print(f"  - Node依赖 (node_modules)               → 可通过 package.json 重新安装")
    print(f"  - 构建产物 (dist, build, .next)         → 可重新构建")
    print(f"  - 包管理器缓存 (.npm, .cargo, .gradle)  → 可重新下载")
    print(f"  - 虚拟环境 (.venv, venv)                → 可通过 requirements 重建")
    print(f"  - 浏览器数据 (.browser-profile)         → 缓存数据，体积大")
    print(f"  - 符号链接/联接点                       → 避免循环遍历")

    if filter_.large_files:
        print()
        info(f"大型文件警告 (>{filter_.max_size // 1024 // 1024}MB):")
        if filter_.skip_large:
            print(f"  已配置为跳过超大文件")
        else:
            print(f"  这些文件已包含在备份中，如不需要请在配置中排除")

    print()
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")


# ── 主函数 ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Smart Backup - 智能备份 OpenClaw 配置和工作空间",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python backup.py                          # 执行备份
  python backup.py --dry-run                # 预览将要备份的文件
  python backup.py --config custom.json     # 使用自定义配置文件
  python backup.py --output D:\\Backups      # 指定输出目录
  python backup.py --max-backups 10         # 只保留最近10个备份
        """
    )
    parser.add_argument("--config", "-c", help="配置文件路径")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--dry-run", "-n", action="store_true", help="预览模式（不实际创建备份）")
    parser.add_argument("--prefix", "-p", help="备份文件名前缀")
    parser.add_argument("--max-backups", type=int, help="保留最近 N 个备份")
    parser.add_argument("--config-dir", help="OpenClaw 配置目录 (.openclaw)")
    parser.add_argument("--workspace-dir", help="OpenClaw 工作空间目录")
    parser.add_argument("--skip-large", action="store_true", help="跳过超过大小限制的文件")
    parser.add_argument("--list-excluded", action="store_true", help="显示将被排除的文件列表")
    parser.add_argument("--no-color", action="store_true", help="禁用彩色输出")
    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    print(f"{Colors.BOLD}{Colors.CYAN}")
    print(r"   ____                   __         __________             __      ")
    print(r"  / __ \____  ___  ____  / /__  ____/ /_  __/ /_____ ______/ /______")
    print(r" / / / / __ \/ _ \/ __ \/ / _ \/ __  / / / / __/ __ `/ ___/ __/ ___/")
    print(r"/ /_/ / /_/ /  __/ / / / /  __/ /_/ / / / / /_/ /_/ (__  ) /_(__  ) ")
    print(r"\____/ .___/\___/_/ /_/_/\___/\__,_/ /_/  \__/\__,_/____/\__/____/  ")
    print(f"    /_/       {Colors.RESET}Smart Backup v1.0{Colors.BOLD}{Colors.CYAN}                                ")
    print(f"{Colors.RESET}")
    print()

    # 加载配置
    config_path = Path(args.config) if args.config else get_config_path()
    config = load_config(config_path)

    # 命令行参数覆盖配置
    if args.output:
        config["output_directory"] = args.output
    if args.prefix:
        config["filename_prefix"] = args.prefix
    if args.max_backups is not None:
        config["max_backups"] = args.max_backups
    if args.config_dir:
        config["config_directory"] = args.config_dir
    if args.workspace_dir:
        config["workspace_directory"] = args.workspace_dir
    if args.skip_large:
        config["skip_large_files"] = True

    # 自动检测目录
    config_dir = Path(config["config_directory"]) if config.get("config_directory") else None
    workspace_dir = Path(config["workspace_directory"]) if config.get("workspace_directory") else None

    if not config_dir or not config_dir.exists():
        config_dir = detect_config_directory()
        if config_dir:
            config["config_directory"] = str(config_dir)
            info(f"自动检测到配置目录: {config_dir}")
        else:
            error("无法找到 OpenClaw 配置目录，请使用 --config-dir 指定")
            sys.exit(1)

    if not workspace_dir or not workspace_dir.exists():
        workspace_dir = detect_workspace_directory()
        if workspace_dir:
            config["workspace_directory"] = str(workspace_dir)
            info(f"自动检测到工作空间: {workspace_dir}")
        else:
            warn("无法自动检测工作空间目录，仅备份配置目录")
            workspace_dir = None

    # 确定输出目录
    output_dir = Path(config.get("output_directory", "")) if config.get("output_directory") else None
    if not output_dir:
        if platform.system() == "Windows":
            output_dir = Path("D:/Personal/Archive")
        else:
            output_dir = Path.home() / "Archive"
        config["output_directory"] = str(output_dir)
        info(f"使用默认输出目录: {output_dir}")

    source_dirs = [config_dir]
    if workspace_dir:
        source_dirs.append(workspace_dir)

    info(f"备份源目录: {source_dirs}")
    info(f"输出目录: {output_dir}")
    info(f"保留备份数: {config['max_backups']}")
    info(f"文件大小限制: {config['max_file_size_mb']}MB")
    info(f"跳过超大文件: {config['skip_large_files']}")
    print()

    # 创建排除过滤器
    filter_ = SmartExclusionFilter(config)

    # 收集文件
    files = collect_files(source_dirs, filter_, dry_run=args.dry_run)

    if not files:
        error("没有可备份的文件")
        sys.exit(1)

    # 打印智能报告
    if not args.dry_run:
        print_smart_report(files, filter_)

    # 生成备份文件名
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    prefix = config.get("filename_prefix", "openclaw-backup")
    output_file = output_dir / f"{prefix}-{timestamp}.tar.gz"

    # 创建备份
    success_flag, file_count, written_bytes = create_tar_gz(
        files, source_dirs, output_file, filter_,
        compression=config.get("compression_level", 6),
        dry_run=args.dry_run
    )

    if not success_flag:
        sys.exit(1)

    # 清理过期备份
    if not args.dry_run:
        cleanup_old_backups(output_dir, prefix, config.get("max_backups", 30))

    # 保存更新后的配置（缓存检测到的路径）
    if not args.dry_run:
        save_config(config_path, config)

    print()
    if args.dry_run:
        info("DRY-RUN 完成。实际备份时将在上述位置创建文件。")
    else:
        success("备份任务完成！")


if __name__ == "__main__":
    main()
