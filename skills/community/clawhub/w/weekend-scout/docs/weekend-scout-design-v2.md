# Weekend Scout -- Design Document (v2)

> This document describes the current state of the project as of late March 2026.
> For the history of design and contract drift, see `docs/design_changes.md`.

---

## 1. Overview

Weekend Scout is a personal tool that discovers outdoor events, festivals,
and fairs happening next weekend within driving distance of your home city.
It builds curated trip options and delivers them to a Telegram group.

The system has two parts:

1. **Python CLI** (`weekend_scout/`) -- handles all data operations: config,
   city lists, event caching, distance calculations, message formatting, and
   Telegram delivery. Every command outputs JSON for machine consumption.

2. **Agent Skill** (`skill_template/`) -- instructs an AI coding agent
   (Claude Code, Codex, or OpenClaw) to run the search/extract/rank/format
   pipeline. The agent calls the Python CLI for data and uses its built-in
   web search and fetch tools for event discovery.

**Design principle:** offload reasoning to the agent, keep the Python code
thin and deterministic. The agent decides what to search, how to interpret
results, and how to score events. Python handles infrastructure.

---

## 2. Architecture

```
User invokes /weekend-scout (or $weekend-scout on Codex)
         |
         v
    +-----------+     WebSearch / WebFetch
    |   Agent   | ------> Internet (event discovery)
    |  (Skill)  |
    +-----+-----+
          |
          | Bash: python -m weekend_scout <command> --args
          v
    +-----------+
    | Python CLI|
    +-----+-----+
          |
     +----+----+----+----+
     |    |    |    |    |
  config cities cache distance telegram
   .py   .py   .py    .py      .py
```

**Data flow per run:**

1. Agent calls `init-skill` -- CLI returns compact run context:
   config limits, city coverage, workflow task cards, and a run_id.
2. Agent searches the web using suggested queries and its own judgment.
3. After each search/fetch, agent calls `log-search` with the kept event array --
   CLI records the search and upserts canonical run-scoped candidates.
4. Before verification, agent calls `session-query` to read the canonical
   weekend candidate set for the run.
5. Agent calls `save --from-session` -- CLI finalizes/deduplicates the
   session file, exports the canonical session candidates, and saves them
   into the permanent SQLite cache.
6. Agent calls `prepare-digest` to get deterministic grouped scoring input,
   then scores events in-prompt.
7. Agent calls `format-message` with top events and trips -- CLI writes HTML file.
8. Agent calls `send` -- CLI delivers to Telegram.
9. Agent calls `cache-mark-served --date <saturday> --run-id <run_id>` -- CLI marks events as sent.

---

## 3. Dependencies

| Package       | Purpose                              |
|---------------|--------------------------------------|
| `pyyaml`      | Config file read/write               |
| `requests`    | Telegram Bot API, GeoNames download  |
| `pytest`      | Test framework (dev dependency only)  |

No search APIs, no routing APIs, no LLM libraries. SQLite is built into
Python's standard library.

---

## 4. Component Design

### 4.1 Configuration (`config.py`)

Config is stored as YAML in the repo-local state directory:

- `.weekend_scout/config.yaml`

Cache files, logs, the SQLite DB, and GeoNames data live under:

- `.weekend_scout/cache/`

**Default configuration:**

```yaml
home_city: ""
home_country: ""
home_coordinates:
  lat: 0.0          # 0,0 is the "unset" sentinel
  lon: 0.0
radius_km: 150
search_language: "en"
max_city_options: 3
max_trip_options: 10
output_language: "en"
telegram_bot_token: ""
telegram_chat_id: ""
auto_run: false
run_day: "friday"
run_time: "18:00"
max_searches: 15
max_fetches: 15
```

`max_fetches` is the discovery fetch budget for Phases A-C. Phase D uses a
separate fixed validation reserve of 5 fetches.

**`load_config`** merges stored YAML over defaults (stored values win).
This means new config keys added in upgrades get their defaults automatically.

**Country and language maps:** `config.py` contains two dicts that drive
auto-detection during setup:

- `COUNTRY_CODE_MAP`: ISO 3166-1 alpha-2 to full country name (36 countries)
- `COUNTRY_LANGUAGE_MAP`: full country name to 2-letter search language code

