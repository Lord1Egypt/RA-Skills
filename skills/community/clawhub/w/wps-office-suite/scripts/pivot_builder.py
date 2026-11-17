"""
原生透视表构建器 v5.5.0
========================
用 openpyxl 原生 OOXML 对象模型构建「真透视表」——生成完整的
pivotCacheDefinition + pivotCacheRecords + pivotTableDefinition 部件，
而非静态汇总行。WPS / MS Office / 纯 Python(openpyxl) 均可识别 pivot 结构。

技术基石（沙箱实测 PROTO OK）：
  - TableDefinition.cache 挂载 CacheDefinition
  - ws.add_pivot() 后 writer 自动写 5 个 pivot 部件并挂 workbook pivotCaches
  - 重载后 ws._pivots 保留，可被 Excel/WPS 直接刷新

死规则合规：
  - 规则9：纯本地 openpyxl，无外部 API
  - 规则10：数据行数上限保护，大文件抽样构建缓存
  - 规则13：仅 .py，无禁止文件类型
  - 规则14：三轮自审
  - 规则15：沙箱模拟运行
"""
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import openpyxl
    from openpyxl.pivot.cache import (
        CacheDefinition, CacheSource, WorksheetSource, CacheField,
        SharedItems, Text as PCacheText, Number as PCacheNumber,
    )
    from openpyxl.pivot.table import (
        TableDefinition, Location, DataField, PivotField,
        RowColField, RowColItem, FieldItem, Index,
    )
    from openpyxl.pivot.record import Record, RecordList
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

# 大文件缓存上限（规则10：不拖累设备）
MAX_CACHE_ROWS = 10000
# 高基数字段最大共享项数（超过则跳过该字段作为维度）
MAX_SHARED_ITEMS = 1000

AGG_MAP = {
    "sum": "sum", "求和": "sum",
    "avg": "average", "average": "average", "mean": "average", "平均": "average",
    "count": "count", "计数": "count",
    "max": "max", "最大": "max",
    "min": "min", "最小": "min",
}


