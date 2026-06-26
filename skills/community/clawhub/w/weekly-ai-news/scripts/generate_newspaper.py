#!/usr/bin/env python3
"""
旧报纸风格 HTML 生成器 - 优化版
Usage: python generate_newspaper.py --input news.json --output weekly-ai-news.html
"""

import sys
import json
import argparse
import re
import html as html_mod
from datetime import datetime, timedelta

# 期号起始日期（2026-01-05 为第001期，每7天递增）
EPOCH = datetime(2026, 1, 5)

def escape_html(text):
    """转义 HTML 特殊字符，防止 XSS"""
    if not text:
        return ""
    return html_mod.escape(str(text), quote=True)

def safe_date(published, fallback=""):
    """安全提取日期前10个字符"""
    if not published or len(published) < 10:
        return fallback
    return escape_html(published[:10])

def clean_text(text):
    """清理文本"""
    if not text:
        return ""
    # 移除 HTML 标签
    text = re.sub(r'<[^\u003e]+>', '', text)
    # 移除多余空白
    text = ' '.join(text.split())
    return text.strip()

def truncate_text(text, max_len=200):
    """截断文本，保持完整句子"""
    text = clean_text(text)
    if len(text) <= max_len:
        return text
    # 找到最后一个完整句子
    truncated = text[:max_len]
    last_period = max(truncated.rfind('。'), truncated.rfind('.'), truncated.rfind('！'), truncated.rfind('!'))
    if last_period > max_len * 0.6:
        return truncated[:last_period + 1]
    return truncated + "..."

