"""
Visualization module for LSE options flow analysis.
Generates interactive Plotly charts and a combined HTML dashboard.
"""
from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from lse_options import CompositePrediction, Signal, LSEClient, _filter_valid_prints


def _spot_line(fig: go.Figure, spot: float, row: int = 1, col: int = 1):
    """Add a vertical spot-price reference line."""
    fig.add_vline(
        x=spot, line_dash="dash", line_color="royalblue", line_width=2,
        annotation_text=f"Spot ${spot:,.0f}",
        row=row, col=col,
    )


# ---------------------------------------------------------------------------
# Chart 1: Flow GEX Profile
# ---------------------------------------------------------------------------

def chart_gex_profile(signal: Signal, spot: float, symbol: str) -> go.Figure:
    """Gamma exposure by strike — shows dealer positioning from today's flow."""
    raw = signal.raw
    by_strike = raw["by_strike"]
    strikes = sorted(by_strike.keys())

    call_gex = [by_strike[s]["call_gex"] / 1e6 for s in strikes]
    put_gex = [by_strike[s]["put_gex"] / 1e6 for s in strikes]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=strikes, y=[g if g > 0 else 0 for g in call_gex],
        name="Call GEX (+)", marker_color="#22c55e",
        hovertemplate="Strike %{x}<br>Call GEX $%{y:.1f}M<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=strikes, y=[g if g > 0 else 0 for g in [-g for g in put_gex]],
        name="Put GEX (−)", marker_color="#ef4444",
        hovertemplate="Strike %{x}<br>Put GEX $%{y:.1f}M<extra></extra>",
    ))

    _spot_line(fig, spot)
    fig.add_vline(x=raw["call_wall"], line_dash="dot", line_color="#16a34a",
                  annotation_text=f"Call Wall {raw['call_wall']}")
    fig.add_vline(x=raw["put_wall"], line_dash="dot", line_color="#dc2626",
                  annotation_text=f"Put Wall {raw['put_wall']}")

    net = raw["net_gex"] / 1e6
    regime = "Positive (Vol Suppressed)" if net > 0 else "Negative (Vol Amplified)"

    fig.update_layout(
        barmode="relative",
        title=f"{symbol} — Flow Gamma Exposure by Strike<br>"
              f"<sup>Net GEX ${net:+.1f}M — {regime}</sup>",
        xaxis_title="Strike Price",
        yaxis_title="Gamma Exposure ($M)",
        height=450,
        template="plotly_dark",
        showlegend=True,
    )
    return fig


# ---------------------------------------------------------------------------
# Chart 2: Premium Walls
# ---------------------------------------------------------------------------

def chart_premium_walls(signal: Signal, spot: float, symbol: str) -> go.Figure:
    """Net premium by strike — shows institutional commitment levels."""
    raw = signal.raw
    by_strike = raw["by_strike"]
    strikes = sorted(by_strike.keys())

    call_prem = [by_strike[s]["call_prem"] / 1e6 for s in strikes]
    put_prem = [by_strike[s]["put_prem"] / 1e6 for s in strikes]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=strikes, y=call_prem, name="Call Premium",
        marker_color="#22c55e",
        hovertemplate="Strike %{x}<br>Call $%{y:.1f}M<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=strikes, y=put_prem, name="Put Premium",
        marker_color="#ef4444",
        hovertemplate="Strike %{x}<br>Put $%{y:.1f}M<extra></extra>",
    ))

    _spot_line(fig, spot)
    fig.add_vline(x=raw["magnet_strike"], line_dash="dot", line_color="#a855f7",
                  annotation_text=f"Magnet {raw['magnet_strike']}")

    fig.update_layout(
        barmode="group",
        title=f"{symbol} — Premium Walls (Flow-Based)<br>"
              f"<sup>Total ${raw['total_call']/1e6:.1f}M calls / "
              f"${raw['total_put']/1e6:.1f}M puts — "
              f"Premium magnet @ {raw['magnet_strike']}</sup>",
        xaxis_title="Strike Price",
        yaxis_title="Premium ($M)",
        height=450,
        template="plotly_dark",
        showlegend=True,
    )
    return fig


# ---------------------------------------------------------------------------
# Chart 3: IV Smile
# ---------------------------------------------------------------------------

