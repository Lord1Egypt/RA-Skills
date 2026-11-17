# Zola mobile-api endpoints (curl + jq)

All paths are relative to `$BASE=https://mobile-api.zola.com`. Every call
carries `authorization: Bearer $SESSION_TOKEN`, `x-zola-platform-type:
iphone_app`, `x-zola-session-id: $DEVICE_SESSION_ID`, `user-agent: $UA` (see
`SKILL.md`); POST/PUT/DELETE-with-body also need `-H 'content-type:
application/json'`. `$ACCT` = `wedding_account_id`, `$REG` = `registry_id`,
`$WEDDING_ID` = `wedding_id`, all three from `GET /v3/users/me/context` (see
`SKILL.md`'s "resolve context first" section). Response envelope is `{"data": ...}`
unless noted. Paths/bodies below are transcribed from `src/tools/*.ts` —
each section names its source file.

Shorthand used below:

```sh
H=(-H "authorization: Bearer $SESSION_TOKEN" -H "x-zola-platform-type: iphone_app" \
   -H "x-zola-session-id: $DEVICE_SESSION_ID" -H "user-agent: $UA")
HJ=("${H[@]}" -H 'content-type: application/json')
```

---

## Context (`src/client.ts`)

```sh
curl -sS "${H[@]}" "$BASE/v3/users/me/context" | jq '.data'
# .data.user.id, .data.wedding_account.wedding_account_id,
# .data.wedding.{wedding_id,wedding_date,slug}, .data.registry.id
```

---

## Vendors (`src/tools/vendors.ts`)

**List booked vendors** — `POST /v3/account-vendors/booked-list` body `{}`:

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/account-vendors/booked-list" -d '{}' \
  | jq '.data.booked_vendors'
```

**Search vendors (typeahead)** — `POST /v3/reference-vendors/typeahead-taxonomy`:

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/reference-vendors/typeahead-taxonomy" \
  -d '{"query":"Acme Photography","taxonomy_key":"wedding-photographers"}' | jq '.data'
# taxonomy_key default: wedding-venues. Other keys: wedding-planners, wedding-bands-djs, ...
```

**Book a vendor** — find an unbooked slot from `booked-list` for the
`vendor_type`, then `PUT /v5/account-vendors/vendor` (note: **v5**, not v3):

```sh
curl -sS "${HJ[@]}" -X PUT "$BASE/v5/account-vendors/vendor" -d '{
  "uuid": "<slot-uuid-from-booked-list>", "id": 0, "vendor_type": "PHOTOGRAPHER",
  "booked": true, "booking_source": "BOOKED_VENDORS",
  "price_cents": 350000, "event_date": null,
  "sync_with_budget_tool_enabled": true, "facet_keys": [],
  "reference_vendor_request": {
    "id": null, "name": "Acme Photography", "email": null, "phone": null,
    "address": {"city": "Charlotte", "state_province_region": "NC"}
  }
}' | jq '.data'
```

**Update a booked vendor** — same `PUT /v5/account-vendors/vendor`, but
read-modify-write: GET `booked-list`, find by `uuid`, keep `id`/`vendor_type`,
only patch the fields you're changing (name/city/state/email/price/date
default to the current value).

**Unbook a vendor** — `POST /v3/account-vendors/vendor/unbook`:

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/account-vendors/vendor/unbook" \
  -d '{"uuid":"<vendor-uuid>"}'
```

---

## Budget (`src/tools/budget.ts`)

**Get budget** — `GET /v3/budgets`:

```sh
curl -sS "${H[@]}" "$BASE/v3/budgets" | jq '{
  budgeted_cents: .data.budgeted_cents, cost_cents: .data.cost_cents,
  paid_cents: .data.paid_cents, balance_due_cents: .data.balance_due_cents,
  items: [.data.taxonomy_nodes[].items[] | {uuid, title, cost_cents, paid_cents}]
}'
```

**Update a budget item** — read-modify-write: `GET /v3/budgets`, find the item
by `uuid`, then `PUT /v3/budgets/items` with every required field (server
rejects a bare partial):

```sh
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/budgets/items" -d '{
  "item_uuid": "<uuid>", "taxonomy_node_uuid": "<from-get>",
  "estimated_cost_cents": <from-get>, "actual_cost_cents": 250000,
  "note": "Deposit paid", "item_type": "<from-get, e.g. VENUE>",
  "title": "<from-get>"
}' | jq '.data'
```

---

## Guests (`src/tools/guests.ts`)

**List guests** — `POST /v3/guestlists/directory/wedding-accounts/$ACCT` body
`{"sort_by_name_asc": true}`. Guest shape is **flat** (fields directly on the
guest object, no `{guest:{...}}` wrapper):

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/guestlists/directory/wedding-accounts/$ACCT" \
  -d '{"sort_by_name_asc": true}' \
  | jq '.data.guest_groups[] | {guest_group_id, guests: [.guests[] | {guest_id, first_name, family_name, rsvp}]}'
```

