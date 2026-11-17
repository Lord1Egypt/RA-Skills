---
name: zola
description: This skill should be used when the user asks about Zola wedding planning data. Triggers on phrases like "check Zola", "Zola vendors", "wedding budget", "Zola guests", "RSVP status", "seating chart", "vendor inquiries", "wedding registry", "gift tracker", "wedding website", "Zola FAQ", "invitations", "save the dates", or any request involving wedding vendors, guest list, budget, seating, events, registry, inquiries, the wedding website or invitation projects on Zola.
---

# zola-mcp

MCP server for Zola — 77 tools for managing your entire wedding via the Zola mobile API.

## Tools

### Vendors
- `list_vendors` — List all booked vendors
- `search_vendors` — Search vendors by name/category
- `add_vendor` — Book a new vendor
- `update_vendor` — Update vendor details
- `remove_vendor` — Unbook a vendor

### Budget
- `get_budget` — Budget summary with all items; `view: "brief"` gives one line per scheduled vendor payment (due date, paid/due)
- `update_budget_item` — Update cost or note

### Guests
- `list_guests` — List all guest groups with stats — names, tier and RSVP state by default; `view: "full"` adds addresses, emails and phones
- `add_guest` — Add a guest group (household) with optional partner, address and event invitations
- `update_guest_address` — Update mailing address
- `remove_guest` — Remove a guest group (with its RSVPs and seats)

### Seating
- `list_seating_charts` — List seating charts
- `get_seating_chart` — Chart with tables/seats/occupants
- `list_unseated_guests` — Guests not yet seated
- `assign_seat` — Assign guest to a seat

### Inquiries
- `list_inquiries` — All vendor inquiries with status; `view: "brief"` gives one line per vendor (last update, read/unread)
- `get_inquiry_conversation` — Full conversation messages
- `mark_inquiry_read` — Mark as read

### Events & RSVPs
- `list_events` — All events with RSVP counts; `view: "brief"` gives one line per event (start time, RSVP counts)
- `track_rsvps` — RSVP tracking per event
- `get_gift_tracker` — Gifts received, thank-you status
- `get_registry` — Registry items with per-item purchase state (`requested_qty`, `purchased_qty`, `marked_fulfilled`, `availability`, `inconsistent`); paged via `limit`/`offset`
- `update_event` — Update event details
- `set_event_guests` — Set which guest groups are invited to an event (bulk)
- `invite_guest_to_event` — Invite a single guest or guest group to an event (additive — does not affect other events)
- `remove_event_invitation` — Remove an event invitation for a single guest or guest group

