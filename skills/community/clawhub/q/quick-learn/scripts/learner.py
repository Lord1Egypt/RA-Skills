#!/usr/bin/env python3
"""
Quick Learn Helper Script — 快速学习辅助脚本
Generate learning path structure + quiz templates
生成学习路径结构 + 自测题目

Usage / 用法:
  python3 learner.py path <topic> <days> --output <json_path>
  python3 learner.py path <topic> <days> --lang en --output <json_path>
  python3 learner.py quiz  <path_json> <day_label> --output <json_path>
  python3 learner.py list --dir learning-data
"""

import json, sys, os, argparse, glob
from datetime import datetime, timedelta

# Bilingual title templates / 双语标题模板
DAY_TITLES_EN = [
    "Build Awareness",        # Day 1
    "Core Concepts Deep Dive", # Day 2
    "Core Architecture",       # Day 3
    "Hands-on Practice",       # Day 4
    "Best Practices & Pitfalls", # Day 5
    "Advanced Topics",         # Day 6
    "Summary & Self-test",     # Day 7+
]

DAY_TITLES_ZH = [
    "建立认知",        # Day 1
    "深入核心概念",    # Day 2
    "核心架构",        # Day 3
    "动手实践",        # Day 4
    "最佳实践与踩坑",  # Day 5
    "进阶主题",        # Day 6
    "总结与自测",      # Day 7+
]

FEYNMAN_PROMPT_TEMPLATES_EN = [
    "Try to explain in your own words: What is {topic}? Why is it needed?",
    "Explain the core concepts of {topic} as if teaching a beginner. What problem does it solve?",
    "How does {topic} work under the hood? Walk through the key mechanisms.",
    "If you had to build something with {topic}, what would your approach be and why?",
    "What are the common pitfalls in {topic}? How would you avoid them?",
    "Compare {topic} with alternatives. When would you choose it and when not?",
    "Summarize everything you've learned about {topic}. What surprised you most?",
]

FEYNMAN_PROMPT_TEMPLATES_ZH = [
    "试着用你自己的话解释：{topic} 是什么？为什么需要它？",
    "像教新手一样解释 {topic} 的核心概念。它解决什么问题？",
    "{topic} 底层是怎么工作的？逐步讲解关键机制。",
    "如果你要用 {topic} 构建一个东西，你会怎么做？为什么？",
    "{topic} 有哪些常见的坑？你会如何避免？",
    "对比 {topic} 和替代方案。什么时候选它？什么时候不选？",
    "总结一下你学到的关于 {topic} 的所有内容。什么最让你意外？",
]

SIMPLIFY_TARGET_TEMPLATES_EN = [
    "Imagine you're explaining to someone who knows nothing about it.",
    "Use a real-life analogy to explain the core mechanism.",
    "Simplify it so a non-technical person would understand.",
    "Explain it like you're talking to a friend at a coffee shop.",
    "If you had to explain it in 3 sentences, what would you say?",
    "Use an everyday analogy to describe how it works.",
    "What's the simplest way to describe the essence of {topic}?",
]

SIMPLIFY_TARGET_TEMPLATES_ZH = [
    "想象你在给一个完全不懂的人解释。",
    "用一个生活中的类比来解释核心机制。",
    "简化到不懂技术的人也能听懂。",
    "像在咖啡厅跟朋友聊天一样解释。",
    "如果只能用 3 句话说清楚，你会怎么说？",
    "用日常生活中的例子来描述它是如何工作的。",
    "用最简单的方式描述 {topic} 的本质是什么？",
]


def get_timezone():
    """Auto-detect system timezone, fallback to UTC."""
    try:
        import time
        tz = time.tzname[0]
        return tz if tz else "UTC"
    except Exception:
        return "UTC"


