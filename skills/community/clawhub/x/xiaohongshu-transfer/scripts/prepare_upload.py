#!/usr/bin/env python3
"""小红书笔记信息提取"""

from PIL import Image
import os
import sys

def convert_webp_to_jpg(webp_path, jpg_path, quality=95):
    """转换 webp 到 jpg"""
    img = Image.open(webp_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(jpg_path, 'JPEG', quality=quality)
    return jpg_path

def prepare_upload_dir(save_dir, upload_dir="/tmp/openclaw/uploads"):
    """准备上传目录（清空并复制图片）"""
    # 清空上传目录
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            fp = os.path.join(upload_dir, f)
            if os.path.isfile(fp):
                os.remove(fp)
    else:
        os.makedirs(upload_dir)
    
    # 复制图片
    for f in os.listdir(save_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            src = os.path.join(save_dir, f)
            dst = os.path.join(upload_dir, f)
            with open(src, 'rb') as s:
                with open(dst, 'wb') as d:
                    d.write(s.read())
            print(f"复制: {f}")
    
    return upload_dir

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python prepare_upload.py <日记保存目录>")
        sys.exit(1)
    
    save_dir = sys.argv[1]
    upload_dir = prepare_upload_dir(save_dir)
    print(f"✅ 上传目录已准备: {upload_dir}")
    print(f"图片数量: {len(os.listdir(upload_dir))}")