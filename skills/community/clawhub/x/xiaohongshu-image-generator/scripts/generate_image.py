#!/usr/bin/env python3
"""
小红书配图生成器
根据提示词生成小红书风格的竖版配图

用法:
    python generate_image.py --title "今日分享" --content "每天进步一点点" --tag "📌 今日分享"
    python generate_image.py --prompt "生成一个温暖风格的每日一句卡片"
"""

import argparse
import os
import re
import subprocess
import time
import webbrowser
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import threading

# 默认配置
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 1000
DEFAULT_PORT = 8765

# 配色方案
COLOR_SCHEMES = {
    'purple': {'start': '#667eea', 'end': '#764ba2', 'name': '紫色渐变'},
    'pink': {'start': '#f093fb', 'end': '#f5576c', 'name': '粉色渐变'},
    'blue': {'start': '#4facfe', 'end': '#00f2fe', 'name': '蓝色渐变'},
    'orange': {'start': '#fa709a', 'end': '#fee140', 'name': '橙色渐变'},
    'green': {'start': '#38f9d7', 'end': '#43e97b', 'name': '绿色渐变'},
    'warm': {'start': '#f6d365', 'end': '#fda085', 'name': '暖色渐变'},
    'cool': {'start': '#a18cd1', 'end': '#fbc2eb', 'name': '冷色渐变'},
    'dark': {'start': '#2b5876', 'end': '#4e4376', 'name': '深色渐变'},
}

# 风格模板
STYLES = {
    'default': {
        'border_radius': '32px',
        'shadow': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'title_size': '48px',
        'content_size': '22px',
    },
    'minimal': {
        'border_radius': '16px',
        'shadow': '0 10px 30px -5px rgba(0, 0, 0, 0.1)',
        'title_size': '36px',
        'content_size': '18px',
    },
    'fancy': {
        'border_radius': '48px',
        'shadow': '0 30px 60px -15px rgba(0, 0, 0, 0.3)',
        'title_size': '56px',
        'content_size': '24px',
    },
}

TEMPLATE = '''<!DOCTYPE html>
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
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, {bg_start} 0%, {bg_end} 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            padding: 20px;
        }}
        
        .card {{
            width: 800px;
            height: 1000px;
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: {border_radius};
            box-shadow: {shadow};
            padding: 60px;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        
        .card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
            pointer-events: none;
        }}
        
        .tag {{
            display: inline-block;
            background: linear-gradient(135deg, {bg_start} 0%, {bg_end} 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 1px;
            align-self: flex-start;
            margin-bottom: 24px;
        }}
        
        .title {{
            font-size: {title_size};
            font-weight: 800;
            color: #1a1a2e;
            line-height: 1.2;
            margin-bottom: 24px;
            background: linear-gradient(135deg, #1a1a2e 0%, #4a4a6a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .divider {{
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, {bg_start} 0%, {bg_end} 100%);
            border-radius: 2px;
            margin-bottom: 32px;
        }}
        
        .content {{
            font-size: {content_size};
            color: #4a4a6a;
            line-height: 1.8;
            flex: 1;
        }}
        
        .content p {{
            margin-bottom: 16px;
        }}
        
        .footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
            padding-top: 32px;
            border-top: 1px solid #eee;
        }}
        
        .author {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .avatar {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, {bg_start} 0%, {bg_end} 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
            font-weight: 700;
        }}
        
        .author-info {{
            font-size: 16px;
            color: #1a1a2e;
            font-weight: 600;
        }}
        
        .date {{
            font-size: 14px;
            color: #888;
        }}
        
        .emoji {{
            font-size: 64px;
            position: absolute;
            bottom: 60px;
            right: 60px;
            opacity: 0.3;
        }}
    </style>
</head>
<body>
    <div class="card">
        <span class="tag">{tag}</span>
        <h1 class="title">{title}</h1>
        <div class="divider"></div>
        <div class="content">
            {content_html}
        </div>
        <div class="footer">
            <div class="author">
                <div class="avatar">{author_initial}</div>
                <div class="author-info">
                    <div>{author}</div>
                    <div class="date">{date}</div>
                </div>
            </div>
        </div>
        <div class="emoji">{emoji}</div>
    </div>
</body>
</html>
'''


