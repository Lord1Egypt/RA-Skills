---
name: vacation-property-management
description: Manage vacation rental properties, guest reservations, and cleaning checklists with the TIDY platform.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TIDY_API_TOKEN
    primaryEnv: TIDY_API_TOKEN
    emoji: "🏠"
    homepage: https://tidy.com
---

# Vacation Property Management — TIDY

Manage vacation rental properties, guest reservations, and cleaning checklists through the TIDY API. Built for short-term rental hosts, vacation property managers, and Airbnb/VRBO operators.

## Authentication

All requests require a Bearer token. Obtain one by logging in or signing up.

```bash
# Sign up
curl -X POST https://public-api.tidy.com/api/v2/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Doe","email":"jane@example.com","password":"secret123"}'

# Log in
curl -X POST https://public-api.tidy.com/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","password":"secret123"}'
```

Both return `{ "token": "abc123..." }`. Tokens do not expire.

```bash
export TIDY_API_TOKEN="abc123..."
```

Include `Authorization: Bearer $TIDY_API_TOKEN` on all subsequent requests.

---

## Addresses (Properties)

Properties are called "addresses" in the API. Each address represents a physical property you manage.

### List all addresses

```bash
curl -s https://public-api.tidy.com/api/v2/addresses \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

### Get a single address

```bash
curl -s https://public-api.tidy.com/api/v2/addresses/123 \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

Response fields: `id`, `address`, `unit`, `city`, `postal_code`, `country_code`, `address_name`, `notes` (`access`, `closing`), `parking` (`paid_parking`, `parking_spot`, `parking_pay_with`, `max_parking_cost`, `parking_notes`), `created_at`.

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

### Update an address

```bash
curl -X PUT https://public-api.tidy.com/api/v2/addresses/123 \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_name": "Oceanfront Beach House",
    "notes": { "access": "Updated: use smart lock code 9876" }
  }'
```

Only provided fields are changed.

### Delete an address

```bash
curl -X DELETE https://public-api.tidy.com/api/v2/addresses/123 \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

---

## Guest Reservations

Track guest check-in and check-out dates for each property. Reservations can trigger automatic turnover cleaning.

### List all reservations

```bash
curl -s https://public-api.tidy.com/api/v2/guest-reservations \
  -H "Authorization: Bearer $TIDY_API_TOKEN"

# Filter by address
curl -s "https://public-api.tidy.com/api/v2/guest-reservations?address_id=123" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

### Get a single reservation

```bash
curl -s https://public-api.tidy.com/api/v2/guest-reservations/456 \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

Response fields: `id`, `address_id`, `job_id`, `check_in` (`date`, `time`), `check_out` (`date`, `time`), `created_at`.

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

Date format: `YYYY-MM-DD`. Time format: `HH:MM` (24-hour).

### Delete a reservation

```bash
curl -X DELETE https://public-api.tidy.com/api/v2/guest-reservations/456 \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

---

## To-Do Lists (Cleaning Checklists)

To-do lists are cleaning checklists that can be attached to jobs. They tell service providers what specific tasks to perform at a property.

```bash
curl -s https://public-api.tidy.com/api/v2/to-do-lists \
  -H "Authorization: Bearer $TIDY_API_TOKEN"

# Filter by address
curl -s "https://public-api.tidy.com/api/v2/to-do-lists?address_id=123" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

---

## Natural Language (message-tidy)

For complex multi-step operations, send a natural language request instead of calling individual endpoints.

```bash
curl -X POST https://public-api.tidy.com/api/v2/message-tidy \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a new property at 456 Oak Lane, Austin TX 78701 with gate code 1234",
    "context": { "address_id": 123 }
  }'
```

This is asynchronous. Poll with `GET /api/v2/message-tidy/{id}` every 3–5 seconds until `status` is `completed` or `failed`.

### Example requests

- "Add a new vacation rental at 789 Palm Dr, Scottsdale AZ 85251"
- "Create a guest reservation at my Beach House for April 10-14"
- "Show me all upcoming reservations at address 123"
- "Update the access notes for my downtown condo to say use smart lock code 5678"

---

## CLI Alternative

Install: `brew install tidyapp/tap/tidy-request` or `npm i -g @tidydotcom/cli`.

```bash
tidy-request login
tidy-request "Create a guest reservation at Beach House for April 10-14"
tidy-request "List all my properties"
tidy-request "Update access notes for address 123" --address-id 123
tidy-request "Extend the reservation by 2 days" --reservation-id 456
```

---

## Error Handling

| HTTP Status | Error Type | When |
|---|---|---|
| 400 | `invalid_request_error` | Missing or invalid parameters |
| 401 | `authentication_error` | Bad credentials or missing token |
| 404 | `not_found_error` | Resource does not exist |
| 500 | `internal_error` | Server error |
