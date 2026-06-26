# Token Tamer — AI API Cost Control

**Monitor, budget, and optimize AI API spending across ANY provider.**

Token Tamer tracks every AI API call, enforces budgets, detects waste, and provides actionable optimization recommendations. Works with OpenAI, Anthropic, Google, xAI, OpenRouter, or any custom provider. Stop runaway costs before they happen.

---

## The Problem

AI API costs are unpredictable and can spiral out of control:

- **No visibility** — You don't know how much you're spending until the bill arrives
- **Runaway costs** — One buggy loop can burn $100 in minutes
- **No budgets** — APIs don't stop when you hit a limit; they just charge more
- **Hidden waste** — Duplicate calls, oversized contexts, unnecessary retries
- **No attribution** — Can't tell which task/model/session is costing the most

Manual cost tracking doesn't work. Spreadsheets are always outdated. Provider dashboards are too slow.

## What Token Tamer Does

### 1. **Real-Time Cost Tracking** (`token_tamer.py`)
- Log every API call: provider, model, tokens, cost
- Per-task and per-session cost attribution
- Configurable model pricing database (all major providers included)
- Custom provider support (bring your own pricing)
- Persistent storage (JSON-based, survives restarts)

### 2. **Budget Enforcement**
- Daily, weekly, and monthly budget limits
- Configurable alert thresholds (warning at 80%, critical at 95%)
- **Kill switch** — Hard stop at 100% of budget (blocks all API calls)
- Pre-call budget check (prevent calls that would exceed budget)
- Status dashboard (see current spend vs. budget at any time)

### 3. **Cost Reports** (`token_reports.py`)
- Daily, weekly, monthly summaries
- Breakdown by provider (which provider costs the most?)
- Breakdown by task (which tasks burn budget fastest?)
- Breakdown by model (are you using expensive models unnecessarily?)
- JSON and text output formats

### 4. **Waste Detection** (`token_optimizer.py`)
- **Duplicate calls** — Detects identical calls within time window
- **Excessive retries** — Flags tasks with too many retry attempts
- **Large contexts** — Identifies calls with bloated input (>50K tokens)
- **Low output ratio** — Finds calls sending huge context, getting tiny output
- **Overqualified models** — Detects expensive models used for simple tasks
- Estimates cost savings from eliminating waste

### 5. **Optimization Recommendations**
- Model selection advice (cheaper alternatives for routine tasks)
- Task-level optimization (which tasks need caching/refactoring)
- Potential savings calculation (how much you could save)
- Prioritized recommendations (fix high-impact issues first)

---

## Quick Start

```bash
# 1. Configure Token Tamer
cp config_example.py token_config.py
# Edit token_config.py with your budgets and model pricing

# 2. Log an API call
python3 token_tamer.py --log \
    --provider openai \
    --model gpt-4o \
    --input-tokens 1500 \
    --output-tokens 300 \
    --task "code_generation" \
    --session "sess_001"

# 3. Check status
python3 token_tamer.py --status

# 4. Generate daily report
python3 token_reports.py --daily

# 5. Detect waste
python3 token_optimizer.py --detect-waste --days 7

# 6. Get optimization recommendations
python3 token_optimizer.py --recommendations --days 7
```

---

## Design Philosophy

### Budget First, Optimize Second
Set budgets before you start spending. Kill switch ensures you never exceed limits, even if code goes haywire.

### Provider-Agnostic
Token Tamer doesn't care which AI provider you use. Configure pricing, log usage, track costs. Works with any API that returns token counts.

### Zero External Dependencies
Pure Python stdlib. No pip installs, no network calls (except your API usage). Runs anywhere Python runs.

### Actionable Insights
Reports aren't just numbers. Token Tamer tells you **what** is expensive and **how** to fix it.

### Safety by Default
Kill switch activates automatically when budget exceeded. Better to block one API call than burn $1000.

---

## Use Cases

### For Indie Developers
- **Cost control** — Never exceed your budget (critical when using personal credit card)
- **Waste detection** — Find and fix expensive bugs before they drain your account
- **Model selection** — Use expensive models only when necessary, cheaper models for routine tasks

### For Startups
- **Budget allocation** — Track costs per feature/customer/session
- **Scalability testing** — Project costs as you scale (how much will 10x users cost?)
- **Investor reporting** — Show AI cost metrics to investors/stakeholders

### For Enterprises
- **Multi-team tracking** — Attribute costs to specific teams/projects/tasks
- **Compliance** — Audit trail of all API usage
- **Cost optimization** — Identify waste at scale, optimize before it compounds

