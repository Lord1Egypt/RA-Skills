# Google Sheet Setup

## Create the Sheet

1. Go to Google Sheets and create a new spreadsheet
2. Name it something like "OpenClaw_Leads"
3. Name the first tab "leads"

## Add Column Headers (Row 1, Columns A-O)

| Column | Header | Description |
|--------|--------|-------------|
| A | created_at | ISO timestamp when lead was discovered |
| B | niche | Business category (landscaping, cleaning, etc.) |
| C | business_name | Full business name |
| D | address | Street address |
| E | phone | Phone number |
| F | email | Contact email |
| G | website | Current website URL (if any) |
| H | google_maps_url | Google Maps link |
| I | rating | Google rating (1-5) |
| J | reviews_count | Number of Google reviews |
| K | has_website | true/false |
| L | website_quality_score | 0-40 quality score |
| M | lead_score | 0-100 overall score |
| N | status | review / filtered / approved / demo_ready / failed |
| O | notes | Free text, demo URLs added here by pipeline |

## Service Account Access

1. Create a GCP project and enable the Sheets API
2. Create a service account and download the JSON key
3. Share your sheet with the service account email (Editor access)
4. Save the JSON key to `~/.openclaw/workspace/gcp-service-account.json`

## Lead Scoring

- No website: +40 points
- Weak website (quality < 20): +25 points
- Rating >= 4.0: +10 points
- 10+ reviews: +10 points
- Has phone: +10 points
- Base: +5 points
- **Minimum for review:** 60 points

## Status Flow

```
review → approved (manual) → processing (auto) → demo_ready (auto)
  ↓                                                    ↓
filtered (auto, score < 60)                     failed (auto, on error)
```
