# TripIt Email Template Format Reference

TripIt parses structured emails sent to `plans@tripit.com`. This document covers the complete field reference for the "TripIt Approved" format, matching TripIt's official vendor templates.

## General Rules

1. **Header line**: Email body must start with `TripIt Approved` (exactly)
2. **Date format**: Use one consistent format per email — ISO 8601 (`2026-03-15`), US (`March 15, 2026`), or EU (`15 March, 2026`)
3. **Time format**: `HH:MM` (24h), `H:MM AM/PM`, or `H AM/PM` — one format per email
4. **Field format**: `Label : Value` (colon required after label, spaces around colon are fine)
5. **Case**: First letters are case-insensitive
6. **Multi-line values**: End with `***` on a new line
7. **Max items**: Up to 60 travel objects per email
8. **Sections**: Each object type is wrapped in start/end tags (e.g., `Flight Information` / `End of Flight Information`)
9. **Empty fields**: Omit entirely (don't include blank values)
10. **Dashes and spaces**: Interchangeable in labels

## Header Block

Present at the top of every email, before any object sections.

| Field | JSON Key | Required | Notes |
|-------|----------|----------|-------|
| Booking confirmation # | `confirmation` | No | Booking reference / PNR |
| Booking date | `booking_date` | No | Auto-set to today if omitted |
| Booking site name | `booking_site_name` | No | Auto-derived from airline/hotel/etc. |
| Booking site phone | `booking_site_phone` | No | |
| Booking site web-page | `booking_site_url` | No | |

## Flight Information

Section tags: `Flight Information` / `End of Flight Information`

Uses nested `Traveler #N` and `Flight segment #N` sub-blocks.

### Top-level flight fields

| Field | JSON Key | Required | Notes |
|-------|----------|----------|-------|
| Airline name | `airline` | **Yes** | Operating carrier |
| Airline confirmation # | `airline_confirmation` | No | Falls back to `confirmation` |

### Traveler fields (inside `Traveler #1` block)

| Field | JSON Key | Required | Notes |
|-------|----------|----------|-------|
| First name | `first_name` | No | Auto-split from `passenger` if not set |
| Middle name | `middle_name` | No | |
| Last name | `last_name` | No | Auto-split from `passenger` if not set |
| Ticket # | `ticket_number` | No | |
| Frequent flyer # | `frequent_flyer` | No | |
| Program name | `program_name` | No | |

**Shortcut**: Provide `passenger` (e.g., `"Jane Smith"`) and first/last are auto-split.

### Segment fields (inside `Flight segment #1` block)

| Field | JSON Key | Required | Notes |
|-------|----------|----------|-------|
| Airline | `airline` | No | Inherited from top-level |
| Flight # | `flight_number` | **Yes** | |
| Codeshare airline | `codeshare_airline` | No | |
| Departure date | `departure_date` | **Yes** | |
| Departure time | `departure_time` | **Yes** | |
| Arrival date | `arrival_date` | **Yes** | |
| Arrival time | `arrival_time` | **Yes** | |
| Departure airport | `departure_airport` | **Yes** | IATA code |
| Departure terminal | `departure_terminal` | No | |
| Arrival airport | `arrival_airport` | **Yes** | IATA code |
| Arrival terminal | `arrival_terminal` | No | |
| Class | `class` | No | Economy, Business, First |
| Aircraft | `aircraft` | No | |
| Meal | `meal` | No | |
| Distance | `distance` | No | |
| Duration | `duration` | No | |
| Seat | `seat` | No | |

### Flight footer fields

| Field | JSON Key | Notes |
|-------|----------|-------|
| Booking rate | `booking_rate` | |
| Total cost | `total_cost` | |
| Notes | `notes` | Use `***` if multi-line |
| Restrictions | `restrictions` | Use `***` if multi-line |

### Multi-segment flights

For connections, provide a `segments` array:
```json
{
  "airline": "United Airlines",
  "passenger": "Jane Smith",
  "confirmation": "UA789",
  "segments": [
    {"flight_number": "1234", "departure_airport": "SFO", "departure_date": "2025-06-15", "departure_time": "08:30", "arrival_airport": "ORD", "arrival_date": "2025-06-15", "arrival_time": "14:30"},
    {"flight_number": "5678", "departure_airport": "ORD", "departure_date": "2025-06-15", "departure_time": "16:00", "arrival_airport": "JFK", "arrival_date": "2025-06-15", "arrival_time": "19:15"}
  ]
}
```

### Flight Example

```
Flight Information
Airline name : United Airlines
Airline confirmation # : UA1234X
Traveler #1
First name : Jane
Last name : Smith
Flight segment #1
Airline : United Airlines
Flight # : 1234
Departure date : 2025-06-15
Departure time : 08:30
Arrival date : 2025-06-15
Arrival time : 17:05
Departure airport : SFO
Arrival airport : JFK
Class : Economy
End of Flight Information
```

## Hotel Information

Section tags: `Hotel Information` / `End of Hotel Information`

| Field | JSON Key | Required | Notes |
|-------|----------|----------|-------|
| Hotel name | `hotel_name` | **Yes** | |
| Hotel address | `hotel_address` | No | Single field; or auto-built from `street_address`, `city`, `state`, `country` |
| Hotel phone | `phone` or `hotel_phone` | No | |
| Hotel confirmation # | `hotel_confirmation` | No | Falls back to `confirmation` |
| Guest name | `guest_name` | No | Also accepts `passenger` or `first_name`/`last_name` |
| Check-in date | `checkin_date` | **Yes** | |
| Check-out date | `checkout_date` | **Yes** | |
| Check-in time | `checkin_time` | No | |
| Check-out time | `checkout_time` | No | |
| Room type | `room_type` | No | e.g., `1 King Size Bed` |
| Room description | `room_description` | No | |
| Number of nights | `number_of_nights` | No | |
| Number of guests | `number_of_guests` | No | |
| Number of rooms | `number_of_rooms` | No | |
| Frequent guest # | `frequent_guest` | No | |
| Cancellation remarks | `cancellation_remarks` | No | Also accepts `cancellation_policy`. Use `***` if multi-line |
| Booking rate | `rate` or `booking_rate` | No | |
| Total cost | `total_cost` | No | |
| Notes | `notes` | No | Use `***` if multi-line |
| Restrictions | `restrictions` | No | Use `***` if multi-line |

### Hotel Example

```
Hotel Information
Hotel name : Hotel & Spa Napa Valley
Hotel address : 123 Vineyard Lane, Napa, CA, US
Hotel confirmation # : NV8842
Guest name : Jane Smith
Check-in date : 2025-06-15
Check-in time : 3 PM
Check-out date : 2025-06-18
Check-out time : 11 AM
Room type : King Suite
Number of guests : 2
Number of rooms : 1
Booking rate : $189/night
Total cost : $567
End of Hotel Information
```

## Car Information

Section tags: `Car Information` / `End of Car Information`

| Field | JSON Key | Required | Notes |
|-------|----------|----------|-------|
| Car rental company | `rental_company` | **Yes** | |
| Car rental confirmation # | `car_confirmation` | No | Falls back to `confirmation` |
| Car rental phone | `rental_phone` | No | |
| Driver | `driver` | No | Also accepts `passenger` |
| Frequent renter # | `frequent_renter` | No | |
| Car type | `car_type` | No | e.g., `Compact SUV` |
| Car description | `car_description` | No | |
| Pick-up date | `pickup_date` | **Yes** | |
| Pick-up time | `pickup_time` | No | |
| Drop-off date | `dropoff_date` | **Yes** | |
| Drop-off time | `dropoff_time` | No | |
| Pick-up location name | `pickup_location` | No | |
| Pick-up location address | `pickup_address` | No | |
| Pick-up location phone | `pickup_phone` | No | |
| Pick-up location hours | `pickup_hours` | No | e.g., `24 Hours` |
| Pick-up instructions | `pickup_instructions` | No | |
| Drop-off location name | `dropoff_location` | No | |
| Drop-off location address | `dropoff_address` | No | |
| Drop-off location phone | `dropoff_phone` | No | |
| Drop-off location hours | `dropoff_hours` | No | |
| Booking rate | `rate` or `booking_rate` | No | |
| Mileage charges | `mileage_charges` | No | e.g., `Unlimited` |
| Total cost | `total_cost` | No | |
| Notes | `notes` | No | Use `***` if multi-line |
| Restrictions | `restrictions` | No | Use `***` if multi-line |

### Car Example

```
Car Information
Car rental company : Hertz
Car rental confirmation # : H123456
Driver : Jane Smith
Car type : Compact SUV
Pick-up date : 2025-07-01
Pick-up time : 10:00
Drop-off date : 2025-07-05
Drop-off time : 10:00
Pick-up location name : CUN Airport
Pick-up location address : Cancun International Airport
Mileage charges : Unlimited
Total cost : $350
End of Car Information
```

## Rail Information

Section tags: `Rail Information` / `End of Rail Information`

Uses nested `Traveler #N` and `Rail segment #N` sub-blocks.

### Top-level rail fields

| Field | JSON Key | Notes |
|-------|----------|-------|
| Booking rate | `booking_rate` | |
| Total cost | `total_cost` | |
| Notes | `notes` | Use `***` if multi-line |
| Restrictions | `restrictions` | Use `***` if multi-line |

### Traveler fields (inside `Traveler #1` block)

| Field | JSON Key | Notes |
|-------|----------|-------|
| First name | `first_name` | Auto-split from `passenger` |
| Middle name | `middle_name` | |
| Last name | `last_name` | |
| Frequent traveler # | `frequent_traveler` | |
| Program name | `program_name` | |

### Segment fields (inside `Rail segment #1` block)

| Field | JSON Key | Required | Notes |
|-------|----------|----------|-------|
| Departure date | `departure_date` | **Yes** | |
| Departure time | `departure_time` | **Yes** | |
| Arrival date | `arrival_date` | **Yes** | |
| Arrival time | `arrival_time` | **Yes** | |
| Departure from | `departure_station` | No | City or station name |
| Departure station address | `departure_station_address` | No | |
| Arrival at | `arrival_station` | No | City or station name |
| Arrival station address | `arrival_station_address` | No | |
| Confirmation # | `confirmation` | No | |
| Carrier | `carrier` | **Yes** | |
| Train type | `train_type` | No | |
| Train # | `train_number` | No | |
| Class | `class` | No | |
| Coach # | `coach` | No | |
| Seats | `seat` or `seats` | No | |

### Rail Example

```
Rail Information
Traveler #1
First name : Jane
Last name : Smith
Rail segment #1
Departure date : 2025-07-10
Departure time : 06:00
Arrival date : 2025-07-10
Arrival time : 09:30
Departure from : Washington Union Station
Arrival at : New York Penn Station
Carrier : Amtrak
Train # : 2150
Class : Business
End of Rail Information
```

## Activity Information

Section tags: `Activity Information` / `End of Activity Information`

| Field | JSON Key | Required | Notes |
|-------|----------|----------|-------|
| Activity name | `activity_name` | **Yes** | |
| Location | `location` | No | Venue or place name |
| Address | `address` | No | Auto-built from `street_address`, `city`, `state`, `country` |
| Start date | `start_date` | **Yes** | |
| Start time | `start_time` | No | |
| End date | `end_date` | No | |
| End time | `end_time` | No | |
| Participants | `participants` | No | Comma-separated names |
| Confirmation # | `confirmation` | No | |
| Booking rate | `rate` or `booking_rate` | No | |
| Total cost | `total_cost` | No | |
| Notes | `notes` | No | Use `***` if multi-line |
| Restrictions | `restrictions` | No | Use `***` if multi-line |

### Activity Example

```
Activity Information
Activity name : Wine Tasting Tour
Location : Sonoma Valley Vineyards
Address : Sonoma, CA, US
Start date : 2025-06-16
Start time : 10:00
End date : 2025-06-16
End time : 14:00
Participants : Jane Smith, John Smith
Notes : Includes lunch and 6 tastings.
Reserve the private room.
***
End of Activity Information
```

## Multi-Item Emails

Multiple objects can be included in a single email. Use one header block followed by multiple sections:

```
TripIt Approved
Booking confirmation # : ABC123
Booking date : 2025-06-01
Booking site name : Expedia

Flight Information
...
End of Flight Information

Hotel Information
...
End of Hotel Information
```

**Rules for multi-item emails:**
- One header block at the top (shared across all items)
- Up to 60 object sections per email
- Each section independently tagged with start/end markers
- Use consistent date format across all sections