**Add a guest group** — `POST /v3/guestlists/groups`. **Omit** optional
fields instead of sending `""`: empty-string `prefix` / `middle_name` / `suffix`
make the endpoint answer a bare 400 "Bad Request" (verified live, Nov 2026).
Invitations go per guest; the address is per guest too. A 2xx is only a success
if `data.guest_group_id` comes back — it has answered 200 with an error envelope
and created nothing.

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/guestlists/groups" -d '{
  "wedding_account_id": '"$ACCT"',
  "guest_group_affiliation": "PRIMARY_FRIEND", "guest_group_tier": "A",
  "invited": true, "invitation_sent": false, "save_the_date_sent": false,
  "guests": [{
    "first_name": "Mike", "family_name": "Smith", "relationship_type": "PRIMARY",
    "source": "IOS", "affiliation": "PRIMARY_FRIEND", "tier": "A",
    "address1": "123 Main St", "city": "Chicago", "state_province": "IL",
    "postal_code": "60613", "country_code": "US",
    "event_invitations": [{"id": null, "event_id": <event_id>, "rsvp_type": "NO_RESPONSE"}],
    "tags": []
  }]
}' | jq '.data.guest_group_id'
```

**Update a guest group's address** — read-modify-write via
`PUT /v3/guestlists/groups/wedding-accounts/$ACCT/bulk/directory`. **Must**
preserve each guest's existing `event_invitations` verbatim (a group that
sends `event_invitations: []` wipes them, per `docs/zola-api-quirks.md` §5):

```sh
# 1. GET the directory (above), find the target group by guest_group_id,
#    keep its `guests[]` array as-is except the address fields you're changing.
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/guestlists/groups/wedding-accounts/$ACCT/bulk/directory" \
  -d '{"updated_guest_groups": [ <full-group-object-with-patched-guest-addresses> ]}' \
  | jq '.data'
```

**Remove a guest group** — `PUT /v3/guestlists/groups/wedding-accounts/$ACCT/delete`:

```sh
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/guestlists/groups/wedding-accounts/$ACCT/delete" \
  -d '{"wedding_account_id": '"$ACCT"', "guest_group_ids": [<id>]}'
```

---

## Seating (`src/tools/seating.ts`)

```sh
curl -sS "${H[@]}" "$BASE/v3/seating-charts/summaries" | jq '.'   # NOT wrapped in `data`
curl -sS "${H[@]}" "$BASE/v3/seating-charts/<chart-uuid>" | jq '.'
```

**Unseated guests** — `POST /v3/guestlists/directory/wedding-accounts/$ACCT`
(same call as guests list), filter client-side for
`.guests[].seating_chart_seat == null`.

**Assign a seat** — `PUT /v3/seating-charts/seats`:

```sh
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/seating-charts/seats" -d '{
  "guest_uuid": "<guest-uuid>", "seat_uuid": "<seat-uuid>",
  "table_uuid": "<table-uuid>", "seating_chart_uuid": "<chart-uuid>"
}' | jq '.'
```

---

## Inquiries (`src/tools/inquiries.ts`)

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/inquiries/unified-inquiries" -d '{}' \
  | jq '.data[].inquiry_summaries[] | {inquiry_uuid, vendor_name: .vendor_card.vendor_name, unread, status_text}'

curl -sS "${H[@]}" "$BASE/v3/inquiries/<inquiry-uuid>/conversation" | jq '.data.messages'

curl -sS "${H[@]}" -X PUT "$BASE/v3/inquiries/<inquiry-uuid>/conversation/read"
```

---

## Events, RSVPs, gifts, registry (`src/tools/events.ts`)

