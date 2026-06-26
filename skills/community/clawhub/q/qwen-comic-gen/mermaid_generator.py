#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid 图表生成器
用于将 Mermaid 语法转换为 PNG/SVG 图片

使用方法:
    python mermaid_generator.py input.mmd output.png
    python mermaid_generator.py --text "graph TD; A-->B" output.svg
    python mermaid_generator.py --help
"""

import argparse
import subprocess
import sys
import os
import tempfile
from pathlib import Path

# 默认配置
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_THEME = 'default'
DEFAULT_BACKGROUND = 'transparent'

# Mermaid 主题列表
THEMES = [
    'default', 'forest', 'dark', 'neutral', 'base',
    'supernova', 'halloween', 'cyberpunk'
]

def check_mmdc_installed():
    """检查 mmdc 是否已安装"""
    try:
        result = subprocess.run(
            ['mmdc', '--version'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return True, result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return False, str(e)

def generate_mermaid(input_file, output_file, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, 
                     theme=DEFAULT_THEME, background=DEFAULT_BACKGROUND):
    """
    使用 mmdc 生成 Mermaid 图表
    
    参数:
        input_file: 输入的 .mmd 文件路径
        output_file: 输出文件路径（.png 或 .svg）
        width: 图片宽度（像素）
        height: 图片高度（像素）
        theme: 主题名称
        background: 背景颜色（transparent 或颜色代码）
    
    返回:
        (success, message)
    """
    cmd = [
        'mmdc',
        '-i', str(input_file),
        '-o', str(output_file),
        '-w', str(width),
        '-H', str(height),
        '-t', theme
    ]
    
    if background != 'transparent':
        cmd.extend(['-b', background])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            shell=True,
            cwd=os.path.dirname(os.path.abspath(input_file)) or '.'
        )
        return True, f"成功生成：{output_file}"
    except subprocess.CalledProcessError as e:
        return False, f"生成失败：{e.stderr}"
    except FileNotFoundError:
        return False, "错误：未找到 mmdc 命令，请先安装 @mermaid-js/mermaid-cli"

def generate_from_text(text, output_file, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                       theme=DEFAULT_THEME, background=DEFAULT_BACKGROUND):
    """
    从文本直接生成 Mermaid 图表
    
    参数:
        text: Mermaid 语法的文本
        output_file: 输出文件路径
        width: 图片宽度
        height: 图片高度
        theme: 主题名称
        background: 背景颜色
    
    返回:
        (success, message)
    """
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as f:
        f.write(text)
        temp_file = f.name
    
    try:
        success, message = generate_mermaid(
            temp_file, output_file, width, height, theme, background
        )
        return success, message
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def main():
    parser = argparse.ArgumentParser(
        description='Mermaid 图表生成器 - 将 Mermaid 语法转换为 PNG/SVG 图片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python mermaid_generator.py input.mmd output.png
  python mermaid_generator.py --text "graph TD; A-->B" output.svg
  python mermaid_generator.py input.mmd output.png -w 1000 -H 800 -t dark
  python mermaid_generator.py --check

主题选项:
  default, forest, dark, neutral, base, supernova, halloween, cyberpunk
        """
    )
    
    parser.add_argument('input', nargs='?', help='输入的 .mmd 文件路径')
    parser.add_argument('output', nargs='?', help='输出文件路径（.png 或 .svg）')
    parser.add_argument('--text', '-t', help='Mermaid 语法文本（替代输入文件）')
    parser.add_argument('--width', '-w', type=int, default=DEFAULT_WIDTH,
                        help=f'图片宽度（默认：{DEFAULT_WIDTH}）')
    parser.add_argument('--height', '-H', type=int, default=DEFAULT_HEIGHT,
                        help=f'图片高度（默认：{DEFAULT_HEIGHT}）')
    parser.add_argument('--theme', type=str, default=DEFAULT_THEME,
                        choices=THEMES, help=f'主题（默认：{DEFAULT_THEME}）')
    parser.add_argument('--background', '-b', type=str, default=DEFAULT_BACKGROUND,
                        help=f'背景颜色（默认：{DEFAULT_BACKGROUND}）')
    parser.add_argument('--check', action='store_true',
                        help='检查 mmdc 是否已安装')
    
    args = parser.parse_args()
    
    # 检查模式
    if args.check:
        installed, version = check_mmdc_installed()
        if installed:
            print(f"[OK] mmdc 已安装，版本：{version}")
            sys.exit(0)
        else:
            print(f"[ERROR] mmdc 未安装：{version}")
            print("\n安装命令：npm install -g @mermaid-js/mermaid-cli")
            sys.exit(1)
    
    # 验证参数
    if not args.output:
        parser.error("必须指定输出文件路径")
    
    if not args.input and not args.text:
        parser.error("必须指定输入文件或 --text 参数")
    
    if args.input and args.text:
        parser.error("不能同时指定输入文件和 --text 参数")
    
    # 生成图表
    if args.text:
        print(f"[INFO] 从文本生成图表...")
        success, message = generate_from_text(
            args.text, args.output,
            width=args.width, height=args.height,
            theme=args.theme, background=args.background
        )
    else:
        if not os.path.exists(args.input):
            print(f"[ERROR] 输入文件不存在：{args.input}")
            sys.exit(1)
        print(f"[INFO] 从文件生成图表：{args.input}")
        success, message = generate_mermaid(
            args.input, args.output,
            width=args.width, height=args.height,
            theme=args.theme, background=args.background
        )
    
    print(message)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
