#!/usr/bin/env python3
"""
生成20个不同主题的封面（马卡龙配色）
"""

import os

# 20个主题的封面模板（马卡龙配色）
COVERS = {
    # ===== 原有 8 个主题 =====
    'minimal': {
        'name': '极简商务',
        'bg': 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
        'accent': '#0984e3',
        'title': '极简商务主题'
    },
    'warm': {
        'name': '温暖文艺',
        'bg': 'linear-gradient(135deg, #8b6914 0%, #d4c4a8 100%)',
        'accent': '#f5f0e8',
        'title': '温暖文艺主题'
    },
    'tech': {
        'name': '科技现代',
        'bg': 'linear-gradient(135deg, #0d1117 0%, #161b22 50%, #21262d 100%)',
        'accent': '#58a6ff',
        'title': '科技现代主题'
    },
    'fresh': {
        'name': '活泼清新',
        'bg': 'linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%)',
        'accent': '#ffffff',
        'title': '活泼清新主题'
    },
    'magazine': {
        'name': '杂志高级',
        'bg': 'linear-gradient(135deg, #1a1a1a 0%, #3d3d3d 50%, #5a5a5a 100%)',
        'accent': '#c0a080',
        'title': '杂志高级主题'
    },
    'academic': {
        'name': '学术专业',
        'bg': 'linear-gradient(135deg, #1a365d 0%, #2d3748 50%, #1a365d 100%)',
        'accent': '#4299e1',
        'title': '学术专业主题'
    },
    'retro': {
        'name': '复古经典',
        'bg': 'linear-gradient(135deg, #5c3d2e 0%, #8b6914 50%, #c9a86c 100%)',
        'accent': '#f5f0e8',
        'title': '复古经典主题'
    },
    'dark': {
        'name': '暗黑极简',
        'bg': 'linear-gradient(135deg, #1a202c 0%, #2d3748 50%, #1a202c 100%)',
        'accent': '#63b3ed',
        'title': '暗黑极简主题'
    },
    # ===== 马卡龙主题 12 个 =====
    'macaron_pink': {
        'name': '马卡龙粉',
        'bg': 'linear-gradient(135deg, #fef6f9 0%, #fce4ec 50%, #f8bbd9 100%)',
        'accent': '#d4859a',
        'title': '马卡龙粉色主题'
    },
    'macaron_blue': {
        'name': '马卡龙蓝',
        'bg': 'linear-gradient(135deg, #f0f9ff 0%, #dbeafe 50%, #bfdbfe 100%)',
        'accent': '#4299e1',
        'title': '马卡龙蓝色主题'
    },
    'macaron_mint': {
        'name': '马卡龙薄荷',
        'bg': 'linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 50%, #99f6e4 100%)',
        'accent': '#14b8a6',
        'title': '马卡龙薄荷主题'
    },
    'macaron_lavender': {
        'name': '马卡龙薰衣草',
        'bg': 'linear-gradient(135deg, #faf5ff 0%, #ede9fe 50%, #ddd6fe 100%)',
        'accent': '#a78bfa',
        'title': '马卡龙薰衣草主题'
    },
    'macaron_peach': {
        'name': '马卡龙蜜桃',
        'bg': 'linear-gradient(135deg, #fff7ed 0%, #ffedd5 50%, #fed7aa 100%)',
        'accent': '#f97316',
        'title': '马卡龙蜜桃主题'
    },
    'macaron_lemon': {
        'name': '马卡龙柠檬',
        'bg': 'linear-gradient(135deg, #fefce8 0%, #fef9c3 50%, #fef08a 100%)',
        'accent': '#eab308',
        'title': '马卡龙柠檬主题'
    },
    'macaron_coral': {
        'name': '马卡龙珊瑚',
        'bg': 'linear-gradient(135deg, #fff5f5 0%, #fee2e2 50%, #fecaca 100%)',
        'accent': '#f87171',
        'title': '马卡龙珊瑚主题'
    },
    'macaron_sage': {
        'name': '马卡龙鼠尾草',
        'bg': 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%)',
        'accent': '#4ade80',
        'title': '马卡龙鼠尾草主题'
    },
    'macaron_lilac': {
        'name': '马卡龙丁香',
        'bg': 'linear-gradient(135deg, #fdf4ff 0%, #fae8ff 50%, #f5d0fe 100%)',
        'accent': '#d946ef',
        'title': '马卡龙丁香主题'
    },
    'macaron_cream': {
        'name': '马卡龙奶油',
        'bg': 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 50%, #fde68a 100%)',
        'accent': '#d4a574',
        'title': '马卡龙奶油主题'
    },
    'macaron_sky': {
        'name': '马卡龙天空',
        'bg': 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%)',
        'accent': '#38bdf8',
        'title': '马卡龙天空主题'
    },
    'macaron_rose': {
        'name': '马卡龙玫瑰',
        'bg': 'linear-gradient(135deg, #fdf2f8 0%, #fce7f3 50%, #fbcfe8 100%)',
        'accent': '#ec4899',
        'title': '马卡龙玫瑰主题'
    }
}]

def generate_cover_html(theme_key, theme_data):
    """生成单个封面的HTML"""
    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ 
    background: #111; 
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    padding: 40px 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}}
.cover {{ 
    width: 900px; 
    height: 383px; 
    background: {theme_data['bg']}; 
    position: relative; 
    overflow: hidden; 
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}
.brand {{
    position: absolute;
    top: 30px;
    left: 40px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.brand-icon {{
    width: 40px;
    height: 40px;
    background: {theme_data['accent']};
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}}
.brand-text {{
    color: {theme_data['accent']};
    font-size: 18px;
    font-weight: 500;
}}
.title {{
    color: {theme_data['accent']};
    font-size: 48px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 2px;
    margin-bottom: 20px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}}
.subtitle {{
    color: {theme_data['accent']};
    font-size: 24px;
    opacity: 0.9;
    letter-spacing: 1px;
}}
.badge {{
    background: rgba(225, 112, 85, 0.9);
    color: white;
    padding: 10px 30px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 500;
    margin-top: 30px;
    box-shadow: 0 4px 15px rgba(225, 112, 85, 0.4);
}}
.footer {{
    position: absolute;
    bottom: 30px;
    right: 40px;
    color: {theme_data['accent']};
    font-size: 14px;
    opacity: 0.7;
}}
</style>
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>
</head>
<body>
<div class="cover" id="cover">
    <div class="brand">
        <div class="brand-icon">🐾</div>
        <div class="brand-text">小爪</div>
    </div>
    <div class="title">{theme_data['title']}</div>
    <div class="subtitle">排版演示</div>
    <div class="badge">需要审核</div>
    <div class="footer">{theme_data['name']}风格</div>
</div>
<script>
html2canvas(document.getElementById('cover'), {{ scale: 2 }}).then(canvas => {{
    canvas.toBlob(blob => {{
        saveAs(blob, 'cover_{theme_key}_900x383.png');
    }}, 'image/png');
}});
</script>
</body>
</html>'''

def generate_all_covers():
    """生成所有封面"""
    for key, data in COVERS.items():
        filename = f'cover_{key}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(generate_cover_html(key, data))
        print(f"✅ 已生成: {filename} ({data['name']})")
    
    print("\n📖 使用方式:")
    print("1. 用浏览器打开 cover_xxx.html 文件")
    print("2. 自动下载封面图片 (900×383)")
    print("3. 上传到公众号作为封面")

if __name__ == "__main__":
    generate_all_covers()
