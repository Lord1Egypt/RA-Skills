#!/usr/bin/env python3
import argparse
import base64
import mimetypes
import os
import sys

def convert_to_base64(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
        
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        ext = os.path.splitext(image_path)[1].lower()
        if ext == '.svg':
            mime_type = 'image/svg+xml'
        else:
            mime_type = 'image/png'
            
    with open(image_path, "rb") as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"

def main():
    parser = argparse.ArgumentParser(description="Convert cover or any image to base64 Data URL.")
    parser.add_argument("image", help="Path to the image file.")
    parser.add_argument("--output", help="Optional path to write the base64 string to. If omitted, prints to stdout.")
    
    args = parser.parse_args()
    
    try:
        data_url = convert_to_base64(args.image)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(data_url)
            print(f"Successfully converted and saved base64 to {args.output}")
        else:
            print(data_url)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
