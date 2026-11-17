"""
Run options flow analysis on a symbol and generate visualizations.
Usage: python run_analysis.py [SYMBOL]  (default: MU)
"""
import os
import sys

from lse_options import analyze_symbol, format_report, LSEClient, _latest_spot
from expiration_model import forecast_expiration
from visualize import generate_dashboard


def main():
    symbol = sys.argv[1] if len(sys.argv) > 1 else "MU"
    # Output to skill root (parent of scripts/) so the dashboard sits next to README
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    output_html = os.path.join(skill_root, f"{symbol}_dashboard.html")

    print(f"Fetching options flow for {symbol}...")
    try:
        pred = analyze_symbol(symbol, flow_limit=5000)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Print text report
    print(format_report(pred))

    # Compute the BL expiration forecast so the dashboard shows the
    # risk-neutral density + confidence intervals.
    print(f"\nGenerating dashboard -> {output_html}")
    client = LSEClient()
    flow = client.options_flow(symbol, limit=5000)
    spot = _latest_spot(flow)
    forecast = None
    try:
        forecast = forecast_expiration(flow, spot)
        print(f"\n{forecast.summary()}")
    except Exception as e:
        print(f"\n(CI forecast skipped: {e})")

    generate_dashboard(pred, flow, output_html, forecast=forecast)
    print(f"\nDashboard saved. Open with: open {output_html}")

    try:
        usage = client.usage()
        print(f"\nQuota: {usage['calls_per_minute']} calls/min, "
              f"{usage['bytes_used_month']/1e6:.1f}MB/"
              f"{usage['bytes_cap_month']/1e9:.0f}GB used this month")
    except Exception:
        pass

    return pred


if __name__ == "__main__":
    main()
