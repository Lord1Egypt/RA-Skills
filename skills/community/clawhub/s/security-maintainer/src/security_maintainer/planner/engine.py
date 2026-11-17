"""
Motor de construcción de planes deterministas de actualización y remediación.
"""

from __future__ import annotations
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

from ..models import (
    InventoryItem,
    Vulnerability,
    PlanAction,
    ActionPlan,
    FindingCategory,
    ManagerType,
    EnvironmentType,
    ActionStatus,
)
from .policy import PolicyEngine
from .approval import compute_plan_hash


class PlannerEngine:
    """Construye planes deterministas respetando prioridades, dependencias y políticas."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.policy = PolicyEngine(config)
        self.max_actions = int(config.get("execution", {}).get("max_actions_per_run", 25))
        self.validity_minutes = int(config.get("execution", {}).get("plan_validity_minutes", 30))

    def create_plan(
        self,
        inventory_items: List[InventoryItem],
        vulnerability_map: Dict[str, List[Vulnerability]],
        target_environment: str = "all"
    ) -> ActionPlan:
        """Genera un ActionPlan ordenado determinísticamente con huella SHA-256."""
        actions: List[PlanAction] = []
        action_counter = 1

        # Ordenar componentes por prioridad estricta de riesgo real:
        # 0. Explotación activa confirmada: CISA KEV o VulnCheck KEV
        # 1. Riesgo predictivo inminente: EPSS >= 0.36 o percentil >= 90%
        # 2. Severidad Crítica (CVSS >= 9.0 o CRITICAL)
        # 3. Severidad Alta (CVSS >= 7.0 o HIGH)
        # 4. Actualizaciones generales
        def sort_key(item: InventoryItem):
            vulns = vulnerability_map.get(item.id, [])
            has_active_exploit = any(v.in_cisa_kev or v.in_vulncheck_kev for v in vulns)
            max_epss = max([v.epss_score or 0.0 for v in vulns], default=0.0)
            max_cvss = max([v.cvss_score or 0.0 for v in vulns], default=0.0)
            has_predictive_risk = max_epss >= 0.36
            max_sev = max([v.severity.value for v in vulns], default="LOW")

            priority_rank = 4
            if has_active_exploit:
                priority_rank = 0
            elif has_predictive_risk:
                priority_rank = 1
            elif max_cvss >= 9.0 or max_sev == "CRITICAL":
                priority_rank = 2
            elif max_cvss >= 7.0 or max_sev == "HIGH":
                priority_rank = 3

            return (priority_rank, -max_epss, -max_cvss, item.name.lower())

        sorted_items = sorted(inventory_items, key=sort_key)

        for item in sorted_items:
            if len(actions) >= self.max_actions:
                break

            # Filtrar por entorno si se especificó
            if target_environment != "all":
                if target_environment.lower() not in item.environment.value.lower():
                    continue

            # Determinar si existe actualización disponible
            if not item.latest_version and item.installed_version != "pending":
                continue

            vulns = vulnerability_map.get(item.id, [])
            cve_ids = [v.cve_id for v in vulns]

            # Categorizar hallazgo
            if vulns:
                category = FindingCategory.VULNERABILITY_PATCHED
            else:
                category = FindingCategory.GENERAL_UPDATE_AVAILABLE

            # Evaluar políticas
            permitted, reason = self.policy.is_action_permitted(item, category)
            if not permitted:
                # Si no está permitido, registrar como acción omitida/bloqueada
                continue

            target_version = item.latest_version or "latest"
            cmd, privs, reboot, verify_desc, rollback_desc, rollback_lims = self._resolve_execution_details(item, target_version)

            action = PlanAction(
                action_id=f"act-{action_counter:02d}",
                environment=item.environment,
                target=item.target_name,
                product_name=item.name,
                product_id=item.id,
                manager=item.manager,
                installed_version=item.installed_version,
                target_version=target_version,
                category=category,
                related_vulnerabilities=cve_ids,
                exact_command=cmd,
                required_privileges=privs,
                expected_reboot=reboot,
                verification_method=verify_desc,
                rollback_available=rollback_desc != "No soportado",
                rollback_limitations=rollback_lims,
                status=ActionStatus.PROPOSED
            )
            actions.append(action)
            action_counter += 1

        now = datetime.now(timezone.utc)
        expires = now + timedelta(minutes=self.validity_minutes)
        plan_id = f"plan-{uuid.uuid4().hex[:8]}"
        plan_hash = compute_plan_hash(actions)

        return ActionPlan(
            plan_id=plan_id,
            created_at=now.isoformat(),
            expires_at=expires.isoformat(),
            environment=target_environment,
            mode=self.config.get("mode", "ask"),
            plan_hash=plan_hash,
            actions=actions,
            is_approved=False
        )

    def _resolve_execution_details(self, item: InventoryItem, target_version: str):
        """Genera comandos deterministas sin inyecciones arbitrarias de shell."""
        if item.manager == ManagerType.WINGET:
            cmd = ["winget", "upgrade", "--id", item.id, "--exact", "--accept-source-agreements", "--accept-package-agreements"]
            privs = "user"
            reboot = False
            verify = "Ejecutar 'winget list --id' y validar que la versión instalada coincida con la versión objetivo."
            rollback = "No soportado de forma automática por WinGet."
            lims = "WinGet no proporciona reversión transaccional; requiere reinstalar el instalador previo manualmente."

        elif item.manager == ManagerType.APT:
            cmd = ["apt-get", "--only-upgrade", "install", "-y", item.id]
            privs = "sudo"
            reboot = item.name in ["linux-image", "libc6", "systemd"]
            verify = f"Ejecutar 'dpkg-query -W -f=\"${{Version}}\" {item.id}' y verificar ausencia en lista de actualizables."
            rollback = "Parcial (mediante 'apt-get install <paquete>=<version_anterior>')."
            lims = "La versión anterior debe seguir existiendo en el repositorio de la distribución o en la caché local."

        elif item.manager == ManagerType.WINDOWS_UPDATE:
            kb_num = item.id.replace("KB", "").strip()
            cmd = ["dism.exe", "/Online", "/Add-Package", f"/PackagePath:{item.id}"]
            privs = "admin"
            reboot = True
            verify = f"Consultar 'Get-HotFix -Id {item.id}' en Windows."
            rollback = f"Desinstalación vía 'wusa.exe /uninstall /kb:{kb_num} /quiet /norestart'."
            lims = "Algunas actualizaciones acumulativas del kernel de Windows no permiten desinstalación permanente."

        elif item.manager == ManagerType.NODE_ENV:
            cmd = ["npm", "update", item.name]
            privs = "user"
            reboot = False
            verify = "Verificar coherencia de package-lock.json y ejecutar npm test."
            rollback = "Disponible (restauración de package-lock.json previo vía git o copia de seguridad)."
            lims = "Solo aplicable dentro del repositorio local del proyecto registrado."

        elif item.manager == ManagerType.PYTHON_ENV:
            cmd = ["pip", "install", "--upgrade", f"{item.name}=={target_version}"]
            privs = "user"
            reboot = False
            verify = "Ejecutar 'pip show' y correr pruebas de pytest configuradas."
            rollback = f"Reinstalación de versión previa 'pip install {item.name}=={item.installed_version}'."
            lims = "Depende de la disponibilidad del paquete en PyPI o rueda local."

        elif item.manager == ManagerType.HOMEBREW:
            cask_flag = ["--cask"] if item.id.startswith("brew-cask:") else []
            cmd = ["brew", "upgrade"] + cask_flag + [item.name]
            privs = "user"
            reboot = False
            verify = f"Ejecutar 'brew outdated' y comprobar que {item.name} no figure en la lista."
            rollback = "Parcial ('brew extract' o reinstalación de versión previa)."
            lims = "Requiere que la fórmula previa esté disponible en el historial de git de Homebrew."

        elif item.manager == ManagerType.MAS:
            app_id = item.id.replace("mas:", "")
            cmd = ["mas", "upgrade", app_id]
            privs = "user"
            reboot = False
            verify = "Ejecutar 'mas outdated' y verificar ausencia de la aplicación."
            rollback = "No soportado automáticamente por Mac App Store."
            lims = "Mac App Store no ofrece reversión a versiones anteriores."

        elif item.manager == ManagerType.APPLE_UPDATE:
            cmd = ["softwareupdate", "-i", item.name]
            privs = "admin"
            reboot = True
            verify = "Ejecutar 'softwareupdate -l' y verificar ausencia del paquete."
            rollback = "No soportado"
            lims = "Las actualizaciones acumulativas de macOS no permiten desinstalación directa."
            cmd = ["manual-action"]
            privs = "user"
            reboot = False
            verify = "Comprobación manual."
            rollback = "No soportado"
            lims = "No existe gestor automatizado para este componente."

        return cmd, privs, reboot, verify, rollback, lims
