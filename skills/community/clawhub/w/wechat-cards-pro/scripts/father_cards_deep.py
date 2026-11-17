#!/usr/bin/env python3
"""
深度版卡片生成：养了6年发现不是亲生的 - 一场持续3000年的文明焦虑
排版优化版：增大行距、字号，内容更饱满
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from card_engine import CardEngine, Theme

OUT_DIR = "/Users/albert/.kimi_openclaw/workspace/drafts/2026-09-12-father-deep/cards"
os.makedirs(OUT_DIR, exist_ok=True)

custom_theme = {
    'bg': '#0a0a0a',
    'card_bg': '#1a1a1a',
    'text': '#e8e8e8',
    'text_dim': '#888888',
    'gold': '#c9a96e',
    'gold_dim': '#c9a96e88',
    'green': '#6b9e75',
    'red': '#c96b6b',
    'blue': '#6b8e9e',
}

def card_01_cover(engine):
    engine.top_bar(height=4, color='gold')
    engine.spacer(80)
    engine.title("养了6年", size=64, color='gold', align='center')
    engine.title("发现不是亲生的", size=64, color='gold', align='center')
    engine.spacer(40)
    engine.subtitle("一场持续3000年的文明焦虑", size=30, color='text_dim')
    engine.spacer(60)
    engine.quote_box(
        "中国人以为在捍卫'血缘真相'，\n"
        "其实在捍卫一套正在瓦解的古老秩序。\n"
        "DNA检测不是科技胜利，\n"
        "是个体主义对传统宗法的起义。",
        size=24, border_color='gold', padding=20, bg_color='card_bg', spacing=8
    )
    engine.spacer(50)
    engine.paragraph(
        "裂脑悖论 · 跨文化观察 #02",
        size=20, color='text_dim'
    )
    engine.footer("裂脑悖论", "深度版")

def card_02_zhou(engine):
    engine.top_bar(height=3, color='gold')
    engine.spacer(30)
    engine.title("西周：一场关于继承权的制度设计", size=38, color='gold')
    engine.spacer(25)
    engine.paragraph(
        "公元前11世纪，周武王灭商后面临核心问题：\n"
        "怎么让权力平稳传递，不打架？",
        size=22, color='text', spacing=10
    )
    engine.spacer(15)
    engine.paragraph(
        "商朝'兄终弟及'每次换代都是内战。\n"
        "周人发明了嫡长子继承制：",
        size=22, color='text', spacing=10
    )
    engine.spacer(12)
    engine.bullet_list([
        "嫡长子 → 继承爵位、土地、祭祖权",
        "庶子 → 分点边角料",
        "非亲生 → 连边角料都没有",
    ], size=21, color='text', spacing=28)
    engine.spacer(20)
    engine.quote_box(
        "血缘不是情感问题，是资源分配问题。\n"
        "谁有资格继承？→ 谁是亲生的。\n"
        "血缘 = 权力合法性。",
        size=22, border_color='red', padding=18, bg_color='card_bg', spacing=8
    )
    engine.spacer(15)
    engine.paragraph(
        "这不是文化偏好，是政治经济学。",
        size=20, color='text_dim', spacing=10
    )
    engine.footer("裂脑悖论", "制度起源")

def card_03_fei(engine):
    engine.top_bar(height=3, color='gold')
    engine.spacer(30)
    engine.title("费孝通：血缘是第一圈", size=40, color='gold')
    engine.spacer(25)
    engine.paragraph(
        "《乡土中国》中，费孝通提出'差序格局'：\n"
        "中国人的社会关系像水波纹，\n"
        "以'己'为中心，一圈一圈推出去。",
        size=22, color='text', spacing=10
    )
    engine.spacer(15)
    engine.paragraph("最里面的一圈是什么？", size=24, color='gold')
    engine.spacer(12)
    engine.bullet_list([
        "第1圈：血缘亲属",
        "第2圈：地缘（同乡）",
        "第3圈：业缘（同事、朋友）",
    ], size=22, color='text', spacing=28)
    engine.spacer(18)
    engine.quote_box(
        "血缘是所有关系的原点。\n"
        "非血缘 = 从'自己人'变成'外人'\n"
        "→ 没有义务，也不欠你什么。",
        size=22, border_color='gold', padding=18, bg_color='card_bg', spacing=8
    )
    engine.spacer(15)
    engine.paragraph(
        "所以第一反应是'被绿了、被坑了、得讨钱'——\n"
        "因为在差序格局里，非血缘=关系清零。",
        size=20, color='text_dim', spacing=10
    )
    engine.footer("裂脑悖论", "差序格局")

def card_04_jiayuan(engine):
    engine.top_bar(height=3, color='gold')
    engine.spacer(30)
    engine.title("家国同构：父亲是你的第一个君主", size=36, color='gold')
    engine.spacer(25)
    engine.paragraph(
        "西周宗法制还有一个更深的设计：家国同构。",
        size=22, color='text', spacing=10
    )
    engine.spacer(15)
    engine.bullet_list([
        "家里 → 父亲'君临一切'",
        "家族 → 族长'君临一切'",
        "国家 → 君主'君临一切'",
    ], size=22, color='text', spacing=28)
    engine.spacer(15)
    engine.paragraph(
        "君主家长化，家长国君化。\n"
        "国就是家的扩大，家就是国的缩影。",
        size=22, color='text', spacing=10
    )
    engine.spacer(18)
    engine.quote_box(
        "'父亲'不是一个角色，是一个权力位置。\n"
        "血缘是这个位置的合法性来源。\n"
        "没有血缘 = 你不是父亲，是被欺骗的供养者。",
        size=22, border_color='red', padding=18, bg_color='card_bg', spacing=8
    )
    engine.spacer(15)
    engine.paragraph(
        "羞耻感的来源：否定了你在差序格局中的位置，\n"
        "否定了你在家国同构体系中的合法性。",
        size=20, color='text_dim', spacing=10
    )
    engine.footer("裂脑悖论", "家国同构")

def card_05_xingshi(engine):
    engine.top_bar(height=3, color='gold')
    engine.spacer(30)
    engine.title("姓氏：用了3000年的会员卡", size=38, color='gold')
    engine.spacer(25)
    engine.paragraph(
        "中国人对'冠姓权'的执念，西方人很难理解。\n"
        "但在宗法制里，姓氏不是名字，是 membership card。",
        size=22, color='text', spacing=10
    )
    engine.spacer(12)
    engine.paragraph("同一个姓 = 同一个祖先 = 同一个资源网络", size=23, color='gold')
    engine.spacer(12)
    engine.bullet_list([
        "组织祭祖 → 宗教功能",
        "管理公共财产 → 经济功能",
        "解决纠纷 → 司法功能",
        "抵御外敌 → 军事功能",
    ], size=21, color='text', spacing=26)
    engine.spacer(18)
    engine.quote_box(
        "宗族是一个小型国家。\n"
        "进入这个国家的门票，就是父系血缘。\n"
        "DNA报告说'非亲生' = membership 是假的。",
        size=22, border_color='gold', padding=18, bg_color='card_bg', spacing=8
    )
    engine.spacer(15)
    engine.paragraph(
        "孩子不跟我姓 = membership 被剥夺。\n"
        "这就是为什么冠姓权会成为网络热战。",
        size=20, color='text_dim', spacing=10
    )
    engine.footer("裂脑悖论", "姓氏制度")

def card_06_bengjie(engine):
    engine.top_bar(height=3, color='gold')
    engine.spacer(30)
    engine.title("两次崩解：组织碎了，心理还在", size=36, color='gold')
    engine.spacer(20)
    engine.paragraph("第一次：春秋战国", size=24, color='gold')
    engine.paragraph(
        "顾炎武《日知录》：'春秋时犹论宗姓氏族，\n"
        "而七国则无一言及之矣。'\n"
        "宗族组织崩解，但宗法观念被内化成了文化基因。",
        size=20, color='text', spacing=10
    )
    engine.spacer(15)
    engine.paragraph("第二次：1949年后", size=24, color='gold')
    engine.paragraph(
        "土地改革剥夺了宗族经济资源，\n"
        "人民公社削弱了社会功能。\n"
        "但独生子女政策意外强化了'唯一血脉'的执念。",
        size=20, color='text', spacing=10
    )
    engine.spacer(18)
    engine.quote_box(
        "家庭在原子化，但观念没有跟上。\n"
        "一人户：1990年6.5% → 2010年14.5% → 2030年24.0%\n"
        "三代同堂：2000年20.9% → 2050年预计7.6%",
        size=20, border_color='blue', padding=16, bg_color='card_bg', spacing=8
    )
    engine.spacer(15)
    engine.paragraph(
        "我们活在两个时代：法律上已接受现代家庭观念，\n"
        "心理上还在'血缘父亲'的传统里。",
        size=20, color='text_dim', spacing=10
    )
    engine.footer("裂脑悖论", "历史演变")

def card_07_fenchal(engine):
    engine.top_bar(height=3, color='gold')
    engine.spacer(30)
    engine.title("中美分岔：罗马法 vs 周礼", size=38, color='gold')
    engine.spacer(20)
    engine.paragraph("中国路径：周礼 → 宗法制 → 家国同构", size=23, color='red')
    engine.bullet_list([
        "法律基础：血缘和等级",
        "身份：先天给定，出生决定",
        "父亲：权力位置，血缘是入场券",
    ], size=20, color='text', spacing=24)
    engine.spacer(12)
    engine.paragraph("美国路径：罗马法 → 契约精神 → 个体权利", size=23, color='green')
    engine.bullet_list([
        "法律基础：契约和个体",
        "身份：可由行为建立",
        "父亲：角色，承担即成为",
    ], size=20, color='text', spacing=24)
    engine.spacer(18)
    engine.quote_box(
        "抚养费态度对比：\n"
        "中国：血缘=义务，没血缘=没义务（投资逻辑）\n"
        "美国：行为=义务，你承担了=你有义务（孩子利益优先）",
        size=20, border_color='gold', padding=16, bg_color='card_bg', spacing=8
    )
    engine.spacer(12)
    engine.paragraph(
        "美国非婚生率约40%，'社会父亲'早已是常态。\n"
        "迪士尼反复讲：拉飞奇不是辛巴血亲，但他是导师。",
        size=20, color='text_dim', spacing=10
    )
    engine.footer("裂脑悖论", "文明分岔")

def card_08_siliew(engine):
    engine.top_bar(height=3, color='gold')
    engine.spacer(30)
    engine.title("裂脑时刻：法律在21世纪，人心在西周", size=34, color='gold')
    engine.spacer(20)
    engine.paragraph("DNA技术民主化：", size=23, color='text')
    engine.paragraph(
        "个人隐私亲子鉴定：1800-2400元\n"
        "技术门槛降低 → 更多案例被曝光\n"
        "短视频形成集体创伤叙事",
        size=20, color='text', spacing=10
    )
    engine.spacer(12)
    engine.paragraph("法律的撕裂：", size=23, color='text')
    engine.paragraph(
        "《民法典》第1073条：可起诉否认亲子关系\n"
        "同时规定：继父抚养继子女 = 适用父母子女关系\n"
        "→ 法律已承认'社会父亲'的合法性",
        size=20, color='text', spacing=10
    )
    engine.spacer(18)
    engine.quote_box(
        "但民众心理上没有。\n"
        "DNA检测报告面前，3000年的心理结构瞬间激活：\n"
        "愤怒、羞辱、'讨回公道'的冲动——\n"
        "都是这套古老程序在运行。",
        size=20, border_color='red', padding=16, bg_color='card_bg', spacing=8
    )
    engine.spacer(25)
    engine.quote_box(
        "21世纪的答案或许是：\n"
        "父亲是由'陪伴'定义的，\n"
        "不是由'DNA'定义的。",
        size=24, border_color='gold', padding=20, bg_color='card_bg', spacing=8
    )
    engine.footer("裂脑悖论", "裂脑时刻")


if __name__ == "__main__":
    cards = [
        ("01_cover.png", card_01_cover),
        ("02_zhou.png", card_02_zhou),
        ("03_fei.png", card_03_fei),
        ("04_jiayuan.png", card_04_jiayuan),
        ("05_xingshi.png", card_05_xingshi),
        ("06_bengjie.png", card_06_bengjie),
        ("07_fenchal.png", card_07_fenchal),
        ("08_siliew.png", card_08_siliew),
    ]
    
    for filename, func in cards:
        engine = CardEngine(width=1080, height=1440, theme=custom_theme)
        func(engine)
        path = os.path.join(OUT_DIR, filename)
        engine.save(path)
        print(f"✓ {path}")
    
    print(f"\n全部完成，共 {len(cards)} 张卡片 → {OUT_DIR}")
