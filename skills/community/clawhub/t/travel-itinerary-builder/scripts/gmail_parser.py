#!/usr/bin/env python3
"""
Gmail Booking Parser

Extracts travel bookings from Gmail using GOG skill:
- Flights (airline, flight number, times, PNR)
- Hotels (name, dates, booking number, price)
- Car rentals (company, car type, dates, price)
- Activities/tickets (concerts, museums, events)

Supports: Agoda, Booking.com, Singapore Airlines, ANA, Trip.com, Klook, KKday
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="Parse travel bookings from Gmail")
    parser.add_argument("--account", required=True, help="Gmail account email")
    parser.add_argument("--after", required=True, help="Start date for email search (YYYY-MM-DD)")
    parser.add_argument("--keywords", default="flight,hotel,booking,confirmation,reservation",
                        help="Search keywords (comma-separated)")
    parser.add_argument("--output", required=True, help="Output JSON file")
    return parser.parse_args()


def search_gmail(account, after_date, keywords):
    """Search Gmail using GOG skill"""
    # Build search query
    keyword_list = [k.strip() for k in keywords.split(',')]
    query_parts = [f"subject:({' OR '.join(keyword_list)})"]
    query_parts.append(f"after:{after_date}")
    query = ' '.join(query_parts)
    
    print(f"🔍 Searching Gmail: {query}")
    
    # Call GOG gmail search
    try:
        cmd = [
            "gog", "gmail", "search",
            "--account", account,
            "--query", query,
            "--json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True,
                               env={**subprocess.os.environ, "GOG_KEYRING_PASSWORD": subprocess.os.environ.get("GOG_KEYRING_PASSWORD", "")})
        messages = json.loads(result.stdout)
        print(f"✅ Found {len(messages)} messages")
        return messages
    except subprocess.CalledProcessError as e:
        print(f"❌ Gmail search failed: {e.stderr}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse Gmail response: {e}", file=sys.stderr)
        return []


def extract_flights(messages):
    """Extract flight information from emails"""
    flights = []
    
    for msg in messages:
        subject = msg.get("subject", "").lower()
        body = msg.get("snippet", "")
        
        # Check if this is a flight confirmation
        if not any(keyword in subject for keyword in ["flight", "confirmation", "itinerary", "ticket"]):
            continue
        
        flight = {
            "email_id": msg.get("id"),
            "subject": msg.get("subject"),
            "from": msg.get("from"),
            "date": msg.get("date")
        }
        
        # Extract airline (common patterns)
        airlines = ["Singapore Airlines", "ANA", "Cathay Pacific", "JAL", "Korean Air", "Thai Airways"]
        for airline in airlines:
            if airline.lower() in subject or airline.lower() in body:
                flight["airline"] = airline
                break
        
        # Extract flight number (e.g., SQ634, NH991, CX715)
        flight_num_match = re.search(r'\b([A-Z]{2}\d{3,4})\b', subject + " " + body)
        if flight_num_match:
            flight["flight_number"] = flight_num_match.group(1)
        
        # Extract PNR (6-character alphanumeric code)
        pnr_match = re.search(r'\b([A-Z0-9]{6})\b', body)
        if pnr_match and pnr_match.group(1).isalnum() and not pnr_match.group(1).isdigit():
            flight["pnr"] = pnr_match.group(1)
        
        # Extract dates (YYYY-MM-DD or DD MMM YYYY)
        date_matches = re.findall(r'\b(\d{4}-\d{2}-\d{2})\b|\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4})\b', body, re.IGNORECASE)
        if date_matches:
            dates = [m[0] if m[0] else m[1] for m in date_matches]
            if len(dates) >= 1:
                flight["departure_date"] = dates[0]
            if len(dates) >= 2:
                flight["arrival_date"] = dates[1]
        
        # Extract times (HH:MM format)
        time_matches = re.findall(r'\b(\d{1,2}:\d{2})\b', body)
        if len(time_matches) >= 2:
            flight["departure_time"] = time_matches[0]
            flight["arrival_time"] = time_matches[1]
        
        flights.append(flight)
    
    return flights


def extract_hotels(messages):
    """Extract hotel booking information from emails"""
    hotels = []
    
    for msg in messages:
        subject = msg.get("subject", "").lower()
        body = msg.get("snippet", "")
        
        # Check if this is a hotel booking
        if not any(keyword in subject for keyword in ["booking", "reservation", "hotel", "accommodation"]):
            continue
        
        hotel = {
            "email_id": msg.get("id"),
            "subject": msg.get("subject"),
            "from": msg.get("from"),
            "date": msg.get("date")
        }
        
        # Extract booking platform
        if "agoda" in subject or "agoda" in body.lower():
            hotel["platform"] = "Agoda"
        elif "booking.com" in subject or "booking.com" in body.lower():
            hotel["platform"] = "Booking.com"
        elif "hotels.com" in subject or "hotels.com" in body.lower():
            hotel["platform"] = "Hotels.com"
        elif "marriott" in subject or "marriott" in body.lower():
            hotel["platform"] = "Marriott"
        
        # Extract booking number (Agoda: 10 digits, Booking.com: 9-10 digits)
        booking_num_match = re.search(r'#(\d{9,10})\b', body)
        if booking_num_match:
            hotel["booking_number"] = booking_num_match.group(1)
        
        # Extract hotel name (heuristic: capitalized words before "Hotel")
        hotel_name_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+Hotel)\b', body)
        if hotel_name_match:
            hotel["name"] = hotel_name_match.group(1)
        
        # Extract dates
        date_matches = re.findall(r'\b(\d{4}-\d{2}-\d{2})\b|\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4})\b', body, re.IGNORECASE)
        if date_matches:
            dates = [m[0] if m[0] else m[1] for m in date_matches]
            if len(dates) >= 1:
                hotel["checkin_date"] = dates[0]
            if len(dates) >= 2:
                hotel["checkout_date"] = dates[1]
        
        # Extract price (SGD, USD, JPY patterns)
        price_match = re.search(r'(?:SGD|USD|JPY|S\$|\$|¥)\s*([0-9,]+(?:\.\d{2})?)', body)
        if price_match:
            price_str = price_match.group(1).replace(',', '')
            hotel["price"] = float(price_str)
            hotel["currency"] = "SGD" if "SGD" in price_match.group(0) or "S$" in price_match.group(0) else "USD"
        
        hotels.append(hotel)
    
    return hotels


def extract_car_rentals(messages):
    """Extract car rental information from emails"""
    rentals = []
    
    for msg in messages:
        subject = msg.get("subject", "").lower()
        body = msg.get("snippet", "")
        
        # Check if this is a car rental
        if not any(keyword in subject for keyword in ["car", "rental", "vehicle", "trip.com"]):
            continue
        
        rental = {
            "email_id": msg.get("id"),
            "subject": msg.get("subject"),
            "from": msg.get("from"),
            "date": msg.get("date")
        }
        
        # Extract rental company
        companies = ["Trip.com", "Hertz", "Avis", "Budget", "Enterprise"]
        for company in companies:
            if company.lower() in subject or company.lower() in body.lower():
                rental["company"] = company
                break
        
        # Extract booking number
        booking_match = re.search(r'#(\d{10,16})\b', body)
        if booking_match:
            rental["booking_number"] = booking_match.group(1)
        
        # Extract dates
        date_matches = re.findall(r'\b(\d{4}-\d{2}-\d{2})\b', body)
        if len(date_matches) >= 2:
            rental["pickup_date"] = date_matches[0]
            rental["dropoff_date"] = date_matches[1]
        
        # Extract price
        price_match = re.search(r'(?:SGD|USD|S\$|\$)\s*([0-9,]+(?:\.\d{2})?)', body)
        if price_match:
            price_str = price_match.group(1).replace(',', '')
            rental["price"] = float(price_str)
        
        rentals.append(rental)
    
    return rentals


def extract_activities(messages):
    """Extract activity/ticket bookings (concerts, museums, etc.)"""
    activities = []
    
    for msg in messages:
        subject = msg.get("subject", "").lower()
        body = msg.get("snippet", "")
        
        # Check if this is a ticket/activity
        if not any(keyword in subject for keyword in ["ticket", "concert", "show", "event", "museum", "klook", "kkday"]):
            continue
        
        activity = {
            "email_id": msg.get("id"),
            "subject": msg.get("subject"),
            "from": msg.get("from"),
            "date": msg.get("date"),
            "type": "activity"
        }
        
        # Extract platform
        if "klook" in subject or "klook" in body.lower():
            activity["platform"] = "Klook"
        elif "kkday" in subject or "kkday" in body.lower():
            activity["platform"] = "KKday"
        
        # Extract event name from subject
        activity["name"] = msg.get("subject")
        
        # Extract date
        date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', body)
        if date_match:
            activity["date"] = date_match.group(1)
        
        # Extract time
        time_match = re.search(r'\b(\d{1,2}:\d{2})\b', body)
        if time_match:
            activity["time"] = time_match.group(1)
        
        activities.append(activity)
    
    return activities


def main():
    args = parse_args()
    
    # Search Gmail
    messages = search_gmail(args.account, args.after, args.keywords)
    
    if not messages:
        print("⚠️ No messages found", file=sys.stderr)
        bookings = {
            "flights": [],
            "hotels": [],
            "car_rentals": [],
            "activities": []
        }
    else:
        # Extract bookings by category
        print("📧 Parsing emails...")
        bookings = {
            "flights": extract_flights(messages),
            "hotels": extract_hotels(messages),
            "car_rentals": extract_car_rentals(messages),
            "activities": extract_activities(messages)
        }
        
        # Print summary
        print(f"\n✅ Extracted bookings:")
        print(f"   ✈️  Flights: {len(bookings['flights'])}")
        print(f"   🏨 Hotels: {len(bookings['hotels'])}")
        print(f"   🚗 Car rentals: {len(bookings['car_rentals'])}")
        print(f"   🎫 Activities: {len(bookings['activities'])}")
    
    # Save to JSON
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(bookings, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to: {args.output}")


if __name__ == "__main__":
    main()
