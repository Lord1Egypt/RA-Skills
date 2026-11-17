# Web search in an app (Brave, Serper, SerpAPI)

**New, untested in production**: written from the providers' API docs (October 2026); test the route with the student's keys before shipping.

## Fallback order

1. **Brave Search** (`BRAVE_API_KEY`): own index, free monthly allowance, good for general results. `GET https://api.search.brave.com/res/v1/web/search?q=<query>&count=10`, header `X-Subscription-Token: <key>`. Results in `web.results[]` (`title`, `url`, `description`).
2. **Serper** (`SERPER_API_KEY`): Google results, cheap per search. `POST https://google.serper.dev/search`, header `X-API-KEY: <key>`, JSON body `{"q": "<query>", "num": 10}`. Results in `organic[]` (`title`, `link`, `snippet`).
3. **SerpAPI** (`SERPAPI_API_KEY`): most engines (Google, Bing, news, maps), most expensive. `GET https://serpapi.com/search.json?engine=google&q=<query>&api_key=<key>`. Results in `organic_results[]` (`title`, `link`, `snippet`). The key is in the URL, so never log request URLs.

Use the first provider whose key is set; on a timeout (8 s), HTTP 429 or 5xx try the next one. On 401/403 stop and log "key rejected" (the next provider would hide a broken key).

## Shape

- One server file `src/lib/search.ts` exporting `search(query, { limit })` that returns `{ provider, results: [{ title, url, snippet }] }`, so pages never depend on one provider's format.
- One route `src/app/api/search/route.ts`: signed-in users only, query length at most 200 characters, rate limit (see `rate-limit.md`), cache identical queries for an hour (Upstash) to save credits.
- Tests fake each provider's response and the fallback on 429.
- Add the keys with `app-keys.mjs <appDir> BRAVE_API_KEY SERPER_API_KEY` and name the providers in the privacy page (`legal-generate.mjs`).
