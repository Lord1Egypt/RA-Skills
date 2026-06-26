#!/usr/bin/env python3
"""
OCR 文字提取模块
优先使用编译好的 Swift CLI 工具（macOS Vision），失败则降级到 pytesseract，
都不可用则返回空字符串。
"""

import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OCR_BINARY = os.path.join(SCRIPT_DIR, "ocr_tool")  # 编译后的二进制


def extract_text(image_path: str) -> str:
    """
    从图片中提取文字。
    尝试顺序: Swift Vision CLI → pytesseract → 空字符串
    """
    text = _try_swift_ocr(image_path)
    if text is not None:
        return text

    text = _try_pytesseract(image_path)
    if text is not None:
        return text

    return ""


def _try_swift_ocr(image_path: str):
    """调用编译好的 Swift OCR 二进制"""
    if not os.path.isfile(OCR_BINARY):
        return None
    try:
        result = subprocess.run(
            [OCR_BINARY, image_path],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def _try_pytesseract(image_path: str):
    """用 pytesseract 做备选 OCR"""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        return pytesseract.image_to_string(img, lang="chi_sim+eng").strip()
    except Exception:
        return None


def compile_swift_ocr():
    """编译 Swift OCR 工具（setup 时调用一次）"""
    swift_src = os.path.join(SCRIPT_DIR, "ocr_tool.swift")
    if not os.path.isfile(swift_src):
        return False
    try:
        result = subprocess.run(
            ["swiftc", "-O", "-o", OCR_BINARY, swift_src],
            capture_output=True, text=True, timeout=120,
        )
        return result.returncode == 0
    except Exception:
        return False


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(extract_text(sys.argv[1]))
    else:
        print("用法: python ocr_processor.py <image_path>")
