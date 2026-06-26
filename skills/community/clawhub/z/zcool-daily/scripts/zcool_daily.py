#!/usr/bin/env python3
"""
站酷每日热门作品推荐脚本

使用方式：
    python3 zcool_daily.py --mode list     # 获取作品列表
"""
import requests
from bs4 import BeautifulSoup
import time
import os
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent

# 分类关键词
CATEGORY_KEYWORDS = {
    "AI绘画": ["AI", "AIGC", "Midjourney", "Stable Diffusion", "SD", "MJ", "人工智能", "生成式"],
    "插画": ["插画", "绘制", "儿插", "商业插画", "人物", "场景"],
    "品牌设计": ["品牌", "VI", "Logo", "标志", "包装", "IP", "Identity"],
    "UI/UX": ["UI", "UX", "界面", "交互", "App", "小程序", "Web"],
    "3D": ["3D", "C4D", "Blender", "建模", "渲染", "三维"],
    "动画": ["动画", "Motion", "动效", "Live2D", "MG", "逐帧"],
    "游戏": ["游戏", "原画", "角色", "场景", "概念"],
    "摄影": ["摄影", "拍摄", "写真", "人像"],
    "海报": ["海报", "Poster", "视觉", "宣传"],
    "手办": ["手办", "雕像", "GK", "BJD", "ARTISAN"],
    "汽车/工业": ["汽车", "工业", "产品", "交通工具"],
    "电商": ["电商", "详情页", "主图"],
}

def classify_work(title, description):
    """作品分类"""
    text = (title + " " + (description or "")).upper()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.upper() in text:
                return category
    if "山海" in title or "神话" in title:
        return "插画"
    # 视频/MV 检测
    if any(k in title.lower() for k in ['mv', '视频', 'video', 'pv', '动画']):
        return "视频/MV"
    return "其他"


def generate_highlight(title, description, category):
    """根据作品信息生成详细亮点描述"""
    text = (title + " " + (description or "")).lower()
    title_only = title.lower()
    
    # 针对具体作品标题生成详细亮点
    # 下雪的城市
    if "雪" in title:
        return "温馨雪景插画，氛围感拉满"
    
    # 绘本/帽子镇
    if "绘本" in title or "帽子镇" in title:
        return "充满想象力的原创绘本角色设计"
    
    # 茶饮品牌
    if "茶" in title or "品牌" in title:
        return "新中式茶饮视觉系统，质感出众"
    
    # MV/大唐Gang
    if "mv" in title_only or "大唐" in title:
        return "国风说唱 MV，视觉冲击力强"
    
    # 云顶之弈/李青
    if "云顶" in title or "李青" in title:
        return "东方武学风格游戏 CG，武侠氛围浓厚"
    
    # 电动车/产品渲染
    if "电动车" in title or "产品渲染" in title:
        return "产品级 3D 渲染，细节精致"
    
    # 剑与远征/九尾
    if "剑与远征" in title or "九尾" in title:
        return "游戏角色动画 PV，特效炸裂"
    
    # 2D转3D
    if "3d conversion" in title_only or "2d" in title_only:
        return "2D 转 3D 风格转换，视觉效果惊艳"
    
    # 身体与水
    if "身体" in title or "水" in title:
        return "充满意象的创意插画作品"
    
    # 杂志插画/少年
    if "少年" in title or "文章插画" in title:
        return "杂志文章配图，风格清新细腻"
    
    # AI 相关
    if any(k in text for k in ['ai', 'aigc', 'midjourney', 'mj', 'sd', 'stable diffusion', 'dall', '生成式', '人工智能']):
        return "AI 生成艺术作品"
    
    # 3D 相关
    if any(k in text for k in ['3d', 'c4d', 'blender', '建模', '渲染', '三维', 'octane', 'redshift']):
        return "3D 建模与渲染作品"
    
    # 动态/视频
    if any(k in text for k in ['动画', 'motion', '动效', 'live2d', 'mg', 'video', '视频', 'pv', 'cg']):
        return "动画/视频制作"
    
    # 品牌设计
    if any(k in text for k in ['品牌', 'logo', 'vi', '标志', '包装', 'ip', 'identity', '视觉']):
        return "品牌视觉设计系统"
    
    # 插画/手绘
    if any(k in text for k in ['插画', '绘制', '儿插', '手绘', '原画']):
        return "精美插画作品"
    
    # 国风/传统
    if any(k in text for k in ['国风', '传统', '中国', '大唐', '东方', '神话', '山海']):
        return "国风美学设计"
    
    # 游戏
    if any(k in text for k in ['游戏', '原画', '概念']):
        return "游戏美术设计"
    
    # 默认描述
    default_highlights = {
        "插画": "精美插画作品",
        "AI绘画": "AI 生成艺术",
        "3D": "3D 渲染作品",
        "动画": "动态视觉效果",
        "品牌设计": "品牌视觉设计",
        "UI/UX": "界面设计方案",
        "游戏": "游戏美术作品",
        "海报": "创意海报设计",
        "摄影": "摄影作品",
        "手办": "手办模型制作",
        "汽车/工业": "工业设计方案",
        "电商": "电商视觉设计",
        "视频/MV": "视频/MV作品",
        "其他": "精彩设计作品"
    }
    return default_highlights.get(category, "精彩设计作品")

