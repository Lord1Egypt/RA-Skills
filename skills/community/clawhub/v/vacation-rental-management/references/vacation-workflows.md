# Vacation Rental Workflows

Detailed end-to-end workflows for common vacation rental scenarios.

---

## Workflow 1: Airbnb Turnover (Complete Example)

A guest checks out Saturday at 11am, a new guest arrives at 3pm. You need a turnover clean in between.

### Using the CLI

```bash
# 1. Record the outgoing guest's reservation
tidy-request "Guest checking out March 22 at 11am at 123 Main St"

# 2. Record the incoming guest's reservation
tidy-request "New guest checking in March 22 at 3pm, checking out March 26 at 11am, at 123 Main St"

# 3. Schedule the turnover clean in the gap
tidy-request "Schedule a 2.5-hour turnover clean at 123 Main St on March 22, between 11am and 3pm"

# 4. Attach the turnover checklist
tidy-request "Add the turnover checklist to the cleaning on March 22 at 123 Main St"

# 5. Check status
tidy-request "What's the status of the turnover clean at 123 Main St on March 22?"
```

### Using the REST API

```bash
# 1. Create the reservation
curl -X POST https://public-api.tidy.com/api/v2/guest-reservations \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "check_in": { "date": "2025-03-22", "time": "15:00" },
    "check_out": { "date": "2025-03-26", "time": "11:00" }
  }'

# 2. Check availability for the turnover window
curl "https://public-api.tidy.com/api/v2/booking-availabilities?address_id=123&service_type_key=turnover_cleaning.two_and_a_half_hours" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Book the turnover clean
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

# 4. Monitor the booking
curl https://public-api.tidy.com/api/v2/jobs/789 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Using MCP

```
login(email: "host@example.com", password: "...")
  → { token: "...", customer_id: 100 }

message_tidy("Guest checks out March 22 at 11am, new guest at 3pm at 123 Main St. Schedule turnover clean.")
  → { id: 5001, status: "processing", is_complete: false }

get_message_tidy(5001)
  → { id: 5001, status: "processing", is_complete: false }

get_message_tidy(5001)
  → { id: 5001, status: "completed", is_complete: true,
      response_message: "Done! I've scheduled a 2.5-hour turnover cleaning at 123 Main St on March 22 between 11:00 AM and 3:00 PM." }
```

---

## Workflow 2: Multi-Property Weekly Schedule

You manage 3 Airbnb listings. Here's how to check and coordinate the week:

```bash
# See everything at a glance
tidy-request "What guest reservations and cleanings do I have this week across all properties?"

# Schedule cleanings based on the reservations
tidy-request "Schedule turnover cleans after every checkout this week"

# Check a specific property
tidy-request "Show me the schedule for 456 Oak Ave this week"
```

### Setting up multiple properties

```bash
tidy-request "Add 123 Main St, Austin TX 78701. Gate code 1234, park in driveway."
tidy-request "Add 456 Oak Ave, Austin TX 78702. Key in lockbox code 5678, street parking."
tidy-request "Add 789 Beach Dr, Galveston TX 77550. Key under mat, guest parking lot."
```

---

## Workflow 3: Last-Minute Booking Change

A guest extends their stay by 2 days:

```bash
# Guest tells you they want to extend
tidy-request "The guest at 123 Main St is extending from March 25 to March 27"

# The turnover clean auto-adjusts if booked through TIDY
# Or manually reschedule:
tidy-request "Reschedule the turnover clean at 123 Main St from March 25 to March 27, same time window"
```

A guest cancels:

```bash
tidy-request "Guest cancelled the reservation at 456 Oak Ave for next week. Cancel the turnover clean too."
```

New last-minute booking:

```bash
tidy-request "Just got a booking at 789 Beach Dr. Guest arrives tomorrow at 4pm. Need a deep clean before then."
```

---

## Workflow 4: Seasonal Rate and Availability Check

Before accepting a booking, check if cleaning is available and affordable:

```bash
# Check what time slots are open
tidy-request "What's available for a turnover clean at the beach house on July 4th?"

# Check pricing / acceptance probability
tidy-request "What are the chances of getting a cleaner on July 4th between 11am and 3pm at the beach house?"
```

Via REST API:

```bash
# Availability
curl "https://public-api.tidy.com/api/v2/booking-availabilities?address_id=789&service_type_key=turnover_cleaning.two_and_a_half_hours" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Acceptance probability
curl "https://public-api.tidy.com/api/v2/job-acceptance-probabilities/preview?address_id=789&service_type_key=turnover_cleaning.two_and_a_half_hours&start_no_earlier_than[date]=2025-07-04&start_no_earlier_than[time]=11:00&end_no_later_than[date]=2025-07-04&end_no_later_than[time]=15:00" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Workflow 5: Property Setup with Full Details

Setting up a new listing with everything a cleaner needs to know:

```bash
tidy-request "Add my new Airbnb at 100 Lake Shore Dr, Unit 4B, Chicago IL 60611. Doorman building, tell front desk you're here for cleaning in 4B. Guest parking available in lower level, free. Name it 'Lake Shore Condo'."
```

REST API with full details:

```bash
curl -X POST https://public-api.tidy.com/api/v2/addresses \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "100 Lake Shore Dr",
    "unit": "4B",
    "city": "Chicago",
    "postal_code": "60611",
    "address_name": "Lake Shore Condo",
    "notes": {
      "access": "Doorman building — tell front desk you are here for cleaning in 4B",
      "closing": "Lock deadbolt, leave key with doorman"
    },
    "parking": {
      "paid_parking": false,
      "parking_spot": "guest",
      "parking_notes": "Guest parking in lower level"
    }
  }'
```
