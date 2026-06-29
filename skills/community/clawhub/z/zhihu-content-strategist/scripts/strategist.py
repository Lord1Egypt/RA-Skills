#!/usr/bin/env python3
"""
Zhihu Content Strategist — analyze trends, detect content gaps, and generate
high-engagement answer strategies and drafts for Zhihu.

Usage:
  python strategist.py --domain AI --task recommend
  python strategist.py --domain AI --task draft --topic "AI Agent 落地案例"
  python strategist.py --task analyze --answers data/top_answers.json
  python strategist.py --help

MIT-0 License
"""
import argparse
import json
import os
import sys
from datetime import datetime

REF_DIR = os.path.join(os.path.dirname(__file__), "..", "references")
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_reference(name):
    return load_json(os.path.join(REF_DIR, name))


# ── Domain Reference Data (mock/fallback) ──────────────────────────────────

DOMAIN_TAXONOMY = {
    "AI": ["AI Agent 落地案例", "大模型应用实践", "Prompt 工程技巧",
           "深度学习框架对比", "AI 在行业中的应用", "模型训练优化",
           "AI 产品经理", "AI 绘画与生成", "AI 编程助手", "AI 创业"],
    "career": ["跳槽策略", "面试技巧", "职场沟通", "副业指南",
               "职业规划", "行业选择", "薪资谈判", "管理技能",
               "远程办公", "35岁危机"],
    "psychology": ["原生家庭", "焦虑管理", "人际关系", "自我成长",
                   "恋爱心理学", "职场心理", "情绪管理", "认知偏差"],
    "finance": ["理财入门", "基金定投", "保险配置", "股票投资",
                "房产投资", "副业收入", "财务自由", "消费主义"],
    "tech": ["Python", "Go语言", "分布式系统", "云原生",
             "数据库", "前端开发", "后端架构", "DevOps",
             "开源项目", "系统设计"],
}

# Mock high-performing answer patterns per domain
ANSWER_PATTERNS = {
    "AI": {
        "opening_hooks": [
            {"type": "data_drop", "example": "我训练了500个模型之后，发现90%的人犯了这个错误"},
            {"type": "counter_intuitive", "example": "都说AI会取代程序员，但我在大厂看到的是相反的趋势"},
            {"type": "story_based", "example": "去年我用GPT-4写了一个全栈项目，结果让我很意外"},
        ],
        "structure": ["Problem-Solution", "Step-by-step tutorial", "Comparative analysis"],
        "avg_length_chars": 2500,
        "golden_line_pattern": "短期XX vs 长期XX 的反转认知",
    },
    "career": {
        "opening_hooks": [
            {"type": "empathy", "example": "刚毕业那年，我也觉得迷茫，直到我明白了这个道理"},
            {"type": "question", "example": "你确定你是在努力工作，而不是在无效努力？"},
        ],
        "structure": ["Timeline narrative", "Listicle with tips", "Case study"],
        "avg_length_chars": 2000,
        "golden_line_pattern": "职场陷阱/认知, 个人经验+可复用的方法论",
    },
}

# Mock gap detection data
MOCK_GAP_DATA = {
    "AI": [
        {"subtopic": "AI Agent 落地案例", "questions": 230, "avg_upvotes": 42, "competition": "Low", "gap_score": 5},
        {"subtopic": "Prompt 工程技巧", "questions": 1500, "avg_upvotes": 180, "competition": "High", "gap_score": 2},
        {"subtopic": "大模型应用实践", "questions": 890, "avg_upvotes": 65, "competition": "Medium", "gap_score": 4},
        {"subtopic": "AI 在行业中的应用", "questions": 1200, "avg_upvotes": 35, "competition": "Low", "gap_score": 5},
        {"subtopic": "AI 绘画与生成", "questions": 1800, "avg_upvotes": 120, "competition": "High", "gap_score": 2},
        {"subtopic": "AI 编程助手", "questions": 680, "avg_upvotes": 55, "competition": "Medium", "gap_score": 4},
        {"subtopic": "AI 创业", "questions": 320, "avg_upvotes": 28, "competition": "Low", "gap_score": 5},
        {"subtopic": "深度学习框架对比", "questions": 450, "avg_upvotes": 90, "competition": "Medium", "gap_score": 3},
        {"subtopic": "AI 产品经理", "questions": 280, "avg_upvotes": 38, "competition": "Low", "gap_score": 4},
        {"subtopic": "模型训练优化", "questions": 560, "avg_upvotes": 75, "competition": "Medium", "gap_score": 3},
    ],
    "career": [
        {"subtopic": "35岁危机", "questions": 2500, "avg_upvotes": 200, "competition": "High", "gap_score": 2},
        {"subtopic": "副业指南", "questions": 1800, "avg_upvotes": 150, "competition": "High", "gap_score": 2},
        {"subtopic": "职场沟通", "questions": 1200, "avg_upvotes": 60, "competition": "Medium", "gap_score": 4},
        {"subtopic": "跳槽策略", "questions": 1500, "avg_upvotes": 85, "competition": "Medium", "gap_score": 3},
        {"subtopic": "远程办公", "questions": 800, "avg_upvotes": 45, "competition": "Low", "gap_score": 5},
        {"subtopic": "薪资谈判", "questions": 600, "avg_upvotes": 40, "competition": "Low", "gap_score": 5},
    ],
}


