#!/bin/bash
#===========================================================
# AI Repair Assistant - Ask Ollama for help
#===========================================================
# Usage: bash ai-repair.sh "describe your issue"

OLLAMA_MODEL="llama3.2:1b"

ISSUE="${1:-Sol won't start}"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install | sh
fi

# Pull model if needed
if ! ollama list 2>/dev/null | grep -q "$OLLAMA_MODEL"; then
    echo "Pulling repair model..."
    ollama pull "$OLLAMA_MODEL"
fi

# Get system info for context
SYSTEM_INFO=$(openclaw gateway status 2>/dev/null | head -20 || echo "Gateway not responding")

# Ask AI
PROMPT="You are an OpenClaw AI expert. 

System status:
$SYSTEM_INFO

User issue: $ISSUE

Give specific terminal commands to fix this. Be brief and practical."

echo "🤖 Asking AI for help..."
echo ""
echo "$PROMPT" | ollama run "$OLLAMA_MODEL" --quiet