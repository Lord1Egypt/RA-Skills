---
name: tiktok-hotspot-monitor
description: >
  TikTok US women's fashion hotspot monitor. Crawls video metadata via Apify
  (primary) or Playwright (backup), analyzes trends with heat/coverage scoring,
  generates static HTML reports. Supports cost-aware 5-window crawl strategy.
type: skill
version: 2.0.0
author: Claude
repository: https://github.com/TanDongTaotao/tiktok-hotspot-monitor
trigger:
  - "Crawl TikTok hotspot data for fashion trend analysis"
  - "Analyze TikTok video metadata and generate trend report"
  - "Monitor TikTok keywords/hashtags for emerging signals"
  - "User mentions: tiktok crawler / scraper / trend monitor"
---

# TikTok Hotspot Monitor — Agent Skill

## 1. Task Boundary (Scope)

### Responsible For
- Crawling TikTok video public metadata (keyword/hashtag/creator/music sources)
  via Apify cloud Actor (`clockworks/tiktok-scraper`)
- Fallback crawling via Playwright browser automation with saved session
- Offline deduplication, heat scoring, and trend analysis
- Term extraction: content keywords and TikTok hashtags, with multi-bucket aging
- Long-term term status based on current-snapshot age distribution, not only previous-snapshot overlap
- Coverage scoring to surface "broadly appearing" signals vs "single viral" signals
- Static HTML report generation with dark theme

### NOT Responsible For
- Downloading video/audio files
- Real-time streaming or WebSocket data
- TikTok login or session management (must be pre-configured)
- Sentiment analysis of comments
- Cross-platform trend comparison
- Automated social media posting
- User authentication or authorization
- Data persistence beyond local JSONL/JSON files

### Agent Addition Scope
The agent MAY add new keyword/hashtag sources to the config. The agent MUST
NOT modify crawl window weights or add new window types without user approval,
as those affect Apify billing.

---

## 2. Input Schema

### 2.1 Main Config (`config/tiktok_hotspot_sources.json`)

```typescript
interface CrawlerConfig {
  market: string;                    // default: "US"
  output: {
    base_dir: string;                // default: "data/tiktok_hotspots"
    snapshots_dir: string;           // default: "snapshots"
    logs_dir: string;                // default: "logs"
  };
  provider: {
    type: "apify" | "tiktok_mcp";   // default: "apify"
    actor_id?: string;               // required if type=apify
  };
  defaults: {
    limit: number;                   // default: 10, per-source limit
  };
  sources: Array<{
    type: "keyword" | "hashtag" | "creator" | "music";
    value: string;
    limit?: number;                  // override defaults.limit
    enabled?: boolean;               // default: true
  }>;
  apify?: {
    token_env?: string;              // default: "APIFY_TOKEN"
    actor_id?: string;
    input: {
      defaults: Record<string, any>;
      per_source?: Record<string, any>;
      crawl_windows?: Record<string, CrawlWindow[]>;
    };
  };
  tiktok_mcp?: {
    command?: string;
    args?: string[];
    timeout_seconds?: number;
    reject_simulated?: boolean;
  };
}

interface CrawlWindow {
  name: string;
  label: string;
  weight: number;                    // allocation weight
  input: Record<string, any>;        // searchSorting, searchDatePosted, etc.
}
```

### 2.2 CLI Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--config` | Path | `config/tiktok_hotspot_sources.json` | Config file |
| `--once` | Flag | - | Run single crawl |
| `--schedule` | Flag | - | Run continuously |
| `--max-sources` | int | None | Limit enabled sources |
| `--snapshot` | Path | latest | JSONL snapshot for analysis |
| `--previous-snapshot` | Path | auto | Previous snapshot for comparison |
| `--top` | int | 10 | Items per ranked section |
| `--report` | Path | latest | Analysis JSON for rendering |

### 2.3 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `APIFY_TOKEN` | For Apify mode | Apify API token |
| `TIKTOK_PROXY` | For Playwright mode | Proxy URL |

---

## 3. Output Schema