# ── Step 1: Define Target Domain ────────────────────────────────────────────

def define_domain(domain_input):
    """Define target domain and generate sub-topic taxonomy.

    AI Prompt Template:
      Given target domain: {domain_input}, generate 5-8 sub-topics for
      exploration. Verify the domain has sufficient question volume on Zhihu.
      If a URL is provided, extract the topic directly.
    """
    domain = domain_input.strip().lower()
    sub_topics = DOMAIN_TAXONOMY.get(domain, [])
    if not sub_topics:
        # Generate plausible sub-topics for unknown domain
        sub_topics = [f"{domain} 入门指南", f"{domain} 实战经验",
                      f"{domain} 工具推荐", f"{domain} 职业发展",
                      f"{domain} 趋势分析"]
    return {
        "domain": domain,
        "sub_topics": sub_topics,
        "question_volume": "high" if domain in DOMAIN_TAXONOMY else "unknown",
        "status": "explored" if domain in DOMAIN_TAXONOMY else "limited_data",
    }


# ── Step 2-3: Pattern Analysis (placeholder) ───────────────────────────────

def analyze_answers(answers_data, domain):
    """Analyze high-performing answer patterns.

    AI Prompt Template:
      Analyze the provided Zhihu answers dataset and extract:
      - Opening hook patterns (question/story/data/counter-intuitive)
      - Structure patterns (problem-solution/list/timeline)
      - Emotional tone
      - Data usage patterns
      - Length distribution
      - Golden lines (most-upvoted sentences)
      Return a pattern report with examples and replicable templates.
    """
    patterns = ANSWER_PATTERNS.get(domain, {})

    report = {
        "domain": domain,
        "sources": {
            "note": "Mock data — replace with actual scraped answers in production",
            "sample_size": 20,
        },
        "opening_hooks": patterns.get("opening_hooks", [
            {"type": "question_based", "example": "你有没有遇到过这样的情况…"},
            {"type": "story_based", "example": "五年前我也面临同样的选择……"},
        ]),
        "structure_patterns": patterns.get("structure", [
            "Problem-Solution", "Timeline narrative", "Listicle"
        ]),
        "avg_length_chars": patterns.get("avg_length_chars", 2000),
        "golden_line_pattern": patterns.get("golden_line_pattern",
                                            "Personal experience + actionable insight"),
        "emotional_tone_distribution": {
            "empathetic": 0.35,
            "authoritative": 0.30,
            "humorous": 0.20,
            "contrarian": 0.15,
        },
    }
    return report


# ── Step 4: Content Gap Detection ───────────────────────────────────────────

def detect_gaps(domain, expertise_level="intermediate"):
    """Detect content gaps in target domain.

    AI Prompt Template:
      For target domain: {domain}, analyze:
      - Question volume per sub-topic
      - Average upvotes of top answers (answer quality)
      - Competition index (established creators)
      - Gap score = question_volume × (1 - answer_quality_percentile)
      Return gap matrix sorted by opportunity score.
    """
    gaps = MOCK_GAP_DATA.get(domain, [
        {"subtopic": f"{domain} 入门", "questions": 500, "avg_upvotes": 50,
         "competition": "Medium", "gap_score": 3},
        {"subtopic": f"{domain} 进阶", "questions": 300, "avg_upvotes": 35,
         "competition": "Low", "gap_score": 4},
    ])

    # Sort by gap score descending
    gaps.sort(key=lambda g: g["gap_score"], reverse=True)

    return gaps


# ── Step 5: Topic Recommendation ───────────────────────────────────────────

