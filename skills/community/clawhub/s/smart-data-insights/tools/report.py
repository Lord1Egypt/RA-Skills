#!/usr/bin/env python3
"""
Report generation utilities.
"""

from datetime import datetime
from pathlib import Path


def generate_report(summary, issues, insights, output_path):
    """
    Generate a comprehensive markdown report.
    
    Args:
        summary: Data summary dictionary
        issues: List of data quality issues
        insights: List of insights
        output_path: Path to save the report
    """
    report = []
    
    # Header
    report.append("# Data Analysis Report")
    report.append(f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    # Executive Summary
    report.append("## Executive Summary\n")
    report.append(f"This dataset contains **{summary['rows']:,} rows** and **{summary['columns']} columns**.")
    
    total_missing = sum(summary['missing_values'].values())
    if total_missing > 0:
        report.append(f"There are **{total_missing:,} missing values** across the dataset.")
    
    if issues:
        high_priority = [i for i in issues if i.get('percentage', 0) > 20]
        if high_priority:
            report.append(f"\n⚠️ **{len(high_priority)} significant data quality issues** require attention.")
    
    # Dataset Overview
    report.append("\n## Dataset Overview\n")
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Rows | {summary['rows']:,} |")
    report.append(f"| Columns | {summary['columns']} |")
    report.append(f"| Missing Values | {total_missing:,} |")
    report.append(f"| Duplicate Rows | {summary.get('duplicates', 'N/A')} |")
    
    # Column Information
    report.append("\n## Column Information\n")
    report.append("| Column | Type | Missing | Missing % |")
    report.append("|--------|------|---------|-----------|")
    
    for col in summary['column_names']:
        dtype = summary['dtypes'].get(col, 'unknown')
        missing = summary['missing_values'].get(col, 0)
        missing_pct = summary['missing_percentage'].get(col, 0)
        report.append(f"| {col} | {dtype} | {missing} | {missing_pct:.1f}% |")
    
    # Numeric Statistics
    if 'numeric_stats' in summary and summary['numeric_stats']:
        report.append("\n## Numeric Statistics\n")
        report.append("| Column | Mean | Median | Std Dev | Min | Max |")
        report.append("|--------|------|--------|---------|-----|-----|")
        
        for col, stats in summary['numeric_stats'].items():
            mean = f"{stats['mean']:.2f}" if stats['mean'] is not None else 'N/A'
            median = f"{stats['median']:.2f}" if stats['median'] is not None else 'N/A'
            std = f"{stats['std']:.2f}" if stats['std'] is not None else 'N/A'
            min_val = f"{stats['min']:.2f}" if stats['min'] is not None else 'N/A'
            max_val = f"{stats['max']:.2f}" if stats['max'] is not None else 'N/A'
            report.append(f"| {col} | {mean} | {median} | {std} | {min_val} | {max_val} |")
    
    # Categorical Statistics
    if 'categorical_stats' in summary and summary['categorical_stats']:
        report.append("\n## Categorical Statistics\n")
        
        for col, stats in summary['categorical_stats'].items():
            report.append(f"### {col}\n")
            report.append(f"- **Unique values**: {stats['unique_count']}")
            report.append(f"- **Top values**:")
            for value, count in list(stats['top_values'].items())[:5]:
                report.append(f"  - {value}: {count}")
            report.append("")
    
    # Data Quality Issues
    if issues:
        report.append("\n## Data Quality Issues\n")
        
        # Group by issue type
        issue_groups = {}
        for issue in issues:
            issue_type = issue['type']
            if issue_type not in issue_groups:
                issue_groups[issue_type] = []
            issue_groups[issue_type].append(issue)
        
        for issue_type, group in issue_groups.items():
            report.append(f"### {issue_type.replace('_', ' ').title()}\n")
            for issue in group:
                report.append(f"- {issue['suggestion']}")
            report.append("")
    
    # Insights
    if insights:
        report.append("\n## Key Insights\n")
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        insights_sorted = sorted(insights, key=lambda x: priority_order.get(x['priority'], 3))
        
        for insight in insights_sorted:
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(insight['priority'], '⚪')
            report.append(f"### {priority_emoji} [{insight['priority'].upper()}] {insight['category'].replace('_', ' ').title()}\n")
            report.append(f"**{insight['message']}**\n")
            if 'details' in insight:
                for detail in insight['details']:
                    report.append(f"- {detail}")
            report.append("")
    
    # Recommendations
    report.append("\n## Recommendations\n")
    
    if issues:
        report.append("### Data Cleaning\n")
        report.append("1. Remove duplicate rows")
        report.append("2. Handle missing values appropriately")
        report.append("3. Investigate and address outliers")
        report.append("")
    
    report.append("### Next Steps\n")
    report.append("1. Review the data quality issues identified above")
    report.append("2. Consider feature engineering opportunities")
    report.append("3. Explore correlations between key variables")
    report.append("4. Build predictive models if applicable")
    
    # Footer
    report.append("\n---\n")
    report.append("*Report generated by Data Analyst Skill*")
    
    # Write to file
    output_path = Path(output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))


def generate_executive_summary(summary, issues, insights):
    """Generate a brief executive summary."""
    lines = []
    
    lines.append(f"📊 Dataset: {summary['rows']:,} rows × {summary['columns']} columns")
    
    total_missing = sum(summary['missing_values'].values())
    if total_missing > 0:
        missing_pct = total_missing / (summary['rows'] * summary['columns']) * 100
        lines.append(f"⚠️ Missing data: {total_missing:,} values ({missing_pct:.1f}%)")
    
    if issues:
        high_priority = len([i for i in issues if i.get('percentage', 0) > 20])
        if high_priority:
            lines.append(f"🔴 Critical issues: {high_priority}")
    
    if insights:
        high_insights = len([i for i in insights if i['priority'] == 'high'])
        if high_insights:
            lines.append(f"💡 Key insights: {high_insights}")
    
    return '\n'.join(lines)