### 3.1 Crawl Snapshot (JSONL, one record per line)

```typescript
interface CrawlRecord {
  crawl_timestamp: string;           // UTC ISO
  source_type: "keyword" | "hashtag" | "creator" | "music";
  source_value: string;
  crawl_window: string;
  crawl_window_label: string;
  crawl_window_limit: number;
  video_id: string | null;
  webpage_url: string | null;
  title: string | null;
  description: string | null;
  uploader: string | null;
  uploader_id: string | null;
  view_count: number | null;
  like_count: number | null;
  comment_count: number | null;
  share_count: number | null;
  collect_count: number | null;
  hashtags: string[] | null;
  music: {
    id: string | null;
    track: string | null;
    artist: string | null;
  };
  upload_date: string | null;        // ISO date
  duration: number | null;
  is_ad: boolean | null;
}
```

### 3.2 Crawl Log (JSONL)

```typescript
interface LogEntry {
  crawl_timestamp: string;
  source_type: string;
  source_value: string;
  crawl_window: string;
  crawl_window_limit: number;
  status: "success" | "failed";
  record_count: number;
  error: string | null;
}
```

Last entry is a `CrawlRoundSummary`:

```typescript
interface CrawlRoundSummary {
  event: "crawl_round_summary";
  crawl_timestamp: string;
  provider: string;
  enabled_source_count: number;
  crawl_window_count: number;
  planned_run_count: number;
  requested_total_limit: number;
  completed_run_count: number;
  failed_run_count: number;
  raw_record_count: number;
  unique_video_count: number;
  duplicate_rate: number;            // 0.0 - 1.0
  effective_unique_yield: number;    // unique / requested
  windows: Record<string, WindowMetrics>;
  cost_model_note: string;
}
```

### 3.3 Analysis Report (JSON)

```typescript
interface AnalysisReport {
  generated_at: string;
  snapshot_path: string;
  previous_snapshot_path: string | null;
  analysis_window: {
    current_snapshot_time: string;
    previous_snapshot_time: string | null;
    interval_hours: number | null;
    matched_previous_video_count: number;
  };
  record_count: number;
  unique_video_count: number;
  source_counts: Record<string, number>;
  top_videos: VideoItem[];
  top_rising_videos: VideoItem[];
  recent_videos_by_age: AgeBucket<VideoItem>[];
  recent_signals_by_age: SignalBucket[];
  established_terms: TermItem[];
  established_hashtags: TermItem[];
  top_music: RankedItem[];
  top_creators: RankedItem[];
  crawl_metrics: CrawlRoundSummary | null;
}
```

### 3.4 HTML Report

Self-contained static HTML file at `data/tiktok_hotspot_analysis/tiktok_hotspot_report_<timestamp>.html`.
No external dependencies. Dark themed. Machine-readable data embedded as JSON in comments.

---

## 4. Tools

### 4.1 `crawl_tiktok_hotspots.py` — Metadata Crawler

**When to call:**
- User requests data collection
- Need fresh snapshot for analysis
- Smoke test / validation run

**When NOT to call:**
- User wants to view existing data only (use analyze instead)
- No config changes made when config is invalid
- Apify mode: APIFY_TOKEN not set (check env first)
- MCP mode: session file missing (run `tiktok_login_save_session.py` first)

**Provider switching:**
Edit `config/tiktok_hotspot_sources.json` to switch between providers:

```json
// Apify mode (default, full features)
{ "provider": { "type": "apify", "actor_id": "clockworks/tiktok-scraper" } }

// Local MCP mode (limited, testing only)
{ "provider": { "type": "tiktok_mcp" } }
```

MCP mode requires:
1. `pip install playwright && playwright install chromium`
2. `python scripts/tiktok_login_save_session.py` (manual TikTok login)
3. Config `tiktok_mcp.args` pointing to `scripts/tiktok_search_mcp_adapter.py`

**Implementation:**
```python
# Provider dispatch
if config.provider_type == "apify":
    # Requires APIFY_TOKEN in env
    # Each source × window → one Actor run
    # Supports all 4 source types
elif config.provider_type == "tiktok_mcp":
    # Requires saved session file
    # Keyword/hashtag only, ~12 items per source
```