Supported: PL, US, CA, GB, IE, AU, NZ, SG, JP, KR, DE, FR, CZ, SK, AT,
HU, UA, LT, LV, EE, BY, IT, ES, PT, NL, SE, NO, DK, FI, RO, HR, BG, RS,
GR, TR, RU.

### 4.2 City List and GeoNames (`cities.py`)

**Data source:** GeoNames `cities15000.txt` -- a free downloadable file
containing all cities worldwide with population above 15,000.

- **Storage:** Downloaded to `<config_dir>/cache/geonames/cities15000.txt` (~24 MB)
- **Auto-download:** `ensure_geonames()` downloads automatically on first use
  if the file is missing. The `download-data` CLI command allows explicit
  pre-download.
- **Parsing:** `parse_geonames_file()` reads the tab-separated file, skipping
  `PPLX` entries (city districts). Returns dicts with: name, name_local, lat,
  lon, population, country, feature_code, admin2, admin3.

**City list generation (`get_city_list`):**

1. Computes Haversine distance from home coordinates to every city in the file.
2. Filters to cities within `radius_km`, excluding the home city itself (< 2 km).
3. Filters out home-city districts: PPL-coded entries within 15 km that share
   admin2/admin3 codes with the home city. This handles Warsaw boroughs,
   Brussels communes, Madrid districts, etc. that GeoNames incorrectly tags
   as standalone cities.
4. Assigns tiers by population:

   | Tier | Population     | Search strategy                              |
   |------|----------------|----------------------------------------------|
   | 1    | 100,000+       | Always searched individually (Phase C)       |
   | 2    | 30,000-99,999  | Searched individually if budget allows        |
   | 3    | 15,000-29,999  | Covered by regional queries only              |

5. Caches the result as `<config_dir>/cache/cities_<home>_<radius>.json`.
   Invalidated when home_city, coordinates, or radius change.

**Region mapping (`regions.py`):**

A Python module containing a `REGIONS` dict that maps city names to regional
names for search query generation (e.g., "Warsaw" to "Mazowsze", "Berlin" to
"Brandenburg"). Covers representative major cities across all supported
countries in both English and native names. The `get_region()` function does a
case-insensitive lookup, falling back to the city name itself.

**Query generation:**

`generate_broad_queries()` returns 4 template strings using the configured
search language. Each template has `{placeholders}` that the agent fills
using variables provided by `init`:

```python
# Example for Polish:
[
    "imprezy plenerowe weekend {date} {region}",
    "festiwale jarmarki okolice {city} {month} {year}",
    "festyny wydarzenia weekend {month} {year} {country}",
    "outdoor events weekend {date} {country}",  # English fallback
]
```

`generate_targeted_template()` returns a single template for per-city
searches: `"{city} events {date}"` (language-specific).

**Date formatting:** `format_date_local()` formats ISO dates for the full
supported-country set, including dedicated Japanese/Korean forms such as
`"2026年4月10日"` and `"2026년 4월 10일"`, alongside existing European
day-first/month-first layouts such as `"28 marca 2026"` and `"March 28, 2026"`.

**City lookup:** `find_city_candidates()` searches the GeoNames file for a
city name (case-insensitive, checks both ASCII and native names), limited to
supported countries, deduplicated by country (highest population wins).
Returns one match per country for disambiguation.

### 4.3 Distance Calculations (`distance.py`)

**Haversine formula:** `haversine_km(lat1, lon1, lat2, lon2)` returns
great-circle distance in kilometres.

**Driving time heuristic:** `estimated_drive_minutes(distance_km)` uses
a three-tier model calibrated for Poland/Central Europe:

| Distance     | Avg Speed | Multiplier |
|-------------|-----------|------------|
| < 30 km     | ~40 km/h  | 1.5 min/km |
| 30-80 km    | ~60 km/h  | 1.0 min/km |
| > 80 km     | ~80 km/h  | 0.75 min/km|

No routing API needed. Accurate enough for "about 1h45" estimates.

**Next weekend dates:** `next_weekend_dates()` returns the ISO dates of the
upcoming Saturday and Sunday. If today is Saturday, it skips to next week.

### 4.4 Event Cache (`cache.py`, `session_cache.py`)

**Database:** SQLite at `<config_dir>/cache/cache.db`.