def chart_iv_smile(flow: list[dict], spot: float, symbol: str) -> go.Figure:
    """IV vs strike for calls and puts — shows the volatility skew."""
    valid = _filter_valid_prints(flow)
    calls = sorted(
        [p for p in valid if p["contract_type"] == "call"],
        key=lambda p: p["strike"],
    )
    puts = sorted(
        [p for p in valid if p["contract_type"] == "put"],
        key=lambda p: p["strike"],
    )

    fig = go.Figure()
    if calls:
        fig.add_trace(go.Scatter(
            x=[c["strike"] for c in calls],
            y=[c["iv"] * 100 for c in calls],
            mode="lines+markers", name="Call IV",
            line=dict(color="#22c55e", width=2),
            hovertemplate="Strike %{x}<br>IV %{y:.1f}%<extra></extra>",
        ))
    if puts:
        fig.add_trace(go.Scatter(
            x=[p["strike"] for p in puts],
            y=[p["iv"] * 100 for p in puts],
            mode="lines+markers", name="Put IV",
            line=dict(color="#ef4444", width=2),
            hovertemplate="Strike %{x}<br>IV %{y:.1f}%<extra></extra>",
        ))

    _spot_line(fig, spot)

    fig.update_layout(
        title=f"{symbol} — Implied Volatility Smile (from Flow Prints)",
        xaxis_title="Strike Price",
        yaxis_title="Implied Volatility (%)",
        height=400,
        template="plotly_dark",
        showlegend=True,
    )
    return fig


# ---------------------------------------------------------------------------
# Chart 4: Signal Dashboard (composite gauge)
# ---------------------------------------------------------------------------

def chart_signal_dashboard(pred: CompositePrediction) -> go.Figure:
    """Radar/gauge showing each signal's directional contribution."""
    signal_names = [s.name.replace("_", " ").upper() for s in pred.signals]
    # Map direction+confidence to [-1, 1] signed score
    scores = [s.direction * s.confidence for s in pred.signals]

    fig = go.Figure()
    # Bars: positive = bullish (green), negative = bearish (red)
    colors = ["#22c55e" if s > 0 else "#ef4444" for s in scores]
    fig.add_trace(go.Bar(
        x=signal_names, y=scores,
        marker_color=colors,
        text=[f"{s:+.2f}" for s in scores],
        textposition="outside",
        hovertemplate="%{x}<br>Score %{y:+.2f}<extra></extra>",
    ))

    composite = pred.direction * pred.confidence
    fig.add_hline(y=composite, line_dash="dash", line_color="#fbbf24",
                  annotation_text=f"Composite: {composite:+.2f}")

    fig.update_layout(
        title=f"{pred.symbol} — Signal Dashboard<br>"
              f"<sup>Direction: {['NEUTRAL','BULLISH','BEARISH'][pred.direction]} "
              f"| Confidence: {pred.confidence:.0%} "
              f"| Disagreement: {pred.disagreement:.3f}</sup>",
        yaxis_title="Signed Confidence Score (-1 to +1)",
        yaxis_range=[-1, 1],
        height=400,
        template="plotly_dark",
        showlegend=False,
    )
    return fig


# ---------------------------------------------------------------------------
# Chart 5: Expiration Risk-Neutral Density
# ---------------------------------------------------------------------------

