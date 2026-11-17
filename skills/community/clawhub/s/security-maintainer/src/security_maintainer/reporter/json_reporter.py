"""
Generador de informes JSON estructurados con trazabilidad completa.
"""

from __future__ import annotations
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..models import (
    InventoryItem,
    Vulnerability,
    ActionPlan,
    ExecutionResult,
    CoverageSummary,
)


class JSONReporter:
    """Genera el informe JSON canónico de auditoría y ejecución."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (Path.home() / ".security-maintainer" / "reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(
        self,
        environment: str,
        mode: str,
        coverage: CoverageSummary,
        inventory: List[InventoryItem],
        vulnerabilities: Dict[str, List[Vulnerability]],
        plan: Optional[ActionPlan] = None,
        execution_results: Optional[List[ExecutionResult]] = None
    ) -> Dict[str, Any]:
        report = {
            "metadata": {
                "generator": "OpenClaw-SecurityMaintainer",
                "version": "1.0.0",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "environment": environment,
                "mode": mode,
            },
            "coverage_summary": coverage.to_dict(),
            "inventory": [item.to_dict() for item in inventory],
            "vulnerabilities": {
                pkg_id: [v.to_dict() for v in v_list]
                for pkg_id, v_list in vulnerabilities.items()
            },
            "plan": plan.to_dict() if plan else None,
            "execution_results": [res.to_dict() for res in execution_results] if execution_results else []
        }

        # Guardar en disco
        filename = f"report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.output_dir / filename
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        return report
