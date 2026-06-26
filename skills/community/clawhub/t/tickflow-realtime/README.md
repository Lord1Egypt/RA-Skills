# tickflow-realtime

A Codex skill for querying real-time quotes and daily K-lines from TickFlow.

## What It Does

This skill wraps the TickFlow HTTP API and provides two main capabilities:

- Real-time quotes for one or more symbols
- K-line queries, with `1d` as the default period

It supports:

- Single-symbol quote lookup
- Multi-symbol quote comparison
- Quote lookup by `universes`
- Single-symbol K-line queries
- Batch K-line queries for multiple symbols

## Project Structure

```text
.
├── SKILL.md
├── README.md
├── TODO.md
├── references/
│   ├── api.md
│   └── output-contract.md
└── scripts/
    ├── query_klines.py
    ├── query_quotes.py
    └── tickflow_common.py
```

## Requirements

- Python 3
- A valid TickFlow API key

## API Key

This project reads the API key from the environment variable:

```bash
export TICKFLOW_API_KEY=your_key_here
```

The key is sent as the `x-api-key` header.

## Usage

### Real-Time Quotes

Single symbol:

```bash
python3 scripts/query_quotes.py --symbols 600519.SH --format summary
```

Multiple symbols:

```bash
python3 scripts/query_quotes.py --symbols 600519.SH,000001.SZ,AAPL.US --format table
```

Universe query:

```bash
python3 scripts/query_quotes.py --universes my-universe-id --format json --pretty
```

### K-Lines

Single symbol daily K:

```bash
python3 scripts/query_klines.py --symbol 600519.SH --period 1d --count 20 --format table
```

Batch latest daily K:

```bash
python3 scripts/query_klines.py --symbols 600519.SH,000001.SZ --period 1d --count 1 --format summary
```

Adjusted K-lines:

```bash
python3 scripts/query_klines.py --symbol 600519.SH --period 1d --count 60 --adjust forward --format table
```

## Output Modes

Both scripts support:

- `summary`
- `table`
- `json`

For JSON output, add `--pretty` for formatted output.

## Notes

- TickFlow percentage fields use the convention `0.01 -> 1%`
- Timestamps are epoch milliseconds
- K-line responses are returned in compact columnar form and are expanded by the script before summary/table rendering

## References

- Skill definition: [SKILL.md](./SKILL.md)
- API notes: [references/api.md](./references/api.md)
- Output contract: [references/output-contract.md](./references/output-contract.md)

## Publish Checklist

Before pushing to GitHub:

- Confirm `TICKFLOW_API_KEY` is not committed anywhere
- Review `TODO.md` and decide whether to keep it public
- Remove local-only helper files if they are not meant for the repository
- Run:

```bash
python3 -m py_compile scripts/tickflow_common.py scripts/query_quotes.py scripts/query_klines.py
```
