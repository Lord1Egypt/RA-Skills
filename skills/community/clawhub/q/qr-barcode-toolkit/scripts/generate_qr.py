#!/usr/bin/env python3
"""
qr-code-toolkit/scripts/generate_qr.py
基础二维码生成器
"""

import argparse
import os

import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q


def generate(data: str, output_path: str, size: int = 10, border: int = 2,
             error_correction: str = 'M', box_size: int = 10,
             fg_color: str = 'black', bg_color: str = 'white'):
    """Generate a QR code"""
    
    ec_map = {
        'L': ERROR_CORRECT_L,  # ~7%
        'M': ERROR_CORRECT_M,  # ~15%
        'Q': ERROR_CORRECT_Q,  # ~25%
        'H': ERROR_CORRECT_H,  # ~30%
    }
    
    qr = qrcode.QRCode(
        version=None,  # Auto-fit
        error_correction=ec_map.get(error_correction, ERROR_CORRECT_M),
        box_size=box_size,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
    
    # Resize if needed
    if size:
        pixel_size = size * box_size
        img = img.resize((pixel_size, pixel_size))
    
    img.save(output_path)
    print(f"QR code generated: {output_path}")
    print(f"  Data: {data[:50]}{'...' if len(data) > 50 else ''}")
    print(f"  Size: {img.size}")
    print(f"  Error correction: {error_correction}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Generate QR code')
    parser.add_argument('data', help='Data to encode')
    parser.add_argument('--output', '-o', required=True, help='Output image path')
    parser.add_argument('--size', '-s', type=int, default=10, help='Size multiplier')
    parser.add_argument('--border', '-b', type=int, default=2, help='Border width')
    parser.add_argument('--error-correction', '-e', choices=['L', 'M', 'Q', 'H'],
                        default='M', help='Error correction level')
    parser.add_argument('--box-size', type=int, default=10, help='Box size in pixels')
    parser.add_argument('--fg-color', default='black', help='Foreground color')
    parser.add_argument('--bg-color', default='white', help='Background color')
    args = parser.parse_args()
    
    generate(args.data, args.output, args.size, args.border,
             args.error_correction, args.box_size, args.fg_color, args.bg_color)


if __name__ == '__main__':
    main()
