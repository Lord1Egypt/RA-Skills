#!/usr/bin/env python3
"""
Process Monitor for Skills-Coach
Monitors subprocess CPU usage and kills stuck processes
"""

import os
import sys
import time
import psutil
from pathlib import Path


class ProcessMonitor:
    """Monitor a subprocess and kill it if stuck."""

    def __init__(self, pid: int, timeout_minutes: int = 5, check_interval: int = 60):
        """
        Initialize process monitor.

        Args:
            pid: Process ID to monitor
            timeout_minutes: Minutes of zero CPU before killing (default 5)
            check_interval: Seconds between checks (default 60)
        """
        self.pid = pid
        self.timeout_minutes = timeout_minutes
        self.check_interval = check_interval
        self.zero_cpu_count = 0
        self.required_zero_checks = 5  # Need 5 consecutive zero CPU readings (5 minutes)

    def is_process_alive(self) -> bool:
        """Check if process is still running."""
        try:
            process = psutil.Process(self.pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def get_cpu_percent(self) -> float:
        """Get CPU usage percentage for the process."""
        try:
            process = psutil.Process(self.pid)
            # Get CPU percent over 1 second interval
            return process.cpu_percent(interval=1.0)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return -1.0

    def monitor(self) -> tuple[bool, str]:
        """
        Monitor the process until completion or timeout.

        Returns:
            (success, message) tuple
        """
        print(f"🔍 Monitoring process {self.pid} (timeout: {self.timeout_minutes} min)")

        start_time = time.time()
        last_check_time = start_time

        while True:
            # Check if process is still alive
            if not self.is_process_alive():
                elapsed = (time.time() - start_time) / 60
                return True, f"Process completed after {elapsed:.1f} minutes"

            # Check CPU usage every check_interval seconds
            current_time = time.time()
            if current_time - last_check_time >= self.check_interval:
                cpu_percent = self.get_cpu_percent()

                if cpu_percent < 0:
                    return False, "Process disappeared during monitoring"

                elapsed_min = (current_time - start_time) / 60

                if cpu_percent == 0.0:
                    self.zero_cpu_count += 1
                    print(f"⚠️  [{elapsed_min:.1f}min] CPU: {cpu_percent:.1f}% (zero count: {self.zero_cpu_count}/{self.required_zero_checks})")

                    # Kill if we've seen zero CPU for required number of checks
                    if self.zero_cpu_count >= self.required_zero_checks:
                        try:
                            process = psutil.Process(self.pid)
                            process.terminate()
                            time.sleep(2)
                            if process.is_running():
                                process.kill()
                            return False, f"Process killed after {self.zero_cpu_count} consecutive zero CPU readings ({elapsed_min:.1f} min)"
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            return False, f"Failed to kill stuck process: {e}"
                else:
                    # Reset counter if CPU is active
                    if self.zero_cpu_count > 0:
                        print(f"✓ [{elapsed_min:.1f}min] CPU: {cpu_percent:.1f}% (active, reset counter)")
                    self.zero_cpu_count = 0

                last_check_time = current_time

            time.sleep(1)


def monitor_subprocess(pid: int, timeout_minutes: int = 5) -> bool:
    """
    Monitor a subprocess and return success status.

    Args:
        pid: Process ID to monitor
        timeout_minutes: Minutes of zero CPU before killing

    Returns:
        True if process completed successfully, False if killed
    """
    monitor = ProcessMonitor(pid, timeout_minutes)
    success, message = monitor.monitor()

    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")

    return success


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_monitor.py <pid> [timeout_minutes]")
        sys.exit(1)

    pid = int(sys.argv[1])
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    success = monitor_subprocess(pid, timeout)
    sys.exit(0 if success else 1)