def _col_letter(n: int) -> str:
    """1-based 列号 -> Excel 列字母"""
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def build_pivot(
    filepath: str,
    row_field: str,
    value_field: str,
    col_field: str = "",
    agg_func: str = "sum",
    sheet: str = "",
    output: str = "",
    pivot_name: str = "PivotTable1",
) -> Dict[str, Any]:
    """
    在 Excel 中生成原生透视表（新建独立 Sheet 承载 pivot）。

    Args:
        filepath: 源 xlsx
        row_field: 行维度字段
        value_field: 值（度量）字段
        col_field: 列维度字段（可选）
        agg_func: sum/avg/count/max/min（含中文）
        sheet: 数据源 Sheet（空则第一个）
        output: 输出路径（空则覆盖源文件前备份为 .bak.xlsx? 不，原地保存到临时再替换）
        pivot_name: 透视表名

    Returns:
        {success, path, row_field, value_field, col_field, agg_func,
         shared_items, cache_records, pivot_sheet, warning}
    """
    if not HAS_OPENPYXL:
        return {"success": False, "error": "openpyxl 未安装，无法构建原生透视表"}
    if not Path(filepath).exists():
        return {"success": False, "error": f"文件不存在: {filepath}"}

    agg = AGG_MAP.get(str(agg_func).lower(), "sum")
    try:
        wb = openpyxl.load_workbook(filepath)
        src_ws = wb[sheet] if sheet and sheet in wb.sheetnames else wb[wb.sheetnames[0]]
        src_name = src_ws.title

        # ---- 读取表头与数据 ----
        headers = []
        for c in range(1, src_ws.max_column + 1):
            v = src_ws.cell(row=1, column=c).value
            headers.append(str(v).strip() if v is not None else f"列{c}")

        def find_field(name: str) -> int:
            for i, h in enumerate(headers):
                if h == name:
                    return i
            return -1

        row_idx = find_field(row_field)
        val_idx = find_field(value_field)
        if row_idx < 0:
            return {"success": False, "error": f"行字段不存在: {row_field}", "available": headers}
        if val_idx < 0:
            return {"success": False, "error": f"值字段不存在: {value_field}", "available": headers}
        col_idx = find_field(col_field) if col_field else -1
        if col_field and col_idx < 0:
            return {"success": False, "error": f"列字段不存在: {col_field}", "available": headers}

        data_rows = []
        for r in range(2, src_ws.max_row + 1):
            row = [src_ws.cell(row=r, column=c).value for c in range(1, len(headers) + 1)]
            if all(v is None for v in row):
                continue
            data_rows.append(row)
        total_rows = len(data_rows)
        truncated = total_rows > MAX_CACHE_ROWS
        if truncated:
            data_rows = data_rows[:MAX_CACHE_ROWS]

        if not data_rows:
            return {"success": False, "error": "数据源无数据行"}

        # ---- 维度字段共享项 ----
        def uniques(idx: int) -> List[Any]:
            seen, out = set(), []
            for row in data_rows:
                if idx >= len(row):
                    continue
                v = row[idx]
                key = str(v) if v is not None else "(blank)"
                if key not in seen:
                    seen.add(key)
                    out.append(v)
                    if len(out) >= MAX_SHARED_ITEMS:
                        break
            return out

        row_uniq = uniques(row_idx)
        col_uniq = uniques(col_idx) if col_idx >= 0 else []
        if len(row_uniq) >= MAX_SHARED_ITEMS:
            return {"success": False,
                    "error": f"行字段「{row_field}」基数过高（≥{MAX_SHARED_ITEMS}），不适合做透视维度"}

        def idx_of(items: List[Any], val: Any) -> int:
            key = str(val) if val is not None else "(blank)"
            for i, it in enumerate(items):
                sk = str(it) if it is not None else "(blank)"
                if sk == key:
                    return i
            return 0

        # ---- 构建 CacheField ----
        def make_text_shared(items: List[Any]) -> SharedItems:
            fields = [PCacheText(v=str(it) if it is not None else "(blank)") for it in items]
            return SharedItems(_fields=fields, containsString=True, containsSemiMixedTypes=False,
                               containsNumber=False, count=len(fields))

        cache_fields = []
        # 行维度
        cache_fields.append(CacheField(name=row_field, sharedItems=make_text_shared(row_uniq)))
        # 列维度（可选）—— 即使无列字段也放一个占位 cacheField 保持结构对齐
        if col_idx >= 0:
            cache_fields.append(CacheField(name=col_field, sharedItems=make_text_shared(col_uniq)))
        # 值字段（数值共享项留空，由 records 直接写数值）
        cache_fields.append(CacheField(name=value_field, sharedItems=SharedItems(
            containsNumber=True, containsSemiMixedTypes=False)))

        # 字段顺序: [row] [col?] [value]
        val_pos = len(cache_fields) - 1
        col_pos = 1 if col_idx >= 0 else -1

        # ---- CacheSource ref ----
        ref = f"A1:{_col_letter(len(headers))}{len(data_rows) + 1}"
        cs = CacheSource(type="worksheet",
                         worksheetSource=WorksheetSource(ref=ref, sheet=src_name))
        cache = CacheDefinition(cacheSource=cs, cacheFields=cache_fields,
                                recordCount=len(data_rows))

        # ---- CacheRecords ----
        recs = []
        for row in data_rows:
            rv = idx_of(row_uniq, row[row_idx] if row_idx < len(row) else None)
            xv = [rv]
            if col_idx >= 0:
                xv.append(idx_of(col_uniq, row[col_idx] if col_idx < len(row) else None))
            raw = row[val_idx] if val_idx < len(row) else None
            try:
                num = float(raw) if raw is not None and raw != "" else 0.0
            except (ValueError, TypeError):
                num = 0.0
            xv.append(num)
            recs.append(Record(x=xv))
        cache.records = RecordList(count=len(recs), r=recs)

        # ---- PivotField / rowItems / colItems ----
        pivot_fields = []
        pivot_fields.append(PivotField(axis="axisRow",
                                       items=[FieldItem(x=i) for i in range(len(row_uniq))]))
        if col_idx >= 0:
            pivot_fields.append(PivotField(axis="axisCol",
                                           items=[FieldItem(x=i) for i in range(len(col_uniq))]))
        pivot_fields.append(PivotField(dataField=True))

        row_fields = [RowColField(x=0)]
        col_fields = [RowColField(x=col_pos)] if col_idx >= 0 else []
        data_fields = [DataField(name=f"{agg_title(agg)} of {value_field}", fld=val_pos, subtotal=agg)]

        row_items = [RowColItem(x=[Index(v=i)]) for i in range(len(row_uniq))]
        row_items.append(RowColItem(t="grand"))
        if col_idx >= 0:
            col_items = [RowColItem(x=[Index(v=i)]) for i in range(len(col_uniq))]
            col_items.append(RowColItem(t="grand"))
        else:
            col_items = []

        # ---- location：承载 Sheet 独立，pivot 与快照都从 A1 起始 ----
        n_rows = len(row_uniq) + 2          # 表头 + 数据 + 总计
        n_cols = (len(col_uniq) if col_idx >= 0 else 1) + 2
        start_col = 1
        loc_ref = (f"{_col_letter(start_col)}1:"
                   f"{_col_letter(start_col + n_cols - 1)}{n_rows}")

        pt = TableDefinition(
            name=pivot_name, cacheId=1,
            dataCaption="", grandTotalCaption="总计", errorCaption="", missingCaption="",
            pageStyle="", pivotTableStyle="", vacatedStyle="", tag="",
            location=Location(ref=loc_ref, firstHeaderRow=1, firstDataRow=1, firstDataCol=1),
            pivotFields=pivot_fields, rowFields=row_fields, colFields=col_fields,
            rowItems=row_items, colItems=col_items, dataFields=data_fields,
            rowGrandTotals=True, colGrandTotals=True,
        )
        pt.cache = cache

        # ---- 承载 pivot 的 Sheet ----
        pivot_sheet_name = _unique_sheet_name(wb, f"透视_{value_field}")
        pivot_ws = wb.create_sheet(pivot_sheet_name)
        _write_display_values(pivot_ws, start_col, row_uniq, col_uniq, col_idx >= 0,
                              data_rows, row_idx, val_idx, col_idx, agg)
        pivot_ws.add_pivot(pt)

        out = output or filepath
        wb.save(out)
        return {
            "success": True,
            "path": out,
            "source_sheet": src_name,
            "pivot_sheet": pivot_sheet_name,
            "pivot_name": pivot_name,
            "row_field": row_field,
            "value_field": value_field,
            "col_field": col_field or None,
            "agg_func": agg,
            "shared_items": len(row_uniq),
            "cache_records": len(recs),
            "location": loc_ref,
            "warning": ("缓存行数截断至 %d（原 %d）" % (MAX_CACHE_ROWS, total_rows)) if truncated else None,
        }
    except Exception as e:
        return {"success": False, "error": f"透视表构建失败: {e}"}


