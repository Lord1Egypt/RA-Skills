---
name: searxng
description: "Multi-engine web search aggregation via local Python script. Use when: (1) searching the web for information, articles, documentation, (2) searching code repos on GitHub/GitLab, (3) finding academic papers on arXiv/Semantic Scholar/Crossref, (4) searching Hacker News or Reddit discussions, (5) looking up HuggingFace models, (6) searching StackOverflow for programming answers, (7) fetching news from Bing News or Reuters, (8) any task requiring web search beyond the built-in web_search tool — especially when multiple sources or specific engines are needed. NOT for: single quick lookups (use web_search), image generation, or real-time streaming data."
---

# SearXNG-lite

Lightweight multi-engine aggregated web search. No Docker, no server, no SearXNG instance required — just a single Python script that queries search engines directly.

26 engines across 9 categories, concurrent execution, JSON + compact text output.

## What makes this different

Unlike other SearXNG skills that need a running SearXNG server, this skill:

- **Zero infrastructure** — no Docker, no SearXNG instance, no HTTP server
- **Single file** — one Python script (~850 lines) does everything
- **Direct queries** — sends requests to search engines in-process via httpx
- **Hot-reload config** — edit `config.yml` to toggle categories, changes apply instantly
- **Concurrent** — queries multiple engines in parallel (up to 5 threads)
- **Deduplication** — merges results from multiple engines, scores by cross-engine overlap

## Requirements

- Python 3.10+
- `httpx` — HTTP client (`pip3 install httpx`)
- `lxml` — HTML parser (`pip3 install lxml`, pre-installed on macOS)
- (Optional) `socksio` — for SOCKS proxy support (`pip3 install socksio`)
- (Optional) `pyyaml` — for config parsing (`pip3 install pyyaml`; falls back to built-in parser)

## Quick start

```bash
# Install dependencies
pip3 install httpx lxml

# Search
python3 scripts/search.py "your query"

# List all engines
python3 scripts/search.py --list
```

## How to search

```bash
python3 scripts/search.py "query"                          # default (general + knowledge engines)
python3 scripts/search.py "query" -c dev                   # by category
python3 scripts/search.py "query" -c dev,academic          # multiple categories
python3 scripts/search.py "query" -e github,arxiv          # specific engines
python3 scripts/search.py "query" --all                    # all enabled engines
python3 scripts/search.py "query" -l zh-CN                 # Chinese results
python3 scripts/search.py "query" -n 5                     # limit results
python3 scripts/search.py "query" --compact                # title + url + snippet text output
python3 scripts/search.py --list                           # show all engines & categories
```

All paths are relative to this skill's directory.

## Arguments

| Arg | Short | Default | Description |
|-----|-------|---------|-------------|
| `query` | | required | Search query |
| `--engines` | `-e` | | Comma-separated engine names |
| `--categories` | `-c` | | Comma-separated categories |
| `--max-results` | `-n` | 10 | Max results |
| `--lang` | `-l` | en | Language code (e.g. `en`, `zh-CN`, `de`) |
| `--page` | `-p` | 1 | Page number |
| `--proxy` | | from config | Proxy URL (overrides config/env) |
| `--timeout` | | 12 | Timeout in seconds |
| `--all` | | | Use all enabled engines |
| `--compact` | | | Human-readable text output |
| `--list` | | | List engines and exit |
| `--debug` | | | Enable debug logging |

Without `-e` or `-c`, searches `general` + `knowledge` categories.

## Configuration

Edit `config.yml` in the skill directory to customize behavior:

```yaml
# Proxy for engines that need it (Google, YouTube, Reddit, etc.)
# Supports: http, https, socks5, socks5h
# Leave empty to disable — proxy-required engines will fail silently.
proxy: "socks5h://127.0.0.1:1080"

# Category toggles
categories:
  general: true       # bing, brave, duckduckgo, google🌐, startpage, yahoo
  knowledge: true     # wikipedia, wikidata, wolframalpha🌐
  dev: true           # github, gitlab, stackoverflow, hackernews, reddit🌐, huggingface🌐, mdn
  academic: true      # arxiv, semantic_scholar, google_scholar🌐, crossref
  news: false         # bing_news, reuters
  video: false        # youtube🌐
  images: false       # unsplash
  social: false       # lemmy🌐
  translate: false    # lingva🌐
```

### Proxy setup

Some engines (marked with 🌐) require a proxy to access. Three ways to configure:

1. **config.yml** (recommended): set `proxy: "your-proxy-url"`
2. **Environment variable**: set `HTTPS_PROXY=your-proxy-url`
3. **CLI flag**: pass `--proxy your-proxy-url` per search

Priority: CLI flag > config.yml > environment variable.

If no proxy is configured, 🌐-marked engines will fail silently and results from other engines are still returned.

### Config hot-reload

The config file is read on every search call. No restart needed — just edit and save.

If `config.yml` is missing, the script falls back to a default set of engines: `bing`, `brave`, `duckduckgo`, `wikipedia`.

## Categories and engines

| Category | Engines | Use for |
|----------|---------|---------|
| `general` | bing, brave, duckduckgo, google🌐, startpage, yahoo | General web search |
| `knowledge` | wikipedia, wikidata, wolframalpha🌐 | Facts, definitions, calculations |
| `dev` | github, gitlab, stackoverflow, hackernews, reddit🌐, huggingface🌐, mdn | Code, repos, dev Q&A, AI models |
| `academic` | arxiv, semantic_scholar, google_scholar🌐, crossref | Papers, citations |
| `news` | bing_news, reuters | Current events |
| `video` | youtube🌐 | Video search |
| `images` | unsplash | Free stock photos |
| `social` | lemmy🌐 | Community discussions |
| `translate` | lingva🌐 | Translation |

🌐 = requires proxy. Without proxy, these engines are skipped.

## Output format

Default JSON:
```json
{
  "query": "search term",
  "results": [
    {"title": "...", "url": "...", "content": "...", "engines": ["bing","brave"], "score": 2}
  ],
  "result_count": 15,
  "elapsed": 2.1,
  "engines_used": ["bing", "brave", "wikipedia"],
  "errors": []
}
```

`--compact` outputs human-readable text: numbered title, URL, snippet, engine tags.

`score` = number of engines that returned this result. Higher = more relevant.

## Typical agent workflows

- **General research**: `python3 scripts/search.py "topic" -n 5`
- **Find a library**: `python3 scripts/search.py "image processing python" -e github`
- **Academic papers**: `python3 scripts/search.py "attention mechanism" -c academic -n 5`
- **Tech discussions**: `python3 scripts/search.py "topic" -e hackernews,reddit`
- **AI models**: `python3 scripts/search.py "text-to-speech" -e huggingface`
- **Dev docs**: `python3 scripts/search.py "fetch API" -e mdn,stackoverflow`
- **Chinese search**: `python3 scripts/search.py "大语言模型" -l zh-CN -n 5`
- **News**: `python3 scripts/search.py "AI regulation" -c news`
