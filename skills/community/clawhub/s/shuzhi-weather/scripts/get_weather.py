#!/usr/bin/env python3
"""
Shuzhi Weather API Client
Fetches hourly weather forecasts with HMAC-SHA256 authentication
"""

import hashlib
import hmac
import base64
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# API Configuration
API_CONFIG = {
    "url": "https://test-apisix-gateway.shuzhi.shuqinkeji.cn",
    "path": "/2033738771717074945",
    "method": "POST",
    "product_id": "2033747427070226434"
}


def load_config() -> Dict[str, str]:
    """
    Load credentials from ~/.openclaw/skills/shuzhi-weather/config.json

    Returns:
        Dictionary containing app_key and app_secret

    Raises:
        FileNotFoundError: If config file does not exist
        ValueError: If config file is missing required fields
    """
    # Determine home directory
    home_dir = os.path.expanduser("~")
    skill_config_dir = os.path.join(home_dir, ".openclaw", "skills", "shuzhi-weather")
    config_file_path = os.path.join(skill_config_dir, "config.json")

    # Check if config file exists
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            f"Configuration file not found: {config_file_path}\n"
            f"Please create this file with your credentials:\n"
            f"  {{'app_key': 'your_app_key', 'app_secret': 'your_app_secret'}}"
        )

    # Load and parse config file
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")

    # Validate required fields
    if 'app_key' not in config or 'app_secret' not in config:
        raise ValueError(
            f"Config file is missing required fields: 'app_key' and 'app_secret'\n"
            f"Current config: {config}"
        )

    return {
        'app_key': config['app_key'],
        'app_secret': config['app_secret']
    }


def format_date(date: datetime) -> str:
    """Format date to GMT format"""
    return date.strftime("%a, %d %b %Y %H:%M:%S GMT")


def generate_hmac_signature(app_secret: str, signing_string: str) -> str:
    """Generate HMAC-SHA256 signature"""
    hmac_obj = hmac.new(
        app_secret.encode('utf-8'),
        signing_string.encode('utf-8'),
        hashlib.sha256
    )
    return base64.b64encode(hmac_obj.digest()).decode('utf-8')


def get_weather_forecast(
    longitude: str,
    latitude: str,
    hourly: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Query Shuzhi Weather API with HMAC-SHA256 authentication

    Args:
        longitude: Longitude coordinate (required)
        latitude: Latitude coordinate (required)
        hourly: Hourly data type (optional)

    Returns:
        Weather data dictionary, or None if failed
    """
    # Validate required parameters
    if not longitude or not latitude:
        print("Error: longitude and latitude are required parameters", file=sys.stderr)
        return None

    # Load credentials
    try:
        credentials = load_config()
    except (FileNotFoundError, ValueError) as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return None

    # Build request parameters
    body_map = {
        "longitude": longitude,
        "latitude": latitude
    }

    if hourly:
        body_map["hourly"] = hourly

    current_time = format_date(datetime.now(timezone.utc))
    body_json = json.dumps(body_map, separators=(',', ':'))

    # Generate signatures
    canonical_string = f"{API_CONFIG['method']}\n{API_CONFIG['path']}\n\n{credentials['app_key']}\n{current_time}\n"
    signature = generate_hmac_signature(credentials['app_secret'], canonical_string)
    body_signature = generate_hmac_signature(credentials['app_secret'], body_json)

    # Build request
    request_url = API_CONFIG['url'] + API_CONFIG['path']

    headers = {
        "X-HMAC-ACCESS-KEY": credentials['app_key'],
        "X-APP-PRODUCT-ID": API_CONFIG['product_id'],
        "X-HMAC-ALGORITHM": "hmac-sha256",
        "X-HMAC-SIGNATURE": signature,
        "X-HMAC-DIGEST": body_signature,
        "Date": current_time,
        "Content-Type": "application/json"
    }

    # Send HTTP POST request
    try:
        req = urllib.request.Request(
            request_url,
            data=body_json.encode('utf-8'),
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            response_body = response.read().decode('utf-8')
            response_code = response.getcode()

            # Parse response
            response_data = json.loads(response_body)

            if response_code != 200:
                print(f"Error: HTTP status code is not 200, actual: {response_code}", file=sys.stderr)
                return None

            if response_data.get('code') != 200:
                print(f"Error: Response code is not 200, actual: {response_data.get('code')}", file=sys.stderr)
                print(f"Error message: {response_data.get('message')}", file=sys.stderr)
                return None

            if not response_data.get('data'):
                print("Error: Response data is empty", file=sys.stderr)
                return None

            # Return weather data
            return response_data['data']

    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error response: {error_body}", file=sys.stderr)
        except:
            pass
        return None
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unknown error: {e}", file=sys.stderr)
        return None


def main():
    """Main function - command line test"""
    if len(sys.argv) < 3:
        print("Usage: python get_weather.py <longitude> <latitude> [hourly]", file=sys.stderr)
        print("Example: python get_weather.py 116.4074 39.9042 temperature_2m", file=sys.stderr)
        sys.exit(1)

    longitude = sys.argv[1]
    latitude = sys.argv[2]
    hourly = sys.argv[3] if len(sys.argv) > 3 else None

    # Call API
    result = get_weather_forecast(longitude, latitude, hourly)

    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)
    else:
        print("Weather query failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
