#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞哥公众号排版 Formatter
功能：将 Markdown 文章转换为飞哥专属风格的公众号 HTML

Python 版本要求：3.6+（仅用标准库，无第三方依赖）
如遇 glibc 版本不兼容，请使用低版本 Python 运行，例如：
    python3.8 formatter.py input.md -o output.html

使用示例：
    python3 formatter.py input.md --output output.html --brand-color "#DE7356"
"""

import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any

class FeigePFormatter:
    """飞哥公众号排版格式化器"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        'brand_color': '#DE7356',           # Claude 桃色
        'brand_color_light': '#E8956D',     # 浅桃色
        'brand_color_dark': '#B54432',      # 深棕红
        'brand_color_lighter': '#FFF5F0',   # 超浅桃色背景
        'secondary_color': '#0891B2',       # 技术提示色（青色）
        'secondary_light': '#ECFEFF',       # 浅青背景
        'font_size_body': '15px',
        'font_size_title': '20px',
        'font_size_h3': '17px',
    }
    
    # 警告颜色
    ALERT_COLORS = {
        '警告': {
            'bg': '#FFF5F0',
            'border': '#DE7356',
            'text': '#C75D42',
            'icon': '⚠️'
        },
        '技术': {
            'bg': '#ECFEFF',
            'border': '#0891B2',
            'text': '#0891B2',
            'icon': '💡'
        },
        '信息': {
            'bg': '#EFF6FF',
            'border': '#3B82F6',
            'text': '#3B82F6',
            'icon': 'ℹ️'
        }
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.embed_images = self.config.pop('embed_images', True)
    
    def markdown_to_html(self, markdown_content: str) -> str:
        """将 Markdown 转换为 HTML"""
        html_parts = []
        lines = markdown_content.strip().split('\n')
        
        i = 0
        breaking = None
        parts = []
        current_content = []
        h2_counter = 0   # 普通 ## 标题自动编号计数器
        article_title = ''   # 从 # 标题提取，用于自动 BREAKING
        article_summary = ''  # 从首段提取，用于自动 BREAKING
        
        while i < len(lines):
            line = lines[i]
            
            # 跳过空行
            if not line.strip():
                i += 1
                continue
            
            # 一级标题：提取文章标题用于自动 BREAKING，自身不渲染
            if re.match(r'^#{1}\s*\S', line) and not line.startswith('##'):
                if not article_title:
                    article_title = re.sub(r'^#{1}\s*', '', line).strip()
                i += 1
                continue

            # Breaking 标题处理（手动指定）
            if re.match(r'^#{2}\s*BREAKING', line):
                breaking = self._parse_breaking_section(lines, i)
                i += breaking['offset']
                continue
            
            # PART 分节处理（手动指定 ## PART 01 xxx）
            if re.match(r'^#{2}\s*PART\s*\d', line):
                if current_content:
                    parts.append({'type': 'content', 'data': current_content})
                    current_content = []
                part = self._parse_part_section(line)
                parts.append({'type': 'part', 'data': part})
                i += 1
                continue
            
            # 普通 ## 标题 → 自动编号转 PART 渐变卡片
            if re.match(r'^#{2}\s*\S', line) and not re.match(r'^#{3}', line):
                title_text = re.sub(r'^#{2}\s*', '', line).strip()
                # 排除 BREAKING / PART 关键字（由上面的分支处理）
                if not title_text.startswith('BREAKING') and not title_text.startswith('PART'):
                    if current_content:
                        parts.append({'type': 'content', 'data': current_content})
                        current_content = []
                    h2_counter += 1
                    # 支持 "## 标题 | 副标题" 语法
                    if '|' in title_text:
                        split = title_text.split('|', 1)
                        main_title = split[0].strip()
                        sub_title = split[1].strip()
                    else:
                        main_title = title_text
                        sub_title = ''
                    parts.append({'type': 'part', 'data': {
                        'number': str(h2_counter),
                        'title': main_title,
                        'subtitle': sub_title
                    }})
                    i += 1
                    continue
            
            # 特殊块处理 (> 开头的特殊格式)
            if line.startswith('> '):
                # STEP 块（容忍 > STEP01 无空格）
                if re.match(r'>\s*STEP\s*\d', line):
                    step = self._parse_step_block(lines, i)
                    current_content.append({'type': 'step', 'data': step['data']})
                    i = step['offset']
                    continue
                # Insight 块 (> ✨ 或 > 💡)
                elif line.startswith('> ✨') or line.startswith('> 💡'):
                    insight = self._parse_insight_block(lines, i)
                    current_content.append({'type': 'insight', 'data': insight['data']})
                    i = insight['offset']
                    continue
                # PROMPT 块
                elif line.startswith('> 🤖 PROMPT') or line.startswith('> PROMPT'):
                    prompt = self._parse_prompt_block(lines, i)
                    current_content.append({'type': 'prompt', 'data': prompt['data']})
                    i = prompt['offset']
                    continue
                # 警告提示 [警告] 等
                elif line.startswith('> ['):
                    alert = self._parse_alert(line)
                    if alert:
                        current_content.append({'type': 'alert', 'data': alert})
                    i += 1
                    continue
                else:
                    # 孤立的 > 行：去掉 > 前缀当普通文本处理，不让 > 泄漏到输出
                    plain_text = line[2:].strip()
                    if plain_text:
                        current_content.append({'type': 'text', 'data': plain_text})
                    i += 1
                    continue
            
            # 代码块处理
            if line.strip().startswith('```'):
                code_block = self._parse_code_block(lines, i)
                current_content.append({'type': 'code', 'data': code_block['content']})
                i = code_block['offset']
                continue
            
            # 图片处理 ![](...)
            if line.strip().startswith('!['):
                current_content.append({'type': 'image', 'data': line})
                i += 1
                continue
            
            # 其他所有有内容的行都加入
            current_content.append({'type': 'text', 'data': line})
            # 提取首段摘要（第一条普通段落，不超过 60 字）
            if not article_summary and line.strip() and not re.match(r'^[#>\-\*`!\|]', line):
                article_summary = line.strip()[:80]
            
            i += 1
        
        if current_content:
            parts.append({'type': 'content', 'data': current_content})
        
        # 如果没有手动 BREAKING，且有文章标题，则自动生成开篇板块
        if not breaking and article_title:
            import datetime
            now = datetime.datetime.now()
            date_str = f'{now.year}.{now.month:02d}'
            breaking = {
                'title_strikethrough': '',
                'title_bold': article_title,
                'title_highlight': '',
                'subtitle': '',   # 自动模式不填 subtitle，避免与正文第一段重复
                'date': date_str,
                '_auto': True   # 标记为自动生成
            }
        
        # 生成 HTML
        html_parts.append(self._generate_html_head())
        html_parts.append('<div class="container">')
        
        # Breaking 标题
        if breaking:
            html_parts.append(self._render_breaking(breaking))
        
        # 内容部分
        for part in parts:
            if part['type'] == 'part':
                html_parts.append(self._render_part_header(part['data']))
            elif part['type'] == 'content':
                html_parts.append(self._render_content(part['data']))
        
        # 结尾
        html_parts.append(self._render_footer())
        
        html_parts.append('</div>')
        html_parts.append(self._generate_html_tail())
        
        return '\n'.join(html_parts)
    
    def _parse_breaking_section(self, lines: List[str], start: int) -> Dict:
        """解析 BREAKING 部分"""
        breaking = {
            'title_strikethrough': '',
            'title_bold': '',
            'title_highlight': '',
            'subtitle': '',
            'date': '2026.03',
            'offset': 1
        }
        
        i = start + 1
        while i < len(lines) and lines[i].startswith('- '):
            line = lines[i]
            key, value = line[2:].split(':', 1) if ':' in line else (line[2:], '')
            key = key.strip()
            value = value.strip()
            
            key_map = {
                'strikethrough': 'title_strikethrough',
                'bold': 'title_bold',
                'highlight': 'title_highlight',
                'subtitle': 'subtitle',
                'date': 'date'
            }
            
            if key in key_map:
                breaking[key_map[key]] = value
            
            i += 1
            breaking['offset'] += 1
        
        return breaking
    
    def _parse_part_section(self, line: str) -> Dict:
        """解析 PART 分节，支持 '## PART 02 主标题' 或 '## PART 02 主标题 | 副标题' 或 '## PART 02 | 副标题'，也容忍 ##PART02 无空格写法"""
        match = re.match(r'^#{2}\s*PART\s*(\d+)\s*(.*?)(?:\n|$)', line)
        if match:
            raw_title = match.group(2).strip()
            # 支持 "主标题 | 副标题" 语法
            if '|' in raw_title:
                parts_split = raw_title.split('|', 1)
                left = parts_split[0].strip()
                right = parts_split[1].strip()
                # 如果 | 左侧为空，用右侧作为主标题
                title = left if left else right
                subtitle = right if left else ''
                return {
                    'number': match.group(1),
                    'title': title,
                    'subtitle': subtitle
                }
            return {
                'number': match.group(1),
                'title': raw_title if raw_title else '未命名章节',
                'subtitle': ''
            }
        return {'number': '1', 'title': '部分标题', 'subtitle': ''}
    
    def _parse_alert(self, line: str) -> Dict:
        """解析警告提示框"""
        match = re.match(r'>\s*\[(\S+)\]\s*(.*)', line)
        if match:
            alert_type = match.group(1)
            content = match.group(2)
            
            if alert_type in self.ALERT_COLORS:
                return {
                    'type': alert_type,
                    'content': content,
                    'colors': self.ALERT_COLORS[alert_type]
                }
        return None
    
    def _parse_step_block(self, lines: List[str], start: int) -> Dict:
        """解析 STEP 块（容忍空行，遇到新特殊块或非 > 行才停）"""
        lines_data = []
        i = start
        step_title = ''
        step_num = '1'

        # 第一行是 STEP 标题
        first_line = lines[i]
        match = re.match(r'>\s*STEP\s+(\d+)\s*(.*)', first_line)
        if match:
            step_num = match.group(1)
            step_title = match.group(2).strip()

        i += 1
        # 收集后续说明行：允许空行（跳过），遇到新特殊块或普通非 > 行才停
        while i < len(lines):
            curr = lines[i]
            # 空行：允许，跳过继续向后看
            if not curr.strip():
                # 往后扫，判断下一个非空行是否还是 > 块的内容
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and lines[j].startswith('> ') and not re.match(r'>\s*(STEP|✨|💡|🤖|PROMPT|\[)', lines[j]):
                    i += 1  # 跳过空行，继续收集
                    continue
                else:
                    break  # 空行后跟的不是本块内容，停止
            # 非 > 开头：停止
            if not curr.startswith('> '):
                break
            # 新的特殊块：停止
            if re.match(r'>\s*(STEP\s+\d|✨|💡|🤖|PROMPT|\[)', curr):
                break
            # 普通内容行
            content_line = curr[2:].strip()
            if content_line:
                lines_data.append(content_line)
            i += 1

        return {
            'offset': i,
            'data': {
                'number': step_num,
                'title': step_title,
                'content': '\n'.join(lines_data)
            }
        }
    
    def _parse_insight_block(self, lines: List[str], start: int) -> Dict:
        """解析 Insight 块（总结框，容忍空行）"""
        lines_data = []
        i = start
        insight_title = ''
        icon = ''

        first_line = lines[i]
        match = re.match(r'>\s*(✨|💡)\s+(.*)', first_line)
        if match:
            icon = match.group(1)
            insight_title = match.group(2).strip()

        i += 1
        while i < len(lines):
            curr = lines[i]
            if not curr.strip():
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and lines[j].startswith('> ') and not re.match(r'>\s*(✨|💡|STEP|🤖|PROMPT|\[)', lines[j]):
                    i += 1
                    continue
                else:
                    break
            if not curr.startswith('> '):
                break
            if re.match(r'>\s*(✨|💡|STEP\s+\d|🤖|PROMPT|\[)', curr):
                break
            content_line = curr[2:].strip()
            if content_line:
                lines_data.append(content_line)
            i += 1

        return {
            'offset': i,
            'data': {
                'icon': icon,
                'title': insight_title,
                'content': '\n'.join(lines_data)
            }
        }
    
    def _parse_prompt_block(self, lines: List[str], start: int) -> Dict:
        """解析 Prompt 块（容忍空行）"""
        lines_data = []
        i = start + 1

        while i < len(lines):
            curr = lines[i]
            if not curr.strip():
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and lines[j].startswith('> ') and not re.match(r'>\s*(✨|💡|STEP|🤖|PROMPT|\[)', lines[j]):
                    i += 1
                    continue
                else:
                    break
            if not curr.startswith('> '):
                break
            if re.match(r'>\s*(✨|💡|STEP\s+\d|🤖|PROMPT|\[)', curr):
                break
            content_line = curr[2:].strip()
            if content_line:
                lines_data.append(content_line)
            i += 1

        return {
            'offset': i,
            'data': '\n'.join(lines_data)
        }
    
    def _parse_code_block(self, lines: List[str], start: int) -> Dict:
        """解析代码块"""
        code_lines = []
        i = start + 1
        
        while i < len(lines) and not lines[i].strip().startswith('```'):
            code_lines.append(lines[i])
            i += 1
        
        return {
            'content': '\n'.join(code_lines).strip(),
            'offset': i + 1
        }
    
    def _render_breaking(self, breaking: Dict) -> str:
        """渲染 Breaking 标题（支持自动生成模式）"""
        bc = self.config['brand_color']
        bc_light = self.config['brand_color_light']
        bc_rgb = self._hex_to_rgb(bc)
        is_auto = breaking.get('_auto', False)

        # 组装标题行 HTML
        title_lines = ''
        if is_auto:
            # 自动模式：只有文章标题，大字黑色居左，无删除线和高亮行
            title_lines = f'''
          <p style="font-size: 26px; font-weight: 900; color: #111827; margin: 0 0 12px; line-height: 1.2; letter-spacing: -1px;">{breaking['title_bold']}</p>'''
        else:
            if breaking.get('title_strikethrough'):
                title_lines += f'\n          <p style="font-size: 15px; color: #D1D5DB; margin: 0 0 6px; text-decoration: line-through; letter-spacing: 0.5px;">{breaking["title_strikethrough"]}</p>'
            if breaking.get('title_bold'):
                title_lines += f'\n          <p style="font-size: 26px; font-weight: 900; color: #111827; margin: 0; line-height: 1.1; letter-spacing: -1px;">{breaking["title_bold"]}</p>'
            if breaking.get('title_highlight'):
                title_lines += f'\n          <p style="font-size: 22px; font-weight: 900; color: {bc}; margin: 0 0 12px; line-height: 1.1; letter-spacing: -1px;">{breaking["title_highlight"]}</p>'

        subtitle_html = ''
        if breaking.get('subtitle'):
            subtitle_html = f'<p style="font-size: 13px; color: #9CA3AF; margin: 0; line-height: 1.7; letter-spacing: 0.5px;">{breaking["subtitle"]}</p>'

        html = f"""
  <section style="margin: 0 0 32px; background: #ffffff; border: 1.5px solid rgba({bc_rgb}, 0.2); border-radius: 20px; overflow: hidden; width: 100%;">
    <section style="padding: 32px 28px 28px;">
      <section style="display: flex; align-items: center; gap: 8px; margin-bottom: 24px;">
        <span style="width: 6px; height: 6px; background: {bc}; border-radius: 50%; display: inline-block;"></span>
        <span style="font-size: 11px; font-weight: bold; letter-spacing: 3px; color: {bc};">BREAKING</span>
        <span style="flex: 1; height: 1px; background: linear-gradient(to right, rgba({bc_rgb}, 0.15), transparent);"></span>
        <span style="font-size: 10px; color: #D1D5DB; font-weight: bold;">{breaking['date']}</span>
      </section>
      <section style="display: flex; align-items: center; gap: 20px;">
        <section style="flex: 1;">{title_lines}
          <section style="width: 48px; height: 3px; background: linear-gradient(to right, {bc}, {bc_light}); border-radius: 2px; margin: 12px 0;"></section>
          {subtitle_html}
        </section>
      </section>
    </section>
  </section>
"""
        return html
    
    def _render_part_header(self, part: Dict) -> str:
        """渲染 PART 分节头 —— 左侧 PART+编号标签，右侧主标题，紧凑单行"""
        html = f"""
  <section style="margin: 36px 0 18px;">
    <section style="background: linear-gradient(135deg, {self.config['brand_color']}, {self.config['brand_color_light']}); border-radius: 12px; overflow: hidden; display: table; width: 100%; box-sizing: border-box;">
      <section style="display: table-cell; width: 1%; white-space: nowrap; padding: 14px 16px; vertical-align: middle; text-align: center; border-right: 1px solid rgba(255,255,255,0.22);">
        <span style="font-size: 9px; font-weight: 800; letter-spacing: 2.5px; color: rgba(255,255,255,0.7); text-transform: uppercase; display: block; line-height: 1;">PART</span>
        <span style="font-size: 22px; font-weight: 900; color: #ffffff; line-height: 1.1; letter-spacing: -1px; display: block; margin-top: 2px;">{part['number'].zfill(2)}</span>
      </section>
      <section style="display: table-cell; padding: 14px 18px; vertical-align: middle;">
        <h2 style="font-size: 18px; font-weight: 900; color: #ffffff; margin: 0; letter-spacing: -0.2px; line-height: 1.35;">{part['title']}</h2>
      </section>
    </section>
  </section>"""
        return html
    
    def _render_content(self, content_items: List[Dict]) -> str:
        """渲染内容"""
        html_parts = []
        
        # 自动修正 STEP 序号：按出现顺序重新编号，忽略原始编号
        step_counter = 0
        for item in content_items:
            if item['type'] == 'step':
                step_counter += 1
                item['data']['number'] = str(step_counter)
        
        i = 0
        while i < len(content_items):
            item = content_items[i]
            
            if item['type'] == 'text':
                line = item['data']
                
                # 一级标题 # - 已在主循环提取，这里不应出现，防御性跳过
                if re.match(r'^#{1}\s*\S', line) and not line.startswith('##'):
                    pass
                
                # 二级标题 ## - 已在主循环转为 PART，这里不应出现，防御性跳过
                elif re.match(r'^#{2}\s*\S', line) and not line.startswith('###'):
                    pass
                
                # 三级标题 ### - 支持 | 副标题语法（容忍 ### 后无空格）
                elif re.match(r'^#{3}\s*\S', line):
                    title = re.sub(r'^#{3}\s*', '', line).strip()
                    # 支持 "### 标题 | 副标题" 语法
                    if '|' in title:
                        parts_split = title.split('|', 1)
                        h3_title = parts_split[0].strip()
                        h3_subtitle = parts_split[1].strip()
                        html_parts.append(f'  <section style="margin: 20px 0 10px;"><h3 style="font-size: 17px; font-weight: 800; color: {self.config["brand_color"]}; margin: 0 0 4px; letter-spacing: -0.2px;">{self._process_inline_markdown(h3_title)}</h3><p style="font-size: 12px; color: #9CA3AF; margin: 0; line-height: 1.5;">{self._process_inline_markdown(h3_subtitle)}</p></section>')
                    else:
                        html_parts.append(f'  <h3 style="margin: 20px 0 10px; font-size: 17px; font-weight: 800; color: {self.config["brand_color"]}; letter-spacing: -0.2px; padding-bottom: 6px; border-bottom: 1.5px solid {self.config["brand_color"]}33;">{self._process_inline_markdown(title)}</h3>')
                
                # 列表项 - 或 * 或数字序号（1. / 1） / 1、）
                elif line.startswith('- ') or line.startswith('* ') or re.match(r'^\d+[\.）、]\s*\S', line):
                    # 收集连续的列表项（支持多种格式）
                    list_items = []
                    j = i
                    while j < len(content_items) and content_items[j]['type'] == 'text':
                        curr_line = content_items[j]['data']
                        if curr_line.startswith('- ') or curr_line.startswith('* '):
                            list_items.append(curr_line[2:].strip())
                            j += 1
                        elif re.match(r'^\d+[\.）、]\s*', curr_line):
                            # 去掉序号前缀，只保留内容
                            content_text = re.sub(r'^\d+[\.）、]\s*', '', curr_line).strip()
                            list_items.append(content_text)
                            j += 1
                        else:
                            break
                    
                    html_parts.append(self._render_list(list_items))
                    i = j - 1
                
                # 表格检测
                elif '|' in line and i + 1 < len(content_items) and '|' in content_items[i+1]['data']:
                    # 收集表格行
                    table_rows = [line]
                    j = i + 1
                    while j < len(content_items) and content_items[j]['type'] == 'text' and '|' in content_items[j]['data']:
                        table_rows.append(content_items[j]['data'])
                        j += 1
                    
                    html_parts.append(self._render_table(table_rows))
                    i = j - 1
                
                # 水平线 ---
                elif line.strip() == '---' or line.strip() == '***':
                    html_parts.append(f'  <section style="height: 2px; background: linear-gradient(to right, rgba({self._hex_to_rgb(self.config["brand_color"])}, 0.3), transparent); margin: 24px 0;"></section>')
                
                # 普通段落
                elif line.strip():
                    html_parts.append(f'  <p style="margin: 14px 0; color: #374151; line-height: 1.8; font-size: 15px;">{self._process_inline_markdown(line)}</p>')
            
            elif item['type'] == 'alert':
                html_parts.append(self._render_alert(item['data']))
            
            elif item['type'] == 'code':
                html_parts.append(self._render_code_block(item['data']))
            
            elif item['type'] == 'step':
                html_parts.append(self._render_step_block(item['data']))
            
            elif item['type'] == 'insight':
                html_parts.append(self._render_insight_block(item['data']))
            
            elif item['type'] == 'prompt':
                html_parts.append(self._render_prompt_block(item['data']))
            
            elif item['type'] == 'image':
                html_parts.append(self._render_image(item['data']))
            
            i += 1
        
        return '\n'.join(html_parts)
    
    def _process_inline_markdown(self, text: str) -> str:
        """处理内联 Markdown 格式：**加粗** *斜体* ~~删除线~~ ==高亮== `代码`"""
        # ==关键词高亮== → 主色字体 + 渐变底色背景（对标效果）
        text = re.sub(r'==(.+?)==', 
            rf'<span style="color: {self.config["brand_color_dark"]}; background: linear-gradient(135deg, {self.config["brand_color"]}22, {self.config["brand_color_light"]}33); padding: 2px 8px; border-radius: 4px; font-weight: 700; letter-spacing: 0.3px;">\1</span>', 
            text)
        # `行内代码` → <code> (需在 ** 之前处理，避免干扰)
        text = re.sub(r'`([^`]+)`', r'<code style="font-family: \'SF Mono\', Monaco, Consolas, monospace; font-size: 0.88em; background: #F3F4F6; color: #B54432; padding: 1px 5px; border-radius: 3px;">\1</code>', text)
        # **加粗** → <strong>
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="font-weight: 900; color: #111827;">\1</strong>', text)
        # *斜体* → <em>
        text = re.sub(r'\*(.+?)\*', r'<em style="font-style: italic; color: #4B5563;">\1</em>', text)
        # ~~删除线~~ → <del>
        text = re.sub(r'~~(.+?)~~', r'<del style="text-decoration: line-through; color: #9CA3AF;">\1</del>', text)
        # [链接](url) → <a>
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color: #DE7356; text-decoration: none; border-bottom: 1px solid #DE7356;">\1</a>', text)
        return text
    
    def _render_list(self, items: List[str]) -> str:
        """渲染列表"""
        html = '  <ul style="margin: 14px 0 14px 24px; list-style: none; padding: 0;">\n'
        for item in items:
            processed = self._process_inline_markdown(item)
            html += f'    <li style="margin: 8px 0; color: #374151; line-height: 1.8; position: relative; padding-left: 16px;">'
            html += f'<span style="position: absolute; left: 0; color: {self.config["brand_color"]}; font-weight: bold;">•</span>{processed}</li>\n'
        html += '  </ul>'
        return html
    
    def _render_table(self, rows: List[str]) -> str:
        """渲染表格"""
        table_rows = []
        for i, row in enumerate(rows):
            cells = [cell.strip() for cell in row.split('|') if cell.strip()]
            
            # 跳过分隔符行 |---|---|
            if all(c.replace('-', '').replace(':', '').strip() == '' for c in cells):
                continue
            
            table_rows.append(cells)
        
        if len(table_rows) < 2:
            return ''
        
        html = '  <table style="width: 100%; border-collapse: collapse; margin: 18px 0; border: 1px solid #E5E7EB;">\n'
        
        # 表头
        html += '    <thead>\n      <tr style="background: linear-gradient(135deg, #FFF5F0, #ECFEFF);">\n'
        for cell in table_rows[0]:
            html += f'        <th style="padding: 12px 16px; text-align: left; font-weight: 900; color: #111827; border-right: 1px solid #E5E7EB;">{self._process_inline_markdown(cell)}</th>\n'
        html += '      </tr>\n    </thead>\n'
        
        # 表体
        html += '    <tbody>\n'
        for row in table_rows[1:]:
            html += '      <tr style="border-bottom: 1px solid #E5E7EB;">\n'
            for cell in row:
                html += f'        <td style="padding: 10px 16px; color: #374151; border-right: 1px solid #E5E7EB;">{self._process_inline_markdown(cell)}</td>\n'
            html += '      </tr>\n'
        html += '    </tbody>\n'
        
        html += '  </table>'
        return html
    
    def _render_alert(self, alert: Dict) -> str:
        """渲染警告框"""
        colors = alert['colors']
        html = f"""
  <section style="padding: 16px 20px; border-radius: 12px; margin: 18px 0; background: {colors['bg']}; border-left: 4px solid {colors['border']}; box-shadow: 0 1px 8px rgba(0,0,0,0.05);">
    <section style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
      <span style="font-size: 15px; line-height: 1;">{colors['icon']}</span>
      <span style="font-weight: 800; font-size: 13px; color: {colors['text']}; letter-spacing: 0.5px;">{alert['type']}</span>
    </section>
    <p style="margin: 0; color: #374151; font-size: 13.5px; line-height: 1.75;">{alert['content']}</p>
  </section>
"""
        return html
    
    def _render_code_block(self, code: str) -> str:
        """渲染代码块"""
        # 转义 HTML 特殊字符
        code_escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        html = f"""
  <section style="background: #2B2622; border-radius: 11px; padding: 18px; margin: 18px 0; overflow-x: auto; font-family: 'SF Mono', Monaco, Consolas, 'Courier New', monospace; font-size: 12px; line-height: 1.6; color: #E5E7EB;">
<pre style="margin: 0; white-space: pre-wrap; word-wrap: break-word;"><code>{code_escaped}</code></pre>
  </section>
"""
        return html
    
    def _render_step_block(self, step: Dict) -> str:
        """渲染 STEP 块 —— 无阴影无发光，STEP 01 格式编号"""
        html = f"""
  <section style="margin: 16px 0; background: #ffffff; border-radius: 14px; border: 1px solid rgba({self._hex_to_rgb(self.config['brand_color'])}, 0.18); overflow: hidden;">
    <section style="background: {self.config['brand_color_lighter']}; padding: 10px 18px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid rgba({self._hex_to_rgb(self.config['brand_color'])}, 0.12);">
      <span style="font-size: 10px; font-weight: 800; letter-spacing: 1.5px; color: {self.config['brand_color']}; line-height: 1; text-transform: uppercase;">STEP</span>
      <span style="font-size: 10px; font-weight: 800; color: {self.config['brand_color']}; letter-spacing: 1.5px; line-height: 1;">{step['number'].zfill(2)}</span>
      <span style="width: 1px; height: 14px; background: rgba({self._hex_to_rgb(self.config['brand_color'])}, 0.25);"></span>
      <span style="font-size: 13.5px; font-weight: 800; color: #111827; letter-spacing: -0.2px;">{self._process_inline_markdown(step['title'])}</span>
    </section>
    <section style="padding: 14px 18px;">
      <p style="font-size: 13.5px; color: #4B5563; line-height: 1.8; margin: 0;">{self._process_inline_markdown(step['content'])}</p>
    </section>
  </section>
"""
        return html
    
    def _render_insight_block(self, insight: Dict) -> str:
        """渲染 Insight 块（总结框）"""
        html = f"""
  <section style="margin: 24px 0; padding: 20px 22px; background: #ffffff; border-left: 4px solid {self.config['brand_color']}; border-radius: 0 12px 12px 0; box-shadow: 0 2px 16px rgba({self._hex_to_rgb(self.config['brand_color'])}, 0.08);">
    <section style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
      <span style="font-size: 18px; line-height: 1;">{insight['icon']}</span>
      <span style="font-size: 15px; font-weight: 900; color: {self.config['brand_color']}; letter-spacing: -0.2px;">{self._process_inline_markdown(insight['title'])}</span>
    </section>
    <p style="font-size: 13.5px; color: #374151; line-height: 1.8; margin: 0;">{self._process_inline_markdown(insight['content'])}</p>
  </section>
"""
        return html
    
    def _render_prompt_block(self, content: str) -> str:
        """渲染 Prompt 块"""
        html = f"""
  <section style="margin: 24px 0; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
    <section style="padding: 10px 18px; background: #1E1B18; display: flex; align-items: center; gap: 8px;">
      <span style="width: 10px; height: 10px; background: #FF5F57; border-radius: 50%; display: inline-block;"></span>
      <span style="width: 10px; height: 10px; background: #FFBD2E; border-radius: 50%; display: inline-block;"></span>
      <span style="width: 10px; height: 10px; background: #28C840; border-radius: 50%; display: inline-block;"></span>
      <span style="font-size: 11px; color: rgba(255,255,255,0.4); margin-left: 8px; letter-spacing: 2px; font-weight: 600;">PROMPT</span>
      <span style="font-size: 15px; margin-left: 4px;">🤖</span>
    </section>
    <section style="padding: 18px 20px; background: #2B2622; border: 1px solid #3F3B35; border-top: none; border-radius: 0 0 14px 14px;">
      <p style="font-size: 13px; color: #E5E7EB; line-height: 1.85; font-family: 'SF Mono', Monaco, Consolas, 'Courier New', monospace; margin: 0; white-space: pre-wrap; word-wrap: break-word;">{self._process_inline_markdown(content)}</p>
    </section>
  </section>
"""
        return html
    
    def _render_image(self, markdown_line: str) -> str:
        """渲染图片（带圆角容器），embed_images=True 时自动将本地图片转 base64"""
        import base64, mimetypes
        match = re.match(r'!\[(.*?)\]\((.*?)\)', markdown_line)
        if match:
            alt_text = match.group(1)
            src = match.group(2)

            # 尝试将本地路径转为 base64（embed_images 开启，或路径不是 http/https 时均处理）
            if self.embed_images and not src.startswith('http://') and not src.startswith('https://'):
                local_path = Path(src)
                if not local_path.is_absolute():
                    # 相对路径：尝试相对当前工作目录解析
                    local_path = Path.cwd() / local_path
                if local_path.exists():
                    mime, _ = mimetypes.guess_type(str(local_path))
                    mime = mime or 'image/jpeg'
                    with open(local_path, 'rb') as f:
                        b64 = base64.b64encode(f.read()).decode('utf-8')
                    src = f"data:{mime};base64,{b64}"

            html = f"""
  <section style="margin: 24px 0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); line-height: 0;">
    <img src="{src}" alt="{alt_text}" style="width: 100%; max-width: 100%; display: block; border-radius: 16px;" />
  </section>
"""
            return html
        return ''
    
    def _render_footer(self) -> str:
        """渲染结尾部分"""
        bc = self.config['brand_color']
        bc_rgb = self._hex_to_rgb(bc)
        # SVG 图标（灰色点赞、灰色收藏、主色转发）
        icon_like = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3H14z" stroke="#999999" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" stroke="#999999" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        icon_star = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="#999999" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        icon_share = f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" stroke="{bc}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><polyline points="16 6 12 2 8 6" stroke="{bc}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><line x1="12" y1="2" x2="12" y2="15" stroke="{bc}" stroke-width="1.8" stroke-linecap="round"/></svg>'
        html = f"""
  <section style="height: 1px; background: linear-gradient(to right, rgba({bc_rgb}, 0.2), transparent); margin: 36px 0;"></section>

  <section style="margin: 36px 0 16px; padding: 26px 22px; background: #fff8f5; border-radius: 16px; border: 1px solid rgba({bc_rgb}, 0.12); text-align: center;">
    <p style="font-size: 15px; font-weight: 700; color: #1a1a1a; margin: 0 0 6px; line-height: 1.5;">如果这篇文章对你有帮助</p>
    <p style="font-size: 13px; color: #999999; margin: 0 0 20px; line-height: 1.6;">点个赞、收藏起来，或者转发给需要的朋友</p>
    <section style="display: table; margin: 0 auto;">
      <section style="display: table-cell; vertical-align: middle; padding: 0 18px; text-align: center;">
        {icon_like}
        <span style="font-size: 12px; color: #666666; margin-top: 6px; display: block;">点赞</span>
      </section>
      <section style="display: table-cell; vertical-align: middle; padding: 0 18px; text-align: center;">
        {icon_star}
        <span style="font-size: 12px; color: #666666; margin-top: 6px; display: block;">收藏</span>
      </section>
      <section style="display: table-cell; vertical-align: middle; padding: 0 18px; text-align: center;">
        {icon_share}
        <span style="font-size: 12px; font-weight: 700; color: {bc}; margin-top: 6px; display: block;">转发</span>
      </section>
    </section>
  </section>
"""
        return html
    
    def _generate_html_head(self) -> str:
        """生成 HTML head"""
        bc = self.config['brand_color']
        bc_light = self.config['brand_color_light']
        bc_dark = self.config['brand_color_dark']
        bc_lighter = self.config['brand_color_lighter']

        # 预设主题色板（每个主题包含完整的4色体系）
        themes = [
            {"name": "桃色",   "bc": "#DE7356", "light": "#E8956D", "dark": "#B54432", "lighter": "#FFF5F0"},
            {"name": "清华紫", "bc": "#660874", "light": "#9B3BAE", "dark": "#4A0554", "lighter": "#F5EDF8"},
            {"name": "深海蓝", "bc": "#1D6FA4", "light": "#3A8FC2", "dark": "#124D75", "lighter": "#EBF5FB"},
            {"name": "墨绿",   "bc": "#1A7A5E", "light": "#2E9E7A", "dark": "#0F5442", "lighter": "#E8F8F3"},
            {"name": "暗金",   "bc": "#B8860B", "light": "#D4A017", "dark": "#8B6508", "lighter": "#FDF6E3"},
            {"name": "石墨",   "bc": "#374151", "light": "#4B5563", "dark": "#1F2937", "lighter": "#F3F4F6"},
        ]

        # 生成色板 JS 数据
        themes_js = str(themes).replace("'", '"').replace('True', 'true').replace('False', 'false')

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>飞哥公众号文章</title>
<style>
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    background-color: #ffffff;
    color: #374151;
    line-height: 1.75;
    letter-spacing: 0.5px;
    font-size: 15px;
  }}

  .container {{
    max-width: 677px;
    margin: 0 auto;
    background: #ffffff;
    padding: 20px 0;
  }}

  @media (max-width: 600px) {{
    .container {{
      padding: 0;
    }}
  }}

  /* 顶部工具栏 */
  #toolbar {{
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 999;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
  }}

  /* 主题色切换按钮 */
  #theme-btn {{
    background: #ffffff;
    border: 1.5px solid rgba(0,0,0,0.12);
    border-radius: 20px;
    padding: 7px 13px;
    font-size: 13px;
    font-weight: 600;
    color: #374151;
    cursor: pointer;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
    white-space: nowrap;
  }}
  #theme-btn:hover {{
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  }}
  #theme-dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: {bc};
    flex-shrink: 0;
    transition: background 0.2s;
  }}

  /* 主题色面板 */
  #theme-panel {{
    display: none;
    position: fixed;
    top: 52px;
    right: 16px;
    z-index: 998;
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 14px;
    padding: 12px 14px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    min-width: 180px;
  }}
  #theme-panel.open {{ display: block; }}
  #theme-panel p {{
    font-size: 11px;
    font-weight: 700;
    color: #9CA3AF;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
    text-transform: uppercase;
  }}
  .theme-options {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .theme-option {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 10px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s;
    border: 1.5px solid transparent;
  }}
  .theme-option:hover {{ background: #F3F4F6; }}
  .theme-option.active {{ border-color: rgba(0,0,0,0.15); background: #F9FAFB; }}
  .theme-swatch {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: inset 0 0 0 1px rgba(0,0,0,0.1);
  }}
  .theme-name {{
    font-size: 13px;
    font-weight: 500;
    color: #374151;
  }}

  /* 复制按钮 */
  #copy-btn {{
    background: #ffffff;
    border: 1.5px solid rgba(222,115,86,0.35);
    border-radius: 20px;
    padding: 7px 16px;
    font-size: 13px;
    font-weight: 600;
    color: #DE7356;
    cursor: pointer;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
    white-space: nowrap;
  }}
  #copy-btn:hover {{
    background: #DE7356;
    color: #ffffff;
    border-color: #DE7356;
  }}
  #copy-btn.copied {{
    background: #22C55E;
    color: #ffffff;
    border-color: #22C55E;
  }}
