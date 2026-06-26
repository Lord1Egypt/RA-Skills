# Website Email Scraper Skill for OpenClaw and AI Agents

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](./LICENSE)
[![Apify Actor](https://img.shields.io/badge/Apify-kWfD7C0WpHtIt8VAh-ff6b00)](https://console.apify.com/actors/kWfD7C0WpHtIt8VAh/source)
[![Skill Type](https://img.shields.io/badge/OpenClaw-Skill-111827)](./SKILL.md)
[![skills.sh](https://skills.sh/b/hundevmode/apify-website-email-scraper-agent-skill)](https://skills.sh/hundevmode/apify-website-email-scraper-agent-skill)

AI-agent skill for running the Website Email Scraper & Phone Finder through Apify. It helps agents build correct payloads, control spend, run the actor, and return structured public business emails, phones, social profiles, source URLs, and website crawl diagnostics from domains and URLs.

Default actor:

- Actor ID: [`kWfD7C0WpHtIt8VAh`](https://console.apify.com/actors/kWfD7C0WpHtIt8VAh/source)
- Actor name: `x_guru/website-email-phone-finder`
- Store page: [https://apify.com/x_guru/website-email-phone-finder](https://apify.com/x_guru/website-email-phone-finder)
- Auth: `APIFY_TOKEN`

## What This Skill Does

- Builds Website Email Scraper payloads from natural-language lead enrichment requests.
- Runs domain and URL lists through the Apify actor.
- Defaults to `emailsOnly`, so rows are saved only when a public email is found.
- Supports phone extraction, social profile extraction, personal data toggle, crawl depth, same-domain crawling, and concurrency.
- Applies Apify run budget guard with `maxTotalChargeUsd`.
- Returns rows ready for CRM import, outreach workflows, spreadsheets, databases, or agent pipelines.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Agent trigger rules, workflow, payload rules, and output contract |
| `agents/openai.yaml` | OpenClaw UI metadata |
| `scripts/website_email_scraper_actor.py` | CLI runner for the Apify actor |
| `references/input-output-contract.md` | Detailed input and output contract |
| `references/sample_input.json` | Ready-to-run sample input |
| `references/troubleshooting.md` | Common failures and fixes |

## Quick Start

Set token:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Run a quick website email scrape:

```bash
python3 scripts/website_email_scraper_actor.py quick-domains \
  --domains example.com apify.com \
  --max-results 50 \
  --budget-usd 1
```

Run custom JSON:

```bash
python3 scripts/website_email_scraper_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Install as a Skill

OpenClaw or ClawHub:

```bash
npx skills add hundevmode/apify-website-email-scraper-agent-skill \
  --skill website-email-scraper-apify
```

Codex or another supported Skills CLI agent:

```bash
npx skills add hundevmode/apify-website-email-scraper-agent-skill \
  --skill website-email-scraper-apify \
  --agent codex \
  -y
```

List skills:

```bash
npx skills add hundevmode/apify-website-email-scraper-agent-skill --list
```

## Output

The runner prints JSON with:

- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Each row is one website contact record, including public emails when found, email metadata, phone numbers, social links, source URLs, fetched pages, HTTP status codes, crawl errors, and duration diagnostics.

## Pricing Notes

The hosted actor uses Apify pay-per-event pricing:

- Paid plans: from `$2.00 / 1,000` saved website contact results
- Free plan: `$5.00 / 1,000` saved website contact results
- Actor start event: tiny PPE start fee

Use `--budget-usd` to pass Apify `maxTotalChargeUsd`.

## Security

- Do not hardcode Apify tokens.
- Prefer `APIFY_TOKEN` from the environment.
- Use `--budget-usd` for controlled runs.
- Set `includePersonalData=false` when person-like emails or personal LinkedIn profile URLs are not needed.

## SEO Keywords

Website email scraper skill, website email finder, domain email scraper, domain email finder, business email scraper, company email finder, website contact scraper, email phone finder, public business emails, lead generation email scraper, Apify website email actor, AI agent scraping skill, OpenClaw skill, ClawHub skill, skills.sh skill.

## License

MIT-0, matching ClawHub skill publishing terms.
