---
name: travel-itinerary-builder
description: "Comprehensive travel itinerary generator that creates detailed, multi-day trip plans with automatic weather forecasts, points of interest, restaurant recommendations, transportation logistics, and budget estimates. Generates print-ready HTML documents with dark theme styling. Use when: (1) Planning a trip and need a complete itinerary, (2) User provides destination(s) and dates, (3) Organizing travel bookings (flights, hotels, car rentals) from Gmail, (4) Need multi-language support for destination names, (5) Creating printable travel documents, (6) Estimating travel budgets and costs."
metadata:
  openclaw:
    emoji: "🌍"
    requires:
      bins:
        - curl
    optionalBins:
      - gog
      - goplaces
    optionalEnv:
      - GOG_KEYRING_PASSWORD
      - GOOGLE_PLACES_API_KEY
    install:
      - id: gog
        kind: brew
        formula: gogcli
        bins:
          - gog
        label: "Install GOG (Google OAuth CLI) for Gmail parsing (optional)"
      - id: goplaces
        kind: brew
        formula: steipete/tap/goplaces
        bins:
          - goplaces
        label: "Install goplaces for Google Places API (optional)"
---

# Travel Itinerary Builder

Generate comprehensive, print-ready travel itineraries with automatic integration of weather, places, dining, transportation, and budget planning.

## ⚠️ Security & Privacy Notice

**This skill accesses sensitive data and requires external credentials:**

### Gmail Access (Optional)
- The `gmail_parser.py` script **reads your Gmail messages** to extract booking confirmations
- Requires `GOG_KEYRING_PASSWORD` environment variable (for GOG CLI authentication)
- **What it accesses**: Email subjects, snippets, and full message bodies matching search queries
- **What it extracts**: Flight details (PNR, times), hotel bookings, car rentals, activity tickets
- **Data handling**: Extracted data is stored locally in JSON files; no external transmission

### Google Places API (Optional)
- The `places_fetcher.py` script queries Google Places for attractions
- Requires `GOOGLE_PLACES_API_KEY` environment variable (free tier: 1000 requests/month)
- Fallback to built-in database if API key not provided

### External CLI Dependencies
- **gog** (Google OAuth CLI): Authenticates Gmail access via OAuth2
- **goplaces**: Queries Google Places API
- **curl**: Fetches weather data from wttr.in

**Before installing**:
1. Review all scripts in `scripts/` directory
2. Only provide credentials if you trust the external CLIs
3. Consider running in an isolated environment (container/VM)
4. Gmail integration is **optional** — you can use the skill without it

## Quick Start

### Basic Usage

```bash
# Generate itinerary from user input
python3 scripts/generate_itinerary.py \
  --destination "Tokyo, Osaka, Kyoto" \
  --start-date "2026-03-06" \
  --end-date "2026-03-15" \
  --language zh \
  --output ./japan_trip.html
```

### With Gmail Integration

```bash
# Extract bookings from Gmail and generate itinerary
python3 scripts/gmail_parser.py \
  --account rachelchoo1212@gmail.com \
  --after "2026-03-01" \
  --output ./bookings.json

python3 scripts/generate_itinerary.py \
  --bookings ./bookings.json \
  --destination "Tokyo, Osaka" \
  --start-date "2026-03-06" \
  --end-date "2026-03-15" \
  --output ./trip.html
```

## Core Features

### 1. Automatic Data Collection
- **Weather forecasts**: Integrates with `weather` skill for daily forecasts
- **Points of interest**: Uses `goplaces` skill for attractions, restaurants, landmarks
- **Multi-language names**: Shows place names in user language + local language
- **Gmail parsing**: Extracts flight, hotel, car rental bookings from confirmation emails

### 2. Intelligent Planning
- **Daily schedules**: Auto-generates time-based itineraries (08:00 departure → 10:00 attraction → 12:00 lunch)
- **Transportation routing**: Calculates distances, travel times, and costs for driving/transit
- **Budget estimation**: Computes total costs for accommodation, meals, transport, tickets
- **Packing lists**: Generates climate-appropriate packing suggestions

### 3. Output Formats
- **HTML**: Beautiful dark-themed, print-ready documents (based on proven template)
- **Markdown**: Editable plain-text format
- **JSON**: Structured data for further processing
- **PDF**: Optional export via HTML → PDF conversion

## Workflow

### Step 1: Gather Information

Ask user for:
- Destinations (cities/regions)
- Travel dates (start and end)
- Budget range (optional)
- Interests/tags (history, nature, food, shopping, concerts)
- Language preference (zh, en, ja, ko)
- Special requirements (dietary, accessibility, child-friendly)

### Step 2: Extract Existing Bookings (Optional)

If user has Gmail access configured:

```bash
python3 scripts/gmail_parser.py \
  --account <email> \
  --after <YYYY-MM-DD> \
  --keywords "flight,hotel,booking,reservation,confirmation" \
  --output bookings.json
```

This extracts:
- ✈️ Flights: airline, flight number, departure/arrival times, PNR
- 🏨 Hotels: name, address, check-in/out dates, booking number, price
- 🚗 Car rentals: company, car type, pickup/return times, booking number
- 🎫 Tickets: concerts, museums, activities with times and seat info

Supported platforms: Agoda, Booking.com, Singapore Airlines, ANA, Trip.com, Klook, KKday

### Step 3: Query Weather and Places

```bash
# Weather forecasts for each destination
python3 scripts/weather_fetcher.py \
  --destinations "Tokyo,Osaka,Kyoto" \
  --start-date "2026-03-06" \
  --end-date "2026-03-15" \
  --output weather.json

# Points of interest
python3 scripts/places_fetcher.py \
  --destinations "Tokyo,Osaka,Kyoto" \
  --interests "temples,food,shopping" \
  --language zh \
  --output places.json
```

