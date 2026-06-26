# yc — CLI for YC Startup School, a16z Speedrun, SPC & Startup Discovery

A CLI tool for managing your YC Startup School journey, submitting a16z Speedrun and South Park Commons applications, and discovering 24+ accelerators, fellowships, and incubators — all from the terminal.

> ### Easiest way to get started
>
> Paste this to your AI coding agent (Claude Code, Cursor, Codex, Windsurf, OpenClaw, etc.):
>
> **"Install the `@lucasygu/yc` tool via npm and run `yc whoami` to verify it works. Repo: https://github.com/lucasygu/yc-cli"**
>
> OpenClaw users can also run: **`clawhub install yc`**
>
> The agent will handle installation, verify the connection, and troubleshoot any cookie issues. Just make sure you're logged into [startupschool.org](https://www.startupschool.org/) in Chrome first.
>
> Once installed, try: **"Check my YC Startup School dashboard and submit this week's update"** — the agent will pull your streak, curriculum progress, and walk you through submitting.

## Install

```bash
npm install -g @lucasygu/yc
# Or via ClawHub (OpenClaw ecosystem)
clawhub install yc
```

Requires Node.js >= 22.

- **YC Startup School**: Uses cookies from your Chrome browser session — log into [startupschool.org](https://www.startupschool.org/) in Chrome first.
- **a16z Speedrun**: No authentication needed (public API).
- **South Park Commons**: Uses Playwright (headless Chromium) to fill Airtable forms — no auth needed.

After installing, run `yc whoami` to verify the connection. If macOS shows a Keychain prompt, click "Always Allow". The CLI auto-detects all Chrome profiles to find your YC session.

## What You Can Do

- **Dashboard tracking** — Check your streak, curriculum progress, and weekly update status
- **Weekly updates** — Submit updates from the terminal (interactive or scripted)
- **Update history** — Review all past updates with metrics, morale, and goals
- **Speedrun applications** — Apply to a16z Speedrun with a JSON template or interactively
- **Deck upload** — Upload pitch deck PDFs for Speedrun applications
- **SPC applications** — Apply to South Park Commons Founder Fellowship or Community Membership via Playwright browser automation
- **Program discovery** — Browse 24+ curated accelerators, fellowships, and incubators with deadlines, terms, and application links

When used through an AI agent, these workflows chain together automatically. Each CLI command also works standalone.

## Quick Start

```bash
# YC Startup School
yc whoami                    # Test connection, show user info
yc dashboard                 # Show streak, curriculum, weekly status
yc updates                   # List all weekly updates
yc show <id>                 # Show a single update in detail
yc new                       # Submit new weekly update (interactive)
yc new --metric 5 --morale 7 --talked-to 3   # Non-interactive

# a16z Speedrun
yc speedrun template         # Generate JSON template
yc speedrun apply            # Interactive application
yc speedrun apply --from-json app.json        # Submit from JSON
yc speedrun apply --from-json app.json --dry-run  # Validate only
yc speedrun upload-deck deck.pdf              # Upload pitch deck

# Discover Programs
yc discover                  # Overview — deadlines + rolling programs
yc discover list             # Browse all 24+ programs
yc discover list --type fellowship   # Filter by type
yc discover list --stage pre-seed    # Filter by stage
yc discover deadlines        # Upcoming deadlines sorted by date
yc discover show yc          # Full details for a program
yc discover search "deep tech"       # Search by name/focus/description
yc discover open yc          # Open application page in browser

# South Park Commons
yc spc info                  # Show programs and form URLs
yc spc template              # Generate JSON template (fellowship)
yc spc template --type membership             # Community membership
yc spc apply                 # Interactive application
yc spc apply --from-json app.json             # Fill from JSON
yc spc apply --from-json app.json --dry-run --headed  # Visual preview
yc spc open                  # Open form in browser
```

## Commands

| Command | Description |
|---------|-------------|
| `whoami` | Test connection and show current user info |
| `dashboard` | Show streak, curriculum progress, and weekly update status |
| `updates` | List all weekly updates with metrics and morale |
| `show <id>` | Show a single update in full detail |
| `new` | Submit a new weekly update (interactive or with flags) |
| `speedrun template` | Generate a JSON template for a16z Speedrun application |
| `speedrun apply` | Submit a Speedrun application (interactive or from JSON) |
| `speedrun upload-deck <file>` | Upload a pitch deck PDF |
| `spc info` | Show SPC programs and form URLs |
| `spc template` | Generate a JSON template for SPC application |
| `spc apply` | Fill and submit SPC application via Playwright |
| `spc open` | Open SPC application form in browser |
| `discover` | Overview — upcoming deadlines and rolling programs |
| `discover list` | Browse all programs (with `--type`, `--stage`, `--focus`, `--tier` filters) |
| `discover deadlines` | Upcoming deadlines sorted by closing date |
| `discover show <slug>` | Full details for a program |
| `discover search <query>` | Search programs by name, focus, or description |
| `discover open <slug>` | Open program website or application in browser |

### Global Options (YC Startup School)

| Option | Description | Default |
|--------|-------------|---------|
| `--cookie-source <browser>` | Browser to read cookies from (chrome, safari, firefox) | `chrome` |
| `--chrome-profile <name>` | Chrome profile directory name (e.g., "Profile 1"). Auto-detected if omitted. | auto |
| `--json` | Output as JSON | `false` |

### Weekly Update Options (`yc new`)

| Option | Description |
|--------|-------------|
| `--metric <value>` | Primary metric value (number) |
| `--morale <value>` | Morale 1-10 |
| `--talked-to <value>` | Users talked to (number) |
| `--change <text>` | What most improved your metric |
| `--blocker <text>` | Biggest obstacle |
| `--learned <text>` | What you learned from users |
| `--goal <goals...>` | Goals for next week (can specify multiple) |

### Speedrun Options (`yc speedrun apply`)

| Option | Description |
|--------|-------------|
| `--from-json <file>` | Load application from a JSON file |
| `--dry-run` | Validate and show payload without submitting |

### SPC Options (`yc spc apply`)

| Option | Description | Default |
|--------|-------------|---------|
| `--type <type>` | Form type: `fellowship` or `membership` | `fellowship` |
| `--from-json <file>` | Load application from JSON file | — |
| `--dry-run` | Fill form but do not submit | `false` |
| `--headed` | Show browser window (default: headless) | `false` |

### Discover Options (`yc discover list`)

| Option | Description | Default |
|--------|-------------|---------|
| `--type <type>` | Filter: `accelerator`, `fellowship`, `incubator`, `community` | all |
| `--stage <stage>` | Filter: `pre-idea`, `pre-seed`, `seed` | all |
| `--focus <focus>` | Filter by focus area: `ai`, `deep-tech`, `fintech`, etc. | all |
| `--tier <tier>` | Filter: `1` (elite), `2` (major), `3` (notable) | all |
| `--json` | Output as JSON | `false` |

### Speedrun Categories

```
B2B / Enterprise Applications
Consumer Applications
Deep Tech
Gaming / Entertainment Studio
Infrastructure / Dev Tools
Healthcare
GovTech
Web3
Other
```

### SPC Programs

| Program | Funding | Duration |
|---------|---------|----------|
| Founder Fellowship | $400K for 7% + $600K follow-on | Cohort-based (Spring/Fall) |
| Community Membership | No funding | Up to 6 months |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `No session cookie found` | Log into startupschool.org in Chrome, then retry |
| macOS Keychain prompt | Enter your password and click "Always Allow" — the CLI needs to decrypt Chrome's cookies |
| Multiple Chrome profiles | The CLI auto-scans all profiles. To pick one: `--chrome-profile "Profile 1"` |
| Using Brave/Arc/other | Try `--cookie-source safari`, or log into startupschool.org in Chrome |
| Speedrun API error | No auth needed — check your internet connection |
| SPC form timeout | Airtable forms are heavy SPAs. Retry or use `--headed` to debug |

## How It Works

**YC Startup School** — Reads your session cookies from Chrome (via [@steipete/sweet-cookie](https://github.com/steipete/sweet-cookie)), extracts the Rails CSRF token, then uses GraphQL for reads (`/graphql` endpoint) and Rails REST for writes (weekly update submission). No browser automation needed — just HTTP requests.

**a16z Speedrun** — Direct JSON API calls to Speedrun's public endpoint. No authentication, no signing, no cookies. Upload pitch decks via GCS signed URLs.

**South Park Commons** — SPC uses Airtable Interface forms (client-rendered SPAs). Since there's no public API, the CLI uses [Playwright](https://playwright.dev/) to navigate, fill, and submit the form programmatically. Supports headless and headed modes for preview before submission.

## Workflows

### Weekly Update Routine

```bash
yc dashboard            # Check streak and status
yc new                  # Submit this week's update
yc updates              # Verify it's there
```

### Speedrun Application via AI Agent

```bash
yc speedrun template > /tmp/speedrun-app.json         # Generate template
# ... AI fills in the JSON with your details ...
yc speedrun apply --from-json /tmp/speedrun-app.json --dry-run  # Validate
yc speedrun apply --from-json /tmp/speedrun-app.json            # Submit
```

### SPC Application via AI Agent

```bash
yc spc template > /tmp/spc-app.json                           # Generate template
# ... AI fills in the JSON with your details ...
yc spc apply --from-json /tmp/spc-app.json --dry-run --headed  # Preview in browser
yc spc apply --from-json /tmp/spc-app.json                     # Submit
```

## AI Agent Integration

### Claude Code

Installs automatically as a Claude Code skill. Use `/yc` in Claude Code:

```
/yc whoami                    # Test connection
/yc dashboard                 # Check streak
/yc new                       # Submit weekly update
/yc speedrun apply            # Apply to a16z Speedrun
/yc spc apply                 # Apply to SPC
```

You can give natural language instructions for complex tasks:

- *"Check my Startup School dashboard and tell me if I need to submit this week"*
- *"Submit my weekly update — metric is 15, morale is 8, talked to 5 users"*
- *"Help me apply to a16z Speedrun with my startup details"*
- *"Fill out an SPC Founder Fellowship application for me"*

Claude will automatically generate templates, fill in your details, validate, and submit.

### OpenClaw / ClawHub

Officially supports [OpenClaw](https://openclaw.ai) and [ClawHub](https://docs.openclaw.ai/tools/clawhub). Install via ClawHub:

```bash
clawhub install yc
```

All `yc` commands are available in OpenClaw after installation. The SKILL.md is compatible with both Claude Code and OpenClaw ecosystems.

## Authentication

| Platform | Method | Setup |
|----------|--------|-------|
| YC Startup School | Chrome session cookies | Log into startupschool.org in Chrome |
| a16z Speedrun | None (public API) | — |
| South Park Commons | Playwright (headless browser) | — |

## Disclaimer

This tool uses unofficial APIs for YC Startup School. YC may change or block these APIs at any time. The a16z Speedrun API is public. SPC uses Playwright to fill Airtable forms. Use responsibly and at your own risk. This project is not affiliated with Y Combinator, a16z, or South Park Commons.

## License

MIT
