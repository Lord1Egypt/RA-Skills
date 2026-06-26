# VCD Waveform Analysis with Python

Use Python `vcdvcd` library or custom parser to analyze simulation waveforms programmatically.

## Installation

```bash
pip install vcdvcd
```

## Quick Start

Use the provided script: `<skill_dir>/scripts/check_vcd.py`

### Check Counter Verification

```bash
python3 <skill_dir>/scripts/check_vcd.py counter.vcd
```

### Check Specific Signal Values

```bash
python3 <skill_dir>/scripts/check_vcd.py counter.vcd "counter_tb.dut.count" 0:0 10:1 20:2 100:10
```

## Python API Examples

### Parse VCD and Check Signals

```python
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

# Usage example
check_vcd(
    "counter.vcd",
    "counter_tb.dut.count",
    [(0, "0"), (10, "1"), (20, "2"), (100, "10")]
)
```

### Extract Signal Transitions

```python
from vcdvcd import VCDVCD

def get_transitions(vcd_file, signal_path):
    """Get all transitions for a signal."""
    vcd = VCDVCD(vcd_file)
    signal = vcd[signal_path]
    return signal.tv  # List of (time, value) tuples

# Usage
transitions = get_transitions("counter.vcd", "counter_tb.dut.count")
for time, value in transitions:
    print(f"t={time}: count={value}")
```

## Integration with Testbench

Call Python VCD checker from testbench:

```verilog
initial begin
    // ... simulation ...
    $finish();
end

// Post-simulation check
final begin
    $display("Running VCD verification...");
    $system("python3 check_vcd.py counter.vcd");
end
```

Or run separately after simulation completes.
