---
name: "Token Tamer — AI API Cost Control"
description: "Monitor, budget, and optimize AI API spending across any provider. Tracks every call, enforces budgets, detects waste, provides optimization recommendations."
author: "@TheShadowRose"
version: "1.1.0"
tags: ["cost-control", "budget", "optimization", "api-costs", "monitoring", "spending"]
license: "MIT"
---

# Token Tamer — AI API Cost Control

Use this skill to track AI API costs, enforce spending budgets, and get optimization recommendations. Works with any provider: OpenAI, Anthropic, Gemini, Ollama, or custom.

## When to Use This Skill

Invoke this skill when a user asks about:
- "How much am I spending on API calls?"
- Setting daily/weekly/monthly budget limits
- Getting a cost breakdown by model or provider
- Detecting wasteful API usage patterns
- Receiving an alert when spending approaches a budget limit

## Setup

1. Copy `config_example.py` to `token_config.py`
2. Set your budget limits and model pricing
3. Configure your storage file path

```python
# token_config.py
USAGE_FILE = "./token_usage.json"
BUDGETS = {
    'daily': 10.00,
    'weekly': 50.00,
    'monthly': 150.00,
}
ALERT_THRESHOLDS = {
    'warning': 80,   # alert at 80% of budget
    'critical': 95,  # alert at 95% of budget
}
```

## Recording API Usage

Call this after every API request to track the cost:

```python
import token_config as config
from token_tamer import TokenTamer

tamer = TokenTamer(config)

# Log a call — returns (cost, status)
cost, status = tamer.log_usage(
    provider='anthropic',
    model='claude-sonnet-4-5',
    input_tokens=1500,
    output_tokens=800,
    task='summarize',       # optional
    session='sess_001'      # optional
)

if status == 'KILL':
    raise Exception("Kill switch activated — daily budget exceeded")
```

## Checking Budget Status

```python
status = tamer.get_status()
# Returns: {
#   'daily':   { 'cost': 2.40, 'budget': 10.00, 'status': 'OK', 'message': None },
#   'weekly':  { 'cost': 8.10, 'budget': 50.00, 'status': 'OK', 'message': None },
#   'monthly': { 'cost': 8.10, 'budget': 150.00, 'status': 'OK', 'message': None },
#   'kill_switch': False
# }

if status['daily']['status'] == 'CRITICAL':
    print("Daily budget nearly exhausted — switch to cheaper model")
```

## Pre-Call Budget Check

```python
# Check before making an expensive call (returns True = OK, False = blocked)
if not tamer.check_before_call(estimated_cost=0.10):
    raise Exception("Kill switch active — API calls blocked")
```

## Cost Reports

```python
import token_config as config
from token_reports import ReportGenerator

reporter = ReportGenerator(config)

# Daily report
report = reporter.generate_daily_report()
reporter.print_report(report)

# Weekly report
report = reporter.generate_weekly_report()
reporter.print_report(report)

# Breakdown by provider
report = reporter.generate_by_provider_report()
reporter.print_report(report)

# Breakdown by model
report = reporter.generate_by_model_report()
reporter.print_report(report)

# Breakdown by task
report = reporter.generate_by_task_report()
reporter.print_report(report)
```

## Waste Detection & Optimization

```python
import token_config as config
from token_optimizer import WasteDetector, Optimizer

# Detect waste (last 7 days)
detector = WasteDetector(config)
waste = detector.detect_all(days=7)

# Get optimization recommendations
optimizer = Optimizer(config)
recommendations = optimizer.generate_recommendations(days=7)
```

## CLI Usage

```bash
# Check current spend status
python token_tamer.py --status

# Log a call via CLI
python token_tamer.py --log --provider openai --model gpt-4o \
    --input-tokens 1500 --output-tokens 300 --task "code_generation"

# Check if API calls should proceed (exit code 0 = OK, 1 = blocked)
python token_tamer.py --check

# Generate daily report
python token_reports.py --daily

# Detect waste (last 7 days)
python token_optimizer.py --detect-waste --days 7

# Get optimization recommendations
python token_optimizer.py --recommendations --days 7
```

See README.md for full API reference, model pricing configuration, and advanced usage.
