# -*- coding: utf-8 -*-
"""
共用侧边栏和样式模块
所有学习页面共享的导航栏、CSS 和 HTML 框架。
"""

NAV_ITEMS = [
    {"file": "lesson.html", "icon": "📖", "label": "课文学习"},
    {"file": "quiz.html", "icon": "📝", "label": "单词测验"},
    {"file": "reading_quiz.html", "icon": "📚", "label": "原文理解"},
    {"file": "sentence_quiz.html", "icon": "✏️", "label": "句子测验"},
]


def sidebar_html(active_file):
    """生成侧边栏 HTML"""
    items = ""
    for nav in NAV_ITEMS:
        cls = "active" if nav["file"] == active_file else ""
        items += f'      <a href="{nav["file"]}" class="nav-item {cls}">{nav["icon"]} {nav["label"]}</a>\n'

    return f'''
  <nav class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>📚 英语学习</h2>
    </div>
{items}
  </nav>'''


def page_css():
    """返回所有页面共用的 CSS"""
    return '''
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f5f5f5;
      color: #333;
      display: flex;
      min-height: 100vh;
    }
    /* ── 侧边栏 ── */
    .sidebar {
      position: fixed;
      left: 0; top: 0;
      width: 200px;
      height: 100vh;
      background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
      color: #fff;
      padding: 20px 0;
      z-index: 100;
      display: flex;
      flex-direction: column;
    }
    .sidebar-header {
      padding: 10px 20px 24px;
      border-bottom: 1px solid rgba(255,255,255,0.1);
      margin-bottom: 12px;
    }
    .sidebar-header h2 { font-size: 1.1em; }
    .nav-item {
      display: block;
      padding: 12px 20px;
      color: rgba(255,255,255,0.7);
      text-decoration: none;
      font-size: 0.95em;
      transition: all 0.2s;
      border-left: 3px solid transparent;
    }
    .nav-item:hover {
      background: rgba(255,255,255,0.08);
      color: #fff;
    }
    .nav-item.active {
      background: rgba(255,255,255,0.12);
      color: #fff;
      border-left-color: #667eea;
      font-weight: 600;
    }
    /* ── 主内容 ── */
    .main-content {
      margin-left: 200px;
      flex: 1;
      padding: 20px;
      min-height: 100vh;
    }
    .page-title {
      font-size: 1.5em;
      color: #1a73e8;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 2px solid #e9ecef;
    }
    .card {
      background: #fff;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .card h2 {
      margin-bottom: 16px;
      color: #333;
      font-size: 1.15em;
    }
    .card p { margin-bottom: 10px; }
    /* ── 响应式 ── */
    @media (max-width: 768px) {
      .sidebar {
        width: 100%;
        height: auto;
        position: relative;
        flex-direction: row;
        flex-wrap: wrap;
        padding: 0;
      }
      .sidebar-header { display: none; }
      .nav-item {
        flex: 1;
        text-align: center;
        padding: 10px 6px;
        border-left: none;
        border-bottom: 3px solid transparent;
        font-size: 0.85em;
      }
      .nav-item.active { border-bottom-color: #667eea; border-left: none; }
      .main-content { margin-left: 0; }
    }'''


def wrap_html(title, active_file, body_content, extra_css="", extra_js=""):
    """将内容包装为完整的带侧边栏 HTML 页面"""
    sidebar = sidebar_html(active_file)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>{page_css()}{extra_css}</style>
</head>
<body>
{sidebar}
  <div class="main-content">
{body_content}
  </div>
  <script>{extra_js}</script>
</body>
</html>'''


def esc_html(text):
    """HTML 转义"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))
