"""
Pruebas unitarias para el verificador post-remediación.
"""

import unittest

from security_maintainer.verifier.verifier import RemediationVerifier
from security_maintainer.models import (
    PlanAction,
    ExecutionResult,
    ActionStatus,
    EnvironmentType,
    ManagerType,
    FindingCategory,
)


class TestVerifier(unittest.TestCase):

    def setUp(self):
        self.action = PlanAction(
            action_id="act-test-verify",
            environment=EnvironmentType.WINDOWS,
            target="Windows Host",
            product_name="Git",
            product_id="Git.Git",
            manager=ManagerType.WINGET,
            installed_version="2.44.0",
            target_version="2.47.0",
            category=FindingCategory.GENERAL_UPDATE_AVAILABLE,
            related_vulnerabilities=[],
            exact_command=["winget", "upgrade"],
            required_privileges="user",
            expected_reboot=False,
            verification_method="winget list",
            rollback_available=False,
            rollback_limitations="none",
            status=ActionStatus.PROPOSED
        )

    def test_verified_when_effective_version_matches(self):
        # Simular que el sistema reporta la versión objetivo
        verifier = RemediationVerifier(config={}, fixture_versions={"Git.Git": "2.47.0"})
        exec_res = ExecutionResult(
            action_id="act-test-verify",
            product_name="Git",
            manager=ManagerType.WINGET,
            success=True,
            exit_code=0,
            status=ActionStatus.EXECUTED_UNVERIFIED
        )

        verified = verifier.verify(self.action, exec_res)
        self.assertEqual(verified.status, ActionStatus.EXECUTED_VERIFIED)
        self.assertTrue(verified.verification_passed)
        self.assertEqual(verified.effective_version_detected, "2.47.0")

    def test_unverified_when_version_discrepancy(self):
        # El comando retornó código 0 pero la versión sigue siendo la anterior
        verifier = RemediationVerifier(config={}, fixture_versions={"Git.Git": "2.44.0"})
        exec_res = ExecutionResult(
            action_id="act-test-verify",
            product_name="Git",
            manager=ManagerType.WINGET,
            success=True,
            exit_code=0,
            status=ActionStatus.EXECUTED_UNVERIFIED
        )

        verified = verifier.verify(self.action, exec_res)
        # No debe marcarse como EXECUTED_VERIFIED
        self.assertEqual(verified.status, ActionStatus.EXECUTED_UNVERIFIED)
        self.assertFalse(verified.verification_passed)
        self.assertIn("Discrepancia post-instalación", verified.error_message)


if __name__ == "__main__":
    unittest.main()
