#!/usr/bin/env python3
"""
memory_insight.py - AI 记忆洞察与自我进化

功能:
  1. 分析记忆使用模式，发现规律和趋势
  2. 生成洞察报告，帮助理解自己
  3. 自动标记重要记忆，优化向量权重
  4. 发现知识盲点，建议补充

用法:
  python scripts/memory_insight.py --uid pupper                    # 综合洞察
  python scripts/memory_insight.py --uid pupper --daily          # 每日洞察
  python scripts/memory_insight.py --uid pupper --weekly           # 每周洞察
  python scripts/memory_insight.py --uid pupper --auto-mark       # 自动标记重要记忆
  python scripts/memory_insight.py --uid pupper --find-gaps        # 发现知识盲点
  python scripts/memory_insight.py --uid pupper --learn-patterns   # 学习记忆模式

依赖:
  pip install openai numpy
"""

import os
import sys
import json
import sqlite3
import argparse
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import Counter, defaultdict

# 添加 embed_backends 路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


DB_NAME = ".memory_vectors.db"
ACCESS_DB = ".memory_access_log.db"


# ══════════════════════════════════════════════════════════════
#  数据提取
# ══════════════════════════════════════════════════════════════

def get_db_path(base_dir):
    return os.path.join(os.path.abspath(base_dir), DB_NAME)


def connect_db(db_path):
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def extract_memories(conn, uid, days=None, scope="private"):
    """提取记忆数据"""
    c = conn.cursor()

    if days:
        since = (datetime.now() - timedelta(days=days)).timestamp()
        time_filter = f"AND mtime >= {since}"
    else:
        time_filter = ""

    scope_filter = f"AND scope = '{scope}'" if scope != "all" else ""

    c.execute(f"""
        SELECT chunk_id, title, content, level, importance_score,
               related_ids, mtime, created_at
        FROM memory_embeddings
        WHERE (uid = ? OR uid = 'shared') {scope_filter} {time_filter}
        ORDER BY mtime DESC
    """, (uid,))

    cols = [desc[0] for desc in c.description]
    return [dict(zip(cols, row)) for row in c.fetchall()]


def extract_access_patterns(base_dir, uid, days=7):
    """提取访问模式"""
    access_db = os.path.join(os.path.abspath(base_dir), ACCESS_DB)
    if not os.path.exists(access_db):
        return {}

    conn = sqlite3.connect(access_db)
    c = conn.cursor()

    since = (datetime.now() - timedelta(days=days)).timestamp()
    c.execute("""
        SELECT chunk_id, access_type, COUNT(*) as cnt,
               MAX(access_time) as last_access
        FROM memory_access_log
        WHERE uid = ? AND access_time >= ?
        GROUP BY chunk_id, access_type
    """, (uid, since))

    patterns = defaultdict(lambda: {"count": 0, "types": Counter(), "last": 0})
    for chunk_id, access_type, cnt, last in c.fetchall():
        patterns[chunk_id]["count"] += cnt
        patterns[chunk_id]["types"][access_type] = cnt
        patterns[chunk_id]["last"] = max(patterns[chunk_id]["last"], last)

    conn.close()
    return dict(patterns)


def analyze_topics(memories):
    """分析记忆主题"""
    # 简单的关键词提取
    stop_words = {"的", "是", "在", "了", "和", "与", "或", "为", "上", "下", "中", "后", "前", "我", "你", "他", "它", "我们", "你们", "他们"}

    all_text = " ".join(m.get("content", "") + " " + m.get("title", "") for m in memories)

    # 提取中文字符序列作为词
    words = re.findall(r'[\u4e00-\u9fff]{2,}', all_text)
    words = [w for w in words if w not in stop_words]

    # 词频统计
    word_freq = Counter(words)
    return word_freq.most_common(20)


def analyze_level_distribution(memories):
    """分析层级分布"""
    levels = Counter(m.get("level", "L1") for m in memories)
    return dict(levels)


