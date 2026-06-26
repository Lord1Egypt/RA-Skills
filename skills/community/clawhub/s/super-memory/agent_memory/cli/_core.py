"""Core commands: init, remember, recall, forget, restore, context, stats, maintain, compress, graph, feedback, learn, heal, sync, export, conflicts, notifications, reactor-scan, flush, purge-deleted, auto-context, batch-remember."""

from __future__ import annotations

import sys
import os
import json
import re
import time
from argparse import Namespace
from datetime import datetime

from agent_memory.cli._utils import (
    get_memory,
    PROJECT_DIR,
)


def cmd_init(args: Namespace) -> None:
    """首次运行引导 — 初始化记忆系统"""
    from agent_memory.onboarding import WelcomeGuide, seed_memories as get_seed_memories

    mem = get_memory()
    guide = WelcomeGuide(mem)

    # Step 1: 检查是否首次使用
    first_time = guide.is_first_time()

    print("=" * 60)
    print("  🧠 Agent Memory V12 — 初始化引导")
    print("=" * 60)

    if not first_time:
        print("\nℹ️  检测到已有记忆数据，系统已初始化过。")
        configured = WelcomeGuide.is_configured()
        if configured:
            print("   ✅ 配置正常")
        else:
            print("   ⚠️  配置可能不完整，建议检查：")
            config_guide = WelcomeGuide.get_config_guide()
            for step in config_guide["steps"]:
                print(f"      {step['step']}. {step['title']}: {step['description']}")
                env_var = step.get("env_var") or ""
                current = os.environ.get(env_var, step.get("default", "未设置")) if env_var else step.get("default", "未设置")
                if env_var:
                    print(f"         当前: {env_var}={current}")
        mem.close()
        return

    # Step 2: 显示欢迎信息
    print("\n🎉 欢迎使用 Agent Memory V12！")
    print("   这是一个为 AI Agent 设计的智能记忆管理系统。")
    print("   让我们一起完成初始化设置。\n")

    # Step 3: 配置检查
    configured = WelcomeGuide.is_configured()
    if not configured:
        print("⚠️  检测到配置可能不完整：")
        config_guide = WelcomeGuide.get_config_guide()
        for step in config_guide["steps"]:
            print(f"\n   步骤 {step['step']}: {step['title']}")
            print(f"   {step['description']}")
            for opt in step.get("options", []):
                marker = " (默认)" if opt["value"] == step.get("default") else ""
                print(f"     • {opt['value']}: {opt['description']}{marker}")
            env_var = step.get("env_var") or ""
            current = os.environ.get(env_var, step.get("default", "未设置")) if env_var else step.get("default", "未设置")
            if env_var:
                print(f"   当前: {env_var}={current}")
        print()

    # Step 4: 注入种子记忆
    print("🌱 正在注入种子记忆...")
    seeds = get_seed_memories()
    injected = 0
    for s in seeds:
        try:
            result = mem.remember(
                content=s["content"],
                importance="medium",
                force=True,
            )
            if result.get("written"):
                injected += 1
                print(f"   ✅ {s['metadata']['type']}: {s['content'][:60]}...")
            else:
                print(f"   ⏭️  跳过: {s['content'][:60]}...")
        except Exception as e:
            print(f"   ❌ 失败: {e}")
    print(f"   已注入 {injected}/{len(seeds)} 条种子记忆\n")

    # Step 5: 迷你快速演示
    print("🚀 运行迷你演示...")
    print("   ⏳ 首次运行可能需要 10-15 秒加载模型...")

    # remember
    try:
        demo_result = mem.remember(
            content="This is my first memory in Agent Memory V12!",
            importance="low",
            force=True,
        )
        if demo_result.get("written"):
            print("   ✅ 写入演示记忆成功")
        else:
            print("   ℹ️  演示记忆已存在")
    except Exception as e:
        print(f"   ⚠️  写入演示记忆失败: {e}")

    # recall
    try:
        recall_result = mem.recall(query="first memory", limit=3)
        count = len(recall_result.get("primary", []))
        print(f"   ✅ 检索演示: 找到 {count} 条相关记忆")
    except Exception as e:
        print(f"   ⚠️  检索演示失败: {e}")

    # health check
    try:
        health = mem.health_check()
        healthy = health.get("healthy", False)
        components = health.get("components", {})
        available = sum(1 for v in components.values() if v)
        total = len(components)
        print(f"   {'✅' if healthy else '⚠️'} 健康检查: {available}/{total} 组件可用")
        for name, status in components.items():
            print(f"      {'✓' if status else '✗'} {name}")
    except Exception as e:
        print(f"   ⚠️  健康检查失败: {e}")

    # Step 6: 入门提示
    print("\n" + "=" * 60)
    print("  🎯 入门指南")
    print("=" * 60)
    print("""
  常用命令:
    agent-memory remember "你的记忆内容"     — 写入记忆
    agent-memory recall "搜索关键词"         — 检索记忆
    agent-memory stats                       — 查看统计
    agent-memory health                      — 健康检查
    agent-memory whoami                      — 自我叙述

  进阶功能:
    agent-memory spirit "你的指令"           — 自然语言操作
    agent-memory distill                     — 蒸馏记忆
    agent-memory snapshot --label "v1"       — 创建快照
    agent-memory curiosity targets           — 探索知识空白

  文档: https://github.com/agent-memory-v12
""")
    print("✅ 初始化完成！开始使用 Agent Memory V12 吧！")
    mem.close()