```sh
curl -sS "${H[@]}" "$BASE/v3/websites/events/wedding-accounts/$ACCT/groups" \
  | jq '.data[].events[]'   # event_entity_id, name, start_at, num_guests_*

curl -sS "${H[@]}" "$BASE/v3/websites/events/track-rsvps" | jq '.data.modules'

curl -sS "${H[@]}" "$BASE/v3/gift_tracker/$REG" | jq '.data | del(.info_modules)'

curl -sS "${H[@]}" "$BASE/v4/shop/registry?registry_id=$REG&updated_modules=true" | jq '.data'
```

**Update an event** — read-modify-write: GET the groups above, find by
`event_entity_id`, then `PUT /v3/websites/events/{event_id}` with the full
event object (patch only the fields you're changing; everything else —
`type`, `uuid`, `wedding_account_id`, counts, `meal_options` — round-trips
from the GET):

```sh
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/websites/events/<event_id>" -d '{
  "event_entity_id": <event_id>, "uuid": "<from-get>", "wedding_account_id": '"$ACCT"',
  "type": "<from-get>", "name": "Reception", "start_at": "<from-get>", "end_at": "<from-get>",
  "timezone": "<from-get>", "venue_name": "The Grand Hall", "address1": "", "address2": "",
  "city": "Charlotte", "state_province": "NC", "postal_code": "", "country_code": "US",
  "note": "", "attire": "Black tie", "collect_rsvps": true, "public": <from-get>,
  "display_order": 0, "num_guests_attending": <from-get>, "num_guests_declined": <from-get>,
  "num_guests_not_responded": <from-get>, "meal_options": <from-get>,
  "rsvp_questions": [], "add_booked_vendor": false
}' | jq '.data'
```

**Event invitations (per-guest, read-modify-write)** — from
`src/tools/event-invitations.ts`. Each guest carries an `event_invitations`
array; invite = append `{"event_id":<id>,"id":null,"rsvp_type":"NO_RESPONSE"}`,
uninvite = drop that element, **preserve every other element verbatim**
(same wipe risk as the guest-address write above). Write through the same
`PUT /v3/guestlists/groups/wedding-accounts/$ACCT/bulk/directory` used for
guest writes, sending `{"updated_guest_groups": [...]}` with full group
objects (each guest keeps its full shape, only `event_invitations` patched).

---

## Discover / storefronts (`src/tools/discover.ts`)

```sh
curl -sS "${H[@]}" "$BASE/v4/your-wedding" | jq '.data'

curl -sS "${HJ[@]}" -X POST "$BASE/v3/storefronts/search" -d '{
  "taxonomy_node_id": 2, "city": "Charlotte", "state": "NC",
  "limit": 24, "offset": 0, "facets": {},
  "metro_types": ["HOME","HOME_SERVICE","AWAY"], "metros": [],
  "exclude_inquired_storefronts": false, "exclude_booked_storefronts": false,
  "boost_featured_storefronts": false, "suggested_vendors_for_inquiry_limit": 12
}' | jq '.data'
# taxonomy_node_id: 1=Venues 2=Photographers 3=Florists 7=Planners 9=Bands/DJs

curl -sS "${H[@]}" "$BASE/v3/storefronts/<storefront-uuid>" | jq '.data'
curl -sS "${H[@]}" "$BASE/v3/favorites/" | jq '.data'
```

---

## Registry items (`src/tools/registry-items.ts`)

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/categories/<category_id>/entities" \
  -d '{"offset":0,"limit":50,"registry_id":"'"$REG"'"}' | jq '.data'

# Default collection id: `.data.default_collection_id` from the registry GET
# above, or the first `groups[].modules[]` entry with `type == "COLLECTION"`.
curl -sS "${HJ[@]}" -X POST "$BASE/v3/registries/$REG/collections/<collection_id>" \
  -d '{"sku_id":"<sku>","quantity":1,"most_wanted":false,"enable_group_gifting":false}' \
  | jq '.data'

# Full replace — all fields required:
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/registries/$REG/items/<collection_item_id>" -d '{
  "quantity": 2, "group_gift": false, "marked_fulfilled": false,
  "personal_note": "", "most_wanted": true, "collection_id": "<collection_id>"
}' | jq '.data'

curl -sS "${H[@]}" -X DELETE "$BASE/v3/registries/$REG/items/<collection_item_id>"
```

---

## Website pages & settings (`src/tools/website.ts`)

```sh
curl -sS "${H[@]}" "$BASE/v3/websites/pages/wedding-accounts/full" | jq '.data'

curl -sS "${H[@]}" -X PUT "$BASE/v3/websites/pages/<page_id>/hidden/true"  # or /false

