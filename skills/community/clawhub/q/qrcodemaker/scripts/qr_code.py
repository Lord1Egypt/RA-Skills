#!/usr/bin/env python3
"""
QR Code Generator & Decoder
支持：URL / vCard / WIFI 模式生成，颜色美化，嵌入 Logo，解析二维码
依赖：qrcode, pillow
可选（解析功能）：opencv-python
"""

import sys
import os
import argparse
import json

def generate_text(data, output, fg="black", bg="white", logo=None, logo_size=0.25):
    """生成纯文本二维码"""
    import qrcode
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H if logo else qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")
    if logo:
        img = add_logo(img, logo, logo_size)
    img.convert("RGB").save(output)
    print(f"✅ 文本二维码已保存: {output}")

def generate_url(data, output, fg="black", bg="white", logo=None, logo_size=0.25, quiet_zone=True):
    """生成 URL 二维码"""
    import qrcode
    from PIL import Image

    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H if logo else qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=4 if quiet_zone else 0)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")

    if logo:
        img = add_logo(img, logo, logo_size)

    img.convert("RGB").save(output)
    print(f"✅ URL 二维码已保存: {output}")

def generate_vcard(data, output, fg="black", bg="white", logo=None, logo_size=0.25):
    """生成 vCard 二维码"""
    import qrcode
    from PIL import Image

    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H if logo else qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")

    if logo:
        img = add_logo(img, logo, logo_size)

    img.convert("RGB").save(output)
    print(f"✅ vCard 二维码已保存: {output}")

