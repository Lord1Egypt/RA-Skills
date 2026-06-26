#!/usr/bin/env python3
"""
VatGentic - End-to-End VAT Validation

Complete flow: request → auto-pay → wait → return result.

Usage:
    python3 vatgentic-validate.py --vat-number LU26375245 --auto-pay
    python3 vatgentic-validate.py --vat-number DE123456789 --timeout 300

Environment:
    VATGENTIC_N8N_URL - Your n8n instance URL
    LNBOT_API_TOKEN - ln.bot API token (for auto-pay)
    LNBOT_WALLET_ID - ln.bot wallet ID (for auto-pay)
"""

import argparse
import json
import os
import sys
import time
import requests
from typing import Optional

# Configuration
API_BASE = os.environ.get('VATGENTIC_API_URL')
if not API_BASE:
    print("❌ Error: VATGENTIC_API_URL not set")
    print("   export VATGENTIC_API_URL=https://api.vatgentic.com")
    sys.exit(1)

DEFAULT_AMOUNT = int(os.environ.get('VATGENTIC_AMOUNT', '10'))
DEFAULT_TIMEOUT = int(os.environ.get('VATGENTIC_TIMEOUT', '300'))
REQUEST_ENDPOINT = f'{API_BASE}/vat/request'
STATUS_ENDPOINT = f'{API_BASE}/vat/status'

# ln.bot configuration
LNBOT_API_KEY = os.environ.get('LNBOT_API_TOKEN')
LNBOT_WALLET_ID = os.environ.get('LNBOT_WALLET_ID')


def request_validation(
    vat_number: str,
    country: Optional[str] = None,
    amount_sats: int = DEFAULT_AMOUNT,
    provider: str = 'vatapi'
) -> dict:
    """Request VAT validation."""
    if not country and len(vat_number) > 2:
        if vat_number[:2].isalpha():
            country = vat_number[:2]
    
    payload = {
        'vatNumber': vat_number.upper().replace(' ', ''),
        'country': country.upper() if country else '',
        'amountSats': amount_sats,
        'provider': provider
    }
    
    response = requests.post(
        REQUEST_ENDPOINT,
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def check_status(request_id: str) -> dict:
    """Check validation status."""
    try:
        response = requests.get(f'{STATUS_ENDPOINT}/{request_id}', timeout=30)
        if response.status_code == 404:
            response = requests.get(
                STATUS_ENDPOINT,
                params={'requestId': request_id},
                timeout=30
            )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'request_id': request_id}


def auto_pay_invoice(invoice_id: str, checkout_link: str) -> bool:
    """
    Auto-pay invoice using ln.bot.
    
    Returns True if payment successful.
    """
    if not LNBOT_API_KEY or not LNBOT_WALLET_ID:
        print("⚠️  ln.bot credentials not found. Manual payment required.")
        print(f"   Open in browser: {checkout_link}")
        return False
    
    try:
        # Try to pay via ln.bot
        import importlib.util
        lnbot_spec = importlib.util.find_spec('lnbot')
        
        if lnbot_spec is None:
            print("⚠️  ln.bot package not installed. Manual payment required.")
            return False
        
        from lnbot import LnBot
        
        client = LnBot(api_key=LNBOT_API_KEY)
        wallet = client.wallet(LNBOT_WALLET_ID)
        
        # Get invoice details
        # Note: ln.bot API may require different method for payment
        # This is a placeholder - actual payment method depends on ln.bot API
        print(f"💳 Attempting auto-payment for invoice {invoice_id}...")
        
        # TODO: Implement actual ln.bot payment
        # For now, just print checkout link
        print(f"   Opening: {checkout_link}")
        
        return False  # Manual payment for now
        
    except Exception as e:
        print(f"⚠️  Auto-payment failed: {e}")
        print(f"   Manual payment: {checkout_link}")
        return False


def wait_for_completion(request_id: str, timeout: int = DEFAULT_TIMEOUT, interval: int = 3):
    """Wait for validation to complete."""
    elapsed = 0
    last_status = None
    
    while elapsed < timeout:
        result = check_status(request_id)
        status = result.get('status', 'unknown')
        
        if status != last_status:
            print(f"  Status: {status} (elapsed: {elapsed}s)")
            last_status = status
        
        if status == 'completed':
            return result
        elif status == 'failed':
            print(f"❌ Validation failed")
            return result
        
        time.sleep(interval)
        elapsed += interval
    
    print(f"⏱️  Timeout after {timeout}s")
    return {'error': 'timeout', 'request_id': request_id}


