"""
SenseGuard Report Generator
Generates Markdown-formatted security risk reports.
Supports single skill detailed reports and batch summary reports.
"""

import os
from datetime import datetime
from typing import List, Dict, Optional


class ReportGenerator:
    """Generates Markdown security reports from scan results."""

    RATING_ICONS = {
        "SAFE": "✅",
        "CAUTION": "⚠️",
        "DANGEROUS": "🔶",
        "MALICIOUS": "🔴",
    }

    def generate_single_report(
        self,
        skill_name: str,
        score: int,
        rating: str,
        layer1_result: dict,
        layer2_result: Optional[dict],
        score_breakdown: List[dict],
        layers_used: List[str],
        previous_result: Optional[dict] = None,
    ) -> str:
        """Generate a detailed report for a single skill."""
        icon = self.RATING_ICONS.get(rating, "")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        engine_str = " + ".join(layers_used)

        lines = []
        lines.append(f"# 🛡️ SenseGuard Security Report")
        lines.append("")
        lines.append(f"## Skill: {skill_name}")
        lines.append(f"**Score: {score}/100** {icon} **{rating}**")
        lines.append(f"**Scan time**: {now}")
        lines.append(f"**Scan engine**: {engine_str}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Group findings by severity
        pattern_findings = layer1_result.get("pattern_findings", [])
        structure_findings = layer1_result.get("structure_findings", [])

        critical_findings = [f for f in pattern_findings if f["severity"] == "critical"]
        high_findings = [f for f in pattern_findings if f["severity"] == "high"]
        medium_findings = [f for f in pattern_findings if f["severity"] == "medium"]
        critical_structure = [f for f in structure_findings if f["severity"] == "critical"]

        # Add Layer 2 findings as pseudo-findings for display
        l2_display = []
        if layer2_result:
            l2_display = self._extract_layer2_findings(layer2_result)

        # Critical findings
        all_critical = critical_findings + critical_structure + [f for f in l2_display if f["severity"] == "critical"]
        if all_critical:
            lines.append(f"### 🚨 Critical Findings ({len(all_critical)})")
            lines.append("")
            for i, f in enumerate(all_critical, 1):
                lines.extend(self._format_finding(i, f))
            lines.append("")

        # High findings
        all_high = high_findings + [f for f in l2_display if f["severity"] == "high"]
        if all_high:
            lines.append(f"### ⚠️ High Findings ({len(all_high)})")
            lines.append("")
            offset = len(all_critical)
            for i, f in enumerate(all_high, offset + 1):
                lines.extend(self._format_finding(i, f))
            lines.append("")

        # Medium findings
        medium_structure = [f for f in structure_findings if f["severity"] == "medium"]
        all_medium = medium_findings + medium_structure
        if all_medium:
            lines.append(f"### 📋 Medium Findings ({len(all_medium)})")
            lines.append("")
            offset = len(all_critical) + len(all_high)
            for i, f in enumerate(all_medium, offset + 1):
                lines.extend(self._format_finding(i, f))
            lines.append("")

        # No findings
        if not all_critical and not all_high and not all_medium:
            lines.append("### ✅ No significant findings")
            lines.append("")
            lines.append("No suspicious patterns or structural issues detected.")
            lines.append("")

        # Score breakdown table
        lines.append("### 📊 Reputation Score Breakdown")
        lines.append("")
        lines.append("| Dimension | Points | Reason |")
        lines.append("|-----------|--------|--------|")
        lines.append("| Base score | 100 | |")
        for item in score_breakdown:
            points = item["points"]
            sign = "+" if points > 0 else str(points)
            if points > 0:
                sign = f"+{points}"
            lines.append(f"| {item['dimension']} | {sign} | {item['reason']} |")
        lines.append(f"| **Final score** | **{score}** | |")
        lines.append("")

        # Diff with previous scan
        if previous_result:
            lines.extend(self._generate_diff_section(previous_result, layer1_result, score))

        # Recommendations
        lines.extend(self._generate_recommendations(rating, all_critical, all_high, skill_name))

        return "\n".join(lines)

    def generate_batch_report(
        self,
        results: List[dict],
        previous_results: Optional[Dict[str, dict]] = None,
    ) -> str:
        """Generate a summary report for multiple skills."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Categorize by rating
        by_rating = {"MALICIOUS": [], "DANGEROUS": [], "CAUTION": [], "SAFE": []}
        for r in results:
            rating = r.get("rating", "SAFE")
            by_rating.setdefault(rating, []).append(r)

        lines = []
        lines.append("# 🛡️ SenseGuard Full Security Checkup")
        lines.append("")
        lines.append(f"**Scan time**: {now}")
        lines.append(f"**Skills scanned**: {len(results)}")
        engine_layers = set()
        for r in results:
            engine_layers.update(r.get("layers_used", ["Layer 1"]))
        lines.append(f"**Scan engine**: {' + '.join(sorted(engine_layers))}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Overview table
        lines.append("## 📊 Overview")
        lines.append("")
        lines.append("| Rating | Count | Skills |")
        lines.append("|--------|-------|--------|")
        for rating in ["MALICIOUS", "DANGEROUS", "CAUTION", "SAFE"]:
            icon = self.RATING_ICONS.get(rating, "")
            skill_list = by_rating.get(rating, [])
            names = ", ".join(r["skill_name"] for r in skill_list) if skill_list else "-"
            lines.append(f"| {icon} {rating} | {len(skill_list)} | {names} |")
        lines.append("")

        # Urgent actions
        urgent = by_rating.get("MALICIOUS", []) + by_rating.get("DANGEROUS", [])
        if urgent:
            lines.append("## 🚨 Requires Immediate Attention")
            lines.append("")
            for i, r in enumerate(urgent, 1):
                icon = self.RATING_ICONS.get(r["rating"], "")
                score = r.get("score", 0)
                critical = r.get("critical_count", 0)
                high = r.get("high_count", 0)
                action = "Remove immediately" if r["rating"] == "MALICIOUS" else "Review before continued use"
                lines.append(f"### {i}. {r['skill_name']} ({score}/100 {icon})")
                lines.append(f"- {critical} critical + {high} high findings")
                lines.append(f"- **Recommendation: {action}**")
                lines.append("")

        # Caution items
        caution = by_rating.get("CAUTION", [])
        if caution:
            lines.append("## ⚠️ Caution")
            lines.append("")
            for r in caution:
                icon = self.RATING_ICONS.get(r["rating"], "")
                score = r.get("score", 0)
                lines.append(f"- **{r['skill_name']}** ({score}/100 {icon})")
            lines.append("")

        # Safe items
        safe = by_rating.get("SAFE", [])
        if safe:
            lines.append("## ✅ Safe")
            lines.append("")
            for r in safe:
                score = r.get("score", 0)
                lines.append(f"- **{r['skill_name']}** ({score}/100)")
            lines.append("")

        # Diff with previous
        if previous_results:
            lines.extend(self._generate_batch_diff(results, previous_results))

        return "\n".join(lines)

    def _format_finding(self, index: int, finding: dict) -> List[str]:
        """Format a single finding for display."""
        lines = []
        if "description_zh" in finding and finding["description_zh"]:
            desc = f"{finding['description']} / {finding['description_zh']}"
        elif "description" in finding:
            desc = finding["description"]
        else:
            desc = finding.get("check_name", "Unknown")

        source = finding.get("layer", "layer1")
        category = finding.get("category", finding.get("check_name", "structure"))
        severity = finding.get("severity", "medium")

        lines.append(f"{index}. **{desc}** ({source}: {category}.{severity})")

        if "evidence" in finding and finding["evidence"]:
            lines.append(f"   > Evidence: `{finding['evidence']}`")
        if "file_path" in finding:
            rel_path = os.path.basename(finding["file_path"])
            line_num = finding.get("line_number", "?")
            lines.append(f"   > Location: {rel_path} line {line_num}")
        if "details" in finding and finding["details"]:
            lines.append(f"   > {finding['details']}")
        if "explanation" in finding and finding["explanation"]:
            lines.append(f"   > {finding['explanation']}")

        lines.append("")
        return lines

    def _extract_layer2_findings(self, layer2: dict) -> List[dict]:
        """Convert Layer 2 semantic analysis results into finding-like dicts."""
        findings = []

        pi = layer2.get("prompt_injection", {})
        if pi.get("detected") and pi.get("confidence", 0) > 0.5:
            sev = "critical" if pi.get("confidence", 0) > 0.7 else "high"
            evidence_list = pi.get("evidence", [])
            evidence_str = "; ".join(evidence_list[:3]) if evidence_list else ""
            findings.append({
                "severity": sev,
                "description": f"Prompt Injection (confidence: {pi.get('confidence', 0):.2f})",
                "description_zh": f"提示注入攻击 (置信度: {pi.get('confidence', 0):.2f})",
                "category": "semantic_analysis",
                "layer": "layer2",
                "evidence": evidence_str,
                "explanation": pi.get("explanation", ""),
            })

        perm = layer2.get("permission_analysis", {})
        if perm.get("overprivileged"):
            findings.append({
                "severity": "high",
                "description": "Overprivileged skill",
                "description_zh": "权限过度",
                "category": "semantic_analysis",
                "layer": "layer2",
                "evidence": f"Declared: {perm.get('declared_purpose', 'N/A')}",
                "explanation": perm.get("explanation", ""),
            })

        data = layer2.get("data_access", {})
        if data.get("data_sent_externally"):
            endpoints = data.get("external_endpoints", [])
            findings.append({
                "severity": "critical",
                "description": "Data sent to external endpoints",
                "description_zh": "数据外传到外部端点",
                "category": "semantic_analysis",
                "layer": "layer2",
                "evidence": ", ".join(endpoints[:5]),
                "explanation": "",
            })

        hidden = layer2.get("hidden_instructions", {})
        if hidden.get("detected"):
            findings.append({
                "severity": "critical",
                "description": "Hidden instructions detected",
                "description_zh": "检测到隐藏指令",
                "category": "semantic_analysis",
                "layer": "layer2",
                "evidence": "; ".join(hidden.get("instructions", [])[:3]),
                "explanation": f"Technique: {hidden.get('technique', 'unknown')}",
            })

        behav = layer2.get("behavioral_risk", {})
        if behav.get("modifies_agent_config"):
            findings.append({
                "severity": "high",
                "description": "Modifies agent configuration",
                "description_zh": "修改 agent 配置",
                "category": "semantic_analysis",
                "layer": "layer2",
                "evidence": "",
                "explanation": behav.get("explanation", ""),
            })
        if behav.get("bypasses_confirmation"):
            findings.append({
                "severity": "high",
                "description": "Bypasses user confirmation",
                "description_zh": "绕过用户确认",
                "category": "semantic_analysis",
                "layer": "layer2",
                "evidence": "",
                "explanation": behav.get("explanation", ""),
            })
        if behav.get("creates_persistence"):
            findings.append({
                "severity": "high",
                "description": "Creates persistence mechanism",
                "description_zh": "创建持久化机制",
                "category": "semantic_analysis",
                "layer": "layer2",
                "evidence": "",
                "explanation": behav.get("explanation", ""),
            })

        return findings

    def _generate_recommendations(
        self, rating: str, critical: list, high: list, skill_name: str
    ) -> List[str]:
        """Generate recommendation section based on rating."""
        lines = ["### 💡 Recommendations", ""]

        if rating == "MALICIOUS":
            lines.append(f"**⛔ Strongly recommend NOT installing this skill.**")
            lines.append(f"This skill exhibits clear malicious characteristics.")
            lines.append("If already installed, consider removing it and checking:")
            lines.append("- `~/.openclaw/SOUL.md`")
            lines.append("- `~/.openclaw/AGENTS.md`")
            lines.append("- Environment variables and API keys")
        elif rating == "DANGEROUS":
            lines.append(f"**🔶 High risk. Not recommended for installation.**")
            lines.append("Review the critical/high findings above carefully before deciding.")
        elif rating == "CAUTION":
            lines.append(f"**⚠️ Potential risks detected. Review recommended.**")
            lines.append("The findings above may be benign, but manual review is advised.")
        else:
            lines.append(f"**✅ No significant risks detected.**")
            lines.append("This skill appears safe based on automated analysis.")

        lines.append("")
        return lines

    def _generate_diff_section(
        self, previous: dict, current: dict, current_score: int
    ) -> List[str]:
        """Generate diff comparison with previous scan."""
        lines = ["### 🔄 Changes Since Last Scan", ""]

        prev_score = previous.get("score", 100)
        if current_score != prev_score:
            direction = "⬆️ improved" if current_score > prev_score else "⬇️ degraded"
            lines.append(f"- Score: {prev_score} → {current_score} ({direction})")

        prev_critical = previous.get("critical_count", 0)
        curr_critical = current.get("summary", {}).get("critical", 0)
        if curr_critical != prev_critical:
            lines.append(f"- Critical findings: {prev_critical} → {curr_critical}")

        prev_high = previous.get("high_count", 0)
        curr_high = current.get("summary", {}).get("high", 0)
        if curr_high != prev_high:
            lines.append(f"- High findings: {prev_high} → {curr_high}")

        if current_score == prev_score and curr_critical == prev_critical and curr_high == prev_high:
            lines.append("- No changes detected.")

        lines.append("")
        return lines

    def _generate_batch_diff(
        self, results: List[dict], previous_results: Dict[str, dict]
    ) -> List[str]:
        """Generate diff section for batch reports."""
        lines = ["## 🔄 Changes Since Last Scan", ""]

        current_names = {r["skill_name"] for r in results}
        previous_names = set(previous_results.keys())

        new_skills = current_names - previous_names
        removed_skills = previous_names - current_names

        if new_skills:
            for name in sorted(new_skills):
                r = next((x for x in results if x["skill_name"] == name), None)
                rating = r["rating"] if r else "UNKNOWN"
                icon = self.RATING_ICONS.get(rating, "")
                lines.append(f"- **New skill**: {name} (first scan, {icon} {rating})")

        if removed_skills:
            for name in sorted(removed_skills):
                lines.append(f"- **Removed skill**: {name}")

        # Check for file changes (by hash)
        for r in results:
            name = r["skill_name"]
            if name in previous_results:
                prev = previous_results[name]
                if r.get("hash") and prev.get("hash") and r["hash"] != prev["hash"]:
                    lines.append(f"- **File changed**: {name} SKILL.md was modified ← ⚠️ review recommended")

        if not new_skills and not removed_skills:
            changed = any(
                r.get("hash") != previous_results.get(r["skill_name"], {}).get("hash")
                for r in results if r["skill_name"] in previous_results
            )
            if not changed:
                lines.append("- No changes detected since last scan.")

        lines.append("")
        return lines
