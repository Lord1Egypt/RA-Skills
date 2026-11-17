#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出 Quicker 动作列表到 Excel（.xlsx），「图标」列支持三种处理方式。

图标模式（--icon-mode / icon_mode）：
- embedded（默认）：「图标」列嵌入真实 PNG 图片（与 1.4.0 行为一致）
- path：         「图标」列只写图标文件的相对路径（配合 --icons-dir，Excel 极小、生成极快）
- none：         不处理图标

图标去重：
- 图标取值先去重，同一个图标只解析/渲染/下载一次
- embedded 模式下同一 PNG 仍会按行写出多个相同媒体，保存后会统一压缩为一份
  （相同内容的 xl/media/* 只保留一份并复用，见 `_dedupe_media`）

用法：
    python scripts/export_actions_excel.py                     # 使用 config.json 的 CSV
    python scripts/export_actions_excel.py -o 动作清单.xlsx
    python scripts/export_actions_excel.py -o out.xlsx --icon-mode embedded --icons-dir out_icons
    python scripts/export_actions_excel.py -o out.xlsx --icon-mode path  --icons-dir out_icons
    python scripts/export_actions_excel.py -o out.xlsx --icons-only --icons-dir out_icons
    python scripts/export_actions_excel.py --no-icons           # 不处理图标

依赖：openpyxl、Pillow（图标需要 Pillow）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.drawing.image import Image as XLImage
except ImportError:
    print("缺少依赖，请先安装：pip install openpyxl pillow")
    sys.exit(1)

from icon_exporter import export_icons, validate_icon_size  # noqa: E402
from icon_resolver import IconResolver  # noqa: E402

COLUMNS = [
    ("图标", 7),
    ("名称", 26),
    ("说明", 52),
    ("类型", 12),
    ("动作页", 16),
    ("EXE", 18),
    ("关联Exe", 14),
    ("位置", 9),
    ("大小", 8),
    ("创建或安装时间", 19),
    ("最后更新", 19),
    ("Uri", 42),
    ("来源动作", 42),
    ("图标定义", 34),
]

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
BAND_FILL = PatternFill("solid", fgColor="F2F7FB")

ICON_MODE_EMBEDDED = "embedded"
ICON_MODE_PATH = "path"
ICON_MODE_NONE = "none"
VALID_ICON_MODES = (ICON_MODE_EMBEDDED, ICON_MODE_PATH, ICON_MODE_NONE)

DEFAULT_ICON_SIZE = 48
DEFAULT_MAX_WORKERS = 8

_REL_TAG_RE = re.compile(r"<Relationship\b[^>]*?/>", re.S)
_REL_ID_RE = re.compile(r'Id="([^"]+)"')
_REL_TARGET_RE = re.compile(r'Target="([^"]+)"')
_EMBED_RE = re.compile(r'r:embed="([^"]+)"')


def _rel_icon_path(icon_file: str, base_dir: str) -> str:
    """
    把图标文件绝对路径转成相对 Excel 所在目录的路径。

    Args:
        icon_file: 图标文件绝对路径
        base_dir: Excel 文件所在目录

    Returns:
        相对路径字符串（跨盘时退回绝对路径）
    """
    try:
        rel = os.path.relpath(icon_file, base_dir)
    except ValueError:  # Windows 下跨盘无法计算相对路径
        return icon_file
    return rel


def _normalize_part_path(target: str, base: str = "xl/drawings") -> str:
    """把 drawing rels 里的相对 Target 规范化为包内绝对路径"""
    target = target.replace("\\", "/")
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(base, target))


def _check_media_refs(xlsx_path: str) -> List[str]:
    """
    校验 xlsx 包内 media 引用完整性。

    Args:
        xlsx_path: xlsx 文件路径

    Returns:
        错误列表（为空表示校验通过）
    """
    errors: List[str] = []
    with zipfile.ZipFile(xlsx_path) as z:
        names = set(z.namelist())
        for rels_name in [n for n in names if n.startswith("xl/drawings/_rels/") and n.endswith(".rels")]:
            drawing_name = posixpath.join("xl/drawings", Path(rels_name).name[: -len(".rels")])
            rels_text = z.read(rels_name).decode("utf-8", "replace")
            rid_set = set()
            for tag in _REL_TAG_RE.findall(rels_text):
                rid = _REL_ID_RE.search(tag)
                tgt = _REL_TARGET_RE.search(tag)
                if rid:
                    rid_set.add(rid.group(1))
                if tgt and "media/" in tgt.group(1):
                    full = _normalize_part_path(tgt.group(1), posixpath.dirname(rels_name))
                    if full not in names:
                        errors.append(f"{rels_name}: 目标部件缺失 {full}")
            if drawing_name in names:
                drawing_text = z.read(drawing_name).decode("utf-8", "replace")
                for rid in _EMBED_RE.findall(drawing_text):
                    if rid not in rid_set:
                        errors.append(f"{drawing_name}: r:embed={rid} 未定义")
    return errors


def _dedupe_media(xlsx_path: str, expect_images: Optional[int] = None) -> Dict[str, int]:
    """
    压缩 xlsx 内重复的图标媒体。

    openpyxl 每行一个 Image 对象时，同一个 PNG 会被写出成多份完全相同的 xl/media/*。
    这里按内容 SHA1 去重：重复媒体的 drawing 关系 Target 改指向保留的那一份，
    并从包中删除冗余部件。关系 ID 与 drawing XML 的锚点均保持不变，
    因此每张图片的行锚定不受影响。

    Args:
        xlsx_path: 已保存的 xlsx 文件路径
        expect_images: 预期的图片数量（给出时会校验去重后仍能被 openpyxl 读回同样数量）

    Returns:
        {"before": 去重前媒体数, "after": 去重后媒体数, "saved_bytes": 释放的未压缩字节数}

    Raises:
        ValueError: 校验失败（此时原文件保持不变）
    """
    src = Path(xlsx_path)
    with zipfile.ZipFile(src) as zin:
        infos = zin.infolist()
        names = [i.filename for i in infos]
        medias = [n for n in names if n.startswith("xl/media/")]
        if len(medias) < 2:
            return {"before": len(medias), "after": len(medias), "saved_bytes": 0}

        canonical: Dict[str, str] = {}
        digests: Dict[str, str] = {}
        for n in medias:
            digest = hashlib.sha1(zin.read(n)).hexdigest()
            canonical[n] = digests.setdefault(digest, n)
        drop = {n for n in medias if canonical[n] != n}
        if not drop:
            return {"before": len(medias), "after": len(medias), "saved_bytes": 0}

        rels_names = [n for n in names if n.startswith("xl/drawings/_rels/") and n.endswith(".rels")]
        if not rels_names:
            raise ValueError("未找到 drawing 关系部件，跳过媒体去重")

        new_rels: Dict[str, bytes] = {}
        for rels_name in rels_names:
            part_dir = posixpath.dirname(rels_name)
            rels_text = zin.read(rels_name).decode("utf-8")
            for tag in _REL_TAG_RE.findall(rels_text):
                tgt = _REL_TARGET_RE.search(tag)
                if not tgt:
                    continue
                raw_target = tgt.group(1)
                full = _normalize_part_path(raw_target, part_dir)
                canon_full = canonical.get(full)
                if not canon_full or canon_full == full:
                    continue
                if raw_target.startswith("/"):
                    # 保持 openpyxl 的写法：包内绝对路径（openpyxl 读回时按此解析）
                    new_target = "/" + canon_full
                else:
                    new_target = posixpath.relpath(canon_full, part_dir)
                rels_text = rels_text.replace(tag, tag.replace(f'Target="{raw_target}"', f'Target="{new_target}"'))
            new_rels[rels_name] = rels_text.encode("utf-8")

        saved = 0
        tmp_path = src.with_name(src.stem + ".dedupe" + src.suffix)
        with zipfile.ZipFile(tmp_path, "w") as zout:
            for item in infos:
                if item.filename in drop:
                    saved += item.file_size
                    continue
                data = new_rels.get(item.filename)
                if data is None:
                    data = zin.read(item.filename)
                zout.writestr(item, data)

    errors = _check_media_refs(str(tmp_path))
    if errors:
        os.remove(tmp_path)
        raise ValueError("媒体去重后校验失败: " + "; ".join(errors[:5]))

    # 真实读回校验：确保 openpyxl（也代表主流解析器）仍能打开且图片数量不变
    try:
        wb = load_workbook(tmp_path)
    except Exception as e:
        os.remove(tmp_path)
        raise ValueError(f"去重后无法被 openpyxl 打开: {e}")
    n_reloaded = sum(len(ws._images) for ws in wb.worksheets)
    wb.close()
    if expect_images is not None and n_reloaded != expect_images:
        os.remove(tmp_path)
        raise ValueError(f"去重后图片数量异常: {n_reloaded} != {expect_images}")

    os.replace(tmp_path, src)
    return {
        "before": len(medias),
        "after": len(medias) - len(drop),
        "saved_bytes": saved,
    }


def _save_workbook(wb, out: Path) -> None:
    """
    保存工作簿：先写同目录临时文件、校验成功后再原子替换。

    好处：目标文件被其它程序独占（如 Excel 打开着）时，不会破坏原文件、
    也不会留下写了一半的半成品；失败时清理临时文件。

    Args:
        wb: openpyxl Workbook
        out: 目标 xlsx 路径

    Raises:
        PermissionError: 目标文件被占用或目录不可写（消息含处理建议）
    """
    tmp = out.with_name(out.name + ".part")

    def _cleanup() -> None:
        try:
            if tmp.exists():
                os.remove(tmp)
        except OSError:
            pass

    try:
        wb.save(tmp)
    except PermissionError as e:
        _cleanup()
        raise PermissionError(f"无法写入临时文件：{tmp}，请检查目录权限或关闭占用该目录的程序") from e
    except Exception:
        _cleanup()
        raise

    try:
        os.replace(tmp, out)
    except PermissionError as e:
        _cleanup()
        raise PermissionError(
            f"目标文件被占用，无法写入：{out}，请关闭正在打开它的程序（如 Excel）后重试"
        ) from e
    except Exception:
        _cleanup()
        raise


def export_actions_to_excel(
    actions: Iterable,
    output_path: str,
    icon_size: int = DEFAULT_ICON_SIZE,
    with_icons: bool = True,
    resolver: Optional[IconResolver] = None,
    log=print,
    icon_mode: str = ICON_MODE_EMBEDDED,
    icons_dir: Optional[str] = None,
    max_workers: int = DEFAULT_MAX_WORKERS,
    dedupe_media: bool = True,
) -> Dict[str, Any]:
    """
    把动作列表写成 Excel。

    Args:
        actions: QuickerAction 可迭代对象（需有 name/description/icon/... 属性）
        output_path: 输出 .xlsx 路径
        icon_size: 图标像素尺寸
        with_icons: 总开关，False 等价于 icon_mode="none"（向后兼容）
        resolver: 图标解析器（None 时自动创建）
        log: 日志回调
        icon_mode: embedded（嵌图） / path（只写路径） / none（不处理）
        icons_dir: 图标文件目录；给出时会先用 export_icons() 批量导出，再生成 Excel
        max_workers: 图标解析并发线程数
        dedupe_media: embedded 模式下是否压缩重复图片媒体

    Returns:
        统计 dict：
        {"total","with_icon","no_icon","output","icon_mode","output_size"}
        + 可选 "resolver_stats" / "icons_dir" / "icon_files" / "media_before" / "media_after"

    Raises:
        ValueError: icon_mode 非法或 icon_size < 1
        PermissionError: 目标文件被占用（原文件不会被破坏）
    """
    actions = list(actions)
    icon_size = validate_icon_size(icon_size)
    mode = (icon_mode or ICON_MODE_EMBEDDED).lower()
    if mode not in VALID_ICON_MODES:
        raise ValueError(f"不支持的 icon_mode: {icon_mode}，可选 {VALID_ICON_MODES}")
    if not with_icons:
        mode = ICON_MODE_NONE

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # ---------- 1) 图标准备（去重 + 并发解析） ----------
    icon_files: Dict[int, str] = {}      # 行索引 -> 图标 PNG 绝对路径
    icons_export_stats: Optional[Dict[str, Any]] = None
    if mode != ICON_MODE_NONE:
        if icons_dir:
            icons_export_stats = export_icons(
                actions, icons_dir,
                size=icon_size, max_workers=max_workers, log=log,
            )
            icons_root = Path(icons_dir)
            for i, item in enumerate(icons_export_stats["items"]):
                if item.get("icon_file"):
                    icon_files[i] = str(icons_root / item["icon_file"])
        else:
            if resolver is None:
                resolver = IconResolver(size=icon_size, max_workers=max_workers)
            values = [(getattr(a, "icon", "") or "").strip() for a in actions]
            resolved = resolver.resolve_many(values, max_workers=max_workers)
            for i, v in enumerate(values):
                if resolved.get(v):
                    icon_files[i] = resolved[v]

    # ---------- 2) 表格搭建 ----------
    wb = Workbook()
    ws = wb.active
    ws.title = "动作列表"

    columns = list(COLUMNS)
    if mode == ICON_MODE_PATH:
        columns[0] = ("图标文件", 46)

    for col, (title, width) in enumerate(columns, start=1):
        c = ws.cell(row=1, column=col, value=title)
        c.fill = HEADER_FILL
        c.font = HEADER_FONT
        c.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[get_column_letter(col)].width = width
    ws.row_dimensions[1].height = 24
    ws.freeze_panes = "C2"

    wrap = Alignment(vertical="top", wrap_text=True)
    top = Alignment(vertical="center")

    n_with_icon = 0
    row = 2
    for idx, a in enumerate(actions):
        band = BAND_FILL if idx % 2 else None
        icon_cell = ""
        if mode == ICON_MODE_PATH:
            icon_file = icon_files.get(idx)
            if icon_file:
                icon_cell = _rel_icon_path(icon_file, str(out.parent))

        values = [
            icon_cell,              # 图标列（图片或文件路径）
            a.name,
            a.description,
            a.action_type,
            a.panel,
            a.exe,
            a.associated_exe,
            a.position,
            a.size,
            a.create_time,
            a.update_time,
            a.uri,
            a.source,
            a.icon,
        ]
        for col, v in enumerate(values, start=1):
            c = ws.cell(row=row, column=col, value=v)
            c.alignment = wrap if col in (3, 12, 13) else top
            if band:
                c.fill = band

        if mode == ICON_MODE_EMBEDDED and idx in icon_files:
            try:
                # 注意：必须每行新建一个 Image 对象——openpyxl 保存时才读取 anchor，
                # 复用同一对象会让所有行都指向最后一次设置的 anchor。
                img = XLImage(icon_files[idx])
                ratio = img.height / img.width if img.width else 1.0
                img.width = icon_size
                img.height = max(int(icon_size * ratio), 1)
                img.anchor = f"A{row}"
                ws.add_image(img)
                n_with_icon += 1
            except Exception as e:
                log(f"嵌入图标失败 [{a.name}]: {e}")
        row += 1

    # 行高：容纳图标
    for r in range(2, row):
        ws.row_dimensions[r].height = icon_size * 0.78 + 4

    ws.auto_filter.ref = f"A1:{get_column_letter(len(columns))}{max(row - 1, 1)}"
    _save_workbook(wb, out)

    # ---------- 3) 图片媒体去重（保存后压缩完全相同的媒体） ----------
    media_info: Optional[Dict[str, int]] = None
    if mode == ICON_MODE_EMBEDDED and dedupe_media and n_with_icon > 1:
        try:
            media_info = _dedupe_media(str(out), expect_images=n_with_icon)
        except Exception as e:
            log(f"图片媒体去重失败（已保留原文件）: {e}")

    stats: Dict[str, Any] = {
        "total": len(actions),
        "with_icon": n_with_icon,
        "no_icon": len(actions) - n_with_icon,
        "output": str(out),
        "icon_mode": mode,
        "output_size": out.stat().st_size,
    }
    if mode == ICON_MODE_PATH:
        # path 模式「有图标」= 有对应图标文件的行数
        stats["with_icon"] = len(icon_files)
        stats["no_icon"] = len(actions) - len(icon_files)
    if icons_export_stats is not None:
        stats["icons_dir"] = icons_export_stats["out_dir"]
        stats["icon_files"] = icons_export_stats["files"]
        stats["icons_elapsed_sec"] = icons_export_stats["elapsed_sec"]
    if resolver is not None:
        stats["resolver_stats"] = dict(resolver.stats)
    if media_info is not None:
        stats["media_before"] = media_info["before"]
        stats["media_after"] = media_info["after"]
        stats["media_saved_bytes"] = media_info["saved_bytes"]
    return stats


def main() -> None:
    ap = argparse.ArgumentParser(description="导出 Quicker 动作列表到 Excel（含真实图标）")
    ap.add_argument("-o", "--output", default="quicker_actions.xlsx", help="输出 xlsx 路径")
    ap.add_argument("--csv", default=None, help="动作 CSV 路径（默认读 config.json）")
    ap.add_argument("--size", type=int, default=DEFAULT_ICON_SIZE, help=f"图标像素尺寸，默认 {DEFAULT_ICON_SIZE}")
    ap.add_argument("--no-icons", action="store_true", help="不处理图标")
    ap.add_argument("--icon-mode", choices=list(VALID_ICON_MODES), default=ICON_MODE_EMBEDDED,
                    help="embedded=嵌入图片（默认），path=只写图标文件路径，none=不处理")
    ap.add_argument("--icons-dir", default=None, help="图标文件导出目录（path/--icons-only 未指定时自动用 <输出同目录>/<输出名>_icons）")
    ap.add_argument("--icons-only", action="store_true", help="只导出图标文件，不生成 Excel")
    ap.add_argument("--no-dedupe", action="store_true", help="embedded 模式下不做图片媒体去重")
    ap.add_argument("--workers", type=int, default=DEFAULT_MAX_WORKERS, help=f"图标并发线程数，默认 {DEFAULT_MAX_WORKERS}")
    args = ap.parse_args()

    from quicker_connector import QuickerConnector, DEFAULT_CSV_PATH, CONFIG_FILE

    csv_path = args.csv
    if not csv_path and Path(CONFIG_FILE).exists():
        try:
            cfg = json.loads(Path(CONFIG_FILE).read_text(encoding="utf-8"))
            csv_path = cfg.get("csv_path") or None
        except Exception:
            pass
    csv_path = csv_path or DEFAULT_CSV_PATH

    connector = QuickerConnector(source="csv", csv_path=csv_path)
    actions = connector.read_actions()
    print(f"读取动作 {len(actions)} 个 ...")

    mode = ICON_MODE_NONE if args.no_icons else args.icon_mode
    out = Path(args.output)
    # 默认 embedded 与旧版一致：不额外产出图标目录；path / --icons-only 才自动派生
    icons_dir = args.icons_dir
    if not icons_dir and (args.icons_only or mode == ICON_MODE_PATH):
        icons_dir = str(out.parent / (out.stem + "_icons"))

    try:
        size = validate_icon_size(args.size)
    except ValueError as e:
        print(f"参数错误：{e}")
        sys.exit(2)

    try:
        if args.icons_only:
            from icon_exporter import print_stats as _print_icon_stats
            print(f"仅导出图标到 {icons_dir} ...")
            _print_icon_stats(
                export_icons(actions, icons_dir, size=size, max_workers=args.workers,
                             log=lambda m: print("  ", m))
            )
            return

        stats = export_actions_to_excel(
            actions,
            args.output,
            icon_size=size,
            with_icons=not args.no_icons,
            icon_mode=mode,
            icons_dir=icons_dir,
            max_workers=args.workers,
            dedupe_media=not args.no_dedupe,
            log=lambda m: print("  ", m),
        )
    except ValueError as e:
        print(f"参数错误：{e}")
        sys.exit(2)
    except PermissionError as e:
        print(f"写入失败：{e}")
        sys.exit(2)

    print(f"完成：{stats['output']}  ({stats['output_size'] / 1024:.1f} KB)")
    print(f"  动作总数 {stats['total']}，有图标 {stats['with_icon']}，无图标 {stats['no_icon']}，模式 {stats['icon_mode']}")
    if "icons_dir" in stats:
        print(f"  图标目录 {stats['icons_dir']}（文件 {stats['icon_files']} 个，导出耗时 {stats['icons_elapsed_sec']} 秒）")
    if "media_after" in stats:
        print(f"  图片媒体 {stats['media_before']} → {stats['media_after']}（节省 {stats['media_saved_bytes'] / 1024:.1f} KB）")
    if "resolver_stats" in stats:
        print(f"  图标解析：{stats['resolver_stats']}")


if __name__ == "__main__":
    main()
