# Output Formats

All `yf` commands support an `--output` / `-o` flag that controls how results are rendered.
Available values depend on the command — check [commands.md](commands.md) for per-command support.

---

## Comparison

| Format | Flag | Supported by | Best for |
|--------|------|--------------|----------|
| Table (default) | _(none)_ | all commands | Displaying results directly to the user |
| JSON | `--output json` | all commands | Parsing values, computing statistics, chaining commands |
| CSV | `--output csv` | most commands* | Exporting data for spreadsheet or downstream processing |

\* `calendar`, `info`, `market`, `news`, `search` do not support CSV.

---

## Table (default)

Rich-formatted table with borders and aligned columns. Uses ANSI colour codes to highlight
positive/negative changes.

```
yf quote AAPL
```

```
┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃        ┃        ┃        ┃        ┃        ┃       ┃        ┃        ┃   Mkt ┃
┃ Symbol ┃  Price ┃ Change ┃  Chg % ┃   Open ┃  High ┃    Low ┃ Volume ┃   Cap ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ AAPL   │ 269.37 │  -2.13 │ -0.78% │ 271.44 │ 272.8 │ 269.31 │      — │ 3959… │
└────────┴────────┴────────┴────────┴────────┴───────┴────────┴────────┴───────┘
```

**Use when:** the result is the final answer to show the user.

---

## JSON

Structured output. Returns either an array (for list results like `quote`, `options`) or an
object (for keyed results like `financials`).

```
yf quote AAPL --output json
```

```json
[
  {
    "symbol": "AAPL",
    "currency": "USD",
    "last_price": 269.45,
    "previous_close": 271.5,
    "open": 271.44,
    "day_high": 272.8,
    "day_low": 269.31,
    "volume": null,
    "market_cap": 3960356340118.0,
    "fifty_day_average": 260.51,
    "two_hundred_day_average": 252.44,
    "change": -2.05,
    "change_pct": -0.76
  }
]
```

**Use when:**
- You need to extract a specific field (e.g. `last_price`, `change_pct`)
- You are passing data to a second command or computation
- You want to compare values across multiple tickers

**Tip:** pipe into `python3 -c` or `jq` for quick field extraction:
```bash
yf quote AAPL MSFT --output json | python3 -c "
import json, sys
for r in json.load(sys.stdin):
    print(r['symbol'], r['last_price'])
"
```

---

## CSV

Comma-separated values with a header row. No ANSI codes, no borders.

```
yf quote AAPL --output csv
```

```
symbol,currency,last_price,previous_close,open,day_high,day_low,volume,market_cap,fifty_day_average,two_hundred_day_average,change,change_pct
AAPL,USD,269.45,271.5,271.44,272.8,269.31,,3960356340118.0,260.51,252.44,-2.05,-0.76
```

**Use when:**
- The user wants to save data to a file (`> data.csv`)
- The user wants to open results in a spreadsheet

**Redirect to file:**
```bash
yf history AAPL --period 1y --output csv > aapl_1y.csv
```

---

## Disabling Colour (`--no-color`)

`--no-color` is a **global flag** — it must appear before the subcommand name:

```bash
yf --no-color quote AAPL        # correct
yf quote AAPL --no-color        # error: No such option
```

**Use when:**
- Output will be logged or piped to a file
- The terminal does not support ANSI escape codes
- The agent's environment strips colour codes unpredictably
