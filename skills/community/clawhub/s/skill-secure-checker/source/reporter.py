#!/usr/bin/env python3
"""
Report generator for security scan results
Supports JSON and HTML output formats
"""

import json
from pathlib import Path
from typing import Dict, Any

class ReportGenerator:
    def __init__(self, results: Dict[str, Any], output_format: str = "json"):
        self.results = results
        self.output_format = output_format

    def generate(self) -> str:
        """Generate report in specified format"""
        if self.output_format == "json":
            return self._generate_json()
        elif self.output_format == "html":
            return self._generate_html()
        else:  # both handled by caller
            return self._generate_json()

    def _generate_json(self) -> str:
        """Generate JSON report"""
        return json.dumps(self.results, indent=2, ensure_ascii=False)

    def _generate_html(self) -> str:
        """Generate HTML dashboard (beautified with frontend-design style)"""
        skill = self.results["skill"]
        scan_time = self.results["scan_time"]
        total_files = self.results["total_files"]
        total_lines = self.results["total_lines"]
        findings = self.results["findings"]
        risk_score = self.results["risk_score"]
        risk_level = self.results["risk_level"]
        issues = self.results["issues"]

        # Color coding for risk levels
        risk_colors = {
            "low": "#22c55e",      # green
            "medium": "#f59e0b",   # amber
            "high": "#ef4444",     # red
            "critical": "#991b1b"  # dark red
        }
        color = risk_colors.get(risk_level, "#6b7280")

        # Issue type icons
        issue_icons = {
            "dangerous_function": "⚠️",
            "hardcoded_secret": "🔑",
            "insecure_communication": "🌐",
            "path_traversal": "📁",
            "config_secret": "⚙️",
            "potential_secret": "🔍",
            "syntax_error": "🐛"
        }

        # Group issues by severity
        issues_by_severity = {"critical": [], "high": [], "medium": [], "low": []}
        for issue in issues:
            issues_by_severity[issue["severity"]].append(issue)

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 Security Scan Report - {skill}</title>
    <style>
        :root {{
            --primary: #3b82f6;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --critical: #991b1b;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-700: #374151;
            --gray-900: #111827;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5rem;
            font-weight: 700;
        }}
        .header p {{
            margin: 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        .meta {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        .content {{ padding: 40px; }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: var(--gray-700);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .risk-badge {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 9999px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: {color};
            color: white;
        }}
        .issues-section {{ margin-top: 40px; }}
        .section-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .severity-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .tab {{
            padding: 10px 20px;
            border-radius: 8px;
            background: var(--gray-100);
            cursor: pointer;
            font-weight: 500;
            border: 2px solid transparent;
            transition: all 0.2s;
        }}
        .tab.active {{
            border-color: var(--primary);
            background: white;
        }}
        .issue-card {{
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
            border-left: 4px solid var(--gray-200);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
        }}
        .issue-card.critical {{ border-left-color: var(--critical); }}
        .issue-card.high {{ border-left-color: var(--danger); }}
        .issue-card.medium {{ border-left-color: var(--warning); }}
        .issue-card.low {{ border-left-color: var(--success); }}
        .issue-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }}
        .issue-title {{
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .issue-severity {{
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .severity-critical {{ background: var(--critical); color: white; }}
        .severity-high {{ background: var(--danger); color: white; }}
        .severity-medium {{ background: var(--warning); color: white; }}
        .severity-low {{ background: var(--success); color: white; }}
        .issue-location {{
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 0.85rem;
            color: var(--gray-700);
            margin-bottom: 8px;
        }}
        .issue-message {{ color: var(--gray-900); margin-bottom: 12px; }}
        .code-block {{
            background: #1f2937;
            color: #f3f4f6;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            margin-top: 10px;
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: var(--gray-700);
            font-size: 0.9rem;
            border-top: 1px solid var(--gray-200);
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .content {{ padding: 20px; }}
            .meta {{ flex-direction: column; gap: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Security Scan Report</h1>
            <p>Skill Security Scanner v0.1.0 (MVP)</p>
            <div class="meta">
                <span>📦 Skill: {skill}</span>
                <span>🕒 {scan_time}</span>
                <span>📊 {total_files} files, {total_lines} lines</span>
            </div>
        </div>

        <div class="content">
            <div class="summary">
                <div class="stat-card">
                    <div class="stat-value" style="color: var(--primary)">{total_files}</div>
                    <div class="stat-label">Files Scanned</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: var(--primary)">{findings}</div>
                    <div class="stat-label">Issues Found</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: {color}">{risk_score}</div>
                    <div class="stat-label">Risk Score</div>
                </div>
                <div class="stat-card">
                    <div class="stat-badge">
                        <span class="risk-badge" style="background: {color}">{risk_level.upper()}</span>
                    </div>
                    <div class="stat-label">Risk Level</div>
                </div>
            </div>

            <div class="issues-section">
                <h2 class="section-title">
                    <span>📋</span>
                    <span>Security Issues ({findings})</span>
                </h2>
'''

        if not issues:
            html += '''
                <div style="background: #dcfce7; border: 1px solid #86efac; border-radius: 8px; padding: 30px; text-align: center; color: #166534;">
                    <h3 style="margin: 0 0 10px 0;">🎉 No security issues found!</h3>
                    <p style="margin: 0;">Your skill passed all security checks.</p>
                </div>
            '''
        else:
            # Add severity filter tabs
            html += '''
                <div class="severity-tabs">
                    <button class="tab active" onclick="filterIssues('all')">All ({total})</button>
            '''.format(total=len(issues))

            for severity in ["critical", "high", "medium", "low"]:
                count = len(issues_by_severity[severity])
                if count > 0:
                    html += f'''
                    <button class="tab" onclick="filterIssues('{severity}')">{severity.title()} ({count})</button>
                    '''

            html += '''
                </div>
                <div id="issues-list">
            '''

            for idx, issue in enumerate(issues, 1):
                severity = issue["severity"]
                icon = issue_icons.get(issue["type"], "🔍")
                html += f'''
                <div class="issue-card {severity}" data-severity="{severity}">
                    <div class="issue-header">
                        <div class="issue-title">
                            <span>{icon}</span>
                            <span>{issue['type'].replace('_', ' ').title()}</span>
                        </div>
                        <span class="issue-severity severity-{severity}">{severity}</span>
                    </div>
                    <div class="issue-location">
                        📁 {issue['file']}:{issue['line']}
                    </div>
                    <div class="issue-message">{issue['message']}</div>
                    <div class="code-block"><pre>{issue['snippet']}</pre></div>
                </div>
                '''

            html += '''
                </div>
            '''

        html += '''
        </div>

        <div class="footer">
            <p>Generated by skill-security-scanner | MIT License | 小叮当</p>
            <p style="margin-top: 10px; font-size: 0.8rem; opacity: 0.7;">
                Note: This is a static analysis tool. Some vulnerabilities may not be detected.
            </p>
        </div>
    </div>

    <script>
        function filterIssues(severity) {{
            const cards = document.querySelectorAll('.issue-card');
            const tabs = document.querySelectorAll('.tab');

            // Update active tab
            tabs.forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');

            // Filter cards
            cards.forEach(card => {{
                if (severity === 'all' || card.dataset.severity === severity) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>'''

        return html