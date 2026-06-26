---
name: tidy
description: Full-featured AI property management — addresses, cleanings, reservations, tasks, pros, and natural language messaging.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TIDY_API_TOKEN
      bins:
        - tidy-request
    primaryEnv: TIDY_API_TOKEN
    emoji: "✨"
    homepage: https://tidy.com
    os:
      - macos
      - linux
  keywords:
    - tidy
    - property management
    - cleaning
    - maintenance
    - vacation rental
    - Airbnb
    - VRBO
    - short-term rental
    - booking
    - guest reservation
    - MCP server
    - AI assistant
    - natural language
    - service professional
---

# TIDY — AI Property Management Platform

TIDY is an AI-powered property management platform. This skill provides complete access to all TIDY capabilities: property management, cleaning scheduling, guest reservations, maintenance tasks, service professionals, and a natural language AI assistant.

**Base URL:** `https://public-api.tidy.com`
**Interactive API docs:** `https://public-api.tidy.com/docs`
**MCP endpoint:** `https://public-api.tidy.com/mcp`

## Quick Start

The fastest way to interact with TIDY is the CLI or the natural language message-tidy endpoint.

### CLI Quick Start

```bash
# Install
brew install tidyapp/tap/tidy-request   # or: npm i -g @tidydotcom/cli

# Authenticate
tidy-request signup    # new account
tidy-request login     # existing account

# Send any property management request in plain English
tidy-request "Schedule a deep clean for next Tuesday at my Beach House"
tidy-request "Create a guest reservation for April 10-14"
tidy-request "Report a broken window at address 123" --address-id 123
```

### API Quick Start

```bash
# Get a token
curl -X POST https://public-api.tidy.com/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"yourpassword"}'
# Returns: { "token": "abc123..." }

export TIDY_API_TOKEN="abc123..."

# Send a natural language request
curl -X POST https://public-api.tidy.com/api/v2/message-tidy \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Schedule a cleaning for next Tuesday"}'
```

---

## Authentication

### Sign Up

```bash
curl -X POST https://public-api.tidy.com/api/v2/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "password": "secret123"
  }'
```

### Log In

```bash
curl -X POST https://public-api.tidy.com/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","password":"secret123"}'
```

Both return: `{ "token": "abc123..." }`. Tokens do not expire.

Use `Authorization: Bearer <token>` on all subsequent requests.

### CLI Authentication

```bash
tidy-request signup    # interactive: prompts for name, email, password
tidy-request login     # interactive: prompts for email, password
tidy-request logout    # removes stored credentials
```

Credentials are stored at `~/.config/tidy/credentials`. Set `TIDY_API_TOKEN` as an environment variable to override stored credentials.

---

## MCP Server

TIDY exposes an MCP (Model Context Protocol) server for use with Claude Desktop, Claude Code, Cursor, and any MCP client.

**Endpoint:** `https://public-api.tidy.com/mcp` (Streamable HTTP, POST)

### Available MCP Tools

| Tool | Auth Required | Description |
|---|---|---|
| `login` | No | Authenticate with email/password |
| `signup` | No | Create account |
| `message_tidy` | Yes | Send natural language request (async) |
| `get_message_tidy` | Yes | Poll for async message result |
| `list_messages_tidy` | Yes | List all previous messages |
| `list_addresses` | Yes | List all managed properties |
| `create_address` | Yes | Add a new property |
| `get_address` | Yes | Get property details |
| `update_address` | Yes | Update a property |
| `delete_address` | Yes | Remove a property |
| `list_bookings` | Yes | List cleaning jobs |
| `create_booking` | Yes | Schedule a cleaning |
| `get_booking` | Yes | Get job details |
| `update_booking` | Yes | Modify a job |
| `cancel_booking` | Yes | Cancel a job |
| `reschedule_booking` | Yes | Reschedule a job |
| `list_booking_availabilities` | Yes | Find available time slots |
| `list_guest_reservations` | Yes | List guest stays |
| `create_guest_reservation` | Yes | Create a guest stay |
| `get_guest_reservation` | Yes | Get reservation details |
| `delete_guest_reservation` | Yes | Cancel a guest stay |
| `list_tasks` | Yes | List maintenance issues |
| `create_task` | Yes | Report a maintenance issue |
| `get_task` | Yes | Get task details |
| `update_task` | Yes | Update a task |
| `delete_task` | Yes | Remove a task |
| `list_to_do_lists` | Yes | List cleaning checklists |
| `create_pro` | Yes | Add a service professional |

