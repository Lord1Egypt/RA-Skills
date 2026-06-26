#!/usr/bin/env python3
import argparse
import base64
import mimetypes
import os
import re
from bs4 import BeautifulSoup

def inline_local_images(html_path: str, output_path: str = None) -> None:
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML file not found: {html_path}")
        
    html_dir = os.path.dirname(os.path.abspath(html_path))
    
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    images = soup.find_all("img")
    
    inlined_count = 0
    
    for img in images:
        src = img.get("src")
        if not src:
            continue
            
        src = src.strip()
        # 跳过网络图片和已经内联的 base64 图片
        if src.startswith(("http://", "https://", "data:")):
            continue
            
        # 拼接本地图片绝对路径
        img_abs_path = os.path.abspath(os.path.join(html_dir, src))
        
        if not os.path.exists(img_abs_path):
            print(f"Warning: Image file not found at: {img_abs_path}, skipping.")
            continue
            
        # 根据后缀推导 mime type，若无法识别则默认 image/png
        mime_type, _ = mimetypes.guess_type(img_abs_path)
        if not mime_type:
            ext = os.path.splitext(img_abs_path)[1].lower()
            if ext == '.svg':
                mime_type = 'image/svg+xml'
            else:
                mime_type = 'image/png'
                
        try:
            with open(img_abs_path, "rb") as f:
                img_data = f.read()
                base64_data = base64.b64encode(img_data).decode("utf-8")
                data_url = f"data:{mime_type};base64,{base64_data}"
                img["src"] = data_url
                inlined_count += 1
        except Exception as e:
            print(f"Error processing image {img_abs_path}: {e}")
            
    if inlined_count > 0:
        target_path = output_path if output_path else html_path
        # 使用 formatter 写入，保留原始排版
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Successfully inlined {inlined_count} local image(s) in: {target_path}")
    else:
        print("No local images needed inlining.")

def main():
    parser = argparse.ArgumentParser(description="Inline local relative images in HTML as base64 Data URLs.")
    parser.add_argument("--html", required=True, help="Path to the target HTML content file.")
    parser.add_argument("--output", help="Optional path to output the modified HTML. If omitted, overwrites the input HTML in-place.")
    
    args = parser.parse_args()
    
    try:
        inline_local_images(args.html, args.output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()
