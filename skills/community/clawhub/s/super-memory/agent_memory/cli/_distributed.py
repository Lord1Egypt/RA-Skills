"""Distributed: sync-peers, sync-with, sync-all, sync-checkpoint, sync-stats, federation."""

from __future__ import annotations

import json
from argparse import Namespace
from datetime import datetime

from agent_memory.cli._utils import get_memory


def cmd_sync_peers(args):
    """列出所有同步对等节点"""
    mem = get_memory()
    peers = mem.sync_engine.list_peers()
    if not peers:
        print("（无同步对等节点）")
    else:
        for p in peers:
            ts = datetime.fromtimestamp(p["last_sync"]).strftime("%Y-%m-%d %H:%M") if p["last_sync"] else "从未"
            print(f"  📡 {p['node_id']}  状态: {p['status']}  上次同步: {ts}")
    mem.close()


def cmd_sync_with(args):
    """与指定对等节点同步"""
    mem = get_memory()
    result = mem.sync_engine.sync_with_peer(args.peer_id)
    if result.errors and result.errors[0] == "peer_not_found":
        print(f"❌ 对等节点不存在: {args.peer_id}")
    else:
        print(f"✅ 同步完成: {result.source_node} → {result.target_node}")
        print(f"   操作数: {result.operations_applied}  冲突: {result.conflicts_resolved}  拒绝: {result.operations_rejected}")
        print(f"   耗时: {result.duration_ms:.1f}ms")
        if result.errors:
            for e in result.errors:
                print(f"   ❌ {e}")
    mem.close()


def cmd_sync_all(args):
    """与所有对等节点同步"""
    mem = get_memory()
    results = mem.sync_engine.sync_all()
    if not results:
        print("（无对等节点）")
    else:
        for r in results:
            status = "✅" if not r.errors else "⚠️"
            print(f"  {status} {r.source_node} → {r.target_node}: {r.operations_applied} ops, {r.duration_ms:.1f}ms")
            if r.errors:
                for e in r.errors:
                    print(f"     ❌ {e}")
    mem.close()


def cmd_sync_checkpoint(args):
    """创建同步检查点"""
    mem = get_memory()
    checkpoint = mem.sync_engine.create_checkpoint()
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))
    mem.close()


def cmd_sync_stats(args):
    """查看同步引擎统计"""
    mem = get_memory()
    stats = mem.sync_engine.get_stats()
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    mem.close()


# ── v10.1: 联邦知识命令 ──────────────────────────────────


def cmd_federation(args):
    """跨 Agent 知识联邦命令"""
    subcmd = args.federation_subcmd

    if subcmd == "peers":
        _cmd_federation_peers(args)
    elif subcmd == "search":
        _cmd_federation_search(args)
    elif subcmd == "conflicts":
        _cmd_federation_conflicts(args)
    elif subcmd == "resolve":
        _cmd_federation_resolve(args)
    else:
        print("用法: agent-memory federation <peers|search|conflicts|resolve> [参数]")


def _cmd_federation_peers(args):
    """列出联邦对等 Agent"""
    mem = get_memory()
    try:
        engine = mem.federation_engine
        stats = engine.get_stats()
        peers = stats["peer_ids"]
        if peers:
            print(f"📡 联邦对等 Agent ({len(peers)}):")
            for p in peers:
                print(f"   → {p}")
        else:
            print("📡 暂无联邦对等 Agent")
        print(f"   已完成共享: {stats['shares_completed']} 次")
        print(f"   检测到冲突: {stats['conflicts_detected']} 个")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def _cmd_federation_search(args):
    """跨 Agent 联邦检索"""
    mem = get_memory()
    try:
        engine = mem.federation_engine
        topics = args.topics.split(",") if args.topics else None
        result = engine.federated_search(
            query=args.query,
            topics=topics,
            max_per_peer=args.max_per_peer,
        )
        output = {
            "total": result["total"],
            "query": result["query"],
            "peer_stats": result["peer_stats"],
            "results": [
                {
                    "content": m.get("content", "")[:200],
                    "importance": m.get("importance", "medium"),
                    "source_agent": m.get("_source_agent", "local"),
                    "federated": m.get("_federated", False),
                    "quality_score": m.get("quality_score", 0.5),
                }
                for m in result["results"][:args.limit]
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def _cmd_federation_conflicts(args):
    """检测跨 Agent 知识冲突"""
    mem = get_memory()
    try:
        engine = mem.federation_engine
        conflicts = engine.detect_conflicts(topic=args.topic)
        if conflicts:
            print(f"⚠️ 检测到 {len(conflicts)} 个知识冲突:")
            for i, c in enumerate(conflicts, 1):
                print(f"  {i}. [{c.conflict_type}] 主题: {c.topic}")
                print(f"     Agent A ({c.agent_a}): {c.agent_a_claim[:60]}")
                print(f"     Agent B ({c.agent_b}): {c.agent_b_claim[:60]}")
                print(f"     置信度: A={c.confidence_a:.2f} B={c.confidence_b:.2f}")
                print(f"     状态: {c.resolution}")
        else:
            print("✅ 未检测到知识冲突")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def _cmd_federation_resolve(args):
    """解决知识冲突"""
    mem = get_memory()
    try:
        from engines.federation import KnowledgeConflict
        engine = mem.federation_engine
        conflict = KnowledgeConflict(
            topic=args.topic,
            agent_a=args.agent_a,
            agent_a_claim=args.agent_a_claim,
            agent_b=args.agent_b,
            agent_b_claim=args.agent_b_claim,
            conflict_type="contradiction",
        )
        resolved = engine.resolve_conflict(conflict, strategy=args.strategy)
        print(f"✅ 冲突已解决")
        print(f"   主题: {resolved.topic}")
        print(f"   策略: {args.strategy}")
        print(f"   结果: {resolved.resolution}")
        if resolved.resolution == "a_wins":
            print(f"   → 采纳 {resolved.agent_a} 的观点")
        elif resolved.resolution == "b_wins":
            print(f"   → 采纳 {resolved.agent_b} 的观点")
        elif resolved.resolution == "merged":
            print(f"   → 合并双方观点")
        elif resolved.resolution == "both_kept":
            print(f"   → 保留双方观点作为替代视角")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()
