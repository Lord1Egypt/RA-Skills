"""
WPS Worker v2.1 - 三引擎自动切换
WPS > MS Office > Pure Python

新增：目录生成 / 环境自检 / 反馈入口
"""
import sys
import json
import traceback
from pathlib import Path

from wps_common import (
    detect_engine, get_engine, get_wps, get_ms_word,
    safe_path, ensure_desktop_path, release_wps, release_ms, with_retry
)
from wps_pure import (
    pure_create_word, pure_edit_word, pure_info_word,
    pure_create_excel, pure_input_excel, pure_info_excel,
    pure_create_ppt, pure_info_ppt
)

# MS Office 兼容层
wps_ms = None

def get_ms_module():
    global wps_ms
    if wps_ms is None:
        import wps_ms as m
        wps_ms = m
    return wps_ms


# ==================== Word ====================

def cmd_create_word(args):
    engine = get_engine()
    title = args.get("title", "新建文档")
    
    if engine == "WPS":
        wps = get_wps()
        doc = wps.Documents.Add()
        if title:
            para = doc.Paragraphs.Add()
            para.Range.Text = title
            para.Range.Font.Size = 16
            para.Range.Font.Bold = True
            para.Range.ParagraphFormat.Alignment = 1
        filepath = ensure_desktop_path(f"{title}.docx")
        doc.SaveAs(filepath)
        doc.Close()
        release_wps()
        return {"success": True, "path": filepath, "engine": "WPS"}

    elif engine == "MSOFFICE":
        ms = get_ms_module()
        filepath = ensure_desktop_path(f"{title}.docx")
        result = ms.ms_create_word(title, filepath)
        release_ms()
        return {**result, "engine": "MSOFFICE"}

    else:
        filepath = args.get("filepath", str(ensure_desktop_path(f"{title}.docx")))
        return pure_create_word(title, filepath)


