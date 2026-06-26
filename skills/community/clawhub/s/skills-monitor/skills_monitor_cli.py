#!/usr/bin/env python3
"""
Skills Monitor CLI — 本地 Skills 监控评估系统 Demo
Day 1-4 完整功能 CLI（隐性评分版）

用法:
    python skills_monitor_cli.py init                          # 初始化身份
    python skills_monitor_cli.py identity [--show-key]         # 查看身份信息
    python skills_monitor_cli.py status                        # 查看系统状态
    python skills_monitor_cli.py list                          # 列出已安装 skills
    python skills_monitor_cli.py run <skill_id> [task]         # 运行 skill 并采集数据
    python skills_monitor_cli.py history [--skill <id>] [--limit N]  # 查看运行历史
    python skills_monitor_cli.py summary [--skill <id>]        # 查看汇总
    python skills_monitor_cli.py benchmark <skill_id> [--runs N] # 基准运行
    python skills_monitor_cli.py evaluate [--skill <id>]       # 综合评估
    python skills_monitor_cli.py compare <skill_id>            # 基准对比
    python skills_monitor_cli.py recommend                     # Skill 推荐
    python skills_monitor_cli.py report                        # 生成完整日报
    python skills_monitor_cli.py diagnose [--send] [--trigger ...] # 诊断报告
    python skills_monitor_cli.py web [--port N]                # 启动 Web 面板
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 确保项目根目录在 path 中
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from skills_monitor.core.identity import IdentityManager
from skills_monitor.core.interceptor import configure, run_skill_function
from skills_monitor.core.implicit_feedback import ImplicitFeedbackEngine
from skills_monitor.core.benchmark import BenchmarkRunner
from skills_monitor.core.comparator import SkillComparator
from skills_monitor.core.evaluator import SkillEvaluator
from skills_monitor.core.recommender import SkillRecommender
from skills_monitor.core.reporter import ReportGenerator
from skills_monitor.core.diagnostic import DiagnosticReporter
from skills_monitor.data.store import DataStore
from skills_monitor.adapters.skill_registry import SkillRegistry
from skills_monitor.adapters.runners import SkillRunner, get_adapter


# ──────── 默认路径 ────────
DEFAULT_SKILLS_DIR = str(PROJECT_ROOT / "skills")
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.skills_monitor")


def _get_manager() -> IdentityManager:
    return IdentityManager(DEFAULT_CONFIG_DIR)


def _get_store() -> DataStore:
    return DataStore(DEFAULT_CONFIG_DIR)


def _get_registry() -> SkillRegistry:
    return SkillRegistry(DEFAULT_SKILLS_DIR)


def _init_interceptor(mgr: IdentityManager, store: DataStore):
    """初始化拦截器"""
    if mgr.is_initialized:
        configure(store, mgr.agent_id)


# ──────── 子命令 ────────

def cmd_init(args):
    """初始化身份"""
    mgr = _get_manager()
    result = mgr.initialize(force=args.force)

    if result["status"] == "initialized":
        print("🎉 初始化成功！")
        print(f"   Agent ID  : {result['agent_id']}")
        print(f"   API Key   : {result['api_key']}")
        print(f"   配置文件  : {result['config_path']}")
        print()
        print("⚠️  请妥善保管 API Key，它仅在初始化时显示一次。")
    else:
        print(f"ℹ️  已初始化过 (Agent ID: {result['agent_id']})")
        print("   使用 --force 重新初始化")

    # 自动设置 skills 目录
    mgr.set_skills_dir(DEFAULT_SKILLS_DIR)

    # 扫描 skills
    registry = _get_registry()
    print(f"\n{registry.summary()}")


def cmd_identity(args):
    """查看身份信息（Agent ID + API Key）"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 尚未初始化，请先运行: skills-monitor init")
        return

    config = mgr.get_config()
    agent_id = config.get("agent_id", "N/A")

    print("=" * 55)
    print("🔑 Skills Monitor 身份信息")
    print("=" * 55)
    print(f"  Agent ID    : {agent_id}")
    print(f"  初始化时间  : {config.get('created_at', 'N/A')}")

    if args.show_key:
        api_key = mgr.api_key
        if api_key:
            print(f"  API Key     : {api_key}")
        else:
            print(f"  API Key     : (无法从安全存储读取，请使用 init --force 重新生成)")
    else:
        print(f"  API Key     : (已隐藏，使用 --show-key 查看)")

    # Key 健康检查
    health = mgr.check_key_health()
    if health.get("warnings"):
        print()
        for w in health["warnings"]:
            print(f"  ⚠️  {w}")
    else:
        print(f"\n  ✅ Key 状态正常 (安全存储: {health.get('secure_store', 'none')})")

    print()
    print("📋 绑定小程序时需要填写：")
    print(f"  • 智能体 ID : {agent_id}")
    if args.show_key and mgr.api_key:
        print(f"  • Key       : {mgr.api_key}")
    else:
        print(f"  • Key       : 运行 skills-monitor identity --show-key 查看")