curl -sS "${HJ[@]}" -X PUT "$BASE/v3/websites/pages/wedding-accounts/$ACCT/reorder" \
  -d '{"ids": [<page_id_1>, <page_id_2>, ...]}' | jq '.data'

# Partial patch is fine here (unlike most write endpoints):
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/websites/pages-v2/<page_id>" \
  -d '{"page_id": <page_id>, "title": "Our Story"}' | jq '.data'
```

**Wedding settings** — read via `GET /v3/users/me/context` → `.data.wedding`;
write is read-modify-write (all fields required) to
`PUT /v3/weddings/{wedding_id}`:

```sh
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/weddings/$WEDDING_ID" -d '{
  "wedding_id": '"$WEDDING_ID"', "account_id": '"$ACCT"',
  "slug": "<from-get>", "owner_first_name": "<from-get>", "owner_last_name": "<from-get>",
  "partner_first_name": "<from-get>", "partner_last_name": "<from-get>",
  "title": "Alex & Jordan", "wedding_date": "<from-get>", "hashtag": "#alexandjordan2026",
  "enable_search_engine": true, "enable_search_zola": true,
  "city": "Charlotte", "state_province": "NC", "guest_count": 150
}' | jq '.data'
```

---

## Website theme & customization (`src/tools/website-theme.ts`)

```sh
curl -sS "${H[@]}" "$BASE/v3/themes/current" | jq '.data'
curl -sS "${H[@]}" "$BASE/v3/websites/website-customizations/context" | jq '.data.current_style_customizations'

curl -sS "${HJ[@]}" -X POST "$BASE/v3/themes/search" \
  -d '{"limit":50,"offset":0,"theme_layout_types":["MULTI_PAGE"]}' | jq '.data'

curl -sS "${HJ[@]}" -X PUT "$BASE/v3/themes/current" \
  -d '{"theme_key":"galata","theme_layout_type":"MULTI_PAGE"}' | jq '.data'
```

**Update colors/fonts** — `POST /v3/websites/website-customizations/context`.
**Gotcha (see `docs/zola-api-quirks.md` §1–4):** changing `header_font`
(i.e. `header_font_family_id`) wipes every *other* active color unless you
re-send them in the same POST — GET the current state first and bundle its
non-null `accent_color` / `background_color` / `body.color` /
`navigation_customization.background_color` into the body. `body_font`'s
`font_family_id` only accepts `68` (Libre Baskerville) or `198` (Circular) —
any other value 500s. `header_color` / `nav_font_color` are **not** writable
on this API at all (web-api-only, cookie+CSRF auth — out of scope here).

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/websites/website-customizations/context" -d '{
  "accent_color": "C9A66B",
  "background_color": "FFFFFF",
  "body_font": {"color": "222222"},
  "navigation_customization": {"background_color": "FFFFFF"}
}' | jq '.data'
```

---

## Website content: FAQs / home sections / POIs / travel (`src/tools/website-content.ts`)

All four follow the same list/add/update/remove shape;
`{wedding_account_id: $ACCT}` and an `_entity_id: 0` (create) or the real id
(update) prefix every write body. Deletes share one path shape:
`DELETE /v3/websites/{pages}/{entities}/{entity_id}/wedding-accounts/$ACCT`
where `{pages}` is looked up per-type from
`GET /v3/websites/pages/wedding-accounts/full` (`.data.{home,faq,poi,travel}_page.page_id`).

```sh
# FAQs
curl -sS "${H[@]}" "$BASE/v3/websites/faqs/wedding-accounts/$ACCT" | jq '.data'
curl -sS "${HJ[@]}" -X POST "$BASE/v3/websites/faqs" -d '{
  "wedding_account_id": '"$ACCT"', "faq_entity_id": 0,
  "question": "What is the dress code?", "answer": "Cocktail attire", "display_order": 0
}' | jq '.data'
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/websites/faqs/<faq_entity_id>" -d '{
  "wedding_account_id": '"$ACCT"', "faq_entity_id": <faq_entity_id>,
  "question": "...", "answer": "...", "display_order": 0
}' | jq '.data'
curl -sS "${H[@]}" -X DELETE "$BASE/v3/websites/pages/<faq_page_id>/entities/<faq_entity_id>/wedding-accounts/$ACCT"

# Home page story sections — same shape, path `/v3/websites/home-sections[...]`,
# id field `homepage_entity_id`, extra `hidden` boolean, `title`+`subtitle`+`description`.

# Points of interest — `/v3/websites/points-of-interest[...]`, id field
# `poi_entity_id`; fields: title, description, address1/2, city, state_province,
# postal_code, country_code, latitude, longitude, google_place_id, contact_phone, url.

# Travel items — `/v3/websites/travel[...]`, id field `travel_entity_id`;
# fields: type (HOTEL|FLIGHT|TRAIN|BUS|CAR|OTHER), name, note, code,
# address1/2, city, state_province, postal_code, country_code, latitude,
# longitude, google_place_id, contact_number, email_address, url, source
# (GOOGLE_PLACES|MANUAL), timezone, display_order.
```

