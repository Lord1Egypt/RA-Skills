#!/usr/bin/env python3
"""
Resume Generator CLI
命令行入口
"""

import argparse
import json
import sys
from pathlib import Path

from generator import ResumeGenerator, generate_resume


def load_json_file(filepath: str) -> dict:
    """从JSON文件加载数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件不存在: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"错误: JSON格式错误: {filepath}")
        sys.exit(1)


def save_file(content: str, filepath: str):
    """保存内容到文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已保存: {filepath}")
    except Exception as e:
        print(f"错误: 保存失败: {e}")
        sys.exit(1)


def cmd_generate(args):
    """生成简历命令"""
    # 加载数据
    if args.input:
        data = load_json_file(args.input)
    else:
        # 从命令行参数构建数据
        data = {
            'name': args.name or '未命名',
            'email': args.email or '',
            'phone': args.phone or '',
            'location': args.location or ''
        }
    
    # 生成简历
    generator = ResumeGenerator(data)
    
    if args.format == 'markdown':
        output = generator.generate_markdown(args.template)
    elif args.format == 'html':
        output = generator.generate_html(args.template)
    else:
        print(f"错误: 不支持的格式: {args.format}")
        sys.exit(1)
    
    # 输出
    if args.output:
        save_file(output, args.output)
    else:
        print(output)


def cmd_export(args):
    """导出简历命令"""
    # 读取输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 文件不存在: {args.input}")
        sys.exit(1)
    
    content = input_path.read_text(encoding='utf-8')
    
    # 如果是markdown，转为html
    if input_path.suffix in ['.md', '.markdown']:
        if args.format == 'html':
            # 从markdown生成HTML
            # 简单处理：创建完整HTML文档
            html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>简历导出</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
           max-width: 800px; margin: 40px auto; padding: 20px; color: #333; }}
    h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
    h2 {{ color: #34495e; margin-top: 30px; }}
    h3 {{ color: #7f8c8d; }}
    pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    ul {{ line-height: 1.8; }}
    blockquote {{ border-left: 4px solid #3498db; margin: 0; padding-left: 15px; color: #666; }}
  </style>
</head>
<body>
  <pre>{content}</pre>
</body>
</html>'''
            output = html
        elif args.format == 'pdf':
            print("提示: PDF导出需要安装pdfkit和wkhtmltopdf")
            print("请使用HTML导出后浏览器打印为PDF")
            output = content
        else:
            output = content
    else:
        output = content
    
    # 保存
    save_file(output, args.output)


def cmd_optimize(args):
    """优化简历命令"""
    # 读取简历
    resume_path = Path(args.resume)
    if not resume_path.exists():
        print(f"错误: 文件不存在: {args.resume}")
        sys.exit(1)
    resume_content = resume_path.read_text(encoding='utf-8')
    
    # 读取JD
    jd_path = Path(args.jd)
    if not jd_path.exists():
        print(f"错误: 文件不存在: {args.jd}")
        sys.exit(1)
    jd_content = jd_path.read_text(encoding='utf-8')
    
    # 生成优化建议
    # 简单实现：从resume提取信息
    data = {'name': '优化目标', 'email': '', 'skills': []}
    
    # 尝试从markdown提取技能
    for line in resume_content.split('\n'):
        if '## 技术' in line or '## 技能' in line:
            continue
        if line.startswith('- '):
            # 简单提取
            data['skills'].append({'category': '检测到', 'items': [line[2:]]})
    
    generator = ResumeGenerator(data)
    suggestions = generator.optimize_for_jd(jd_content)
    
    if args.output:
        save_file(suggestions, args.output)
    else:
        print(suggestions)


def main():
    parser = argparse.ArgumentParser(
        description='Resume Generator - AI简历生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # generate命令
    gen_parser = subparsers.add_parser('generate', help='生成简历')
    gen_parser.add_argument('--name', '-n', help='姓名')
    gen_parser.add_argument('--email', '-e', help='邮箱')
    gen_parser.add_argument('--phone', '-p', help='电话')
    gen_parser.add_argument('--location', '-l', help='位置')
    gen_parser.add_argument('--input', '-i', help='JSON数据文件')
    gen_parser.add_argument('--template', '-t', choices=['simple', 'classic', 'modern'],
                           default='simple', help='模板类型')
    gen_parser.add_argument('--format', '-f', choices=['markdown', 'html'],
                           default='markdown', help='输出格式')
    gen_parser.add_argument('--output', '-o', help='输出文件')
    gen_parser.set_defaults(func=cmd_generate)
    
    # export命令
    export_parser = subparsers.add_parser('export', help='导出简历')
    export_parser.add_argument('--input', '-i', required=True, help='输入文件')
    export_parser.add_argument('--format', '-f', choices=['markdown', 'html', 'pdf'],
                              default='html', help='输出格式')
    export_parser.add_argument('--output', '-o', required=True, help='输出文件')
    export_parser.set_defaults(func=cmd_export)
    
    # optimize命令
    opt_parser = subparsers.add_parser('optimize', help='优化简历')
    opt_parser.add_argument('--resume', '-r', required=True, help='简历文件')
    opt_parser.add_argument('--jd', '-j', required=True, help='岗位描述文件')
    opt_parser.add_argument('--output', '-o', help='输出文件')
    opt_parser.set_defaults(func=cmd_optimize)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()