def extract_author(title):
    """提取作者名"""
    title = title.replace('_站酷ZCOOL', '').replace('-站酷ZCOOL', '')
    if "_" in title and "-" in title:
        parts = title.split("_")
        author = parts[-1].split("-")[0].strip()
        if author and author != "站酷ZCOOL":
            return author
    if "-" in title:
        parts = title.split("-")
        author = parts[-1].strip()
        if author and author != "站酷ZCOOL":
            return author
    return None

def extract_description(html):
    """提取作品描述"""
    soup = BeautifulSoup(html, 'html.parser')
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        desc = meta_desc.get('content', '').strip()
        if '站酷聚集了1800万' in desc:
            desc = desc[:desc.find('站酷聚集了1800万')].strip()
        return desc[:200] if desc else ""
    return ""

def fetch_works(count=10):
    """获取站酷热门作品"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 获取首页
    response = requests.get('https://www.zcool.com.cn/', headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取作品链接
    work_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/work/' in href and len(work_links) < count + 10:
            full_link = href if href.startswith('http') else f"https://www.zcool.com.cn{href}"
            if full_link not in work_links:
                work_links.append(full_link)
    
    works = []
    for link in work_links[:count]:
        try:
            work_response = requests.get(link, headers=headers)
            work_soup = BeautifulSoup(work_response.text, 'html.parser')
            
            title_tag = work_soup.find('title')
            title = title_tag.text.strip() if title_tag else '未知标题'
            title = title.replace('_站酷ZCOOL', '').strip()
            
            description = extract_description(work_response.text)
            category = classify_work(title, description)
            author = extract_author(title)
            highlight = generate_highlight(title, description, category)
            
            works.append({
                'title': title,
                'link': link,
                'description': description,
                'category': category,
                'author': author,
                'highlight': highlight
            })
            time.sleep(0.3)
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return works

def format_list(works):
    """格式化作品列表（不含亮点，供人工撰写）"""
    date_str = datetime.now().strftime('%Y年%m月%d日')
    output = f"📢 {date_str} 站酷热门设计作品推荐：\n\n"
    
    for i, w in enumerate(works, 1):
        output += f"{i}. {w['title']}\n"
        output += f"   类型：{w['category']}\n"
        if w['author']:
            output += f"   作者：{w['author']}\n"
        output += f"   链接：{w['link']}\n\n"
    
    # 统计
    categories = {}
    for w in works:
        cat = w['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    output += "## 📊 今日总结\n\n"
    output += "**类型分布：** " + " | ".join([f"{k}({v})" for k, v in sorted(categories.items(), key=lambda x: -x[1])])
    
    return output

def format_auto_message(works):
    """格式化自动消息（含标题链接、类型分类、亮点描述、趋势统计）"""
    date_str = datetime.now().strftime('%Y年%m月%d日')
    message = f"📢 {date_str} 站酷热门设计作品推荐：\n\n"
    
    # 标题带链接的格式
    emoji_map = {
        "插画": "🎨", "AI绘画": "🤖", "3D": "🧊", "动画": "🎬",
        "品牌设计": "📛", "UI/UX": "📱", "游戏": "🎮", "海报": "🖼️",
        "摄影": "📷", "手办": "🦾", "汽车/工业": "🚗", "电商": "🛒",
        "其他": "✨", "视频/MV": "🎵"
    }
    
    for i, w in enumerate(works, 1):
        emoji = emoji_map.get(w['category'], "✨")
        # 标题带链接
        message += f"{i}. {emoji} [{w['title']}]({w['link']})\n"
        # 类型分类 + 亮点描述（使用中文竖线）
        message += f"   🏷️ 类型：{w['category']} | 🌟 {w.get('highlight', '精彩设计作品')}\n\n"
    
    # 趋势统计
    categories = {}
    for w in works:
        cat = w['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    sorted_cats = sorted(categories.items(), key=lambda x: -x[1])
    trend_str = " | ".join([f"{k}({v})" for k, v in sorted_cats])
    message += f"---\n📊 今日趋势：**{trend_str}**\n"
    
    return message

def main():
    parser = argparse.ArgumentParser(description='站酷每日热门作品推荐')
    parser.add_argument('--output-dir', default='zcool_daily',
                        help='输出目录')
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("🔍 正在获取站酷热门作品...")
    works = fetch_works(10)
    print(f"✅ 获取到 {len(works)} 条作品")
    
    # 使用带链接的格式输出
    content = format_auto_message(works)
    date_str = datetime.now().strftime('%Y-%m-%d')
    save_path = os.path.join(args.output_dir, f'zcool_{date_str}.txt')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 已保存至：{save_path}")
    print("\n" + "="*50)
    print(content)

if __name__ == "__main__":
    main()