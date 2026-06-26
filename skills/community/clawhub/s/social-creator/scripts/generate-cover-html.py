#!/usr/bin/env python3
"""
小红书封面 HTML 生成器
生成 3:4 比例的极简风格视觉页面，适合社交媒体文案展示

优化点：
- 圆角卡片容器，视觉更柔和
- 关键字块级布局，避免窜行
- 互动引导单独一行，与正文分离
- ✅ 移动端完美适配，F12 手机模式无背景缝隙
"""

import argparse
import os
from datetime import datetime

# 预设风格模板
STYLES = {
    "tech": {
        "name": "科技感",
        "bg_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "card_bg": "rgba(255, 255, 255, 0.08)",
        "text_color": "#ffffff",
        "highlight_bg": "rgba(255, 215, 0, 0.25)",
        "highlight_color": "#ffd700",
        "guide_bg": "rgba(255, 255, 255, 0.12)",
        "guide_color": "#ffffff",
        "emoji": "🤖"
    },
    "dark": {
        "name": "深色模式",
        "bg_gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        "card_bg": "rgba(255, 255, 255, 0.05)",
        "text_color": "#ffffff",
        "highlight_bg": "rgba(233, 69, 96, 0.25)",
        "highlight_color": "#e94560",
        "guide_bg": "rgba(233, 69, 96, 0.15)",
        "guide_color": "#ff8a9e",
        "emoji": "🔥"
    },
    "minimal": {
        "name": "简约风",
        "bg_gradient": "linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%)",
        "card_bg": "rgba(255, 255, 255, 0.6)",
        "text_color": "#2d3436",
        "highlight_bg": "rgba(0, 184, 148, 0.15)",
        "highlight_color": "#00b894",
        "guide_bg": "rgba(0, 184, 148, 0.1)",
        "guide_color": "#009174",
        "emoji": "💡"
    },
    "red": {
        "name": "小红书红",
        "bg_gradient": "linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)",
        "card_bg": "rgba(255, 255, 255, 0.12)",
        "text_color": "#ffffff",
        "highlight_bg": "rgba(255, 255, 255, 0.25)",
        "highlight_color": "#ffffff",
        "guide_bg": "rgba(255, 255, 255, 0.18)",
        "guide_color": "#ffffff",
        "emoji": "❤️"
    }
}