def generate_path(topic, days, output=None, lang="auto"):
    """Generate a learning path JSON structure."""
    # Input validation
    if not topic or not topic.strip():
        print("Error: Topic cannot be empty. / 错误：主题不能为空。")
        sys.exit(1)
    if days < 1:
        print("Warning: Days must be at least 1, setting to 3 (minimum). / 警告：天数至少为1，已设为3（最低值）。")
        days = 3
    
    # Sanitize slug: only lowercase alphanumeric and hyphens
    import re
    slug = topic.lower().strip()
    slug = re.sub(r'[^a-z0-9\u4e00-\u9fff-]', '-', slug)  # Keep Chinese chars, replace rest
    slug = re.sub(r'-+', '-', slug).strip('-')  # Collapse multiple hyphens
    if not slug:
        slug = "unknown-topic"
    
    # Auto-detect language from topic or use specified
    if lang == "auto":
        # Simple heuristic: if topic contains Chinese chars, use ZH
        lang = "zh" if any('\u4e00' <= c <= '\u9fff' for c in topic) else "en"
    
    # Select templates based on language
    titles = DAY_TITLES_ZH if lang == "zh" else DAY_TITLES_EN
    feynman_templates = FEYNMAN_PROMPT_TEMPLATES_ZH if lang == "zh" else FEYNMAN_PROMPT_TEMPLATES_EN
    simplify_templates = SIMPLIFY_TARGET_TEMPLATES_ZH if lang == "zh" else SIMPLIFY_TARGET_TEMPLATES_EN
    
    path = {
        "topic": topic,
        "slug": slug,
        "total_days": days,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "status": "active",
        "current_day": 1,
        "daily_time_min": 30,
        "preferred_time": "09:00",
        "timezone": get_timezone(),
        "push_channel": "webchat",
        "learning_method": "feynman",
        "language": lang,
        "days": []
    }
    
    for i in range(1, days + 1):
        # Pick template by day index (cycle with variation for long plans)
        if i <= len(titles):
            idx = i - 1
        else:
            # For plans > 7 days, cycle with day-specific modifiers
            cycle_idx = (i - 1) % len(titles)
            idx = cycle_idx
        
        title = titles[idx]
        # Add day number suffix for plans > 7 days to differentiate repeated titles
        if i > len(titles):
            title = f"{title} (Part {i - len(titles)})"
        
        feynman_prompt = feynman_templates[idx].format(topic=topic)
        simplify_target = simplify_templates[idx].format(topic=topic)
        
        path["days"].append({
            "day": i,
            "title": title,
            "keywords": [],
            "feynman_prompt": feynman_prompt,
            "simplify_target": simplify_target,
            "completed": False,
            "completed_at": None
        })
    
    result = json.dumps(path, ensure_ascii=False, indent=2)
    if output:
        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
        with open(output, "w") as f:
            f.write(result)
        lang_label = "中文" if lang == "zh" else "English"
        print(f"Path saved to {output} (slug: {slug}, language: {lang_label})")
    else:
        print(result)


def generate_quiz(path_json, day_label, output=None):
    """Generate a quiz template based on the learning path."""
    try:
        with open(path_json) as f:
            path = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {path_json}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path_json}: {e}")
        sys.exit(1)
    
    quiz = {
        "topic": path["topic"],
        "day_label": day_label,
        "language": path.get("language", "auto"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "questions": []
    }
    
    result = json.dumps(quiz, ensure_ascii=False, indent=2)
    if output:
        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
        with open(output, "w") as f:
            f.write(result)
        print(f"Quiz template saved to {output}")
    else:
        print(result)


def list_plans(data_dir):
    """List all active learning plans."""
    pattern = os.path.join(data_dir, "*", "path.json")
    files = sorted(glob.glob(pattern))
    if not files:
        print("No active learning plans found. / 没有找到活跃的学习计划。")
        return
    for f in files:
        try:
            with open(f) as fh:
                d = json.load(fh)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read {f}: {e}")
            continue
        status_icon = "✅" if d["status"] == "completed" else "🚀" if d["status"] == "active" else "⏸"
        day_info = f"Day {d['current_day']}/{d['total_days']}"
        lang = d.get("language", "auto")
        lang_tag = f"[ZH]" if lang == "zh" else f"[EN]" if lang == "en" else ""
        print(f"{status_icon} {d['topic']} ({d.get('slug', '?')}) {lang_tag} — {day_info} | {d['status']} | Created: {d['created_at']}")


def main():
    parser = argparse.ArgumentParser(
        description="Quick Learn Helper / 快速学习辅助脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples / 示例:
  python3 learner.py path "React Basics" 7 --output learning-data/react-intro/path.json
  python3 learner.py path "机器学习" 5 --lang zh --output learning-data/ml-intro/path.json
  python3 learner.py quiz learning-data/react-intro/path.json day-1
  python3 learner.py list --dir learning-data
        """
    )
    sub = parser.add_subparsers(dest="cmd")
    
    p1 = sub.add_parser("path", help="Generate learning path / 生成学习路径")
    p1.add_argument("topic", help="Learning topic / 学习主题")
    p1.add_argument("days", type=int, help="Number of days / 天数")
    p1.add_argument("--output", help="Output file path / 输出文件路径")
    p1.add_argument("--lang", choices=["en", "zh", "auto"], default="auto",
                    help="Language: en=English, zh=Chinese, auto=detect (default) / 语言")
    
    p2 = sub.add_parser("quiz", help="Generate quiz template / 生成自测模板")
    p2.add_argument("path_json", help="Path to path.json / path.json 路径")
    p2.add_argument("day_label", help="Day label (e.g., day-1) / 日期标签")
    p2.add_argument("--output", help="Output file path / 输出文件路径")
    
    p3 = sub.add_parser("list", help="List learning plans / 列出学习计划")
    p3.add_argument("--dir", default="learning-data", help="Data directory / 数据目录")
    
    args = parser.parse_args()
    if args.cmd == "path":
        generate_path(args.topic, args.days, args.output, args.lang)
    elif args.cmd == "quiz":
        generate_quiz(args.path_json, args.day_label, args.output)
    elif args.cmd == "list":
        list_plans(args.dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
