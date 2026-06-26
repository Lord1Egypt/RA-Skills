#!/usr/bin/env python3
"""
卫星云图下载脚本（集成 OCR 时间识别）
- 下载云图
- 用 OCR 识别北京时间，格式化为 YYYYMMDD_HHMM
- 将原图压缩至 10MB 以内，以识别到的时间命名（如 20260331_0815.jpg）
- 输出图片路径（供 AI 读取）

依赖：
  - requests
  - pillow
  - pytesseract
  - tesseract-ocr（系统安装，需包含 chi_sim 语言包）
"""

import os
import sys
import platform
import time
import re
from pathlib import Path
from glob import glob

import requests
from PIL import Image
import pytesseract


# ========== 配置 ==========
URL = "https://img.nsmc.org.cn/CLOUDIMAGE/FY4B/AGRI/GCLR/FY4B_REGC_GCLR.JPG"
CACHE_DIR = Path.home() / ".openclaw" / "satellite_cache"
MAX_FILES = 5
MAX_SIZE_MB = 10
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

# OCR 裁剪区域（原图 7800x4900，时间区域左上角）
CROP_BOX = (92, 92, 968, 200)


# ========== 辅助函数 ==========
def get_headers():
    """模拟浏览器请求头"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.nsmc.org.cn/',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }


def ensure_cache_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def download_image(url, save_path):
    """下载图片，带重试"""
    headers = get_headers()
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(resp.content)
                return True
            elif attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"下载失败，HTTP {resp.status_code}", file=sys.stderr)
                return False
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"下载异常: {e}", file=sys.stderr)
                return False
    return False


def ocr_time_from_image(image_path, crop_box=CROP_BOX, black_threshold=50):
    """
    从图片中裁剪指定区域，进行图像预处理（灰度、放大、二值化），
    然后用 Tesseract OCR 识别北京时间，返回格式化的 YYYYMMDD_HHMM。
    """
    try:
        img = Image.open(image_path)
        roi = img.crop(crop_box)

        # 1. 转灰度
        gray = roi.convert('L')

        # 2. 放大 2 倍（提高 OCR 识别率）
        width, height = gray.size
        enlarged = gray.resize((width * 2, height * 2), Image.Resampling.LANCZOS)

        # 3. 二值化处理
        bw = enlarged.point(lambda p: p if p <= black_threshold else 255, 'L')

        # 使用 Tesseract 识别
        text = pytesseract.image_to_string(bw, lang='chi_sim+eng', config='--psm 7')
        text = text.strip()

        # 匹配格式：2026-03-31 08:15 或 2026-03-31 08:15 (BJT)
        match = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})\s+(\d{1,2}):(\d{2})', text)
        if match:
            year, month, day, hour, minute = match.groups()
            formatted = f"{year}{int(month):02d}{int(day):02d}_{int(hour):02d}{int(minute):02d}"
            return formatted
        else:
            print("[OCR] 未能匹配日期时间格式", file=sys.stderr)
            return None
    except Exception as e:
        print(f"[OCR] 处理异常: {e}", file=sys.stderr)
        return None


def compress_image(filepath, max_bytes=MAX_SIZE_BYTES):
    """压缩图片至指定大小以内"""
    size = os.path.getsize(filepath)
    if size <= max_bytes:
        return filepath

    try:
        img = Image.open(filepath)
        # 转换为 RGB（JPEG 不支持透明通道）
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb = Image.new('RGB', img.size, (255, 255, 255))
            rgb.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 尝试降低质量
        quality = 95
        step = 5
        temp_path = filepath.with_suffix('.tmp.jpg')
        while quality >= 10:
            img.save(temp_path, 'JPEG', quality=quality, optimize=True)
            if temp_path.stat().st_size <= max_bytes:
                os.replace(temp_path, filepath)
                return filepath
            quality -= step

        # 若质量已到最低，则缩小尺寸
        width, height = img.size
        scale = 0.9
        while scale > 0.3:
            new_w = int(width * scale)
            new_h = int(height * scale)
            resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            resized.save(temp_path, 'JPEG', quality=70, optimize=True)
            if temp_path.stat().st_size <= max_bytes:
                os.replace(temp_path, filepath)
                return filepath
            scale -= 0.05

        # 放弃压缩
        if temp_path.exists():
            temp_path.unlink()
        print("警告: 无法压缩至 10MB 以内，将使用原图", file=sys.stderr)
        return filepath
    except Exception as e:
        print(f"压缩失败: {e}", file=sys.stderr)
        return filepath


def clean_old_files():
    """删除旧文件，保留最新 MAX_FILES 张"""
    files = sorted(glob(str(CACHE_DIR / "*.jpg")))
    if len(files) > MAX_FILES:
        for old in files[:-MAX_FILES]:
            os.remove(old)


def main():
    ensure_cache_dir()

    # 1. 下载到临时文件
    tmp_path = CACHE_DIR / "temp_download.jpg"
    if not download_image(URL, tmp_path):
        print("ERROR: 下载失败", file=sys.stderr)
        sys.exit(1)

    # 2. OCR 识别时间
    time_str = ocr_time_from_image(tmp_path)
    if time_str:
        final_name = f"{time_str}.jpg"
    else:
        # 回退到时间戳
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        final_name = f"satellite_{timestamp}.jpg"

    final_path = CACHE_DIR / final_name

    # 3. 移动临时文件到最终路径
    if final_path.exists():
        final_path.unlink()
    os.rename(tmp_path, final_path)

    # 4. 压缩图片
    compress_image(final_path)

    # 5. 清理旧文件
    clean_old_files()

    # 6. 输出图片路径（供 AI 读取）
    print(str(final_path))


if __name__ == "__main__":
    main()
