#!/bin/bash
# extract-prompts.sh - 分析AI Agent源码与架构
# Usage: ./extract-prompts.sh <binary_path> [output_dir]

set -euo pipefail

BINARY="${1:?Usage: $0 <binary_path> [output_dir]}"
OUTPUT_DIR="${2:-/tmp/source-analysis}"

if [ ! -f "$BINARY" ]; then
  echo "Error: Binary not found: $BINARY"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
BASENAME=$(basename "$BINARY")
REPORT="$OUTPUT_DIR/extracted-${BASENAME}.txt"

echo "=== Source Analysis Extract ===" > "$REPORT"
echo "Binary: $BINARY" >> "$REPORT"
echo "Size: $(ls -lh "$BINARY" | awk '{print $5}')" >> "$REPORT"
echo "Date: $(date -Iseconds)" >> "$REPORT"
echo "" >> "$REPORT"

# 1. Identity declarations
echo "[1/8] Extracting identity declarations..."
echo "=== IDENTITY ===" >> "$REPORT"
grep -aoP 'You are [A-Z][^"]{0,500}' "$BINARY" 2>/dev/null | sort -u >> "$REPORT" || true
echo "" >> "$REPORT"

# 2. System prompt sections
echo "[2/8] Extracting system prompt sections..."
echo "=== SECTIONS ===" >> "$REPORT"
grep -aoP '"# [A-Z][^"]{0,200}"' "$BINARY" 2>/dev/null | sort -u >> "$REPORT" || true
echo "" >> "$REPORT"

# 3. Tool names
echo "[3/8] Extracting tool definitions..."
echo "=== TOOL NAMES ===" >> "$REPORT"
grep -aoP '"tool_name":"[^"]*"' "$BINARY" 2>/dev/null | sort -u >> "$REPORT" || true
echo "" >> "$REPORT"

# 4. Behavioral instructions
echo "[4/8] Extracting behavioral instructions..."
echo "=== INSTRUCTIONS ===" >> "$REPORT"
grep -aoP '(Prefer|Avoid|Be concise|Be thorough|Be careful|Do not|Never|Always|When reporting|If the user|Use |Keep |Make sure)[^"]{0,300}' "$BINARY" 2>/dev/null | sort -u >> "$REPORT" || true
echo "" >> "$REPORT"

# 5. CLI flags
echo "[5/8] Extracting CLI flags..."
echo "=== CLI FLAGS ===" >> "$REPORT"
grep -aoP '--[a-z][-a-z]+[^"]{0,100}' "$BINARY" 2>/dev/null | sort -u | head -50 >> "$REPORT" || true
echo "" >> "$REPORT"

# 6. Feature flags
echo "[6/8] Extracting feature flags..."
echo "=== FEATURE FLAGS ===" >> "$REPORT"
grep -aoP 'tengu_[a-z_]+' "$BINARY" 2>/dev/null | sort -u >> "$REPORT" || true
echo "" >> "$REPORT"

# 7. Environment variables
echo "[7/8] Extracting environment variables..."
echo "=== ENV VARS ===" >> "$REPORT"
grep -aoP 'CLAUDE_CODE_[A-Z_]+' "$BINARY" 2>/dev/null | sort -u >> "$REPORT" || true
grep -aoP 'ANTHROPIC_[A-Z_]+' "$BINARY" 2>/dev/null | sort -u >> "$REPORT" || true
echo "" >> "$REPORT"

# 8. Version info
echo "[8/8] Extracting version info..."
echo "=== VERSION ===" >> "$REPORT"
grep -aoP '[0-9]+\.[0-9]+\.[0-9]+' "$BINARY" 2>/dev/null | sort -u | head -10 >> "$REPORT" || true
echo "" >> "$REPORT"

echo "=== DONE ===" >> "$REPORT"
echo ""
echo "Report saved to: $REPORT"
echo "Lines: $(wc -l < "$REPORT")"