### Step 4: Generate Itinerary

```bash
python3 scripts/generate_itinerary.py \
  --bookings bookings.json \
  --weather weather.json \
  --places places.json \
  --start-date "2026-03-06" \
  --end-date "2026-03-15" \
  --budget 2000 \
  --currency SGD \
  --language zh \
  --output japan_trip.html
```

### Step 5: Export (Optional)

```bash
# Export to PDF
python3 scripts/export_pdf.py japan_trip.html japan_trip.pdf

# Sync to Notion (if configured)
python3 scripts/sync_notion.py japan_trip.json
```

## Scripts Reference

### `generate_itinerary.py`
Core generator. Combines all data sources into a complete itinerary.

**Arguments**:
- `--destination`: Comma-separated list of cities/regions
- `--start-date`: Trip start date (YYYY-MM-DD)
- `--end-date`: Trip end date (YYYY-MM-DD)
- `--bookings`: Path to bookings JSON (from gmail_parser.py)
- `--weather`: Path to weather JSON (from weather_fetcher.py)
- `--places`: Path to places JSON (from places_fetcher.py)
- `--budget`: Total budget amount (optional)
- `--currency`: Currency code (SGD, USD, JPY, etc.)
- `--language`: Output language (zh, en, ja, ko)
- `--interests`: Comma-separated tags (history, nature, food, shopping, concerts)
- `--output`: Output file path (.html, .md, or .json)

### `gmail_parser.py`
Extracts travel bookings from Gmail using GOG skill.

**Requirements**: GOG_KEYRING_PASSWORD environment variable

**Arguments**:
- `--account`: Gmail account email
- `--after`: Start date for email search (YYYY-MM-DD)
- `--keywords`: Search keywords (default: "flight,hotel,booking,confirmation")
- `--output`: Output JSON file

### `weather_fetcher.py`
Fetches weather forecasts for destinations using weather skill.

**Arguments**:
- `--destinations`: Comma-separated cities
- `--start-date`: Forecast start date
- `--end-date`: Forecast end date
- `--output`: Output JSON file

### `places_fetcher.py`
Queries points of interest using goplaces skill.

**Arguments**:
- `--destinations`: Comma-separated cities
- `--interests`: Activity tags (temples, museums, food, shopping)
- `--language`: Display language
- `--output`: Output JSON file

### `translator.py`
Translates place names to multiple languages.

**Arguments**:
- `--text`: Text to translate
- `--source-lang`: Source language code
- `--target-langs`: Comma-separated target language codes
- `--output`: Output JSON file

### `budget_calculator.py`
Estimates trip costs based on destination, duration, and bookings.

**Arguments**:
- `--destination`: Primary destination
- `--days`: Number of days
- `--bookings`: Path to bookings JSON
- `--category`: Budget category (budget, mid-range, luxury)
- `--output`: Output JSON file

### `export_html.py`
Converts itinerary JSON to styled HTML using template.

**Arguments**:
- `--input`: Itinerary JSON file
- `--template`: HTML template (default: assets/itinerary_template.html)
- `--output`: Output HTML file

## References

- **destination_templates.md**: Pre-built templates for popular destinations (Tokyo, Seoul, Paris, etc.)
- **travel_tips.md**: Climate guides, packing lists, visa requirements, cultural tips
- **email_patterns.md**: Email parsing rules for different booking platforms
- **poi_database.md**: Common attractions with multi-language names

## Assets

- **itinerary_template.html**: Dark-themed HTML template with CSS styling
- **icons/**: SVG icons for flights, hotels, restaurants, attractions
- **fonts/**: Web fonts for print-quality output

## Multi-Language Support

Place names are displayed in **user language + local language**:

```
东京塔 (東京タワー / Tokyo Tower)
和歌山城 (和歌山城 / Wakayama Castle)
```

Supported languages: Chinese (zh), English (en), Japanese (ja), Korean (ko)

## Output Example

Generated HTML includes:
- 📅 **Day-by-day timeline** with emoji icons
- 🌤️ **Daily weather** forecasts
- ✈️ **Flight details** with boarding times
- 🏨 **Hotel information** with check-in/out
- 🚗 **Driving routes** with distances and tolls
- 🍽️ **Restaurant recommendations** with local specialties
- 💰 **Budget breakdown** by category
- 📋 **Packing checklist** based on climate
- ⚠️ **Important reminders** (visa, insurance, IDP)

## Integration with Other Skills

This skill calls:
- `weather` — Daily forecasts
- `goplaces` — Attraction and restaurant search
- `gog` — Gmail parsing (optional, requires GOG_KEYRING_PASSWORD)
- `notion` — Sync to Notion database (optional, requires Notion API key)

## Tips

- **For self-driving trips**: Include rental car details, calculate fuel costs, note toll roads
- **For concert/event trips**: Add venue info, seating, merchandise shop times
- **For multi-city trips**: Calculate transit times between cities
- **For international trips**: Include visa requirements, vaccination, travel insurance reminders

## Troubleshooting

- **Gmail parsing fails**: Check GOG_KEYRING_PASSWORD is set and account has access
- **Weather data missing**: Ensure dates are within forecast range (usually 10 days)
- **Places not found**: Try broader search terms or check goplaces API key
- **HTML rendering issues**: Open in modern browser (Chrome, Firefox, Safari)

## Future Enhancements

- Real-time flight status updates
- Amadeus API integration for flight price tracking
- Google Sheets export for budget tracking
- PDF generation without external tools
- Mobile-responsive HTML output
