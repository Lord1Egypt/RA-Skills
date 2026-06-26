"""
QR Code Generator - 本地生成二维码并保存到文件。

用法:
  python scripts/generate.py --data <文本内容> --output <保存路径> [选项]

选项:
  --size              图片尺寸，默认 400x400
  --format            输出格式 png|svg，默认 png
  --error-correction  纠错级别 L|M|Q|H，默认 M
  --border            边框宽度，默认 2

输出 JSON:
  {"file": "..."}
  错误时: {"error": "..."}
"""

import sys
import json
import os
import argparse

ECC_MAP = {"L": 1, "M": 0, "Q": 3, "H": 2}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="二维码文本内容")
    parser.add_argument("--output", required=True, help="本地保存路径")
    parser.add_argument("--size", default="400x400")
    parser.add_argument("--format", default="png", dest="fmt", choices=["png", "svg"])
    parser.add_argument("--error-correction", default="M", dest="ecc", choices=["L", "M", "Q", "H"])
    parser.add_argument("--border", type=int, default=2)
    args = parser.parse_args()

    output_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    try:
        import qrcode
        import qrcode.image.svg

        size_int = int(args.size.split("x")[0])

        qr = qrcode.QRCode(
            error_correction=ECC_MAP.get(args.ecc, 0),
            box_size=max(1, size_int // 41),
            border=args.border,
        )
        qr.add_data(args.data)
        qr.make(fit=True)

        if args.fmt == "svg":
            img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
            img.save(output_path)
        else:
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((size_int, size_int))
            img.save(output_path)

        print(json.dumps({"file": output_path}, ensure_ascii=False))
    except ImportError:
        print(json.dumps({"error": "本地 qrcode 库未安装，请先执行 pip install qrcode Pillow"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"生成失败: {e}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