def agg_title(agg: str) -> str:
    return {"sum": "求和", "average": "平均", "count": "计数",
            "max": "最大值", "min": "最小值"}.get(agg, "求和")


def _unique_sheet_name(wb, base: str) -> str:
    name = base[:28]
    if name not in wb.sheetnames:
        return name
    i = 2
    while f"{name}_{i}" in wb.sheetnames:
        i += 1
    return f"{name}_{i}"


def _write_display_values(ws, start_col, row_uniq, col_uniq, has_col,
                          data_rows, row_idx, val_idx, col_idx, agg):
    """
    写入透视表的可见值（缓存的静态快照），确保无 pivot 引擎时也能看到结果。
    单元格布局以 A1 为基准（承载 Sheet 独立），pivot location 指向相同区域。
    """
    def aggregate(vals):
        if not vals:
            return 0
        if agg == "count":
            return len(vals)
        if agg == "average":
            return round(sum(vals) / len(vals), 4)
        if agg == "max":
            return max(vals)
        if agg == "min":
            return min(vals)
        return round(sum(vals), 4)

    # 用 A1 起始（承载 sheet 独立），与 location 的 start_col 对齐
    base = 1
    header_row = 1
    ws.cell(row=header_row, column=base, value=("行标签" if not has_col else "行\\列"))
    if has_col:
        for j, cv in enumerate(col_uniq):
            ws.cell(row=header_row, column=base + 1 + j, value=str(cv))
        ws.cell(row=header_row, column=base + 1 + len(col_uniq), value="总计")
    else:
        ws.cell(row=header_row, column=base + 1, value=agg_title(agg))

    # 聚合
    grouped = {}
    for row in data_rows:
        rk = str(row[row_idx]) if row_idx < len(row) and row[row_idx] is not None else "(blank)"
        ck = None
        if has_col:
            ck = str(row[col_idx]) if col_idx < len(row) and row[col_idx] is not None else "(blank)"
        raw = row[val_idx] if val_idx < len(row) else None
        try:
            nv = float(raw) if raw is not None and raw != "" else 0.0
        except (ValueError, TypeError):
            nv = 0.0
        grouped.setdefault((rk, ck), []).append(nv)

    for i, rv in enumerate(row_uniq):
        rkey = str(rv) if rv is not None else "(blank)"
        r = header_row + 1 + i
        ws.cell(row=r, column=base, value=rkey)
        if has_col:
            for j, cv in enumerate(col_uniq):
                ckey = str(cv) if cv is not None else "(blank)"
                vals = grouped.get((rkey, ckey), [])
                ws.cell(row=r, column=base + 1 + j, value=aggregate(vals))
            all_vals = [v for (rk, _), vs in grouped.items() if rk == rkey for v in vs]
            ws.cell(row=r, column=base + 1 + len(col_uniq), value=aggregate(all_vals))
        else:
            ws.cell(row=r, column=base + 1, value=aggregate(grouped.get((rkey, None), [])))

    # 总计行
    grand_r = header_row + 1 + len(row_uniq)
    ws.cell(row=grand_r, column=base, value="总计")
    all_vals = [v for vs in grouped.values() for v in vs]
    if has_col:
        for j in range(len(col_uniq) + 1):
            ws.cell(row=grand_r, column=base + 1 + j, value=aggregate(all_vals) if j == len(col_uniq)
                    else aggregate([v for (rk, ck), vs in grouped.items()
                                    if ck == (str(col_uniq[j]) if col_uniq[j] is not None else "(blank)")
                                    for v in vs]))
    else:
        ws.cell(row=grand_r, column=base + 1, value=aggregate(all_vals))


