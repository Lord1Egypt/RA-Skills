#!/usr/bin/env python3
"""
Skills Firewall - Generate security reports for skills.
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

try:
    from scan_skill import scan_skill, ThreatLevel
    from firewall_check import SkillsFirewall, ActionType
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from scan_skill import scan_skill, ThreatLevel
    from firewall_check import SkillsFirewall, ActionType


@dataclass
class SecurityReport:
    report_id: str
    generated_at: str
    skills_scanned: int
    safe_skills: int
    warning_skills: int
    blocked_skills: int
    critical_skills: int
    total_threats: int
    summary: Dict
    details: List[Dict]
    recommendations: List[str]


def generate_report(skills_dir: str, output_format: str = "text") -> SecurityReport:
    skills_path = Path(skills_dir)
    scan_results = []
    firewall = SkillsFirewall()
    
    if skills_path.is_file() or (skills_path.is_dir() and (skills_path / "SKILL.md").exists()):
        scan_result = scan_skill(str(skills_path))
        scan_results.append(scan_result)
        firewall_decision = firewall.check_skill(str(skills_path))
    else:
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                scan_result = scan_skill(str(skill_dir))
                scan_results.append(scan_result)
    
    safe_count = 0
    warning_count = 0
    blocked_count = 0
    critical_count = 0
    total_threats = 0
    details = []
    all_recommendations = []
    
    threat_categories = {}
    
    for result in scan_results:
        total_threats += len(result.threats_found)
        
        if result.threat_level == ThreatLevel.SAFE.value:
            safe_count += 1
        elif result.threat_level == ThreatLevel.LOW.value:
            warning_count += 1
        elif result.threat_level == ThreatLevel.MEDIUM.value:
            warning_count += 1
        elif result.threat_level == ThreatLevel.HIGH.value:
            blocked_count += 1
        elif result.threat_level == ThreatLevel.CRITICAL.value:
            critical_count += 1
        
        for threat in result.threats_found:
            category = threat.get("category", "unknown")
            threat_categories[category] = threat_categories.get(category, 0) + 1
        
        details.append({
            "skill_name": result.skill_name,
            "threat_level": result.threat_level,
            "threats_count": len(result.threats_found),
            "is_safe": result.is_safe,
            "warnings": result.warnings,
            "recommendations": result.recommendations
        })
        
        all_recommendations.extend(result.recommendations)
    
    unique_recommendations = list(dict.fromkeys(all_recommendations))
    
    report_id = f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    summary = {
        "by_threat_level": {
            "safe": safe_count,
            "low": sum(1 for r in scan_results if r.threat_level == "low"),
            "medium": sum(1 for r in scan_results if r.threat_level == "medium"),
            "high": sum(1 for r in scan_results if r.threat_level == "high"),
            "critical": critical_count
        },
        "by_category": threat_categories,
        "risk_score": calculate_risk_score(scan_results)
    }
    
    return SecurityReport(
        report_id=report_id,
        generated_at=datetime.now().isoformat(),
        skills_scanned=len(scan_results),
        safe_skills=safe_count,
        warning_skills=warning_count,
        blocked_skills=blocked_count,
        critical_skills=critical_count,
        total_threats=total_threats,
        summary=summary,
        details=details,
        recommendations=unique_recommendations[:10]
    )


def calculate_risk_score(scan_results) -> float:
    if not scan_results:
        return 0.0
    
    score = 0.0
    weights = {
        "safe": 0,
        "low": 1,
        "medium": 3,
        "high": 7,
        "critical": 15
    }
    
    for result in scan_results:
        score += weights.get(result.threat_level, 0)
    
    max_score = len(scan_results) * 15
    return min((score / max_score) * 100, 100) if max_score > 0 else 0


def format_text_report(report: SecurityReport) -> str:
    lines = []
    
    lines.append("=" * 70)
    lines.append("                    SKILLS FIREWALL SECURITY REPORT")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Report ID: {report.report_id}")
    lines.append(f"Generated: {report.generated_at}")
    lines.append("")
    lines.append("-" * 70)
    lines.append("                           EXECUTIVE SUMMARY")
    lines.append("-" * 70)
    lines.append("")
    lines.append(f"Skills Scanned:     {report.skills_scanned}")
    lines.append(f"Safe Skills:        {report.safe_skills}")
    lines.append(f"Warning Skills:     {report.warning_skills}")
    lines.append(f"Blocked Skills:     {report.blocked_skills}")
    lines.append(f"Critical Skills:    {report.critical_skills}")
    lines.append(f"Total Threats:      {report.total_threats}")
    lines.append(f"Risk Score:         {report.summary['risk_score']:.1f}/100")
    lines.append("")
    
    lines.append("-" * 70)
    lines.append("                        THREAT DISTRIBUTION")
    lines.append("-" * 70)
    lines.append("")
    
    by_level = report.summary["by_threat_level"]
    lines.append("By Threat Level:")
    lines.append(f"  [SAFE]     {by_level['safe']:>5} skills")
    lines.append(f"  [LOW]      {by_level['low']:>5} skills")
    lines.append(f"  [MEDIUM]   {by_level['medium']:>5} skills")
    lines.append(f"  [HIGH]     {by_level['high']:>5} skills")
    lines.append(f"  [CRITICAL] {by_level['critical']:>5} skills")
    lines.append("")
    
    by_category = report.summary["by_category"]
    if by_category:
        lines.append("By Category:")
        for category, count in sorted(by_category.items(), key=lambda x: -x[1]):
            lines.append(f"  {category:<25} {count:>5} threats")
        lines.append("")
    
    lines.append("-" * 70)
    lines.append("                          DETAILED FINDINGS")
    lines.append("-" * 70)
    lines.append("")
    
    for detail in report.details:
        status_icon = "[OK]" if detail["is_safe"] else "[!!]"
        lines.append(f"{status_icon} {detail['skill_name']}")
        lines.append(f"    Threat Level: {detail['threat_level'].upper()}")
        lines.append(f"    Threats Found: {detail['threats_count']}")
        
        if detail["warnings"]:
            lines.append(f"    Warnings: {', '.join(detail['warnings'][:2])}")
        lines.append("")
    
    lines.append("-" * 70)
    lines.append("                         RECOMMENDATIONS")
    lines.append("-" * 70)
    lines.append("")
    
    for i, rec in enumerate(report.recommendations, 1):
        lines.append(f"{i}. {rec}")
    
    lines.append("")
    lines.append("=" * 70)
    lines.append("                      END OF SECURITY REPORT")
    lines.append("=" * 70)
    
    return "\n".join(lines)


def format_json_report(report: SecurityReport) -> str:
    return json.dumps(asdict(report), indent=2)


def format_html_report(report: SecurityReport) -> str:
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skills Firewall Security Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4a90d9; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .meta {{ color: #666; font-size: 14px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
        .summary-card {{ background: #f8f9fa; padding: 15px; border-radius: 6px; text-align: center; }}
        .summary-card .number {{ font-size: 28px; font-weight: bold; color: #333; }}
        .summary-card .label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
        .risk-score {{ font-size: 48px; font-weight: bold; text-align: center; margin: 20px 0; }}
        .risk-low {{ color: #28a745; }}
        .risk-medium {{ color: #ffc107; }}
        .risk-high {{ color: #dc3545; }}
        .detail-item {{ padding: 10px; border-left: 4px solid #ddd; margin: 10px 0; background: #f8f9fa; }}
        .detail-item.safe {{ border-left-color: #28a745; }}
        .detail-item.warning {{ border-left-color: #ffc107; }}
        .detail-item.danger {{ border-left-color: #dc3545; }}
        .recommendations {{ background: #e7f3ff; padding: 15px; border-radius: 6px; }}
        .recommendations li {{ margin: 8px 0; }}
        .category-bar {{ display: flex; align-items: center; margin: 5px 0; }}
        .category-name {{ width: 200px; }}
        .category-count {{ background: #4a90d9; color: white; padding: 2px 8px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Skills Firewall Security Report</h1>
        <div class="meta">
            <p>Report ID: {report.report_id}</p>
            <p>Generated: {report.generated_at}</p>
        </div>
        
        <div class="risk-score {'risk-low' if report.summary['risk_score'] < 30 else 'risk-medium' if report.summary['risk_score'] < 70 else 'risk-high'}">
            Risk Score: {report.summary['risk_score']:.1f}/100
        </div>
        
        <h2>Summary</h2>
        <div class="summary-grid">
            <div class="summary-card">
                <div class="number">{report.skills_scanned}</div>
                <div class="label">Skills Scanned</div>
            </div>
            <div class="summary-card">
                <div class="number" style="color: #28a745;">{report.safe_skills}</div>
                <div class="label">Safe</div>
            </div>
            <div class="summary-card">
                <div class="number" style="color: #ffc107;">{report.warning_skills}</div>
                <div class="label">Warnings</div>
            </div>
            <div class="summary-card">
                <div class="number" style="color: #dc3545;">{report.blocked_skills}</div>
                <div class="label">Blocked</div>
            </div>
            <div class="summary-card">
                <div class="number" style="color: #721c24;">{report.critical_skills}</div>
                <div class="label">Critical</div>
            </div>
        </div>
        
        <h2>Threat Categories</h2>
        <div>
            {''.join(f'<div class="category-bar"><span class="category-name">{cat}</span><span class="category-count">{count}</span></div>' for cat, count in sorted(report.summary['by_category'].items(), key=lambda x: -x[1]))}
        </div>
        
        <h2>Detailed Findings</h2>
        {''.join(f'<div class="detail-item {"safe" if d["is_safe"] else "warning" if d["threat_level"] in ["low", "medium"] else "danger"}"><strong>{d["skill_name"]}</strong> - {d["threat_level"].upper()} ({d["threats_count"]} threats)</div>' for d in report.details)}
        
        <h2>Recommendations</h2>
        <div class="recommendations">
            <ol>
                {''.join(f'<li>{rec}</li>' for rec in report.recommendations)}
            </ol>
        </div>
    </div>
</body>
</html>
"""
    return html


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate security reports for skills")
    parser.add_argument("path", help="Path to skill directory or skills folder")
    parser.add_argument("--format", "-f", choices=["text", "json", "html"], default="text",
                       help="Output format (default: text)")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    report = generate_report(args.path)
    
    if args.format == "json":
        output = format_json_report(report)
    elif args.format == "html":
        output = format_html_report(report)
    else:
        output = format_text_report(report)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
