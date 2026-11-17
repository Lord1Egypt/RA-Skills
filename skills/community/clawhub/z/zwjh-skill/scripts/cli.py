# -*- coding: utf-8 -*-
"""
zwjh-skill v2.0.0 统一命令行入口。

把「长期记忆 + 知识图谱 + 自动沉淀 + 检索 + 健康度 + 备份」串成一条命令。
所有功能纯本地、零密钥、按硬件自适应，不拖累电脑。

用法示例：
  python cli.py deposit --text "客户张三的对接人是李四" --source conversation
  python cli.py deposit --file notes.md
  python cli.py query "发布失败的根因"
  python cli.py ask "我最近在忙什么项目"
  python cli.py timeline --from 2026-07-01 --to 2026-07-31 --keyword 发布
  python cli.py graph list
  python cli.py graph show
  python cli.py health
  python cli.py compact --apply
  python cli.py backup
  python cli.py diary --text "今天想清楚了一件事"
  python cli.py analyze
  python cli.py setup
  python cli.py update-check
  python cli.py autopilot
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# ── 让本文件既能 `python cli.py` 也能 `python -m scripts.cli` 运行 ──────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

from scripts import (config, store, embeddings, retrieval, graph, deposit,
                     health, backup, legacy, setup, update_check, hardware, version,
                     conflict_resolver, export, narrative, multimodal, archive,
                     rebuild_index, embedder, memory_access)


# ── 子命令实现 ────────────────────────────────────────────────────────────
def cmd_deposit(args):
    if args.file:
        r = deposit.ingest_file(args.file, day=args.day)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.text:
        if args.conversation:
            r = deposit.deposit_conversation(args.text, day=args.day)
        else:
            r = deposit.deposit_text(args.text, source=args.source or "conversation",
                                     day=args.day, namespace=args.namespace)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        # 从 stdin 读取（便于管道）
        data = sys.stdin.read()
        r = deposit.deposit_conversation(data, day=args.day)
        print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_query(args):
    hits = retrieval.semantic_search(args.query, top_k=args.top)
    if not hits:
        print("（未找到相关记忆）")
        return
    for h in hits:
        print(f"[{h['day']} · {h['source']} · {h['score']}] {h['snippet']}")


def cmd_ask(args):
    print(retrieval.ask(args.query, top_k=args.top))


def cmd_timeline(args):
    hits = retrieval.timeline_search(args.frm, args.to, keyword=args.keyword,
                                     limit=args.limit)
    if not hits:
        print("（该时间线内没有记忆）")
        return
    for h in hits:
        print(f"[{h['day']} · {h['source']}] {h['snippet']}")


def cmd_graph(args):
    if args.gaction == "add-entity":
        eid = store.upsert_entity(args.type, args.name, importance=float(args.importance))
        print("entity_id:", eid)
    elif args.gaction == "relate":
        f = store.find_entity(None, args.frm)
        t = store.find_entity(None, args.to)
        if not f or not t:
            print("实体不存在，请先用 add-entity 创建")
            return
        rid = store.add_relation(f["id"], t["id"], args.relation,
                                 weight=0.6, confidence=0.7)
        print("relation_id:", rid)
    elif args.gaction == "list":
        for e in store.list_entities(limit=args.limit):
            print(f"  [{e['type']}] {e['name']} (id={e['id']}, 重要度={e['importance']})")
    elif args.gaction == "show":
        print(graph.render_mermaid())
    elif args.gaction == "mention":
        for m in graph.mention_link(args.text):
            print(f"  命中实体: {m['name']} ({m['type']})")


def cmd_health(args):
    h = health.audit()
    print(json.dumps(h, ensure_ascii=False, indent=2))


def cmd_compact(args):
    r = health.compact(dry_run=not args.apply)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if args.apply:
        print("✅ 已执行压缩（生成摘要 + 清理索引）")
    else:
        print("⚠️ 这是预览（dry-run）。加 --apply 真正执行。")


def cmd_snapshot(args):
    p = health.snapshot(args.path)
    print("快照已保存:", p)


def cmd_backup(args):
    if args.target == "baidunetdisk":
        r = backup.backup_baidunetdisk(args.path)
    else:
        r = backup.export_local(args.path)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_restore(args):
    r = backup.restore_local(args.path, include_logs=not args.no_logs)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_diary(args):
    mid = store.add_diary(config.today_str(), args.text, mood=args.mood)
    print("diary_id:", mid)


def cmd_analyze(args):
    legacy.analyze_memory(day=args.day)


def cmd_predict(args):
    legacy.predict_risks()


def cmd_report(args):
    legacy.generate_report(days=args.days)


def cmd_demo(args):
    legacy.demo()


def cmd_setup(args):
    r = setup.setup_daily(hour=args.hour, minute=args.minute)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if r.get("ok"):
        print("✅ 定时任务已创建（每日 %02d:%02d 自动进化）" % (args.hour, args.minute))
    else:
        print("❌ 创建失败：", r.get("error") or r.get("output"))


def cmd_remove(args):
    r = setup.remove()
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_status(args):
    r = setup.status()
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_update(args):
    r = update_check.check(remote=args.remote)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    if r["update_available"]:
        print(r["reminder"])
    update_check.mark_seen()


def cmd_hardware(args):
    print(hardware.describe())
    print("示例：5000 条知识点建议子任务数 =", hardware.recommend_subtasks(5000))


# ── 导出命令 ─────────────────────────────────────────────────────────────
def cmd_export(args):
    """多格式导出。"""
    result = export.selective_export(
        format=args.format,
        types=args.types.split(",") if args.types else None,
        day_from=args.from_day,
        day_to=args.to_day,
        importance_min=float(args.importance),
        output_dir=args.output,
    )
    if result["status"] == "ok":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        # 对于文本格式，直接打印内容
        if args.format in ("markdown", "json", "cypher", "csv") and result.get("content"):
            print("\n--- 文件内容 ---")
            print(result["content"][:2000])  # 限制输出长度
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_import(args):
    """从 JSON 文件导入知识图谱数据（export --format json 的往返格式）。"""
    if not os.path.exists(args.path):
        print(f"文件不存在: {args.path}")
        return
    with open(args.path, "r", encoding="utf-8") as f:
        data = json.load(f)
    entities = data.get("entities", [])
    relations = data.get("relations", [])
    facts = data.get("facts", [])
    # 导入实体
    name_to_id = {}
    for e in entities:
        existing = store.find_entity(e.get("type"), e["name"])
        if existing:
            name_to_id[e["name"]] = existing["id"]
        else:
            eid = store.upsert_entity(e.get("type", "concept"), e["name"],
                                       importance=float(e.get("importance", 0.5)))
            name_to_id[e["name"]] = eid
    # 导入关系
    rel_count = 0
    for r in relations:
        from_id = name_to_id.get(r.get("from_name", ""))
        to_id = name_to_id.get(r.get("to_name", ""))
        if from_id and to_id:
            store.add_relation(from_id, to_id, r.get("relation", "关联"),
                               weight=float(r.get("weight", 1.0)),
                               confidence=float(r.get("confidence", 1.0)))
            rel_count += 1
    # 导入事实
    fact_count = 0
    for f in facts:
        ent_id = name_to_id.get(f.get("entity_name", ""))
        if ent_id:
            store.add_fact(ent_id, f.get("predicate", "属性"), f.get("value", ""),
                            source_memory_id=f.get("source_memory_id"))
            fact_count += 1
    print(f"导入完成：实体 {len(entities)}/{len(entities)}，关系 {rel_count}/{len(relations)}，事实 {fact_count}/{len(facts)}")


# ── 叙事命令 ─────────────────────────────────────────────────────────────
def cmd_narrative(args):
    """叙事生成。"""
    if args.naction == "project":
        print(narrative.generate_project_timeline(args.name))
    elif args.naction == "person":
        print(narrative.generate_person_interaction(args.name))
    elif args.naction == "knowledge":
        print(narrative.generate_knowledge_growth(args.name))
    elif args.naction == "weekly":
        print(narrative.generate_weekly_review())
    elif args.naction == "monthly":
        print(narrative.generate_monthly_review())


# ── 多模态命令 ───────────────────────────────────────────────────────────
def cmd_multimodal(args):
    """多模态记忆。"""
    if args.maction == "index-image":
        r = multimodal.index_image(args.path, entity_name=args.entity,
                                    memory_text=args.text)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.maction == "index-audio":
        r = multimodal.index_audio(args.path, entity_name=args.entity,
                                    project_name=args.project)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.maction == "index-file":
        r = multimodal.index_file(args.path, entity_name=args.entity,
                                   project_name=args.project)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.maction == "list":
        r = multimodal.list_media(media_type=args.type, entity_name=args.entity)
        for m in r:
            print(f"[{m['media_type']}] {m['file_path']}")
            print(f"  描述: {m['description'][:60]}...")
    elif args.maction == "associate":
        r = multimodal.MultimodalManager().associate_entity(args.id, args.entity)
        print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_conflicts(args):
    """查看和消解冲突。"""
    pending = conflict_resolver.get_all_pending()

    # 处理指定冲突
    if args.resolve is not None:
        if args.resolve < 1 or args.resolve > len(pending):
            print(f"❌ 编号无效（1~{len(pending)}）")
            return
        c = pending[args.resolve - 1]
        strategies = [
            conflict_resolver.ConflictResolution.OVERWRITE,
            conflict_resolver.ConflictResolution.KEEP_BOTH,
            conflict_resolver.ConflictResolution.MERGE,
            conflict_resolver.ConflictResolution.IGNORE,
        ]
        strategy = strategies[args.strategy - 1]

        # 构建 Conflict 对象
        conflict = conflict_resolver.Conflict(
            conflict_id=c.get("conflict_id", ""),
            entity_id=c.get("entity_id", 0),
            entity_name=c.get("entity_name", ""),
            predicate=c.get("predicate", ""),
            old_value=c.get("old_value", ""),
            new_value=c.get("new_value", ""),
        )

        resolver = conflict_resolver.get_resolver()
        result = resolver.resolve_with_strategy(conflict, strategy)
        conflict_resolver.remove_pending_conflict(c.get("conflict_id", ""))
        print(f"✅ 已处理冲突 #{args.resolve}：{result}")
        return

    # 显示列表
    if not pending:
        print("✅ 没有待处理冲突。")
        return

    print(f"共 {len(pending)} 个待处理冲突：")
    print("=" * 50)
    for i, c in enumerate(pending, 1):
        print(f"{'=' * 50}")
        print(f"  编号 #{i}")
        print(f"  类型：{c.get('type', '?')}")
        print(f"  实体：{c.get('entity_name', '?')}")
        print(f"  属性：{c.get('predicate', '?')}")
        print(f"  旧值：{c.get('old_value', '?')}")
        print(f"  新值：{c.get('new_value', '?')}")
        print(f"  描述：{c.get('description', '?')}")
        print(f"  创建时间：{c.get('created_at', '?')}")
        print(f"  冲突ID：{c.get('conflict_id', '?')}")

    print(f"\n{'=' * 50}")
    print("处理方式：")
    print("  1. 覆盖（新替旧）")
    print("  2. 保留两者（标注版本）")
    print("  3. 合并（取并集）")
    print("  4. 忽略（保留旧值）")
    print(f"\n运行 `python cli.py conflicts --resolve <编号> --strategy <1-4>` 处理")


def cmd_archive(args):
    """自动归档。"""
    if args.stats:
        r = archive.get_archive_stats()
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        r = archive.run_archive(dry_run=args.dry_run)
        print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_mcp(args):
    """启动 MCP 服务器（跨 skill 记忆总线）。"""
    from scripts.mcp_server import run
    run()


def cmd_rebuild_index(args):
    """重建存量记忆向量索引。"""
    r = rebuild_index.rebuild_with_progress(batch_size=args.batch)
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_embedder_info(args):
    """查看 embedding 模型状态。"""
    info = embedder.get_model_info()
    print(json.dumps(info, ensure_ascii=False, indent=2))


# ── v2.6.0 新增命令 ─────────────────────────────────────────────────────────

def cmd_graph_query(args):
    """知识图谱查询（实体搜索/详情/事实/路径）。"""
    if args.action == "search":
        if not args.name:
            print(json.dumps({"error": "缺少 --name 参数"}, ensure_ascii=False))
            return
        results = store.search_entities_by_name(args.name, limit=args.limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.action == "entity":
        if not args.entity_id:
            print(json.dumps({"error": "缺少 --entity-id 参数"}, ensure_ascii=False))
            return
        conn = store.get_conn()
        row = conn.execute("SELECT * FROM entities WHERE id=?", (args.entity_id,)).fetchone()
        if not row:
            print(json.dumps({"error": "实体不存在"}, ensure_ascii=False))
            return
        ent = dict(row)
        rels = store.relations_of(args.entity_id, direction="both")
        facts = store.current_facts(args.entity_id)
        print(json.dumps({"entity": ent, "relations": rels, "facts": facts},
                         ensure_ascii=False, indent=2))
    elif args.action == "facts":
        eid = args.entity_id
        if eid is None and args.name:
            ent = store.find_entity(None, args.name)
            if not ent:
                print(json.dumps({"error": "实体不存在"}, ensure_ascii=False))
                return
            eid = ent["id"]
        if eid is None:
            print(json.dumps({"error": "缺少 --entity-id 或 --name"}, ensure_ascii=False))
            return
        facts = store.current_facts(eid)
        print(json.dumps(facts, ensure_ascii=False, indent=2))
    elif args.action == "path":
        if not args.from_name or not args.to_name:
            print(json.dumps({"error": "缺少 --from-name 或 --to-name"}, ensure_ascii=False))
            return
        result = graph.find_shortest_path(args.from_name, args.to_name)
        if not result:
            print(json.dumps({"error": "未找到路径"}, ensure_ascii=False))
            return
        print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_forget(args):
    """遗忘（软删除）指定记忆或恢复归档。"""
    if args.restore:
        result = store.restore_from_archive(args.restore)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if args.list_archive:
        items = store.list_archive(limit=args.limit)
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return
    if not args.memory_id and not args.day:
        print(json.dumps({"error": "缺少 --memory-id 或 --day 参数"}, ensure_ascii=False))
        return
    conn = store.get_conn()
    now = __import__("datetime").datetime.now().isoformat(timespec="seconds")
    if args.memory_id:
        row = conn.execute("SELECT * FROM memories WHERE id=?", (args.memory_id,)).fetchone()
        if not row:
            print(json.dumps({"error": "记忆不存在"}, ensure_ascii=False))
            return
        d = dict(row)
        existing = conn.execute("SELECT id FROM memories_archive WHERE original_id=?",
                                (args.memory_id,)).fetchone()
        if not existing:
            conn.execute(
                """INSERT INTO memories_archive(original_id, day, source, raw_text,
                   norm_hash, tokens_json, importance, archived_at, reason)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (args.memory_id, d["day"], d["source"], d["raw_text"], d["norm_hash"],
                 d["tokens_json"], d["importance"], now, args.reason))
        conn.execute("DELETE FROM memories WHERE id=?", (args.memory_id,))
        conn.commit()
        print(json.dumps({"ok": True, "forgotten_id": args.memory_id, "archived": True},
                         ensure_ascii=False, indent=2))
    else:
        rows = conn.execute("SELECT * FROM memories WHERE day=?", (args.day,)).fetchall()
        if not rows:
            print(json.dumps({"error": "该日期没有记忆"}, ensure_ascii=False))
            return
        count = 0
        for row in rows:
            d = dict(row)
            existing = conn.execute("SELECT id FROM memories_archive WHERE original_id=?",
                                    (d["id"],)).fetchone()
            if not existing:
                conn.execute(
                    """INSERT INTO memories_archive(original_id, day, source, raw_text,
                       norm_hash, tokens_json, importance, archived_at, reason)
                       VALUES(?,?,?,?,?,?,?,?,?)""",
                    (d["id"], d["day"], d["source"], d["raw_text"], d["norm_hash"],
                     d["tokens_json"], d["importance"], now, args.reason))
            conn.execute("DELETE FROM memories WHERE id=?", (d["id"],))
            count += 1
        conn.commit()
        print(json.dumps({"ok": True, "forgotten_day": args.day, "count": count},
                         ensure_ascii=False, indent=2))


