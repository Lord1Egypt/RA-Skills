# scraper-skill

ScrapeBox-style candidate discovery for link building and outreach — **without getting your server IP banned**.

## Why

Search engines (Google, Brave, DuckDuckGo, Bing, Ecosia) aggressively block **datacenter IPs** (Hetzner, AWS, DO...). A direct search from a VPS returns captchas or garbage ~100% of the time. This skill routes queries through **rotating Tor exit nodes** so the server's real IP never touches the engine, then harvests, dedupes, triages, and exports a scored candidate list.

Verified Aug 2026 from a Hetzner datacenter IP:
- Google → `/sorry` captcha block
- DuckDuckGo → "Select all squares containing a duck" challenge
- Brave → slider captcha / HTTP 429
- Bing → returns 200 but useless results for quoted phrases
- **Via Tor: DuckDuckGo HTML works (200 + real results), Marginalia works (200 + real results)**

## What it does

1. **Rotates** to a fresh Tor exit node before every query (NEWNYM signal via control port)
2. **Harvests** candidate URLs from DuckDuckGo HTML and Marginalia
3. **Retries** on blocked/failed exits (~1/3 of Tor exits are already flagged; rotate-and-retry is built in)
4. **Dedupes** and optionally **triages** each URL (alive / Cloudflare-walled / parked-dead)
5. **Exports** a ranked markdown candidate list ready for the directory-submission workflow

## Quick start

```bash
# 1. Run a dedicated Tor instance (SOCKSPort 19050, ControlPort 19051)
sudo tor -f /tmp/tor-harvestrc     # see SKILL.md for the config

# 2. Harvest
python3 scripts/search-harvester.py \
  '"submit your company" directory' \
  '"add your company" free listing' \
  --engine ddg --max-rotations 3 --triage --out /tmp/harvest.md
```

## Requirements

- Linux with `tor`, `curl`, `nc`, `python3` (stdlib only — no pip deps)
- A running Tor instance on `127.0.0.1:19050` (SOCKS) with control port `127.0.0.1:19051`

## Repo layout

```
scraper-skill/
├── search-harvester/          # the skill (ClawHub-compliant package)
│   ├── SKILL.md               # full workflow, engine status, pitfalls
│   ├── skill-card.md          # ClawHub catalog card
│   └── scripts/
│       └── search-harvester.py  # automated harvest loop
├── LICENSE                    # MIT-0
└── README.md
```

## Publishing to ClawHub

This repo is ClawHub-compliant (see [skill format docs](https://docs.openclaw.ai/clawhub/skill-format)):

```bash
npm i -g clawhub
clawhub login
clawhub skill publish ./search-harvester \
  --slug search-harvester --name "Search Harvester" \
  --owner toniilic \
  --categories research,automation \
  --topics "tor,scraping,seo,link-building,directories"
```

Or import from GitHub on [clawhub.ai/import](https://clawhub.ai/import) — the web importer discovers `SKILL.md` in public repos owned by the signed-in account.

## License

MIT-0 — no attribution required. See [LICENSE](LICENSE).
