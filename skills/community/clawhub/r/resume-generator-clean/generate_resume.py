#!/usr/bin/env python3
"""
Resume Generator CLI
Main entry point for the resume-generator skill.
"""

import os
import sys
import argparse

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from resume_pdf import ResumePDFGenerator, generate_from_yaml


def main():
    parser = argparse.ArgumentParser(
        description='Resume Generator - Professional PDF resume creator with Chinese support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from config file
  python generate_resume.py -c resume.yaml -o output.pdf
  
  # Use classic theme
  python generate_resume.py -c resume.yaml -o output.pdf -t classic
  
  # Interactive mode (coming soon)
  python generate_resume.py --interactive
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Path to YAML configuration file'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output PDF file path'
    )
    
    parser.add_argument(
        '--theme', '-t',
        choices=['modern_blue', 'classic'],
        default='modern_blue',
        help='Visual theme (default: modern_blue)'
    )
    
    parser.add_argument(
        '--font',
        help='Path to custom Chinese font file'
    )
    
    parser.add_argument(
        '--example',
        action='store_true',
        help='Generate example resume'
    )
    
    args = parser.parse_args()
    
    if args.example:
        # Generate example resume
        print("Generating example resume...")
        gen = ResumePDFGenerator(theme=args.theme, font_path=args.font)
        
        gen.add_header(
            name="张三",
            title="高级工程师 · 某某科技有限公司",
            phone="138-0000-0000",
            email="example@example.com",
            address="北京市海淀区示例路1号"
        )
        
        gen.add_section("工作经历", [
            {
                "title": "高级工程师",
                "org": "某某科技有限公司",
                "period": "2020-至今",
                "detail": "软件开发 · 系统架构设计 · 人工智能应用"
            },
            {
                "title": "软件工程师",
                "org": "某某科技有限公司",
                "period": "2015-2020",
                "detail": "后端开发 · 数据库设计 · 系统优化"
            }
        ])
        
        gen.add_section("教育背景", [
            {
                "title": "计算机科学硕士",
                "org": "某某大学",
                "period": "2010-2013",
                "detail": "导师：某某教授"
            },
            {
                "title": "软件工程学士",
                "org": "某某大学",
                "period": "2006-2010",
                "detail": None
            }
        ])
        
        output_path = args.output or "example_resume.pdf"
        gen.save(output_path)
        print(f"\nExample resume created: {output_path}")
        return
    
    if not args.config or not args.output:
        parser.print_help()
        sys.exit(1)
    
    # Generate from config
    try:
        generate_from_yaml(args.config, args.output, args.theme)
        print(f"\n✓ Resume generated successfully!")
        print(f"  Config: {args.config}")
        print(f"  Output: {args.output}")
        print(f"  Theme: {args.theme}")
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
