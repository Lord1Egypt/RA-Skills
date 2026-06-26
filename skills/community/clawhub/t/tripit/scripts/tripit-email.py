#!/usr/bin/env python3
"""Generate TripIt-formatted confirmation emails.

TripIt parses structured "TripIt Approved" emails sent to plans@tripit.com.
This script generates the correctly formatted email body matching TripIt's
official vendor template format.

Usage:
    echo '{"airline":"Volaris",...}' | python3 tripit-email.py flight
    python3 tripit-email.py hotel --json '{"hotel_name":"Hotel Reforma",...}'

Output is plain text ready to send to plans@tripit.com.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def emit(label: str, value: str | None) -> str:
    """Emit a single 'Label : Value' line, or empty string if no value."""
    if value is None or value == "":
        return ""
    str_value = str(value)
    if "\n" in str_value:
        return f"{label} : {str_value}\n***"
    return f"{label} : {str_value}"


def emit_lines(pairs: list[tuple[str, str | None]]) -> str:
    """Emit multiple label/value pairs, skipping empty ones."""
    lines = [emit(label, value) for label, value in pairs]
    return "\n".join(line for line in lines if line)


def validate_date(value: str) -> bool:
    """Check that a date string is in ISO 8601 format (YYYY-MM-DD)."""
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_time(value: str) -> bool:
    """Check that a time string is in HH:MM or H:MM AM/PM format."""
    for fmt in ("%H:%M", "%I:%M %p", "%I %p", "%I:%M%p", "%I%p"):
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False


def require(data: dict, keys: list[str], context: str) -> list[str]:
    """Return list of missing required keys."""
    return [k for k in keys if not data.get(k)]


def warn_dates(data: dict, keys: list[str]) -> list[str]:
    """Warn about date fields not in ISO 8601."""
    warnings = []
    for k in keys:
        v = data.get(k)
        if v and not validate_date(v):
            warnings.append(f"{k}: '{v}' is not ISO 8601 (YYYY-MM-DD). "
                            "TripIt also accepts 'March 15, 2026' or '15 March, 2026'.")
    return warnings


def split_name(name: str) -> tuple[str, str, str]:
    """Split a full name into (first, middle, last)."""
    parts = name.strip().split()
    if len(parts) == 1:
        return parts[0], "", ""
    elif len(parts) == 2:
        return parts[0], "", parts[1]
    else:
        return parts[0], " ".join(parts[1:-1]), parts[-1]


# ---------------------------------------------------------------------------
# Header (shared by all types)
# ---------------------------------------------------------------------------

def build_header(data: dict) -> str:
    """Build the TripIt Approved header block using official field labels."""
    lines = ["TripIt Approved"]

    # Derive booking site name from type-specific fields if not explicit
    site_name = data.get("booking_site_name") or data.get("airline") or \
                data.get("hotel_name") or data.get("rental_company") or \
                data.get("carrier") or ""

    header = emit_lines([
        ("Booking confirmation #", data.get("confirmation")),
        ("Booking date", data.get("booking_date", datetime.now().strftime("%Y-%m-%d"))),
        ("Booking site name", site_name or None),
        ("Booking site phone", data.get("booking_site_phone")),
        ("Booking site web-page", data.get("booking_site_url")),
    ])
    if header:
        lines.append(header)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Flight
# ---------------------------------------------------------------------------

FLIGHT_REQUIRED = ["airline", "flight_number", "departure_airport",
                   "departure_date", "departure_time", "arrival_airport",
                   "arrival_date", "arrival_time"]
FLIGHT_DATE_KEYS = ["departure_date", "arrival_date"]


def build_flight(data: dict) -> str:
    """Build Flight Information section matching official TripIt template."""
    lines = ["Flight Information"]

    # Airline header
    lines.append(emit("Airline name", data.get("airline")))
    conf = data.get("airline_confirmation") or data.get("confirmation")
    if conf:
        lines.append(emit("Airline confirmation #", conf))

    # Traveler block — accept "passenger" (full name) or first/last
    passenger = data.get("passenger", "")
    first = data.get("first_name", "")
    last = data.get("last_name", "")
    if passenger and not first:
        first, middle, last = split_name(passenger)
    else:
        middle = data.get("middle_name", "")

    if first or last:
        lines.append("Traveler #1")
        traveler = emit_lines([
            ("First name", first),
            ("Middle name", middle or None),
            ("Last name", last),
            ("Ticket #", data.get("ticket_number")),
            ("Frequent flyer #", data.get("frequent_flyer")),
            ("Program name", data.get("program_name")),
        ])
        if traveler:
            lines.append(traveler)

    # Flight segment(s) — single segment from flat fields, or "segments" array
    segments = data.get("segments", [])
    if not segments:
        # Build single segment from flat fields
        segments = [data]

    for i, seg in enumerate(segments):
        lines.append(f"Flight segment #{i + 1}")
        seg_text = emit_lines([
            ("Airline", seg.get("airline", data.get("airline"))),
            ("Flight #", seg.get("flight_number")),
            ("Codeshare airline", seg.get("codeshare_airline")),
            ("Departure date", seg.get("departure_date")),
            ("Departure time", seg.get("departure_time")),
            ("Arrival date", seg.get("arrival_date")),
            ("Arrival time", seg.get("arrival_time")),
            ("Departure airport", seg.get("departure_airport")),
            ("Departure terminal", seg.get("departure_terminal")),
            ("Arrival airport", seg.get("arrival_airport")),
            ("Arrival terminal", seg.get("arrival_terminal")),
            ("Class", seg.get("class")),
            ("Aircraft", seg.get("aircraft")),
            ("Meal", seg.get("meal")),
            ("Distance", seg.get("distance")),
            ("Duration", seg.get("duration")),
            ("Seat", seg.get("seat")),
        ])
        if seg_text:
            lines.append(seg_text)

    # Footer fields
    footer = emit_lines([
        ("Booking rate", data.get("booking_rate")),
        ("Total cost", data.get("total_cost")),
        ("Notes", data.get("notes")),
        ("Restrictions", data.get("restrictions")),
    ])
    if footer:
        lines.append(footer)

    lines.append("End of Flight Information")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Hotel
# ---------------------------------------------------------------------------

HOTEL_REQUIRED = ["hotel_name", "checkin_date", "checkout_date"]
HOTEL_DATE_KEYS = ["checkin_date", "checkout_date"]


def build_hotel(data: dict) -> str:
    """Build Hotel Information section matching official TripIt template."""
    # Build a combined address if separate fields provided
    address = data.get("hotel_address") or data.get("address")
    if not address:
        parts = [data.get("street_address", ""), data.get("city", ""),
                 data.get("state", ""), data.get("country", "")]
        combined = ", ".join(p for p in parts if p)
        if combined:
            address = combined

    # Guest name — accept "guest_name" or "passenger" or first/last
    guest = data.get("guest_name") or data.get("passenger")
    if not guest and data.get("first_name"):
        guest = f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()

    lines = ["Hotel Information"]
    body = emit_lines([
        ("Hotel name", data.get("hotel_name")),
        ("Hotel address", address),
        ("Hotel phone", data.get("phone") or data.get("hotel_phone")),
        ("Hotel confirmation #", data.get("hotel_confirmation") or data.get("confirmation")),
        ("Guest name", guest),
        ("Check-in date", data.get("checkin_date")),
        ("Check-out date", data.get("checkout_date")),
        ("Check-in time", data.get("checkin_time")),
        ("Check-out time", data.get("checkout_time")),
        ("Room type", data.get("room_type")),
        ("Room description", data.get("room_description")),
        ("Number of nights", data.get("number_of_nights")),
        ("Number of guests", data.get("number_of_guests")),
        ("Number of rooms", data.get("number_of_rooms")),
        ("Frequent guest #", data.get("frequent_guest")),
        ("Cancellation remarks", data.get("cancellation_remarks") or data.get("cancellation_policy")),
        ("Booking rate", data.get("rate") or data.get("booking_rate")),
        ("Total cost", data.get("total_cost")),
        ("Notes", data.get("notes")),
        ("Restrictions", data.get("restrictions")),
    ])
    if body:
        lines.append(body)
    lines.append("End of Hotel Information")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Car
# ---------------------------------------------------------------------------

CAR_REQUIRED = ["rental_company", "pickup_date", "dropoff_date"]
CAR_DATE_KEYS = ["pickup_date", "dropoff_date"]


def build_car(data: dict) -> str:
    """Build Car Information section matching official TripIt template."""
    lines = ["Car Information"]
    body = emit_lines([
        ("Car rental company", data.get("rental_company")),
        ("Car rental confirmation #", data.get("car_confirmation") or data.get("confirmation")),
        ("Car rental phone", data.get("rental_phone")),
        ("Driver", data.get("driver") or data.get("passenger")),
        ("Frequent renter #", data.get("frequent_renter")),
        ("Car type", data.get("car_type")),
        ("Car description", data.get("car_description")),
        ("Pick-up date", data.get("pickup_date")),
        ("Pick-up time", data.get("pickup_time")),
        ("Drop-off date", data.get("dropoff_date")),
        ("Drop-off time", data.get("dropoff_time")),
        ("Pick-up location name", data.get("pickup_location") or data.get("pickup_location_name")),
        ("Pick-up location address", data.get("pickup_address")),
        ("Pick-up location phone", data.get("pickup_phone")),
        ("Pick-up location hours", data.get("pickup_hours")),
        ("Pick-up instructions", data.get("pickup_instructions")),
        ("Drop-off location name", data.get("dropoff_location") or data.get("dropoff_location_name")),
        ("Drop-off location address", data.get("dropoff_address")),
        ("Drop-off location phone", data.get("dropoff_phone")),
        ("Drop-off location hours", data.get("dropoff_hours")),
        ("Booking rate", data.get("rate") or data.get("booking_rate")),
        ("Mileage charges", data.get("mileage_charges")),
        ("Total cost", data.get("total_cost")),
        ("Notes", data.get("notes")),
        ("Restrictions", data.get("restrictions")),
    ])
    if body:
        lines.append(body)
    lines.append("End of Car Information")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Rail
# ---------------------------------------------------------------------------

RAIL_REQUIRED = ["carrier", "departure_date", "departure_time",
                 "arrival_date", "arrival_time"]
RAIL_DATE_KEYS = ["departure_date", "arrival_date"]


def build_rail(data: dict) -> str:
    """Build Rail Information section matching official TripIt template."""
    lines = ["Rail Information"]

    # Top-level fields
    top = emit_lines([
        ("Booking rate", data.get("booking_rate")),
        ("Total cost", data.get("total_cost")),
        ("Notes", data.get("notes")),
        ("Restrictions", data.get("restrictions")),
    ])
    if top:
        lines.append(top)

    # Traveler block
    passenger = data.get("passenger", "")
    first = data.get("first_name", "")
    last = data.get("last_name", "")
    if passenger and not first:
        first, middle, last = split_name(passenger)
    else:
        middle = data.get("middle_name", "")

    if first or last:
        lines.append("Traveler #1")
        traveler = emit_lines([
            ("First name", first),
            ("Middle name", middle or None),
            ("Last name", last),
            ("Frequent traveler #", data.get("frequent_traveler")),
            ("Program name", data.get("program_name")),
        ])
        if traveler:
            lines.append(traveler)

    # Rail segment(s)
    segments = data.get("segments", [])
    if not segments:
        segments = [data]

    for i, seg in enumerate(segments):
        lines.append(f"Rail segment #{i + 1}")
        seg_text = emit_lines([
            ("Departure date", seg.get("departure_date")),
            ("Departure time", seg.get("departure_time")),
            ("Arrival date", seg.get("arrival_date")),
            ("Arrival time", seg.get("arrival_time")),
            ("Departure from", seg.get("departure_station") or seg.get("departure_from")),
            ("Departure station address", seg.get("departure_station_address")),
            ("Arrival at", seg.get("arrival_station") or seg.get("arrival_at")),
            ("Arrival station address", seg.get("arrival_station_address")),
            ("Confirmation #", seg.get("segment_confirmation") or data.get("confirmation")),
            ("Carrier", seg.get("carrier", data.get("carrier"))),
            ("Train type", seg.get("train_type")),
            ("Train #", seg.get("train_number")),
            ("Class", seg.get("class")),
            ("Coach #", seg.get("coach")),
            ("Seats", seg.get("seat") or seg.get("seats")),
        ])
        if seg_text:
            lines.append(seg_text)

    lines.append("End of Rail Information")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Activity (not in the sample doc but referenced in help article)
# ---------------------------------------------------------------------------

ACTIVITY_REQUIRED = ["activity_name", "start_date"]
ACTIVITY_DATE_KEYS = ["start_date", "end_date"]


def build_activity(data: dict) -> str:
    """Build Activity Information section."""
    # Build address from parts if no single address field
    address = data.get("address")
    if not address:
        parts = [data.get("street_address", ""), data.get("city", ""),
                 data.get("state", ""), data.get("country", "")]
        combined = ", ".join(p for p in parts if p)
        if combined:
            address = combined

    lines = ["Activity Information"]
    body = emit_lines([
        ("Activity name", data.get("activity_name")),
        ("Location", data.get("location")),
        ("Address", address),
        ("Start date", data.get("start_date")),
        ("Start time", data.get("start_time")),
        ("End date", data.get("end_date")),
        ("End time", data.get("end_time")),
        ("Participants", data.get("participants")),
        ("Confirmation #", data.get("confirmation")),
        ("Booking rate", data.get("rate") or data.get("booking_rate")),
        ("Total cost", data.get("total_cost")),
        ("Notes", data.get("notes")),
        ("Restrictions", data.get("restrictions")),
    ])
    if body:
        lines.append(body)
    lines.append("End of Activity Information")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Builders registry
# ---------------------------------------------------------------------------

BUILDERS = {
    "flight": (build_flight, FLIGHT_REQUIRED, FLIGHT_DATE_KEYS),
    "hotel": (build_hotel, HOTEL_REQUIRED, HOTEL_DATE_KEYS),
    "car": (build_car, CAR_REQUIRED, CAR_DATE_KEYS),
    "rail": (build_rail, RAIL_REQUIRED, RAIL_DATE_KEYS),
    "activity": (build_activity, ACTIVITY_REQUIRED, ACTIVITY_DATE_KEYS),
}


# ---------------------------------------------------------------------------
# Email assembly
# ---------------------------------------------------------------------------

def build_email(obj_type: str, data: dict) -> str:
    """Build a complete TripIt-formatted email for a single object."""
    builder, _, _ = BUILDERS[obj_type]
    return build_header(data) + "\n\n" + builder(data) + "\n"


def build_multi_email(items: list[dict]) -> str:
    """Build a multi-item email."""
    if not items:
        print("Error: 'items' array is empty.", file=sys.stderr)
        sys.exit(1)

    header_data = dict(items[0])
    sections = []
    for item in items:
        obj_type = item["type"]
        builder, _, _ = BUILDERS[obj_type]
        sections.append(builder(item))

    return build_header(header_data) + "\n\n" + "\n\n".join(sections) + "\n"


def generate_subject(obj_type: str, data: dict) -> str:
    """Generate a suitable email subject line."""
    if obj_type == "flight":
        dep = data.get("departure_airport", "")
        arr = data.get("arrival_airport", "")
        date = data.get("departure_date", "")
        airline = data.get("airline", "Flight")
        return f"{airline} {dep}-{arr} {date}".strip()
    elif obj_type == "hotel":
        name = data.get("hotel_name", "Hotel")
        checkin = data.get("checkin_date", "")
        return f"{name} reservation {checkin}".strip()
    elif obj_type == "activity":
        name = data.get("activity_name", "Activity")
        date = data.get("start_date", "")
        return f"{name} {date}".strip()
    elif obj_type == "car":
        company = data.get("rental_company", "Car rental")
        date = data.get("pickup_date", "")
        return f"{company} reservation {date}".strip()
    elif obj_type == "rail":
        carrier = data.get("carrier", "Train")
        dep = data.get("departure_station", data.get("departure_from", ""))
        arr = data.get("arrival_station", data.get("arrival_at", ""))
        date = data.get("departure_date", "")
        return f"{carrier} {dep}-{arr} {date}".strip()
    return "Travel confirmation"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def read_input(args) -> dict | list:
    """Read JSON from --json arg or stdin."""
    if args.json:
        raw = args.json
    else:
        raw = sys.stdin.read()

    if not raw.strip():
        print("Error: No JSON input provided. Use --json or pipe to stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def handle_single(args, obj_type: str):
    """Handle a single-object subcommand."""
    data = read_input(args)
    if isinstance(data, list):
        print("Error: Expected a JSON object, got an array. Use 'multi' for multiple items.",
              file=sys.stderr)
        sys.exit(1)

    _, required, date_keys = BUILDERS[obj_type]

    # Validate
    missing = require(data, required, obj_type)
    if missing:
        print(f"Error: Missing required fields: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    for w in warn_dates(data, date_keys):
        print(f"Warning: {w}", file=sys.stderr)

    body = build_email(obj_type, data)

    if args.subject:
        print(f"Subject: {generate_subject(obj_type, data)}")
        print("---")

    print(body)


def handle_multi(args):
    """Handle the multi subcommand."""
    data = read_input(args)

    if isinstance(data, dict):
        items = data.get("items", [])
    elif isinstance(data, list):
        items = data
    else:
        print("Error: Expected a JSON array or object with 'items' key.", file=sys.stderr)
        sys.exit(1)

    if not items:
        print("Error: No items provided.", file=sys.stderr)
        sys.exit(1)

    for i, item in enumerate(items):
        obj_type = item.get("type")
        if not obj_type or obj_type not in BUILDERS:
            valid = ", ".join(BUILDERS.keys())
            print(f"Error: Item {i} missing or invalid 'type'. Valid types: {valid}",
                  file=sys.stderr)
            sys.exit(1)

        _, required, date_keys = BUILDERS[obj_type]
        missing = require(item, required, obj_type)
        if missing:
            print(f"Error: Item {i} ({obj_type}) missing required fields: {', '.join(missing)}",
                  file=sys.stderr)
            sys.exit(1)

        for w in warn_dates(item, date_keys):
            print(f"Warning: Item {i}: {w}", file=sys.stderr)

    body = build_multi_email(items)

    if args.subject:
        print(f"Subject: {generate_subject('multi', items[0])}")
        print("---")

    print(body)


def main():
    parser = argparse.ArgumentParser(
        description="Generate TripIt-formatted confirmation emails.",
        epilog="Output is plain text suitable for sending to plans@tripit.com.",
    )
    parser.add_argument("--json", help="JSON input (alternative to stdin)")
    parser.add_argument("--subject", action="store_true",
                        help="Include a suggested email subject line")

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("flight", help="Generate a flight confirmation")
    subparsers.add_parser("hotel", help="Generate a hotel confirmation")
    subparsers.add_parser("activity", help="Generate an activity confirmation")
    subparsers.add_parser("car", help="Generate a car rental confirmation")
    subparsers.add_parser("rail", help="Generate a rail confirmation")
    subparsers.add_parser("multi", help="Generate a multi-item confirmation")

    args = parser.parse_args()

    if args.command == "multi":
        handle_multi(args)
    else:
        handle_single(args, args.command)


if __name__ == "__main__":
    main()
