#!/usr/bin/env python3
"""
生成旅行攻略 PPT
调用 powerpoint-pptx skill 创建精美 PPT
"""

import json
import sys
import argparse
from typing import Dict, Any, List

def create_ppt_content(city: str, days: int, attractions: List[Dict]) -> str:
    """
    创建 PPT 内容结构
    
    Args:
        city: 城市名称
        days: 天数
        attractions: 景点列表
    
    Returns:
        PPT 结构 JSON 字符串
    """
    
    slides = []
    
    # 1. 封面
    slides.append({
        "type": "title",
        "title": f"{city} {days}日深度游攻略",
        "content": "精选路线 · 避雷指南 · 必玩项目\n\n discover the best of {city}",
        "images": []
    })
    
    # 2. 行程概览
    overview_content = f""""📍 目的地：{city}
📅 行程天数：{days} 天
🏆 精选景点：{len(attractions)} 个

🎯 行程特色：
"""
    
    # 添加 TOP 5 景点到概览
    for i, attr in enumerate(attractions[:5], 1):
        overview_content += f"\n{i}. {attr['name']} ⭐ {attr['total_score']}分"
    
    slides.append({
        "type": "content",
        "title": "行程概览",
        "content": overview_content
    })
    
    # 3. 景点推荐（每个景点一页）
    for i, attr in enumerate(attractions[:10], 1):
        # 构建标签文本
        tags_text = " | ".join(attr.get('tags', []))
        
        # 构建亮点
        highlights = attr.get('typical_comments', [])
        highlights_text = "\n".join([f"✓ {h}" for h in highlights[:3]]) if highlights else ""
        
        # 构建警告
        warnings = attr.get('warnings', [])
        warnings_text = "\n".join([f"⚠️ {w}" for w in warnings[:2]]) if warnings else ""
        
        content = f"""📊 推荐指数：{attr['total_score']}/10
🏷️ 标签：{tags_text}

💎 游客评价：
{highlights_text}

{warnings_text}
"""
        
        slides.append({
            "type": "content",
            "title": f"#{i} {attr['name']}",
            "content": content,
            "images": []  # 可添加景点图片
        })
    
    # 4. 游乐项目优先级表
    priority_content = """📋 游乐项目优先级指南

🟢 高优先级（强烈推荐）：
- 独特性强、当地特色体验
- 口碑极佳、体验感满分
- 性价比高、值得专程前往


🟡 中优先级（可选体验）：
- 大众化项目、可玩可不玩
- 时间充裕可以去体验
- 评价中等、无功无过


🔴 低优先级（不建议）：
- 排队时间过长（>2小时）
- 差评集中、有明显坑点
- 价格虚高、体验一般
"""
    
    slides.append({
        "type": "content",
        "title": "游乐项目优先级",
        "content": priority_content
    })
    
    # 5. 避雷指南
    warnings_list = []
    for attr in attractions:
        for warning in attr.get('warnings', []):
            warnings_list.append(f"⚠️ {attr['name']}：{warning}")
    
    # 取前 8 条
    warnings_text = "\n\n".join(warnings_list[:8]) if warnings_list else "暂无集中踩坑反馈"
    
    slides.append({
        "type": "content",
        "title": "避雷指南 ⚠️",
        "content": f"根据网友真实反馈整理的踩坑项目：\n\n{warnings_text}\n\n💡 建议：热门景点尽量避开节假日，早去或晚去可避开人流高峰。"
    })
    
    # 6. 实用贴士
    tips_content = """📝 出行小贴士

📸 拍照建议：
- 早起避开人流拍摄
- 傍晚黄金光线最佳
- 准备充电宝备用

🍜 美食提示：
- 别在景区内吃饭（贵且一般）
- 去当地人多的老店
- 提前查好必吃榜单

🚗 交通建议：
- 下载当地交通APP
- 准备零钱备用
- 高峰时段避开地铁

💰 省钱技巧：
- 提前订票通常更便宜
- 关注官方优惠
- 学生证/老年证带好
"""
    
    slides.append({
        "type": "content",
        "title": "实用贴士",
        "content": tips_content
    })
    
    # 7. 结束页
    slides.append({
        "type": "title",
        "title": "祝你旅途愉快！🎉",
        "content": f"愿你在{city}发现美好，收获满满回忆\n\nSafe Travels ✈️"
    })
    
    # 构建完整 PPT 数据
    ppt_data = {
        "title": f"{city} {days}日深度游攻略",
        "slides": slides
    }
    
    return json.dumps(ppt_data, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='生成旅行攻略 PPT 数据结构')
    parser.add_argument('city', help='目标城市')
    parser.add_argument('--days', type=int, default=3, help='旅行天数')
    parser.add_argument('--attractions-file', help='景点数据 JSON 文件')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 加载景点数据（如果提供了文件）
    attractions = []
    if args.attractions_file:
        try:
            with open(args.attractions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                attractions = data.get('attractions', [])
        except Exception as e:
            print(f"警告：无法加载景点文件: {e}", file=sys.stderr)
    
    # 如果没有加载到数据，使用示例数据
    if not attractions:
        print("使用示例数据生成 PPT 结构...")
        attractions = [
            {"name": "示例景点A", "total_score": 9.5, "tags": ["必打卡", "自然风光"], 
             "typical_comments": ["太美了", "强烈推荐"], "warnings": ["节假日人多"]},
            {"name": "示例景点B", "total_score": 8.8, "tags": ["人文", "历史"],
             "typical_comments": ["很有文化底蕴"], "warnings": []}
        ]
    
    # 生成 PPT 数据
    ppt_json = create_ppt_content(args.city, args.days, attractions)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(ppt_json)
        print(f"✅ PPT 数据已保存到: {args.output}")
    else:
        print(ppt_json)

if __name__ == "__main__":
    main()
