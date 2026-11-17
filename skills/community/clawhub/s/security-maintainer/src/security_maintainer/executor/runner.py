"""
Deterministic Execution Coordinator.
Manages concurrency locking, fault tolerance, and cross-platform execution order.
"""

from __future__ import annotations
import os
import sys
import time
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from ..models import (
    ActionPlan,
    PlanAction,
    ExecutionResult,
    ActionStatus,
    EnvironmentType,
)
from .windows_runner import WindowsRunner
from .wsl_runner import WSLRunner

logger = logging.getLogger(__name__)

LOCK_FILE = Path.home() / ".security-maintainer" / "maintainer.lock"


class ConcurrencyLock:
    """Prevents simultaneous execution runs using an active PID lockfile."""

    def __init__(self, lock_path: Optional[Path] = None, timeout_seconds: int = 60):
        self.lock_path = lock_path or LOCK_FILE
        self.timeout_seconds = timeout_seconds
        self.acquired = False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        start_time = time.time()
        while time.time() - start_time < self.timeout_seconds:
            try:
                # Apertura exclusiva para crear el archivo
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w") as f:
                    f.write(f"{os.getpid()}\n{time.time()}")
                self.acquired = True
                return
            except FileExistsError:
                # Comprobar si el proceso que tiene el lock sigue vivo
                try:
                    with open(self.lock_path, "r") as f:
                        lines = f.readlines()
                        if lines:
                            pid = int(lines[0].strip())
                            # Si es el mismo proceso o el proceso ya no existe
                            if not self._is_pid_alive(pid):
                                self.lock_path.unlink(missing_ok=True)
                                continue
                except Exception:
                    pass
                time.sleep(0.1)

        raise TimeoutError(f"No se pudo adquirir el bloqueo de concurrencia en {self.lock_path}.")

    def release(self):
        if self.acquired:
            try:
                self.lock_path.unlink(missing_ok=True)
            except Exception:
                pass
            self.acquired = False

    def _is_pid_alive(self, pid: int) -> bool:
        if pid <= 0:
            return False
        if pid == os.getpid():
            return True

        if sys.platform == "win32":
            try:
                import ctypes
                from ctypes import wintypes

                kernel32 = getattr(ctypes, "windll", None)
                if kernel32 is not None:
                    k32 = kernel32.kernel32
                    SYNCHRONIZE = 0x00100000
                    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
                    WAIT_TIMEOUT = 0x00000102
                    WAIT_OBJECT_0 = 0x00000000
                    ERROR_ACCESS_DENIED = 5
                    ERROR_INVALID_PARAMETER = 87

                    handle = k32.OpenProcess(
                        PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE,
                        False,
                        wintypes.DWORD(pid),
                    )

                    if handle:
                        try:
                            wait_result = k32.WaitForSingleObject(handle, 0)
                            if wait_result == WAIT_TIMEOUT:
                                return True
                            elif wait_result == WAIT_OBJECT_0:
                                return False

                            exit_code = wintypes.DWORD()
                            if k32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                                return exit_code.value == 259  # STILL_ACTIVE
                            return True
                        finally:
                            k32.CloseHandle(handle)
                    else:
                        err = ctypes.GetLastError()
                        if err == ERROR_ACCESS_DENIED:
                            # Falta de permisos: conservar el bloqueo
                            return True
                        elif err == ERROR_INVALID_PARAMETER:
                            # Proceso inexistente
                            return False
                        else:
                            # Ante cualquier otra incertidumbre, conservar el bloqueo
                            return True
            except Exception as e:
                logger.warning("Error comprobando PID %s mediante Windows API: %s", pid, e)
                return True

        # En Unix / POSIX
        try:
            os.kill(pid, 0)
            return True
        except PermissionError:
            # Falta de permisos: el proceso existe pero no podemos enviar señales
            return True
        except (ProcessLookupError, OSError):
            return False
        except Exception:
            return True


class PlanExecutor:
    """Ejecuta ordenadamente las acciones aprobadas de un plan."""

    def __init__(
        self,
        config: Dict[str, Any],
        windows_runner: Optional[WindowsRunner] = None,
        wsl_runner: Optional[WSLRunner] = None
    ):
        self.config = config
        self.windows_runner = windows_runner or WindowsRunner(config)
        self.wsl_runner = wsl_runner or WSLRunner(config)

    def execute_plan(self, plan: ActionPlan) -> List[ExecutionResult]:
        """Ejecuta secuencialmente las acciones del plan bajo bloqueo de concurrencia."""
        results: List[ExecutionResult] = []

        with ConcurrencyLock(timeout_seconds=self.config.get("execution", {}).get("lock_timeout_seconds", 60)):
            for action in plan.actions:
                start_t = time.time()
                logger.info(f"Executing action {action.action_id}: {action.product_name} ({action.target})")

                if action.environment == EnvironmentType.WINDOWS:
                    res = self.windows_runner.execute_action(action)
                elif action.environment == EnvironmentType.WSL:
                    res = self.wsl_runner.execute_action(action)
                elif action.environment == EnvironmentType.MACOS:
                    res = self._execute_macos_action(action)
                else:
                    res = ExecutionResult(
                        action_id=action.action_id,
                        product_name=action.product_name,
                        manager=action.manager,
                        success=False,
                        exit_code=1,
                        status=ActionStatus.FAILED,
                        error_message="Environment type not supported for direct execution."
                    )

                res.duration_seconds = time.time() - start_t
                results.append(res)

                # If an action fails, log and continue with independent ones
                if not res.success:
                    logger.warning(f"Action {action.action_id} failed: {res.error_message}")

        return results

    def _execute_macos_action(self, action: PlanAction) -> ExecutionResult:
        import subprocess
        import re
        allowed_macos = {"brew", "mas", "softwareupdate"}
        dangerous_regex = re.compile(r"[;&|`$><\n\r]")

        if not action.exact_command or not isinstance(action.exact_command, list):
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=1,
                status=ActionStatus.FAILED,
                error_message="Invalid or empty command."
            )

        cmd_bin = Path(action.exact_command[0]).name.lower()
        if cmd_bin not in allowed_macos:
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=126,
                status=ActionStatus.BLOCKED_PERMISSIONS,
                error_message=f"Unauthorized package manager in macOS allowlist: {cmd_bin}"
            )

        for arg in action.exact_command:
            if not isinstance(arg, str) or dangerous_regex.search(arg):
                return ExecutionResult(
                    action_id=action.action_id,
                    product_name=action.product_name,
                    manager=action.manager,
                    success=False,
                    exit_code=126,
                    status=ActionStatus.BLOCKED_PERMISSIONS,
                    error_message=f"Dangerous metacharacter in command token: {arg}"
                )

        logger.warning(
            "[SECURITY AUDIT] Executing pre-approved macOS package update: %s",
            " ".join(action.exact_command)
        )

        try:
            cmd = list(action.exact_command)
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            success = proc.returncode == 0
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=success,
                exit_code=proc.returncode,
                status=ActionStatus.EXECUTED_VERIFIED if success else ActionStatus.FAILED,
                error_message=proc.stderr if not success else None,
                diagnostic_output=proc.stdout or proc.stderr,
                reboot_pending=action.expected_reboot
            )
        except Exception as e:
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=1,
                status=ActionStatus.FAILED,
                error_message=str(e)
            )
