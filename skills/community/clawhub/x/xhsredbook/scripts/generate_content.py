#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_content.py - Generate title and content for Xiaohongshu posts
Supports template-based generation with rich topic coverage.
"""

import sys
import json
import random
from datetime import datetime

from config import get_subdir

OUTPUT_DIR = get_subdir("generated_content")

# ── 话题模板库 ──────────────────────────────────────────────────────────

TEMPLATES = {
    "美食": {
        "titles": [
            "这家店我能吃一辈子！",
            "人均50吃到撑的宝藏店",
            "闭眼入！好吃到舌盘子",
            "这个味道绝了！",
            "必打卡！本地人都爱的店",
            "今天的晚餐太满足了",
            "一口就爱上的味道",
            "吃货必看！这家真的绝",
        ],
        "contents": [
            "今天发现了一家超好吃的店！\n环境很舒服，服务也很好\n\n人均：50-80元\n营业时间：10:00-22:00\n\n强烈推荐他们家的招牌菜，\n味道真的绝了！\n下次还要带朋友来！\n\n#美食推荐 #探店 #好吃到飞起",
            "周末探店记录📝\n\n这家店藏在小巷子里\n但味道真的一绝！\n\n必点：\n🔥 招牌菜 - 入口即化\n🔥 特色甜品 - 甜而不腻\n🔥 手工饮品 - 清爽解腻\n\n环境也很出片📸\n适合约会/闺蜜聚餐\n\n#探店打卡 #美食分享 #周末去哪吃",
        ],
    },
    "旅游": {
        "titles": [
            "这个地方太美了！",
            "小众景点｜人少景美",
            "周末出游好去处！",
            "拍照超出片的地方",
            "这才是度假该有的样子",
            "私藏景点大公开！",
            "一个人也能玩的地方",
        ],
        "contents": [
            "这次旅行真的太棒了！\n风景超美，人也不多\n非常适合周末放松\n\n拍照tips：\n- 早上光线最好\n- 穿浅色衣服更出片\n- 记得带防晒！\n\n实用信息：\n门票：免费/50元\n交通：地铁/自驾\n建议游玩时间：2-3小时\n\n#旅游攻略 #周末去哪儿 #打卡",
            "终于去了心心念念的地方！\n\n📍 位置：市中心30分钟车程\n🎫 门票：免费\n⏰ 建议时间：半天\n\n亮点：\n✨ 自然风光超美\n✨ 人少不用排队\n✨ 拍照随便出大片\n\n小tips：\n带够水和零食\n穿舒适的鞋子\n\n#旅行日记 #小众景点 #出游推荐",
        ],
    },
    "穿搭": {
        "titles": [
            "这套穿搭绝了！",
            "显瘦10斤的穿搭公式",
            "小个子必看穿搭！",
            "通勤穿搭｜简约大方",
            "这样穿真的很显气质",
            "懒人穿搭一周不重样",
        ],
        "contents": [
            "今天的穿搭分享\n\n上衣：简约款\n下装：高腰阔腿裤\n鞋子：小白鞋\n\n穿搭 tips：\n- 高腰线拉长比例\n- 同色系更显高级\n- 配饰点睛很重要\n\n这套真的超好看！\n而且很日常，上班约会都 OK\n\n#穿搭分享 #OOTD #时尚穿搭",
            "一周通勤穿搭合集👔\n\n周一：西装+阔腿裤（干练）\n周二：针织+半裙（温柔）\n周三：衬衫+牛仔裤（休闲）\n周四：连衣裙（省心）\n周五：卫衣+短裙（轻松）\n\n每套都是基础款混搭\n不用花太多钱就能穿出质感\n\n#通勤穿搭 #职场穿搭 #一周穿搭",
        ],
    },
    "科技": {
        "titles": [
            "这个工具太好用了！",
            "效率翻倍的神器推荐",
            "后悔没早点知道！",
            "打工人必备工具合集",
            "这个APP改变了我的生活",
            "手机里必装的宝藏APP",
            "省时省力的效率神器",
            "数码好物推荐！",
        ],
        "contents": [
            "今天给大家分享几个超实用的效率工具！\n\n用了一段时间，工作效率真的提升很多\n\n推荐清单：\n📝 笔记工具 - 随时记录灵感\n📊 表格工具 - 数据一目了然\n🎨 设计工具 - 零基础也能出图\n📅 日程管理 - 再也不会忘事\n\n每个都亲测好用！\n关键是大部分都免费\n\n收藏起来慢慢用～\n\n#效率工具 #好物推荐 #科技分享",
            "手机里的宝藏APP分享📱\n\n用了3年的私藏清单\n每个都是精挑细选\n\n🔥 修图：轻松出大片\n🔥 记账：月底不再迷茫\n🔥 学习：碎片时间利用\n🔥 健康：运动饮食记录\n🔥 出行：省钱又省心\n\n都是免费或超便宜的\n学生党打工人都适用！\n\n#APP推荐 #手机必备 #实用工具",
            "数码好物开箱分享🎁\n\n最近入手了几个小玩意\n性价比真的超高！\n\n1️⃣ 无线充电器 - 告别线缆\n2️⃣ 蓝牙耳机 - 通勤必备\n3️⃣ 便携支架 - 解放双手\n4️⃣ 收纳包 - 出门不乱\n\n总花费不到200块\n但幸福感直线上升\n\n#数码好物 #开箱 #性价比之王",
        ],
    },
    "生活": {
        "titles": [
            "提升幸福感的小习惯",
            "独居生活也可以很精彩",
            "这些小事让生活更美好",
            "分享我的日常好物",
            "简单生活的快乐",
            "今天也是元气满满的一天",
        ],
        "contents": [
            "分享几个提升幸福感的小习惯✨\n\n1. 早起喝一杯温水\n2. 每天运动30分钟\n3. 睡前读书15分钟\n4. 定期整理房间\n5. 记录每天的小确幸\n\n坚持一个月\n你会发现生活真的不一样了\n\n#生活方式 #自律 #提升幸福感",
            "我的居家好物分享🏠\n\n🕯️ 香薰蜡烛 - 氛围感拉满\n🌿 绿植 - 看着心情好\n📖 好书 - 充实自己\n☕ 手冲咖啡 - 仪式感\n🎵 蓝牙音箱 - 随时有音乐\n\n不需要花很多钱\n就能让家变得温馨舒适\n\n#居家好物 #生活分享 #家居",
        ],
    },
    "健身": {
        "titles": [
            "坚持运动30天的变化",
            "新手友好的健身计划",
            "在家也能练出好身材",
            "这个动作瘦腿超有效",
            "健身小白必看！",
        ],
        "contents": [
            "分享我的健身日常💪\n\n今日训练：\n🔥 深蹲 x 15 x 3组\n🔥 平板支撑 60秒 x 3组\n🔥 开合跳 30个 x 3组\n🔥 拉伸 10分钟\n\n总用时：40分钟\n\n坚持一个月真的有变化！\n关键是要循序渐进\n不要一上来就猛练\n\n#健身打卡 #居家健身 #运动日常",
        ],
    },
}

# 通用模板（匹配不到具体话题时使用）
DEFAULT_TEMPLATE = {
    "titles": [
        "分享一个好东西！",
        "这个真的太实用了",
        "强烈推荐！",
        "宝藏发现！",
        "这个必须安利给你们",
        "今天的分享来了",
        "收藏起来慢慢看",
    ],
    "contents": [
        "今天给大家分享：{topic}\n\n真的超级好用/好看/好吃！\n自己用了一段时间，\n效果/体验都很不错\n\n优点：\n- 性价比高\n- 质量好\n- 值得入手\n\n有需要的姐妹可以冲了！\n\n#好物分享 #种草 #推荐",
        "关于{topic}的分享📝\n\n最近一直在研究这个\n总结了一些心得给大家\n\n重点：\n1️⃣ 入门简单\n2️⃣ 效果明显\n3️⃣ 坚持很重要\n\n希望对你们有帮助！\n有问题评论区聊～\n\n#经验分享 #干货 #实用",
    ],
}


def match_template(topic: str) -> dict:
    """Match topic to the best template."""
    topic_lower = topic.lower()
    for key, tmpl in TEMPLATES.items():
        if key in topic_lower:
            return tmpl
    return DEFAULT_TEMPLATE


def generate_content(topic: str) -> dict:
    """
    Generate title (<20 chars) and content based on topic.
    Returns: {"title": "...", "content": "...", "topic": "..."}
    """
    template = match_template(topic)
    title = random.choice(template["titles"])
    content = random.choice(template["contents"]).format(topic=topic)
    return {"title": title, "content": content.strip(), "topic": topic}


def save_content(topic: str) -> str:
    """Generate and save content to JSON. Returns file path."""
    data = generate_content(topic)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"{timestamp}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Content saved: {output_path}")
    print(f"[Title] {data['title']}")
    print(f"[Content preview] {data['content'][:80]}...")
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        topics = list(TEMPLATES.keys())
        print(f"Usage: python generate_content.py <topic>")
        print(f"Available topics: {', '.join(topics)}")
        print(f"Or use any custom topic text.")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])
    try:
        save_content(topic)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
