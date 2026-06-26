"""
ClawGuard Report Generator
Generates human-readable and JSON reports from analysis results.
"""

import json
from typing import Dict, Any
from analyzer import AnalysisResult

class Reporter:
    """Generate security reports"""
    
    @staticmethod
    def generate_text_report(result: AnalysisResult, skill_name: str) -> str:
        """Generate human-readable text report"""
        
        # Risk level emoji
        risk_emoji = {
            "SAFE": "🟢",
            "CAUTION": "🟡",
            "DANGEROUS": "🔴",
        }.get(result.risk_level, "⚪")
        
        # Header
        lines = [
            "🛡️  ClawGuard Security Report",
            "━" * 50,
            f"Skill: {skill_name}",
            f"Score: {result.risk_score}/100 {risk_emoji} {result.risk_level}",
            f"Files scanned: {result.files_scanned}",
            f"Lines scanned: {result.lines_scanned}",
            "",
        ]
        
        # Findings
        if result.findings:
            lines.append(f"⚠️  Issues Found ({len(result.findings)}):")
            lines.append("")
            
            # Sort by severity
            severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
            sorted_findings = sorted(
                result.findings,
                key=lambda f: (severity_order[f.severity], f.file_path, f.line_number)
            )
            
            for i, finding in enumerate(sorted_findings, 1):
                severity_label = {
                    "HIGH": "[HIGH]",
                    "MEDIUM": "[MED] ",
                    "LOW": "[LOW] ",
                }.get(finding.severity, "[???] ")
                
                lines.append(
                    f"{i}. {severity_label} {finding.file_path}:{finding.line_number} — {finding.description}"
                )
                
                if finding.code_snippet:
                    lines.append(f"   Code: {finding.code_snippet[:80]}")
                
                lines.append("")
        
        else:
            lines.append("✅ No security issues detected!")
            lines.append("")
        
        # Network endpoints
        if result.urls:
            lines.append(f"🌐 Network Endpoints ({len(result.urls)}):")
            lines.append("")
            
            for url, is_safe in sorted(result.urls):
                safety_icon = "✓" if is_safe else "⚠️"
                safety_label = "known safe" if is_safe else "unknown"
                lines.append(f"  {safety_icon} {url} ({safety_label})")
            
            lines.append("")
        
        # Recommendation
        lines.append("📋 Recommendation:")
        if result.risk_level == "SAFE":
            lines.append("✅ This skill appears safe to install.")
        elif result.risk_level == "CAUTION":
            lines.append("⚠️  Review flagged items before installing.")
        else:
            lines.append("🔴 DO NOT INSTALL — High-risk patterns detected.")
        
        lines.append("")
        lines.append("━" * 50)
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_json_report(result: AnalysisResult, skill_name: str) -> str:
        """Generate JSON report"""
        
        report: Dict[str, Any] = {
            "skill": skill_name,
            "risk_score": result.risk_score,
            "risk_level": result.risk_level,
            "files_scanned": result.files_scanned,
            "lines_scanned": result.lines_scanned,
            "findings": [
                {
                    "file": f.file_path,
                    "line": f.line_number,
                    "severity": f.severity,
                    "category": f.category,
                    "description": f.description,
                    "code_snippet": f.code_snippet,
                    "weight": f.weight,
                }
                for f in result.findings
            ],
            "urls": [
                {
                    "url": url,
                    "is_safe": is_safe,
                }
                for url, is_safe in result.urls
            ],
            "recommendation": Reporter._get_recommendation(result.risk_level),
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    @staticmethod
    def _get_recommendation(risk_level: str) -> str:
        """Get recommendation text"""
        if risk_level == "SAFE":
            return "This skill appears safe to install."
        elif risk_level == "CAUTION":
            return "Review flagged items before installing."
        else:
            return "DO NOT INSTALL — High-risk patterns detected."
