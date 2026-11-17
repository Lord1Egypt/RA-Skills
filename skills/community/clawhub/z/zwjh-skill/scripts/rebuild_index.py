# -*- coding: utf-8 -*-
"""
存量记忆重建索引 —— 后台分批进行，不阻塞使用。

功能：
  - 读取所有存量记忆
  - 批量推理生成向量（ONNX BGE）
  - 写入 vectors 表（BLOB）
  - 进度日志输出
  - 不阻塞正常使用（分批 + 让出 CPU）
  - 支持断点续传（已处理的跳过）
"""

from __future__ import annotations

import sys
import time
from datetime import datetime

from . import store, config
from .hardware import get_plan


def rebuild(batch_size: int = 50, max_count: int = 0) -> dict:
    """
    重建所有存量记忆的向量索引。
    
    batch_size: 每批处理的条数
    max_count: 最大处理条数（0 表示全部）
    
    返回: {total, processed, skipped, failed, elapsed_seconds}
    """
    from . import embedder

    # 检查模型是否可用
    if not embedder.is_model_available():
        # 尝试初始化
        if not embedder.initialize():
            return {
                "total": 0,
                "processed": 0,
                "skipped": 0,
                "failed": 0,
                "error": "ONNX 模型不可用，将回退 TF-IDF: %s" % embedder.get_model_info().get("error", ""),
            }

    # 获取所有记忆
    conn = store.get_conn()
    rows = conn.execute(
        "SELECT id, raw_text FROM memories ORDER BY id"
    ).fetchall()

    total = len(rows)
    if max_count > 0:
        rows = rows[:max_count]

    processed = 0
    skipped = 0
    failed = 0
    start_time = time.time()

    # 确保 vectors 表存在
    embedder._ensure_vectors_table()

    # 分批处理
    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i + batch_size]
        for row in chunk:
            memory_id = row["id"]
            text = row["raw_text"] or ""

            # 检查是否已存在
            existing = conn.execute(
                "SELECT 1 FROM vectors WHERE memory_id=?", (memory_id,)
            ).fetchone()
            if existing:
                skipped += 1
                continue

            # 编码并存储
            try:
                success = embedder.encode_and_store(memory_id, text)
                if success:
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                print("编码失败 (memory_id=%d): %s" % (memory_id, str(e)), file=sys.stderr)

        # 每批处理后让出 CPU
        if i + batch_size < len(rows):
            time.sleep(0.01)  # 10ms 让出

    elapsed = round(time.time() - start_time, 2)

    return {
        "total": total,
        "processed": processed,
        "skipped": skipped,
        "failed": failed,
        "elapsed_seconds": elapsed,
        "batch_size": batch_size,
    }


def rebuild_with_progress(batch_size: int = 50, max_count: int = 0) -> dict:
    """
    带进度输出的重建索引（供 CLI 调用）。
    """
    from . import embedder

    if not embedder.is_model_available():
        if not embedder.initialize():
            info = embedder.get_model_info()
            print("⚠️ ONNX 模型不可用: %s" % info.get("error", ""), file=sys.stderr)
            print("将回退 TF-IDF 检索。", file=sys.stderr)
            return {
                "total": 0,
                "processed": 0,
                "skipped": 0,
                "failed": 0,
                "error": info.get("error", ""),
            }

    conn = store.get_conn()
    rows = conn.execute(
        "SELECT id, raw_text FROM memories ORDER BY id"
    ).fetchall()

    total = len(rows)
    if max_count > 0:
        rows = rows[:max_count]

    print("开始重建索引：共 %d 条记忆，批次大小 %d" % (len(rows), batch_size))

    processed = 0
    skipped = 0
    failed = 0
    start_time = time.time()

    embedder._ensure_vectors_table()

    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i + batch_size]
        for row in chunk:
            memory_id = row["id"]
            text = row["raw_text"] or ""

            existing = conn.execute(
                "SELECT 1 FROM vectors WHERE memory_id=?", (memory_id,)
            ).fetchone()
            if existing:
                skipped += 1
                continue

            try:
                success = embedder.encode_and_store(memory_id, text)
                if success:
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                print("编码失败 (memory_id=%d): %s" % (memory_id, str(e)), file=sys.stderr)

        # 进度输出
        progress = min(i + batch_size, len(rows))
        pct = progress / len(rows) * 100 if rows else 100
        print("  进度: %d/%d (%.1f%%) 已处理 %d 跳过 %d 失败 %d" % (
            progress, len(rows), pct, processed, skipped, failed
        ))

        if i + batch_size < len(rows):
            time.sleep(0.01)

    elapsed = round(time.time() - start_time, 2)

    print("\n重建索引完成：")
    print("  总计: %d" % total)
    print("  已处理: %d" % processed)
    print("  已跳过: %d" % skipped)
    print("  失败: %d" % failed)
    print("  耗时: %d 秒" % elapsed)

    return {
        "total": total,
        "processed": processed,
        "skipped": skipped,
        "failed": failed,
        "elapsed_seconds": elapsed,
        "batch_size": batch_size,
    }


if __name__ == "__main__":
    rebuild_with_progress(batch_size=50)