**Error states:**
| Error | Recovery |
|-------|----------|
| Apify token missing | Check env, prompt user to set APIFY_TOKEN |
| Actor run timeout | Retry with same config |
| No videos found | Log as failed window, continue |
| MCP session expired | Prompt re-login via tiktok_login_save_session.py |
| Proxy unreachable | Skip proxy or switch to Apify |
| Snapshot empty | Check sources config, ensure keywords are valid |

**Retry policy:**
- Network errors: retry up to 2 times with 5s backoff
- Actor failures: no retry (Apify handles internally), log and continue
- MCP browser crash: retry once

### 4.2 `analyze_tiktok_hotspots.py` — Offline Analyzer

**When to call:**
- After crawl completes
- User has existing snapshot to analyze
- Need updated report

**Implementation steps:**
1. Load snapshot JSONL → validate each record has `video_id`
2. Deduplicate by `video_id` (keep highest heat score)
3. Compute per-video heat score
4. Bucket videos by upload age (1d/3d/7d/14d)
5. Extract content terms and hashtags
6. Compute cross-bucket novelty (new vs existing terms)
7. Compute coverage scores
8. Compare with previous snapshot for growth metrics
9. Output structured JSON

### 4.2.1 Long-term Term Status

Long-term content terms and hashtags are **not** dropped when they are missing from the previous snapshot. A term enters the long-term section when its oldest matched video is older than 30 days. Its status is then computed from the current snapshot's video-age distribution:

| Status | Condition | Meaning |
|--------|-----------|---------|
| `spreading` | newest video <= 7 days AND recent_7d_count / video_count >= 10% | Still actively spreading |
| `mature_or_flat` | newest video <= 30 days but 7d ratio is too low | Existing signal, activity weakening |
| `cooling` | newest video > 30 days | No recent new videos; cooling down |

This avoids losing a long-term term simply because the previous crawl did not hit it, while also preventing one recent video among many old videos from falsely marking a term as spreading.



### 4.3  — HTML Report Generator

**When to call:**
- After analysis completes
- User requests visual output

**Output:** Valid HTML5, self-contained, no external CSS/JS.

### 4.4 `tiktok_login_save_session.py` — Session Setup (optional)

**When to call:**
- User wants to use local Playwright mode
- Session file missing or expired

---

## 5. State Machine

```
IDLE
  │
  ▼
CONFIG_LOAD ──invalid──▶ ERROR (report config issue)
  │
  ▼
CRAWL_PLAN
  ├─ Build requests: enabled_sources × crawl_windows
  ├─ Compute: planned_run_count, requested_total_limit
  └─ Validate: at least 1 enabled source
  │
  ▼
CRAWL_EXECUTE ──fail──▶ PARTIAL_COMPLETE (log failures, continue)
  │                       │
  ▼                       ▼
SNAPSHOT_WRITTEN       PARTIAL_SNAPSHOT
  │                       │
  └───────both────────────▶
  │
  ▼
ANALYZE ──empty_snapshot──▶ ERROR (no records to analyze)
  │
  ▼
REPORT_GENERATE ──fail──▶ ERROR (corrupted analysis JSON)
  │
  ▼
COMPLETE
```

State management is handled by the Python scripts via:
- Exit codes: 0 (success), 1 (partial failure), 2 (config/input error)
- Logs: per-run JSONL entries with status
- Summary: `CrawlRoundSummary` as last log entry

---

## 6. Error Recovery

### 6.1 Crawl Phase

