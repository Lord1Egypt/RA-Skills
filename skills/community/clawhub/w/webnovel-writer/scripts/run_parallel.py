#!/usr/bin/env python3
"""Novel Writer 增量检测引擎

- 基于文件 mtime + SHA256 判断是否需要重新检测
- SQLite 缓存检测结果，相同内容秒出
- 并行执行检测脚本
"""

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent.parent / ".cache" / "novel_writer_cache.db"

def _ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            script TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            result_json TEXT,
            created_at REAL,
            UNIQUE(script, file_path)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_lookup ON cache(script, file_path)")
    conn.commit()
    return conn

def _file_hash(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def _get_cached(conn, script: str, filepath: str, file_hash: str) -> Optional[dict]:
    row = conn.execute(
        "SELECT result_json FROM cache WHERE script=? AND file_path=? AND file_hash=?",
        (script, filepath, file_hash)
    ).fetchone()
    if row:
        return json.loads(row[0])
    return None

def _set_cache(conn, script: str, filepath: str, file_hash: str, result: dict):
    conn.execute(
        "INSERT OR REPLACE INTO cache (script, file_path, file_hash, result_json, created_at) VALUES (?,?,?,?,?)",
        (script, filepath, file_hash, json.dumps(result, ensure_ascii=False), time.time())
    )
    conn.commit()

def get_changed_files(directory: str) -> list[str]:
    """获取所有 .md 文件，按 mtime 排序"""
    files = []
    for f in sorted(Path(directory).rglob("*.md")):
        files.append(str(f))
    return files

def run_parallel_checks(
    novel_dir: str,
    scripts: list[str] = None,
    workers: int = 4,
    use_cache: bool = True,
    extra_args: list[str] = None,
) -> dict[str, subprocess.CompletedProcess]:
    """并行运行检测脚本，支持缓存"""
    if scripts is None:
        scripts_dir = Path(__file__).parent
        scripts = sorted(
            p.stem for p in scripts_dir.glob("*.py")
            if p.stem not in ("cli", "__init__", "backup", "changelog", "config_manager", "run_parallel", "cache_engine")
        )

    extra_args = extra_args or []
    files = get_changed_files(novel_dir)
    if not files:
        print("⚠️  未找到章节文件")
        return {}

    conn = _ensure_db() if use_cache else None
    results = {}
    cache_hits = 0
    total = len(scripts)

    print(f"🚀 并行检测 {total} 个脚本 × {len(files)} 个文件 (workers={workers})\n")

    def run_one(script: str) -> tuple[str, subprocess.CompletedProcess, bool]:
        cached = False
        # 检查缓存
        if conn:
            all_same = True
            cached_result = None
            for f in files:
                fh = _file_hash(f)
                c = _get_cached(conn, script, f, fh)
                if c is None:
                    all_same = False
                    break
                cached_result = c
            if all_same and cached_result is not None:
                cached = True
                # 返回一个假的 CompletedProcess
                fake = subprocess.CompletedProcess(
                    args=[script], returncode=0,
                    stdout=json.dumps(cached_result, ensure_ascii=False, indent=2),
                    stderr=""
                )
                return script, fake, True

        # 真正执行
        script_path = Path(__file__).parent / f"{script}.py"
        result = subprocess.run(
            [sys.executable, str(script_path)] + extra_args + [novel_dir],
            capture_output=True, text=True, timeout=120
        )

        # 存缓存
        if conn and result.returncode == 0:
            for f in files:
                fh = _file_hash(f)
                try:
                    data = json.loads(result.stdout)
                    _set_cache(conn, script, f, fh, data)
                except (json.JSONDecodeError, Exception):
                    pass

        return script, result, False

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_one, s): s for s in scripts}
        for future in as_completed(futures):
            script, result, was_cached = future.result()
            results[script] = result
            if was_cached:
                cache_hits += 1
                print(f"  ⚡ {script} (缓存命中)")
            elif result.returncode == 0:
                print(f"  ✅ {script}")
            else:
                print(f"  ❌ {script} (exit {result.returncode})")

    if use_cache:
        print(f"\n📊 缓存: {cache_hits}/{total} 命中, {total - cache_hits} 重新计算")

    if conn:
        conn.close()

    return results

def clear_cache():
    """清除所有缓存"""
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("🗑️  缓存已清除")

def cache_stats():
    """显示缓存统计"""
    if not DB_PATH.exists():
        print("📭 无缓存")
        return
    conn = sqlite3.connect(str(DB_PATH))
    total = conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
    scripts = conn.execute("SELECT COUNT(DISTINCT script) FROM cache").fetchone()[0]
    size_mb = DB_PATH.stat().st_size / 1024 / 1024
    print(f"📊 缓存统计:")
    print(f"   脚本数: {scripts}")
    print(f"   缓存条目: {total}")
    print(f"   占用空间: {size_mb:.2f} MB")
    conn.close()

def main():
    if len(sys.argv) < 2:
        print("📖 Novel Writer 性能引擎")
        print("用法: run_parallel <小说目录> [选项]")
        print("  --workers N    并行数 (默认4)")
        print("  --no-cache     禁用缓存")
        print("  --scripts a,b  指定脚本")
        print("  --stats        缓存统计")
        print("  --clear        清除缓存")
        sys.exit(0)

    if sys.argv[1] == "--stats":
        cache_stats()
        return
    if sys.argv[1] == "--clear":
        clear_cache()
        return

    novel_dir = sys.argv[1]
    workers = 4
    use_cache = True
    scripts = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--workers" and i + 1 < len(args):
            workers = int(args[i + 1])
            i += 2
        elif args[i] == "--no-cache":
            use_cache = False
            i += 1
        elif args[i] == "--scripts" and i + 1 < len(args):
            scripts = args[i + 1].split(",")
            i += 2
        else:
            i += 1

    results = run_parallel_checks(novel_dir, scripts=scripts, workers=workers, use_cache=use_cache)

    # 输出汇总
    ok = sum(1 for r in results.values() if r.returncode == 0)
    print(f"\n🏁 完成: {ok}/{len(results)} 成功")

if __name__ == "__main__":
    main()