def cmd_status(args):
    """查看系统状态"""
    mgr = _get_manager()
    store = _get_store()
    registry = _get_registry()

    if not mgr.is_initialized:
        print("❌ 尚未初始化，请先运行: python skills_monitor_cli.py init")
        return

    config = mgr.get_config()
    print("=" * 55)
    print("📊 Skills Monitor 系统状态")
    print("=" * 55)
    print(f"  Agent ID    : {config.get('agent_id', 'N/A')}")
    print(f"  初始化时间  : {config.get('created_at', 'N/A')}")
    print(f"  Skills 目录 : {config.get('skills_dir', 'N/A')}")
    print()
    print(registry.summary())

    # 今日运行统计
    today = datetime.now().strftime("%Y-%m-%d")
    runs = store.get_runs(agent_id=mgr.agent_id, limit=1000)
    today_runs = [r for r in runs if r["start_time"].startswith(today)]
    success_runs = [r for r in today_runs if r["status"] == "success"]

    print()
    print(f"📈 今日运行: {len(today_runs)} 次 (成功 {len(success_runs)})")

    if today_runs:
        durations = [r["duration_ms"] for r in today_runs if r.get("duration_ms")]
        if durations:
            avg_d = sum(durations) / len(durations)
            print(f"   平均耗时: {avg_d:.0f}ms")


def cmd_list(args):
    """列出已安装 skills"""
    registry = _get_registry()
    categories = registry.get_skills_by_category()

    print("=" * 55)
    print("📦 已安装 Skills")
    print("=" * 55)

    for cat, skills in sorted(categories.items()):
        print(f"\n  🏷  {cat}")
        for s in skills:
            entry_icon = "✅" if s.entry_type != "none" else "📄"
            print(f"    {entry_icon} {s.slug:35s} v{s.version:8s} [{s.entry_type}]")
            if s.description:
                print(f"       {s.description[:60]}")

    runnable = registry.get_runnable_skills()
    print(f"\n  ─── 可运行: {len(runnable)} / {len(registry.list_skills())} ───")


