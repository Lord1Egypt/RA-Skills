#!/usr/bin/env python3
"""
Report Generator
Generate professional Markdown and PDF reports
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    def __init__(self, workspace=None):
        self.workspace = workspace or os.environ.get("OPENCLAW_WORKSPACE", os.getcwd())

    def load_task_data(self, task_dir):
        """Load all task data"""

        data = {"meta": {}, "progress": {}, "plan": "", "research": {}, "analysis": {}}

        # Load meta
        meta_file = f"{task_dir}/meta.json"
        if os.path.exists(meta_file):
            with open(meta_file, "r", encoding="utf-8") as f:
                data["meta"] = json.load(f)

        # Load progress
        progress_file = f"{task_dir}/progress.json"
        if os.path.exists(progress_file):
            with open(progress_file, "r", encoding="utf-8") as f:
                data["progress"] = json.load(f)

        # Load plan
        plan_file = f"{task_dir}/plan.md"
        if os.path.exists(plan_file):
            with open(plan_file, "r", encoding="utf-8") as f:
                data["plan"] = f.read()

        # Load research
        research_dir = f"{task_dir}/research"
        if os.path.exists(research_dir):
            for filename in os.listdir(research_dir):
                if filename.endswith(".md"):
                    filepath = f"{research_dir}/{filename}"
                    with open(filepath, "r", encoding="utf-8") as f:
                        angle_id = filename.replace(".md", "")
                        data["research"][angle_id] = f.read()

        # Load analysis
        analysis_dir = f"{task_dir}/analysis"
        if os.path.exists(analysis_dir):
            analysis_file = f"{analysis_dir}/analysis_report.md"
            if os.path.exists(analysis_file):
                with open(analysis_file, "r", encoding="utf-8") as f:
                    data["analysis"]["report"] = f.read()

            insights_file = f"{analysis_dir}/insights.json"
            if os.path.exists(insights_file):
                with open(insights_file, "r", encoding="utf-8") as f:
                    data["analysis"]["insights"] = json.load(f)

        return data

    def generate_report(self, task_dir, output_lang="en"):
        """Generate final research report"""

        # Load all data
        data = self.load_task_data(task_dir)

        topic = data["meta"].get("query", "Research Report")
        task_id = data["meta"].get("task_id", "unknown")

        # Generate report based on language
        if output_lang.startswith("zh"):
            report = self._generate_chinese_report(topic, task_id, data)
        else:
            report = self._generate_english_report(topic, task_id, data)

        # Save report
        output_dir = f"{self.workspace}/deep-research/output/{task_id}"
        os.makedirs(output_dir, exist_ok=True)

        md_file = f"{output_dir}/report.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"📄 Report generated: {md_file}")
        return md_file

    def _generate_chinese_report(self, topic, task_id, data):
        """Generate Chinese report"""

        insights = data["analysis"].get("insights", {})
        total_findings = insights.get("total_findings", 0)
        total_sources = insights.get("total_sources", 0)

        report = f"""---
title: "{topic}"
subtitle: "深度研究报告"
date: "{datetime.now().strftime("%Y年%m月%d日")}"
author: "Deep Research Agent"
version: "1.0"
task_id: "{task_id}"
---

<div class="cover">

# {topic}

## 深度研究报告

**研究日期**: {datetime.now().strftime("%Y年%m月%d日")}

**任务ID**: {task_id}

---

**Deep Research Agent**

</div>

---

# 执行摘要

> 本报告对"{topic}"进行了全面深入的研究与分析。

**关键数据**:
- 总发现数: {total_findings}
- 总来源数: {total_sources}
- 研究角度: {len(data.get("research", {}))}个

---

# 目录

1. 研究方法论
2. 研究发现
3. 深度分析
4. 风险与机遇
5. 结论与建议
6. 参考文献

---

# 1. 研究方法论

## 1.1 研究概述

本研究采用多源信息收集与交叉验证方法，确保研究结果的准确性和可靠性。

## 1.2 数据来源

| 来源类型 | 数量 | 说明 |
|----------|------|------|
| 行业报告 | - | Gartner、IDC等 |
| 新闻报道 | - | 主流媒体 |
| 学术论文 | - | arXiv、Google Scholar |
| 官方数据 | - | 政府、企业 |

## 1.3 研究限制

- 部分数据可能存在时效性差异
- 某些领域数据可获得性有限

---

# 2. 研究发现

