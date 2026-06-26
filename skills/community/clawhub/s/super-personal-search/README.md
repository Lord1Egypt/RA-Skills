# Connectify

Connectify is a founder network analytics platform that combines a modern React dashboard with an AI-powered backend for connection discovery, relevance scoring, and action suggestions.

## What It Does

- Shows cross-platform network insights (LinkedIn + Instagram placeholders)
- Renders a clean analytics dashboard with stats, recent connections, network map preview, and suggested actions
- Provides an AI assistant chat panel that can query your network and return top-matching contacts
- Uses Redis caching per session to reduce repeated OpenAI recomputation

## Tech Stack

- Frontend: React + Vite + Tailwind CSS
- Backend: Node.js + Express
- AI: OpenAI API
- Data + cache: Redis
- Deployment: Render (single-service mode supported)

## Project Structure

```text
connectify/
├── src/                         # React dashboard UI
│   ├── components/              # UI components
│   └── data/placeholders.js     # centralized placeholder data
├── server.js                    # Express API + static hosting for built frontend
├── redis.js                     # Redis data + query-context helpers
├── agent.js                     # OpenAI scoring + suggested actions logic
├── apify.js                     # Placeholder data fetch module (Apify stub)
├── .env.example                 # Environment template
└── README.md
```

## Environment Variables

Copy `.env.example` to `.env` and set real values:

```bash
cp .env.example .env
```

Required:

- `OPENAI_API_KEY` - OpenAI API key
- `REDIS_URL` - Redis connection string, e.g. `redis://localhost:6379`
- `APIFY_TOKEN` - token reserved for future live Apify actor integration

Optional:

- `OPENAI_MODEL` (default: `gpt-4.1-mini`)
- `PORT` (default: `3001`)

## Local Development

Install dependencies:

```bash
npm install
```

### Frontend only (Vite dev server)

```bash
npm run dev
```

### Backend only

```bash
npm run dev:server
```

Backend runs on `http://localhost:3001`.

### Production-style local run (single service)

This is the same shape used for Render deployment:

```bash
npm run build
npm start
```

Then open `http://localhost:3001`.

## API Contract

### `POST /api/query`

Request body:

```json
{
  "query": "Who in my network works in AI and is based in SF?",
  "sessionId": "uuid-or-stable-session-id"
}
```

Response body:

```json
{
  "results": [
    {
      "name": "Leila Park",
      "role": "ML Engineer",
      "company": "OpenAI",
      "platforms": ["LinkedIn", "Instagram"],
      "relevanceScore": 92,
      "reason": "Strong AI relevance and SF location match.",
      "suggestedActions": ["Draft intro email", "Share product update"]
    }
  ]
}
```

## Backend Flow

1. Validate `{ query, sessionId }`
2. Check Redis cached context for the same session/query
3. On cache miss:
   - load all connections from Redis
   - score relevance via OpenAI (`agent.scoreConnections`)
   - generate 2 suggested actions per top result (`agent.suggestActions`)
   - cache the query context for 30 minutes
4. Return top 5 ranked results

## Redis Data Model

Connection records are stored as:

- key: `connection:{id}`
- value: JSON object

Query context cache:

- key: `query-context:{sessionId}`
- TTL: 30 minutes

## Apify Integration Stub

`apify.js` currently returns placeholder connection data and is intentionally isolated so you can swap to a real actor call by editing that file only.

```js
// TODO: replace with real Apify actor call using APIFY_TOKEN
```

## Deploying to Render (Hackathon-Friendly)

Create a Render Web Service from this repo and set:

- Build command: `npm install && npm run build`
- Start command: `npm start`
- Environment variables: `OPENAI_API_KEY`, `REDIS_URL`, `APIFY_TOKEN`, optional `OPENAI_MODEL`, `PORT`

The app is configured so Express serves the built frontend (`dist`) and the API from the same origin.

## Current Notes

- The frontend currently uses placeholder records for visual consistency.
- The AI assistant is wired to live backend logic.
- For team demos, deploying the single Render service is the fastest route.

## License

ISC
