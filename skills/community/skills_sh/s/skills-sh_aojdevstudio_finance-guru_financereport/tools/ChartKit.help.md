# ChartKit Help

Chart generation CLI for Finance Guru PDF reports.

## Usage

```bash
uv run python ChartKit.py --ticker TICKER --chart-type TYPE [OPTIONS]
```

## Required Arguments

| Argument | Description |
|----------|-------------|
| `--chart-type` | Chart type: `line`, `bar`, `barh`, `heatmap`, `technical` |

## Optional Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--ticker` | - | Stock ticker symbol |
| `--tickers` | - | Comma-separated tickers (for heatmap) |
| `--days` | 90 | Days of historical data |
| `--data` | - | JSON data string (alternative to CLI tools) |
| `--title` | Auto | Custom chart title |
| `--output` | chart.png | Output file path |
| `--figsize` | 7,3 | Figure size as width,height |
| `--dpi` | 150 | Output resolution |

## Chart Types

### Line Chart
Best for: Price history, trends, moving averages
```bash
uv run python ChartKit.py --ticker TSLA --chart-type line --days 90
```

### Bar Chart (Horizontal)
Best for: Comparing metrics across categories
```bash
uv run python ChartKit.py --ticker TSLA --chart-type barh --data '{"labels":["Sharpe","Sortino","Beta"],"values":[1.5,2.1,1.2]}'
```

### Heatmap
Best for: Correlation matrices
```bash
uv run python ChartKit.py --chart-type heatmap --tickers TSLA,PLTR,NVDA,AAPL
```

### Technical Chart
Best for: Price with RSI/MACD overlay
```bash
uv run python ChartKit.py --ticker TSLA --chart-type technical --days 90
```

## Data Sources

ChartKit integrates with Finance Guru CLI tools:
- `risk_metrics_cli.py` - For risk/return data
- `momentum_cli.py` - For technical indicators
- `correlation_cli.py` - For correlation matrices

## Output

Charts are saved as PNG files at the specified DPI.
For PDF embedding, use `--dpi 150` minimum.
