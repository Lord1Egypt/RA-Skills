#!/usr/bin/env python3
"""
贴图卡片生成：养了6年发现不是亲生的
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from card_engine import CardEngine, Theme

OUT_DIR = "/tmp/wechat_cards_father"
os.makedirs(OUT_DIR, exist_ok=True)

# 自定义主题：深黑金
custom_theme = {
    'bg': '#0a0a0a',
    'card_bg': '#1a1a1a',
    'text': '#e8e8e8',
    'text_dim': '#888888',
    'gold': '#c9a96e',
    'gold_dim': '#c9a96e88',
    'green': '#6b9e75',
    'red': '#c96b6b',
}

def card_cover(engine):
    engine.top_bar(height=4, color='gold')
    engine.spacer(60)
    engine.title("养了6年", size=64, color='gold', align='center')
    engine.title("发现不是亲生的", size=64, color='gold', align='center')
    engine.spacer(30)
    engine.subtitle("一个让中国男人破防、", size=30, color='text_dim')
    engine.subtitle("美国人摊手的故事", size=30, color='text_dim')
    engine.spacer(50)
    engine.quote_box(
        "DNA报告推翻的不是亲子关系，\n是我们对'父亲'的全部想象",
        size=26, border_color='gold', padding=20, bg_color='card_bg'
    )
    engine.footer("裂脑悖论", "跨文化观察 #01")

def card_event(engine):
    engine.top_bar(height=3, color='gold')
    engine.title("先说说这个故事", size=44, color='text')
    engine.spacer(20)
    engine.paragraph(
        "某男子离婚6年后做DNA检测，发现养了6年的孩子不是亲生的。",
        size=24, color='text'
    )
    engine.spacer(15)
    engine.paragraph(
        "网上反应：太惨了！被绿了！帮别人养孩子！\n"
        "吃瓜群众纷纷表示同情，有人建议打官司要回抚养费。",
        size=24, color='text'
    )
    engine.spacer(20)
    engine.quote_box(
        "但如果我们把镜头切到美国，\n同样的故事，完全不同的剧本。",
        size=24, border_color='text_dim', padding=18, bg_color='card_bg'
    )
    engine.footer("裂脑悖论", "事件")

def card_china(engine):
    engine.top_bar(height=3, color='gold')
    engine.title("中国人的第一反应", size=44, color='text')
    engine.spacer(20)
    engine.bullet_list([
        "愤怒：我的香火断了！",
        "羞辱：我成了冤大头",
        "算账：6年抚养费得讨回来",
    ], size=24, color='text', spacing=32)
    engine.spacer(20)
    engine.quote_box(
        "中国人的'父亲' = 血缘 + 姓氏 + 宗族延续\n三件套，缺一不可",
        size=26, border_color='red', padding=18, bg_color='card_bg'
    )
    engine.spacer(15)
    engine.paragraph(
        "费孝通在《乡土中国》里说：中国人的社会关系像水波纹，\n"
        "血缘是第一圈。非血缘 = 没有义务。",
        size=22, color='text_dim'
    )
    engine.footer("裂脑悖论", "中国视角")

def card_usa(engine):
    engine.top_bar(height=3, color='gold')
    engine.title("美国人的第一反应", size=44, color='text')
    engine.spacer(20)
    engine.bullet_list([
        "So what? 你养了6年，你就是你爸",
        "Biological father = 捐精的而已",
        "Social father = 真正的父亲",
    ], size=24, color='text', spacing=32)
    engine.spacer(20)
    engine.quote_box(
        "美国继父收到的父亲节贺卡\n增速超过生父\n——'chosen father'比\n'biological father'更有分量",
        size=24, border_color='green', padding=18, bg_color='card_bg'
    )
    engine.spacer(15)
    engine.paragraph(
        "美国非婚生率约40%，'父亲'早已去生物化。\n"
        "迪士尼反复讲：拉飞奇不是辛巴的血亲，但他是导师。",
        size=22, color='text_dim'
    )
    engine.footer("裂脑悖论", "美国视角")

def card_brain(engine):
    engine.top_bar(height=3, color='gold')
    engine.title("裂脑时刻", size=48, color='gold')
    engine.spacer(20)
    engine.paragraph(
        "中国人以为在捍卫'血缘真相'，\n"
        "其实在捍卫一套正在瓦解的宗族秩序。",
        size=26, color='text'
    )
    engine.spacer(15)
    engine.paragraph(
        "DNA检测不是科技胜利，\n"
        "是个体主义对传统宗族的起义。",
        size=26, color='text'
    )
    engine.spacer(15)
    engine.quote_box(
        "讽刺的是：他争取个体权利的方式，\n恰恰是最生物学的（DNA）。",
        size=26, border_color='gold', padding=20, bg_color='card_bg'
    )
    engine.spacer(15)
    engine.paragraph(
        "我们活在两个时代：\n"
        "法律上接受了'推定父亲'（现代），\n"
        "心理上还在'血缘父亲'（传统）。",
        size=22, color='text_dim'
    )
    engine.footer("裂脑悖论", "核心洞察")

def card_family(engine):
    engine.top_bar(height=3, color='gold')
    engine.title("重组家庭怎么办？", size=44, color='text')
    engine.spacer(20)
    engine.bullet_list([
        "生物学父亲：可能只是个'基因快递员'",
        "养育父亲：你投入的爱，比血缘更有分量",
        "孩子：我有两个爸爸，一个给我生命，一个给我人生",
    ], size=24, color='text', spacing=32)
    engine.spacer(25)
    engine.quote_box(
        "21世纪的父亲，\n该由'陪伴'定义，\n而不是'DNA'定义。",
        size=30, border_color='gold', padding=22, bg_color='card_bg'
    )
    engine.spacer(30)
    engine.paragraph(
        "那个男人失去的不是一个孩子，\n"
        "是他对'父亲'这个词的全部想象。\n"
        "但更深层的问题是：这个想象，本来就不属于21世纪。",
        size=22, color='text_dim'
    )
    engine.footer("裂脑悖论", "结语")

if __name__ == "__main__":
    cards = [
        ("01_cover.png", card_cover),
        ("02_event.png", card_event),
        ("03_china.png", card_china),
        ("04_usa.png", card_usa),
        ("05_brain.png", card_brain),
        ("06_family.png", card_family),
    ]
    
    for filename, func in cards:
        engine = CardEngine(width=1080, height=1440, theme=custom_theme)
        func(engine)
        path = os.path.join(OUT_DIR, filename)
        engine.save(path)
        print(f"✓ {path}")
    
    print(f"\n全部完成，共 {len(cards)} 张卡片 → {OUT_DIR}")
