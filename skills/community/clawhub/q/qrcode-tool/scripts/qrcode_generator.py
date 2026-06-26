#!/usr/bin/env python3
"""QR Code Generator - Generate QR codes from text/URL"""
import sys
import os
import base64
import ssl
import urllib.request
import urllib.parse
import argparse

try:
    import certifi
    CERTIFI_AVAILABLE = True
except ImportError:
    CERTIFI_AVAILABLE = False

def generate_qrcode(text, size=300, margin=4, format='png'):
    """Generate QR code using qrserver.com API
    
    Args:
        text: Text or URL to encode
        size: QR code size in pixels (default 300)
        margin: Margin around QR code (default 4)
        format: Output format (default png)
    
    Returns:
        dict with success status and data/base64 or error message
    """
    encoded_text = urllib.parse.quote(text)
    url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&margin={margin}&format={format}&data={encoded_text}"
    
    headers = {
        'User-Agent': 'QRCode-Tool/1.0 (https://github.com/qiance)'
    }
    
    try:
        # SSL with certifi if available, fallback to default
        if CERTIFI_AVAILABLE:
            ctx = ssl.create_default_context()
            ctx.load_verify_locations(certifi.where())
        else:
            ctx = ssl.create_default_context()
        
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = response.read()
        
        return {
            "success": True,
            "data": f"data:image/{format};base64,{base64.b64encode(data).decode()}",
            "url": url,
            "size": size,
            "text_length": len(text)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(
        description='Generate QR codes from text or URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 qrcode_generator.py "https://example.com"
  python3 qrcode_generator.py "Hello World" --size 500
  python3 qrcode_generator.py "WIFI:T:WPA;S:MyNetwork;P:password;;" --margin 2
        """
    )
    
    parser.add_argument('text', help='Text or URL to encode')
    parser.add_argument('--size', type=int, default=300, help='QR code size in pixels (default: 300)')
    parser.add_argument('--margin', type=int, default=4, help='Margin around QR code (default: 4)')
    parser.add_argument('--format', choices=['png', 'gif', 'jpeg', 'jpg'], default='png', help='Output format (default: png)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = generate_qrcode(args.text, args.size, args.margin, args.format)
    
    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"✅ QR Code generated successfully!")
            print(f"   Size: {result['size']}x{result['size']} pixels")
            print(f"   Text length: {result['text_length']} characters")
            print(f"   Base64 length: {len(result['data'])} characters")
        else:
            print(f"❌ Failed to generate QR code: {result['error']}")

if __name__ == '__main__':
    main()