def chart_expiration_density(forecast, symbol: str) -> go.Figure:
    """Risk-neutral density from Breeden-Litzenberger with CI bands."""
    strikes = forecast.density_strikes
    density = forecast.density_values
    spot = forecast.spot

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=strikes, y=density,
        mode="lines", name="Risk-Neutral Density",
        line=dict(color="#60a5fa", width=2.5),
        fill="tozeroy", fillcolor="rgba(96,165,250,0.15)",
        hovertemplate="Strike $%{x:,.0f}<br>Density %{y:.4f}<extra></extra>",
    ))

    def add_ci_band(lo, hi, name, color, opacity):
        mask = (strikes >= lo) & (strikes <= hi)
        if mask.any():
            fig.add_trace(go.Scatter(
                x=strikes[mask], y=density[mask],
                mode="lines", name=f"{name}: ${lo:,.0f}–${hi:,.0f}",
                line=dict(color=f"rgba({color},0)", width=0),
                fill="tozeroy", fillcolor=f"rgba({color},{opacity})",
                hoverinfo="skip",
            ))

    add_ci_band(forecast.ci_95[0], forecast.ci_95[1], "95% CI", "239,68,68", 0.08)
    add_ci_band(forecast.ci_80[0], forecast.ci_80[1], "80% CI", "245,158,11", 0.12)
    add_ci_band(forecast.ci_50[0], forecast.ci_50[1], "50% CI", "34,197,94", 0.15)

    fig.add_vline(x=spot, line_dash="dash", line_color="royalblue", line_width=2,
                  annotation_text=f"Spot ${spot:,.0f}")
    fig.add_vline(x=forecast.median, line_dash="dot", line_color="#a855f7", line_width=2,
                  annotation_text=f"Median ${forecast.median:,.0f}")
    fig.add_vline(x=forecast.forward_price, line_dash="longdash", line_color="#94a3b8",
                  line_width=1.5,
                  annotation_text=f"Forward ${forecast.forward_price:,.0f}")

    if forecast.premium_magnet:
        fig.add_vline(x=forecast.premium_magnet, line_dash="dashdot",
                      line_color="#f472b6", line_width=1.5,
                      annotation_text=f"Heaviest flow ${forecast.premium_magnet:,.0f}")

    dirs_prob = forecast.prob_above_spot
    title = (
        f"{symbol} — Risk-Neutral Close Distribution ({forecast.expiry}, {forecast.dte}d)<br>"
        f"<sup>ATM IV {forecast.atm_iv:.0%} | "
        f"Q(close > spot) {dirs_prob:.0%} | "
        f"Skew {forecast.skew:+.3f} | No-arb: {forecast.arb_check.get('status', 'n/a')}</sup>"
    )

    # CI summary annotation
    def pct(dist, ref):
        return f"{(dist - ref) / ref:+.1%}"
    ci_text = (
        f"<b>Risk-Neutral Confidence Intervals</b><br>"
        f"Median: <b>${forecast.median:,.2f}</b> ({pct(forecast.median, spot)} vs spot)<br>"
        f"Mean:   ${forecast.mean:,.2f} (fwd ${forecast.forward_price:,.2f})<br>"
        f"<br>"
        f"50% CI: ${forecast.ci_50[0]:,.0f} – ${forecast.ci_50[1]:,.0f} "
        f"({pct(forecast.ci_50[0], spot)} / {pct(forecast.ci_50[1], spot)})<br>"
        f"80% CI: ${forecast.ci_80[0]:,.0f} – ${forecast.ci_80[1]:,.0f} "
        f"({pct(forecast.ci_80[0], spot)} / {pct(forecast.ci_80[1], spot)})<br>"
        f"95% CI: ${forecast.ci_95[0]:,.0f} – ${forecast.ci_95[1]:,.0f} "
        f"({pct(forecast.ci_95[0], spot)} / {pct(forecast.ci_95[1], spot)})<br>"
        f"<br>"
        f"<i>Risk-neutral (market-implied). Not real-world.</i>"
    )
    fig.add_annotation(
        text=ci_text,
        align="left", valign="top",
        xref="paper", yref="paper", x=0.98, y=0.98, xanchor="right",
        showarrow=False,
        font=dict(size=11, color="#e2e8f0"),
        bgcolor="rgba(15,23,42,0.85)",
        bordercolor="#334155", borderwidth=1, borderpad=8,
    )

    fig.update_layout(
        title=title,
        xaxis_title="Strike / Close Price",
        yaxis_title="Probability Density",
        height=500,
        template="plotly_dark",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    )
    return fig


def chart_ci_ladder(forecast, symbol: str) -> go.Figure:
    """
    Horizontal-bar ladder showing the 50/80/95% confidence intervals explicitly.
    Each band is drawn at a different y level with its range annotated.
    """
    spot = forecast.spot
    bands = [
        ("50% CI", forecast.ci_50, "34,197,94", 0.55),
        ("80% CI", forecast.ci_80, "245,158,11", 0.50),
        ("95% CI", forecast.ci_95, "239,68,68", 0.45),
    ]
    fig = go.Figure()
    for i, (name, (lo, hi), color, alpha) in enumerate(bands):
        fig.add_trace(go.Bar(
            x=[hi - lo], y=[name], orientation="h", name=name,
            base=[lo], marker_color=f"rgba({color},{alpha})",
            text=[f"${lo:,.0f} – ${hi:,.0f}  ({(hi-lo)/spot:.1%} wide)"],
            textposition="inside", insidetextanchor="middle",
            hovertemplate=f"{name}: $%{{base:,.0f}} – $%{{x:,.0f}}<extra></extra>",
            showlegend=False,
        ))
    # Spot + median + forward markers
    fig.add_vline(x=spot, line_dash="dash", line_color="royalblue", line_width=2,
                  annotation_text=f"Spot ${spot:,.0f}", annotation_position="top left")
    fig.add_vline(x=forecast.median, line_dash="dot", line_color="#a855f7", line_width=2,
                  annotation_text=f"Median ${forecast.median:,.0f}",
                  annotation_position="top right")
    fig.add_vline(x=forecast.forward_price, line_dash="longdash", line_color="#94a3b8",
                  line_width=1.5, annotation_text=f"Forward ${forecast.forward_price:,.0f}")

    fig.update_layout(
        title=f"{symbol} — Risk-Neutral CI Ladder  ({forecast.expiry}, {forecast.dte}d)",
        xaxis_title="Close Price",
        yaxis_title="Confidence Band",
        height=300,
        template="plotly_dark",
        barmode="overlay",
        showlegend=False,
        yaxis=dict(categoryorder="array", categoryarray=["95% CI", "80% CI", "50% CI"]),
    )
    return fig


