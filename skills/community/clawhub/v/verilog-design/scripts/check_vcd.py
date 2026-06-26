#!/usr/bin/env python3
"""
VCD Waveform Analysis Script
Check if signal matches expected values at specific times.

Usage:
    python3 check_vcd.py <vcd_file> <signal_path> <time_value_pairs...>
    
Example:
    python3 check_vcd.py counter.vcd "counter_tb.dut.count" 0:0 10:1 20:2 100:10
"""

import sys
from vcdvcd import VCDVCD

def check_vcd(vcd_file, signal_path, expected_values):
    """
    Check if signal matches expected values at specific times.
    expected_values: list of (time, value) tuples
    """
    vcd = VCDVCD(vcd_file)
    signal = vcd[signal_path]
    
    for time, expected in expected_values:
        actual = signal[time]
        if actual != expected:
            print(f"FAIL at t={time}: expected {expected}, got {actual}")
            return False
    
    print("PASS: All signal checks passed")
    return True

def get_transitions(vcd_file, signal_path):
    """Get all transitions for a signal."""
    vcd = VCDVCD(vcd_file)
    signal = vcd[signal_path]
    return signal.tv  # List of (time, value) tuples

def verify_counter(vcd_file):
    """Verify counter increments correctly."""
    vcd = VCDVCD(vcd_file)
    
    # Find the counter signal
    count_signal = None
    for path in vcd.signals:
        if "count" in path.lower():
            count_signal = vcd[path]
            break
    
    if not count_signal:
        print("ERROR: Counter signal not found")
        return False
    
    # Check monotonic increment
    prev_val = -1
    for time, val in count_signal.tv:
        val_int = int(val, 2) if val.startswith('b') else int(val)
        if val_int != (prev_val + 1) % 16:  # Assuming 4-bit counter
            print(f"ERROR at t={time}: count jumped from {prev_val} to {val_int}")
            return False
        prev_val = val_int
    
    print("PASS: Counter verified")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <vcd_file> [signal_path] [time:value pairs...]")
        print(f"       {sys.argv[0]} counter.vcd  # Run counter verification")
        sys.exit(1)
    
    vcd_file = sys.argv[1]
    
    # If only vcd file provided, run counter verification
    if len(sys.argv) == 2:
        success = verify_counter(vcd_file)
        sys.exit(0 if success else 1)
    
    # Otherwise check specific signal with expected values
    signal_path = sys.argv[2]
    expected_values = []
    for pair in sys.argv[3:]:
        time, value = pair.split(':')
        expected_values.append((int(time), value))
    
    success = check_vcd(vcd_file, signal_path, expected_values)
    sys.exit(0 if success else 1)