def cmd_remember(args: Namespace) -> None:
    """写入记忆"""
    mem = get_memory()
    result = mem.remember(
        content=args.content,
        importance=args.importance,
        topics=args.topics.split(",") if args.topics else None,
        nature=args.nature,
        force=args.force,
        auto_write=not args.review,
    )

    if hasattr(result, 'to_dict'):
        result = result.to_dict()
    elif not isinstance(result, dict):
        result = {"written": bool(result), "memory_id": getattr(result, 'memory_id', '')}

    # 输出情感分析结果（写入成功时）
    if result.get("written") and result.get("emotion"):
        emotion = result["emotion"]
        if isinstance(emotion, dict) and emotion.get("significance"):
            from emotion import EmotionAnalyzer as _EA
            sig_icon = _EA.significance_icon(emotion.get("significance", ""))
            val_label = _EA.valence_label(emotion.get("valence", 0))
            result["emotion_display"] = f"{sig_icon} {val_label}"

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    mem.close()


def cmd_recall(args: Namespace) -> None:
    """检索记忆"""
    mem = get_memory()
    result = mem.recall(
        query=args.query,
        topic=args.topic,
        importance=args.importance,
        significance=args.significance,
        limit=args.limit,
    )
    if hasattr(result, 'to_dict'):
        result = result.to_dict()
    elif not isinstance(result, dict):
        result = {"total": 0, "search_mode": "unknown", "primary": []}

    total = result.get("total", 0)

    if total == 0:
        suggestions = result.get("suggestions", [])
        print("🔍 未找到相关记忆")
        if suggestions:
            print("💡 建议：")
            for s in suggestions:
                print(f"  - {s}")
        mem.close()
        return

    # 简化输出（含情感信号）
    output = {
        "total": total,
        "mode": result.get("search_mode", "unknown"),
        "memories": [
            {
                "id": m["memory_id"],
                "content": m["content"][:200],
                "importance": m.get("importance", "medium"),
                "topics": [t.get("code", t) if isinstance(t, dict) else t for t in m.get("topics", [])],
                "emotion": {
                    "significance": m.get("significance", ""),
                    "significance_icon": m.get("_significance_icon", ""),
                    "valence": m.get("valence"),
                    "valence_label": m.get("_valence_label", ""),
                } if m.get("significance") else None,
            }
            for m in result.get("primary", [])[:args.limit]
        ],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    mem.close()


def cmd_context(args: Namespace) -> None:
    """组装上下文"""
    mem = get_memory()
    ctx = mem.build_context(
        query=args.query,
        max_tokens=args.max_tokens,
        style=args.style,
    )
    if ctx:
        print(ctx)
    else:
        print("（无相关记忆）")
    mem.close()


def cmd_stats(args: Namespace) -> None:
    """查看统计"""
    mem = get_memory()
    stats = mem.get_stats()
    if not stats or (isinstance(stats, dict) and stats.get("total", 0) == 0 and not stats.get("topics")):
        print("📭 暂无统计数据 — 使用 remember 写入第一条记忆")
    else:
        print(json.dumps(stats, ensure_ascii=False, indent=2, default=str))
    mem.close()


def cmd_maintain(args):
    """执行维护"""
    mem = get_memory()
    results = {}

    # 去重
    dedup_result = mem.deduplicate()
    results["dedup"] = {
        "scanned": dedup_result.get("total_scanned", 0),
        "found": dedup_result.get("duplicates_found", 0),
    }

    # 自修复
    heal_result = mem.self_heal()
    results["self_heal"] = {
        "contradictions": len(heal_result.get("contradictions", [])),
        "outdated": len(heal_result.get("outdated", [])),
        "healed": heal_result.get("importance_healed", 0),
        "total": heal_result.get("total_issues", 0),
    }

    # 衰减分析
    decay_result = mem.analyze_decay()
    results["decay"] = {
        "total": decay_result.get("total", 0),
        "needs_action": len(decay_result.get("needs_action", [])),
        "summary": decay_result.get("summary", ""),
    }

    print(json.dumps(results, ensure_ascii=False, indent=2))
    mem.close()


def cmd_compress(args):
    """压缩记忆"""
    # 确认提示（--yes/-y 跳过）
    if not args.yes:
        confirm = input("确认压缩记忆？压缩后原始碎片将被合并 [y/N] ").strip().lower()
        if confirm != 'y':
            print("已取消")
            return

    mem = get_memory()
    result = mem.compress(topic=args.topic, smart=True)
    merged = result.get("merged_count", result.get("fragments_merged", 0))
    if merged:
        print(f"✅ 压缩完成：合并了 {merged} 条记忆碎片")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    mem.close()


def cmd_graph(args):
    """生成图谱"""
    mem = get_memory()
    graph = mem.generate_graph(topic=args.topic, format=args.format)
    print(graph)
    mem.close()


def cmd_feedback(args):
    """记录反馈"""
    mem = get_memory()
    mem.feedback(args.memory_id, useful=args.useful, note=args.note)
    print("✅ 反馈已记录")
    mem.close()


def cmd_feedback_v2(args):
    """记录反馈（v2 — 支持 FeedbackLearner 持续学习）"""
    mem = get_memory()
    context = {}
    if args.correction_id:
        context["correction_id"] = args.correction_id
    if args.query:
        context["query"] = args.query

    result = mem.feedback_learner.record_feedback(
        memory_id=args.memory_id,
        feedback_type=args.feedback_type,
        context=context if context else None,
    )
    if result.get("error"):
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("✅ 反馈已记录")
    mem.close()


def cmd_learn(args):
    """应用反馈学习 — 调整质量/重要度"""
    mem = get_memory()
    result = mem.feedback_learner.apply_learning(dry_run=args.dry_run)
    if isinstance(result, dict):
        adjusted = result.get("adjusted_count", result.get("total_adjusted", 0))
        if adjusted:
            print(f"✅ 学习完成：调整了 {adjusted} 条记忆的质量/重要度")
        else:
            print("ℹ️ 暂无需要调整的记忆")
    else:
        print(json.dumps(result, ensure_ascii=False, default=str))
    mem.close()


def cmd_forget(args: Namespace) -> None:
    """删除单条记忆（含关联清理 + 向量清理）"""
    mem = get_memory()

    # 确认提示（--yes/-y 跳过）
    if not args.yes:
        confirm = input(f"确认删除记忆 {args.memory_id}？删除后30天内可使用 restore 恢复 [y/N] ").strip().lower()
        if confirm != 'y':
            print("已取消")
            mem.close()
            return

    permanent = args.permanent if hasattr(args, 'permanent') and args.permanent else False
    result = mem.store.delete_memory(args.memory_id, reason=args.reason or "user_delete", permanent=permanent)
    if result.get("deleted"):
        if result.get("soft_delete"):
            print(f"🗑️  记忆已软删除: {args.memory_id}（可使用 restore 命令恢复）")
        else:
            print(f"🗑️  记忆已永久删除: {args.memory_id}")
        if args.reason:
            print(f"   原因: {args.reason}")
    else:
        print(f"❌ 记忆不存在: {args.memory_id} — 使用 recall 搜索相关记忆")
    mem.close()


def cmd_restore(args: Namespace) -> None:
    """恢复软删除的记忆"""
    mem = get_memory()
    result = mem.store.restore_memory(args.memory_id)
    if result.get("restored"):
        print(f"✅ 记忆已恢复: {args.memory_id}")
    else:
        print(f"❌ 恢复失败: {result.get('reason', '未知原因')} — 确认记忆ID正确且已被软删除")
    mem.close()


def cmd_purge_deleted(args):
    """永久清理软删除的记忆"""
    # 确认提示（--yes/-y 跳过）
    if not args.yes:
        confirm = input(f"确认永久清理 {args.older_than_days} 天前的软删除记录？此操作不可撤销 [y/N] ").strip().lower()
        if confirm != 'y':
            print("已取消")
            return

    mem = get_memory()
    result = mem.store.purge_deleted(older_than_days=args.older_than_days)
    print(f"🗑️  已永久清理 {result['purged']} 条软删除记录（超过 {result['older_than_days']} 天）")
    mem.close()


def cmd_flush(args):
    """L1 沉淀到 L2"""
    mem = get_memory()
    from pipeline import IngestPipeline
    pipeline = IngestPipeline(
        mem.store, mem.encoder,
        index_dir=os.path.join(PROJECT_DIR, "daily_index"),
    )
    result = mem.flush_session()
    n = len(result)
    print(f"✅ 已沉淀 {n} 条 L1 记忆到 L2")
    mem.close()


def cmd_heal(args):
    """自我修复"""
    mem = get_memory()
    result = mem.self_heal()
    total_issues = result.get("total_issues", 0)
    if total_issues and total_issues > 0:
        print(f"✅ 自检完成：修复了 {total_issues} 个问题")
    else:
        print("✅ 系统健康，无需修复")
    mem.close()


def cmd_sync(args):
    """从 MEMORY.md 或其他 Markdown 文件同步记忆"""
    mem = get_memory()
    source = args.source
    if not os.path.exists(source):
        print(json.dumps({"error": f"文件不存在: {source}"}, ensure_ascii=False))
        sys.exit(1)

    with open(source, "r", encoding="utf-8") as f:
        content = f.read()

    # 按 ## 标题分割段落
    sections = re.split(r'\n(?=##\s)', content)
    written = 0
    skipped = 0
    errors = []

    for section in sections:
        section = section.strip()
        if not section or len(section) < 20:
            continue

        # 提取标题（如果有）
        title_match = re.match(r'^##\s+(.+)', section)
        title = title_match.group(1).strip() if title_match else ""

        # 推断重要度
        importance = "medium"
        if any(kw in section.lower() for kw in ["重要", "关键", "核心", "必须", "注意", "⚠️", "❗"]):
            importance = "high"
        elif any(kw in section.lower() for kw in ["临时", "草稿", "随便", "可以忽略"]):
            importance = "low"

        # 推断性质
        nature = None
        if any(kw in section for kw in ["TODO", "待办", "要做", "计划"]):
            nature = "todo"
        elif any(kw in section for kw in ["决定", "选择", "结论"]):
            nature = "note"
        elif any(kw in section for kw in ["教训", "踩坑", "错误"]):
            nature = "note"
        elif title:
            nature = "note"

        # 写入
        try:
            result = mem.remember(
                content=section,
                importance=importance,
                nature=nature,
                force=args.force,
            )
            if result["written"]:
                written += 1
            else:
                skipped += 1
        except Exception as e:
            errors.append({"section": title or section[:30], "error": str(e)})

    output = {
        "source": source,
        "total_sections": len([s for s in sections if len(s.strip()) >= 20]),
        "written": written,
        "skipped": skipped,
        "errors": len(errors),
    }
    if errors:
        output["error_details"] = errors[:5]
    print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


def cmd_auto_context(args):
    """自动组装上下文 — 根据最近对话智能检索 + 摘要"""
    mem = get_memory()
    ctx = mem.build_context(
        query=args.query,
        max_tokens=args.max_tokens,
        style=args.style,
    )
    if ctx:
        print(ctx)
    else:
        print("（记忆系统：暂无相关记忆）")
    mem.close()


def cmd_export(args):
    """导出记忆为 Markdown"""
    mem = get_memory()
    memories = mem.store.query(
        topic_path=args.topic,
        importance=args.importance,
        limit=args.limit,
    )

    lines = [
        f"# 记忆导出",
        f"",
        f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"共 {len(memories)} 条记忆",
        f"",
    ]

    # 按重要度分组
    by_importance = {"high": [], "medium": [], "low": []}
    for m in memories:
        imp = m.get("importance", "medium")
        by_importance.get(imp, by_importance["medium"]).append(m)

    icon_map = {"high": "⚡", "medium": "", "low": "🔻"}
    for imp in ["high", "medium", "low"]:
        mems = by_importance[imp]
        if not mems:
            continue
        lines.append(f"## {icon_map[imp]} {imp} ({len(mems)}条)")
        lines.append("")
        for m in mems:
            dt = datetime.fromtimestamp(m.get("time_ts", 0)).strftime("%Y-%m-%d %H:%M")
            content = m.get("content", "")
            mid = m.get("memory_id", "")
            lines.append(f"### [{dt}] {content[:50]}")
            lines.append(f"")
            lines.append(content)
            lines.append(f"")
            lines.append(f"> ID: `{mid}`")
            lines.append("")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ 已导出 {len(memories)} 条记忆到 {args.output}")
    mem.close()


def cmd_notifications(args):
    """查看待处理的主动通知"""
    mem = get_memory()
    notifications = mem.get_pending_notifications()
    result = {
        "total": len(notifications),
        "notifications": notifications,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    mem.close()


def cmd_reactor_scan(args):
    """手动触发 reactor 全量扫描"""
    mem = get_memory()
    result = mem.reactor_scan()
    # 简化输出
    output = {
        "total_actions": result["total_actions"],
        "contradictions_triggered": len(result["contradictions"]),
        "decay_reviews_triggered": len(result["decay_reviews"]),
        "decisions_triggered": len(result["decisions"]),
        "action_details": [
            {"action": r.action_name, "success": r.success, "message": r.message}
            for r in result["contradictions"] + result["decay_reviews"] + result["decisions"]
        ],
        "stats": result["stats"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    mem.close()


def cmd_conflicts(args: Namespace) -> None:
    """检测记忆冲突"""
    mem = get_memory()
    if not mem.dedup:
        print(json.dumps({"error": "去重功能未启用，请设置 AGENT_MEMORY_ENABLE_DEDUP=true"}, ensure_ascii=False))
        mem.close()
        return

    limit = getattr(args, 'limit', 100) or 100
    # M10: 加载记忆时使用 limit 参数，n > 100 时发出警告
    all_mems = mem.store.query(limit=limit)
    if len(all_mems) > 100:
        print(f"⚠️  加载了 {len(all_mems)} 条记忆进行 O(n²) 比较，可能较慢。使用 --limit 减少扫描数量。", file=sys.stderr)
    conflicts = []
    checked = set()

    for i, m1 in enumerate(all_mems):
        for m2 in all_mems[i+1:]:
            pair_key = f"{m1['memory_id']}_{m2['memory_id']}"
            if pair_key in checked:
                continue
            checked.add(pair_key)

            score = mem.dedup._text_similarity(m1["content"], m2["content"])
            if mem.dedup.CONFLICT_LOW <= score < mem.dedup.CONFLICT_HIGH:
                conflicts.append({
                    "memory_1": {"id": m1["memory_id"], "content": m1["content"][:60]},
                    "memory_2": {"id": m2["memory_id"], "content": m2["content"][:60]},
                    "similarity": round(score, 4),
                })

    conflicts.sort(key=lambda x: -x["similarity"])
    result = {
        "total_memories": len(all_mems),
        "conflicts_found": len(conflicts),
        "conflicts": conflicts[:20],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    mem.close()


def cmd_echo(args):
    """主动推荐相关记忆"""
    mem = get_memory()
    try:
        from agent_memory.echo import MemoryEcho
        echo_engine = MemoryEcho(mem.store, mem.recall_engine)
        results = echo_engine.echo(context=args.context, limit=args.limit)
    except Exception as e:
        results = []

    if not results:
        print("📭 暂无推荐记忆")
    else:
        for r in results:
            reason = r.get("reason", "")
            content = r.get("content", "")
            mid = r.get("memory_id", "")
            print(f"📖 {reason}: {content}")
            if mid:
                print(f"   ID: {mid}")
    mem.close()


def cmd_bookmark(args):
    """收藏一条记忆"""
    mem = get_memory()
    result = mem.store.bookmark(args.memory_id)
    if result.get("bookmarked"):
        print(f"⭐ 已收藏记忆: {args.memory_id}")
    else:
        print(f"❌ 收藏失败: {result.get('reason', '记忆不存在')}")
    mem.close()


def cmd_bookmarks(args):
    """查看所有收藏的记忆"""
    mem = get_memory()
    results = mem.store.get_bookmarks(limit=args.limit)
    if not results:
        print("📭 暂无收藏的记忆")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
    mem.close()


def cmd_milestones(args):
    """查看成就和解锁状态"""
    mem = get_memory()
    try:
        from agent_memory.growth.achievements import AchievementSystem
        achievements = AchievementSystem(mem.store)
        all_achievements = achievements.get_achievements()
        result = []
        for a in all_achievements:
            result.append({
                "name": a.get("name", ""),
                "icon": a.get("icon", "🔒"),
                "description": a.get("description", ""),
                "unlocked": a.get("unlocked", False),
            })
        if not result:
            print("📭 暂无成就数据")
        else:
            unlocked = sum(1 for a in result if a["unlocked"])
            total = len(result)
            print(f"🏆 成就进度: {unlocked}/{total}")
            for a in result:
                status = "✅" if a["unlocked"] else "🔒"
                print(f"  {status} {a['icon']} {a['name']}: {a['description']}")
    except Exception as e:
        print(f"❌ 获取成就失败: {e}")
    mem.close()


def cmd_batch_remember(args):
    """批量写入记忆（高性能单事务模式）"""
    file_path = args.file
    if not os.path.exists(file_path):
        print(json.dumps({"error": f"文件不存在: {file_path}"}, ensure_ascii=False))
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            items = json.load(f)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"JSON 解析失败: {e}"}, ensure_ascii=False))
            sys.exit(1)

    if not isinstance(items, list):
        print(json.dumps({"error": "文件内容必须是 JSON 数组，示例: [{\"content\": \"...\"}]"}, ensure_ascii=False))
        sys.exit(1)

    mem = get_memory()
    try:
        results = mem.ingest_engine.batch_remember(items)
        stored = sum(1 for r in results if r.get("written"))
        failed = len(items) - stored
        print(f"✅ 批量写入完成：成功 {stored} 条，失败 {failed} 条")
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
    finally:
        mem.close()
