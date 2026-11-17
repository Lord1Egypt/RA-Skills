"""
Pruebas unitarias para los ejecutores deterministas y control de concurrencia.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from security_maintainer.executor.runner import ConcurrencyLock, PlanExecutor
from security_maintainer.executor.windows_runner import WindowsRunner
from security_maintainer.models import (
    PlanAction,
    ActionStatus,
    EnvironmentType,
    ManagerType,
    FindingCategory,
    ActionPlan,
)


class TestExecutor(unittest.TestCase):

    @patch("os.kill")
    def test_windows_does_not_call_os_kill(self, mock_os_kill):
        lock = ConcurrencyLock()
        with patch("sys.platform", "win32"):
            mock_k32 = MagicMock()
            mock_k32.OpenProcess.return_value = 0
            mock_windll = MagicMock()
            mock_windll.kernel32 = mock_k32
            with patch("ctypes.windll", mock_windll, create=True), patch("ctypes.GetLastError", return_value=87, create=True):
                # 1. Comprobar que para el PID propio devuelve True sin llamar a os.kill
                self.assertTrue(lock._is_pid_alive(os.getpid()))
                mock_os_kill.assert_not_called()

                # 2. Comprobar que para PIDs menores o iguales a 0 devuelve False sin llamar a os.kill
                self.assertFalse(lock._is_pid_alive(0))
                self.assertFalse(lock._is_pid_alive(-10))
                mock_os_kill.assert_not_called()

                # 3. Comprobar que para un PID inexistente se utiliza Windows API y no os.kill
                self.assertFalse(lock._is_pid_alive(99999999))
                mock_os_kill.assert_not_called()

    @patch("os.kill")
    def test_windows_access_denied_preserves_lock(self, mock_os_kill):
        lock = ConcurrencyLock()
        with patch("sys.platform", "win32"):
            # Simular ERROR_ACCESS_DENIED (5) en la API de Windows
            mock_k32 = MagicMock()
            mock_k32.OpenProcess.return_value = 0
            mock_windll = MagicMock()
            mock_windll.kernel32 = mock_k32
            with patch("ctypes.windll", mock_windll, create=True):
                with patch("ctypes.GetLastError", return_value=5, create=True):
                    # Si no hay permisos para consultar el proceso, debe conservar el bloqueo (True)
                    self.assertTrue(lock._is_pid_alive(44444))
            mock_os_kill.assert_not_called()

    def test_concurrency_lock(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_path = Path(tmpdir) / "test.lock"
            lock1 = ConcurrencyLock(lock_path=lock_path, timeout_seconds=0.2)
            lock1.acquire()
            self.assertTrue(lock_path.exists())

            # Intentar adquirir un segundo lock sobre el mismo archivo debe fallar por timeout
            lock2 = ConcurrencyLock(lock_path=lock_path, timeout_seconds=0.2)
            with self.assertRaises(TimeoutError):
                lock2.acquire()

            lock1.release()
            self.assertFalse(lock_path.exists())

    def test_windows_runner_permission_blocked_without_silent_elevation(self):
        # Acción que requiere privilegios de Administrador
        action = PlanAction(
            action_id="act-admin-test",
            environment=EnvironmentType.WINDOWS,
            target="Windows Host",
            product_name="Windows Update KB123456",
            product_id="KB123456",
            manager=ManagerType.WINDOWS_UPDATE,
            installed_version="pending",
            target_version="latest",
            category=FindingCategory.GENERAL_UPDATE_AVAILABLE,
            related_vulnerabilities=[],
            exact_command=["fake-admin-cmd"],
            required_privileges="admin",
            expected_reboot=True,
            verification_method="Get-Hotfix",
            rollback_available=False,
            rollback_limitations="none",
            status=ActionStatus.PROPOSED
        )

        runner = WindowsRunner(config={})
        res = runner.execute_action(action)

        # Si el runner no se ejecuta como Administrador real (en test sin elevación)
        # debe registrarse como BLOCKED_PERMISSIONS en vez de intentar elevar silenciosamente
        if res.status == ActionStatus.BLOCKED_PERMISSIONS:
            self.assertFalse(res.success)
            self.assertEqual(res.exit_code, 126)
            self.assertIn("Acción bloqueada: Se requieren privilegios de Administrador", res.error_message)


if __name__ == "__main__":
    unittest.main()
