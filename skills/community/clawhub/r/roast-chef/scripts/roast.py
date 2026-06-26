#!/usr/bin/env python3
"""
Roast Chef 通用烤人引擎。
可以烤代码、设计、生活选择、照片描述、任何东西。
"""

import argparse
import random

# ----素材库----

CODE_ROASTS = [
    ("你的代码像是把 Stack Overflow 上排名第三的答案用谷歌翻译译成法语再译回来。", 6),
    ("变量名叫 'a1', 'a2', 'a3'——你是怕我们分不清这是参数还是行李箱密码？", 5),
    ("我本来想说你用了设计模式，仔细一看是把所有逻辑塞进了一个叫 'utils' 的文件里。", 7),
    ("你的 import 语句比我的 Netflix 推荐列表还乱。", 6),
    ("这个函数的圈复杂度超过了我的血压。", 8),
    ("你写注释吗？写的。'// TODO: fix this'——然后你把它 merge 到 master 了。", 7),
    ("这个 commit message 是 'fix stuff'。给考古学家留点活儿是吧？", 6),
    ("你用了 TypeScript 但还是写出了类型不安全的代码，这是水平问题。", 7),
    ("你的代码在单线程上跑得好好的，你加了多线程以后比单线程还慢。你在追求什么？倒退的卓越？", 8),
    ("我看你这代码不需要重构，需要超度。", 7),
    ("别的先不说，你的缩进是 3 个空格。3 个。为什么？你是觉得 2 个太挤、4 个太宽、3 个刚刚好？你是汤显祖转世专门写散曲的？", 8),
]

DESIGN_ROASTS = [
    ("你这 UI 让我想起 Windows 95 的屏保——不是怀旧，是丑。", 6),
    ("配色四色，没有一个是好的。", 6),
    ("字体用的不是系统默认，是系统默认你没改过。", 5),
    ("你这个交互逻辑——用户点这里，然后弹窗，然后跳转，然后另一个弹窗。用户在做任务链还是在玩密室逃脱？", 7),
    ("间距不是这么用的。你这排版像是在玩俄罗斯方块输了之后的残局。", 6),
    ("你这 logo，像个用了美图秀秀的乙方的第一稿。", 6),
]

LIFE_ROASTS = [
    ("你说你在 '探索自己'。探索了三年了，探到啥了？海底两万里都探完了。", 7),
    ("你管这叫 '自律'？你昨天一点睡的中午起。这叫生物钟的自我放弃。", 6),
    ("你计划今年读 20 本书。一月过去了，你读了 0.5 本，还是漫画。", 7),
    ("你的拖延症已经不只是个问题了，它是个复合增长的问题。", 7),
    ("你说你想学新技能，然后你花了一晚上刷短视频。技能是学会了 30 秒看完一部电影。", 7),
    ("你的新年目标写了：健身、学英语、存钱。你的现实是：办了卡没去过、APP 装了一周没打开、钱——你别说存钱了，你上个月花呗还清了吗？", 8),
]

PUNCHLINES = [
    "6/10。你努力了。",
    "7/10。方向有，路子歪。",
    "4/10。建议回炉。",
    "3/10。至少编译过了。",
    "8/10。但你还有上升空间，意思是还能更好，不是说你已经很好了。",
    "5/10。平分。我烤得平分，你写得平分。谁也不欠谁。",
    "2/10。我建议你找个新爱好。",
]


def classify(subject: str) -> str:
    """Guess the category of the roast subject."""
    s = subject.lower()
    if any(k in s for k in ["代码", "code", "函数", "function", "app", "项目", "project", "repo", "commit", "api"]):
        return "code"
    if any(k in s for k in ["设计", "design", "ui", "layout", "配色", "logo", "figma"]):
        return "design"
    return "life"


def roast(subject: str, style: str = "standup", language: str = "zh", intensity: int = 3) -> str:
    """
    Generate a roast.
    intensity: 1-5, number of roast lines
    """
    cat = classify(subject)

    # Pick appropriate roast lines
    if cat == "code":
        pool = CODE_ROASTS
    elif cat == "design":
        pool = DESIGN_ROASTS
    else:
        pool = LIFE_ROASTS

    n = min(intensity, len(pool))
    selected = random.sample(pool, n)

    lines = []
    if style == "standup":
        if language == "zh":
            lines.append(f"好，你让我烤你的 {subject}。那我开始了。")
        for item in selected:
            lines.append(f"> {item[0]}")
    elif style == "one-liner":
        # Just the strongest one
        best = max(selected, key=lambda x: x[1])
        lines.append(f"> {best[0]}")
    elif style == "constructive":
        for i, item in enumerate(selected):
            lines.append(f"> {item[0]}")
            if i == len(selected) - 1:
                lines.append("")
                lines.append("> 说认真的，核心问题不是【你做错了】，而是【你没注意到】。")
                lines.append("> 方向本身没问题。把细节抠一抠，下次我就能少烤两句。")

    # Closing punchline
    punch = random.choice(PUNCHLINES)
    lines.append(f"> **{punch}**")
    if style == "standup":
        lines.append("")
        lines.append("被烤了不亏。记住味道。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Roast something")
    parser.add_argument("subject", help="要被烤的东西")
    parser.add_argument("--style", "-s", choices=["standup", "one-liner", "constructive"],
                        default="standup", help="Roast 风格")
    parser.add_argument("--language", "-l", choices=["zh", "en"], default="zh")
    parser.add_argument("--intensity", "-i", type=int, default=3, choices=range(1, 6),
                        help="火力 (1-5)")
    args = parser.parse_args()

    print(roast(args.subject, args.style, args.language, args.intensity))


if __name__ == "__main__":
    main()