**Events table:**

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT DEFAULT '',
    start_date TEXT NOT NULL,       -- ISO date
    end_date TEXT,                  -- nullable if single-day
    time_info TEXT,                 -- free text: '10:00-18:00'
    location_name TEXT,
    lat REAL,
    lon REAL,
    category TEXT,
    description TEXT,
    free_entry BOOLEAN,
    source_url TEXT,
    source_name TEXT,
    discovered_date TEXT NOT NULL,
    confidence TEXT DEFAULT 'likely',
    served BOOLEAN DEFAULT 0,
    canceled BOOLEAN DEFAULT 0,
    dedup_key TEXT UNIQUE
);
```

**Deduplication:** `dedup_key = normalize(event_name) + "_" + normalize(city) + "_" + start_date`.
Normalization strips non-word characters and lowercases.

- In the permanent DB, exact `dedup_key` collisions are merged in place:
  missing `country`, `time_info`, `location_name`, `source_url`,
  `source_name`, and `description` are backfilled, and `confidence`
  is upgraded when the incoming row is stronger.
- Fuzzy/alias deduplication does **not** happen in SQLite. It happens in the
  run session layer before save.

**Search log table:**

```sql
CREATE TABLE search_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    search_date TEXT NOT NULL,
    target_weekend TEXT NOT NULL,
    result_count INTEGER DEFAULT 0,
    cities_covered TEXT,            -- JSON array
    phase TEXT,
    run_id TEXT,
    events_discovered INTEGER DEFAULT 0
);
```

**Action log:** `log_action()` appends structured JSONL entries to
`<config_dir>/cache/action_log.jsonl` with fields: timestamp, action, phase,
run_id, source, target_weekend, detail. Used for debugging agent behavior
and analyzing search efficiency.

**Run session store:** `session_cache.py` maintains run-scoped canonical
candidate files under `<config_dir>/cache/runs/<run_id>.candidates.json`.
Each file stores:

- `run_id`
- `target_weekend` (ISO Saturday)
- `updated_at`
- `candidates` (canonical event-schema rows for the run)

This session store is the authoritative discovery-state handoff between
search phases. It keeps future/off-weekend discoveries for later permanent
cache save, while `session-query` filters to the run's target weekend.
Candidates are canonicalized on write and on read:

- missing `country` is filled from `home_city -> home_country`, nearby-city
  metadata, or a safe single GeoNames match
- same-city same-weekend aliases are conservatively auto-merged by exact
  name/date, shared source URL, or strong normalized-name containment
- stronger/confirmed rows override weaker date/time/location/source fields

**Key operations:**

- `save_events(config, events)` -- inserts events, returns (saved, skipped) counts
- `query_events(config, saturday)` -- returns all non-canceled events for the
  weekend (Saturday and Sunday), using `start_date <= sunday AND end_date >= saturday`
- `log_search(...)` -- records a search in SQLite, writes to action log, and
  optionally upserts canonical candidates into the run session
- `query_session_candidates(config, run_id)` -- returns canonical session
  candidates overlapping the run's target weekend
- `export_session_candidates(config, run_id)` -- returns all canonical session
  candidates for final `save --from-session`
- `prepare-digest --date X` -- reads saved weekend cache rows and returns
  deterministic `home_city_candidates`, grouped `trip_city_groups` (with all
  canonical city events sorted best-first), and pool summary counts for Step 3
- `get_searches_this_week(config, saturday)` -- returns query strings already
  run for this target weekend (used for dedup in the skill)
- `mark_served(config, saturday)` -- sets `served=1` on all events for the weekend

### 4.5 Telegram Sender (`telegram.py`)

**Formatting:** HTML parse_mode. Only `<`, `>`, `&` need escaping via
`html.escape()`. Supports `<b>`, `<i>`, `<a href="...">`.

**Message structure:**

```
🗓 Weekend Scout | March 28-29, 2026

🏙 In Warsaw

1. <b>Event Name</b>
   📍 Location name
   🗓 Sat 10:00-18:00 • ✅ Free entrance
   Description text
   🔗 Details

🚗 Road Trips

01. <b>Trip Name</b>
   📍 City (130 km, ~1h45)
   🎉 Event details
   🕒 Leave by: 10:00 | Back by: ~20:00
   🔗 Details

