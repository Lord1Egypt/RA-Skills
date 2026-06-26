#!/usr/bin/env python3
"""Markdown转微信公众号兼容HTML，内置多套主题"""

import os
import re
import sys

# 自动安装 markdown 库
try:
    import markdown
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "-q", "--break-system-packages"])
    import markdown

THEMES_DIR = os.path.join(os.path.dirname(__file__), "..", "themes")
AVAILABLE_THEMES = ["default", "elegant", "dark"]


def load_theme(name="default"):
    """加载主题CSS"""
    if name not in AVAILABLE_THEMES:
        print(f"⚠️ 未知主题 '{name}'，使用 default", file=sys.stderr)
        name = "default"
    path = os.path.join(THEMES_DIR, f"{name}.css")
    if not os.path.exists(path):
        return ""
    with open(path) as f:
        return f.read()


def md_to_html(md_text, theme="default"):
    """将Markdown转为微信公众号兼容HTML（内联样式）"""
    # 转换markdown
    html = markdown.markdown(
        md_text,
        extensions=["extra", "codehilite", "toc", "nl2br"],
        extension_configs={"codehilite": {"css_class": "code"}},
    )
    css = load_theme(theme)
    # 微信不支持 <style> 标签，需要内联样式
    # 这里我们把CSS包裹在section里，微信编辑器会保留内联style
    wrapped = f'<section style="max-width:100%;box-sizing:border-box;word-wrap:break-word;">\n'
    if css:
        # 将CSS规则转为内联style的方式：用section包裹并在首部嵌入style
        # 微信草稿接口实际支持<style>在content中
        wrapped += f"<style>{css}</style>\n"
    wrapped += html
    wrapped += "\n</section>"
    return wrapped


def convert_file(md_path, theme="default"):
    """转换文件"""
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()
    return md_to_html(md_text, theme)


def find_local_images(md_text):
    """找出markdown中的本地图片路径"""
    # ![alt](path) 格式
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    images = []
    for alt, src in re.findall(pattern, md_text):
        if not src.startswith(("http://", "https://", "data:")):
            images.append(src)
    return images


def replace_image_urls(md_text, url_map):
    """替换markdown中的图片路径为新URL"""
    def replacer(m):
        alt = m.group(1)
        src = m.group(2)
        new_url = url_map.get(src, src)
        return f"![{alt}]({new_url})"
    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replacer, md_text)


def main():
    if len(sys.argv) < 2:
        print("用法: md2html.py <markdown文件> [主题名]")
        print(f"可用主题: {', '.join(AVAILABLE_THEMES)}")
        sys.exit(1)
    md_path = sys.argv[1]
    theme = sys.argv[2] if len(sys.argv) > 2 else "default"
    html = convert_file(md_path, theme)
    print(html)


if __name__ == "__main__":
    main()
