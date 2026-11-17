"""
WPS Worker v4.5.0 - 智能引擎切换 v4.5
引擎优先级: WPS > MS Office > LibreOffice > 纯Python

v4.5.0 变更:
  - 🎯 会议纪要生成（ASR 转写 → LLM 摘要 → Word 生成）
  - 🎯 ASR 降级链（whisper → azure → google → template）
  - 🎯 LLM 降级链（rule-engine → external-llm → pure-template）
  - 🎯 COM 健康检查（状态检测 + 残留进程 + 自动释放）
  - 🎯 故障排除大章合并（避坑+FAQ+错误ID 统一索引）

v4.4.0 变更:
  - 🎯 长文档排版自动化（目录/页眉页脚/标题编号/图表索引/交叉引用/格式统一）
  - 🎯 多级标题编号引擎（中文/阿拉伯/罗马数字三种样式）
  - 🎯 格式统一预设模板（论文/标书/报告）

v4.3.0 变更:
  - 🎯 Excel 深度分析（公式纠错/数据清洗/透视表/数据预测/NL2Formula）
  - 🎯 硬件自适应降级（低配禁用线性回归）
  - 🎯 数据质量评分体系（0-100分）

v4.1.0 变更:
  - 🎯 PPT 智能生成深度增强（多源输入/演讲者备注/动画建议/配色适配/图表推荐/排练辅助）

v4.0.0 变更:
  - 🎯 Word→PPT 一键生成（chapter splitting + 模板匹配）
  - 🎯 Excel 自然语言数据分析（NL2SQL+透视分析+图表）
  - 🎯 Word 合同条款自动审查标注（规则引擎+红线标注）
  - 🎯 Excel 发票 OCR 入账（PDF/图片→Excel，本地OCR）

v3.1.0 变更:
  - 模板安全修复：删除二进制模板，改为纯Python代码生成
  - 避坑指南：20+ 条高频/中频/低频错误排查
  - FAQ 扩展至 15 个（含文件大小、并发数、批量限制）

v3.0.0 变更:
  - 自动重试机制（max_retry_count=3，指数退避）
  - 性能优化：硬件自适应（CPU/内存检测，动态线程分配）
  - 子进程超时保护（60s/120s 分级超时）
  - Update checker（7天检查一次）
"""
import sys
import json
import subprocess
import traceback
import time
from pathlib import Path

# 智能引擎检测器
from wps_engine import detect_best_engine, get_engine

# WPS/MS COM 对象管理
from wps_common import (
    get_wps, get_ms_word,
    safe_path, ensure_desktop_path, release_wps, release_ms, with_retry
)

# 纯 Python 模式（惰性导入 / 坑13 优化：仅在 PURE/LIBREOFFICE 路径真正调用时加载，
# 省去每条命令的 wps_pure 模块导入开销；pywin32/python-docx/openpyxl 经核查已在其内部惰性导入）
_PURE_MOD = None


def _pure():
    global _PURE_MOD
    if _PURE_MOD is None:
        import wps_pure
        _PURE_MOD = wps_pure
    return _PURE_MOD

# 错误处理模块
from wps_error import wps_error

# 性能管理 v3.0
from wps_performance import (
    get_worker_config, adjust_timeout_for_file,
    should_use_parallel, get_optimal_worker_count,
    get_hardware_info
)

# 更新检查器 v3.0
from wps_update import show_update_reminder, try_check_update

# MS Office 兼容层
wps_ms = None


def get_ms_module():
    global wps_ms
    if wps_ms is None:
        import wps_ms as m
        wps_ms = m
    return wps_ms


# ==================== 三层容错：重试→回退→报错 ====================

def with_auto_retry(func, max_retries=None, backoff_base=1):
    """
    自动重试包装器。
    如果 max_retries 未指定，自动使用硬件配置的建议值。
    重试间隔：指数退避（1s, 2s, 4s...）
    """
    if max_retries is None:
        cfg = get_worker_config()
        max_retries = cfg.get("retry_count", 3)
    
    def wrapper(*args, **kwargs):
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                # 只有超时/通信错误才重试
                if any(kw in err_str for kw in ["timeout", "busy", "rpc", "socket", "connection", "locked"]):
                    if attempt < max_retries:
                        wait = backoff_base * (2 ** attempt)
                        time.sleep(wait)
                        # 释放 COM 对象后重试
                        try:
                            release_wps()
                            release_ms()
                        except Exception:
                            pass
                        continue
                # 其他错误直接返回
                raise
        raise last_error
    return wrapper


