"""
SkillGuard — Report Generators (JSON + Markdown)
TRACE五维安全评分
"""

import json as _json
from typing import List, Dict
from skillguard.detectors.base import Finding


class ReportGenerator:
    """Base report generator with TRACE scoring."""

    @staticmethod
    def _trace_score(findings: List[Finding]) -> dict:
        """Calculate TRACE five-dimension security score."""
        if not findings:
            return {"T": 5.0, "R": 5.0, "A": 5.0, "C": 5.0, "E": 5.0,
                    "overall": 5.0, "level": "优秀", "description": "未发现任何安全风险"}

        critical = sum(1 for f in findings if f.severity == "CRITICAL")
        high = sum(1 for f in findings if f.severity == "HIGH")
        medium = sum(1 for f in findings if f.severity == "MEDIUM")
        low = sum(1 for f in findings if f.severity == "LOW")
        total = len(findings)

        # Trust: inverse of critical+high ratio
        T = max(0, 5.0 - (critical * 1.5 + high * 0.5) * 5.0 / max(total, 1))
        # Reliability: how many detectors passed without issues
        R = max(0, 5.0 - (critical * 1.0 + high * 0.3) * 5.0 / max(total, 1))
        # Authenticity: avg confidence of findings
        A = max(0, 5.0 - sum(1 - f.confidence for f in findings) / max(total, 1))
        # Compliance: OWASP ASI coverage
        covered_asi = set(f.owasp_asi_id for f in findings if f.owasp_asi_id)
        C = min(5.0, len(covered_asi) * 0.5)
        # Exposure: ratio of low vs critical
        E = max(0, 5.0 - (critical * 2.0 + high * 1.0) / max(total, 1))

        overall = (T + R + A + C + E) / 5.0
        level = "危险" if overall < 2 else "警告" if overall < 3 else "一般" if overall < 3.5 else "良好" if overall < 4 else "优秀"

        return {
            "T": round(T, 1), "R": round(R, 1), "A": round(A, 1),
            "C": round(C, 1), "E": round(E, 1),
            "overall": round(overall, 2), "level": level,
            "stats": {"critical": critical, "high": high, "medium": medium, "low": low, "total": total},
            "description": f"T(信任)={T:.1f} R(可靠)={R:.1f} A(真实)={A:.1f} C(合规)={C:.1f} E(暴露)={E:.1f}",
        }


class JSONReport(ReportGenerator):
    """Generate machine-readable JSON security report."""

    def generate(self, findings: List[Finding], skill_name: str = "", skill_version: str = "") -> str:
        trace = self._trace_score(findings)
        report = {
            "skillguard_version": "1.0.0",
            "skill": {"name": skill_name, "version": skill_version},
            "trace_score": trace,
            "findings": [f.to_dict() for f in findings],
            "summary": {
                "total_findings": len(findings),
                "by_severity": trace.get("stats", {}),
            },
        }
        return _json.dumps(report, ensure_ascii=False, indent=2)


class MarkdownReport(ReportGenerator):
    """Generate human-readable Markdown security report."""

    def generate(self, findings: List[Finding], skill_name: str = "", skill_version: str = "") -> str:
        trace = self._trace_score(findings)
        stats = trace.get("stats", {})

        lines = [
            f"# 🔒 SkillGuard 安全审计报告",
            f"",
            f"**Skill**: {skill_name} v{skill_version}",
            f"**审计时间**: {self._now()}",
            f"**SkillGuard版本**: 1.0.0",
            f"",
            f"---",
            f"",
            f"## 📊 TRACE 安全评分",
            f"",
            f"| 维度 | 评分 | 说明 |",
            f"|------|:--:|------|",
            f"| **T**·信任 | {trace['T']}/5 | Agent可信度 |",
            f"| **R**·可靠 | {trace['R']}/5 | 功能可靠性 |",
            f"| **A**·真实 | {trace['A']}/5 | 行为真实性 |",
            f"| **C**·合规 | {trace['C']}/5 | 标准合规度 |",
            f"| **E**·暴露 | {trace['E']}/5 | 攻击面暴露 |",
            f"| **综合** | **{trace['overall']}/5** | **{trace['level']}** |",
            f"",
            f"---",
            f"",
            f"## 🔍 发现问题统计",
            f"",
            f"| 严重级别 | 数量 |",
            f"|---------|:--:|",
            f"| 🔴 CRITICAL | {stats.get('critical', 0)} |",
            f"| 🟠 HIGH | {stats.get('high', 0)} |",
            f"| 🟡 MEDIUM | {stats.get('medium', 0)} |",
            f"| 🔵 LOW | {stats.get('low', 0)} |",
            f"| **总计** | **{stats.get('total', 0)}** |",
            f"",
        ]

        if not findings:
            lines.append("✅ 未发现任何安全风险！")
        else:
            lines.append("---")
            lines.append("")
            
            for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                sev_findings = [f for f in findings if f.severity == sev]
                if not sev_findings:
                    continue
                
                emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}.get(sev, "⚪")
                lines.append(f"## {emoji} {sev}")
                lines.append("")
                
                for f in sev_findings:
                    lines.append(f"### {f.title}")
                    lines.append(f"- **检测器**: {f.detector}")
                    lines.append(f"- **置信度**: {f.confidence:.0%}")
                    lines.append(f"- **OWASP ASI**: {f.owasp_asi_id} | **CWE**: {f.cwe_id}")
                    if f.file_path:
                        lines.append(f"- **位置**: `{f.file_path}` L{f.line_number}")
                    lines.append(f"")
                    lines.append(f"{f.description}")
                    lines.append(f"")
                    if f.code_snippet:
                        lines.append(f"```")
                        lines.append(f.code_snippet)
                        lines.append(f"```")
                        lines.append(f"")
                    if f.remediation:
                        lines.append(f"**修复建议**: {f.remediation}")
                    lines.append("")

        lines.append("---")
        lines.append(f"*审计由 SkillGuard v1.0.0 生成 — Agent技能安全扫描器*")
        return "\n".join(lines)

    @staticmethod
    def _now() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
