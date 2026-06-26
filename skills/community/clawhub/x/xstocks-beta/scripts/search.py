#!/usr/bin/env python3
"""Search xStocks tokens on Solana."""

import argparse
import json
import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

from xstocks import (
    filter_tokens,
    find_token_by_solana_address,
    format_names,
    get_catalog,
    get_solana_addresses,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="scripts/search.py",
        description="Search xStocks tokens on Solana (104 tokens).",
        epilog="""examples:
  python3 scripts/search.py                                 List all tokens
  python3 scripts/search.py --filter "apple"                Filter by name/symbol
  python3 scripts/search.py --filter "tesla" --address-only Get mint address
  python3 scripts/search.py --lookup "svm:XsDoVf..."        Reverse lookup by mint
  python3 scripts/search.py --json                          Full JSON output""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--filter",
        metavar="TEXT",
        help="Case-insensitive substring filter on name or symbol",
    )
    parser.add_argument(
        "--address-only",
        action="store_true",
        help="Print only Solana mint addresses, one per line (use with --filter)",
    )
    parser.add_argument(
        "--lookup",
        metavar="ADDRESS",
        help="Reverse lookup: given a Solana mint address, print the matching token",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output as JSON instead of human-readable lines",
    )
    args = parser.parse_args()

    catalog = get_catalog()

    # Reverse lookup mode
    if args.lookup:
        token = find_token_by_solana_address(catalog, args.lookup)
        if not token:
            print(f"Error: no xStock found for address {args.lookup}", file=sys.stderr)
            return 1
        if args.json_output:
            json.dump(token, sys.stdout)
            print()
        else:
            name = token.get("name", "")
            symbol = token.get("symbol", "")
            address = token.get("address", "")
            print(f"{name} [{symbol}] (mint: {address})")
        return 0

    # Filter
    tokens = filter_tokens(catalog, args.filter or "")

    if args.filter and not tokens:
        print(f'Error: no xStocks matched filter "{args.filter}"', file=sys.stderr)
        return 1

    # Address-only mode
    if args.address_only:
        if not args.filter:
            print("Error: --address-only requires --filter", file=sys.stderr)
            return 2
        for addr in get_solana_addresses(tokens):
            print(addr)
        return 0

    # JSON output
    if args.json_output:
        json.dump(tokens, sys.stdout, indent=2)
        print()
        return 0

    # Default: human-readable names
    for line in format_names(tokens):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