✨ Scouted by Weekend Scout
```

- Home city events: up to `max_city_options`
- Road trips: up to `max_trip_options`
- Low-results hint: appended when `total_events < 3`, suggesting the user
  increase `max_searches` and `max_fetches`

**Message splitting:** `split_message()` breaks messages longer than 4096
characters (Telegram's limit) at paragraph boundaries (`\n\n`), falling back
to line breaks (`\n`), then hard-splitting as a last resort.

**Sending:** `send_telegram()` uses `requests.post` to the Bot API with
`disable_web_page_preview: True` and a 30-second timeout. It returns a
structured result dict (`sent`, `reason`, `error_code`, `status_code`,
`error`, `parts_sent`) and never raises.

### 4.6 Search Query Generation (`cities.py`)

Queries are generated in the user's configured `search_language`. Each
supported language has:

- `MONTHS` dict: localized month names (genitive/nominative as appropriate)
- `QUERY_TEMPLATES` dict: 3 broad templates + 1 targeted template per language
- `format_date_local()`: locale-aware date formatting

Date format variants:
- Period-first: `"28. Marz 2026"` (de, no, da, hr, sr)
- Day-first: `"28 marca 2026"` (pl, fr, cs, sk, hu, uk, lt, lv, et, be, it, es, pt, nl, sv, fi, ro, bg, el, tr, ru)
- Month-first: `"March 28, 2026"` (en, fallback)

The `init` command returns query templates with placeholder variables (`{city}`,
`{date}`, `{region}`, `{month}`, `{year}`, `{country}`) and a `vars` dict
for the agent to fill them.

---

## 5. Agent Skill Definition

### 5.1 Multi-Platform Architecture

The skill follows the Agent Skills open standard (agentskills.io). A single
template generates platform-specific SKILL.md files for three platforms:

| Platform    | Project skills dir          | Global skills dir               | Invoke command     |
|-------------|-----------------------------|----------------------------------|--------------------|
| Claude Code | `.claude/skills/<name>/`    | `~/.claude/skills/<name>/`      | `/weekend-scout`   |
| Codex       | `.agents/skills/<name>/`    | `~/.agents/skills/<name>/`      | `$weekend-scout`   |
| OpenClaw    | `<workspace>/skills/<name>/`| `~/.openclaw/skills/<name>/`    | `weekend-scout`    |

**Template system (`skill_template/`):**

- `weekend-scout.template.md` -- single source of truth for all platforms
- `platforms.yaml` -- per-platform variables and output paths
- `generate.py` -- preprocessor using `#@IF platform` / `#@ENDIF` directives
  and `%%VAR%%` substitution

Platform-specific differences in the generated SKILL.md:

| Feature              | Claude Code                  | Codex                             | OpenClaw                         |
|----------------------|------------------------------|-----------------------------------|----------------------------------|
| Model                | `model: haiku` (enforced)    | Advisory in `metadata` block      | Advisory in `metadata.openclaw`  |
| Auto-invoke disable  | `disable-model-invocation: true` | `agents/openai.yaml` policy   | Config-level                     |
| Tool restrictions    | `allowed-tools: Bash, Read, Write, WebSearch, WebFetch` | Not in SKILL.md    | Not in SKILL.md                  |
| Extra files          | None                         | `agents/openai.yaml`              | None                             |

Generated files are committed to git so the repo works on clone. The generator
also mirrors outputs to `weekend_scout/skill_data/` so they are included in
the pip-installed package (for the `install-skill` CLI command).

### 5.2 Skill Workflow (6 Steps)

The skill uses `disable-model-invocation: true` (Claude Code) / equivalent on
other platforms because it has side effects (web searching, Telegram sending).
User must explicitly invoke it.

**Step 1: Initialize**

```bash
python -m weekend_scout init-skill [--city <name>] [--radius <km>]
```

The shipped skill extracts from the JSON response:
- `config.target_weekend.saturday`, `config.target_weekend.sunday`
- `config.home_city`
- `config.max_city_options`, `config.max_trip_options`
- `config.max_searches`, `config.max_fetches`
- `cities.tier1`
- `cities.tier2_count`, `cities.tier3_count`
- `cached.count`, `cached.covered_cities`, `cached.city_counts`
- `run_id`
- `workflow` (`phase_a`, `phase_c`, `phase_d`, `audit_command`)

