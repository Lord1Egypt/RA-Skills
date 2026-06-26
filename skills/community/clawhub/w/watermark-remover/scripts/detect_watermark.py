#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检测 PDF 文件中的水印
用法: python detect_watermark.py <pdf 文件路径> [--output-dir <输出目录>]
"""
import fitz
import os
import sys
import json

def detect_watermark(pdf_path, output_dir=None):
    """检测 PDF 中的水印"""
    if not os.path.exists(pdf_path):
        return {'error': f'文件不存在：{pdf_path}'}
    
    if output_dir is None:
        output_dir = os.path.dirname(pdf_path)
    
    result = {
        'file': pdf_path,
        'watermark_found': False,
        'watermarks': [],
        'preview_images': []
    }
    
    try:
        doc = fitz.open(pdf_path)
        result['pages'] = len(doc)
        
        # 检查所有对象
        for xref in range(1, doc.xref_length()):
            try:
                obj_type = doc.xref_get_key(xref, "Type")
                subtype = doc.xref_get_key(xref, "Subtype")
                
                if "Image" in str(subtype):
                    width = doc.xref_get_key(xref, "Width")
                    height = doc.xref_get_key(xref, "Height")
                    
                    if isinstance(width, tuple) and isinstance(height, tuple):
                        w, h = width[1], height[1]
                        
                        # 检测可能的水印图像（较大的背景图）
                        if w > 300 and h > 200:
                            result['watermark_found'] = True
                            watermark_info = {
                                'type': 'image',
                                'xref': xref,
                                'width': w,
                                'height': h
                            }
                            result['watermarks'].append(watermark_info)
                            
                            # 提取并保存水印图像
                            try:
                                image = doc.extract_image(xref)
                                if image:
                                    preview_path = os.path.join(
                                        output_dir, 
                                        f'watermark_preview_xref{xref}.{image["ext"]}'
                                    )
                                    with open(preview_path, 'wb') as f:
                                        f.write(image['image'])
                                    result['preview_images'].append(preview_path)
                            except Exception as e:
                                pass
                
                # 检查 Pattern 对象
                if "Pattern" in str(obj_type):
                    result['watermark_found'] = True
                    result['watermarks'].append({
                        'type': 'pattern',
                        'xref': xref
                    })
                    
            except Exception:
                continue
        
        # 检查每页的 Resources
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_xref = page.xref
            resources = doc.xref_get_key(page_xref, "Resources")
            
            if resources[0] == "xref":
                res_xref = int(resources[1])
                res_obj = doc.xref_object(res_xref)
                
                if "/Pattern" in res_obj:
                    result['watermark_found'] = True
                    if not any(w.get('type') == 'pattern' for w in result['watermarks']):
                        result['watermarks'].append({
                            'type': 'pattern_resource',
                            'page': page_num + 1
                        })
        
        doc.close()
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供 PDF 文件路径'}, ensure_ascii=False))
        return
    
    pdf_path = sys.argv[1]
    output_dir = None
    
    if '--output-dir' in sys.argv:
        idx = sys.argv.index('--output-dir')
        if idx + 1 < len(sys.argv):
            output_dir = sys.argv[idx + 1]
    
    result = detect_watermark(pdf_path, output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
