#!/usr/bin/env python3
"""
PDF导出脚本
将Markdown周报导出为PDF
"""

import argparse
import os
import subprocess
import tempfile


def markdown_to_pdf(markdown_content: str, output_path: str, title: str = "周报") -> dict:
    """使用pandoc将Markdown转换为PDF"""
    try:
        # 检查pandoc是否安装
        result = subprocess.run(['which', 'pandoc'], capture_output=True)
        if result.returncode != 0:
            return {"success": False, "error": "请先安装 pandoc: brew install pandoc"}
        
        # 创建临时Markdown文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(markdown_content)
            md_path = f.name
        
        try:
            # 构建pandoc命令
            cmd = [
                'pandoc',
                md_path,
                '-o', output_path,
                '--pdf-engine=xelatex',
                '-V', 'mainfont=SF Pro Text',
                '-V', 'geometry:margin=1in',
                '--standalone'
            ]
            
            # 执行转换
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {"success": True, "path": output_path}
            else:
                return {"success": False, "error": result.stderr}
                
        finally:
            # 清理临时文件
            if os.path.exists(md_path):
                os.unlink(md_path)
                
    except Exception as e:
        return {"success": False, "error": str(e)}


def markdown_to_html(markdown_content: str, title: str = "周报") -> str:
    """Markdown转HTML（无需pandoc）"""
    import re
    
    html = markdown_content
    
    # 标题
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 粗体/斜体
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 代码
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # 链接
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # 列表
    lines = html.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        if line.startswith('- '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{line[2:]}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)
    if in_list:
        new_lines.append('</ul>')
    html = '\n'.join(new_lines)
    
    # 段落
    html = html.replace('\n\n', '</p><p>')
    
    # 完整HTML
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
            line-height: 1.6;
        }}
        h1 {{ color: #1a1a1a; border-bottom: 2px solid #7CB342; padding-bottom: 10px; }}
        h2 {{ color: #333; margin-top: 30px; }}
        h3 {{ color: #555; }}
        code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: 'SF Mono', monospace; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 8px 0; }}
        a {{ color: #7CB342; }}
        p {{ margin: 15px 0; }}
    </style>
</head>
<body>
    {html}
</body>
</html>'''
    
    return full_html


def export_html(markdown_content: str, output_path: str, title: str = "周报") -> dict:
    """导出为HTML"""
    try:
        html = markdown_to_html(markdown_content, title)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return {"success": True, "path": output_path}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="导出周报为PDF/HTML")
    parser.add_argument("--input", required=True, help="Markdown文件路径")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--format", choices=["pdf", "html"], default="html", help="输出格式")
    parser.add_argument("--title", default="周报", help="文档标题")
    
    args = parser.parse_args()
    
    # 读取Markdown
    with open(args.input, encoding='utf-8') as f:
        content = f.read()
    
    # 转换
    if args.format == "pdf":
        result = markdown_to_pdf(content, args.output, args.title)
    else:
        result = export_html(content, args.output, args.title)
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
