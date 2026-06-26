#!/usr/bin/env python3
"""
TokenBooks - HTML Dashboard Generator
Generate visual HTML reports with CSS charts.

Author: Shadow Rose
License: MIT
"""

import json
from datetime import datetime
from typing import List, Dict
from token_books import CostAggregator, CostBreakdown, TimeSeries
from token_import import UsageRecord


class DashboardGenerator:
    """Generate HTML dashboard for spending analysis."""
    
    HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TokenBooks Dashboard</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 0.9em; }}
        .card {{
            background: white;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .metric {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .metric-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .bar-chart {{
            margin: 20px 0;
        }}
        .bar-item {{
            margin-bottom: 15px;
        }}
        .bar-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-size: 0.9em;
        }}
        .bar-bg {{
            background: #e9ecef;
            border-radius: 10px;
            height: 30px;
            position: relative;
            overflow: hidden;
        }}
        .bar-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            border-radius: 10px;
        }}
        .line-chart {{
            position: relative;
            height: 200px;
            margin: 20px 0;
            padding: 10px;
        }}
        .line-chart-bg {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 100%;
            border-bottom: 2px solid #ddd;
            border-left: 2px solid #ddd;
        }}
        .line-chart-bars {{
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            height: 100%;
        }}
        .line-bar {{
            flex: 1;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            margin: 0 2px;
            border-radius: 4px 4px 0 0;
            min-height: 2px;
        }}
        .waste-alert {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .budget-status {{
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .budget-ok {{ background: #d4edda; color: #155724; }}
        .budget-warning {{ background: #fff3cd; color: #856404; }}
        .budget-over {{ background: #f8d7da; color: #721c24; }}
        h2 {{ color: #667eea; margin-bottom: 20px; }}
        h3 {{ margin: 20px 0 10px 0; }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 TokenBooks Dashboard</h1>
            <div class="subtitle">Generated: {timestamp}</div>
        </div>
        
        {content}
        
        <div class="footer">
            <p>TokenBooks | Author: Shadow Rose | MIT License</p>
        </div>
    </div>
</body>
</html>
"""
    
    @classmethod
    def generate(cls, records: List[UsageRecord], monthly_budget: float = None) -> str:
        """
        Generate HTML dashboard.
        
        Args:
            records: Usage records
            monthly_budget: Optional monthly budget
        
        Returns:
            HTML string
        """
        aggregator = CostAggregator(records)
        
        # Build sections
        metrics_html = cls._build_metrics(aggregator)
        provider_html = cls._build_provider_chart(aggregator)
        model_html = cls._build_model_chart(aggregator)
        trend_html = cls._build_trend_chart(aggregator)
        waste_html = cls._build_waste_alerts(aggregator)
        
        budget_html = ''
        if monthly_budget:
            budget_html = cls._build_budget_status(aggregator, monthly_budget)
        
        content = f"""
        {budget_html}
        {metrics_html}
        {provider_html}
        {model_html}
        {trend_html}
        {waste_html}
        """
        
        return cls.HTML_TEMPLATE.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            content=content
        )
    
    @classmethod
    def _build_metrics(cls, aggregator: CostAggregator) -> str:
        """Build metrics overview."""
        total_cost = aggregator.get_total_cost()
        total_tokens = aggregator.get_total_tokens()
        
        by_provider = aggregator.by_provider()
        provider_count = len(by_provider)
        
        by_model = aggregator.by_model()
        model_count = len(by_model)
        
        return f"""
        <div class="card">
            <h2>📊 Overview</h2>
            <div class="metric-grid">
                <div class="metric">
                    <div class="metric-label">Total Spend</div>
                    <div class="metric-value">${total_cost:.2f}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Total Tokens</div>
                    <div class="metric-value">{total_tokens:,}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Providers</div>
                    <div class="metric-value">{provider_count}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Models Used</div>
                    <div class="metric-value">{model_count}</div>
                </div>
            </div>
        </div>
        """
    
    @classmethod
    def _build_provider_chart(cls, aggregator: CostAggregator) -> str:
        """Build provider breakdown chart."""
        by_provider = aggregator.by_provider()
        
        if not by_provider:
            return ''
        
        total_cost = sum(b.total_cost for b in by_provider.values())
        
        bars_html = ''
        for provider, breakdown in sorted(by_provider.items(), key=lambda x: x[1].total_cost, reverse=True):
            percentage = (breakdown.total_cost / total_cost * 100) if total_cost > 0 else 0
            
            bars_html += f"""
            <div class="bar-item">
                <div class="bar-label">
                    <span><strong>{provider}</strong></span>
                    <span>${breakdown.total_cost:.2f} ({percentage:.1f}%)</span>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" style="width: {percentage}%"></div>
                </div>
            </div>
            """
        
        return f"""
        <div class="card">
            <h2>📈 Spending by Provider</h2>
            <div class="bar-chart">
                {bars_html}
            </div>
        </div>
        """
    
    @classmethod
    def _build_model_chart(cls, aggregator: CostAggregator) -> str:
        """Build model breakdown chart."""
        by_model = aggregator.by_model()
        
        if not by_model:
            return ''
        
        total_cost = sum(b.total_cost for b in by_model.values())
        
        # Top 10 models
        top_models = sorted(by_model.items(), key=lambda x: x[1].total_cost, reverse=True)[:10]
        
        bars_html = ''
        for model, breakdown in top_models:
            percentage = (breakdown.total_cost / total_cost * 100) if total_cost > 0 else 0
            
            bars_html += f"""
            <div class="bar-item">
                <div class="bar-label">
                    <span><strong>{model}</strong></span>
                    <span>${breakdown.total_cost:.2f} ({breakdown.request_count} requests)</span>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" style="width: {percentage}%"></div>
                </div>
            </div>
            """
        
        return f"""
        <div class="card">
            <h2>📈 Top Models by Cost</h2>
            <div class="bar-chart">
                {bars_html}
            </div>
        </div>
        """
    
    @classmethod
    def _build_trend_chart(cls, aggregator: CostAggregator) -> str:
        """Build time series trend chart."""
        series = aggregator.time_series(period='day')
        
        if not series:
            return ''
        
        max_cost = max(s.cost for s in series) if series else 1
        
        bars_html = ''
        for point in series[-30:]:  # Last 30 days
            height_percent = (point.cost / max_cost * 100) if max_cost > 0 else 0
            bars_html += f'<div class="line-bar" style="height: {height_percent}%" title="{point.date}: ${point.cost:.2f}"></div>'
        
        return f"""
        <div class="card">
            <h2>📅 Daily Spending Trend (Last 30 Days)</h2>
            <div class="line-chart">
                <div class="line-chart-bg"></div>
                <div class="line-chart-bars">
                    {bars_html}
                </div>
            </div>
        </div>
        """
    
    @classmethod
    def _build_waste_alerts(cls, aggregator: CostAggregator) -> str:
        """Build waste detection alerts."""
        waste = aggregator.detect_waste()
        
        if not waste:
            return ''
        
        alerts_html = ''
        for case in waste[:5]:  # Top 5
            alerts_html += f"""
            <div class="waste-alert">
                <strong>⚠️ {case['model']}</strong><br>
                Cost: ${case['total_cost']:.2f} across {case['request_count']} requests<br>
                <em>{case['suggestion']}</em>
            </div>
            """
        
        return f"""
        <div class="card">
            <h2>💡 Potential Optimizations</h2>
            {alerts_html}
        </div>
        """
    
    @classmethod
    def _build_budget_status(cls, aggregator: CostAggregator, monthly_budget: float) -> str:
        """Build budget status card."""
        budget = aggregator.budget_analysis(monthly_budget)
        
        status_class = f"budget-{budget['status'].replace('_', '-')}"
        
        return f"""
        <div class="card">
            <h2>💰 Budget Status</h2>
            <div class="budget-status {status_class}">
                <strong>Monthly Budget: ${budget['budget']:.2f}</strong><br>
                Spent: ${budget['spent']:.2f} | Remaining: ${budget['remaining']:.2f}<br>
                Utilization: {budget['utilization_percent']:.1f}%
            </div>
        </div>
        """


def main():
    """CLI interface for dashboard generation."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='TokenBooks Dashboard Generator'
    )
    parser.add_argument(
        'data',
        help='Input JSON data file'
    )
    parser.add_argument(
        '--output',
        default='dashboard.html',
        help='Output HTML file'
    )
    parser.add_argument(
        '--budget',
        type=float,
        help='Monthly budget in USD'
    )
    
    args = parser.parse_args()
    
    try:
        # Load data
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        records = [
            UsageRecord(**record) for record in data
        ]
        
        # Generate dashboard
        html = DashboardGenerator.generate(records, monthly_budget=args.budget)
        
        # Write output
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Dashboard generated: {args.output}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