def analyze_related_strength(memories):
    """分析关联强度"""
    strong_related = 0  # 有超过3条关联的记忆
    weak_related = 0    # 有关联但少于3条
    no_related = 0      # 无关联

    for m in memories:
        rids = m.get("related_ids", "[]")
        try:
            related = json.loads(rids) if rids else []
            if len(related) >= 3:
                strong_related += 1
            elif len(related) > 0:
                weak_related += 1
            else:
                no_related += 1
        except:
            no_related += 1

    return {
        "strong": strong_related,
        "weak": weak_related,
        "none": no_related
    }


def analyze_importance_distribution(memories):
    """分析重要性分布"""
    scores = [m.get("importance_score", 50) for m in memories]
    if not scores:
        return {"avg": 50, "high": 0, "medium": 0, "low": 0}

    avg = sum(scores) / len(scores)
    high = sum(1 for s in scores if s >= 75)
    medium = sum(1 for s in scores if 50 <= s < 75)
    low = sum(1 for s in scores if s < 50)

    return {
        "avg": avg,
        "high": high,
        "medium": medium,
        "low": low
    }


def analyze_recency(memories):
    """分析记忆新鲜度"""
    now = datetime.now().timestamp()
    recency = {
        "today": 0,
        "week": 0,
        "month": 0,
        "older": 0
    }

    for m in memories:
        mtime = m.get("mtime", 0)
        age_days = (now - mtime) / 86400

        if age_days < 1:
            recency["today"] += 1
        elif age_days < 7:
            recency["week"] += 1
        elif age_days < 30:
            recency["month"] += 1
        else:
            recency["older"] += 1

    return recency


def detect_patterns(memories, access_patterns):
    """检测记忆模式"""
    patterns = []

    # 模式1：高访问低重要性 -> 建议提升权重
    for m in memories:
        cid = m.get("chunk_id")
        if cid in access_patterns:
            access_cnt = access_patterns[cid]["count"]
            importance = m.get("importance_score", 50)
            if access_cnt > 10 and importance < 60:
                patterns.append({
                    "type": "high_access_low_importance",
                    "chunk_id": cid,
                    "title": m.get("title"),
                    "access_count": access_cnt,
                    "current_importance": importance,
                    "suggestion": f"该记忆被访问 {access_cnt} 次，建议提升重要性评分"
                })

    # 模式2：孤立记忆（无关联）-> 建议手动关联
    for m in memories:
        rids = m.get("related_ids", "[]")
        try:
            related = json.loads(rids) if rids else []
            if len(related) == 0 and m.get("importance_score", 50) > 70:
                patterns.append({
                    "type": "isolated_important",
                    "chunk_id": m.get("chunk_id"),
                    "title": m.get("title"),
                    "importance": m.get("importance_score"),
                    "suggestion": "重要记忆无关联，建议检查并建立关联"
                })
        except:
            pass

    # 模式3：同一主题频繁记录 -> 可能需要整合
    topics = Counter()
    for m in memories:
        content = m.get("content", "") + m.get("title", "")
        # 提取前5个字符作为简化的主题标识
        words = re.findall(r'[\u4e00-\u9fff]{3,}', content)
        if words:
            topics[words[0]] += 1

    for topic, cnt in topics.items():
        if cnt >= 5:
            patterns.append({
                "type": "frequent_topic",
                "topic": topic,
                "count": cnt,
                "suggestion": f"'{topic}' 主题已记录 {cnt} 次，建议整合"
            })

    return patterns


def find_knowledge_gaps(memories, topics):
    """发现知识盲点"""
    gaps = []

    # 基于已有主题，推测可能缺失的领域
    known_topics = set(t[0] for t in topics)

    # 常见技术领域（可以根据用户角色调整）
    common_domains = [
        ("架构设计", ["架构", "架构师", "设计模式", "系统设计"]),
        ("性能优化", ["性能", "优化", "benchmark", "profiling"]),
        ("安全", ["安全", "加密", "认证", "授权"]),
        ("测试", ["测试", "单元测试", "集成测试", "E2E"]),
        ("DevOps", ["部署", "CI/CD", "Docker", "K8s"]),
        ("数据库", ["数据库", "SQL", "索引", "优化"]),
        ("前端", ["React", "Vue", "CSS", "前端"]),
        ("后端", ["API", "微服务", "Node", "Python", "Go"]),
    ]

    for domain, keywords in common_domains:
        domain_mentioned = any(kw in " ".join(known_topics) for kw in keywords)
        if not domain_mentioned:
            gaps.append({
                "domain": domain,
                "suggestion": f"缺少{domain}相关记录，建议补充"
            })

    return gaps


