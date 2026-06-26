#!/usr/bin/env python3
"""
ClawHub Daily 一键执行器
按顺序编排 4 步脚本链路：抓取 → 指标计算 → 推荐 → 推送

使用方法：
  python clawhub_daily_executor.py
  python clawhub_daily_executor.py --skip-push       # 只生成简报，不推送
  python clawhub_daily_executor.py --date 2026-06-03  # 指定日期
  python clawhub_daily_executor.py --num 100          # 只抓 100 个
"""
import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# 项目根目录（executor 所在目录）
PROJECT_ROOT = Path(__file__).parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"


def run_step(name, cmd, cwd=None):
    """执行单步脚本，返回是否成功"""
    print(f"\n{'='*60}")
    print(f"  STEP: {name}")
    print(f"  CMD:  {' '.join(str(c) for c in cmd)}")
    print(f"{'='*60}")
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or str(PROJECT_ROOT),
            capture_output=False,
            text=True,
        )
        elapsed = time.time() - start
        if result.returncode != 0:
            print(f"  [FAIL] {name} 退出码: {result.returncode} ({elapsed:.1f}s)")
            return False
        print(f"  [OK] {name} 完成 ({elapsed:.1f}s)")
        return True
    except Exception as e:
        elapsed = time.time() - start
        print(f"  [FAIL] {name} 异常: {e} ({elapsed:.1f}s)")
        return False


def main():
    parser = argparse.ArgumentParser(description="ClawHub Daily 一键执行器")
    parser.add_argument("--date", default=None, help="快照日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--num", type=int, default=200, help="抓取数量（默认 200）")
    parser.add_argument("--skip-push", action="store_true", help="跳过推送步骤")
    parser.add_argument("--skip-feishu", action="store_true", help="跳过飞书推送")
    parser.add_argument("--skip-ima", action="store_true", help="跳过 IMA 推送")
    parser.add_argument("--dimension", default=None, help="推荐维度（默认按日期自动）")
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    print(f"\n🦞 ClawHub Daily Executor | {date_str}")
    print(f"   抓取数量: {args.num}")
    print(f"   推送: {'跳过' if args.skip_push else '开启'}")

    snapshot_path = DATA_DIR / "snapshots" / f"{date_str}.json"
    metrics_path = DATA_DIR / "snapshots" / f"{date_str}.metrics.json"
    rec_path = DATA_DIR / "recommended" / f"{date_str}.json"

    # Step 1: 抓取
    if not run_step(
        "1/4 抓取 ClawHub 数据",
        [sys.executable, str(SCRIPTS_DIR / "fetch_clawhub.py"),
         "--num", str(args.num), "--output", str(snapshot_path.parent),
         "--date", date_str],
    ):
        print("\n[ABORT] 抓取失败，终止执行")
        return 1

    # Step 2: 指标计算
    if not run_step(
        "2/4 计算指标",
        [sys.executable, str(SCRIPTS_DIR / "compute_metrics.py"),
         "--input", str(snapshot_path),
         "--output", str(metrics_path)],
    ):
        print("\n[ABORT] 指标计算失败，终止执行")
        return 1

    # Step 3: 生成推荐
    recommend_cmd = [
        sys.executable, str(SCRIPTS_DIR / "daily_recommend.py"),
        "--date", date_str,
        "--data-dir", str(DATA_DIR),
    ]
    if args.dimension:
        recommend_cmd.extend(["--dimension", args.dimension])
    if not run_step("3/4 生成推荐", recommend_cmd):
        print("\n[ABORT] 推荐生成失败，终止执行")
        return 1

    # Step 4: 推送
    if args.skip_push:
        print("\n[SKIP] 推送步骤已跳过")
    else:
        # 4a: 飞书推送
        if not args.skip_feishu:
            feishu_cmd = [
                sys.executable, str(SCRIPTS_DIR / "push_to_feishu.py"),
                "--recommendation", str(rec_path),
            ]
            if not run_step("4a/4 飞书推送", feishu_cmd):
                print("  [WARN] 飞书推送失败，继续执行后续步骤")

        # 4b: IMA 推送
        if not args.skip_ima:
            ima_cmd = [
                sys.executable, str(SCRIPTS_DIR / "push_to_ima.py"),
                "--recommendation", str(rec_path),
            ]
            if not run_step("4b/4 IMA 推送", ima_cmd):
                print("  [WARN] IMA 推送失败，不影响主流程")

    # 汇总
    print(f"\n{'='*60}")
    print(f"  🦞 执行完成 | {date_str}")
    print(f"  快照: {snapshot_path}")
    print(f"  指标: {metrics_path}")
    print(f"  推荐: {rec_path}")
    print(f"  简报: {rec_path.with_suffix('.md')}")
    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
