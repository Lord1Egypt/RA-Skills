#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 容量管理器
检测 memory 目录容量，在接近满时自动触发归档

用法:
    from capacity_manager import CapacityManager
    cm = CapacityManager()
    cm.check_usage()      # 检测容量
    cm.warn_if_full()     # 超过80%警告
    cm.auto_archive_if_needed()  # 超过95%自动归档
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, Optional

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
MEMORY_MD = MEMORY_DIR / "memory.md"   # 长期记忆精选
ARCHIVE_DIR = MEMORY_DIR / "archive"   # 归档目录
DAILY_DIR = MEMORY_DIR / "daily"      # 每日日志

# 容量阈值
WARN_THRESHOLD = 0.80   # 80% 警告
CRITICAL_THRESHOLD = 0.95  # 95% 自动归档

# MEMORY.md 最大行数（经验值，可调整）
MAX_MEMORY_MD_LINES = 500
# daily/ 目录最大文件数
MAX_DAILY_FILES = 30
# archive/ 目录最大容量（MB）
MAX_ARCHIVE_SIZE_MB = 100


# ============== 容量检查器 ==============

class CapacityManager:
    """容量管理器"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.state_file = MEMORY_DIR / ".capacity_state.json"
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """加载容量状态"""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "last_check": None,
            "memory_md_lines": 0,
            "daily_file_count": 0,
            "archive_size_mb": 0.0,
            "last_warn_time": None,
            "last_archive_time": None,
        }

    def _save_state(self):
        """保存容量状态"""
        self.state["last_check"] = datetime.now().isoformat()
        try:
            self.state_file.write_text(
                json.dumps(self.state, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception:
            pass

    def _get_memory_md_info(self) -> Tuple[int, int]:
        """获取 MEMORY.md 行数和最大行数

        Returns:
            (当前行数, 最大行数)
        """
        if MEMORY_MD.exists():
            try:
                lines = len(MEMORY_MD.read_text(encoding="utf-8").splitlines())
                return lines, MAX_MEMORY_MD_LINES
            except Exception:
                pass
        return 0, MAX_MEMORY_MD_LINES

    def _get_daily_file_count(self) -> int:
        """获取 daily/ 目录文件数"""
        if DAILY_DIR.exists():
            return len([f for f in DAILY_DIR.iterdir() if f.is_file() and not f.name.startswith('.')])
        return 0

    def _get_archive_size_mb(self) -> float:
        """获取 archive/ 目录大小（MB）"""
        total = 0.0
        if ARCHIVE_DIR.exists():
            for f in ARCHIVE_DIR.rglob("*"):
                if f.is_file():
                    total += f.stat().st_size
        return total / (1024 * 1024)

    def _get_dir_file_count(self, dir_path: Path) -> int:
        """获取指定目录的文件数（递归）"""
        if not dir_path.exists():
            return 0
        return len([f for f in dir_path.rglob("*") if f.is_file() and not f.name.startswith('.')])

    def check_usage(self) -> Dict[str, any]:
        """全面检测容量使用情况

        Returns:
            容量使用报告
        """
        memory_md_lines, max_lines = self._get_memory_md_info()
        daily_count = self._get_daily_file_count()
        archive_size = self._get_archive_size_mb()

        # 计算各项使用率
        memory_md_ratio = memory_md_lines / max_lines if max_lines > 0 else 0
        daily_ratio = daily_count / MAX_DAILY_FILES if MAX_DAILY_FILES > 0 else 0
        archive_ratio = archive_size / MAX_ARCHIVE_SIZE_MB if MAX_ARCHIVE_SIZE_MB > 0 else 0

        report = {
            "timestamp": datetime.now().isoformat(),
            "memory_md": {
                "lines": memory_md_lines,
                "max_lines": max_lines,
                "ratio": round(memory_md_ratio, 3),
                "percent": round(memory_md_ratio * 100, 1),
                "status": "critical" if memory_md_ratio >= CRITICAL_THRESHOLD else "warning" if memory_md_ratio >= WARN_THRESHOLD else "ok"
            },
            "daily": {
                "count": daily_count,
                "max_count": MAX_DAILY_FILES,
                "ratio": round(daily_ratio, 3),
                "percent": round(daily_ratio * 100, 1),
                "status": "critical" if daily_ratio >= CRITICAL_THRESHOLD else "warning" if daily_ratio >= WARN_THRESHOLD else "ok"
            },
            "archive": {
                "size_mb": round(archive_size, 2),
                "max_size_mb": MAX_ARCHIVE_SIZE_MB,
                "ratio": round(archive_ratio, 3),
                "percent": round(archive_ratio * 100, 1),
                "status": "critical" if archive_ratio >= CRITICAL_THRESHOLD else "warning" if archive_ratio >= WARN_THRESHOLD else "ok"
            },
            "overall": {
                "max_ratio": max(memory_md_ratio, daily_ratio, archive_ratio),
                "status": "critical" if max(memory_md_ratio, daily_ratio, archive_ratio) >= CRITICAL_THRESHOLD else "warning" if max(memory_md_ratio, daily_ratio, archive_ratio) >= WARN_THRESHOLD else "ok"
            }
        }

        # 更新状态
        self.state["memory_md_lines"] = memory_md_lines
        self.state["daily_file_count"] = daily_count
        self.state["archive_size_mb"] = round(archive_size, 2)
        self._save_state()

        if self.verbose:
            self._print_report(report)

        return report

    def _print_report(self, report: Dict):
        """打印容量报告"""
        print("\n## 容量使用报告")
        print(f"时间: {report['timestamp'][:19]}")

        md = report["memory_md"]
        print(f"\n[MEMORY.md] {md['lines']}/{md['max_lines']} 行 ({md['percent']}%) - {md['status'].upper()}")

        daily = report["daily"]
        print(f"[daily/] {daily['count']}/{daily['max_count']} 文件 ({daily['percent']}%) - {daily['status'].upper()}")

        archive = report["archive"]
        print(f"[archive/] {archive['size_mb']}/{archive['max_size_mb']} MB ({archive['percent']}%) - {archive['status'].upper()}")

        overall = report["overall"]
        print(f"\n总体状态: {overall['status'].upper()} (最大使用率: {overall['max_ratio']*100:.1f}%)")

    def warn_if_full(self, report: Optional[Dict] = None) -> bool:
        """检查是否超过容量阈值，打印警告

        Args:
            report: 可选，已有的容量报告

        Returns:
            是否需要警告
        """
        if report is None:
            report = self.check_usage()

        needs_warn = False
        warnings = []

        for key in ["memory_md", "daily", "archive"]:
            item = report[key]
            if item["status"] == "critical":
                warnings.append(f"  [!] {key}: {item['percent']}% (超过临界值 {CRITICAL_THRESHOLD*100:.0f}%)")
                needs_warn = True
            elif item["status"] == "warning":
                warnings.append(f"  [~] {key}: {item['percent']}% (超过警告线 {WARN_THRESHOLD*100:.0f}%)")
                needs_warn = True

        if warnings:
            print("\n" + "="*50)
            print("[容量警告] memory 目录接近容量上限!")
            print("="*50)
            for w in warnings:
                print(w)
            print("建议: 运行 python3 consolidate.py --verbose 进行归档")
            print("="*50)

            # 记录警告时间
            self.state["last_warn_time"] = datetime.now().isoformat()
            self._save_state()

        return needs_warn

    def auto_archive_if_needed(self) -> Tuple[bool, str]:
        """检查是否需要自动归档

        Returns:
            (是否触发了归档, 消息)
        """
        report = self.check_usage()

        # 检查是否超过临界值
        if report["overall"]["status"] != "critical":
            return False, "容量未超过临界值，无需自动归档"

        # 检查是否在24小时内已经自动归档过
        last_archive = self.state.get("last_archive_time")
        if last_archive:
            try:
                last_time = datetime.fromisoformat(last_archive)
                hours_since = (datetime.now() - last_time).total_seconds() / 3600
                if hours_since < 24:
                    return False, f"距离上次自动归档仅 {hours_since:.1f} 小时，跳过"
            except Exception:
                pass

        # 触发归档前检查
        can_archive = False
        reasons = []

        if report["memory_md"]["status"] == "critical":
            reasons.append(f"MEMORY.md 超过 {MAX_MEMORY_MD_LINES} 行")
            can_archive = True

        if report["daily"]["status"] == "critical":
            reasons.append(f"daily/ 超过 {MAX_DAILY_FILES} 个文件")
            can_archive = True

        if report["archive"]["status"] == "critical":
            reasons.append(f"archive/ 超过 {MAX_ARCHIVE_SIZE_MB} MB")
            can_archive = True

        if not can_archive:
            return False, "容量已满但无法自动清理"

        print("\n" + "="*50)
        print("[容量管理器] 自动归档触发!")
        print("="*50)
        for r in reasons:
            print(f"  - {r}")
        print("="*50)
        print("将执行 consolidation 流程...\n")

        # 记录触发时间
        self.state["last_archive_time"] = datetime.now().isoformat()
        self._save_state()

        return True, "; ".join(reasons)

    def get_summary(self) -> str:
        """获取容量摘要（一行）"""
        report = self.check_usage()
        parts = []

        md = report["memory_md"]
        daily = report["daily"]
        archive = report["archive"]

        parts.append(f"MEMORY.md: {md['lines']}行")
        parts.append(f"daily: {daily['count']}文件")
        parts.append(f"archive: {archive['size_mb']}MB")

        overall = report["overall"]["status"]
        status_icon = "🔴" if overall == "critical" else "🟡" if overall == "warning" else "🟢"

        return f"{status_icon} [{', '.join(parts)}]"


# ============== 主程序 ==============

def main():
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 容量管理器")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--check", "-c", action="store_true", help="检查容量")
    parser.add_argument("--warn", "-w", action="store_true", help="检查并警告")
    parser.add_argument("--auto", "-a", action="store_true", help="检查并触发自动归档")
    args = parser.parse_args()

    cm = CapacityManager(verbose=args.verbose)

    if args.check:
        cm.check_usage()

    if args.warn:
        cm.warn_if_full()

    if args.auto:
        triggered, msg = cm.auto_archive_if_needed()
        print(f"自动归档: {'是' if triggered else '否'} - {msg}")

    if not (args.check or args.warn or args.auto):
        # 默认：检查 + 警告
        report = cm.check_usage()
        cm.warn_if_full(report)
        print(f"\n容量摘要: {cm.get_summary()}")


if __name__ == "__main__":
    main()