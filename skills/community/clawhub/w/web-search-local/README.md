# web-search-local — Local Web Search Skill

Network search script without API Key, based on Bing search (with DuckDuckGo, Yandex, WebFetch as fallback engines).

## Features

- 🔍 Multi-engine Search: Bing (RSS + HTML), DuckDuckGo, Yandex, WebFetch (urllib)
- 🔄 Auto Failover: `auto` mode automatically switches engines by priority, supports automatic supplementation when results are insufficient
- 📊 Detailed Engine Logs: `auto` mode logs each engine's attempt order and result count for easy debugging
- 💾 Search Cache: Local JSON cache to reduce duplicate requests
- 📄 Multiple Output Formats: JSON (machine-readable) / Text (human-readable)
- 📁 File Output: `-o results.json` outputs to file
- ⚡ Fast Mode: `--fast` skips cookie acquisition to reduce latency
- 🕒 Metadata Timing: JSON output includes cookie/search/parse stage timing + cache_hit flag
- 🔧 Verbose Summary: `-v` mode automatically outputs detailed summary after search completion

## Installation

Dependencies (`requests` only):
```bash
pip install requests
```

## Usage

### Basic Search

```bash
python3 scripts/search.py --query "keywords"
python3 scripts/search.py -q "python tutorial" --limit 5
```

### Specify Engine

```bash
python3 scripts/search.py -q "keywords" -e bing      # Bing (default)
python3 scripts/search.py -q "keywords" -e ddg       # DuckDuckGo
python3 scripts/search.py -q "keywords" -e yandex    # Yandex
python3 scripts/search.py -q "keywords" -e webfetch  # WebFetch (urllib)
python3 scripts/search.py -q "keywords" -e auto      # Auto-switch
```

### Output Format

```bash
python3 scripts/search.py -q "keywords" -f json     # JSON format (default)
python3 scripts/search.py -q "keywords" -f text     # Human-readable text
python3 scripts/search.py -q "keywords" -o out.json # Output to file
```

### Fast Mode

```bash
python3 scripts/search.py -q "keywords" --fast  # Skip cookies, reduce latency
```

### Result Count

```bash
python3 scripts/search.py -q "keywords" --count 5  # --count is alias for --limit
```

### Cache Management

```bash
python3 scripts/search.py --cache-stats          # View cache statistics
python3 scripts/search.py --cache-clear          # Clear cache
python3 scripts/search.py --cache-ttl 300 -q ... # Custom cache TTL (seconds)
python3 scripts/search.py --no-cache -q ...      # Skip cache
```

### Search Language

```bash
python3 scripts/search.py -q "python" --lang en        # Force English results
python3 scripts/search.py -q "Python教程" --lang zh-Hans # Force Chinese results
```

### Timeout and Color Control

```bash
python3 scripts/search.py -q "keywords" --timeout 5    # 5 second timeout (default 10s)
python3 scripts/search.py -q "keywords" --no-color      # Disable ANSI colors (for piping)
python3 scripts/search.py -q "keywords" -t 15 -f text  # 15 second timeout + text output
```

### Proxy Support

```bash
python3 scripts/search.py -q "keywords" --proxy http://proxy:8080          # HTTP proxy
python3 scripts/search.py -q "keywords" --proxy socks5://proxy:1080       # SOCKS5 proxy
python3 scripts/search.py -q "keywords" --proxy http://user:pass@proxy:8080  # With authentication
```

> Note: SOCKS5 proxy requires `pip install requests[socks]`

### Result Sorting

```bash
python3 scripts/search.py -q "keywords" --sort relevance  # Sort by relevance (default)
python3 scripts/search.py -q "keywords" --sort date       # Sort by date (effective when RSS has pubDate)
```

### Debugging

```bash
python3 scripts/search.py -q "keywords" -v  # Show verbose logging (DEBUG level) + search completion summary
```

**Verbose Mode Output Example:**

```bash
python3 scripts/search.py -q "python" -e auto -v
```

```
DEBUG:Delay 2.7s
INFO:Search: python (engine=auto, limit=10)
INFO:[Auto] Trying engine 1/5: Bing RSS
INFO:[Auto] ✓ Bing RSS succeeded, got 3 results
INFO:[Auto] Insufficient results, trying to supplement...
INFO:[Auto] Supplement source: Bing HTML
INFO:[Auto] Supplement source: Yandex
INFO:[Auto] ✓ Yandex supplement succeeded, got 4 results (net increase 4 after deduplication)
INFO:[Auto] Still insufficient, trying DuckDuckGo supplement...
INFO:[Auto] ✗ DuckDuckGo failed: SSLError
INFO:[Auto] Trying engine 5/5: WebFetch
INFO:[Auto] ✓ WebFetch supplement succeeded, got 3 results (net increase 3 after deduplication)
INFO:Search completion summary:
  Query: python
  Engine: auto(bing→bing_html→yandex→webfetch)
  Results: 10
  Total time: 3.12s
  Breakdown: cookie=0.48s, search=2.60s, parse=0.04s
  Cache status: ✗ NOT HIT
============================================================
```

## Parameter Reference

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--query` | `-q` | Search keywords | (required) |
| `--limit` | `-l`, `--count` | Number of results to return | 10 |
| `--engine` | `-e` | Engine: bing/ddg/yandex/webfetch/auto | bing |
| `--format` | `-f` | Output format: json/text | json |
| `--output` | `-o` | Output to file | stdout |
| `--fast` | | Skip cookie acquisition | off |
| `--lang` | | Search language (e.g., en, zh-Hans) | — |
| `--timeout` | `-t` | Request timeout in seconds | 10 |
| `--no-color` | | Disable ANSI color codes | off |
| `--proxy` | | HTTP/SOCKS5 proxy address | — |
| `--sort` | | Result sorting: relevance/date | relevance |
| `--verbose` | `-v` | Verbose logging | off |
| `--no-cache` | | Skip cache | off |
| `--cache-ttl` | | Cache expiration in seconds | 3600 |
| `--cache-clear` | | Clear all cache | |
| `--cache-stats` | | Show cache statistics | |

## Engine Description

| Engine | Availability | Speed | Use Case |
|--------|-------------|-------|----------|
| bing | ✅ Stable | Medium | Default primary |
| webfetch | ✅ Stable | Medium | Fallback when requests unavailable |
| auto | ✅ | Slowest | Maximum coverage needed |
| ddg | ⚠️ SSL limited | — | Available in specific environments |
| yandex | ⚠️ CAPTCHA | — | Available in specific environments |

## Output Format Examples

### JSON

```json
{
  "query": "python",
  "engine": "bing",
  "count": 3,
  "results": [
    {"title": "...", "url": "...", "snippet": "..."}
  ],
  "elapsed_seconds": 0.58,
  "metadata": {
    "cookie_seconds": 0.0,
    "search_seconds": 0.519,
    "parse_seconds": 0.001
  }
}
```

`metadata` field description:
- `cookie_seconds`: Time to acquire cookie (0 in fast mode)
- `search_seconds`: Time for search request
- `parse_seconds`: Time to parse results
- `cache_hit`: `true` when cache is hit

### Text

```
Search: python
Engine: bing
Results: 3
============================================================

1. Python Official Website
   https://www.python.org/
   Welcome to Python.org...

Search time: 0.58s
  [search 0.581s, parse 0.001s]
```

## OpenClaw Integration

The skill SKILL.md defines triggers and usage, OpenClaw agent will automatically recognize search requests and invoke this skill.

## Testing

```bash
python3 -m pytest tests/test_search.py -v
```
