#!/usr/bin/env python3
"""
qr-code-toolkit/scripts/decode_qr.py
二维码/条形码识别器
"""

import argparse
import os
import sys

import cv2
from pyzbar.pyzbar import decode
from PIL import Image


def decode_qr(image_path: str):
    """Decode QR code or barcode from image"""
    
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}")
        return None
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        # Try with PIL
        try:
            pil_img = Image.open(image_path)
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception:
            print(f"Error: Cannot read image: {image_path}")
            return None
    
    # Decode
    decoded_objects = decode(img)
    
    if not decoded_objects:
        print(f"No QR code or barcode found in: {image_path}")
        return None
    
    results = []
    for i, obj in enumerate(decoded_objects):
        result = {
            'index': i + 1,
            'data': obj.data.decode('utf-8'),
            'type': obj.type,
            'rect': {
                'left': obj.rect.left,
                'top': obj.rect.top,
                'width': obj.rect.width,
                'height': obj.rect.height,
            },
        }
        results.append(result)
        print(f"[{i+1}] Type: {obj.type}")
        print(f"    Data: {obj.data.decode('utf-8')}")
        print(f"    Position: ({obj.rect.left}, {obj.rect.top}, {obj.rect.width}x{obj.rect.height})")
    
    return results


def decode_batch(directory: str, output_path: str = None):
    """Decode all images in a directory"""
    import json
    
    image_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    files = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in image_exts]
    
    all_results = {}
    for f in sorted(files):
        path = os.path.join(directory, f)
        results = decode_qr(path)
        if results:
            all_results[f] = results
    
    print(f"\nDecoded {len(all_results)}/{len(files)} images")
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"Results saved: {output_path}")
    
    return all_results


def main():
    parser = argparse.ArgumentParser(description='Decode QR code or barcode')
    parser.add_argument('input', help='Image file or directory')
    parser.add_argument('--batch', '-b', action='store_true', help='Batch process directory')
    parser.add_argument('--output', '-o', help='Output JSON file (for batch)')
    args = parser.parse_args()
    
    if args.batch or os.path.isdir(args.input):
        decode_batch(args.input, args.output)
    else:
        decode_qr(args.input)


if __name__ == '__main__':
    main()
