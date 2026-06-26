#!/usr/bin/env python3
"""
download.py — 从指定URL下载中考真题文件
用法: python3 download.py <url> <output_path> [--referer <url>]
返回: JSON格式的下载结果
"""

import sys
import os
import json
import urllib.request
import urllib.error
import ssl

def detect_format(file_path):
    """通过magic bytes检测文件格式"""
    try:
        with open(file_path, "rb") as f:
            header = f.read(16)
        
        if header[:4] == b'%PDF':
            return "pdf"
        elif header[:4] == b'PK\x03\x04':
            return "zip"  # could be docx too
        elif header[:6] == b'Rar!\x1a\x07':
            return "rar"
        elif header[:8] == b'\x89PNG\r\n\x1a\n':
            return "png"
        elif header[:2] == b'\xff\xd8':
            return "jpeg"
        elif header[:4] == b'\xd0\xcf\x11\xe0':
            return "ole2"
        else:
            # Check for HTML
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(500).lower()
                    if '<html' in content or '<!doctype' in content:
                        return "html"
            except:
                pass
            return "unknown"
    except:
        return "unknown"


def download_file(url, output_path, referer=""):
    """下载文件并返回结果"""
    result = {
        "success": False,
        "url": url,
        "output": output_path
    }
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 构建请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if referer:
        headers["Referer"] = referer
    
    req = urllib.request.Request(url, headers=headers)
    
    # 创建SSL上下文（macOS Python可能缺少根证书，直接跳过验证）
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        result["success"] = True
    except urllib.error.HTTPError as e:
        result["error"] = f"HTTP {e.code}"
        result["success"] = False
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    except urllib.error.URLError as e:
        result["error"] = str(e.reason)
        result["success"] = False
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    
    # 检查文件大小
    file_size = os.path.getsize(output_path)
    result["file_size"] = file_size
    
    if file_size < 1024:
        result["warning"] = f"文件过小 ({file_size} bytes)，可能是HTML重定向页面"
    
    # 检测文件格式
    fmt = detect_format(output_path)
    result["format"] = fmt
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "error": "用法: download.py <url> <output_path> [--referer <url>]"
        }, ensure_ascii=False))
        sys.exit(1)
    
    url = sys.argv[1]
    output_path = sys.argv[2]
    referer = ""
    
    if len(sys.argv) > 3 and sys.argv[3] == "--referer" and len(sys.argv) > 4:
        referer = sys.argv[4]
    
    result = download_file(url, output_path, referer)
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
