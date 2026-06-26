# skill-instantly-campaign-launcher

Programmatically create an Instantly.ai cold email campaign with D0/D3/D8 sequences and bulk-import leads — all via Instantly API v2. One script, zero dashboard clicking.

## What it does
1. Creates a new Instantly campaign (or finds an existing one by name)
2. Adds a 3-step D0/D3/D8 email sequence to the campaign
3. Imports leads from a JSON file (with dedup/skip for existing leads)
4. Reports imported/skipped/failed counts

## Use cases
- Launching any cold email campaign via code (no UI required)
- B2B agency or service business outreach
- Quickly adapting a campaign template for new ICPs or industries

## Inputs
- `INSTANTLY_KEY` — Instantly API v2 Bearer token (set as env var)
- `scripts/campaign.config.js` — campaign name, schedule, D0/D3/D8 email bodies
- `leads.json` — array of lead objects: `{email, firstName, lastName, companyName, website}`

## Outputs
- Instantly campaign created (or found) with sequences attached
- Leads imported; console report: total / imported / skipped / failed

## Scripts
- `scripts/campaign-launcher.js` — main entry point
- `scripts/campaign.config.js` — config template (edit before running)

## Usage
```bash
# 1. Get your Instantly API v2 token from app.instantly.ai → Settings → API Keys
export INSTANTLY_KEY=your_token_here

# 2. Edit scripts/campaign.config.js — set campaign name, schedule, email copy
# 3. Create leads.json (array of lead objects)
# 4. Run:
node scripts/campaign-launcher.js --config scripts/campaign.config.js --leads leads.json
```

## leads.json format
```json
[
  { "email": "john@example.com", "firstName": "John", "lastName": "Smith", "companyName": "Acme Inc", "website": "acme.com" },
  { "email": "jane@corp.io", "firstName": "Jane", "companyName": "Corp IO" }
]
```

## campaign.config.js format
```js
module.exports = {
  campaignName: 'My Outreach Campaign',
  schedule: {
    name: 'Business Hours',
    timing: { from: '09:00', to: '17:00' },
    days: { monday: true, tuesday: true, wednesday: true, thursday: true, friday: true, saturday: false, sunday: false },
    timezone: 'America/New_York', // or Asia/Dubai, Europe/London, etc.
  },
  sequences: [
    { step: 1, delay: 0, subject: 'Your subject', body: 'Hi {{firstName}}, ...' },
    { step: 2, delay: 3, subject: 'Re: Your subject', body: 'Follow-up body...' },
    { step: 3, delay: 8, subject: 'Last note, {{firstName}}', body: 'Closing body...' },
  ],
};
```

## Notes
- Instantly API v2 — sequences endpoint: `POST /campaigns/:id/sequences`
- Dedup: 409 responses = lead already in campaign (counted as skipped, not error)
- Rate limit: 200ms sleep between lead imports to avoid 429s
- Known issue: Instantly API v2 `/sequences` endpoint occasionally returns 404 → add sequences manually in dashboard if this occurs
- Instantly free plan supports unlimited campaigns; warming up inboxes recommended before launch
