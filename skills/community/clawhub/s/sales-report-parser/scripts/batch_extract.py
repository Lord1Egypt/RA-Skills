#!/usr/bin/env python3
"""
销售报表图片批量提取工具
一键完成: OCR识别 -> 大模型解析 -> JSON转Excel

使用方式: python batch_extract.py --api_key 你的API密钥 [--image 图片路径或目录]
"""

import argparse
import json
import os
import sys
import time
from typing import List, Optional

# 导入拆分后的模块
from ocr_images import ocr_recognize
from llm_json import chat_with_json
from json_to_excel import json_to_excel


IMAGE_FIELDS = [
    "日期",
    "总销售",
    "产品净销售",
    "现烤面包",
    "袋装面包",
    "软点",
    "西点",
    "中点",
    "蛋糕个数",
    "蛋糕金额",
    "卡劵",
    "交易次数"
]


DEFAULT_PROMPT = """请从以下OCR识别的销售报表文本中提取数据。

请严格按照以下JSON格式输出一个数组，不要添加任何其他内容：
[
  {{"日期": "", "总销售": "", "产品净销售": "", "现烤面包": "", "袋装面包": "", "软点": "", "西点": "", "中点": "", "蛋糕个数": "", "蛋糕金额": "", "卡劵": "", "交易次数": ""}}
]

注意：
1. 日期格式请提取为 YYYY-MM-DD 格式
2. OCR识别可能存在误差，请根据上下文合理推断和修正数据
3. 图片中的所有数据必须完整准确提取，不能遗漏任何一个字段
4. 如果某个字段在文本中找不到，请填写"无"
5. 如果文本只包含1天的数据，就只返回1个对象"""


def get_all_images(path: str) -> List[str]:
    """获取目录下所有图片文件"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    if os.path.isfile(path):
        return [path]
    
    image_files = []
    for file in os.listdir(path):
        ext = os.path.splitext(file)[1].lower()
        if ext in image_extensions:
            image_files.append(os.path.join(path, file))
    
    return sorted(image_files)


def extract_single_image(
    image_path: str,
    api_key: str,
    max_retries: int = 3,
    base_url: str = "https://api.minimaxi.com/v1",
) -> Optional[List[dict]]:
    """单张图片提取"""
    for attempt in range(max_retries):
        try:
            print(f"  第 {attempt + 1} 次尝试...")
            
            # Step 1: OCR 识别
            print(f"  正在进行 OCR 识别...")
            text_lines = ocr_recognize(image_path)
            
            if not text_lines:
                print(f"  × OCR 未能识别出任何文字")
                continue
            
            ocr_text = "\n".join(text_lines)
            print(f"  OCR 识别完成，文字行数: {len(text_lines)}")
            
            # Step 2: 大模型解析
            print(f"  正在调用大模型解析...")
            result = chat_with_json(
                content=ocr_text,
                prompt=DEFAULT_PROMPT,
                api_key=api_key,
                base_url=base_url,
                use_structured_output=False,
            )
            
            if result and isinstance(result, list) and len(result) > 0:
                print(f"  ✓ 成功提取 {len(result)} 条数据")
                return result
            elif result and isinstance(result, dict) and "raw_response" not in result:
                return [result]
            
            print(f"  × 第 {attempt + 1} 次尝试未获取到有效数据")
            
        except Exception as e:
            print(f"  × 第 {attempt + 1} 次尝试出错: {str(e)}")
        
        if attempt < max_retries - 1:
            print(f"  等待 2 秒后重试...")
            time.sleep(2)
    
    return None


def main():
    parser = argparse.ArgumentParser(description='销售报表图片批量提取工具')
    parser.add_argument('--api_key', '-k', required=True, help='MiniMax API 密钥')
    parser.add_argument('--image', '-i', required=True, help='图片文件路径或目录')
    parser.add_argument('--output', '-o', default='output', help='输出文件名（不含扩展名）')
    parser.add_argument('--base_url', default='https://api.minimaxi.com/v1', help='API 地址')
    parser.add_argument('--retries', type=int, default=3, help='最大重试次数')
    
    args = parser.parse_args()
    
    # 获取图片列表
    image_files = get_all_images(args.image)
    if not image_files:
        print(f"未找到图片文件: {args.image}")
        sys.exit(1)
    
    print(f"找到 {len(image_files)} 张图片")
    
    all_data = []
    
    for image_path in image_files:
        image_name = os.path.basename(image_path)
        print(f"\n{'='*40}")
        print(f"正在处理: {image_name}")
        print(f"{'='*40}")
        
        data_list = extract_single_image(
            image_path, 
            args.api_key, 
            max_retries=args.retries,
            base_url=args.base_url,
        )
        
        if data_list:
            all_data.extend(data_list)
            print(f"✓ {image_name} 提取成功，共 {len(data_list)} 条")
        else:
            print(f"✗ {image_name} 提取失败")
    
    print(f"\n{'='*60}")
    print(f"共提取 {len(all_data)} 条数据")
    print(f"{'='*60}")
    
    if len(all_data) > 0:
        # 保存 JSON
        json_path = f"{args.output}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"已保存 JSON: {json_path}")
        
        # 转换为 Excel
        excel_path = f"{args.output}.xlsx"
        json_to_excel(json_path, excel_path)
    else:
        print("没有提取到数据")


if __name__ == "__main__":
    main()