def generate_wifi(ssid, password, hidden, output, fg="black", bg="white", logo=None, logo_size=0.25):
    """生成 WIFI 二维码"""
    import qrcode
    from PIL import Image

    # WIFI:T:WPA;S:<SSID>;P:<PASSWORD>;;
    wifi_str = f"WIFI:T:WPA;S:{ssid};P:{password};{'H:true;' if hidden else ''};;"
    encryption = "WPA" if password else "nopass"

    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H if logo else qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=4)
    qr.add_data(wifi_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")

    if logo:
        img = add_logo(img, logo, logo_size)

    img.convert("RGB").save(output)
    print(f"✅ WIFI 二维码已保存: {output}")

def add_logo(qr_img, logo_path, logo_size=0.25):
    """在二维码中心嵌入 Logo"""
    from PIL import Image as PILImage

    logo = PILImage.open(logo_path).convert("RGBA")
    qr_w, qr_h = qr_img.size

    # Logo 大小：不超过二维码面积的 logo_size
    max_logo_size = int(min(qr_w, qr_h) * logo_size)
    logo.thumbnail((max_logo_size, max_logo_size), PILImage.LANCZOS)

    # 留白：Logo 周围加一圈白色边框
    border = int(max_logo_size * 0.1)
    lw, lh = logo.size
    box_size = max(lw, lh) + border * 2

    box = PILImage.new("RGBA", (box_size, box_size), (255, 255, 255, 255))
    paste_x = (box_size - lw) // 2
    paste_y = (box_size - lh) // 2
    box.paste(logo, (paste_x, paste_y), logo)

    # 居中粘贴到 QR 码
    pos = ((qr_w - box_size) // 2, (qr_h - box_size) // 2)
    qr_img.paste(box, pos, box)
    return qr_img

def decode_qr(image_path):
    """解析二维码内容"""
    try:
        import cv2
        from pyzbar.pyzbar import decode as pyzbar_decode
    except ImportError:
        print("❌ 解析功能需要安装 opencv-python")
        print("   pip install opencv-python")
        return

    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ 无法读取图片: {image_path}")
        return

    decoded = pyzbar_decode(img)
    if not decoded:
        # 尝试 cv2 QRCodeDetector
        detector = cv2.QRCodeDetector()
        data, vertices, _ = detector.detectAndDecode(img)
        if data:
            print(f"📱 {data}")
        else:
            print("❌ 未检测到二维码")
        return

    for obj in decoded:
        print(f"📱 {obj.data.decode('utf-8')}")

def main():
    parser = argparse.ArgumentParser(description="QR Code Generator & Decoder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # 生成 URL
    g_url = sub.add_parser("url", help="生成 URL 二维码")
    g_url.add_argument("data", help="URL 地址")
    g_url.add_argument("-o", "--output", default="qrcode.png", help="输出文件")
    g_url.add_argument("--fg", default="black", help="前景色")
    g_url.add_argument("--bg", default="white", help="背景色")
    g_url.add_argument("--logo", help="Logo 图片路径")
    g_url.add_argument("--logo-size", type=float, default=0.25, help="Logo 大小比例 (0.1-0.3)")
    g_url.add_argument("--no-quiet-zone", action="store_true", help="无边距")

    # 生成 vCard
    g_vcard = sub.add_parser("vcard", help="生成 vCard 二维码")
    g_vcard.add_argument("-n", "--name", required=True, help="姓名")
    g_vcard.add_argument("-t", "--tel", help="电话")
    g_vcard.add_argument("-e", "--email", help="邮箱")
    g_vcard.add_argument("-u", "--url", help="个人网站")
    g_vcard.add_argument("-o", "--output", default="qrcode_vcard.png", help="输出文件")
    g_vcard.add_argument("--fg", default="black", help="前景色")
    g_vcard.add_argument("--bg", default="white", help="背景色")
    g_vcard.add_argument("--logo", help="Logo 图片路径")
    g_vcard.add_argument("--logo-size", type=float, default=0.25, help="Logo 大小比例")

    # 生成 WIFI
    g_wifi = sub.add_parser("wifi", help="生成 WIFI 二维码")
    g_wifi.add_argument("-s", "--ssid", required=True, help="WiFi 名称")
    g_wifi.add_argument("-p", "--password", default="", help="密码（无密码留空）")
    g_wifi.add_argument("--hidden", action="store_true", help="隐藏网络")
    g_wifi.add_argument("-o", "--output", default="qrcode_wifi.png", help="输出文件")
    g_wifi.add_argument("--fg", default="black", help="前景色")
    g_wifi.add_argument("--bg", default="white", help="背景色")
    g_wifi.add_argument("--logo", help="Logo 图片路径")
    g_wifi.add_argument("--logo-size", type=float, default=0.25, help="Logo 大小比例")

    # 生成纯文本
    g_txt = sub.add_parser("text", help="生成纯文本二维码")
    g_txt.add_argument("data", help="任意文本内容")
    g_txt.add_argument("-o", "--output", default="qrcode_text.png", help="输出文件")
    g_txt.add_argument("--fg", default="black", help="前景色")
    g_txt.add_argument("--bg", default="white", help="背景色")
    g_txt.add_argument("--logo", help="Logo 图片路径")
    g_txt.add_argument("--logo-size", type=float, default=0.25, help="Logo 大小比例 (0.1-0.3)")

    # 解析
    g_dec = sub.add_parser("decode", help="解析二维码图片")
    g_dec.add_argument("image", help="二维码图片路径")

    args = parser.parse_args()

    if args.cmd == "text":
        generate_text(args.data, args.output, args.fg, args.bg, args.logo, args.logo_size)
    elif args.cmd == "url":
        generate_url(args.data, args.output, args.fg, args.bg, args.logo, args.logo_size, not args.no_quiet_zone)
    elif args.cmd == "vcard":
        vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{args.name}\n"
        if args.tel: vcard += f"TEL:{args.tel}\n"
        if args.email: vcard += f"EMAIL:{args.email}\n"
        if args.url: vcard += f"URL:{args.url}\n"
        vcard += "END:VCARD"
        generate_vcard(vcard, args.output, args.fg, args.bg, args.logo, args.logo_size)
    elif args.cmd == "wifi":
        generate_wifi(args.ssid, args.password, args.hidden, args.output, args.fg, args.bg, args.logo, args.logo_size)
    elif args.cmd == "decode":
        decode_qr(args.image)

if __name__ == "__main__":
    main()
