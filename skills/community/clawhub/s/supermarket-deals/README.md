# supermarket-deals

> 🇩🇪 An OpenClaw skill for tracking product deals at German supermarkets (Aldi, Lidl, REWE, EDEKA, Kaufland and more) via the [Marktguru](https://www.marktguru.de) API.

[![ClawHub](https://img.shields.io/badge/clawhub-supermarket--deals-blue)](https://clawhub.ai/benmillerat/supermarket-deals)

---

## What it does

German supermarkets publish weekly flyers ("Prospekte") with discounted products. This skill searches those flyers for any product you care about and returns results ranked by **best price per litre (EUR/L)** — so you always see the best value deal first.

It works by extracting Marktguru's API keys from their homepage at runtime — no registration, no API key, no cost.

**Example use cases:**
- Find the cheapest Coca-Cola Zero near you this week
- Track Monster Energy deals across Aldi, Lidl and REWE
- Monitor any product category across all major German chains

---

## How it works

1. On each run, the skill fetches fresh API keys from the Marktguru homepage (cached for 6 hours)
2. It searches current Prospekte by your query + ZIP code (PLZ)
3. Results are filtered by your preferred stores, ranked by EUR/L, and returned with a direct Marktguru link per deal
4. Your agent (e.g. OpenClaw) applies intelligent filtering to the results and sends you a summary — via Telegram, weekly cron, or on demand

The skill is intentionally a **dumb data fetcher**. The agent applies the smart filtering — this makes it reusable for any product and any notification style.

---

## Requirements

- Node.js 18+
- A German postal code (PLZ)

---

## Install

**Via ClawHub** (once approved):
```bash
clawhub install supermarket-deals
cd supermarket-deals
npm install
npm run build
```

**Via GitHub** (available now):
```bash
git clone https://github.com/benmillerat/openclaw-supermarket-deals.git
cd supermarket-deals
npm install
npm run build
```

---

## Setup

Set your defaults (optional — can also pass `--zip` per search):

```bash
node dist/index.js config set zip 85540
node dist/index.js config set stores "Lidl,REWE,EDEKA,ALDI SÜD,ALDI NORD,Kaufland"
```

Config is stored at `~/.supermarket-deals/config.json`.

---

## Usage

### Search

```bash
node dist/index.js search <query> [query2 ...] [--zip <PLZ>] [--stores <list>] [--limit <n>] [--json]
```

**Examples:**

```bash
# Search for a product
node dist/index.js search "Cola Zero" --zip 85540

# Multiple terms — merged, deduplicated, ranked together
node dist/index.js search "Cola Zero" "Coke Zero" --zip 85540

# Broad search — recommended for agent/cron use
node dist/index.js search "Cola" --zip 85540

# Filter to specific stores
node dist/index.js search "Monster Energy" --zip 80331 --stores "Lidl,ALDI SÜD"

# JSON output for agent/cron pipelines
node dist/index.js search "Cola" --zip 85540 --json
```

### Options

| Flag | Description |
|------|-------------|
| `--zip <PLZ>` | German postal code (overrides config default) |
| `--stores <list>` | Comma-separated store filter (overrides config default) |
| `--limit <n>` | Max results (default: 20, max: 100) |
| `--json` | Structured JSON output |

### Config

```bash
node dist/index.js config                        # show current config
node dist/index.js config set zip 85540          # set default ZIP
node dist/index.js config set stores "Lidl,REWE" # set default stores
```

---

## Output

```
Description                                             | Store    | Size    | Price    | EUR/L      | Valid                 | URL
--------------------------------------------------------------------------------------------------------------------------------
oder Coca-Cola zero 2-l-Flasche zzgl. Pfand 0.25        | ALDI SÜD | 2l      | 1.29 EUR | 0.65 EUR/L | 2026-03-12–2026-03-14 | https://www.marktguru.de/offers/21916812
Fanta/Sprite/Mezzo Mix versch. Sorten. 1,25 l           | Lidl     | 1.25l   | 0.99 EUR | 0.79 EUR/L | 2026-03-01–2026-03-07 | https://www.marktguru.de/offers/21894391
```

---

## Recommended agent pattern (e.g. weekly cron)

The power comes from combining the skill's broad search with your agent's intelligence.

**Step 1 — Search broadly:**
```bash
node dist/index.js search "Cola" --zip 85540 --json
```

**Step 2 — Let your agent filter:**
> You are looking for Coca-Cola Zero deals. Include deals that explicitly mention Coca-Cola/Coke Zero, OR deals that say "versch. Sorten" (various sorts — these bundled deals cover all Cola variants including Zero). Exclude deals that only mention Powerade, Fuze Tea, or clearly non-Cola products. Rank by EUR/L, highlight the best deal with 🏆, include the Marktguru URL for each.

**Why broad + agent instead of narrow query?**
German supermarkets often list Cola deals as "Fanta/Sprite/Mezzo Mix **versch. Sorten**" (various sorts) — meaning the deal covers all Cola variants including Coke Zero, but Coke Zero isn't named explicitly. A narrow `"Coke Zero"` query would miss these. A broad `"Cola"` query catches them all.

---

## Notes

- Prospekte refresh on **Mondays and Thursdays**
- Marktguru caches API results for ~15 minutes
- Some regional store branches don't submit flyers to Marktguru — if you get zero results for your PLZ, try a nearby larger ZIP as a sanity check
- API keys rotate and are extracted fresh from the Marktguru homepage at runtime (cached 6h in `~/.supermarket-deals/keys.json`)

---

## License

MIT
