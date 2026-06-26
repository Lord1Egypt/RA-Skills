# Weekend Scout

A Python CLI + Agent Skill that discovers outdoor events, festivals, and
fairs happening next weekend near your city. Builds curated trip options
and delivers them to Telegram.

<p align="center">
  <img src="docs/images/weekend-scout-overview.png" alt="Weekend Scout overview with sample Telegram digest and core features" width="700">
</p>

## Important

Weekend Scout is **not** a standalone app. It must run inside at least one
supported agentic platform, because the skill relies on the agent's chat flow
and built-in web search/fetch tools. Install one of the supported platforms
below first, then install Weekend Scout into that platform.

## Supported Platforms

- **Claude Code** 
- **OpenAI Codex** 
- **OpenClaw** 
- Other Agent Skills platforms may be possible with manual adaptation, but the
  repo currently ships and validates built-in support for Claude Code, Codex,
  and OpenClaw.

## Installation

### For users

Recommended bootstrap install:

```bash
git clone https://github.com/goooroooX/Weekend-Scout.git
cd Weekend-Scout
python install/install_skill.py --with-pip
cd ..
```

The package is now installed for this Python interpreter. You can safely delete the
`Weekend-Scout/` folder after installation.
The installed skill is bound to the exact Python interpreter that ran the
installer, so later skill runs use the same environment that contains
`weekend-scout` and its dependencies.
If `pip` is missing for that interpreter, the installer first tries the stdlib
`ensurepip` bootstrap before showing platform-appropriate manual recovery
guidance: distro package-manager suggestions on Linux, and Python
repair/reinstall guidance on Windows.
On Linux systems with externally managed Python (PEP 668), prefer the scoped
one-shot override:

```bash
python install/install_skill.py --with-pip --break-system-packages
```

An optional persistent workaround is:

```bash
pip config set global.break-system-packages true
```

Prefer the installer flag first, because it affects only this install command.

### For developers

```bash
git clone https://github.com/goooroooX/Weekend-Scout.git
cd Weekend-Scout
pip install -e ".[dev]"
```

Claude Code and OpenAI Codex auto-discover the project-scoped skill from
`.claude/skills/weekend-scout/` and `.agents/skills/weekend-scout/`.
Do not delete those folders.

If you want a global skill install after `pip install -e ".[dev]"`, prefer:

```bash
python -m weekend_scout install-skill --platform <claude-code|codex|openclaw|all>
```

The repo installer without `--with-pip` is an advanced copy-only path and
assumes that same Python interpreter already has `weekend-scout` installed.

See [install/README.md](install/README.md) for platform-specific install details.

## Quick Start

Just invoke the skill — no manual configuration needed:

```
/weekend-scout            # Claude Code
$weekend-scout            # Codex
/weekend-scout            # OpenClaw, invocation via Telegram
/weekend-scout --reset    # ask for confirmation, then clear config + cache
```

On first run the skill will ask for your city and search radius, look up
the coordinates automatically, and save everything to config. Then it
searches the web for outdoor events happening next weekend near you,
scores and ranks them, builds road trip options for nearby cities, and
presents the digest right in chat.

