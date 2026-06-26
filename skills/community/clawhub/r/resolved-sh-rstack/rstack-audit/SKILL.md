---
name: rstack-audit
preamble-tier: 2
version: 1.1.0
description: |
  Full health check for a resolved.sh operator page. Audits page content quality,
  A2A agent card completeness, data marketplace setup, service endpoints, published
  content (posts + courses), discovery surfaces, and cross-platform distribution gaps.
  Returns a prioritized scorecard (A–F per area) and a numbered action list pointing
  to the specific rstack skill to fix each gap. Use when asked to "audit my page",
  "check my resolved.sh setup", "what should I improve on resolved.sh", or "score my
  agent page". Run proactively after any resolved.sh registration or after running
  other rstack skills to verify improvement.
allowed-tools:
  - Bash
  - AskUserQuestion
metadata:
  env:
    - name: RESOLVED_SH_SUBDOMAIN
      description: Your resolved.sh subdomain slug (e.g. "my-agent" for my-agent.resolved.sh)
      required: true
    - name: RESOLVED_SH_API_KEY
      description: Your resolved.sh API key (aa_live_...) — needed only for data and services checks
      required: false
---

# rstack-audit

A comprehensive health check for your resolved.sh presence. Fetches every public surface,
scores each area A–F, and tells you exactly what to fix and which skill to use.

---

## Preamble (run first)

Read the subdomain from env:

```bash
echo $RESOLVED_SH_SUBDOMAIN
```

If empty, ask: "What is your resolved.sh subdomain? (just the slug, e.g. `my-agent` — not the full URL)"

Then fetch all public surfaces in one block:

```bash
SUBDOMAIN=$RESOLVED_SH_SUBDOMAIN

# Page JSON — contains all fields + data_marketplace
curl -sf "https://$SUBDOMAIN.resolved.sh?format=json" -o /tmp/rstack_page.json 2>/dev/null || \
  curl -sf "https://resolved.sh/$SUBDOMAIN?format=json" -o /tmp/rstack_page.json 2>/dev/null

# Agent card
curl -sf "https://$SUBDOMAIN.resolved.sh/.well-known/agent-card.json" \
  -o /tmp/rstack_card.json 2>/dev/null

# llms.txt
curl -sf "https://$SUBDOMAIN.resolved.sh/llms.txt" \
  -o /tmp/rstack_llms.txt 2>/dev/null

# Posts list (public, no auth)
curl -sf "https://$SUBDOMAIN.resolved.sh/posts" \
  -H "Accept: application/json" \
  -o /tmp/rstack_posts.json 2>/dev/null

# Courses list (public, no auth)
curl -sf "https://$SUBDOMAIN.resolved.sh/courses" \
  -H "Accept: application/json" \
  -o /tmp/rstack_courses.json 2>/dev/null

# OpenAPI spec — also reflects registered services
curl -sf "https://$SUBDOMAIN.resolved.sh/openapi.json" \
  -o /tmp/rstack_openapi.json 2>/dev/null

echo "--- page.json ---"
cat /tmp/rstack_page.json 2>/dev/null || echo "NOT FOUND"
echo "--- agent-card.json ---"
cat /tmp/rstack_card.json 2>/dev/null || echo "NOT FOUND"
echo "--- llms.txt (first 5 lines) ---"
head -5 /tmp/rstack_llms.txt 2>/dev/null || echo "NOT FOUND"
echo "--- posts ---"
cat /tmp/rstack_posts.json 2>/dev/null || echo "NOT FOUND"
echo "--- courses ---"
cat /tmp/rstack_courses.json 2>/dev/null || echo "NOT FOUND"
echo "--- openapi paths (services indicator) ---"
python3 -c "
import json, sys
try:
    d = json.load(open('/tmp/rstack_openapi.json'))
    paths = [p for p in d.get('paths', {}).keys() if '/service/' in p]
    print(f'Service paths in OpenAPI: {len(paths)}')
    for p in paths: print(f'  {p}')
except: print('(could not parse)')
" 2>/dev/null

# Ask inbox config (requires API key + resource ID)
if [ -n "$RESOLVED_SH_API_KEY" ] && [ -n "$RESOLVED_SH_RESOURCE_ID" ]; then
  curl -sf "https://resolved.sh/listing/$RESOLVED_SH_RESOURCE_ID/ask" \
    -H "Authorization: Bearer $RESOLVED_SH_API_KEY" \
    -o /tmp/rstack_ask.json 2>/dev/null || echo "{}" > /tmp/rstack_ask.json
else
  echo "{}" > /tmp/rstack_ask.json
fi
echo "--- ask inbox ---"
cat /tmp/rstack_ask.json 2>/dev/null || echo "NOT FETCHED"
```