</style>
<script>
  // 主题色配置
  var THEMES = {themes_js};
  var currentThemeIdx = -1; // -1 = 自定义（当前文件颜色）

  // 记录初始品牌色（从当前文档中读取）
  var ORIGINAL_COLORS = {{
    bc: "{bc}",
    light: "{bc_light}",
    dark: "{bc_dark}",
    lighter: "{bc_lighter}"
  }};

  function hexToRgb(hex) {{
    var r = parseInt(hex.slice(1,3),16);
    var g = parseInt(hex.slice(3,5),16);
    var b = parseInt(hex.slice(5,7),16);
    return r+','+g+','+b;
  }}

  function escapeReg(s) {{
    return s.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&');
  }}

  function applyTheme(theme, idx) {{
    var container = document.querySelector('.container');
    if (!container) return;

    var html = container.innerHTML;
    var from = (idx === -1) ? ORIGINAL_COLORS : {{
      bc: THEMES[idx].bc, light: THEMES[idx].light,
      dark: THEMES[idx].dark, lighter: THEMES[idx].lighter
    }};
    // 确定"当前颜色"（从上次应用的主题取）
    var cur = (currentThemeIdx === -1) ? ORIGINAL_COLORS : {{
      bc: THEMES[currentThemeIdx].bc, light: THEMES[currentThemeIdx].light,
      dark: THEMES[currentThemeIdx].dark, lighter: THEMES[currentThemeIdx].lighter
    }};

    var to = theme;

    // 替换顺序：lighter > dark > light > bc（避免短色值被提前替换）
    var pairs = [
      [cur.lighter, to.lighter],
      [cur.dark,    to.dark],
      [cur.light,   to.light],
      [cur.bc,      to.bc],
      // rgb 形式
      [hexToRgb(cur.lighter), hexToRgb(to.lighter)],
      [hexToRgb(cur.dark),    hexToRgb(to.dark)],
      [hexToRgb(cur.light),   hexToRgb(to.light)],
      [hexToRgb(cur.bc),      hexToRgb(to.bc)],
    ];

    for (var i = 0; i < pairs.length; i++) {{
      if (pairs[i][0] !== pairs[i][1]) {{
        html = html.split(pairs[i][0].toUpperCase()).join(pairs[i][1]);
        html = html.split(pairs[i][0].toLowerCase()).join(pairs[i][1]);
        html = html.split(pairs[i][0]).join(pairs[i][1]);
      }}
    }}

    container.innerHTML = html;
    currentThemeIdx = idx;

    // 更新色点和复制按钮颜色
    var dot = document.getElementById('theme-dot');
    if (dot) dot.style.background = to.bc;
    var copyBtn = document.getElementById('copy-btn');
    if (copyBtn) {{
      copyBtn.style.color = to.bc;
      copyBtn.style.borderColor = to.bc+'55';
    }}
    // 更新 active 状态
    document.querySelectorAll('.theme-option').forEach(function(el, i) {{
      el.classList.toggle('active', i === idx);
    }});
  }}

  function togglePanel() {{
    var panel = document.getElementById('theme-panel');
    panel.classList.toggle('open');
  }}

  function closePanel(e) {{
    var panel = document.getElementById('theme-panel');
    var btn = document.getElementById('theme-btn');
    if (!panel.contains(e.target) && !btn.contains(e.target)) {{
      panel.classList.remove('open');
    }}
  }}

  function copyArticle() {{
    var btn = document.getElementById('copy-btn');
    var container = document.querySelector('.container');
    if (!container) return;
    if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) {{
      var html = container.innerHTML;
      var blob = new Blob([html], {{type: 'text/html'}});
      var plainBlob = new Blob([container.innerText], {{type: 'text/plain'}});
      navigator.clipboard.write([
        new ClipboardItem({{'text/html': blob, 'text/plain': plainBlob}})
      ]).then(function() {{ showCopied(btn); }}).catch(function() {{ fallbackCopy(btn, container); }});
    }} else {{
      fallbackCopy(btn, container);
    }}
  }}

  function fallbackCopy(btn, container) {{
    var range = document.createRange();
    range.selectNodeContents(container);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    try {{
      document.execCommand('copy');
      showCopied(btn);
    }} catch(e) {{
      alert('复制失败，请手动 Ctrl+A / Cmd+A 全选后复制');
    }}
    sel.removeAllRanges();
  }}

  function showCopied(btn) {{
    btn.classList.add('copied');
    btn.innerHTML = '✓ 已复制';
    setTimeout(function() {{
      btn.classList.remove('copied');
      btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>一键复制';
    }}, 2000);
  }}

  document.addEventListener('DOMContentLoaded', function() {{
    document.addEventListener('click', closePanel);
    // 初始化色板
    var optionsEl = document.querySelector('.theme-options');
    THEMES.forEach(function(t, i) {{
      var div = document.createElement('div');
      div.className = 'theme-option' + (t.bc.toUpperCase() === "{bc}".toUpperCase() ? ' active' : '');
      div.innerHTML = '<span class="theme-swatch" style="background:'+t.bc+'"></span><span class="theme-name">'+t.name+'</span>';
      div.onclick = function(e) {{ e.stopPropagation(); applyTheme(t, i); document.getElementById('theme-panel').classList.remove('open'); }};
      optionsEl.appendChild(div);
      if (t.bc.toUpperCase() === "{bc}".toUpperCase()) currentThemeIdx = i;
    }});
  }});
