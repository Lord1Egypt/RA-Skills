#!/usr/bin/env python3
"""
Fetch Historical Weather Data

Script to fetch historical weather data for a given location.
Returns the last N days of actual weather observations (default 10, max 30).
"""

import argparse
import sys
import json

# Import from local utils module
from utils import get_lat_lon, load_history, process_data, DEFAULT_HISTORICAL_DAYS, MAX_HISTORICAL_DAYS


def fetch_historical_weather(lat: float, lon: float, display_name: str = None, days: int = None, kc: float = 1.0, output_format: str = 'csv'):
    """
    Fetch historical weather data for coordinates.

    Args:
        lat: Latitude
        lon: Longitude
        display_name: Optional label for logs (e.g. from geocoding)
        kc: Crop coefficient for evapotranspiration (default: 1.0)
        output_format: Output format - 'csv' or 'json' (default: 'csv')

    Returns:
        DataFrame with historical weather data or None if error
    """
    if display_name is None:
        display_name = f"({lat:.5f}, {lon:.5f})"
    print(f"Using coordinates: {display_name} (Lat: {lat:.5f}, Lon: {lon:.5f})", file=sys.stderr)

    # Load historical data
    print("Fetching historical weather data...", file=sys.stderr)
    data = load_history(lat, lon, days=days)
    
    if data is None or data.empty:
        print("Error: No historical data available for this location", file=sys.stderr)
        return None
    
    # Process data with crop coefficient
    data = process_data("historical", data, kc=kc)
    
    print(f"Retrieved {len(data)} days of historical data", file=sys.stderr)
    
    return data


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Fetch historical weather data for a location or coordinates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fetch_historical.py "Oslo, Norway"
  python fetch_historical.py --location "London, UK" --format json
  python fetch_historical.py --lat 59.91 --lon 10.75 --days 20 --kc 1.05
        """
    )

    parser.add_argument(
        "location",
        nargs="?",
        type=str,
        help="Location name (e.g., 'Oslo, Norway')"
    )
    parser.add_argument(
        "--location", "-l",
        type=str,
        dest="location_opt",
        metavar="LOCATION",
        help="Location name (alternative to positional)"
    )
    parser.add_argument(
        "--lat",
        type=float,
        help="Latitude (use with --lon instead of location)"
    )
    parser.add_argument(
        "--lon",
        type=float,
        help="Longitude (use with --lat instead of location)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_HISTORICAL_DAYS,
        metavar="N",
        help=f"Number of days of history (default: {DEFAULT_HISTORICAL_DAYS}, max: {MAX_HISTORICAL_DAYS})"
    )

    parser.add_argument(
        "--kc",
        type=float,
        default=1.0,
        help="Crop coefficient for evapotranspiration calculation (default: 1.0)"
    )
    
    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=['csv', 'json'],
        default='csv',
        help="Output format: 'csv' or 'json' (default: csv)"
    )
    
    args = parser.parse_args()

    # Resolve lat/lon: either from --lat/--lon or by looking up location
    lat, lon, display_name = None, None, None
    if args.lat is not None or args.lon is not None:
        if args.lat is None or args.lon is None:
            parser.error("Both --lat and --lon must be given together")
        lat, lon = args.lat, args.lon
        display_name = f"({lat:.5f}, {lon:.5f})"
    else:
        location_str = args.location or args.location_opt
        if not location_str:
            parser.error("Provide either location (positional or --location) or both --lat and --lon")
        print(f"Looking up location: {location_str}", file=sys.stderr)
        lat, lon, display_name = get_lat_lon(location_str)
        if lat is None or lon is None:
            print(f"Error: Location not found - {location_str}", file=sys.stderr)
            sys.exit(1)

    # Validate crop coefficient and days
    if args.kc < 0 or args.kc > 2:
        print("Warning: Crop coefficient (Kc) is typically between 0 and 2", file=sys.stderr)
    if args.days < 1 or args.days > MAX_HISTORICAL_DAYS:
        parser.error(f"--days must be between 1 and {MAX_HISTORICAL_DAYS}")

    # Fetch data
    data = fetch_historical_weather(lat, lon, display_name=display_name, days=args.days, kc=args.kc, output_format=args.format)
    
    if data is None:
        sys.exit(1)
    
    # Serialise once
    if args.format == 'json':
        data_dict = data.to_dict(orient='records')
        for record in data_dict:
            if 'date' in record:
                record['date'] = str(record['date'])
        output_str = json.dumps(data_dict, indent=2)
    else:
        output_str = data.to_csv(index=False)

    print(output_str)
    
    # Print summary statistics
    print("\n--- Summary Statistics ---", file=sys.stderr)
    print(f"Date range: {data['date'].min()} to {data['date'].max()}", file=sys.stderr)
    print(f"Average temperature: {data['temp'].mean():.1f}°C", file=sys.stderr)
    print(f"Total precipitation: {data['precip'].sum():.1f} mm", file=sys.stderr)
    print(f"Total evapotranspiration: {data['et0_fao'].sum():.1f} mm", file=sys.stderr)
    
    # Calculate water balance
    water_balance = data['precip'].sum() - data['et0_fao'].sum()
    if water_balance > 0:
        print(f"Water balance: +{water_balance:.1f} mm (surplus)", file=sys.stderr)
    else:
        print(f"Water balance: {water_balance:.1f} mm (deficit)", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
