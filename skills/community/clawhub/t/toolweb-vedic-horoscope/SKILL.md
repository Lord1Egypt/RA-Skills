---
name: Vedic Horoscope Generator
description: Generates personalized Vedic horoscopes and birth charts based on birth data and astrological calculations.
---

# Overview

The Vedic Horoscope Generator is a backend API that automates the creation of detailed horoscopes using traditional Vedic astrology principles. It processes birth information including date, time, and location to calculate planetary positions, create natal charts, and generate comprehensive astrological insights.

This tool is designed for astrology practitioners, wellness platforms, and applications requiring authentic Vedic horoscope generation. It supports multiple chart types (South Indian, North Indian) and languages, making it accessible to a global audience interested in Vedic astrological analysis.

The API handles all heavy computational work—from city lookups to PDF generation—enabling seamless integration into web and mobile applications. Results are available as downloadable PDF documents containing full birth chart analysis and horoscope predictions.

## Usage

### Generate a Horoscope

**Request:**

```json
{
  "person_name": "Rajesh Kumar",
  "father_name": "Suresh Kumar",
  "mother_name": "Priya Devi",
  "mobile": "9876543210",
  "gender": "Male",
  "dob": "15/Jan/1990",
  "hour": "10",
  "minute": "30",
  "am_pm": "AM",
  "country": "IN",
  "birth_place": "Mumbai",
  "language_id": "1",
  "chart_type": "South Indian"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Horoscope generated successfully",
  "pdf_url": "https://api.mkkpro.com/downloads/horoscope_rajesh_1234567890.pdf",
  "generated_at": "2024-01-15T10:45:30Z"
}
```

## Endpoints

### GET /api/search-city
**Summary:** Search City

Searches for cities in the VedicSage database by name, optionally filtered by country.

**Parameters:**
- `search` (string, required) - City name or partial name to search for
- `country` (string, optional, default: "India") - Country code or name to filter results

**Response:** Returns matching cities with their geographic and astrological coordinates.

---

### GET /
**Summary:** Root

Health check endpoint for the API service.

**Response:** Returns API status and basic service information.

---

### GET /api/status
**Summary:** Status

Returns the current operational status of the horoscope generation service.

**Response:** Service health status, database connectivity, and processing queue information.

---

### POST /api/generate-horoscope
**Summary:** Generate Horoscope

Generates a complete Vedic horoscope and birth chart based on provided personal and birth information.

**Request Body:**
- `person_name` (string, required) - Person's full name
- `father_name` (string, required) - Father's name
- `mother_name` (string, required) - Mother's name
- `mobile` (string, required) - 10-digit mobile number
- `gender` (string, required) - Male or Female
- `dob` (string, required) - Date of birth in DD/Mon/YYYY format
- `hour` (string, required) - Birth hour (1-12)
- `minute` (string, required) - Birth minute (00-59)
- `am_pm` (string, required) - AM or PM
- `country` (string, required) - Country code
- `birth_place` (string, required) - Birth city name
- `language_id` (string, optional, default: "1") - Language ID (1=Tamil)
- `chart_type` (string, optional, default: "South Indian") - Chart type (South Indian or North Indian)

**Response:**
- `success` (boolean) - Whether generation was successful
- `message` (string or null) - Success or error message
- `pdf_url` (string or null) - URL to download generated horoscope PDF
- `generated_at` (string or null) - ISO timestamp of generation

---

### GET /downloads/{filename}
**Summary:** Download File

Downloads a previously generated horoscope PDF file.

**Parameters:**
- `filename` (string, required) - Name of the PDF file to download

**Response:** Binary PDF file with horoscope and birth chart analysis.

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

- **Kong Route:** https://api.mkkpro.com/lifestyle/vedic-horoscope
- **API Docs:** https://api.mkkpro.com:8159/docs
