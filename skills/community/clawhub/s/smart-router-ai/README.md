# Smart Model Router

Never choose an AI model manually again.

## How It Works

1. You type your prompt naturally
2. Router analyzes trigger words and routes to optimal model
3. Response streams back immediately
4. Override with `--intent` flag when needed

## Trigger Detection

| Intent | Trigger Words | Routes To |
|--------|--------------|-----------|
| **fix** | bug, error, crash, broken, exception, fail, debug, issue, problem, stuck | cloud-code (CodeLLaMA) |
| **plan** | design, architect, structure, how should, approach, strategy, pattern | deepseek-r1 (Architect) |
| **flow** | (default) creative, conversational, general | kimi-k2.5:cloud (main) |

## Perfect For

- OpenClaw users with multiple agents
- Teams standardizing model usage
- Anyone tired of manual model switching
- Workflows needing consistent routing

## What's Included

- Intent detection engine (keyword + pattern matching)
- Shell aliases for quick access (fix/plan/flow/ask commands)
- Confidence scoring on detections
- Override flags for manual control
- Router dashboard for monitoring

## Why It Sells

- **Cognitive offload**: Stop choosing, start solving
- **Better results**: Right tool for the right job
- **Time saver**: No more manual model switching
- **Learns your patterns**: Intent detection improves with use
- **Override-friendly**: Force specific model when needed

## Quick Start

```bash
# Setup router
bash scripts/setup.sh

# Add aliases to shell
echo 'source ~/.openclaw/workspace/intent-router-aliases.sh' >> ~/.zshrc
source ~/.zshrc

# Test detection
router-test "my app keeps crashing with null pointer"
# Output: Detected intent: fix (confidence: 94%) → Routing to cloud-code

# Use in practice
fix "TypeError: Cannot read property 'map' of undefined in cart.js"
plan "How should I structure a multi-tenant SaaS database?"
flow "Write a creative product description for our new AI tool"

# Override when needed
ask --intent fix --model deepseek-r1 "Debug this race condition"
```

## Router Dashboard

```bash
# View routing stats
router-dashboard

# See recent detections
router-history --last 20

# Export analytics
router-dashboard --export report.json
```

## Requirements

- Termux (Android) or Linux environment
- OpenClaw agent system
- At least 2 agents configured (main + cloud-code or deepseek-r1)

## Support

Email: support@cod3black.agency