def cmd_run(args):
    """运行 skill 并自动采集数据"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化: python skills_monitor_cli.py init")
        return

    store = _get_store()
    _init_interceptor(mgr, store)
    registry = _get_registry()

    skill_info = registry.get_skill(args.skill_id)
    if not skill_info:
        print(f"❌ 找不到 skill: {args.skill_id}")
        print(f"   可用的 skills:")
        for s in registry.get_runnable_skills():
            print(f"     - {s.slug}")
        return

    if skill_info.entry_type == "none":
        print(f"⚠️  Skill [{args.skill_id}] 是纯文档型 skill，没有可执行入口")
        return

    # 获取适配器
    adapter = get_adapter(skill_info)
    task_name = args.task or ""

    # 构建参数
    params = {}
    if args.params:
        for p in args.params:
            if "=" in p:
                k, v = p.split("=", 1)
                params[k] = v

    print(f"🚀 运行 [{skill_info.slug}]", end="")
    if task_name:
        print(f" → {task_name}", end="")
    print(f" ...")
    print(f"   入口: {skill_info.entry_file}")
    print()

    # 用拦截器包裹运行
    def _do_run():
        if isinstance(adapter, SkillRunner):
            return adapter.run(task_name=task_name, params=params)
        elif hasattr(adapter, "run_task"):
            if task_name:
                return adapter.run_task(task_name, **params)
            else:
                return adapter.run_task(**params)
        return {"success": False, "error": "无法调用"}

    result = run_skill_function(
        func=_do_run,
        skill_id=skill_info.slug,
        task_name=task_name or "default",
    )

    # 输出结果
    print("-" * 55)
    status_icon = "✅" if result["status"] == "success" else "❌"
    print(f"{status_icon} 状态: {result['status']}")
    print(f"⏱  耗时: {result['duration_ms']:.0f}ms")
    print(f"🔑 Run ID: {result['run_id']}")

    if result.get("error"):
        print(f"\n❌ 错误: {result['error']}")

    if result.get("result"):
        inner = result["result"]
        if isinstance(inner, dict):
            output = inner.get("output", inner)
            if isinstance(output, str) and len(output) > 500:
                print(f"\n📄 输出 (截取前500字):\n{output[:500]}...")
            elif isinstance(output, (dict, list)):
                print(f"\n📄 输出:\n{json.dumps(output, ensure_ascii=False, indent=2)[:1000]}")
            else:
                print(f"\n📄 输出:\n{output}")

    # 运行后自动记录隐性反馈（基于执行结果）
    store = _get_store()
    engine = ImplicitFeedbackEngine(store, mgr.agent_id)
    engine.record_from_run_context(
        skill_id=skill_info.slug,
        run_id=result["run_id"],
        run_status=result["status"],
        run_duration_ms=result["duration_ms"],
        user_messages=[],  # CLI 模式无对话上下文
        session_continued=True,
    )


def cmd_history(args):
    """查看运行历史"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化")
        return

    store = _get_store()
    runs = store.get_runs(
        skill_id=args.skill if args.skill else None,
        agent_id=mgr.agent_id,
        limit=args.limit,
    )

    if not runs:
        print("📭 暂无运行记录")
        return

    print("=" * 70)
    print(f"📜 运行历史 (最近 {len(runs)} 条)")
    print("=" * 70)
    print(f"{'Run ID':>12}  {'Skill':25s}  {'Task':20s}  {'Status':8s}  {'Duration':>10s}")
    print("-" * 70)

    for r in runs:
        dur = f"{r['duration_ms']:.0f}ms" if r.get("duration_ms") else "N/A"
        status_icon = "✅" if r["status"] == "success" else ("❌" if r["status"] == "error" else "⏳")
        print(
            f"{r['run_id']:>12}  {r['skill_id']:25s}  "
            f"{(r.get('task_name') or '-'):20s}  "
            f"{status_icon} {r['status']:6s}  {dur:>10s}"
        )


