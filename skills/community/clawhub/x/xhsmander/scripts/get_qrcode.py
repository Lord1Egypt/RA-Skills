"""
获取登录二维码并保存为图片
输出：保存路径 + 过期时间
"""
import sys
import os
import base64
import json
sys.path.insert(0, os.path.dirname(__file__))

from mcp_dispatcher import call_tool, check_running

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
QR_OUTPUT = os.path.join(SCRIPT_DIR, "login_qrcode.png")

if __name__ == "__main__":
    if not check_running():
        print("MCP service not running")
        sys.exit(1)
    
    result = call_tool("get_login_qrcode")
    
    image_data = None
    expire_time = None
    
    for item in result:
        if item.get("type") == "text":
            # 提取过期时间
            text = item["text"]
            print(text)
        elif item.get("type") == "image":
            image_data = item.get("data")
    
    if image_data:
        img_bytes = base64.b64decode(image_data)
        with open(QR_OUTPUT, "wb") as f:
            f.write(img_bytes)
        print(f"QR code saved to: {QR_OUTPUT}")
        print(f"Image size: {len(img_bytes)} bytes")
    else:
        print("No QR code in response")
        sys.exit(1)
