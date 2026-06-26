#!/usr/bin/env python3
"""BGE palace index builder with incremental auto-maintenance.

方案 A: git diff 门 — palace 文件无变化时跳过重建，0 秒退出。
方案 B: mtime 追踪 — 精确到文件级的变更检测，无人值守。

运行方式:
  python3 build_index_bge.py          # 方案 A（git diff 门）
  python3 build_index_bge.py --force  # 强制全量重建
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/zhouyi0415126.com/ai_matrix/vault/01_core')
MANIFEST = ROOT / 'memory/palace/watchdog/index/watchdog_manifest_v1_2026-04-08.jsonl'
OUT = ROOT / 'memory/palace/watchdog/index/watchdog_vectors_v1_2026-04-08.jsonl'
TRACKER = ROOT / 'scripts/watchdog/.palace_index_tracker.json'


def read_text(rel_path: str) -> str:
    p = ROOT / rel_path
    if not p.exists():
        return ''
    return p.read_text(encoding='utf-8', errors='ignore')[:12000]


def is_cold_zone_path(path: str) -> bool:
    return "archive_basement" in path


def has_palace_changes_since_last_commit() -> bool:
    """方案 A: git diff 门。检查 palace/ 是否有未提交变更。"""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", "memory/palace/"],
        capture_output=True, text=True, cwd=ROOT
    )
    # 排除索引构建产物自身变更（watchdog/index/ 下的文件）
    changed_lines = [
        line for line in result.stdout.strip().splitlines()
        if line and 'memory/palace/watchdog/index/' not in line
    ]
    if changed_lines:
        print(f"[GIT_DIFF] 检测到 palace 源文件变更 ({len(changed_lines)} 个):")
        for l in changed_lines[:10]:
            print(f"  {l}")
        return True
    print("[GIT_DIFF] palace 源文件无变更（自上次 commit 以来）")
    return False


def detect_changes_via_mtime() -> tuple:
    """方案 B: mtime 追踪。对比 tracker 中的 mtime，返回变更文件列表。"""
    tracker = {}
    if TRACKER.exists():
        tracker = json.loads(TRACKER.read_text())

    changed_files = []
    new_tracker = {}

    for line in MANIFEST.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if is_cold_zone_path(item['path']):
            continue
        fp = ROOT / item['path']
        current_mtime = round(fp.stat().st_mtime, 2) if fp.exists() else 0
        new_tracker[item['path']] = current_mtime
        if current_mtime != tracker.get(item['path'], 0):
            changed_files.append(item['path'])

    return changed_files, new_tracker


def main():
    force = '--force' in sys.argv

    # 方案 A: git diff 门
    if not force:
        if not has_palace_changes_since_last_commit():
            # 没有 git 变更时，检查 mtime 追踪（方案 B）
            changed_files, new_tracker = detect_changes_via_mtime()
            if not changed_files:
                print("[SKIP] 无 palace 文件变更（git diff + mtime 均无变化），跳过重建")
                return
            print(f"[MTIME] mtime 检测到 {len(changed_files)} 个文件变更，触发重建")
            TRACKER.write_text(json.dumps(new_tracker, indent=2, ensure_ascii=False) + '\n')
        else:
            # git 有变更，重建后更新 tracker
            _, new_tracker = detect_changes_via_mtime()
            TRACKER.write_text(json.dumps(new_tracker, indent=2, ensure_ascii=False) + '\n')

    # 全量索引构建
    from FlagEmbedding import BGEM3FlagModel

    model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=False)
    rows = []
    batch = []
    metas = []

    for line in MANIFEST.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if is_cold_zone_path(item['path']):
            print(f"[COLD_ZONE_SKIP] 跳过冷区文件: {item['path']}")
            continue
        text = read_text(item['path'])
        if not text:
            continue
        batch.append(text)
        metas.append(item)

    result = model.encode(batch, batch_size=4, max_length=512)
    dense_vecs = result['dense_vecs']

    for item, vec in zip(metas, dense_vecs):
        fp = ROOT / item['path']
        mtime = round(fp.stat().st_mtime, 2) if fp.exists() else 0
        rows.append({
            'path': item['path'],
            'type': item.get('type'),
            'priority': item.get('priority'),
            'mtime': mtime,
            'embedding': vec.tolist() if hasattr(vec, 'tolist') else list(vec),
        })

    OUT.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n', encoding='utf-8')
    print(f'[WATCHDOG_INDEX_READY] rows={len(rows)} out={OUT}')


if __name__ == '__main__':
    main()
