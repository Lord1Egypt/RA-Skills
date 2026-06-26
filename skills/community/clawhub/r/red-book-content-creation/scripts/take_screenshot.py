#!/usr/bin/env python3
"""
小红书内容截图工具
将 HTML 页面截取为多张图片（封面 + 内容区块）
"""

import imgkit
import argparse
import os
import sys

def take_screenshot(input_html, output_prefix="output", width=680):
    """截取 HTML 页面为多张图片"""
    
    options = {
        'width': width,
        'format': 'png',
        'quality': 90,
    }
    
    # 读取 HTML 获取内容高度
    with open(input_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 计算预估高度（简单估算）
    # 实际使用时建议手动指定截取区域
    
    outputs = []
    
    # 1. 截取封面（前800px）
    options_cover = {
        'width': width,
        'height': 800,
        'format': 'png',
        'quality': 90,
        'crop-h': 800,
        'crop-y': 0,
    }
    
    cover_output = f"{output_prefix}_cover.png"
    try:
        imgkit.from_file(input_html, cover_output, options=options_cover)
        outputs.append(cover_output)
        print(f"✅ 封面已保存: {cover_output}")
    except Exception as e:
        print(f"❌ 封面截图失败: {e}", file=sys.stderr)
    
    # 2. 截取内容区块（每500px一个区块）
    content_height = 3000  # 预估内容高度
    chunk_size = 600
    offset = 400  # 跳过封面区域
    
    chunk_num = 1
    while offset < content_height:
        options_chunk = {
            'width': width,
            'format': 'png',
            'quality': 90,
            'crop-h': chunk_size,
            'crop-y': offset,
        }
        
        chunk_output = f"{output_prefix}_part{chunk_num}.png"
        try:
            imgkit.from_file(input_html, chunk_output, options=options_chunk)
            outputs.append(chunk_output)
            print(f"✅ 内容区块{chunk_num}已保存: {chunk_output}")
            chunk_num += 1
        except Exception as e:
            print(f"❌ 内容区块{chunk_num}截图失败: {e}", file=sys.stderr)
            break
        
        offset += chunk_size
    
    return outputs

def main():
    parser = argparse.ArgumentParser(description='小红书内容截图工具')
    parser.add_argument('--input', '-i', required=True, help='输入 HTML 文件路径')
    parser.add_argument('--output', '-o', default='output', help='输出文件前缀')
    parser.add_argument('--width', '-w', type=int, default=680, help='图片宽度')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    outputs = take_screenshot(args.input, args.output, args.width)
    
    if outputs:
        print(f"\n📸 共生成 {len(outputs)} 张图片")
        for o in outputs:
            print(f"   - {o}")

if __name__ == '__main__':
    main()
