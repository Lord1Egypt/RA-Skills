#!/bin/bash
# Self-Improving Science Error Detector Hook
# Triggers on PostToolUse for Bash to detect ML/data pipeline failures
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "data leakage"
    "overfitting"
    "underfitting"
    "NaN loss"
    "nan loss"
    "NaN"
    "convergence"
    "not converge"
    "diverge"
    "p-value"
    "p_value"
    "not reproducible"
    "irreproducible"
    "CUDA error"
    "CUDA out of memory"
    "out of memory"
    "OOM"
    "shape mismatch"
    "RuntimeError"
    "ValueError"
    "dimension mismatch"
    "Traceback"
    "ModuleNotFoundError"
    "ImportError"
    "FileNotFoundError"
    "KeyError"
    "IndexError"
    "TypeError"
    "ZeroDivisionError"
    "MemoryError"
    "gradient explosion"
    "vanishing gradient"
    "loss is nan"
    "loss: nan"
    "accuracy: 0.0"
    "f1: 0.0"
    "inf loss"
    "class imbalance"
    "data drift"
    "distribution shift"
    "feature mismatch"
    "column not found"
    "missing values"
    "null values"
    "SettingWithCopyWarning"
    "FutureWarning"
    "DeprecationWarning"
    "failed"
    "FAILED"
    "Error:"
    "error:"
    "ERROR:"
    "fatal:"
    "Permission denied"
    "No such file"
    "command not found"
    "exit code"
    "non-zero"
)

contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

if [ "$contains_error" = true ]; then
    cat << 'EOF'
<science-error-detected>
A data science / ML error was detected. Consider logging to .learnings/ if:
- Data leakage, distribution shift, or quality issue found
- Model training failed (NaN loss, OOM, convergence)
- Statistical assumption violated or test misapplied
- Results not reproducible across runs
- Shape mismatch, missing data, or pipeline failure

Log experiment issues to EXPERIMENT_ISSUES.md: [EXP-YYYYMMDD-XXX]
Log methodology learnings to LEARNINGS.md: [LRN-YYYYMMDD-XXX]
Include: metrics, seeds, library versions, dataset name.
</science-error-detected>
EOF
fi
