---
name: "TokenBooks Cross-Provider AI Spend Dashboard"
description: "See where your AI money goes. Track spending across OpenAI, Anthropic, Google, and more. Per-provider breakdowns, per-model costs, budget tracking, waste detection."
author: "@TheShadowRose"
version: "1.0.0"
tags: ["spending", "dashboard", "analytics", "budget", "multi-provider", "cost-tracking"]
license: "MIT"
---

# TokenBooks Cross-Provider AI Spend Dashboard

See where your AI money goes. Track spending across OpenAI, Anthropic, Google, and more. Per-provider breakdowns, per-model costs, budget tracking, waste detection.

---

**See where your AI money goes. Track spending across OpenAI, Anthropic, Google, and more. Find waste. Stay under budget.**

TokenBooks imports billing data from multiple AI providers, aggregates everything into one view, and shows you exactly where every dollar went. Per-provider breakdowns, per-model costs, time series trends, budget tracking, and waste detection — all in one tool, all local, zero cloud dependencies.

---

## The Problem

You use OpenAI for coding, Anthropic for research, Google for experiments. Each has its own billing dashboard. You have no idea:
- How much you're spending **total** across all providers
- Which models are eating your budget
- Whether you're on track for your monthly limit
- If you're using expensive models for simple tasks

Manually exporting CSVs and combining them in Excel is tedious and error-prone.

## What TokenBooks Does

### Unified Dashboard
- Import from OpenAI (CSV), Anthropic (JSON), Google Cloud, or custom formats
- See total spending across all providers in one place
- Per-provider, per-model, per-task breakdowns
- Visual HTML reports with CSS-based charts (zero JavaScript)

### Budget Tracking
- Set monthly budgets
- See remaining balance and utilization percentage
- Alerts when you hit 80% or 95%

### Waste Detection
- Identify expensive models used for simple tasks
- Calculate cost-per-1k-tokens for each model
- Suggest cheaper alternatives

### Time Series Analysis
- Daily, weekly, or monthly spending trends
- See when costs spiked
- Compare this month vs. last month

### Task-Level Tracking
- Tag API calls with task names ("code_review", "documentation", etc.)
- See which tasks cost the most
- Optimize task-to-model assignments

---

## Quick Start

```bash
# 1. Import billing data
python3 token_import.py openai_billing.csv --provider openai --output data.json

# 2. Analyze spending
python3 token_books.py data.json --budget 100

# 3. Generate HTML dashboard
python3 token_report.py data.json --output dashboard.html --budget 100
```

Open `dashboard.html` in a browser to see:
- Total spend and token usage
- Provider and model breakdowns
- Daily spending trend (last 30 days)
- Budget status
- Waste detection alerts

---

## Usage Guide

### Import Data

**From OpenAI:**
```bash
# Download CSV from OpenAI usage dashboard
python3 token_import.py openai_usage.csv --provider openai --output data.json
```

**From Anthropic:**
```bash
# Download JSON from Anthropic console
python3 token_import.py anthropic_usage.json --provider anthropic --output data.json
```

**From Custom CSV:**
```bash
# Provide column mapping
python3 token_import.py my_billing.csv --provider custom --column-map mapping.json --output data.json
```

**Column mapping format (mapping.json):**
```json
{
  "timestamp": "Date",
  "provider": "API_Provider",
  "model": "Model_Name",
  "input_tokens": "Prompt_Tokens",
  "output_tokens": "Response_Tokens",
  "cost": "Cost_USD"
}
```

### Analyze Spending

```bash
# Basic analysis
python3 token_books.py data.json

# With budget tracking
python3 token_books.py data.json --budget 100

# JSON output for scripting
python3 token_books.py data.json --output json > analysis.json
```

### Generate Dashboard

```bash
# Generate HTML dashboard
python3 token_report.py data.json --output dashboard.html

# With budget status
python3 token_report.py data.json --output dashboard.html --budget 100
```

---

## Use Cases

### 1. **Multi-Provider Cost Tracking**
You use OpenAI, Anthropic, and Google. Import all billing data into TokenBooks, see total spend in one place.

### 2. **Budget Enforcement**
Set a $100/month budget. TokenBooks tells you when you've spent $80 (warning) or $95 (critical). Avoid surprise bills.

### 3. **Model Optimization**
See which models cost the most. If GPT-4 is 80% of your spend but only used for simple tasks, switch to GPT-3.5 Turbo.

### 4. **Task Cost Allocation**
Tag API calls with task names. See that "code_review" costs $30/month while "documentation" costs $5. Optimize accordingly.

### 5. **Team Reporting**
Generate monthly HTML dashboards for your team. Share spending trends and optimization opportunities.

### 6. **Vendor Comparison**
Compare costs across providers for similar workloads. Maybe Anthropic is cheaper for your use case than OpenAI.

---

## What Gets Tracked

### Per-Provider
- Total cost
- Total tokens (input + output)
- Request count

