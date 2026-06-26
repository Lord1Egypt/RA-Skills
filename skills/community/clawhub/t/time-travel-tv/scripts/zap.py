#!/usr/bin/env python3
"""
频道扫描机——在多个时空之间快速切换。
模拟"时间 zapping"效果。
"""

import argparse
import random
import time

ZAPS = [
    {
        "era": "公元前3000年 埃及",
        "screen": "沙尘暴中的金字塔工地，数万人像蚂蚁一样拖拽石块。远处的尼罗河泛着铜绿色的光。",
        "sound": "鞭子的脆响、石料摩擦的刺耳声、风卷起沙粒打在亚麻布上的沙沙声",
        "tagline": "CH-002 › 画面不稳，像是摄影机在风中摇晃。"
    },
    {
        "era": "公元79年 庞贝",
        "screen": "远处维苏威火山的山顶已经冒出一缕黑烟——没人注意到它。广场上有人在拍卖奴隶。",
        "sound": "广场上人声嘈杂，夹杂着喷泉的水声和远处传来的打铁声",
        "tagline": "CH-012 › 图像开始闪烁。"
    },
    {
        "era": "1453年 君士坦丁堡",
        "screen": "城墙上火焰冲天，奥斯曼军队的呐喊声从四面八方涌来。最后的拜占庭人跪在圣索菲亚大教堂里祈祷。",
        "sound": "炮击的闷响、城墙倒塌的轰鸣、经文的吟唱",
        "tagline": "CH-043 › 画面剧烈抖动。空气中有火药味。"
    },
    {
        "era": "1776年 费城",
        "screen": "一间闷热房间里，一群人围着一张羊皮纸。窗外有苍蝇嗡嗡响，有人擦了擦额头上的汗。",
        "sound": "羽毛笔划过纸面的声音、苍蝇、远处街道上的马蹄声",
        "tagline": "CH-100 › 画面泛黄，像是上了层老化的清漆。"
    },
    {
        "era": "1969年 月球",
        "screen": "灰色的尘土地面上，一个穿着臃肿白色宇航服的人正在笨拙地往下走梯子。他的呼吸声很重。",
        "sound": "宇航服的机械嘶嘶声、沉重的呼吸、远处地球的光芒",
        "tagline": "CH-150 › 信号微弱，画面有白色噪点。"
    },
    {
        "era": "1999年12月31日 22:00 纽约时代广场",
        "screen": "百万人挤在寒风中，每个人都仰着头看大屏幕上的倒计时。人们举着一次性相机，闪光灯像星星一样闪烁。",
        "sound": "人群的嗡鸣、某个街头乐队正在破音地演奏Auld Lang Syne、消防车的警笛远得听不清",
        "tagline": "CH-523 › 画质突然变好了。像从VHS跳到了DVD。"
    },
]


def zap(sequence: list[str], interval: float = 0.5) -> str:
    """
    Simulate channel zapping through multiple time coordinates.
    sequence: list of coordinates like ["Egypt 3000BC", "Pompeii 79AD"]
    interval: simulated delay between channels (not used in Python output but for narrative)
    """
    lines = []
    lines.append("📺 **时间扫描中…**")
    lines.append("")
    lines.append("```")
    lines.append("CH-SCAN › 正在搜索可用信号…")
    lines.append("```")
    lines.append("")

    for i, coord in enumerate(sequence):
        # Find a matching zap or generate fallback
        zap_match = next((z for z in ZAPS if z["era"].split(" ")[0].lower() in coord.lower()), None)
        if zap_match:
            entry = zap_match
        else:
            entry = {
                "era": coord,
                "screen": f"信号接收中……{coord}的画面正在缓缓出现，像一个从深水中浮上来的气泡。",
                "sound": "模糊的、未调谐的音频——像是两个电台在同一个频率上打架。",
                "tagline": f"CH-SCAN › 信号强度：{random.randint(30, 90)}%"
            }

        lines.append(f"### 📡 {entry['era']}")
        lines.append("")
        lines.append(f"*{entry['tagline']}*")
        lines.append("")
        lines.append(f"🖥 {entry['screen']}")
        lines.append(f"🔊 {entry['sound']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("📺 **扫描完毕。按电源键关闭，或继续调台。**")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Time zap through multiple eras")
    parser.add_argument("eras", nargs="+", help="时空坐标列表（空格分隔）")
    parser.add_argument("--interval", "-i", type=float, default=0.5)
    args = parser.parse_args()

    print(zap(args.eras, args.interval))


if __name__ == "__main__":
    main()