# ══════════════════════════════════════════════════════════════
#  报告生成
# ══════════════════════════════════════════════════════════════

def generate_summary_report(memories, access_patterns, topics, uid):
    """生成综合洞察报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    level_dist = analyze_level_distribution(memories)
    related_stats = analyze_related_strength(memories)
    importance_dist = analyze_importance_distribution(memories)
    recency_dist = analyze_recency(memories)
    patterns = detect_patterns(memories, access_patterns)
    gaps = find_knowledge_gaps(memories, topics)

    # 洞察生成
    insights = []

    # 层级洞察
    total = len(memories)
    if total > 0:
        if level_dist.get("L3", 0) / total < 0.1:
            insights.append("📚 永久记忆较少，考虑将核心知识升级到 L3")
        if level_dist.get("L1", 0) / total > 0.7:
            insights.append("⚠️  临时记忆过多，建议定期整理，重要内容升级到 L2/L3")

    # 重要性洞察
    if importance_dist["avg"] < 50:
        insights.append("📊 平均重要性偏低，记忆可能缺乏足够的访问和关注")

    # 关联洞察
    if related_stats["none"] / total > 0.5:
        insights.append("🔗 大量记忆无关联，建议使用语义搜索重新整理")

    # 模式洞察
    high_access = [p for p in patterns if p["type"] == "high_access_low_importance"]
    if high_access:
        insights.append(f"🔥 发现 {len(high_access)} 条高访问低重要性记忆，建议提升权重")

    # 趋势洞察
    recent = sum(recency_dist.values())
    if recent < 5:
        insights.append("📝 最近记忆较少，建议保持每日记录习惯")

    report = f"""# 🧠 AI 记忆洞察报告

**生成时间**: {now}
**用户**: {uid}
**记忆总数**: {total}

---

## 📊 记忆概览

| 指标 | 数值 |
|------|------|
| 私人记忆 | {level_dist.get('private', 0)} 条 |
| 公共记忆 | {level_dist.get('shared', 0)} 条 |
| L1 临时 | {level_dist.get('L1', 0)} 条 ({level_dist.get('L1', 0)/max(total,1)*100:.0f}%) |
| L2 长期 | {level_dist.get('L2', 0)} 条 ({level_dist.get('L2', 0)/max(total,1)*100:.0f}%) |
| L3 永久 | {level_dist.get('L3', 0)} 条 ({level_dist.get('L3', 0)/max(total,1)*100:.0f}%) |

---

## ⭐ 重要性分布

- **高重要性** (≥75): {importance_dist['high']} 条
- **中等** (50-74): {importance_dist['medium']} 条
- **低** (<50): {importance_dist['low']} 条
- **平均分**: {importance_dist['avg']:.1f}

---

## 🔗 关联分析

| 类型 | 数量 |
|------|------|
| 强关联 (≥3条) | {related_stats['strong']} 条 |
| 弱关联 (1-2条) | {related_stats['weak']} 条 |
| 无关联 | {related_stats['none']} 条 |

---

## ⏰ 时间分布

| 时间范围 | 数量 |
|----------|------|
| 今天 | {recency_dist['today']} 条 |
| 近7天 | {recency_dist['week']} 条 |
| 近30天 | {recency_dist['month']} 条 |
| 更早 | {recency_dist['older']} 条 |

---

## 🔥 发现的问题