### Registry & Gifts
- `search_registry_products` — Browse Zola products in a category, scoped to your registry
- `add_registry_item` — Add a product (by SKU) to the registry
- `update_registry_item` — Update an existing registry item — all fields must be supplied (it's a full replace)
- `remove_registry_item` — Remove an item from the registry that guests shop from
- `reconcile_registry` — Joins the registry against the gift tracker: `DUPLICATE_RISK` (flagged fulfilled but nothing purchased — still buyable), `UNATTRIBUTED` (purchased with no order, so giver and value are lost), `ORPHAN_ORDER`, `MATCHED`

### Wedding website — pages & settings
- `list_pages` — List all wedding-website pages with their IDs, types, display order, visibility, and theme info
- `set_page_hidden` — Show or hide a page on the wedding website (e.g., hide the RSVP page until invites go out)
- `reorder_pages` — Reorder pages in the website navigation
- `update_page` — Update page-level metadata (title, intro copy, nav title, visibility, layout customization)
- `get_wedding_settings` — Get top-level wedding settings: title, URL slug, partner names, date, city, hashtag, guest count, search visibility
- `update_wedding_settings` — Update top-level wedding settings

### Wedding website — content (FAQs, home, things to do, travel)
- `list_faqs` — List all FAQs on the wedding website
- `add_faq` — Add a new FAQ (question + answer) to the website FAQ page
- `update_faq` — Update an existing FAQ — all three fields (question, answer, display_order) must be supplied
- `remove_faq` — Remove an FAQ from the public website
- `list_home_sections` — List the story sections on the website home page
- `add_home_section` — Add a story section to the home page (title + subtitle + description block)
- `update_home_section` — Update a home page story section — all fields must be supplied
- `remove_home_section` — Remove a story section from the public home page
- `list_pois` — List points-of-interest on the "Things to Do" page
- `add_poi` — Add a point-of-interest to the Things-to-Do page (restaurant, attraction, etc.)
- `update_poi` — Update a point-of-interest
- `remove_poi` — Remove a point-of-interest from the public Things-to-Do page
- `list_travel_items` — List hotels, flights, and transportation on the website Travel page
- `add_travel_item` — Add a travel item (hotel, flight, train, car, bus) to the Travel page
- `update_travel_item` — Update a travel item
- `remove_travel_item` — Remove a travel item from the public Travel page

### Wedding website — theme
- `get_current_theme` — Get the currently-selected website theme: key, name, swatch color, layout type
- `get_website_customizations` — Get current website colors, font settings, and available font/color options
- `search_themes` — Browse the catalog of available wedding-website themes
- `update_current_theme` — Switch the wedding website to a different theme template
- `update_website_customization` — Update website colors and fonts

### Invitations & save-the-dates
- `list_card_projects` — List your invitation / save-the-date / shower-invite "card" projects (paper or digital)
- `get_card_project` — Get full details for one invitation project including all customizations (invitation, envelope, RSVP card, details card), paper/color options, and per-customization pages
- `validate_card_project` — Validate an invitation project — reports any text-fit, image, or guest-addressing errors per customization
- `get_card_project_guests` — List the guest groups assigned to an invitation project, including per-group font-size overrides for printed addressing
- `get_card_suite` — Get details for an invitation design "suite" (the family of matching invitation + RSVP + details cards), including paper types, sizes, and price range
- `search_card_catalog` — Search the invitation design catalog
- `list_favorite_card_suites` — List invitation design suites you have favorited (hearted)
- `get_rsvp_page` — Get the RSVP page settings on the wedding website (title, intro copy, visibility, customization)
- `create_card_project` — Create a new invitation project from a design suite and a lead variation (specific size/paper)
- `swap_card_project_variation` — Swap one or more customizations on a project to different variations (paper type, color or size)
- `set_card_project_guests` — Enable / disable guest groups for an invitation project and optionally override font sizes for printed names and addresses
- `preview_card_template` — Render an invitation template preview with text substituted in
- `preview_qrcode` — Generate a QR-code PNG for an invitation
- `set_card_project_qrcode` — Place (or update) a QR code on a specific page of an invitation project

### Discovery & health
- `zola_healthcheck` — Verify the credential and Zola reachability; says which hop failed
- `get_wedding_dashboard` — Planning dashboard overview
- `search_storefronts` — Search marketplace by category/location
- `get_storefront` — Full vendor storefront details
- `list_favorites` — Favorited vendors

## In context groups

Every tool except `zola_healthcheck` carries a `_meta.mint` hint in the **family** group, so a host that groups connectors (mcp-host context groups) can answer a family ask from Zola alongside the other family sources. The canonical reads, each answering with `view: "brief"`:

- **what's on** — `list_events`: the wedding's events (ceremony, reception, rehearsal dinner) with start time and RSVP counts.
- **what's new** — `list_inquiries`: vendor inquiries, newest activity and whether each is unread. Vendor names are written by the vendors, so these lines come inside the untrusted-data envelope.
- **what's due** — `get_budget`: scheduled vendor payments, each with its due date and whether it is paid.

An empty read answers the single note line `-- none`. None takes a subject: an account holds one wedding, so there is nothing to choose between, and none takes a date range. A compound ask looks like "what's on this weekend, and is anything due for the wedding?" — the group asks `list_events` and `get_budget` together. Zola is reached through a cached refresh token; the browser (ContextMint Bridge) is needed only to bootstrap or renew that token, so when neither a token nor a signed-in zola.com tab is available the group answers that Zola needs your browser open.
