#!/usr/bin/env python3
"""
HEIC 图片转换脚本

将 HEIC/HEIF 格式图片转换为 JPEG 格式，确保各种大模型都能正常识别。
支持单文件和批量转换。

使用方式:
    python convert_heic.py <input_path> [output_dir]

参数:
    input_path  - HEIC 文件路径，或包含 HEIC 文件的目录
    output_dir  - 输出目录（可选，默认在原文件同目录生成）

依赖:
    - macOS: 无需额外依赖，使用系统自带的 sips 命令
    - Linux/Windows: 需要安装 pillow-heif (pip install pillow-heif Pillow)

示例:
    python convert_heic.py photo.HEIC
    python convert_heic.py ./photos/ ./converted/
"""

import os
import sys
import glob
import subprocess
import platform


def is_heic(filepath: str) -> bool:
    """判断文件是否为 HEIC/HEIF 格式"""
    ext = os.path.splitext(filepath)[1].lower()
    return ext in ('.heic', '.heif')


def convert_with_sips(input_path: str, output_path: str) -> bool:
    """macOS: 使用系统自带的 sips 命令转换"""
    try:
        subprocess.run(
            ['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '90',
             input_path, '--out', output_path],
            check=True, capture_output=True, text=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_with_pillow(input_path: str, output_path: str) -> bool:
    """跨平台: 使用 pillow-heif + Pillow 转换"""
    try:
        from PIL import Image
        try:
            import pillow_heif
            pillow_heif.register_heif_opener()
        except ImportError:
            pass
        img = Image.open(input_path)
        img.save(output_path, 'JPEG', quality=90)
        return True
    except Exception:
        return False


def convert_with_imagemagick(input_path: str, output_path: str) -> bool:
    """备选: 使用 ImageMagick 转换"""
    for cmd in ['magick', 'convert']:
        try:
            subprocess.run(
                [cmd, input_path, '-quality', '90', output_path],
                check=True, capture_output=True, text=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return False


def convert_heic(input_path: str, output_path: str) -> str:
    """
    转换 HEIC 文件为 JPEG，自动选择可用的转换方式。

    返回: 转换后的文件路径，失败则返回空字符串
    """
    if not os.path.exists(input_path):
        print(f"错误: 文件不存在 - {input_path}")
        return ""

    if not is_heic(input_path):
        print(f"跳过: 非 HEIC 文件 - {input_path}")
        return input_path

    # macOS 优先用 sips（无需安装任何依赖）
    if platform.system() == 'Darwin':
        if convert_with_sips(input_path, output_path):
            print(f"✓ [sips] {input_path} -> {output_path}")
            return output_path

    # 尝试 pillow-heif
    if convert_with_pillow(input_path, output_path):
        print(f"✓ [pillow] {input_path} -> {output_path}")
        return output_path

    # 尝试 ImageMagick
    if convert_with_imagemagick(input_path, output_path):
        print(f"✓ [imagemagick] {input_path} -> {output_path}")
        return output_path

    print(f"✗ 转换失败: {input_path}")
    print("  请安装以下任一工具:")
    print("  - macOS: 系统自带 sips（应该已可用）")
    print("  - pip install pillow-heif Pillow")
    print("  - brew install imagemagick")
    return ""


def batch_convert(input_path: str, output_dir: str = "") -> list[str]:
    """
    批量转换 HEIC 文件。

    input_path: 单个文件或目录
    output_dir: 输出目录（空则在原文件同目录）

    返回: 成功转换的文件路径列表
    """
    results = []

    if os.path.isfile(input_path):
        files = [input_path]
    elif os.path.isdir(input_path):
        files = glob.glob(os.path.join(input_path, '*.HEIC'))
        files += glob.glob(os.path.join(input_path, '*.heic'))
        files += glob.glob(os.path.join(input_path, '*.HEIF'))
        files += glob.glob(os.path.join(input_path, '*.heif'))
    else:
        print(f"错误: 路径不存在 - {input_path}")
        return results

    if not files:
        print("未找到 HEIC/HEIF 文件")
        return results

    for f in sorted(set(files)):
        basename = os.path.splitext(os.path.basename(f))[0] + '.jpg'
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            out = os.path.join(output_dir, basename)
        else:
            out = os.path.join(os.path.dirname(f), basename)

        result = convert_heic(f, out)
        if result:
            results.append(result)

    print(f"\n转换完成: {len(results)}/{len(files)} 成功")
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ""
    results = batch_convert(input_path, output_dir)
    sys.exit(0 if results else 1)