def cmd_export_stream(args):
    """流式导出记忆（分批返回）。"""
    batch_size = min(max(args.batch_size, 1), 200)
    rows = store.list_memories(day_from=args.from_day, day_to=args.to_day,
                               limit=100000, offset=0)
    if not rows:
        print("没有可导出的记忆。")
        return
    batch = rows[:batch_size]
    remaining = len(rows) - len(batch)
    if args.format == "json":
        content = json.dumps(batch, ensure_ascii=False, indent=2)
    elif args.format == "markdown":
        lines = ["# 记忆导出\n\n共 %d 条\n" % len(rows)]
        for r in batch:
            lines.append("## [%s] %s (id=%d)\n\n%s\n" % (
                r["day"], r["source"], r["id"], r["raw_text"]))
        content = "\n".join(lines)
    else:  # csv
        lines = ["id,day,source,importance,raw_text"]
        for r in batch:
            txt = r["raw_text"].replace('"', '""').replace('\n', ' ')
            lines.append('%d,%s,%s,%.2f,"%s"' % (
                r["id"], r["day"], r["source"], r["importance"], txt))
        content = "\n".join(lines)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print("已写入 %s（第 1 批 %d 条，共 %d 条）" % (args.output, len(batch), len(rows)))
    else:
        print(content)
    if remaining > 0:
        print("\n（剩余 %d 条未导出，缩小日期范围或分批请求）" % remaining)


