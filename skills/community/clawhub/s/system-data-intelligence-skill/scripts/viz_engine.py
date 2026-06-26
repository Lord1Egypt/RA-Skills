#!/usr/bin/env python3
"""
Visualization Engine — Plotly interactive + Matplotlib static output.
Usage: python viz_engine.py <analysis_result.json> <output_dir>
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

STYLE = {
    'font': 'Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif',
    'bg': '#FAFAFA',
    'grid': '#E8E8E8',
    'colors': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B4A6B', '#6BAB5E'],
    'title_size': 18,
    'axis_size': 12,
}


def create_dashboard(report: dict, title: str = "Data Intelligence Dashboard"):
    """Build a multi-panel interactive Plotly dashboard from analysis report."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    distributions = report.get('distributions', {})
    anomalies = report.get('anomalies', {})
    correlations = report.get('correlations', {})
    quality = report.get('quality', {})
    time_series = report.get('time_series', {})
    has_ts = bool(time_series and 'trend_7d' in time_series)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Trend Analysis' if has_ts else 'Value Distribution',
            'Missing Rate',
            'Anomaly Detection',
            'Correlation Matrix',
        ],
        vertical_spacing=0.14,
        horizontal_spacing=0.10,
    )

    # Panel 1: Time series or distribution
    if has_ts:
        dates = list(time_series['trend_7d'].keys())
        values = list(time_series['trend_7d'].values())
        fig.add_trace(go.Scatter(
            x=dates, y=values, mode='lines', name='7d Trend',
            line=dict(color=STYLE['colors'][0], width=2)
        ), row=1, col=1)
    elif distributions:
        col_name = next(iter(distributions))
        d = distributions[col_name]
        fig.add_trace(go.Bar(
            x=['Mean', 'Median', 'Q25', 'Q75'],
            y=[d['mean'], d['median'], d['q25'], d['q75']],
            name=col_name, marker_color=STYLE['colors'][0]
        ), row=1, col=1)

    # Panel 2: Missing rate
    mr = {k: v for k, v in quality.get('missing_rate', {}).items() if v > 0}
    if mr:
        fig.add_trace(go.Bar(
            x=list(mr.values()), y=list(mr.keys()), orientation='h',
            name='Missing Rate', marker_color=STYLE['colors'][2]
        ), row=1, col=2)
    else:
        fig.add_annotation(
            text="No missing data", xref="paper", yref="paper",
            x=0.75, y=0.75, showarrow=False, font=dict(size=14)
        )

    # Panel 3: Anomaly counts
    if anomalies:
        fig.add_trace(go.Bar(
            x=list(anomalies.keys()),
            y=[v['outlier_count'] for v in anomalies.values()],
            name='Outlier Count', marker_color=STYLE['colors'][3]
        ), row=2, col=1)

    # Panel 4: Correlation heatmap
    full_matrix = correlations.get('full_matrix', {})
    if full_matrix:
        keys = list(full_matrix.keys())
        z = [[full_matrix[r].get(c, 0) for c in keys] for r in keys]
        fig.add_trace(go.Heatmap(
            z=z, x=keys, y=keys, colorscale='RdYlGn', zmid=0, name='Correlation'
        ), row=2, col=2)

    fig.update_layout(
        title=dict(text=title, font=dict(size=STYLE['title_size'], family=STYLE['font'])),
        font=dict(family=STYLE['font'], size=STYLE['axis_size']),
        paper_bgcolor=STYLE['bg'],
        plot_bgcolor=STYLE['bg'],
        colorway=STYLE['colors'],
        height=800,
        showlegend=False,
    )
    fig.update_xaxes(gridcolor=STYLE['grid'])
    fig.update_yaxes(gridcolor=STYLE['grid'])
    return fig


def export_viz(fig, output_path: str, formats: list = None):
    """Export figure to HTML and optionally PNG."""
    if formats is None:
        formats = ['html', 'png']
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    if 'html' in formats:
        fig.write_html(f"{output_path}.html", include_plotlyjs='cdn')
        logger.info(f"HTML saved: {output_path}.html")
    if 'png' in formats:
        try:
            fig.write_image(f"{output_path}.png", scale=2, width=1200, height=800)
            logger.info(f"PNG saved: {output_path}.png")
        except Exception as e:
            logger.warning(f"PNG export failed (install kaleido): {e}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python viz_engine.py <analysis_result.json> <output_dir>")
        sys.exit(1)

    with open(sys.argv[1], encoding='utf-8') as f:
        report = json.load(f)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = str(Path(sys.argv[2]) / f"report_{timestamp}")
    fig = create_dashboard(report)
    export_viz(fig, output_path)
    logger.info(f"Done. HTML: {output_path}.html")


if __name__ == "__main__":
    main()
