#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一鱼三吃内容改写器
功能：输入内容 → 输出抖音/小红书/B站三个平台专属版本
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path

# ============ 平台配置 ============

PLATFORMS = {
    "douyin": {
        "name": "抖音",
        "title_style": "悬念/数字/冲突型，≤20字，强钩子",
        "body_style": "口语化，情绪共鸣，≤150字",
        "hashtag_count": (5, 8),
        "best_times": ["12:00-13:00", "18:00-19:00", "21:00-22:00"],
        "emoji": "🔥",
        "hook_templates": [
            "没想到...{core}竟然这么简单！",
            "学会这{num}个技巧，{core}不是梦",
            "曝光！{core}的内幕",
            "为什么...{core}越来越火了？",
            "{core}，看完你就懂了",
        ],
    },
    "xhs": {
        "name": "小红书",
        "title_style": "干货/避坑/测评型，≤25字，有吸引力",
        "body_style": "分段emoji，真实感，种草力，≤500字",
        "hashtag_count": (8, 12),
        "best_times": ["08:00-09:00", "12:00-13:00", "20:00-21:00"],
        "emoji": "📕",
        "hook_templates": [
            "救命！{core}真的太绝了！",
            "{core}测评 | 真实使用感受",
            "新手必看！{core}完整攻略",
            "避坑指南！{core}那些事",
            "私藏！{core}的正确打开方式",
        ],
    },
    "bilibili": {
        "name": "B站",
        "title_style": "疑问/揭秘/教程型，≤30字，干货感",
        "body_style": "结构化，深度，干货，≤800字",
        "hashtag_count": (5, 10),
        "best_times": ["18:00-20:00", "22:00-23:00"],
        "emoji": "📺",
        "hook_templates": [
            "【{core}】深度解析",
            "关于{core}，你可能不知道的事",
            "{core}全攻略｜零基础到精通",
            "揭秘：{core}为什么突然火了",
            "从零开始学{core}（附资源）",
        ],
    },
}

# 通用话题标签池
HASHTAG_POOL = {
    "douyin": [
        "#AI工具", "#AI写作", "#AI变现", "#效率神器", "#自媒体工具",
        "#干货分享", "#涨粉技巧", "#副业赚钱", "#科技数码", "#实用技巧",
        "#小红书运营", "#抖音运营", "#短视频制作", "#内容创作", "#AI助手",
    ],
    "xhs": [
        "#AI工具", "#效率提升", "#自媒体变现", "#好物推荐", "#干货教程",
        "#种草清单", "#科技数码", "#软件推荐", "#学习技巧", "#工作神器",
        "#效率神器", "#AI写作", "#创作工具", "#数码种草", "#实用好物",
    ],
    "bilibili": [
        "#科技", "#数码", "#软件工具", "#教程", "#测评",
        "#硬核", "#知识分享", "#AI工具", "#效率提升", "#创作工具",
    ],
}


# ============ 核心类 ============