"""

        # Add research findings
        for angle_id, content in data.get("research", {}).items():
            report += f"## 2.{list(data['research'].keys()).index(angle_id) + 1} {angle_id.replace('_', ' ').title()}\n\n"
            report += content + "\n\n"

        report += """
---

# 3. 深度分析

"""

        # Add analysis
        if "report" in data.get("analysis", {}):
            report += data["analysis"]["report"]

        report += """

---

# 4. 风险与机遇

## 4.1 主要风险

[待分析填充]

## 4.2 发展机遇

[待分析填充]

---

# 5. 结论与建议

## 5.1 主要结论

[待分析填充]

## 5.2 建议

[待分析填充]

---

# 6. 参考文献

"""

        # Add sources
        all_sources = []
        for content in data.get("research", {}).values():
            # Extract sources from content (simplified)
            lines = content.split("\n")
            for line in lines:
                if line.startswith("- ") and ("http" in line or "www" in line):
                    all_sources.append(line)

        for i, source in enumerate(all_sources[:20], 1):
            report += f"[{i}] {source}\n"

        report += f"""

---

<div class="footnote">

**报告生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**生成工具**: Deep Research Agent

</div>
"""

        return report

    def _generate_english_report(self, topic, task_id, data):
        """Generate English report"""

        insights = data["analysis"].get("insights", {})
        total_findings = insights.get("total_findings", 0)
        total_sources = insights.get("total_sources", 0)

        report = f"""---
title: "{topic}"
subtitle: "Deep Research Report"
date: "{datetime.now().strftime("%B %d, %Y")}"
author: "Deep Research Agent"
version: "1.0"
task_id: "{task_id}"
---

<div class="cover">

# {topic}

## Deep Research Report

**Research Date**: {datetime.now().strftime("%B %d, %Y")}

**Task ID**: {task_id}

---

**Deep Research Agent**

</div>

---

# Executive Summary

> This report provides a comprehensive analysis of "{topic}".

**Key Metrics**:
- Total Findings: {total_findings}
- Total Sources: {total_sources}
- Research Angles: {len(data.get("research", {}))}

---

# Table of Contents

1. Methodology
2. Research Findings
3. Deep Analysis
4. Risks & Opportunities
5. Conclusions & Recommendations
6. References

---

# 1. Methodology

## 1.1 Research Overview

This research employed multi-source information collection and cross-validation methods to ensure accuracy and reliability of findings.

## 1.2 Data Sources

| Source Type | Count | Description |
|-------------|-------|-------------|
| Industry Reports | - | Gartner, IDC, etc. |
| News Articles | - | Major media outlets |
| Academic Papers | - | arXiv, Google Scholar |
| Official Data | - | Government, corporate |

## 1.3 Research Limitations

- Some data may have time-lag differences
- Limited data availability in certain areas

---

# 2. Research Findings

"""

        # Add research findings
        for angle_id, content in data.get("research", {}).items():
            report += f"## 2.{list(data['research'].keys()).index(angle_id) + 1} {angle_id.replace('_', ' ').title()}\n\n"
            report += content + "\n\n"

        report += """
---

# 3. Deep Analysis

"""

        # Add analysis
        if "report" in data.get("analysis", {}):
            report += data["analysis"]["report"]

        report += """

---

# 4. Risks & Opportunities

## 4.1 Key Risks

[To be analyzed]

## 4.2 Development Opportunities

[To be analyzed]

---

# 5. Conclusions & Recommendations

## 5.1 Main Conclusions

[To be analyzed]

## 5.2 Recommendations

[To be analyzed]

---

# 6. References

"""

        # Add sources
        all_sources = []
        for content in data.get("research", {}).values():
            lines = content.split("\n")
            for line in lines:
                if line.startswith("- ") and ("http" in line or "www" in line):
                    all_sources.append(line)

        for i, source in enumerate(all_sources[:20], 1):
            report += f"[{i}] {source}\n"

        report += f"""

---

<div class="footnote">

**Report Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Generated By**: Deep Research Agent

</div>
"""

        return report


def main():
    """CLI interface"""

    if len(sys.argv) < 2:
        print("Usage: python3 report_generator.py <command> [args]")
        print("Commands:")
        print("  generate <task_dir> [lang] - Generate report")
        sys.exit(1)

    command = sys.argv[1]
    generator = ReportGenerator()

    if command == "generate":
        task_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        lang = sys.argv[3] if len(sys.argv) > 3 else "en"

        md_file = generator.generate_report(task_dir, lang)
        print(f"Report: {md_file}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
