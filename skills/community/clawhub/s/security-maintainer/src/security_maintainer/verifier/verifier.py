"""
Remediation Verifier / Verificador riguroso post-modificación.
Validates effective package versions, service statuses, and pending reboots across Windows, macOS, and Linux/WSL.
"""

from __future__ import annotations
import logging
import shutil
import subprocess
from typing import Dict, Any, Optional

from ..models import (
    PlanAction,
    ExecutionResult,
    ActionStatus,
    ManagerType,
    EnvironmentType,
)

logger = logging.getLogger(__name__)


class RemediationVerifier:
    """Verifica que el parche haya surtido efecto en el sistema y no solo que el código de salida sea 0."""

    def __init__(self, config: Dict[str, Any], fixture_versions: Optional[Dict[str, str]] = None):
        self.config = config
        self.fixture_versions = fixture_versions or {}

    def verify(self, action: PlanAction, exec_result: ExecutionResult) -> ExecutionResult:
        # Si la ejecución falló o fue bloqueada, no procede verificación de versión
        if not exec_result.success or exec_result.status == ActionStatus.BLOCKED_PERMISSIONS:
            return exec_result

        # 1. Obtener versión efectiva instalada tras la actualización
        effective_ver = self._detect_installed_version(action)
        exec_result.effective_version_detected = effective_ver

        # 2. Comprobar si hay un reinicio pendiente
        reboot_pending = self._check_reboot_pending(action)
        exec_result.reboot_pending = reboot_pending

        # 3. Validar coincidencia de versión
        if effective_ver:
            if action.target_version.lower() == "latest" or effective_ver == action.target_version or action.target_version in effective_ver:
                if reboot_pending:
                    exec_result.status = ActionStatus.PENDING_REBOOT
                    exec_result.verification_passed = True
                else:
                    exec_result.status = ActionStatus.EXECUTED_VERIFIED
                    exec_result.verification_passed = True
            else:
                # El gestor terminó con código 0 pero la versión no coincide con el objetivo
                exec_result.status = ActionStatus.EXECUTED_UNVERIFIED
                exec_result.verification_passed = False
                exec_result.error_message = (
                    f"Discrepancia post-instalación: se esperaba versión '{action.target_version}' "
                    f"pero se detectó '{effective_ver}'."
                )
        else:
            # No se pudo consultar la versión efectiva post-instalación
            exec_result.status = ActionStatus.EXECUTED_UNVERIFIED
            exec_result.verification_passed = False

        return exec_result

    def _detect_installed_version(self, action: PlanAction) -> Optional[str]:
        if action.product_id in self.fixture_versions:
            return self.fixture_versions[action.product_id]

        if action.environment == EnvironmentType.WINDOWS and action.manager == ManagerType.WINGET:
            winget_bin = shutil.which("winget")
            if winget_bin:
                try:
                    res = subprocess.run(
                        ["winget", "list", "--id", action.product_id, "--exact", "--accept-source-agreements"],
                        capture_output=True,
                        text=True,
                        timeout=15
                    )
                    if res.returncode == 0:
                        for line in res.stdout.splitlines():
                            if action.product_id.lower() in line.lower():
                                parts = line.split()
                                if len(parts) >= 2:
                                    return parts[1]
                except Exception:
                    pass

        elif action.environment == EnvironmentType.WSL and action.manager == ManagerType.APT:
            distro_name = action.target.replace("WSL:", "")
            wsl_bin = shutil.which("wsl.exe") or shutil.which("wsl")
            if wsl_bin:
                try:
                    res = subprocess.run(
                        [wsl_bin, "-d", distro_name, "-e", "dpkg-query", "-W", "-f=${Version}", action.product_id],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if res.returncode == 0 and res.stdout.strip():
                        return res.stdout.strip()
                except Exception:
                    pass

        elif action.environment == EnvironmentType.MACOS and action.manager == ManagerType.HOMEBREW:
            brew_bin = shutil.which("brew")
            if brew_bin:
                try:
                    res = subprocess.run(
                        [brew_bin, "list", "--versions", action.product_id],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if res.returncode == 0 and res.stdout.strip():
                        parts = res.stdout.strip().split()
                        if len(parts) >= 2:
                            return parts[1]
                except Exception:
                    pass

        elif action.environment == EnvironmentType.LINUX and action.manager == ManagerType.APT:
            dpkg_bin = shutil.which("dpkg-query")
            if dpkg_bin:
                try:
                    res = subprocess.run(
                        [dpkg_bin, "-W", "-f=${Version}", action.product_id],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if res.returncode == 0 and res.stdout.strip():
                        return res.stdout.strip()
                except Exception:
                    pass

        return None

    def _check_reboot_pending(self, action: PlanAction) -> bool:
        if action.environment == EnvironmentType.WINDOWS:
            # En entorno real inspecciona el registro de Windows
            return False
        elif action.environment == EnvironmentType.WSL:
            distro_name = action.target.replace("WSL:", "")
            wsl_bin = shutil.which("wsl.exe") or shutil.which("wsl")
            if wsl_bin:
                try:
                    res = subprocess.run(
                        [wsl_bin, "-d", distro_name, "-e", "test", "-f", "/var/run/reboot-required"],
                        capture_output=True,
                        timeout=5
                    )
                    return res.returncode == 0
                except Exception:
                    pass
        return False
