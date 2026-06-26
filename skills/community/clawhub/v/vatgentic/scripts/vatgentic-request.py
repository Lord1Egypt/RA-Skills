#!/usr/bin/env python3
"""
VatGentic - Request VAT Validation

Creates a new VAT validation request and returns a Lightning invoice.

Usage:
    python3 vatgentic-request.py --vat-number LU26375245 --country LU
    python3 vatgentic-request.py --vat-number DE123456789 --amount-sats 10

Environment:
    VATGENTIC_N8N_URL - **REQUIRED** - Your n8n instance URL
    VATGENTIC_AMOUNT - Default amount in sats (default: 10)
"""

import argparse
import json
import os
import sys
import requests
from typing import Optional

# Configuration
API_BASE = os.environ.get('VATGENTIC_API_URL')
if not API_BASE:
    print("❌ Error: VATGENTIC_API_URL not set")
    print("   export VATGENTIC_API_URL=https://api.vatgentic.com")
    sys.exit(1)

DEFAULT_AMOUNT = int(os.environ.get('VATGENTIC_AMOUNT', '10'))
REQUEST_ENDPOINT = f'{API_BASE}/vat/request'


def request_vat_validation(
    vat_number: str,
    country: Optional[str] = None,
    amount_sats: int = DEFAULT_AMOUNT,
    provider: str = 'vatapi'
) -> dict:
    """
    Request VAT validation via VatGentic webhook.
    
    Args:
        vat_number: VAT number to validate (with or without country prefix)
        country: Country code (optional, auto-detected if in VAT number)
        amount_sats: Payment amount in satoshis (default: 10)
        provider: VAT API provider (default: vatapi)
    
    Returns:
        dict with request_id, invoice details, and payment information
    """
    # Extract country code from VAT number if not provided
    if not country and len(vat_number) > 2:
        # Check if first 2 chars are letters (country prefix)
        if vat_number[:2].isalpha():
            country = vat_number[:2]
    
    payload = {
        'vatNumber': vat_number.upper().replace(' ', ''),
        'country': country.upper() if country else '',
        'amountSats': amount_sats,
        'provider': provider
    }
    
    try:
        response = requests.post(
            REQUEST_ENDPOINT,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {
            'ok': False,
            'error': str(e),
            'status_code': getattr(e.response, 'status_code', 0) if hasattr(e, 'response') else 0
        }


def format_payment_link(result: dict) -> str:
    """Format a user-friendly payment message."""
    if not result.get('ok'):
        return f"Error: {result.get('error', 'Unknown error')}"
    
    lines = [
        f"✅ VAT Validation Request Created",
        f"",
        f"Request ID: {result.get('request_id', 'N/A')}",
        f"VAT Number: {result.get('vat_number', 'N/A')}",
        f"Amount: {result.get('amount_sats', 0)} sats",
        f"",
        f"📄 Invoice ID: {result.get('invoice_id', 'N/A')}",
        f"📄 Status: {result.get('invoice_status', 'N/A')}",
        f"⏰ Expires: {result.get('expires_at', 'N/A')}",
        f"",
        f"💳 Payment Options:",
    ]
    
    if result.get('checkout_link'):
        lines.append(f"   Browser: {result['checkout_link']}")
    
    if result.get('payment_link'):
        lines.append(f"   Lightning: {result['payment_link']}")
    
    if result.get('bolt11'):
        bolt11 = result['bolt11']
        # Format Bolt11 for display (first 50 chars + ...)
        lines.append(f"   Bolt11: {bolt11[:50]}...")
    
    lines.extend([
        f"",
        f"Next step: Pay the invoice, then check status with:",
        f"  python3 vatgentic-status.py --request-id {result.get('request_id', '...')}"
    ])
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Request VAT validation with Lightning payment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --vat-number LU26375245 --country LU
  %(prog)s --vat-number DE123456789 --amount-sats 10
  %(prog)s --vat-number FR12345678901 --json

Environment variables:
  VATGENTIC_API_URL  - **REQUIRED** - VatGentic service URL
  VATGENTIC_AMOUNT   - Default amount in sats (default: 10)

Example:
  export VATGENTIC_API_URL="https://api.vatgentic.com"
        """
    )
    
    parser.add_argument(
        '--vat-number', '-v',
        required=True,
        help='VAT number to validate (e.g., LU26375245)'
    )
    
    parser.add_argument(
        '--country', '-c',
        help='Country code (optional, auto-detected from VAT number)'
    )
    
    parser.add_argument(
        '--amount-sats', '-a',
        type=int,
        default=DEFAULT_AMOUNT,
        help=f'Payment amount in satoshis (default: {DEFAULT_AMOUNT})'
    )
    
    parser.add_argument(
        '--provider', '-p',
        default='vatapi',
        help='VAT API provider (default: vatapi)'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output raw JSON (for scripting)'
    )
    
    args = parser.parse_args()
    
    # Make request
    result = request_vat_validation(
        vat_number=args.vat_number,
        country=args.country,
        amount_sats=args.amount_sats,
        provider=args.provider
    )
    
    # Output result
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_payment_link(result))
    
    # Exit with error code if request failed
    sys.exit(0 if result.get('ok') else 1)


if __name__ == '__main__':
    main()
