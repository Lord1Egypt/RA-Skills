# Contributing

Thanks for your interest in contributing! 🎉

## How to contribute

### 🐛 Bug reports

Before opening an issue, please:
1. Search existing issues to avoid duplicates
2. Test on the latest version
3. Provide:
   - Python version
   - OS
   - Exact command that triggered the bug
   - Full error trace
   - Expected vs actual behavior

### 💡 Feature requests

Open an issue with:
- Clear use case
- Proposed API / behavior
- Whether you can implement it yourself

### 🛠 Pull requests

1. **Fork** and create a branch from `main`
2. **Add tests** if you're changing logic
3. **Run tests**: `pytest tests/`
4. **Format**: `black src/ tests/`
5. **Lint**: `ruff check src/`
6. **Commit** with conventional format: `feat: add X`, `fix: handle Y`, etc.
7. **Open PR** with clear description

### 📊 Adding a new data source

Data sources should follow this contract:

```python
def fetch_realtime(codes: list[str]) -> dict[str, dict]:
    """Returns: {code: {price, pct_change, open, high, low, prev_close, ...}}"""

def fetch_hist_kline(code: str, days: int = 90) -> pandas.DataFrame:
    """Returns: DataFrame with columns [日期, 开盘, 收盘, 最高, 最低, 成交量]"""
```

Add to `src/stock_realtime_brief/data_sources.py` and register in the priority chain.

### 📈 Adding a new indicator

Add a function to `src/stock_realtime_brief/indicators.py`:

```python
def my_indicator(closes: list[float], **params) -> float | None:
    """Description of what this indicator measures."""
    if len(closes) < required_length:
        return None
    return computed_value
```

Then expose via the analyzer chain.

### 🌍 Translations

Especially welcome! Open a PR adding `README_<lang>.md` and translating key user-facing strings in source.

## Code style

- Python 3.10+
- Type hints required for public APIs
- Docstrings for public functions
- Keep functions under 80 lines
- No global state (pass dependencies explicitly)

## Development setup

```bash
git clone https://github.com/Michaelliugh/stock-realtime-brief.git
cd stock-realtime-brief
pip install -e ".[dev]"
pytest
```

## Code of Conduct

Be respectful, assume good intent, and focus on what's best for users. Personal attacks, harassment, or discriminatory remarks will not be tolerated.

## Questions?

Open a discussion on GitHub Discussions or contact via Issues.
