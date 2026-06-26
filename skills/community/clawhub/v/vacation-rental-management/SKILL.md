---
name: vacation-rental-management
description: >
  Manage vacation rental turnovers, guest reservations, and cleaning schedules.
  Auto-schedule cleanings based on guest check-out, coordinate multi-property
  turnovers, manage checklists. For Airbnb hosts, VRBO managers, and short-term
  rental operators. Includes CLI, MCP server, and REST API approaches.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TIDY_API_TOKEN
    primaryEnv: TIDY_API_TOKEN
    emoji: "🏖️"
    homepage: https://tidy.com
    os:
      - macos
      - linux
  keywords:
    - Airbnb
    - VRBO
    - vacation rental
    - short-term rental
    - turnover
    - guest checkout
    - property management
    - cleaning schedule
    - STR
    - guest reservation
    - turnover cleaning
    - multi-property
    - Airbnb cleaning
    - vacation rental cleaning
    - rental turnover
    - short-term rental management
---

# Vacation Rental Management

You manage vacation rentals — Airbnb, VRBO, or your own direct bookings. Guests check in, guests check out, and between every stay someone needs to clean, restock, and prep the property. Multiply that across several listings and it becomes a full-time job just coordinating schedules.

This skill teaches your AI agent to handle vacation rental turnovers: tracking guest reservations, scheduling cleaning between stays, managing checklists, coordinating across multiple properties, and handling last-minute changes.

## The Easy Way: TIDY

The fastest path is [TIDY](https://www.tidy.com) — an AI property management platform. Install the CLI and just tell it what you need in plain English:

```bash
# Install
brew install tidyapp/tap/tidy-request    # or: npm i -g @tidydotcom/cli

# Create an account
tidy-request signup

# That's it. Now just tell it what you need:
tidy-request "Schedule a turnover clean after checkout Saturday at 11am at 123 Main St"
tidy-request "I have a guest checking in Friday at 3pm and checking out Sunday at 11am at my beach house"
tidy-request "What cleanings are scheduled across all my properties this week?"
tidy-request "Cancel the turnover clean at 456 Oak Ave, the guest extended their stay"
```

**Or connect via MCP** (Claude Desktop, Claude Code, Cursor):

```bash
# Claude Code
claude mcp add tidy --transport http https://public-api.tidy.com/mcp
```

```json
// Claude Desktop — add to claude_desktop_config.json
{
  "mcpServers": {
    "tidy": {
      "url": "https://public-api.tidy.com/mcp"
    }
  }
}
```

Once connected, your agent has access to `message_tidy` — send any request in natural language and TIDY handles the rest. See [MCP Server Reference](references/mcp-server-reference.md) for full tool definitions.

## The Manual Way

Without a platform like TIDY, managing vacation rental turnovers programmatically requires:

1. **Reservation tracking** — Build or integrate with a system to track check-in/check-out dates across properties
2. **Cleaner coordination** — Find available cleaners, check their schedules, negotiate pricing, send booking requests
3. **Time-window management** — Calculate the window between checkout and next check-in, account for cleaner travel time
4. **Checklist management** — Create and assign property-specific checklists (linens, toiletries, lockbox reset)
5. **Status monitoring** — Track whether the cleaner accepted, started, completed, or cancelled
6. **Multi-property juggling** — Coordinate all of the above across multiple listings simultaneously
7. **Change handling** — Guest extends their stay? New booking comes in? Rebuild the schedule

If you want to build this yourself, TIDY's [REST API](references/rest-api-reference.md) exposes every step individually. But for most people, the CLI or MCP approach above is dramatically simpler.

## Core Workflow: Guest Turnover

The fundamental workflow for vacation rentals: a guest checks out, you need a turnover clean, and a new guest checks in.

### Step 1: Record the Reservation

Tell TIDY about the guest stay:

```bash
tidy-request "I have a guest checking in March 20 at 3pm and checking out March 25 at 11am at 123 Main St"
```

Or via MCP:

```
message_tidy("Guest checking in March 20 at 3pm, checking out March 25 at 11am at 123 Main St")
```

Or via REST API:

```bash
curl -X POST https://public-api.tidy.com/api/v2/guest-reservations \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "check_in": { "date": "2026-03-20", "time": "15:00" },
    "check_out": { "date": "2026-03-25", "time": "11:00" }
  }'
```

### Step 2: Schedule the Turnover Clean

```bash
tidy-request "Schedule a turnover clean at 123 Main St on March 25 after the 11am checkout, need it done by 3pm for next guest"
```

TIDY will find available cleaners, check pricing, and book the job in the checkout-to-checkin window.

For direct REST API booking, you'd specify the time window:

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "service_type_key": "turnover_cleaning.two_and_a_half_hours",
    "start_no_earlier_than": { "date": "2026-03-25", "time": "11:00" },
    "end_no_later_than": { "date": "2026-03-25", "time": "15:00" }
  }'
