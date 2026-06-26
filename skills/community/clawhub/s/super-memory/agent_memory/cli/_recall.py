"""Recall quality & optimization: meta-recall, evaluate, traces, trace-detail, trace-log, awareness."""

from __future__ import annotations

import json
from argparse import Namespace
from datetime import datetime

from agent_memory.cli._utils import get_memory


# ── Phase 2: 推理追踪命令 ────────────────────────────────


def cmd_traces(args):
    """查看推理追踪历史"""
    mem = get_memory()
    traces = mem.self_model.get_traces(limit=args.limit, topic=args.topic)
    if not traces:
        print("📭 暂无推理追踪")
    else:
        output = []
        for t in traces:
            dt = datetime.fromtimestamp(t.get("created_at", 0)).strftime("%Y-%m-%d %H:%M")
            conf = t.get("confidence", 0)
            steps = t.get("steps", [])
            sources = t.get("sources_used", [])
            uncertainty = t.get("uncertainty", [])
            output.append({
                "id": t["trace_id"],
                "time": dt,
                "query": t["query"][:80],
                "confidence": round(conf, 3),
                "steps": len(steps),
                "sources": len(sources),
                "uncertainty": uncertainty[:3],
                "summary": (t.get("result_summary") or "")[:100],
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


def cmd_trace_log(args):
    """查看结构化追踪日志"""
    from trace_logger import get_tracer
    tracer = get_tracer()
    if args.clear:
        tracer.clear_logs()
        print(json.dumps({"status": "cleared"}))
        return
    logs = tracer.get_recent_traces(module=args.module, limit=args.limit)
    print(json.dumps(logs, ensure_ascii=False, indent=2))


def cmd_trace_detail(args):
    """查看单次推理的详细步骤"""
    mem = get_memory()
    traces = mem.self_model.get_traces(limit=200)
    target = None
    for t in traces:
        if t["trace_id"] == args.trace_id:
            target = t
            break

    if not target:
        print(f"❌ 推理追踪不存在: {args.trace_id} — 使用 traces 查看所有追踪")
        mem.close()
        return

    dt = datetime.fromtimestamp(target.get("created_at", 0)).strftime("%Y-%m-%d %H:%M:%S")
    print(f"🧠 推理追踪 {target['trace_id']}")
    print(f"   时间: {dt}")
    print(f"   查询: {target['query']}")
    print(f"   置信度: {target.get('confidence', 0):.3f}")
    print(f"   摘要: {target.get('result_summary', 'N/A')}")
    print()

    steps = target.get("steps", [])
    if steps:
        print(f"📝 推理步骤 ({len(steps)}):")
        for i, s in enumerate(steps):
            ts = datetime.fromtimestamp(s.get("timestamp", 0)).strftime("%H:%M:%S")
            print(f"   {i+1}. [{ts}] {s.get('step_type', '?')}: {s.get('detail', '')}")

    sources = target.get("sources_used", [])
    if sources:
        print(f"\n🔗 查阅的记忆 ({len(sources)}):")
        for sid in sources[:10]:
            print(f"   → {sid}")

    uncertainty = target.get("uncertainty", [])
    if uncertainty:
        print(f"\n❓ 不确定因素 ({len(uncertainty)}):")
        for u in uncertainty:
            print(f"   ⚠️ {u}")

    mem.close()


# ── Phase 3: 元认知命令 ──────────────────────────────────


def cmd_meta_recall(args):
    """带反思的检索（不确定时自动修正查询重试）"""
    mem = get_memory()
    result = mem.meta_recall(
        query=args.query,
        limit=args.limit,
        max_rounds=args.max_rounds,
    )
    # 简化输出
    output = {
        "rounds": result["rounds"],
        "final_count": len(result["results"]),
        "evaluation": result.get("evaluation", {}),
        "reflections": [
            {
                "round": r.get("round", 0),
                "confidence": r.get("confidence", 0),
                "insight": r.get("reflection_text", "")[:100],
                "revised_query": r.get("revised_queries", [None])[0],
            }
            for r in result.get("reflections", [])
        ],
        "memories": [
            {
                "id": m["memory_id"],
                "content": m["content"][:150],
                "importance": m.get("importance", "medium"),
            }
            for m in result["results"][:args.limit]
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


def cmd_evaluate(args):
    """评估检索结果质量（多维度分析）"""
    mem = get_memory()
    evaluation = mem.evaluate_recall(query=args.query)
    print(json.dumps(evaluation, ensure_ascii=False, indent=2))
    mem.close()


# ── 知识感知度命令 ────────────────────────────────────────


def cmd_awareness(args):
    """查询知识感知度 — 了解系统对某主题的认知状况"""
    mem = get_memory()
    try:
        result = mem.spirit.query_awareness(args.topic)
        if result.get('status') == 'error':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            confidence = result.get('confidence', 0)
            if confidence >= 0.8:
                level = "精通"
                icon = "🟢"
            elif confidence >= 0.5:
                level = "熟悉"
                icon = "🟡"
            elif confidence > 0:
                level = "了解"
                icon = "🟠"
            else:
                level = "未知"
                icon = "🔴"

            print(f"{icon} 主题「{args.topic}」认知度: {confidence:.0%} ({level})")
            print(f"   关联记忆: {result.get('source_count', 0)} 条")

            content = result.get('content', '')
            if content:
                print(f"\n{content}")

            if result.get('unverified'):
                print(f"\n⚠️ 包含未验证内容")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()
