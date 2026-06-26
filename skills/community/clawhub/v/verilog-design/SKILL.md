---
name: Verilog Design Flow
description: Design, implement, and verify Verilog/SystemVerilog modules with spec-driven development, self-checking testbenches, and automated simulation workflows. Supports Synopsys VCS, Cadence Xrun, Icarus Verilog simulators, and slang static syntax checker. Use when the user needs to write Verilog modules, design digital circuits, create counters/FSMs/interfaces, simulate and verify designs, or analyze VCD waveforms.
---

## Core Rules

### Phase 1: Understand Requirements
1. Ask clarifying questions if the design spec is incomplete
2. Identify: clock/reset strategy, interface signals, functionality, timing constraints
3. Confirm the target: synthesis (FPGA/ASIC) or simulation only

### Phase 2: Write Design Spec
1. Create a markdown spec document with:
   - Module name and purpose
   - Port list (direction, width, description)
   - Functional description
   - Timing diagram (if applicable)
   - Test scenarios checklist
2. Store spec in memory or as a file for reference

### Phase 3: Implement Verilog
1. **One-always-one-signal coding style**: Each signal should be assigned in exactly one always block
   - Separate sequential (posedge clk) and combinational (@*) logic
   - Declare intermediate signals for complex logic
   - Avoid mixing blocking (=) and non-blocking (<=) assignments in the same always block
2. Follow synthesizable coding guidelines:
   - Use `always @(posedge clk)` for sequential logic
   - Use `assign` or `always @(*)` for combinational logic
   - Avoid latches (ensure all branches assign in combinational blocks)
   - Explicit reset strategy (sync/async)
3. Include header comments with author, date, and revision (see Version Tracking below)
4. Use descriptive signal names, avoid single-letter variables

### Phase 3b: Static Syntax Check with Slang
Before simulation, run static syntax checking using slang:

```bash
# Check Verilog/SystemVerilog syntax
slang <module_name>.v

# Or for SystemVerilog files
slang <module_name>.sv
```

**What slang checks:**
- Syntax errors and parsing issues
- Type mismatches
- Undefined references
- Port connection errors
- SystemVerilog compliance

**If slang reports errors:**
1. Fix all syntax errors before proceeding to simulation
2. Pay attention to warnings about potential issues
3. Re-run slang until "Build succeeded: 0 errors"

### Phase 3c: Design Review Checklist
Before simulation, verify:
- [ ] Slang syntax check passes (0 errors)
- [ ] All sequential signals have explicit reset values
- [ ] No combinational logic loops (synthesis will error)
- [ ] No unintentional latches (all `if`/`case` branches assign in combinational blocks)
- [ ] State machines have `default` case branch
- [ ] Clock domain crossing signals are properly synchronized
- [ ] Vector widths match between assignment source and destination
- [ ] Array indices are within declared bounds
- [ ] No blocking assignments (`=`) in sequential always blocks
- [ ] No non-blocking assignments (`<=`) in combinational always blocks
- [ ] `timescale` directive present in all source files

### Phase 4: Write Testbench
1. Create self-checking testbench using:
   - Clock generator (typical: `always #5 clk = ~clk;` for 10ns period)
   - Reset stimulus
   - Input stimulus generation
   - Expected output generation/comparison
   - `$display()` or `$monitor()` for pass/fail reporting
   - `$finish()` after all tests complete
2. Save as `<module_name>_tb.v`

### Phase 5: Simulate with EDA Tools

The skill automatically detects and uses available simulators in priority order:
1. **Synopsys VCS** (if `vcs` command available)
2. **Cadence Xrun** (if `xrun` command available)
3. **Icarus Verilog** (fallback)

#### Simulator Detection Logic
```bash
# Priority order: VCS → Xrun → Icarus
which vcs && use_vcs
which xrun && use_xrun
fallback to iverilog
```

#### Synopsys VCS (Verilog)
```bash
vcs -full64 -debug_acc+all -l sim.log -R <module_name>.v <module_name>_tb.v
```

#### Synopsys VCS (SystemVerilog)
```bash
vcs -full64 -debug_acc+all -sverilog -l sim.log -R <module_name>.sv <module_name>_tb.sv
```

#### Cadence Xrun (Verilog)
```bash
xrun -64bit -access rwc -l sim.log <module_name>.v <module_name>_tb.v
```

#### Cadence Xrun (SystemVerilog)
```bash
xrun -64bit -access rwc -sv -l sim.log -R <module_name>.sv <module_name>_tb.sv
```

#### Icarus Verilog (Fallback)
```bash
iverilog -o <module_name>.vvp <module_name>.v <module_name>_tb.v
vvp <module_name>.vvp
```

#### VCD Waveform Output
⚠️ **Important**: Always use VCD format for waveform dumping to ensure compatibility:
```verilog
initial begin
    $dumpfile("<module_name>.vcd");
    $dumpvars(0, <module_name>_tb);
end
```
- VCS and Xrun support VCD via `$dumpfile()`/`$dumpvars()`
- FSDB format (for Verdi) is NOT supported by the VCD analysis scripts
- Keep testbench VCD-compatible for cross-simulator portability

### Phase 6: Debug & Iterate
1. If assertions fail or outputs incorrect:
   - Review waveforms with `gtkwave` OR
   - Use Python VCD analysis script: `python3 <skill_dir>/scripts/check_vcd.py <module>.vcd`
   - See [references/vcd-analysis.md](references/vcd-analysis.md) for detailed API
2. Fix RTL bugs, update testbench if needed
3. Re-simulate until all tests pass
4. Update spec with any design changes

## Testbench Template

```verilog
`timescale 1ns/1ps