`init` remains available for manual inspection/debugging. It mirrors the same
top-level runtime shape but includes an expanded `debug` block with full cached
rows, query templates, and later-tier city cards.

**Onboarding guard:** If `needs_setup: true`, the skill runs an in-chat
setup flow: asks for city and radius, calls `find-city` to geocode, handles
multi-country disambiguation, then calls `setup --json` to persist. No
separate terminal needed.

If the skill is invoked with `--cached-only`, that flag belongs to the skill
invocation itself. The Python startup commands remain `init-skill` / `init`
without a `--cached-only` CLI flag.

**Step 2: Search for Events (4 phases)**

Budget: `max_searches` WebSearch calls + `max_fetches` discovery WebFetch
calls for Phases A-C (configurable, default 15/15). Phase D gets a separate
fixed validation reserve of 5 fetches. Bash CLI calls are free.

Budget allocation guidance:

```
Phase A  (broad)     : up to 5 searches + up to 6 discovery fetches
Phase B  (aggregators): counts against the 6 fetch slots above
Phase C  (per-city)  : up to 2 searches + 1 discovery fetch per uncovered tier1 city
                       deterministic later-tier sweep: tier2 first, then tier3,
                       until the main search budget is exhausted or the tier is exhausted
Phase D  (verification): up to 5 validation fetches from a fixed reserve
```

Phase A -- Broad sweep: run the prefilled `workflow.phase_a` WebSearch queries,
extract events from titles, and queue aggregator URLs for Phase B.

Phase B -- Aggregator deep-dive: fetch queued aggregator URLs, extract all
outdoor events from the page content.

Phase C -- Targeted per-city: use `workflow.phase_c.tier1` cards first, then
request later-tier batches on demand via `phase-c-cities`. Priority is strict
and deterministic: tier1 first, then tier2, then tier3, continuing later tiers
until the main search budget is exhausted or there are no more later-tier city
cards to request. On same-week reruns, tier1 cards explicitly expose
`still_uncovered`, `retry_on_rerun`, and `retry_query`, so a city like Potsdam
remains actionable even when its original base query is already in the weekly
done-query set.

Phase D -- Verification: call `session-query` to load the canonical weekend
candidate set, then use the separate fixed validation reserve on the top 5
candidate events to fetch official sources and confirm dates/details. Updates
are merged back into the run session and can correct weekend date/time fields
without creating duplicates.

Each search/fetch is logged via `log-search` with phase, query, result count,
and the action-local event array. The CLI computes authoritative
`events_discovered` counts from session upserts and returns
`duplicates_merged` when the kept payload matched an existing candidate.

All discovered events (including future-weekend finds noticed along the way)
are saved via a single `save --from-session` call at the end of Step 2. That
save finalizes the session file so `<run_id>.candidates.json` ends the run in a
deduplicated canonical form.

**Step 3: Score and Rank**

The agent scores each event 1-10 using these criteria (applied in-prompt, not
via Python):

| Factor                              | Points |
|-------------------------------------|--------|
| Category match (festival/fair = high)| 0-3   |
| Scale (city-wide = high)            | 0-2    |
| Uniqueness (annual = high)          | 0-2    |
| Confidence (confirmed=1, likely=0.5)| 0-1    |
| Free entry                          | 0-1    |
| Source quality (official=1)         | 0-1    |

Pool: `prepare-digest` output from the saved weekend cache.
Step 3 uses that helper output as its working set; raw cached rows are not
carried forward after the helper runs.
Select: up to `max_city_options` home-city events and up to
`max_trip_options` road trip options (tier1 cities first).
The helper owns objective dedupe and per-city grouping; the agent keeps the
final ranking and wording.

**Step 4: Build Trip Options**

Build up to `max_trip_options` trips, one per city with confirmed events,
with final labels rendered as `01..NN`.

Each trip dict:
```json
{
    "name":   "City Day Trip",
    "route":  "City (X km, ~Yh)",
    "events": "Event Name | Venue | Day Time",
    "timing": "Leave by: HH:MM | Back by: ~HH:MM",
    "url":    "https://..."
}
```

"Leave by" formula: `event_start + 1h30 - drive_time`, minimum 09:00.

