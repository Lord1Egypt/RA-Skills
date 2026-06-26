"""Self-awareness: whoami, identity, narrative, worldview, self-concept, self, mood, gaps, curious, confidence, reflect, uncertainty."""

from __future__ import annotations

import json
import time
from argparse import Namespace
from datetime import datetime

from agent_memory.cli._utils import get_memory


# ── Phase 4: 内在动机命令 ────────────────────────────────


def cmd_mood(args):
    """查看 Agent 当前内在状态"""
    mem = get_memory()
    state = mem.motivation.state
    output = {
        "mood": state.mood_summary,
        "emoji": state.mood_emoji,
        "state": state.to_dict(),
        "dominant_drive": state.dominant_drive,
    }
    if args.detail:
        output["boredom_analysis"] = mem.motivation.compute_boredom_analysis()
        output["knowledge_gaps"] = len(mem.motivation.detect_knowledge_gaps())
    print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


def cmd_gaps(args):
    """查看知识空白"""
    mem = get_memory()
    gaps = mem.motivation.detect_knowledge_gaps()
    if not gaps:
        print("✅ 知识版图完整，暂无空白区域")
    else:
        print(json.dumps(gaps, ensure_ascii=False, indent=2))
    mem.close()


def cmd_curious(args):
    """查看好奇驱动的探索任务"""
    mem = get_memory()
    tasks = mem.motivation.generate_curiosity_tasks()
    if not tasks:
        print("📭 暂无探索建议 — 使用 curious --check 查看是否有新发现")
    else:
        print(json.dumps(tasks, ensure_ascii=False, indent=2))
    mem.close()


# ── Phase 5: 叙事自我命令 ────────────────────────────────


def cmd_whoami(args):
    """我是谁 — 第一人称自我叙述"""
    mem = get_memory()
    print("⚠️ 以上内容基于记忆数据自动生成，仅供参考，不代表对事实或人格的权威判断。")
    print(mem.narrative.whoami())
    mem.close()


def cmd_identity(args):
    """查看身份画像"""
    mem = get_memory()
    profile = mem.narrative.build_identity_profile()
    if args.raw:
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        if profile.get("core_values"):
            print(f"核心价值观: {', '.join(profile['core_values'])}")
        if profile.get("expertise"):
            for e in profile["expertise"][:5]:
                print(f"  📚 {e['topic']} ({e['depth']}, {e['memory_count']}条)")
        if profile.get("personality_traits"):
            print(f"人格特质: {', '.join(profile['personality_traits'])}")
        if profile.get("interests"):
            print(f"兴趣: {', '.join(profile['interests'])}")
        if profile.get("preferences"):
            for k, v in profile["preferences"].items():
                print(f"  {k}: {v}")
        print(f"\n置信度: {profile.get('confidence', 0):.0%} (基于 {profile.get('evidence_count', 0)} 条记忆)")
    mem.close()


def cmd_narrative(args):
    """构建叙事（时间线/主题）"""
    mem = get_memory()
    if args.topic:
        result = mem.narrative.build_topic_narrative(args.topic, limit=args.limit)
        print(result)
    elif args.from_date:
        from timeline import parse_date_to_ts
        from_ts = parse_date_to_ts(args.from_date)
        to_ts = parse_date_to_ts(args.to_date) if args.to_date else None
        result = mem.narrative.build_timeline_narrative(from_ts=from_ts, to_ts=to_ts)
        print(result)
    else:
        # 默认：最近 7 天
        from_ts = int(time.time()) - 86400 * 7
        result = mem.narrative.build_timeline_narrative(from_ts=from_ts)
        print(result)
    mem.close()


def cmd_worldview(args):
    """查看世界观（信念/价值观/原则）"""
    mem = get_memory()
    print("⚠️ 世界观内容基于记忆数据自动生成，仅供参考，不代表对事实或价值观的权威判断。")
    worldview = mem.narrative.get_worldview()
    print(json.dumps(worldview, ensure_ascii=False, indent=2))
    mem.close()


def cmd_self_concept(args):
    """查看完整自我概念"""
    mem = get_memory()
    concept = mem.narrative.update_self_concept()
    print(json.dumps(concept, ensure_ascii=False, indent=2))
    mem.close()


# ── Phase 2: 置信度与反思 ────────────────────────────────


