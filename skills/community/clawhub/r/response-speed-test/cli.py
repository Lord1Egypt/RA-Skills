#!/usr/bin/env python3
"""
Response Speed Test CLI
命令行界面

Usage:
    response-speed-test run [--output FORMAT]
    response-speed-test benchmark --iterations N
    response-speed-test report --input FILE
    response-speed-test probe --component COMPONENT
"""

import argparse
import sys
import time
from pathlib import Path

from core import ResponseSpeedMeter, ResponseSpeedBenchmark
from probes import GatewayProbe, SessionProbe, MemoryProbe, LLMProbe
from reporters import ConsoleReporter, JSONReporter, MarkdownReporter


def cmd_run(args):
    """執行單次測試"""
    meter = ResponseSpeedMeter()
    console = ConsoleReporter()
    
    print("🚀 開始響應速度測試...")
    
    # 模擬完整測量流程
    meter.start({"message": "CLI 測試消息"})
    
    # 模擬各階段
    time.sleep(0.02)
    meter.checkpoint("T1", {"gateway": "test"})
    
    time.sleep(0.01)
    meter.checkpoint("T2", {"session": "main"})
    
    time.sleep(0.05)
    meter.checkpoint("T3", {"segments": 89})
    
    time.sleep(0.01)
    meter.checkpoint("T4", {"model": "qwen3.5-plus"})
    
    time.sleep(0.5)  # 模擬 TTFT
    meter.checkpoint("T5", {"first_token": True})
    
    time.sleep(0.3)  # 模擬生成
    meter.checkpoint("T6", {"completion_tokens": 100})
    
    time.sleep(0.02)
    meter.checkpoint("T7", {"delivered": True})
    
    meter.end()
    
    # 輸出報告
    if args.output == "json":
        reporter = JSONReporter()
        print(reporter.export_meter(meter))
    elif args.output == "markdown":
        reporter = MarkdownReporter()
        print(reporter.export_meter(meter))
    else:
        console.report_meter(meter)
    
    return 0


def cmd_benchmark(args):
    """執行基準測試"""
    benchmark = ResponseSpeedBenchmark()
    console = ConsoleReporter()
    
    print(f"🏃 執行 {args.iterations} 次基準測試...")
    
    for i in range(args.iterations):
        meter = ResponseSpeedMeter(f"bench_{i:03d}")
        
        meter.start()
        time.sleep(0.01)
        meter.checkpoint("T1")
        time.sleep(0.01)
        meter.checkpoint("T2")
        time.sleep(0.02)
        meter.checkpoint("T3")
        time.sleep(0.01)
        meter.checkpoint("T4")
        time.sleep(0.1)
        meter.checkpoint("T5")
        time.sleep(0.05)
        meter.checkpoint("T6")
        meter.end()
        
        benchmark.add_result(meter)
        print(f"  完成測試 {i+1}/{args.iterations}")
    
    # 輸出報告
    console.report_benchmark(benchmark)
    
    # 保存結果
    if args.save:
        reporter = JSONReporter(output_dir=args.save)
        filepath = reporter.save_benchmark(benchmark)
        print(f"\n📁 結果已保存到: {filepath}")
    
    return 0


def cmd_probe(args):
    """執行探針測試"""
    console = ConsoleReporter()
    
    print(f"🔍 執行 {args.component} 探針測試...")
    
    if args.component == "gateway":
        probe = GatewayProbe()
    elif args.component == "session":
        probe = SessionProbe()
    elif args.component == "memory":
        probe = MemoryProbe()
    elif args.component == "llm":
        probe = LLMProbe()
    else:
        print(f"❌ 未知組件: {args.component}")
        return 1
    
    result = probe.probe()
    
    print(f"\n📊 探針結果:")
    print(f"  組件: {result.probe_name}")
    print(f"  階段: {result.stage}")
    print(f"  成功: {'✅' if result.success else '❌'}")
    print(f"  耗時: {result.duration_ms:.3f} ms")
    
    if result.error:
        print(f"  錯誤: {result.error}")
    
    return 0


def cmd_report(args):
    """生成報告"""
    print(f"📝 生成報告...")
    print(f"輸入文件: {args.input}")
    print(f"輸出格式: {args.format}")
    
    # TODO: 實現從文件讀取並生成報告
    
    return 0


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="Response Speed Test - 響應速度測試工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # run 命令
    run_parser = subparsers.add_parser("run", help="執行單次測試")
    run_parser.add_argument(
        "--output", "-o",
        choices=["console", "json", "markdown"],
        default="console",
        help="輸出格式"
    )
    
    # benchmark 命令
    bench_parser = subparsers.add_parser("benchmark", help="執行基準測試")
    bench_parser.add_argument(
        "--iterations", "-n",
        type=int,
        default=10,
        help="測試次數"
    )
    bench_parser.add_argument(
        "--save", "-s",
        type=str,
        help="保存結果到目錄"
    )
    
    # probe 命令
    probe_parser = subparsers.add_parser("probe", help="執行探針測試")
    probe_parser.add_argument(
        "--component", "-c",
        choices=["gateway", "session", "memory", "llm"],
        required=True,
        help="測試組件"
    )
    
    # report 命令
    report_parser = subparsers.add_parser("report", help="生成報告")
    report_parser.add_argument(
        "--input", "-i",
        required=True,
        help="輸入文件"
    )
    report_parser.add_argument(
        "--format", "-f",
        choices=["console", "json", "markdown"],
        default="markdown",
        help="輸出格式"
    )
    
    args = parser.parse_args()
    
    if args.command == "run":
        return cmd_run(args)
    elif args.command == "benchmark":
        return cmd_benchmark(args)
    elif args.command == "probe":
        return cmd_probe(args)
    elif args.command == "report":
        return cmd_report(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
