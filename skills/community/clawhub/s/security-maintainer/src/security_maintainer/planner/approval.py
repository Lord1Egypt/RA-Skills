"""
Validación de aprobaciones criptográficas con huella SHA-256 y caducidad temporal.
Garantiza que una aprobación quede estrictamente vinculada a acciones concretas.
"""

from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple

from ..models import ActionPlan, PlanAction


def compute_plan_hash(actions: List[PlanAction]) -> str:
    """Calcula una huella SHA-256 determinista del conjunto de acciones del plan."""
    canonical_items = []
    for act in actions:
        canonical_items.append({
            "action_id": act.action_id,
            "target": act.target,
            "product_id": act.product_id,
            "installed_version": act.installed_version,
            "target_version": act.target_version,
            "category": act.category.value,
            "exact_command": act.exact_command,
            "required_privileges": act.required_privileges
        })
    # Ordenar por action_id para garantizar determinismo
    canonical_items.sort(key=lambda x: x["action_id"])
    serialized = json.dumps(canonical_items, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class ApprovalManager:
    """Valida tokens de aprobación y vigencia de planes de remediación."""

    @staticmethod
    def verify_approval(
        plan: ActionPlan,
        provided_hash: str,
        current_inventory_hash: Optional[str] = None,
        expected_inventory_hash: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Verifica que:
        1. El plan no haya caducado.
        2. La huella SHA-256 del plan coincida exactamente.
        3. El estado del sistema no haya cambiado materialmente (si se proporcionan hashes de inventario).
        """
        # 1. Comprobación de caducidad
        try:
            expires_at = datetime.fromisoformat(plan.expires_at)
            # Asegurar timezone UTC para comparación consistente
            now = datetime.now(timezone.utc)
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if now > expires_at:
                return False, f"El plan {plan.plan_id} ha caducado a las {plan.expires_at}. Se requiere generar un nuevo plan."
        except Exception as e:
            return False, f"Formato de fecha de caducidad no válido: {e}"

        # 2. Comprobación de integridad de la huella
        recomputed_hash = compute_plan_hash(plan.actions)
        if provided_hash.lower() != recomputed_hash.lower():
            return False, (
                f"Huella del plan inválida. Proporcionada: '{provided_hash}', "
                f"Calculada sobre las acciones: '{recomputed_hash}'. El plan fue modificado o no coincide."
            )

        if plan.plan_hash.lower() != recomputed_hash.lower():
            return False, "La huella registrada en el plan no coincide con la recalculada sobre las acciones."

        # 3. Comprobación de cambio material del sistema
        if expected_inventory_hash and current_inventory_hash:
            if expected_inventory_hash != current_inventory_hash:
                return False, "El estado del sistema ha cambiado materialmente desde que se planificaron las acciones. Se requiere un nuevo plan."

        return True, None
