---
name: streaming-availability-comparison
description: Compare movie, show, season, and episode viewing offers across countries and providers using Crawlora JustWatch. Use for where-to-watch shortlists or regional availability matrices with subscription, rental, purchase, presentation, title identity, and missing-offer limits preserved.
---

# Streaming availability comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Find viewing offers for specified titles and markets. Establish the exact title,
release year, movie/show/episode scope, countries, preferred providers, language,
presentation quality, and user-supplied subscriptions when relevant.

## Resolve titles and market-specific offers

1. Search in the requested country/language and verify title/year/type. Raw
   JustWatch title IDs are `tm…` for movies or `ts…` for shows, not IMDb/TMDB IDs.
   Similar names, remakes, and translated titles need identity checks before joins.
   Retain the result's canonical title URL and public source metadata.
2. Discover providers separately for each country. Provider catalog identity is
   not proof of availability for the selected title. Preserve country-specific
   short/technical names and IDs rather than assuming identical plans across markets.
3. Fetch title offers for the actual raw ID. `countries` accepts one to five
   comma-separated country codes per call; split a larger requested set and
   retain failed countries explicitly. A country format passing validation does
   not guarantee that every requested provider/title market is available.
4. For a specific season/episode, discover show seasons and season episodes first,
   then use the returned `tse…` episode ID for episode offers. A show-level offer
   does not establish every season/episode is included. Season IDs and title IDs
   are not interchangeable despite related numeric strings.

```sh
scripts/crawlora.sh /justwatch/search query="Inception" country=US language=en limit=5
scripts/crawlora.sh /justwatch/providers country=US
# Use a verified raw title ID before:
# scripts/crawlora.sh /justwatch/title/offers id="$TITLE_ID" countries=US,GB language=en
```

## Compare viewing conditions and deliver

Keep subscription, rental, purchase, free, and ad-supported offers separate,
retaining raw monetization type, presentation, price/currency, provider link,
country, title/episode scope, and observation time. A subscription offer is not
proof it is included in the user's specific plan or without a channel add-on.
Rental duration, accessibility/audio languages, ads, taxes, and regional/device
restrictions remain unknown unless supported by returned/source evidence.

Do not combine different currencies, a full-season purchase with a single episode,
or a rental with permanent access. Use user-supplied plan costs only on their
stated basis; provider catalogs do not supply a full subscription-price model.
Return a title-by-country/provider matrix and a practical shortlist with offer
basis, source/time, and missing-condition columns. A 404 search/detail or an empty
market offer set is a bounded retrieval result, not proof the title is unavailable
on every service. Errors remain unavailable evidence. Do not subscribe, pay,
start playback, or promise geographic restriction bypass from this research task.