**Step 5: Format and Send**

```bash
python -m weekend_scout format-message \
    --saturday <date> --sunday <date> \
    --city-events '<json>' --trips '<json>' \
    [--low-results true]
python -m weekend_scout send --file <path>
```

The message is always displayed to the user in-chat. If Telegram is not
configured, the skill shows setup commands. If `total_events < 3`, the
`--low-results true` flag appends a hint to increase `max_searches` and
`max_fetches`.

**Step 6: Mark Served and Report**

If send succeeded, mark events as served and log run completion:

```bash
python -m weekend_scout cache-mark-served --date "<saturday>" --run-id "<run_id>"
```

Report to user:
- Events found (new vs cached)
- Discovery budget used (`searches_used/max_searches`, `fetches_used/max_fetches`)
- Validation budget used (`validation_fetches_used/validation_fetch_limit`)
- Any tier1 cities with zero coverage

### 5.3 Event Inclusion and Exclusion Criteria

**Include:**
- Open-air festivals (music, food, craft, cultural)
- City Days (Dni Miasta), town celebrations
- Large fairs and markets (jarmark, kiermasz)
- Historical reenactments, outdoor spectacles
- Street art and performer festivals
- Food truck rallies, beer/wine festivals
- Outdoor concerts, open-air cinema
- Large sporting events with public attendance

**Exclude:**
- Museum openings, gallery exhibitions
- Indoor theater, cinema, opera, conferences
- Small recurring weekly farmers markets
- Private corporate events
- Ticketed indoor concerts
- Religious services (but religious festivals/processions are OK)

---

## 6. Project File Structure

```
Weekend-Scout/
    CLAUDE.md                              Project guide for Claude Code
    README.md                              User-facing documentation
    SKILL.md                               Repo-root bundle bootstrap/dispatcher entrypoint
    LICENSE                                MIT
    pyproject.toml                         Package metadata and dependencies

    weekend_scout/                         Python package
        __init__.py
        __main__.py                        CLI entry point (argparse subcommands)
        config.py                          YAML config, setup wizard, country maps
        cities.py                          GeoNames parsing, city lists, query generation
        distance.py                        Haversine, drive time, next_weekend_dates
        cache.py                           SQLite events + search log + JSONL action log
        session_cache.py                   Run-scoped candidate session files
        telegram.py                        HTML formatting, message splitting, Bot API
        regions.py                         City-to-region mapping (~200 entries)
        skill_data/                        Bundled skill files for install-skill command
            __init__.py
            claude-code/SKILL.md
            codex/SKILL.md
            codex/agents/openai.yaml
            openclaw/SKILL.md

    skill_template/                        Skill generator (source of truth)
        weekend-scout.template.md          Template with #@IF directives
        platforms.yaml                     Platform configs and variables
        generate.py                        Generator script
        README.md                          Generator documentation

    .claude/                               Claude Code project-scoped skill + settings
        skills/weekend-scout/SKILL.md      Generated
        skills/review/SKILL.md             Code review skill
        settings.json                      Permissions and hooks
        settings.local.json                Local overrides
        compaction-notes.md                Post-compaction context

    .agents/                               Codex project-scoped skill
        skills/weekend-scout/SKILL.md      Generated
        skills/weekend-scout/agents/openai.yaml

    .openclaw/                             OpenClaw project-scoped skill
        skills/weekend-scout/SKILL.md      Generated

    install/                               Installation helpers
        install_skill.py                   Cross-platform installer
        README.md                          Per-platform install instructions

    tests/                                 Test suite
        test_config.py
        test_cities.py
        test_distance.py
        test_cache.py
        test_telegram.py
        test_main.py
        test_regions.py
        test_session_cache.py

    docs/                                  Documentation
        weekend-scout-design-v2.md         This document
        design_changes.md                  Historical drift log
        backlog.md                         Task tracking
        platform-skill-reference.md        Platform research reference
```

---

## 7. CLI Command Reference

All commands output JSON to stdout. Diagnostic messages go to stderr.

