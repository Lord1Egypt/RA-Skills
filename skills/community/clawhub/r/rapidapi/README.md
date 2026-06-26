# RapidAPI Universal Skill (Minimal)

Minimal-dependency RapidAPI skill core. No server, no frameworks, no build step.

## What you get
- A universal RapidAPI request engine (no server required)
- Declarative templates that map to stable action names
- Automatic action registration from `templates/*.json`
- A power-user entrypoint: `callRapidApi` for ad‑hoc calls

## When to use this
Use this skill if you want a repeatable, programmatic interface over RapidAPI:
- You need to call the same endpoint across tasks without retyping host/path/method
- You want to document inputs and defaults as a template
- You want to share a portable template library in version control

Not a good fit if you need a long‑running API server or webhooks.

## Install / Use
Node.js 18+ required (uses global `fetch`).

Create `config.json` from `config.example.json` and pass it in:
```json
{
  "rapidApiKey": "your_rapidapi_key",
  "templatesDir": "./templates",
  "timeoutMs": 15000,
  "allowNonRapidApiHosts": true
}
```

Example:
```js
import { createRapidApiSkill } from "./index.js";
import config from "./config.json" assert { type: "json" };

const skill = await createRapidApiSkill({ config });

console.log(skill.listActions());

const res = await skill.callAction("toktok_user_info", { username: "example_user" });
console.log(res);

const direct = await skill.callRapidApi({
  host: "linkedin-data-api.p.rapidapi.com",
  path: "/get-profile",
  method: "GET",
  query: { url: "https://www.linkedin.com/in/example/" }
});
console.log(direct);
```

## Response Shape (stable contract)
Every call returns this shape so callers can handle errors consistently:
```json
{
  "ok": true,
  "status": 200,
  "data": {},
  "meta": { "host": "...", "path": "...", "method": "GET" }
}
```

Errors always follow:
```json
{
  "ok": false,
  "status": 400,
  "error": { "message": "...", "details": {} },
  "meta": { "host": "...", "path": "...", "method": "GET" }
}
```

## How templates map to requests
- `querySchema` → query string params
- `bodySchema` → JSON body (for non‑GET methods)
- `headerSchema` → extra request headers
- `pathParams` → `{param}` substitution in the path

`paramMapping` lets you map a single input into a specific bucket:
```json
{
  "paramMapping": { "profileUrl": "query.url" }
}
```

## OpenClaw compatibility
This skill follows OpenClaw conventions:
- `SKILL.md` with single-line `metadata` JSON
- `metadata.openclaw.primaryEnv` is `RAPIDAPI_KEY`
- You can pass `apiKey` or inject env via `skills.entries.<name>.env` / `apiKey`

Programmatic usage with injected env:
```js
const skill = await createRapidApiSkill({
  apiKey: "sk-xxxx" // maps to primaryEnv
});
```

Programmatic usage with config:
```js
import config from "./config.json" assert { type: "json" };
const skill = await createRapidApiSkill({ config });
```

## Scripts
List actions:
```bash
node scripts/list.js
```

Call a preset action:
```bash
echo '{\"action\":\"toktok_user_info\",\"params\":{\"username\":\"example_user\"}}' | node scripts/call.js
```

Call a direct RapidAPI request:
```bash
echo '{\"rapidapi\":{\"host\":\"linkedin-data-api.p.rapidapi.com\",\"path\":\"/get-profile\",\"method\":\"GET\",\"query\":{\"url\":\"https://www.linkedin.com/in/example/\"}}}' | node scripts/call.js
```

## Import endpoint JSON (auto-generate template)
If you already have a RapidAPI endpoint JSON payload (from the RapidAPI UI or export), you can generate a template file automatically.\n\nThe input must include a top-level `host`.\n\n```bash
echo '{\"host\":\"twitter241.p.rapidapi.com\",\"data\":{\"endpoint\":{\"name\":\"Get User Tweets\",\"method\":\"GET\",\"route\":\"/user-tweets\",\"params\":{\"parameters\":[{\"name\":\"user\",\"condition\":\"REQUIRED\",\"paramType\":\"STRING\"},{\"name\":\"count\",\"condition\":\"REQUIRED\",\"paramType\":\"STRING\",\"value\":\"20\"},{\"name\":\"cursor\",\"condition\":\"OPTIONAL\",\"paramType\":\"STRING\"}]}}}}' | node scripts/import-endpoint.js
```

## Template system
Templates live in `templates/*.json` and are auto-registered at startup.

See details: `docs/template-schema.md`

## Error format
```json
{
  "ok": false,
  "status": 400,
  "error": {
    "message": "Missing required parameter: url",
    "details": {}
  }
}
```

## Security defaults
- Disallows overriding `X-RapidAPI-Key`
- Optional host restriction with `ALLOW_NON_RAPIDAPI_HOSTS=false`
- Method allow-list
- Body size and timeout limits