def cmd_edit_word(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    text = args["text"]
    position = args.get("position", "end")

    if engine == "WPS":
        wps = get_wps()
        doc = wps.Documents.Open(filepath.__str__())
        if position == "end":
            doc.Content.InsertAfter(Text=text)
        elif position == "start":
            doc.Content.InsertBefore(Text=text)
        doc.Save()
        doc.Close()
        release_wps()
        return {"success": True, "engine": "WPS"}

    elif engine == "MSOFFICE":
        ms = get_ms_module()
        result = ms.ms_edit_word(filepath.__str__(), text, position)
        release_ms()
        return {**result, "engine": "MSOFFICE"}

    else:
        return pure_edit_word(filepath.__str__(), text, position)


def cmd_format_word(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    
    if engine == "WPS":
        wps = get_wps()
        doc = wps.Documents.Open(filepath.__str__())
        for para in doc.Paragraphs:
            rng = para.Range
            if not rng.Text.strip():
                continue
            am = {"center": 1, "left": 0, "right": 2}
            if args.get("align") in am:
                rng.ParagraphFormat.Alignment = am[args["align"]]
        doc.Save()
        doc.Close()
        release_wps()
        return {"success": True, "engine": "WPS"}
    
    elif engine == "MSOFFICE":
        ms = get_ms_module()
        result = ms.ms_format_word(filepath.__str__(), 
                                   args.get("align", "center"),
                                   args.get("font", ""),
                                   args.get("size", 0),
                                   args.get("indent", 0))
        release_ms()
        return {**result, "engine": "MSOFFICE"}
    
    else:
        return {"success": False, "error": "纯 Python 模式暂不支持格式设置"}


def cmd_export_word(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    
    if engine == "WPS":
        wps = get_wps()
        doc = wps.Documents.Open(filepath.__str__())
        fmt = args.get("format", "pdf")
        fmt_map = {"pdf": 17, "txt": 7, "html": 8}
        if fmt not in fmt_map:
            doc.Close()
            release_wps()
            return {"success": False, "error": f"Word 不支持转 {fmt}，支持: {list(fmt_map.keys())}"}
        out = filepath.with_suffix(f".{fmt}")
        doc.SaveAs(out.__str__(), fmt_map[fmt])
        doc.Close()
        release_wps()
        return {"success": True, "path": out.__str__(), "engine": "WPS"}

    elif engine == "MSOFFICE":
        ms = get_ms_module()
        result = ms.ms_export_word(filepath.__str__(), args.get("format", "pdf"))
        release_ms()
        return {**result, "engine": "MSOFFICE"}

    else:
        return {"success": False, "error": "纯 Python 模式不支持格式转换，请安装 WPS 或 MS Office"}


def cmd_info_word(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    
    if engine == "WPS":
        wps = get_wps()
        doc = wps.Documents.Open(filepath.__str__())
        info = {
            "success": True,
            "name": filepath.name,
            "path": filepath.__str__(),
            "page_count": doc.ComputeStatistics(2),
            "word_count": doc.ComputeStatistics(0),
            "paragraph_count": doc.Paragraphs.Count,
            "engine": "WPS",
        }
        doc.Close()
        release_wps()
        return info
    else:
        return pure_info_word(filepath.__str__())


# ==================== Excel ====================

def cmd_create_excel(args):
    engine = get_engine()
    name = args.get("name", "新建表格")
    
    if engine == "WPS":
        wps = get_wps()
        wb = wps.Workbooks.Add()
        sheets = args.get("sheets")
        if sheets:
            for i, sn in enumerate(sheets):
                if i < wb.Sheets.Count:
                    wb.Sheets(i+1).Name = sn
                else:
                    wb.Sheets.Add().Name = sn
        filepath = ensure_desktop_path(f"{name}.xlsx")
        wb.SaveAs(filepath)
        wb.Close()
        release_wps()
        return {"success": True, "path": filepath.__str__(), "engine": "WPS"}

    elif engine == "MSOFFICE":
        ms = get_ms_module()
        result = ms.ms_create_excel(name, args.get("sheets"))
        release_ms()
        return {**result, "engine": "MSOFFICE"}

    else:
        filepath = args.get("filepath", str(ensure_desktop_path(f"{name}.xlsx")))
        sheets = args.get("sheets", ["Sheet1"])
        return pure_create_excel(name, sheets, filepath)


def cmd_input_excel(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    data = args.get("data", [])

    if engine == "WPS":
        wps = get_wps()
        wb = wps.Workbooks.Open(filepath.__str__())
        ws = wb.Sheets(sheet)
        for r, row in enumerate(data, start=1):
            for c, val in enumerate(row, start=1):
                ws.Cells(r, c).Value = val
        wb.Save()
        wb.Close()
        release_wps()
        return {"success": True, "input_rows": len(data), "engine": "WPS"}

    elif engine == "MSOFFICE":
        ms = get_ms_module()
        # 复用 WPS 实现（简化）
        return {"success": False, "error": "MS Office 模式暂不支持数据录入，请使用 WPS 模式"}

    else:
        return pure_input_excel(filepath.__str__(), sheet, data)


def cmd_formula_excel(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    cell = args.get("cell", "A1")
    formula = args.get("formula", "")

    if engine == "WPS":
        wps = get_wps()
        wb = wps.Workbooks.Open(filepath.__str__())
        ws = wb.Sheets(sheet)
        ws.Range(cell).Formula = formula
        wb.Save()
        wb.Close()
        release_wps()
        return {"success": True, "formula_set": True, "engine": "WPS"}

    elif engine == "MSOFFICE":
        return {"success": False, "error": "MS Office 模式暂不支持公式，请使用 WPS 模式"}

    else:
        return {"success": False, "error": "纯 Python 模式暂不支持公式"}


def cmd_sort_excel(args):
    """多列排序（WPS 模式）"""
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    sorts = args.get("sorts", [])  # [{"column":"金额","ascending":false}, ...]

    if engine not in ("WPS",):
        return {"success": False, "error": "排序需要 WPS 模式，请安装 WPS Office"}

    try:
        wps = get_wps()
        wb = wps.Workbooks.Open(filepath.__str__())
        ws = wb.Sheets(sheet)

        used = ws.UsedRange
        if used.Rows.Count <= 1:
            wb.Close()
            release_wps()
            return {"success": True, "note": "数据不足，无需排序"}

        # 读取数据
        data = []
        for r in range(1, used.Rows.Count + 1):
            row = [ws.Cells(r, c).Value for c in range(1, used.Columns.Count + 1)]
            data.append(row)

        header = data[0]
        body = data[1:]

        # 构建排序键
        def sort_key(row):
            keys = []
            for s in sorts:
                col = s["column"]
                asc = s.get("ascending", True)
                idx = None
                for i, h in enumerate(header):
                    if h and str(h).strip().lower() == col.lower():
                        idx = i
                        break
                if idx is None and len(col) == 1:
                    idx = ord(col.upper()) - ord('A')
                if idx is None:
                    idx = 0
                val = row[idx] if idx < len(row) else None
                if val is None:
                    keys.append((2, ""))
                elif isinstance(val, (int, float)):
                    keys.append((0, val if asc else -val))
                else:
                    keys.append((0, str(val).lower()))
            return tuple(keys)

        body.sort(key=sort_key)

        # 写回
        for r, row in enumerate(body, start=2):
            for c, val in enumerate(row, start=1):
                ws.Cells(r, c).Value = val

        wb.Save()
        wb.Close()
        release_wps()
        return {"success": True, "sorts": sorts, "rows": len(body), "engine": "WPS"}

    except Exception as e:
        release_wps()
        return {"success": False, "error": str(e)}


def cmd_filter_excel(args):
    """多条件筛选"""
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    conditions = args.get("conditions", [])

    if engine not in ("WPS",):
        return {"success": False, "error": "筛选需要 WPS 模式，请安装 WPS Office"}

    try:
        wps = get_wps()
        wb = wps.Workbooks.Open(filepath.__str__())
        ws = wb.Sheets(sheet)

        used = ws.UsedRange
        if used.Rows.Count <= 1:
            wb.Close()
            release_wps()
            return {"success": True, "filtered": 0, "rows": []}

        data = []
        for r in range(1, used.Rows.Count + 1):
            row = [ws.Cells(r, c).Value for c in range(1, used.Columns.Count + 1)]
            data.append(row)

        header = data[0]
        body = data[1:]

        def col_to_idx(col_name):
            for i, h in enumerate(header):
                if h and str(h).strip().lower() == col_name.lower():
                    return i
            if len(col_name) == 1:
                return ord(col_name.upper()) - ord('A')
            return None

        filtered = [header]
        for row in body:
            match_all = True
            for cond in conditions:
                ci = col_to_idx(cond["column"])
                if ci is None:
                    match_all = False
                    break
                val = row[ci] if ci < len(row) else None
                op = cond["op"]
                target = cond["value"]

                if op == ">":
                    try:
                        if val is None or float(val) <= float(target):
                            match_all = False
                            break
                    except (ValueError, TypeError):
                        match_all = False
                        break
                elif op == "<":
                    try:
                        if val is None or float(val) >= float(target):
                            match_all = False
                            break
                    except (ValueError, TypeError):
                        match_all = False
                        break
                elif op == "=":
                    if val is None or str(val) != target:
                        match_all = False
                        break
                elif op == "contains":
                    if val is None or target.lower() not in str(val).lower():
                        match_all = False
                        break

            if match_all:
                filtered.append(row)

        wb.Close()
        release_wps()
        return {"success": True, "filtered": len(filtered) - 1, "rows": filtered, "engine": "WPS"}

    except Exception as e:
        release_wps()
        return {"success": False, "error": str(e)}


def cmd_chart_excel(args):
    """生成图表"""
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    chart_type = args.get("type", "bar")
    data_range = args.get("data", "A1:B10")

    if engine not in ("WPS",):
        return {"success": False, "error": "图表需要 WPS 模式，请安装 WPS Office"}

    try:
        wps = get_wps()
        wb = wps.Workbooks.Open(filepath.__str__())
        ws = wb.Sheets(sheet)

        type_map = {"bar": 57, "line": 4, "pie": 5, "column": 51}
        obj = ws.ChartObjects().Add(100, 100, 350, 250)
        obj.Chart.SetSourceData(ws.Range(data_range))
        obj.Chart.ChartType = type_map.get(chart_type, 57)

        wb.Save()
        wb.Close()
        release_wps()
        return {"success": True, "chart_created": True, "engine": "WPS"}

    except Exception as e:
        release_wps()
        return {"success": False, "error": str(e)}


# ==================== PPT ====================

def cmd_create_ppt(args):
    engine = get_engine()
    title = args.get("title", "新建演示")
    
    if engine == "WPS":
        wps = get_wps()
        ppt = wps.Presentations.Add()
        slide = ppt.Slides.Add(1, 1)
        if title and slide.Shapes.Count > 0:
            slide.Shapes(1).TextFrame.TextRange.Text = title
        filepath = ensure_desktop_path(f"{title}.pptx")
        ppt.SaveAs(filepath)
        ppt.Close()
        release_wps()
        return {"success": True, "path": filepath.__str__(), "engine": "WPS"}

    elif engine == "MSOFFICE":
        ms = get_ms_module()
        result = ms.ms_create_ppt(title)
        release_ms()
        return {**result, "engine": "MSOFFICE"}

    else:
        filepath = args.get("filepath", str(ensure_desktop_path(f"{title}.pptx")))
        return pure_create_ppt(title, filepath)


def cmd_add_ppt_slide(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    layout = args.get("layout", "title_content")
    title = args.get("title", "")

    if engine == "WPS":
        wps = get_wps()
        ppt = wps.Presentations.Open(filepath.__str__())
        layout_map = {"title": 1, "title_content": 2, "text": 3, "blank": 12}
        layout_id = layout_map.get(layout, 2)
        slide = ppt.Slides.Add(ppt.Slides.Count + 1, layout_id)
        if title and slide.Shapes.Count > 0:
            try:
                slide.Shapes(1).TextFrame.TextRange.Text = title
            except Exception:
                pass
        total = ppt.Slides.Count
        ppt.Save()
        ppt.Close()
        release_wps()
        return {"success": True, "total_slides": total, "engine": "WPS"}

    elif engine == "MSOFFICE":
        return {"success": False, "error": "MS Office 模式暂不支持添加幻灯片"}

    else:
        return {"success": False, "error": "纯 Python 模式暂不支持添加幻灯片"}


def cmd_insert_ppt(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    slide_num = args.get("slide", 1)
    content = args.get("content", "")

    if engine == "WPS":
        wps = get_wps()
        ppt = wps.Presentations.Open(filepath.__str__())
        if slide_num < 1 or slide_num > ppt.Slides.Count:
            ppt.Close()
            release_wps()
            return {"success": False, "error": f"幻灯片 {slide_num} 不存在"}
        slide = ppt.Slides(slide_num)
        shape = slide.Shapes.AddTextbox(1, 100, 120, 500, 350)
        shape.TextFrame.TextRange.Text = content
        ppt.Save()
        ppt.Close()
        release_wps()
        return {"success": True, "inserted": True, "engine": "WPS"}

    elif engine == "MSOFFICE":
        return {"success": False, "error": "MS Office 模式暂不支持插入内容"}

    else:
        return {"success": False, "error": "纯 Python 模式暂不支持插入内容"}


def cmd_theme_ppt(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    theme_name = args.get("name", "business")

    if engine == "WPS":
        wps = get_wps()
        ppt = wps.Presentations.Open(filepath.__str__())
        theme_map = {
            "business_blue": "BusinessBlue", "business": "Business",
            "modern": "Modern", "tech": "Tech", "elegant": "Elegant",
            "dark": "Dark", "minimal": "Minimal", "colorful": "Colorful",
        }
        display_name = theme_map.get(theme_name)
        if not display_name:
            ppt.Close()
            release_wps()
            return {"success": False, "error": f"不支持的主题: {theme_name}"}
        wps_dirs = [
            Path("C:/Program Files/WPS Office/Office6/Theme"),
            Path("C:/Program Files (x86)/WPS Office/Office6/Theme"),
        ]
        applied = False
        for d in wps_dirs:
            if d.exists():
                for f in d.glob(f"*{display_name}*.thmx"):
                    ppt.ApplyTheme(str(f))
                    applied = True
                    break
                if applied:
                    break
        ppt.Save()
        ppt.Close()
        release_wps()
        return {"success": True, "applied": applied, "theme": theme_name, "engine": "WPS"}

    elif engine == "MSOFFICE":
        return {"success": False, "error": "MS Office 模式暂不支持主题"}

    else:
        return {"success": False, "error": "纯 Python 模式暂不支持主题"}


def cmd_export_ppt(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    fmt = args.get("format", "pdf")

    if engine == "WPS":
        wps = get_wps()
        ppt = wps.Presentations.Open(filepath.__str__())
        fmt_map = {"pdf": 32, "pptx": 1, "png": 17}
        if fmt not in fmt_map:
            ppt.Close()
            release_wps()
            return {"success": False, "error": f"PPT 不支持转 {fmt}"}
        out = filepath.with_suffix(f".{fmt}")
        ppt.SaveAs(out.__str__(), fmt_map[fmt])
        ppt.Close()
        release_wps()
        return {"success": True, "path": out.__str__(), "engine": "WPS"}

    elif engine == "MSOFFICE":
        return {"success": False, "error": "MS Office 模式暂不支持导出"}

    else:
        return {"success": False, "error": "纯 Python 模式不支持导出"}


def cmd_info_ppt(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    
    if engine == "WPS":
        wps = get_wps()
        ppt = wps.Presentations.Open(filepath.__str__())
        info = {
            "success": True,
            "name": filepath.name,
            "path": filepath.__str__(),
            "slide_count": ppt.Slides.Count,
            "engine": "WPS",
        }
        ppt.Close()
        release_wps()
        return info
    else:
        return pure_info_ppt(filepath.__str__())


# ==================== 格式转换 ====================

def cmd_convert(args):
    filepath = safe_path(args["filepath"])
    fmt = args.get("output_format", "pdf")

    if not filepath.exists():
        return {"success": False, "error": f"文件不存在: {filepath}"}

    engine = get_engine()
    if engine not in ("WPS", "MSOFFICE"):
        return {"success": False, "error": "格式转换需要 WPS 或 MS Office 模式"}

    ext = filepath.suffix.lower()
    output_path = filepath.with_suffix(f".{fmt}")

    try:
        wps = get_wps()
        if ext == ".docx":
            doc = wps.Documents.Open(filepath.__str__())
            fmt_map = {"pdf": 17, "txt": 7, "html": 8}
            if fmt not in fmt_map:
                doc.Close()
                release_wps()
                return {"success": False, "error": f"Word 不支持转 {fmt}"}
            doc.SaveAs(output_path.__str__(), fmt_map[fmt])
            doc.Close()
        elif ext == ".xlsx":
            wb = wps.Workbooks.Open(filepath.__str__())
            if fmt == "csv":
                wb.SaveAs(output_path.__str__(), 6)
            elif fmt == "pdf":
                wb.SaveAs(output_path.__str__(), 0)
            else:
                wb.Close()
                release_wps()
                return {"success": False, "error": f"Excel 不支持转 {fmt}"}
            wb.Close()
        elif ext == ".pptx":
            ppt = wps.Presentations.Open(filepath.__str__())
            if fmt == "pdf":
                ppt.SaveAs(output_path.__str__(), 32)
            else:
                ppt.Close()
                release_wps()
                return {"success": False, "error": f"PPT 不支持转 {fmt}"}
            ppt.Close()
        else:
            release_wps()
            return {"success": False, "error": f"不支持的文件类型: {ext}"}
        
        release_wps()
        return {"success": True, "path": output_path.__str__(), "engine": engine}

    except Exception as e:
        release_wps()
        return {"success": False, "error": str(e)}


# ==================== 引擎信息 ====================

def cmd_engine_info(args):
    return {"engine": detect_engine()}


# ==================== 命令路由表 ====================

COMMANDS = {
    "create_word": cmd_create_word,
    "edit_word": cmd_edit_word,
    "format_word": cmd_format_word,
    "export_word": cmd_export_word,
    "info_word": cmd_info_word,
    "create_excel": cmd_create_excel,
    "input_excel": cmd_input_excel,
    "formula_excel": cmd_formula_excel,
    "sort_excel": cmd_sort_excel,
    "filter_excel": cmd_filter_excel,
    "chart_excel": cmd_chart_excel,
    "create_ppt": cmd_create_ppt,
    "add_ppt_slide": cmd_add_ppt_slide,
    "insert_ppt": cmd_insert_ppt,
    "theme_ppt": cmd_theme_ppt,
    "export_ppt": cmd_export_ppt,
    "info_ppt": cmd_info_ppt,
    "convert": cmd_convert,
    "engine_info": cmd_engine_info,
    "exit": None,
}


def run():
    """主循环"""
    line = sys.stdin.readline()
    while line:
        line = line.strip()
        if not line:
            line = sys.stdin.readline()
            continue
        try:
            req = json.loads(line)
            cmd = req.get("cmd")
            args = req.get("args", {})

            if cmd == "exit":
                break

            if cmd not in COMMANDS:
                resp = {"ok": False, "error": f"未知命令: {cmd}"}
            else:
                try:
                    result = COMMANDS[cmd](args)
                    resp = {"ok": True, **result} if isinstance(result, dict) else result
                except Exception as e:
                    resp = {
                        "ok": False,
                        "error": str(e),
                        "hint": traceback.format_exc().split("\n")[-3] if hasattr(e, '__traceback__') else "",
                    }

            print(json.dumps(resp, ensure_ascii=False, default=str))
            sys.stdout.flush()

        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "error": f"JSON 解析错误: {e}"}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"ok": False, "error": f"致命错误: {e}"}))
            sys.stdout.flush()

        line = sys.stdin.readline()

    release_wps()
    release_ms()


if __name__ == "__main__":
    run()
