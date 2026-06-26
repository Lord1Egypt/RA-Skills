import sys
import time
import argparse
from qc_api.client import QCApiClient
from qc_api.config import get_default_project_id

TIMEOUT_SECONDS = 3600  # 1 hour

# Exit codes
EXIT_SUCCESS   = 0   # Backtest completed normally
EXIT_ERROR     = 1   # Runtime error in backtest
EXIT_TIMEOUT   = 2   # Monitoring timed out
EXIT_EARLY_STOP = 3  # Threshold exceeded — deleted and stopped early


def _parse_pct(raw):
    """Parse '59.700%' or '0.597' -> float 0.597. Returns None if unparseable."""
    if raw is None:
        return None
    s = str(raw).strip().rstrip('%')
    try:
        val = float(s)
        # QC returns drawdown as e.g. "59.700" (already a percentage), not 0.597
        return val / 100.0 if val > 1.0 else val
    except ValueError:
        return None


def _parse_equity(raw):
    """Parse '$2,881.20' or '-$7,010.04' -> float. Returns None if unparseable."""
    if raw is None:
        return None
    s = str(raw).strip().replace(',', '').replace('$', '')
    try:
        return float(s)
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Monitor a running backtest with optional early-stop on threshold breach"
    )
    parser.add_argument("backtest_id", help="Backtest ID to monitor")
    parser.add_argument("--project-id", type=int, default=get_default_project_id(),
                        help="QuantConnect Project ID")
    parser.add_argument("--timeout", type=int, default=TIMEOUT_SECONDS,
                        help="Max monitoring time in seconds (default 3600)")
    parser.add_argument("--max-dd", type=float, default=None,
                        help=(
                            "Early-stop threshold: delete backtest if drawdown exceeds this value. "
                            "Accepts fraction (0.40) or percentage (40). "
                            "Example: --max-dd 0.40 or --max-dd 40"
                        ))
    parser.add_argument("--check-after-progress", type=float, default=0.20,
                        help=(
                            "Only start threshold checks after this fraction of progress "
                            "(default 0.20 = 20%%). Avoids false positives from early volatility."
                        ))

    args = parser.parse_args()

    # Normalise max-dd: accept both 0.40 and 40 as "40%"
    max_dd = None
    if args.max_dd is not None:
        max_dd = args.max_dd if args.max_dd <= 1.0 else args.max_dd / 100.0

    client = QCApiClient()
    print(f"Monitoring Backtest {args.backtest_id}...")
    if max_dd is not None:
        print(f"   Early-stop: DD > {max_dd*100:.0f}%  "
              f"(active after {args.check_after_progress*100:.0f}% progress)")

    start_time = time.time()
    had_error = False
    peak_equity = 0.0  # high-water mark for live drawdown calculation

    while True:
        elapsed = time.time() - start_time
        if elapsed > args.timeout:
            print(f"\nTimeout: backtest did not finish within {args.timeout}s.")
            sys.exit(EXIT_TIMEOUT)

        try:
            resp = client.read_backtest(args.project_id, args.backtest_id)
            bt = resp.get('backtest', resp)
            state = bt.get('progress', 0)

            # Progress bar
            bar_length = 30
            filled = int(bar_length * state)
            bar = '=' * filled + '-' * (bar_length - filled)
            sys.stdout.write(f"\rProgress: |{bar}| {state*100:.1f}%")
            sys.stdout.flush()

            # Runtime error check
            error = bt.get('error')
            if error:
                print(f"\nRuntime Error:\n{error}")
                had_error = True
                break

            # Completion check
            if state >= 1.0:
                print("\nBacktest Completed!")
                break

            # -- Live equity tracking for real-time drawdown --
            runtime_stats = bt.get('runtimeStatistics', {})
            current_equity = _parse_equity(runtime_stats.get('Equity'))
            if current_equity is not None and current_equity > peak_equity:
                peak_equity = current_equity

            live_dd = None
            if peak_equity > 0 and current_equity is not None:
                live_dd = (peak_equity - current_equity) / peak_equity

            # -- Early-stop threshold check --
            if max_dd is not None and state >= args.check_after_progress:
                # Prefer live drawdown from equity tracking; fall back to statistics
                dd = live_dd
                if dd is None:
                    stats = bt.get('statistics', {})
                    dd = _parse_pct(stats.get('Drawdown'))

                if dd is not None and dd > max_dd:
                    print(
                        f"\nEarly Stop triggered at {state*100:.1f}% progress: "
                        f"Drawdown {dd*100:.1f}% > threshold {max_dd*100:.0f}%"
                    )
                    print(f"   Deleting backtest {args.backtest_id} via API...")
                    try:
                        client.delete_backtest(args.project_id, args.backtest_id)
                        print("   Backtest deleted.")
                    except Exception as del_err:
                        print(f"   Delete failed (backtest may have already finished): {del_err}")
                    print(f"OUTPUT_EARLY_STOP_DD:{dd*100:.2f}")
                    sys.exit(EXIT_EARLY_STOP)

        except Exception as e:
            print(f"\nMonitoring Error: {e}")
            time.sleep(5)

        time.sleep(2)

    if had_error:
        sys.exit(EXIT_ERROR)


if __name__ == "__main__":
    main()