"""

    if patterns:
        for i, p in enumerate(patterns[:5], 1):
            report += f"{i}. **{p['suggestion']}**\nfrom typing import List, Dict, Optional, Union, Any, Tuple\n"
            if "title" in p:
                report += f"   - {p['title']}\n"
    else:
        report += "暂未发现问题 ✓\n"

    report += "\n---\n\n## 💡 AI 洞察\n\n"
    if insights:
        for insight in insights:
            report += f"- {insight}\n"
    else:
        report += "- 记忆系统运行良好，继续保持！\n"

    report += "\n---\n\n## 🎯 建议补充的知识领域\n\n"

    if gaps:
        for g in gaps[:5]:
            report += f"- {g['suggestion']}\n"
    else:
        report += "- 知识覆盖良好！\n"

    return report


def generate_daily_report(memories, access_patterns, uid):
    """生成每日洞察"""
    now = datetime.now().strftime("%Y-%m-%d")

    today_memories = [m for m in memories if (datetime.now().timestamp() - m.get("mtime", 0)) < 86400]
    today_access = {cid: p for cid, p in access_patterns.items() if p["last"] > (datetime.now() - timedelta(days=1)).timestamp()}

    report = f"""# 📅 每日洞察 - {now}

**用户**: {uid}

---

## 📝 今日记忆

- 新增记忆: {len(today_memories)} 条

"""

    if today_memories:
        report += "### 最新记录\n\n"
        for m in today_memories[:5]:
            report += f"- [{m.get('level', 'L1')}] {m.get('title', '无标题')}\n"
            report += f"  {m.get('content', '')[:80]}...\n\n"

    report += "\n## 🔍 今日搜索\n\n"
    search_access = [cid for cid, p in today_access.items() if "search" in p.get("types", {})]
    if search_access:
        report += f"搜索了 {len(search_access)} 条记忆\n"
    else:
        report += "今日暂无搜索记录\n"

    report += "\n---\n\n## 💡 每日建议\n\n"

    if len(today_memories) == 0:
        report += "- 今日尚未记录，养成每日总结的习惯很重要\n"
    elif len(today_memories) < 3:
        report += "- 今日记录较少，考虑补充更多细节\n"
    else:
        report += "- 今日记录良好！\n"

    return report


def generate_weekly_report(memories, access_patterns, uid):
    """生成每周洞察"""
    now = datetime.now().strftime("%Y-W%W")

    week_memories = [m for m in memories if (datetime.now().timestamp() - m.get("mtime", 0)) < 7 * 86400]
    topics = analyze_topics(week_memories)
    level_dist = analyze_level_distribution(week_memories)

    report = f"""# 📆 每周洞察 - {now}

**用户**: {uid}

---

## 📊 本周概况

| 指标 | 数值 |
|------|------|
| 本周新增 | {len(week_memories)} 条 |
| L1 临时 | {level_dist.get('L1', 0)} 条 |
| L2 长期 | {level_dist.get('L2', 0)} 条 |
| L3 永久 | {level_dist.get('L3', 0)} 条 |

---

## 🔥 本周热点主题