def cmd_summary(args):
    """查看汇总"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化")
        return

    store = _get_store()
    registry = _get_registry()

    if args.skill:
        # 单个 skill 汇总
        summary = store.get_skill_summary(args.skill, mgr.agent_id)
        print(f"\n📊 Skill 汇总: {args.skill}")
        print("-" * 40)
        print(f"  总运行次数 : {summary['total_runs']}")
        print(f"  成功次数   : {summary['success_count']}")
        print(f"  成功率     : {summary['success_rate']}%")
        if summary['avg_duration_ms']:
            print(f"  平均耗时   : {summary['avg_duration_ms']}ms")
        if summary['avg_rating']:
            print(f"  满意度(隐性): {summary['avg_rating']:.2f}/5.0")
            fb_count = summary.get('implicit_feedback_count', 0)
            conf = summary.get('avg_confidence')
            conf_str = f" (置信度 {conf:.1%})" if conf else ""
            print(f"  隐性反馈数 : {fb_count}{conf_str}")
    else:
        # 全局汇总
        print("=" * 55)
        print("📊 全局运行汇总")
        print("=" * 55)
        
        for skill_info in registry.get_runnable_skills():
            summary = store.get_skill_summary(skill_info.slug, mgr.agent_id)
            if summary["total_runs"] > 0:
                rate = f"{summary['success_rate']}%"
                dur = f"{summary['avg_duration_ms']:.0f}ms" if summary['avg_duration_ms'] else "N/A"
                rating = f"{summary['avg_rating']:.1f}/5" if summary['avg_rating'] else "-"
                print(
                    f"  {skill_info.slug:30s}  "
                    f"runs:{summary['total_runs']:3d}  "
                    f"success:{rate:>6s}  "
                    f"avg:{dur:>8s}  "
                    f"satisfaction:{rating}"
                )

        # 无记录的 skills
        total = len(registry.list_skills())
        with_data = sum(
            1
            for s in registry.get_runnable_skills()
            if store.get_skill_summary(s.slug, mgr.agent_id)["total_runs"] > 0
        )
        if with_data < total:
            print(f"\n  ℹ️  {total - with_data} 个 skill 尚无运行记录")


# ──────── Day 2/3 新增子命令 ────────

DEMO_DATA_DIR = str(PROJECT_ROOT / ".skills_monitor_demo")
DEMO_CACHE_DIR = str(PROJECT_ROOT / ".skills_monitor_demo" / "benchmark_cache")
REPORTS_DIR = str(PROJECT_ROOT / "reports" / "monitor")


def cmd_benchmark(args):
    """基准运行"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化: python skills_monitor_cli.py init")
        return

    store = _get_store()
    registry = _get_registry()

    skill_info = registry.get_skill(args.skill_id)
    if not skill_info:
        print(f"❌ 找不到 skill: {args.skill_id}")
        return

    runner = BenchmarkRunner(
        registry=registry,
        store=store,
        agent_id=mgr.agent_id,
        cache_dir=os.path.join(DEFAULT_CONFIG_DIR, "benchmark_cache"),
    )

    n_runs = args.runs or 10

    if args.simulate:
        print(f"📊 模拟基准运行 [{args.skill_id}] ({n_runs} 次)")
        stats = runner.run_simulated_benchmark(args.skill_id, n_runs=n_runs)
    else:
        print(f"🔬 真实基准运行 [{args.skill_id}] ({n_runs} 次)")
        task = args.task or ""

        def _progress(cur, total, result):
            if result:
                icon = "✅" if result.success else "❌"
                print(f"  [{cur}/{total}] {icon} {result.duration_ms:.0f}ms")

        stats = runner.run_benchmark(
            skill_id=args.skill_id,
            task_name=task,
            n_runs=n_runs,
            delay_between=0.5,
            progress_callback=_progress,
        )

    print(f"\n📊 基准结果:")
    print(f"  {stats.summary_line()}")


def cmd_evaluate(args):
    """综合评估"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化")
        return

    store = _get_store()
    registry = _get_registry()
    evaluator = SkillEvaluator(store, mgr.agent_id)

    if args.skill:
        scores = [evaluator.evaluate_skill(args.skill)]
    else:
        skill_ids = [s.slug for s in registry.get_runnable_skills()]
        scores = evaluator.evaluate_all(skill_ids)

    if not scores:
        print("📭 暂无可评估的数据")
        return

    print("=" * 70)
    print("📊 综合评估")
    print("=" * 70)
    print(f"  {'排名':<4} {'Skill':<28} {'总分':<8} {'等级':<16} {'成功率':<8}")
    print(f"  {'─' * 64}")

    for i, score in enumerate(scores, 1):
        sr = f"{score.factors['success_rate']:.0f}%" if score.factors.get('success_rate') is not None else "-"
        grade_short = score.grade.split("(")[0].strip()
        print(f"  {i:<4} {score.skill_id:<28} {score.total_score:<8.1f} {grade_short:<16} {sr:<8}")

    # 详细评分
    if args.verbose and scores:
        print()
        for score in scores:
            print(score.format_report())
            print()


def cmd_compare(args):
    """基准对比"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化")
        return

    store = _get_store()
    registry = _get_registry()
    comparator = SkillComparator(store, mgr.agent_id)

    runner = BenchmarkRunner(
        registry=registry,
        store=store,
        agent_id=mgr.agent_id,
        cache_dir=os.path.join(DEFAULT_CONFIG_DIR, "benchmark_cache"),
    )

    # 尝试加载缓存的基准数据，否则模拟
    cached = runner.load_cached_stats(args.skill_id)
    if cached:
        print(f"📊 使用缓存基准数据对比 [{args.skill_id}]")
        bench_stats = cached
    else:
        print(f"📊 生成模拟基准数据并对比 [{args.skill_id}]")
        bench_stats = runner.run_simulated_benchmark(args.skill_id, n_runs=10)

    comp = comparator.compare_with_benchmark(args.skill_id, bench_stats)
    print(comp.format_report())