# ==================== LibreOffice Headless ====================

def libreoffice_convert(input_path: str, output_format: str = "pdf") -> dict:
    """LibreOffice Headless 转换（120s 超时）"""
    input_p = Path(input_path).resolve()
    if not input_p.exists():
        return {"success": False, "error": wps_error("E013", path=input_path)}

    output_dir = input_p.parent
    
    soffice_path = "soffice"
    if sys.platform == "win32":
        # 搜索 soffice.exe
        candidates = [
            Path("C:/Program Files/LibreOffice/program/soffice.exe"),
            Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe"),
        ]
        for c in candidates:
            if c.exists():
                soffice_path = str(c)
                break

    try:
        cmd = [
            soffice_path, "--headless",
            "--convert-to", output_format,
            "--outdir", str(output_dir),
            str(input_p)
        ]

        cfg = get_worker_config()
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=cfg["timeout"] * 2
        )

        if result.returncode != 0:
            stderr = result.stderr.strip()
            return {"success": False, "error": wps_error("E012", detail=stderr[:200])}

        output_file = input_p.with_suffix(f".{output_format}")
        if not output_file.exists():
            return {"success": False, "error": wps_error("E015")}

        return {"success": True, "path": str(output_file), "engine": "LIBREOFFICE"}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": wps_error("E006")}
    except FileNotFoundError:
        return {"success": False, "error": wps_error("E011")}
    except Exception as e:
        return {"success": False, "error": wps_error("E014", detail=str(e))}


# ==================== Word ====================

def cmd_create_word(args):
    engine = get_engine()
    title = args.get("title", "新建文档")
    body = args.get("body", "")
    filepath = args.get("filepath", str(ensure_desktop_path(f"{title}.docx")))

    if engine in ("PURE", "LIBREOFFICE"):
        return _pure().pure_create_word(title, filepath, body)

    try:
        if engine == "WPS":
            wps = get_wps()
            doc = wps.Documents.Add()
            if title:
                para = doc.Paragraphs.Add()
                para.Range.Text = title
                para.Range.Font.Size = 16
                para.Range.Font.Bold = True
                para.Range.ParagraphFormat.Alignment = 1
            if body:
                for line in body.split("\n"):
                    if line.strip():
                        p = doc.Content.Add()
                        p.Range.Text = line
            doc.SaveAs(filepath)
            doc.Close()
            release_wps()
            return {"success": True, "path": filepath, "engine": "WPS"}

        if engine == "MSOFFICE":
            ms = get_ms_module()
            result = ms.ms_create_word(title, filepath)
            release_ms()
            return {**result, "engine": "MSOFFICE"}

    except Exception as e:
        release_wps()
        release_ms()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


def cmd_edit_word(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    text = args["text"]
    position = args.get("position", "end")

    if engine == "LIBREOFFICE":
        return {"success": False, "error": wps_error("E010", feature="编辑文档")}

    if engine == "PURE":
        return _pure().pure_edit_word(filepath.__str__(), text, position)

    try:
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

        if engine == "MSOFFICE":
            ms = get_ms_module()
            result = ms.ms_edit_word(filepath.__str__(), text, position)
            release_ms()
            return {**result, "engine": "MSOFFICE"}

    except Exception as e:
        release_wps()
        release_ms()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


def cmd_format_word(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])

    # 所有引擎走纯 Python（兼容性最好）
    return _pure().pure_format_word(
        filepath.__str__(),
        font_name=args.get("font", ""),
        font_size=args.get("size", 0),
        bold=args.get("bold", False),
        align=args.get("align", ""),
        space_after=args.get("space_after", 0),
        first_line_indent=args.get("first_line_indent", 0),
        color=args.get("color", "")
    )


