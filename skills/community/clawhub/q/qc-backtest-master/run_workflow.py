import sys
import subprocess
import os
import argparse
import time
from qc_api.config import get_default_project_id

# Monitor exit codes (mirrors monitor_backtest.py)
EXIT_MONITOR_SUCCESS    = 0
EXIT_MONITOR_ERROR      = 1
EXIT_MONITOR_TIMEOUT    = 2
EXIT_MONITOR_EARLY_STOP = 3


def run_script(script_path, args):
    """
    Runs a python script and streams output line-by-line.
    Returns: (returncode, full_output_lines, captured_id, captured_early_stop_dd)
    """
    python_cmd = sys.executable
    cmd = [python_cmd, script_path] + args

    print(f"\nRunning: {os.path.basename(script_path)} {' '.join(args)}")

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        captured_id = None
        captured_early_stop_dd = None
        full_output = []

        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                stripped = line.strip()
                print(stripped)
                full_output.append(stripped)

                if "OUTPUT_BACKTEST_ID:" in stripped:
                    captured_id = stripped.split("OUTPUT_BACKTEST_ID:")[1].strip()
                if "OUTPUT_EARLY_STOP_DD:" in stripped:
                    captured_early_stop_dd = stripped.split("OUTPUT_EARLY_STOP_DD:")[1].strip()

        returncode = process.poll()
        return returncode, full_output, captured_id, captured_early_stop_dd

    except Exception as e:
        print(f"Failed to run script: {e}")
        return -1, [], None, None


def main():
    default_project_id = str(get_default_project_id())

    parser = argparse.ArgumentParser(description="Full Workflow: Submit -> Monitor -> Get Results")
    parser.add_argument("--main-file", required=True, help="Path to the main strategy .py file")
    parser.add_argument("--project-id", type=str, default=default_project_id, help="QuantConnect Project ID")
    parser.add_argument("--name", help="Backtest Name")
    parser.add_argument("--max-dd", type=float, default=None,
                        help=(
                            "Early-stop threshold: delete backtest if drawdown exceeds this value "
                            "mid-run. Accepts fraction (0.40) or percentage (40). "
                            "Example: --max-dd 40"
                        ))
    parser.add_argument("--check-after-progress", type=float, default=0.20,
                        help=(
                            "Start early-stop checks only after this fraction of progress "
                            "(default 0.20 = 20%%). Avoids false positives from early volatility."
                        ))

    args = parser.parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # -- 1. Submit --
    submit_script = os.path.join(base_dir, "submit_backtest.py")
    submit_args = ["--main-file", args.main_file, "--project-id", args.project_id]
    if args.name:
        submit_args.extend(["--name", args.name])

    rc, _, backtest_id, _ = run_script(submit_script, submit_args)
    if rc != 0 or not backtest_id:
        print("Submission failed or Backtest ID not found.")
        sys.exit(1)

    print(f"\nBacktest ID Captured: {backtest_id}")
    time.sleep(2)

    # -- 2. Monitor --
    monitor_script = os.path.join(base_dir, "monitor_backtest.py")
    monitor_args = [backtest_id, "--project-id", args.project_id]
    if args.max_dd is not None:
        monitor_args.extend(["--max-dd", str(args.max_dd)])
        monitor_args.extend(["--check-after-progress", str(args.check_after_progress)])

    rc, _, _, early_stop_dd = run_script(monitor_script, monitor_args)

    if rc == EXIT_MONITOR_ERROR:
        print("Backtest ended with a runtime error. Skipping result download.")
        sys.exit(1)

    if rc == EXIT_MONITOR_TIMEOUT:
        print("Monitoring timed out. Skipping result download.")
        sys.exit(2)

    if rc == EXIT_MONITOR_EARLY_STOP:
        dd_str = f"{early_stop_dd}%" if early_stop_dd else "unknown"
        print(f"\nWorkflow stopped early: drawdown ({dd_str}) exceeded threshold.")
        print("   Backtest has been deleted from QC. No results to download.")
        print("   -> Adjust strategy and resubmit.")
        sys.exit(3)

    # -- 3. Get Results --
    get_results_script = os.path.join(base_dir, "get_results.py")
    get_results_args = [backtest_id, "--project-id", args.project_id, "--output-dir", os.getcwd()]

    rc, _, _, _ = run_script(get_results_script, get_results_args)
    if rc == 0:
        print("\nWorkflow Completed Successfully!")
    else:
        print("\nFailed to retrieve results.")


if __name__ == "__main__":
    main()
