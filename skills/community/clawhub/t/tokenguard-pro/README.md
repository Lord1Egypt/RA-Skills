# TokenGuard Pro 🛡️

**AI Token Cost Optimizer for OpenClaw**

TokenGuard Pro helps OpenClaw users reduce their AI API costs by 50-95% through intelligent analysis of usage patterns and actionable optimization recommendations.

## Overview

Running AI agents at scale gets expensive fast. TokenGuard Pro scans your usage patterns and identifies specific, fixable sources of waste:

- **Context bloat** — Old messages piling up unnecessarily
- **Model mismatch** — Using expensive models for simple tasks
- **Repeated queries** — Same questions asked without caching
- **Inefficient tool chains** — Unnecessary tool call sequences

## Who This Is For

- OpenClaw users spending $100–$3,600/month on AI APIs
- Teams running multiple agents in production
- Anyone noticing steadily increasing API bills

## Installation

```bash
npx clawhub install tokenguard-pro
```

## Usage

### Basic Analysis

```bash
# Analyze recent usage (default: last 14 days)
tokenguard-analyze

# Specify time range
tokenguard-analyze --days 30
tokenguard-analyze --since 2024-01-01
```

### Focused Analysis

```bash
# Focus on specific optimization areas
tokenguard-analyze --focus model      # Model selection issues
tokenguard-analyze --focus context    # Context size issues
tokenguard-analyze --focus caching    # Missing caching opportunities
tokenguard-analyze --focus tools      # Inefficient tool usage
```

### Output Options

```bash
# Pretty-printed table (default)
tokenguard-analyze

# JSON for programmatic use
tokenguard-analyze --format json

# Save to file
tokenguard-analyze --output report.txt
```

## Understanding the Report

The analysis report includes:

1. **Usage Summary** — Total tokens, estimated costs, peak usage periods
2. **Waste Identification** — Specific patterns draining your budget
3. **Optimization Recommendations** — Actionable fixes with step-by-step guidance
4. **Savings Projection** — Estimated monthly savings if recommendations are applied

## Sample Recommendations

### Context Pruning
```
Issue: Conversations averaging 12K tokens
Fix: Implement sliding window (keep last 10 messages)
Savings: ~$340/month
```

### Model Downgrade
```
Issue: GPT-4 used for 65% of tasks suitable for GPT-3.5
Fix: Route simple queries to cheaper model
Savings: ~$520/month
```

### Query Caching
```
Issue: 34 identical "check weather" queries in 7 days
Fix: Cache responses for 1 hour
Savings: ~$45/month
```

## Architecture

TokenGuard Pro analyzes:
- Session logs for token consumption patterns
- Tool call sequences for inefficiencies
- Model usage distribution
- Context growth over time

## Limitations

- Historical analysis only (not real-time monitoring)
- Cost estimates based on standard pricing tiers
- Cannot automatically apply fixes (provides guidance only)
- Requires readable OpenClaw session logs

## Pricing

**$49 one-time license**

ROI: If you're spending $500/month and we save you 50%, this pays for itself in 12 days.

## Changelog

### v1.0.0
- Initial release
- Full usage pattern analysis
- JSON and pretty-printed report formats
- Focused analysis modes

## License

Commercial license included with ClawHub purchase.

## Support

- GitHub Issues: github.com/appincubator/tokenguard-pro
- Email: support@appincubator.io
