#!/usr/bin/env python3
"""
Weekly Report Login - Standalone Login Script

Performs login to the weekly report system and caches the authentication token.

Usage:
    python login.py              # Use cached token if available
    python login.py --force      # Force fresh login
    python login.py --headless   # Run in headless mode
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.config import Settings
from lib.login import (
    get_or_refresh_token,
    login_with_browser,
    clear_token_cache,
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Login to weekly report system and cache token"
    )

    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force fresh login (ignore cached token)"
    )
    parser.add_argument(
        "--headless", "-H",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.add_argument(
        "--logout",
        action="store_true",
        help="Clear cached token and exit"
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to config file"
    )

    return parser.parse_args()


def output_json(data: dict):
    """Output result as JSON to stdout."""
    print(json.dumps(data, ensure_ascii=False))


async def do_login(
    force: bool,
    headless: bool,
    config_path: str,
) -> dict:
    """
    Perform login operation.

    Returns:
        dict with success status and message
    """
    result = {
        "success": False,
        "message": None,
        "error": None,
    }

    try:
        settings = Settings.from_yaml(config_path)

        if headless:
            settings.login.headless = True

        if force:
            print("[Login] Forcing fresh login...")

        login_result = await get_or_refresh_token(
            settings,
            force_login=force,
            verbose=True,
        )

        result["success"] = True
        result["message"] = "Login successful, token cached"

    except TimeoutError:
        result["error"] = "Login timed out"
    except Exception as e:
        result["error"] = f"Login failed: {e}"

    return result


def main():
    """Main entry point."""
    args = parse_args()

    # Handle logout
    if args.logout:
        clear_token_cache()
        output_json({
            "success": True,
            "message": "Token cache cleared",
        })
        return

    # Perform login
    result = asyncio.run(do_login(
        force=args.force,
        headless=args.headless,
        config_path=args.config,
    ))

    output_json(result)
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