class ContentConverter:
    """内容改写器"""

    def __init__(self, input_text, topic_hint=""):
        self.original = input_text.strip()
        self.topic_hint = topic_hint or self._extract_topic()
        self.results = {}

    def _extract_topic(self):
        """从原文提取主题"""
        # 取前50字作为主题提示
        lines = self.original.split("\n")
        for line in lines:
            line = line.strip().strip("#-*")
            if len(line) > 5:
                return line[:50]
        return self.original[:50]

    def _extract_core_points(self):
        """提取核心要点（简化版，实际可用AI）"""
        # 简单分句
        sentences = [s.strip() for s in self.original.split("。") if len(s.strip()) > 5]
        if len(sentences) > 5:
            return sentences[:5]
        return sentences if sentences else [self.topic_hint]

    def _extract_keywords(self):
        """提取关键词：完整中文词（配合停用词过滤）"""
        # 预定义好词表（从原文匹配，优先完整词）
        good_phrases = [
            "AI工具", "AI写作", "AI技能", "AI变现", "AI助手",
            "自媒体", "热点追踪", "热门话题", "视频生成", "竞品监控",
            "选题生成", "自动发布", "多平台", "内容创作", "效率神器",
            "干货分享", "涨粉技巧", "副业赚钱", "月入过万", "全家桶",
            "ClawHub", "QClaw", "edge-tts", "小红书", "抖音", "B站",
        ]

        # 从原文和好词表匹配
        text = self.original
        found = []
        for phrase in good_phrases:
            if phrase in text and phrase not in found:
                found.append(phrase)

        # 英文完整词（边界匹配）
        english = re.findall(r'\b[a-zA-Z]{3,}\b', text)

        return found[:8] + english[:3]

    def _generate_title(self, platform):
        """生成平台专属标题"""
        cfg = PLATFORMS[platform]
        # 核心词：取原文前30字（会进一步在模板中截断）
        core_long = self.topic_hint[:30]
        # 短核心词（用于模板，≤8字）
        keywords = self._extract_keywords()
        core = core_long[:8] if len(core_long) > 8 else core_long

        # 根据平台生成候选标题
        candidates = []

        if platform == "douyin":
            candidates = [
                f"没想到...{core}竟然这么简单！",
                f"学会这5个技巧，少走3年弯路",
                f"曝光！{core}的内幕（看完收藏）",
                f"为什么...{core}越来越火了？",
                f"{core}，3分钟讲清楚",
            ]
        elif platform == "xhs":
            candidates = [
                f"救命！{core}真的太绝了！",
                f"{core}测评 | 真实使用感受分享",
                f"新手必看！{core}完整攻略💡",
                f"避坑指南！{core}那些事",
                f"私藏！{core}的正确打开方式✨",
            ]
        else:  # bilibili
            candidates = [
                f"【{core}】深度解析",
                f"关于{core}，你可能不知道的事",
                f"{core}全攻略｜零基础到精通",
                f"揭秘：{core}为什么突然火了",
                f"从零开始学{core}（附资源）",
            ]

        return candidates[0], candidates[1:]

    def _generate_body(self, platform):
        """生成平台专属正文"""
        core_points = self._extract_core_points()
        keywords = self._extract_keywords()

        if platform == "douyin":
            body = f"""{"。".join(core_points[:3])}。

{core_points[0] if core_points else core_points}！
#AI工具 #效率神器 #干货分享 #自媒体"""

        elif platform == "xhs":
            sections = []
            for i, p in enumerate(core_points[:4]):
                emoji_map = ["💡", "🔧", "✨", "📌"]
                sections.append(f"{emoji_map[i % len(emoji_map)]} {p}。")

            body = f"""今天来聊聊{self.topic_hint[:20]}～

{"".join(sections)}

{" ".join(f"#{(k[:3] if len(k) > 3 else k)}" for k in keywords[:8])}

---
❤️ 觉得有用记得收藏！""".strip()

        else:  # bilibili
            sections = []
            for i, p in enumerate(core_points):
                sections.append(f"**{i+1}. {p}。**\n")

            body = f"""{self.topic_hint}

{"".join(sections)}

**总结：**
{" ".join(f"#{(k[:3] if len(k) > 3 else k)}" for k in keywords[:6])}
#知识分享 #教程 #科技"""

        return body

    def _generate_hashtags(self, platform, count=None):
        """生成话题标签"""
        pool = HASHTAG_POOL.get(platform, HASHTAG_POOL["douyin"])
        cfg = PLATFORMS[platform]
        min_c, max_c = cfg["hashtag_count"]
        n = count or min_c

        # 混入原文关键词（中文取前4字，英文取原样）
        keywords = self._extract_keywords()
        import re
        extra_tags = []
        for k in keywords[:5]:
            # 中文话题用前4字，英文用全词
            if re.match(r'^[\u4e00-\u9fff]', k):
                extra_tags.append(f'#{k[:4]}')
            else:
                extra_tags.append(f'#{k[:8]}')

        # 组合标签
        tags = extra_tags + pool[:n]
        return tags[:max_c]

    def _generate_cover_suggestion(self, platform):
        """生成封面文案建议"""
        cfg = PLATFORMS[platform]
        core = self.topic_hint[:10]

        if platform == "douyin":
            return {
                "text": f"{core}🔥",
                "style": "大字+背景图",
                "colors": ["#FF6B6B", "#FFE66D"],
            }
        elif platform == "xhs":
            return {
                "text": f"✨{core}",
                "style": "简洁封面+emoji装饰",
                "colors": ["#FFFDD0", "#FFF8DC"],
            }
        else:
            return {
                "text": f"[{core}]",
                "style": "中括号+副标题",
                "colors": ["#00BFFF", "#1E90FF"],
            }

    def convert_all(self):
        """改写所有平台"""
        for platform in PLATFORMS:
            title, alt_titles = self._generate_title(platform)
            body = self._generate_body(platform)
            hashtags = self._generate_hashtags(platform)
            cover = self._generate_cover_suggestion(platform)
            cfg = PLATFORMS[platform]

            self.results[platform] = {
                "platform": cfg["name"],
                "emoji": cfg["emoji"],
                "title": title,
                "alternative_titles": alt_titles,
                "body": body,
                "hashtags": hashtags,
                "best_times": cfg["best_times"],
                "cover": cover,
            }

        return self.results

    def save_output(self, output_dir):
        """保存输出文件"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        summary = {
            "original_topic": self.topic_hint,
            "original_length": len(self.original),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "platforms": {},
        }

        for platform, result in self.results.items():
            # 保存各平台版本
            ext_map = {"douyin": "douyin", "xhs": "xhs", "bilibili": "bilibili"}
            filename = f"{ext_map[platform]}_version.md"
            filepath = output_path / filename

            lines = [
                f"# {result['emoji']} {result['platform']}版本\n",
                f"## 标题\n{result['title']}\n",
                "### 备选标题\n",
            ]
            for t in result["alternative_titles"]:
                lines.append(f"- {t}\n")

            lines += [
                f"\n## 正文\n{result['body']}\n",
                f"\n## 话题标签\n{' '.join(result['hashtags'])}\n",
                f"\n## 封面建议\n",
                f"- 文案：{result['cover']['text']}\n",
                f"- 风格：{result['cover']['style']}\n",
                f"\n## 最佳发布时间\n",
            ]
            for t in result["best_times"]:
                lines.append(f"- {t}\n")

            filepath.write_text("".join(lines), encoding="utf-8")
            summary["platforms"][platform] = {
                "title": result["title"],
                "hashtags": result["hashtags"],
                "best_times": result["best_times"],
            }

        # 保存总览JSON
        summary_path = output_path / "summary.json"
        summary_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        return str(output_path)


# ============ 入口 ============

def main():
    parser = argparse.ArgumentParser(description="一鱼三吃内容改写器")
    parser.add_argument("--input", type=str, default=None, help="输入内容")
    parser.add_argument("--input-file", type=str, default=None, help="输入文件路径")
    parser.add_argument("--topic", type=str, default="", help="主题提示")
    parser.add_argument("--platforms", type=str, default="douyin,xhs,bilibili",
                        help="目标平台（逗号分隔）")
    parser.add_argument("--output", type=str, default=None, help="输出目录")

    args = parser.parse_args()

    # 读取输入
    if args.input_file:
        text = Path(args.input_file).read_text(encoding="utf-8")
    elif args.input:
        text = args.input
    else:
        print("❌ 请提供 --input 或 --input-file 参数")
        sys.exit(1)

    # 输出目录
    if args.output:
        out_dir = args.output
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
        out_dir = str(Path.home() / "Desktop" / f"content_convert_{date_str}")

    # 执行转换
    print(f"\n🚀 正在改写内容...")
    print(f"📋 主题: {args.topic or text[:50]}...")
    print(f"🎯 平台: {args.platforms}\n")

    converter = ContentConverter(text, topic_hint=args.topic)
    results = converter.convert_all()

    # 输出结果
    for platform, r in results.items():
        print(f"{'='*50}")
        print(f"{r['emoji']} {r['platform']}")
        print(f"{'='*50}")
        print(f"📌 标题: {r['title']}")
        print(f"📝 正文: {r['body'][:100]}...")
        print(f"🏷️  标签: {' '.join(r['hashtags'])}")
        print(f"⏰ 发布时间: {', '.join(r['best_times'])}")
        print()

    # 保存
    output_path = converter.save_output(out_dir)
    print(f"✅ 文件已保存: {output_path}")

    return results


if __name__ == "__main__":
    main()
