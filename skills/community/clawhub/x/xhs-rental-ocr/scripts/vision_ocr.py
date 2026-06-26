#!/usr/bin/env python3
"""
Apple Vision OCR 模块
使用 macOS Vision 框架进行图片文字识别
"""

import os
import sys
from PIL import Image

try:
    from AppKit import NSData
    from Vision import VNImageRequestHandler, VNRecognizeTextRequest, VNRequestTextRecognitionLevelAccurate
except ImportError:
    print("❌ 错误：需要安装 pyobjc-framework-Vision 和 pyobjc-framework-Cocoa")
    print("   运行：pip3 install pyobjc-framework-Vision pyobjc-framework-Cocoa")
    sys.exit(1)


def ocr_image(image_path: str, languages: str = "zh-Hans,en-US"):
    """
    使用 Apple Vision 进行 OCR
    
    Args:
        image_path: 图片路径
        languages: 识别语言，逗号分隔（默认：zh-Hans,en-US）
    
    Returns:
        识别到的文本列表
    """
    try:
        # 加载图片
        image_data = NSData.dataWithContentsOfFile_(image_path)
        if not image_data:
            print(f"   错误：无法读取图片 - {image_path}")
            return []
        
        # 创建请求处理器
        handler = VNImageRequestHandler.alloc().initWithData_options_(image_data, {})
        
        # 创建文本识别请求
        request = VNRecognizeTextRequest.alloc().init()
        
        # 设置识别语言
        lang_list = [l.strip() for l in languages.split(",")]
        request.setRecognitionLanguages_(lang_list)
        request.setUsesLanguageCorrection_(True)
        request.setRecognitionLevel_(VNRequestTextRecognitionLevelAccurate)
        
        # 执行识别
        handler.performRequests_error_([request], None)
        
        # 获取结果
        results = request.results()
        
        if not results or len(results) == 0:
            return []
        
        # 处理结果
        texts = []
        for obs in results:
            text = obs.text()
            confidence = obs.confidence()
            if text and confidence > 0.3:
                texts.append(text.strip())
        
        return texts
        
    except Exception as e:
        print(f"   错误：{str(e)}")
        return []


def slice_image(image_path: str, num_slices: int):
    """
    将长图裁切成 N 份
    
    Args:
        image_path: 图片路径
        num_slices: 裁切份数
    
    Returns:
        裁切后的图片路径列表
    """
    try:
        img = Image.open(image_path)
        width, height = img.size
        piece_height = height // num_slices
        
        pieces = []
        base_dir = os.path.dirname(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        for i in range(num_slices):
            top = i * piece_height
            bottom = (i + 1) * piece_height if i < num_slices - 1 else height
            
            box = (0, top, width, bottom)
            piece = img.crop(box)
            
            piece_path = os.path.join(base_dir, f"{base_name}_part{i+1}.jpg")
            piece.save(piece_path, 'JPEG', quality=90)
            pieces.append(piece_path)
        
        return pieces
        
    except Exception as e:
        print(f"   错误：裁切失败 - {str(e)}")
        return [image_path]