def parse_prompt(prompt: str) -> dict:
    """从提示词中解析配置"""
    config = {
        'title': '今日分享',
        'content': '分享一些温暖的小确幸',
        'tag': '📌 今日分享',
        'author': '袁佳鹏',
        'color': 'purple',
        'style': 'default',
        'emoji': '💜',
    }
    
    # 解析标题
    title_match = re.search(r'标题[是为：:]([^，,\n]+)', prompt)
    if title_match:
        config['title'] = title_match.group(1).strip()
    
    # 解析内容
    content_match = re.search(r'内容[是为：:]([^，,\n]+)', prompt)
    if content_match:
        config['content'] = content_match.group(1).strip()
    
    # 解析标签
    tag_match = re.search(r'标签[是为：:]([^，,\n]+)', prompt)
    if tag_match:
        config['tag'] = tag_match.group(1).strip()
    
    # 解析配色
    for color_name in COLOR_SCHEMES:
        if color_name in prompt:
            config['color'] = color_name
            break
    
    # 解析风格
    for style_name in STYLES:
        if style_name in prompt:
            config['style'] = style_name
            break
    
    # 解析 emoji
    emoji_match = re.search(r'([\U0001F300-\U0001F9FF])', prompt)
    if emoji_match:
        config['emoji'] = emoji_match.group(1)
    
    return config


def generate_html(config: dict, output_path: str) -> str:
    """生成 HTML 文件"""
    color = COLOR_SCHEMES.get(config.get('color', 'purple'), COLOR_SCHEMES['purple'])
    style = STYLES.get(config.get('style', 'default'), STYLES['default'])
    
    # 格式化内容为 HTML 段落
    content_lines = config.get('content', '').split('\n')
    content_html = ''.join(f'<p>{line}</p>' for line in content_lines if line.strip())
    
    # 作者首字母
    author_initial = config.get('author', 'P')[0]
    
    # 当前日期
    date = datetime.now().strftime('%Y-%m-%d')
    
    html = TEMPLATE.format(
        title=config.get('title', '今日分享'),
        content_html=content_html or '<p>每天进步一点点</p>',
        tag=config.get('tag', '📌 今日分享'),
        author=config.get('author', '袁佳鹏'),
        author_initial=author_initial,
        date=date,
        emoji=config.get('emoji', '💜'),
        bg_start=color['start'],
        bg_end=color['end'],
        border_radius=style['border_radius'],
        shadow=style['shadow'],
        title_size=style['title_size'],
        content_size=style['content_size'],
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path


def start_server(port: int, directory: str) -> HTTPServer:
    """启动 HTTP 服务器"""
    os.chdir(directory)  # 切换到正确的目录
    handler = SimpleHTTPRequestHandler
    server = HTTPServer(('localhost', port), handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print(f"✅ HTTP Server 启动成功: http://localhost:{port}")
    return server


def main():
    parser = argparse.ArgumentParser(description='小红书配图生成器')
    parser.add_argument('--title', '-t', help='卡片标题')
    parser.add_argument('--content', '-c', help='卡片内容（用换行分隔多段）')
    parser.add_argument('--tag', help='标签文字')
    parser.add_argument('--author', '-a', default='袁佳鹏', help='作者名')
    parser.add_argument('--color', choices=list(COLOR_SCHEMES.keys()), default='purple', help='配色方案')
    parser.add_argument('--style', choices=list(STYLES.keys()), default='default', help='风格')
    parser.add_argument('--emoji', help='装饰 emoji')
    parser.add_argument('--prompt', '-p', help='完整提示词（会覆盖其他参数）')
    parser.add_argument('--output', '-o', default='output.html', help='输出文件名')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='HTTP 服务器端口')
    
    args = parser.parse_args()
    
    # 从提示词解析或使用命令行参数
    if args.prompt:
        config = parse_prompt(args.prompt)
    else:
        config = {
            'title': args.title or '今日分享',
            'content': args.content or '每天进步一点点',
            'tag': args.tag or '📌 今日分享',
            'author': args.author,
            'color': args.color,
            'style': args.style,
            'emoji': args.emoji or '💜',
        }
    
    # 生成 HTML
    output_path = os.path.abspath(args.output)
    generate_html(config, output_path)
    print(f"✅ HTML 生成成功: {output_path}")
    
    # 启动服务器
    server = start_server(args.port, os.path.dirname(output_path))
    
    # 打开浏览器
    url = f"http://localhost:{args.port}/{os.path.basename(output_path)}"
    print(f"🌐 打开页面: {url}")
    webbrowser.open(url)
    
    print("\n📝 下一步：")
    print("1. 等待页面加载完成（约 2 秒）")
    print("2. 使用 OpenClaw browser 工具截图:")
    print(f"   browser action=screenshot targetId=<你的tab-id>")
    print("\n🎨 可用配色: " + ", ".join(f"{k}({v['name']})" for k, v in COLOR_SCHEMES.items()))
    print("🎭 可用风格: " + ", ".join(STYLES.keys()))
    
    # 保持服务器运行
    try:
        input("\n按 Enter 停止服务器...")
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