def cmd_access_key(args):
    """查看/轮换访问密钥。"""
    if args.rotate:
        cfg = config.load_config()
        old_key = cfg.get("access_key", "")
        import secrets
        new_key = secrets.token_hex(32)
        cfg["access_key"] = new_key
        config.save_config(cfg)
        print(json.dumps({"ok": True, "rotated": True,
                         "old_key_prefix": old_key[:8] + "..." if old_key else None,
                         "new_key_prefix": new_key[:8] + "..."}, ensure_ascii=False))
        print("⚠️ 密钥已轮换，旧 manifest 签名将失效。请通知调用方。")
    else:
        cfg = config.load_config()
        key = cfg.get("access_key", "")
        if key:
            print("当前 access_key 前缀：%s..." % key[:8])
        else:
            print("尚未配置 access_key，首次调用 manifest 会自动生成。")
        print("运行 `python cli.py access-key --rotate` 轮换密钥。")


def cmd_status_overview(args):
    h = health.audit()
    print("═══════════════════════════════════════════")
    print(f"  🧠 {version.DISPLAY_NAME} v{version.VERSION}")
    print("═══════════════════════════════════════════")
    print(f"  记忆条目 : {h['memories']}")
    print(f"  实体     : {h['entities']}")
    print(f"  关系     : {h['relations']}")
    print(f"  健康度   : {h['score']} / 100")
    print(f"  DB 体积  : {h['db_size_mb']} MB")
    print(f"  硬件档位 : {h['tier']}")
    print("═══════════════════════════════════════════")


