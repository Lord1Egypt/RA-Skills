"""
Generador de informes en Markdown estructurados y legibles en español.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..models import (
    InventoryItem,
    Vulnerability,
    ActionPlan,
    ExecutionResult,
    CoverageSummary,
    ActionStatus,
    AISecurityFinding,
)


class MarkdownReporter:
    """Genera informes legibles en formato Markdown."""

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
        execution_results: Optional[List[ExecutionResult]] = None,
        ai_findings: Optional[List[AISecurityFinding]] = None,
    ) -> str:
        lines: List[str] = []
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        # 1. Cabecera
        lines.append(f"# Informe de Seguridad y Mantenimiento — OpenClaw")
        lines.append(f"**Fecha y Hora:** {now_str}  ")
        lines.append(f"**Entorno analizado:** `{environment}` | **Modo de ejecución:** `{mode}`\n")

        # 2. Resumen de Cobertura
        lines.append("## 1. Cobertura del Inventario")
        lines.append(f"- **Total de componentes detectados:** {coverage.total_components_detected}")
        lines.append(f"- **Gestionables automáticamente:** {coverage.manageable_components}")
        lines.append(f"- **Gestión parcial o con dependencias:** {coverage.partially_manageable}")
        lines.append(f"- **Requieren intervención manual / Sin soporte:** {coverage.unsupported_or_manual}\n")

        if not coverage.is_coverage_complete or coverage.query_sources_failed:
            lines.append("> [!WARNING]")
            lines.append("> **Cobertura incompleta de vulnerabilidades:**")
            lines.append(f"> Una o más fuentes de datos ({', '.join(coverage.query_sources_failed) or 'red/API'}) no estuvieron disponibles durante la consulta. "
                         "Los resultados reflejan solo las fuentes accesibles y la caché local. Esto **no** garantiza la ausencia de otras vulnerabilidades.\n")

        # 3. Vulnerabilidades Conocidas Detectadas
        total_vulns = sum(len(v_list) for v_list in vulnerabilities.values())
        lines.append(f"## 2. Vulnerabilidades Conocidas Identificadas ({total_vulns})")

        if total_vulns == 0:
            lines.append("No se detectaron vulnerabilidades conocidas en los componentes evaluados por las fuentes disponibles.\n")
        else:
            lines.append("| Componente | CVE / Advisory | Gravedad | CVSS | EPSS (Riesgo) | KEV Activo | Parche Oficial | Inteligencia / Avisos |")
            lines.append("| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |")
            for pkg_id, v_list in vulnerabilities.items():
                for v in v_list:
                    # Indicador de KEV activo
                    kev_tags = []
                    if v.in_cisa_kev:
                        kev_tags.append("🔥 CISA")
                    if v.in_vulncheck_kev:
                        kev_tags.append("⚡ VulnCheck")
                    kev_str = " + ".join(kev_tags) if kev_tags else "No"

                    # EPSS
                    if v.epss_score is not None:
                        epss_str = f"**{v.epss_score * 100:.1f}%**"
                        if v.epss_percentile and v.epss_percentile >= 0.90:
                            epss_str += f" (p{int(v.epss_percentile * 100)})"
                    else:
                        epss_str = "-"

                    # CVSS
                    cvss_str = f"`{v.cvss_score:.1f}`" if v.cvss_score is not None else "-"

                    # Detalles adicionales (USN / MSRC / Source)
                    extra_notes = []
                    if v.ubuntu_usn:
                        extra_notes.append(f"USN: {v.ubuntu_usn}")
                    if v.msrc_severity:
                        extra_notes.append(f"MSRC: {v.msrc_severity}")
                    if not extra_notes:
                        extra_notes.append(v.source)
                    intel_str = " · ".join(extra_notes)

                    fixed = v.fixed_version or "Sin parche disponible"
                    lines.append(
                        f"| `{pkg_id}` | [{v.cve_id}](https://nvd.nist.gov/vuln/detail/{v.cve_id}) | "
                        f"**{v.severity.value}** | {cvss_str} | {epss_str} | {kev_str} | `{fixed}` | {intel_str} |"
                    )
            lines.append("")

        # 4. Actualizaciones Generales Disponibles (Sin CVE)
        general_updates = [item for item in inventory if item.latest_version and item.id not in vulnerabilities]
        lines.append(f"## 3. Actualizaciones Generales Disponibles ({len(general_updates)})")
        if general_updates:
            lines.append("| Entorno | Componente | Gestor | Versión Actual | Versión Objetivo |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for u in general_updates:
                lines.append(f"| {u.target_name} | `{u.name}` | {u.manager.value} | `{u.installed_version}` | `{u.latest_version}` |")
            lines.append("")
        else:
            lines.append("No se detectaron actualizaciones generales pendientes en los componentes gestionables.\n")

        # 5. Plan de Remediación y Ejecución
        if plan:
            lines.append(f"## 4. Plan de Acción (`{plan.plan_id}`)")
            lines.append(f"- **Huella SHA-256:** `{plan.plan_hash}`")
            lines.append(f"- **Caducidad:** {plan.expires_at}  \n")

            lines.append("| ID Acción | Producto | Tipo | Versión Objetivo | Privilegios | Reinicio | Estado |")
            lines.append("| :--- | :--- | :--- | :--- | :---: | :---: | :--- |")

            exec_map = {res.action_id: res for res in (execution_results or [])}

            for act in plan.actions:
                res = exec_map.get(act.action_id)
                status_str = res.status.value if res else act.status.value
                reboot_str = "Sí" if act.expected_reboot else "No"
                cat_desc = "Parche Seguridad" if "vulnerability" in act.category.value else "Actualización"
                lines.append(
                    f"| `{act.action_id}` | `{act.product_name}` | {cat_desc} | "
                    f"`{act.target_version}` | {act.required_privileges} | {reboot_str} | **{status_str}** |"
                )
            lines.append("")

        # 5. Hallazgos de Seguridad en IA y Agentes (si existen)
        if ai_findings:
            lines.append(f"## 5. Auditoría de Seguridad de IA y Agentes ({len(ai_findings)})")
            lines.append("| Severidad | Componente / Objetivo | Tipo de Riesgo | Hallazgo y Recomendación |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for f in ai_findings:
                lines.append(
                    f"| **{f.severity.value}** | `{f.target_component}` | {f.threat_type.value} | "
                    f"**{f.title}**: {f.description} *Remediación:* {f.remediation_recommendation} |"
                )
            lines.append("")

        # 6. Software que Requiere Intervención Manual o Sin Soporte
        manual_items = [item for item in inventory if item.requires_manual_intervention or not item.is_supported]
        if manual_items:
            lines.append("## 6. Software no Gestionable Automáticamente")
            lines.append("| Entorno | Componente | Motivo / Limitación |")
            lines.append("| :--- | :--- | :--- |")
            for m in manual_items:
                reason = m.notes or "Sin mecanismo de actualización programática"
                lines.append(f"| {m.target_name} | `{m.name}` | {reason} |")
            lines.append("")

        content = "\n".join(lines)

        # Guardar en disco
        filename = f"report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.output_dir / filename
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass

        return content
