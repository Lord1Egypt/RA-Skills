---
name: rapidapi-universal-skill
description: Template-driven RapidAPI client with auto-registered actions and a universal call entrypoint
metadata: {"openclaw":{"requires":{"env":["RAPIDAPI_KEY"]},"primaryEnv":"RAPIDAPI_KEY"}}
---

Use `{baseDir}/index.js` to call RapidAPI with templates from `{baseDir}/templates`.
Prefer this skill when the task involves RapidAPI endpoints or template-defined actions.

## What This Skill Actually Does
This skill is a minimal RapidAPI client that turns RapidAPI endpoint definitions into callable actions.
It is meant for:
- converting a RapidAPI endpoint into a stable action name
- standardizing inputs into query/body/header/path params
- returning a consistent `ok/status/data/error/meta` shape

It is not a server. It is a small local client you can call from scripts or other skills.

## Key Capabilities
- Auto-registers templates from `{baseDir}/templates/*.json`
- `listActions()` enumerates all registered actions with schemas
- `callAction(name, params)` calls a template-defined endpoint
- `callRapidApi(payload)` allows direct RapidAPI calls without a template
- `scripts/import-endpoint.js` converts a RapidAPI endpoint JSON payload into a template file

## Basic Usage
Use config-driven init (recommended):
```js
import { createRapidApiSkill } from "{baseDir}/index.js";
import config from "{baseDir}/config.json" assert { type: "json" };

const skill = await createRapidApiSkill({ config });
const res = await skill.callAction("get_user_tweets", {
  user: "2455740283",
  count: 20
});
```

Or direct call (no template):
```js
const skill = await createRapidApiSkill({ config });
const res = await skill.callRapidApi({
  host: "twitter241.p.rapidapi.com",
  path: "/user-tweets",
  method: "GET",
  query: { user: "2455740283", count: 20 }
});
```

## Template Design Notes
Templates are plain JSON. They should contain:
- `name`, `host`, `path`, `method`
- `querySchema` (and optionally `bodySchema`, `headerSchema`, `pathParams`)

Example snippet:
```json
{
  "name": "get_user_tweets",
  "host": "twitter241.p.rapidapi.com",
  "path": "/user-tweets",
  "method": "GET",
  "querySchema": {
    "user": {"type": "string", "required": true},
    "count": {"type": "number", "required": true},
    "cursor": {"type": "string"}
  }
}
```

## Where It Fits
Use this skill when you need a consistent, reusable RapidAPI interface without building a backend.
It is especially useful for:
- social data APIs (X/Twitter, TikTok, LinkedIn)
- search/aggregation APIs
- repeated RapidAPI calls across multiple tasks or workflows
