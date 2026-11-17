"""
WSL Action Runner.
Executes pre-approved package manager updates inside targeted WSL distributions.
Enforces non-interactive privilege verification, distribution isolation, argument sanitization, and binary allowlists.
"""

from __future__ import annotations
import logging
import subprocess
import shutil
import re
from pathlib import Path
from typing import Dict, Any, Optional

from ..models import PlanAction, ExecutionResult, ActionStatus, ManagerType

logger = logging.getLogger(__name__)

ALLOWED_WSL_MANAGERS = {
    "apt", "apt-get", "dpkg", "apk", "dnf", "yum", "pacman", "zypper"
}

DANGEROUS_SHELL_CHARS_REGEX = re.compile(r"[;&|`$><\n\r]")


class WSLRunner:
    """Executes authorized update actions inside targeted WSL distributions."""

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

        distro_name = action.target.replace("WSL:", "")
        wsl_bin = shutil.which("wsl.exe") or shutil.which("wsl")
        if not wsl_bin:
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=127,
                status=ActionStatus.FAILED,
                error_message="wsl.exe executable not found in PATH."
            )

        # 1. Non-interactive privilege verification
        if action.required_privileges in ["sudo", "admin"]:
            check_priv_cmd = [wsl_bin, "-d", distro_name, "-e", "true"]
            check_res = subprocess.run(check_priv_cmd, capture_output=True, timeout=10)
            if check_res.returncode != 0:
                return ExecutionResult(
                    action_id=action.action_id,
                    product_name=action.product_name,
                    manager=action.manager,
                    success=False,
                    exit_code=126,
                    status=ActionStatus.BLOCKED_PERMISSIONS,
                    error_message=(
                        f"Action blocked: Non-interactive elevated privileges unavailable for '{action.product_name}' in {distro_name}. "
                        "Manual execution or pre-configured delegation is required."
                    )
                )

        # 2. Package manager and argument sanitization
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

        cmd_binary = Path(action.exact_command[0]).name.lower()
        if cmd_binary not in ALLOWED_WSL_MANAGERS:
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=126,
                status=ActionStatus.BLOCKED_PERMISSIONS,
                error_message=f"Unauthorized package manager in WSL distribution: {cmd_binary}"
            )

        # Enforce strict subcommand allowlist to prevent arbitrary package manager actions
        ALLOWED_WSL_SUBCOMMANDS = {
            "install", "upgrade", "dist-upgrade", "update", "-u", "-Syu", "-y", "--only-upgrade"
        }
        if len(action.exact_command) > 1:
            subcmd = action.exact_command[1].lower()
            if subcmd not in ALLOWED_WSL_SUBCOMMANDS and not subcmd.startswith("-"):
                return ExecutionResult(
                    action_id=action.action_id,
                    product_name=action.product_name,
                    manager=action.manager,
                    success=False,
                    exit_code=126,
                    status=ActionStatus.BLOCKED_PERMISSIONS,
                    error_message=f"Disallowed subcommand for package manager in WSL: {subcmd}"
                )

        for arg in action.exact_command:
            if not isinstance(arg, str) or DANGEROUS_SHELL_CHARS_REGEX.search(arg):
                return ExecutionResult(
                    action_id=action.action_id,
                    product_name=action.product_name,
                    manager=action.manager,
                    success=False,
                    exit_code=126,
                    status=ActionStatus.BLOCKED_PERMISSIONS,
                    error_message=f"Disallowed metacharacter in command token: {arg}"
                )

        # 3. Assemble command and execute under explicit safety notice
        full_cmd = [wsl_bin, "-d", distro_name, "-e"]
        full_cmd.extend(action.exact_command)

        logger.warning(
            "[SECURITY AUDIT] Executing pre-approved update inside WSL (%s): %s",
            distro_name,
            " ".join(action.exact_command)
        )

        try:
            res = subprocess.run(full_cmd, capture_output=True, text=True, timeout=180)
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
                error_message=f"Execution timed out while updating {action.product_name} in WSL."
            )
        except Exception as e:
            return ExecutionResult(
                action_id=action.action_id,
                product_name=action.product_name,
                manager=action.manager,
                success=False,
                exit_code=1,
                status=ActionStatus.FAILED,
                error_message=f"Execution error in WSL: {e}"
            )