### Connect from Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tidy": {
      "url": "https://public-api.tidy.com/mcp"
    }
  }
}
```

### Connect from Claude Code

```bash
claude mcp add tidy --transport http https://public-api.tidy.com/mcp
```

### Stdio Proxy (for clients that only support stdio)

```bash
npx @tidydotcom/mcp-server
npx @tidydotcom/mcp-server --api-token YOUR_TOKEN
```

### MCP Async Workflow

`message_tidy` is asynchronous:

1. Call `login` or `signup` to get a token
2. Call `message_tidy` with your request in plain English
3. Note the returned `id`
4. Poll `get_message_tidy` with that ID every 3–5 seconds
5. When `status` is `completed`, read `response_message` for the result

---

## Message TIDY (Natural Language AI)

Send any property management request in plain English and TIDY's AI handles it.

### Send a message

```bash
curl -X POST https://public-api.tidy.com/api/v2/message-tidy \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Schedule a turnover cleaning before my next guest arrives on April 10",
    "context": { "address_id": 123, "guest_reservation_id": 456 }
  }'
```

**Parameters:**
- `message` (required): natural language request
- `context` (optional): `{ address_id, booking_id, issue_id, guest_reservation_id }` to scope the request
- `response_schema` (optional): JSON Schema describing desired structured response format

**Status values:** `queued` → `in_progress` → `completed` or `failed`

### Poll for result

```bash
curl -s https://public-api.tidy.com/api/v2/message-tidy/123 \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

Poll every 3–5 seconds. When `status` is `completed`, the answer is in `response_message`.

### List all messages

```bash
curl -s "https://public-api.tidy.com/api/v2/message-tidy?status=completed" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

---

## Addresses (Properties)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v2/addresses` | List all addresses |
| GET | `/api/v2/addresses/:id` | Get address details |
| POST | `/api/v2/addresses` | Create an address |
| PUT | `/api/v2/addresses/:id` | Update an address |
| DELETE | `/api/v2/addresses/:id` | Delete an address |

### Create an address

```bash
curl -X POST https://public-api.tidy.com/api/v2/addresses \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Beach Rd",
    "city": "Miami",
    "postal_code": "33139",
    "country_code": "US",
    "address_name": "Beach House",
    "notes": {
      "access": "Lockbox code 4521 on side gate",
      "closing": "Leave keys on kitchen counter"
    },
    "parking": {
      "paid_parking": false,
      "parking_spot": "myspot",
      "parking_pay_with": "card",
      "max_parking_cost": 0,
      "parking_notes": "Park in driveway spot #2"
    }
  }'
```

**Required:** `address`, `city`, `postal_code`, `parking` (with `paid_parking`, `parking_spot`, `parking_notes`).

**Optional:** `unit`, `country_code` (default `"US"`), `address_name`, `notes` (with `access`, `closing`).

**`parking_spot` values:** `myspot`, `meter`, `street`, `guest`, `paidlot`.

**`parking_pay_with` values:** `card`, `cash` (default `"card"`).

---

## Jobs (Cleaning Bookings)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v2/jobs` | List all jobs |
| GET | `/api/v2/jobs/:id` | Get job details |
| POST | `/api/v2/jobs` | Create a job |
| PUT | `/api/v2/jobs/:id` | Update a job |
| POST | `/api/v2/jobs/:id/cancel` | Cancel a job |
| POST | `/api/v2/jobs/:id/reschedule` | Reschedule a job |

### Service Types

