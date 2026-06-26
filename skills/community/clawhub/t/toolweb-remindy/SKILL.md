---
name: Remindy - Smart Reminder Service
description: Email and browser push notification reminders delivered 15 minutes before scheduled events.
---

# Overview

Remindy is a smart reminder service that delivers timely notifications via email and browser push notifications. The service automatically triggers reminders 15 minutes before your scheduled events, ensuring you never miss important dates, meetings, or tasks. Built with security best practices, Remindy integrates seamlessly with web applications through push subscription management and flexible reminder scheduling.

Remindy supports multiple notification channels including email and browser push notifications, with full timezone awareness. Users can create, manage, and delete reminders while maintaining complete control over their notification preferences. The service uses the Web Push Protocol (VAPID) for secure browser notifications, making it ideal for productivity applications, event management systems, and personal scheduling tools.

Whether you're building a project management platform, calendar application, or task tracking system, Remindy provides a reliable backend for user notification management with minimal integration overhead.

## Usage

### Create a Reminder

```json
POST /api/reminders/create

{
  "userId": 12345,
  "title": "Team Meeting",
  "description": "Quarterly planning session with stakeholders",
  "remindAt": "2025-01-15T14:00:00",
  "timezone": "America/New_York",
  "channel": "email",
  "notifyEmail": "john.doe@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "reminderId": "reminder_abc123xyz",
  "message": "Reminder created successfully",
  "scheduledFor": "2025-01-15T14:00:00"
}
```

### List Reminders

```json
POST /api/reminders/list

{
  "userId": 12345
}
```

**Response:**
```json
{
  "reminders": [
    {
      "reminderId": "reminder_abc123xyz",
      "title": "Team Meeting",
      "description": "Quarterly planning session with stakeholders",
      "remindAt": "2025-01-15T14:00:00",
      "timezone": "America/New_York",
      "channel": "email",
      "status": "active",
      "createdAt": "2025-01-10T09:30:00"
    },
    {
      "reminderId": "reminder_def456uvw",
      "title": "Project Deadline",
      "description": null,
      "remindAt": "2025-01-20T17:00:00",
      "timezone": "UTC",
      "channel": "push",
      "status": "active",
      "createdAt": "2025-01-10T10:15:00"
    }
  ],
  "total": 2
}
```

## Endpoints

### Push Notifications

#### `POST /api/push/subscribe`
Save or update a user's push subscription for browser notifications.

**Parameters:**
- `userId` (integer, required): Unique user identifier
- `endpoint` (string, required): Browser push service endpoint URL
- `p256dh` (string, required): Diffie-Hellman public key for encryption
- `auth` (string, required): Authentication secret for push messages

**Response:** 
```json
{
  "success": true,
  "message": "Push subscription saved"
}
```

---

#### `POST /api/push/unsubscribe`
Remove a user's push subscription.

**Parameters:**
- `userId` (integer, required): Unique user identifier

**Response:**
```json
{
  "success": true,
  "message": "Push subscription removed"
}
```

---

#### `GET /api/push/vapid-public-key`
Retrieve the VAPID public key required for client-side push notification setup.

**Parameters:** None

**Response:**
```json
{
  "publicKey": "BEX_public_key_base64_encoded_string"
}
```

---

#### `POST /api/push/status`
Check whether a user has an active push subscription.

**Parameters:**
- `userId` (integer, required): Unique user identifier

**Response:**
```json
{
  "userId": 12345,
  "subscribed": true,
  "endpoint": "https://...",
  "subscribedAt": "2025-01-10T08:30:00"
}
```

---

### Reminders

#### `POST /api/reminders/create`
Create a new reminder with email and/or push notification settings.

**Parameters:**
- `userId` (integer, required): Unique user identifier
- `title` (string, required): Reminder title
- `description` (string, optional): Detailed description of the reminder
- `remindAt` (string, required): ISO 8601 datetime when reminder should trigger
- `timezone` (string, optional, default: "UTC"): IANA timezone identifier
- `channel` (string, optional, default: "email"): Notification channel ("email" or "push")
- `notifyEmail` (string, optional): Email address for notification (required if channel is "email")

**Response:**
```json
{
  "success": true,
  "reminderId": "reminder_abc123xyz",
  "scheduledFor": "2025-01-15T14:00:00"
}
```

---

#### `POST /api/reminders/list`
Retrieve all reminders for a specific user.

**Parameters:**
- `userId` (integer, required): Unique user identifier

**Response:**
```json
{
  "reminders": [
    {
      "reminderId": "string",
      "title": "string",
      "description": "string or null",
      "remindAt": "string (ISO 8601)",
      "timezone": "string",
      "channel": "string",
      "status": "string",
      "createdAt": "string (ISO 8601)"
    }
  ],
  "total": 0
}
```

---

#### `POST /api/reminders/delete`
Delete a reminder by ID.

**Parameters:**
- `reminderId` (string, required): Unique reminder identifier
- `userId` (integer, required): Unique user identifier

**Response:**
```json
{
  "success": true,
  "message": "Reminder deleted successfully"
}
```

---

### Health & Status

#### `GET /`
Root endpoint returning service information.

**Response:**
```json
{
  "service": "Remindy",
  "version": "2.0.0",
  "status": "operational"
}
```

---

#### `GET /health`
Health check endpoint for monitoring service availability.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-10T12:00:00Z"
}
```

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

- **Kong Route:** https://api.toolweb.in/tools/remindy
- **API Docs:** https://api.toolweb.in:8198/docs
