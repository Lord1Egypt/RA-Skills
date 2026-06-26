---
name: website-email-scraper-apify
description: "Use this skill when the user needs public business emails, phone numbers, social profiles, source URLs, and crawl diagnostics from website domains or URLs through the Website Email Scraper & Phone Finder Apify actor."
version: 1.0.0
required_env_vars:
  - APIFY_TOKEN
required-env-vars:
  - APIFY_TOKEN
primary_credential: APIFY_TOKEN
primary-credential: APIFY_TOKEN
metadata:
  short-description: Run website email and contact extraction with Apify
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - python3
    primaryEnv: APIFY_TOKEN
    envVars:
      - name: APIFY_TOKEN
        required: true
        description: Apify API token used to run the Website Email Scraper & Phone Finder actor.
    primaryCredential: APIFY_TOKEN
    emoji: "📬"
    homepage: https://github.com/hundevmode/apify-website-email-scraper-agent-skill
---

# Website Email Scraper Apify Skill

## Overview

This skill helps an AI agent run the Apify Website Email Scraper & Phone Finder actor for public website contact extraction from domains and URLs.

Default actor:

- Actor ID: `kWfD7C0WpHtIt8VAh`
- Actor name: `x_guru/website-email-phone-finder`
- Store page: `https://apify.com/x_guru/website-email-phone-finder`
- Console source: `https://console.apify.com/actors/kWfD7C0WpHtIt8VAh/source`

Use this skill when a user asks to:

- scrape public business emails from website domains
- find emails from company websites, landing pages, contact pages, or domain lists
- enrich lead lists with emails, phones, social profile links, source URLs, and crawl diagnostics
- process domains from Google Maps, CRMs, spreadsheets, directories, search results, Apollo-style lists, or agency prospecting workflows
- return only websites with emails, only websites with any contact, or all scanned websites
- control Apify spend with `maxTotalChargeUsd`
- export contact rows for Sheets, Airtable, n8n, CRM, BI, CSV, JSON, or agent workflows

## Quick Workflow

1. Clarify the submitted domains or website URLs and the desired saved result count.
2. Use `resultMode: "emailsOnly"` by default for email lead extraction.
3. Use `contactsOnly` when phone numbers or social profiles are useful even without emails.
4. Use `allWebsites` only when the user needs diagnostics for every submitted website.
5. Keep `maxPagesPerWebsite` at `3` for fast runs; use `5-10` when contacts are likely on staff, team, legal, imprint, or contact pages.
6. Set `includePersonalData=false` when person-like emails or personal LinkedIn profile URLs should be excluded.
7. Set a budget guard with Apify `maxTotalChargeUsd` when spend matters.
8. Run `scripts/website_email_scraper_actor.py` or call the Apify API directly.
9. Return compact metrics and website contact rows. Check `RUN_SUMMARY` for diagnostics when counts are lower than requested.

## Payload Rules

- Use `domains` for bare domains and full website URLs.
- `urls` and `startUrls` can be normalized into `domains` by the runner for agent convenience.
- `maxResults` is the maximum number of saved dataset rows.
- `resultMode` must be `emailsOnly`, `contactsOnly`, or `allWebsites`.
- `maxPagesPerWebsite` must be `1-25`; default is `3`.
- `concurrency` must be `1-500`; default is `100`.
- `requestTimeoutSecs` must be `2-30`; default is `5`.
- `extractPhones`, `extractSocials`, `includePersonalData`, and `sameDomainOnly` are booleans.
- Do not send Google Maps search fields such as `searchStringsArray`, `placeIds`, `locationQuery`, or review fields to this website-only actor.
- Pass `maxTotalChargeUsd` as an Apify run option, not inside actor input. The included script exposes it as `--budget-usd`.

## Authentication

Use the Apify API token from the environment:

```bash
export APIFY_TOKEN='apify_api_xxx'
```

Never hardcode or print the full token in user-facing output.

## Script Usage

The bundled script uses only Python standard library.

Run a quick domain email scrape:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/website_email_scraper_actor.py quick-domains \
  --domains example.com apify.com \
  --max-results 50 \
  --budget-usd 1
```

Run with deeper contact-page discovery:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/website_email_scraper_actor.py quick-domains \
  --domains centralrestaurante.com alchemist.dk caitlinmcweeney.com \
  --max-results 100 \
  --max-pages 5 \
  --result-mode emailsOnly \
  --budget-usd 1
```

Run custom JSON:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/website_email_scraper_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Recommended Inputs

### Public email leads only

```json
{
  "domains": ["centralrestaurante.com", "alchemist.dk", "caitlinmcweeney.com"],
  "maxResults": 1000,
  "resultMode": "emailsOnly",
  "maxPagesPerWebsite": 3,
  "concurrency": 100,
  "requestTimeoutSecs": 5,
  "extractPhones": true,
  "extractSocials": true,
  "includePersonalData": true,
  "sameDomainOnly": true
}
```

### Company inboxes only

```json
{
  "domains": ["example.com", "https://example.com/contact"],
  "maxResults": 500,
  "resultMode": "emailsOnly",
  "includePersonalData": false,
  "extractPhones": true,
  "extractSocials": true
}
```

### Contact records for every website with any public contact

```json
{
  "domains": ["example.com", "apify.com"],
  "maxResults": 100,
  "resultMode": "contactsOnly",
  "maxPagesPerWebsite": 5
}
```

## Output Contract

The runner returns JSON:

- `ok`
- `actorId`
- `fetchedAt`
- `inputUsed`
- `itemCount`
- `rows[]`

Rows are actor dataset items. Important groups:

- Website identity: `input`, `url`, `domain`, `status`
- Emails: `emails`, `emailDetails.email`, `emailDetails.type`, `emailDetails.sourceUrl`, `emailDetails.domainMatch`
- Contacts: `phones`, `socialLinks`, `facebooks`, `instagrams`, `linkedIns`, `twitters`, `youtubes`, `tiktoks`
- Crawl diagnostics: `contactSignals`, `pagesFetched`, `fetchedUrls`, `httpStatusCodes`, `errors`, `durationMs`

For the full contract, read `references/input-output-contract.md`.

## Agent Response Rules

- If rows are empty, say the run succeeded but no website contact rows matched the selected mode, then suggest checking `RUN_SUMMARY`.
- If fewer rows than requested are returned, explain that submitted websites had fewer public contacts, the result mode filtered rows, or budget stopped saving.
- If `emails` is empty in `contactsOnly` or `allWebsites`, explain that the row was saved due to phone/social/diagnostic data.
- Explain website email extraction as best-effort because each website controls what it publishes.
- Use `maxTotalChargeUsd` for any user concerned about spend.
- Do not promise Google Maps place discovery from this actor. Use the Google Maps Email Extractor actor when the user needs search-by-keyword/location first.

## References

- `references/input-output-contract.md`
- `references/sample_input.json`
- `references/troubleshooting.md`
