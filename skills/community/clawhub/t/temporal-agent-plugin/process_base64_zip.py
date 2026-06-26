#!/usr/bin/env python3
"""
处理Base64编码的ZIP包
"""

import base64
import zipfile
import io
import os

def process_base64_zip(base64_file, output_dir):
    """
    处理Base64编码的ZIP包
    
    Args:
        base64_file: Base64编码文件路径
        output_dir: 输出目录
    """
    print(f"读取Base64文件: {base64_file}")
    
    # 读取Base64文件内容
    with open(base64_file, 'r', encoding='utf-8') as f:
        base64_content = f.read()
    
    print(f"Base64内容长度: {len(base64_content)} 字符")
    
    try:
        # 清理Base64内容（移除空格、换行等）
        base64_content = base64_content.strip()
        # 添加适当的填充
        padding = len(base64_content) % 4
        if padding:
            base64_content += '=' * (4 - padding)
        
        # 解码Base64内容
        print("解码Base64内容...")
        decoded_content = base64.b64decode(base64_content)
        print(f"解码后长度: {len(decoded_content)} 字节")
        
        # 检查是否为有效的ZIP文件
        print("验证ZIP文件...")
        with io.BytesIO(decoded_content) as zip_buffer:
            if zipfile.is_zipfile(zip_buffer):
                print("是有效的ZIP文件")
                
                # 创建输出目录
                os.makedirs(output_dir, exist_ok=True)
                
                # 提取ZIP内容
                print(f"提取ZIP内容到: {output_dir}")
                with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                    zip_ref.extractall(output_dir)
                    print(f"成功提取 {len(zip_ref.namelist())} 个文件")
                    for file in zip_ref.namelist():
                        print(f"  - {file}")
            else:
                print("不是有效的ZIP文件")
                # 创建输出目录
                os.makedirs(output_dir, exist_ok=True)
                # 保存解码后的内容到文件，以便进一步分析
                raw_output = os.path.join(output_dir, "decoded_raw.bin")
                with open(raw_output, 'wb') as f:
                    f.write(decoded_content)
                print(f"已保存解码后的原始内容到: {raw_output}")
                
    except Exception as e:
        print(f"处理出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    base64_file = "C:\\Users\\Administrator\\Desktop\\trae-self-evolve-72h.zip"
    output_dir = "C:\\Users\\Administrator\\Desktop\\trae-self-evolve-72h"
    
    process_base64_zip(base64_file, output_dir)
