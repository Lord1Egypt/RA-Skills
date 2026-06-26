# /scry — 17-Source Research Engine for Claude Code

> Type `/scry AI agents` and get 239 items from 17 sources in 60 seconds.
> No API keys needed. No pip install. Just clone and go.

```
/scry best Claude Code skills
/scry bitcoin ETF --deep
/scry CRISPR gene editing --domain=science
/scry Taylor Swift Eras Tour
```

---

## What It Does

SCRY searches **17 sources in parallel** and returns one scored, deduplicated, cross-linked report:

| Source | API Key? | What You Get |
|--------|----------|-------------|
| Hacker News | No | Stories + top comments |
| Reddit | No | Threads + upvotes (no OpenAI key needed) |
| GitHub | No | Repos sorted by stars, not random portfolios |
| YouTube | No* | Videos with transcripts + engagement |
| ArXiv | No | Papers sorted by relevance |
| Semantic Scholar | No | Papers with citation counts |
| OpenAlex | No | Academic works + metadata |
| Bluesky | No | Posts via AT Protocol |
| Mastodon | No | Public timeline posts |
| Dev.to | No | Developer articles + reactions |
| Lobsters | No | Tech discussions |
| Stack Overflow | No | Q&A threads |
| Wikipedia | No | Current articles + revisions |
| GDELT | No | Global news events |
| SEC EDGAR | No | Financial filings (ETFs, 10-Ks) |
| Google News | No | RSS headlines |
| GitLab | No | Repos + merge requests |

**\*** YouTube requires `yt-dlp` (`brew install yt-dlp`)

### Optional Sources (need API keys)

| Source | Requires |
|--------|----------|
| X / Twitter | Browser cookies or `XAI_API_KEY` |
| CoinGecko | Free (rate-limited without key) |
| Polymarket | Free (prediction markets) |
| TikTok | `SCRAPECREATORS_API_KEY` |
| Instagram | `SCRAPECREATORS_API_KEY` |
| HuggingFace | `HF_TOKEN` |
| Product Hunt | `PRODUCTHUNT_TOKEN` |

---

## Install

### Claude Code

```bash
git clone https://github.com/Kastarter/scry.git ~/.claude/skills/scry
```

### Codex CLI

```bash
git clone https://github.com/Kastarter/scry.git ~/.agents/skills/scry
```

### Optional: YouTube + X support

```bash
# YouTube transcripts
brew install yt-dlp

# X/Twitter via xAI (optional)
mkdir -p ~/.config/scry
echo 'XAI_API_KEY=xai-...' > ~/.config/scry/.env
chmod 600 ~/.config/scry/.env
```

That's it. No `pip install`. No `npm install`. Pure Python stdlib.

---

## Usage

```
/scry [topic]                           # auto-detect domain
/scry [topic] --domain=finance          # force domain
/scry [topic] --deep                    # comprehensive mode
/scry [topic] --quick                   # fast mode
/scry [topic] --sources=github,arxiv    # specific sources only
/scry [topic] --tier=1                  # free sources only
```

### Examples

```
/scry best AI coding assistants
/scry what's happening with OpenAI
/scry rust async runtime comparison --domain=tech
/scry solana vs ethereum --domain=crypto
/scry CRISPR clinical trials --domain=science --deep
/scry SEC bitcoin ETF filings --domain=finance
```

---

## How It Works

```
/scry "bitcoin ETF"
      |
      v
  scry.py orchestrator
  ThreadPoolExecutor(16)
      |
      |--- SEC EDGAR -----> 6 ETF filings (IBIT, ARKB, BTCO...)
      |--- Reddit --------> 15 threads + upvotes
      |--- YouTube -------> 8 videos + transcripts
      |--- HN ------------> 5 discussions + comments
      |--- ArXiv ---------> 10 papers
      |--- Bluesky -------> 8 posts
      |--- 11 more... ----> ...
      |
      v
  normalize -> score -> dedupe -> cross-link -> render
      |
      v
  192 items | 14 sources | top score: 94
```

