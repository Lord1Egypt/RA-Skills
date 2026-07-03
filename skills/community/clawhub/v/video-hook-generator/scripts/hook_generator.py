#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短视频爆款钩子生成器
输入主题 → 输出10种高点击率开场钩子
"""

import sys
import argparse
from datetime import datetime


# ============ 钩子模板库 ============

HOOK_TEMPLATES = {
    "douyin": {
        "冲突型": [
            "别再瞎努力了，{truth}才是真相",
            "你以为很难？学会这招其实超简单",
            "{topic}最大的谎言，99%的人都信了",
            "别被{topic}骗了！真正有用的是这个",
            "{topic}，很多人第一步就做错了",
        ],
        "数字型": [
            "{num}个{topic}技巧，让你的{goal}翻倍",
            "学会这{num}点，{topic}不再难",
            "{num}年经验总结：{topic}最重要的{num}件事",
            "{topic}只需{num}步，一看就会",
            "揭秘{topic}的{num}个核心秘密",
        ],
        "悬念型": [
            "我以为{topic}很难，直到我用了这个方法",
            "{topic}，其实大部分人都理解错了",
            "这个{topic}技巧，80%的博主不会告诉你",
            "{topic}的关键，不是你想象的那样",
            "关于{topic}，今天说点不一样",
        ],
        "揭秘型": [
            "{topic}的内幕，今天全部说清楚",
            "行业内部才知道的{topic}秘密",
            "曝光：{topic}的真相",
            "揭秘{topic}到底是怎么回事",
            "{topic}背后的逻辑，90%的人不知道",
        ],
        "反常型": [
            "{topic}？其实你一直在误解",
            "你绝对想不到的{topic}方法",
            "{topic}竟然可以这样",
            "这种{topic}方式，我从没见过",
            "所有人都做错了的{topic}",
        ],
        "痛点型": [
            "还在为{topic}头疼？教你{num}招解决",
            "{topic}难？看完你就懂了",
            "{topic}的常见问题，一次说清楚",
            "{topic}踩坑指南，看完少走3年弯路",
            "{topic}必学的入门课",
        ],
        "成果型": [
            "用这个方法，{topic}效果提升{num}倍",
            "{topic}改变了我的人生",
            "自从学会{topic}，每月多赚{num}万",
            "{topic}后的第{num}天，效果惊到我了",
            "这个{topic}方法，让我从此告别焦虑",
        ],
        "福利型": [
            "免费送你{topic}资料，限前{num}名",
            "{topic}完整教程，今天免费分享",
            "这份{topic}攻略，价值{num}元",
            "{topic}资料包，评论区扣{num}领取",
            "限时免费！{topic}全套教程",
        ],
    },
    "xhs": {
        "冲突型": [
            "别再踩坑了！{topic}的正确打开方式",
            "{topic}的那些坑，我都替你踩完了",
            "后悔没早点知道的{topic}技巧",
        ],
        "种草型": [
            "救命！{topic}真的太绝了！",
            "私藏{topic}分享✨建议收藏",
            "被问了{num}次的{topic}！真心推荐",
            "宝藏{topic}清单🧾建议直接抄作业",
        ],
        "测评型": [
            "{topic}测评｜真实使用感受",
            "3款{topic}横向对比，谁赢了？",
            "花{num}元买的{topic}，值不值？",
        ],
        "教程型": [
            "新手必看！{topic}完整攻略",
            "手把手教你{topic}，零基础可学",
            "{topic}入门，看这一篇就够了",
        ],
    },
    "bilibili": {
        "深度型": [
            "【{topic}】深度解析",
            "关于{topic}，你可能不知道的{num}件事",
            "{topic}全解｜从入门到精通",
        ],
        "揭秘型": [
            "揭秘：{topic}为什么突然火了",
            "深度起底{topic}的背后逻辑",
            "{topic}行业报告｜内行人才知道的",
        ],
        "教程型": [
            "{topic}完全指南｜附资源",
            "从零开始学{topic}（附工具清单）",
            "{topic}入门教程（持续更新）",
        ],
    },
}

# 数字库
NUMS = ["3", "5", "7", "10", "12", "15", "20"]


def format_hook(template, topic, num=None):
    """填充模板"""
    import random
    n = num or random.choice(NUMS)

    # 常见 action/truth 配对
    actions = ["瞎努力", "乱花钱", "盲目跟风", "随便选"]
    truths = ["正确的做法", "真正有效的方法", "行业内幕"]

    # 先处理带占位符的组合，再处理单个占位符
    # 防止"你以为{false}？其实{true}" → "你以为很难？其实其实超简单"
    intermediate = result = template.replace("{topic}", topic)
    intermediate = result = intermediate.replace("{num}", n)
    intermediate = result = intermediate.replace("{goal}", "效率")
    intermediate = result = intermediate.replace("{action}", actions[hash(topic) % len(actions)])
    intermediate = result = intermediate.replace("{truth}", truths[hash(topic) % len(truths)])
    # false和true要在truth之后处理，避免"其实"被重复
    if "{false}" not in result and "{true}" not in result:
        pass  # 已被组合处理
    else:
        result = result.replace("{false}", "很难")
        result = result.replace("{true}", "其实超简单")
    return result


def generate_hooks(topic, platform="douyin", count=10, include_script=False):
    """生成钩子"""
    platform_templates = HOOK_TEMPLATES.get(platform, HOOK_TEMPLATES["douyin"])
    all_hooks = []

    for hook_type, templates in platform_templates.items():
        for tmpl in templates:
            hook_text = format_hook(tmpl, topic)
            entry = {
                "type": hook_type,
                "hook": hook_text,
                "script": f"{hook_text}（前3秒画面建议：展示{topic}的{['效果', '过程', '成果', '对比'][hash(hook_text) % 4]}）"
                           if include_script else None
            }
            all_hooks.append(entry)

    return all_hooks[:count]


def print_hooks(hooks, platform_name, topic):
    """格式化输出"""
    emoji_map = {
        "冲突型": "🔥", "数字型": "📊", "悬念型": "🎭",
        "揭秘型": "💡", "反常型": "😂", "痛点型": "😰",
        "成果型": "🚀", "福利型": "🎁",
        "种草型": "🌱", "测评型": "🔬", "教程型": "📖",
        "深度型": "🧠",
    }

    print(f"\n{'='*55}")
    print(f"{emoji_map.get(hooks[0]['type'], '📌')} {platform_name}钩子 - {topic}")
    print(f"{'='*55}")

    for i, h in enumerate(hooks, 1):
        emoji = emoji_map.get(h["type"], "📌")
        print(f"\n{i:2d}. [{h['type']}] {emoji} {h['hook']}")
        if h["script"]:
            print(f"    📹 脚本：{h['script']}")


def save_to_file(hooks, topic, output_dir):
    """保存到文件"""
    import os
    import json
    from pathlib import Path

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_path = Path(output_dir) / f"hooks_{topic[:10]}_{date_str}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"topic": topic, "hooks": hooks, "generated_at": date_str}, f, ensure_ascii=False, indent=2)

    return out_path


def main():
    parser = argparse.ArgumentParser(description="短视频爆款钩子生成器")
    parser.add_argument("--topic", "-t", type=str, required=True, help="视频主题")
    parser.add_argument("--platform", "-p", type=str, default="douyin",
                        choices=["douyin", "xhs", "bilibili"], help="目标平台")
    parser.add_argument("--count", "-n", type=int, default=10, help="生成数量")
    parser.add_argument("--include-script", "-s", action="store_true", help="包含前3秒脚本建议")
    parser.add_argument("--output", "-o", type=str, default=None, help="输出文件目录")
    args = parser.parse_args()

    platform_name = {"douyin": "抖音", "xhs": "小红书", "bilibili": "B站"}[args.platform]

    print(f"\n🎯 正在为【{args.topic}】生成{platform_name}爆款钩子...")
    hooks = generate_hooks(args.topic, args.platform, args.count, args.include_script)
    print_hooks(hooks, platform_name, args.topic)

    if args.output:
        path = save_to_file(hooks, args.topic, args.output)
        print(f"\n✅ 已保存: {path}")


if __name__ == "__main__":
    main()
