# Reddit Stonks

Scrape Reddit stock pages + AI-powered analysis to find the best stock for a 1-week return.

**Live:** [stonks.altusrossouw.co.za](http://stonks.altusrossouw.co.za) | **192.168.10.170:80**

[![ClawHub](https://img.shields.io/badge/ClawHub-reddit--stonks-green)](https://clawhub.ai/skills/reddit-stonks)

## How it works

1. **Scrapes** 7 stock-related subreddits (r/wallstreetbets, r/stocks, r/investing, etc.) for hot posts
2. **Extracts** stock tickers (`$TICKER` and all-caps mentions) from post titles and bodies
3. **Fetches** real-time stock data via Yahoo Finance (price, P/E, beta, volume, short float, analyst targets)
4. **Analyzes** everything with Deepseek AI to identify the single best stock for a 7-day return

## Quickstart

### CLI

```bash
pip install -r requirements.txt
cp .env.example .env   # add DEEPSEEK_API_KEY
python3 stonks.py       # standard run
python3 stonks.py -e    # with European equivalents
python3 stonks.py -p 10 # fast (fewer posts)
```

### Web App

```bash
pip install -r requirements.txt
cp .env.example .env
python3 -m uvicorn app:app --host 0.0.0.0 --port 8080
```

Then open http://localhost:8080

## Flags

| Flag | Description |
|------|-------------|
| `-e`, `--euro` | Show European exchange equivalents |
| `-p N`, `--posts N` | Posts per subreddit (default: 50) |

## Deployment

Deployed on a Proxmox LXC container (Ubuntu 24.04) behind a systemd service:

```bash
systemctl status stonks   # check status
journalctl -u stonks -f   # tail logs
```

## Output

- Stock data table with price, 1-week change, market cap, P/E, beta, volume, analyst consensus
- AI analysis: Top Pick, Runner-up, Wildcard, Risk Factors, Confidence Score
- Optional: European exchange equivalents (Xetra, Vienna, Swiss, etc.)

## Architecture

| File | Purpose |
|------|---------|
| `app.py` | FastAPI web server + SSE streaming |
| `stonks.py` | CLI orchestrator + AI analysis |
| `reddit_scraper.py` | Reddit JSON API scraper (no auth required) |
| `stock_data.py` | Yahoo Finance data + European ticker lookup |

## Disclaimer

AI-generated analysis for entertainment/educational purposes only. Not financial advice. Past performance does not guarantee future results.