| Key | Description |
|---|---|
| `regular_cleaning.one_hour` | 1-hour regular cleaning |
| `regular_cleaning.two_and_a_half_hours` | 2.5-hour regular cleaning |
| `regular_cleaning.four_hours` | 4-hour regular cleaning |
| `deep_cleaning.two_and_a_half_hours` | 2.5-hour deep cleaning |
| `deep_cleaning.four_hours` | 4-hour deep cleaning |
| `turnover_cleaning.two_and_a_half_hours` | 2.5-hour turnover cleaning |
| `turnover_cleaning.four_hours` | 4-hour turnover cleaning |

### Booking Statuses

`scheduled` → `in_progress` → `completed` or `cancelled` or `failed`

### Create a job

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "service_type_key": "regular_cleaning.two_and_a_half_hours",
    "start_no_earlier_than": { "date": "2026-04-10", "time": "09:00" },
    "end_no_later_than": { "date": "2026-04-10", "time": "17:00" },
    "preferred_start_datetime": { "date": "2026-04-10", "time": "10:00" },
    "to_do_list_id": 789
  }'
```

**Required:** `address_id`, `service_type_key`, `start_no_earlier_than` (date + time), `end_no_later_than` (date + time).

**Optional:** `preferred_start_datetime`, `to_do_list_id`.

### Cancel a job

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs/456/cancel \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

### Reschedule a job

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs/456/reschedule \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service_type_key": "regular_cleaning.two_and_a_half_hours",
    "start_no_earlier_than": { "date": "2026-04-15", "time": "09:00" },
    "end_no_later_than": { "date": "2026-04-15", "time": "17:00" }
  }'
```

---

## Booking Availability

```bash
curl -s "https://public-api.tidy.com/api/v2/booking-availabilities?address_id=123&service_type_key=regular_cleaning.two_and_a_half_hours" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

**Required:** `address_id`, `service_type_key`.

---

## Guest Reservations

| Method | Path | Description |
|---|---|---|
| GET | `/api/v2/guest-reservations` | List reservations (optional `address_id` filter) |
| GET | `/api/v2/guest-reservations/:id` | Get reservation details |
| POST | `/api/v2/guest-reservations` | Create a reservation |
| DELETE | `/api/v2/guest-reservations/:id` | Delete a reservation |

### Create a reservation

```bash
curl -X POST https://public-api.tidy.com/api/v2/guest-reservations \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "check_in": { "date": "2026-04-10", "time": "15:00" },
    "check_out": { "date": "2026-04-14", "time": "11:00" }
  }'
```

**Required:** `address_id`, `check_in.date`, `check_out.date`.

**Optional:** `check_in.time`, `check_out.time`.

---

## Tasks (Maintenance / Issues)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v2/tasks` | List tasks (filter by `address_id`, `status`, `type`, `urgency`, `assigned_to_concierge`) |
| GET | `/api/v2/tasks/:id` | Get task details |
| POST | `/api/v2/tasks` | Create a task |
| PUT | `/api/v2/tasks/:id` | Update a task |
| DELETE | `/api/v2/tasks/:id` | Delete a task |

### Task Statuses

`reported` → `in_progress` → `completed`

### Task Urgency Levels

`low`, `normal`, `high`, `emergency`

### Create a task

```bash
curl -X POST https://public-api.tidy.com/api/v2/tasks \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "title": "Broken window in master bedroom",
    "description": "Left pane is cracked, needs glass replacement.",
    "type": "repair",
    "urgency": "high",
    "due_date": "2026-04-05",
    "assigned_to_concierge": true
  }'
```

**Required:** `address_id`, `title`, `description`, `type`.

**Optional:** `status`, `urgency`, `due_date`, `assigned_to_concierge`.

---

## To-Do Lists

```bash
curl -s "https://public-api.tidy.com/api/v2/to-do-lists?address_id=123" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

---

## Service Professionals (Pros)

```bash
curl -X POST https://public-api.tidy.com/api/v2/pros \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Garcia",
    "email": "maria@example.com",
    "phone": "+1-555-0199",
    "service_types": ["regular_cleaning"]
  }'