# ---------------------------------------------------------------------------
# Combined Dashboard
# ---------------------------------------------------------------------------

def generate_dashboard(pred: CompositePrediction, flow: list[dict], output_path: str,
                       forecast=None):
    """Generate a combined HTML dashboard with all charts."""
    # Pick whichever GEX signal is available (chain_gex preferred over flow_gex)
    gex_signal = next(
        (s for s in pred.signals if s.name in ("chain_gex", "flow_gex")), None
    )
    if gex_signal is None:
        # Fallback: synthesize an empty signal so the chart still renders
        gex_signal = Signal(name="gex", direction=0, confidence=0.0, magnitude=0.0,
                            raw={"by_strike": {}, "net_gex": 0.0,
                                 "call_wall": pred.spot, "put_wall": pred.spot,
                                 "total_call_gex": 0.0, "total_put_gex": 0.0},
                            interpretation="No GEX signal available")
    gex_chart = chart_gex_profile(gex_signal, pred.spot, pred.symbol)
    walls_chart = chart_premium_walls(
        next(s for s in pred.signals if s.name == "premium_walls"), pred.spot, pred.symbol
    )
    smile_chart = chart_iv_smile(flow, pred.spot, pred.symbol)
    dashboard = chart_signal_dashboard(pred)

    has_forecast = forecast is not None

    if has_forecast:
        density_chart = chart_expiration_density(forecast, pred.symbol)
        ci_ladder = chart_ci_ladder(forecast, pred.symbol)
        combined = make_subplots(
            rows=5, cols=2,
            subplot_titles=(
                "Flow Gamma Exposure", "Premium Walls",
                "IV Smile (from Flow)", "Signal Dashboard",
                "Expiration Close Distribution (risk-neutral)", None,
                "CI Ladder (50% / 80% / 95%)", None,
                None, None,
            ),
            vertical_spacing=0.08,
            row_heights=[0.18, 0.18, 0.22, 0.18, 0.24],
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "scatter", "colspan": 2}, None],
                [{"type": "bar", "colspan": 2}, None],
                [{"colspan": 2}, None],
            ],
        )
    else:
        combined = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                "Flow Gamma Exposure", "Premium Walls",
                "IV Smile (from Flow)", "Signal Dashboard",
            ),
            vertical_spacing=0.12,
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "bar"}],
                [{"colspan": 2}, None],
            ],
        )

    for trace in gex_chart.data:
        combined.add_trace(trace, row=1, col=1)
    for trace in walls_chart.data:
        combined.add_trace(trace, row=1, col=2)
    for trace in smile_chart.data:
        combined.add_trace(trace, row=2, col=1)
    for trace in dashboard.data:
        combined.add_trace(trace, row=2, col=2)

    if has_forecast:
        for trace in density_chart.data:
            combined.add_trace(trace, row=3, col=1)
        combined.add_vline(x=pred.spot, line_dash="dash", line_color="royalblue", row=3, col=1)
        combined.add_vline(x=forecast.median, line_dash="dot", line_color="#a855f7",
                           line_width=2, row=3, col=1)
        combined.add_vline(x=forecast.forward_price, line_dash="longdash",
                           line_color="#94a3b8", line_width=1.5, row=3, col=1)
        if forecast.premium_magnet:
            combined.add_vline(x=forecast.premium_magnet, line_dash="dashdot",
                               line_color="#f472b6", line_width=1.5, row=3, col=1)
        # CI summary annotation — placed on the density subplot (row 3)
        def _pct(dist, ref):
            return f"{(dist - ref) / ref:+.1%}"
        ci_text = (
            f"<b>Risk-Neutral Confidence Intervals ({forecast.expiry}, {forecast.dte}d)</b><br>"
            f"Median: <b>${forecast.median:,.2f}</b> ({_pct(forecast.median, pred.spot)} vs spot)<br>"
            f"Mean:   ${forecast.mean:,.2f}  (forward ${forecast.forward_price:,.2f})<br>"
            f"Q(close > spot) = {forecast.prob_above_spot:.1%}  |  "
            f"No-arb: {forecast.arb_check.get('status', 'n/a')} "
            f"(μ/F={forecast.arb_check.get('mean_to_forward', 0):.3f})<br>"
            f"50% CI: ${forecast.ci_50[0]:,.0f} – ${forecast.ci_50[1]:,.0f} "
            f"({_pct(forecast.ci_50[0], pred.spot)} / {_pct(forecast.ci_50[1], pred.spot)})<br>"
            f"80% CI: ${forecast.ci_80[0]:,.0f} – ${forecast.ci_80[1]:,.0f} "
            f"({_pct(forecast.ci_80[0], pred.spot)} / {_pct(forecast.ci_80[1], pred.spot)})<br>"
            f"95% CI: ${forecast.ci_95[0]:,.0f} – ${forecast.ci_95[1]:,.0f} "
            f"({_pct(forecast.ci_95[0], pred.spot)} / {_pct(forecast.ci_95[1], pred.spot)})<br>"
            f"<i>Risk-neutral (market-implied). Not real-world.</i>"
        )
        combined.add_annotation(
            text=ci_text, align="left", valign="top",
            xref="x3 domain", yref="y3 domain",
            x=0.98, y=0.97, xanchor="right",
            showarrow=False,
            font=dict(size=10, color="#e2e8f0"),
            bgcolor="rgba(15,23,42,0.85)",
            bordercolor="#334155", borderwidth=1, borderpad=6,
        )
        # CI ladder
        for trace in ci_ladder.data:
            combined.add_trace(trace, row=4, col=1)
        combined.add_vline(x=pred.spot, line_dash="dash", line_color="royalblue", row=4, col=1)
        combined.add_vline(x=forecast.median, line_dash="dot", line_color="#a855f7",
                           line_width=2, row=4, col=1)
        combined.add_vline(x=forecast.forward_price, line_dash="longdash",
                           line_color="#94a3b8", line_width=1.5, row=4, col=1)

    combined.add_vline(x=pred.spot, line_dash="dash", line_color="royalblue", row=1, col=1)
    combined.add_vline(x=pred.spot, line_dash="dash", line_color="royalblue", row=1, col=2)
    combined.add_vline(x=pred.spot, line_dash="dash", line_color="royalblue", row=2, col=1)

    # Signal summary text at bottom
    dirs = {1: "BULLISH", -1: "BEARISH", 0: "NEUTRAL"}
    summary_lines = [
        f"<b>PREDICTION: {dirs[pred.direction]}</b>  |  "
        f"Confidence: {pred.confidence:.0%}  |  "
        f"Disagreement: {pred.disagreement:.3f}  |  "
        f"Spot: ${pred.spot:,.2f}  |  Data: {pred.timestamp}",
        "",
    ]
    for s in pred.signals:
        arrow = "▲" if s.direction > 0 else "▼" if s.direction < 0 else "■"
        color = "#22c55e" if s.direction > 0 else "#ef4444" if s.direction < 0 else "#94a3b8"
        summary_lines.append(
            f"<span style='color:{color}'>{arrow} {s.name.upper()} "
            f"({s.confidence:.0%})</span> — {s.interpretation}"
        )

    combined.add_annotation(
        text="<br>".join(summary_lines),
        align="left", valign="top",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        font=dict(size=11, color="#e2e8f0"),
        bgcolor="rgba(15,23,42,0.85)",
        bordercolor="#334155", borderwidth=1, borderpad=8,
    )

    combined.update_layout(
        title=f"{pred.symbol} — Options Flow Analysis Dashboard",
        height=1900 if has_forecast else 1400,
        template="plotly_dark",
        showlegend=True,
        barmode="relative",
    )
    combined.update_xaxes(title_text="Strike Price", row=1, col=1)
    combined.update_xaxes(title_text="Strike Price", row=1, col=2)
    combined.update_xaxes(title_text="Strike Price", row=2, col=1)
    if has_forecast:
        combined.update_xaxes(title_text="Close Price (Strike Grid)", row=3, col=1)
        combined.update_xaxes(title_text="Close Price", row=4, col=1)
    combined.update_yaxes(title_text="GEX ($M)", row=1, col=1)
    combined.update_yaxes(title_text="Premium ($M)", row=1, col=2)
    combined.update_yaxes(title_text="IV (%)", row=2, col=1)
    combined.update_yaxes(title_text="Score", range=[-1, 1], row=2, col=2)

    pio.write_html(combined, output_path, include_plotlyjs="cdn")
    return output_path
