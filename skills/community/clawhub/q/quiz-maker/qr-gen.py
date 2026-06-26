#!/usr/bin/env python3
"""本地二维码生成脚本"""
import sys, os, subprocess
from datetime import datetime

try:
    import qrcode
except ImportError:
    print("正在安装 qrcode...", file=sys.stderr)
    subprocess.run([sys.executable, "-m", "pip", "install", "qrcode", "pillow", "-q"])
    import qrcode

if len(sys.argv) < 2:
    print("用法: python3 qr-gen.py <url> [输出路径]", file=sys.stderr)
    sys.exit(1)

url = sys.argv[1]

if len(sys.argv) > 2:
    output_path = sys.argv[2]
else:
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_path = os.path.expanduser(f"~/.openclaw/canvas/quiz_qr_local_{timestamp}.png")

img = qrcode.make(url)
img.save(output_path)
print(f"二维码已保存: {output_path}")
