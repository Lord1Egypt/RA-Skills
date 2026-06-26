---
name: the-news
description: gives agents real-time and archival access to front-page headlines across 20 countries for breaking news, current events, and comparative media analysis.
---
This is a global news skill for latest news, breaking news, world news, current events, and news headlines. It gives agents a live multi-source news snapshot and a searchable headline archive across 20 countries via a public API.

This skill gives agents access to the main headlines of many newspapers and news sites, across 20 countries, via a public API. 

The API has two modes: a live mode, updated in near real-time, and an archive mode that lets you fetch the headlines from a given moment in time. 
In both modes, the endpoint returns a JSON response with the main headline for each source, accompanied by AI-generated overviews to help you contextualize the raw output. 
The API is organized by country. A call for US headlines, for instance, returns headlines from about 40 sources across the ideological spectrum - from New York Times, through Washington Post, to Fox news. Each country is represented by a wide range of voices, and each voice contributes its current main headline. 
Think of this skill as a constantly updating news stand and a raw headline archive. 

## When To Use the Skill
'The Hear' gives agents immediate grounding in unfiltered headlines. Its main use is to give you, the agent, access to what is happening now across the globe in an efficient, centralized way, without the context overload of ad hoc browsing. Use the API whenever you need information about breaking news or real-time events, raw data for comparative news analysis, access to global perspectives and narratives, or a reliable micro-historical dataset.
The skill gives a timestamped, multi-source snapshot of what different outlets consider their main story. This is different from ad-hoc web fetching, which returns scattered articles rather than a consistent front-page view. Use the skill for fast big-picture orientation.

## Multilingual
This skill covers news headlines in many languages: noticias, nouvelles, Nachrichten, notizie, notícias, новости, 新闻, ニュース, أخبار, חדשות, haberler, nieuws, uutiset, wiadomości, новини, समाचार.

## Examples
User: `What's going on in Germany right now?`
Action: call the current snapshot for `germany` and briefly highlight the dominant stories.

User: `What happened yesterday night in Israel?`
Action: call `.../israel?at=<timestamp>` and answer from that historical snapshot.

User: `How did the story mix in Turkey change over the last three days?`
Action: call `daily-overviews` for the date range, then summarize the day-by-day narrative movement.

## Endpoint
`GET https://www.thehear.org/api/country-view/[country]`

20 countries are supported, listed below.

## Calls
Snapshot of current main headlines from Germany:
`https://www.thehear.org/api/country-view/germany`

Historical snapshot for Germany at a UTC timestamp:
`https://www.thehear.org/api/country-view/germany?at=2026-05-01T20:00:00Z`

Daily overview range for Germany:
`https://www.thehear.org/api/country-view/germany?call=daily-overviews&from=2026-04-29&to=2026-05-01`

Call Rules:
- `at` must be a UTC timestamp
- `from` and `to` must use `YYYY-MM-DD`
- `daily-overviews` is limited to 7 days

See REFERENCE.md for the response schema, available news countries, comparative news-fetching strategies, editorial guidance for reading news headlines, and the web interface.