def cmd_export_word(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    fmt = args.get("format", "pdf")

    if engine == "LIBREOFFICE":
        return libreoffice_convert(filepath.__str__(), fmt)

    if engine == "PURE":
        info = detect_best_engine()
        if info.get("libreoffice"):
            return libreoffice_convert(filepath.__str__(), fmt)
        return {"success": False, "error": wps_error("E010", feature="格式转换")}

    if engine == "WPS":
        try:
            wps = get_wps()
            doc = wps.Documents.Open(filepath.__str__())
            fmt_map = {"pdf": 17, "txt": 7, "html": 8}
            if fmt not in fmt_map:
                doc.Close()
                release_wps()
                return {"success": False, "error": wps_error("E015")}
            out = filepath.with_suffix(f".{fmt}")
            doc.SaveAs(out.__str__(), fmt_map[fmt])
            doc.Close()
            release_wps()
            return {"success": True, "path": out.__str__(), "engine": "WPS"}
        except Exception as e:
            release_wps()
            return {"success": False, "error": wps_error("E014", detail=str(e))}

    if engine == "MSOFFICE":
        try:
            ms = get_ms_module()
            result = ms.ms_export_word(filepath.__str__(), fmt)
            release_ms()
            return {**result, "engine": "MSOFFICE"}
        except Exception as e:
            release_ms()
            return {"success": False, "error": wps_error("E014", detail=str(e))}

    return {"success": False, "error": wps_error("E014", detail=f"未知引擎: {engine}")}


def cmd_info_word(args):
    filepath = safe_path(args["filepath"])
    return _pure().pure_info_word(filepath.__str__)


# ==================== Excel ====================

def cmd_create_excel(args):
    engine = get_engine()
    name = args.get("name", "新建表格")

    if engine in ("PURE", "LIBREOFFICE"):
        filepath = args.get("filepath", str(ensure_desktop_path(f"{name}.xlsx")))
        sheets = args.get("sheets", ["Sheet1"])
        result = _pure().pure_create_excel(name, sheets, filepath)
        return result

    try:
        if engine == "WPS":
            wps = get_wps()
            wb = wps.Workbooks.Add()
            sheets = args.get("sheets")
            if sheets:
                for i, sn in enumerate(sheets):
                    if i < wb.Sheets.Count:
                        wb.Sheets(i + 1).Name = sn
                    else:
                        wb.Sheets.Add().Name = sn
            filepath = ensure_desktop_path(f"{name}.xlsx")
            wb.SaveAs(filepath)
            wb.Close()
            release_wps()
            return {"success": True, "path": filepath.__str__(), "engine": "WPS"}

        if engine == "MSOFFICE":
            ms = get_ms_module()
            result = ms.ms_create_excel(name, args.get("sheets"), args.get("filepath"))
            release_ms()
            return {**result, "engine": "MSOFFICE"}

    except Exception as e:
        release_wps()
        release_ms()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


def cmd_input_excel(args):
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    data = args.get("data", [])
    return _pure().pure_input_excel(filepath.__str__(), sheet, data)


def cmd_formula_excel(args):
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    cell = args.get("cell", "A1")
    formula = args.get("formula", "")

    engine = get_engine()
    if engine != "WPS":
        # 非 WPS 走纯 Python（openpyxl 支持写公式）
        return _pure().pure_formula_excel(filepath.__str__(), sheet, cell, formula)

    try:
        wps = get_wps()
        wb = wps.Workbooks.Open(filepath.__str__())
        ws = wb.Sheets(sheet)
        ws.Range(cell).Formula = formula
        wb.Save()
        wb.Close()
        release_wps()
        return {"success": True, "formula_set": True, "engine": "WPS"}
    except Exception as e:
        release_wps()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


def cmd_add_sheet_excel(args):
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    headers = args.get("headers")
    data = args.get("data")
    return _pure().pure_add_excel_sheet(filepath.__str__(), sheet, headers, data)


def cmd_stats_excel(args):
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    column = args.get("column", "A")
    stat_type = args.get("type", "SUM")
    return _pure().pure_statistics_excel(filepath.__str__(), sheet, column, stat_type)


def cmd_sort_excel(args):
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    sorts = args.get("sorts", [])
    return _pure().pure_sort_excel(filepath.__str__(), sheet, sorts)


def cmd_filter_excel(args):
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    conditions = args.get("conditions", [])
    logic = args.get("logic", "AND")
    return _pure().pure_filter_excel(filepath.__str__(), sheet, conditions, logic)


def cmd_chart_excel(args):
    filepath = safe_path(args["filepath"])
    sheet = args.get("sheet", "Sheet1")
    chart_type = args.get("type", "bar")
    data_range = args.get("data", "A1:B10")
    title = args.get("title", "")
    return _pure().pure_chart_excel(filepath.__str__(), sheet, chart_type, data_range, title)


def cmd_info_excel(args):
    filepath = safe_path(args["filepath"])
    return _pure().pure_info_excel(filepath.__str__)


# ==================== PPT ====================

def cmd_create_ppt(args):
    engine = get_engine()
    title = args.get("title", "新建演示")
    filepath = args.get("filepath", str(ensure_desktop_path(f"{title}.pptx")))

    if engine in ("PURE", "LIBREOFFICE"):
        return _pure().pure_create_ppt(title, filepath)

    try:
        if engine == "WPS":
            wps = get_wps()
            ppt = wps.Presentations.Add()
            slide = ppt.Slides.Add(1, 1)
            if title and slide.Shapes.Count > 0:
                slide.Shapes(1).TextFrame.TextRange.Text = title
            ppt.SaveAs(filepath)
            ppt.Close()
            release_wps()
            return {"success": True, "path": filepath, "engine": "WPS"}

        if engine == "MSOFFICE":
            ms = get_ms_module()
            result = ms.ms_create_ppt(title, filepath)
            release_ms()
            return {**result, "engine": "MSOFFICE"}

    except Exception as e:
        release_wps()
        release_ms()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


def cmd_add_ppt_slide(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    layout = args.get("layout", "title_content")
    title = args.get("title", "")

    if engine in ("PURE", "LIBREOFFICE"):
        return {"success": False, "error": wps_error("E010", feature="添加幻灯片（仅WPS支持）")}

    if engine != "WPS":
        return {"success": False, "error": wps_error("E010", feature="添加幻灯片")}

    try:
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

    except Exception as e:
        release_wps()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


def cmd_insert_ppt(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    slide_num = args.get("slide", 1)
    content = args.get("content", "")

    if engine in ("PURE", "LIBREOFFICE"):
        return {"success": False, "error": wps_error("E010", feature="插入内容")}

    if engine != "WPS":
        return {"success": False, "error": wps_error("E010", feature="插入内容")}

    try:
        wps = get_wps()
        ppt = wps.Presentations.Open(filepath.__str__())
        if slide_num < 1 or slide_num > ppt.Slides.Count:
            ppt.Close()
            release_wps()
            return {"success": False, "error": wps_error("E013", path=f"幻灯片 {slide_num}")}
        slide = ppt.Slides(slide_num)
        shape = slide.Shapes.AddTextbox(1, 100, 120, 500, 350)
        shape.TextFrame.TextRange.Text = content
        ppt.Save()
        ppt.Close()
        release_wps()
        return {"success": True, "inserted": True, "engine": "WPS"}

    except Exception as e:
        release_wps()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


def cmd_theme_ppt(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    theme_name = args.get("name", "business")

    if engine in ("PURE", "LIBREOFFICE"):
        return {"success": False, "error": wps_error("E010", feature="主题应用")}

    if engine != "WPS":
        return {"success": False, "error": wps_error("E010", feature="主题应用")}

    try:
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
            return {"success": False, "error": wps_error("E015")}
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

    except Exception as e:
        release_wps()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


def cmd_export_ppt(args):
    engine = get_engine()
    filepath = safe_path(args["filepath"])
    fmt = args.get("format", "pdf")

    if engine == "LIBREOFFICE":
        return libreoffice_convert(filepath.__str__(), fmt)

    if engine == "PURE":
        info = detect_best_engine()
        if info.get("libreoffice"):
            return libreoffice_convert(filepath.__str__(), fmt)
        return {"success": False, "error": wps_error("E010", feature="导出")}

    if engine == "WPS":
        try:
            wps = get_wps()
            ppt = wps.Presentations.Open(filepath.__str__())
            fmt_map = {"pdf": 32, "pptx": 1, "png": 17}
            if fmt not in fmt_map:
                ppt.Close()
                release_wps()
                return {"success": False, "error": wps_error("E015")}
            out = filepath.with_suffix(f".{fmt}")
            ppt.SaveAs(out.__str__(), fmt_map[fmt])
            ppt.Close()
            release_wps()
            return {"success": True, "path": out.__str__(), "engine": "WPS"}
        except Exception as e:
            release_wps()
            return {"success": False, "error": wps_error("E014", detail=str(e))}

    if engine == "MSOFFICE":
        return {"success": False, "error": wps_error("E010", feature="导出")}

    return {"success": False, "error": wps_error("E014", detail=f"未知引擎: {engine}")}


def cmd_info_ppt(args):
    filepath = safe_path(args["filepath"])
    return _pure().pure_info_ppt(filepath.__str__)


# ==================== 格式转换 ====================

def cmd_convert(args):
    filepath = safe_path(args["filepath"])
    fmt = args.get("output_format", "pdf")

    if not filepath.exists():
        return {"success": False, "error": wps_error("E013", path=filepath.__str__())}

    engine = get_engine()
    
    # PURE/LIBREOFFICE 走 LibreOffice
    if engine in ("PURE", "LIBREOFFICE"):
        info = detect_best_engine()
        if info.get("libreoffice"):
            return libreoffice_convert(filepath.__str__(), fmt)
        return {"success": False, "error": wps_error("E010", feature="格式转换")}

    if engine not in ("WPS", "MSOFFICE"):
        return {"success": False, "error": wps_error("E014")}

    output_path = filepath.with_suffix(f".{fmt}")

    try:
        wps = get_wps()
        ext = filepath.suffix.lower()
        if ext == ".docx":
            doc = wps.Documents.Open(filepath.__str__())
            fmt_map = {"pdf": 17, "txt": 7, "html": 8}
            if fmt not in fmt_map:
                doc.Close()
                release_wps()
                return {"success": False, "error": wps_error("E015")}
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
                return {"success": False, "error": wps_error("E015")}
            wb.Close()
        elif ext == ".pptx":
            ppt = wps.Presentations.Open(filepath.__str__())
            if fmt == "pdf":
                ppt.SaveAs(output_path.__str__(), 32)
            else:
                ppt.Close()
                release_wps()
                return {"success": False, "error": wps_error("E015")}
            ppt.Close()
        else:
            release_wps()
            return {"success": False, "error": wps_error("E015")}

        release_wps()
        return {"success": True, "path": output_path.__str__(), "engine": engine}

    except Exception as e:
        release_wps()
        return {"success": False, "error": wps_error("E014", detail=str(e))}


# ==================== 引擎信息 + 硬件信息 ====================

def cmd_engine_info(args):
    info = detect_best_engine()
    hw = get_hardware_info()
    return {
        "engine": info["engine"],
        "word": info["word"],
        "excel": info["excel"],
        "ppt": info["ppt"],
        "wps": info.get("wps", False),
        "msword": info.get("msword", False),
        "msexcel": info.get("msexcel", False),
        "msppt": info.get("msppt", False),
        "libreoffice": info.get("libreoffice", False),
        "platform": info["platform"],
        "hardware": hw,
    }


def cmd_hardware_info(args):
    return get_hardware_info()


def cmd_check_update(args):
    return try_check_update(force=True)


# ==================== 命令路由表 ====================

# ==================== 新模块路由命令 ====================

def cmd_docx_to_ppt(args):
    """Word → PPT 一键生成"""
    from wps_docx_to_ppt import docx_to_ppt
    return docx_to_ppt(
        input_path=args.get("input"),
        output_path=args.get("output", ""),
        title=args.get("title", ""),
        theme=args.get("theme", "business")
    )

def cmd_nl_analyze(args):
    """Excel 自然语言数据分析"""
    from wps_nl_analysis import nl_analyze
    return nl_analyze(
        filepath=args.get("file"),
        query=args.get("query"),
        sheet=args.get("sheet", "Sheet1")
    )

def cmd_invoice_ocr(args):
    """发票 OCR 入账"""
    from wps_invoice_ocr import invoice_to_accounting
    return invoice_to_accounting(
        input_path=args.get("input"),
        output_path=args.get("output", "")
    )

def cmd_ppt_generate(args):
    """PPT 智能生成（多源输入 + 增强）"""
    from ppt_generator import generate_ppt
    return generate_ppt(
        input_path=args.get("input"),
        output_path=args.get("output", ""),
        input_type=args.get("type", "auto"),
        title=args.get("title", ""),
        theme=args.get("theme", "business"),
        brand_color=args.get("brand_color", ""),
        scheme_type=args.get("scheme_type", "complementary"),
        enable_notes=not args.get("no_notes", False),
        enable_animations=not args.get("no_animations", False),
        enable_rehearsal=not args.get("no_rehearsal", False)
    )

def cmd_excel_analyze(args):
    """Excel 深度分析 v4.3"""
    from excel_analyzer import analyze_excel
    return analyze_excel(
        filepath=args.get("file"),
        task=args.get("task", "profile"),
        sheet=args.get("sheet", "Sheet1"),
        column_name=args.get("column", ""),
        method=args.get("method", "auto"),
        forecast_steps=args.get("steps", 3),
        query=args.get("query", ""),
        use_llm=args.get("use_llm", False),
        row_field=args.get("row_field", ""),
        value_field=args.get("value_field", ""),
        col_field=args.get("col_field", ""),
        agg_func=args.get("agg_func", "sum"),
    )

def cmd_long_document(args):
    """长文档排版 v4.4"""
    from long_document import format_document
    return format_document(
        filepath=args.get("file"),
        task=args.get("task", "analyze"),
        max_level=args.get("max_level", 3),
        field=args.get("field", False),
        insert=args.get("insert", False),
        odd_even=args.get("odd_even", False),
        odd_header=args.get("odd_header", ""),
        even_header=args.get("even_header", ""),
        chapter_in_header=args.get("chapter_in_header", False),
        page_number=args.get("page_number", False),
        page_format=args.get("page_format", "arabic"),
        page_start=args.get("page_start", 1),
        style=args.get("style", "arabic"),
        preset=args.get("preset", "thesis"),
        numbering_style=args.get("numbering_style", "arabic"),
        output_path=args.get("output", ""),
    )

def cmd_meeting_minutes(args):
    """会议纪要生成 v4.5"""
    from meeting_minutes import MeetingMinutesGenerator
    config = {
        "asr_method": args.get("asr_method", "auto"),
        "summary_method": args.get("summary_method", "auto"),
        "segment_minutes": args.get("segment_minutes", 5),
        "progress_cb": lambda *a: None,  # Worker 模式下静默
    }
    gen = MeetingMinutesGenerator(config)
    return gen.generate_minutes(
        audio_path=args.get("file"),
        output_path=args.get("output", ""),
        title=args.get("title", "会议纪要"),
        language=args.get("language", "zh"),
    )

def cmd_com_health(args):
    """COM 健康检查 v4.5"""
    from com_health import COMHealthChecker
    checker = COMHealthChecker(auto_release=args.get("auto_release", False))
    check_type = args.get("check_type", "full")
    
    if check_type == "wps":
        return checker.check_wps_com()
    elif check_type == "ms":
        return checker.check_ms_com()
    elif check_type == "residuals":
        return checker.check_com_residuals()
    elif check_type == "release":
        return checker.release_all_com(force=args.get("force", False))
    else:
        return checker.full_health_check()

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
    "add_sheet_excel": cmd_add_sheet_excel,
    "stats_excel": cmd_stats_excel,
    "info_excel": cmd_info_excel,
    "create_ppt": cmd_create_ppt,
    "add_ppt_slide": cmd_add_ppt_slide,
    "insert_ppt": cmd_insert_ppt,
    "theme_ppt": cmd_theme_ppt,
    "export_ppt": cmd_export_ppt,
    "info_ppt": cmd_info_ppt,
    "convert": cmd_convert,
    "engine_info": cmd_engine_info,
    "hardware_info": cmd_hardware_info,
    "check_update": cmd_check_update,
    "docx_to_ppt": cmd_docx_to_ppt,
    "nl_analyze": cmd_nl_analyze,
    "invoice_ocr": cmd_invoice_ocr,
    "ppt_generate": cmd_ppt_generate,
    "excel_analyze": cmd_excel_analyze,
    "long_document": cmd_long_document,
    "meeting_minutes": cmd_meeting_minutes,
    "com_health": cmd_com_health,
    "exit": None,
}


def run():
    """主循环（带更新检查提醒）"""
    # 每次启动时检查更新（7天一次）
    reminder = show_update_reminder()
    if reminder:
        print(f"[UPDATE] {reminder}", file=sys.stderr)
    
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
                resp = {"ok": False, "error": wps_error("E014", detail=f"未知命令: {cmd}")}
            else:
                try:
                    result = COMMANDS[cmd](args)
                    resp = {"ok": True, **result} if isinstance(result, dict) else result
                except Exception as e:
                    resp = {
                        "ok": False,
                        "error": wps_error("E014", detail=str(e)),
                        "hint": traceback.format_exc().split("\n")[-3] if hasattr(e, '__traceback__') else "",
                    }

            print(json.dumps(resp, ensure_ascii=False, default=str))
            sys.stdout.flush()

        except json.JSONDecodeError as e:
            print(json.dumps({"ok": False, "error": wps_error("E014", detail=f"JSON解析错误: {e}")}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"ok": False, "error": wps_error("E014", detail=str(e))}))
            sys.stdout.flush()

        line = sys.stdin.readline()

    release_wps()
    release_ms()


if __name__ == "__main__":
    run()
