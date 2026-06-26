# TokenLens Token Value Optimization Engine

**Free skill for OpenClaw — Maximize value per token**

## Quick Start

```bash
# Once published to ClawHub:
clawhub install tokenlens-token-value-optimizer

# Navigate to skill directory
cd ~/.openclaw/workspace/skills/tokenlens-token-value-optimizer

# Check current token usage
python3 scripts/token_value_tracker.py check

# Get optimization recommendations
python3 scripts/token_value_tracker.py recommend

# Apply optimizations
python3 scripts/token_value_tracker.py optimize --apply
```

## What It Does

### 1. **Tracks Token Usage**
- Daily and weekly token consumption
- Cost projections (if API costs configured)
- Efficiency trends

### 2. **Provides Smart Recommendations**
- Context loading optimization (biggest savings)
- Model selection suggestions
- Heartbeat interval tuning
- Session pruning reminders

### 3. **Calculates Value Scores**
- Efficiency scoring (1-10)
- Improvement opportunities
- Weekly optimization reports

### 4. **Simple Automation**
- One-command optimization scans
- Weekly report generation
- Alert for inefficient patterns

## Philosophy

**We don't just save tokens — we maximize value.**

Traditional optimization focuses on cost reduction. TokenLens focuses on **value creation**:
- **Value Score** = Business outcome / tokens used
- **Efficiency Ratio** = Tasks completed per 1k tokens
- **Optimization Index** = Potential improvement percentage

## Features

### Free Version
- Basic token tracking
- Smart recommendations
- Efficiency scoring
- Weekly reports
- Simple automation

### Premium Version (Coming Soon)
- Advanced value mapping
- Multi-agent optimization
- Predictive optimization
- Custom integration APIs
- Team collaboration

## Architecture

**Local-only, privacy-first:**
- No network calls
- No external dependencies
- Data stays on your machine
- OpenClaw-native integration

**Three simple scripts:**
1. `token_value_tracker.py` — Core tracking & recommendations
2. `context_optimizer.py` — Context loading optimization
3. `model_router.py` — Model recommendation
4. `optimize.sh` — Unified CLI

## Data & Privacy

- All data stored locally in `~/.openclaw/workspace/memory/tokenlens/`
- No telemetry, no tracking, no external calls
- You own 100% of your data

## Support

- Documentation: Planned for Q2 2026
- Community: Discord/Telegram (Planned for Q2 2026)
- Issues: GitHub repository (Planned for Q2 2026)
- Current support: ClawHub skill page discussions

## Roadmap

**Version 1.0 (Current)**
- Basic tracking & recommendations
- Simple optimization suggestions
- Weekly reports

**Version 2.0 (Premium)**
- Advanced value mapping
- Predictive optimization
- Custom integrations
- Priority support

## License

Free for personal and commercial use. Premium features require subscription.

---

**Built by TokenLens — "Every token, fully seen."**