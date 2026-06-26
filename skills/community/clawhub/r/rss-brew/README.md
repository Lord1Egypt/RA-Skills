# rss-brew 🍺

A personal RSS digest pipeline that fetches, scores, analyzes, and delivers curated news digests — powered by LLMs.

## What it does

RSS-Brew runs a multi-phase pipeline:

1. **Fetch** — pull items from your RSS feeds
2. **Score** — rule-based and LLM-based relevance scoring
3. **Analyze** — enrich top items with context (via Tavily search)
4. **Rank & Distribute** — select the best items, deduplicate
5. **Render** — generate a formatted digest (PDF / Markdown)
6. **Deliver** — track delivery status per run

## Requirements

- Python 3.10+
- `DEEPSEEK_API_KEY` — for LLM scoring (DeepSeek via OpenAI-compatible API)
- `TAVILY_API_KEY` — for context enrichment (optional but recommended)

## Installation

```bash
git clone https://github.com/your-username/rss-brew.git
cd rss-brew
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Set your API keys in environment variables or a `.env` file:

```bash
DEEPSEEK_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

Choose a data root directory where RSS-Brew will store run records, digests, and state:

```bash
export RSS_BREW_DATA_ROOT=~/rss-brew-data
```

## Usage

```bash
export PYTHONPATH=app/src

# Dry run (no writes, preview scoring)
python3 -m rss_brew.cli dry-run --data-root ~/rss-brew-data --debug

# Full run
python3 -m rss_brew.cli run --data-root ~/rss-brew-data

# Inspect latest run
python3 -m rss_brew.cli inspect latest --data-root ~/rss-brew-data

# Mark latest digest as sent
python3 -m rss_brew.cli delivery update --data-root ~/rss-brew-data --status sent
```

## Project structure

```
rss-brew/
├── scripts/          # Runtime pipeline scripts (source of truth)
├── app/
│   └── src/
│       └── rss_brew/ # App wrapper + CLI entrypoint
├── references/       # Usage, ops, and pipeline spec docs
├── docs/             # Architecture and implementation docs
├── requirements.txt
└── SKILL.md          # OpenClaw skill descriptor
```

## Architecture notes

RSS-Brew uses a **wrapper architecture**: the `app/` layer provides a clean CLI and packaging boundary, while `scripts/` remains the runtime source of truth. This allows the pipeline to be used both standalone and as an OpenClaw skill.

See [`app/docs/architecture.md`](app/docs/architecture.md) for full details.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `DEEPSEEK_API_KEY` | Yes | LLM scoring (DeepSeek or compatible) |
| `TAVILY_API_KEY` | No | Context enrichment via Tavily search |

## License

MIT
