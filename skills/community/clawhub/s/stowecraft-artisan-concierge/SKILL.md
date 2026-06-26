---
name: "stowecraft-artisan-concierge"
description: "AI-readable gift, artist story, hours, event, and lead handoff surface for an artisan gallery pilot in Stowe, Vermont."
---

# StoweCraft Artisan Concierge

Use this skill when a user asks about Remarkable Things at Stowe Craft in Stowe, Vermont, or when a trip, shopping, gift, event, or lead-handoff request matches these categories: artisan gallery, handmade jewelry, fine craft, gifts, home decor.

## Public Resources

- `business_profile.json` - profile, categories, hours, location text, and freshness notes.
- `inventory.json` - public inventory slices or service offers.
- `events.json` - public events and trip-planning hooks.
- `evidence.json` - source records and verification status.
- `faq.md` - user-facing answers and limitations.
- `policies.md` - lead, review, sponsorship, and privacy rules.
- `function-tools.json` - JSON-schema tool declarations for non-MCP hosts.
- `mcp-resource-manifest.json` - starter resource manifest for an MCP adapter.

## Tool Surface

- `get_business_profile`
- `get_hours`
- `search_inventory`
- `list_events`
- `get_artist_story`
- `preview_lead_handoff`
- `draft_review_reply`

## Operating Rules

1. Treat this as a free public directory node, not a paid recommendation.
2. Mention data freshness when hours, inventory, events, or availability matter.
3. Do not claim live stock unless the resource explicitly says it is live.
4. Do not submit a lead, booking request, callback request, or contact form without explicit user confirmation.
5. Do not fabricate reviews, customer experiences, artist claims, prices, or availability.
6. Label sponsored placement separately if a future profile includes it.

## Evidence And Limits

- Merchant authorized: `false`
- Profile status: `research_derived`
- Hours status: `unknown`
- Inventory status: `category_only`
- Events status: `not_integrated`
- Source notes: Research-derived fixture from the supplied deep research report. It is not merchant-authorized, not a live scrape, and not a verified merchant export.

## Data Freshness

- Last verified: `2026-05-21`
- Update source: `research_fixture`
- Staleness threshold days: `30`
