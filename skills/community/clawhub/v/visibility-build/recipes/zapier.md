---
id: zapier
kind: platform
unlocks: [zapier]
source: https://docs.zapier.com/integrations/quickstart/ui-tutorial.md, https://docs.zapier.com/integrations/publish/integration-publishing-requirements.md, https://docs.zapier.com/llms.txt (loaded 2026-11-08)
---
Note: no official Zapier page found for building a public integration *from an MCP server* (docs.zapier.com index and searches show only Zapier's own MCP server and the beta "MCP Client" action that consumes remote MCP servers). The catalog's MCP path is unconfirmed; the documented path is a Platform UI integration over the REST API, which still requires the catalog's `test-account`.

## Smallest version
A public Platform UI integration with API Key auth, one polling trigger on the product's main "list new items" endpoint, and 1-3 actions (create / find) mapped to existing endpoints. Same operations the MCP tools already expose.

## Scaffold
developer.zapier.com -> "Start a Zapier Integration" (Platform UI visual builder). CLI alternative not loaded (unconfirmed).

## Fields the listings check
- Create form: Name (exactly as core branding), Description (<=140 chars; starts "<Integration Name> is a..."; no links, no Zapier/other app mentions), Logo (square transparent PNG >=256x256, no app name), Homepage URL (marketing site, not login page; its domain gates team email access), Intended Audience (public/private), Role (relationship to the app), Category.
- Auth types: API Key, Basic, Digest, OAuth v2, Session. Credentials only via the Authentication configuration; no hard-coded secrets.
- Triggers via REST Hooks or polling; actions create/search/update via the API Configuration tab.
- Publishing requirements: you own/are contracted by the API owner; app fully launched (not invite-only/beta); HTTPS production endpoints; API docs supplied; every trigger/action/search tested, each test Zap turned on with a successful run; an admin team member with an email on the app's domain; reviewer test account non-expiring using `integration-testing@zapier.com`, password changeable by Zapier support, paid features enabled; demo video or docs for complex features.
- All Errors and Publishing Tasks validated before publishing; integrations start private (from search summary of the build-guidelines page, unconfirmed).

## Steps
claude: map MCP tools / OpenAPI operations to one trigger and 1-3 actions; write input field specs, sample responses, and the 140-char description
human: developer.zapier.com account; Start a Zapier Integration; fill name, logo, homepage, audience=public, role, category
human: configure API Key auth and the trigger/actions in the Platform UI from claude's specs
human: create the reviewer test account on integration-testing@zapier.com (non-expiring, paid features on)
human: build and turn on a test Zap per trigger/action until each has a successful run, connected to the test account, never a real customer's: an action's test run creates, sends or changes real data in whatever account it is connected to
human: add a teammate with a company-domain email as admin
approve: submit for publishing review

## Verify locally
No local command for Platform UI; the Platform UI auth test passes and each test Zap shows a successful run. claude can pre-check read-only (GET) endpoints with `curl -H "<auth header>: <YOUR_API_KEY>" https://<api>/<endpoint>`, using the test account's key. Never call an action endpoint to check it: that changes live data.
