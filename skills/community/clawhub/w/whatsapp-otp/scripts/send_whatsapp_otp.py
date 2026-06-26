#!/usr/bin/env python3
"""
Send WhatsApp OTP via CMI OmniChannel RCS API
"""

import argparse
import json
import sys
import os
from datetime import datetime, timezone

# CRITICAL: Clear proxy settings from environment to avoid connection timeout
# This is necessary because the API endpoint may not be accessible through proxies
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['no_proxy'] = '*'

# Suppress SSL warnings for this specific endpoint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import ssl

try:
    import requests
except ImportError:
    print("[ERROR] requests library not installed. Run: pip install requests")
    sys.exit(1)

from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context


class SSLAdapter(HTTPAdapter):
    """Custom adapter to handle problematic SSL configurations"""
    def init_poolmanager(self, *args, **kwargs):
        # Create a very permissive SSL context for legacy servers
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # Enable legacy server support
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        # Use default minimum TLS version (TLSv1.2) to avoid deprecation warning
        # but allow legacy server connections via OP_LEGACY_SERVER_CONNECT
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)


def generate_timestamp():
    """Generate ISO8601 UTC timestamp"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def send_whatsapp_otp(access_key_id, access_key_secret, app_name,
                      app_secret, to_number, otp_code):
    """
    Send WhatsApp OTP message

    Args:
        access_key_id: Tenant AccessKeyId
        access_key_secret: Tenant AccessKeySecret
        app_name: Application name
        app_secret: Application secret
        to_number: Recipient phone number with country code (e.g., +8613800138000)
        otp_code: OTP code to send
    """

    url = "https://cpaas-rcs.cmidict.com:7081/singleSend"

    # Build request payload
    payload = {
        "Method": "SingleSend",
        "AccessKeyId": access_key_id,
        "AccessKeySecret": access_key_secret,
        "Timestamp": generate_timestamp(),
        "ApplicationName": app_name,
        "ApplicationSecret": app_secret,
        "From": "+8618247665684",  # Fixed sender number (with + prefix)
        "To": to_number,
        "Type": "template",
        "Content": {
            "template": {
                "name": "test_otp_cn_111501",  # Pre-configured template
                "language": {
                    "code": "zh_CN"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [{
                            "type": "text",
                            "text": otp_code
                        }]
                    },
                    {
                        "type": "button",
                        "sub_type": "url",
                        "index": 0,
                        "parameters": [{
                            "type": "text",
                            "text": otp_code
                        }]
                    }
                ]
            }
        },
        "TemplateName": "test_otp_cn_111501"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Create a session with custom SSL adapter for problematic endpoints
        session = requests.Session()
        session.mount('https://', SSLAdapter())

        # Send POST request
        # Note: Using custom SSL adapter to handle the API endpoint's certificate configuration
        response = session.post(
            url,
            json=payload,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()

        result = response.json()

        # Check if successful
        if result.get("Code") == 0:
            print("[SUCCESS] WhatsApp OTP sent successfully!")
            print(f"  From: {result.get('From')}")
            print(f"  To: {result.get('To')}")
            print(f"  BizId: {result.get('BizId')}")
            print(f"  Timestamp: {result.get('Timestamp')}")
            return 0
        else:
            print(f"[ERROR] API returned error:")
            print(f"  Code: {result.get('Code')}")
            print(f"  Message: {result.get('Message')}")
            print(f"  Timestamp: {result.get('Timestamp')}")
            return 1

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Send WhatsApp OTP via CMI OmniChannel RCS API"
    )
    parser.add_argument("--access-key-id", required=True,
                        help="Tenant AccessKeyId")
    parser.add_argument("--access-key-secret", required=True,
                        help="Tenant AccessKeySecret")
    parser.add_argument("--app-name", default="default",
                        help="Application name (default: default)")
    parser.add_argument("--app-secret", required=True,
                        help="Application secret")
    parser.add_argument("--to", required=True,
                        help="Recipient phone number with country code, no + prefix (e.g., 8613800138000)")
    parser.add_argument("--otp", required=True,
                        help="OTP code to send")

    args = parser.parse_args()

    # Validate phone number format (should not start with +)
    if args.to.startswith('+'):
        print("[ERROR] Phone number should NOT include + prefix")
        print("  Correct format: 8613800138000")
        print(f"  Your input: {args.to}")
        return 1

    return send_whatsapp_otp(
        args.access_key_id,
        args.access_key_secret,
        args.app_name,
        args.app_secret,
        args.to,
        args.otp
    )


if __name__ == "__main__":
    sys.exit(main())
