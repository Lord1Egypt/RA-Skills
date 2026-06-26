#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
去除 PDF 文件中的水印
用法: python remove_watermark.py <pdf 文件路径> [--output <输出路径>]
"""
from pypdf import PdfReader, PdfWriter
import re
import os
import sys
import json

def remove_watermark(pdf_path, output_path=None):
    """去除 PDF 水印"""
    if not os.path.exists(pdf_path):
        return {'error': f'文件不存在：{pdf_path}'}
    
    # 生成输出路径
    if output_path is None:
        base, ext = os.path.splitext(pdf_path)
        output_path = f"{base}_no_watermark{ext}"
    
    result = {
        'input': pdf_path,
        'output': output_path,
        'success': False
    }
    
    try:
        # 读取 PDF
        reader = PdfReader(pdf_path)
        result['pages'] = len(reader.pages)
        writer = PdfWriter()
        
        # 处理每一页
        for i, page in enumerate(reader.pages):
            page_obj = page.get_object()
            
            # 1. 移除 Resources 中的 Pattern
            if "/Resources" in page_obj:
                res = page_obj["/Resources"]
                if hasattr(res, 'get_object'):
                    res = res.get_object()
                if "/Pattern" in res:
                    del res["/Pattern"]
            
            # 2. 清理内容流中的 Pattern 引用
            if "/Contents" in page_obj:
                contents = page_obj["/Contents"]
                if hasattr(contents, 'get_object'):
                    contents = contents.get_object()
                
                if isinstance(contents, list):
                    for content_obj in contents:
                        if hasattr(content_obj, 'get_object'):
                            content_obj = content_obj.get_object()
                        if hasattr(content_obj, '_data'):
                            data = content_obj._data
                            data = re.sub(rb'/P\d+\s+scn', b'0 g', data)
                            data = re.sub(rb'/P\d+\s+SCN', b'0 G', data)
                            data = re.sub(rb'/P\d+\s+sc', b'0 g', data)
                            data = re.sub(rb'/P\d+\s+G', b'0 G', data)
                            data = re.sub(rb'/P\d+\s+g', b'0 g', data)
                            content_obj._data = data
                elif hasattr(contents, '_data'):
                    data = contents._data
                    data = re.sub(rb'/P\d+\s+scn', b'0 g', data)
                    data = re.sub(rb'/P\d+\s+SCN', b'0 G', data)
                    contents._data = data
            
            writer.add_page(page)
        
        # 保存
        with open(output_path, "wb") as f:
            writer.write(f)
        
        result['success'] = True
        result['output_size'] = os.path.getsize(output_path)
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def verify_result(output_path):
    """验证去水印结果"""
    if not os.path.exists(output_path):
        return {'verified': False, 'error': '输出文件不存在'}
    
    try:
        import fitz
        doc = fitz.open(output_path)
        
        # 检查是否有 Pattern
        has_pattern = False
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_xref = page.xref
            resources = doc.xref_get_key(page_xref, "Resources")
            if resources[0] == "xref":
                res_xref = int(resources[1])
                res_obj = doc.xref_object(res_xref)
                if "/Pattern" in res_obj:
                    has_pattern = True
                    break
        
        doc.close()
        
        return {
            'verified': True,
            'pages': len(doc) if 'doc' in dir() else 0,
            'has_pattern': has_pattern,
            'watermark_removed': not has_pattern
        }
    except Exception as e:
        return {'verified': False, 'error': str(e)}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供 PDF 文件路径'}, ensure_ascii=False))
        return
    
    pdf_path = sys.argv[1]
    output_path = None
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    print(json.dumps({'status': 'start', 'input': pdf_path}, ensure_ascii=False))
    
    # 执行去水印
    result = remove_watermark(pdf_path, output_path)
    print(json.dumps({'status': 'remove_result', **result}, ensure_ascii=False))
    
    # 验证结果
    if result.get('success'):
        verify_result = verify_result(result['output'])
        print(json.dumps({'status': 'verify', **verify_result}, ensure_ascii=False))

if __name__ == '__main__':
    main()