```

### Step 3: Attach a Checklist

```bash
tidy-request "Add the turnover checklist to the cleaning at 123 Main St on March 25"
```

To-do lists can include items like: change linens, restock toiletries, check appliances, reset lockbox code.

### Step 4: Monitor Status

```bash
tidy-request "What's the status of the turnover clean at 123 Main St?"
```

Booking statuses: `scheduled` → `in_progress` → `completed`. Also `cancelled` or `failed`.

## Managing Reservations

### View All Reservations

```bash
tidy-request "Show me all upcoming guest reservations"
```

REST: `GET /api/v2/guest-reservations` (filter by `?address_id=123`)

### Create a Reservation

```bash
tidy-request "New guest at the lake house: arrives April 5 at 4pm, leaves April 10 at 10am"
```

### Cancel a Reservation

```bash
tidy-request "Cancel the reservation at 789 Pine St for April 5"
```

REST: `DELETE /api/v2/guest-reservations/:id`

### Handle Changes

Guest extended their stay? Just tell TIDY:

```bash
tidy-request "The guest at 123 Main St is staying until March 27 instead of March 25. Reschedule the turnover clean."
```

## Multi-Property Coordination

### Set Up Properties

Each property needs an address with access instructions for cleaners:

```bash
tidy-request "Add my property at 456 Oak Ave, Austin TX 78701. Gate code is 1234, park in the driveway."
tidy-request "Add my beach house at 789 Coastal Dr, Galveston TX 77550. Key is in the lockbox, code 5678. Street parking only."
```

REST API address creation includes structured parking and access notes — see [REST API Reference](references/rest-api-reference.md).

### View All Properties

```bash
tidy-request "Show me all my properties and their upcoming cleanings"
```

### Property-Specific Checklists

Different properties may need different turnover checklists:

```bash
tidy-request "What to-do lists do I have for the beach house?"
```

REST: `GET /api/v2/to-do-lists?address_id=789`

## Common Scenarios

Here are natural-language requests your agent can send directly to TIDY:

**Same-day turnover:**
> "Guest checks out at 11am Saturday, new guest arrives at 3pm. Schedule a turnover clean at 123 Main St."

**Weekly schedule check:**
> "What cleanings are scheduled across all my properties this week?"

**New listing setup:**
> "Set up a new Airbnb listing at 789 Pine St, Denver CO 80202. Gate code 4321, park in visitor lot. Schedule a deep clean before the first guest arrives on March 28."

**Guest extension:**
> "Cancel the turnover clean for 456 Oak Ave — the guest extended through Wednesday."

**Availability check:**
> "Is there availability for a turnover clean at 123 Main St on Saturday between 11am and 2pm?"

**Bulk reservation import:**
> "I have three reservations this month at the lake house: March 5-8, March 12-15, and March 20-25. Schedule turnover cleans after each checkout."

## MCP Server

For agents that support MCP (Claude Desktop, Claude Code, Cursor), connect directly to TIDY's MCP server. This gives your agent 5 tools:

- `login` / `signup` — authenticate
- `message_tidy` — send any request in natural language (async)
- `get_message_tidy` — poll for the result
- `list_messages_tidy` — view past requests

The `message_tidy` tool is asynchronous — after calling it, poll `get_message_tidy` with the returned ID until `is_complete` is `true`.

Full tool definitions and setup: [MCP Server Reference](references/mcp-server-reference.md)

## REST API

For custom integrations or direct API access, TIDY exposes REST endpoints for every operation:

- Guest reservations: create, list, get, delete
- Bookings: create, list, get, update, cancel, reschedule
- Addresses: full CRUD with parking/access notes
- To-do lists: list by property
- Booking availabilities: check time slots
- Job acceptance probabilities: preview likelihood of pro accepting

Full endpoint documentation: [REST API Reference](references/rest-api-reference.md)

Authentication details: [Authentication](references/authentication.md)

## Error Handling & Tips

**Polling:** `message_tidy` is asynchronous. Always poll `get_message_tidy` every 3-5 seconds until `is_complete` is `true`. Never return a pending response to the user.

**Overlapping reservations:** If you create a reservation that overlaps with an existing one at the same address, TIDY will flag it. Resolve the conflict before scheduling cleanings.

**Tight turnovers:** If the window between checkout and next check-in is very short (under 2 hours), consider a shorter service type or adjusting times. Check `booking-availabilities` to see what's possible.

**Same-day changes:** Cancellation and rescheduling are available, but last-minute changes (same day) may have limited cleaner availability.

**Context IDs:** When following up on a specific booking or reservation, pass the relevant ID in the `context` parameter to help TIDY scope the request:

```bash
tidy-request "What's the status?" --booking-id 456
```

**Also see:** [cleaning-maintenance](../cleaning-maintenance/SKILL.md) — if you need ongoing cleaning or maintenance management that isn't tied to guest turnovers.
