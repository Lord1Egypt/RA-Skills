#!/usr/bin/env python3
"""
Structured PDF Export Helper Script

快速生成美化表格 PDF 的辅助脚本。
✅ 安全特性：使用用户主目录 + 环境变量，权限检查，避免 /tmp

使用示例：
  python3 generate_table_pdf.py --title "技能清单"
  python3 generate_table_pdf.py --title "技能清单" --workdir ~/.openclaw/workspace
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

def generate_html_template(title="表格", subtitle="OpenClaw 结构化数据可视化"):
    """生成基础 HTML 模板"""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border: none;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background-color: #f8f9ff;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        .tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }}
        .status-ok {{
            background: #d4edda;
            color: #155724;
        }}
        .status-no {{
            background: #f8d7da;
            color: #721c24;
        }}
        .row-alt {{
            background-color: #f9f9f9;
        }}
        hr {{
            margin: 30px 0;
            border: none;
            border-top: 2px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 {title}</h1>
        <p class="subtitle">{subtitle}</p>
        <!-- 在这里插入表格内容 -->
    </div>
</body>
</html>'''

def setup_temp_dir(work_dir):
    """
    设置临时目录，权限检查，返回临时目录路径。
    
    Args:
        work_dir: 工作目录路径
        
    Returns:
        临时目录路径（字符串）
        
    Raises:
        OSError: 无法创建目录或权限不足
    """
    work_path = Path(work_dir).expanduser().resolve()
    
    # 检查工作目录存在性
    if not work_path.exists():
        try:
            work_path.mkdir(parents=True, mode=0o755)
            print(f"✅ 创建工作目录: {work_path}")
        except OSError as e:
            print(f"❌ 无法创建工作目录 {work_path}: {e}")
            raise
    
    # 检查工作目录可写性
    if not os.access(work_path, os.W_OK):
        print(f"❌ 工作目录无写权限: {work_path}")
        raise PermissionError(f"无写权限: {work_path}")
    
    # 创建专用临时目录
    temp_dir = work_path / ".pdf-export-tmp"
    try:
        temp_dir.mkdir(parents=True, mode=0o700, exist_ok=True)
        print(f"✅ 临时目录已设置: {temp_dir}")
    except OSError as e:
        print(f"❌ 无法创建临时目录 {temp_dir}: {e}")
        raise
    
    return str(temp_dir)

def main():
    parser = argparse.ArgumentParser(
        description="生成美化表格 PDF 的辅助工具（安全版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 使用默认工作目录（$OPENCLAW_WORKSPACE 或 ~/.openclaw/workspace）
  python3 generate_table_pdf.py --title "技能清单"
  
  # 自定义工作目录
  python3 generate_table_pdf.py --title "技能清单" --workdir /my/custom/path
  
  # 完整流程：
  python3 generate_table_pdf.py --title "表格对比" --output my-table.html
  # → 编辑 ~/.openclaw/workspace/.pdf-export-tmp/my-table.html
  # → 启动服务器并打开浏览器
  # → 生成 PDF 并复制到工作目录
  # → 发送给用户并清理
        """
    )
    
    parser.add_argument('--title', default='表格', help='表格标题（必需）')
    parser.add_argument('--subtitle', default='OpenClaw 结构化数据可视化', help='副标题')
    parser.add_argument('--output', default=None, help='输出 HTML 文件名（可选，默认自动生成）')
    parser.add_argument('--workdir', default=None, help='工作目录（可选，默认 $OPENCLAW_WORKSPACE 或 ~/.openclaw/workspace）')
    
    args = parser.parse_args()
    
    # 确定工作目录
    if args.workdir:
        work_dir = args.workdir
    else:
        # 优先使用环境变量
        work_dir = os.environ.get('OPENCLAW_WORKSPACE')
        if not work_dir:
            # 回退到默认位置
            work_dir = os.path.expanduser("~/.openclaw/workspace")
    
    print(f"📁 工作目录: {work_dir}")
    
    try:
        # 设置临时目录并进行权限检查
        temp_dir = setup_temp_dir(work_dir)
    except (OSError, PermissionError) as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)
    
    # 自动生成文件名（如果未指定）
    if args.output is None:
        today = datetime.now().strftime('%Y-%m-%d')
        args.output = f"table-{today}.html"
    else:
        # 确保文件名不包含路径分隔符（安全检查）
        if "/" in args.output or "\\" in args.output:
            print(f"❌ 文件名不能包含路径: {args.output}")
            sys.exit(1)
    
    # 生成 HTML
    html_content = generate_html_template(args.title, args.subtitle)
    
    # 写入到临时目录
    output_path = Path(temp_dir) / args.output
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML 文件已生成: {output_path}")
    except IOError as e:
        print(f"❌ 无法写入文件 {output_path}: {e}")
        sys.exit(1)
    
    # 打印后续步骤
    print(f"\n📋 后续步骤：")
    print(f"1. 编辑 HTML 文件，在 <!-- 在这里插入表格内容 --> 处添加表格")
    print(f"   编辑器: nano {output_path}")
    print(f"\n2. 启动服务器:")
    print(f"   cd {temp_dir} && python3 -m http.server 8888 > server.log 2>&1 &")
    print(f"\n3. 打开浏览器:")
    print(f"   openclaw browser open http://localhost:8888/{args.output}")
    print(f"\n4. 生成 PDF:")
    print(f"   openclaw browser pdf [targetId]")
    print(f"\n5. 复制并重命名到工作目录:")
    print(f"   cp /path/to/generated.pdf {work_dir}/[中文名]-{datetime.now().strftime('%Y-%m-%d')}.pdf")
    print(f"\n6. 发送给用户:")
    print(f"   message send --filePath \"{work_dir}/[中文名]-{datetime.now().strftime('%Y-%m-%d')}.pdf\"")
    print(f"\n7. 清理临时文件:")
    print(f"   rm -rf {temp_dir}")
    print(f"\n⚠️  重要：完成所有步骤后，务必清理临时目录")

if __name__ == '__main__':
    main()
