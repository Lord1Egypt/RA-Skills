# SMB Sales Boost - Agent Skill for Claude Code and OpenClaw

> **Note for AI agents:** This file and the other files in this skill folder may be truncated when opened. Always read files fully, in chunks if necessary, so that no instructions, endpoints or examples are missed. The agent instructions are in `SKILL.md` and `REFERENCE.md`.

Find and export growing local businesses with plain-language requests. This skill connects an AI agent (Claude Code, OpenClaw and other agents that support skills) to the [SMB Sales Boost](https://smbsalesboost.com) lead database of small and medium-sized businesses in the United States. Every lead carries a **Last Buying Signal**, the date something changed that makes the business worth contacting now: it was newly added, or it got a new phone number, email address or address, or added or changed a social profile.

Ask things like "find med spas in Florida with a buying signal this week", "export 500 dental practices in Texas, spend at most 300 credits" or "get the contact details for these 200 websites", and the agent turns them into the right API calls.

## What's new in version 1.9.6 (October 2026)

Long-running calls no longer hit the 100-second network timeout:

- **Background jobs:** `POST /leads/export`, `POST /email-schedules/{id}/trigger`, `POST /ai/suggest-categories` and the three `POST /lead-export-history/...` calls now answer as usual when they finish within about 75 seconds, and otherwise answer `202` with a `jobId` while the work keeps running on the server. The script follows the job with the new `GET /jobs/{jobId}` endpoint (progress is printed on stderr) and then handles the final answer exactly like before: exports and files are saved the same way.
- **Safe retries:** each of these calls sends an idempotency key and prints it. If a call times out, re-running the same command with `--idempotency-key` set to that value returns the same job instead of exporting or sending again (the server keeps the key with the job for up to about 25 hours after it finishes, about 48 hours for a schedule trigger; a server restart forgets it).
- **New options:** `--async` (answer `202` at once and print the `jobId`), `--no-wait` (print the `jobId` instead of following a `202`) and `--job-timeout SEC` (how long to follow a job, default 3600). `GET /jobs/{jobId}` can also be called directly; it waits for the result and saves any file.
- **New answers:** `409 schedule_run_in_progress` when a schedule's regular run is sending it at that moment (nothing was sent), `429 job_capacity_busy` and, for exports and lead searches, `429 charge_in_progress` (nothing was charged), `410 job_result_expired` once a finished result is no longer kept (for about a day, then `404 job_not_found`; never repeat an export or a send then, check what it already did first), and `503 schema_types_warming` from `GET /leads/other/schema-types` right after a server restart. `REFERENCE.md` section 16 has the details, and `openapi.json` matches the live API.

## What's new in version 1.9.5 (October 2026)

- Version number only: this release has the same content as 1.9.4 and is published as 1.9.5. `smb_api.py --version` and the User-Agent the script sends now report 1.9.5.

## What's new in version 1.9.4 (October 2026)

Updated for this month's integration changes:

- **`lead.updated` only for real changes:** it is now sent when a lead you already received reaches your account again with a newer Last Buying Signal than when you last received it (an export or email schedule that includes it, a push to another integration, or a `GET /leads` page or MCP `search_leads` call that returns it), or when a Lead Export History refresh finds that newer data (except for leads on your export blacklist). Receiving an unchanged lead again sends nothing.
- **Fuller event samples:** `export.completed` and `email_schedule.sent` now fill in `sampleLeads` (up to 5 leads, each with id, companyName, website, email, phone, city and state); before, only the id had a value.
- **One lead shape for webhooks:** a `leadId` push to a webhook sends the same flat lead summary as a live `lead.created` event, with source `crm_push`. A push of your own data still sends `{"lead": <your object as sent>, "source": "manual_push"}`.
- **HubSpot Companies:** HubSpot integrations create or update Contacts matched by email (a lead without an email creates no Contact) and Companies matched by website domain, or by exact company name when the lead has no website of its own (none, or a social or listing page such as Facebook or Yelp), and link each Contact to its Company. Before, every delivery added a new Company. If HubSpot does not confirm which account you signed in to, a connection now stops with nothing connected or changed: try again a minute later.
- **Reconnect a CRM:** connecting a CRM account that is already connected re-authorizes that integration in place: it gets new access, a `needs_attention` integration becomes connected again, a paused one stays paused, and its events, field mapping, Pipedrive deal settings and delivery history are kept. The 25-integration limit applies only to new connections. The agent uses this when a CRM integration needs attention because its access was removed or expired, and the dashboard has a Reconnect button for each CRM integration.
- **CRM events and pacing:** HubSpot, Salesforce and Pipedrive integrations take only `lead.created` and `lead.updated`; a subscription to any other event returns `400 validation_error`. Deliveries to these CRMs are sent at most 3 at a time per integration, and HubSpot calls are paced to HubSpot's rate limits, so a large export reaches the CRM gradually.
- **Every push and retry counts:** every push (HubSpot and Salesforce included) is recorded in the integration's deliveries and counts toward `needs_attention` like any other delivery, and so does a retry that could not reach the destination.
- **Lead export history:** on refresh and refresh-and-export, an invalid date or filter value returns `400` with a message naming it (an invalid date used to cause a server error), and refresh-and-export checks everything before it changes any entry.
- `smb_api.py --version` and the User-Agent the script sends now report 1.9.4.

## What's new in version 1.9.3 (October 2026)

- **Version numbers match the GitHub releases:** what earlier notes called 2.1.0 is 1.9.2, and 2.0.0 is 1.9.1. `smb_api.py --version` and the User-Agent the script sends now report 1.9.3.
- **Safer deletes:** before deleting a saved search (filter preset), the agent names the email schedules that will be deleted with it. When you only want something to stop, it offers to pause it instead: a paused email schedule keeps its list of recipients who unsubscribed, and a paused integration keeps its delivery log and signing secret. The script's confirmation messages say the same.
- **Lost signing secret:** before deleting a webhook integration to get a new secret, the agent reads it and shows you its destination and events, then recreates it with the same values after you approve.

## What's new in version 1.9.2 (October 2026)

- **Integrations through the API:** the agent can now list, create and manage CRM and webhook integrations (HubSpot, Salesforce, Pipedrive, Zapier, n8n, Make, Pipedream, Clay and any webhook URL), send a test event, push a lead, read the delivery log and set up CRM field mappings. Integrations send lead data, including business contact details, to systems outside SMB Sales Boost, so the agent describes the destination and asks for your approval first, and every call that sets one up or sends data through it needs `--confirm`.
- **Owner safeguards:** the dashboard shows which API key created or last re-pointed each integration (pausing it, or resuming it in the dashboard, keeps that label). When an API key creates a webhook integration, connects a CRM, changes where an integration sends data, adds events or re-enables one, the account owner is emailed for each change; during bursts of more than 10 changes in an hour, further changes are combined into summary emails. When you revoke an API key you can also pause every integration that key set up, and a CRM connect link the key asked for stops working.
- **Credit caps enforced by the script:** `GET /leads` and `POST /leads/export` without `maxCredits` now need `--confirm`, and a `maxCredits` of `null`, a negative number, a decimal, `true`/`false` or text is refused before anything is sent (previously a `null` cap on an export was silently removed). On `GET /leads`, `limit` must be one whole number from 1 to 1000 (the API reads `0` as a page of 100, so the script refuses it).
- **No automatic retries for integration changes:** a `429` or `503` on a call that creates, changes or sends through an integration is returned with advice (check `GET /integrations` or the delivery log first) instead of being repeated by the script.
- Clearer advice after a timeout (for example, check `GET /integrations` before creating a webhook again: the same URL returns `409 integration_exists`, a changed URL creates a second integration with its own signing secret, and a lost secret means delete and create again), a `--help` list of every call that needs `--confirm`, and the skill metadata now declares `python3` and the homepage.

## What's new in version 1.9.1 (October 2026)

- Updated for the current API: buying-signal names and filters (`lastBuyingSignalFrom`, `buyingSignalTypeFilter`, "Last Buying Signal" and "Buying Signal Type"), the current lead fields (Total Phones, Tier 1-6 emails, founders, software, ad pixels, ratings and more) and dozens of new filters.
- New features: URL enrichment, 90-day export history with direct downloads, free re-export of leads you already received, the overage budget, and the 14-day free trial (including trial plan switching and early activation).
- One lead database: the former Home Improvement database was retired, so every request uses the Main database.
- Correct rate limits (600 requests per minute; 5 exports per minute) and error handling.
- `smb_api.py` rewritten: no third-party packages; CSV and JSON exports now save correctly (previously only XLSX did); downloads are saved instead of discarded; safe, bounded retries; a `--confirm` safety gate for purchases, plan changes, automatic charges, enrichments, sending email and deleting data (searches and exports spend credits without it, so the agent previews first and caps each one with `maxCredits`); `--dry-run`, `--compact` and `--out` options; the API key is read from the environment.
- New `REFERENCE.md` with every parameter, field, status and error, so `SKILL.md` stays short.

## Installation

The skill is a folder:

```
smb-sales-boost/
├── SKILL.md        Agent instructions (with OpenClaw metadata)
├── REFERENCE.md    Complete API details for the agent
├── smb_api.py      API client (Python 3.8+, standard library only)
├── openapi.json    Published OpenAPI 3.1 specification (reference)
├── README.md       This file
└── LICENSE
```

**Claude Code:** copy the folder to `~/.claude/skills/smb-sales-boost/` (available in every project) or to `.claude/skills/smb-sales-boost/` inside a project.

```bash
git clone https://github.com/Tomsonx232/smb-sales-boost-skill.git ~/.claude/skills/smb-sales-boost
```

**OpenClaw:** place the folder in your skills directory, for example `<workspace>/skills/smb-sales-boost/`.

## Requirements

- An SMB Sales Boost subscription: Starter, Growth, Scale, Platinum or Enterprise (an active free trial works too). New customers can also subscribe through the API; the agent can start the checkout for you.
- An API key from the dashboard: [Dashboard > API](https://smbsalesboost.com/dashboard?tab=api). Keys start with `smbk_`.
- Python 3.8 or newer. No packages to install. On Windows the agent runs it with `py -3` and passes JSON in files.

## Configuration

Set the API key as an environment variable before starting your agent:

```bash
export SMB_SALES_BOOST_API_KEY="smbk_your_key_here"
```

For OpenClaw, the skill declares `SMB_SALES_BOOST_API_KEY` as its required variable (`metadata.openclaw.requires.env` and `primaryEnv` in `SKILL.md`) and `python3` as its required program (`requires.bins`). You can configure it in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "smb-sales-boost": {
        "enabled": true,
        "apiKey": { "source": "env", "provider": "default", "id": "SMB_SALES_BOOST_API_KEY" },
        "env": {
          "SMB_SALES_BOOST_API_KEY": "smbk_your_key_here"
        }
      }
    }
  }
}
```

Optional: set `SMB_SALES_BOOST_OUTPUT_DIR` to choose where exported files are saved. Otherwise they go to `/mnt/user-data/outputs` when that folder exists, or to `./smb-sales-boost-files`.

Never paste your API key into a chat, a shared document or version control.

## What you can ask

- **Search:** "Find new dental practices in Texas", "Auto repair shops in Chicago that just got a new phone number", "Bakeries and caterers in New York, excluding franchises"
- **Buying signals:** "Show me businesses with a buying signal in the last 7 days", "Only businesses that just added an email address"
- **Preview for free:** "How many med spas are in Florida?" (masked contacts, no credits)
- **Control spending:** "Search but spend at most 25 credits", "Show me only leads I already bought" (free)
- **Export:** "Export these leads as a CSV", "Export only leads I don't have yet", "Export as XLSX with my saved format"
- **Re-download:** "Download my export from last week", "Re-export the leads I bought in September" (free)
- **Enrich websites:** "Get the phone numbers and emails for these 200 websites"
- **Automate:** "Email new HVAC leads in Ohio to my team every day", "Split leads evenly among my reps"
- **Keywords and categories:** "What kinds of businesses should I target?", "Turn on auto-refine for my keyword list"
- **Integrations:** "Send every new lead to my Zapier webhook", "Connect my HubSpot", "Are my integrations working?", "Reconnect my HubSpot", "Pause the Make integration"
- **Account:** "How many credits do I have?", "Buy 1,000 more credits", "Upgrade to Growth", "Set up auto top-up", "Cancel my subscription"
- **Sign up:** "I want to start a Starter trial"

## Plans and credits

| Plan | Price / month | Credits / month | Extra credits | Free trial |
|---|---|---|---|---|
| Starter | $49 | 500 | $0.10 each | 14 days, 250 credits |
| Growth | $149 | 2,000 | $0.075 each | 14 days, 1,000 credits |
| Scale | $499 | 10,000 | $0.05 each | 14 days, 5,000 credits |
| Platinum | $1,999 | 100,000 | $0.03 each | No |
| Enterprise | $4,999 | 250,000 | $0.02 each | No |

- Each **new** lead you search or export costs 1 credit. Leads you already received are free to get again, and previews are always free.
- Unused credits roll over while your subscription is active. A downgrade makes the whole remaining balance (including purchased credits) expire at the next renewal, and cancelling forfeits it when the subscription ends.
- Free trial: a payment method is required. The plan price is not charged until day 14, when it is charged automatically unless you cancel first. Credits you buy during the trial, and activating the plan early, are charged right away. One trial per person.
- URL enrichment: 1 credit per new database match, 0.1 credit per website fetched live, nothing for URLs that return no data.
- All charges are final; there are no refunds.

## Safety by design

- **Your approval for anything that costs money.** The agent must ask before buying credits, changing plans, starting a subscription checkout, turning on automatic charges (auto top-up, overage budget) or starting an enrichment. The client script refuses these calls unless the agent adds `--confirm`, which the instructions allow only after you approve.
- **Your approval before emailing anyone or deleting anything.** Email schedules are created paused for your review; sending, cancelling, deleting and keyword regeneration also need `--confirm`.
- **Your approval before lead data leaves SMB Sales Boost.** Creating a webhook integration, connecting a CRM, pointing an integration at a new destination, re-enabling it, changing the header API key it sends, pushing a lead, sending a test event, retrying a delivery and changing or testing a CRM field mapping all need `--confirm`, after the agent has told you where the data goes. When an API key creates or re-points an integration, the account owner is emailed for each change; during bursts of more than 10 changes in an hour, further changes are combined into summary emails. The webhook signing secret is shown once and the script never saves it to a file.
- **Credit caps.** The agent previews first for free and sets a credit limit on every search and export. The script refuses an uncapped search or export unless you approved it, and refuses a cap that the API would ignore.
- **Safe retries.** Only rate-limit and temporary-unavailability errors are retried automatically, and never on a call that creates, changes or sends through an integration. A request that may have charged or sent data is never repeated blindly; the script explains how to check first. Exports, schedule triggers and the other long-running calls carry an idempotency key, so re-running a timed-out call with that key returns the same job instead of charging or sending again.

## Security

- **No shell injection:** every call goes through `smb_api.py`, which sends structured JSON over HTTPS. User text is never built into a shell command (text containing quotes is passed in a file).
- **Fixed destination:** requests go only to `https://smbsalesboost.com/api/v1`. Endpoints are validated, redirects are never followed, and the key is never sent to the public sign-up endpoints. Short-lived download links are fetched without the key, over HTTPS, and only from Amazon S3 (`amazonaws.com`) hosts; they are not printed unless the agent explicitly asks for the link instead of the file (`--no-fetch`).
- **Safe files:** file names from the server are reduced to a plain base name with a `.csv`, `.json` or `.xlsx` extension and written only inside the output folder, as new files readable only by you (existing files are never overwritten).
- **Key protection:** the key is read from `SMB_SALES_BOOST_API_KEY` and sent only in the `Authorization` header. It is never printed, logged or saved.
- **Personal data:** exported files contain business phone numbers and email addresses. Keep them in a secure location and do not share them publicly.

## Verifying the published files

SMB Sales Boost publishes the SHA-256 digest of each file in this skill except LICENSE at [https://smbsalesboost.com/.well-known/agent-skills/index.json](https://smbsalesboost.com/.well-known/agent-skills/index.json). To check your copy:

```bash
sha256sum SKILL.md REFERENCE.md README.md smb_api.py openapi.json
```

## Also available

- **MCP server:** a remote Model Context Protocol server at `https://smbsalesboost.com/mcp` (Bearer API key). Details: [server card](https://smbsalesboost.com/.well-known/mcp/server-card.json).
- **API documentation:** [https://smbsalesboost.com/docs/api](https://smbsalesboost.com/docs/api) and the [OpenAPI specification](https://smbsalesboost.com/openapi.json).
- **Dashboard-only features:** API key management (including pausing the integrations a key set up when you revoke it), billing details and undoing a cancellation.

## Data accuracy

Lead data comes from publicly available sources and is not verified. Phone numbers and email addresses are not checked for deliverability, and figures such as revenue, employee counts and ratings are estimates. Verify important details before relying on them.

## Support

support@smbsalesboost.com - https://smbsalesboost.com

## License

MIT - see `LICENSE`.
