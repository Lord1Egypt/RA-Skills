"""
Pruebas unitarias para el motor de planificación, huellas SHA-256 y control de aprobaciones.
"""

import unittest
from datetime import datetime, timezone, timedelta

from security_maintainer.planner.engine import PlannerEngine
from security_maintainer.planner.approval import ApprovalManager, compute_plan_hash
from security_maintainer.models import (
    InventoryItem,
    Vulnerability,
    EnvironmentType,
    ManagerType,
    SeverityLevel,
    FindingCategory,
    ActionPlan,
    PlanAction,
    ActionStatus,
)


class TestPlannerAndApproval(unittest.TestCase):

    def setUp(self):
        self.config = {
            "mode": "ask",
            "windows": {
                "allow_major_upgrades": False, # Prohibir saltos mayores
                "allow_reboots": False,
                "excluded_packages": []
            },
            "execution": {
                "max_actions_per_run": 10,
                "plan_validity_minutes": 30
            }
        }
        self.planner = PlannerEngine(self.config)

    def test_plan_generation_and_hash(self):
        item = InventoryItem(
            environment=EnvironmentType.WINDOWS,
            target_name="Windows Host",
            name="Git",
            id="Git.Git",
            installed_version="2.44.0",
            latest_version="2.47.0",
            manager=ManagerType.WINGET
        )
        plan = self.planner.create_plan([item], {})
        self.assertEqual(len(plan.actions), 1)
        self.assertTrue(plan.plan_hash.isalnum())
        self.assertEqual(len(plan.plan_hash), 64) # Longitud SHA-256

        # Verificar aprobación con la huella correcta
        is_valid, err = ApprovalManager.verify_approval(plan, plan.plan_hash)
        self.assertTrue(is_valid)
        self.assertIsNone(err)

    def test_tampered_plan_rejection(self):
        item = InventoryItem(
            environment=EnvironmentType.WINDOWS,
            target_name="Windows Host",
            name="Git",
            id="Git.Git",
            installed_version="2.44.0",
            latest_version="2.47.0",
            manager=ManagerType.WINGET
        )
        plan = self.planner.create_plan([item], {})

        # Intentar aprobar con una huella alterada
        fake_hash = "0" * 64
        is_valid, err = ApprovalManager.verify_approval(plan, fake_hash)
        self.assertFalse(is_valid)
        self.assertIn("Huella del plan inválida", err)

        # Alterar una acción en el plan sin recalcular
        plan.actions[0].target_version = "99.99.99"
        is_valid_mod, err_mod = ApprovalManager.verify_approval(plan, plan.plan_hash)
        self.assertFalse(is_valid_mod)

    def test_expired_plan_rejection(self):
        # Crear un plan expirado en el pasado
        past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        plan = ActionPlan(
            plan_id="plan-expired",
            created_at=past_time,
            expires_at=past_time,
            environment="all",
            mode="ask",
            plan_hash="",
            actions=[]
        )
        plan.plan_hash = compute_plan_hash(plan.actions)

        is_valid, err = ApprovalManager.verify_approval(plan, plan.plan_hash)
        self.assertFalse(is_valid)
        self.assertIn("ha caducado", err)

    def test_major_upgrade_blocked_by_policy(self):
        # Paquete con salto mayor: 1.2.0 -> 2.0.0
        item = InventoryItem(
            environment=EnvironmentType.WINDOWS,
            target_name="Windows Host",
            name="NodeJS",
            id="OpenJS.NodeJS",
            installed_version="18.12.0",
            latest_version="20.0.0",
            manager=ManagerType.WINGET
        )
        plan = self.planner.create_plan([item], {})
        # Debe omitir la acción porque allow_major_upgrades es False
        self.assertEqual(len(plan.actions), 0)


if __name__ == "__main__":
    unittest.main()
