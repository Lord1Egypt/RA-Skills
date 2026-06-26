# Website Phone Number Finder Input and Output Contract

Default actor:

- Actor ID: `HE8ML7ZqmGI6OtyFU`
- Actor name: `x_guru/website-phone-number-finder`
- Store page: `https://apify.com/x_guru/website-phone-number-finder`

## Input Fields

| Field | Type | Notes |
| --- | --- | --- |
| `domains` | array | Domains or website URLs to scan. Examples: `example.com`, `https://example.com/contact`. |
| `maxResults` | integer | Maximum number of saved website phone results. |
| `resultMode` | string | `phonesOnly`, `contactsOnly`, or `allWebsites`. Default/recommended mode is `phonesOnly`. |
| `maxPagesPerWebsite` | integer | Number of pages to fetch per website. Default is `3`; use `5-10` for deeper phone discovery. |
| `concurrency` | integer | Number of websites scanned in parallel. Default is `100`. |
| `requestTimeoutSecs` | integer | Per-page timeout. Default is `5` seconds. |
| `extractPhones` | boolean | Extract public phone numbers from visible text and `tel:` links. |
| `extractEmails` | boolean | Optionally include public emails as secondary enrichment fields. |
| `extractSocials` | boolean | Extract public Facebook, Instagram, LinkedIn, X/Twitter, YouTube, and TikTok links. |
| `includePersonalData` | boolean | Include personal LinkedIn URLs and person-like emails when optional email extraction is enabled. |
| `sameDomainOnly` | boolean | Follow only same-domain contact/about links. Social profile links are still extracted. |

## Source Rules

- Use `domains` for website domains and URLs.
- Use `phonesOnly` for paid phone lead extraction.
- Use `contactsOnly` when social profiles or optional emails are acceptable even without phones.
- Use `allWebsites` when diagnostics for every submitted site are needed.
- Keep `extractPhones=true` for normal phone scraping.
- Keep `sameDomainOnly=true` unless the user explicitly wants cross-domain crawl behavior.
- If the user needs Google Maps keyword/location discovery first, use the Google Maps Scraper or Google Maps Email Extractor actor instead.

## Budget Guard

Pass `maxTotalChargeUsd` as an Apify run option, not inside actor input. The included script exposes it as `--budget-usd`.

The actor uses the `website-phone-saved` PPE event for saved website phone results and respects available run budget. It finishes successfully and writes `RUN_SUMMARY` when budget, filters, or input exhaustion stop the run.

## Dataset Output Fields

Each dataset item is one website phone result.

| Group | Fields |
| --- | --- |
| Website identity | `input`, `url`, `domain`, `status` |
| Phones | `phones`, `phoneDetails.phone`, `phoneDetails.sourceUrl` |
| Optional emails | `emails`, `emailDetails.email`, `emailDetails.type`, `emailDetails.sourceUrl`, `emailDetails.domainMatch` |
| Social profiles | `socialLinks`, `facebooks`, `instagrams`, `linkedIns`, `twitters`, `youtubes`, `tiktoks` |
| Contact counts | `contactSignals.phones`, `contactSignals.emails`, `contactSignals.socialProfiles`, `contactSignals.pagesFetched` |
| Crawl diagnostics | `pagesFetched`, `fetchedUrls`, `httpStatusCodes`, `errors`, `durationMs` |

The actor output page also exposes:

- `results`: default dataset URL
- `summary`: key-value store URL for `RUN_SUMMARY`

## Response Guidance

- Missing phones are normal in `contactsOnly` and `allWebsites`; in `phonesOnly`, rows should only be saved when a phone number is present.
- `phoneDetails.sourceUrl` shows the page where the phone number was found.
- If a run returns fewer rows than requested, check `RUN_SUMMARY` for `exhaustionReason`, budget, filters, and failed website count.
- Public website phone extraction is best-effort because every website is different.
