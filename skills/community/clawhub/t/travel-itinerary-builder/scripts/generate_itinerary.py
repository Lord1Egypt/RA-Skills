#!/usr/bin/env python3
"""
Travel Itinerary Generator - Core Script

Generates comprehensive travel itineraries by combining:
- User input (destinations, dates, interests)
- Weather forecasts (from weather skill)
- Points of interest (from goplaces skill)
- Existing bookings (from Gmail via gmail_parser.py)
- Budget estimates

Outputs: HTML, Markdown, or JSON
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Generate travel itinerary")
    parser.add_argument("--destination", required=True, help="Comma-separated destinations")
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--bookings", help="Path to bookings JSON file")
    parser.add_argument("--weather", help="Path to weather JSON file")
    parser.add_argument("--places", help="Path to places JSON file")
    parser.add_argument("--budget", type=float, help="Total budget amount")
    parser.add_argument("--currency", default="SGD", help="Currency code (default: SGD)")
    parser.add_argument("--language", default="en", choices=["zh", "en", "ja", "ko"], help="Output language")
    parser.add_argument("--interests", help="Comma-separated interests (history,nature,food,shopping)")
    parser.add_argument("--output", required=True, help="Output file (.html, .md, or .json)")
    return parser.parse_args()


def load_json(path):
    """Load JSON file if exists"""
    if not path:
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {path} not found, skipping", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse {path}: {e}", file=sys.stderr)
        return None


def parse_date(date_str):
    """Parse YYYY-MM-DD to datetime"""
    return datetime.strptime(date_str, "%Y-%m-%d")


def generate_date_range(start_date, end_date):
    """Generate list of dates between start and end"""
    start = parse_date(start_date)
    end = parse_date(end_date)
    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def build_itinerary_structure(args, bookings, weather, places):
    """Build core itinerary data structure"""
    destinations = [d.strip() for d in args.destination.split(',')]
    dates = generate_date_range(args.start_date, args.end_date)
    interests = [i.strip() for i in (args.interests or "").split(',')] if args.interests else []
    
    itinerary = {
        "title": f"🌍 Travel Itinerary: {', '.join(destinations)}",
        "destinations": destinations,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "duration_days": len(dates),
        "budget": {
            "total": args.budget,
            "currency": args.currency
        },
        "language": args.language,
        "interests": interests,
        "days": []
    }
    
    # Group places by city
    places_by_city = {}
    if places and "places" in places:
        for place in places["places"]:
            city = place.get("city", "Unknown")
            if city not in places_by_city:
                places_by_city[city] = []
            places_by_city[city].append(place)
    
    # Build day-by-day schedule
    for i, date in enumerate(dates):
        day_num = i + 1
        date_str = date.strftime("%Y-%m-%d")
        weekday = date.strftime("%A")
        
        # Get weather for this date
        day_weather = get_weather_for_date(weather, date_str)
        
        # Get bookings for this date
        day_bookings = get_bookings_for_date(bookings, date_str)
        
        # Suggest activities based on destinations and interests
        suggested_activities = []
        for city in destinations:
            city_places = places_by_city.get(city, [])
            if city_places and day_num <= len(city_places):
                place = city_places[min(day_num-1, len(city_places)-1)]
                suggested_activities.append({
                    "time": "10:00",
                    "activity": f"Visit {place['name']} ({place['name_local']})",
                    "type": place.get("type", "attraction"),
                    "rating": place.get("rating", 0),
                    "address": place.get("address", "")
                })
        
        day_data = {
            "day_number": day_num,
            "date": date_str,
            "weekday": weekday,
            "activities": suggested_activities,
            "weather": day_weather,
            "bookings": day_bookings,
            "notes": []
        }
        
        # Add weather-based notes
        if day_weather and "rain" in day_weather.get("condition", "").lower():
            day_data["notes"].append("⚠️ Rain expected - bring umbrella")
        
        itinerary["days"].append(day_data)
    
    # Add summary statistics
    if bookings:
        itinerary["bookings_summary"] = summarize_bookings(bookings)
    
    if places and "places" in places:
        itinerary["places_summary"] = {
            "total": len(places["places"]),
            "by_city": {city: len(p) for city, p in places_by_city.items()}
        }
    
    return itinerary


def get_weather_for_date(weather_data, date_str):
    """Extract weather forecast for specific date"""
    if not weather_data or "forecasts" not in weather_data:
        return None
    
    for forecast in weather_data["forecasts"]:
        if forecast.get("date") == date_str:
            return {
                "temperature": forecast.get("temperature"),
                "condition": forecast.get("condition"),
                "precipitation": forecast.get("precipitation"),
                "wind": forecast.get("wind")
            }
    return None


def get_bookings_for_date(bookings_data, date_str):
    """Extract bookings (flights, hotels, etc.) for specific date"""
    if not bookings_data:
        return []
    
    date_bookings = []
    
    # Check flights
    for flight in bookings_data.get("flights", []):
        if flight.get("departure_date") == date_str or flight.get("arrival_date") == date_str:
            date_bookings.append({
                "type": "flight",
                "data": flight
            })
    
    # Check hotels
    for hotel in bookings_data.get("hotels", []):
        checkin = hotel.get("checkin_date")
        checkout = hotel.get("checkout_date")
        if checkin == date_str or checkout == date_str:
            date_bookings.append({
                "type": "hotel",
                "data": hotel
            })
    
    # Check car rentals
    for rental in bookings_data.get("car_rentals", []):
        pickup = rental.get("pickup_date")
        dropoff = rental.get("dropoff_date")
        if pickup == date_str or dropoff == date_str:
            date_bookings.append({
                "type": "car_rental",
                "data": rental
            })
    
    # Check activities/tickets
    for activity in bookings_data.get("activities", []):
        if activity.get("date") == date_str:
            date_bookings.append({
                "type": "activity",
                "data": activity
            })
    
    return date_bookings


def summarize_bookings(bookings_data):
    """Generate summary statistics from bookings"""
    summary = {
        "flights": len(bookings_data.get("flights", [])),
        "hotels": len(bookings_data.get("hotels", [])),
        "car_rentals": len(bookings_data.get("car_rentals", [])),
        "activities": len(bookings_data.get("activities", [])),
        "total_cost": 0.0
    }
    
    # Sum up costs if available
    for category in ["flights", "hotels", "car_rentals", "activities"]:
        for item in bookings_data.get(category, []):
            if "price" in item:
                summary["total_cost"] += float(item["price"])
    
    return summary


def generate_markdown_output(itinerary):
    """Convert itinerary to Markdown format"""
    lines = []
    lines.append(f"# {itinerary['title']}")
    lines.append("")
    lines.append(f"**Dates**: {itinerary['start_date']} to {itinerary['end_date']} ({itinerary['duration_days']} days)")
    lines.append(f"**Destinations**: {', '.join(itinerary['destinations'])}")
    if itinerary['budget']['total']:
        lines.append(f"**Budget**: {itinerary['budget']['currency']} {itinerary['budget']['total']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for day in itinerary['days']:
        lines.append(f"## Day {day['day_number']} - {day['date']} ({day['weekday']})")
        lines.append("")
        
        # Weather
        if day['weather']:
            w = day['weather']
            lines.append(f"🌤️ **Weather**: {w.get('condition', 'N/A')} | {w.get('temperature', 'N/A')}")
            lines.append("")
        
        # Bookings
        if day['bookings']:
            lines.append("### Bookings")
            for booking in day['bookings']:
                if booking['type'] == 'flight':
                    f = booking['data']
                    lines.append(f"✈️ **Flight**: {f.get('airline', 'N/A')} {f.get('flight_number', 'N/A')}")
                    lines.append(f"   - {f.get('departure_time', 'N/A')} → {f.get('arrival_time', 'N/A')}")
                elif booking['type'] == 'hotel':
                    h = booking['data']
                    lines.append(f"🏨 **Hotel**: {h.get('name', 'N/A')}")
                    lines.append(f"   - Check-in: {h.get('checkin_date', 'N/A')}")
            lines.append("")
        
        # Activities placeholder
        if day['activities']:
            lines.append("### Activities")
            for activity in day['activities']:
                lines.append(f"- {activity}")
            lines.append("")
        
        # Notes
        if day['notes']:
            lines.append("### Notes")
            for note in day['notes']:
                lines.append(f"- {note}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def generate_html_output(itinerary, template_path):
    """Convert itinerary to HTML using template"""
    from datetime import datetime
    
    # Read template
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        # Fallback to basic template
        template = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{{title}}</title></head>
<body><h1>{{title}}</h1>{{content}}</body></html>"""
    
    # Build content HTML
    content_parts = []
    
    for day in itinerary['days']:
        content_parts.append(f'<div class="day-card">')
        content_parts.append(f'<div class="day-header">Day {day["day_number"]} - {day["date"]} ({day["weekday"]})</div>')
        content_parts.append(f'<div class="day-body">')
        
        # Weather
        if day['weather']:
            w = day['weather']
            content_parts.append(f'<div class="weather">🌤️ {w.get("condition", "N/A")} | {w.get("temperature", "N/A")}</div>')
        
        # Bookings
        if day['bookings']:
            for booking in day['bookings']:
                if booking['type'] == 'flight':
                    f = booking['data']
                    content_parts.append(f'<div class="booking">✈️ <strong>Flight:</strong> {f.get("airline", "N/A")} {f.get("flight_number", "N/A")}<br>{f.get("departure_time", "N/A")} → {f.get("arrival_time", "N/A")}</div>')
                elif booking['type'] == 'hotel':
                    h = booking['data']
                    content_parts.append(f'<div class="booking">🏨 <strong>Hotel:</strong> {h.get("name", "N/A")}<br>Check-in: {h.get("checkin_date", "N/A")}</div>')
        
        # Activities placeholder
        if day['activities']:
            content_parts.append('<ul class="timeline">')
            for activity in day['activities']:
                content_parts.append(f'<li>{activity}</li>')
            content_parts.append('</ul>')
        else:
            content_parts.append('<ul class="timeline"><li>Activities to be added</li></ul>')
        
        content_parts.append('</div></div>')
    
    content_html = '\n'.join(content_parts)
    
    # Replace template placeholders
    html = template.replace('{{title}}', itinerary['title'])
    html = html.replace('{{language}}', itinerary['language'])
    html = html.replace('{{subtitle}}', ', '.join(itinerary['destinations']))
    html = html.replace('{{dates}}', f"{itinerary['start_date']} to {itinerary['end_date']} ({itinerary['duration_days']} days)")
    html = html.replace('{{content}}', content_html)
    html = html.replace('{{generated_date}}', datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    return html


def main():
    args = parse_args()
    
    # Load external data
    bookings = load_json(args.bookings)
    weather = load_json(args.weather)
    places = load_json(args.places)
    
    # Build itinerary structure
    itinerary = build_itinerary_structure(args, bookings, weather, places)
    
    # Determine output format
    output_path = Path(args.output)
    output_ext = output_path.suffix.lower()
    
    if output_ext == ".json":
        # JSON output
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(itinerary, f, indent=2, ensure_ascii=False)
        print(f"✅ Generated JSON itinerary: {output_path}")
    
    elif output_ext == ".md":
        # Markdown output
        markdown = generate_markdown_output(itinerary)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"✅ Generated Markdown itinerary: {output_path}")
    
    elif output_ext == ".html":
        # HTML output
        template_path = Path(__file__).parent.parent / "assets" / "itinerary_template.html"
        html = generate_html_output(itinerary, template_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Generated HTML itinerary: {output_path}")
    
    else:
        print(f"Error: Unsupported output format: {output_ext}", file=sys.stderr)
        print("Supported formats: .json, .md, .html", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