| Failure Mode | Detection | Recovery |
|-------------|-----------|----------|
| Invalid config | `load_config()` raises `ValueError` | Report exact field, suggest fix |
| No enabled sources | Config load check | Add at least one source |
| Apify token missing | `os.environ.get()` returns empty | Message: "Set APIFY_TOKEN in .env" |
| All sources fail | All log entries show `failed` | Check token, network, actor_id |
| Some sources fail | Log shows mixed success/fail | Continue, report failed count |
| Snapshot empty | 0 records written | Check source keywords/limits |
| Disk full | `write()` raises `OSError` | Free disk space, retry |
| MCP browser timeout | `asyncio.wait_for` raises | Fallback to fewer sources |
| MCP session expired | Actor raises RuntimeError | Run `tiktok_login_save_session.py` |

### 6.2 Analyze Phase

| Failure Mode | Detection | Recovery |
|-------------|-----------|----------|
| Snapshot missing | `FileNotFoundError` | Run crawl first |
| Corrupted JSONL | `json.JSONDecodeError` | Check snapshot, re-crawl |
| No video records | All lines lack `video_id` | Report empty snapshot |
| Previous snapshot missing | `valid_snapshots()` empty | Run without comparison |
| Division by zero | `video_count = 0` | Guard with `max(vc, 1)` |

### 6.3 Report Phase

| Failure Mode | Detection | Recovery |
|-------------|-----------|----------|
| Analysis JSON missing | `FileNotFoundError` | Run analyze first |
| Corrupted JSON | `json.JSONDecodeError` | Re-run analyze |
| KeyError in template | `report.get(key)` missing | Graceful fallback to empty |
| Encoding error | `UnicodeEncodeError` | Force UTF-8 output |

---

## 7. Planning Logic

### 7.1 Task Decomposition

For a typical hotspot monitoring request, decompose as:

```
Step 1: Check existing data
  ├─ Is there a recent snapshot? (< 24h old)
  │   └─ Yes → skip crawl, go to Step 3
  │   └─ No → continue to Step 2
  │
Step 2: Crawl
  ├─ Validate APIFY_TOKEN exists
  ├─ Load config
  ├─ Run crawl (with timeout guard)
  └─ Verify snapshot has records
  │
Step 3: Analyze
  ├─ Auto-select latest snapshot
  ├─ Auto-select previous snapshot (if exists)
  ├─ Run analysis
  └─ Verify output JSON has all required fields
  │
Step 4: Generate report
  ├─ Render HTML from analysis JSON
  └─ Verify output is valid HTML
```

### 7.2 Decision Tree

```
User: "check TikTok trends for summer dresses"

Check: Does latest snapshot exist and have records?
├─ YES: Is it < 24h old?
│   ├─ YES: Skip crawl, go to analyze
│   └─ NO: Is user OK waiting 5-30 min for crawl?
│       ├─ YES: Run crawl, then analyze
│       └─ NO: Use existing snapshot, warn about staleness
└─ NO: Must crawl first
    ├─ Is APIFY_TOKEN configured?
    │   ├─ YES: Use Apify provider
    │   └─ NO: Check MCP session
    │       ├─ EXISTS: Use MCP provider (limited data)
    │       └─ MISSING: Ask user to configure one
    └─ Run crawl
```

---

## 8. Guardrails

### 8.1 Cost Limits

| Guardrail | Value | Enforcement |
|-----------|-------|-------------|
| Max sources per crawl | 50 | Config validation |
| Max limit per source | 500 | Config validation (`positive_int`) |
| Max requested total | 5000 | Config validation (project-level) |
| Max planned runs | 250 | 50 sources × 5 windows |
| Apify mode | Required for > 200 records | MCP limited to ~12/source |
| Report HTML size | < 5MB | Self-limiting (trim if exceeded) |

### 8.2 Time Limits

| Operation | Timeout | Enforcement |
|-----------|---------|-------------|
| Single crawl run | 60 min | Bash timeout parameter |
| Per-Apify Actor | No limit | Apify handles internally |
| Per-MCP search | 120s | `tiktok_mcp.timeout_seconds` |
| Analysis | 30s | Python processing (fast) |
| Report render | 10s | Python processing (fast) |

### 8.3 Rate Limits

- No concurrent Apify runs (sequentially dispatched)
- MCP browser: one at a time (sequential per source)
- Web fetching: 60s minimum between full re-crawls

### 8.4 Token / Credit Safety