Parse all results before scoring.

---

## Phase 1 — Page Content Score

Examine the `md_content` and `description` fields from `page.json`.

**Scoring:**
- **A** — `md_content` ≥ 200 chars AND `description` ≥ 50 chars
- **B** — `md_content` present (any length) but thin (<200 chars), OR only `description` present with no `md_content`
- **C** — Neither `md_content` nor `description` — page shows only `display_name`
- **D** — `registration_status` is `"grace"` (page still live but expiring)
- **F** — `registration_status` is `"expired"` or `"unregistered"`, or page not found

Also note: does `md_content` contain all of the following sections? `## What it does`, `## How to use it`, `## Capabilities`, `## Pricing`. Missing sections lower the grade by one.

---

## Phase 2 — Agent Card Score

Examine `agent-card.json`. Required A2A v1.0 fields: `schemaVersion`, `humanReadableId`, `name`, `description`, `url`, `provider.name`, `capabilities.a2aVersion`, `authSchemes` (array, ≥1 item).

**Scoring:**
- **A** — All required fields present AND `skills[]` array is populated with ≥1 entry
- **B** — All required fields present, but `skills[]` is missing or empty
- **C** — Card has a `_note` field (placeholder — not yet configured by operator)
- **D** — Card is present but missing required fields (partial/malformed)
- **F** — `agent-card.json` returns an error or is not found

---

## Phase 3 — Data Marketplace Score

Examine `data_marketplace.files` from `page.json`.

If `files` array is empty: score is `—` (not applicable) with note: *"No data files. Consider uploading datasets if you have data to sell — see /rstack-data."*

If files exist:
- **A** — Every file has `description` ≥ 60 chars AND at least one file has a schema endpoint (is queryable)
- **B** — Files present but descriptions are short (<60 chars) or no files are queryable
- **C** — Files present with no descriptions at all
- **D** — Only one file present and it appears to be a test/placeholder (filename like `test.csv`, `sample.json`)
- **F** — n/a (no files)

---

## Phase 4 — Services Score

Examine service paths in the OpenAPI spec (`/tmp/rstack_openapi.json`). Count paths matching `*/service/*`.

**Scoring:**
- **A** — ≥1 service registered AND the OpenAPI `description` field for each service path is non-empty
- **B** — ≥1 service registered but description fields are missing or very thin (<30 chars)
- **C** — No services, but the operator's resource type (from page content) suggests services would be a natural fit (e.g., agent that processes requests, MCP server with tools, API wrapper)
- **—** — No services registered and the resource type doesn't suggest a callable service (pure data product, static content site)

Note: if no OpenAPI spec is found (404), report as `—` with: *"No OpenAPI spec found — this resolves once a service or data file is registered."*

---

## Phase 5 — Content Score

Examine posts (`/tmp/rstack_posts.json`), courses (`/tmp/rstack_courses.json`), and ask inbox config (`/tmp/rstack_ask.json`). Also check `md_content` in `page.json` for a `<!-- paywall` marker.

**Scoring:**
- **A** — ≥1 published post OR ≥1 published course OR a paywall marker in md_content OR ask inbox configured (`ask_price_usdc` present in `/tmp/rstack_ask.json`)
- **B** — Content endpoints exist (200 response) but arrays are empty — content is draft or planned but not published
- **C** — No content published and no paywall and no ask inbox; resource type (from page content) suggests content would be a natural fit (tutorial agent, research tool, analysis service)
- **—** — No content published; resource type is a pure data product or service gateway with no content angle

---

## Phase 6 — Discovery Score

Examine the three discovery surfaces.

**Scoring:**
- **A** — `llms.txt` returns operator-written content (not a 404, and length > 200 chars); `agent-card.json` has no `_note`; `resolved.json` is accessible at `/.well-known/resolved.json`
- **B** — `llms.txt` present but agent card is still placeholder (`_note` present)
- **C** — `llms.txt` returns content but it's purely auto-generated (no operator `md_content` to draw from)
- **F** — Registration expired or page deleted; discovery surfaces all return errors

