#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Free Image Gen - 主入口脚本
使用 Gitee AI API 生成免费图片
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from config import Config
from gitee_api import GiteeImageGenerator
from utils import generate_timestamp_filename


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='免费AI图片生成工具 - 使用 Gitee AI API'
    )
    parser.add_argument(
        '--prompt', '-p',
        type=str,
        required=True,
        help='图片生成提示词'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='输出文件路径'
    )
    parser.add_argument(
        '--model', '-m',
        type=str,
        default='Kolors',
        help='使用的模型 (默认: Kolors)'
    )
    parser.add_argument(
        '--count', '-n',
        type=int,
        default=1,
        help='生成图片数量 (默认: 1)'
    )
    parser.add_argument(
        '--upload-cos',
        action='store_true',
        help='上传到腾讯云 COS'
    )
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='配置文件路径 (默认: 自动查找)'
    )
    parser.add_argument(
        '--size', '-s',
        type=str,
        default='1024x1024',
        help='图片尺寸 (默认: 1024x1024)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='JSON 格式输出'
    )
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()
    
    # 加载配置
    config = Config(args.config)
    
    # 初始化生成器
    generator = GiteeImageGenerator(
        api_key=config.get('gitee.api_key'),
        model=args.model or config.get('gitee.model', 'Kolors'),
        cos_config=config.get_cos_config() if args.upload_cos else None
    )
    
    # 生成图片
    print(f"正在生成图片: {args.prompt}")
    
    # 设置输出目录
    output_dir = args.output
    if output_dir is None:
        output_dir = config.get('output.path', './output')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    # 生成图片
    for i in range(args.count):
        try:
            print(f"正在生成第 {i+1}/{args.count} 张图片...")
            
            result = generator.generate(
                prompt=args.prompt,
                output_dir=output_dir,
                upload_to_cos=args.upload_cos
            )
            
            results.append({
                "success": True,
                "index": i + 1,
                "local_path": result.get("local_path"),
                "url": result.get("url"),
                "cos_url": result.get("cos_url")
            })
            
            print(f"[OK] 第 {i+1} 张图片生成成功!")
            
        except Exception as e:
            results.append({
                "success": False,
                "index": i + 1,
                "error": str(e)
            })
            print(f"[FAIL] 第 {i+1} 张图片生成失败: {e}")
    
    # 输出结果
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("\n" + "="*50)
        print("生成完成!")
        print("="*50)
        for r in results:
            if r["success"]:
                print(f"图片 {r['index']}:")
                print(f"  本地路径: {r['local_path']}")
                if r.get("cos_url"):
                    print(f"  COS URL: {r['cos_url']}")
            else:
                print(f"图片 {r['index']}: 失败 - {r['error']}")


if __name__ == '__main__':
    main()
