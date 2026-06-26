#!/usr/bin/env python3
"""Validate URL lists and check robots.txt compliance."""

import argparse
import sys
from pathlib import Path
from typing import List, Set, Tuple
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import requests


def load_urls(input_file: Path) -> List[str]:
    """Load URLs from file (one per line)."""
    with open(input_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return urls


def validate_url_format(url: str) -> Tuple[bool, str]:
    """Validate URL format."""
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, "Missing scheme or domain"
        if result.scheme not in ['http', 'https']:
            return False, f"Invalid scheme: {result.scheme}"
        return True, "Valid"
    except Exception as e:
        return False, str(e)


def check_robots_txt(url: str, user_agent: str = '*') -> Tuple[bool, str]:
    """Check if URL is allowed by robots.txt."""
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        rp = RobotFileParser()
        rp.set_url(robots_url)

        try:
            rp.read()
        except Exception:
            # If robots.txt doesn't exist or can't be read, assume allowed
            return True, "No robots.txt (allowed by default)"

        can_fetch = rp.can_fetch(user_agent, url)
        if can_fetch:
            return True, "Allowed by robots.txt"
        else:
            return False, "Disallowed by robots.txt"

    except Exception as e:
        return True, f"Could not check robots.txt: {e} (allowed by default)"


def group_by_domain(urls: List[str]) -> dict[str, List[str]]:
    """Group URLs by domain."""
    domains = {}
    for url in urls:
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(url)
    return domains


def main():
    parser = argparse.ArgumentParser(
        description="Validate URL lists and check robots.txt compliance"
    )
    parser.add_argument(
        'input_file',
        type=Path,
        help='File containing URLs (one per line)'
    )
    parser.add_argument(
        '--user-agent',
        default='*',
        help='User agent to check in robots.txt (default: *)'
    )
    parser.add_argument(
        '--skip-robots',
        action='store_true',
        help='Skip robots.txt checking'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Exit with error if any URL is invalid or disallowed'
    )

    args = parser.parse_args()

    # Load URLs
    try:
        urls = load_urls(args.input_file)
    except Exception as e:
        print(f"❌ Error loading URL file: {e}", file=sys.stderr)
        sys.exit(1)

    if not urls:
        print("❌ No URLs found in input file", file=sys.stderr)
        sys.exit(1)

    print(f"📋 Validating {len(urls)} URLs...\n")

    # Validate formats
    invalid_urls = []
    valid_urls = []

    for url in urls:
        is_valid, reason = validate_url_format(url)
        if is_valid:
            valid_urls.append(url)
        else:
            invalid_urls.append((url, reason))
            print(f"❌ INVALID: {url}")
            print(f"   Reason: {reason}\n")

    if invalid_urls:
        print(f"⚠️  Found {len(invalid_urls)} invalid URLs\n")
        if args.strict:
            sys.exit(1)
    else:
        print(f"✅ All {len(urls)} URLs have valid format\n")

    # Group by domain
    domains = group_by_domain(valid_urls)
    print(f"🌐 URLs span {len(domains)} domain(s):")
    for domain, domain_urls in domains.items():
        print(f"   {domain}: {len(domain_urls)} URLs")
    print()

    # Check robots.txt
    if not args.skip_robots and valid_urls:
        print(f"🤖 Checking robots.txt compliance (user-agent: {args.user_agent})...\n")

        disallowed = []
        for url in valid_urls:
            allowed, reason = check_robots_txt(url, args.user_agent)
            if not allowed:
                disallowed.append((url, reason))
                print(f"🚫 DISALLOWED: {url}")
                print(f"   Reason: {reason}\n")

        if disallowed:
            print(f"⚠️  {len(disallowed)} URLs are disallowed by robots.txt")
            print(f"   Consider removing these URLs or using a different user agent\n")
            if args.strict:
                sys.exit(1)
        else:
            print(f"✅ All {len(valid_urls)} URLs are allowed by robots.txt\n")

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total URLs: {len(urls)}")
    print(f"Valid URLs: {len(valid_urls)}")
    print(f"Invalid URLs: {len(invalid_urls)}")
    if not args.skip_robots:
        print(f"Disallowed by robots.txt: {len(disallowed) if 'disallowed' in locals() else 0}")
    print(f"Unique domains: {len(domains)}")

    if args.strict and (invalid_urls or (not args.skip_robots and disallowed)):
        print("\n❌ Validation failed (--strict mode)")
        sys.exit(1)
    else:
        print("\n✅ Validation complete")


if __name__ == '__main__':
    main()
