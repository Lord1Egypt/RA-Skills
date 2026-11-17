#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WBFlow 批量工厂 · 汇总（Aggregate）

扫描 batches/<batch_id>/output/ 各条目 final.mp4 → 更新 batch_manifest.json
（存在即 done）+ 打印批量清单表。可选 --montage 用 ffmpeg 把所有成品拼合集预览。

纯标准库；montage 需要 ffmpeg 在 PATH（同 assemble.py 前置要求）。

用法：
  python aggregate.py --batch batches/<batch_id>
  python aggregate.py --batch batches/<batch_id> --montage
  python aggregate.py --batch batches/<batch_id> --dry-run
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_manifest(batch_dir):
    mpath = os.path.join(batch_dir, "batch_manifest.json")
    if not os.path.exists(mpath):
        print(f"[ERROR] 找不到 {mpath}，请先跑 init_series.py", file=sys.stderr)
        sys.exit(1)
    with open(mpath, encoding="utf-8") as f:
        return json.load(f)


def find_final(workdir):
    if not os.path.isdir(workdir):
        return None
    cand = [f for f in os.listdir(workdir)
            if f.lower().endswith(".mp4") and "final" in f.lower()]
    return os.path.join(workdir, cand[0]) if cand else None


def main():
    ap = argparse.ArgumentParser(description="WBFlow aggregate: 汇总批量成品")
    ap.add_argument("--batch", required=True, help="batches/<batch_id> 目录")
    ap.add_argument("--montage", action="store_true", help="把所有成品拼成合集预览")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划不写文件")
    args = ap.parse_args()

    batch_dir = os.path.abspath(args.batch)
    manifest = load_manifest(batch_dir)

    done = failed = queued = 0
    for it in manifest["items"]:
        workdir = os.path.join(batch_dir, it["workdir"])
        final = find_final(workdir)
        if final:
            it["status"] = "done"
            it["final_path"] = final
            it["updated_at"] = now_iso()
            done += 1
        elif it["status"] == "failed":
            failed += 1
        else:
            it["status"] = "queued"
            queued += 1

    print(f"\n批次 {manifest.get('batch_id')} 汇总：done={done} queued={queued} failed={failed}\n")
    print(f"{'#':>2}  {'slug':22s} {'output_name':18s} {'status':7s} final")
    print("-" * 72)
    for it in manifest["items"]:
        fp = it.get("final_path") or "-"
        print(f"{it['index']:>2}  {it['slug']:22s} {str(it['output_name']):18s} "
              f"{it['status']:7s} {fp}")

    if not args.dry_run:
        mpath = os.path.join(batch_dir, "batch_manifest.json")
        with open(mpath, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"\n已刷新 batch_manifest.json")
    else:
        print("\n[dry-run] 未写入 manifest")

    if args.montage and not args.dry_run:
        finals = [it["final_path"] for it in manifest["items"]
                  if it["status"] == "done" and it.get("final_path")]
        if len(finals) < 2:
            print("[WARN] 成品不足 2 条，跳过合集")
        else:
            _montage(batch_dir, finals)
    elif args.montage and args.dry_run:
        print("[dry-run] 将拼接所有 done 成品为 montage.mp4（未执行）")


def _montage(batch_dir, finals):
    import tempfile
    concat = os.path.join(tempfile.gettempdir(), "wbflow_montage_concat.txt")
    with open(concat, "w", encoding="utf-8") as f:
        for p in finals:
            f.write(f"file '{os.path.abspath(p)}'\n")
    out = os.path.join(batch_dir, "montage.mp4")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
           "-i", concat, "-c", "copy", out]
    print(f"\n拼接合集：{' | '.join(os.path.basename(p) for p in finals)}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"已生成合集预览：{out}")
    except FileNotFoundError:
        print("[ERROR] 未找到 ffmpeg（需置于 PATH），合集跳过", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        msg = e.stderr[-300:] if e.stderr else str(e)
        print(f"[ERROR] ffmpeg 失败：{msg}", file=sys.stderr)


if __name__ == "__main__":
    main()
