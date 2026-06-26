"""System: validate, validate-all, model-server, update, versions, curiosity (targets/suggestions/explore)."""

from __future__ import annotations

import json
from argparse import Namespace
from datetime import datetime

from agent_memory.cli._utils import get_memory


# ── 模型守护进程管理 ──────────────────────────────────────


def cmd_model_server(args):
    """管理模型守护进程"""
    from model_server import is_running, start_server, stop_server

    if args.action == "start":
        if is_running():
            print("✅ 模型守护进程已在运行")
        else:
            start_server(daemon=True)
            if is_running():
                print("✅ 模型守护进程已启动")
            else:
                print("❌ 守护进程启动失败 — 检查模型配置和端口占用情况")
    elif args.action == "stop":
        if not is_running():
            print("ℹ️  模型守护进程未运行")
        else:
            stop_server()
            print("✅ 模型守护进程已停止")
    elif args.action == "restart":
        if is_running():
            stop_server()
        start_server(daemon=True)
        if is_running():
            print("✅ 模型守护进程已重启")
        else:
            print("❌ 守护进程重启失败 — 尝试先 stop 再 start")
    elif args.action == "status":
        if is_running():
            from model_server import send_request
            resp = send_request({"action": "ping"}, timeout=2)
            model_name = resp.get("model", "unknown")
            print(f"✅ 运行中 — 模型: {model_name}")
        else:
            print("⏸️ 未运行 — 运行 agent-memory model-server start 启动")


# ── 记忆版本化命令 ────────────────────────────────────────


def cmd_update(args: Namespace) -> None:
    """更新记忆内容（版本化）"""
    mem = get_memory()
    topics = args.topics.split(",") if args.topics else None
    result = mem.store.update_memory(
        memory_id=args.memory_id,
        new_content=args.content,
        change_reason=args.reason,
        importance=args.importance,
        topics=topics,
    )
    if result.get("changed"):
        print(f"✅ 记忆已更新 → v{result['version']}")
        print(f"   原内容: {result['old_content'][:100]}{'...' if len(result['old_content']) > 100 else ''}")
        print(f"   新内容: {result['new_content'][:100]}{'...' if len(result['new_content']) > 100 else ''}")
        if result.get("reason"):
            print(f"   原因:   {result['reason']}")
    elif result.get("error"):
        print(f"❌ {result['error']}")
    else:
        print(f"ℹ️  {result.get('reason', '未变更')}")
    mem.close()


def cmd_versions(args: Namespace) -> None:
    """查看记忆版本历史"""
    mem = get_memory()
    versions = mem.store.get_memory_versions(args.memory_id)
    if not versions:
        print(f"❌ 记忆不存在或无版本历史: {args.memory_id}")
        mem.close()
        return

    if args.as_json:
        print(json.dumps(versions, ensure_ascii=False, indent=2, default=str))
    else:
        mem_data = mem.store.get_memory(args.memory_id)
        print(f"📋 记忆 {args.memory_id} 的版本历史")
        if mem_data:
            topics = [t["code"] for t in mem_data.get("topics", [])]
            print(f"   当前主题: {', '.join(topics) if topics else '无'}")
        print(f"   共 {len(versions)} 个版本\n")

        for v in versions:
            marker = "→ " if v.get("is_current") else "  "
            ts = datetime.fromtimestamp(v["created_at"]).strftime("%Y-%m-%d %H:%M") if v.get("created_at") else "?"
            reason = v.get("change_reason", "")
            content_preview = v["content"][:80].replace("\n", " ")
            print(f"  {marker}v{v['version_id']} [{ts}] {reason}")
            print(f"     {content_preview}{'...' if len(v['content']) > 80 else ''}")
    mem.close()


# ── Level 6.0: Curiosity Engine 命令 ─────────────────────