```

**Required:** `name`, `email`. **Optional:** `phone`, `service_types`.

---

## CLI Reference

### Install

```bash
brew install tidyapp/tap/tidy-request   # macOS/Linux via Homebrew
npm install -g @tidydotcom/cli          # via npm
```

### Commands

```bash
tidy-request login                          # authenticate
tidy-request signup                         # create account
tidy-request logout                         # remove credentials

tidy-request "your request"                 # natural language request
tidy-request "message" --address-id 123     # with address context
tidy-request "message" --booking-id 456     # with booking context
tidy-request "message" --issue-id 789       # with task context
tidy-request "message" --reservation-id 101 # with reservation context

tidy-request --list                         # list all messages
tidy-request --get ID                       # get a specific message
tidy-request --help                         # help
tidy-request --version                      # version
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `TIDY_API_HOST` | API base URL | `https://public-api.tidy.com` |
| `TIDY_API_TOKEN` | Bearer token (overrides stored credentials) | — |

---

## Complete API Endpoint Reference

| Method | Path | Description |
|---|---|---|
| POST | `/api/v2/auth/signup` | Create account |
| POST | `/api/v2/auth/login` | Log in |
| POST | `/api/v2/message-tidy` | Send AI message (async) |
| GET | `/api/v2/message-tidy/:id` | Poll message result |
| GET | `/api/v2/message-tidy` | List messages |
| GET | `/api/v2/addresses` | List addresses |
| POST | `/api/v2/addresses` | Create address |
| GET | `/api/v2/addresses/:id` | Get address |
| PUT | `/api/v2/addresses/:id` | Update address |
| DELETE | `/api/v2/addresses/:id` | Delete address |
| GET | `/api/v2/jobs` | List jobs |
| POST | `/api/v2/jobs` | Create job |
| GET | `/api/v2/jobs/:id` | Get job |
| PUT | `/api/v2/jobs/:id` | Update job |
| POST | `/api/v2/jobs/:id/cancel` | Cancel job |
| POST | `/api/v2/jobs/:id/reschedule` | Reschedule job |
| GET | `/api/v2/guest-reservations` | List reservations |
| POST | `/api/v2/guest-reservations` | Create reservation |
| GET | `/api/v2/guest-reservations/:id` | Get reservation |
| DELETE | `/api/v2/guest-reservations/:id` | Delete reservation |
| GET | `/api/v2/tasks` | List tasks |
| POST | `/api/v2/tasks` | Create task |
| GET | `/api/v2/tasks/:id` | Get task |
| PUT | `/api/v2/tasks/:id` | Update task |
| DELETE | `/api/v2/tasks/:id` | Delete task |
| GET | `/api/v2/to-do-lists` | List to-do lists |
| POST | `/api/v2/pros` | Add a pro |
| GET | `/api/v2/booking-availabilities` | Check availability |

Full interactive documentation: `https://public-api.tidy.com/docs`

---

## Date and Time Formats

- Dates: `YYYY-MM-DD` (e.g., `2026-04-10`)
- Times: `HH:MM` 24-hour format (e.g., `09:00`, `17:30`)
- Date-time fields use nested objects: `{ "date": "2026-04-10", "time": "09:00" }`

---

## Error Handling

All errors return:

```json
{
  "object": "error",
  "type": "authentication_error",
  "code": "ErrorCode",
  "message": "Human-readable description",
  "invalid_params": []
}
```

| HTTP Status | Error Type | When |
|---|---|---|
| 400 | `invalid_request_error` | Missing or invalid parameters |
| 401 | `authentication_error` | Bad credentials or missing token |
| 404 | `not_found_error` | Resource does not exist |
| 500 | `internal_error` | Server error |

---

## Detailed Reference Documentation

- [Authentication](references/authentication.md) — token lifecycle, storage, MCP auth
- [MCP Server Reference](references/mcp-server-reference.md) — full tool definitions, async pattern, setup
- [REST API Reference](references/rest-api-reference.md) — complete endpoint documentation with parameters

## Related Skills

- [cleaning-maintenance](../cleaning-maintenance/SKILL.md) — focused on booking cleanings and managing maintenance
- [vacation-rental-management](../vacation-rental-management/SKILL.md) — focused on Airbnb/VRBO turnovers and guest reservations
