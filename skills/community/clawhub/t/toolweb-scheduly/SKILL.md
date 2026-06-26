---
name: Scheduly API
description: A scheduling and booking management platform with Google Calendar integration, event type management, availability rules, and time slot booking capabilities.
---

# Overview

Scheduly is a comprehensive scheduling API that enables users to create custom event types, manage availability, and handle bookings with built-in Google Calendar synchronization. The platform is designed for professionals and teams who need to streamline their scheduling workflows with flexible availability rules, blocked date management, and automatic renewal capabilities.

Key capabilities include event type creation and management with monthly renewal (500 coins per creation), granular availability scheduling by day and time, public booking pages for guests, and complete booking lifecycle management. Users can connect their Google Calendar accounts, set timezone preferences, and automate renewal processes to ensure continuous availability.

Ideal users include freelancers, consultants, coaches, therapists, and any service provider who needs to offer time slots to clients while maintaining control over their availability and managing calendar integrations seamlessly.

## Usage

### Create an Event Type

```json
{
  "name": "30-Minute Consultation",
  "description": "One-on-one consultation session",
  "duration_minutes": 30,
  "color": "#3b82f6"
}
```

**Request:**

```bash
curl -X POST https://api.toolweb.in/tools/scheduly/event-types \
  -H "Content-Type: application/json" \
  -d '{
    "name": "30-Minute Consultation",
    "description": "One-on-one consultation session",
    "duration_minutes": 30,
    "color": "#3b82f6"
  }' \
  -G --data-urlencode "user_id=user123"
```

**Response:**

```json
{
  "id": 1,
  "user_id": "user123",
  "name": "30-Minute Consultation",
  "slug": "30-minute-consultation",
  "description": "One-on-one consultation session",
  "duration_minutes": 30,
  "color": "#3b82f6",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-02-15T10:30:00Z",
  "is_expired": false,
  "in_grace_period": false,
  "auto_renewal_enabled": false
}
```

### Create a Booking

```json
{
  "event_type_slug": "30-minute-consultation",
  "guest_name": "John Doe",
  "guest_email": "john@example.com",
  "start_time": "2024-01-20T14:00:00Z",
  "timezone": "America/New_York",
  "notes": "Please call 5 minutes before the meeting"
}
```

**Request:**

```bash
curl -X POST https://api.toolweb.in/tools/scheduly/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "event_type_slug": "30-minute-consultation",
    "guest_name": "John Doe",
    "guest_email": "john@example.com",
    "start_time": "2024-01-20T14:00:00Z",
    "timezone": "America/New_York",
    "notes": "Please call 5 minutes before the meeting"
  }'
```

**Response:**

```json
{
  "id": "booking-001",
  "event_type_id": 1,
  "event_type_name": "30-Minute Consultation",
  "guest_name": "John Doe",
  "guest_email": "john@example.com",
  "start_time": "2024-01-20T14:00:00Z",
  "end_time": "2024-01-20T14:30:00Z",
  "timezone": "America/New_York",
  "notes": "Please call 5 minutes before the meeting",
  "created_at": "2024-01-15T11:00:00Z",
  "status": "confirmed"
}
```

## Endpoints

### Root & Health

#### `GET /`
Read root endpoint. Returns basic service information.

**Parameters:** None

**Response:** Service metadata and status.

---

#### `GET /health`
Health check endpoint. Verify API is running and operational.

**Parameters:** None

**Response:** Health status confirmation.

---

### Google OAuth Authentication

#### `GET /google/login`
Initiate Google OAuth flow for calendar integration.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Response:** OAuth authorization URL and session state.

---

#### `GET /google/callback`
Handle Google OAuth callback after user authorization.

**Parameters:**
- `code` (string, required): Authorization code from Google
- `state` (string, required): State parameter for CSRF protection

**Response:** User profile and calendar connection confirmation.

---

#### `POST /user/disconnect-google`
Disconnect Google Calendar account and revoke tokens.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Response:** Confirmation of disconnection.

---

### Event Type Management

#### `POST /event-types`
Create a new event type. Costs 500 coins and is valid for 1 month.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Request Body:**
- `name` (string, required): Event type name
- `description` (string, optional): Event description
- `duration_minutes` (integer, required): Duration in minutes
- `color` (string, optional, default: `#3b82f6`): Hex color code for UI display

**Response:** Created event type with slug, expiry date, and renewal status.

---

#### `GET /event-types`
Get all event types for a user with expiry status, grace period, and auto-renewal info.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Response:** Array of event types with:
- `id`: Event type ID
- `name`: Event type name
- `slug`: URL-friendly identifier
- `duration_minutes`: Booking duration
- `is_expired`: Boolean indicating expiry status
- `in_grace_period`: Boolean indicating grace period
- `auto_renewal_enabled`: Boolean for auto-renewal status
- `expires_at`: Expiration timestamp

---

#### `GET /event-types/{slug}`
Get a specific event type by slug.

