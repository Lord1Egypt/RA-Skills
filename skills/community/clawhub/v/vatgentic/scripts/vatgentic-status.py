#!/usr/bin/env python3
"""
VatGentic - Check Validation Status

Check the status of a VAT validation request.

Usage:
    python3 vatgentic-status.py --request-id vat_1776348560582_yq24e3

Environment:
    VATGENTIC_N8N_URL - **REQUIRED** - Your n8n instance URL
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

STATUS_ENDPOINT = f'{API_BASE}/vat/status'


def check_status(request_id: str) -> dict:
    """
    Check the status of a VAT validation request.
    
    Args:
        request_id: Request ID from vatgentic-request.py
    
    Returns:
        dict with status and VAT result (if completed)
    """
    try:
        # Try path parameter first
        response = requests.get(
            f'{STATUS_ENDPOINT}/{request_id}',
            timeout=30
        )
        
        # If 404, try query parameter
        if response.status_code == 404:
            response = requests.get(
                STATUS_ENDPOINT,
                params={'requestId': request_id},
                timeout=30
            )
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {
            'error': str(e),
            'status_code': getattr(e.response, 'status_code', 0) if hasattr(e, 'response') else 0,
            'request_id': request_id
        }


def format_status(result: dict) -> str:
    """Format status result for human reading."""
    if 'error' in result:
        return f"❌ Error: {result['error']}\n\nRequest ID: {result.get('request_id', 'N/A')}"
    
    lines = [
        f"📊 VAT Validation Status",
        f"",
        f"Request ID: {result.get('request_id', 'N/A')}",
        f"Status: {result.get('status', 'unknown')}",
    ]
    
    # Add VAT details if available
    if result.get('vat_number'):
        lines.append(f"VAT Number: {result['vat_number']}")
    
    if result.get('country'):
        lines.append(f"Country: {result['country']}")
    
    # Add VAT result if completed
    vat_result = result.get('vat_result')
    if vat_result:
        lines.extend([
            f"",
            f"✅ Validation Result:",
        ])
        
        if isinstance(vat_result, str):
            # If vat_result is a JSON string, parse it
            try:
                vat_result = json.loads(vat_result)
            except:
                lines.append(f"   {vat_result}")
        
        if isinstance(vat_result, dict):
            lines.append(f"   Valid: {vat_result.get('valid', 'unknown')}")
            
            if vat_result.get('valid'):
                if vat_result.get('company_name'):
                    lines.append(f"   Company: {vat_result['company_name']}")
                if vat_result.get('company_address'):
                    lines.append(f"   Address: {vat_result['company_address']}")
                if vat_result.get('country_code'):
                    lines.append(f"   Country: {vat_result['country_code']}")
            else:
                lines.append(f"   ⚠️ Invalid VAT number")
    
    elif result.get('status') == 'pending_payment':
        lines.extend([
            f"",
            f"⏳ Waiting for payment...",
            f"   Pay the invoice to proceed with validation."
        ])
    
    elif result.get('status') == 'processing':
        lines.extend([
            f"",
            f"⏳ Processing...",
            f"   Payment received, validating with VAT API..."
        ])
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Check VAT validation request status',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --request-id vat_1776348560582_yq24e3
  %(prog)s --request-id vat_1234567890_abc123 --json

Environment variables:
  VATGENTIC_API_URL  - **REQUIRED** - VatGentic service URL
  
Example:
  export VATGENTIC_API_URL="https://api.vatgentic.com"
        """
    )
    
    parser.add_argument(
        '--request-id', '-r',
        required=True,
        help='Request ID from vatgentic-request.py'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output raw JSON (for scripting)'
    )
    
    parser.add_argument(
        '--wait', '-w',
        type=int,
        default=0,
        help='Wait for completion (timeout in seconds)'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=3,
        help='Check interval in seconds (default: 3)'
    )
    
    args = parser.parse_args()
    
    # Check status
    if args.wait > 0:
        # Wait for completion
        print(f"Waiting for completion (timeout: {args.wait}s)...")
        elapsed = 0
        
        while elapsed < args.wait:
            result = check_status(args.request_id)
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                # Clear previous output
                print('\033[2J\033[H', end='')
                print(format_status(result))
            
            if result.get('status') in ['completed', 'failed']:
                break
            
            elapsed += args.interval
            if elapsed < args.wait:
                time.sleep(args.interval)
    else:
        result = check_status(args.request_id)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_status(result))
    
    # Exit with error code if status check failed
    sys.exit(0 if 'error' not in result else 1)


if __name__ == '__main__':
    import time
    main()