| Command | Purpose | Key arguments |
|---------|---------|---------------|
| `setup` | Interactive setup wizard or JSON config apply | `--json '{...}'` |
| `config` | Show/set config values | `[key] [value]` |
| `init` | Load runtime run context plus expanded debug inspection data | `--city`, `--radius` |
| `init-skill` | Load compact agent-facing run context | `--city`, `--radius` |
| `find-city` | Look up a city in GeoNames | `--name`, `--country` |
| `save` | Save discovered events to cache | `--events '<json>'`, `--events-file`, `--from-session`, `--run-id` |
| `send` | Send message to Telegram | `--file` or `--message` |
| `cache-query` | Query cached events for a weekend | `--date` |
| `session-query` | Query canonical run-session candidates for the target weekend | `--run-id` |
| `prepare-digest` | Build deterministic grouped scoring input from saved weekend cache rows | `--date` |
| `log-search` | Record a web search in the log and optionally persist kept candidates | `--query`, `--target-weekend`, `--phase`, `--run-id`, `--events-file` |
| `log-action` | Append to action_log.jsonl | `--action`, `--phase`, `--detail`, `--run-id` |
| `phase-c-cities` | Load the next later-tier targeted-search batch | `--run-id`, `--tier`, `--offset`, `--limit` |
| `phase-summary` | Log one canonical discovery-phase summary | `--run-id`, `--phase`, `--target-weekend` |
| `score-summary` | Log one canonical ranking summary | `--run-id`, `--target-weekend`, `--total-pool` |
| `run-complete` | Log the canonical final run summary | `--run-id`, `--target-weekend`, `--events-sent` |
| `audit-run` | Audit one logged scout run by `run_id` | `--run-id`, `--strict` |
| `cache-mark-served` | Mark weekend events as sent | `--date`, `--run-id` |
| `format-message` | Format scout message to file | `--saturday`, `--sunday`, `--city-events`, `--trips`, `--low-results` |
| `install-skill` | Copy skill to global skills dir | `--platform` |
| `download-data` | Download GeoNames cities15000.zip | `--force` |
| `run` | Print manual run instructions | |

---

## 8. Installation

### End users

```bash
git clone https://github.com/goooroooX/Weekend-Scout.git
cd Weekend-Scout
python install/install_skill.py --with-pip
```

This runs `pip install .` (non-editable, copies to site-packages), copies
the SKILL.md to the user's global skills directory, and downloads GeoNames
data. The cloned folder can be safely deleted afterward.

### Developers

```bash
git clone https://github.com/goooroooX/Weekend-Scout.git
cd Weekend-Scout
pip install -e ".[dev]"
```

Editable install -- the skill loads from `.claude/skills/` in the repo
(project-scoped). Do not delete the repo folder.

### Updating the skill template

After editing `skill_template/weekend-scout.template.md`:

```bash
python skill_template/generate.py
```

This regenerates all platform SKILL.md files (in `.claude/`, `.agents/`,
`.openclaw/`, and `weekend_scout/skill_data/`). Test with `/weekend-scout`
in Claude Code and `$weekend-scout` in Codex, then commit all generated files.

---

## 9. Example: Full Run Walkthrough

User types `/weekend-scout` in Claude Code on Thursday evening.

**1. Agent runs `init-skill`:**

```json
{
    "config": {
        "home_city": "Warsaw",
        "radius_km": 150,
        "max_city_options": 3,
        "max_trip_options": 10,
        "max_searches": 15,
        "max_fetches": 15,
        "target_weekend": {"saturday": "2026-04-04", "sunday": "2026-04-05"}
    },
    "cities": {
        "tier1": ["Lodz|PL", "Radom|PL", "Lublin|PL"],
        "tier2_count": 3,
        "tier3_count": 2
    },
    "cached": {"count": 0, "covered_cities": [], "city_counts": {}},
    "run_id": "2026-04-04_1830",
    "workflow": {
        "phase_a": {
            "queries": [{"query": "imprezy plenerowe weekend 4 kwietnia 2026 Mazowsze", "query_already_done": false}]
        },
        "phase_c": {
            "tier1": [{"city_name": "Lodz", "query": "Lodz wydarzenia 4 kwietnia 2026", "query_already_done": false, "still_uncovered": true, "retry_on_rerun": false, "retry_query": "Lodz wydarzenia 4 kwietnia 2026 festyn jarmark festiwal plener weekend"}],
            "tier2_request": {"request_command": "python -m weekend_scout phase-c-cities --run-id \"2026-04-04_1830\" --tier 2 --offset 0 --limit 6"}
        },
        "phase_d": {
            "session_query_command": "python -m weekend_scout session-query --run-id \"2026-04-04_1830\"",
            "prepare_digest_command": "python -m weekend_scout prepare-digest --date \"2026-04-04\"",
            "validation_fetch_limit": 5
        }
    }
}
```

