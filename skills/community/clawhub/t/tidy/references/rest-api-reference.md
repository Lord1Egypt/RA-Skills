# REST API Reference

**Base URL:** `https://public-api.tidy.com`
**Interactive docs:** [public-api.tidy.com/docs](https://public-api.tidy.com/docs)

All endpoints are under `/api/v2/`. Include `Authorization: Bearer YOUR_TOKEN` in all authenticated requests.

---

## Endpoint Summary

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v2/auth/signup` | No | Create account, get token |
| POST | `/api/v2/auth/login` | No | Log in, get token |
| POST | `/api/v2/message-tidy` | Yes | Send natural-language request (async) |
| GET | `/api/v2/message-tidy/:id` | Yes | Poll message status |
| GET | `/api/v2/message-tidy` | Yes | List all messages |
| GET | `/api/v2/addresses` | Yes | List addresses |
| POST | `/api/v2/addresses` | Yes | Create address |
| GET | `/api/v2/addresses/:id` | Yes | Get address |
| PUT | `/api/v2/addresses/:id` | Yes | Update address |
| DELETE | `/api/v2/addresses/:id` | Yes | Delete address |
| GET | `/api/v2/jobs` | Yes | List bookings |
| POST | `/api/v2/jobs` | Yes | Create booking |
| GET | `/api/v2/jobs/:id` | Yes | Get booking |
| PUT | `/api/v2/jobs/:id` | Yes | Update booking |
| POST | `/api/v2/jobs/:id/cancel` | Yes | Cancel booking |
| POST | `/api/v2/jobs/:id/reschedule` | Yes | Reschedule booking |
| GET | `/api/v2/guest-reservations` | Yes | List reservations |
| POST | `/api/v2/guest-reservations` | Yes | Create reservation |
| GET | `/api/v2/guest-reservations/:id` | Yes | Get reservation |
| DELETE | `/api/v2/guest-reservations/:id` | Yes | Delete reservation |
| GET | `/api/v2/tasks` | Yes | List tasks/issues |
| POST | `/api/v2/tasks` | Yes | Create task/issue |
| GET | `/api/v2/tasks/:id` | Yes | Get task/issue |
| PUT | `/api/v2/tasks/:id` | Yes | Update task/issue |
| DELETE | `/api/v2/tasks/:id` | Yes | Delete task/issue |
| GET | `/api/v2/to-do-lists` | Yes | List to-do lists |
| POST | `/api/v2/pros` | Yes | Add a pro |
| GET | `/api/v2/booking-availabilities` | Yes | Check availability |
| GET | `/api/v2/job-acceptance-probabilities/preview` | Yes | Preview acceptance probability |

---

## Message TIDY (Primary Interface)

The simplest way to interact. Send any request in plain English.

### Create Message

```
POST /api/v2/message-tidy
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | Natural language request |
| `context` | object | No | Scope the request |
| `context.address_id` | integer | No | Relevant address ID |
| `context.booking_id` | integer | No | Relevant booking ID |
| `context.issue_id` | integer | No | Relevant task/issue ID |
| `context.guest_reservation_id` | integer | No | Relevant reservation ID |
| `response_schema` | object | No | JSON Schema for structured response |

**Response:** `{ "id": 123, "status": "processing", "is_complete": false }`

### Get Message

```
GET /api/v2/message-tidy/:message_tidy_id
```

Poll until `is_complete` is `true`. Status values: `received` → `processing` → `completed` or `failed`.

### List Messages

```
GET /api/v2/message-tidy
```

Optional filter: `?status=completed,processing`

---

## Addresses

### Create Address

```
POST /api/v2/addresses
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | string | Yes | Street address |
| `city` | string | Yes | City |
| `postal_code` | string | Yes | Postal/ZIP code |
| `unit` | string | No | Unit/apartment number |
| `country_code` | string | No | 2-letter country code (default: `US`) |
| `address_name` | string | No | Friendly name for the property |
| `notes.access` | string | No* | Access instructions for service providers |
| `notes.closing` | string | No* | Closing/lockup instructions |
| `parking.paid_parking` | boolean | Yes | Whether parking requires payment |
| `parking.parking_spot` | string | Yes | One of: `myspot`, `meter`, `street`, `guest`, `paidlot` |
| `parking.parking_pay_with` | string | No | `card` or `cash` (default: `card`) |
| `parking.max_parking_cost` | integer | No | Maximum parking cost in cents |
| `parking.parking_notes` | string | Yes | Parking instructions |

*Notes fields are optional at the top level but `access` and `closing` are required if `notes` is provided.

### Update Address

```
PUT /api/v2/addresses/:address_id
```

Only provided fields are changed. Accepts `address_name`, `notes`, and `parking`.

### Delete Address

```
DELETE /api/v2/addresses/:address_id
```

Active jobs must be cancelled first.

---

## Bookings (Jobs)

### Service Type Keys

| Key | Description |
|---|---|
| `regular_cleaning.one_hour` | 1-hour regular cleaning |
| `regular_cleaning.two_and_a_half_hours` | 2.5-hour regular cleaning |
| `regular_cleaning.four_hours` | 4-hour regular cleaning |
| `deep_cleaning.two_and_a_half_hours` | 2.5-hour deep cleaning |
| `deep_cleaning.four_hours` | 4-hour deep cleaning |
| `turnover_cleaning.two_and_a_half_hours` | 2.5-hour turnover cleaning |
| `turnover_cleaning.four_hours` | 4-hour turnover cleaning |

### Booking Status Values

`scheduled` → `in_progress` → `completed`

Also: `cancelled`, `failed`

### Create Booking

```
POST /api/v2/jobs
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address_id` | integer | Yes | Property address |
| `service_type_key` | string | Yes | See service type keys above |
| `to_do_list_id` | integer | No | Attach a to-do list/checklist |
| `start_no_earlier_than.date` | date | Yes | Earliest start date (YYYY-MM-DD) |
| `start_no_earlier_than.time` | string | Yes | Earliest start time (HH:MM) |
| `end_no_later_than.date` | date | Yes | Latest end date (YYYY-MM-DD) |
| `end_no_later_than.time` | string | Yes | Latest end time (HH:MM) |
| `preferred_start_datetime.date` | date | No | Preferred date |
| `preferred_start_datetime.time` | string | No | Preferred time (HH:MM) |

**Example:**

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "service_type_key": "turnover_cleaning.two_and_a_half_hours",
    "start_no_earlier_than": { "date": "2025-03-22", "time": "11:00" },
    "end_no_later_than": { "date": "2025-03-22", "time": "15:00" },
    "to_do_list_id": 456
  }'
```

### List Bookings

```
GET /api/v2/jobs
```

Optional filters: `?address_id=123&status=scheduled&to_do_list_id=456`

### Cancel Booking

```
POST /api/v2/jobs/:job_id/cancel
```

### Reschedule Booking

```
POST /api/v2/jobs/:job_id/reschedule
```

Same parameters as create (requires `service_type_key`, `start_no_earlier_than`, `end_no_later_than`).

---

## Guest Reservations

### Create Reservation

```
POST /api/v2/guest-reservations
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address_id` | integer | Yes | Property address |
| `check_in.date` | date | Yes | Check-in date (YYYY-MM-DD) |
| `check_in.time` | string | No | Check-in time (HH:MM) |
| `check_out.date` | date | Yes | Check-out date (YYYY-MM-DD) |
| `check_out.time` | string | No | Check-out time (HH:MM) |

**Example:**

```bash
curl -X POST https://public-api.tidy.com/api/v2/guest-reservations \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "check_in": { "date": "2025-03-20", "time": "15:00" },
    "check_out": { "date": "2025-03-25", "time": "11:00" }
  }'
```

### List Reservations

```
GET /api/v2/guest-reservations
```

Optional filter: `?address_id=123`

### Delete Reservation

```
DELETE /api/v2/guest-reservations/:guest_reservation_id
```

---

## Tasks (Issues / Maintenance Reports)

### Create Task

```
POST /api/v2/tasks
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address_id` | integer | Yes | Property address |
| `title` | string | Yes | Short title |
| `description` | string | Yes | Detailed description |
| `type` | string | Yes | Issue type (e.g., `plumbing`, `electrical`, `general`) |
| `status` | string | No | Status |
| `urgency` | string | No | Urgency level |
| `due_date` | string | No | Due date |
| `assigned_to_concierge` | boolean | No | Assign to concierge for automatic handling |

### List Tasks

```
GET /api/v2/tasks
```

Optional filters: `?address_id=123&status=open&type=plumbing&urgency=high&assigned_to_concierge=true`

### Update Task

```
PUT /api/v2/tasks/:task_id
```

Only provided fields are changed. Accepts all create parameters plus `task_id`.

### Delete Task

```
DELETE /api/v2/tasks/:task_id
```

---

## To-Do Lists

### List To-Do Lists

```
GET /api/v2/to-do-lists
```

Optional filter: `?address_id=123`

---

## Service Professionals (Pros)

### Add a Pro

```
POST /api/v2/pros
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Pro's name |
| `email` | string | Yes | Pro's email |
| `phone` | string | No | Pro's phone number |
| `service_types` | array | No | Service types (default: `["regular_cleaning"]`) |

---

## Booking Availabilities

### Check Availability

```
GET /api/v2/booking-availabilities?address_id=123&service_type_key=regular_cleaning.two_and_a_half_hours
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address_id` | integer | Yes | Property address |
| `service_type_key` | string | Yes | Service type (default: `regular_cleaning.one_hour`) |

Returns available time slots.

---

## Job Acceptance Probabilities

### Preview Acceptance Probability

```
GET /api/v2/job-acceptance-probabilities/preview
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address_id` | integer | Yes | Property address |
| `service_type_key` | string | Yes | Service type |
| `start_no_earlier_than.date` | date | Yes | Earliest start date |
| `start_no_earlier_than.time` | string | Yes | Earliest start time (HH:MM) |
| `end_no_later_than.date` | date | Yes | Latest end date |
| `end_no_later_than.time` | string | Yes | Latest end time (HH:MM) |
| `price` | integer | No | Price in cents |
| `preferred_start_datetime.date` | date | No | Preferred date |
| `preferred_start_datetime.time` | string | No | Preferred time (HH:MM) |

Returns the probability that a pro will accept the job at the given parameters.

---

## Error Format

All errors follow a consistent format:

```json
{
  "object": "error",
  "type": "authentication_error",
  "code": "AuthenticationError",
  "message": "Invalid email or password",
  "invalid_params": []
}
```

| HTTP Status | Error Type | When |
|---|---|---|
| 400 | `invalid_request_error` | Missing or invalid parameters |
| 401 | `authentication_error` | Bad credentials or missing token |
| 404 | `not_found_error` | Resource doesn't exist |
| 422 | `invalid_request_error` | Validation failed |
| 500 | `internal_error` | Server error |
