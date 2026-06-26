---
name: connectify
description: Build, debug, and extend the Connectify founder network platform (React/Vite frontend + Express backend + Redis cache + OpenAI ranking + Apify ingestion). Use when working in this repository to run local development, modify `/api/query`, tune scoring and suggested actions, replace placeholder connection ingestion with real Apify actor calls, or troubleshoot frontend/backend data flow.
---

# Connectify Development Guide

## Set up the project

1. Install dependencies:
   ```bash
   npm install
   ```
2. Create `.env` from `.env.example` and set:
   - `OPENAI_API_KEY`
   - `REDIS_URL`
   - `APIFY_TOKEN`
   - optional `OPENAI_MODEL`, `PORT`
3. Start Redis before running the backend.

## Run the app

Prefer single-service mode when validating full user flows (dashboard + chat + API):

```bash
npm run build
npm start
```

Open `http://localhost:3001`.

Use split mode only when focusing on one side:

- Frontend only: `npm run dev`
- Backend only: `npm run dev:server`

## Use the file map

- `server.js`: Express API, Redis seeding, `/api/query`, static hosting of `dist/`.
- `agent.js`: OpenAI relevance scoring and follow-up action generation.
- `redis.js`: Redis connection lifecycle, connection storage, query-context cache (30 min TTL).
- `apify.js`: Connection ingestion adapter (currently placeholder dataset).
- `src/components/AIChatPanel.jsx`: chat UX and `/api/query` client call.
- `src/data/placeholders.js`: dashboard placeholder cards/lists/map seed data.

## Preserve the backend response contract

Return this shape from `/api/query`:

```json
{
  "results": [
    {
      "name": "string",
      "role": "string",
      "company": "string",
      "platforms": ["string"],
      "relevanceScore": 0,
      "reason": "string",
      "suggestedActions": ["string", "string"]
    }
  ]
}
```

If changing fields, update both `server.js` and `src/components/AIChatPanel.jsx` together.

## Implement real Apify ingestion

When replacing the stub in `apify.js`:

1. Keep output normalized to this connection schema:
   - `id`, `name`, `role`, `company`, `location`, `platforms`, `tags`, `lastInteraction`, `notes`
2. Keep IDs stable and unique to prevent duplicate Redis records.
3. Return an array compatible with `saveConnection(connection.id, connection)`.
4. Keep actor/network logic isolated in `apify.js`; avoid spreading Apify-specific code through `server.js`.

## Tune AI behavior safely

When editing `agent.js`:

1. Keep `response_format: { type: 'json_object' }`.
2. Keep strict parsing and fallback handling (`safeJsonParse`, bounded score 0-100).
3. Keep deterministic-ish scoring temperature low and action generation temperature moderate.
4. Preserve fallback actions in `server.js` if action generation fails.

## Validate changes quickly

1. Build frontend:
   ```bash
   npm run build
   ```
2. Start server:
   ```bash
   npm start
   ```
3. Smoke test query endpoint:
   ```bash
   curl -X POST http://localhost:3001/api/query \
     -H "Content-Type: application/json" \
     -d "{\"query\":\"Who in my network works in AI and is based in SF?\",\"sessionId\":\"local-test-session\"}"
   ```
4. Confirm the response includes ranked `results` and cached repeat requests return quickly.

## Watch for common pitfalls

- `npm run dev` serves only frontend; `/api/query` will not work there unless a proxy/backend is also configured.
- `server.js` CORS currently allows `http://localhost:3000`; adjust if using different local origins.
- `redis.js` uses `keys('connection:*')`; avoid very large production datasets without pagination/scans.
- Do not commit secrets from `.env` or hardcode API tokens.
