#!/bin/bash
# Technical Eval - Tavily API Configuration
# Unified configuration using ~/.openclaw/.env

# Load Tavily API Key from unified config
if [ -f "$HOME/.openclaw/.env" ]; then
    export $(grep -v '^#' $HOME/.openclaw/.env | xargs)
    if [ -z "$TAVILY_API_KEY" ]; then
        echo "Error: TAVILY_API_KEY not found in ~/.openclaw/.env"
        exit 1
    fi
else
    echo "Error: ~/.openclaw/.env file not found"
    echo "Please create it with: echo 'TAVILY_API_KEY=your_key' > ~/.openclaw/.env"
    exit 1
fi

# Domain whitelist for technical evaluation
TECHNICAL_DOMAINS=(
    "mlperf.org"
    "benchmarkai.com" 
    "paperswithcode.com"
    "github.com"
    "stackoverflow.com"
    "gitlab.com"
    "bitbucket.org"
    "linkedin.com"
    "indeed.com"
    "glassdoor.com"
    "levels.fyi"
    "techcrunch.com"
    "wired.com"
    "gartner.com"
    "forrester.com"
    "idc.com"
    "medium.com"
    "dev.to"
    "hackernoon.com"
)

echo "✅ Technical Eval Tavily configuration loaded successfully"
echo "🔑 Using TAVILY_API_KEY from ~/.openclaw/.env"
echo "🌐 Configured $((${#TECHNICAL_DOMAINS[@]})) technical domains for search"