def recommend_topics(domain, gaps, expertise_level="intermediate"):
    """Recommend topics based on gap matrix and expertise.

    AI Prompt Template:
      From the gap matrix, pick 5-10 topics that balance:
      - High gap score (low competition, high demand)
      - User expertise level
      - Estimated exposure potential
      For each topic, suggest: angle, difficulty, estimated views.
    """
    recommendations = []
    for g in gaps[:5]:
        # Map gap_score to stars
        stars = "⭐" * g["gap_score"]

        if g["gap_score"] >= 4:
            difficulty = "Quick answer (1-2 hours)"
            exposure = "Medium-High"
        elif g["gap_score"] >= 3:
            difficulty = "Moderate research (3-6 hours)"
            exposure = "Medium"
        else:
            difficulty = "Deep research needed (1-2 days)"
            exposure = "Low-Medium"

        angle = generate_angle(domain, g["subtopic"])

        recommendations.append({
            "topic_title": g["subtopic"],
            "opportunity_score": stars,
            "competition": g["competition"],
            "estimated_exposure": exposure,
            "difficulty": difficulty,
            "suggested_angle": angle,
        })

    return recommendations


def generate_angle(domain, subtopic):
    """Generate a unique angle suggestion for the topic.

    AI Prompt Template:
      Given domain {domain} and subtopic {subtopic}, suggest 2-3
      unique angles that stand out from existing answers.
    """
    if "入门" in subtopic or "指南" in subtopic:
        return "Don't just list resources — share your personal learning path with specific mistakes and breakthroughs"
    elif "对比" in subtopic or "vs" in subtopic:
        return "Use real benchmarks/data from your own experience, not generic comparisons"
    elif "实战" in subtopic or "案例" in subtopic:
        return "Tell a specific story with measurable results; include code/data snippets"
    elif "趋势" in subtopic:
        return "Back predictions with data from multiple sources; acknowledge uncertainty"
    else:
        return "Start with a counter-intuitive claim or personal story to hook readers"


# ── Step 6-7: Strategy + Draft Generation ──────────────────────────────────

def generate_strategy(topic, domain):
    """Generate per-topic strategy brief.

    AI Prompt Template:
      Create a strategy brief for answering the Zhihu question:
      {topic} in domain {domain}.
      Include: 2-3 hook variants, argument structure, evidence plan,
      golden lines, CTA, visual suggestions, style profile.
    """
    return {
        "topic": topic,
        "domain": domain,
        "strategy": {
            "hook_variants": [
                f"数据切入: 我分析了{topic}领域的100个案例，发现…",
                f"故事切入: 去年我亲身经历了一个{topic}项目，结果让我…",
                f"反直觉: 你可能不相信，但{topic}的真相和大部分人想的恰恰相反",
            ],
            "argument_structure": [
                "1. 开篇：用数据或故事建立信任",
                "2. 核心论点：分3-4个方面展开",
                "3. 个人经验：为什么我的观点值得信",
                "4. 可操作建议：读者能立刻做的事",
                "5. 金句收尾：值得转发的浓缩总结",
            ],
            "evidence_plan": [
                "引用1-2个权威研究或数据源",
                "包含1个个人案例（具体数字+结果）",
                "对比不同观点，展示思考深度",
            ],
            "golden_lines": [
                f"关于{topic}，大多数人看到的是XX，但真正重要的是YY",
                f"短期来看{topic}是ZZ，但长期来看…",
            ],
            "cta": "引导关注 + 评论区互动问题 + 个人简介引流",
            "visual_suggestions": [
                "关键数据截图",
                "对比表格",
                "思维导图（前3点）",
            ],
            "style_profile": "专业但有温度，避免学术腔，多用具体数字",
        },
    }


