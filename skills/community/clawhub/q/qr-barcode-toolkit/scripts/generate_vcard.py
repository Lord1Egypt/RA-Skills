#!/usr/bin/env python3
"""
qr-code-toolkit/scripts/generate_vcard.py
vCard 名片二维码生成器
"""

import argparse

from generate_qr import generate


def generate_vcard_qr(name: str, phone: str = None, email: str = None,
                      org: str = None, title: str = None, url: str = None,
                      address: str = None, output_path: str = 'vcard_qr.png'):
    """Generate vCard QR code"""
    
    vcard = "BEGIN:VCARD\nVERSION:3.0\n"
    vcard += f"FN:{name}\n"
    vcard += f"N:{name};;;;\n"
    
    if phone:
        vcard += f"TEL;TYPE=CELL:{phone}\n"
    if email:
        vcard += f"EMAIL;TYPE=WORK:{email}\n"
    if org:
        vcard += f"ORG:{org}\n"
    if title:
        vcard += f"TITLE:{title}\n"
    if url:
        vcard += f"URL:{url}\n"
    if address:
        vcard += f"ADR;TYPE=WORK:;;{address};;;;\n"
    
    vcard += "END:VCARD"
    
    generate(vcard, output_path, error_correction='M')
    print(f"vCard QR generated for: {name}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Generate vCard QR code')
    parser.add_argument('--name', '-n', required=True, help='Full name')
    parser.add_argument('--phone', '-p', help='Phone number')
    parser.add_argument('--email', '-e', help='Email address')
    parser.add_argument('--org', '-o', help='Organization')
    parser.add_argument('--title', '-t', help='Job title')
    parser.add_argument('--url', '-u', help='Website URL')
    parser.add_argument('--address', '-a', help='Address')
    parser.add_argument('--output', default='vcard_qr.png', help='Output path')
    args = parser.parse_args()
    
    generate_vcard_qr(args.name, args.phone, args.email, args.org,
                     args.title, args.url, args.address, args.output)


if __name__ == '__main__':
    main()
