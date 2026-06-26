"""
compress_img.py - 压缩封面图以满足微信永久素材上传限制

用法:
  python compress_img.py <输入图片路径> <输出图片路径> [quality]

默认 quality=85，输出 JPEG 格式
微信永久素材限制 2MB，目标压到 500KB 以内以保证上传速度
"""
from PIL import Image
import os
import sys


def compress_cover(input_path, output_path, quality=85, max_size=500 * 1024):
    """
    压缩封面图：保持原分辨率，用 JPEG quality 控制文件大小。
    微信永久素材限制 2MB，公众号封面图固定横版 1280×720，目标 < 500KB。
    """
    img = Image.open(input_path).convert("RGB")
    orig_w, orig_h = img.width, img.height

    # 先用指定 quality 保存
    img.save(output_path, "JPEG", quality=quality, optimize=True)
    size = os.path.getsize(output_path)
    print(f"输入:  {os.path.getsize(input_path):,} bytes ({orig_w}x{orig_h})")
    print(f"JPEG q={quality}: {size:,} bytes ({img.width}x{img.height})")

    # 如果还是太大，逐步降 quality
    q = quality
    while size > max_size and q > 30:
        q -= 10
        img.save(output_path, "JPEG", quality=q, optimize=True)
        size = os.path.getsize(output_path)
        print(f"  重试 q={q}: {size:,} bytes")

    # 如果 quality 降到太低还太大，才缩分辨率
    if size > max_size:
        scale = 0.8
        while size > max_size and scale > 0.3:
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
            img_small = img.resize((new_w, new_h), Image.LANCZOS)
            img_small.save(output_path, "JPEG", quality=70, optimize=True)
            size = os.path.getsize(output_path)
            print(f"  缩放 {new_w}x{new_h}: {size:,} bytes")
            scale -= 0.1

    final_size = os.path.getsize(output_path)
    final_img = Image.open(output_path)
    print(f"最终: {final_size:,} bytes, {final_img.width}x{final_img.height}, quality={q}")

    # 检查分辨率
    if final_img.width != orig_w or final_img.height != orig_h:
        print(f"⚠️  注意：图片被缩放了（{orig_w}x{orig_h} → {final_img.width}x{final_img.height}）")

    return final_size


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 85

    compress_cover(input_path, output_path, quality)
