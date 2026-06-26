#!/usr/bin/env python3
"""
Roast Battle — 两人/两个项目互烤模式。
模拟两个对象互相 roast 的对抗赛。
"""

import argparse
import random

PERSONALITY_A = [
    "你是技术派的，冷静理性，擅长找出逻辑漏洞。",
    "你是吐槽流的，反应快，擅长即兴发挥。",
    "你是学院派的，用词精确，善于引用权威来反驳。",
    "你是 street 风格的，粗犷直接，不按套路出牌。",
]

PERSONALITY_B = [
    "你是文艺派的，擅长类比和意象。",
    "你是毒舌派的，一句废话都不说，刀刀见骨。",
    "你是情怀派的，用价值观差异来烤对方。",
    "你是冷面笑匠型的，面无表情地扔包袱。",
    "你是技术派的，冷静理性，擅长找出逻辑漏洞。",
    "你是吐槽流的，反应快，擅长即兴发挥。",
]


def battle(combatant_a: str, combatant_b: str, rounds: int = 3) -> str:
    """
    Simulate a roast battle between two combatants.
    """
    lines = []
    lines.append(f"🔥 **ROAST BATTLE** 🔥")
    lines.append("")
    lines.append(f"左：{combatant_a}")
    lines.append(f"右：{combatant_b}")
    lines.append("")
    lines.append("=" * 40)
    lines.append("")

    persona_a = random.choice(PERSONALITY_A)
    persona_b = random.choice(PERSONALITY_B)

    for r in range(1, rounds + 1):
        lines.append(f"### 回合 {r}")
        lines.append("")

        if r == 1:
            lines.append(f"🎤 {combatant_a}（{persona_a}）：")
            lines.append(f"> 面对 {combatant_b}，我先不急。你看起来像是个……让我想想怎么说比较不容易伤到你……算了不想了。")
            lines.append(f"> 你在你的领域是什么水平呢？就是那种——有人在群里问有没有人懂这个——然后你的所有同事集体静音的水平。")
        elif r == 2:
            lines.append(f"🎤 {combatant_b}（{persona_b}）：")
            lines.append(f"> 哦，来真的了。{combatant_a}，我刚才听着呢。你说的每一个字都在帮我证明我的观点：你真的很会说话，前提是不需要说到点上。")
            lines.append(f"> 你的知识面广，我承认。广得像……一个停车场。大是很大，但上面没有一栋楼。")
        else:
            lines.append(f"🎤 {combatant_a}的反击：")
            lines.append(f"> 你说我的知识像停车场——那你的知识像什么？像加油站——就那一个点，加完就得走。")
            lines.append("")
            lines.append(f"🎤 {combatant_b}的回击：")
            lines.append(f"> 好了，不闹了。我们又不是真的仇人。我给你一个真诚的：你比我强的地方是你敢说。这很重要。继续练。")

        lines.append("")

    lines.append("=" * 40)
    lines.append(f"🏆 **平局！两个人都很精彩！（或者说两个人都需要再练练。）**")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Roast battle between two things")
    parser.add_argument("a", help="参赛者A")
    parser.add_argument("b", help="参赛者B")
    parser.add_argument("--rounds", "-r", type=int, default=3, help="回合数 (默认3)")
    args = parser.parse_args()

    print(battle(args.a, args.b, args.rounds))


if __name__ == "__main__":
    main()