def cmd_confidence(args):
    """查看置信度历史/概览"""
    mem = get_memory()
    if args.overview:
        overview = mem.self_model.get_confidence_overview()
        if not overview:
            print("📭 暂无置信度数据 — 积累更多记忆后系统将自动评估")
        else:
            print(json.dumps(overview, ensure_ascii=False, indent=2))
    else:
        history = mem.self_model.get_confidence_history(topic=args.topic, limit=args.limit)
        if not history:
            print("📭 暂无置信度数据 — 积累更多记忆后系统将自动评估")
        else:
            print(json.dumps(history, ensure_ascii=False, indent=2))
    mem.close()


def cmd_reflect(args):
    """查看自我反思历史"""
    mem = get_memory()
    reflections = mem.self_model.get_reflections(limit=args.limit)
    if not reflections:
        print("📭 暂无反思记录")
    else:
        output = []
        for r in reflections:
            dt = datetime.fromtimestamp(r.get("created_at", 0)).strftime("%Y-%m-%d %H:%M")
            output.append({
                "id": r["reflection_id"],
                "time": dt,
                "insight": r["insight"][:100],
                "action": (r.get("action") or "")[:80],
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


def cmd_uncertainty(args):
    """查看不确定因素模式分析"""
    mem = get_memory()
    patterns = mem.self_model.get_uncertainty_patterns(limit=args.limit)
    if not patterns:
        print("📭 暂无不确定因素分析")
    else:
        print(json.dumps(patterns, ensure_ascii=False, indent=2))
    mem.close()


# ── 统一自我入口 ──────────────────────────────────────────


def cmd_self(args):
    """统一自我状态仪表盘"""
    mem = get_memory()

    if args.mood:
        state = mem.motivation.state
        print(f"{state.mood_emoji} 当前状态: {state.mood_summary}")
        print(f"   好奇心 {state.curiosity:.2f} | 无聊度 {state.boredom:.2f} | "
              f"自信度 {state.confidence:.2f} | 满足感 {state.satisfaction:.2f} | "
              f"紧迫感 {state.urgency:.2f}")
        print(f"   主导动机: {state.dominant_drive}")
    elif args.narrative:
        print(mem.narrative.whoami())
    elif args.confidence:
        overview = mem.self_model.get_confidence_overview()
        if overview:
            for topic, info in list(overview.items())[:8]:
                trend_icon = {"rising": "📈", "falling": "📉", "stable": "➡️"}.get(info["trend"], "❓")
                print(f"  {trend_icon} {topic}: {info['avg_confidence']:.2f} ({info['trace_count']}次)")
        else:
            print("（暂无置信度数据）")
    elif args.gaps:
        gaps = mem.motivation.detect_knowledge_gaps()
        if gaps:
            for g in gaps[:8]:
                print(f"  ❓ [{g['gap_type']}] {g['topic']}: {g['detail']}")
        else:
            print("（暂无知识空白）")
    elif args.recent_thinking:
        traces = mem.self_model.get_traces(limit=5)
        for t in traces:
            dt = datetime.fromtimestamp(t.get("created_at", 0)).strftime("%m-%d %H:%M")
            conf = t.get("confidence", 0)
            print(f"  🧠 [{dt}] conf={conf:.2f} {t['query'][:60]}")
    else:
        # 完整仪表盘
        print("=" * 50)
        print("🧠 自我状态仪表盘")
        print("=" * 50)

        # 身份
        profile = mem.narrative.build_identity_profile()
        if profile.get("core_values"):
            print(f"\n📌 价值观: {', '.join(profile['core_values'][:3])}")
        if profile.get("expertise"):
            top = profile["expertise"][0]
            print(f"📚 专长: {top['topic']} ({top['depth']})")

        # 内在状态
        state = mem.motivation.state
        print(f"\n{state.mood_emoji} 心情: {state.mood_summary}")
        print(f"   好奇={state.curiosity:.2f} 无聊={state.boredom:.2f} "
              f"自信={state.confidence:.2f} 满足={state.satisfaction:.2f}")

        # 知识空白
        gaps = mem.motivation.detect_knowledge_gaps()
        if gaps:
            print(f"\n❓ 待探索: {', '.join(g['topic'] for g in gaps[:3])}")

        # 最近推理
        traces = mem.self_model.get_traces(limit=3)
        if traces:
            avg_conf = sum(t.get("confidence", 0) for t in traces) / len(traces)
            print(f"\n🧠 最近推理: {len(traces)} 次, 平均置信度 {avg_conf:.2f}")

        # 统计
        sm_stats = mem.self_model.get_stats()
        print(f"\n📊 推理追踪: {sm_stats.get('traces', 0)} | 反思: {sm_stats.get('reflections', 0)}")

    mem.close()