### Per-Model
- Total cost
- Token usage
- Request count
- Cost per 1k tokens

### Per-Task
- Total cost (if you tag API calls)
- Token usage
- Request count

### Time Series
- Daily, weekly, or monthly trends
- Spot spending spikes
- Compare periods

### Waste Detection
- Models with high cost-per-token ratios
- Suggestions for cheaper alternatives
- Identify over-provisioned tasks

---

## Configuration

See `config_example.json` for reference constants and example values

```python
# Set monthly budget
MONTHLY_BUDGET = 100.0

# Update pricing for accurate cost calculation
MODEL_PRICING = {
    'gpt-4': {'input': 30.0, 'output': 60.0},
    'claude-3-opus': {'input': 15.0, 'output': 75.0},
}

# Budget alert thresholds
ALERT_THRESHOLDS = {
    'warning': 80,  # 80% utilization
    'critical': 95  # 95% utilization
}

# Waste detection threshold
WASTE_THRESHOLD = 0.10  # $0.10 per 1k tokens

# Number of top models to show
TOP_MODELS_LIMIT = 10
```

See `config_example.json` for full options.

---

## Examples

### Example 1: Monthly Budget Tracking

```bash
# Import January data
python3 token_import.py openai_jan.csv --provider openai --output jan.json

# Check budget status
python3 token_books.py jan.json --budget 100

# Output:
# Total cost: $87.42
# 📊 Budget Analysis:
#   Monthly budget: $100.00
#   Spent this month: $87.42
#   Remaining: $12.58
#   Utilization: 87.4%
```

### Example 2: Waste Detection

```bash
python3 token_books.py data.json

# Output:
# 💡 Potential Waste Detected:
#   gpt-4: $45.23 (127 requests)
#     → Consider using a cheaper model for simple tasks
```

### Example 3: Multi-Provider Dashboard

```bash
# Import from multiple providers
python3 token_import.py openai.csv --provider openai --output combined.json
python3 token_import.py anthropic.json --provider anthropic --output temp.json

# Merge manually or import again (appends)
# ... (or use custom tooling to merge JSON files)

# Generate unified dashboard
python3 token_report.py combined.json --output dashboard.html
```

---

## What's Included

| File | Purpose |
|------|---------|
| `token_books.py` | Main aggregation engine (CLI + library) |
| `token_import.py` | Import parsers for OpenAI, Anthropic, custom CSV |
| `token_report.py` | HTML dashboard generator |
| `config_example.json` | Configuration template |
| `README.md` | This file |
| `LIMITATIONS.md` | What it doesn't do |
| `LICENSE` | MIT License |

---

## Requirements

- Python 3.7+
- **Zero external dependencies** (stdlib only)
- Works on Linux, macOS, Windows

---

## Python API

Use TokenBooks in your own scripts:

```python
from token_import import ImportManager, UsageRecord
from token_books import CostAggregator
from token_report import DashboardGenerator

# Import data
manager = ImportManager()
manager.import_openai('openai.csv')
records = manager.get_all_records()

# Analyze
aggregator = CostAggregator(records)

print(f"Total cost: ${aggregator.get_total_cost():.2f}")
print(f"Total tokens: {aggregator.get_total_tokens():,}")

# By provider
by_provider = aggregator.by_provider()
for provider, breakdown in by_provider.items():
    print(f"{provider}: ${breakdown.total_cost:.2f}")

# Generate dashboard
html = DashboardGenerator.generate(records, monthly_budget=100.0)
with open('dashboard.html', 'w') as f:
    f.write(html)
```

---

## quality-verified


---

## FAQ

**Q: Does it work with Google Cloud billing?**  
A: Not directly. Google Cloud billing CSVs can be imported via custom CSV parser with column mapping. See config_example.json for mapping format.

**Q: Can it track API calls in real-time?**  
A: No. TokenBooks analyzes exported billing data, not live API usage. Export from your provider, then import.

**Q: Does it send data anywhere?**  
A: **No.** Everything runs locally. Zero network calls.

**Q: How do I tag API calls with task names?**  
A: Add a "task" field to your billing exports. If your provider doesn't support this, manually add it to the CSV before importing.

**Q: Can I combine multiple months of data?**  
A: Yes. Import each month's data into the same JSON file, or merge JSON files manually.

**Q: Does it support non-USD currencies?**  
A: Not directly. Convert to USD before importing, or manually adjust cost values.

---

## License

MIT — See `LICENSE` file.

---

## Author

**Shadow Rose**

Built for people who want to understand and control their AI spending without enterprise-grade analytics platforms.


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


**TRADING DISCLAIMER:** This software is a tool, not a trading system. It does not 
make trading decisions for you and does not guarantee profits. Trading cryptocurrency, 
stocks, or any financial instrument carries significant risk of loss. You can lose 
some or all of your investment. Past performance of any system or methodology is not 
indicative of future results. Never trade with money you cannot afford to lose. 
Consult a qualified financial advisor before making investment decisions.
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

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)