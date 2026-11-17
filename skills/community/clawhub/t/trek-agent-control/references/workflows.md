# Research and synchronization workflows

For visits after midnight, keep the intended grouping day and apply the explicit date offsets described in [cross-midnight.md](cross-midnight.md). Check actual local dates and zones when reading back; do not automatically move the visit to another day.

## Research a new trip

1. Collect hard constraints: travelers, ages, accessibility, origin, dates, fixed bookings, work/school windows, budget and transport.
2. Verify time-sensitive claims online. Prefer official attraction, venue, carrier, hotel, government and map sources.
3. Use `search_place` for each real destination. In Mainland China pass `market: "china"` and an administrative region such as `深圳` or `清远`; overseas pass `market: "global"` and a two-letter country code such as `JP` or `FR`.
4. Design each day around geography, opening windows, heat/rain, meals, rest and transfer buffers. Extract every planned POI/activity into `expectedAssignmentsByDate`; do not leave locations only in narrative text.
5. Mark every item as confirmed, recommended, optional or pending confirmation.
6. Preview the plan before creating data.

## Create or update a trip

1. `list_trips` and normalize titles/dates to detect an existing trip.
2. Create only when no match exists; otherwise use the current trip ID.
3. `get_trip_summary` and map its day IDs to ISO dates.
4. Create/reuse places, then assign every expected POI/activity to the correct day with start/end time, duration, transport mode and assignment notes. New place: `create_and_assign_place`; existing place: `assign_place_to_day`. For arrival follow [arrival-mode.md](arrival-mode.md): infer when not explicitly specified, preserve manual choices, and pass transport_mode, transport_source and a brief reason per visit. Pass `place_time`/`end_time` in that same creation call when known; both fields belong to the daily assignment. Use `update_assignment_time` only for later edits. A CLI batch can therefore contain one create action per visit without referencing a previous action's assignment ID.
5. Add reservations/accommodations only from evidence. Accommodation tools create a date range, not a daily assignment; if the hotel/check-in is part of the visible daily plan, also assign the hotel place to that day.
6. Add costs as estimates unless receipts/orders establish actual values.
7. Add packing items for traveler and destination needs.
8. Add todos for unresolved bookings, deadlines, safety checks and missing documents. Use due dates and priority.
9. Add collaboration notes for cross-cutting instructions that must remain visible.
10. For a new trip, follow the cover recipe below. For an explicitly requested place image, upload the image, write its authenticated `file.url` to `place.image_url`, and verify it on readback. Uploading bytes alone does not make an image visible.
11. Read back and compare each date's normalized assignment place names/IDs to `expectedAssignmentsByDate`. Any planned day with zero assignments, any expected place missing, or any POI present only in day-note text is a failed synchronization. Fix it before reporting completion. Intentional rest/location-free travel days must be marked explicitly.

### New trip cover

- Default to **one** landscape image of the main destination, landmark or theme; no unrelated stock photo, no automatic gallery. Prefer the user's chosen file. Otherwise search [Wikimedia Commons](https://commons.wikimedia.org/) by public destination/landmark (e.g. “Kyoto Arashiyama river landscape”), or use an official tourism media library with explicit reuse terms. Never send travelers' names, booking details or private addresses to search. Verify the image matches the actual destination on its original page.
- Prefer public-domain/CC0 assets. [Check each file's reuse terms](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia); if required attribution cannot accompany the image on all relevant surfaces, skip it. Store source URL, creator, licence and any edits as applicable in the file description and tell the user the source. Avoid search thumbnails, hotlinks, private/sensitive photos and unverified copies.
- Use the trip ID returned by creation. Prefer a local JPG/PNG, up to 10 MB; download the actual file and check it opens. Run `trek set-cover <trip-id> /absolute/path/cover.jpg --description '<credit and source URL>'` or call `apply_trip_change` with `action: "set_cover"`, `tripId`, `filename`, `mime_type`, raw `content_base64` and optional `description`. Do not print base64. Check `receipt.persisted` and `receipt.readback.cover_image` (legacy CLI: `verified` and `coverImage`). Uploading without binding the cover does not count. If a write outcome is unclear, read back before retrying.
- Respect “no image”; never replace an existing cover by default or enable sharing to display one. If no suitable image or tool permission exists, finish the itinerary and report the cover as not set. Persisted readback proves the cover is attached, not that an anonymous viewer or every client can render it.

### Verify the itinerary

Save the full expected checklist as a JSON object when using the bundled audit command. An empty array explicitly marks a rest/location-free day:

```json
{
  "2026-09-23": ["金门大桥", "Presidio"],
  "2026-09-24": [],
  "2026-09-25": ["Stanford University", "Apple Park Visitor Center"]
}
```

Run `node scripts/trek-mcp.mjs audit-plan <trip-id> /absolute/path/expected-assignments.json`. Exit code `2` means at least one date is missing, has missing assignments, or contains unexpected assignments; do not report completion.

## Collaborative planning

Use proposals before formal itinerary writes when a group has not decided:

1. `create_trip_proposal`
2. `react_trip_proposal`
3. `decide_trip_proposal` only after the owner confirms
4. `schedule_trip_proposal` only after choosing a day
5. `list_trip_proposals` to verify final status

Use polls for broad group choices and proposals for candidate places that may become scheduled items.

### Add one pending place

Prefer the semantic tool; do not assemble this from primitive writes:

1. If the place is already in 收藏, obtain its ID from `list_places`.
2. Call `add_pending_place({ tripId, placeId, title, ... })`; `placeId` is preferred
   for an existing saved place and prevents duplicate data.
   For a new candidate, pass `description`, `imageUrl`, `website`, `phone` and
   `placeNotes` when verified. Keep `reason` short and specific to this trip.
3. Require `persisted: true`, `destination: "pending"`, and an `open` proposal
   in the returned readback.
4. To remove it from active discussion but keep it saved, call
   `move_pending_place_to_saved({ tripId, proposalId })` after user confirmation.

Do not use `create_place`: a saved place is not the mini program's “待决定” item.
Do not report success without the semantic tool's persisted readback.

## Change an existing trip safely

Create a diff with:

- current value
- proposed value
- reason/source
- affected reservations, costs, members and travel time

Get confirmation before deleting, moving fixed bookings, changing financial data, or replacing confirmed reservations. Apply changes in dependency order and read back after each group.

## Daily briefing

Read the trip summary, today's day, reservations, todos and weather. Return:

- next fixed event and departure deadline
- route and buffer
- weather/clothing
- tickets/documents
- meal plan
- unresolved high-priority todo

Do not write anything for a briefing unless the user explicitly asks to update the trip.

## Evidence policy

- A map result establishes name/address/coordinates, not quality or current opening hours.
- A social post is a recommendation signal, not proof of current policy.
- A reservation is confirmed only with user/order evidence.
- If exact time, address, price, phone or booking status is unknown, preserve the uncertainty in a todo or note.

## Verify notes and daily reminders

After synchronization, use `trek day-view TRIP_ID DAY_ID` to read the 0.3.18+ display contract. `audit-plan` verifies assignment names only; it does not verify notes, reminders, client version or screenshots.

For timed notes, create an expected JSON file (no real user content in shared examples):

```json
{"2026-10-01":[{"text":"带好演出门票和证件","time":"18:00"}]}
```

Run `trek audit-notes TRIP_ID expected-notes.json`. Missing, unexpected or duplicate text/time entries fail the audit (exit 2). Read back the exact daily brief through `day-view`; do not write again simply because an old client cannot show it.
