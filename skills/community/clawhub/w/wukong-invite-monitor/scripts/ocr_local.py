#!/usr/bin/env python3
"""
本地 OCR 识别模块 - 零 token 消耗
使用 Tesseract OCR 进行文字识别
"""

import os
import sys
import subprocess
import shutil


def check_tesseract():
    """检查 Tesseract 是否安装"""
    return shutil.which('tesseract') is not None


def get_tesseract_version():
    """获取 Tesseract 版本"""
    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=5
        )
        return result.stdout.split('\n')[0] if result.returncode == 0 else None
    except:
        return None


def check_tesseract_langs():
    """检查已安装的语言包"""
    try:
        result = subprocess.run(
            ['tesseract', '--list-langs'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=5
        )
        if result.returncode == 0:
            langs = result.stdout.strip().split('\n')[1:]
            return [l.strip() for l in langs if l.strip()]
    except:
        pass
    return []


def ocr_with_tesseract(image_path, lang='chi_sim'):
    """
    使用 Tesseract 进行 OCR 识别
    
    Args:
        image_path: 图片路径
        lang: 语言包
    
    Returns:
        str: 识别的文字
    """
    try:
        output_base = image_path + '.ocr'
        
        result = subprocess.run(
            ['tesseract', image_path, output_base, '-l', lang, '--psm', '6'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output_file = output_base + '.txt'
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                try:
                    os.remove(output_file)
                except:
                    pass
                return text
            else:
                return f"[错误] {result.stderr}"
        else:
            return f"[错误] {result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "[超时]"
    except Exception as e:
        return f"[异常] {str(e)}"


def ocr_image(image_path):
    """
    OCR 识别统一接口
    
    Returns:
        dict: {
            "success": bool,
            "text": str,
            "engine": str
        }
    """
    if not os.path.exists(image_path):
        return {"success": False, "text": "", "engine": "none", "error": "文件不存在"}
    
    if check_tesseract():
        version = get_tesseract_version()
        langs = check_tesseract_langs()
        
        # 选择语言
        lang = 'chi_sim' if 'chi_sim' in langs or 'chs' in langs else 'eng'
        
        text = ocr_with_tesseract(image_path, lang)
        
        return {
            "success": True,
            "text": text,
            "engine": f"Tesseract ({version})",
            "language": lang
        }
    else:
        # 降级：简单分析
        try:
            size = os.path.getsize(image_path) / 1024
            return {
                "success": True,
                "text": f"[图片 {size:.1f} KB，请手动查看]",
                "engine": "Simple (Tesseract not installed)"
            }
        except:
            return {"success": True, "text": "[无法分析]", "engine": "none"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 ocr_local.py <图片路径>")
        sys.exit(1)
    
    result = ocr_image(sys.argv[1])
    print(f"引擎：{result.get('engine', '未知')}")
    print(f"识别内容：{result.get('text', '[无]')}")