### For AI Researchers
- **Experiment tracking** — Cost per experiment/run
- **Model comparison** — Which model gives best quality/cost ratio?
- **Hyperparameter tuning** — How much does each tuning run cost?

---

## What's Included

| File | Purpose |
|------|---------|
| `token_tamer.py` | Main cost tracking and budget engine |
| `token_reports.py` | Report generation (daily, weekly, by-task) |
| `token_optimizer.py` | Waste detection and optimization suggestions |
| `config_example.py` | Configuration template with all settings |
| `LIMITATIONS.md` | What Token Tamer doesn't do |
| `LICENSE` | MIT License |

---

## Configuration

See `config_example.py` for full details. Key settings:

### Budgets
```python
BUDGETS = {
    'daily': 10.00,      # $10/day
    'weekly': 50.00,     # $50/week
    'monthly': 150.00,   # $150/month
}

ALERT_THRESHOLDS = {
    'warning': 80,    # Warn at 80%
    'critical': 95,   # Critical at 95%
    # Kill switch at 100%
}
```

### Model Pricing
```python
MODEL_PRICING = {
    'openai/gpt-4o': {
        'input': 2.50,   # Per million tokens
        'output': 10.00
    },
    'anthropic/claude-sonnet-4': {
        'input': 3.00,
        'output': 15.00
    },
    # Add your models here
}
```

### Waste Detection
```python
WASTE_THRESHOLDS = {
    'duplicate_window_minutes': 5,
    'excessive_retries_count': 3,
    'large_context_tokens': 50000,
    'low_output_ratio': 0.01,
}
```

---

## Advanced Usage

### Integration with API Wrapper

```python
from token_tamer import TokenTamer
import token_config as config

tamer = TokenTamer(config)

def call_openai_api(prompt):
    # Check budget before calling
    if not tamer.check_before_call(estimated_cost=0.10):
        raise Exception("Budget exceeded — kill switch active")
    
    # Make API call
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Log usage
    cost, status = tamer.log_usage(
        provider="openai",
        model="gpt-4o",
        input_tokens=response['usage']['prompt_tokens'],
        output_tokens=response['usage']['completion_tokens'],
        task="chat"
    )
    
    if status == 'KILL':
        raise Exception("Kill switch activated after this call")
    
    return response
```

### Daily Cost Report (cron)

```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/token-tamer && python3 token_reports.py --daily --format text | mail -s "Daily AI Cost Report" you@example.com
```

### Weekly Optimization Review

```bash
# Run weekly on Monday morning
0 9 * * 1 cd /path/to/token-tamer && python3 token_optimizer.py --recommendations --days 7
```

### Pre-Deployment Budget Check

```bash
# Check if we're within budget before deploying
python3 token_tamer.py --check || exit 1
# If kill switch is active, deployment is blocked
```

---

## Reports Examples

### Daily Report
```
============================================================
            Daily Report: 2026-02-21
============================================================

Total calls:           127
Total tokens:      1,234,567
  Input:             987,654
  Output:            246,913
Total cost:          $  12.34
Avg cost/call:       $   0.0972
Avg tokens/call:          9,721
```

### By Provider Report
```
BY PROVIDER
────────────────────────────────────────────────────────────

openai               $   8.50     89 calls   1,000,000 tokens
anthropic            $   3.20     28 calls     200,000 tokens
google               $   0.64     10 calls      34,567 tokens
```

### Waste Detection
```
WASTE DETECTION REPORT
============================================================

Period: Last 7 days
Total records analyzed: 1,234
Total waste detected: $45.67

Waste Detected:

  • 12 groups of duplicate API calls within 5 minutes
    Estimated waste: $23.45

  • 5 tasks with >3 retry attempts
    Estimated waste: $12.34

  • 34 calls with input >50,000 tokens
    Estimated waste: $9.88

Recommendations:

  → Implement caching to avoid duplicate calls
  → Add exponential backoff and better error handling
  → Implement context pruning and summarization
```

---

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- Works on Linux, macOS, Windows
- ~100KB disk space for code
- Usage data storage grows with usage (JSON file)

---

## License

MIT — See `LICENSE` file.


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.

---

?? **GitHub:** https://github.com/TheShadowRose
?? **Found a bug?** Email TheShadowyRose@proton.me
? **Ko-fi:** https://ko-fi.com/theshadowrose
?? **Twitter:** https://x.com/TheShadowyRose
---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at . If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)

