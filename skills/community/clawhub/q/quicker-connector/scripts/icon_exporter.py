#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker 动作图标批量导出器：把每个动作的图标导出为独立的 PNG 文件。

设计要点（比逐条 resolve() 快得多）：
1. **去重**：先按「图标」列的取值去重，同一个图标只解析/渲染/下载一次，
   再用 shutil.copyfile 复制到每个动作对应的文件名（不用硬链接，跨盘安全）。
2. **本地缓存优先**：走到 IconResolver.try_local() 的取值不进线程池（磁盘 IO 很快且无网络）。
3. **真并发**：只有需要联网下载或需要栅格化渲染的取值才进 ThreadPoolExecutor。
4. **容错**：单个图标失败只记录统计，不影响整体导出。

输出：
- 每个动作一个 PNG：`<三位序号>_<动作名安全化>_<图标短key>.png`
- `icons_manifest.json`：`[{id, name, icon, icon_file, source, ok}, ...]`

用法：
    python scripts/icon_exporter.py --out <目录> [--size 48] [--workers 8]
    python scripts/icon_exporter.py --out icons --no-manifest
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from icon_resolver import (  # noqa: E402
    IconResolver,
    KIND_FA_CACHE,
    KIND_FA_RENDER,
    KIND_LOCAL_FILE,
    KIND_MISS,
    KIND_URL_CACHE,
    KIND_URL_DOWNLOAD,
)

MANIFEST_NAME = "icons_manifest.json"
DEFAULT_SIZE = 48
DEFAULT_MAX_WORKERS = 8
MAX_NAME_LEN = 40
MAX_KEY_LEN = 24

_INVALID_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_BLANKS = re.compile(r"\s+")
_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
}


def validate_icon_size(size: Any) -> int:
    """
    校验图标像素尺寸（导出入口统一使用）。

    Args:
        size: 期望的图标边长（像素）

    Returns:
        校验通过的 int 尺寸（>= 1）

    Raises:
        ValueError: 不是整数、或小于 1 时（避免静默产出 0 个图标）
    """
    if isinstance(size, bool) or (isinstance(size, float) and not float(size).is_integer()):
        raise ValueError(f"size 必须是整数，当前为 {size!r}")
    try:
        value = int(size)
    except (TypeError, ValueError):
        raise ValueError(f"size 必须是整数，当前为 {size!r}")
    if value < 1:
        raise ValueError(f"size 必须 >= 1，当前为 {value}")
    return value


def sanitize_file_part(value: str, max_len: int = MAX_NAME_LEN) -> str:
    """
    把任意文本转成可用于 Windows 文件名的安全字段。

    Args:
        value: 原始文本（动作名 / 图标 key）
        max_len: 最大字符数（按字符截断，超出后丢尾）

    Returns:
        安全的文件名字段（不为空）
    """
    s = _INVALID_CHARS.sub("_", value or "")
    s = _BLANKS.sub("_", s)
    s = s.strip(" ._").replace("..", ".")
    if not s:
        s = "unnamed"
    if s.upper() in _RESERVED_NAMES:
        s = "_" + s
    return s[:max_len] if len(s) > max_len else s


def icon_short_key(icon_value: str, max_len: int = MAX_KEY_LEN) -> str:
    """
    由图标取值生成短 key（用于文件名后缀，便于肉眼区分图标来源）。

    Args:
        icon_value: CSV「图标」列的取值
        max_len: 最大字符数

    Returns:
        短 key，如 `Solid_Search` / `a91f3c.png` / `none`
    """
    v = (icon_value or "").strip()
    if not v:
        return "none"
    low = v.lower()
    if low.startswith("fa:"):
        return sanitize_file_part(v[3:], max_len)
    if low.startswith(("http://", "https://")):
        tail = v.split("?")[0].rstrip("/").rsplit("/", 1)[-1]
        return sanitize_file_part(tail or "url", max_len)
    return sanitize_file_part(Path(v).stem or v, max_len)


def build_icon_filename(index: int, action_name: str, icon_value: str) -> str:
    """
    生成图标文件名：`<三位序号>_<动作名安全化>_<图标短key>.png`

    Args:
        index: 动作序号（从 1 开始）
        action_name: 动作名称
        icon_value: 图标取值

    Returns:
        PNG 文件名
    """
    return f"{index:03d}_{sanitize_file_part(action_name)}_{icon_short_key(icon_value)}.png"


