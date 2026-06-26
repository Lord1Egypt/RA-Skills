---
name: website-phone-number-finder-apify
description: "Use this skill when the user needs public business phone numbers, tel links, optional emails, social profiles, source URLs, and crawl diagnostics from website domains or URLs through the Website Phone Number Finder Apify actor."
version: 1.0.0
required_env_vars:
  - APIFY_TOKEN
required-env-vars:
  - APIFY_TOKEN
primary_credential: APIFY_TOKEN
primary-credential: APIFY_TOKEN
metadata:
  short-description: Run website phone number extraction with Apify
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
        description: Apify API token used to run the Website Phone Number Finder actor.
    primaryCredential: APIFY_TOKEN
    emoji: "☎️"
    homepage: https://github.com/hundevmode/apify-website-phone-number-finder-agent-skill
---

# Website Phone Number Finder Apify Skill

## Overview

This skill helps an AI agent run the Apify Website Phone Number Finder actor for public website phone extraction from domains and URLs.

Default actor:

- Actor ID: `HE8ML7ZqmGI6OtyFU`
- Actor name: `x_guru/website-phone-number-finder`
- Store page: `https://apify.com/x_guru/website-phone-number-finder`
- Console source: `https://console.apify.com/actors/HE8ML7ZqmGI6OtyFU/source`

Use this skill when a user asks to:

- scrape public phone numbers from website domains
- find business phone numbers from company websites, landing pages, contact pages, locations pages, booking pages, or domain lists
- extract `tel:` links, visible phone numbers, source URLs, social profiles, optional emails, and crawl diagnostics
- enrich lead lists from Google Maps, CRMs, spreadsheets, directories, search results, company databases, or agency prospecting workflows
- return only websites with phones, only websites with any contact, or all scanned websites
- control Apify spend with `maxTotalChargeUsd`
- export phone lead rows for Sheets, Airtable, n8n, CRM, BI, CSV, JSON, or agent workflows

## Quick Workflow

1. Clarify submitted domains or website URLs and desired saved phone result count.
2. Use `resultMode: "phonesOnly"` by default for phone lead extraction.
3. Use `contactsOnly` when social profiles or optional emails are useful even without phones.
4. Use `allWebsites` only when the user needs diagnostics for every submitted website.
5. Keep `maxPagesPerWebsite` at `3` for fast runs; use `5-10` when phone numbers are likely on locations, booking, contact, legal, imprint, or team pages.
6. Keep `extractPhones=true`; disable `extractEmails` unless secondary email enrichment is requested.
7. Set `includePersonalData=false` when personal LinkedIn profile URLs or person-like optional emails should be excluded.
8. Set a budget guard with Apify `maxTotalChargeUsd` when spend matters.
9. Run `scripts/website_phone_number_finder_actor.py` or call the Apify API directly.
10. Return compact metrics and website phone rows. Check `RUN_SUMMARY` for diagnostics when counts are lower than requested.

## Payload Rules

- Use `domains` for bare domains and full website URLs.
- `urls` and `startUrls` can be normalized into `domains` by the runner for agent convenience.
- `maxResults` is the maximum number of saved dataset rows.
- `resultMode` must be `phonesOnly`, `contactsOnly`, or `allWebsites`.
- `maxPagesPerWebsite` must be `1-25`; default is `3`.
- `concurrency` must be `1-500`; default is `100`.
- `requestTimeoutSecs` must be `2-30`; default is `5`.
- `extractPhones`, `extractEmails`, `extractSocials`, `includePersonalData`, and `sameDomainOnly` are booleans.
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

Run a quick phone scrape:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/website_phone_number_finder_actor.py quick-domains \
  --domains alchemist.dk disfrutarbarcelona.com \
  --max-results 50 \
  --budget-usd 1
```

Run with deeper phone discovery:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/website_phone_number_finder_actor.py quick-domains \
  --domains alchemist.dk disfrutarbarcelona.com diverxo.com \
  --max-results 100 \
  --max-pages 5 \
  --result-mode phonesOnly \
  --budget-usd 1
```

Run custom JSON:

```bash
APIFY_TOKEN='apify_api_xxx' \
python3 scripts/website_phone_number_finder_actor.py run \
  --input-file references/sample_input.json \
  --budget-usd 1
```

## Recommended Inputs

### Public phone leads only

```json
{
  "domains": ["alchemist.dk", "disfrutarbarcelona.com", "diverxo.com"],
  "maxResults": 1000,
  "resultMode": "phonesOnly",
  "maxPagesPerWebsite": 3,
  "concurrency": 100,
  "requestTimeoutSecs": 5,
  "extractPhones": true,
  "extractEmails": false,
  "extractSocials": true,
  "includePersonalData": true,
  "sameDomainOnly": true
}
```

### Phone leads with optional emails

```json
{
  "domains": ["example.com", "https://example.com/contact"],
  "maxResults": 500,
  "resultMode": "phonesOnly",
  "extractPhones": true,
  "extractEmails": true,
  "extractSocials": true
}
```

### Any contact record

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
- Phones: `phones`, `phoneDetails.phone`, `phoneDetails.sourceUrl`
- Optional emails: `emails`, `emailDetails.email`, `emailDetails.type`, `emailDetails.sourceUrl`, `emailDetails.domainMatch`
- Contacts: `socialLinks`, `facebooks`, `instagrams`, `linkedIns`, `twitters`, `youtubes`, `tiktoks`
- Crawl diagnostics: `contactSignals`, `pagesFetched`, `fetchedUrls`, `httpStatusCodes`, `errors`, `durationMs`

For the full contract, read `references/input-output-contract.md`.

## Agent Response Rules

- If rows are empty, say the run succeeded but no website phone rows matched the selected mode, then suggest checking `RUN_SUMMARY`.
- If fewer rows than requested are returned, explain that submitted websites had fewer public phone numbers, the result mode filtered rows, or budget stopped saving.
- If `phones` is empty in `contactsOnly` or `allWebsites`, explain that the row was saved due to email/social/diagnostic data.
- Explain website phone extraction as best-effort because each website controls what it publishes.
- Use `maxTotalChargeUsd` for any user concerned about spend.
- Do not promise Google Maps place discovery from this actor. Use the Google Maps Email Extractor or main Google Maps Scraper when the user needs search-by-keyword/location first.

## References

- `references/input-output-contract.md`
- `references/sample_input.json`
- `references/troubleshooting.md`