def cmd_autopilot(args):
    print("🤖 自动进化开始 ...")
    r = deposit.index_daily_logs()
    print(f"  · 每日日志补录：{r['added']} 条新增")
    legacy.analyze_memory()
    legacy.predict_risks()
    legacy.generate_report()
    h = health.audit()
    print(f"  · 健康度：{h['score']} / 100（陈旧 {h['stale_memories']} · "
          f"孤儿实体 {h['orphan_entities']} · 冲突事实 {h['conflicting_facts']}）")
    # 自动归档
    a = archive.run_archive(dry_run=False)
    print(f"  · 自动归档：{a['archived']['hot']} 热 / {a['archived']['warm']} 温 / {a['archived']['cold']} 冷")
    cfg = config.load_config()
    if cfg.get("auto_backup"):
        b = backup.export_local()
        print(f"  · 自动备份：{b['backup_path']}")
    upd = update_check.check()
    if upd["update_available"]:
        print(upd["reminder"])
    update_check.mark_seen()
    print("✅ 自动进化完成。")


# ── 参数解析 ──────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="zwjh-skill",
        description=f"{version.DISPLAY_NAME} v{version.VERSION} 命令行",
    )
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("deposit", help="沉淀知识点（对话/文件）")
    d.add_argument("--text", help="直接传入文本")
    d.add_argument("--file", help="读取纯文本文件并沉淀")
    d.add_argument("--conversation", action="store_true", help="按段落拆分沉淀")
    d.add_argument("--source", default="conversation")
    d.add_argument("--day", default=None)
    d.add_argument("--namespace", default="public", help="命名空间（默认 public）")
    d.set_defaults(func=cmd_deposit)

    q = sub.add_parser("query", help="语义检索")
    q.add_argument("query")
    q.add_argument("--top", type=int, default=8)
    q.set_defaults(func=cmd_query)

    a = sub.add_parser("ask", help="记忆问答（拼接相关记忆）")
    a.add_argument("query")
    a.add_argument("--top", type=int, default=5)
    a.set_defaults(func=cmd_ask)

    t = sub.add_parser("timeline", help="时间线检索")
    t.add_argument("--from", dest="frm", default=None)
    t.add_argument("--to", default=None)
    t.add_argument("--keyword", default=None)
    t.add_argument("--limit", type=int, default=100)
    t.set_defaults(func=cmd_timeline)

    g = sub.add_parser("graph", help="知识图谱")
    g.add_argument("gaction", choices=["add-entity", "relate", "list", "show", "mention"])
    g.add_argument("--type", default="concept")
    g.add_argument("--name", default=None)
    g.add_argument("--from", dest="frm", default=None)
    g.add_argument("--to", default=None)
    g.add_argument("--relation", default="关联")
    g.add_argument("--importance", default="0.5")
    g.add_argument("--text", default=None)
    g.add_argument("--limit", type=int, default=50)
    g.set_defaults(func=cmd_graph)

    hh = sub.add_parser("health", help="健康度审计")
    hh.set_defaults(func=cmd_health)

    c = sub.add_parser("compact", help="压缩（去重 + 摘要）")
    c.add_argument("--apply", action="store_true")
    c.set_defaults(func=cmd_compact)

    sn = sub.add_parser("snapshot", help="导出快照")
    sn.add_argument("--path", default=None)
    sn.set_defaults(func=cmd_snapshot)

    b = sub.add_parser("backup", help="备份")
    b.add_argument("--target", default="local", choices=["local", "baidunetdisk"])
    b.add_argument("--path", default=None)
    b.set_defaults(func=cmd_backup)

    rs = sub.add_parser("restore", help="恢复")
    rs.add_argument("path")
    rs.add_argument("--no-logs", action="store_true")
    rs.set_defaults(func=cmd_restore)

    di = sub.add_parser("diary", help="写日记")
    di.add_argument("--text", required=True)
    di.add_argument("--mood", default=None)
    di.set_defaults(func=cmd_diary)

    an = sub.add_parser("analyze", help="v1.7 记忆分析")
    an.add_argument("--day", default=None)
    an.set_defaults(func=cmd_analyze)

    pr = sub.add_parser("predict", help="v1.7 预测性维护")
    pr.set_defaults(func=cmd_predict)

    rp = sub.add_parser("report", help="v1.7 进化报告")
    rp.add_argument("--days", type=int, default=30)
    rp.set_defaults(func=cmd_report)

    dm = sub.add_parser("demo", help="模拟演示")
    dm.set_defaults(func=cmd_demo)

    st = sub.add_parser("setup", help="配置硬件感知定时任务")
    st.add_argument("--hour", type=int, default=23)
    st.add_argument("--minute", type=int, default=0)
    st.set_defaults(func=cmd_setup)

    rm = sub.add_parser("remove", help="删除定时任务")
    rm.set_defaults(func=cmd_remove)

    ss = sub.add_parser("task-status", help="查看定时任务状态")
    ss.set_defaults(func=cmd_status)

    uc = sub.add_parser("update-check", help="检查更新")
    uc.add_argument("--remote", action="store_true")
    uc.set_defaults(func=cmd_update)

    hw = sub.add_parser("hardware", help="查看硬件自适应计划")
    hw.set_defaults(func=cmd_hardware)

    cf = sub.add_parser("conflicts", help="查看/消解冲突")
    cf.add_argument("--resolve", type=int, default=None, help="按编号处理冲突")
    cf.add_argument("--strategy", type=int, default=1, choices=[1, 2, 3, 4],
                    help="1=覆盖 2=保留两者 3=合并 4=忽略")
    cf.set_defaults(func=cmd_conflicts)

    # 导出
    ex = sub.add_parser("export", help="多格式导出（Markdown/JSON/Cypher/CSV/Obsidian/Logseq）")
    ex.add_argument("--format", default="markdown",
                    choices=["markdown", "json", "cypher", "csv", "obsidian", "logseq"])
    ex.add_argument("--types", default=None, help="实体类型筛选（逗号分隔）")
    ex.add_argument("--from-day", default=None)
    ex.add_argument("--to-day", default=None)
    ex.add_argument("--importance", default="0")
    ex.add_argument("--output", default=None, help="输出目录")
    ex.set_defaults(func=cmd_export)

    # 导入
    im = sub.add_parser("import", help="导入数据")
    im.add_argument("path", help="文件路径")
    im.set_defaults(func=cmd_import)

    # 叙事
    na = sub.add_parser("narrative", help="时间线叙事生成")
    na.add_argument("naction", choices=["project", "person", "knowledge", "weekly", "monthly"])
    na.add_argument("--name", default=None, help="项目/人物/主题名称")
    na.set_defaults(func=cmd_narrative)

    # 多模态
    mm = sub.add_parser("multimodal", help="多模态记忆")
    mm.add_argument("maction", choices=["index-image", "index-audio", "index-file", "list", "associate"])
    mm.add_argument("--path", default=None)
    mm.add_argument("--entity", default=None)
    mm.add_argument("--text", default=None)
    mm.add_argument("--project", default=None)
    mm.add_argument("--type", default=None)
    mm.add_argument("--id", type=int, default=None)
    mm.set_defaults(func=cmd_multimodal)

    # 归档
    ar = sub.add_parser("archive", help="自动归档（冷热分层 + 时间衰减）")
    ar.add_argument("--dry-run", action="store_true", help="只显示计划，不执行")
    ar.add_argument("--stats", action="store_true", help="显示归档统计")
    ar.set_defaults(func=cmd_archive)

    ov = sub.add_parser("status", help="总览")
    ov.set_defaults(func=cmd_status_overview)

    ap = sub.add_parser("autopilot", help="每日自动进化")
    ap.set_defaults(func=cmd_autopilot)

    # MCP 服务器
    mcp = sub.add_parser("mcp", help="启动 MCP 服务器（跨 skill 记忆总线）")
    mcp.set_defaults(func=cmd_mcp)

    # 重建索引
    ri = sub.add_parser("rebuild-index", help="重建存量记忆向量索引")
    ri.add_argument("--batch", type=int, default=50, help="批次大小（默认 50）")
    ri.set_defaults(func=cmd_rebuild_index)

    # Embedder 信息
    ei = sub.add_parser("embedder-info", help="查看 embedding 模型状态")
    ei.set_defaults(func=cmd_embedder_info)

    # v2.6.0 新增子命令

    # graph-query（知识图谱查询）
    gq = sub.add_parser("graph-query", help="知识图谱查询（实体搜索/详情/事实/路径）")
    gq.add_argument("--action", required=True, choices=["search", "entity", "facts", "path"],
                    help="查询动作")
    gq.add_argument("--name", default=None, help="实体名称（search/facts 用）")
    gq.add_argument("--entity-id", type=int, default=None, help="实体 ID（entity/facts 用）")
    gq.add_argument("--from-name", default=None, help="起始实体名（path 用）")
    gq.add_argument("--to-name", default=None, help="目标实体名（path 用）")
    gq.add_argument("--limit", type=int, default=20, help="返回数量上限（默认 20）")
    gq.set_defaults(func=cmd_graph_query)

    # forget（遗忘/归档）
    fg = sub.add_parser("forget", help="遗忘（软删除）指定记忆")
    fg.add_argument("--memory-id", type=int, default=None, help="要遗忘的记忆 ID")
    fg.add_argument("--day", default=None, help="要遗忘的日期（YYYY-MM-DD）")
    fg.add_argument("--reason", default="CLI forget request", help="遗忘原因")
    fg.add_argument("--restore", type=int, default=None, help="从归档表恢复指定 archive_id")
    fg.add_argument("--list-archive", action="store_true", help="列出归档的记忆")
    fg.set_defaults(func=cmd_forget)

    # export-stream（流式导出）
    es = sub.add_parser("export-stream", help="流式导出记忆（分批返回）")
    es.add_argument("--format", required=True, choices=["json", "markdown", "csv"],
                    help="导出格式")
    es.add_argument("--batch-size", type=int, default=50, help="每批条数（默认 50，最大 200）")
    es.add_argument("--from-day", default=None, help="起始日期过滤")
    es.add_argument("--to-day", default=None, help="结束日期过滤")
    es.add_argument("--output", default=None, help="输出文件路径（不指定则打印到 stdout）")
    es.set_defaults(func=cmd_export_stream)

    # access-key（查看/轮换访问密钥）
    ak = sub.add_parser("access-key", help="查看/轮换访问密钥（HMAC 用）")
    ak.add_argument("--rotate", action="store_true", help="轮换密钥（旧 manifest 失效）")
    ak.set_defaults(func=cmd_access_key)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "cmd", None):
        # 默认进入总览
        cmd_status_overview(args)
        return 0
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