def export_icons(
    actions: Iterable,
    out_dir: str,
    size: int = DEFAULT_SIZE,
    max_workers: int = DEFAULT_MAX_WORKERS,
    manifest: bool = True,
    resolver: Optional[IconResolver] = None,
    log: Callable[[str], None] = print,
) -> Dict[str, Any]:
    """
    批量导出动作图标为独立 PNG 文件。

    Args:
        actions: QuickerAction 可迭代对象（需有 id/name/icon 属性）
        out_dir: 图标输出目录（不存在会创建）
        size: 图标像素尺寸
        max_workers: 并发线程数
        manifest: 是否写出 icons_manifest.json
        resolver: 复用的图标解析器（None 时内部创建）
        log: 日志回调

    Returns:
        统计 dict：
        {
          "total", "unique", "files", "from_cache", "downloaded", "rendered",
          "local", "missing", "elapsed_sec", "out_dir", "resolver_stats", "items"
        }
        其中 items 为每个动作的明细行（顺序与 actions 一致）：
        [{"id","name","icon","icon_file","source","ok"}, ...]

    Raises:
        ValueError: size 不是 >= 1 的整数
    """
    size = validate_icon_size(size)
    t0 = time.perf_counter()
    actions = list(actions)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if resolver is None:
        resolver = IconResolver(size=size, max_workers=max_workers)

    # 1) 取值整理：去重后统计，但整份列表交给 resolve_many（内部去重 + 计数 reused）
    all_values = [(getattr(a, "icon", "") or "").strip() for a in actions]
    unique_values = list(dict.fromkeys(all_values))

    # 2) 批量解析（本地缓存命中不进线程池，下载/渲染才并发）
    resolved = resolver.resolve_many(all_values, max_workers=max_workers)

    # 3) 统计来源（按唯一取值计数）
    counters = {"from_cache": 0, "downloaded": 0, "rendered": 0, "local": 0, "missing": 0}
    for key in unique_values:
        if not resolved.get(key):
            counters["missing"] += 1
            continue
        kind = resolver.kind_of(key) or KIND_MISS
        if kind in (KIND_URL_CACHE, KIND_FA_CACHE):
            counters["from_cache"] += 1
        elif kind == KIND_URL_DOWNLOAD:
            counters["downloaded"] += 1
        elif kind == KIND_FA_RENDER:
            counters["rendered"] += 1
        elif kind == KIND_LOCAL_FILE:
            counters["local"] += 1

    # 4) 逐动作落盘（同源图标直接文件复制）
    items: List[Dict[str, Any]] = []
    n_files = 0
    for idx, action in enumerate(actions, start=1):
        raw_icon = getattr(action, "icon", "") or ""
        key = raw_icon.strip()
        src = resolved.get(key)
        fname: Optional[str] = None

        if src and Path(src).exists():
            fname = build_icon_filename(idx, getattr(action, "name", "") or "", raw_icon)
            dst = out / fname
            try:
                shutil.copyfile(src, dst)
            except Exception as e:  # 单个文件失败不影响整体
                log(f"图标落盘失败 [{getattr(action, 'name', '')}]: {e}")
                fname = None

        ok = bool(fname)
        if ok:
            n_files += 1
        items.append({
            "id": getattr(action, "id", ""),
            "name": getattr(action, "name", ""),
            "icon": raw_icon,
            "icon_file": fname,
            "source": resolver.kind_of(key) or (KIND_MISS if not ok else KIND_LOCAL_FILE),
            "ok": ok,
        })

    if manifest:
        manifest_path = out / MANIFEST_NAME
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    return {
        "total": len(actions),
        "unique": len(unique_values),
        "files": n_files,
        "from_cache": counters["from_cache"],
        "downloaded": counters["downloaded"],
        "rendered": counters["rendered"],
        "local": counters["local"],
        "missing": counters["missing"],
        "elapsed_sec": round(time.perf_counter() - t0, 3),
        "out_dir": str(out.resolve()),
        "resolver_stats": dict(resolver.stats),
        "items": items,
    }


def print_stats(stats: Dict[str, Any]) -> None:
    """打印导出统计（人类可读）"""
    print("图标导出完成：")
    print(f"  动作总数     {stats['total']}")
    print(f"  唯一图标     {stats['unique']}")
    print(f"  导出文件数   {stats['files']}")
    print(f"  命中缓存     {stats['from_cache']}")
    print(f"  联网下载     {stats['downloaded']}")
    print(f"  本地渲染     {stats['rendered']}")
    print(f"  本地图片路径 {stats['local']}")
    print(f"  无法解析     {stats['missing']}")
    print(f"  耗时         {stats['elapsed_sec']} 秒")
    print(f"  输出目录     {stats['out_dir']}")
    print(f"  解析器统计   {stats['resolver_stats']}")


def _load_actions(csv_path: Optional[str] = None) -> List[Any]:
    """从 CSV（或 config.json 的 csv_path / 默认路径）读取动作列表"""
    from quicker_connector import QuickerConnector, DEFAULT_CSV_PATH, CONFIG_FILE

    if not csv_path and Path(CONFIG_FILE).exists():
        try:
            cfg = json.loads(Path(CONFIG_FILE).read_text(encoding="utf-8"))
            csv_path = cfg.get("csv_path") or None
        except Exception:
            csv_path = None
    csv_path = csv_path or DEFAULT_CSV_PATH

    connector = QuickerConnector(source="csv", csv_path=csv_path)
    return connector.read_actions()


def main() -> None:
    ap = argparse.ArgumentParser(description="批量导出 Quicker 动作图标为独立 PNG 文件")
    ap.add_argument("--out", "-o", required=True, help="图标输出目录")
    ap.add_argument("--csv", default=None, help="动作 CSV 路径（默认读 config.json）")
    ap.add_argument("--size", type=int, default=DEFAULT_SIZE, help=f"图标像素尺寸，默认 {DEFAULT_SIZE}")
    ap.add_argument("--workers", type=int, default=DEFAULT_MAX_WORKERS, help=f"并发线程数，默认 {DEFAULT_MAX_WORKERS}")
    ap.add_argument("--no-manifest", action="store_true", help="不生成 icons_manifest.json")
    args = ap.parse_args()

    try:
        size = validate_icon_size(args.size)
    except ValueError as e:
        print(f"参数错误：{e}")
        sys.exit(2)

    actions = _load_actions(args.csv)
    print(f"读取动作 {len(actions)} 个，开始导出图标 ...")

    stats = export_icons(
        actions,
        args.out,
        size=size,
        max_workers=args.workers,
        manifest=not args.no_manifest,
        log=lambda m: print("  ", m),
    )
    print_stats(stats)


if __name__ == "__main__":
    main()
