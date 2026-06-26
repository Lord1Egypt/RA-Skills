#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "crawl4ai",
# ]
# ///
#
"""
Website Scraper Pro - Scrape a single page into clean markdown or JSON with Crawl4AI.
"""

import sys
import warnings

warnings.filterwarnings(
    "ignore",
    message=r"urllib3 \(.*\) or chardet \(.*\)/charset_normalizer \(.*\) doesn't match a supported version!",
)

from mutex import acquire_lock
from service import format_output, get_website_scrape
from utils import parse_cli_args


def main():
    """Entry point for the website scraper skill."""
    try:
        options = parse_cli_args(sys.argv[1:])
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    with acquire_lock():
        result = get_website_scrape(
            options["url"],
            options["use_js"],
            options["query"],
            options["output_format"],
        )
    print(format_output(result))


if __name__ == "__main__":
    main()