def cmd_curiosity_targets(args):
    """查看值得探索的知识目标"""
    mem = get_memory()
    try:
        targets = mem.curiosity_engine.identify_targets(limit=args.limit)
        output = []
        for t in targets:
            output.append({
                "topic": t.topic,
                "reason": t.reason,
                "priority": round(t.priority, 3),
                "estimated_value": round(t.estimated_value, 3),
                "current_coverage": t.current_coverage,
                "avg_confidence": round(t.avg_confidence, 3),
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_curiosity_suggestions(args):
    """获取建议查询 — 填补知识空白"""
    mem = get_memory()
    try:
        suggestions = mem.curiosity_engine.get_suggested_queries(limit=args.limit)
        print(json.dumps(suggestions, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_curiosity_explore(args):
    """执行探索 — 主动获取新知识"""
    mem = get_memory()
    try:
        from engines.curiosity import ExplorationTarget
        targets = mem.curiosity_engine.identify_targets(limit=50)
        target = None
        for t in targets:
            if t.topic == args.topic:
                target = t
                break
        if target is None:
            target = ExplorationTarget(
                topic=args.topic,
                reason="manual",
                priority=0.5,
                estimated_value=0.5,
                current_coverage=0,
                avg_confidence=0.0,
                last_updated=0.0,
            )
        result = mem.curiosity_engine.explore(target)
        print(json.dumps({
            "topic": result.target.topic,
            "action_taken": result.action_taken,
            "new_knowledge_count": result.new_knowledge_count,
            "confidence_improvement": round(result.confidence_improvement, 3),
        }, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_curiosity_dispatch(args):
    """好奇心引擎命令分发"""
    subcmd = args.curiosity_subcmd
    if subcmd == "targets":
        cmd_curiosity_targets(args)
    elif subcmd == "suggestions":
        cmd_curiosity_suggestions(args)
    elif subcmd == "explore":
        if not args.topic:
            print(json.dumps({"error": "explore 需要指定主题，使用 --topic 参数"}, ensure_ascii=False))
            return
        cmd_curiosity_explore(args)
    else:
        print("用法: agent-memory curiosity <targets|suggestions|explore> [参数]")


# ── Level 6.0: Knowledge Validation 命令 ─────────────────


def cmd_validate(args):
    """验证单条记忆 — 交叉引用、时效性、置信度衰减"""
    mem = get_memory()
    try:
        result = mem.knowledge_validator.validate_memory(args.memory_id)
        if result is None:
            print(f"❌ 记忆不存在: {args.memory_id} — 使用 recall 搜索相关记忆")
        else:
            status_icons = {
                "verified": "✅",
                "uncertain": "🟡",
                "outdated": "⏰",
                "contradicted": "🔴",
                "unverifiable": "❓",
            }
            icon = status_icons.get(result.validation_status, "❓")
            print(f"{icon} 验证状态: {result.validation_status}")
            print(f"   置信度: {result.confidence_before:.3f} → {result.confidence_after:.3f}")
            print(f"   交叉引用: {result.cross_references} | 矛盾: {result.contradictions}")
            print(f"   陈旧天数: {result.staleness_days:.1f}")
            print(f"   建议: {result.recommendation}")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()


def cmd_validate_all(args):
    """验证所有记忆并输出摘要"""
    mem = get_memory()
    try:
        result = mem.knowledge_validator.validate_all(limit=args.limit)
        if not result or result.get("total_validated", 0) == 0:
            print("📭 暂无记忆可验证")
        else:
            status_icons = {
                "verified": "✅",
                "uncertain": "🟡",
                "outdated": "⏰",
                "contradicted": "🔴",
                "unverifiable": "❓",
            }
            print(f"📊 验证摘要: 共 {result['total_validated']} 条记忆")
            for status, count in result["status_distribution"].items():
                icon = status_icons.get(status, "❓")
                print(f"   {icon} {status}: {count}")
            print(f"   平均置信度: {result['avg_confidence_before']:.3f} → {result['avg_confidence_after']:.3f} (变化 {result['confidence_change']:+.3f})")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()
