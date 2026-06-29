#!/usr/bin/env python3
"""
storage-clean v2: Cross-platform disk storage scanner
Scans system/user/dev directories, generates 3-tier report with copy-paste commands.
NEVER auto-deletes — read-only scanning + command output.
"""

import os
import sys
import json
import time
import platform
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Fix Windows console encoding for emoji/Unicode
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("[!] psutil not installed. Disk overview will be unavailable. Install: pip install psutil")

# ============================================================
#  OS Detection
# ============================================================
SYSTEM = platform.system()  # "Windows", "Darwin", "Linux"
IS_WIN = SYSTEM == "Windows"
IS_MAC = SYSTEM == "Darwin"
IS_LINUX = SYSTEM == "Linux"

HOME = Path.home()
USERNAME = os.environ.get("USERNAME", os.environ.get("USER", "user"))

# ============================================================
#  Path Definitions (cross-platform)
# ============================================================

def expand_path(path_str):
    """Expand env vars and user home. Returns resolved path or None."""
    try:
        expanded = os.path.expandvars(path_str)
        expanded = os.path.expanduser(expanded)
        return expanded if os.path.exists(expanded) else None
    except Exception:
        return None


def get_green_paths():
    """Return list of green (safe-to-clean) paths for current OS."""
    paths = []

    if IS_WIN:
        # System temp
        for env_var in ["TEMP", "TMP"]:
            p = os.environ.get(env_var)
            if p:
                paths.append({"path": p, "label": f"系统临时文件 ({env_var})", "desc": "系统环境变量指定的临时文件夹，可放心清理"})
        paths.append({"path": r"C:\Windows\Temp", "label": "Windows 临时文件夹", "desc": "Windows 系统临时文件"})
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\Temp"), "label": "用户临时文件", "desc": "用户临时文件夹"})

        # Browser caches
        chrome_cache = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache")
        paths.append({"path": chrome_cache, "label": "Chrome 缓存", "desc": "Chrome 浏览器缓存"})
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache"), "label": "Chrome 代码缓存", "desc": "Chrome 代码缓存"})
        edge_cache = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache")
        paths.append({"path": edge_cache, "label": "Edge 缓存", "desc": "Edge 浏览器缓存"})
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Code Cache"), "label": "Edge 代码缓存", "desc": "Edge 代码缓存"})
        paths.append({"path": os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles"), "label": "Firefox 缓存", "desc": "Firefox 浏览器缓存目录"})

        # App caches
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\bilibili"), "label": "B站客户端缓存", "desc": "B站客户端缓存（含离线视频）"})
        paths.append({"path": os.path.expandvars(r"%APPDATA%\Tencent\WeChat"), "label": "微信缓存", "desc": "微信缓存文件"})
        paths.append({"path": os.path.expandvars(r"%APPDATA%\Tencent\WXWork"), "label": "企业微信缓存", "desc": "企业微信缓存"})
        paths.append({"path": os.path.expandvars(r"%APPDATA%\Tencent\QQ"), "label": "QQ 缓存", "desc": "QQ 缓存文件"})
        paths.append({"path": os.path.expandvars(r"%APPDATA%\DingTalk"), "label": "钉钉缓存", "desc": "钉钉缓存"})
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\Lark"), "label": "飞书缓存", "desc": "飞书（Lark）缓存"})

        # Package manager caches
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\pip\cache"), "label": "pip 缓存", "desc": "Python pip 安装包缓存"})
        paths.append({"path": os.path.expandvars(r"%APPDATA%\npm-cache"), "label": "npm 缓存", "desc": "Node.js npm 缓存"})
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\Yarn\cache"), "label": "Yarn 缓存", "desc": "Yarn 包管理器缓存"})

        # IDE caches
        paths.append({"path": os.path.expandvars(r"%APPDATA%\Code\Cache"), "label": "VS Code 缓存", "desc": "VS Code 编辑器缓存"})
        paths.append({"path": os.path.expandvars(r"%APPDATA%\Code\CachedData"), "label": "VS Code CachedData", "desc": "VS Code 缓存数据"})
        jetbrains = os.path.expandvars(r"%LOCALAPPDATA%\JetBrains")
        paths.append({"path": jetbrains, "label": "JetBrains IDE 缓存", "desc": "JetBrains 系列 IDE 缓存"})

        # Thumbnails & Recycle
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Explorer"), "label": "缩略图缓存", "desc": "Windows 缩略图缓存，自动重建"})
        paths.append({"path": r"C:\$Recycle.Bin", "label": "回收站", "desc": "回收站文件，可清空", "special": "recycle"})

        # Additional Windows paths
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\INetCache"), "label": "IE/Edge 网络缓存", "desc": "Internet Explorer / 旧版 Edge 缓存"})
        paths.append({"path": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\WER"), "label": "Windows 错误报告", "desc": "Windows Error Reporting 日志"})

    else:  # macOS or Linux
        # System temp
        paths.append({"path": "/tmp", "label": "系统临时文件 (/tmp)", "desc": "系统临时目录，重启后可能清空"})
        paths.append({"path": "/var/tmp", "label": "系统临时文件 (/var/tmp)", "desc": "系统持久临时目录"})

        if IS_MAC:
            # User caches
            paths.append({"path": str(HOME / "Library/Caches"), "label": "用户缓存 (~/Library/Caches)", "desc": "用户应用缓存目录"})
            paths.append({"path": str(HOME / "Library/Logs"), "label": "用户日志 (~/Library/Logs)", "desc": "应用日志文件"})
            paths.append({"path": str(HOME / ".Trash"), "label": "废纸篓", "desc": "废纸篓文件，可清空"})

            # Browser caches (macOS)
            paths.append({"path": str(HOME / "Library/Caches/Google/Chrome"), "label": "Chrome 缓存 (Mac)", "desc": "Chrome 浏览器缓存"})
            paths.append({"path": str(HOME / "Library/Caches/com.google.Chrome"), "label": "Chrome 缓存", "desc": "Chrome 浏览器缓存"})
            paths.append({"path": str(HOME / "Library/Caches/com.microsoft.edgemac"), "label": "Edge 缓存 (Mac)", "desc": "Edge 浏览器缓存"})
            paths.append({"path": str(HOME / "Library/Caches/org.mozilla.firefox"), "label": "Firefox 缓存 (Mac)", "desc": "Firefox 浏览器缓存"})

            # Dev caches (macOS)
            paths.append({"path": str(HOME / "Library/Caches/pip"), "label": "pip 缓存", "desc": "Python pip 缓存"})
            paths.append({"path": str(HOME / "Library/Caches/Yarn"), "label": "Yarn 缓存", "desc": "Yarn 包管理器缓存"})
            paths.append({"path": str(HOME / ".npm/_cacache"), "label": "npm 缓存", "desc": "npm 缓存"})

            # Xcode
            xcode_derived = str(HOME / "Library/Developer/Xcode/DerivedData")
            paths.append({"path": xcode_derived, "label": "Xcode DerivedData", "desc": "Xcode 构建缓存"})
            sim = str(HOME / "Library/Developer/CoreSimulator")
            paths.append({"path": sim, "label": "iOS 模拟器", "desc": "iOS 模拟器数据（设备+缓存），可大幅释放空间"})

            # macOS specific
            paths.append({"path": str(HOME / "Library/Developer/Xcode/iOS DeviceSupport"), "label": "Xcode 设备支持文件", "desc": "iOS 调试符号文件"})

        if IS_LINUX:
            paths.append({"path": str(HOME / ".cache"), "label": "用户缓存 (~/.cache)", "desc": "用户应用缓存"})
            paths.append({"path": str(HOME / ".local/share/Trash"), "label": "废纸篓", "desc": "Gnome 废纸篓"})
            paths.append({"path": str(HOME / ".npm/_cacache"), "label": "npm 缓存", "desc": "npm 缓存"})
            paths.append({"path": str(HOME / ".cache/pip"), "label": "pip 缓存", "desc": "Python pip 缓存"})

    return paths


def get_yellow_paths():
    """Return list of yellow (confirm-first) paths for current OS."""
    paths = []

    # Downloads & Desktop (cross-platform)
    paths.append({"path": str(HOME / "Downloads"), "label": "下载文件夹", "desc": "下载的安装包、文档等，可能包含重要文件"})
    paths.append({"path": str(HOME / "Desktop"), "label": "桌面", "desc": "桌面文件，可能包含重要快捷方式和文件"})

    if IS_WIN:
        paths.append({"path": str(HOME / "Documents"), "label": "文档", "desc": "Windows 文档文件夹（仅展示大文件）"})
        paths.append({"path": str(HOME / "Videos"), "label": "视频", "desc": "Windows 视频文件夹"})

    if IS_MAC:
        paths.append({"path": str(HOME / "Documents"), "label": "文档", "desc": "macOS 文档文件夹（仅展示大文件）"})
        paths.append({"path": str(HOME / "Movies"), "label": "影片", "desc": "macOS 影片文件夹"})

    if IS_LINUX:
        paths.append({"path": str(HOME / "Documents"), "label": "文档", "desc": "文档文件夹（仅展示大文件）"})

    return paths


def get_red_paths():
    """Return list of red (never-delete) paths for current OS."""
    if IS_WIN:
        return [
            {"path": r"C:\Windows\System32", "label": "Windows 系统文件 (System32)", "desc": "核心系统文件，删除会导致系统崩溃"},
            {"path": r"C:\Windows\SysWOW64", "label": "Windows 系统文件 (SysWOW64)", "desc": "核心系统文件"},
            {"path": r"C:\Program Files", "label": "已安装程序 (Program Files)", "desc": "已安装程序目录"},
            {"path": r"C:\Program Files (x86)", "label": "已安装程序 (Program Files x86)", "desc": "32位已安装程序目录"},
            {"path": r"C:\Windows", "label": "Windows 系统目录", "desc": "整个 Windows 目录"},
        ]
    elif IS_MAC:
        return [
            {"path": "/System", "label": "macOS 系统文件", "desc": "macOS 核心系统"},
            {"path": "/bin", "label": "系统二进制文件", "desc": "核心系统工具"},
            {"path": "/sbin", "label": "系统管理二进制文件", "desc": "系统管理工具"},
            {"path": "/usr", "label": "Unix 系统资源", "desc": "Unix 系统资源目录"},
            {"path": "/etc", "label": "系统配置", "desc": "系统配置文件"},
        ]
    else:  # Linux
        return [
            {"path": "/etc", "label": "系统配置", "desc": "系统配置文件"},
            {"path": "/usr", "label": "Unix 系统资源", "desc": "系统程序和数据"},
            {"path": "/boot", "label": "启动文件", "desc": "内核和引导文件"},
            {"path": "/lib", "label": "系统库", "desc": "共享系统库"},
            {"path": "/sbin", "label": "系统管理工具", "desc": "系统管理二进制文件"},
            {"path": "/bin", "label": "系统二进制文件", "desc": "核心系统工具"},
        ]


def get_dev_project_roots():
    """Get common development project root directories. Auto-discovers .git repos."""
    roots = []
    common_dirs = [
        HOME / "projects",
        HOME / "dev",
        HOME / "code",
        HOME / "workspace",
        HOME / "src",
        HOME / "WorkBuddy",
        HOME / "Documents" / "GitHub",
        HOME / "git",
        HOME / "repos",
    ]

    for d in common_dirs:
        if d.exists():
            roots.append(str(d))

    # Auto-discover: scan Desktop + home top-level for .git dirs
    for scan_root in [HOME / "Desktop", HOME]:
        if not scan_root.exists():
            continue
        try:
            for item in scan_root.iterdir():
                if item.is_dir() and not item.name.startswith('.') and (item / ".git").exists():
                    p = str(item)
                    if p not in roots:
                        roots.append(p)
        except (OSError, PermissionError):
            continue

    # Also check D: drive for projects (common on Windows)
    if IS_WIN:
        d_drive = Path("D:/")
        if d_drive.exists():
            try:
                for item in d_drive.iterdir():
                    if item.is_dir() and not item.name.startswith('.') and (item / ".git").exists():
                        p = str(item)
                        if p not in roots:
                            roots.append(p)
            except (OSError, PermissionError):
                pass

    return roots


# ============================================================
#  Helper functions
# ============================================================

def get_folder_size(path, max_depth=None, current_depth=0):
    """Calculate folder size in bytes. Returns (size_bytes, file_count)."""
    total_size = 0
    file_count = 0
    try:
        for entry in os.scandir(path):
            if max_depth is not None and current_depth >= max_depth:
                break
            try:
                if entry.is_file(follow_symlinks=False):
                    total_size += entry.stat().st_size
                    file_count += 1
                elif entry.is_dir(follow_symlinks=False):
                    sub_size, sub_count = get_folder_size(entry.path, max_depth, current_depth + 1)
                    total_size += sub_size
                    file_count += sub_count
            except (OSError, PermissionError):
                continue
    except (OSError, PermissionError):
        pass
    return total_size, file_count


def get_file_size_quick(filepath):
    """Get single file size."""
    try:
        return os.path.getsize(filepath)
    except (OSError, PermissionError):
        return 0


def format_size(bytes_val):
    """Format bytes to human readable string."""
    if bytes_val == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"


def format_count(n):
    """Format file count."""
    if n < 1000:
        return str(n)
    return f"{n:,}"


def generate_clean_command(path, method="recycle"):
    """Generate platform-appropriate clean command."""
    escaped = path.replace('"', '\\"')

    if method == "recycle":
        if IS_WIN:
            return f'Remove-Item -Path "{escaped}" -Recurse -Force -ErrorAction SilentlyContinue'
        else:
            return f'rm -rf "{escaped}"   # 彻底删除；安全方式：mv "{escaped}" ~/.Trash/'

    elif method == "delete":
        if IS_WIN:
            return f'Remove-Item -Path "{escaped}" -Recurse -Force -ErrorAction SilentlyContinue'
        else:
            return f'rm -rf "{escaped}"'

    elif method == "open":
        if IS_WIN:
            return f'explorer "{escaped}"'
        elif IS_MAC:
            return f'open "{escaped}"'
        else:
            return f'xdg-open "{escaped}"'

    return f'# No command for: {path}'


def generate_shell_hint():
    """Return a shell type hint for command display."""
    if IS_WIN:
        return "PowerShell"
    else:
        return "bash"


# ============================================================
#  Scanning functions
# ============================================================

def scan_paths(path_defs, color, min_size_mb=1):
    """Generic path scanner. Returns list of results."""
    results = []
    min_size = min_size_mb * 1024 * 1024

    for item in path_defs:
        path = item.get("path")
        if not path or not os.path.exists(path):
            continue
        try:
            size, count = get_folder_size(path)
            if size < min_size:
                continue
            result = {
                "label": item["label"],
                "path": path,
                "size": size,
                "size_fmt": format_size(size),
                "file_count": count,
                "count_fmt": format_count(count),
                "desc": item.get("desc", ""),
                "color": color,
            }

            if color == "green":
                result["cmd_recycle"] = generate_clean_command(path, "recycle")
                result["cmd_delete"] = generate_clean_command(path, "delete")
                result["shell_type"] = generate_shell_hint()
                if item.get("special") == "recycle":
                    result["special"] = "recycle"
                    if IS_WIN:
                        result["cmd_recycle"] = 'Clear-RecycleBin -Force'
                        result["cmd_delete"] = 'rd /s /q C:\\$Recycle.Bin'

            elif color == "yellow":
                result["cmd_open"] = generate_clean_command(path, "open")
                result["cmd_delete"] = generate_clean_command(path, "delete")
                result["shell_type"] = generate_shell_hint()
                result["needs_confirmation"] = True

            elif color == "red":
                result["do_not_delete"] = True

            results.append(result)
        except Exception:
            continue

    return sorted(results, key=lambda x: x["size"], reverse=True)


def scan_large_files(directories=None, min_size_mb=500):
    """Scan for large files (>min_size_mb MB) in given directories."""
    if directories is None:
        directories = [str(HOME)]

    results = []
    min_size = min_size_mb * 1024 * 1024
    seen = set()
    cutoff_time = time.time()

    for root_dir in directories:
        if not os.path.exists(root_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=False):
            # Skip hidden and system directories
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in
                          ('node_modules', '__pycache__', 'dist', 'build', '.next', '.git',
                           'System Volume Information', '$Recycle.Bin')]
            # Limit depth
            depth = dirpath[len(root_dir):].count(os.sep)
            if depth > 5:
                dirnames[:] = []
                continue

            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                try:
                    size = get_file_size_quick(fpath)
                    if size >= min_size and fpath not in seen:
                        seen.add(fpath)
                        mtime = os.path.getmtime(fpath)
                        age_days = (cutoff_time - mtime) / 86400
                        results.append({
                            "path": fpath,
                            "size": size,
                            "size_fmt": format_size(size),
                            "age_days": round(age_days),
                            "ext": os.path.splitext(fname)[1].lower() or "(无扩展名)",
                        })
                except (OSError, PermissionError):
                    continue

    return sorted(results, key=lambda x: x["size"], reverse=True)[:30]


def scan_old_files(directories=None, min_age_days=90, min_size_mb=100):
    """Scan for old, large files (>min_age_days, >min_size_mb)."""
    if directories is None:
        directories = [str(HOME / "Downloads"), str(HOME / "Desktop"), str(HOME / "Documents")]

    results = []
    min_size = min_size_mb * 1024 * 1024
    cutoff_time = time.time() - (min_age_days * 86400)
    seen = set()

    for root_dir in directories:
        if not os.path.exists(root_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=False):
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
            depth = dirpath[len(root_dir):].count(os.sep)
            if depth > 4:
                dirnames[:] = []
                continue

            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                try:
                    size = get_file_size_quick(fpath)
                    mtime = os.path.getmtime(fpath)
                    if size >= min_size and mtime < cutoff_time and fpath not in seen:
                        seen.add(fpath)
                        age_days = round((time.time() - mtime) / 86400)
                        results.append({
                            "path": fpath,
                            "size": size,
                            "size_fmt": format_size(size),
                            "age_days": age_days,
                            "last_modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d"),
                        })
                except (OSError, PermissionError):
                    continue

    return sorted(results, key=lambda x: x["size"], reverse=True)[:20]


def scan_dev_artifacts(project_roots=None):
    """Scan for build artifacts in development projects."""
    if project_roots is None:
        project_roots = get_dev_project_roots()

    if not project_roots:
        return []

    artifacts = {
        "node_modules": {"label": "node_modules", "desc": "Node.js 依赖，删除后需 npm install"},
        "__pycache__": {"label": "__pycache__", "desc": "Python 编译缓存，删除后会自动重建"},
        "dist": {"label": "构建输出 (dist)", "desc": "项目构建输出，删除后需重新构建"},
        "build": {"label": "构建输出 (build)", "desc": "项目构建输出，删除后需重新构建"},
        ".next": {"label": "Next.js 构建 (.next)", "desc": "Next.js 构建输出，删除后需重新构建"},
        "out": {"label": "静态导出 (out)", "desc": "静态导出输出"},
        "target": {"label": "Maven/Gradle 构建 (target)", "desc": "Java 项目构建输出"},
        ".turbo": {"label": "Turborepo 缓存 (.turbo)", "desc": "Turborepo 构建缓存"},
        "venv": {"label": "Python 虚拟环境 (venv)", "desc": "Python 虚拟环境，删除后需重建"},
        ".venv": {"label": "Python 虚拟环境 (.venv)", "desc": "Python 虚拟环境，删除后需重建"},
        ".mypy_cache": {"label": "Mypy 缓存", "desc": "Python 类型检查缓存"},
        ".pytest_cache": {"label": "pytest 缓存", "desc": "测试缓存"},
        ".ruff_cache": {"label": "Ruff 缓存", "desc": "Ruff linter 缓存"},
    }

    found = defaultdict(lambda: {"size": 0, "count": 0, "paths": []})

    for proj_root in project_roots:
        if not os.path.exists(proj_root):
            continue
        for dirpath, dirnames, _ in os.walk(proj_root, followlinks=False):
            depth = 0 if proj_root == dirpath else dirpath[len(proj_root):].count(os.sep)
            if depth > 4:
                dirnames[:] = []
                continue

            for d in dirnames[:]:
                if d in artifacts:
                    full_path = os.path.join(dirpath, d)
                    try:
                        size, count = get_folder_size(full_path)
                        found[d]["size"] += size
                        found[d]["count"] += count
                        found[d]["paths"].append(full_path)
                    except Exception:
                        pass
                    # Don't recurse into these
                    dirnames.remove(d)

    results = []
    for pattern, data in found.items():
        if data["size"] < 1024 * 1024:
            continue
        info = artifacts[pattern]
        paths_str = "; ".join(data["paths"][:3])
        if len(data["paths"]) > 3:
            paths_str += f" ... 等 {len(data['paths'])} 个目录"

        results.append({
            "label": info["label"],
            "desc": info["desc"],
            "size": data["size"],
            "size_fmt": format_size(data["size"]),
            "file_count": data["count"],
            "count_fmt": format_count(data["count"]),
            "color": "yellow",
            "path": paths_str,
            "paths": data["paths"],
            "multi_path": True,
            "needs_confirmation": True,
            "cmd_open": generate_clean_command(data["paths"][0], "open") if data["paths"] else "",
            "shell_type": generate_shell_hint(),
        })

    return sorted(results, key=lambda x: x["size"], reverse=True)


def scan_docker():
    """Check Docker disk usage if Docker is installed."""
    try:
        result = subprocess.run(
            ["docker", "system", "df", "--format", "json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        items = []

        # Images
        images = data.get("Images", [])
        if images:
            total_img_size = sum(img.get("Size", 0) for img in images)
            items.append({
                "label": "Docker 镜像",
                "desc": "Docker 镜像占用（docker image prune 可清理未使用镜像）",
                "size": total_img_size,
                "size_fmt": format_size(total_img_size),
                "color": "yellow",
                "needs_confirmation": True,
                "cmd_delete": "docker image prune -a",
                "shell_type": generate_shell_hint(),
            })

        # Containers
        containers = data.get("Containers", [])
        if containers:
            total_ctr_size = sum(ctr.get("Size", 0) for ctr in containers)
            items.append({
                "label": "Docker 容器",
                "desc": "Docker 容器占用（docker container prune 可清理已停止容器）",
                "size": total_ctr_size,
                "size_fmt": format_size(total_ctr_size),
                "color": "yellow",
                "needs_confirmation": True,
                "cmd_delete": "docker container prune",
                "shell_type": generate_shell_hint(),
            })

        # Volumes
        volumes = data.get("Volumes", [])
        if volumes:
            total_vol_size = sum(vol.get("Size", 0) for vol in volumes)
            items.append({
                "label": "Docker 卷",
                "desc": "Docker 数据卷占用（docker volume prune 可清理未使用卷）",
                "size": total_vol_size,
                "size_fmt": format_size(total_vol_size),
                "color": "yellow",
                "needs_confirmation": True,
                "cmd_delete": "docker volume prune",
                "shell_type": generate_shell_hint(),
            })

        # Build cache
        build_cache_size = data.get("BuildCache", [{}])[0].get("Size", 0) if data.get("BuildCache") else 0
        if build_cache_size > 0:
            items.append({
                "label": "Docker 构建缓存",
                "desc": "Docker 构建缓存（docker builder prune 清理）",
                "size": build_cache_size,
                "size_fmt": format_size(build_cache_size),
                "color": "green",
                "cmd_recycle": "docker builder prune",
                "cmd_delete": "docker builder prune -a",
                "shell_type": generate_shell_hint(),
            })

        return items
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return []
    except Exception:
        return []


# ============================================================
#  Disk info
# ============================================================

def get_disk_info():
    """Get disk usage information using psutil."""
    if not HAS_PSUTIL:
        return []

    partitions = psutil.disk_partitions()
    disks = []
    for part in partitions:
        # Skip CD-ROM, empty fstype, snap loop devices
        if 'cdrom' in part.opts or part.fstype == '' or 'snap' in part.device:
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
                "total_fmt": format_size(usage.total),
                "used_fmt": format_size(usage.used),
                "free_fmt": format_size(usage.free),
            })
        except PermissionError:
            continue
    return disks


# ============================================================
#  Report generation
# ============================================================

def generate_html_report(all_data):
    """Generate interactive HTML report."""
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reports")
    reports_dir = os.path.normpath(reports_dir)
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(reports_dir, f"storage_report_{timestamp}.html")
    json_path = os.path.splitext(report_path)[0] + ".json"

    # Write JSON
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(all_data, jf, ensure_ascii=False, indent=2)

    # Read template
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "report_template.html")
    template_path = os.path.normpath(template_path)

    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        html_content = _get_inline_template()

    # Inject data
    html_content = html_content.replace("{{REPORT_DATA}}", json.dumps(all_data, ensure_ascii=False))
    html_content = html_content.replace("{{GENERATED_AT}}", all_data.get("generated_at", ""))
    html_content = html_content.replace("{{SYSTEM}}", all_data.get("system", "Unknown"))
    json_rel = os.path.relpath(json_path, reports_dir)
    html_content = html_content.replace("{{REPORT_JSON_PATH}}", json_rel)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return report_path, json_path


def _get_inline_template():
    """Minimal fallback HTML template."""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>存储清理报告</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .section { margin: 20px 0; }
        .item { border: 1px solid #ddd; padding: 12px; margin: 8px 0; border-radius: 8px; }
        .green { border-left: 4px solid #28a745; }
        .yellow { border-left: 4px solid #ffc107; }
        .red { border-left: 4px solid #dc3545; }
        .cmd { background: #1e1e1e; color: #d4d4d4; padding: 8px 12px; border-radius: 6px; font-family: monospace; font-size: 12px; margin: 8px 0; word-break: break-all; }
        .btn { padding: 6px 14px; border: none; border-radius: 6px; cursor: pointer; font-size: 12px; margin: 4px; }
        .btn-copy { background: #6c757d; color: white; }
        .btn-copy.copied { background: #28a745; }
    </style>
</head>
<body>
    <h1>存储清理报告</h1>
    <p>{{GENERATED_AT}} | {{SYSTEM}}</p>
    <div id="app">报告数据加载中...</div>
    <script>
        const D = {{REPORT_DATA}};
        let html = '';
        D.green.forEach(i => {
            html += `<div class="item green"><strong>${i.label}</strong> (${i.size_fmt})<br>${i.desc}<br><div class="cmd">${i.cmd_recycle||''}</div></div>`;
        });
        D.yellow.forEach(i => {
            html += `<div class="item yellow"><strong>${i.label}</strong> (${i.size_fmt})<br>${i.desc}<br><div class="cmd">${i.cmd_delete||''}</div></div>`;
        });
        D.red.forEach(i => {
            html += `<div class="item red"><strong>${i.label}</strong> (${i.size_fmt})<br>${i.desc}</div>`;
        });
        document.getElementById('app').innerHTML = html || '<p>未发现需要清理的项目</p>';
    </script>
</body>
</html>"""


# ============================================================
#  Main
# ============================================================

def main():
    print("=" * 60)
    print("🧹 storage-clean v2.0 — 磁盘空间盘点")
    print(f"   系统: {SYSTEM} | 用户: {USERNAME}")
    print("=" * 60)

    # 1. Disk info
    print("\n📊 获取磁盘信息...")
    disks = get_disk_info()
    if disks:
        for d in disks:
            pct = d['percent']
            icon = "🔴" if pct > 90 else "🟡" if pct > 75 else "🟢"
            print(f"  {icon} {d['device']} ({d['mountpoint']}) — {pct}% 已用 ({d['used_fmt']} / {d['total_fmt']})")
    else:
        print("  ⚠️  psutil 未安装，跳过磁盘总览")

    # 2. Green paths
    print("\n🟢 扫描「立即清」路径...")
    green = scan_paths(get_green_paths(), "green", min_size_mb=1)
    print(f"  找到 {len(green)} 项可立即清理")
    for item in green[:5]:
        print(f"    {item['label']}: {item['size_fmt']}")

    # 3. Yellow paths
    print("\n🟡 扫描「确认后清」路径...")
    yellow = scan_paths(get_yellow_paths(), "yellow", min_size_mb=10)
    print(f"  找到 {len(yellow)} 项需确认后清理")
    for item in yellow[:5]:
        print(f"    {item['label']}: {item['size_fmt']}")

    # 4. Red paths
    print("\n🔴 扫描「保留」路径...")
    red = scan_paths(get_red_paths(), "red", min_size_mb=0)
    print(f"  找到 {len(red)} 项重要文件（不提供删除命令）")

    # 5. Large files
    print("\n📦 扫描大文件 (>500MB)...")
    large_files = scan_large_files(min_size_mb=500)
    print(f"  找到 {len(large_files)} 个大文件")
    total_large = sum(f['size'] for f in large_files)
    print(f"  总占用: {format_size(total_large)}")

    # 6. Old files
    print("\n📅 扫描旧文件 (>90天未修改, >100MB)...")
    old_files = scan_old_files(min_age_days=90, min_size_mb=100)
    print(f"  找到 {len(old_files)} 个旧文件")
    total_old = sum(f['size'] for f in old_files)
    print(f"  总占用: {format_size(total_old)}")

    # 7. Dev artifacts
    print("\n🔨 扫描开发项目构建产物...")
    dev_artifacts = scan_dev_artifacts()
    print(f"  找到 {len(dev_artifacts)} 类构建产物")
    for item in dev_artifacts[:5]:
        print(f"    {item['label']}: {item['size_fmt']} ({len(item.get('paths', []))} 个目录)")

    # 8. Docker
    print("\n🐳 检查 Docker 磁盘占用...")
    docker_items = scan_docker()
    print(f"  找到 {len(docker_items)} 项 Docker 占用")

    # Compile all data
    all_data = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system": SYSTEM,
        "hostname": platform.node(),
        "user": USERNAME,
        "python_version": platform.python_version(),
        "disks": disks,
        "green": green,
        "yellow": yellow,
        "red": red,
        "large_files": large_files,
        "old_files": old_files,
        "dev_artifacts": dev_artifacts,
        "docker": docker_items,
        "total_green_size": sum(x["size"] for x in green),
        "total_yellow_size": sum(x["size"] for x in yellow),
        "total_large_file_size": total_large,
        "total_old_file_size": total_old,
        "total_dev_artifact_size": sum(x["size"] for x in dev_artifacts),
        "shell_type": generate_shell_hint(),
    }

    # Generate report
    print("\n📝 生成 HTML 报告...")
    report_path, json_path = generate_html_report(all_data)
    print(f"  报告: {report_path}")
    print(f"  数据: {json_path}")

    # Output for parent process
    print(f"\nREPORT:{report_path}")
    print(f"JSON:{json_path}")

    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{report_path}")
        print("  已自动打开浏览器")
    except Exception:
        pass

    # Summary
    print("\n" + "=" * 60)
    print("✅ 扫描完成！")
    print(f"   🟢 立即清: {len(green)} 项, {format_size(all_data['total_green_size'])}")
    print(f"   🟡 确认后清: {len(yellow)} 项, {format_size(all_data['total_yellow_size'])}")
    print(f"   🔴 保留: {len(red)} 项")
    print(f"   📦 大文件: {len(large_files)} 个, {format_size(total_large)}")
    print(f"   📅 旧文件: {len(old_files)} 个, {format_size(total_old)}")
    print(f"   🔨 构建产物: {len(dev_artifacts)} 类, {format_size(all_data['total_dev_artifact_size'])}")
    print(f"\n💡 打开报告，复制命令到终端执行。Agent 不会代为删除。")
    print("=" * 60)


if __name__ == "__main__":
    main()