def generate_newspaper_html(news_data, output_file):
    """生成旧报纸风格的 HTML"""
    
    # 计算周报日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    date_range = f"{start_date.strftime('%Y.%m.%d')} - {end_date.strftime('%Y.%m.%d')}"
    issue_number = f"第{max(1, (end_date - EPOCH).days // 7 + 1):03d}期"

    # 分类新闻（头条1条，其余依次填充各区域，不遗漏）
    headline = news_data[0] if len(news_data) > 0 else None
    main_news = news_data[1:5]      # 主要新闻（左栏+中栏）
    side_news = news_data[5:9]      # 侧边栏新闻
    briefs = news_data[9:15]        # 简讯
    
    # HTML 模板
    html = f'''&lt;!DOCTYPE html&gt;
&lt;html lang="zh-CN"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
    &lt;title&gt;每周AI前沿动态 - {date_range}&lt;/title&gt;
    &lt;style&gt;
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&amp;display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Serif SC', 'SimSun', '宋体', Georgia, serif;
            background: #e8dcc8;
            background-image: 
                url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .newspaper {{
            max-width: 1100px;
            margin: 0 auto;
            background: #faf6ed;
            box-shadow: 
                0 0 0 1px #c9b896,
                0 0 0 8px #e8dcc8,
                0 0 0 9px #b8a88a,
                0 20px 60px rgba(0,0,0,0.4);
            padding: 30px 40px;
            position: relative;
        }}
        
        /* 报纸纹理效果 */
        .newspaper::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(139, 119, 89, 0.02) 2px,
                    rgba(139, 119, 89, 0.02) 4px
                );
            pointer-events: none;
            z-index: 1;
        }}
        
        .content-wrapper {{
            position: relative;
            z-index: 2;
        }}
        
        /* 顶部信息栏 */
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #2c2416;
            margin-bottom: 15px;
            font-size: 11px;
            color: #5a4a3a;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* 报纸标题 */
        .masthead {{
            text-align: center;
            padding: 25px 0 20px;
            border-bottom: 3px double #2c2416;
            margin-bottom: 15px;
        }}
        
        .masthead h1 {{
            font-size: 64px;
            font-weight: 900;
            letter-spacing: 12px;
            color: #1a1410;
            margin-bottom: 8px;
            font-family: 'Noto Serif SC', serif;
        }}
        
        .masthead .tagline {{
            font-size: 14px;
            font-style: italic;
            color: #6a5a4a;
            letter-spacing: 4px;
        }}
        
        /* 日期和期号 */
        .issue-info {{
            display: flex;
            justify-content: center;
            gap: 60px;
            padding: 12px 0;
            border-bottom: 2px solid #2c2416;
            margin-bottom: 25px;
            font-size: 13px;
            font-weight: 600;
        }}
        
        .issue-info span {{
            color: #3a3020;
        }}
        
        /* 主布局 - 经典报纸三栏布局 */
        .main-layout {{
            display: grid;
            grid-template-columns: 1fr 1fr 280px;
            gap: 25px;
            margin-bottom: 25px;
        }}
        
        .left-column {{
            border-right: 1px solid #c9b896;
            padding-right: 25px;
        }}
        
        .center-column {{
            border-right: 1px solid #c9b896;
            padding-right: 25px;
        }}
        
        .right-column {{
            padding-left: 5px;
        }}
        
        /* 头条新闻 */
        .headline {{
            text-align: center;
            padding: 20px 15px;
            margin-bottom: 25px;
            border: 2px solid #2c2416;
            background: linear-gradient(135deg, #f5f0e6 0%, #faf6ed 100%);
        }}
        
        .headline .news-source {{
            font-size: 11px;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}
        
        .headline .news-title {{
            font-size: 28px;
            font-weight: 900;
            line-height: 1.3;
            margin: 12px 0;
        }}
        
        .headline .news-date {{
            font-size: 11px;
            margin-bottom: 12px;
        }}
        
        .headline .news-desc {{
            font-size: 14px;
            line-height: 1.8;
            text-align: justify;
            padding: 0 10px;
        }}
        
        /* 首字下沉 */
        .headline .news-desc::first-letter {{
            float: left;
            font-size: 56px;
            line-height: 0.8;
            padding: 8px 10px 0 0;
            font-weight: 900;
            color: #1a1410;
        }}
        
        /* 普通新闻条目 */
        .news-item {{
            margin-bottom: 22px;
            padding-bottom: 18px;
            border-bottom: 1px solid #d4c4a8;
        }}
        
        .news-item:last-child {{
            border-bottom: none;
        }}
        
        .news-source {{
            font-size: 9px;
            font-weight: 700;
            color: #8b7355;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 5px;
        }}
        
        .news-title {{
            font-size: 17px;
            font-weight: 700;
            line-height: 1.35;
            color: #1a1410;
            margin-bottom: 6px;
        }}
        
        .news-title a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .news-title a:hover {{
            text-decoration: underline;
        }}
        
        .news-date {{
            font-size: 10px;
            color: #8b7355;
            font-style: italic;
            margin-bottom: 8px;
        }}
        
        .news-desc {{
            font-size: 13px;
            line-height: 1.7;
            color: #3a3020;
            text-align: justify;
        }}
        
        /* 简讯区域 */
        .briefs-section {{
            border-top: 2px solid #2c2416;
            padding-top: 15px;
            margin-top: 20px;
        }}
        
        .briefs-title {{
            font-size: 16px;
            font-weight: 900;
            text-align: center;
            margin-bottom: 15px;
            letter-spacing: 4px;
        }}
        
        .briefs-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }}
        
        .brief-item {{
            font-size: 12px;
            line-height: 1.6;
        }}
        
        .brief-item .brief-title {{
            font-weight: 700;
            margin-bottom: 4px;
        }}
        
        .brief-item .brief-source {{
            font-size: 9px;
            color: #8b7355;
        }}

        /* 右栏短讯标题 */
        .sidebar-heading {{
            font-size: 12px;
            font-weight: 900;
            text-align: center;
            margin-bottom: 15px;
            border-bottom: 1px solid #2c2416;
            padding-bottom: 8px;
        }}

        .sidebar-item {{
            border-bottom: 1px dotted #c9b896;
            padding-bottom: 12px;
            margin-bottom: 12px;
        }}

        .sidebar-item:last-child {{
            border-bottom: none;
        }}

        .sidebar-item .news-title {{
            font-size: 13px;
        }}

        /* 装饰分隔 */
        .ornament {{
            text-align: center;
            font-size: 14px;
            color: #a09070;
            margin: 20px 0;
            letter-spacing: 8px;
        }}
        
        /* 页脚 */
        .footer {{
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #2c2416;
            text-align: center;
            font-size: 10px;
            color: #8b7355;
            line-height: 1.8;
        }}
        
        /* 无内容提示 */
        .no-content {{
            text-align: center;
            padding: 60px;
            font-size: 16px;
            color: #8b7355;
        }}
        
        /* 响应式 */
        @media (max-width: 900px) {{
            .main-layout {{
                grid-template-columns: 1fr 1fr;
            }}
            .right-column {{
                display: none;
            }}
        }}
        
        @media (max-width: 600px) {{
            .main-layout {{
                grid-template-columns: 1fr;
            }}
            .left-column, .center-column {{
                border-right: none;
                padding-right: 0;
            }}
            .briefs-grid {{
                grid-template-columns: 1fr;
            }}
            .masthead h1 {{
                font-size: 42px;
                letter-spacing: 6px;
            }}
        }}
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="newspaper"&gt;
        &lt;div class="content-wrapper"&gt;
            &lt;div class="header-top"&gt;
                &lt;span&gt;AI WEEKLY INTELLIGENCE&lt;/span&gt;
                &lt;span&gt;专注于应用前沿的人工智能资讯&lt;/span&gt;
                &lt;span&gt;VOL. {issue_number}&lt;/span&gt;
            &lt;/div&gt;
            
            &lt;div class="masthead"&gt;
                &lt;h1&gt;每周AI前沿动态&lt;/h1&gt;
                &lt;div class="tagline"&gt;Weekly AI Frontier Dynamics&lt;/div&gt;
            &lt;/div&gt;
            
            &lt;div class="issue-info"&gt;
                &lt;span&gt;发行日期: {end_date.strftime('%Y年%m月%d日')}&lt;/span&gt;
                &lt;span&gt;{issue_number}&lt;/span&gt;
                &lt;span&gt;本期精选 {len(news_data)} 条&lt;/span&gt;
            &lt;/div&gt;
'''
    
    if not news_data:
        html += '            <div class="no-content">本周暂无符合条件的 AI 应用动态</div>\n'
    else:
        # 头条区域
        if headline:
            desc = escape_html(truncate_text(headline.get("description", ""), 280))
            html += f'''            <div class="headline">
                <div class="news-source">{escape_html(headline["source"])}</div>
                <div class="news-title">
                    <a href="{escape_html(headline.get("link", ""))}" target="_blank">{escape_html(headline["title"])}</a>
                </div>
                <div class="news-date">{safe_date(headline.get("published"))}</div>
                <div class="news-desc">{desc}</div>
            </div>
'''

        # 确定各栏内容
        left_items = main_news[:2]
        center_items = main_news[2:]
        sidebar_items = side_news

        # 只在有内容时渲染三栏布局
        if left_items or center_items or sidebar_items:
            html += '            <div class="main-layout">\n'

            # 左栏
            html += '                <div class="left-column">\n'
            for news in left_items:
                desc = escape_html(truncate_text(news.get("description", ""), 150))
                html += f'''                    <div class="news-item">
                        <div class="news-source">{escape_html(news["source"])}</div>
                        <div class="news-title">
                            <a href="{escape_html(news.get("link", ""))}" target="_blank">{escape_html(news["title"])}</a>
                        </div>
                        <div class="news-date">{safe_date(news.get("published"))}</div>
                        <div class="news-desc">{desc}</div>
                    </div>
'''
            html += '                </div>\n'

            # 中栏
            html += '                <div class="center-column">\n'
            for news in center_items:
                desc = escape_html(truncate_text(news.get("description", ""), 150))
                html += f'''                    <div class="news-item">
                        <div class="news-source">{escape_html(news["source"])}</div>
                        <div class="news-title">
                            <a href="{escape_html(news.get("link", ""))}" target="_blank">{escape_html(news["title"])}</a>
                        </div>
                        <div class="news-date">{safe_date(news.get("published"))}</div>
                        <div class="news-desc">{desc}</div>
                    </div>
'''
            html += '                </div>\n'

            # 右栏 - 短讯（有内容才渲染）
            if sidebar_items:
                html += '                <div class="right-column">\n'
                html += '                    <div class="sidebar-heading">短讯</div>\n'
                for news in sidebar_items:
                    html += f'''                    <div class="sidebar-item">
                        <div class="news-title">
                            <a href="{escape_html(news.get("link", ""))}" target="_blank">{escape_html(news["title"])}</a>
                        </div>
                        <div class="news-date">{escape_html(news.get("source", ""))} · {safe_date(news.get("published"))}</div>
                    </div>
'''
                html += '                </div>\n'

            html += '            </div>\n'

        # 更多简讯
        if briefs:
            html += '            <div class="briefs-section">\n'
            html += '                <div class="briefs-title">更 多 动 态</div>\n'
            html += '                <div class="briefs-grid">\n'
            for news in briefs:
                html += f'''                    <div class="brief-item">
                        <div class="brief-title">{escape_html(news["title"])}</div>
                        <div class="brief-source">{escape_html(news.get("source", ""))} · {safe_date(news.get("published"))}</div>
                    </div>
'''
            html += '                </div>\n'
            html += '            </div>\n'
    
    html += f'''            
            &lt;div class="footer"&gt;
                &lt;p&gt;&lt;strong&gt;每周AI前沿动态&lt;/strong&gt; 由 AI 自动生成 · 筛选应用向 AI 新闻 · 剔除纯技术内容&lt;/p&gt;
                &lt;p&gt;数据来源: 阮一峰的网络日志、36氪、虎嗅科技、钛媒体、IT之家&lt;/p&gt;
                &lt;p style="margin-top: 8px; font-style: italic;"&gt;{date_range}&lt;/p&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML 已生成: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='生成旧报纸风格的 AI 新闻周报')
    parser.add_argument('--input', '-i', required=True, help='输入 JSON 文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出 HTML 文件路径')
    args = parser.parse_args()
    
    # 读取新闻数据
    with open(args.input, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    
    generate_newspaper_html(news_data, args.output)

if __name__ == "__main__":
    main()