**2. Phase A -- Broad sweep (4 searches):**

Agent runs the prefilled Phase A queries. Finds aggregator URLs
and direct event titles. Queues 3 aggregator URLs for Phase B.

**3. Phase B -- Aggregator fetch (3 fetches):**

Agent fetches aggregator pages, extracts structured event data.
Discovers 8 events across Warsaw and nearby cities.

**4. Phase C -- Targeted per-city (3 searches):**

Radom and Lublin have zero events. Agent runs targeted searches.
Finds 2 more events.

**5. Phase D -- Verification (2 validation fetches):**

Agent verifies top 5 events by fetching official sources.
Updates 4 events to `confidence: "confirmed"`.

**6. Save all events:**

```bash
python -m weekend_scout save --run-id "2026-04-04_1830" --from-session
# -> {"saved": 10, "skipped": 0}
```

**7. Score, rank, format, send:**

Agent scores events, selects up to `max_city_options` home-city picks and
4 road trips.
Formats message, sends to Telegram, marks served.

Budget used: 10/15 searches, 2/15 discovery fetches, 5/5 validation fetches.

---

## 10. Supported Countries

36 supported countries with country-specific search profiles:

Poland, United States, Canada, United Kingdom, Ireland, Australia, New Zealand,
Singapore, Japan, South Korea, Germany, France, Czech Republic, Slovakia,
Austria, Hungary, Ukraine, Lithuania, Latvia, Estonia, Belarus, Italy, Spain,
Portugal, Netherlands, Sweden, Norway, Denmark, Finland, Romania, Croatia,
Bulgaria, Serbia, Greece, Turkey, Russia.

Japan and South Korea use dedicated native-language search queries and date
formatting. English-language queries are used intentionally for the United
States, Canada, United Kingdom, Ireland, Australia, New Zealand, and Singapore,
and remain the fallback for any other location.

---

## 11. Key Design Decisions

**No third-party search APIs.** Uses the agent's built-in WebSearch/WebFetch
tools. No SerpAPI, no AllEvents API, no API keys to manage or revoke.

**No routing API.** Haversine + heuristic driving time. Good enough for day
trip planning. Avoids Google Maps API dependency and costs.

**Agent-side reasoning.** Event scoring, trip building, and search strategy
are all in the skill prompt, not in Python code. This makes iteration fast
(edit the template, regenerate, test) without touching the Python package.

**SQLite event cache.** Future-weekend events discovered along the way are
cached. Over weeks of use, the cache pre-fills and reduces the search budget
needed. `searches_this_week` dedup prevents repeating queries.

**Configurable budgets.** `max_searches` and `max_fetches` are in the config
file for main discovery work, not hardcoded in the skill. Users can increase
them if results are thin, or decrease to save tokens. Phase D verification uses
a separate fixed 5-fetch reserve so validation does not consume the discovery
fetch budget.

**Multi-platform from one template.** The `#@IF` / `%%VAR%%` preprocessor
generates platform-specific SKILL.md files from a single source. Adding a new
platform requires only a `platforms.yaml` entry and any `#@IF` blocks needed.

**HTML for Telegram.** Switched from MarkdownV2 (which requires escaping 18
special characters) to HTML (which requires escaping only 3). Eliminated
`Bad Request: can't parse entities` errors with Polish event names.

---

## 12. Future Enhancements

- **Cron/scheduled execution:** Use Claude Code SDK or `claude --message` for
  automatic Thursday evening runs.
- **PyPI publishing:** `pip install weekend-scout` for simpler end-user install.
- **Scoring iteration:** Tune the scoring rubric based on real run data.
- **Multi-city trips:** Build loop routes through 2-3 nearby cities.
- **Cache analytics:** Dashboard showing search efficiency over time from
  the JSONL action log.
- **Cross-platform testing:** Extend end-to-end validation to OpenClaw and
  broader platform matrices. Claude Code and Codex are already covered.