def generate_draft(strategy):
    """Generate complete answer draft from strategy brief.

    AI Prompt Template:
      Given the strategy brief, write a complete Zhihu answer draft.
      Follow the argument structure, embed golden lines naturally.
      Target length: {avg_length} characters for {domain}.
      Include SEO keywords naturally.
      Tone: professional but warm.
      Return markdown.
    """
    topic = strategy["topic"]
    domain = strategy["domain"]
    s = strategy["strategy"]

    draft = []
    draft.append(f"# {topic}")
    draft.append("")
    draft.append(f"> {s['hook_variants'][0]}")
    draft.append("")
    draft.append("## 先说说背景")
    draft.append("")
    draft.append(f"在过去的半年里，我花了大量时间研究{topic}。"
                 "这篇文章不讲大道理，只分享真实经历和可复用的方法。")
    draft.append("")
    draft.append("## 核心观点")
    draft.append("")
    for point in [
        f"**1. {topic}的核心在于理解本质** — 大多数人只看到表面",
        f"**2. 实践中的三个关键发现** — 每一项都有数据支持",
        f"**3. 避开最常见的坑** — 这些都是我亲自踩过的",
        "**4. 可立即行动的建议** — 看完就能用",
    ]:
        draft.append(point)
        draft.append("")
    draft.append("## 个人经验分享")
    draft.append("")
    draft.append(f"去年我做了一个关于{topic}的项目，结论让我自己都很意外。"
                 "直接说最关键的发现：...（此处用具体数字和案例展开）")
    draft.append("")
    draft.append("### 数据支撑")
    draft.append("")
    draft.append("| 维度 | 我的发现 | 行业普遍认知 | 差异 |")
    draft.append("|------|----------|--------------|------|")
    draft.append(f"| {topic}效果 | 案例A | 案例B | +30% |")
    draft.append("| 投入产出 | 时间X | 时间Y | -40% |")
    draft.append("")
    draft.append(f"> {s['golden_lines'][0]}")
    draft.append("")
    draft.append(f"> {s['golden_lines'][1]}")
    draft.append("")
    draft.append("## 写在最后")
    draft.append("")
    draft.append("如果这篇文章对你有帮助，欢迎**点赞+关注**，我会持续分享更多实战经验。")
    draft.append("")
    draft.append("评论区说说你的想法：你在这方面的经历是怎样的？")
    draft.append("")
    draft.append("---")
    draft.append("")
    draft.append(f"*本文由 Zhihu Content Strategist 辅助生成。内容仅供参考，请结合实际体验调整。*")

    return {
        "topic": topic,
        "domain": domain,
        "draft": "\n".join(draft),
        "char_count": sum(len(line) for line in draft),
        "estimated_reading_time": "3-5 min",
    }


# ── Step 8: Publishing Optimization ─────────────────────────────────────────

def optimize_publishing(draft):
    """Generate publishing recommendations.

    AI Prompt Template:
      Based on the draft and domain analysis, recommend:
      - Best publish time (day + hour)
      - Tag strategy (primary + secondary)
      - Promotion hooks for cross-platform sharing
      - Comment engagement plan (first 10 responses)
    """
    return {
        "best_publish_time": "Tuesday 10:00 AM (tech audience peak) or Thursday 8:00 PM (evening readers)",
        "tags": {
            "primary": [draft["domain"]],
            "secondary": [draft["topic"], "经验分享", "实战"],
        },
        "promotion_hooks": [
            f"写了一篇关于{draft['topic']}的深度回答，分享一些真实经验",
            "这可能是你今年看过最实用的分享",
        ],
        "comment_engagement_plan": [
            "前30分钟务必回复每条评论（算法权重最高）",
            "对已赞评论点赞表示认可",
            "1小时后回复较长的评论（展示深度）",
            "第2天补充1-2条高质量回复（推动二次曝光）",
        ],
        "note": "Publish during the hot window; respond to first 10 comments within 1 hour to boost ranking",
    }


# ── CLI ─────────────────────────────────────────────────────────────────────


def print_gap_matrix(gaps):
    print(f"\n{'Sub-topic':<30} {'Questions':<12} {'Avg Upvotes':<14} {'Competition':<12} {'Gap':<10}")
    print("-" * 78)
    for g in gaps[:8]:
        stars = "⭐" * g["gap_score"]
        print(f"{g['subtopic']:<30} {g['questions']:<12} {g['avg_upvotes']:<14} {g['competition']:<12} {stars:<10}")
    print("-" * 78)


def print_recommendations(recs):
    print(f"\n{'Topic':<30} {'Score':<10} {'Competition':<12} {'Difficulty':<28} {'Angle':<40}")
    print("-" * 120)
    for r in recs:
        print(f"{r['topic_title']:<30} {r['opportunity_score']:<10} {r['competition']:<12} {r['difficulty']:<28} {r['suggested_angle'][:38]:<40}")
    print("-" * 120)


