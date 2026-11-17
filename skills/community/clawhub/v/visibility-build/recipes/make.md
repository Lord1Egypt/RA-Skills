---
id: make
kind: platform
unlocks: [make]
source: https://developers.make.com/custom-apps-documentation, https://developers.make.com/custom-apps-documentation/get-started/make-apps-editor/ai-coding-agent.md, https://developers.make.com/custom-apps-documentation/app-review/prerequisites, https://developers.make.com/custom-apps-documentation/app-review/request-app-review (loaded 2026-11-08)
---
## Smallest version
A Make custom app with a base (API base URL, auth, error handling, sanitization), one API-key connection that hits a real API endpoint to validate, one module per main action from the OpenAPI file, a search module with limit + pagination, and the universal module. Nothing the API does not already do.

## Scaffold
Official path now: an AI coding agent with the Make custom apps skill `https://github.com/integromat/make-apps-skill` and the Make TypeScript SDK (create/update/read app definitions); optional Make Skills (`https://github.com/integromat/make-skills`) + Make MCP server for test scenarios. Needs Node.js 20+, a Make API key, a separate Make team for testing, a sandbox account of the service. The Make Apps Editor VS Code extension is deprecated. Install commands and local file layout are on the Step 1/Step 2 pages, not loaded (unconfirmed).

## Fields the listings check
Mandatory before review ("Custom app code"):
- base and connection sanitize sensitive data (API key/token), have error handling, use an endpoint in the app's API; connection uses the correct URL
- modules have correct labels and descriptions and the correct interface for their output; dates formatted/parsed
- a universal module
- search modules, trigger modules and RPCs have a `limit` parameter and pagination where the API supports it
- every module used in at least one test scenario, run shortly before requesting review (logs expire; no personal data)
- credentials limited to what the connection needs; wraps a service Make does not already integrate (from the review overview search summary, unconfirmed)
Review tab form: link to the service's API documentation, links to scenarios with the app's modules; Make later emails a form asking for the company logo (ISVs).

## Steps
claude: map OpenAPI operations to modules (action/search/trigger) plus the universal module; write base + API-key connection
claude: build and upload the private app with the make-apps-skill + SDK (approve the upload when the skill asks)
human: create the Make API key and the test team; add the test connection with a sandbox API key
human: run every module in a scenario (plus one showing an API error); copy scenario links
claude: fix labels, descriptions, limit/pagination, interfaces flagged by the run
human: remove test modules/connections, set modules visible in the Modules tab
approve: click Publish (cannot be unpublished; public components cannot be deleted)
human: Review tab: API docs URL + scenario links, Request review; answer the QA email thread and logo form

## Delegate
The make-apps-skill above (install it rather than rebuilding it).

## Verify locally
The test scenarios run green in the Make test team for every module; no local command was documented on the pages loaded (unconfirmed).
