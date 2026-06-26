---
name: Seek Alliance - Marriage Matching Backend
description: Generates bride and groom horoscopes then produces a marriage compatibility report with PDF outputs.
---

# Overview

Seek Alliance is a marriage compatibility analysis platform that leverages Vedic astrology to evaluate the astrological compatibility between potential marriage partners. The service generates detailed horoscopes for both the bride and groom based on their birth data, then produces a comprehensive marriage compatibility report in PDF format.

This tool is ideal for matrimonial platforms, astrology consultants, and individuals seeking detailed astrological insights into potential marriages. By analyzing planetary positions and natal chart configurations, the API provides scientifically-grounded astrological assessments that help couples understand their cosmic compatibility across multiple dimensions.

The platform supports multiple Indian languages (Tamil, English, Malayalam, Telugu, Kannada, and Hindi) and both South Indian and North Indian astrological chart systems, making it accessible to diverse user bases across India and the diaspora.

## Usage

### Request

To generate a marriage compatibility report, submit birth details for both the bride and groom. The system will generate three PDF reports: one for the bride's horoscope, one for the groom's horoscope, and one comprehensive marriage matching report.

```json
{
  "bride": {
    "person_name": "Anjali Sharma",
    "father_name": "Rajesh Sharma",
    "mother_name": "Priya Sharma",
    "mobile": "9876543210",
    "dob": "15/Jan/1995",
    "hour": "10",
    "minute": "30",
    "am_pm": "AM",
    "country": "India",
    "birth_place": "Chennai"
  },
  "groom": {
    "person_name": "Arjun Patel",
    "father_name": "Vikram Patel",
    "mother_name": "Meera Patel",
    "mobile": "9123456789",
    "dob": "22/Mar/1993",
    "hour": "02",
    "minute": "15",
    "am_pm": "PM",
    "country": "India",
    "birth_place": "Bangalore"
  },
  "language_id": "2",
  "chart_type": "South Indian"
}
```

### Response

```json
{
  "success": true,
  "message": "Marriage compatibility analysis completed successfully",
  "bride_pdf_url": "https://api.mkkpro.com/downloads/Anjali_Sharma_horoscope_1234567890.pdf",
  "groom_pdf_url": "https://api.mkkpro.com/downloads/Arjun_Patel_horoscope_1234567890.pdf",
  "match_pdf_url": "https://api.mkkpro.com/downloads/marriage_match_report_1234567890.pdf",
  "generated_at": "2024-01-15T14:30:00Z"
}
```

## Endpoints

### POST /api/seek-alliance

Generates horoscopes and marriage compatibility report for a bride-groom pair.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| bride | PersonData object | Yes | Bride (female) personal and birth details |
| groom | PersonData object | Yes | Groom (male) personal and birth details |
| language_id | string | No | Language for report generation: `1`=Tamil, `2`=English, `3`=Malayalam, `4`=Telugu, `5`=Kannada, `6`=Hindi (default: `1`) |
| chart_type | string | No | Astrological chart system: `South Indian` or `North Indian` (default: `South Indian`) |

**PersonData Fields:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| person_name | string | Yes | Person's full name |
| father_name | string | Yes | Father's name |
| mother_name | string | Yes | Mother's name |
| mobile | string | Yes | 10-digit mobile number |
| dob | string | Yes | Date of birth in DD/Mon/YYYY format (e.g., `15/Jan/1995`) |
| hour | string | Yes | Birth hour in 12-hour format (1-12) |
| minute | string | Yes | Birth minute (00-59) |
| am_pm | string | Yes | Time period: `AM` or `PM` |
| country | string | Yes | Country code or name |
| birth_place | string | Yes | Birth city name |

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the operation completed successfully |
| message | string \| null | Human-readable status or error message |
| bride_pdf_url | string \| null | URL to download the bride's horoscope PDF |
| groom_pdf_url | string \| null | URL to download the groom's horoscope PDF |
| match_pdf_url | string \| null | URL to download the marriage compatibility report PDF |
| generated_at | string \| null | ISO 8601 timestamp of report generation |

**Response Codes:**

- `200 OK` - Reports generated successfully
- `422 Unprocessable Entity` - Validation error in request data

---

### GET /api/search-city

Search for a city to retrieve accurate coordinates and timezone information for birth location.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| search | string | Yes | City name or partial city name to search |
| country | string | No | Country filter (default: `India`) |

**Response Schema:**

Returns JSON array of matching cities with geographic and timezone data for accurate horoscope calculations.

**Response Codes:**

- `200 OK` - Cities found
- `422 Unprocessable Entity` - Validation error

---

### GET /api/status

Check the health and operational status of the API service.

**Parameters:** None

**Response Schema:**

Returns JSON object indicating service status and uptime information.

**Response Codes:**

- `200 OK` - Service is operational

---

### GET /

Root endpoint providing API information and available operations.

**Parameters:** None

**Response Schema:**

Returns JSON with API metadata and endpoint summary.

**Response Codes:**

- `200 OK` - Service is available

---

### GET /downloads/{filename}

Download generated PDF reports using the filename provided in the alliance response.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| filename | string | Yes | Name of the file to download (from bride_pdf_url, groom_pdf_url, or match_pdf_url response) |

**Response:** PDF file binary data

**Response Codes:**

- `200 OK` - File downloaded successfully
- `422 Unprocessable Entity` - Invalid filename

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

- **Kong Route:** https://api.mkkpro.com/lifestyle/marriage-matching
- **API Docs:** https://api.mkkpro.com:8197/docs
