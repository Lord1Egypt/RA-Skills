---
name: supabase-dashboard-builder
description: Build admin dashboards and command centers backed by Supabase REST API with D3.js force graphs, Chart.js visualizations, and vanilla JS. Use when creating data exploration UIs, admin panels, mission control dashboards, or any visualization that reads from Supabase tables. No React/Vue required — pure HTML + JS + CSS with a shared dark-theme shell.
---

# Supabase Dashboard Builder

Build rich admin dashboards using Supabase PostgREST API + vanilla JS + D3/Chart.js. No build step, no framework — just HTML files served by FastAPI StaticFiles.

## Architecture

```
FastAPI Server
├── api.py (thin proxy to Supabase REST)
├── static/
│   ├── shell.js + shell.css (shared theme)
│   ├── dashboard/
│   │   ├── index.html (main page)
│   │   ├── agents.html
│   │   ├── skills.html
│   │   └── ...
```

## Step 1: API Layer

Create a thin FastAPI proxy that wraps Supabase REST calls. This keeps the Supabase key server-side.

```python
import httpx
from fastapi import FastAPI

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}

app = FastAPI()

@app.get("/api/mc/{table}")
async def get_table(table: str, select: str = "*", limit: int = 100, offset: int = 0):
    allowed = {"ai_agents", "skills", "knowledge_vault", "tools", "workflows"}
    if table not in allowed:
        raise HTTPException(403, "Table not allowed")
    url = f"{SUPABASE_URL}/rest/v1/{table}?select={select}&limit={limit}&offset={offset}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers={**HEADERS, "Prefer": "count=exact"})
    return r.json()
```

### Key pattern: Lightweight selects
Tables with large text columns (system_prompt, embeddings) will timeout if you `SELECT *`. Always specify columns:
```
?select=id,name,type,status,created_at
```

Add `select` parameter to every API endpoint and default to lightweight fields.

## Step 2: Shared Shell

Create `shell.js` and `shell.css` that every page imports:

```javascript
// shell.js
function createShell(pageTitle, navItems) {
    // Returns: sidebar (collapsible) + top bar + main content area
    // navItems: [{label, href, icon, active}]
}

function createCard(title, content, footer) {
    // Dark-themed card with header, body, optional footer
}

function createTable(headers, rows, options) {
    // Sortable, searchable table with pagination
}

function mcFetch(endpoint, params = {}) {
    // Wrapper: fetch(`/api/mc/${endpoint}?${new URLSearchParams(params)}`)
    // Handles errors, loading states
}

function createSearchBar(placeholder, onSearch) {
    // Debounced search input
}
```

CSS variables for consistent theming:
```css
:root {
    --bg-primary: #0a0a0f;
    --bg-card: #12121a;
    --bg-hover: #1a1a2e;
    --text-primary: #e0e0e0;
    --text-secondary: #888;
    --accent: #6c63ff;
    --accent-glow: rgba(108, 99, 255, 0.3);
    --border: #2a2a3e;
    --success: #4caf50;
    --warning: #ff9800;
    --danger: #f44336;
}
```

## Step 3: Page Patterns

### Data Grid Page (Agents, Skills, Tools)
```
┌─────────────────────────────┐
│ Search bar + Filter chips    │
├─────────────────────────────┤
│ Stats row (total, active,    │
│ by type)                     │
├─────────────────────────────┤
│ Sortable table or card grid  │
│ with pagination              │
└─────────────────────────────┘
```

### Force Graph Page (System Overview)
Use D3.js force-directed graph:
- Nodes = entities (agents, tools, skills)
- Edges = relationships (agent uses tool, skill teaches concept)
- Color by category, size by importance
- Click node → side panel with details
- Zoom + pan + drag

### Chart Page (Analytics, Metrics)
Use Chart.js:
- Radar charts for multi-dimensional scores
- Line charts for time series
- Bar charts for comparisons
- Doughnut for category breakdown

## Step 4: FastAPI Static Mount

```python
from fastapi.staticfiles import StaticFiles

# Mount AFTER API routes
app.mount("/static/mc", StaticFiles(directory="static/mc"), name="mc-static")

# Convenience page routes
@app.get("/mc/{page}")
async def serve_mc_page(page: str):
    return FileResponse(f"static/mc/{page}")

@app.get("/mc/")
async def serve_mc_index():
    return FileResponse("static/mc/index.html")
```

## Common Bugs & Fixes

1. **Double-prefix in mcFetch**: Agents write `mcFetch('/api/mc/agents')` when mcFetch already prepends `/api/mc/`. Fix: `mcFetch('agents')` or make mcFetch accept both.

2. **CORS issues in dev**: Add CORS middleware if frontend is on different port:
   ```python
   app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
   ```

3. **Supabase timeout on large tables**: Use `select` parameter + `limit` + `offset`. Never `SELECT *` on tables with 1000+ rows or text columns > 1KB.

4. **Chart.js canvas reuse**: Destroy previous chart instance before creating new one on the same canvas, or charts stack invisibly.

## Deployment

Works on any platform that serves Python (Railway, Fly, Render):
- Static files are served by FastAPI — no separate CDN needed
- Supabase key stays server-side in env vars
- No build step — edit HTML, refresh browser