"""

    if topics:
        for i, (topic, cnt) in enumerate(topics[:10], 1):
            report += f"{i}. **{topic}** ({cnt} 次)\n"
    else:
        report += "本周暂无主题记录\n"

    report += "\n---\n\n## 📈 本周趋势\n\n"

    daily_counts = Counter()
    for m in week_memories:
        mtime = datetime.fromtimestamp(m.get("mtime", 0))
        daily_counts[mtime.strftime("%Y-%m-%d")] += 1

    for day in sorted(daily_counts.keys()):
        cnt = daily_counts[day]
        bar = "█" * cnt + "░" * max(0, 10 - cnt)
        report += f"{day}: {bar} {cnt}条\n"

    report += "\n---\n\n## 🧠 本周总结\n\n"

    if len(week_memories) < 7:
        report += f"- 本周记录较少（{len(week_memories)}条），建议增加记录频率\n"
    elif len(week_memories) > 30:
        report += "- 本周记录丰富，注意定期整理和归档\n"
    else:
        report += "- 记录节奏良好\n"

    if level_dist.get("L3", 0) == 0 and level_dist.get("L2", 0) > 5:
        report += "- 本周有内容可考虑升级到永久记忆\n"

    return report


# ══════════════════════════════════════════════════════════════
#  自动标记
# ══════════════════════════════════════════════════════════════

def auto_mark_importance(conn, memories, access_patterns):
    """自动标记高价值记忆"""
    c = conn.cursor()
    marked = 0

    for m in memories:
        cid = m.get("chunk_id")
        current_score = m.get("importance_score", 50)

        # 如果是高访问记忆，但重要性低 -> 提升
        if cid in access_patterns:
            access_cnt = access_patterns[cid]["count"]
            if access_cnt >= 10 and current_score < 70:
                new_score = min(100, current_score + 20)
                c.execute(
                    "UPDATE memory_embeddings SET importance_score = ? WHERE chunk_id = ?",
                    (new_score, cid)
                )
                marked += 1

        # 如果是永久记忆且无重要标记 -> 确保至少70分
        if m.get("level") == "L3" and current_score < 70:
            c.execute(
                "UPDATE memory_embeddings SET importance_score = ? WHERE chunk_id = ?",
                (70, cid)
            )
            marked += 1

    conn.commit()
    return marked


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

def generate_insight(base_dir, uid, report_type="summary", days=None):
    """生成洞察报告"""
    db_path = get_db_path(base_dir)
    conn = connect_db(db_path)

    if conn is None:
        raise Exception(f"向量数据库不存在: {db_path}")

    memories = extract_memories(conn, uid, days)
    access_patterns = extract_access_patterns(base_dir, uid, days or 7)
    topics = analyze_topics(memories)

    if report_type == "daily":
        report = generate_daily_report(memories, access_patterns, uid)
    elif report_type == "weekly":
        report = generate_weekly_report(memories, access_patterns, uid)
    else:
        report = generate_summary_report(memories, access_patterns, topics, uid)

    conn.close()
    return report


def main():
    parser = argparse.ArgumentParser(description="AI 记忆洞察与自我进化")
    parser.add_argument("--base-dir", default=".", help="记忆仓库根目录")
    parser.add_argument("--uid", required=True, help="用户ID")
    parser.add_argument("--days", type=int, help="分析最近N天")
    parser.add_argument("--daily", action="store_true", help="每日洞察")
    parser.add_argument("--weekly", action="store_true", help="每周洞察")
    parser.add_argument("--auto-mark", action="store_true", help="自动标记重要记忆")
    parser.add_argument("--find-gaps", action="store_true", help="发现知识盲点")
    parser.add_argument("--learn-patterns", action="store_true", help="学习记忆模式")
    parser.add_argument("--save", help="保存报告到文件")
    args = parser.parse_args()

    base_dir = os.path.abspath(args.base_dir)
    db_path = get_db_path(base_dir)

    if not os.path.exists(db_path):
        print(f"❌ 向量数据库不存在: {db_path}")
        print("   请先运行: python scripts/memory_embed.py --uid " + args.uid)
        return 1

    conn = connect_db(db_path)
    memories = extract_memories(conn, args.uid, args.days)
    access_patterns = extract_access_patterns(base_dir, args.uid, args.days or 7)

    if args.auto_mark:
        marked = auto_mark_importance(conn, memories, access_patterns)
        print(f"✅ 自动标记完成，{marked} 条记忆已更新")
        conn.close()
        return 0

    if args.find_gaps:
        topics = analyze_topics(memories)
        gaps = find_knowledge_gaps(memories, topics)
        print("\n🎯 知识盲点分析:\n")
        for g in gaps:
            print(f"  - {g['suggestion']}")
        conn.close()
        return 0

    if args.learn_patterns:
        patterns = detect_patterns(memories, access_patterns)
        print("\n🧠 记忆模式分析:\n")
        for p in patterns[:10]:
            print(f"  [{p['type']}] {p['suggestion']}")
        conn.close()
        return 0

    # 生成报告
    if args.daily:
        report = generate_daily_report(memories, access_patterns, args.uid)
    elif args.weekly:
        report = generate_weekly_report(memories, access_patterns, args.uid)
    else:
        topics = analyze_topics(memories)
        report = generate_summary_report(memories, access_patterns, topics, args.uid)

    print(report)

    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n💾 已保存到: {args.save}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
