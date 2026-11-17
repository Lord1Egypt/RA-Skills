#!/usr/bin/env python3
"""
微信公众号贴图卡片生成模板

用法：
1. 复制本文件，修改 CARD_DATA 定义你的内容
2. 运行: python3 generate_cards.py
3. 检查输出目录的PNG文件

核心原则：
- 所有容器自适应高度，禁止硬编码高度
- 使用 CardEngine 的组件方法，它会自动追踪y坐标
- 每张卡片最后调用 engine.save()
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from card_engine import CardEngine

# ============ 配置 ============
OUT_DIR = "/tmp/wechat_cards_demo"

# ============ 卡片内容定义 ============
# 每张卡片是一个函数，接收 CardEngine 实例

def card_cover(engine):
    """封面卡片"""
    engine.top_bar(height=3)
    engine.title("主标题文字", size=56, color='gold')
    engine.spacer(10)
    engine.subtitle("副标题/一句话说明", size=28)
    engine.spacer(40)
    
    # 核心数据点（可选）
    engine.quote_box(
        "关键数字/金句\n可以有多行",
        size=26, border_color=None, padding=20
    )
    
    engine.footer("公众号名称", "系列标签")


def card_content(engine):
    """标准内容卡片"""
    engine.top_bar()
    engine.title("章节标题", size=44)
    engine.spacer(15)
    
    engine.paragraph("正文段落一。可以写很长，会自动换行。", size=22)
    engine.spacer(10)
    
    engine.paragraph("正文段落二。支持\\n换行。", size=22)
    
    # 引用框
    engine.quote_box(
        "这是一个重点框\n第二行内容\n第三行",
        size=24, padding=18
    )
    
    # 列表
    engine.bullet_list([
        "要点一：说明文字",
        "要点二：说明文字",
        "要点三：说明文字",
    ], size=22, spacing=28)
    
    engine.footer("公众号名称")


def card_timeline(engine):
    """时间线卡片"""
    engine.top_bar()
    engine.title("发展历程", size=44)
    engine.spacer(20)
    
    events = [
        ("2023年", "公司成立\n初始团队5人"),
        ("2024年", "产品发布\n用户突破10万"),
        ("2025年", "B轮融资\n估值10亿美元"),
    ]
    
    for year, desc in events:
        # 年份
        engine.title(year, size=24, color='gold')
        # 描述框
        engine.quote_box(desc, size=22, border_color=None, padding=15)
        engine.spacer(10)
    
    engine.footer("公众号名称")


def card_conclusion(engine):
    """结语卡片"""
    engine.top_bar()
    engine.title("结语", size=48)
    engine.spacer(20)
    
    engine.title("金句标题", size=36, color='gold')
    engine.spacer(15)
    
    engine.quote_box(
        "总结性文字\n可以多行\n\n最后一句收尾",
        size=24, padding=20
    )
    
    engine.spacer(20)
    
    engine.quote_box(
        "轻松收尾的话\n想想还挺期待的呢",
        size=26, color='gold', border_color='gold', padding=20
    )
    
    engine.footer("公众号名称", "文章标题")


# ============ 主流程 ============

def main():
    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    
    cards = [
        ("01_cover.png", card_cover, "封面"),
        ("02_content.png", card_content, "内容"),
        ("03_timeline.png", card_timeline, "时间线"),
        ("04_conclusion.png", card_conclusion, "结语"),
    ]
    
    for filename, func, label in cards:
        engine = CardEngine()
        func(engine)
        path = os.path.join(OUT_DIR, filename)
        engine.save(path)
    
    print(f"\n全部完成: {len(cards)} 张卡片")
    print(f"保存位置: {OUT_DIR}")


if __name__ == '__main__':
    main()