- Never commit `.env` to git
- Never print API tokens in logs or console
- `APIFY_TOKEN` read from environment only
- MCP session file is local only

---

## 9. Evaluation Criteria

### 9.1 Crawl Success

| Criterion | Passing | Warning | Failing |
|-----------|---------|---------|---------|
| Run completion | ≥ 90% runs succeed | 70-90% | < 70% |
| Record count | ≥ 80% requested | 50-80% | < 50% |
| Duplicate rate | < 25% | 25-40% | > 40% |
| Failed windows | 0 | 1-3 | > 3 |
| Unique videos | ≥ 50 | 20-50 | < 20 |

### 9.2 Analysis Success

| Criterion | Passing | Failing |
|-----------|---------|---------|
| Snapshot has records | ≥ 10 unique videos | < 10 |
| Dedup processed | All records checked | Missing video_id |
| Term extraction | ≥ 1 content term found | 0 terms |
| JSON output | All required fields present | Missing required fields |
| Processing time | < 30s | > 60s |

### 9.3 Report Success

| Criterion | Passing | Failing |
|-----------|---------|---------|
| Valid HTML | Closes `</html>` tag | Missing closing tag |
| Metrics visible | ≥ 4 grid metrics shown | Empty grid |
| Videos rendered | Top list non-empty | Empty list |
| All sections present | 6+ sections | < 4 sections |

### 9.4 Decision: Proceed to Next Stage

After a validation crawl (target ~500 records):

```
unique_yield = unique_videos / requested_total_limit

if unique_yield >= 0.6 and duplicate_rate < 0.25:
    ✅ Proceed to pilot (2000 target)
elif unique_yield >= 0.4:
    ⚠️ Proceed with caution, review source quality
else:
    ❌ Block scaling, fix sources/windows first
```

---

## 10. Composability

### 10.1 Output Consumption

Other skills/agents consume analysis JSON via standard path:

```python
# Example: Another agent reads analysis for downstream processing
import json

report = json.load(open("data/tiktok_hotspot_analysis/latest_analysis.json"))
top_signals = [t["name"] for t in report.get("top_videos", [])[:5]]
hot_terms = [t["name"] for t in report.get("established_terms", [])[:10]]
```

### 10.2 Pipeline Integration

```
Data Source Agent
  └─► TikTok Hotspot Monitor Skill
        ├─► crawl → snapshot.jsonl
        │     └─► [External] Apify usage dashboard (cost tracking)
        ├─► analyze → analysis.json
        │     └─► [Downstream] Trend prediction / alerting
        └─► render → report.html
              └─► [Downstream] Static hosting / dashboard
```

### 10.3 File-Based Contract

All inter-skill communication is file-based:

| Artifact | Format | Schema | Consumer |
|----------|--------|--------|----------|
| Snapshot | JSONL | CrawlRecord | Analysis, ML pipeline |
| Analysis | JSON | AnalysisReport | Report, dashboards |
| Log | JSONL | LogEntry / Summary | Monitoring, cost tracking |
| Report | HTML | Self-contained | Human viewing |

### 10.4 Exit Codes

```python
# Standard exit codes for script chaining
0: Success (all operations completed)
1: Partial success (some failures, usable results)
2: Configuration error (fix config before retry)
```

---

## Appendix: Quick Reference

```bash
# Full pipeline (one command each)
python scripts/crawl_tiktok_hotspots.py --config config/tiktok_hotspot_sources.json --once
python scripts/analyze_tiktok_hotspots.py
python scripts/render_tiktok_hotspot_report.py

# Smoke test (2 sources)
python scripts/crawl_tiktok_hotspots.py --once --max-sources 2

# Validation run (500 records)
python scripts/crawl_tiktok_hotspots.py --config config/_tiktok_hotspot_apify_500_config.json --once
```

**Apify Cost Note:** Verify actual charges at console.apify.com → Usage.
Cost depends on Actor pricing, run count, compute duration, memory, proxy usage,
retries, add-ons, and account plan — not only requested result count.