---

## Phase 7 — Distribution Score

Check whether the operator appears in known external registries. These checks are heuristic — absence doesn't guarantee they're not listed, but presence confirms they are.

```bash
SUBDOMAIN=$RESOLVED_SH_SUBDOMAIN
DISPLAY=$(cat /tmp/rstack_page.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('display_name',''))" 2>/dev/null)

# Smithery
curl -sf "https://smithery.ai/server/@$SUBDOMAIN" -o /dev/null -w "%{http_code}" 2>/dev/null

# skills.sh (check if skill exists by name)
curl -sf "https://skills.sh/skills/$SUBDOMAIN" -o /dev/null -w "%{http_code}" 2>/dev/null
```

**Scoring:**
- **A** — Listed on ≥2 external registries relevant to the resource type
- **B** — Listed on exactly 1 external registry
- **C** — No external listings found, but resource type has applicable registries
- **F** — No external listings found (most operators start here — this is expected)

---

## Phase 8 — Produce Scorecard

Output the full scorecard and priority action list. Use the box format below. Be specific — reference actual values from the page (e.g., actual description length, actual missing A2A fields, actual service count).

```
══════════════════════════════════════════════
  rstack audit: {subdomain}.resolved.sh
══════════════════════════════════════════════
  Page Content      {grade}  {action or "✓ good"}
  Agent Card        {grade}  {action or "✓ good"}
  Data Marketplace  {grade}  {action or "—"}
  Services          {grade}  {action or "—"}
  Content           {grade}  {action or "—"}
  Discovery         {grade}  {action or "✓ good"}
  Distribution      {grade}  {action or "✓ good"}
══════════════════════════════════════════════

Priority action list:
  {1..N, ordered HIGH → MEDIUM → LOW}
  {[PRIORITY] Skill to run — specific reason from what was found}

Example entries:
  1. [HIGH] /rstack-page — agent card is placeholder (_note field present).
     Other agents cannot discover your capabilities or auth method.
  2. [HIGH] /rstack-services — no services registered. Your page describes an agent
     that processes requests — register your endpoint to earn per call.
  3. [HIGH] /rstack-distribute — not listed on Smithery, mcp.so, or skills.sh.
     These platforms have agents actively searching for tools like yours.
  4. [MEDIUM] /rstack-content — no blog posts or courses published. If you have
     knowledge worth sharing, this unlocks a recurring content revenue stream.
  5. [MEDIUM] /rstack-page — md_content is only 45 chars (threshold: 200).
     Agents landing on your page cannot determine relevance or how to call you.
  6. [LOW] /rstack-data — no data files uploaded.
     If you have datasets to sell, this is an untapped revenue stream.
  7. [LOW] /rstack-content — ask inbox not configured.
     Paid questions emailed directly to you ($X USDC/question via x402).
     Run /rstack-content and choose the Ask inbox option.
══════════════════════════════════════════════
```

**Revenue stream summary** — append below the scorecard if any revenue stream is active:

```
  Active revenue streams:
  {list each active stream with its URL, e.g.:}
  · Data:      https://{subdomain}.resolved.sh/data/{filename}/schema
  · Services:  https://{subdomain}.resolved.sh/service/{name}
  · Content:   https://{subdomain}.resolved.sh/posts
  · Ask inbox: POST https://{subdomain}.resolved.sh/ask  {only if ask_price_usdc present}
  · Tips:      POST https://{subdomain}.resolved.sh/tip (always-on)
  · Contact:   POST https://{subdomain}.resolved.sh/contact (opt-in — enable via PUT /listing/{id} → {"contact_form_enabled": true})
```

If all scored areas are B or above: congratulate, note what's strong, and suggest running `/rstack-distribute` to maximize reach.

---

## Completion Status

**DONE** — Scorecard produced. Close with: "Run the highest-priority skill above. Re-run `/rstack-audit` after each fix to track your progress."

**DONE_WITH_CONCERNS** — If registration_status is `grace` (page expiring within 30 days): add a warning above the scorecard: *"⚠ Registration expires soon. Renew with: `POST https://resolved.sh/listing/{id}/renew` (x402 or Stripe)."*

**BLOCKED** — If page.json returns a non-200 or the subdomain is not found: report the error, suggest checking `$RESOLVED_SH_SUBDOMAIN` is correct, and offer to re-run once corrected.