module <module>_tb;
    // Parameters
    parameter CLK_PERIOD = 10;
    
    // Signals
    reg clk;
    reg rst_n;
    // ... add inputs/outputs
    
    // Instantiate DUT
    <module> dut (
        .clk(clk),
        .rst_n(rst_n),
        // ... ports
    );
    
    // Clock generation
    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end
    
    // VCD dump
    initial begin
        $dumpfile("<module>.vcd");
        $dumpvars(0, <module>_tb);
    end
    
    // Test stimulus
    initial begin
        // Initialize
        rst_n = 0;
        // ... init inputs
        
        // Release reset
        #(CLK_PERIOD * 2);
        rst_n = 1;
        
        // Apply test vectors
        // ... stimulus code
        
        // Check results
        // ... self-checking assertions
        
        #(CLK_PERIOD * 10);
        $finish();
    end
    
    // Monitor
    initial begin
        $monitor("Time=%0t: signals=...", $time);
    end
endmodule
```

## VCD Analysis

For automated waveform checking, use Python VCD parsing.
Reference: [references/vcd-analysis.md](references/vcd-analysis.md)

## Data Storage

- Design specs: Store in `memory/verilog_specs/<module_name>_spec.md`
- Verilog files: Create in workspace as `<module_name>.v`
- Testbenches: Create as `<module_name>_tb.v`
- Simulation outputs: Generate `.vvp` (Icarus), `sim.log`, and `.vcd` files

## Simulator Auto-Detection Script

Use the provided helper script to automatically select and run the best available simulator:

```bash
# The script checks for VCS → Xrun → Icarus in order
bash <skill_dir>/scripts/simulate.sh <module_name>
```

Example workflow:
```bash
# 1. Detect simulator and run
bash scripts/simulate.sh counter

# 2. Check simulation log
cat sim.log

# 3. Analyze VCD waveforms
python3 scripts/check_vcd.py counter.vcd
```

## External Tools

| Tool | Command | Purpose |
|------|---------|---------|
| Synopsys VCS | `vcs -full64 -debug_acc+all -l sim.log -R file.v` | Compile & Simulate Verilog |
| Synopsys VCS (SV) | `vcs -full64 -debug_acc+all -sverilog -l sim.log -R file.sv` | Compile & Simulate SystemVerilog |
| Cadence Xrun | `xrun -64bit -access rwc -l sim.log file.v` | Compile & Simulate Verilog |
| Cadence Xrun (SV) | `xrun -64bit -access rwc -sv -l sim.log -R file.sv` | Compile & Simulate SystemVerilog |
| Icarus Verilog | `iverilog -o out.vvp file.v` | Compile Verilog (fallback) |
| VVP | `vvp out.vvp` | Run simulation |
| GTKWave | `gtkwave dump.vcd` | View waveforms (optional) |

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Multiple drivers | Ensure one-always-one-signal: each signal assigned in exactly one always block |
| Latch inference | Ensure all `if`/`case` branches assign in combinational always |
| Missing reset | Include explicit reset in sequential always blocks |
| Race conditions | Use non-blocking `<=` in sequential logic only |
| Simulation mismatch | Check `timescale` and delays |
| VCD not generated | Ensure `$dumpfile()` called before `$dumpvars()` |

## Debugging Guide

### Simulation Hangs / Freezes
| Symptom | Cause | Solution |
|---------|-------|----------|
| No output, simulation stuck | Combinational loop | Check for circular logic in combinational always blocks |
| Infinite loop warning | Zero-delay feedback | Add delay elements or check async feedback paths |
| Division by zero | Runtime calculation error | Check divisor is never zero |
| Array out of bounds | Invalid index | Verify index range before array access |

### Output Shows 'X' (Unknown)
| Symptom | Cause | Solution |
|---------|-------|----------|
| Specific signal is X | Uninitialized register | Add explicit reset value |
| Wide bus partially X | Mixed width assignment | Check vector width consistency |
| After reset release | Reset deassertion timing | Ensure reset held long enough |
| Random X propagation | X propagation from input | Trace back to source of X |

### Timing Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| Output one cycle late | Blocking vs non-blocking | Use `<=` in sequential always blocks |
| Glitches on output | Combinational logic hazard | Add register stage or use synchronous output |
| Setup/hold violations (ASIC) | Clock/data skew | Check synthesis timing reports |

### Synthesis Errors
| Error | Cause | Solution |
|-------|-------|----------|
| "Not synthesizable" | Unsupported Verilog construct | Replace with synthesizable equivalent |
| "Multiple drivers" | Signal assigned in multiple always | Merge logic or use intermediate signals |
| "Latch inferred" | Incomplete if/case in combinational | Add default assignment or use `else` |
| "Undriven signal" | Output declared but not assigned | Connect to logic or tie to constant |

## Version Tracking

### File Header Template
Every Verilog file should include:

```verilog
/**
 * Module: <module_name>
 * Description: <brief description>
 * Author: <name>
 * Date: <YYYY-MM-DD>
 * Version: <major>.<minor>.<patch>
 * 
 * Changelog:
 *   v1.0.0 - <date> - Initial release
 *   v1.1.0 - <date> - <description of changes>
 *   v2.0.0 - <date> - <breaking changes>
 * 
 * Parameters:
 *   - PARAM1: <description> (default: <value>)
 *   - PARAM2: <description> (default: <value>)
 * 
 * Ports:
 *   - clk: <description>
 *   - rst_n: <description>
 *   ...
 */
```

### Version Numbering
- **Major**: Breaking changes (interface change, removed features)
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, no functional change

### Git Workflow (Recommended)
```bash
# Before starting new feature
git checkout -b feature/new-functionality

# After completing and testing
git add <files>
git commit -m "feat: add <feature> to <module>"
git checkout main
git merge feature/new-functionality
```
