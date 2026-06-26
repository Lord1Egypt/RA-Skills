#!/usr/bin/env python3
"""Send emails via Resend API."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

RESEND_API_URL = "https://api.resend.com/emails"


def load_env():
    """Load environment from .env files."""
    paths = [
        Path.home() / '.openclaw' / 'workspace' / '.env',
        Path('.env').resolve(),
    ]
    for path in paths:
        if path.exists():
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip().strip('"\'')
                        if k not in os.environ:
                            os.environ[k] = v
            break


def get_config():
    """Get Resend configuration."""
    api_key = os.getenv('RESEND_API_KEY', '')
    from_email = os.getenv('RESEND_FROM', 'onboarding@resend.dev')
    
    if not api_key:
        print("Error: RESEND_API_KEY not configured")
        print("\nSet in .env file:")
        print("  RESEND_API_KEY=your_api_key")
        print("\nGet API key: https://resend.com")
        sys.exit(1)
    
    return {'api_key': api_key, 'from': from_email}


def send_email(config, to, subject, text=None, html=None, cc=None, bcc=None):
    """Send email via Resend API."""
    
    payload = {
        'from': config['from'],
        'to': to if isinstance(to, list) else [to],
        'subject': subject,
    }
    
    if text:
        payload['text'] = text
    if html:
        payload['html'] = html
    if cc:
        payload['cc'] = cc if isinstance(cc, list) else cc.split(',')
    if bcc:
        payload['bcc'] = bcc if isinstance(bcc, list) else bcc.split(',')
    
    headers = {
        'Authorization': f"Bearer {config['api_key']}",
        'Content-Type': 'application/json',
    }
    
    try:
        curl_cmd = [
            'curl', '-s', '-X', 'POST',
            RESEND_API_URL,
            '-H', f'Authorization: Bearer {config["api_key"]}',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(payload)
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if 'id' in response:
                    return True, f"Email sent! ID: {response['id']}"
                else:
                    return False, f"Unexpected response: {result.stdout}"
            except json.JSONDecodeError:
                return False, f"Invalid response: {result.stdout}"
        else:
            error = result.stderr or result.stdout or "Unknown error"
            return False, f"Failed: {error}"
    
    except Exception as e:
        return False, f"Failed: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description='Send email via Resend API')
    parser.add_argument('--to', required=True, help='Recipients (comma-separated)')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--text', help='Plain text content')
    parser.add_argument('--html', help='HTML content')
    parser.add_argument('--cc', help='CC recipients (comma-separated)')
    parser.add_argument('--bcc', help='BCC recipients (comma-separated)')
    
    args = parser.parse_args()
    
    if not args.text and not args.html:
        print("Error: Provide --text or --html")
        sys.exit(1)
    
    load_env()
    config = get_config()
    
    to_list = args.to.split(',')
    cc_list = args.cc.split(',') if args.cc else None
    bcc_list = args.bcc.split(',') if args.bcc else None
    
    success, message = send_email(
        config=config,
        to=to_list,
        subject=args.subject,
        text=args.text,
        html=args.html,
        cc=cc_list,
        bcc=bcc_list
    )
    
    print(message)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
