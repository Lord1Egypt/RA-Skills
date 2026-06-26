#!/usr/bin/env python3
"""
TwitterShots API - Tweet Screenshot Generator

Generate high-quality screenshots of Twitter/X posts.

Usage:
    python screenshot_tweet.py <tweet_id_or_url> [options]

Environment:
    TWITTERSHOTS_API_KEY: Your API key (required)

Examples:
    python screenshot_tweet.py 1617979122625712128
    python screenshot_tweet.py https://twitter.com/user/status/1617979122625712128
    python screenshot_tweet.py 1617979122625712128 --format png --theme dark
    python screenshot_tweet.py 1617979122625712128 --aspect-ratio 4:5 --output tweet.png
"""

import argparse
import os
import re
import sys
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


API_BASE = "https://api.twittershots.com/api/v1/screenshot"


def extract_tweet_id(input_str: str) -> str:
    """Extract tweet ID from URL or return as-is if already numeric."""
    if input_str.isdigit():
        return input_str
    
    match = re.search(r'/status/(\d+)', input_str)
    if match:
        return match.group(1)
    
    raise ValueError(f"Could not extract tweet ID from: {input_str}")


def screenshot_tweet(
    tweet_id: str,
    api_key: str,
    format: str = "png",
    theme: str = "light",
    aspect_ratio: str = "auto",
    return_type: str = "buffer",
    show_stats: bool = True,
    show_views: bool = True,
    show_timestamp: bool = True,
    show_media: bool = True,
    show_full_text: bool = True,
    media_layout: str = "grid",
    time_zone_offset: str = "UTC+0",
    logo: str = "x",
    width: int = None,
    height: str = "auto",
    container_background: str = None,
    background_image: str = None,
    border_radius: int = None,
    container_padding: int = None,
) -> tuple:
    """
    Generate a screenshot of a tweet.
    
    Returns:
        tuple: (content, content_type, headers)
    """
    params = {
        "format": format,
        "theme": theme,
        "aspectRatio": aspect_ratio,
        "returnType": return_type,
        "showStats": str(show_stats).lower(),
        "showViews": str(show_views).lower(),
        "showTimestamp": str(show_timestamp).lower(),
        "showMedia": str(show_media).lower(),
        "showFullText": str(show_full_text).lower(),
        "mediaLayout": media_layout,
        "timeZoneOffset": time_zone_offset,
        "logo": logo,
        "height": height,
    }
    
    if width:
        params["width"] = width
    if container_background:
        params["containerBackground"] = container_background
    if background_image:
        params["backgroundImage"] = background_image
    if border_radius is not None:
        params["borderRadius"] = border_radius
    if container_padding is not None:
        params["containerPadding"] = container_padding
    
    accept_header = {
        "svg": "image/svg+xml",
        "png": "image/png",
        "html": "text/html",
    }.get(format, "image/png")
    
    url = f"{API_BASE}/{tweet_id}"
    
    response = requests.get(
        url,
        headers={
            "X-API-KEY": api_key,
            "Accept": accept_header,
        },
        params=params,
    )
    
    if response.status_code != 200:
        error_msg = f"API Error {response.status_code}"
        try:
            error_data = response.json()
            error_msg += f": {error_data.get('message', response.text)}"
        except:
            error_msg += f": {response.text}"
        raise Exception(error_msg)
    
    return response.content, response.headers.get("Content-Type"), response.headers


def main():
    parser = argparse.ArgumentParser(
        description="Generate tweet screenshots using TwitterShots API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    
    parser.add_argument(
        "tweet",
        help="Tweet ID or URL (e.g., 1617979122625712128 or https://twitter.com/user/status/...)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output filename (default: tweet-{id}.{format})",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["svg", "png", "html"],
        default="png",
        help="Output format (default: png)",
    )
    parser.add_argument(
        "-t", "--theme",
        choices=["light", "dark"],
        default="light",
        help="Color theme (default: light)",
    )
    parser.add_argument(
        "-a", "--aspect-ratio",
        choices=["auto", "1:1", "4:5", "5:4", "16:9", "9:16"],
        default="auto",
        help="Aspect ratio (default: auto)",
    )
    parser.add_argument(
        "--return-url",
        action="store_true",
        help="Return URL instead of downloading image",
    )
    parser.add_argument(
        "--no-stats",
        action="store_true",
        help="Hide reply/retweet/like counts",
    )
    parser.add_argument(
        "--no-views",
        action="store_true",
        help="Hide view count",
    )
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Hide timestamp",
    )
    parser.add_argument(
        "--no-media",
        action="store_true",
        help="Hide images and videos",
    )
    parser.add_argument(
        "--no-full-text",
        action="store_true",
        help="Collapse tweet with 'Show more' button",
    )
    parser.add_argument(
        "--media-layout",
        choices=["grid", "vertical"],
        default="grid",
        help="Media display layout (default: grid)",
    )
    parser.add_argument(
        "--time-zone-offset",
        default="UTC+0",
        help="Fixed UTC offset for timestamp (e.g., UTC+8, UTC-5, UTC+5:30)",
    )
    parser.add_argument(
        "--logo",
        choices=["x", "bluebird", "none"],
        default="x",
        help="Logo style (default: x)",
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Content width in pixels (300-1000)",
    )
    parser.add_argument(
        "--height",
        help="Content height in pixels (default: auto)",
    )
    parser.add_argument(
        "--background",
        help="Background color (hex, rgba, or gradient)",
    )
    parser.add_argument(
        "--background-image",
        help="Background image URL (HTTPS)",
    )
    parser.add_argument(
        "--border-radius",
        type=int,
        help="Border radius in pixels",
    )
    parser.add_argument(
        "--padding",
        type=int,
        help="Container padding in pixels",
    )
    parser.add_argument(
        "--api-key",
        help="API key (default: TWITTERSHOTS_API_KEY env var)",
    )
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("TWITTERSHOTS_API_KEY")
    if not api_key:
        print("Error: API key required. Set TWITTERSHOTS_API_KEY or use --api-key")
        sys.exit(1)
    
    try:
        tweet_id = extract_tweet_id(args.tweet)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    try:
        content, content_type, headers = screenshot_tweet(
            tweet_id=tweet_id,
            api_key=api_key,
            format=args.format,
            theme=args.theme,
            aspect_ratio=args.aspect_ratio,
            return_type="url" if args.return_url else "buffer",
            show_stats=not args.no_stats,
            show_views=not args.no_views,
            show_timestamp=not args.no_timestamp,
            show_media=not args.no_media,
            show_full_text=not args.no_full_text,
            media_layout=args.media_layout,
            time_zone_offset=args.time_zone_offset,
            logo=args.logo,
            width=args.width,
            height=args.height,
            container_background=args.background,
            background_image=args.background_image,
            border_radius=args.border_radius,
            container_padding=args.padding,
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    quota_remaining = headers.get("X-Quota-Remaining", "?")
    quota_limit = headers.get("X-Quota-Limit", "?")
    
    if args.return_url:
        import json
        data = json.loads(content)
        print(f"URL: {data['url']}")
        print(f"Format: {data['format']}")
        print(f"Tweet ID: {data['tweetId']}")
    else:
        output_file = args.output or f"tweet-{tweet_id}.{args.format}"
        with open(output_file, "wb") as f:
            f.write(content)
        print(f"Saved: {output_file}")
    
    print(f"Quota: {quota_remaining}/{quota_limit} remaining")


if __name__ == "__main__":
    main()
