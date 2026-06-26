#!/bin/bash
# Auto-detect and run Verilog/SystemVerilog simulation
# Priority: VCS -> Xrun -> Icarus Verilog
# Usage: simulate.sh <module_name> [sv]

MODULE=$1
TYPE=${2:-v}  # 'v' for Verilog, 'sv' for SystemVerilog

if [ -z "$MODULE" ]; then
    echo "Usage: $0 <module_name> [sv]"
    echo "  module_name: Name of the Verilog module (without extension)"
    echo "  sv: Optional, specify 'sv' for SystemVerilog files (.sv)"
    exit 1
fi

# Determine file extensions
if [ "$TYPE" == "sv" ]; then
    SRC_EXT="sv"
    TB_EXT="_tb.sv"
else
    SRC_EXT="v"
    TB_EXT="_tb.v"
fi

SRC_FILE="${MODULE}.${SRC_EXT}"
TB_FILE="${MODULE}${TB_EXT}"

# Check if source files exist
if [ ! -f "$SRC_FILE" ]; then
    echo "Error: Source file $SRC_FILE not found"
    exit 1
fi

if [ ! -f "$TB_FILE" ]; then
    echo "Error: Testbench file $TB_FILE not found"
    exit 1
fi

echo "========================================"
echo "Verilog Simulation Auto-Detection"
echo "Module: $MODULE"
echo "Source: $SRC_FILE"
echo "Testbench: $TB_FILE"
echo "========================================"

# Priority 1: Synopsys VCS
if command -v vcs &> /dev/null; then
    echo "[INFO] Synopsys VCS detected, using VCS for simulation"
    
    if [ "$TYPE" == "sv" ]; then
        echo "[CMD] vcs -full64 -debug_acc+all -sverilog -l sim.log -R $SRC_FILE $TB_FILE"
        vcs -full64 -debug_acc+all -sverilog -l sim.log -R "$SRC_FILE" "$TB_FILE"
    else
        echo "[CMD] vcs -full64 -debug_acc+all -l sim.log -R $SRC_FILE $TB_FILE"
        vcs -full64 -debug_acc+all -l sim.log -R "$SRC_FILE" "$TB_FILE"
    fi
    
    if [ $? -eq 0 ]; then
        echo "[SUCCESS] VCS simulation completed"
    else
        echo "[ERROR] VCS simulation failed, check sim.log"
        exit 1
    fi

# Priority 2: Cadence Xrun
elif command -v xrun &> /dev/null; then
    echo "[INFO] Cadence Xrun detected, using Xrun for simulation"
    
    if [ "$TYPE" == "sv" ]; then
        echo "[CMD] xrun -64bit -access rwc -sv -l sim.log -R $SRC_FILE $TB_FILE"
        xrun -64bit -access rwc -sv -l sim.log -R "$SRC_FILE" "$TB_FILE"
    else
        echo "[CMD] xrun -64bit -access rwc -l sim.log $SRC_FILE $TB_FILE"
        xrun -64bit -access rwc -l sim.log "$SRC_FILE" "$TB_FILE"
    fi
    
    if [ $? -eq 0 ]; then
        echo "[SUCCESS] Xrun simulation completed"
    else
        echo "[ERROR] Xrun simulation failed, check sim.log"
        exit 1
    fi

# Priority 3: Icarus Verilog (fallback)
elif command -v iverilog &> /dev/null; then
    echo "[INFO] Icarus Verilog detected, using iverilog for simulation"
    
    echo "[CMD] iverilog -o ${MODULE}.vvp $SRC_FILE $TB_FILE"
    iverilog -o "${MODULE}.vvp" "$SRC_FILE" "$TB_FILE"
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] Icarus compilation failed"
        exit 1
    fi
    
    echo "[CMD] vvp ${MODULE}.vvp"
    vvp "${MODULE}.vvp" | tee sim.log
    
    if [ $? -eq 0 ]; then
        echo "[SUCCESS] Icarus simulation completed"
    else
        echo "[ERROR] Icarus simulation failed"
        exit 1
    fi

else
    echo "[ERROR] No supported simulator found!"
    echo "Please install one of:"
    echo "  - Synopsys VCS (commercial)"
    echo "  - Cadence Xrun (commercial)"
    echo "  - Icarus Verilog (open source: apt install iverilog)"
    exit 1
fi

echo "========================================"
echo "Simulation outputs:"
echo "  - Log: sim.log"
if command -v vcs &> /dev/null || command -v xrun &> /dev/null; then
    echo "  - VCD: ${MODULE}.vcd (if \$dumpfile used in testbench)"
else
    echo "  - VVP: ${MODULE}.vvp"
    echo "  - VCD: ${MODULE}.vcd (if \$dumpfile used in testbench)"
fi
echo "========================================"
