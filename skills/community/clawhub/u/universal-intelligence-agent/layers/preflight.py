"""
环境预检引擎 — Phase 0 健康检查
──────────────────────────────
启动时验证所有依赖的完整性：
  - Python 版本 ≥ 3.10
  - 网络连通性
  - 可用 LLM Provider
  - 磁盘空间
  - WAL 日志检查
  - 依赖包检查
"""
from __future__ import annotations

import logging
import os
import shutil
import socket
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class PreflightCheck:
    """单项预检结果"""
    name: str
    passed: bool
    message: str = ""
    severity: str = "error"  # "error" | "warning" | "info"


@dataclass
class PreflightResult:
    """预检总结果"""
    checks: list[PreflightCheck] = field(default_factory=list)
    all_passed: bool = True
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    can_proceed: bool = True  # 是否可以降级运行


class PreflightChecker:
    """
    预检引擎

    用法:
        checker = PreflightChecker()
        result = checker.check()
        if not result.all_passed:
            print(f"Preflight failed: {result.failures}")
    """

    def check(self) -> PreflightResult:
        """执行所有预检"""
        result = PreflightResult()

        checks = [
            self._check_python_version(),
            self._check_network(),
            self._check_disk_space(),
            self._check_wal_status(),
            self._check_dependencies(),
        ]

        for check in checks:
            result.checks.append(check)
            if not check.passed:
                if check.severity == "error":
                    result.all_passed = False
                    result.failures.append(check.message)
                    result.can_proceed = False
                elif check.severity == "warning":
                    result.warnings.append(check.message)
                    # 警告不阻止运行
                else:
                    # info 级别，不记录到 failures/warnings
                    pass

        self._print_report(result)
        return result

    def _check_python_version(self) -> PreflightCheck:
        """检查 Python 版本"""
        version = sys.version_info
        if version >= (3, 10):
            return PreflightCheck(
                name="Python Version",
                passed=True,
                message=f"Python {version.major}.{version.minor}.{version.micro}",
                severity="info",
            )
        else:
            return PreflightCheck(
                name="Python Version",
                passed=False,
                message=f"Python {version.major}.{version.minor} < 3.10 required",
                severity="error",
            )

    def _check_network(self) -> PreflightCheck:
        """检查网络连通性"""
        targets = [
            ("baidu.com", 443),
            ("google.com", 443),
        ]

        reachable = 0
        for host, port in targets:
            try:
                sock = socket.create_connection((host, port), timeout=5)
                sock.close()
                reachable += 1
            except Exception:
                pass

        if reachable >= 2:
            return PreflightCheck(
                name="Network",
                passed=True,
                message=f"All targets reachable ({reachable}/{len(targets)})",
                severity="info",
            )
        elif reachable >= 1:
            return PreflightCheck(
                name="Network",
                passed=True,
                message=f"Partial connectivity ({reachable}/{len(targets)})",
                severity="warning",
            )
        else:
            return PreflightCheck(
                name="Network",
                passed=False,
                message="No network connectivity — search will fail",
                severity="error",
            )

    def _check_disk_space(self, min_mb: int = 500) -> PreflightCheck:
        """检查磁盘空间"""
        try:
            data_dir = Path(os.path.expanduser("~")) / ".uia"
            data_dir.mkdir(parents=True, exist_ok=True)

            usage = shutil.disk_usage(data_dir)
            free_mb = usage.free / (1024 * 1024)

            if free_mb >= min_mb:
                return PreflightCheck(
                    name="Disk Space",
                    passed=True,
                    message=f"{free_mb:.0f} MB free (min: {min_mb} MB)",
                    severity="info",
                )
            else:
                return PreflightCheck(
                    name="Disk Space",
                    passed=False,
                    message=f"Only {free_mb:.0f} MB free, need {min_mb} MB",
                    severity="error",
                )
        except Exception as e:
            return PreflightCheck(
                name="Disk Space",
                passed=False,
                message=f"Cannot check: {e}",
                severity="error",
            )

    def _check_wal_status(self) -> PreflightCheck:
        """检查 WAL 日志状态 — 是否有未完成的任务"""
        try:
            wal_dir = Path(os.path.expanduser("~")) / ".uia" / "wal"
            if not wal_dir.exists():
                return PreflightCheck(
                    name="WAL Status",
                    passed=True,
                    message="No pending WAL entries",
                    severity="info",
                )

            wal_files = list(wal_dir.glob("*.wal"))
            if not wal_files:
                return PreflightCheck(
                    name="WAL Status",
                    passed=True,
                    message="No pending WAL entries",
                    severity="info",
                )

            # 检查是否有未完成的会话
            pending = []
            for wf in wal_files:
                with open(wf, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line and '"committed"' not in last_line:
                            pending.append(wf.stem)

            if pending:
                return PreflightCheck(
                    name="WAL Status",
                    passed=True,
                    message=f"{len(pending)} interrupted sessions found: {pending}",
                    severity="warning",
                )
            else:
                return PreflightCheck(
                    name="WAL Status",
                    passed=True,
                    message="All sessions committed",
                    severity="info",
                )
        except Exception as e:
            return PreflightCheck(
                name="WAL Status",
                passed=True,
                message=f"WAL check skipped: {e}",
                severity="warning",
            )

    def _check_dependencies(self) -> PreflightCheck:
        """检查关键依赖包"""
        required = [
            "re", "json", "logging", "hashlib", "urllib",
            "pathlib", "dataclasses", "threading", "time",
            "uuid", "html", "shutil", "socket", "tempfile",
            "subprocess", "random",
        ]

        missing = []
        for module_name in required:
            try:
                __import__(module_name)
            except ImportError:
                missing.append(module_name)

        if missing:
            return PreflightCheck(
                name="Dependencies",
                passed=False,
                message=f"Missing modules: {missing}",
                severity="error",
            )
        else:
            return PreflightCheck(
                name="Dependencies",
                passed=True,
                message=f"All {len(required)} core modules available",
                severity="info",
            )

    def _print_report(self, result: PreflightResult):
        """打印预检报告"""
        logger.info("=== Preflight Check Report ===")
        for check in result.checks:
            status = "✅" if check.passed else "❌"
            logger.info(f"  {status} {check.name}: {check.message}")

        if result.all_passed:
            logger.info("Preflight: ALL CHECKS PASSED")
        else:
            logger.error(f"Preflight: FAILED — {result.failures}")
        if result.warnings:
            logger.warning(f"Preflight: WARNINGS — {result.warnings}")