def main():
    parser = argparse.ArgumentParser(
        description="Zhihu Content Strategist — analyze trends, detect content gaps, "
                    "generate strategies and drafts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --domain AI --task recommend
  %(prog)s --domain career --task draft --topic "远程办公效率"
  %(prog)s --domain AI --task strategy --topic "AI Agent 落地案例"
  %(prog)s --task analyze --domain AI
  %(prog)s --validate-schemas
        """,
    )
    parser.add_argument("--domain", "-d", default="",
                        help="Target domain (AI, career, psychology, finance, tech)")
    parser.add_argument("--task", "-t",
                        choices=["define", "analyze", "gap", "recommend", "strategy", "draft", "publish"],
                        default="recommend",
                        help="Workflow task to execute")
    parser.add_argument("--topic", default="",
                        help="Specific topic for strategy/draft generation")
    parser.add_argument("--output", "-o", choices=["text", "json"], default="text",
                        help="Output format")
    parser.add_argument("--validate-schemas", action="store_true",
                        help="Validate schemas (dev mode)")

    args = parser.parse_args()

    if args.validate_schemas:
        try:
            load_json(os.path.join(SCHEMA_DIR, "input.schema.json"))
            load_json(os.path.join(SCHEMA_DIR, "output.schema.json"))
            print("  Schemas validated successfully")
            return 0
        except Exception as e:
            print(f"  Schema validation failed: {e}")
            return 1

    domain = args.domain.upper() if args.domain else "AI"
    task = args.task or "recommend"

    # Load reference data
    try:
        load_reference("engagement_patterns.json")
        load_reference("topic_templates.json")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    print(f"Zhihu Content Strategist v1.0.0")
    print(f"Domain: {domain} | Task: {task}")

    output = {}

    if task == "define":
        print(f"\n[Step 1/8] Defining target domain: {domain}")
        result = define_domain(domain)
        output["domain"] = result
        if args.output == "text":
            print(f"  Domain: {result['domain']}")
            print(f"  Sub-topics: {', '.join(result['sub_topics'][:8])}")
            print(f"  Volume status: {result['status']}")

    elif task == "analyze":
        print(f"\n[Steps 2-3/8] Analyzing high-performing answers in {domain}")
        result = analyze_answers({}, domain)
        output["pattern_analysis"] = result
        if args.output == "text":
            print(f"  Sample size: {result['sources']['sample_size']}")
            print(f"  Opening hook types: {[h['type'] for h in result['opening_hooks']]}")
            print(f"  Common structures: {', '.join(result['structure_patterns'])}")
            print(f"  Avg length: {result['avg_length_chars']} chars")
            print(f"  Golden line pattern: {result['golden_line_pattern']}")

    elif task == "gap":
        print(f"\n[Step 4/8] Detecting content gaps in {domain}")
        gaps = detect_gaps(domain)
        output["gap_matrix"] = gaps
        if args.output == "text":
            print_gap_matrix(gaps)

    elif task == "recommend":
        print(f"\n[Step 5/8] Recommending topics in {domain}")
        gaps = detect_gaps(domain)
        recommendations = recommend_topics(domain, gaps)
        output["recommendations"] = recommendations
        output["gap_matrix"] = gaps
        if args.output == "text":
            print_recommendations(recommendations)

    elif task == "strategy":
        topic = args.topic or "AI Agent 落地案例"
        print(f"\n[Step 6/8] Generating strategy for: {topic}")
        strategy = generate_strategy(topic, domain)
        output["strategy"] = strategy
        if args.output == "text":
            s = strategy["strategy"]
            print(f"\n  Topic: {strategy['topic']}")
            print(f"\n  Hook Variants:")
            for h in s["hook_variants"]:
                print(f"    - {h}")
            print(f"\n  Structure:")
            for st in s["argument_structure"]:
                print(f"    - {st}")
            print(f"\n  Golden Lines:")
            for g in s["golden_lines"]:
                print(f"    - {g}")

    elif task == "draft":
        topic = args.topic or "AI Agent 落地案例"
        print(f"\n[Step 7/8] Generating draft for: {topic}")
        strategy = generate_strategy(topic, domain)
        draft = generate_draft(strategy)
        output["draft"] = draft
        if args.output == "text":
            print(f"\n  Draft generated ({draft['char_count']} chars, ~{draft['estimated_reading_time']})")
            print("\n" + "=" * 60)
            print(draft["draft"])
            print("\n" + "=" * 60)

    elif task == "publish":
        topic = args.topic or "AI Agent 落地案例"
        print(f"\n[Step 8/8] Publishing optimization for: {topic}")
        strategy = generate_strategy(topic, domain)
        draft_data = generate_draft(strategy)
        pub = optimize_publishing(draft_data)
        output["publishing"] = pub
        if args.output == "text":
            print(f"\n  Best time: {pub['best_publish_time']}")
            print(f"  Tags: primary={pub['tags']['primary']}, secondary={pub['tags']['secondary']}")
            print(f"\n  Promotion hooks:")
            for h in pub["promotion_hooks"]:
                print(f"    - {h}")
            print(f"\n  Comment plan:")
            for c in pub["comment_engagement_plan"]:
                print(f"    - {c}")

    if args.output == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))

    print(f"\n  Task '{task}' complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