def cmd_recommend(args):
    """Skill 推荐"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化")
        return

    store = _get_store()
    registry = _get_registry()

    recommender = SkillRecommender(registry, store, mgr.agent_id)
    recs = recommender.get_all_recommendations(max_per_type=3)

    if not recs:
        print("✅ 你的 skills 配置很完善！暂无推荐。")
        return

    print("=" * 55)
    print("💡 Skill 推荐")
    print("=" * 55)

    for i, rec in enumerate(recs[:8], 1):
        print(rec.format_line())
        print()


def cmd_report(args):
    """生成完整日报"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化")
        return

    store = _get_store()
    registry = _get_registry()

    print("📄 生成综合日报...")

    # 评估
    evaluator = SkillEvaluator(store, mgr.agent_id)
    skill_ids = [s.slug for s in registry.get_runnable_skills()]
    scores = evaluator.evaluate_all(skill_ids)

    # 推荐
    recommender = SkillRecommender(registry, store, mgr.agent_id)
    recs = recommender.get_all_recommendations(max_per_type=3)

    # 生成报告
    reporter = ReportGenerator(
        store=store,
        registry=registry,
        agent_id=mgr.agent_id,
        reports_dir=REPORTS_DIR,
    )
    filepath = reporter.generate_and_save_daily(
        scores=scores,
        recommendations=recs,
    )

    print(f"✅ 日报已生成: {filepath}")
    print(f"\n💡 查看: cat {filepath}")
    print(f"🌐 Web 面板: python skills_monitor_cli.py web")


