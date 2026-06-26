#!/usr/bin/env python3
"""夸克扫描王 - 图像增强服务入口"""
from common import run_ocr, save_image_from_result

if __name__ == "__main__":
    run_ocr(result_handler=save_image_from_result)
