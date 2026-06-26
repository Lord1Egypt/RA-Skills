#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import markdown

class WeChatTemplate:
    def __init__(self, theme_css='theme_orange.css'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_css_path = os.path.join(current_dir, 'themes', theme_css)
        
        if os.path.exists(full_css_path):
            with open(full_css_path, 'r', encoding='utf-8') as f:
                self.css_content = f.read()
        else:
            self.css_content = "/* 默认样式 */ body { font-family: sans-serif; }"
        
        self.template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
{content}
</body>
</html>"""

    def generate_html(self, markdown_text, title="悟空极度舒适"):
        html_content = markdown.markdown(
            markdown_text,
            extensions=['tables', 'fenced_code', 'nl2br', 'sane_lists']
        )
        return self.template.format(title=title, css=self.css_content, content=html_content)