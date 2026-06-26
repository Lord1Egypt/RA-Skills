---
name: tripit
description: >
  Create and update TripIt travel plans by sending structured confirmation
  emails to plans@tripit.com. Supports flights, hotels, activities, car
  rentals, rail, and cruises. Use when: user asks to add something to TripIt,
  sync a trip to TripIt, update their itinerary, or manage travel plans.
  Requires email sending capability (e.g. MS Graph, Himalaya, or gog skill).
metadata:
  openclaw:
    emoji: "✈️"
    requires:
      bins: ["python3"]
---

# TripIt Skill

Add travel plans to TripIt by sending structured confirmation emails to `plans@tripit.com`. No API keys required — just email sending capability.

## How It Works

TripIt parses specially formatted emails ("TripIt Approved" format) into travel objects. This skill generates those emails; you send them with whatever email tool you have (MS Graph, Himalaya, gog, etc.).

**Flow:**
1. User says "add my flight to TripIt"
2. You construct JSON from their details
3. `tripit-email.py` generates the formatted email body
4. You send it to `plans@tripit.com`
5. TripIt creates the trip object within seconds

## Setup

The sender email must be associated with the user's TripIt account. Either:
- The email is the one they signed up with, OR
- They've added it at **TripIt → Settings → Connected Email Addresses**

No other configuration needed.

## Usage

### Generate a flight confirmation

```bash
echo '{"airline":"United Airlines","flight_number":"1234","class":"Economy",
  "departure_city":"San Francisco","departure_airport":"SFO",
  "departure_date":"2025-06-15","departure_time":"08:30",
  "arrival_city":"New York","arrival_airport":"JFK",
  "arrival_date":"2025-06-15","arrival_time":"17:05",
  "passenger":"Jane Smith","confirmation":"UA1234X",
  "booking_site_url":"https://www.united.com"}' \
| python3 scripts/tripit-email.py flight
```

### Generate a hotel confirmation

```bash
echo '{"hotel_name":"Hotel & Spa Napa Valley","checkin_date":"2025-06-15",
  "checkout_date":"2025-06-18","city":"Napa","state":"CA","country":"US",
  "street_address":"123 Vineyard Lane","confirmation":"NV8842",
  "number_of_guests":"2","rate":"189.00","currency":"USD"}' \
| python3 scripts/tripit-email.py hotel
```

### Generate an activity

```bash
echo '{"activity_name":"Wine Tasting Tour","location":"Sonoma Valley Vineyards",
  "start_date":"2025-06-16","start_time":"10:00",
  "end_date":"2025-06-16","end_time":"14:00",
  "city":"Sonoma","state":"CA","country":"US"}' \
| python3 scripts/tripit-email.py activity
```

### Generate a multi-item email

```bash
echo '{"items":[
  {"type":"flight","airline":"United Airlines","flight_number":"1234",
   "departure_city":"San Francisco","departure_airport":"SFO",
   "departure_date":"2025-06-15","departure_time":"08:30",
   "arrival_city":"New York","arrival_airport":"JFK",
   "arrival_date":"2025-06-15","arrival_time":"17:05",
   "passenger":"Jane Smith","confirmation":"UA1234X"},
  {"type":"hotel","hotel_name":"The Manhattan Grand","checkin_date":"2025-06-15",
   "checkout_date":"2025-06-18","city":"New York","state":"NY","country":"US",
   "confirmation":"MG7890"}
]}' \
| python3 scripts/tripit-email.py multi
```

### Include a subject line

Add `--subject` to any command to get a suggested email subject:

```bash
echo '...' | python3 scripts/tripit-email.py --subject flight
```

## Sending the Email

The script outputs the email body. You send it using whatever email tool is available.

### MS Graph (Microsoft 365 users)

```bash
BODY=$(echo '...' | python3 scripts/tripit-email.py flight)
# Use your MS Graph email sending tool to send:
#   To: plans@tripit.com
#   Subject: United Airlines SFO-JFK 2025-06-15
#   Body: $BODY (plain text)
```

### Himalaya

```bash
echo '...' | python3 scripts/tripit-email.py --subject flight > /tmp/tripit-email.txt
himalaya send --to plans@tripit.com \
  --subject "$(head -1 /tmp/tripit-email.txt | sed 's/Subject: //')" \
  --body "$(tail -n +3 /tmp/tripit-email.txt)"
```

### gog (Google OAuth)

```bash
BODY=$(echo '...' | python3 scripts/tripit-email.py flight)
gog send --to plans@tripit.com --subject "Flight confirmation" --body "$BODY"
```

## Field Reference

See [references/template-format.md](references/template-format.md) for the complete field list for each object type, including required vs optional fields and formatting rules.

## Supported Object Types

| Type | Command | Key Required Fields |
|------|---------|-------------------|
| Flight | `flight` | airline, flight_number, departure/arrival airport+date+time |
| Hotel | `hotel` | hotel_name, checkin_date, checkout_date |
| Activity | `activity` | activity_name, start_date |
| Car Rental | `car` | rental_company, pickup_date, dropoff_date |
| Rail | `rail` | carrier, departure/arrival date+time |
| Multiple | `multi` | Each item needs `type` + that type's required fields |

## Verifying Items Landed

After sending an email, confirm TripIt processed it by fetching the user's **iCal feed**:

1. The user provides their TripIt iCal URL (found at **TripIt → Settings → Calendar Feed**), e.g.:
   `https://www.tripit.com/feed/ical/private/<hash>/tripit.ics`
2. Fetch the feed and look for the newly added item (match on confirmation number, dates, or summary text)
3. If the item doesn't appear after ~60 seconds, check:
   - Was the sender email linked to the TripIt account?
   - Was the email sent as plain text (not HTML)?
   - Were all required fields present?

```bash
# Fetch and search the feed for a confirmation number
curl -s "https://www.tripit.com/feed/ical/private/<hash>/tripit.ics" \
  | grep -A5 "UA1234X"
```

**Tip:** Store the user's iCal feed URL so you can verify future sends without asking again. The URL is stable — it doesn't change unless the user regenerates it.

## Gotchas

- **Date format consistency**: Use one format per email (ISO 8601 recommended: `2026-03-15`)
- **Sender email must be linked**: TripIt ignores emails from unrecognized addresses
- **Plain text only**: Send as plain text, not HTML
- **Multi-line fields**: End with `***` on its own line (e.g., long notes or cancellation policies)
- **Processing time**: TripIt usually processes within seconds, occasionally up to a few minutes
- **Duplicates**: TripIt deduplicates by confirmation number — re-sending updates the existing entry
- **Field labels matter**: TripIt's parser is strict about label names. This script uses the exact labels from TripIt's official vendor templates. Don't hand-craft emails with different labels (e.g., "Confirmation Number" won't work — it must be "Booking confirmation #")
