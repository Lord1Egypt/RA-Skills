#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WBFlow 批量工厂 · 初始化（Init Series）

读 batch.json → 为每个条目在 batches/<batch_id>/output/<NN>_<slug>/ 下建骨架目录
（01_story..07_videos）+ 写 seed.json（展开该条目 seed 供 pipeline Phase0 直读）
+ 初始化 batch_manifest.json（所有条目 status=queued）。

纯标准库，无第三方依赖，适合定时自动化无网环境。

用法：
  python init_series.py --config batches/<batch_id>/batch.json
  python init_series.py --config batch.json --dry-run      # 只打印计划不建目录
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

STAGES = ["01_story", "02_script", "03_storyboard", "04_prompts",
          "05_chars", "06_images", "07_videos"]


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_batch(config_path):
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def build_seed(item, batch, index):
    return {
        "batch_id": batch.get("batch_id"),
        "item_index": index,
        "slug": item.get("slug"),
        "output_name": item.get("output_name", item.get("slug")),
        "seed_theme": item.get("seed_theme", ""),
        "episode_count": item.get("episode_count", 1),
        "duration_sec": item.get("duration_sec", 20),
        "style": item.get("style") or batch.get("default_style", ""),
        "engine": batch.get("engine", ""),
    }


def main():
    ap = argparse.ArgumentParser(description="WBFlow init_series: 按 batch.json 建批量骨架")
    ap.add_argument("--config", required=True, help="batch.json 路径")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划不建目录")
    args = ap.parse_args()

    cfg = load_batch(args.config)
    batch_id = cfg.get("batch_id", "batch")
    base_dir = os.path.dirname(os.path.abspath(args.config))
    output_dir = os.path.join(base_dir, "output")

    items = cfg.get("items", [])
    if not items:
        print("[WARN] batch.json 没有 items，未生成任何骨架", file=sys.stderr)
        return

    manifest = {
        "batch_id": batch_id,
        "title": cfg.get("title", ""),
        "engine": cfg.get("engine", ""),
        "generated_at": now_iso(),
        "items": [],
    }

    print(f"batch_id = {batch_id}  条目数 = {len(items)}")
    for i, item in enumerate(items, start=1):
        slug = item.get("slug") or f"item{i:02d}"
        folder = f"{i:02d}_{slug}"
        workdir = os.path.join(output_dir, folder)
        print(f"  [{i:02d}] {slug:24s} -> {os.path.relpath(workdir, base_dir)}")

        if not args.dry_run:
            os.makedirs(workdir, exist_ok=True)
            for st in STAGES:
                os.makedirs(os.path.join(workdir, st), exist_ok=True)
            seed = build_seed(item, cfg, i)
            with open(os.path.join(workdir, "seed.json"), "w", encoding="utf-8") as f:
                json.dump(seed, f, ensure_ascii=False, indent=2)
        else:
            seed = build_seed(item, cfg, i)

        manifest["items"].append({
            "index": i,
            "slug": slug,
            "output_name": seed["output_name"],
            "workdir": os.path.relpath(workdir, base_dir),
            "status": "queued",
            "final_path": None,
            "duration_sec_est": seed["duration_sec"],
            "error": None,
            "updated_at": now_iso(),
        })

    if not args.dry_run:
        mpath = os.path.join(base_dir, "batch_manifest.json")
        with open(mpath, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"\n已写入 batch_manifest.json（{len(items)} 条，全部 queued）")
        print("下一步：对每条调用 wbflow-pipeline（workdir=<条目目录>, 读 seed.json 直跑）")
    else:
        print("\n[dry-run] 未创建任何目录")


if __name__ == "__main__":
    main()
