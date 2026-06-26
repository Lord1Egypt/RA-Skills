#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 增量实时监控 v2 (修复版)

解决三个核心问题:
1. 写时移动冲突: 等待文件写完才移动，避免数据丢失
2. 轮询延迟: 使用 FSEvents/inotify 事件驱动
3. 文件句柄问题: 移动后创建 symlink，内容同步合并

用法:
    python3 realtime_monitor.py --daemon          # 事件驱动持续监控
    python3 realtime_monitor.py --daemon --poll  # 降级到轮询模式
    python3 realtime_monitor.py --once           # 单次检查后退出
    python3 realtime_monitor.py --status         # 查看监控状态
"""

import os
import re
import json
import time
import signal
import sys
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, Optional, Callable, Tuple
import argparse

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
DAILY_DIR = MEMORY_DIR / "daily"
STATE_FILE = MEMORY_DIR / ".monitor_state.json"

# 等待文件稳定的超时时间（秒）
FILE_STABLE_TIMEOUT = 5
# 轮询间隔（降级模式使用）
DEFAULT_POLL_INTERVAL = 3
# 内容同步检查间隔
SYNC_CHECK_INTERVAL = 10

# ============== 平台检测 ==============

def get_platform() -> str:
    """检测操作系统"""
    if sys.platform == "darwin":
        return "macos"
    elif sys.platform.startswith("linux"):
        return "linux"
    elif sys.platform == "win32":
        return "windows"
    return "unknown"


# ============== 文件状态检测 ==============

class FileStatus:
    """文件状态检测"""

    @staticmethod
    def is_file_stable(file_path: Path, stable_seconds: int = 2) -> Tuple[bool, str]:
        """检测文件是否稳定（没有正在写入）"""
        if not file_path.exists():
            return False, "文件不存在"

        try:
            stat1 = file_path.stat()
            size1 = stat1.st_size
            time.sleep(stable_seconds)
            stat2 = file_path.stat()
            size2 = stat2.st_size

            if size1 == size2:
                if stat1.st_mtime == stat2.st_mtime:
                    return True, f"文件稳定 (大小: {size1})"
                else:
                    return False, "文件 mtime 变化中"
            else:
                return False, f"文件大小变化中: {size1} -> {size2}"
        except Exception as e:
            return False, f"检测失败: {e}"

    @staticmethod
    def is_file_in_use(file_path: Path) -> bool:
        """检测文件是否被其他进程占用"""
        platform = get_platform()

        if platform == "linux":
            try:
                result = subprocess.run(
                    ["fuser", str(file_path)],
                    capture_output=True, text=True, timeout=2
                )
                return result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        elif platform == "macos":
            try:
                result = subprocess.run(
                    ["lsof", str(file_path)],
                    capture_output=True, text=True, timeout=2
                )
                return len(result.stdout.strip()) > 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        # 降级方案：通过稳定性判断
        stable, _ = FileStatus.is_file_stable(file_path, stable_seconds=1)
        return not stable

    @staticmethod
    def wait_for_file_ready(file_path: Path, timeout: int = FILE_STABLE_TIMEOUT) -> bool:
        """等待文件写入完成"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not FileStatus.is_file_in_use(file_path):
                return True
            time.sleep(0.5)
        return False


# ============== 内容同步 ==============

class ContentSync:
    """内容同步器 - 处理 OpenClaw 同时写两个位置的情况"""

    def __init__(self, memory_dir: Path, daily_dir: Path):
        self.memory_dir = memory_dir
        self.daily_dir = daily_dir

    def sync_if_needed(self, date_str: str) -> bool:
        """检查并同步内容"""
        root_file = self.memory_dir / f"{date_str}.md"
        daily_file = self.daily_dir / f"{date_str}.md"

        if root_file.exists() and daily_file.exists():
            root_content = root_file.read_text(encoding="utf-8")
            daily_content = daily_file.read_text(encoding="utf-8")

            if len(root_content) > len(daily_content):
                new_content = root_content[len(daily_content):]
                if new_content.strip():
                    daily_file.write_text(root_content, encoding="utf-8")
                    print(f"[Sync] 合并内容: {len(new_content)} 字符")
                    return True

        return False

    def create_symlink(self, date_str: str) -> bool:
        """创建 symlink 让 OpenClaw 继续写到正确位置"""
        daily_file = self.daily_dir / f"{date_str}.md"
        root_file = self.memory_dir / f"{date_str}.md"

        if daily_file.exists() and not root_file.is_symlink():
            try:
                if root_file.exists():
                    root_file.unlink()
                    print(f"[Sync] 删除根目录残留文件")

                os.symlink(daily_file, root_file)
                print(f"[Sync] 创建 symlink: {root_file.name} -> daily/")
                return True
            except OSError as e:
                print(f"[Error] 创建 symlink 失败: {e}")
                return False
        return False


