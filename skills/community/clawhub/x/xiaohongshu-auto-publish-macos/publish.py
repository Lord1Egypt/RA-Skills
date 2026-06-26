#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书自动发布脚本
基于OpenClaw浏览器自动化
"""

import os
import sys
import time
import requests
from datetime import datetime

# 配置
DESKTOP = os.path.expanduser("~/Desktop")
UPLOAD_DIR = "/tmp/openclaw/uploads"

# 默认笔记内容
DEFAULT_TITLE = "AI时代来临！没有技能将被淘汰？"
DEFAULT_CONTENT = """🔥 未来已来，AI正在悄悄取代这些工作...

🤖 流水线工人 → 被机器人取代
📝 基础文案 → 被ChatGPT取代
🧮 基础会计 → 被AI财务系统取代

但有一样东西AI永远无法替代——专业技能！

💪 学一门真正的技术，才是应对未来的底气！

职业教育，让你掌握一技之长！
#AI时代 #职业教育 #技能学习 #未来生存"""

def download_image(keyword="AI education technology", filename="cover.jpg"):
    """下载图片到桌面"""
    print(f"[1/4] 搜索图片: {keyword}")
    
    # 使用免费图库
    urls = [
        f"https://picsum.photos/800/1000",
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                filepath = os.path.join(DESKTOP, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"  ✅ 图片已保存: {filepath}")
                return filepath
        except Exception as e:
            print(f"  ⚠️ {url} 失败: {e}")
    
    return None

def prepare_upload(image_path):
    """准备上传"""
    print(f"[2/4] 准备图片...")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    if image_path and os.path.exists(image_path):
        upload_path = os.path.join(UPLOAD_DIR, "cover.jpg")
        import shutil
        shutil.copy(image_path, upload_path)
        print(f"  ✅ 已复制到: {upload_path}")
        return upload_path
    return None

def main(keyword=None, title=None, content=None):
    """主函数"""
    print("="*50)
    print("小红书自动发布工具")
    print("="*50)
    
    # 使用参数或默认值
    title = title or DEFAULT_TITLE
    content = content or DEFAULT_CONTENT
    keyword = keyword or "AI artificial intelligence education"
    
    # 1. 下载图片
    image_path = download_image(keyword)
    
    # 2. 准备上传
    upload_path = prepare_upload(image_path)
    
    # 3. 输出说明
    print(f"\n[3/4] 图片准备完成!")
    print(f"  标题: {title[:30]}...")
    print(f"  图片: {upload_path or '无'}")
    print(f"\n[4/4] 请在浏览器中完成以下操作:")
    print(f"  1. 打开 https://creator.xiaohongshu.com/publish/publish")
    print(f"  2. 点击上传图片")
    print(f"  3. 填写标题: {title}")
    print(f"  4. 填写正文")
    print(f"  5. 点击发布")
    print("\n✅ 准备完成!")

if __name__ == "__main__":
    # 支持命令行参数
    kw = sys.argv[1] if len(sys.argv) > 1 else None
    main(keyword=kw)
