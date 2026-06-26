# -*- coding: utf-8 -*-
"""
微信公众号文章排版主题
"""

THEMES = {
    # ========== 橙心 ==========
    "橙心": {
        "title": 'font-size: 24px; font-weight: bold; color: #FF7F00; text-align: center; margin: 20px 0;',
        "title_color": "#FF7F00",
        "separator": 'color: #FF7F00; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #FF7F00; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #FF7F00; background: #FFF8F0; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #FFF8F0; padding: 10px; font-family: monospace; color: #FF7F00;',
    },
    
    # ========== 墨黑 ==========
    "墨黑": {
        "title": 'font-size: 24px; font-weight: bold; color: #1a1a1a; text-align: center; margin: 20px 0;',
        "title_color": "#1a1a1a",
        "separator": 'color: #666; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #1a1a1a; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #1a1a1a; margin: 20px 0 10px 0; border-bottom: 2px solid #1a1a1a; padding-bottom: 5px;',
        "quote": 'border-left: 4px solid #1a1a1a; background: #f5f5f5; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #f5f5f5; padding: 10px; font-family: monospace; color: #1a1a1a;',
    },
    
    # ========== 姹紫 ==========
    "姹紫": {
        "title": 'font-size: 24px; font-weight: bold; color: #8A2BE2; text-align: center; margin: 20px 0;',
        "title_color": "#8A2BE2",
        "separator": 'color: #8A2BE2; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #8A2BE2; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #8A2BE2; background: #F8F4FF; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #F8F4FF; padding: 10px; font-family: monospace; color: #8A2BE2;',
    },
    
    # ========== 嫩青 ==========
    "嫩青": {
        "title": 'font-size: 24px; font-weight: bold; color: #98FB98; text-align: center; margin: 20px 0;',
        "title_color": "#98FB98",
        "separator": 'color: #98FB98; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #98FB98; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #98FB98; background: #F0FFF0; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #F0FFF0; padding: 10px; font-family: monospace; color: #98FB98;',
    },
    
    # ========== 绿意 ==========
    "绿意": {
        "title": 'font-size: 24px; font-weight: bold; color: #228B22; text-align: center; margin: 20px 0;',
        "title_color": "#228B22",
        "separator": 'color: #228B22; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #228B22; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #228B22; background: #F0FFF0; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #F0FFF0; padding: 10px; font-family: monospace; color: #228B22;',
    },
    
    # ========== 红绯 ==========
    "红绯": {
        "title": 'font-size: 24px; font-weight: bold; color: #FF6B6B; text-align: center; margin: 20px 0;',
        "title_color": "#FF6B6B",
        "separator": 'color: #FF6B6B; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #FF6B6B; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #FF6B6B; background: #FFF0F0; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #FFF0F0; padding: 10px; font-family: monospace; color: #FF6B6B;',
    },
    
    # ========== WeChat-Format ==========
    "WeChat-Format": {
        "title": 'font-size: 22px; font-weight: bold; color: #1890ff; text-align: center; margin: 20px 0;',
        "title_color": "#1890ff",
        "separator": 'color: #8c8c8c; font-size: 12px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.6; color: #262626; padding: 0 15px;',
        "h2": 'font-size: 18px; font-weight: bold; color: #262626; margin: 24px 0 12px 0; border-left: 3px solid #1890ff; padding-left: 8px;',
        "quote": 'border-left: 4px solid #1890ff; background: #f7f7f7; padding: 12px 16px; margin: 12px 0; color: #595959; border-radius: 0 4px 4px 0;',
        "code": 'background: #f7f7f7; padding: 12px 16px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; color: #ff4d4f; border-radius: 4px;',
    },
    
    # ========== 科技蓝 ==========
    "科技蓝": {
        "title": 'font-size: 24px; font-weight: bold; color: #00A0E9; text-align: center; margin: 20px 0;',
        "title_color": "#00A0E9",
        "separator": 'color: #00A0E9; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #00A0E9; margin: 20px 0 10px 0; background: linear-gradient(90deg, transparent 50%, rgba(0,160,233,0.1) 50%); padding: 5px 0;',
        "quote": 'border-left: 4px solid #00A0E9; background: #E6F7FF; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #E6F7FF; padding: 10px; font-family: monospace; color: #00A0E9; border-radius: 4px;',
    },
    
    # ========== 兰青 ==========
    "兰青": {
        "title": 'font-size: 24px; font-weight: bold; color: #2E8B57; text-align: center; margin: 20px 0;',
        "title_color": "#2E8B57",
        "separator": 'color: #2E8B57; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #2E8B57; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #2E8B57; background: #F0FFF0; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #F0FFF0; padding: 10px; font-family: monospace; color: #2E8B57;',
    },
    
    # ========== 山吹 ==========
    "山吹": {
        "title": 'font-size: 24px; font-weight: bold; color: #FFB900; text-align: center; margin: 20px 0;',
        "title_color": "#FFB900",
        "separator": 'color: #FFB900; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #FFB900; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #FFB900; background: #FFFBF0; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #FFFBF0; padding: 10px; font-family: monospace; color: #FFB900;',
    },
    
    # ========== 前端之巅 ==========
    "前端之巅": {
        "title": 'font-size: 22px; font-weight: bold; color: #ff4757; text-align: center; margin: 20px 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
        "title_color": "#ff4757",
        "separator": 'color: #a4b0be; font-size: 12px; text-align: center; margin-bottom: 20px; letter-spacing: 2px;',
        "content": 'font-size: 15px; line-height: 1.7; color: #2f3542; padding: 0 12px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;',
        "h2": 'font-size: 18px; font-weight: 600; color: #2f3542; margin: 24px 0 12px 0; padding-bottom: 8px; border-bottom: 1px solid #dfe4ea;',
        "quote": 'border-left: 3px solid #ff4757; background: #fff1f2; padding: 12px 16px; margin: 12px 0; color: #57606f; border-radius: 0 4px 4px 0; font-size: 14px;',
        "code": 'background: #2f3542; padding: 14px 16px; font-family: "SF Mono", Monaco, Consolas, monospace; color: #ffa502; border-radius: 6px; font-size: 13px; line-height: 1.5;',
    },
    
    # ========== 极客黑 ==========
    "极客黑": {
        "title": 'font-size: 24px; font-weight: bold; color: #ffffff; text-align: center; margin: 20px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;',
        "title_color": "#667eea",
        "separator": 'color: #667eea; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #e0e0e0; padding: 0 10px; background: #1a1a2e; padding: 15px; border-radius: 8px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #667eea; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #667eea; background: #16213e; padding: 10px 15px; margin: 10px 0; color: #a0a0a0;',
        "code": 'background: #0f0f23; padding: 10px; font-family: monospace; color: #00d2ff; border: 1px solid #667eea;',
    },
    
    # ========== 简 ==========
    "简": {
        "title": 'font-size: 22px; font-weight: 300; color: #333; text-align: center; margin: 25px 0; letter-spacing: 3px;',
        "title_color": "#333",
        "separator": 'color: #ccc; font-size: 12px; text-align: center; margin-bottom: 25px;',
        "content": 'font-size: 15px; line-height: 2; color: #444; padding: 0 20px; font-family: "PingFang SC", "Microsoft YaHei", sans-serif; letter-spacing: 1px;',
        "h2": 'font-size: 16px; font-weight: 500; color: #333; margin: 30px 0 15px 0; padding-left: 10px; border-left: 2px solid #333;',
        "quote": 'border: none; background: none; border-left: 2px solid #ddd; padding: 10px 15px; margin: 15px 20px; color: #888; font-style: italic;',
        "code": 'background: none; border: 1px solid #eee; padding: 2px 6px; font-family: monospace; color: #666; font-size: 14px;',
    },
    
    # ========== 蔷薇紫 ==========
    "蔷薇紫": {
        "title": 'font-size: 24px; font-weight: bold; color: #C71585; text-align: center; margin: 20px 0;',
        "title_color": "#C71585",
        "separator": 'color: #C71585; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #C71585; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #C71585; background: #FFF0F5; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #FFF0F5; padding: 10px; font-family: monospace; color: #C71585;',
    },
    
    # ========== 萌绿 ==========
    "萌绿": {
        "title": 'font-size: 24px; font-weight: bold; color: #32CD32; text-align: center; margin: 20px 0;',
        "title_color": "#32CD32",
        "separator": 'color: #32CD32; font-size: 14px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;',
        "h2": 'font-size: 20px; font-weight: bold; color: #32CD32; margin: 20px 0 10px 0;',
        "quote": 'border-left: 4px solid #32CD32; background: #F0FFF0; padding: 10px 15px; margin: 10px 0; color: #666;',
        "code": 'background: #F0FFF0; padding: 10px; font-family: monospace; color: #32CD32;',
    },
    
    # ========== 全栈蓝 ==========
    "全栈蓝": {
        "title": 'font-size: 23px; font-weight: bold; color: #007AFF; text-align: center; margin: 20px 0;',
        "title_color": "#007AFF",
        "separator": 'color: #8e8e93; font-size: 13px; text-align: center; margin-bottom: 20px;',
        "content": 'font-size: 16px; line-height: 1.75; color: #1c1c1e; padding: 0 12px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;',
        "h2": 'font-size: 19px; font-weight: 600; color: #007AFF; margin: 24px 0 12px 0; padding-bottom: 6px; border-bottom: 1px solid #e5e5ea;',
        "quote": 'border-left: 3px solid #007AFF; background: #F2F7FF; padding: 12px 16px; margin: 12px 0; color: #636366; border-radius: 0 6px 6px 0;',
        "code": 'background: #1c1c1e; padding: 12px 16px; font-family: SF Mono, Menlo, Monaco, monospace; color: #64D2FF; border-radius: 8px; font-size: 14px;',
    },
}