Home-section/POI/travel `list`/`add`/`update`/`remove` all mirror the FAQ
calls above 1:1 (same verbs, same `wedding_account_id` prefix, same delete
shape) — see `src/tools/website-content.ts` for the exact field names per
type if you need the full body.

---

## Invitations / card projects (`src/tools/invitations.ts`)

```sh
curl -sS "${HJ[@]}" -X POST "$BASE/v3/card-projects/search_request" -d '{
  "completed": false, "limit": 30, "card_suite_uuids": [], "card_suite_ids": [],
  "offset": 0, "fetch_customizations": true, "include_deleted": false,
  "medium": ["PAPER","MAGNET","DIGITAL"], "single_sample": false
}' | jq '.data'

curl -sS "${H[@]}" "$BASE/v3/card-projects/<project_uuid>" | jq '.data'
curl -sS "${H[@]}" "$BASE/v3/card-projects/<project_uuid>/validate" | jq '.data'
curl -sS "${H[@]}" "$BASE/v3/card-projects/<project_uuid>/project-guest-groups" | jq '.data'
curl -sS "${HJ[@]}" -X POST "$BASE/v4/card-catalog/suites/details/<suite_uuid>" | jq '.data'

curl -sS "${HJ[@]}" -X POST "$BASE/v3/card-catalog/search/faceted" -d '{
  "lead_card_types": [], "include_updated_proof_module": true, "limit": 50, "offset": 0,
  "digital_suite": false, "include_lead_card_type_metadata": true,
  "lead_card_type": "INVITATION", "include_module": true
}' | jq '.data'

curl -sS "${H[@]}" "$BASE/v3/favorites/card-suites/" | jq '.data'
curl -sS "${H[@]}" "$BASE/v3/websites/rsvps/wedding-accounts/$ACCT" | jq '.data'

curl -sS "${HJ[@]}" -X POST "$BASE/v3/card-projects" -d '{
  "quantity": 150, "lead_variation_uuid": "<variation-uuid>",
  "extra_customizable": false, "account_id": '"$ACCT"', "suite_uuid": "<suite-uuid>"
}' | jq '.data'

curl -sS "${HJ[@]}" -X PUT "$BASE/v3/card-projects/<project_uuid>" -d '{
  "customizations": {"<customization_uuid>": {"variation_uuid": "<new-variation-uuid>"}}
}' | jq '.data'

curl -sS "${HJ[@]}" -X PUT "$BASE/v3/card-projects/<project_uuid>/project-guest-groups" -d '{
  "guest_group_requests": [{"guest_group_id": <id>, "enabled": true}]
}' | jq '.data'

curl -sS "${HJ[@]}" -X POST "$BASE/v3/card-templates/preview" -d '{
  "variation_uuids": ["<variation-uuid>"], "customizable": true,
  "substitutions": {"first_name": "Alex", "wedding_date": "2026-10-17"}
}' | jq '.data'
```

**QR code** — preview returns raw image bytes (Content-Type lies as
`image/jpeg` even for a PNG — sniff magic bytes if scripting):

```sh
curl -sS "${HJ[@]}" -X PUT "$BASE/v3/card-projects/qrcode/preview" \
  -H 'accept: */*' -d '{"dimension":"MEDIUM","url_type":"CUSTOM","enabled":true,"url":"https://example.com"}' \
  -o qrcode.png

curl -sS "${HJ[@]}" -X PUT "$BASE/v3/card-projects/<project_uuid>/customization/page/<page_uuid>/qrcode" -d '{
  "dimension": "MEDIUM", "url_type": "CUSTOM", "color": "000000",
  "enabled": true, "url": "https://example.com"
}' | jq '.data'
```