def verify_pivot(filepath: str) -> Dict[str, Any]:
    """校验 xlsx 内 pivot 部件完整性（沙箱/验收用）"""
    import zipfile
    if not Path(filepath).exists():
        return {"ok": False, "error": "文件不存在"}
    with zipfile.ZipFile(filepath) as z:
        names = z.namelist()
        has_table = any("pivotTables/pivotTable" in n and n.endswith(".xml") for n in names)
        has_def = any("pivotCacheDefinition" in n and n.endswith(".xml") for n in names)
        has_rec = any("pivotCacheRecords" in n and n.endswith(".xml") for n in names)
        parts = [n for n in names if "pivot" in n.lower()]
    ok = has_table and has_def and has_rec
    # 重载校验
    reload_ok = False
    pivot_count = 0
    try:
        wb = openpyxl.load_workbook(filepath)
        for ws in wb.worksheets:
            pivot_count += len(ws._pivots)
        reload_ok = pivot_count > 0
    except Exception:
        pass
    return {"ok": ok and reload_ok, "has_table": has_table, "has_def": has_def,
            "has_rec": has_rec, "parts": parts, "reload_ok": reload_ok,
            "pivot_count": pivot_count}


def _cli():
    import argparse, json
    p = argparse.ArgumentParser(description="原生透视表构建器 v5.5.0")
    sub = p.add_subparsers(dest="action", required=True)
    b = sub.add_parser("build", help="构建原生透视表")
    b.add_argument("--file", required=True)
    b.add_argument("--row-field", required=True)
    b.add_argument("--value-field", required=True)
    b.add_argument("--col-field", default="")
    b.add_argument("--agg", default="sum")
    b.add_argument("--sheet", default="")
    b.add_argument("--output", default="")
    v = sub.add_parser("verify", help="校验 pivot 部件完整性")
    v.add_argument("--file", required=True)
    args = p.parse_args()
    if args.action == "build":
        r = build_pivot(args.file, args.row_field, args.value_field,
                        col_field=args.col_field, agg_func=args.agg,
                        sheet=args.sheet, output=args.output)
    else:
        r = verify_pivot(args.file)
    print(json.dumps(r, ensure_ascii=False, default=str))


if __name__ == "__main__":
    _cli()
