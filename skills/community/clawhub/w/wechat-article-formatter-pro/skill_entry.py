#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from wechat_template_generator import WeChatTemplate
from datetime import datetime

def generate_wechat_article(markdown_content: str, title: str = "悟空极度舒适", theme: str = "theme_orange.css") -> dict:
    try:
        converter = WeChatTemplate(theme_css=theme)
        html_content = converter.generate_html(markdown_content, title)
        
        output_dir = "output_articles"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/wechat_article_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return {
            "status": "success",
            "message": f"✅ 公众号排版已生成 (使用主题: {theme})",
            "file_path": filename,
            "preview_url": f"file://{os.path.abspath(filename)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ 转换失败: {str(e)}"
        }

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "article.md"
    theme_choice = sys.argv[2] if len(sys.argv) > 2 else "theme_orange.css"
    
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = generate_wechat_article(content, title="悟空极度舒适", theme=theme_choice)
        print(result["message"])
        print(f"路径: {result.get('file_path')}")
    else:
        print(f"❌ 找不到文件 {input_file}")