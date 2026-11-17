---
id: albato
kind: platform
unlocks: [albato]
source: https://albato.com/wiki/articles/app-integrators-quick-start-guide (redirected from wiki.albato.com), https://docs.superhuman.com/d/_d05nbksrqQV/_sufTJ (Publication rules link; content not readable) (loaded 2026-11-08)
---
## Smallest version
An Albato app built in the no-code App Integrator: one authorization using the product's API key, 1-3 actions (outgoing HTTP requests to existing endpoints) and one trigger (a webhook if the product has webhooks, otherwise an API polling trigger on a list endpoint sorted by id/date).

## Scaffold
Albato App Integrator (web, no code). Quick-start steps: provide app details (name), add authorization ("select the correct schema and authentication fields" from your API docs), set up triggers and actions, test, then keep private or apply to publish.

## Fields the listings check
- App details: name; logo and description not stated on the quick-start page (unconfirmed).
- Authorization: schema + auth fields; which schema types exist (API key / OAuth 2.0 / Basic) is not named on the page (unconfirmed).
- Triggers: API trigger polls every five minutes and dedupes by IDs or modification dates; webhook trigger fires on requests to a URL that pass the filter (from Albato concepts pages via search summary, unconfirmed).
- Actions: outgoing HTTP request with configured fields/body.
- Publishing: "apply to publish it in the Albato library (subject to review and approval)". The Publication rules doc (linked Coda doc, now docs.superhuman.com) did not render: requirements such as test account, description, logo and review time are unconfirmed.

## Steps
claude: from the OpenAPI/docs, choose the auth scheme, 1-3 actions and one trigger; write the field mapping table (label, API field, type, required) and sample payloads
human: create an Albato account; open App Integrator; enter app details and logo
human: configure authorization, triggers and actions from the mapping table
human: test each trigger/action in a real automation with a test account
claude: draft the app description and the reviewer notes (test account usage)
approve: apply to publish (submit for moderation)

## Verify locally
No local tooling; a test automation in Albato that fires the trigger and runs each action successfully. claude can pre-check each endpoint with `curl -H "Authorization: Bearer <YOUR_API_KEY>" <endpoint>` (adjust to the API's auth header).
