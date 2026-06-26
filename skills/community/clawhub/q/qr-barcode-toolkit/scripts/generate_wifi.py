#!/usr/bin/env python3
"""
qr-code-toolkit/scripts/generate_wifi.py
WiFi 连接二维码生成器
"""

import argparse

from generate_qr import generate


def generate_wifi_qr(ssid: str, password: str, security: str = 'WPA', hidden: bool = False,
                     output_path: str = 'wifi_qr.png'):
    """Generate WiFi QR code
    
    Format: WIFI:S:ssid;T:security;P:password;H:hidden;;
    """
    # Escape special characters
    ssid_escaped = ssid.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,')
    password_escaped = password.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,')
    
    wifi_string = f"WIFI:S:{ssid_escaped};T:{security};P:{password_escaped};"
    if hidden:
        wifi_string += "H:true;"
    wifi_string += ";"
    
    generate(wifi_string, output_path, error_correction='H')
    print(f"WiFi QR: SSID={ssid}, Security={security}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Generate WiFi QR code')
    parser.add_argument('--ssid', '-s', required=True, help='WiFi SSID')
    parser.add_argument('--password', '-p', required=True, help='WiFi password')
    parser.add_argument('--security', '-t', choices=['WPA', 'WEP', 'nopass'],
                        default='WPA', help='Security type')
    parser.add_argument('--hidden', action='store_true', help='Hidden network')
    parser.add_argument('--output', '-o', default='wifi_qr.png', help='Output path')
    args = parser.parse_args()
    
    generate_wifi_qr(args.ssid, args.password, args.security, args.hidden, args.output)


if __name__ == '__main__':
    main()
