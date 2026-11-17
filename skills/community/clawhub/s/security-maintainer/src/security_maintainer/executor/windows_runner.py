"""
Windows Action Runner.
Executes pre-approved software updates on the Windows host environment.
Enforces privilege validation, argument sanitization, binary allowlists, and execution logging.
"""

from __future__ import annotations
import logging
import subprocess
import shutil
import ctypes
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional

from ..models import PlanAction, ExecutionResult, ActionStatus, ManagerType

logger = logging.getLogger(__name__)

ALLOWED_WINDOWS_BINARIES = {
    "winget", "winget.exe", "powershell", "powershell.exe", "cmd.exe", "msiexec", "msiexec.exe", "dism", "dism.exe"
}

# Disallow shell metacharacters in individual command tokens
DANGEROUS_SHELL_CHARS_REGEX = re.compile(r"[;&|`$><\n\r]")


def is_windows_admin() -> bool:
    """Checks if the current process holds Administrator rights in Windows."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


class WindowsRunner:
    """Executes authorized update actions on Windows with privilege and input controls."""

    def __init__(self, config: Dict[str, Any], fixture_results: Optional[Dict[str, Any]] = None):
        self.config = config
        self.fixture_results = fixture_results

    def execute_action(self, action: PlanAction) -> ExecutionResult:
        if self.fixture_results and action.action_id in self.fixture_results:
            mock = self.fixture_results[action.action_id]
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=mock.get("success", True),
                exit_code=mock.get("exit_code", 0),
                effective_version_detected=mock.get("effective_version", action.target_version),
                verification_passed=mock.get("verification_passed", True),
                reboot_pending=mock.get("reboot_pending", False),
                status=ActionStatus(mock.get("status", ActionStatus.EXECUTED_VERIFIED.value)),
                diagnostic_output=mock.get("output", "Simulated in test fixture.")
            )

        # 1. Privilege check
        if action.required_privileges == "admin":
            if not is_windows_admin():
                return ExecutionResult(
                    action_id=action.action_id,
                    product_name=action.product_name,
                    manager=action.manager,
                    success=False,
                    exit_code=126,
                    status=ActionStatus.BLOCKED_PERMISSIONS,
                    error_message=(
                        f"Action blocked / Acción bloqueada: Se requieren privilegios de Administrador para actualizar '{action.product_name}'. "
                        "OpenClaw does not perform silent elevation. Run in an elevated prompt or apply manually."
                    )
                )

        # 2. Command input and binary allowlist validation
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

        binary_name = Path(action.exact_command[0]).name.lower()
        if binary_name not in ALLOWED_WINDOWS_BINARIES:
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=126,
                status=ActionStatus.BLOCKED_PERMISSIONS,
                error_message=f"Unauthorized executable in Windows allowlist: {binary_name}"
            )

        # Verify arguments do not contain shell injection characters
        for arg in action.exact_command:
            if not isinstance(arg, str) or DANGEROUS_SHELL_CHARS_REGEX.search(arg):
                return ExecutionResult(
                    action_id=action.action_id,
                    product_name=action.product_name,
                    manager=action.manager,
                    success=False,
                    exit_code=126,
                    status=ActionStatus.BLOCKED_PERMISSIONS,
                    error_message=f"Dangerous metacharacter detected in command argument: {arg}"
                )

        # 3. User safety logging and deterministic execution
        logger.warning(
            "[SECURITY AUDIT] Executing pre-approved Windows package modification: %s",
            " ".join(action.exact_command)
        )

        try:
            res = subprocess.run(
                action.exact_command,
                capture_output=True,
                text=True,
                timeout=180
            )
            success = res.returncode == 0
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=success,
                exit_code=res.returncode,
                status=ActionStatus.EXECUTED_UNVERIFIED if success else ActionStatus.FAILED,
                diagnostic_output=res.stdout,
                error_message=res.stderr if not success else None
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=124,
                status=ActionStatus.FAILED,
                error_message=f"Execution timed out while updating {action.product_name}."
            )
        except Exception as e:
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=1,
                status=ActionStatus.FAILED,
                error_message=f"Unexpected error during execution: {e}"
            )
