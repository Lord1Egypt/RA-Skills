---
name: Presently API
description: AI-powered API for generating structured presentations from text input with customizable themes and formatting options.
---

# Overview

Presently API is an intelligent presentation generation service that transforms raw text input into professionally formatted slide decks. Built for developers, content creators, and businesses seeking to automate presentation creation, Presently intelligently structures content into logical slides with customizable themes, colors, and layouts.

The API accepts plain text content and automatically organizes it into a specified number of presentation cards, each optimized for visual delivery. With support for theme customization, color schemes, and format variations, Presently enables programmatic generation of polished presentations without manual slide design.

Ideal users include content management systems, educational platforms, business automation tools, and SaaS applications requiring dynamic presentation generation capabilities.

## Usage

**Sample Request:**

```json
{
  "user_id": 12345,
  "input_text": "Cloud computing has revolutionized how organizations manage data. It provides scalable infrastructure, reduces operational costs, and enables global collaboration. Major providers include AWS, Azure, and Google Cloud. Security considerations include data encryption, access control, and compliance standards. Best practices involve multi-region deployment, automated backups, and disaster recovery planning.",
  "num_cards": 5,
  "format_type": "presentation",
  "theme_id": "modern_blue",
  "primary_color": "#1E40AF",
  "secondary_color": "#60A5FA",
  "user_email": "user@example.com"
}
```

**Sample Response:**

```json
{
  "presentation_id": "pres_8f4a2c9d1e",
  "user_id": 12345,
  "status": "success",
  "cards": [
    {
      "card_number": 1,
      "title": "Cloud Computing Fundamentals",
      "content": "Cloud computing has revolutionized how organizations manage data. It provides scalable infrastructure, reduces operational costs, and enables global collaboration."
    },
    {
      "card_number": 2,
      "title": "Major Cloud Providers",
      "content": "Major providers include AWS, Azure, and Google Cloud."
    },
    {
      "card_number": 3,
      "title": "Security Considerations",
      "content": "Security considerations include data encryption, access control, and compliance standards."
    },
    {
      "card_number": 4,
      "title": "Best Practices",
      "content": "Best practices involve multi-region deployment, automated backups, and disaster recovery planning."
    },
    {
      "card_number": 5,
      "title": "Implementation Strategy",
      "content": "Organizations should evaluate workload requirements and select providers aligned with compliance needs."
    }
  ],
  "theme_applied": "modern_blue",
  "colors": {
    "primary": "#1E40AF",
    "secondary": "#60A5FA"
  },
  "created_at": "2024-01-15T14:32:22Z"
}
```

## Endpoints

### GET /health

**Summary:** Health Check

**Description:** Verify API service availability and health status.

**Parameters:** None

**Response:**
- **200 OK:** Service is operational
  ```json
  {
    "status": "healthy",
    "timestamp": "2024-01-15T14:32:22Z"
  }
  ```

---

### POST /create

**Summary:** Create Presentation

**Description:** Generate a structured presentation from input text with customizable styling and layout options.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | integer | Yes | Unique identifier for the user making the request |
| `input_text` | string | Yes | Source text content to structure into slides (10-100,000 characters) |
| `num_cards` | integer | No | Number of presentation slides to generate (1-50, default: 10) |
| `format_type` | string | No | Output format style (default: "presentation") |
| `theme_id` | string | No | Predefined theme identifier for visual styling |
| `primary_color` | string | No | Hex color code for primary theme color (e.g., "#1E40AF") |
| `secondary_color` | string | No | Hex color code for secondary/accent color (e.g., "#60A5FA") |
| `user_email` | string | No | Email address associated with the user account |

**Request Body:**
```json
{
  "user_id": integer,
  "input_text": "string (10-100000 chars)",
  "num_cards": integer (optional, 1-50),
  "format_type": "string (optional)",
  "theme_id": "string or null (optional)",
  "primary_color": "string or null (optional)",
  "secondary_color": "string or null (optional)",
  "user_email": "string or null (optional)"
}
```

**Response:**
- **200 OK:** Presentation generated successfully
  ```json
  {
    "presentation_id": "string",
    "user_id": integer,
    "status": "success",
    "cards": [
      {
        "card_number": integer,
        "title": "string",
        "content": "string"
      }
    ],
    "theme_applied": "string",
    "colors": {
      "primary": "string",
      "secondary": "string"
    },
    "created_at": "string (ISO 8601)"
  }
  ```

- **422 Unprocessable Entity:** Validation error
  ```json
  {
    "detail": [
      {
        "loc": ["body", "input_text"],
        "msg": "ensure this value has at least 10 characters",
        "type": "value_error.any_str.min_length"
      }
    ]
  }
  ```

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

- Kong Route: https://api.toolweb.in/tools/presently
- API Docs: https://api.toolweb.in:8174/docs
