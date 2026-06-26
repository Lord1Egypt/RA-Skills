#!/usr/bin/env python3
import argparse
import urllib.request

def main():
    parser = argparse.ArgumentParser(description="Fetch a public web page")
    parser.add_argument("--url", required=True, help="Public URL to fetch")
    args = parser.parse_args()

    req = urllib.request.Request(
        args.url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; ScraperSkill/1.0)"
        }
    )

    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    print(html[:4000])

if __name__ == "__main__":
    main()
