#!/usr/bin/env python3
"""
qr-code-toolkit/scripts/generate_barcode.py
条形码生成器 - 支持 EAN/UPC/Code128/Code39
"""

import argparse
import os

import barcode
from barcode.writer import ImageWriter


def generate_barcode(data: str, barcode_type: str = 'code128', output_path: str = 'barcode.png'):
    """Generate barcode image"""
    
    type_map = {
        'code128': 'code128',
        'ean13': 'ean13',
        'ean8': 'ean8',
        'upca': 'upca',
        'code39': 'code39',
        'itf': 'itf',
        'codabar': 'codabar',
    }
    
    barcode_class = barcode.get_barcode_class(type_map.get(barcode_type, 'code128'))
    
    # Remove extension for barcode library
    output_base = os.path.splitext(output_path)[0]
    
    # Generate
    bc = barcode_class(data, writer=ImageWriter())
    bc.save(output_base)
    
    # The library saves as .png by default
    actual_output = output_base + '.png'
    
    # Rename if needed
    if actual_output != output_path and os.path.exists(actual_output):
        os.rename(actual_output, output_path)
    
    print(f"Barcode generated: {output_path}")
    print(f"  Type: {barcode_type}")
    print(f"  Data: {data}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Generate barcode')
    parser.add_argument('data', help='Data to encode')
    parser.add_argument('--type', '-t', choices=['code128', 'ean13', 'ean8', 'upca',
                                                  'code39', 'itf', 'codabar'],
                        default='code128', help='Barcode type')
    parser.add_argument('--output', '-o', default='barcode.png', help='Output path')
    args = parser.parse_args()
    
    generate_barcode(args.data, args.type, args.output)


if __name__ == '__main__':
    main()
