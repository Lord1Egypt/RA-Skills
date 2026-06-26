#!/usr/bin/env python3
"""
HTML 写作模块
生成优化的微信公众号 HTML 内容
"""

from typing import List, Dict
import re


class HTMLWriter:
    """HTML 文章写作器"""
    
    # 默认排版样式（紧凑版，适合手机阅读）
    DEFAULT_STYLES = {
        'body': {
            'font-size': '16px',
            'line-height': '1.75',
            'color': '#333333',
            'letter-spacing': '0.5px',
            'padding': '0 16px',
            'margin': '0 0 16px 0'
        },
        'h1': {
            'font-size': '20px',
            'font-weight': 'bold',
            'color': '#1a1a2e',
            'margin': '24px 0 16px 0',
            'padding': '0 16px',
            'border-bottom': '2px solid #1a1a2e',
            'padding-bottom': '8px',
            'letter-spacing': '0.5px'
        },
        'h2': {
            'font-size': '17px',
            'font-weight': 'bold',
            'color': '#2d3436',
            'margin': '20px 0 12px 0',
            'padding': '0 16px',
            'border-left': '3px solid #0984e3',
            'padding-left': '10px'
        },
        'h3': {
            'font-size': '16px',
            'font-weight': 'bold',
            'color': '#2d3436',
            'margin': '16px 0 10px 0',
            'padding': '0 16px'
        },
        'blockquote': {
            'font-size': '15px',
            'background-color': '#f5f5f5',
            'border-left': '3px solid #0984e3',
            'padding': '12px 16px',
            'margin': '16px 0',
            'color': '#555555',
            'font-style': 'normal',
            'line-height': '1.7'
        },
        'code_inline': {
            'font-size': '14px',
            'background-color': '#f0f0f0',
            'padding': '1px 4px',
            'border-radius': '3px',
            'color': '#e74c3c',
            'font-family': "'SF Mono', 'Courier New', monospace"
        },
        'code_block': {
            'font-size': '13px',
            'background-color': '#f8f8f8',
            'padding': '12px 16px',
            'border-radius': '6px',
            'margin': '16px 0',
            'border': '1px solid #e8e8e8',
            'line-height': '1.6',
            'color': '#333333',
            'overflow-x': 'auto'
        },
        'list': {
            'font-size': '16px',
            'margin': '12px 0',
            'padding': '0 16px',
            'line-height': '1.75'
        },
        'link': {
            'color': '#0984e3',
            'text-decoration': 'none',
            'border-bottom': '1px solid #0984e3'
        },
        'strong': {
            'font-weight': 'bold',
            'color': '#1a1a2e'
        },
        'separator': {
            'border-top': '1px solid #e0e0e0',
            'margin': '24px 15%'
        }
    }
    
    def __init__(self, styles: Dict = None):
        self.styles = styles or self.DEFAULT_STYLES
    
    def _style_to_str(self, style_dict: Dict) -> str:
        """将样式字典转换为 CSS 字符串"""
        return '; '.join([f"{k}: {v}" for k, v in style_dict.items()])
    
    def create_paragraph(self, text: str) -> str:
        """创建段落"""
        style = self._style_to_str(self.styles['body'])
        # 处理加粗和斜体
        text = self._format_inline_styles(text)
        return f'<p style="{style}">{text}</p>'
    
    def create_heading(self, level: int, text: str) -> str:
        """创建标题"""
        tag = f'h{level}'
        style = self._style_to_str(self.styles.get(tag, self.styles['h3']))
        return f'<{tag} style="{style}">{text}</{tag}>'
    
    def create_blockquote(self, text: str) -> str:
        """创建引用块"""
        style = self._style_to_str(self.styles['blockquote'])
        text = self._format_inline_styles(text)
        return f'<blockquote style="{style}">{text}</blockquote>'
    
    def create_code_block(self, code: str, language: str = '') -> str:
        """创建代码块"""
        style = self._style_to_str(self.styles['code_block'])
        # 转义 HTML
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre style="{style}"><code>{code}</code></pre>'
    
    def create_list(self, items: List[str], ordered: bool = False) -> str:
        """创建列表"""
        style = self._style_to_str(self.styles['list'])
        tag = 'ol' if ordered else 'ul'
        
        items_html = []
        for i, item in enumerate(items, 1):
            item_text = self._format_inline_styles(item)
            if ordered:
                items_html.append(f'<li style="margin: 6px 0; line-height: 1.75; color: #333333; padding-left: 30px; position: relative;"><span style="position: absolute; left: 0; color: #0984e3; font-weight: bold;">{i}.</span>{item_text}</li>')
            else:
                items_html.append(f'<li style="margin: 6px 0; line-height: 1.75; color: #333333; padding-left: 20px; position: relative;"><span style="position: absolute; left: 0; color: #0984e3;">·</span>{item_text}</li>')
        
        return f'<{tag} style="{style}; list-style: none;">{ "".join(items_html) }</{tag}>'
    
    def create_separator(self) -> str:
        """创建分隔线"""
        style = self._style_to_str(self.styles['separator'])
        return f'<section style="{style}"></section>'
    
    def _format_inline_styles(self, text: str) -> str:
        """格式化行内样式"""
        # 加粗 **text**
        text = re.sub(r'\*\*(.+?)\*\*', 
                     lambda m: f'<strong style="{self._style_to_str(self.styles["strong"])}">{m.group(1)}</strong>', 
                     text)
        # 斜体 *text*
        text = re.sub(r'\*(.+?)\*', 
                     lambda m: f'<em style="font-style: italic;">{m.group(1)}</em>', 
                     text)
        # 行内代码 `code`
        text = re.sub(r'`(.+?)`', 
                     lambda m: f'<code style="{self._style_to_str(self.styles["code_inline"])}">{m.group(1)}</code>', 
                     text)
        return text
    
    def write_section(self, title: str, content: str, level: int = 2) -> str:
        """
        写作一个章节
        
        Args:
            title: 章节标题
            content: 章节内容（支持 Markdown 格式）
            level: 标题级别
            
        Returns:
            HTML 字符串
        """
        html_parts = []
        
        # 添加标题
        html_parts.append(self.create_heading(level, title))
        
        # 处理内容
        paragraphs = content.strip().split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # 检测特殊格式
            if para.startswith('> '):
                # 引用块
                html_parts.append(self.create_blockquote(para[2:]))
            elif para.startswith('```'):
                # 代码块
                lines = para.split('\n')
                code = '\n'.join(lines[1:-1])  # 去掉 ```
                html_parts.append(self.create_code_block(code))
            elif para.startswith('- ') or para.startswith('* '):
                # 无序列表
                items = [line[2:] for line in para.split('\n') if line.startswith('- ') or line.startswith('* ')]
                html_parts.append(self.create_list(items))
            elif re.match(r'^\d+\.', para):
                # 有序列表
                items = [re.sub(r'^\d+\.\s*', '', line) for line in para.split('\n')]
                html_parts.append(self.create_list(items, ordered=True))
            elif para == '---':
                # 分隔线
                html_parts.append(self.create_separator())
            else:
                # 普通段落
                html_parts.append(self.create_paragraph(para))
        
        return '\n'.join(html_parts)
    
    def write_article(self, title: str, sections: List[Dict]) -> str:
        """
        写作完整文章
        
        Args:
            title: 文章标题
            sections: 章节列表，每个包含 'title' 和 'content'
            
        Returns:
            完整 HTML
        """
        html_parts = []
        
        # 文章标题
        html_parts.append(self.create_heading(1, title))
        
        # 各章节
        for section in sections:
            html_parts.append(self.write_section(
                section['title'],
                section['content'],
                level=2
            ))
        
        return '\n\n'.join(html_parts)
    
    def add_footer(self, html_content: str, text: str = '小爪制作') -> str:
        """添加页脚"""
        footer = f'<p style="font-size: 14px; color: #999999; text-align: center; margin: 24px 0; padding: 0 16px;"><em>{text}</em></p>'
        return html_content + '\n' + footer


# 便捷函数
def write_html_article(title: str, sections: List[Dict]) -> str:
    """快速写作 HTML 文章"""
    writer = HTMLWriter()
    return writer.write_article(title, sections)


def markdown_to_html_simple(md_content: str) -> str:
    """简单 Markdown 转 HTML"""
    writer = HTMLWriter()
    return writer.write_section('', md_content)
