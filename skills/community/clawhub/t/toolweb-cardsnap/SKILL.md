---
name: CardSnap API
description: Digital Business Card Generator — create, manage, and track shareable business cards with analytics.
---

# Overview

CardSnap API is a comprehensive digital business card generation platform that enables users to create, customize, and share professional business cards in a modern digital format. Built on a secure, CISSP-certified infrastructure, CardSnap simplifies the process of creating branded digital business cards with support for multiple social media profiles, contact information, and customizable themes.

The API provides full lifecycle management for digital business cards, including creation, retrieval, updates, and deletion. Beyond card management, CardSnap includes built-in analytics to track engagement metrics such as views, saves, and shares—giving professionals insights into how their cards are being received and shared across networks.

CardSnap is ideal for sales professionals, entrepreneurs, consultants, recruiters, and any business professional seeking a modern alternative to traditional printed business cards. The platform supports rich contact information, social media integration, and real-time engagement tracking to maximize networking effectiveness.

## Usage

### Create a Digital Business Card

```json
POST /cards
Content-Type: application/json

{
  "slug": "john-doe-dev",
  "data": {
    "firstName": "John",
    "lastName": "Doe",
    "title": "Senior Software Engineer",
    "company": "TechCorp Inc.",
    "bio": "Full-stack developer passionate about cloud architecture and security.",
    "phone": "+1-555-123-4567",
    "email": "john.doe@techcorp.com",
    "website": "https://johndoe.dev",
    "location": "San Francisco, CA",
    "linkedin": "https://linkedin.com/in/johndoe",
    "twitter": "https://twitter.com/johndoe",
    "github": "https://github.com/johndoe",
    "instagram": "https://instagram.com/johndoe",
    "whatsapp": "+1-555-123-4567",
    "theme": "ocean",
    "photo": "https://example.com/photos/john-doe.jpg"
  }
}
```

**Response (201 Created):**

```json
{
  "id": "card_12345abcde",
  "slug": "john-doe-dev",
  "data": {
    "firstName": "John",
    "lastName": "Doe",
    "title": "Senior Software Engineer",
    "company": "TechCorp Inc.",
    "bio": "Full-stack developer passionate about cloud architecture and security.",
    "phone": "+1-555-123-4567",
    "email": "john.doe@techcorp.com",
    "website": "https://johndoe.dev",
    "location": "San Francisco, CA",
    "linkedin": "https://linkedin.com/in/johndoe",
    "twitter": "https://twitter.com/johndoe",
    "github": "https://github.com/johndoe",
    "instagram": "https://instagram.com/johndoe",
    "whatsapp": "+1-555-123-4567",
    "theme": "ocean",
    "photo": "https://example.com/photos/john-doe.jpg"
  },
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Track Card Engagement

```json
POST /cards/john-doe-dev/analytics
Content-Type: application/json

{
  "event": "view"
}
```

**Response (200 OK):**

```json
{
  "message": "Event tracked successfully",
  "event": "view",
  "timestamp": "2024-01-15T10:35:22Z"
}
```

### Retrieve Card Analytics

```json
GET /cards/john-doe-dev/analytics
```

**Response (200 OK):**

```json
{
  "slug": "john-doe-dev",
  "total_views": 42,
  "total_saves": 8,
  "total_shares": 3,
  "engagement_rate": 0.38,
  "last_viewed": "2024-01-15T10:35:22Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Endpoints

### `GET /`
**Summary:** Root

**Description:** Health check endpoint that returns API status.

**Parameters:** None

**Response:** 200 OK with API status object.

---

### `GET /health`
**Summary:** Health

**Description:** Service health check endpoint.

**Parameters:** None

**Response:** 200 OK with health status.

---

### `POST /cards`
**Summary:** Create Card

**Description:** Create a new digital business card with customizable profile information and theme settings.

**Parameters:**
- **Request Body** (required): `CardCreate` object
  - `slug` (string, optional): Custom URL-friendly identifier (max 50 chars, alphanumeric, dash, underscore). If not provided, a unique slug is auto-generated.
  - `data` (object, required): `CardData` object containing card information

**CardData Parameters:**
- `firstName` (string, required, max 100 chars): First name of the card owner
- `lastName` (string, optional, max 100 chars): Last name of the card owner
- `title` (string, optional, max 200 chars): Professional title or job position
- `company` (string, optional, max 200 chars): Company or organization name
- `bio` (string, optional, max 500 chars): Professional biography or brief description
- `phone` (string, optional, max 20 chars): Phone number in any format
- `email` (string, optional, max 200 chars): Email address
- `website` (string, optional, max 300 chars): Personal or business website URL
- `location` (string, optional, max 200 chars): City, region, or geographic location
- `linkedin` (string, optional, max 300 chars): LinkedIn profile URL
- `twitter` (string, optional, max 300 chars): Twitter/X profile URL
- `github` (string, optional, max 300 chars): GitHub profile URL
- `instagram` (string, optional, max 300 chars): Instagram profile URL
- `whatsapp` (string, optional, max 20 chars): WhatsApp phone number
- `theme` (string, optional, max 20 chars, default: "ocean"): Card design theme name
- `photo` (string, optional, max 500 chars): Profile photo URL

**Response:** 201 Created with full card object including ID, timestamps, and all provided data.

---

### `GET /cards/{slug}`
**Summary:** Get Card

**Description:** Retrieve a specific digital business card by its unique slug identifier.

**Parameters:**
- `slug` (string, required, path): The unique card identifier or URL slug

**Response:** 200 OK with complete card object and all associated data.

---

### `PUT /cards/{slug}`
**Summary:** Update Card

**Description:** Update an existing digital business card's information and settings.

**Parameters:**
- `slug` (string, required, path): The unique card identifier to update
- **Request Body** (required): `CardUpdate` object
  - `data` (object, required): `CardData` object with fields to update (same structure as creation)

**Response:** 200 OK with updated card object reflecting all changes.

---

### `DELETE /cards/{slug}`
**Summary:** Delete Card

**Description:** Permanently delete a digital business card and all associated data.

**Parameters:**
- `slug` (string, required, path): The unique card identifier to delete

**Response:** 200 OK with confirmation message.

---

### `POST /cards/{slug}/analytics`
**Summary:** Track Event

**Description:** Record user engagement events (view, save, or share) for a specific card to track reach and engagement metrics.

**Parameters:**
- `slug` (string, required, path): The unique card identifier
- **Request Body** (required): `AnalyticsEvent` object
  - `event` (string, required, enum): Type of engagement event: `view`, `save`, or `share`

**Response:** 200 OK with event confirmation and timestamp.

---

### `GET /cards/{slug}/analytics`
**Summary:** Get Analytics

**Description:** Retrieve comprehensive engagement analytics and usage statistics for a specific card.

**Parameters:**
- `slug` (string, required, path): The unique card identifier

**Response:** 200 OK with analytics object containing:
- `total_views`: Count of card views
- `total_saves`: Count of card saves
- `total_shares`: Count of card shares
- `engagement_rate`: Calculated engagement percentage
- `last_viewed`: ISO timestamp of most recent view
- `created_at`: Card creation timestamp

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

- **Kong Route:** https://api.toolweb.in/tools/cardsnap
- **API Docs:** https://api.toolweb.in:8185/docs