### Domain-Aware Scoring

SCRY classifies your query and adjusts source weights:

- **"bitcoin ETF"** -> finance -> SEC EDGAR boosted, TikTok deprioritized
- **"CRISPR"** -> science -> ArXiv/Semantic Scholar boosted
- **"kubernetes"** -> tech -> GitHub/HN/SO boosted

Formula: `0.45 * relevance + 0.25 * recency + 0.30 * engagement` x domain weight

### Cross-Source Intelligence

When the same topic appears on multiple platforms:

```
[91] github: kubernetes/kubernetes 121K stars [also on: HN, Reddit, DevTo]
```

Conflicts between sources are flagged automatically.

---

## vs. Other Research Tools

| | **SCRY** | last30days | WebSearch |
|---|---------|-----------|-----------|
| Sources per query | **14-17** | 1-3 | 1 |
| Items per query | **150-250** | 16-20 | ~10 |
| API keys needed | **0** | 1-3 | 0 |
| GitHub repos | Stars-sorted | -- | -- |
| Academic papers | ArXiv + S2 + OA | -- | -- |
| SEC filings | Yes | -- | -- |
| YouTube transcripts | Yes | Partial | -- |
| Domain-aware scoring | Yes | No | No |
| Cross-source links | Yes | No | No |

---

## Configuration (Optional)

Create `~/.config/scry/.env` for optional API keys:

```bash
mkdir -p ~/.config/scry
cat > ~/.config/scry/.env << 'EOF'
# X/Twitter (pick one)
XAI_API_KEY=xai-...
AUTH_TOKEN=...
CT0=...

# Social media
SCRAPECREATORS_API_KEY=...

# Dev platforms
HF_TOKEN=hf_...
PRODUCTHUNT_TOKEN=...
SO_API_KEY=...

# Search
BRAVE_API_KEY=...
EOF
chmod 600 ~/.config/scry/.env
```

None of these are required. 17 sources work without any keys.

---

## Architecture

```
scripts/
├── scry.py                    # Orchestrator (CLI, parallel search, pipeline)
├── benchmark.py               # SCRY vs last30days comparison
└── lib/
    ├── http.py                # stdlib HTTP client (urllib, retry, backoff)
    ├── dates.py               # Date parsing + recency scoring
    ├── cache.py               # File cache (~/.cache/scry/, 24h TTL)
    ├── query.py               # Core subject extraction + relevance
    ├── schema.py              # Unified ScryItem dataclass
    ├── normalize.py           # Raw dicts -> ScryItem
    ├── score.py               # Domain-aware weighted scoring
    ├── dedupe.py              # Jaccard dedup + cross-source linking
    ├── render.py              # Compact/JSON output
    ├── domain.py              # Topic classification (7 domains)
    ├── conflict.py            # Cross-source disagreement detection
    ├── source_base.py         # Abstract Source class
    ├── source_registry.py     # Auto-discovery + availability
    └── sources/               # 26 source modules
        ├── hackernews.py
        ├── reddit.py
        ├── github.py
        ├── youtube.py
        ├── arxiv.py
        └── ... (21 more)
```

### Adding a New Source

One file, ~50 lines:

```python
class MySource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="mysource", display_name="My Source",
            tier=1, emoji="\U0001f50d", id_prefix="MS",
            has_engagement=True, requires_keys=[], requires_bins=[],
            domains=["tech"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        # Your search logic here
        return [{"title": "...", "url": "...", "relevance": 0.8}]

def get_source():
    return MySource()
```

Drop it in `scripts/lib/sources/`, and SCRY auto-discovers it.

---

## Credits

- Bird X search client vendored from [@steipete/bird](https://github.com/nicosResworworkes/bird) (MIT License)
- Inspired by [/last30days](https://github.com/mvanhorn/last30days-skill) by @mvanhorn

## License

MIT