Once that works, you can optionally [set up Telegram](#telegram-setup)
to receive the digest as a message instead of reading it in chat.
If you use OpenClaw, you do **not** need this Telegram setup for normal skill
usage, because OpenClaw delivers the final digest through its own channel flow.

## Updating

```bash
# Users: re-clone and re-run the installer
git clone https://github.com/goooroooX/Weekend-Scout.git
cd Weekend-Scout
python install/install_skill.py --with-pip

# Developers: pull in your existing clone
git pull
pip install -e ".[dev]"
```

## Uninstalling

```bash
python install/install_skill.py --uninstall
```

Examples:

```bash
# Remove all detected installed skill folders plus the package from this interpreter
python install/install_skill.py --uninstall

# Remove only one platform's skill folder plus the package
python install/install_skill.py --uninstall --platform openclaw

# Externally managed Python uninstall
python install/install_skill.py --uninstall --break-system-packages
```

This removes the installed skill files and uninstalls the `weekend-scout`
package from the same Python interpreter. It does **not** remove
`.weekend_scout/` config, cache, logs, or downloaded data.

To return to the unconfigured state without uninstalling the package, use:

```bash
python -m weekend_scout reset --yes
```

That deletes `.weekend_scout/config.yaml` and `.weekend_scout/cache/` for the
active install. The skill shortcut `/weekend-scout --reset` performs the same
reset flow after asking for confirmation.

## How It Works

Weekend Scout has two parts:

1. **Python CLI** (`weekend_scout/`) — handles config, city data, caching,
   distance calculations, and Telegram delivery
2. **Agent Skill** (SKILL.md) — instructs the AI agent to search for events,
   extract and score them, build trip options, and format output

The skill calls the CLI for data operations and uses the agent's built-in
web search/fetch tools for event discovery.

GeoNames city data (used for geocoding and nearby city discovery) is
downloaded automatically on first run to the active Weekend Scout cache
directory.

## Telegram Setup

Weekend Scout can send event summaries to a Telegram chat (group, channel, or DM).
This is optional — if Telegram is not configured the skill prints the digest in chat
and shows the commands to enable delivery.
For OpenClaw users, this section is usually not needed: OpenClaw handles final
delivery through its own channel path, so bot token/chat ID setup is only for
direct CLI/API Telegram sending outside that flow.

### Step 1: Create a bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`, choose a name and username (e.g. `weekend_scout_bot`)
3. BotFather replies with your **bot token** — looks like `123456789:ABCdefGhIJK...`

### Step 2: Get your chat ID

**For a group:** add the bot, send a message, then open:
```
https://api.telegram.org/bot<TOKEN>/getUpdates
```
Look for `"chat":{"id":-100XXXXXXXXXX}` (negative number = group/channel).

**For a DM:** open a chat with your bot, send `/start`, then use the same URL.
Your chat ID is the positive number in `"chat":{"id":XXXXXXXXX}`.

### Step 3: Configure Weekend Scout

```bash
python -m weekend_scout config telegram_bot_token "YOUR_BOT_TOKEN"
python -m weekend_scout config telegram_chat_id "YOUR_CHAT_ID"
```

If you plan to run `/weekend-scout` more than once in the same week and want each
run to show only new events (excluding what was already sent), enable:

```bash
python -m weekend_scout config exclude_served true
```

## Usage

### Via skill

```
/weekend-scout
/weekend-scout Berlin 100
/weekend-scout --cached-only
/weekend-scout --reset
```

| Argument | Description |
|----------|-------------|
| `CITY` | Bootstrap home city on first run without a separate `setup` step |
| `RADIUS` | Bootstrap search radius on first run |
| `--cached-only` | Skip web searching; format and send from cached events only |
| `--research-only` | Run full discovery and cache results; skip formatting and delivery |
| `--reset` | Ask for confirmation, then delete Weekend Scout config and cache for the active install |

`--cached-only` and `--research-only` are skill-only invocation flags. Do not append them to
`python -m weekend_scout init` or `python -m weekend_scout init-skill`.

`--reset` is a skill-side reset mode. After confirmation, the agent runs
`python -m weekend_scout reset --yes` and stops instead of starting discovery.

If the scout is not configured yet, providing `CITY` and `RADIUS` lets the first
`init-skill` bootstrap configuration immediately. A successful city match is saved
to `.weekend_scout/config.yaml`; if coordinates still need resolving, the skill
continues with the existing coordinate-fix onboarding flow.

#### Scheduling pattern

You have flexibility in how you run the skill depending on your token budget and desired result freshness:

**Option 1: Single run (default)**
```
Fri evening:  /weekend-scout                      # search, build report, send
```
This discovers new events, combines them with any cached events from previous runs, and
delivers the complete digest in one execution.

**Option 2: Multi-run discovery (budget-efficient)**
Run discovery multiple times during the week without delivering intermediate results, then report once on Friday:

```
Mon/Wed:      /weekend-scout --research-only   # discover and cache new events, no delivery
Fri evening:  /weekend-scout --cached-only     # build report from all accumulated cache, no discovery
```

**Option 3: Mixed mode**
```
Mon/Wed:      /weekend-scout --research-only   # discover and cache new events, no delivery
Fri evening:  /weekend-scout                   # search again, combine with cache, send digest
```
Similar to Option 2, but with fresh discovery on Friday. The final digest includes both the
cached events accumulated earlier in the week AND any new events discovered on Friday.

**OpenClaw note:** scheduled runs are typically created with `openclaw cron add ...`. For isolated
cron jobs, OpenClaw's cron runner owns final delivery, so the skill should return the final
plain-text summary for the configured announce target rather than choosing a channel itself. Example:

```bash
openclaw cron add \
  --name "Weekend Scout Friday" \
  --cron "0 18 * * 5" \
  --session isolated \
  --announce \
  --channel telegram \
  --to "<chat-id>" \
  --message "Run Weekend-Scout skill and return the final plain-text summary for cron delivery."
```

### Via CLI

```bash
python -m weekend_scout --help
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `setup` | Interactive setup wizard |
| `setup --json '{...}'` | Apply a JSON config payload (no prompts) |
| `find-city --name CITY` | Look up a city in GeoNames |
| `config` | Show current configuration as JSON |
| `config KEY VALUE` | Set a single configuration value |
| `reset --yes` | Delete the active install's config file and cache directory |
| `init [--city CITY] [--radius KM]` | Load runtime run context plus expanded debug inspection data |
| `init-skill [--city CITY] [--radius KM]` | Load compact agent-facing run context |
| `save --events '<JSON>'` | Save discovered events to cache |
| `format-message` | Format the scout digest and write to file |
| `send --file <path>` | Send a formatted message file to Telegram |
| `send --message '<text>'` | Send a text message to Telegram |
| `cache-query --date YYYY-MM-DD` | Query cached events for a weekend |
| `log-search` | Log a completed web search |
| `log-action` | Append a structured action log entry |
| `cache-mark-served --date YYYY-MM-DD --run-id RUN_ID` | Mark events as sent |
| `install-skill [--platform P]` | Copy bundled skill files to global skills directory |
| `download-data` | Download GeoNames cities15000 to `.weekend_scout/cache/` |

## Configuration

Config lives at:
- `.weekend_scout/config.yaml`

Cache files (database, city lists, logs, GeoNames data) live in:
- `.weekend_scout/cache/`

| Key | Default | Description |
|-----|---------|-------------|
| `home_city` | `""` | Home city — set automatically on first run |
| `home_country` | `""` | Country name — auto-detected from GeoNames |
| `home_coordinates` | `{lat:0, lon:0}` | Lat/lon — auto-set from GeoNames |
| `radius_km` | `150` | Search radius in km |
| `search_language` | `"en"` | Language code for queries |
| `max_searches` | `15` | Max WebSearch calls per run |
| `max_fetches` | `15` | Max discovery WebFetch calls per run (Phases A-C) |
| `max_trip_options` | `10` | Max road trip options to include |
| `exclude_served` | `false` | Skip events already sent to Telegram in previous runs |
| `telegram_bot_token` | `""` | Telegram bot token |
| `telegram_chat_id` | `""` | Telegram chat/group/channel ID |

## Supported Languages

36 supported countries with country-specific search profiles:
Poland, United States, Canada, United Kingdom, Ireland, Australia, New Zealand,
Singapore, Japan, South Korea, Germany, France, Czech Republic, Slovakia,
Austria, Hungary, Ukraine, Lithuania, Latvia, Estonia, Belarus, Italy, Spain,
Portugal, Netherlands, Sweden, Norway, Denmark, Finland, Romania, Croatia,
Bulgaria, Serbia, Greece, Turkey, Russia.

Japan and South Korea use dedicated native-language query/date templates.
English-language queries are used intentionally for the United States, Canada,
United Kingdom, Ireland, Australia, New Zealand, and Singapore, and remain the
fallback for any other location.

## Project Structure

```
Weekend-Scout/
    weekend_scout/           Python package (CLI + data layer)
    skill_template/          Skill template + generator (source of truth)
    .claude/skills/          Generated skill for Claude Code
    .agents/skills/          Generated skill for Codex
    .openclaw/skills/        Generated skill for OpenClaw packaging/staging
    install/                 Cross-platform installer
    tests/                   Test suite
    docs/                    Design docs, backlog, references
```

## For Developers

### Skill Template System

Skills are generated from a single template using a preprocessor.
After editing `skill_template/weekend-scout.template.md`:

```bash
python skill_template/generate.py
```

This regenerates all platform SKILL.md files. See
[skill_template/README.md](skill_template/README.md) for details.

### Development Setup

```bash
git clone https://github.com/goooroooX/Weekend-Scout.git
cd Weekend-Scout
pip install -e ".[dev]"       # editable install with test deps
python -m pytest tests/ -v
```

If you want a global skill install after pip install, prefer:

```bash
python -m weekend_scout install-skill --platform <claude-code|codex|openclaw|all>
```

This copies the bundled skill files and binds them to that same Python interpreter.
The repo installer without `--with-pip` remains an advanced copy-only path for
interpreters that already have the package installed.

## Design

See [docs/weekend-scout-design-v2.md](docs/weekend-scout-design-v2.md)
for architecture and design decisions.

## Third-Party Data

Weekend Scout uses GeoNames city data for geocoding and nearby-city discovery.
GeoNames is provided by [GeoNames](https://www.geonames.org/).

## License

MIT
