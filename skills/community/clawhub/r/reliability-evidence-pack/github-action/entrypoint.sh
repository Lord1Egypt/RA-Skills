#!/bin/bash
set -euo pipefail

# Configuration from inputs
REP_PATH="${INPUT_REP_PATH:-.}"
MODE="${INPUT_MODE:-lenient}"
FAIL_ON_WARNINGS="${INPUT_FAIL_ON_WARNINGS:-false}"
REP_VERSION="${INPUT_REP_VERSION:-latest}"

# Output file for JSON results
REPORT_FILE="rep-validation-report.json"

echo "::group::REP Validation"
echo "Validating REP bundle: $REP_PATH"
echo "Mode: $MODE"
echo "Fail on warnings: $FAIL_ON_WARNINGS"
echo "REP version: $REP_VERSION"
echo "::endgroup::"

# Check if rep CLI is available
if ! command -v rep &> /dev/null; then
    echo "::warning:: REP CLI not found in PATH. Installing rep..."

    # Try to install rep using npm or cargo
    if command -v npm &> /dev/null; then
        npm install -g @anthropic/rep-cli || npm install -g rep
    elif command -v cargo &> /dev/null; then
        cargo install rep
    else
        echo "::error:: Cannot install REP CLI: neither npm nor cargo is available"
        echo '{"valid": false, "errors": ["REP CLI not installed"], "warnings": []}' > "$REPORT_FILE"
        echo "result=fail" >> "$GITHUB_OUTPUT"
        echo "errors=1" >> "$GITHUB_OUTPUT"
        echo "warnings=0" >> "$GITHUB_OUTPUT"
        echo "json-output=$(cat "$REPORT_FILE" | jq -Rs .)" >> "$GITHUB_OUTPUT"
        exit 1
    fi
fi

# Build the rep validate command
REVALIDATE_CMD="rep validate"

# Add REP path
REVALIDATE_CMD="$REVALIDATE_CMD \"$REP_PATH\""

# Add mode flag
if [ "$MODE" = "strict" ]; then
    REVALIDATE_CMD="$REVALIDATE_CMD --strict"
elif [ "$MODE" = "lenient" ]; then
    REVALIDATE_CMD="$REVALIDATE_CMD --lenient"
fi

# Add fail-on-warnings flag
if [ "$FAIL_ON_WARNINGS" = "true" ]; then
    REVALIDATE_CMD="$REVALIDATE_CMD --fail-on-warnings"
fi

# Add output format flag for JSON
REVALIDATE_CMD="$REVALIDATE_CMD --output-format json"

# Add REP version if specified
if [ "$REP_VERSION" != "latest" ]; then
    REVALIDATE_CMD="$REVALIDATE_CMD --version $REP_VERSION"
fi

echo "::group::Running validation command"
echo "Command: $REVALIDATE_CMD"
echo "::endgroup::"

# Run validation and capture output
VALIDATION_OUTPUT=$($REVALIDATE_CMD 2>&1) || true
VALIDATION_EXIT_CODE=$?

echo "::group::Validation output"
echo "$VALIDATION_OUTPUT"
echo "::endgroup::"

# Parse the output to extract results
# Try to parse as JSON first, then fall back to text parsing

# Default values
RESULT="pass"
ERRORS=0
WARNINGS=0

# Try to extract JSON from output
JSON_OUTPUT=$(echo "$VALIDATION_OUTPUT" | grep -o '{.*}' | head -1 || echo "")

if [ -n "$JSON_OUTPUT" ]; then
    # Parse JSON output
    VALID=$(echo "$JSON_OUTPUT" | jq -r '.valid // "unknown"' 2>/dev/null || echo "unknown")
    ERRORS=$(echo "$JSON_OUTPUT" | jq -r '.errors | length // 0' 2>/dev/null || echo "0")
    WARNINGS=$(echo "$JSON_OUTPUT" | jq -r '.warnings | length // 0' 2>/dev/null || echo "0")

    if [ "$VALID" = "true" ] || [ "$VALID" = "pass" ]; then
        RESULT="pass"
    else
        RESULT="fail"
    fi

    # Write the JSON output to report file
    echo "$JSON_OUTPUT" > "$REPORT_FILE"
else
    # Fall back to text parsing
    if echo "$VALIDATION_OUTPUT" | grep -qi "error"; then
        RESULT="fail"
    fi

    ERRORS=$(echo "$VALIDATION_OUTPUT" | grep -ci "error" || echo "0")
    WARNINGS=$(echo "$VALIDATION_OUTPUT" | grep -ci "warning" || echo "0")

    # Create JSON output from text
    cat > "$REPORT_FILE" << EOF
{
  "valid": $RESULT == "pass",
  "errors": [],
  "warnings": [],
  "raw_output": $(echo "$VALIDATION_OUTPUT" | jq -Rs .)
}
EOF
fi

# Handle exit codes
if [ "$FAIL_ON_WARNINGS" = "true" ] && [ "$WARNINGS" -gt 0 ]; then
    echo "::error:: Validation failed: fail-on-warnings is enabled and $WARNINGS warning(s) found"
    RESULT="fail"
    exit 1
fi

if [ "$VALIDATION_EXIT_CODE" -ne 0 ] && [ "$RESULT" = "fail" ]; then
    echo "::error:: Validation failed with exit code $VALIDATION_EXIT_CODE"
    exit "$VALIDATION_EXIT_CODE"
fi

# Set GitHub Actions outputs
echo "result=$RESULT" >> "$GITHUB_OUTPUT"
echo "errors=$ERRORS" >> "$GITHUB_OUTPUT"
echo "warnings=$WARNINGS" >> "$GITHUB_OUTPUT"
echo "json-output=$(cat "$REPORT_FILE" | jq -Rs .)" >> "$GITHUB_OUTPUT"

# Print summary
echo "::group::Validation Summary"
echo "Result: $RESULT"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo "Report: $REPORT_FILE"
echo "::endgroup::"

if [ "$RESULT" = "fail" ]; then
    echo "::error:: REP validation failed"
    exit 1
else
    echo "::notice:: REP validation passed"
    exit 0
fi