def format_with_theme(title: str, content: str, theme_name: str = "简", image_urls: list = None) -> str:
    """
    根据主题格式化文章内容
    
    参数:
        - title: 文章标题
        - content: 文章正文（Markdown格式）
        - theme_name: 主题名称
        - image_urls: 文章内图片URL列表
    
    返回:
        - HTML格式的文章内容
    """
    theme = THEMES.get(theme_name, THEMES["简"])
    
    # 处理内容，先提取代码块并替换为占位符
    import re
    
    # 提取代码块
    code_blocks = []
    def replace_code_block(match):
        # group(2) 是代码内容，group(1) 是语言标识符
        code = match.group(2) if match.lastindex == 2 else match.group(1)
        # 清理代码：去除多余空行但保留缩进
        lines = code.split('\n')
        # 去除开头和结尾的纯空行
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        code = '\n'.join(lines)
        code_blocks.append(code)
        idx = len(code_blocks) - 1
        return f"__CODE_BLOCK_{idx}__"
    
    # 处理代码块（```...```）
    content = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, content, flags=re.DOTALL)
    content = re.sub(r'```(.*?)```', replace_code_block, content, flags=re.DOTALL)
    
    # 处理段落
    paragraphs = content.split("\n\n")
    content_html = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # 检测并恢复代码块
        if "__CODE_BLOCK_" in para:
            # 提取代码块内容
            import re
            match = re.search(r'__CODE_BLOCK_(\d+)__', para)
            if match:
                code_idx = int(match.group(1))
                code = code_blocks[code_idx]
                # 清理代码内容：去除首尾空白，但保留内部换行
                code = code.strip()
                # 转义 HTML 特殊字符
                code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                # 用 <br> 替换换行，不加任何特殊样式
                code_with_br = code.replace("\n", "<br>")
                content_html += f'<p style="background: #f5f5f5; padding: 10px; font-family: Consolas, monospace; font-size: 13px; line-height: 1.6; margin: 10px 0; white-space: pre-wrap; word-break: break-all;">{code_with_br}</p>\n'
        # 检测标题
        elif para.startswith("## "):
            h2_text = para[3:]
            content_html += f'<h2 style="{theme["h2"]}">{h2_text}</h2>\n'
        elif para.startswith("# "):
            # 大标题忽略，用传入的title
            continue
        elif para.startswith("> ") and not para.startswith(">]"):
            # 引用（但排除 >](E:\ 这种图片语法）
            quote_text = para[2:]
            content_html += f'<blockquote style="{theme["quote"]}"><p>{quote_text}</p></blockquote>\n'
        elif para.startswith("- ") or para.startswith("* "):
            # 列表
            lines = para.split("\n")
            content_html += '<ul style="margin: 10px 0; padding-left: 20px;">\n'
            for line in lines:
                if line.startswith("- ") or line.startswith("* "):
                    content_html += f'<li style="margin: 5px 0;">{line[2:]}</li>\n'
            content_html += '</ul>\n'
        else:
            # 普通段落
            para = para.replace("\n", "<br>")
            content_html += f'<p style="{theme["content"]}">{para}</p>\n'
    
    # 添加图片
    if image_urls:
        for img_url in image_urls:
            content_html += f'<p style="text-align: center; margin: 15px 0;"><img src="{img_url}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;"/></p>\n'
    
    # 构建完整HTML
    html = f'''
<h1 style="{theme["title"]}">{title}</h1>

<p style="{theme["separator"]}">— · —</p>

<div>
{content_html}
</div>
'''
    
    return html


def list_themes():
    """列出所有可用主题"""
    return list(THEMES.keys())


# 如果直接运行，显示所有主题
if __name__ == "__main__":
    print("可用主题列表：")
    for i, theme in enumerate(THEMES.keys(), 1):
        print(f"  {i}. {theme}")