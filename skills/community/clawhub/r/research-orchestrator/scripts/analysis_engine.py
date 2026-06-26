#!/usr/bin/env python3
"""
Deep Analysis Engine
Synthesize research into insights and analysis
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


class AnalysisEngine:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())

    def load_research_data(self, task_dir):
        """Load all research data from task directory"""

        research_dir = f"{task_dir}/research"
        research_data = {}

        if os.path.exists(research_dir):
            for filename in os.listdir(research_dir):
                if filename.endswith(".json"):
                    filepath = f"{research_dir}/{filename}"
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        angle_id = filename.replace(".json", "")
                        research_data[angle_id] = data

        return research_data

    def extract_key_findings(self, research_data):
        """Extract key findings across all research"""

        all_findings = []

        for angle_id, data in research_data.items():
            findings = data.get("findings", [])
            for finding in findings:
                finding["angle"] = angle_id
                all_findings.append(finding)

        # Sort by credibility
        credibility_order = {"high": 0, "medium": 1, "low": 2}
        all_findings.sort(
            key=lambda f: credibility_order.get(f.get("credibility", "low"), 3)
        )

        return all_findings

    def identify_patterns(self, findings):
        """Identify patterns and trends in findings"""

        patterns = {
            "high_frequency_topics": [],
            "trends": [],
            "contradictions": [],
            "gaps": [],
        }

        # Simple frequency analysis
        topic_counts = {}
        for finding in findings:
            content = finding.get("content", "").lower()
            # Extract key terms (simplified)
            words = content.split()
            for word in words:
                if len(word) > 5:  # Filter short words
                    topic_counts[word] = topic_counts.get(word, 0) + 1

        # Get top topics
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        patterns["high_frequency_topics"] = sorted_topics[:10]

        return patterns

    def generate_insights(self, research_data, output_lang="en"):
        """Generate analytical insights from research"""

        findings = self.extract_key_findings(research_data)
        patterns = self.identify_patterns(findings)

        insights = {
            "total_findings": len(findings),
            "total_sources": sum(
                len(d.get("sources", [])) for d in research_data.values()
            ),
            "high_credibility_findings": len(
                [f for f in findings if f.get("credibility") == "high"]
            ),
            "key_patterns": patterns,
            "research_coverage": {
                angle: {
                    "findings": len(data.get("findings", [])),
                    "sources": len(data.get("sources", [])),
                }
                for angle, data in research_data.items()
            },
        }

        return insights

    def generate_analysis_report(self, task_dir, output_lang="en"):
        """Generate comprehensive analysis report"""

        # Load research data
        research_data = self.load_research_data(task_dir)

        # Generate insights
        insights = self.generate_insights(research_data, output_lang)

        # Create report
        if output_lang.startswith("zh"):
            report = self._generate_chinese_report(research_data, insights)
        else:
            report = self._generate_english_report(research_data, insights)

        # Save report
        output_file = f"{task_dir}/analysis/analysis_report.md"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        # Save insights JSON
        insights_file = f"{task_dir}/analysis/insights.json"
        with open(insights_file, "w", encoding="utf-8") as f:
            json.dump(insights, f, indent=2, ensure_ascii=False)

        print(f"📊 Analysis report generated: {output_file}")
        return output_file, insights

    def _generate_chinese_report(self, research_data, insights):
        """Generate Chinese analysis report"""

        report = f"""# 深度分析报告

## 分析概要

- **总发现数**: {insights["total_findings"]}
- **总来源数**: {insights["total_sources"]}
- **高可信度发现**: {insights["high_credibility_findings"]}

## 研究覆盖情况

| 研究角度 | 发现数 | 来源数 |
|----------|--------|--------|
"""

        for angle, coverage in insights["research_coverage"].items():
            report += f"| {angle} | {coverage['findings']} | {coverage['sources']} |\n"

        report += """
## 关键发现

### 高频主题

"""

        for topic, count in insights["key_patterns"]["high_frequency_topics"][:5]:
            report += f"- **{topic}**: 出现{count}次\n"

        report += """
## 深度洞察

### 主要趋势

[待分析填充]

### 风险识别

[待分析填充]

### 机会分析

[待分析填充]

## 结论

[待分析填充]
"""

        return report

    def _generate_english_report(self, research_data, insights):
        """Generate English analysis report"""

        report = f"""# Deep Analysis Report

## Analysis Summary

- **Total Findings**: {insights["total_findings"]}
- **Total Sources**: {insights["total_sources"]}
- **High Credibility Findings**: {insights["high_credibility_findings"]}

## Research Coverage

| Research Angle | Findings | Sources |
|----------------|----------|---------|
"""

        for angle, coverage in insights["research_coverage"].items():
            report += f"| {angle} | {coverage['findings']} | {coverage['sources']} |\n"

        report += """
## Key Findings

### High Frequency Topics

"""

        for topic, count in insights["key_patterns"]["high_frequency_topics"][:5]:
            report += f"- **{topic}**: Appears {count} times\n"

        report += """
## Deep Insights

### Key Trends

[To be analyzed]

### Risk Assessment

[To be analyzed]

### Opportunity Analysis

[To be analyzed]

## Conclusions

[To be analyzed]
"""

        return report


def main():
    """CLI interface"""

    if len(sys.argv) < 2:
        print("Usage: python3 analysis_engine.py <command> [args]")
        print("Commands:")
        print("  analyze <task_dir> [lang] - Analyze research data")
        sys.exit(1)

    command = sys.argv[1]
    engine = AnalysisEngine()

    if command == "analyze":
        task_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        lang = sys.argv[3] if len(sys.argv) > 3 else "en"

        output_file, insights = engine.generate_analysis_report(task_dir, lang)
        print(json.dumps(insights, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
