#!/usr/bin/env python3
"""
Fetch Forecast Weather Data

Script to fetch weather forecast data for a given location.
Returns the next N days of weather predictions (default 7, max 15).
"""

import argparse
import sys
import json

# Import from local utils module
from utils import get_lat_lon, load_forecast, process_data, DEFAULT_FORECAST_DAYS, MAX_FORECAST_DAYS


def fetch_forecast_weather(lat: float, lon: float, display_name: str = None, days: int = None, kc: float = 1.0, output_format: str = 'csv'):
    """
    Fetch forecast weather data for coordinates.

    Args:
        lat: Latitude
        lon: Longitude
        display_name: Optional label for logs (e.g. from geocoding)
        kc: Crop coefficient for evapotranspiration (default: 1.0)
        output_format: Output format - 'csv' or 'json' (default: 'csv')

    Returns:
        DataFrame with forecast weather data or None if error
    """
    if display_name is None:
        display_name = f"({lat:.5f}, {lon:.5f})"
    print(f"Using coordinates: {display_name} (Lat: {lat:.5f}, Lon: {lon:.5f})", file=sys.stderr)

    # Load forecast data
    print("Fetching weather forecast data...", file=sys.stderr)
    data = load_forecast(lat, lon, days=days)
    
    if data is None or data.empty:
        print("Error: No forecast data available for this location", file=sys.stderr)
        return None
    
    # Process data with crop coefficient
    data = process_data("forecast", data, kc=kc)
    
    print(f"Retrieved {len(data)} days of forecast data", file=sys.stderr)
    
    return data


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Fetch weather forecast data for a location or coordinates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fetch_forecast.py "Oslo, Norway"
  python fetch_forecast.py --location "London, UK" --format json
  python fetch_forecast.py --lat 59.91 --lon 10.75 --days 15 --kc 1.05
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
        default=DEFAULT_FORECAST_DAYS,
        metavar="N",
        help=f"Number of days of forecast (default: {DEFAULT_FORECAST_DAYS}, max: {MAX_FORECAST_DAYS})"
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
    if args.days < 1 or args.days > MAX_FORECAST_DAYS:
        parser.error(f"--days must be between 1 and {MAX_FORECAST_DAYS}")

    # Fetch data
    data = fetch_forecast_weather(lat, lon, display_name=display_name, days=args.days, kc=args.kc, output_format=args.format)
    
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
    print(f"Total precipitation (forecast): {data['precip'].sum():.1f} mm", file=sys.stderr)
    print(f"Total evapotranspiration (forecast): {data['et0_fao'].sum():.1f} mm", file=sys.stderr)
    
    # Calculate water balance
    water_balance = data['precip'].sum() - data['et0_fao'].sum()
    if water_balance > 0:
        print(f"Forecasted water balance: +{water_balance:.1f} mm (surplus)", file=sys.stderr)
    else:
        print(f"Forecasted water balance: {water_balance:.1f} mm (deficit)", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
