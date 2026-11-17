"""
CLI 入口 — 统一命令行接口
─────────────────────────
用法:
    python run.py search "AI趋势"                  # 快速搜索
    python run.py deep "AI趋势"                     # 深度分析
    python run.py compare "AI" "区块链"              # 对比分析
    python run.py verify "某个断言"                  # 可信度验证
    python run.py monitor "AI趋势"                   # 设置监控
    python run.py resume <session_id>               # 恢复会话
    python run.py health                             # 健康检查
    python run.py status                             # 系统状态
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("uia")


def cmd_search(args):
    """快速搜索"""
    from layers.input_adapter import InputAdapter
    from layers.pipeline_coordinator import PipelineCoordinator

    adapter = InputAdapter()
    request = adapter.adapt({
        "query": args.query,
        "max_results": args.max_results,
        "engine_group": args.engine_group,
    })
    request = request.__class__(
        query=request.query,
        intent=request.intent,
        language=request.language,
        max_results=request.max_results,
        engine_group=request.engine_group,
        timeout=request.timeout,
        session_id=request.session_id,
    )

    coordinator = PipelineCoordinator()
    result = coordinator.execute(request)

    if result.output_path:
        print(f"\n报告已生成: {result.output_path}")
        print(result.data.get("content_preview", ""))
    else:
        print(f"状态: {result.status.value}")
        if result.errors:
            print(f"错误: {result.errors}")


def cmd_deep(args):
    """深度分析"""
    from layers.input_adapter import InputAdapter
    from layers.pipeline_coordinator import PipelineCoordinator

    adapter = InputAdapter()
    request = adapter.adapt({
        "query": args.query,
        "max_results": args.max_results,
    })

    coordinator = PipelineCoordinator()
    result = coordinator.execute(request)

    if result.output_path:
        print(f"\n分析报告已生成: {result.output_path}")
        print(result.data.get("content_preview", ""))
    else:
        print(f"状态: {result.status.value}")
        if result.errors:
            print(f"错误: {result.errors}")


def cmd_compare(args):
    """对比分析"""
    from layers.input_adapter import InputAdapter
    from layers.pipeline_coordinator import PipelineCoordinator

    query = f"{args.item_a} vs {args.item_b}"
    adapter = InputAdapter()
    request = adapter.adapt({
        "query": query,
        "intent": "compare",
    })

    coordinator = PipelineCoordinator()
    result = coordinator.execute(request)

    if result.output_path:
        print(f"\n对比报告已生成: {result.output_path}")
    else:
        print(f"状态: {result.status.value}")


def cmd_verify(args):
    """可信度验证"""
    from layers.input_adapter import InputAdapter
    from layers.pipeline_coordinator import PipelineCoordinator

    adapter = InputAdapter()
    request = adapter.adapt({
        "query": args.claim,
        "intent": "verify",
    })

    coordinator = PipelineCoordinator()
    result = coordinator.execute(request)

    if result.output_path:
        print(f"\n验证报告已生成: {result.output_path}")
    else:
        print(f"状态: {result.status.value}")


def cmd_monitor(args):
    """设置监控"""
    print(f"监控已设置: {args.query}")
    print(f"检查间隔: {args.interval}小时")
    print("(Cron 功能需要在 CodeBuddy runtime 中配置)")
    # TODO: 通过 cron 工具设置定时任务


def cmd_resume(args):
    """恢复会话"""
    from layers.pipeline_coordinator import resume_session

    result = resume_session(args.session_id)
    if result:
        print(f"会话 {args.session_id} 已恢复")
        print(f"状态: {result.status.value}")
    else:
        print(f"无法恢复会话 {args.session_id}")


def cmd_health(args):
    """健康检查"""
    from layers.preflight import PreflightChecker

    checker = PreflightChecker()
    result = checker.check()

    print("\n=== 系统健康检查 ===")
    for check in result.checks:
        status = "✅" if check.passed else "❌"
        print(f"  {status} {check.name}: {check.message}")

    if result.all_passed:
        print("\n系统状态: 正常 ✅")
    else:
        print(f"\n系统状态: 异常 ❌")
        print(f"失败项: {result.failures}")
    if result.warnings:
        print(f"警告: {result.warnings}")


def cmd_status(args):
    """系统状态"""
    from middlewares.metrics import MetricsCollector

    collector = MetricsCollector()
    summary = collector.get_summary()

    print("\n=== 系统状态 ===")
    print(f"运行时间: {summary['uptime_seconds']:.0f}s")
    print(f"总请求数: {summary['total_requests']}")
    print(f"成功: {summary['successful_requests']}")
    print(f"失败: {summary['failed_requests']}")
    print(f"降级: {summary['degraded_requests']}")
    print(f"成功率: {summary['success_rate']:.1%}")
    print(f"熔断事件: {summary['circuit_breaker_events']}")
    print(f"回滚事件: {summary['rollback_events']}")


def main():
    parser = argparse.ArgumentParser(
        description="万能情报员 Universal Intelligence Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run.py search "AI趋势"
  python run.py deep "区块链技术"
  python run.py compare "Python" "Rust"
  python run.py verify "地球是平的这个说法"
  python run.py monitor "科技新闻" --interval 6
  python run.py health
  python run.py status
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # search
    p_search = subparsers.add_parser("search", help="快速搜索")
    p_search.add_argument("query", help="搜索查询")
    p_search.add_argument("--max-results", type=int, default=100, help="最大结果数")
    p_search.add_argument("--engine-group", choices=["cn", "global", "all"], default="all")

    # deep
    p_deep = subparsers.add_parser("deep", help="深度分析")
    p_deep.add_argument("query", help="分析主题")
    p_deep.add_argument("--max-results", type=int, default=100)

    # compare
    p_compare = subparsers.add_parser("compare", help="对比分析")
    p_compare.add_argument("item_a", help="对比项A")
    p_compare.add_argument("item_b", help="对比项B")

    # verify
    p_verify = subparsers.add_parser("verify", help="可信度验证")
    p_verify.add_argument("claim", help="待验证的断言")

    # monitor
    p_monitor = subparsers.add_parser("monitor", help="设置监控")
    p_monitor.add_argument("query", help="监控主题")
    p_monitor.add_argument("--interval", type=int, default=6, help="检查间隔(小时)")

    # resume
    p_resume = subparsers.add_parser("resume", help="恢复会话")
    p_resume.add_argument("session_id", help="会话ID")

    # health
    subparsers.add_parser("health", help="健康检查")

    # status
    subparsers.add_parser("status", help="系统状态")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "search": cmd_search,
        "deep": cmd_deep,
        "compare": cmd_compare,
        "verify": cmd_verify,
        "monitor": cmd_monitor,
        "resume": cmd_resume,
        "health": cmd_health,
        "status": cmd_status,
    }

    try:
        commands[args.command](args)
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        logger.exception(f"命令执行失败: {e}")
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