def main():
    parser = argparse.ArgumentParser(
        description='End-to-end VAT validation with Lightning payment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --vat-number LU26375245
  %(prog)s --vat-number DE123456789 --auto-pay
  %(prog)s --vat-number FR12345678901 --timeout 300 --json

Environment variables:
  VATGENTIC_API_URL  - **REQUIRED** - VatGentic service URL
  VATGENTIC_TIMEOUT  - Maximum wait time in seconds (default: 300)
  LNBOT_API_TOKEN    - ln.bot API token (for auto-pay)
  LNBOT_WALLET_ID    - ln.bot wallet ID (for auto-pay)

Example:
  export VATGENTIC_API_URL="https://api.vatgentic.com"
        """
    )
    
    parser.add_argument(
        '--vat-number', '-v',
        required=True,
        help='VAT number to validate'
    )
    
    parser.add_argument(
        '--country', '-c',
        help='Country code (optional, auto-detected)'
    )
    
    parser.add_argument(
        '--amount-sats', '-a',
        type=int,
        default=DEFAULT_AMOUNT,
        help=f'Payment amount in sats (default: {DEFAULT_AMOUNT})'
    )
    
    parser.add_argument(
        '--provider', '-p',
        default='vatapi',
        help='VAT API provider (default: vatapi)'
    )
    
    parser.add_argument(
        '--auto-pay',
        action='store_true',
        help='Attempt automatic payment (requires ln.bot credentials)'
    )
    
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f'Maximum wait time in seconds (default: {DEFAULT_TIMEOUT})'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=3,
        help='Status check interval in seconds (default: 3)'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output raw JSON'
    )
    
    args = parser.parse_args()
    
    print(f"🔍 Validating VAT: {args.vat_number}")
    print("")
    
    # Step 1: Request validation
    print("1️⃣  Creating validation request...")
    try:
        request_result = request_validation(
            vat_number=args.vat_number,
            country=args.country,
            amount_sats=args.amount_sats,
            provider=args.provider
        )
        
        if not request_result.get('ok'):
            print(f"❌ Request failed: {request_result.get('error')}")
            sys.exit(1)
        
        request_id = request_result.get('request_id')
        print(f"   ✓ Request ID: {request_id}")
        print(f"   ✓ Invoice: {request_result.get('invoice_id')}")
        print(f"   ✓ Amount: {request_result.get('amount_sats')} sats")
        print("")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Step 2: Payment
    print("2️⃣  Processing payment...")
    if args.auto_pay:
        paid = auto_pay_invoice(
            request_result.get('invoice_id'),
            request_result.get('checkout_link')
        )
        if not paid:
            print("   ⚠️  Manual payment may be required")
    else:
        print(f"   💳 Pay invoice:")
        print(f"      {request_result.get('checkout_link')}")
        print("   (Waiting for payment confirmation...)")
    print("")
    
    # Step 3: Wait for completion
    print("3️⃣  Waiting for validation...")
    final_result = wait_for_completion(
        request_id,
        timeout=args.timeout,
        interval=args.interval
    )
    print("")
    
    # Step 4: Output result
    if args.json:
        print(json.dumps(final_result, indent=2))
    else:
        status = final_result.get('status', 'unknown')
        
        if status == 'completed':
            print("✅ Validation Complete!")
            
            vat_result = final_result.get('vat_result')
            if vat_result:
                if isinstance(vat_result, str):
                    try:
                        vat_result = json.loads(vat_result)
                    except:
                        pass
                
                if isinstance(vat_result, dict):
                    print(f"   Valid: {vat_result.get('valid', 'unknown')}")
                    if vat_result.get('valid'):
                        if vat_result.get('company_name'):
                            print(f"   Company: {vat_result['company_name']}")
                        if vat_result.get('company_address'):
                            print(f"   Address: {vat_result['company_address']}")
        elif status == 'failed':
            print("❌ Validation failed")
        else:
            print(f"⏳ Status: {status}")
            print("   Check again later with:")
            print(f"   python3 vatgentic-status.py --request-id {request_id}")
    
    # Exit with appropriate code
    sys.exit(0 if final_result.get('status') == 'completed' else 1)


if __name__ == '__main__':
    main()
