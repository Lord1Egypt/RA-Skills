#!/usr/bin/env python3
"""wdp 可恢复批处理骨架（模板）。

把同目录的 wdp_checkpoint.py 一起复制进你的项目，然后：
  - 替换 process()：幂等处理单项（输出由输入确定性命名 + temp+rename 原子写）
  - 替换 key_of()：确定性幂等键（通常取输入路径/ID/哈希）
  - 脚本逻辑/输入变化时，把 SEED 改为 v2/v3…（旧 checkpoint 自动失效）

用法:
  python batch_runner.py --dry-run --manifest manifest.json        # 预览
  python batch_runner.py --limit 3 --manifest manifest.json        # smoke test
  python batch_runner.py --manifest manifest.json --workers 4      # 全量并发
  python batch_runner.py --retry-failures                          # 只重跑失败项
"""
import argparse
import json
import os
import sys

import wdp_checkpoint as wdp


# ============ 用户需要替换的部分 ============
SEED = "v1"  # 逻辑/输入变化时递增


def load_manifest(path):
    """返回可迭代的 item 列表。"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def key_of(item):
    """确定性幂等键：同一输入永远得到同一键。"""
    return item["id"]


def process(item):
    """幂等处理单项。输出必须：由输入确定性命名 + temp+rename 原子写。"""
    src, dst = item["src"], item["dst"]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(src, "rb") as fin, open(dst + ".tmp", "wb") as fout:
        fout.write(fin.read())
    os.replace(dst + ".tmp", dst)  # 原子替换，绝不半写
# ============ 用户需要替换的部分 ============


def build_parser():
    p = argparse.ArgumentParser(description="可恢复批处理")
    p.add_argument("--manifest", default="manifest.json")
    p.add_argument("--workers", type=int, default=None,
                   help="并发 worker 数（默认 min(8, cpu)，IIS 进程数控制类比）")
    p.add_argument("--checkpoint", default="output/.wdp-checkpoint.json")
    p.add_argument("--failures-log", default="work/logs/failures.log")
    p.add_argument("--dry-run", action="store_true", help="只报告将处理的数量，不执行")
    p.add_argument("--limit", type=int, default=None, help="smoke test：只跑前 N 项")
    p.add_argument("--retry-failures", action="store_true", help="只重跑 failures.log 中失败项")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    items = list(load_manifest(args.manifest))

    if args.retry_failures:
        fl = wdp.FailLog(args.failures_log)
        failed = set(fl.failed_items())
        # FailLog 的 item_key 一律 str() 化，key_of 可能是 int/哈希 → 统一 str 匹配
        items = [it for it in items if str(key_of(it)) in failed]

    if args.dry_run:
        print(f"[dry-run] 将处理 {len(items)} 项, workers={args.workers or 'auto'}")
        return 0

    if args.limit:
        items = items[:args.limit]

    cp = wdp.Checkpoint(args.checkpoint, key_fn=key_of, seed=SEED)
    prog = wdp.Progress(total=len(items), label="batch")
    fl = wdp.FailLog(args.failures_log)
    try:
        res = wdp.run_batch(items, process, max_workers=args.workers,
                            checkpoint=cp, progress=prog, failures=fl)
    finally:
        cp.flush()  # 即使异常也确保已处理项落盘
    print(json.dumps(res, ensure_ascii=False))
    return 1 if (res["fatal"] or res["interrupted"]) else 0


if __name__ == "__main__":
    sys.exit(main())
