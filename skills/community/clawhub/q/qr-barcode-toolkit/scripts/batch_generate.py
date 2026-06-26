#!/usr/bin/env python3
"""
qr-code-toolkit/scripts/batch_generate.py
批量二维码生成器
"""

import argparse
import csv
import json
import os
from pathlib import Path

from generate_qr import generate


def batch_from_csv(csv_path: str, output_dir: str, data_column: str = 'data',
                   filename_column: str = 'filename'):
    """Batch generate QR codes from CSV file"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    generated = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = row.get(data_column, '')
            filename = row.get(filename_column, f"qr_{len(generated)+1}.png")
            
            if not filename.endswith('.png'):
                filename += '.png'
            
            output_path = os.path.join(output_dir, filename)
            generate(data, output_path)
            generated.append(output_path)
    
    print(f"\nGenerated {len(generated)} QR codes in {output_dir}")
    return generated


def batch_from_json(json_path: str, output_dir: str):
    """Batch generate from JSON array"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    generated = []
    for i, item in enumerate(items):
        data = item.get('data', item.get('url', item.get('text', '')))
        filename = item.get('filename', f"qr_{i+1}.png")
        
        if not filename.endswith('.png'):
            filename += '.png'
        
        output_path = os.path.join(output_dir, filename)
        generate(data, output_path)
        generated.append(output_path)
    
    print(f"\nGenerated {len(generated)} QR codes in {output_dir}")
    return generated


def main():
    parser = argparse.ArgumentParser(description='Batch generate QR codes')
    parser.add_argument('input', help='Input CSV or JSON file')
    parser.add_argument('--output-dir', '-o', required=True, help='Output directory')
    parser.add_argument('--data-column', '-d', default='data', help='Data column name (CSV)')
    parser.add_argument('--filename-column', '-f', default='filename', help='Filename column (CSV)')
    args = parser.parse_args()
    
    ext = os.path.splitext(args.input)[1].lower()
    
    if ext == '.csv':
        batch_from_csv(args.input, args.output_dir, args.data_column, args.filename_column)
    elif ext == '.json':
        batch_from_json(args.input, args.output_dir)
    else:
        print(f"Error: Unsupported file format: {ext}. Use CSV or JSON.")


if __name__ == '__main__':
    main()
