#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连环画图片压缩脚本
将源文件夹中的所有 JPG/PNG 图片缩放+降质量后保存到目标文件夹，
同时复制并清理 HTML 文件，用于发布。

功能（匹配 skill v1.5 要求）：
  1. 递归压缩所有 .jpg/.jpeg/.png 为统一 .jpg（最长边 max_size，quality）。
  2. 复制 HTML 时，把其中的 .png/.PNG 图片引用改写为 .jpg（避免压缩后扩展名不一致）。
  3. 默认只保留 HTML 实际引用的图片文件（--keep-unreferenced 可关闭），
     不进发布版的无关文件（如 characters/ 三视图、风格参考图）。

用法:
    python compress.py <源文件夹> <目标文件夹> [--max-size 1024] [--quality 70]
                       [--keep-unreferenced]

默认参数:
    max_size = 1024  (最长边最大像素)
    quality  = 70    (JPEG质量 1-100)
"""

import os
import re
import sys
import argparse
import shutil
from PIL import Image


IMG_EXTS = ('.jpg', '.jpeg', '.png', '.PNG', '.JPG', '.JPEG')


def _rewrite_html_refs(html_text):
    """把 HTML 中的 .png/.PNG 资源引用改写为 .jpg。"""
    def _repl(m):
        pre, ext, post = m.group(1), m.group(2), m.group(3)
        return pre + '.jpg' + post
    return re.sub(r'(src="[^"]*?)\.(png|PNG)(")', _repl, html_text)


def _collect_referenced(src_dir, dst_html_paths):
    """从复制后的 HTML 中收集被引用的相对路径集合（含 .html 自身）。"""
    referenced = set()
    for html_path in dst_html_paths:
        try:
            text = open(html_path, 'r', encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        for m in re.finditer(r'src="([^"]+)"', text):
            ref = m.group(1)
            if ref.startswith(('http://', 'https://', 'data:', '#')):
                continue
            # 归一化：去掉查询串/锚点，统一正斜杠
            ref = ref.split('?')[0].split('#')[0]
            ref = ref.replace('\\', '/').lstrip('/')
            referenced.add(ref)
    return referenced


def compress_images(src_dir, dst_dir, max_size=1024, quality=70,
                    keep_unreferenced=False):
    """压缩源目录中所有图片，复制并清理 HTML，输出到目标目录。"""
    os.makedirs(dst_dir, exist_ok=True)

    count = 0
    total_in = 0
    total_out = 0
    dst_html_paths = []

    abs_dst = os.path.abspath(dst_dir)
    for root, dirs, files in os.walk(src_dir):
        # 跳过目标目录自身：dst 可能在 src 内部，若提前建好会被 walk 再次遍历，
        # 导致发布目录嵌套（comic_publish/comic_publish）与重复压缩。
        dirs[:] = [d for d in dirs
                   if os.path.abspath(os.path.join(root, d)) != abs_dst]
        for f in files:
            src_path = os.path.join(root, f)
            rel_path = os.path.relpath(src_path, src_dir)

            # ---- HTML 文件：复制并改写 .png 引用 ----
            if f.lower().endswith('.html'):
                dst_path = os.path.join(dst_dir, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                try:
                    text = open(src_path, 'r', encoding='utf-8',
                                errors='ignore').read()
                    text = _rewrite_html_refs(text)
                    with open(dst_path, 'w', encoding='utf-8') as fh:
                        fh.write(text)
                    dst_html_paths.append(dst_path)
                except Exception as e:
                    print(f"⚠️  HTML 复制失败 {f}: {e}")
                continue

            # ---- 图片文件：压缩为 .jpg ----
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                dst_path = os.path.join(dst_dir, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)

                img = Image.open(src_path)
                w, h = img.size
                if max(w, h) > max_size:
                    ratio = max_size / max(w, h)
                    img = img.resize((int(w * ratio), int(h * ratio)),
                                     Image.LANCZOS)
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')

                dst_path_jpg = os.path.splitext(dst_path)[0] + '.jpg'
                img.save(dst_path_jpg, 'JPEG', quality=quality, optimize=True)

                count += 1
                total_in += os.path.getsize(src_path)
                total_out += os.path.getsize(dst_path_jpg)

    # ---- 清理未引用文件（v1.5 强制）----
    if not keep_unreferenced and dst_html_paths:
        referenced = _collect_referenced(src_dir, dst_html_paths)
        removed = 0
        for root, dirs, files in os.walk(dst_dir):
            for f in files:
                if f.lower().endswith('.html'):
                    continue
                rel = os.path.relpath(os.path.join(root, f), dst_dir)
                rel_norm = rel.replace('\\', '/')
                # 被引用（用不带扩展名的键匹配，因引用可能来自改写前的 .png）
                base = os.path.splitext(rel_norm)[0]
                if rel_norm in referenced or (base + '.jpg') in referenced:
                    continue
                try:
                    os.remove(os.path.join(root, f))
                    removed += 1
                except OSError:
                    pass
        if removed:
            print(f"已清理未引用文件: {removed} 个")

    # ---- 统计 ----
    print(f"压缩完成: {count} 张图片")
    print(f"原始大小: {total_in / 1024 / 1024:.1f} MB")
    print(f"压缩大小: {total_out / 1024 / 1024:.1f} MB")
    if total_in:
        print(f"压缩率:   {total_out / total_in * 100:.0f}%")

    final_size = sum(
        os.path.getsize(os.path.join(r, f))
        for r, ds, fs in os.walk(dst_dir) for f in fs
    )
    print(f"发布文件夹总大小: {final_size / 1024 / 1024:.1f} MB")

    if final_size > 20 * 1024 * 1024:
        print("\n⚠️  警告: 总大小超过20MB!")
        print("建议: 降低 --max-size 到 800，或降低 --quality 到 60")
    return final_size


def main():
    parser = argparse.ArgumentParser(description='连环画图片压缩发布工具')
    parser.add_argument('src', help='源文件夹路径')
    parser.add_argument('dst', help='目标文件夹路径')
    parser.add_argument('--max-size', type=int, default=1024,
                        help='图片最长边最大像素 (默认: 1024)')
    parser.add_argument('--quality', type=int, default=70,
                        help='JPEG质量 1-100 (默认: 70)')
    parser.add_argument('--keep-unreferenced', action='store_true',
                        help='保留未被 HTML 引用的文件（默认会清理）')
    args = parser.parse_args()

    compress_images(args.src, args.dst, args.max_size, args.quality,
                    args.keep_unreferenced)


if __name__ == '__main__':
    main()
