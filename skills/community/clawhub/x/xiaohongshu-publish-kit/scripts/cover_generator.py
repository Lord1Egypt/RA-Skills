#!/usr/bin/env python3
"""
小红书封面生成器
Xiaohongshu Cover Generator
"""

import argparse
from pathlib import Path


def generate_tech_cover(title="AI热点速递", date="2026.03.17", style="tech_blue"):
    """生成科技风封面"""
    
    # HTML模板
    if style == "tech_blue":
        # 蓝紫科技风
        gradient = "linear-gradient(135deg,#0a0e27 0%,#1a1a5e 40%,#2d1b69 70%,#0a0e27 100%)"
        title_gradient = "linear-gradient(90deg,#00d2ff,#7b2ff7,#ff6ec7)"
    elif style == "security_red":
        # 红黑安全风
        gradient = "linear-gradient(135deg,#1a0000 0%,#4d0000 40%,#800000 70%,#1a0000 100%)"
        title_gradient = "linear-gradient(90deg,#ff4444,#cc0000,#ff6666)"
    else:
        # 默认蓝紫风格
        gradient = "linear-gradient(135deg,#0a0e27 0%,#1a1a5e 40%,#2d1b69 70%,#0a0e27 100%)"
        title_gradient = "linear-gradient(90deg,#00d2ff,#7b2ff7,#ff6ec7)"
    
    html_content = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
body{{margin:0;width:1080px;height:1440px;background:{gradient};font-family:-apple-system,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
.date{{font-size:42px;opacity:.7;margin-bottom:20px;letter-spacing:4px}}
.title{{font-size:88px;font-weight:900;background:{title_gradient};-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:30px;line-height:1.2}}
.sub{{font-size:38px;opacity:.8;letter-spacing:2px}}
.dots{{margin-top:40px;display:flex;gap:12px}}
.dot{{width:14px;height:14px;border-radius:50%;background:#7b2ff7;opacity:.6}}
.dot:nth-child(2){{background:#00d2ff}}.dot:nth-child(3){{background:#ff6ec7}}
.tag{{margin-top:50px;font-size:32px;opacity:.5;letter-spacing:3px}}
</style></head><body>
<div class="date">{date}</div>
<div class="title">{title}</div>
<div class="sub">国内外AI行业要闻一览</div>
<div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
<div class="tag">#AI #科技前沿 #智能聚合</div>
</body></html>'''
    
    # 保存HTML文件
    temp_dir = Path("/tmp/openclaw")
    temp_dir.mkdir(exist_ok=True)
    
    html_path = temp_dir / "cover.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"封面HTML生成: {html_path}")
    return str(html_path)


def html_to_image(html_path, output_path):
    """将HTML转换为图片（需要浏览器支持）"""
    import subprocess
    import time
    
    try:
        # 启动本地HTTP服务器
        subprocess.run("cd /tmp/openclaw && python3 -m http.server 18811 &", shell=True)
        time.sleep(2)
        
        # 用浏览器打开并截图
        cmd = f"browser --browser-profile openclaw navigate http://localhost:18811/cover.html"
        subprocess.run(cmd, shell=True)
        time.sleep(3)
        
        cmd = f"browser --browser-profile openclaw screenshot --full-page --output {output_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        if result.returncode == 0:
            print(f"封面图片生成: {output_path}")
            return True
        else:
            print(f"截图失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"HTML转图片失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='生成小红书封面图片')
    parser.add_argument('--title', default='AI热点速递', help='封面标题')
    parser.add_argument('--date', default='2026.03.17', help='日期')
    parser.add_argument('--style', default='tech_blue', choices=['tech_blue', 'security_red'], help='封面风格')
    parser.add_argument('--output', default='/tmp/openclaw/uploads/cover.jpg', help='输出文件路径')
    
    args = parser.parse_args()
    
    print("🎨 生成小红书封面...")
    
    # 生成HTML
    html_path = generate_tech_cover(args.title, args.date, args.style)
    
    # 转换为图片
    if html_to_image(html_path, args.output):
        print("✅ 封面生成完成!")
    else:
        print("❌ 封面生成失败")


if __name__ == '__main__':
    main()