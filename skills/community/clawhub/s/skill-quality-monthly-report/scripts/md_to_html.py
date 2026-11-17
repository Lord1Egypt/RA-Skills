#!/usr/bin/env python3
"""
Markdown 转 HTML 转换脚本

功能：将包含 Mermaid 图表的 Markdown 文件转换为 HTML
依赖：mermaid-cli（mmdc）
"""

import subprocess
import sys
import os
import re
from pathlib import Path


def check_dependencies():
    """检查必要的依赖是否已安装"""
    try:
        # 检查 mmdc (mermaid-cli)
        result = subprocess.run(
            ["mmdc", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            print("警告：mmdc (mermaid-cli) 未安装", file=sys.stderr)
            print("建议安装：npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
            return False
        
        print("✓ mmdc (mermaid-cli) 已安装")
        return True
        
    except FileNotFoundError:
        print("警告：mmdc (mermaid-cli) 未安装", file=sys.stderr)
        print("建议安装：npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
        return False


def extract_mermaid_diagrams(content: str) -> list:
    """提取 Markdown 中的 Mermaid 图表代码块"""
    # 匹配 ```mermaid ... ``` 格式的代码块
    pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches


def convert_markdown_to_html_basic(content: str) -> str:
    """将 Markdown 转换为基本 HTML（不依赖外部库）"""
    html = content
    
    # 标题转换
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 加粗
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # 列表
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 表格（简单处理）
    html = re.sub(r'\|', '</td><td>', html)
    html = re.sub(r'^<td>(.*?)</td>$', r'<tr><td>\1</td></tr>', html, flags=re.MULTILINE)
    
    # 代码块（非 Mermaid）
    html = re.sub(r'```(?!mermaid)(.*?)\n(.*?)\n```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    return html


def convert_mermaid_to_svg(mermaid_code: str, index: int) -> str:
    """将 Mermaid 代码转换为 SVG"""
    # 创建临时文件
    temp_mmd = Path(f'/tmp/mermaid_temp_{index}.mmd')
    temp_svg = Path(f'/tmp/mermaid_temp_{index}.svg')
    
    try:
        # 写入 Mermaid 代码
        with open(temp_mmd, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        # 调用 mmdc 转换
        result = subprocess.run(
            ["mmdc", "-i", str(temp_mmd), "-o", str(temp_svg), "-t", "default", "-w", "800"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"警告：Mermaid 图表 {index} 转换失败", file=sys.stderr)
            return f'<div class="mermaid-error">图表渲染失败</div>'
        
        # 读取 SVG 内容
        with open(temp_svg, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        return f'<div class="mermaid-diagram">{svg_content}</div>'
        
    except Exception as e:
        print(f"警告：Mermaid 图表 {index} 转换异常：{e}", file=sys.stderr)
        return f'<div class="mermaid-error">图表渲染异常</div>'
    
    finally:
        # 清理临时文件
        if temp_mmd.exists():
            temp_mmd.unlink()
        if temp_svg.exists():
            temp_svg.unlink()


def generate_html_template(title: str, content: str, styles: str = None) -> str:
    """生成完整的 HTML 文件"""
    if styles is None:
        styles = """
        <style>
            body {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }
            h1, h2, h3 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            table td, table th {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            table th {
                background-color: #3498db;
                color: white;
            }
            .mermaid-diagram {
                margin: 20px 0;
                text-align: center;
            }
            .mermaid-diagram svg {
                max-width: 100%;
                height: auto;
            }
            .report-header {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .section {
                margin: 30px 0;
            }
            strong {
                color: #e74c3c;
            }
        </style>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {styles}
</head>
<body>
{content}
</body>
</html>"""
    
    return html


def convert_markdown_to_html(md_file: str, output_file: str = None) -> str:
    """
    将 Markdown 文件转换为 HTML（含 Mermaid 图表渲染）
    
    参数：
        md_file: Markdown 文件路径
        output_file: 输出 HTML 文件路径（可选，默认与输入文件同名）
    
    返回：
        输出 HTML 文件路径
    """
    md_path = Path(md_file)
    
    if not md_path.exists():
        raise FileNotFoundError(f"文件不存在：{md_file}")
    
    # 确定输出文件路径
    if output_file:
        html_path = Path(output_file)
    else:
        html_path = md_path.with_suffix('.html')
    
    print(f"正在转换：{md_path} → {html_path}")
    
    # 读取 Markdown 内容
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 提取并渲染 Mermaid 图表
    mermaid_diagrams = extract_mermaid_diagrams(md_content)
    
    # 渲染 Mermaid 图表为 SVG
    rendered_diagrams = []
    for i, diagram in enumerate(mermaid_diagrams, 1):
        print(f"  正在渲染 Mermaid 图表 {i}/{len(mermaid_diagrams)}...")
        svg = convert_mermaid_to_svg(diagram, i)
        rendered_diagrams.append(svg)
    
    # 替换 Markdown 中的 Mermaid 代码块为渲染后的 SVG
    html_content = md_content
    diagram_pattern = r'```mermaid\n(.*?)\n```'
    
    def replace_with_svg(match):
        index = len(rendered_diagrams) - len(mermaid_diagrams)
        mermaid_diagrams.pop(0)
        return rendered_diagrams[index]
    
    # 替换所有 Mermaid 代码块
    html_content = re.sub(diagram_pattern, replace_with_svg, html_content, flags=re.DOTALL)
    
    # 转换剩余的 Markdown 为 HTML
    html_content = convert_markdown_to_html_basic(html_content)
    
    # 添加 HTML 模板
    title = md_path.stem
    html_content = generate_html_template(title, html_content)
    
    # 写入 HTML 文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ 转换成功：{html_path}")
    return str(html_path)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Markdown 转 HTML 转换工具（支持 Mermaid 图表）')
    parser.add_argument('input', nargs='?', help='输入 Markdown 文件路径')
    parser.add_argument('-o', '--output', help='输出 HTML 文件路径（可选）')
    parser.add_argument('--check-deps', action='store_true', help='仅检查依赖')
    
    args = parser.parse_args()
    
    if args.check_deps:
        success = check_dependencies()
        sys.exit(0 if success else 1)
    
    if not args.input:
        parser.print_help()
        sys.exit(1)
    
    # 检查依赖（可选）
    check_dependencies()
    
    # 转换文件
    try:
        output_file = convert_markdown_to_html(args.input, args.output)
        print(f"\nHTML 文件已生成：{output_file}")
        print("提示：可在浏览器中打开查看，如需 PDF 可使用浏览器打印功能")
    except Exception as e:
        print(f"\n错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