**Parameters:**
- `slug` (string, required, path): Event type slug
- `user_id` (string, required): Unique user identifier

**Response:** Single event type object with full details.

---

#### `DELETE /event-types/{event_id}`
Delete an event type.

**Parameters:**
- `event_id` (integer, required, path): Event type ID
- `user_id` (string, required): Unique user identifier

**Response:** Deletion confirmation.

---

#### `POST /event-types/{event_id}/renew`
Renew an expired event type. Costs 500 coins and extends for 1 month.

**Parameters:**
- `event_id` (integer, required, path): Event type ID
- `user_id` (string, required): Unique user identifier

**Response:** Updated event type with new expiration date.

---

#### `POST /event-types/{event_id}/toggle-auto-renewal`
Enable or disable auto-renewal for an event type.

**Parameters:**
- `event_id` (integer, required, path): Event type ID
- `user_id` (string, required): Unique user identifier
- `enabled` (boolean, required): Auto-renewal state (true/false)

**Response:** Updated event type with auto-renewal status.

---

### Availability Management

#### `POST /availability`
Set availability rules for scheduling.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Request Body:** Array of availability rules:
- `day_of_week` (integer, required): Day 0=Monday to 6=Sunday
- `start_time` (string, required): Start time in HH:MM format
- `end_time` (string, required): End time in HH:MM format

**Response:** Confirmation of availability rules saved.

---

#### `GET /availability`
Get all availability rules for a user.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Response:** Array of availability rules with day, start time, and end time.

---

#### `GET /available-slots`
Get time slots with availability status for a specific date.

**Parameters:**
- `user_id` (string, required): Unique user identifier
- `event_type_slug` (string, required): Event type slug
- `date` (string, required): Date in YYYY-MM-DD format

**Response:** Array of available time slots with:
- `time`: Slot time in HH:MM format
- `available`: Boolean availability status
- `booked_by`: Guest name if booked

---

### Booking Management

#### `POST /bookings`
Create a new booking.

**Parameters:** None

**Request Body:**
- `event_type_slug` (string, required): Event type slug
- `guest_name` (string, required): Guest's full name
- `guest_email` (string, required): Guest's email address
- `start_time` (string, required): Booking start time in ISO 8601 format
- `timezone` (string, required): Guest's timezone (e.g., America/New_York)
- `notes` (string, optional): Additional booking notes

**Response:** Created booking object with confirmation details.

---

#### `GET /bookings`
Get all bookings for a user.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Response:** Array of bookings with guest info, times, and status.

---

#### `DELETE /bookings/{booking_id}`
Cancel a booking.

**Parameters:**
- `booking_id` (string, required, path): Booking ID
- `user_id` (string, required): Unique user identifier

**Response:** Cancellation confirmation.

---

### User Management

#### `GET /user/info`
Get user information and profile details.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Response:** User object with name, email, timezone, and account status.

---

#### `POST /user/timezone`
Update user's timezone setting.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Request Body:**
- `timezone` (string, required): Timezone identifier (e.g., America/Los_Angeles)

**Response:** Updated user profile with new timezone.

---

#### `POST /user/sync-wordpress-name`
Fetch and sync WordPress user's display name.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Response:** Updated user profile with synced display name.

---

#### `POST /user/init`
Initialize a user without Google OAuth (standalone mode).

**Parameters:**
- `user_id` (string, required): Unique user identifier
- `name` (string, optional): User's display name
- `email` (string, optional): User's email address

**Response:** Initialized user profile with account created timestamp.

---

### Blocked Dates Management

#### `GET /blocked-dates`
Get all blocked dates for a user.

**Parameters:**
- `user_id` (string, required): Unique user identifier

**Response:** Array of blocked dates with:
- `id`: Blocked date ID
- `date`: Blocked date in YYYY-MM-DD format
- `reason`: Optional reason for blocking

---

#### `POST /blocked-dates`
Add a blocked date.

**Parameters:**
- `user_id` (string, required): Unique user identifier
- `date_str` (string, required): Date in YYYY-MM-DD format
- `reason` (string, optional): Reason for blocking

**Response:** Created blocked date object.

---

#### `DELETE /blocked-dates/{blocked_id}`
Remove a blocked date.

**Parameters:**
- `blocked_id` (integer, required, path): Blocked date ID
- `user_id` (string, required): Unique user identifier

**Response:** Deletion confirmation.

---

### Public Booking Page

#### `GET /public/{user_id}/{slug}`
Get public booking page information without authentication.

**Parameters:**
- `user_id` (string, required, path): User identifier
- `slug` (string, required, path): Event type slug

**Response:** Public event type details with available slots for booking.

---

### Scheduler

#### `POST /scheduler/process-expirations`
Process all expiring events, auto-renewals, and send notifications.

**Note:** This endpoint should be called daily by a cron job.

**Parameters:** None

**Response:** Processing summary with count of processed expirations and renewals.

---

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.toolweb.in/tools/scheduly
- **API Docs:** https://api.toolweb.in:8160/docs
