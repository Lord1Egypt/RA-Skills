# Website Phone Number Finder Skill for OpenClaw and AI Agents

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green.svg)](./LICENSE)
[![Apify Actor](https://img.shields.io/badge/Apify-HE8ML7ZqmGI6OtyFU-ff6b00)](https://console.apify.com/actors/HE8ML7ZqmGI6OtyFU/source)
[![Skill Type](https://img.shields.io/badge/OpenClaw-Skill-111827)](./SKILL.md)
[![skills.sh](https://skills.sh/b/hundevmode/apify-website-phone-number-finder-agent-skill)](https://skills.sh/hundevmode/apify-website-phone-number-finder-agent-skill)

AI-agent skill for running the Website Phone Number Finder through Apify. It helps agents build correct payloads, control spend, run the actor, and return structured public business phone numbers, `tel:` links, optional emails, social profiles, source URLs, and website crawl diagnostics from domains and URLs.

Default actor:

- Actor ID: [`HE8ML7ZqmGI6OtyFU`](https://console.apify.com/actors/HE8ML7ZqmGI6OtyFU/source)
- Actor name: `x_guru/website-phone-number-finder`
- Store page: [https://apify.com/x_guru/website-phone-number-finder](https://apify.com/x_guru/website-phone-number-finder)
- Auth: `APIFY_TOKEN`

## What This Skill Does

- Builds Website Phone Number Finder payloads from natural-language lead enrichment requests.
- Runs domain and URL lists through the Apify actor.
- Defaults to `phonesOnly`, so rows are saved only when a public phone number is found.
- Supports optional email extraction, social profile extraction, personal data toggle, crawl depth, same-domain crawling, and concurrency.
- Applies Apify run budget guard with `maxTotalChargeUsd`.
- Returns rows ready for CRM import, outreach workflows, spreadsheets, databases, or agent pipelines.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Agent trigger rules, workflow, payload rules, and output contract |
| `agents/openai.yaml` | OpenClaw UI metadata |
| `scripts/website_phone_number_finder_actor.py` | CLI runner for the Apify actor |
| `references/input-output-contract.md` | Detailed input and output contract |
| `references/sample_input.json` | Ready-to-run sample input |
| `references/troubleshooting.md` | Common failures and fixes |

## Quick Start

Set token:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Run a quick website phone scrape:

```bash
python3 scripts/website_phone_number_finder_actor.py quick-domains \
  --domains alchemist.dk disfrutarbarcelona.com \
  --max-results 50 \
  --budget-usd 1
```

Run custom JSON:

```bash
python3 scripts/website_phone_number_finder_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Install as a Skill

OpenClaw or ClawHub:

```bash
npx skills add hundevmode/apify-website-phone-number-finder-agent-skill \
  --skill website-phone-number-finder-apify
```

Codex or another supported Skills CLI agent:

```bash
npx skills add hundevmode/apify-website-phone-number-finder-agent-skill \
  --skill website-phone-number-finder-apify \
  --agent codex \
  -y
```

List skills:

```bash
npx skills add hundevmode/apify-website-phone-number-finder-agent-skill --list
```

## Output

The runner prints JSON with:

- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Each row is one website phone result, including public phone numbers, phone metadata, optional emails, social links, source URLs, fetched pages, HTTP status codes, crawl errors, and duration diagnostics.

## Pricing Notes

The hosted actor uses Apify pay-per-event pricing:

- Paid plans: from `$2.00 / 1,000` saved website phone results
- Free plan: `$5.00 / 1,000` saved website phone results
- Actor start event: tiny PPE start fee

Use `--budget-usd` to pass Apify `maxTotalChargeUsd`.

## Security

- Do not hardcode Apify tokens.
- Prefer `APIFY_TOKEN` from the environment.
- Use `--budget-usd` for controlled runs.
- Set `includePersonalData=false` when personal LinkedIn profile URLs or person-like optional emails are not needed.

## SEO Keywords

Website phone number finder skill, website phone scraper, domain phone number finder, domain phone scraper, business phone number scraper, company phone finder, phone number scraper for lead generation, website contact phone extractor, public business phone numbers, tel link extractor, Apify website phone actor, AI agent scraping skill, OpenClaw skill, ClawHub skill, skills.sh skill.

## License

MIT-0, matching ClawHub skill publishing terms.
