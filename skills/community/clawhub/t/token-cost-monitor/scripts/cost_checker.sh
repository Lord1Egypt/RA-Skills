#!/bin/bash
# Token Cost Checker
# Quick reference for OpenClaw API costs

set -euo pipefail

# SECURITY MANIFEST:
#   Environment variables accessed: none
#   External endpoints called: none
#   Local files read: none
#   Local files written: none

echo "================================"
echo "OpenClaw API Cost Reference (2026)"
echo "================================"
echo ""
echo "Claude Models:"
echo "  Haiku:  \$0.25/1M input, \$1.25/1M output"
echo "  Sonnet: \$3/1M input, \$15/1M output"
echo "  Opus:   \$15/1M input, \$75/1M output"
echo ""
echo "OpenAI Models:"
echo "  GPT-4o Mini: \$0.15/1M input, \$0.60/1M output"
echo "  GPT-4o:      \$2.5/1M input, \$10/1M output"
echo "  o1:          \$15/1M input, \$60/1M output"
echo ""
echo "Google Gemini:"
echo "  Flash: \$0.075/1M input, \$0.30/1M output"
echo "  Pro:   \$1.25/1M input, \$5/1M output"
echo "  Ultra: \$7.5/1M input, \$30/1M output"
echo ""
echo "================================"
echo "Cost Optimization Tips:"
echo "  1. Use Haiku for simple queries (saves 90%)"
echo "  2. Reduce heartbeat frequency to 4-6 hours"
echo "  3. Clear context after completed tasks"
echo "  4. Batch similar tasks together"
echo "================================"
