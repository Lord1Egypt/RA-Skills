"""
Real-time options flow streaming with live expiration CI.

Connects to LSE WebSocket, aggregates ticks, and recomputes the
directional prediction + expiration confidence intervals as new
flow arrives. Generates dashboard on disconnect.

Usage:
  python run_streaming.py MU                    # 24h replay + live
  python run_streaming.py MU --replay 4         # 4h replay
  python run_streaming.py MU --live             # live only (market hours)
  python run_streaming.py MU --duration 60      # run 60 seconds
"""
import os
import sys
import time
import argparse

from lse_options import (
    LSEClient, analyze_symbol, format_report,
    flow_gex, premium_walls, pcr_signal, iv_skew_signal,
    bayesian_aggregate, CompositePrediction, _latest_spot,
)
from expiration_model import forecast_expiration, ExpirationForecast
from ws_stream import LSEOptionsStream, FlowState, OptionTick
from visualize import generate_dashboard


class StreamingAnalyzer:
    """
    Aggregates WS ticks, periodically recomputes signals + CI,
    and generates a final dashboard.
    """

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.flow_list: list[dict] = []
        self.tick_count = 0
        self.last_report_tick = 0
        self.report_interval = 200
        self.stream: LSEOptionsStream | None = None

    def _on_status(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        print(f"  [{ts}] {msg}")

    def _on_tick(self, tick: OptionTick):
        self.tick_count += 1

    def _on_state_update(self, state: FlowState):
        if state.tick_count - self.last_report_tick >= self.report_interval:
            self.last_report_tick = state.tick_count
            self._compute_and_report(state)

    def _compute_and_report(self, state: FlowState):
        flow = state.to_flow_list()
        if len(flow) < 20:
            return

        try:
            spot = state.latest_spot or _latest_spot(flow)
        except ValueError:
            return

        signals = [
            flow_gex(flow, spot),
            premium_walls(flow, spot),
            pcr_signal(flow),
            iv_skew_signal(flow, spot),
        ]
        direction, confidence, disagreement = bayesian_aggregate(signals)

        pred = CompositePrediction(
            symbol=self.symbol,
            spot=spot,
            direction=direction,
            confidence=confidence,
            disagreement=disagreement,
            signals=signals,
            timestamp=flow[0].get("ts", ""),
        )

        print(f"\n{'='*72}")
        print(f"LIVE UPDATE — {self.symbol} | tick #{state.tick_count} | "
              f"spot ${spot:,.2f}")
        print(f"{'='*72}")
        print(format_report(pred))

        try:
            forecast = forecast_expiration(flow, spot)
            print(f"\n{forecast.summary()}")
            self.last_forecast = forecast
        except Exception as e:
            print(f"\n(CI update skipped: {e})")

        self.last_prediction = pred
        self.flow_list = flow

    def run(self, replay_hours: int | None = 24, duration: float | None = None):
        self.stream = LSEOptionsStream()
        self.stream.on_tick = self._on_tick
        self.stream.on_state_update = self._on_state_update
        self.stream.on_status = self._on_status

        print(f"Starting stream for {self.symbol}")
        print(f"  Replay: {replay_hours}h" if replay_hours else "  Mode: live only")
        if duration:
            print(f"  Duration: {duration}s")
        print()

        self.stream.connect(
            underlying=self.symbol,
            replay_hours=replay_hours,
            duration=duration,
        )

    def generate_final_report(self):
        if not self.flow_list:
            print(f"\nNo WS ticks received (market likely closed). "
                  f"Falling back to REST flow data...")
            try:
                client = LSEClient()
                self.flow_list = client.options_flow(self.symbol, limit=5000)
                print(f"Retrieved {len(self.flow_list)} recent flow prints via REST.")
            except Exception as e:
                print(f"REST fallback failed: {e}")
                return

        print(f"\n{'#'*72}")
        print(f"FINAL REPORT — {self.symbol}")
        print(f"{'#'*72}")

        spot = _latest_spot(self.flow_list)
        signals = [
            flow_gex(self.flow_list, spot),
            premium_walls(self.flow_list, spot),
            pcr_signal(self.flow_list),
            iv_skew_signal(self.flow_list, spot),
        ]
        direction, confidence, disagreement = bayesian_aggregate(signals)

        pred = CompositePrediction(
            symbol=self.symbol,
            spot=spot,
            direction=direction,
            confidence=confidence,
            disagreement=disagreement,
            signals=signals,
            timestamp=self.flow_list[0].get("ts", "") if self.flow_list else "",
        )
        print(format_report(pred))

        forecast = None
        try:
            forecast = forecast_expiration(self.flow_list, spot)
            print(f"\n{forecast.summary()}")
        except Exception as e:
            print(f"CI computation error: {e}")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_root = os.path.dirname(script_dir)
        output = os.path.join(skill_root, f"{self.symbol}_streaming_dashboard.html")
        try:
            generate_dashboard(pred, self.flow_list, output, forecast=forecast)
            print(f"\nDashboard saved: {output}")
            print(f"Open with: open {output}")
        except Exception as e:
            print(f"Dashboard error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Stream LSE options flow for a symbol")
    parser.add_argument("symbol", nargs="?", default="MU", help="Ticker symbol")
    parser.add_argument("--replay", type=int, default=24, metavar="HOURS",
                        help="Replay hours (0 = live only, max 24)")
    parser.add_argument("--duration", type=float, default=None, metavar="SECONDS",
                        help="Auto-disconnect after N seconds")
    args = parser.parse_args()

    analyzer = StreamingAnalyzer(args.symbol.upper())

    replay = args.replay if args.replay > 0 else None
    try:
        analyzer.run(replay_hours=replay, duration=args.duration)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        analyzer.generate_final_report()


if __name__ == "__main__":
    main()