# ============== 事件驱动监控 ==============

class EventMonitor:
    """事件驱动监控（使用 FSEvents/inotify）"""

    def __init__(self, watch_dir: Path, callback: Callable):
        self.watch_dir = watch_dir
        self.callback = callback
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def start(self):
        """启动事件监控"""
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print(f"[EventMonitor] 启动事件监控: {self.watch_dir}")

    def stop(self):
        """停止事件监控"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _run(self):
        """事件监控循环"""
        platform = get_platform()

        if platform == "macos":
            self._run_fsevents()
        elif platform == "linux":
            self._run_inotify()
        else:
            self._run_poll()

    def _run_fsevents(self):
        """macOS FSEvents 实现"""
        try:
            import MacOSFSEvents as fsEvents  # type: ignore
        except ImportError:
            print("[EventMonitor] 缺少 fsevents 库，降级到轮询")
            self._run_poll()
            return

        def callback(paths):
            for path in paths:
                self.callback(Path(path))

        observer = fsEvents.Observer()
        observer.schedule(fsEvents.Handler(callback=callback), str(self.watch_dir), recursive=False)
        observer.start()

        while self.running:
            time.sleep(1)

        observer.stop()

    def _run_inotify(self):
        """Linux inotify 实现"""
        try:
            import inotify.adapters  # type: ignore
        except ImportError:
            print("[EventMonitor] 缺少 inotify 库，降级到轮询")
            self._run_poll()
            return

        i = inotify.adapters.Inotify()
        i.add_watch(str(self.watch_dir))

        for event in i.event_gen():
            if not self.running:
                break
            if event is not None:
                (_, type_names, path, filename) = event
                if 'IN_CLOSE_WRITE' in type_names or 'IN_MODIFY' in type_names:
                    file_path = Path(path) / filename
                    self.callback(file_path)

    def _run_poll(self):
        """降级轮询实现"""
        last_mtime = {}

        while self.running:
            try:
                for item in self.watch_dir.iterdir():
                    if item.is_file() and not item.name.startswith('.'):
                        mtime = item.stat().st_mtime
                        if item.name in last_mtime and mtime > last_mtime[item.name]:
                            self.callback(item)
                        last_mtime[item.name] = mtime
            except Exception as e:
                print(f"[EventMonitor] 轮询异常: {e}")

            for _ in range(DEFAULT_POLL_INTERVAL):
                if not self.running:
                    break
                time.sleep(1)


# ============== 增量写入器 ==============

class IncrementalWriter:
    """增量写入器"""

    def __init__(self, daily_dir: Path):
        self.daily_dir = daily_dir
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()

    def ensure_daily_file(self, date_str: str) -> Path:
        """确保当日文件存在"""
        daily_file = self.daily_dir / f"{date_str}.md"
        if not daily_file.exists():
            daily_file.write_text(f"# {date_str}\n\n", encoding="utf-8")
        return daily_file

    def append_content(self, content: str, timestamp: str = None) -> bool:
        """追加内容到当日日志（立即刷盘）"""
        if not content.strip():
            return False

        with self.lock:
            try:
                today = datetime.now().strftime("%Y-%m-%d")
                daily_file = self.ensure_daily_file(today)
                ts = timestamp or datetime.now().strftime("%H:%M")
                entry = f"\n## {ts} - 会话追加\n\n{content.strip()}\n"

                with open(daily_file, "a", encoding="utf-8") as f:
                    f.write(entry)
                    f.flush()
                    os.fsync(f.fileno())

                return True
            except Exception as e:
                print(f"[Error] 增量写入失败: {e}")
                return False


# ============== 实时监控器 ==============

class RealtimeMonitor:
    """实时监控器 v2 - 修复版"""

    def __init__(self, memory_dir: Path, daily_dir: Path, interval: int = DEFAULT_POLL_INTERVAL):
        self.memory_dir = memory_dir
        self.daily_dir = daily_dir
        self.interval = interval
        self.running = False
        self.writer = IncrementalWriter(daily_dir)
        self.sync = ContentSync(memory_dir, daily_dir)
        self.event_monitor: Optional[EventMonitor] = None

    def is_daily_file(self, filename: str) -> bool:
        """检查是否是日期格式的日志文件"""
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}\.md$', filename))

    def is_session_file(self, filename: str) -> bool:
        """检查是否是会话文件"""
        if self.is_daily_file(filename):
            daily_file = self.daily_dir / filename
            root_file = self.memory_dir / filename
            if root_file.exists() and not daily_file.exists() and not root_file.is_symlink():
                return True
        return False

    def _extract_date(self, filename: str) -> str:
        """从文件名提取日期字符串

        避免硬编码 [:10]，正确解析 YYYY-MM-DD 格式
        """
        # 匹配日期格式：YYYY-MM-DD
        match = re.match(r'^(\d{4}-\d{2}-\d{2})', filename)
        if match:
            return match.group(1)
        # 回退方案：取前10个字符
        return filename[:10]

    def safe_move_to_daily(self, filename: str, timeout: int = FILE_STABLE_TIMEOUT) -> Tuple[bool, str]:
        """安全移动文件到 daily/

        策略:
        1. 等待文件写入完成（检测文件句柄）
        2. 移动文件
        3. 创建 symlink 保持兼容性
        4. 同步内容（如果需要）

        Returns:
            (成功标志, 消息)
            - 成功: (True, "移动成功")
            - 失败: (False, "原因")
        """
        source = self.memory_dir / filename
        dest = self.daily_dir / filename
        date_str = self._extract_date(filename)

        if not source.exists():
            return False, "源文件不存在"

        if dest.exists():
            # 目标已存在，只同步内容
            synced = self.sync.sync_if_needed(date_str)
            if synced:
                print(f"[Monitor] 已同步残留内容: {filename}")
            return True, "目标已存在，已同步内容"

        # 等待文件写入完成
        if not FileStatus.wait_for_file_ready(source, timeout=timeout):
            print(f"[Monitor] 文件被占用或超时，跳过: {filename}")
            return False, "文件被占用或超时"

        try:
            self.daily_dir.mkdir(parents=True, exist_ok=True)

            # 读取源文件内容
            content = source.read_text(encoding="utf-8")

            # 写入目标文件
            dest.write_text(content, encoding="utf-8")

            # 删除源文件
            source.unlink()

            # 创建 symlink
            self.sync.create_symlink(date_str)

            print(f"[Monitor] 安全移动: {filename} -> daily/")
            return True, "移动成功"
        except Exception as e:
            # Bug 3: 异常后打印日志，不丢失错误信息
            print(f"[Monitor] 移动失败 ({filename}): {e}")
            return False, f"移动失败: {e}"

    def scan_and_move_new(self) -> int:
        """扫描并移动新文件"""
        count = 0
        for item in self.memory_dir.iterdir():
            if item.is_file() and self.is_session_file(item.name):
                success, msg = self.safe_move_to_daily(item.name)
                if success:
                    count += 1
        return count

    def on_file_event(self, file_path: Path):
        """文件事件回调"""
        if file_path.is_file() and self.is_session_file(file_path.name):
            success, msg = self.safe_move_to_daily(file_path.name)
            if success:
                print(f"[Event] 处理文件: {file_path.name}")

    def run_once(self) -> dict:
        """执行一次检查"""
        result = {"moved_files": 0, "timestamp": datetime.now().isoformat()}
        result["moved_files"] = self.scan_and_move_new()
        return result

    def run_loop_event(self):
        """事件驱动模式"""
        print(f"[Monitor] 启动事件驱动监控...")
        self.event_monitor = EventMonitor(self.memory_dir, self.on_file_event)
        self.event_monitor.start()

        while self.running:
            time.sleep(SYNC_CHECK_INTERVAL)
            for item in self.memory_dir.iterdir():
                if self.is_session_file(item.name):
                    self.safe_move_to_daily(item.name)

        if self.event_monitor:
            self.event_monitor.stop()

    def run_loop_poll(self):
        """轮询模式（降级）"""
        print(f"[Monitor] 启动轮询监控 (间隔 {self.interval}s)...")

        while self.running:
            try:
                result = self.run_once()
                if result["moved_files"] > 0:
                    print(f"[Monitor] 本次检查: 移动了 {result['moved_files']} 个文件")
            except Exception as e:
                print(f"[Error] 监控异常: {e}")

            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)

    def run_loop(self):
        """主循环"""
        self.running = True
        platform = get_platform()

        if platform in ("macos", "linux"):
            try:
                self.run_loop_event()
            except Exception as e:
                print(f"[Monitor] 事件驱动失败，降级到轮询: {e}")
                self.run_loop_poll()
        else:
            self.run_loop_poll()

        print("[Monitor] 监控已停止")

    def stop(self):
        """停止监控"""
        self.running = False


# ============== 主程序 ==============

def status_command():
    """查看监控状态"""
    print(f"## 监控状态\n")
    print(f"memory/: {MEMORY_DIR}")
    print(f"daily/: {DAILY_DIR}")

    if MEMORY_DIR.exists():
        root_files = [f.name for f in MEMORY_DIR.iterdir()
                      if f.is_file() and not f.name.startswith('.') and f.suffix == '.md']
        if root_files:
            print(f"\n根目录日志文件 ({len(root_files)} 个):")
            for f in sorted(root_files)[:10]:
                file_path = MEMORY_DIR / f
                is_link = file_path.is_symlink()
                size = file_path.stat().st_size if file_path.exists() else 0
                link_info = " (symlink)" if is_link else ""
                print(f"  - {f} [{size} 字节]{link_info}")

    if DAILY_DIR.exists():
        daily_files = [f.name for f in DAILY_DIR.iterdir()
                       if f.is_file() and not f.name.startswith('.')]
        print(f"\ndaily/ 日志文件 ({len(daily_files)} 个):")
        for f in sorted(daily_files)[:10]:
            size = (DAILY_DIR / f).stat().st_size
            print(f"  - {f} [{size} 字节]")


def daemon_mode(interval: int, use_poll: bool = False):
    """后台监控模式"""
    monitor = RealtimeMonitor(MEMORY_DIR, DAILY_DIR, interval)

    def signal_handler(sig, frame):
        print("\n[Monitor] 收到停止信号...")
        monitor.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    DAILY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[Monitor] 实时监控已启动 (v2 修复版)")
    print(f"[Monitor] memory/: {MEMORY_DIR}")
    print(f"[Monitor] daily/: {DAILY_DIR}")
    print(f"[Monitor] 模式: {'轮询' if use_poll else '事件驱动'}")
    print(f"[Monitor] 按 Ctrl+C 停止\n")

    if use_poll:
        monitor.run_loop_poll()
    else:
        monitor.run_loop()


def once_mode():
    """单次运行模式"""
    monitor = RealtimeMonitor(MEMORY_DIR, DAILY_DIR)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[Monitor] 执行单次检查...")
    result = monitor.run_once()

    if result["moved_files"] > 0:
        print(f"[OK] 移动了 {result['moved_files']} 个文件")
    else:
        print("[OK] 没有需要移动的新文件")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 秘书式记忆系统 - 增量实时监控 v2 (修复版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
修复内容:
    1. 写时保护: 等待文件写完后才移动，避免数据丢失
    2. 事件驱动: 支持 FSEvents/inotify，零延迟响应
    3. Symlink 兼容: 移动后创建 symlink，OpenClaw 继续写到正确位置
    4. 内容同步: 如果 OpenClaw 写到两个位置，自动合并

示例:
    python3 realtime_monitor.py --daemon          # 事件驱动监控
    python3 realtime_monitor.py --daemon --poll  # 降级到轮询模式
    python3 realtime_monitor.py --once            # 单次运行
    python3 realtime_monitor.py --status          # 查看状态
        """
    )
    parser.add_argument("--daemon", "-d", action="store_true", help="持续监控模式")
    parser.add_argument("--poll", action="store_true", help="强制使用轮询模式")
    parser.add_argument("--interval", "-i", type=int, default=DEFAULT_POLL_INTERVAL, help=f"轮询间隔秒数")
    parser.add_argument("--once", "-o", action="store_true", help="单次运行后退出")
    parser.add_argument("--status", "-s", action="store_true", help="查看监控状态")
    parser.add_argument("--test", "-t", action="store_true", help="测试模式")

    args = parser.parse_args()

    if args.status:
        status_command()
        return

    if args.test:
        print("[Test] 测试文件稳定性检测...")
        test_file = MEMORY_DIR / "test_file.md"
        test_file.write_text("test content")
        stable, msg = FileStatus.is_file_stable(test_file, stable_seconds=1)
        print(f"  文件稳定性: {msg}")
        in_use = FileStatus.is_file_in_use(test_file)
        print(f"  文件占用: {in_use}")
        test_file.unlink()
        print("[OK] 测试完成")
        return

    if args.once:
        once_mode()
        return

    if args.daemon:
        daemon_mode(args.interval, use_poll=args.poll)
        return

    parser.print_help()
    print("\n[Error] 请指定运行模式: --daemon, --once, --status 或 --test")


if __name__ == "__main__":
    main()
