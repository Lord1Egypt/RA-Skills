# Zim Agent-to-Agent Booking Model

## Purpose

This reference defines the intended product behavior for Zim as an agent travel middleware layer.
Use it when shaping responses, documentation, or future implementation work.

## Product definition

Zim sits between:
- a conversational agent or assistant
- travel providers / supply sources
- traveler preferences
- company travel policy
- approval and booking workflow

Its role is to turn a natural-language travel request into a structured, policy-aware, booking-ready itinerary.

## Current state vs future state

### Current beta
- Parses travel intent
- Searches flight / hotel / car sources
- Returns booking-ready options and live booking paths
- Can frame output as itinerary assembly
- Can apply policy / preference logic conversationally

### Future full product
- Executes bookings end-to-end
- Handles secure payment / approval routing
- Stores traveler preference memory
- Supports cancellations, rebooking, and post-booking changes
- Operates as a true agent-to-agent booking layer

## Structured travel object

Recommended fields:

```json
{
  "traveler": {
    "name": "Robin Zieme",
    "mode": "business",
    "preferences": {
      "seat": "window",
      "airlines": ["Emirates", "Singapore Airlines"],
      "noRedeye": true,
      "hotelStyle": "boutique",
      "carClass": "suv"
    }
  },
  "trip": {
    "origin": "LHR",
    "destination": "DXB",
    "departureDate": "2026-04-15",
    "returnDate": "2026-04-19",
    "purpose": "board meeting",
    "meetingLocation": "DIFC"
  },
  "policy": {
    "maxHotelNight": 300,
    "maxFlight": 2000,
    "approvalThreshold": 5000,
    "businessLongHaulClass": "business"
  },
  "constraints": {
    "directOnly": true,
    "refundablePreferred": true
  }
}
```

## Output contract

When Zim responds, prefer this structure:

1. Trip summary
2. Recommended itinerary
3. Policy / preference fit explanation
4. Booking state
5. Next action

Example booking state values:
- `booking-ready`
- `approval-needed`
- `missing-traveler-input`
- `booked` (only when true execution exists)

## Truthfulness rule

Do not say a trip is booked unless booking execution actually happened.
If execution is not connected, say:
- `booking-ready options assembled`
- `awaiting approval`
- `ready for checkout`

## Best positioning line

Zim is the travel middleware layer that lets one agent hand structured travel intent to another layer that can search, compare, assemble, and eventually execute policy-aware travel.
