#!/usr/bin/env python3
"""
沉浸式直播描述生成器。
根据时空坐标输出直播画面描述。
"""

import argparse
import random

SEGMENTS = [
    {
        "century": "ancient",
        "openings": [
            "信号捕捉到了一片广阔的平原。",
            "画面稳定了。你看到了一个古代城市的屋顶——密密麻麻的瓦片反射着午后的阳光。",
            "镜头从上往下俯拍：这个时代还没人知道「俯拍」这个词，但你看得见全貌。",
        ],
        "middle": [
            "在画面的一角，有人在交易——不是在商店里，而是在广场上，地面摆满了货物。",
            "远处有一堵正在建造中的围墙。脚手架是竹子——不，是当地的一种硬木。",
            "有人抬头看了天空一眼。你的出现引起了某种难以言说的气氛变化。",
        ],
        "sound": [
            "背景音是一种持续的嗡鸣——不是机械，而是无数人的低语、动物的叫声、风和火的混合体。",
            "你能听见这座城市在呼吸。柴火噼啪声、木头呻吟声、远处飘来的笛声。",
        ],
        "detail": [
            "一只狗在巷子口躺着睡觉。它的一条腿在半空中抽动——在做梦。",
            "有个孩子在奔跑，手里抓着一根绳子——绳子的另一端是一只绑着线的甲虫当风筝。",
            "一个陶罐被打碎了。没有人停下来看。这里是三千年前，碎陶片是最不稀奇的东西。",
        ]
    },
    {
        "century": "modern",
        "openings": [
            "画面对焦了。你正在看一个城市的街角。看似普通——直到你意识到路边没有手机。",
            "信号稳定了。画面里有人在报亭买报纸。不是电子屏——是纸。",
            "你看到一条大街。路上跑着黄色的出租车。不是电动车——它们在烧汽油，排气管冒着可见的尾气。",
        ],
        "middle": [
            "商店的玻璃橱窗里，有人在用笔在纸上写字。记账。用手。",
            "街角的电线杆上贴着手写的广告。用订书机钉上去的。",
            "路过的人会停下来跟陌生人说话。频率比你习惯的高得多。",
        ],
        "sound": [
            "你能听到底盘传来的嗡鸣。不是引擎——是路面和轮胎的摩擦声，这个频率在未来被电动车消灭了。",
            "有人在用公共电话。硬币掉落的声音在这个时代稀松平常。",
        ],
        "detail": [
            "一辆自行车的链条掉了。主人蹲下来修，修好了以后继续骑，没有拍照。",
            "一个老人的靴子底快要掉了。他用胶带缠了两圈。这个时代的人会修东西。",
            "饭馆门口有只猫在蹭门框。它已经在这里蹭了三年了。同一扇门，同一只猫。",
        ]
    },
    {
        "century": "future",
        "openings": [
            "画面缓缓亮起。你似乎漂浮在半空中——视野非常高。",
            "这个时代的画面有一种不属于任何历史上的光的质感。",
            "信号收到了一组稳定的画面。你看到的场景是……比任何科幻电影都平淡，也任何都真实。",
        ],
        "middle": [
            "建筑表面在呼吸——材料根据光线在微妙地变化颜色。",
            "没有人行道。或者说，到处都是人行道——地面本身就是一块巨大的温和的触摸屏。",
            "你注意到空气是干净的。出奇的干净。这个时代的人大概不知道什么叫雾霾。",
        ],
        "sound": [
            "环境音经过设计——不是安静，而是被调过频的安静。低频基础音+选择性隔音。",
            "人的说话声很轻——不是秘密，而是他们习惯了声音比画面更少地被使用。",
        ],
        "detail": [
            "有一个人抬头看了你所在的方向一眼。停留了一秒。然后继续走路。",
            "一只机械鸟停在树上。它的翅膀在充电。",
            "水面上的倒影被数字化了——你看到的不再是真实的反射，而是信息层。",
        ]
    }
]


def classify_century(query: str) -> str:
    """Guess which era category the query belongs to."""
    q = query.lower()
    if any(k in q for k in ["未来", "future", "3024", "2077", "2100", "3000"]):
        return "future"
    if any(k in q for k in ["19", "20", "21世纪", "现代", "古代", "19th", "20th", "modern"]):
        return "modern"
    return "ancient"


def describe(query: str) -> str:
    """Generate an immersive live-TV description for a time-space coordinate."""
    era_type = classify_century(query)
    pack = next((s for s in SEGMENTS if s["century"] == era_type), SEGMENTS[0])

    lines = []
    # Channel info
    channel_num = random.choice([2, 5, 8, 12, 15, 22, 50, 100, 150, 523, 666, 1001, 2049])
    lines.append(f"📺 **CH-{channel_num:04d}** — {query}")
    lines.append(f"🕒 信号强度：{'█' * random.randint(5, 8)} {'▁' * random.randint(0, 4)} | 实时 | 未录制")
    lines.append("")

    # Opening
    lines.append(f"🖥 {random.choice(pack['openings'])}")
    lines.append("")

    # Middle body
    for _ in range(2):
        lines.append(random.choice(pack['middle']))
    lines.append("")

    # Sound
    lines.append(f"🔊 {random.choice(pack['sound'])}")
    lines.append("")

    # Detail
    lines.append(f"📌 *{random.choice(pack['detail'])}*")
    lines.append("")
    lines.append("---")
    lines.append(f"*以上是来自 {query} 的实时直播。按遥控器换台，或再次输入新坐标。*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Describe a time-space live broadcast")
    parser.add_argument("query", nargs="?", default=None, help="时空坐标")
    args = parser.parse_args()

    if args.query:
        print(describe(args.query))
    else:
        print("用法：python3 describe.py \"3024年 上海陆家嘴\"")


if __name__ == "__main__":
    main()
