# Utility Bill Analyzer

> Detect anomalies, compare usage, forecast costs, and get savings suggestions for electricity, water, and gas bills.

## What It Does

- 📊 **Track** monthly utility bills in a simple JSON database
- ⚠️ **Detect anomalies** — flags bills where usage exceeds 1.5× the rolling average
- 📅 **Compare** same-month usage across years to spot trends
- 🔮 **Forecast** next bill based on seasonal patterns and recent trends
- 📈 **Visualize** usage with ASCII bar charts in the terminal
- 💡 **Suggest savings** based on your usage patterns and 100+ efficiency tips
- 💰 **Track cost per unit** — distinguish rate hikes from usage increases

## Quick Start

```bash
# Add bills
python3 scripts/bill_analyzer.py add --type electricity --date 2025-01-15 --usage 450 --cost 67.50
python3 scripts/bill_analyzer.py add --type gas --date 2025-01-15 --usage 120 --cost 72.00
python3 scripts/bill_analyzer.py add --type water --date 2025-01-15 --usage 8 --cost 25.00

# View history
python3 scripts/bill_analyzer.py history

# Check for anomalies
python3 scripts/bill_analyzer.py anomaly

# Compare January across years
python3 scripts/bill_analyzer.py compare --month 01

# Forecast next bill
python3 scripts/bill_analyzer.py forecast

# Full annual report
python3 scripts/bill_analyzer.py report
```

## Requirements

- Python 3.7+ (stdlib only, no pip dependencies)

## Commands

| Command | Description |
|---------|-------------|
| `add` | Record a bill: `--type`, `--date`, `--usage`, `--cost` |
| `history` | Usage/cost trend with ASCII bar chart |
| `compare --month MM` | Same-month year-over-year comparison |
| `anomaly` | Detect bills >1.5× rolling average |
| `forecast` | Predict next bill from seasonal data |
| `report` | Annual summary + savings suggestions |

All commands (except `add`) accept `--type electricity|water|gas` to filter by utility type.

## Data

Bills are stored in `scripts/bills.json`. Specify a custom path with `--db <path>`.

## License

MIT © Denis Voronin
