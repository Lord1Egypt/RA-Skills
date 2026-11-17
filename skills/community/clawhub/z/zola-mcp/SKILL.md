---
name: zola
description: This skill should be used when the user asks about Zola wedding planning data. Triggers on phrases like "check Zola", "Zola vendors", "wedding budget", "Zola guests", "RSVP status", "seating chart", "vendor inquiries", "wedding registry", "gift tracker", or any request involving wedding vendors, guest list, budget, seating, events, registry, or inquiry management on Zola.
---

# zola-mcp

MCP server for Zola — 31 tools for managing your entire wedding via the Zola mobile API.

## Tools

### Vendors
- `list_vendors` — List all booked vendors
- `search_vendors` — Search vendors by name/category
- `add_vendor` — Book a new vendor
- `update_vendor` — Update vendor details
- `remove_vendor` — Unbook a vendor

### Budget
- `get_budget` — Budget summary with all items
- `update_budget_item` — Update cost or note

### Guests
- `list_guests` — List all guest groups with stats
- `add_guest` — Add a guest group
- `update_guest_address` — Update mailing address
- `remove_guest` — Remove a guest group

### Seating
- `list_seating_charts` — List charts
- `get_seating_chart` — Chart with tables/seats/occupants
- `list_unseated_guests` — Guests not yet seated
- `assign_seat` — Assign guest to seat

### Inquiries
- `list_inquiries` — All vendor inquiries
- `get_inquiry_conversation` — Full conversation
- `mark_inquiry_read` — Mark as read

### Events & RSVPs
- `list_events` — All events with RSVP counts
- `track_rsvps` — RSVP tracking per event
- `update_event` — Update event details
- `set_event_guests` — Bulk set which guest groups are invited to an event
- `invite_guest_to_event` — Invite one guest or group to an event
- `remove_event_invitation` — Remove an event invitation for a guest or group

### Registry & Gifts
- `get_registry` — Registry items with per-item purchase state (requested vs purchased quantity, `marked_fulfilled`, `availability`, `inconsistent`); paged via `limit`/`offset`
- `get_gift_tracker` — Gifts received and thank-you status
- `reconcile_registry` — Joins the registry against the gift tracker and reports DUPLICATE_RISK (flagged fulfilled but nothing purchased, so still buyable), UNATTRIBUTED (purchased with no order behind it), ORPHAN_ORDER and a MATCHED count

### Discovery
- `get_wedding_dashboard` — Planning overview
- `search_storefronts` — Search marketplace
- `get_storefront` — Full vendor details
- `list_favorites` — Saved vendors