</script>
</head>
<body>
<div id="toolbar">
  <div id="theme-btn" onclick="event.stopPropagation(); togglePanel()">
    <span id="theme-dot"></span>主题色
  </div>
  <button id="copy-btn" onclick="copyArticle()">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    一键复制
  </button>
</div>
<div id="theme-panel">
  <p>选择主题色</p>
  <div class="theme-options"></div>
</div>"""
    
    def _generate_html_tail(self) -> str:
        """生成 HTML tail"""
        return """</body>
</html>"""
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """将 16 进制颜色转换为 RGB"""
        hex_color = hex_color.lstrip('#')
        return ','.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))


def main():
    parser = argparse.ArgumentParser(
        description='飞哥公众号排版格式化器 - Markdown 转 HTML'
    )
    parser.add_argument('input', help='输入 Markdown 文件路径')
    parser.add_argument(
        '--output', '-o',
        help='输出 HTML 文件路径 (默认：input.html)',
        default=None
    )
    parser.add_argument(
        '--brand-color', '-c',
        help='品牌主色色值 (默认：#DE7356)',
        default='#DE7356'
    )
    parser.add_argument(
        '--embed-images', '-e',
        help='将本地图片转为 base64 内嵌（方便复制粘贴到公众号编辑器，默认开启）',
        action='store_true',
        default=True
    )
    
    args = parser.parse_args()
    
    # 读取输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f'错误：文件不存在 {args.input}')
        sys.exit(1)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 转换
    formatter = FeigePFormatter(config={
        'brand_color': args.brand_color,
        'embed_images': args.embed_images,
    })
    html_content = formatter.markdown_to_html(markdown_content)
    
    # 写入输出文件
    output_path = args.output or str(input_path).replace('.md', '.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'✅ 转换完成！')
    print(f'📁 输入：{input_path}')
    print(f'📁 输出：{output_path}')
    print(f'🎨 品牌色：{args.brand_color}')
    if args.embed_images:
        print(f'🖼️  图片已内嵌为 base64')


if __name__ == '__main__':
    main()
