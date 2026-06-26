# Website Email Scraper Input and Output Contract

Default actor:

- Actor ID: `kWfD7C0WpHtIt8VAh`
- Actor name: `x_guru/website-email-phone-finder`
- Store page: `https://apify.com/x_guru/website-email-phone-finder`

## Input Fields

| Field | Type | Notes |
| --- | --- | --- |
| `domains` | array | Domains or website URLs to scan. Examples: `example.com`, `https://example.com/contact`. |
| `maxResults` | integer | Maximum number of saved website contact results. |
| `resultMode` | string | `emailsOnly`, `contactsOnly`, or `allWebsites`. Default/recommended mode is `emailsOnly`. |
| `maxPagesPerWebsite` | integer | Number of pages to fetch per website. Default is `3`; use `5-10` for deeper contact-page discovery. |
| `concurrency` | integer | Number of websites scanned in parallel. Default is `100`. |
| `requestTimeoutSecs` | integer | Per-page timeout. Default is `5` seconds. |
| `extractPhones` | boolean | Extract public phone numbers from visible text and `tel:` links. |
| `extractSocials` | boolean | Extract public Facebook, Instagram, LinkedIn, X/Twitter, YouTube, and TikTok links. |
| `includePersonalData` | boolean | Include person-like emails and personal LinkedIn URLs found on public websites. |
| `sameDomainOnly` | boolean | Follow only same-domain contact/about links. Social profile links are still extracted. |

## Source Rules

- Use `domains` for website domains and URLs.
- Use `emailsOnly` for paid email lead extraction.
- Use `contactsOnly` when phone numbers or social profiles are acceptable even without emails.
- Use `allWebsites` when diagnostics for every submitted site are needed.
- Keep `sameDomainOnly=true` unless the user explicitly wants cross-domain crawl behavior.
- If the user needs Google Maps keyword/location discovery first, use the Google Maps Email Extractor actor instead.

## Budget Guard

Pass `maxTotalChargeUsd` as an Apify run option, not inside actor input. The included script exposes it as `--budget-usd`.

The actor uses the `website-contact-saved` PPE event for saved website contact results and respects available run budget. It finishes successfully and writes `RUN_SUMMARY` when budget, filters, or input exhaustion stop the run.

## Dataset Output Fields

Each dataset item is one website contact result.

| Group | Fields |
| --- | --- |
| Website identity | `input`, `url`, `domain`, `status` |
| Emails | `emails`, `emailDetails.email`, `emailDetails.type`, `emailDetails.sourceUrl`, `emailDetails.domainMatch` |
| Phones | `phones` |
| Social profiles | `socialLinks`, `facebooks`, `instagrams`, `linkedIns`, `twitters`, `youtubes`, `tiktoks` |
| Contact counts | `contactSignals.emails`, `contactSignals.phones`, `contactSignals.socialProfiles`, `contactSignals.pagesFetched` |
| Crawl diagnostics | `pagesFetched`, `fetchedUrls`, `httpStatusCodes`, `errors`, `durationMs` |

The actor output page also exposes:

- `results`: default dataset URL
- `summary`: key-value store URL for `RUN_SUMMARY`

## Response Guidance

- Missing emails are normal in `contactsOnly` and `allWebsites`; in `emailsOnly`, rows should only be saved when an email is present.
- `emailDetails.type` can be `role`, `personal`, or `unknown`.
- `domainMatch=false` means the email was found on a source whose domain does not clearly match the submitted website.
- If a run returns fewer rows than requested, check `RUN_SUMMARY` for `exhaustionReason`, budget, filters, and failed website count.
- Public website contact extraction is best-effort because every website is different.