def cmd_diagnose(args):
    """生成诊断报告（含企微推送）"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化")
        return

    store = _get_store()
    registry = _get_registry()

    trigger = args.trigger or "manual"
    print(f"🏥 生成诊断报告 (触发方式: {trigger})...")

    diag = DiagnosticReporter(
        store=store,
        registry=registry,
        agent_id=mgr.agent_id,
        reports_dir=REPORTS_DIR.replace("monitor", "diagnostic"),
    )

    content, filepath = diag.generate_and_save(
        trigger=trigger,
        extra_context=args.context if args.context else None,
    )

    print(f"✅ 诊断报告已生成: {filepath}")

    # 企微推送
    if args.send:
        print(f"\n📤 推送到企微...")
        try:
            from wecom_bot.sender import sender as wecom_sender
            summary = diag.generate_wecom_summary(content)
            ok, result = wecom_sender.send_to_webhook(summary, msgtype="markdown")
            if ok:
                print(f"✅ 企微推送成功")
            else:
                print(f"⚠️ 企微推送失败: {result}")
        except Exception as e:
            print(f"⚠️ 企微推送异常: {e}")

    if args.print_report:
        print(f"\n{'=' * 60}")
        print(content)
        print(f"{'=' * 60}")
    else:
        print(f"\n💡 查看报告: cat {filepath}")
        print(f"💡 带推送: skills-monitor diagnose --send")


def cmd_web(args):
    """启动 Web 面板"""
    port = args.port or 5050
    demo_flag = "--demo" if args.demo else ""
    debug_flag = "--debug" if args.debug else ""

    cmd = f"python3 {PROJECT_ROOT / 'skills_monitor_web.py'} --port {port} {demo_flag} {debug_flag}"
    print(f"🚀 启动 Web 面板: http://127.0.0.1:{port}")
    os.system(cmd.strip())


def cmd_upload(args):
    """上报数据到中心化服务器"""
    mgr = _get_manager()
    if not mgr.is_initialized:
        print("❌ 请先初始化: skills-monitor init")
        return

    from skills_monitor.core.uploader import DataUploader

    server_url = args.server or "http://localhost:5100"
    uploader = DataUploader(server_url)
    uploader.init(mgr.agent_id, mgr.api_key)

    # 1. 注册/更新 Agent
    print(f"📡 连接服务器: {server_url}")
    print(f"🔑 Agent ID: {mgr.agent_id[:8]}...")

    if args.register:
        print("📝 注册 Agent...")
        ok, result = uploader.register(name=args.name)
        if ok:
            print(f"✅ 注册成功: {result.get('agent', {}).get('name', '')}")
        else:
            print(f"❌ 注册失败: {result.get('error', '未知错误')}")
            return

    # 2. 上报数据
    report_type = args.type or "daily"
    print(f"\n📤 上报 {report_type} 数据...")

    if report_type == "diagnostic":
        ok, result = uploader.upload_diagnostic()
    else:
        ok, result = uploader.upload_daily()

    if ok:
        report_info = result.get("report", {})
        print(f"✅ 上报成功!")
        print(f"  日期: {report_info.get('report_date', '-')}")
        print(f"  健康度: {report_info.get('health_score', '-')}")
        print(f"  报告 ID: {report_info.get('id', '-')}")
    else:
        print(f"❌ 上报失败: {result.get('error', '未知错误')}")

    # 3. 查看历史
    if args.history:
        print(f"\n📋 服务器历史报告:")
        ok, reports = uploader.get_reports(limit=5)
        if ok:
            for r in reports:
                print(f"  {r.get('report_date', '-')} | {r.get('report_type', '-')} | 健康度 {r.get('health_score', '-')}")
        else:
            print(f"  (无数据)")


def cmd_server(args):
    """启动中心化服务器"""
    port = args.port or 5100
    host = args.host or "0.0.0.0"
    debug = args.debug

    print(f"🚀 Skills Monitor 中心化服务器")
    print(f"📡 {host}:{port} (debug={'on' if debug else 'off'})")
    print(f"")
    print(f"API 端点:")
    print(f"  Agent 注册:    POST /api/agent/register")
    print(f"  数据上报:      POST /api/agent/report")
    print(f"  微信回调:      /api/wechat/callback")
    print(f"  小程序 API:    /api/mp/*")
    print(f"  H5 报告页:     /h5/*")
    print(f"  健康检查:      GET /health")
    print(f"")

    # 设置环境变量
    os.environ["SM_HOST"] = host
    os.environ["SM_PORT"] = str(port)
    os.environ["SM_DEBUG"] = "true" if debug else "false"

    try:
        from server.app import create_app
        app = create_app()
        app.run(host=host, port=port, debug=debug)
    except ImportError as e:
        print(f"❌ 启动失败: {e}")
        print(f"💡 请先安装依赖: pip install flask-sqlalchemy apscheduler")


# ──────── 主入口 ────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Skills Monitor — 本地 Skills 监控评估系统 Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化身份")
    p_init.add_argument("--force", action="store_true", help="强制重新初始化")

    # identity
    p_id = subparsers.add_parser("identity", help="查看身份信息（智能体 ID / Key）")
    p_id.add_argument("--show-key", action="store_true", help="显示 Key")

    # status
    subparsers.add_parser("status", help="查看系统状态")

    # list
    subparsers.add_parser("list", help="列出已安装 skills")

    # run
    p_run = subparsers.add_parser("run", help="运行 skill 并采集数据")
    p_run.add_argument("skill_id", help="Skill slug")
    p_run.add_argument("task", nargs="?", default="", help="任务名 (可选)")
    p_run.add_argument("--params", "-p", nargs="*", help="参数 key=value")

    # history
    p_hist = subparsers.add_parser("history", help="查看运行历史")
    p_hist.add_argument("--skill", "-s", type=str, help="按 skill 过滤")
    p_hist.add_argument("--limit", "-l", type=int, default=20, help="显示条数")

    # summary
    p_sum = subparsers.add_parser("summary", help="查看汇总")
    p_sum.add_argument("--skill", "-s", type=str, help="指定 skill")

    # benchmark (Day 2)
    p_bench = subparsers.add_parser("benchmark", help="基准运行")
    p_bench.add_argument("skill_id", help="Skill slug")
    p_bench.add_argument("--runs", "-n", type=int, default=10, help="运行次数 (默认 10)")
    p_bench.add_argument("--task", "-t", type=str, default="", help="任务名")
    p_bench.add_argument("--simulate", action="store_true", help="模拟运行 (不实际执行)")

    # evaluate (Day 2)
    p_eval = subparsers.add_parser("evaluate", help="综合评估")
    p_eval.add_argument("--skill", "-s", type=str, help="指定 skill (不指定则评估全部)")
    p_eval.add_argument("--verbose", "-v", action="store_true", help="显示详细评分")

    # compare (Day 2)
    p_comp = subparsers.add_parser("compare", help="基准对比")
    p_comp.add_argument("skill_id", help="Skill slug")

    # recommend (Day 2)
    subparsers.add_parser("recommend", help="Skill 推荐")

    # report (Day 3)
    subparsers.add_parser("report", help="生成完整日报")

    # diagnose (Day 5 — 定时诊断报告)
    p_diag = subparsers.add_parser("diagnose", help="生成诊断报告（含健康度+问题+建议）")
    p_diag.add_argument("--send", action="store_true", help="推送到企微")
    p_diag.add_argument("--trigger", "-t", type=str, default="manual",
                         choices=["manual", "scheduled", "post_install"],
                         help="触发方式 (默认 manual)")
    p_diag.add_argument("--context", "-c", type=str, default="", help="额外上下文说明")
    p_diag.add_argument("--print", dest="print_report", action="store_true", help="在终端打印报告")

    # web (Day 3)
    p_web = subparsers.add_parser("web", help="启动 Web 面板")
    p_web.add_argument("--port", type=int, default=5050, help="端口号 (默认 5050)")
    p_web.add_argument("--demo", action="store_true", help="使用 Demo 数据")
    p_web.add_argument("--debug", action="store_true", help="调试模式")

    # upload (v0.4 — 上报数据到中心化服务器)
    p_upload = subparsers.add_parser("upload", help="上报数据到中心化服务器")
    p_upload.add_argument("--server", "-s", type=str, default="http://localhost:5100",
                          help="服务器地址 (默认 http://localhost:5100)")
    p_upload.add_argument("--type", "-t", type=str, default="daily",
                          choices=["daily", "diagnostic"],
                          help="上报类型 (默认 daily)")
    p_upload.add_argument("--register", action="store_true", help="同时注册/更新 Agent")
    p_upload.add_argument("--name", type=str, default="", help="Agent 名称")
    p_upload.add_argument("--history", action="store_true", help="显示服务器历史")

    # server (v0.4 — 启动中心化服务器)
    p_server = subparsers.add_parser("server", help="启动中心化服务器")
    p_server.add_argument("--port", type=int, default=5100, help="端口号 (默认 5100)")
    p_server.add_argument("--host", type=str, default="0.0.0.0", help="监听地址")
    p_server.add_argument("--debug", action="store_true", help="调试模式")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    commands = {
        "init": cmd_init,
        "identity": cmd_identity,
        "status": cmd_status,
        "list": cmd_list,
        "run": cmd_run,
        "history": cmd_history,
        "summary": cmd_summary,
        "benchmark": cmd_benchmark,
        "evaluate": cmd_evaluate,
        "compare": cmd_compare,
        "recommend": cmd_recommend,
        "report": cmd_report,
        "diagnose": cmd_diagnose,
        "web": cmd_web,
        "upload": cmd_upload,
        "server": cmd_server,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