def generate_html(text, guide_text=None, highlight_words=None, style="tech", emoji=None):
    """生成 HTML 封面页面 - 移动端完美适配版
    
    Args:
        text: 主文案内容
        guide_text: 互动引导语（单独一行）
        highlight_words: 要高亮的关键字列表
        style: 风格名称
        emoji: 自定义 emoji
    """
    
    style_config = STYLES.get(style, STYLES["tech"])
    
    # 处理关键字高亮 - 使用块级 span 避免窜行
    highlighted_text = text
    if highlight_words:
        for word in highlight_words:
            highlighted_text = highlighted_text.replace(
                word, 
                f'<span class="highlight">{word}</span>'
            )
    
    # 使用提供的 emoji 或风格默认 emoji
    display_emoji = emoji if emoji else style_config["emoji"]
    
    # 互动引导 HTML（如果提供）
    guide_html = ""
    if guide_text:
        guide_html = f'''
        <div class="guide">{guide_text}</div>
'''
    
    # 使用 viewport 单位 + aspect-ratio 实现完美移动端适配
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>笔记封面 - {text[:20]}...</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html, body {{
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
        }}
        
        body {{
            background: {style_config["bg_gradient"]};
            display: flex;
            justify-content: center;
            align-items: center;
            /* 关键：使用 aspect-ratio 保持 3:4 比例 */
            aspect-ratio: 3 / 4;
            /* 防止移动端点击高亮 */
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
        }}
        
        .wrapper {{
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: min(6vw, 60px);
        }}
        
        .container {{
            text-align: center;
            padding: min(6vw, 60px) min(8vw, 80px);
            width: 100%;
            max-width: min(740px, 82vw);
            /* 圆角卡片容器 */
            background: {style_config["card_bg"]};
            border-radius: min(4vw, 40px);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 
                0 min(2vw, 20px) min(6vw, 60px) rgba(0, 0, 0, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            /* 确保内容不溢出 */
            max-height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        
        .emoji {{
            font-size: min(8vw, 72px);
            margin-bottom: min(5vw, 50px);
            display: block;
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
            flex-shrink: 0;
        }}
        
        .text {{
            font-size: min(4.5vw, 42px);
            font-weight: 700;
            color: {style_config["text_color"]};
            line-height: 1.8;
            text-shadow: 0 2px min(1.5vw, 12px) rgba(0, 0, 0, 0.2);
            word-wrap: break-word;
            text-align: center;
            flex-shrink: 0;
        }}
        
        /* 关键字高亮 - 块级显示避免窜行 */
        .highlight {{
            display: inline-block;
            background: {style_config["highlight_bg"]};
            color: {style_config["highlight_color"]};
            padding: min(0.7vw, 6px) min(1.8vw, 16px);
            border-radius: min(1.3vw, 12px);
            font-weight: 800;
            margin: min(0.2vw, 2px) min(0.5vw, 4px);
            white-space: nowrap;
            box-shadow: 0 2px min(0.8vw, 8px) rgba(0, 0, 0, 0.1);
        }}
        
        /* 互动引导 - 单独一行 */
        .guide {{
            margin-top: min(4vw, 40px);
            padding: min(2vw, 20px) min(3.5vw, 32px);
            background: {style_config["guide_bg"]};
            color: {style_config["guide_color"]};
            border-radius: min(2vw, 20px);
            font-size: min(3vw, 28px);
            font-weight: 600;
            display: inline-block;
            box-shadow: 0 min(0.4vw, 4px) min(1.6vw, 16px) rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.08);
            flex-shrink: 0;
        }}
        
        /* 可自定义区域标记 -->
        <!-- 文案内容：修改 .text 中的文字 -->
        <!-- 高亮关键字：修改 .highlight 包裹的内容 -->
        <!-- 互动引导：修改 .guide 中的文字（可选） -->
        <!-- 风格切换：修改 style 参数 (tech/dark/minimal/red) -->
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="container">
            <span class="emoji">{display_emoji}</span>
            <div class="text">{highlighted_text}</div>
            {guide_html}
        </div>
    </div>
</body>
</html>
'''
    
    return html

def main():
    parser = argparse.ArgumentParser(
        description="生成小红书封面 HTML 页面（移动端完美适配版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python generate-cover-html.py --text "你的文案" --guide "在线等！" --highlight "关键字" --style tech
  python generate-cover-html.py -t "文案内容" -g "求大佬说说" -s dark -o output.html

特性:
  ✅ 使用 viewport 单位 + aspect-ratio 实现完美适配
  ✅ F12 手机模式无背景缝隙
  ✅ 电脑浏览器直接截图 or 手机模式截图均可
        """
    )
    
    parser.add_argument(
        "--text", "-t",
        required=True,
        help="文案内容（必填）"
    )
    
    parser.add_argument(
        "--guide", "-g",
        help="互动引导语（单独一行显示，可选）"
    )
    
    parser.add_argument(
        "--highlight", "-hl",
        nargs="+",
        help="要高亮的关键字（可选，多个用空格分隔）"
    )
    
    parser.add_argument(
        "--style", "-s",
        choices=["tech", "dark", "minimal", "red"],
        default="tech",
        help="视觉风格（默认：tech）"
    )
    
    parser.add_argument(
        "--emoji", "-e",
        help="自定义 emoji（可选，默认使用风格默认 emoji）"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="cover.html",
        help="输出文件名（默认：cover.html）"
    )
    
    args = parser.parse_args()
    
    # 生成 HTML
    html_content = generate_html(
        text=args.text,
        guide_text=args.guide,
        highlight_words=args.highlight,
        style=args.style,
        emoji=args.emoji
    )
    
    # 写入文件
    output_path = args.output if args.output.endswith(".html") else f"{args.output}.html"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 打印风格信息
    style_info = STYLES.get(args.style, STYLES["tech"])
    print(f"✅ 封面已生成：{output_path}")
    print(f"🎨 风格：{style_info['name']}")
    print(f"📐 比例：3:4（自适应尺寸）")
    print(f"📱 适配：移动端完美适配（F12 手机模式无背景缝隙）")
    print(f"📦 特性：圆角卡片 + 关键字块级布局 + 互动引导独立")
    print(f"\n📋 使用说明:")
    print(f"   方式 1: 电脑浏览器打开 → F12 → 手机模式 → 截图")
    print(f"   方式 2: 电脑浏览器打开 → 调整窗口为 3:4 → 截图")
    print(f"   方式 3: 手机浏览器打开 → 直接截图")

if __name__ == "__main__":
    main()
