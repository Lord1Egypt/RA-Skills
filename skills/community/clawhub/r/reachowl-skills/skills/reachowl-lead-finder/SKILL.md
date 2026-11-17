---
name: reachowl-lead-finder
description: "Find and qualify B2B leads (names, titles, emails, phones, social profiles) from public websites and directories with the ReachOwl Lead Finder Apify Actor, then import them into an existing ReachOwl campaign for Facebook, Instagram, or WhatsApp outreach. Use when the user wants to scrape leads from URLs, build a prospect list for a niche and location, or fill a ReachOwl campaign with new leads."
license: MIT
compatibility: Requires an Apify account (APIFY_TOKEN or the Apify MCP server) and the ReachOwl MCP server (https://reachowl.com/mcp).
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://apify.com/superior_couch/reachowl-lead-finder
  tags: reachowl, lead-generation, lead-scraping, apify, prospecting, b2b-leads
---

# ReachOwl Lead Finder

The Apify Actor **finds** leads. ReachOwl MCP **imports** them and runs the outreach.

- Actor: [`superior_couch/reachowl-lead-finder`](https://apify.com/superior_couch/reachowl-lead-finder) (free; you pay Apify platform usage)

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.
- Requires access to Apify: either the Apify MCP server, or an `APIFY_TOKEN` for the REST API.
- Only crawl public pages the user has the right to use, and follow local rules on contacting people (consent, opt-outs).

## Workflow

1. **Confirm the brief**: start URLs, target audience, location, keywords, max leads.
2. **Pick the campaign**: `list_campaigns` and choose an existing one. If none fits, create one first with `reachowl-campaigns` (for example `audience_type: "file_upload"`, `status: 0`).
3. **Run the Actor in scrape-only mode** (`sendToReachOwl: false`):

```json
{
  "startUrls": [{ "url": "https://example.com/agents" }],
  "targetAudience": "real estate agents",
  "location": "Lahore, Pakistan",
  "keywords": ["real estate", "property dealer", "real estate agent"],
  "maxLeads": 100,
  "minLeadScore": 50,
  "sendToReachOwl": false
}
```

   - Apify MCP: call the Actor `superior_couch/reachowl-lead-finder` with this input.
   - REST (short runs): `POST https://api.apify.com/v2/acts/superior_couch~reachowl-lead-finder/run-sync-get-dataset-items` with header `Authorization: Bearer $APIFY_TOKEN` and the JSON above as the body.
   - Other inputs: `maxPagesPerSite` (default 25), `maxRequestsPerCrawl` (default 200), `scoreWeights`.

4. **Review the leads** with the user. Each item has `fullName`, `firstName`, `title`, `company`, `email`, `phone`, `website`, `facebookUrl`, `instagramUrl`, `linkedinUrl`, `sourceUrl`, `matchedKeywords`, `leadScore`.
5. **Import through MCP** with `add_campaign_contacts { campaign_id, audience }`, in batches of up to 500:

| Campaign platform | Keep leads that have | Row |
|-------------------|----------------------|-----|
| whatsapp | `phone` | `{ name: fullName, phone, company, title }` |
| facebook | `facebookUrl` | `{ name: fullName, profile_url: facebookUrl, company, title }` |
| instagram | `instagramUrl` | `{ name: fullName, profile_url: instagramUrl, company, title }` |

   Extra fields (`company`, `title`) become message variables (`{{company}}`, `{{title}}`).

6. **Verify**: `list_contacts { campaign_id }`.
7. **Start outreach** only after the user approves the messages: `reachowl-campaigns` (`update_campaign { id, body: { status: 1 } }`).

## Rules

- Never create a campaign just to hold uploaded leads if one already fits — use `add_campaign_contacts`.
- Importing through MCP uses the user's own ReachOwl token. Don't use the Actor's built-in `sendToReachOwl` import unless the user runs their own copy of the Actor with their `REACHOWL_API_KEY` secret set.
- Report how many leads were found, kept, and imported, and how many were skipped for missing phone or profile URL.
