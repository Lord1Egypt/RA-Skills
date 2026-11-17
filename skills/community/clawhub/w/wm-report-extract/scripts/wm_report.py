#!/usr/bin/env python3
"""wm_report.py — 财报 PDF 内容理解与按需提取的本地预处理 CLI（wm-report-extract）。

流水线（详见 ../SKILL.md）：
  fetch → convert → scan → extract-tables → materialize-tables
  → apply-promotions（Agent type_promote）→ qa-tables（质量门，无 quality.json 不得给下游）
  → review-extract → render-html（可选，单文件阅览）
  → locate / extract-query / text_scan

缓存：~/.cache/wm-report-extract/{sha12}/（sha256 of PDF，幂等，WM_REPORT_CACHE_DIR 可覆盖）。

依赖：转换需 `pip install docling pymupdf`（Python 3.10+）；scan/locate/cache 仅用标准库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import sys
import time
import unicodedata
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKILL_ID = "wm-report-extract"
CACHE_ENV = "WM_REPORT_CACHE_DIR"
PAGE_MARKER_RE = re.compile(r"<!--\s*page:(\d+)\s*-->")
KANGXI_RE = re.compile(r"[\u2f00-\u2fdf\ufffd]")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


# --------------------------------------------------------------------------
# 基础工具
# --------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def nfkc(s: str) -> str:
    """NFKC 归一化：财报 PDF 常见康熙部首兼容字符（⼈民币/⽬录）→ 常规汉字。"""
    return unicodedata.normalize("NFKC", s or "")


def cache_root() -> Path:
    base = os.environ.get(CACHE_ENV)
    if base:
        return Path(base).expanduser()
    return Path.home() / ".cache" / SKILL_ID


def sha12_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def entry_dir(sha: str) -> Path:
    return cache_root() / sha


def read_json(path: Path, default=None):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def index_load() -> dict:
    idx = read_json(cache_root() / "index.json", {}) or {}
    if not isinstance(idx.get("entries"), dict):
        idx["entries"] = {}
    return idx


def index_save(idx: dict) -> None:
    write_json(cache_root() / "index.json", idx)


def index_upsert(sha: str, **fields) -> None:
    idx = index_load()
    ent = idx["entries"].get(sha, {"added_at": now_iso()})
    ent.update({k: v for k, v in fields.items() if v is not None})
    idx["entries"][sha] = ent
    index_save(idx)


def resolve_source(spec: str) -> Path:
    """接受缓存 id（sha12）或 PDF 路径。"""
    p = Path(spec).expanduser()
    if p.is_file():
        return p
    d = entry_dir(spec)
    if (d / "report.pdf").is_file():
        return d / "report.pdf"
    raise SystemExit(f"找不到 PDF：{spec}（既不是文件路径，也不是缓存 id）")


# --------------------------------------------------------------------------
# ① convert：docling → report.md / pages.json / convert_meta.json
# --------------------------------------------------------------------------

def _hf_cache_has_docling() -> bool:
    """本机 HuggingFace 缓存里是否已有 docling 模型（models--docling-* 目录）。"""
    hf_home = Path(os.environ.get("HF_HOME") or Path.home() / ".cache" / "huggingface")
    hub = hf_home / "hub"
    try:
        return hub.is_dir() and any(p.name.startswith("models--docling") for p in hub.iterdir())
    except OSError:
        return False


def apply_hf_offline_default() -> None:
    """本地已有 docling 模型缓存时默认离线运行。

    docling 每次转换都会向 huggingface.co 做 revision 在线检查；网络波动（SSL 中断/代理切换）
    会把"模型已全部缓存"的转换也卡死。已有缓存则离线；显式设置过 HF_HUB_OFFLINE/
    TRANSFORMERS_OFFLINE 的用户不覆盖；无缓存的机器保持在线（首次转换需下载模型）。
    """
    if "HF_HUB_OFFLINE" in os.environ or "TRANSFORMERS_OFFLINE" in os.environ:
        return
    if _hf_cache_has_docling():
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        print("已检测到本地 docling 模型缓存，默认离线运行（如需更新模型：unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE）",
              file=sys.stderr)


def docling_import_or_die():
    apply_hf_offline_default()  # 必须在 import docling 之前生效
    try:
        from docling.document_converter import (  # noqa: F401
            DocumentConverter,
            PdfFormatOption,
        )
    except ImportError:
        raise SystemExit(
            "缺少依赖 docling（转换阶段必需）。安装：\n"
            "  pip install docling pymupdf\n"
            "（约 1-2GB，含 torch；Python 3.10+。scan/locate/cache 子命令无需安装。）"
        )
    import docling  # noqa: F401

    try:
        import fitz  # noqa: F401
    except ImportError:
        raise SystemExit("缺少依赖 pymupdf（读取书签/加密状态）。安装：pip install pymupdf")
    return True


def _mps_guard(device: str) -> None:
    """darwin 上 docling 的 MPS 后端有内核崩溃风险：import docling 前关掉。"""
    if device == "cpu":
        import torch

        torch.backends.mps.is_available = lambda: False
        torch.backends.mps.is_built = lambda: False
        try:
            torch._dynamo.config.suppress_errors = True
        except Exception:
            pass


def _build_docling_converter(*, accurate: bool, ocr: bool, threads: int, device: str):
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
    from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
    from docling.document_converter import DocumentConverter, PdfFormatOption

    po = PdfPipelineOptions()
    po.do_ocr = bool(ocr)
    po.do_table_structure = True
    po.table_structure_options.mode = TableFormerMode.ACCURATE if accurate else TableFormerMode.FAST
    fo = PdfFormatOption(
        pipeline_options=po,
        accelerator_options=AcceleratorOptions(
            device={"cpu": AcceleratorDevice.CPU, "mps": AcceleratorDevice.MPS,
                    "cuda": AcceleratorDevice.CUDA}.get(device, AcceleratorDevice.AUTO),
            num_threads=max(1, threads),
        ),
    )
    return DocumentConverter(format_options={InputFormat.PDF: fo})


def emit_markdown(events) -> tuple[str, list[dict]]:
    """事件流 → (report.md 文本, pages 统计)。

    events: iterable of {"kind": "text"|"table"|"picture", "label": str,
                         "page": int|None, "text": str}
    纯函数，可用假事件单测。页序按事件流顺序；page 为 None 的事件贴到当前页。
    """
    lines: list[str] = []
    pages: dict[int, dict] = {}
    cur_page = 0
    for ev in events:
        page = ev.get("page") or cur_page
        if page != cur_page:
            cur_page = page
            lines.append("")
            lines.append(f"<!-- page:{page} -->")
            lines.append("")
        stat = pages.setdefault(page, {"page": page, "line_start": len(lines), "chars": 0,
                                       "headings": [], "tables": 0, "pictures": 0})
        kind = ev.get("kind")
        if kind == "picture":
            stat["pictures"] += 1
            continue
        text = nfkc(ev.get("text") or "").strip()
        if not text:
            continue
        if kind == "table":
            stat["tables"] += 1
            lines.append("")
            lines.append(text)
            lines.append("")
        else:
            label = ev.get("label") or "text"
            stat["chars"] += len(text)
            if label in ("title", "section_header"):
                prefix = "# " if label == "title" else "## "
                text = text.lstrip("# ").strip()
                stat["headings"].append(text[:60])
                lines.append("")
                lines.append(prefix + text)
                lines.append("")
            elif label == "list_item":
                lines.append("- " + text)
            elif label in ("page_header", "page_footer"):
                continue  # 页眉页脚不入正文，由 furniture 统计进 pages.json
            else:  # paragraph / caption / footnote / text
                lines.append("")
                lines.append(text)
    md = "\n".join(lines).strip() + "\n"
    page_list = list(pages[p] for p in sorted(pages))
    for j, stat in enumerate(page_list):
        nxt = page_list[j + 1]["line_start"] if j + 1 < len(page_list) else len(lines)
        stat["line_end"] = max(stat["line_start"], nxt - 1)
    return md, page_list


def docling_convert(pdf_path: Path, *, accurate: bool, ocr: bool, threads: int, device: str):
    """执行 docling 转换，返回 (events 迭代器, convert_info dict)。"""
    _mps_guard(device)
    converter = _build_docling_converter(accurate=accurate, ocr=ocr, threads=threads, device=device)

    import fitz

    pdf_doc = fitz.open(pdf_path)
    pdf_info = {
        "pages": pdf_doc.page_count,
        "encrypted": bool(pdf_doc.is_encrypted),
        "bookmarks": pdf_doc.get_toc(),
        "title": (pdf_doc.metadata or {}).get("title") or "",
    }
    pdf_doc.close()

    t0 = time.time()
    try:
        result = converter.convert(str(pdf_path))
    except Exception as e:  # 转换失败：返回带 error 的 info，不中断流程（scan 会标记）
        err = f"{type(e).__name__}: {e}"
        if re.search(r"OfflineModeIsEnabled|offline|local_files_only", err, re.I):
            err += "（离线模式下缺模型文件：unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE 后联网重试）"
        return None, {"error": err, "seconds": round(time.time() - t0, 1),
                      "pdf": pdf_info, "ocr": ocr, "table_mode": "accurate" if accurate else "fast"}
    seconds = time.time() - t0
    doc = result.document
    d = doc.export_to_dict()

    # self_ref → page_no 映射（texts + tables）
    page_map: dict[str, int] = {}
    for t in d.get("texts", []) + d.get("tables", []):
        prov = t.get("prov") or []
        if prov and t.get("self_ref"):
            page_map[t["self_ref"]] = prov[0].get("page_no")

    # 页眉页脚计数（furniture，供异常检测）
    furniture_hits: dict[int, int] = {}
    kangxi_pages: set[int] = set()
    garbled_pages: set[int] = set()
    for t in d.get("texts", []):
        prov = t.get("prov") or []
        page = prov[0].get("page_no") if prov else None
        if not page:
            continue
        if t.get("label") in ("page_header", "page_footer"):
            furniture_hits[page] = furniture_hits.get(page, 0) + 1
        text = t.get("text") or ""
        if "\ufffd" in text:
            garbled_pages.add(page)
        if KANGXI_RE.search(text):
            kangxi_pages.add(page)

    def events():
        table_md_fail = 0
        for item, _level in doc.iterate_items():
            kind = type(item).__name__
            self_ref = getattr(item, "self_ref", None)
            page = page_map.get(self_ref)
            if kind == "TableItem":
                try:
                    md = item.export_to_markdown(doc)
                except Exception:
                    table_md_fail += 1
                    data = getattr(item, "data", None)
                    md = "| 表格导出失败（fallback 网格） |\n|---|\n"
                    if data is not None:
                        md += f"| {getattr(data, 'num_rows', '?')} 行 × {getattr(data, 'num_cols', '?')} 列 |"
                yield {"kind": "table", "label": "table", "page": page, "text": nfkc(md)}
            elif kind == "PictureItem":
                yield {"kind": "picture", "label": "picture", "page": page, "text": ""}
            else:
                label = str(getattr(item, "label", "text"))
                if label in ("page_header", "page_footer"):
                    continue
                text = nfkc(getattr(item, "text", "") or "")
                if text:
                    yield {"kind": "text", "label": label, "page": page, "text": text}

    info = {
        "seconds": round(seconds, 1),
        "ocr": bool(ocr),
        "table_mode": "accurate" if accurate else "fast",
        "device": device,
        "threads": threads,
        "pdf": pdf_info,
        "furniture_hits": furniture_hits,
        "kangxi_pages": sorted(kangxi_pages),
        "garbled_pages": sorted(garbled_pages),
        "converted_at": now_iso(),
    }
    try:
        import importlib.metadata as md

        info["docling_version"] = md.version("docling")
    except Exception:
        info["docling_version"] = "unknown"
    return events(), info


# --------------------------------------------------------------------------
# ①b fitz 轨道：有框线页的零幻觉表格（find_tables）+ 页面线格统计 + ACCURATE 报表页精修
# --------------------------------------------------------------------------

NUM_TOKEN_RE = re.compile(r"\d+(?:\.\d+)?")
PURE_NUM_RE = re.compile(r"^[-−（(+]?[\d,，]+(?:\.\d+)?[）)%％]?$")
SIGNATURE_ROW_TOKS = ("财务负责人", "会计机构负责人", "董事会秘书", "法定代表人", "公司负责人")
HEADER_LABEL_TOKS = ("项目", "科目", "附注")
FITZ_MIN_V_LINES = 4
FITZ_MIN_ROWS = 3
FITZ_TEXT_DUP_THRESHOLD = 0.55  # 同页文本 bigram 包含度 ≥ 此值判为同一物理表（文本表去重）


def _text_bigrams(s: str) -> set:
    """NFKC 去标点空白后的字符 bigram 集合（跨轨文本相似度，对版式/公司无偏）。"""
    s2 = re.sub(r"[\W_]+", "", nfkc(s))
    if len(s2) < 2:
        return {s2} if s2 else set()
    return {s2[i:i + 2] for i in range(len(s2) - 1)}


def _numeric_tokens(s: str) -> list[str]:
    """NFKC + 去千分位/百分号后的数字 token（数值存在性校验与轨道配对共用）。
    数字间 分隔符±空白（「36 , 897」「29 . 3」）双侧同构归一，与 fitz 页文本对齐。"""
    s1 = nfkc(s or "")
    s2 = re.sub(r"(?<=\d)[\s]*[，,．.][\s]*(?=\d)", "", s1)
    s2 = s2.replace("，", "").replace(",", "").replace("％", "").replace("%", "")
    return NUM_TOKEN_RE.findall(s2)


def _numeric_token_variants(s: str) -> list[list[str]]:
    """断字双侧同构的双粒度方案：分段（数字间纯空白为界，如「100 200」两值并格）
    与合并（逐字符断字「1 3 ,0 6 8」还原整值）。存在性判定取「任一方案全部命中」。"""
    seg = _numeric_tokens(s)
    s1 = nfkc(s or "")
    merged_src = re.sub(r"(?<=\d)[\s]*[，,．.]?[\s]*(?=\d)", "", s1)
    merged_src = merged_src.replace("，", "").replace(",", "").replace("％", "").replace("%", "")
    merged = NUM_TOKEN_RE.findall(merged_src)
    return [seg] if merged == seg else [seg, merged]


def _tokens_all_hit(s: str, page_toks: set) -> bool:
    return any(all(t in page_toks for t in toks) for toks in _numeric_token_variants(s))


def _row_has_pure_number(cells) -> bool:
    """是否含纯数值单元格（金额）。表头日期如「2024年12月31日」不算——区分表头区与数据区。"""
    return any(PURE_NUM_RE.match((c or "").strip()) for c in cells)


def _is_signature_row(cells) -> bool:
    """表尾签名行：首列为空、含签名头衔、且无数字（如 招行报表续页的 财务负责人/董事会秘书）。"""
    first = (cells[0] or "").strip() if cells else ""
    if first:
        return False
    blob = " ".join(c or "" for c in cells)
    return any(tok in blob for tok in SIGNATURE_ROW_TOKS) and not _numeric_tokens(blob)


def strip_signature_rows(md_text: str) -> str:
    """从 markdown 管道表中去掉表尾签名行（Docling FAST/ACCURATE 都会并进表，两档均需过滤）。"""
    out = []
    for ln in (md_text or "").splitlines():
        s = ln.strip()
        if s.startswith("|") and s.endswith("|") and not SEP_ROW_PAT.match(s):
            if _is_signature_row(split_md_row(s)):
                continue
        out.append(ln)
    return "\n".join(out)


def _stack_header_cells(a, b) -> str:
    """两级表头堆叠：「2024年12月31日」+「期末余额」→「2024年12月31日期末余额」。

    包含关系去重（a==b / a in b / b in a 取大者），避免「何平何平」式重复拼接。
    """
    a, b = a or "", b or ""
    if a in HEADER_LABEL_TOKS:
        return b or a
    if b in HEADER_LABEL_TOKS:
        return a
    if not a:
        return b
    if not b:
        return a
    if a == b or a in b:
        return b
    if b in a:
        return a
    return a + b


def _md_cell(s) -> str:
    return (s or "").replace("|", "／").replace("\n", " ").strip()


def fitz_matrix_to_md(matrix: list[list], row_bboxes: list | None = None) -> tuple[str, list]:
    """fitz extract() 矩阵 → markdown 管道表。返回 (md, 与输出 md 行对齐的 row_bboxes)。

    后处理：签名行过滤；表头右填充（列跨）；两级表头堆叠；首列 None 向下填充（行标签跨行）。
    数据区其余 None 置空——禁止数值复制下填（避免 Docling 式重复展开污染下游统计）。
    """
    rows = [[nfkc(c).strip() if c else None for c in r] for r in (matrix or [])]
    keep = [i for i, r in enumerate(rows) if not _is_signature_row(r)]
    rows = [rows[i] for i in keep]
    bboxes = [(list(row_bboxes[i]) if row_bboxes and i < len(row_bboxes) and row_bboxes[i] else None)
              for i in keep]
    if not rows or not any(c for r in rows for c in r):
        return "", []
    ncol = max(len(r) for r in rows)
    for r in rows:
        r.extend([None] * (ncol - len(r)))
    hdr_end = 0
    for i, r in enumerate(rows[:2]):
        if not _row_has_pure_number(r):
            hdr_end = i + 1
        else:
            break
    for r in rows[:hdr_end]:  # 表头列跨右填充
        for c in range(1, ncol):
            if r[c] is None and r[c - 1]:
                r[c] = r[c - 1]
    if hdr_end == 2:  # 两级表头堆叠为单行
        rows = [[_stack_header_cells(rows[0][c], rows[1][c]) for c in range(ncol)]] + rows[2:]
        if bboxes:
            bboxes = [bboxes[0]] + bboxes[2:]
    for i in range(1, len(rows)):  # 首列行标签跨行合并下填
        if rows[i][0] is None:
            rows[i][0] = rows[i - 1][0]
    lines = []
    for i, r in enumerate(rows):
        lines.append("| " + " | ".join(_md_cell(c) for c in r) + " |")
        if i == 0:
            lines.append("|" + "|".join([" --- "] * ncol) + "|")
    return "\n".join(lines), bboxes


def _page_line_counts(page) -> tuple[int, int]:
    """页面竖线/横线数量（线段 + 细矩形描边），用于有框线页判定。"""
    v = h = 0
    try:
        drawings = page.get_drawings()
    except Exception:
        return 0, 0
    for dr in drawings:
        for item in dr.get("items") or []:
            if not item:
                continue
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                if abs(p1.x - p2.x) < 0.5:
                    v += 1
                elif abs(p1.y - p2.y) < 0.5:
                    h += 1
            elif item[0] == "re":
                r = item[1]
                if r.width < 1.5:
                    v += 1
                elif r.height < 1.5:
                    h += 1
    return v, h


def extract_fitz_tables(pdf_path: Path) -> tuple[dict, dict, float]:
    """全档 find_tables(lines) + 逐页线格统计 → (tables_by_page, geo_by_page, seconds)。

    只保留 ≥FITZ_MIN_ROWS 行、≥2 列且含数字的表（数据表）；目录点线/页眉框线自然出局。
    """
    import fitz

    t0 = time.time()
    tables_by_page: dict[int, list[dict]] = {}
    geo: dict[int, dict] = {}
    with fitz.open(pdf_path) as doc:
        for pno in range(doc.page_count):
            page = doc[pno]
            v, h = _page_line_counts(page)
            geo[pno + 1] = {"v_lines": v, "h_lines": h}
            if v < FITZ_MIN_V_LINES:
                continue
            try:
                finder = page.find_tables()
            except Exception:
                continue
            tabs = []
            for t in finder.tables:
                if t.row_count < FITZ_MIN_ROWS or t.col_count < 2:
                    continue
                try:
                    matrix = t.extract()
                except Exception:
                    continue
                flat = " ".join(str(c) for row in matrix for c in row if c)
                if not _numeric_tokens(flat):
                    continue
                row_bboxes = []
                for r in t.rows:
                    bb = next((c for c in (r.cells or []) if c), None)
                    row_bboxes.append([round(x, 1) for x in bb] if bb else None)
                tabs.append({
                    "matrix": matrix,
                    "bbox": [round(x, 1) for x in t.bbox],
                    "row_bboxes": row_bboxes,
                    "rows": t.row_count, "cols": t.col_count,
                })
            if tabs:
                tables_by_page[pno + 1] = tabs
    return tables_by_page, geo, round(time.time() - t0, 1)


def merge_fitz_track(events: list[dict], fitz_tables: dict[int, list[dict]]):
    """按页把有框线的 docling 表替换为 fitz 版（零幻觉 + 单元格 bbox）。

    配对按数值集合重叠；fitz 数值比 docling 缺 ≥20% 时不替换（弱线简表/目录点线页保护）。
    第二轮同页文本 bigram 去重：数值配不上的纯文本表（联系人/简历类）与 docling 残留
    互斥——数值表用 fitz（零幻觉优势），文本表用 docling（语义结构优势）。
    未配对且无重复的 fitz 表（docling 真漏检）插入该页表区末尾。
    返回 (新 events, fitz manifest 含最终页内顺序, stats)；fitz 表事件带 _fitz_table 标记。
    """
    stats = {"replaced": 0, "kept_docling_richer": 0, "fitz_added": 0, "suppressed_duplicate": 0}
    table_idx = [i for i, ev in enumerate(events) if ev.get("kind") == "table" and ev.get("page")]
    replace_at: dict[int, dict] = {}
    extra: dict[int, list[dict]] = {}
    for page, tabs in sorted(fitz_tables.items()):
        remaining = [i for i in table_idx if events[i].get("page") == page]
        for ft in tabs:
            ft_nums = set(_numeric_tokens(" ".join(str(c) for row in ft["matrix"] for c in row if c)))
            best, best_ov = None, 0
            for i in remaining:
                ov = len(ft_nums & set(_numeric_tokens(events[i].get("text") or "")))
                if ov > best_ov:
                    best, best_ov = i, ov
            if best is not None and best_ov >= 2 and best_ov >= 0.5 * len(ft_nums):
                if len(ft_nums) >= 0.8 * len(set(_numeric_tokens(events[best].get("text") or ""))):
                    replace_at[best] = ft
                    stats["replaced"] += 1
                else:
                    stats["kept_docling_richer"] += 1
                remaining.remove(best)
            else:
                extra.setdefault(page, []).append(ft)
    insert_after: dict[int, list[dict]] = {}
    for page, tabs in extra.items():
        kept_idx = [i for i in table_idx if events[i].get("page") == page and i not in replace_at]
        keep_tabs = []
        for ft in tabs:
            fb = _text_bigrams(" ".join(str(c) for row in ft["matrix"] for c in row if c))
            dup = False
            for i in kept_idx:
                db = _text_bigrams(events[i].get("text") or "")
                if not fb or not db:
                    continue
                if len(fb & db) / min(len(fb), len(db)) >= FITZ_TEXT_DUP_THRESHOLD:
                    dup = True
                    break
            if dup:
                stats["suppressed_duplicate"] += 1
            else:
                keep_tabs.append(ft)
        if not keep_tabs:
            continue
        idxs = [i for i in table_idx if events[i].get("page") == page]
        anchor = idxs[-1] if idxs else max(
            (i for i, ev in enumerate(events) if ev.get("page") == page), default=None)
        if anchor is not None:
            insert_after.setdefault(anchor, []).extend(keep_tabs)
            stats["fitz_added"] += len(keep_tabs)

    def fitz_event(page, ft, src):
        md, bboxes = fitz_matrix_to_md(ft["matrix"], ft.get("row_bboxes"))
        if not md:
            return None
        ev = {"kind": "table", "label": "table", "page": page, "text": md,
              "_fitz_table": True, "_fitz_info": {
                  "rows": ft.get("rows"), "cols": ft.get("cols"), "bbox": ft.get("bbox"),
                  "row_bboxes": bboxes, "source": src}}
        return ev

    new_events: list[dict] = []
    for i, ev in enumerate(events):
        if i in replace_at:
            fe = fitz_event(ev.get("page"), replace_at[i], "replace")
            new_events.append(fe or ev)
        else:
            if ev.get("kind") == "table":
                ev["text"] = strip_signature_rows(ev.get("text") or "")
            new_events.append(ev)
        for ft in insert_after.get(i) or []:
            fe = fitz_event(ev.get("page"), ft, "added")
            if fe:
                new_events.append(fe)
    manifest_pages: dict[str, list[dict]] = {}
    seen: dict[int, int] = {}
    for ev in new_events:
        if ev.get("kind") != "table" or not ev.get("page"):
            continue
        p = ev["page"]
        k = seen.get(p, 0)
        seen[p] = k + 1
        info = ev.pop("_fitz_info", None)
        if info:
            manifest_pages.setdefault(str(p), []).append({"order": k, **info})
    return new_events, {"pages": manifest_pages, "stats": stats}, stats


STMT_PAGE_TITLE_RE = re.compile(
    r"资产负债表|利润表|现金流量表|所有者权益变动表"
    r"|財務狀況表|财务状况表|損益表|损益表|現金流量表|權益變動表|权益变动表"
)
STMT_STRUCT_TOKENS = (
    "资产总计", "负债和所有者权益总计", "负债及所有者权益总计",
    "营业总收入", "净利润", "经营活动产生的现金流量净额",
    "資產總值", "負債總額", "權益總額", "年內虧損", "期內虧損",
    "經營活動產生的現金流量", "經營活動所得現金淨額", "融資活動",
)
ACCURATE_REFINE_MAX_PAGES = 24


def pick_refine_pages(events: list[dict]) -> list[int]:
    """选 ACCURATE 精修页：fitz 未接管 + docling 表 ≥5 行 + 报表特征（页标题或结构词）；含续页。"""
    page_text: dict[int, str] = {}
    page_tables: dict[int, list[dict]] = {}
    for ev in events:
        p = ev.get("page")
        if not p:
            continue
        if ev.get("kind") == "table":
            page_tables.setdefault(p, []).append(ev)
        else:
            page_text[p] = page_text.get(p, "") + "\n" + (ev.get("text") or "")
    cand: set[int] = set()
    for p, tabs in page_tables.items():
        for ev in tabs:
            if ev.get("_fitz_table"):
                continue
            text = ev.get("text") or ""
            if parse_table_block(text.splitlines()).get("rows", 0) < 5:
                continue
            if STMT_PAGE_TITLE_RE.search(page_text.get(p, "")) or any(
                    tok in text for tok in STMT_STRUCT_TOKENS):
                cand.add(p)
                break
    for p in sorted(cand):  # 续页（签名行所在页）
        nxt = p + 1
        if nxt not in cand and any(not ev.get("_fitz_table") for ev in page_tables.get(nxt, [])):
            cand.add(nxt)
    return sorted(cand)[:ACCURATE_REFINE_MAX_PAGES]


def docling_refine_pages(pdf_path: Path, pages: list[int], *, threads: int, device: str) -> dict[int, list[str]]:
    """ACCURATE 模式逐页重转 → {page: [table md]}（模型只加载一次；失败页跳过）。"""
    _mps_guard(device)
    converter = _build_docling_converter(accurate=True, ocr=False, threads=threads, device=device)
    out: dict[int, list[str]] = {}
    for p in pages:
        try:
            result = converter.convert(str(pdf_path), page_range=(p, p))
        except TypeError:
            print(f"ACCURATE 精修: 当前 docling 不支持 page_range，跳过", file=sys.stderr)
            return {}
        except Exception as e:
            print(f"ACCURATE 精修 p{p} 失败: {e}", file=sys.stderr)
            continue
        mds = []
        doc = result.document
        for item, _lvl in doc.iterate_items():
            if type(item).__name__ != "TableItem":
                continue
            try:
                mds.append(strip_signature_rows(nfkc(item.export_to_markdown(doc))))
            except Exception:
                continue
        if mds:
            out[p] = mds
    return out


def splice_refine_events(events: list[dict], refine_mds: dict[int, list[str]]) -> list[dict]:
    """整页替换：该页表格事件统一换成 ACCURATE 版本（叙述/结构仍用 FAST 产物）。"""
    out: list[dict] = []
    anchors: dict[int, int] = {}
    for ev in events:
        p = ev.get("page")
        if ev.get("kind") == "table" and p in refine_mds:
            anchors.setdefault(p, len(out))
            continue
        out.append(ev)
    for p in sorted(refine_mds, reverse=True):
        idx = anchors.get(p)
        if idx is None:
            continue
        out[idx:idx] = [{"kind": "table", "label": "table", "page": p, "text": m}
                        for m in refine_mds[p]]
    return out


def cmd_convert(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(prog="wm_report.py convert", description="Docling 转换 → 带页标记 markdown")
    ap.add_argument("source", help="PDF 路径或缓存 id")
    ap.add_argument("--accurate", action="store_true", help="ACCURATE 表格模式（慢但更准，默认 FAST）")
    ap.add_argument("--ocr", action="store_true", help="开启 OCR（扫描版 PDF；文本版默认关闭提速）")
    ap.add_argument("--force", action="store_true", help="忽略缓存重转")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--device", default="cpu", choices=["cpu", "mps", "cuda", "auto"],
                    help="默认 cpu（darwin 上 MPS 有内核崩溃风险）")
    ap.add_argument("--import-only", action="store_true", help="仅导入 PDF 入缓存，不转换")
    args = ap.parse_args(argv)

    docling_import_or_die()
    pdf = resolve_source(args.source)
    sha = sha12_of_file(pdf)
    d = entry_dir(sha)
    d.mkdir(parents=True, exist_ok=True)
    if pdf.resolve() != (d / "report.pdf").resolve():
        shutil.copyfile(pdf, d / "report.pdf")
    index_upsert(sha, pdf=str(pdf))
    if args.import_only:
        print(json.dumps({"cache_id": sha, "dir": str(d), "imported": True}, ensure_ascii=False))
        return
    if (d / "report.md").is_file() and not args.force:
        print(json.dumps({"cache_id": sha, "cached": True, "report_md": str(d / "report.md")}, ensure_ascii=False))
        return

    print(f"docling 转换中（{args.device}，{args.threads} 线程，{'ACCURATE' if args.accurate else 'FAST'} 表格）…"
          "数百页年报约 5-20 分钟，建议后台运行", file=sys.stderr)
    events_iter, info = docling_convert(d / "report.pdf", accurate=args.accurate, ocr=args.ocr,
                                        threads=args.threads, device=args.device)
    if events_iter is None:
        write_json(d / "convert_meta.json", info)
        index_upsert(sha, converted=False, convert_error=info.get("error"))
        raise SystemExit(f"转换失败：{info.get('error')}（已写入 convert_meta.json，scan 会标记该异常）")
    events = list(events_iter)
    geo: dict[int, dict] = {}
    if args.accurate:
        info["table_track"] = "docling-accurate"
        (d / "fitz_tables.json").unlink(missing_ok=True)
    else:
        info["table_track"] = "hybrid"
        print("fitz 轨道扫描（有框线页表格接管，约 0.5 分钟）…", file=sys.stderr)
        try:
            fitz_tables, geo, fsec = extract_fitz_tables(d / "report.pdf")
            events, fitz_manifest, mstats = merge_fitz_track(events, fitz_tables)
            info["fitz"] = {"seconds": fsec, **mstats}
            write_json(d / "fitz_tables.json", fitz_manifest)
        except Exception as e:
            info["fitz"] = {"error": f"{type(e).__name__}: {e}"}
            print(f"fitz 轨道失败（回退纯 docling）: {e}", file=sys.stderr)
        refine_pages = pick_refine_pages(events)
        info["accurate_refine"] = {"pages": refine_pages}
        if refine_pages:
            print(f"ACCURATE 精修 {len(refine_pages)} 个报表页（每页约 5 秒 + 模型加载约 1 分钟）…",
                  file=sys.stderr)
            t0 = time.time()
            refine_mds = docling_refine_pages(d / "report.pdf", refine_pages,
                                              threads=args.threads, device=args.device)
            if refine_mds:
                events = splice_refine_events(events, refine_mds)
                info["accurate_refine"] = {"pages": sorted(refine_mds),
                                           "seconds": round(time.time() - t0, 1)}
                print(f"ACCURATE 精修完成 {len(refine_mds)} 页", file=sys.stderr)
    md, pages = emit_markdown(events)
    (d / "report.md").write_text(md, encoding="utf-8")

    # merge furniture/kangxi/garbled/线格统计进 pages.json
    fh = info.get("furniture_hits") or {}
    for p in pages:
        p["header_footer_hits"] = fh.get(p["page"], 0)
        g = geo.get(p["page"]) or {}
        p["v_lines"] = g.get("v_lines", 0)
        p["h_lines"] = g.get("h_lines", 0)
    write_json(d / "pages.json", pages)
    # 页号语义声明：pages.json 的 page 是 docling 内容页序，与 report.md `<!-- page:N -->`
    # （PDF 物理页，表 provenance/narrative 溯源用）存在错位——防下游混用
    info["pages_json_page_basis"] = "docling_content_page_seq; NOT pdf physical page (use report.md page markers)"
    info["pipeline_version"] = PIPELINE_VERSION
    write_json(d / "convert_meta.json", info)
    idx = index_load()
    ent = idx["entries"].get(sha, {})
    src_meta = ent.get("source") or read_json(d / "fetch_meta.json", {}).get("source") or {}
    index_upsert(sha, converted=True, pages=info.get("pdf", {}).get("pages"), convert_error=None,
                 title=src_meta.get("title"), symbol=src_meta.get("symbol"))
    print(json.dumps({
        "cache_id": sha,
        "report_md": str(d / "report.md"),
        "pages_json": str(d / "pages.json"),
        "pages": info.get("pdf", {}).get("pages"),
        "seconds": info.get("seconds"),
        "table_mode": info.get("table_mode"),
    }, ensure_ascii=False))


# --------------------------------------------------------------------------
# ② scan：内容理解 → meta.json
# Domain catalogs / signatures: scripts/domain/ (declarative).
# Industry arbitration: domain.policy.apply_industry_arbitration.
# --------------------------------------------------------------------------
from domain.catalogs import (  # noqa: E402
    INDUSTRY_EXT_GROUPS,
    NARRATIVE_REQUIRED_IDS,
    PRIORITY_GROUPS_BASE,
    TABLE_CATALOG,
    TABLE_SPEC_BY_ID,
)
from domain.industry import (  # noqa: E402
    INDUSTRY_HINTS,
    TITLE_INDUSTRY_HINTS,
    TITLE_TRANSPORT_SEGMENT_HINTS,
    TRANSPORT_NEGATIVE_HINTS,
    TRANSPORT_SEGMENT_HINTS,
)
from domain.policy import apply_industry_arbitration  # noqa: E402
from domain.synonyms import KEYWORD_VARIANTS, synonym_variants  # noqa: E402
from domain.signatures import (  # noqa: E402
    ANALYSIS_TITLE_RE,
    CHAPTER_RE,
    CN_NUM,
    HIGH_CONFIDENCE_SIGNATURES,
    STRUCTURAL_RULES,
    STMT_TITLE_TOKS,
    SUBSECTION_ANCHORS,
    SUBSIDIARY_HEADER_TOKS,
    TABLE_SIGNATURES,
    TYPE_HINT_SIGNATURES,
)

RESULT_LAYOUT_VERSION = "0.4.1"
RESULT_LAYOUT_NAME = "split_tables"
# 与 SKILL.md version 同步（发版时手动改）；convert 落 convert_meta.pipeline_version，
# 消费端（qa/materialize/promote）版本不符时打 stale 提醒——回验/签名规则跨版本演进，旧结论可能过期
PIPELINE_VERSION = "0.6.1"


def warn_stale_cache(sha12: str) -> None:
    """缓存由旧版本流水线转换时打 stderr 提醒（不阻断）。"""
    cm = read_json(entry_dir(sha12) / "convert_meta.json", {}) or {}
    v = cm.get("pipeline_version")
    if v != PIPELINE_VERSION:
        shown = v or "无版本戳(视为更早)"
        print(f"提示: 缓存 {sha12} 由 pipeline {shown} 转换, 当前 {PIPELINE_VERSION} —— "
              f"回验/签名已演进, 既有 QA 结论可能过期, 建议重跑 qa-tables 复核", file=sys.stderr)



def page_of_line(md_lines: list[str], line_no: int) -> int:
    """0-based 行号 → 所属页（该行是页标记则返回其页码，否则向前找最近的标记）。"""
    page = 0
    for i in range(min(line_no, len(md_lines) - 1), -1, -1):
        m = PAGE_MARKER_RE.match(md_lines[i].strip())
        if m:
            return int(m.group(1))
    return page


TOC_CHAPTER_RE = re.compile(r"^-\s*(\d+)\s+第([一二三四五六七八九十\d]+)\s*[节章]\s*[、.．:]?\s*(.{2,24})$")


def find_chapters(md_lines: list[str]) -> list[dict]:
    hits = []
    for i, raw in enumerate(md_lines):
        line = nfkc(raw).strip()
        m = CHAPTER_RE.match(line)
        if not m:
            continue
        num_raw, title = m.group(1), m.group(2).strip()
        if len(num_raw) == 1 and num_raw in CN_NUM:
            num = CN_NUM[num_raw]
        elif num_raw.isdigit():
            num = int(num_raw)
        else:
            num = None
        hits.append({"num": num, "title": title, "page": page_of_line(md_lines, i), "line": i,
                     "anchor": line.lstrip("# ").strip(), "source": "body"})
    if hits:
        out = []
        for h in hits:  # 同章节多次出现（目录引用等）：只留首个
            if out and h["num"] == out[-1]["num"]:
                continue
            out.append(h)
        for j, h in enumerate(out):
            h["page_end"] = out[j + 1]["page"] if j + 1 < len(out) else None
        return out
    # 回退：正文无标准章节标题（如数字编号版式）→ 解析目录行。
    # 注意目录页码是印刷页码（page 字段），与 PDF 物理页存在偏移，plan 阶段优先用 sections（物理页）。
    out = []
    for i, raw in enumerate(md_lines):
        m = TOC_CHAPTER_RE.match(nfkc(raw).strip())
        if not m:
            continue
        printed, num_raw, title = int(m.group(1)), m.group(2), m.group(3).strip()
        num = CN_NUM.get(num_raw, int(num_raw) if num_raw.isdigit() else None)
        if out and num == out[-1]["num"]:
            continue
        out.append({"num": num, "title": title, "page": printed, "page_end": None, "line": i,
                    "anchor": nfkc(raw).strip().lstrip("- ").strip(), "source": "toc",
                    "printed_page": True})
    for j, h in enumerate(out):
        h["page_end"] = out[j + 1]["page"] if j + 1 < len(out) else None
    return out


# MD&A 子节（展望/经营模式/行业/风险）优先落在「管理层讨论与分析」章内，避开重要提示免责声明。
MDA_CHAPTER_TITLE_RE = re.compile(r"管理层讨论与分析|经营情况讨论与分析")
MDA_SCOPED_KEYS = frozenset({
    "mda_overview", "mda_outlook", "mda_business", "mda_industry", "risk_factors",
})
DISCLAIMER_PAT = re.compile(
    r"前瞻性(?:陈述|描述)|展望性陈述|不构成.{0,16}实质承诺|敬请投资.?者注意投资风险"
)


def find_mda_page_span(md_lines: list[str], chapters: list[dict] | None) -> tuple[int, int] | None:
    """MD&A 章的页码闭区间。正文标题优先；目录回退时 page 可能是印刷页，作近似窗。"""
    for c in chapters or []:
        title = c.get("title") or ""
        if not MDA_CHAPTER_TITLE_RE.search(title):
            continue
        start = int(c.get("page") or 0)
        end = c.get("page_end")
        return start, int(end) if end else 10**9
    starts: list[tuple[int, int]] = []
    for i, raw in enumerate(md_lines):
        line = nfkc(raw).strip()
        if CHAPTER_RE.match(line) and MDA_CHAPTER_TITLE_RE.search(line):
            starts.append((i, page_of_line(md_lines, i)))
    if not starts:
        return None
    line0, page0 = starts[0]
    page1 = 10**9
    for j in range(line0 + 1, len(md_lines)):
        if CHAPTER_RE.match(nfkc(md_lines[j]).strip()):
            page1 = page_of_line(md_lines, j)
            break
    return page0, page1


OUTLOOK_RANK = (
    re.compile(r"未来发展的讨论与分析"),
    re.compile(r"前景展望"),
    re.compile(r"未来发展的?展望|^#{1,3}\s*未来展望"),
)


def _pick_section_hit(
    key: str, body_hits: list[tuple[int, str, int]], span: tuple[int, int] | None
) -> tuple[int, str, int]:
    candidates = body_hits
    if key in MDA_SCOPED_KEYS and span:
        lo, hi = span
        in_span = [h for h in body_hits if lo <= h[2] <= hi]
        if in_span:
            candidates = in_span
    if key == "mda_outlook":
        for pat in OUTLOOK_RANK:
            ranked = [h for h in candidates if pat.search(h[1])]
            if ranked:
                return ranked[0]
    if key == "risk_factors":
        specific = [h for h in candidates if "可能面对的风险" in h[1]]
        if specific:
            return specific[0]
    return candidates[0]


def find_sections(md_lines: list[str], chapters: list[dict] | None = None) -> list[dict]:
    """子节锚点：优先命中正文行（标题/普通文本），目录行（- 开头列表）只作回退并标注。

    mda_* / risk_factors：跳过前瞻性免责声明；若能定 MD&A 章页区间，优先取区间内命中。
    """
    span = find_mda_page_span(md_lines, chapters)
    out = []
    for key, name, pat in SUBSECTION_ANCHORS:
        body_hits: list[tuple[int, str, int]] = []
        toc_hit = None
        for i, raw in enumerate(md_lines):
            line = nfkc(raw).strip()
            if not line or len(line) > 80:
                continue
            if not pat.search(line):
                continue
            if key in ("mda_outlook", "risk_factors") and DISCLAIMER_PAT.search(line):
                continue
            if line.startswith("- ") or re.match(r"^\d+\s", line):
                if toc_hit is None:
                    toc_hit = (i, line)
                continue  # 目录条目，继续找正文标题
            body_hits.append((i, line, page_of_line(md_lines, i)))
        chosen: tuple[int, str] | None = None
        from_toc = False
        if body_hits:
            pick = _pick_section_hit(key, body_hits, span)
            chosen = (pick[0], pick[1])
        elif toc_hit:
            chosen = toc_hit
            from_toc = True
        if chosen:
            i, line = chosen
            out.append({"key": key, "title": name, "matched": line.lstrip("#- ").strip()[:60],
                        "page": page_of_line(md_lines, i), "line": i, "from_toc": from_toc})
    return out


def parse_table_block(block_lines: list[str]) -> dict:
    """markdown 表格块 → {rows, cols, text}（容错：分隔行不算行）。"""
    rows = 0
    cols = 0
    for ln in block_lines:
        s = ln.strip()
        if s.startswith("|"):
            rows += 1
            cells = [c for c in s.strip("|").split("|")]
            cols = max(cols, len(cells))
    if rows >= 2 and SEP_ROW_PAT.match((block_lines[1].strip() or "|")):
        rows -= 1  # 表头分隔行
    return {"rows": max(0, rows), "cols": cols}


def _table_context(title: str, headers: list | None, sample_labels: list | None) -> str:
    parts = [nfkc(title or "")]
    parts.extend(nfkc(h or "") for h in (headers or []))
    parts.extend(nfkc(s or "") for s in (sample_labels or [])[:8])
    return " ".join(parts)


# 主体列 × 收入/利润指标列：子公司/被投资方 KPI 宽表，不得定型为利润表
ENTITY_SUBJECT_HEADER_TOKS = (
    "子公司名称", "子公司名", "公司名称", "被投资单位", "企业名称", "单位名称", "公司名 称",
)
INCOME_METRIC_HEADER_TOKS = ("营业收入", "营业总收入", "净利润", "综合收益")
INCOME_ROW_SUBJECT_TOKS = (
    "一、营业总收入", "一、营业收入", "一、營業總收入", "一、營業收入",
    "营业总收入", "减:营业成本", "减：营业成本", "二、营业总成本", "二、营业利润",
)
INCOME_CONT_ROW_TOKS = (
    "税金及附加", "销售费用", "管理费用", "研发费用", "财务费用",
    "营业利润", "利润总额", "净利润", "综合收益", "加:其他收益", "加：其他收益",
    "公允价值变动", "信用减值损失", "资产减值损失",
)
CAS_STATEMENT_TEMPLATE_HINTS = frozenset({
    "claims_payout", "premium_income", "deposit_loan", "solvency", "nbv_ev",
})
# 兼容旧名
CAS_INCOME_TEMPLATE_HINTS = CAS_STATEMENT_TEMPLATE_HINTS

CF_ROW_ANCHOR_TOKS = (
    "经营活动产生的现金流量净额", "经营活动产生的现金流量", "经营活动产生/(使用)的现金流量",
    "一、经营活动产生", "销售商品、提供劳务收到的现金",
    "二、投资活动产生的现金流量", "投资活动产生的现金流量", "三、筹资活动产生的现金流量",
    "筹资活动产生的现金流量",
    "經營活動產生的現金流量", "經營活動所得現金淨額", "銷售商品、提供勞務收到的現金",
    "投資活動", "融資活動",
)


def _squash_text(s: str) -> str:
    return re.sub(r"\s+", "", nfkc(s or ""))


def _blob_has_token(blob: str, blob_sq: str, token: str) -> bool:
    """原文或去空白后命中（兼容『产生 /( 使用 )』类断空）。"""
    t = nfkc(token or "")
    if not t:
        return False
    return t in blob or _squash_text(t) in blob_sq


def _is_furniture_title(title: str) -> bool:
    """签字/单位注记等家具行不当报表标题（否决 STRUCTURAL 时视同无标题）。"""
    t = nfkc(title or "").strip()
    if not t:
        return True
    if _is_unit_annotation(t):
        return True
    if any(k in t for k in (
        "会计机构负责人", "主管会计工作负责人", "法定代表人", "财务负责人",
        "盖章", "签字", "签名",
    )):
        return True
    # 纯日期+单位组合行（平安报表页 '2025 年 12 月 31 日 (除特别注明外,金额单位为人民币百万元'
    # 被当标题误触 STRUCTURAL 否决实证）：剔除日期/单位成分后无实质内容即家具
    residual = re.sub(
        r"[0-9０-９\s,，.。/年月日季度上半下半除特别注明外金额单位为人民币百千万亿元()（）【\[\]]", "", t)
    if not residual.strip():
        return True
    # 节编号标题（永辉 '二、财务报表' / 页码残留 '108 / 262' 实证）：非报表名本体，
    # 视同无标题（STRUCTURAL 否决跳过，靠表体科目词定型）；
    # 但编号+具体报表名（'3、合并利润表'）是真标题，不是家具
    m_sec = re.fullmatch(r"[（(]?[一二三四五六七八九十百\d]{1,4}[）)、.]\s*(.{0,12})", t)
    if m_sec and not any(tok in m_sec.group(1) for tok in (
            "资产负债表", "利润表", "现金流量表", "損益表", "財務狀況表",
            "权益变动表", "财务状况表", "损益表")):
        return True
    return False


def _looks_like_entity_kpi_wide_table(headers: list | None, sample_labels: list | None) -> bool:
    """表头含主体列且收入/净利润作指标列、行非利润表科目 → 假利润表。"""
    headers = headers or []
    header_blob = " ".join(nfkc(h or "") for h in headers)
    if not any(tok in header_blob for tok in ENTITY_SUBJECT_HEADER_TOKS):
        return False
    metric_cols = sum(
        1 for h in headers
        if any(m in nfkc(h or "") for m in INCOME_METRIC_HEADER_TOKS)
    )
    if metric_cols < 2:
        return False
    labels = [nfkc(s or "") for s in (sample_labels or [])[:8] if s]
    if any(any(tok in lab for tok in INCOME_ROW_SUBJECT_TOKS) for lab in labels):
        return False
    return True


def _looks_like_non_income_stmt_rows(
    title: str, headers: list | None, sample_labels: list | None,
) -> bool:
    """样本行无利润表科目：子公司 KPI 名单 / 『表N 财务指标』摘要堆砌 → 拒 STRUCTURAL 利润表。"""
    title_n = nfkc(title or "")
    if any(tok in title_n for tok in (STMT_TITLE_TOKS.get("income_stmt") or ())):
        return False
    labels = [nfkc(s or "") for s in (sample_labels or [])[:12] if s]
    header_blob = " ".join(nfkc(h or "") for h in (headers or []))
    labs_blob = " ".join(labels)
    subject_toks = INCOME_ROW_SUBJECT_TOKS + (
        "营业收入", "營業收入", "营业成本", "营业利润", "利润总额", "净利润",
        "減:營業成本", "减:营业成本",
    )
    if any(any(tok in lab for tok in subject_toks) for lab in labels):
        return False
    if labels and any(tok in labels[0] for tok in ENTITY_SUBJECT_HEADER_TOKS):
        return True
    if "财务指标" in header_blob or "财务指标" in labs_blob:
        return True
    if labels and sum(1 for lab in labels if _item_looks_like_entity_name(lab)) >= max(2, len(labels) // 2):
        return True
    return False


def _title_anchored_income_fragment(
    title: str, sample_labels: list | None, body: str,
) -> bool:
    """标题为利润表且行含营业(总)收入科目 → 允许碎片定型（净利润可在续页）。"""
    title_n = nfkc(title or "")
    if _is_furniture_title(title_n):
        return False
    if ANALYSIS_TITLE_RE.search(title_n):
        return False  # 「…主要项目变动分析」是 MD&A 分析表非报表（神华 p020 实证）
    if not any(tok in title_n for tok in (STMT_TITLE_TOKS.get("income_stmt") or ())):
        return False
    row_blob = " ".join(nfkc(s or "") for s in (sample_labels or [])[:12])
    row_blob = row_blob + "\n" + nfkc(body or "")[:3000]
    row_sq = _squash_text(row_blob)
    return any(_blob_has_token(row_blob, row_sq, k) for k in (
        "一、营业总收入", "一、营业收入", "一、營業總收入", "营业总收入", "營業總收入",
    )) or ("营业收入" in row_blob and "一、" in row_blob)


def _title_anchored_cashflow_fragment(
    title: str, sample_labels: list | None, body: str,
) -> bool:
    """标题为现金流量表且行含经营活动/销售收现 → 允许定型（行文可无「净额」）。"""
    title_n = nfkc(title or "")
    if _is_furniture_title(title_n):
        return False
    if ANALYSIS_TITLE_RE.search(title_n):
        return False  # 「利润表及现金流量表主要项目变动分析」11/14 行是损益科目非 CF
    if not any(tok in title_n for tok in (STMT_TITLE_TOKS.get("cashflow_stmt") or ())):
        return False
    row_blob = " ".join(nfkc(s or "") for s in (sample_labels or [])[:12])
    row_blob = row_blob + "\n" + nfkc(body or "")[:3000]
    row_sq = _squash_text(row_blob)
    return any(_blob_has_token(row_blob, row_sq, k) for k in CF_ROW_ANCHOR_TOKS)


def _cas_statement_template_context(
    title: str, sample_labels: list | None, body: str,
) -> bool:
    """CAS 通用三表模板上下文（含保险/银行零行）——抑制跨行业 hint。"""
    title_n = nfkc(title or "")
    if any(tok in title_n for tok in (STMT_TITLE_TOKS.get("income_stmt") or ())):
        return True
    if any(tok in title_n for tok in (STMT_TITLE_TOKS.get("cashflow_stmt") or ())):
        return True
    row_blob = " ".join(nfkc(s or "") for s in (sample_labels or [])[:10])
    row_sq = _squash_text(row_blob)
    if any(_blob_has_token(row_blob, row_sq, k) for k in (
        "一、营业总收入", "一、营业收入", "一、營業總收入",
    )):
        return True
    if any(_blob_has_token(row_blob, row_sq, k) for k in CF_ROW_ANCHOR_TOKS):
        return True
    body_n = nfkc(body or "")[:2000]
    body_sq = _squash_text(body_n)
    if "一、营业总收入" in body_n or "一、營業總收入" in body_n:
        return True
    return any(_blob_has_token(body_n, body_sq, k) for k in (
        "经营活动产生的现金流量", "销售商品、提供劳务收到的现金",
    ))


def _cas_income_stmt_template_context(
    title: str, sample_labels: list | None, body: str,
) -> bool:
    """兼容旧调用名。"""
    return _cas_statement_template_context(title, sample_labels, body)


def _income_stmt_subject_continuation(a: dict, b: dict) -> bool:
    """上表像利润表开头、下表像科目续片 → 跨页粘链（不依赖公司/固定页码）。"""
    a_labs = " ".join(nfkc(s or "") for s in (a.get("sample_labels") or [])[:10])
    b_labs = " ".join(nfkc(s or "") for s in (b.get("sample_labels") or [])[:6])
    if not any(tok in a_labs for tok in ("营业总收入", "营业收入", "一、营业", "營業總收入")):
        return False
    return any(tok in b_labs for tok in INCOME_CONT_ROW_TOKS)


def _collect_continued_pieces(head: dict, by_index: dict) -> list[dict]:
    """传递收集 continued_by 链上全部续片。"""
    out = [head]
    stack = list(head.get("continued_by") or [])
    seen: set[int] = set()
    while stack:
        idx = stack.pop(0)
        if idx in seen or idx not in by_index:
            continue
        seen.add(idx)
        piece = by_index[idx]
        out.append(piece)
        stack.extend(piece.get("continued_by") or [])
    return out


def infer_table_type(
    text: str,
    *,
    title: str = "",
    headers: list | None = None,
    sample_labels: list | None = None,
) -> tuple[str | None, list[str], str | None]:
    """高置信才返回 type；type_hint 为低置信候选。优先用标题+表头+样本行，全文仅作兼容回退。"""
    headers = headers or []
    sample_labels = sample_labels or []
    ctx = _table_context(title, headers, sample_labels)
    if not ctx.strip():
        ctx = nfkc(text or "")[:2000]
    header_blob = " ".join(nfkc(h or "") for h in headers)
    title_n = nfkc(title)
    body = nfkc(text or "")[:8000]

    if all(k in header_blob for k in ("姓名", "职务")) and any(
        k in header_blob for k in ("报酬", "持股", "薪酬")
    ):
        return "executives", ["姓名", "职务"], None

    for typ, kws in HIGH_CONFIDENCE_SIGNATURES:
        found = [k for k in kws if k in ctx]
        if len(found) == len(kws):
            return typ, found, None

    # 标题锚定的利润表碎片（净利润可在续页）
    if _title_anchored_income_fragment(title_n, sample_labels, body):
        return "income_stmt", ["利润表", "营业总收入"], None
    # 标题锚定的现金流量表（行文可无「净额」）
    if _title_anchored_cashflow_fragment(title_n, sample_labels, body):
        return "cashflow_stmt", ["现金流量表", "经营活动产生的现金流量"], None

    ctx_sq = _squash_text(ctx)
    body_sq = _squash_text(body)
    for typ, groups in STRUCTURAL_RULES:
        # 结构性三表：ctx（标题+表头+样本）∪ 表体全文匹配——合计科目常在长表后部，样本截断会漏。
        # 安全性由标题否决保证：有标题但不含报表名的同形表（范围调整/分季度）进不来；
        # 「禁止表体定型」仅约束签名类规则（会议纪要误定型），会计准则结构词不受此限。
        # 去空白匹配：兼容『产生 /( 使用 )』等断空变体
        if not all(
            any(_blob_has_token(ctx, ctx_sq, k) or _blob_has_token(body, body_sq, k) for k in grp)
            for grp in groups
        ):
            continue
        if any(tok in header_blob for tok in SUBSIDIARY_HEADER_TOKS):
            continue
        if typ == "income_stmt" and _looks_like_entity_kpi_wide_table(headers, sample_labels):
            continue
        if typ == "income_stmt" and _looks_like_non_income_stmt_rows(title_n, headers, sample_labels):
            continue
        title_toks = STMT_TITLE_TOKS.get(typ) or ()
        if ANALYSIS_TITLE_RE.search(title_n):
            # 变动分析/摘要类标题：同形分析表不是报表本体
            continue
        if title_n and not _is_furniture_title(title_n) and title_toks \
                and not any(tok in title_n for tok in title_toks):
            # 有标题但不含对应报表名（单位注记/签字行视同无标题）：结构词命中大概率是范围调整/分季度等同形表
            continue
        return typ, [g[0] for g in groups], None

    hint = None
    hint_score = -1
    # 低置信 hint 额外对去空白 ctx 匹配：docling 常把表头断成「工程 进度」，hint 仅作晋升候选，风险可控
    # 多候选时取关键词总长度最大者，避免泛签名（资源量+储量）抢先窄签名（煤炭资源量+可采储量）
    # 表体参与 hint：经营 KPI 常在第二列（如客车流量），sample_labels 只取首列会漏
    ctx_squash = re.sub(r"\s+", "", ctx)
    body_short = nfkc(text or "")[:4000]
    body_squash = re.sub(r"\s+", "", body_short)
    # 子公司情况表（注册资本/业务性质/公司类型等列）表体常含行业词（配送/零售/医院），
    # 会误命中消费/制药渠道类 hint；SUBSIDIARY_HEADER_TOKS 此前只护三大报表结构规则
    subs_blob = re.sub(r"\s+", "", header_blob) + body_squash
    if sum(1 for tok in SUBSIDIARY_HEADER_TOKS if tok in subs_blob) >= 2:
        return None, [], None
    for typ, kws in TYPE_HINT_SIGNATURES:
        if all(k in ctx or k in ctx_squash or k in body_short or k in body_squash for k in kws):
            score = sum(len(k) for k in kws)
            if score > hint_score:
                hint, hint_score = typ, score
    # 会议/议程表常出现「股权激励」字样，禁止误 hint
    if hint == "equity_incentive" and any(k in title_n for k in ("会议", "议程", "议案")):
        hint = None
    # CAS 通用报表模板零行（赔付/保费/存贷款）不得在非银行/保险报表上抢 hint
    if hint in CAS_STATEMENT_TEMPLATE_HINTS and _cas_statement_template_context(
        title_n, sample_labels, body_short
    ):
        hint = None
    return None, [], hint


def detect_transport_segment(md_text: str, *, title: str = "") -> str | None:
    """交运子业态：highway|port|mixed；证据不足返回 None。"""
    title_n = nfkc(title)
    seg_scores: dict[str, float] = {}
    for seg, kws in TRANSPORT_SEGMENT_HINTS.items():
        hit = [k for k in kws if k in md_text]
        if hit:
            seg_scores[seg] = float(len(hit))
        thit = [h for h in TITLE_TRANSPORT_SEGMENT_HINTS.get(seg, []) if h in title_n]
        if thit:
            seg_scores[seg] = seg_scores.get(seg, 0.0) + len(thit) * 3.0
    if not seg_scores:
        return None
    ranked = sorted(seg_scores, key=lambda k: seg_scores[k], reverse=True)
    top, second = ranked[0], ranked[1] if len(ranked) > 1 else None
    if second and seg_scores[second] >= max(seg_scores[top] * 0.6, 2.0):
        return "mixed"
    return top


def detect_industry(md_text: str, *, title: str = "", pages: int = 0) -> dict:
    scores: dict[str, float] = {}
    matched: dict[str, list[str]] = {}
    short_doc = pages > 0 and pages < 50
    for ind, kws in INDUSTRY_HINTS.items():
        hit = [k for k in kws if k in md_text]
        if not hit:
            continue
        weight = 0.4 if short_doc and ind in ("bank", "insurance", "broker") else 1.0
        scores[ind] = len(hit) * weight
        matched[ind] = hit
    title_n = nfkc(title)
    for ind, hints in TITLE_INDUSTRY_HINTS.items():
        thit = [h for h in hints if h in title_n]
        if thit:
            scores[ind] = scores.get(ind, 0.0) + len(thit) * 3.0
            matched.setdefault(ind, []).extend(thit)
    # 短文档：无「保险/证券/银行」标题时清掉仅靠附注撑起的 insurance/broker/bank（准则模板污染；
    # bank 此前缺席——非金融公司集团财务公司附注的「吸收存款/发放贷款」各 1 次即误中，北新/盾安/电投 Q1 实证）
    if short_doc:
        for fin in ("insurance", "broker", "bank"):
            if scores.get(fin) and not any(h in title_n for h in TITLE_INDUSTRY_HINTS.get(fin, [])):
                scores.pop(fin, None)
                matched.pop(fin, None)
    # 快递/EPC/航司等负向词：交运运营证据不足时清掉或降权
    if scores.get("transport_infrastructure"):
        neg = [k for k in TRANSPORT_NEGATIVE_HINTS if k in md_text or k in title_n]
        tr_body = [k for k in matched.get("transport_infrastructure", [])
                   if k in INDUSTRY_HINTS.get("transport_infrastructure", [])]
        if neg and len(tr_body) < 2:
            scores.pop("transport_infrastructure", None)
            matched.pop("transport_infrastructure", None)
        elif neg and len(neg) >= 2:
            scores["transport_infrastructure"] = scores["transport_infrastructure"] * 0.35
    apply_industry_arbitration(scores, matched, title_n)
    if not scores:
        return {"industry": None, "confidence": 0.0, "matched": {}}
    ranked = sorted(scores, key=lambda k: scores[k], reverse=True)
    top = ranked[0]
    conf = round(scores[top] / max(len(INDUSTRY_HINTS.get(top, []) or TITLE_INDUSTRY_HINTS.get(top, []) or [1]), 1), 2)
    # 低置信不出行业标签：1-2 个弱词命中（如季报仅「合同负债」）判 real_estate/bank 是误导，
    # None 走通用层比错误行业更诚实。阈值 0.15 低于已知最弱合法样本（港股智驾公告 0.25）
    if conf < 0.15:
        return {"industry": None, "confidence": conf, "matched": {k: matched[k] for k in ranked[:3]}}
    out: dict = {
        "industry": top,
        "confidence": min(conf, 1.0),
        "matched": {k: matched[k] for k in ranked[:3]},
    }
    if top == "transport_infrastructure":
        seg = detect_transport_segment(md_text, title=title)
        if seg:
            out["transport_segment"] = seg
    return out


def infer_filing_kind(source: dict | None, pages: int = 0, md_text: str = "") -> str:
    title = nfkc((source or {}).get("title") or "")
    # 本地路径 convert 无 fetch_meta（source.title 为空）：用正文头部特征兜底（封面/重要提示页）
    head = nfkc(md_text or "")[:8000]
    if any(k in title for k in ("全球發售", "全球发售", "招股章程", "招股说明书", "招股書", "PROSPECTUS")):
        return "prospectus"
    if not title and "全球發售" in head and any(k in head for k in ("聯席保薦人", "联席保荐人")):
        return "prospectus"
    if any(k in title for k in ("第一季度", "第一季度报告", "一季报", "一季報")):
        return "q1"
    if any(k in title for k in ("第三季度", "第三季度报告", "三季报", "三季報")):
        return "q3"
    if any(k in title for k in ("第二季度", "第四季度", "季度报告")):
        return "quarter"
    if any(k in title for k in ("半年度", "中期报告", "半年报", "中期報告", "中期簡明", "半年度報告", "中期业绩", "中期業績")):
        return "semi"
    if not title and any(k in head for k in ("中期報告", "中期报告", "中期業績", "中期业绩")):
        return "semi"
    if "六个月" in title or "六個月" in title:
        return "semi"
    if not title and any(k in head for k in ("第一季度报告", "第一季度", "一季报", "一季報")):
        return "q1"
    if not title and any(k in head for k in ("第三季度报告", "第三季度", "三季报", "三季報")):
        return "q3"
    if pages and pages <= 30:
        return "quarter"
    return "annual"


def _is_q1_q3(filing_kind: str | None) -> bool:
    return (filing_kind or "") in ("q1", "q3")


def detect_market(title: str, md_text: str) -> str:
    blob = nfkc(f"{title}\n{md_text[:8000]}")
    hk_markers = ("股份代號", "股份代号", "聯交所", "香港聯合交易所有限公司", "中期報告",
                  "中期報告", "全球發售", "簡明合併", "合併財務狀況表", "年內虧損")
    a_markers = ("年度报告", "半年度报告", "第一季度报告", "第三季度报告", "证券代码", "股票代码",
                 "巨潮资讯", "深圳证券交易所", "上海证券交易所", "合并资产负债表")
    hk_hits = sum(1 for k in hk_markers if k in blob)
    a_hits = sum(1 for k in a_markers if k in blob)
    if hk_hits > a_hits and hk_hits:
        return "hk"
    if a_hits:
        return "a_share"
    return "unknown"


def detect_script(title: str, md_text: str) -> str:
    blob = nfkc(f"{title}\n{md_text[:12000]}")
    hant_markers = "體臺灣網龍業務點與關於為發佈虧損務總額證券簡明聯營"
    hans_markers = "体台业务点与关于为发布亏损务总额证券简明联营"
    hant = sum(blob.count(ch) for ch in hant_markers)
    hans = sum(blob.count(ch) for ch in hans_markers)
    ascii_letters = sum(ch.isascii() and ch.isalpha() for ch in blob)
    cjk = sum("\u4e00" <= ch <= "\u9fff" for ch in blob)
    if ascii_letters >= 80 and cjk < 30:
        return "en"
    if hant and hans:
        return "mixed"
    if hant:
        return "zh_hant"
    if hans or cjk:
        return "zh_hans"
    return "unknown"


def detect_accounting(title: str, md_text: str, market: str) -> str:
    blob = nfkc(f"{title}\n{md_text[:10000]}")
    if market == "hk" or any(k in blob for k in ("合併財務狀況表", "簡明合併", "國際財務報告準則", "国际财务报告准则")):
        return "ifrs_hk"
    if any(k in blob for k in ("合并资产负债表", "母公司资产负债表", "企业会计准则")):
        return "cas"
    return "unknown"


def build_document_profile(
    *,
    title: str,
    md_text: str,
    anomalies: list[dict],
    pages: list[dict],
    tables: list[dict],
    industry: dict,
    filing_kind: str,
) -> dict:
    market = detect_market(title, md_text)
    script = detect_script(title, md_text)
    accounting = detect_accounting(title, md_text, market)
    total_pages = max(len(pages), 1)
    low_text_pages = sum(1 for a in anomalies if a.get("code") == "low_text_page")
    garbled_pages = sum(1 for a in anomalies if a.get("code") == "garbled")
    kangxi_pages = sum(1 for a in anomalies if a.get("code") == "kangxi_compat")
    fitz_tables = sum(1 for t in tables if t.get("track") == "fitz")
    typed_tables = {t.get("type") for t in tables if t.get("type")}
    statement_types = {"balance_sheet", "income_stmt", "cashflow_stmt"}
    novelty_reasons: list[str] = []
    if not (industry.get("industry") or "").strip():
        novelty_reasons.append("industry_unknown")
    if len(typed_tables & statement_types) < 3:
        novelty_reasons.append("statement_signature_gap")
    if script == "en":
        novelty_reasons.append("language_unsupported")
    if low_text_pages / total_pages >= 0.2:
        novelty_reasons.append("scan_heavy")
    if garbled_pages:
        novelty_reasons.append("garbled_pages")
    profile = {
        "market": market,
        "script": script,
        "accounting": accounting,
        "filing_kind": filing_kind,
        "industry": industry.get("industry"),
        "industry_confidence": industry.get("confidence") or 0.0,
        "convert_health": {
            "low_text_pages": low_text_pages,
            "low_text_ratio": round(low_text_pages / total_pages, 4),
            "garbled_pages": garbled_pages,
            "kangxi_pages": kangxi_pages,
            "fitz_table_ratio": round(fitz_tables / max(len(tables), 1), 4),
            "table_count": len(tables),
            "anomaly_codes": [a.get("code") for a in anomalies if a.get("code")],
        },
        "novelty": bool(novelty_reasons),
        "novelty_reasons": novelty_reasons,
    }
    return profile


def build_convert_strategy(profile: dict) -> dict:
    health = profile.get("convert_health") or {}
    flags: list[str] = []
    reasons: list[str] = []
    if (health.get("low_text_ratio") or 0) >= 0.2:
        flags.append("--ocr")
        reasons.append("low_text_page 占比较高，建议 OCR 重转")
    if health.get("garbled_pages"):
        flags.append("--accurate")
        reasons.append("存在 garbled 页面，建议 ACCURATE 精修")
    return {
        "recommended_flags": flags,
        "requires_reconvert": bool(flags),
        "reasons": reasons,
    }


def anomaly_strategy_text(anomaly: dict) -> str:
    code = anomaly.get("code") or "unknown"
    page = anomaly.get("page")
    tag = f"{code}@p{page}" if page else code
    mapping = {
        "low_text_page": "建议 OCR 重转或将相关结论记为 suspect",
        "table_fragment": "改走 key-value / 邻页拼接复核，禁止强行 promote",
        "garbled": "优先 ACCURATE 或缩小到锚点页重转",
        "kangxi_compat": "quote 回验使用 NFKC 归一化文本",
        "missing_chapter_anchors": "依赖 sections + locate，不硬编码章节页码",
        "chapters_from_toc": "目录页仅作提示，正文页需 locate 复核",
    }
    return f"{tag} -> {mapping.get(code, '按异常页人工复核并保留 gaps 诚实状态')}"


UNIT_PAT = re.compile(r"[（(]\s*(?:人民币)?\s*[佰百千万]{0,2}(?:元|特别注明除外|股)[^）)]*[）)]|单位[:：]\s*[佰百千万]{0,2}(?:元|%|股)")
PERIOD_COL_PAT = re.compile(r"(20\d{2})\s*年|本期|上年同期|本年比上年|增减|期末|期初|上年度|报告期")
SEP_ROW_PAT = re.compile(r"^\|[\s:|-]*-[\s:|-]*\|$")  # 分隔行必须含 -，区别于空壳表头行 | | | |


def split_md_row(line: str) -> list[str]:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        s = "|" + s.strip("|") + "|"
    return [c.strip() for c in s.strip("|").split("|")]


def parse_table_schema(block_lines: list[str]) -> dict:
    """markdown 表块 → schema：headers/unit/periods/row_labels/rows(完整)/quality。"""
    rows = [split_md_row(ln) for ln in block_lines
            if ln.strip().startswith("|") and not SEP_ROW_PAT.match(ln.strip())]
    if not rows:
        return {}
    headers = rows[0]
    ncol = len(headers)
    data_rows = [r for r in rows[1:]]
    unit = ""
    m = UNIT_PAT.search(" ".join(block_lines[:3]))
    if m:
        unit = (m.group(0).strip("()（） ") or "").strip() or "元"
    periods: dict[int, str] = {}
    for ci, h in enumerate(headers):
        if PERIOD_COL_PAT.search(h):
            periods[ci] = h
    labels = [r[0] for r in data_rows if r and r[0]]
    stable = all(len(r) == ncol for r in data_rows) if data_rows else False
    return {
        "headers": headers, "unit": unit, "periods": periods,
        "row_labels": labels, "rows": data_rows,
        "quality": {"header_ok": ncol >= 2, "cols_stable": stable, "data_rows": len(data_rows)},
    }


NEW_STMT_PAT = re.compile(
    r"(合并|合併|母公司|\b公司\b).{0,4}(资产负债表|利润表|现金流量表|財務狀況表|損益表|現金流量表)"
    r"|所有者权益变动表|權益變動表|^#{1,3}\s"
)
# 附注小节编号（A 股附注体例级约定）：续表碎片之间不会出现编号标题，出现即阻断合并
NOTE_HEADING_PAT = re.compile(r"[（(][一二三四五六七八九十百\d]+[)）]")
# 续表标题标记：（续）/（續）/ -续 / –續 等——归一化比较用（长城 '合并资产负债表 -续' 实证）
_CONT_TITLE_MARK_RE = re.compile(r"[（(]\s*[续續]\s*[）)]|[-–−]\s*[续續]\s*$")


def _norm_cont_title(ln: str) -> str:
    """行文本去 # 前缀、去 (续) 标记 + 去空白——用于识别「页脚重印的不带续同名标题」。"""
    s = re.sub(r"^#{1,6}\s*", "", nfkc(ln or ""))
    return re.sub(r"\s+", "", _CONT_TITLE_MARK_RE.sub("", s))


def _empty_col_indexes(t: dict) -> list[int]:
    """表内全空列（表头+所有数据行均空）的列下标——docling/fitz 对齐伪影。"""
    lines = [l for l in (t.get("_text") or "").splitlines() if l.strip().startswith("|")]
    rows = [split_md_row(l) for l in lines if not SEP_ROW_PAT.match(l.strip())]
    if not rows:
        return []
    ncol = max(len(r) for r in rows)
    return [ci for ci in range(ncol)
            if not any(ci < len(r) and r[ci].strip() for r in rows)]


def _drop_empty_column(t: dict, ci: int) -> None:
    """从表块中物理剔除全空列（重写 _text 行 + headers/periods/cols）。"""
    new_lines: list[str] = []
    for l in (t.get("_text") or "").splitlines():
        if not l.strip().startswith("|"):
            new_lines.append(l)
            continue
        cells = split_md_row(l)
        keep = cells[:ci] + cells[ci + 1:]
        if SEP_ROW_PAT.match(l.strip()):
            new_lines.append("|" + "|".join(c if c.strip() else "---" for c in keep) + "|")
        else:
            new_lines.append("| " + " | ".join(keep) + " |")
    t["_text"] = "\n".join(new_lines)
    t["cols"] = int(t.get("cols") or 0) - 1
    if t.get("headers") is not None:
        cells = list(t["headers"])
        if ci < len(cells):
            cells = cells[:ci] + cells[ci + 1:]
        t["headers"] = cells
    if t.get("periods"):
        t["periods"] = {(k if k < ci else k - 1): v for k, v in t["periods"].items() if k != ci}


def _norm_heading(ln: str) -> str:
    """标题行归一化：去 #/空白。"""
    return re.sub(r"\s+", "", re.sub(r"^#{1,6}\s*", "", nfkc(ln or "").strip()))


def _own_table_heading(md_lines: list[str], line_no: int) -> str:
    """表块上方最近的 # 标题（跳过空行/页标/家具行；紧邻实质文本则视为无标题）。"""
    for i in range(max(0, line_no - 1), -1, -1):
        ln = (md_lines[i] or "").strip()
        if not ln or ln.startswith("<!--"):
            continue
        if ln.startswith("#"):
            return ln
        if _is_furniture_title(ln):
            continue  # 日期/单位行（平安报表页实证）不遮挡真实标题
        return ""
    return ""


def merge_continued_tables(tables: list[dict], md_lines: list[str]) -> None:
    """跨页续表标记：相邻、同列数、页距≤1，且满足其一——间距间文本含「续」（强信号，允许≤24 行
    表头块）/ 表头相同 / 表头空壳 / 前表为长表且间距≤12（财报长表续片表头常变为新节名）。
    间距间出现新报表标题（合并/母公司XX表、## 标题）或附注小节编号则阻断——相邻的不同表不是续表。"""
    for j in range(1, len(tables)):
        a, b = tables[j - 1], tables[j]
        if b.get("cols") != a.get("cols"):
            # 单侧恰多 1 个全空列（对齐伪影，神华母公司 BS 5列 vs 续片 4列实证）：
            # 剔除后再续链，避免伪列阻断同表跨页合并
            for wide, narrow in ((a, b), (b, a)):
                if wide.get("cols") and narrow.get("cols") \
                        and wide["cols"] - narrow["cols"] == 1:
                    empt = _empty_col_indexes(wide)
                    if len(empt) == 1:
                        _drop_empty_column(wide, empt[0])
            # 续片带稀疏节号前置列（平安 IS p191 col0 仅 三、四、五、六 实证）：
            # 填充率 ≤25% 且均为节号 token → 剔除对齐后再链
            if b.get("cols") - a.get("cols") == 1 and (b.get("rows") or 0) >= 4:
                lines = [l for l in (b.get("_text") or "").splitlines()
                         if l.strip().startswith("|")]
                rows_b = [split_md_row(l) for l in lines if not SEP_ROW_PAT.match(l.strip())]
                filled0 = [r[0] for r in rows_b if r and r[0].strip()]
                if rows_b and len(filled0) <= 0.25 * len(rows_b) and all(
                        re.fullmatch(r"[（(]?[一二三四五六七八九十\d]+[)）、.]*", c.strip())
                        for c in filled0):
                    _drop_empty_column(b, 0)
            if b.get("cols") != a.get("cols"):
                continue
        if (b["page"] - a["page"]) not in (0, 1):
            continue
        gap = b["line"] - a["line_end"]
        if gap > 24:
            continue
        between = nfkc("\n".join(md_lines[a["line_end"] + 1:b["line"]]))
        # 「合并资产负债表（续）」类续表标题含报表名，不能当"新报表"阻断——剔除含「续」的行再判；
        # 报表页脚常重印一遍**不带「续」**的同名标题（神华 p147→p148 实证阻断粘链），
        # 页首 (续) 标题可带 ##/公司名前缀而页脚没有——去(续)归一化后互为包含即视为同款标题，一并剔除；
        # 平安类报表每页页首重印**同一 ## 标题**（无「续」标记，p187→p188 实证）——
        # 与表 a 自身标题相同的标题行亦为页眉回声，一并剔除
        btw_lines = between.splitlines()
        cont_norms = {_norm_cont_title(l) for l in btw_lines if _CONT_TITLE_MARK_RE.search(l)}
        a_own_head = _norm_heading(_own_table_heading(md_lines, a.get("line", 0)))

        def _is_cont_title_echo(l: str) -> bool:
            n = _norm_cont_title(l)
            if len(n) >= 6 and any(n in cn or cn in n for cn in cont_norms if cn):
                return True
            return bool(a_own_head) and len(a_own_head) >= 6 \
                and _norm_heading(l) == a_own_head

        stmt_between = "\n".join(
            l for l in btw_lines if "续" not in l and not _is_cont_title_echo(l)
        )
        if NEW_STMT_PAT.search(stmt_between) or NOTE_HEADING_PAT.search(between):
            continue
        # 独立续表标记：「（续）/(续)/-续/续表/（续上表…」；单字「续」会被标题词「后续/续聘」误中
        # （恒瑞附表4「已上市创新药后续主要临床研发管线」即把附表4 误并进附表3 链）；
        # 「-续」为行尾标记须逐行判（长城 between 末行是单位行，整串 $ 锚失效实证）
        explicit_cont = bool(re.search(r"[（(]\s*续\s*[）)]|[（(]\s*续上|续表", between)) or any(
            re.search(r"[-–−]\s*[续續]\s*$", l) for l in btw_lines)
        ha = a.get("headers") or []
        hb = b.get("headers") or []
        same_header = bool(ha) and bool(hb) and ha[:2] == hb[:2]
        headerless = not hb or all(not c for c in hb[:2])
        long_table = a.get("rows", 0) >= 15 and gap <= 12
        # 前表虽长，但本片带全短格的干净表头 → 同构新表（附表3→附表5 管线表），
        # 续片表头是「列名+数据」粘连长格（fitz）或空壳，纯列名表头即新表，阻断误合并
        if long_table and hb and len(hb) == b.get("cols") and all(c and len(c) <= 12 for c in hb):
            long_table = False
        income_seq = _income_stmt_subject_continuation(a, b)
        # 页界紧贴续片：两表之间仅页标/空行（无任何夹文）——新表出现必伴随标题文字。
        # 续片常无自身表头行，docling 以首数据行为 headers（陕煤 BS/CF 实证，same_header/
        # long_table 均失效）；MD&A KPI 小表也页界相邻无夹文——以两侧行数 ≥4 区分
        # （真续片是长表，KPI 残表仅 1 行数据）。同页零夹文则还须首表头相同
        blank_only = not re.sub(r"<!-- page:\d+ -->|\s", "", between)
        first_hdr_echo = bool(ha and hb and ha[0] and ha[0] == hb[0])
        page_split = blank_only and (
            ((b["page"] - a["page"]) == 1
             and a.get("rows", 0) >= 4 and b.get("rows", 0) >= 4)
            or ((b["page"] - a["page"]) == 0 and first_hdr_echo))
        if explicit_cont or same_header or headerless or long_table or income_seq or page_split:
            b["continued"] = True
            a.setdefault("continued_by", []).append(b["index"])


def compute_chain_heads(tables: list[dict]) -> None:
    """为每个续表片标注 chain_head（所在合并链的头表 index）——类型继承/分表分组的作用域。"""
    prev_of: dict[int, int] = {}
    for t in tables:
        for piece in t.get("continued_by") or []:
            prev_of[piece] = t["index"]
    for t in tables:
        if not t.get("continued"):
            continue
        head = t["index"]
        hops = 0
        while head in prev_of and hops < 128:
            head = prev_of[head]
            hops += 1
        t["chain_head"] = head


def find_tables(md_lines: list[str]) -> list[dict]:
    tables = []
    block: list[tuple[int, str]] = []

    def flush():
        nonlocal block
        if len(block) >= 2:
            geom = parse_table_block([t for _, t in block])
            schema = parse_table_schema([t for _, t in block])
            line_start = block[0][0]
            t = {
                "index": len(tables), "page": page_of_line(md_lines, line_start),
                "line": line_start, "line_end": block[-1][0],
                "rows": geom["rows"], "cols": geom["cols"],
                "type": None, "keywords": [], "type_hint": None,
                "_text": "\n".join(txt for _, txt in block),
            }
            t.update({k: schema[k] for k in ("headers", "unit", "periods", "quality") if k in schema})
            t["sample_labels"] = (schema.get("row_labels") or [])[:8]
            tables.append(t)
        block = []

    for i, ln in enumerate(md_lines):
        if ln.strip().startswith("|"):
            block.append((i, ln))
        else:
            flush()
    flush()
    merge_continued_tables(tables, md_lines)
    compute_chain_heads(tables)
    by_index = {t["index"]: t for t in tables}
    for t in tables:
        if t.get("continued"):
            continue
        pieces = _collect_continued_pieces(t, by_index)
        headers = t.get("headers") or []
        samples: list[str] = []
        for p in pieces:
            samples.extend(p.get("sample_labels") or [])
        title = _guess_table_title(md_lines, t.get("line", 0))
        t["nearby_title"] = title
        body = "\n".join(p.get("_text") or "" for p in pieces)[:8000]
        typ, kws, hint = infer_table_type(
            body, title=title, headers=headers, sample_labels=samples[:12]
        )
        t["type"], t["keywords"], t["type_hint"] = typ, kws, hint
    for t in tables:
        t.pop("_text", None)
    return tables


def detect_anomalies(pages: list[dict], tables: list[dict], chapters: list[dict],
                     convert_meta: dict, md_text: str) -> list[dict]:
    anomalies: list[dict] = []

    def add(code: str, pages_hit: list, severity: str, hint: str):
        if pages_hit:
            anomalies.append({"code": code, "pages": pages_hit[:40], "severity": severity, "hint": hint})

    if not convert_meta:
        add("convert_missing", [0], "blocker", "缺少 convert_meta.json，请先运行 convert")
        return anomalies
    if convert_meta.get("error"):
        anomalies.append({"code": "convert_failed", "pages": [0], "severity": "blocker",
                          "hint": f"docling 转换失败：{convert_meta['error'][:200]}。可尝试 --ocr 或 --accurate 重转"})
    pdf = convert_meta.get("pdf") or {}
    if pdf.get("encrypted"):
        add("encrypted", [0], "blocker", "PDF 加密，需先解密再转换")
    if not pdf.get("bookmarks"):
        add("no_bookmarks", [0], "info", "PDF 无书签，章节定位依赖标题锚点扫描")
    if not chapters:
        add("missing_chapter_anchors", [0], "warn",
            "未命中「第X节/章」章节锚点（目录也未解析出），已回退 sections 子节锚点定位")
    elif chapters[0].get("source") == "toc":
        add("chapters_from_toc", [0], "info",
            "正文章节非标准标题版式，章节树来自目录解析：page 为印刷页码，与 PDF 物理页有偏移；"
            "定位优先用 sections/tables（物理页）")
    low = [p["page"] for p in pages if p.get("chars", 0) < 40 and p.get("tables", 0) == 0]
    add("low_text_page", low, "warn", "文本极少且无表格：可能是扫描图/图片页，该页数据慎用，必要时 --ocr 重转")
    frag = [t["page"] for t in tables if t["cols"] < 2 or t["rows"] < 2]
    add("table_fragment", sorted(set(frag)), "warn", "疑似碎表（<2列或<2行）：提取时改用正文键值对或相邻表拼接")
    longt = [t["page"] for t in tables if t["rows"] > 60]
    add("long_table", sorted(set(longt)), "info", "超长表格：分段读取，注意跨页行归属")
    hdr = [p["page"] for p in pages if p.get("header_footer_hits", 0) >= 3]
    add("header_noise", hdr, "info", "页眉页脚残留较多：提取时忽略版式重复文本")
    add("garbled", list(convert_meta.get("garbled_pages") or []), "warn", "含替换字符（乱码）：该页引用需人工复核")
    add("kangxi_compat", list(convert_meta.get("kangxi_pages") or [])[:40], "info",
        "原文含康熙部首兼容字符，report.md 已 NFKC 归一化；quote 为归一化后文本")
    no_type = [t["page"] for t in tables if t["type"] is None and t["rows"] >= 4]
    add("table_type_unknown", sorted(set(no_type))[:20], "info",
        "较多表格未能按签名归类：plan 阶段需人工读表头确认类型")
    return anomalies


def recompute_page_lines(md_lines: list[str], pages: list[dict]) -> list[dict]:
    """以 report.md 页标记为准重算每页 line_start/line_end（修正旧缓存/防御性对齐）。"""
    by_page = {p.get("page"): p for p in pages}
    marks = [(i, int(m.group(1))) for i, ln in enumerate(md_lines)
             if (m := PAGE_MARKER_RE.match(ln.strip()))]
    for j, (i, pg) in enumerate(marks):
        end = (marks[j + 1][0] - 1) if j + 1 < len(marks) else len(md_lines) - 1
        stat = by_page.setdefault(pg, {"page": pg})
        stat["line_start"] = i
        stat["line_end"] = end
    return [by_page[k] for k in sorted(by_page)]


def summarize_sections(sections: list[dict], tables: list[dict], md_lines: list[str]) -> list[dict]:
    """锚点区段摘要：该锚点页区间内有哪些表、标题，供 plan 快速选源。"""
    out = []
    for i, s in enumerate(sections):
        page_end = (sections[i + 1]["page"] - 1) if i + 1 < len(sections) else s["page"] + 8
        sec_tables = [t["index"] for t in tables if s["page"] <= t["page"] <= max(s["page"], page_end)]
        out.append({"key": s["key"], "page": s["page"], "page_end": page_end,
                    "tables": sec_tables[:12], "table_count": len(sec_tables),
                    "from_toc": s.get("from_toc", False)})
    return out


def build_priority(tables: list[dict], sections: list[dict], industry: str | None) -> list[dict]:
    """coverage-checklist 分组 → 入口指引。confidence: table(结构性/签名) > section(锚点) > keyword。"""
    sec_by_key = {s["key"]: s for s in sections}
    out = []
    for g in PRIORITY_GROUPS_BASE:
        sources = []
        for typ in g["tables"]:
            for t in tables:
                if t.get("type") == typ and t.get("rows", 0) >= 3:
                    sources.append({"kind": "table", "ref": t["index"], "page": t["page"],
                                    "type": typ, "confidence": "high" if typ in ("balance_sheet", "income_stmt", "cashflow_stmt") else "medium",
                                    "headers": (t.get("headers") or [])[:4]})
        for key in g["sections"]:
            s = sec_by_key.get(key)
            if s:
                sources.append({"kind": "section", "ref": key, "page": s["page"],
                                "confidence": "low" if s.get("from_toc") else "medium"})
        out.append({"group": g["group"], "label": g["label"], "sources": sources[:16]})
    ext = INDUSTRY_EXT_GROUPS.get(industry or "")
    if ext:
        sources = [{"kind": "keyword", "ref": kw, "confidence": "keyword"} for kw in ext["keywords"]]
        for typ in ext.get("tables") or []:
            for t in tables:
                if t.get("type") == typ and t.get("rows", 0) >= 3:
                    sources.append({"kind": "table", "ref": t["index"], "page": t["page"],
                                    "type": typ, "confidence": "medium",
                                    "headers": (t.get("headers") or [])[:4]})
        out.append({"group": ext["group"], "label": ext["label"], "sources": sources[:16]})
    return out


def annotate_table_tracks(tables: list[dict], fitz_manifest: dict | None) -> None:
    """按 fitz_tables.json 的页内顺序标注每张表来源轨道（fitz=几何零幻觉 / docling）。"""
    if not fitz_manifest:
        return
    pages = fitz_manifest.get("pages") or {}
    by_page: dict[int, list[dict]] = {}
    for t in tables:
        t.setdefault("track", "docling")
        by_page.setdefault(t.get("page") or 0, []).append(t)
    for page_key, ents in pages.items():
        try:
            p = int(page_key)
        except (TypeError, ValueError):
            continue
        orders = {int(e.get("order", -1)) for e in ents}
        seq = sorted(by_page.get(p, []), key=lambda t: t.get("line") or 0)
        for k, t in enumerate(seq):
            if k in orders:
                t["track"] = "fitz"


def build_meta(sha: str, md_text: str, pages: list[dict], convert_meta: dict, source: dict,
               fitz_manifest: dict | None = None) -> dict:
    md_lines = md_text.split("\n")
    pages = recompute_page_lines(md_lines, pages)
    chapters = find_chapters(md_lines)
    sections = find_sections(md_lines, chapters)
    tables = find_tables(md_lines)
    annotate_table_tracks(tables, fitz_manifest)
    anomalies = detect_anomalies(pages, tables, chapters, convert_meta, md_text)
    pdf = (convert_meta or {}).get("pdf") or {}
    doc_pages = pdf.get("pages") or len(pages)
    src = source or {}
    industry = detect_industry(md_text, title=src.get("title") or "", pages=doc_pages)
    filing_kind = infer_filing_kind(src, doc_pages, md_text)
    profile = build_document_profile(
        title=src.get("title") or "",
        md_text=md_text,
        anomalies=anomalies,
        pages=pages,
        tables=tables,
        industry=industry,
        filing_kind=filing_kind,
    )
    return {
        "cache_id": sha,
        "generated_at": now_iso(),
        "source": src,
        "filing_kind": filing_kind,
        "industry_hint": industry,
        "document_profile": profile,
        "doc": {
            "pages": doc_pages,
            "chars": len(md_text),
            "table_count": len(tables),
            "bookmarks": len(pdf.get("bookmarks") or []),
            "docling_version": (convert_meta or {}).get("docling_version"),
            "table_mode": (convert_meta or {}).get("table_mode"),
            "seconds": (convert_meta or {}).get("seconds"),
        },
        "chapters": chapters,
        "sections": sections,
        "section_summaries": summarize_sections(sections, tables, md_lines),
        "priority": build_priority(tables, sections, industry.get("industry")),
        "tables": tables,
        "pages": pages,
        "anomalies": anomalies,
    }


def meta_summary_text(meta: dict) -> str:
    src = meta.get("source") or {}
    doc = meta.get("doc") or {}
    ind = meta.get("industry_hint") or {}
    out = [
        f"cache_id: {meta.get('cache_id')} | 页数: {doc.get('pages')} | 表格: {doc.get('table_count')}",
        f"来源: {src.get('title') or '本地 PDF'} symbol={src.get('symbol') or '-'} 报告期={src.get('report_date') or '-'}",
    ]
    if ind.get("industry"):
        top_kw = (ind.get("matched") or {}).get(ind["industry"], [])
        out.append(f"行业: {ind['industry']} (置信 {ind.get('confidence')}；特征词 {','.join(top_kw[:5])})")
    profile = meta.get("document_profile") or {}
    if profile:
        out.append(
            "画像: "
            f"market={profile.get('market') or '-'} "
            f"script={profile.get('script') or '-'} "
            f"accounting={profile.get('accounting') or '-'} "
            f"filing_kind={profile.get('filing_kind') or meta.get('filing_kind') or '-'} "
            f"novelty={'yes' if profile.get('novelty') else 'no'}"
        )
    ch = meta.get("chapters") or []
    if ch:
        tag = "印刷页" if ch[0].get("printed_page") else "p"
        out.append("章节: " + "；".join(
            f"{c['anchor']}({tag}{c['page']}~{c['page_end'] or '?'})" for c in ch[:12]))
    else:
        out.append("章节: 未命中标准锚点（见 anomalies.missing_chapter_anchors）")
    secs = meta.get("sections") or []
    if secs:
        out.append("子节锚点: " + "；".join(f"{s['key']}(p{s['page']})" for s in secs))
    tt = {}
    for t in meta.get("tables") or []:
        if t.get("type"):
            tt[t["type"]] = tt.get(t["type"], 0) + 1
    if tt:
        out.append("表格类型: " + "；".join(f"{k}×{v}" for k, v in sorted(tt.items())))
    pr = meta.get("priority") or []
    if pr:
        lines = []
        for g in pr:
            hi = [s for s in g.get("sources") or [] if s.get("kind") in ("table", "section")]
            if hi:
                lines.append(f"{g['group']}→" + ",".join(
                    (f"表{s['ref']}(p{s['page']})" if s["kind"] == "table" else f"{s['ref']}(p{s['page']})") for s in hi[:3]))
        if lines:
            out.append("优先指引: " + " | ".join(lines[:10]))
    an = meta.get("anomalies") or []
    if an:
        out.append("异常: " + "；".join(f"{a['code']}[{a['severity']}]" for a in an))
    else:
        out.append("异常: 无")
    return "\n".join(out)


def inherit_industry_from_cache(sha: str, meta: dict) -> dict:
    """短文档行业回退：季报/中报/HK 公告关键词不足（industry=null）时，按 symbol 继承
    同发行人年报的 industry（宇通Q1/电投Q1/盾安Q1 七家 null 实证）。置信上限 0.3 + 继承标记，
    年报/招股书不继承（未适配行业应显式 null + review warning，而非静默补齐）。"""
    ih = meta.get("industry_hint") or {}
    if ih.get("industry") or ih.get("inherited_from"):
        return meta
    if (meta.get("filing_kind") or "") in ("annual", "prospectus"):
        return meta
    symbol = str((meta.get("source") or {}).get("symbol") or "").strip()
    if not symbol:
        return meta
    idx = read_json(cache_root() / "index.json", {}) or {}
    for sha2, ent in sorted((idx.get("entries") or {}).items()):
        if sha2 == sha or str((ent or {}).get("symbol") or "").strip() != symbol:
            continue
        m2 = read_json(entry_dir(sha2) / "meta.json", None)
        if not m2 or (m2.get("filing_kind") or "") != "annual":
            continue
        ind2 = ((m2.get("industry_hint") or {}).get("industry") or "").strip()
        if not ind2:
            continue
        ih["industry"] = ind2
        ih["confidence"] = 0.3
        ih["inherited_from"] = {
            "cache_id": sha2, "filing_kind": "annual",
            "title": ((m2.get("source") or {}).get("title") or "")[:60],
        }
        meta["industry_hint"] = ih
        (meta.get("document_profile") or {}).update(
            {"industry": ind2, "industry_confidence": 0.3})
        return meta
    return meta


def cmd_scan(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(prog="wm_report.py scan", description="内容理解 → meta.json")
    ap.add_argument("sha12")
    ap.add_argument("--force", action="store_true", help="重扫")
    ap.add_argument("--summary", action="store_true", help="打印紧凑摘要")
    args = ap.parse_args(argv)

    d = entry_dir(args.sha12)
    md_path = d / "report.md"
    if not md_path.is_file():
        raise SystemExit(f"缓存 {args.sha12} 无 report.md，请先 convert")
    meta_path = d / "meta.json"
    if meta_path.is_file() and not args.force and not args.summary:
        print(json.dumps({"cache_id": args.sha12, "cached": True, "meta": str(meta_path)}, ensure_ascii=False))
        return

    md_text = md_path.read_text(encoding="utf-8")
    pages = read_json(d / "pages.json", []) or []
    convert_meta = read_json(d / "convert_meta.json", {}) or {}
    fitz_manifest = read_json(d / "fitz_tables.json")
    fetch_meta = read_json(d / "fetch_meta.json", {})
    source = fetch_meta.get("source") or index_load()["entries"].get(args.sha12, {}).get("source") or {}
    meta = build_meta(args.sha12, md_text, pages, convert_meta, source, fitz_manifest=fitz_manifest)
    meta = inherit_industry_from_cache(args.sha12, meta)
    write_json(meta_path, meta)
    index_upsert(args.sha12, scanned=True)
    if args.summary:
        print(meta_summary_text(meta))
    else:
        print(json.dumps({"cache_id": args.sha12, "meta": str(meta_path),
                          "sections": len(meta["sections"]), "tables": len(meta["tables"]),
                          "chapters": len(meta["chapters"]), "anomalies": len(meta["anomalies"])},
                         ensure_ascii=False))


# --------------------------------------------------------------------------
# ③ extract-tables：全表逐行确定性预提取 → records.json
# --------------------------------------------------------------------------

def build_records(md_lines: list[str], tables: list[dict]) -> list[dict]:
    """每表每数据行 → record（行级溯源）。

    类型只从**本合并链的链头**继承（chain_head）——禁止全局沿用，防止跨链类型传染
    （如股东表定型后，附注区被误连的无关长表整片继承 top_holders）。链头无类型 → 整链 untyped。
    """
    records = []
    type_by_index = {t["index"]: t.get("type") for t in tables}
    for t in tables:
        typ = t.get("type")
        if typ is None and t.get("continued"):
            typ = type_by_index.get(t.get("chain_head"))
        block = md_lines[t["line"]:t["line_end"] + 1]
        schema = parse_table_schema(block)
        headers = schema.get("headers") or []
        periods = schema.get("periods") or {}
        unit = schema.get("unit") or ""
        for r in schema.get("rows") or []:
            # 科目列定位：首列空时取首个非空且非纯数值的 cell 作 label（fitz 长格报表
            # 常见形态——首列空、科目在 col1，死取 r[0] 会整表行级丢弃，地产年报实证）
            label = (r[0] if r else "").strip()
            label_col = 0
            if not label or label in ("项目", "科目", "附注"):
                alt = next(((ci, c.strip()) for ci, c in enumerate(r)
                            if c.strip() and c.strip() not in ("项目", "科目", "附注")
                            and not PURE_NUM_RE.match(c.strip())), None)
                if alt is None:
                    continue
                label_col, label = alt
            values = []
            for ci, cell in enumerate(r, start=0):
                if ci <= label_col:
                    continue
                v = cell.strip()
                if not v:
                    continue
                values.append({"col": ci, "value": v,
                               "period": periods.get(ci), "header": headers[ci] if ci < len(headers) else ""})
            if not values or not any(re.search(r"[\d%]", v["value"]) for v in values):
                continue  # 纯文本行（说明/小标题）不进 records
            records.append({
                "table": t["index"], "page": t["page"], "type": typ,
                "row_label": label, "label_norm": re.sub(r"\s+", "", label),
                "values": values, "unit": unit,
                "headers": headers[:6],
            })
    return records


def cmd_extract_tables(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(prog="wm_report.py extract-tables", description="全表逐行预提取 → records.json")
    ap.add_argument("sha12")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)

    d = entry_dir(args.sha12)
    md_path = d / "report.md"
    meta = read_json(d / "meta.json")
    if not md_path.is_file() or not meta:
        raise SystemExit(f"缓存 {args.sha12} 缺 report.md/meta.json，请先 convert + scan")
    out_path = d / "records.json"
    if out_path.is_file() and not args.force:
        recs = read_json(out_path, [])
        print(json.dumps({"cache_id": args.sha12, "cached": True, "records": len(recs),
                          "path": str(out_path)}, ensure_ascii=False))
        return
    md_lines = md_path.read_text(encoding="utf-8").split("\n")
    records = build_records(md_lines, meta.get("tables") or [])
    write_json(out_path, records)
    index_upsert(args.sha12, records=len(records))
    typed = {}
    for r in records:
        if r.get("type"):
            typed[r["type"]] = typed.get(r["type"], 0) + 1
    print(json.dumps({"cache_id": args.sha12, "records": len(records),
                      "by_type": typed, "path": str(out_path)}, ensure_ascii=False))


# --------------------------------------------------------------------------
# ③ locate：关键词 → 页码+行区间
# --------------------------------------------------------------------------


def expand_need_keywords(need: str) -> list[str]:
    n = nfkc(need).strip()
    variants = KEYWORD_VARIANTS.get(n) or synonym_variants(n)
    if variants:
        return list(variants)
    out = [n]
    # 简繁常见单字：货/貨 价/價 账/賬 现/現 储/儲
    swapped = (
        n.replace("货", "貨").replace("价", "價").replace("账", "賬")
        .replace("现", "現").replace("储", "儲").replace("负", "負")
        .replace("债", "債").replace("收", "收").replace("应", "應")
    )
    if swapped != n:
        out.append(swapped)
    return out


def locate_in_records(recs: list, keyword: str, max_hits: int = 20) -> list[dict]:
    kw_n = re.sub(r"\s+", "", nfkc(keyword))
    hits = []
    for r in recs:
        label_norm = r.get("label_norm") or re.sub(r"\s+", "", r.get("row_label") or "")
        if kw_n not in label_norm:
            continue
        hits.append({
            "page": r.get("page"),
            "table": r.get("table"),
            "type": r.get("type"),
            "row_label": r.get("row_label"),
            "unit": r.get("unit"),
            "values": (r.get("values") or [])[:6],
        })
        if len(hits) >= max_hits:
            break
    return hits


def locate_in_md(md_lines: list[str], keyword: str, max_hits: int = 20) -> list[dict]:
    kw_n = nfkc(keyword)
    hits = []
    for i, ln in enumerate(md_lines):
        if kw_n not in nfkc(ln):
            continue
        hits.append({
            "page": page_of_line(md_lines, i),
            "line": i + 1,
            "text": ln.strip()[:200],
        })
        if len(hits) >= max_hits:
            break
    return hits


def split_md_pages(md_lines: list[str]) -> dict[int, list[str]]:
    pages: dict[int, list[str]] = {}
    current = 0
    buf: list[str] = []
    for ln in md_lines:
        m = PAGE_MARKER_RE.match(ln.strip())
        if m:
            if current:
                pages[current] = buf
            current = int(m.group(1))
            buf = [ln]
        else:
            buf.append(ln)
    if current:
        pages[current] = buf
    return pages


def slice_pages(pages: dict[int, list[str]], hit_pages: list[int], pad: int = 1) -> dict[int, str]:
    wanted: set[int] = set()
    known = set(pages)
    for p in hit_pages:
        if not p:
            continue
        for q in range(p - pad, p + pad + 1):
            if q in known:
                wanted.add(q)
    return {p: "\n".join(pages[p]) for p in sorted(wanted)}


def quote_on_page(quote: str, page_text: str) -> bool:
    q = re.sub(r"\s+", "", nfkc(quote or ""))
    t = re.sub(r"\s+", "", nfkc(page_text or ""))
    return bool(q) and q in t


def classify_extract_status(record_hits: list, md_hits: list, ambiguous_page_cap: int = 8) -> str:
    if not record_hits and not md_hits:
        return "not_in_pdf"
    pages = {h.get("page") for h in record_hits + md_hits if h.get("page")}
    if not record_hits and len(pages) > ambiguous_page_cap:
        return "ambiguous"
    return "found"


def build_extract_query_item(
    query: str,
    record_hits: list,
    md_hits: list,
    page_texts: dict[int, str],
) -> dict:
    status = classify_extract_status(record_hits, md_hits)
    primary = None
    quote = ""
    selected_value = ""
    if record_hits:
        primary = record_hits[0]
        vals = primary.get("values") or []
        first_val = vals[0].get("value") if vals and isinstance(vals[0], dict) else ""
        selected_value = str(first_val or "")
        quote = " ".join(x for x in [primary.get("row_label"), str(first_val or "")] if x).strip()
    elif md_hits:
        primary = md_hits[0]
        quote = (primary.get("text") or "").strip()
    page = (primary or {}).get("page")
    page_text = page_texts.get(page or -1, "")
    if quote and page_text and not quote_on_page(quote, page_text):
        quote = ""
    return {
        "id": _slug(query),
        "query": query,
        "value": selected_value or None,
        "unit": (record_hits[0].get("unit") if record_hits else None),
        "page": page,
        "quote": quote or None,
        "status": status,
        "record_hits": record_hits,
        "md_hits": md_hits[:8],
        "note": "value 由 Agent 按 quote/切片填写；禁止写入 PDF 外数字",
    }


def cmd_locate(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(prog="wm_report.py locate", description="关键词 → 页码命中（records 模式按科目行检索）")
    ap.add_argument("sha12")
    ap.add_argument("keywords", nargs="+")
    ap.add_argument("--max-hits", type=int, default=20)
    ap.add_argument("--records", action="store_true", help="在 records.json 的行科目中检索（行级数据）")
    args = ap.parse_args(argv)

    d = entry_dir(args.sha12)
    if args.records:
        recs = read_json(d / "records.json", [])
        if not recs:
            raise SystemExit(f"缓存 {args.sha12} 无 records.json，请先 extract-tables")
        result = {kw: locate_in_records(recs, kw, args.max_hits) for kw in args.keywords}
        print(json.dumps({"cache_id": args.sha12, "mode": "records", "hits": result}, ensure_ascii=False, indent=1))
        return

    md_path = d / "report.md"
    if not md_path.is_file():
        raise SystemExit(f"缓存 {args.sha12} 无 report.md，请先 convert")
    md_lines = md_path.read_text(encoding="utf-8").split("\n")
    result = {kw: locate_in_md(md_lines, kw, args.max_hits) for kw in args.keywords}
    print(json.dumps({"cache_id": args.sha12, "hits": result}, ensure_ascii=False, indent=1))


def cmd_extract_query(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py extract-query",
        description="个性化抽取：locate → 页切片 → adhoc JSON（value 留空给 Agent；禁止写入 PDF 外数字）",
    )
    ap.add_argument("sha12")
    ap.add_argument("--need", action="append", dest="needs", required=True, help="查询项，可重复")
    ap.add_argument("--pad", type=int, default=1, help="命中页前后各保留页数")
    ap.add_argument("--max-hits", type=int, default=20)
    ap.add_argument("--out", default="", help="adhoc.json 输出路径；默认写入缓存 adhoc-{ts}/adhoc.json")
    args = ap.parse_args(argv)

    d = entry_dir(args.sha12)
    md_path = d / "report.md"
    if not md_path.is_file():
        raise SystemExit(f"缓存 {args.sha12} 无 report.md，请先 convert（港股 typed 表可空，L2 仍要跑）")
    md_lines = md_path.read_text(encoding="utf-8").split("\n")
    recs = read_json(d / "records.json", []) or []
    pages = split_md_pages(md_lines)

    items = []
    all_hit_pages: list[int] = []
    for need in args.needs:
        rec_hits: list[dict] = []
        md_hits: list[dict] = []
        seen_md: set[tuple] = set()
        for kw in expand_need_keywords(need):
            if recs:
                rec_hits.extend(locate_in_records(recs, kw, args.max_hits))
            for h in locate_in_md(md_lines, kw, args.max_hits):
                key = (h.get("page"), h.get("line"))
                if key in seen_md:
                    continue
                seen_md.add(key)
                md_hits.append(h)
        rec_hits = rec_hits[: args.max_hits]
        md_hits = md_hits[: args.max_hits]
        hit_pages = [h.get("page") for h in rec_hits + md_hits if h.get("page")]
        all_hit_pages.extend(hit_pages)
        slices = slice_pages(pages, [p for p in hit_pages if p], pad=args.pad)
        items.append(build_extract_query_item(need, rec_hits, md_hits, slices))

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = d / f"adhoc-{ts}"
    slice_dir = out_dir / "slices"
    slice_dir.mkdir(parents=True, exist_ok=True)
    unique_pages = sorted({p for p in all_hit_pages if p})
    written_slices = slice_pages(pages, unique_pages, pad=args.pad)
    slice_files = []
    for p, text in written_slices.items():
        fp = slice_dir / f"page-{p}.md"
        fp.write_text(text, encoding="utf-8")
        slice_files.append(str(fp))

    payload = {
        "cache_id": args.sha12,
        "created_at": now_iso(),
        "needs": args.needs,
        "items": items,
        "slices": slice_files,
        "note": "status=found 的 quote 须为该页原文；Web/东财数字不得写入本文件",
    }
    out_path = Path(args.out).expanduser() if args.out else out_dir / "adhoc.json"
    write_json(out_path, payload)
    print(json.dumps({
        "cache_id": args.sha12,
        "path": str(out_path),
        "items": [{"query": it["query"], "status": it["status"], "page": it["page"]} for it in items],
    }, ensure_ascii=False, indent=1))


# --------------------------------------------------------------------------
# ④b resolve-fields：按需字段 resolve → result-{ts}/fields/*.json
# --------------------------------------------------------------------------

def _norm_label(s: str) -> str:
    return re.sub(r"\s+", "", nfkc(s or ""))


def _field_id_from_need(need: str) -> str:
    """
    字段 id 需要可枚举且稳定；不能直接复用 `_slug(need)`（中文会变成 `table`）。
    """
    base = _slug(need)
    if base != "table":
        return base
    raw = nfkc(need).encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()[:10]
    return f"field_{h}"


def _value_has_number(s: str) -> bool:
    return bool(re.search(r"[\d%]", s or ""))


def _select_value(values: list[dict], *, period: str | None = None, column: str | None = None) -> tuple[str, str]:
    """
    values: records.json 的 values[]（{value, period, header}）
    return: (value, chosen_period_or_header_hint)
    """
    if not values:
        return "", ""
    period_n = nfkc(period or "").strip()
    col_n = nfkc(column or "").strip()

    numeric = [v for v in values if _value_has_number(str(v.get("value") or ""))]
    cand = numeric or values

    if period_n:
        for v in cand:
            if period_n and (
                (v.get("period") and period_n in nfkc(str(v.get("period") or ""))) or
                (v.get("header") and period_n in nfkc(str(v.get("header") or "")))
            ):
                return str(v.get("value") or ""), (v.get("period") or v.get("header") or "")

    if col_n:
        for v in cand:
            if col_n and v.get("header") and col_n in nfkc(str(v.get("header") or "")):
                return str(v.get("value") or ""), (v.get("period") or v.get("header") or "")

    # 默认：选择“量级最大”的数值单元（避免把注记序号/括号数字误当主金额）。
    def _to_abs_float(x: Any) -> float:
        raw = nfkc(str(x or "")).replace(",", "")
        # 提取第一个形如 -12 / 12.3 的数字
        m = re.search(r"[-+]?\d+(?:\.\d+)?", raw)
        if not m:
            return -1.0
        try:
            return abs(float(m.group(0)))
        except ValueError:
            return -1.0

    best = max(cand, key=lambda v: _to_abs_float(v.get("value")))
    return str(best.get("value") or ""), (best.get("period") or best.get("header") or "")


def _page_texts_from_md_lines(md_lines: list[str]) -> dict[int, str]:
    pages = split_md_pages(md_lines)
    out: dict[int, str] = {}
    for p, lines in pages.items():
        out[p] = "\n".join(lines)
    return out


def _latest_result_dir(sha12: str) -> Path:
    d = entry_dir(sha12)
    dirs = sorted([p for p in d.glob("result-*") if p.is_dir()], key=lambda p: p.name)
    if not dirs:
        raise SystemExit(f"缓存 {sha12} 无 result-* 目录，请先 materialize-tables")
    return dirs[-1]


def _build_records_index(records: list[dict]) -> dict[tuple[int, int, str], list[dict]]:
    """
    key = (page, table, label_norm)
    用于 L1 typed row → records 的确定性取值。
    """
    idx: dict[tuple[int, int, str], list[dict]] = {}
    for rec in records or []:
        try:
            page = int(rec.get("page") or 0)
            table = int(rec.get("table") or 0)
        except (TypeError, ValueError):
            continue
        ln = rec.get("label_norm") or _norm_label(rec.get("row_label") or "")
        key = (page, table, ln)
        idx.setdefault(key, []).append(rec)
    return idx


def _best_matching_value_from_records(
    records_index: dict[tuple[int, int, str], list[dict]],
    *,
    need_label_norm: str,
    page: int,
    table: int,
    period: str | None,
    column: str | None,
) -> dict | None:
    key = (int(page), int(table), need_label_norm)
    recs = records_index.get(key) or []
    if not recs:
        return None
    # 同一行理论上只有一条 record；遇到多条保留第一个以保持确定性
    rec = recs[0]
    values = rec.get("values") or []
    value, hint = _select_value(values, period=period, column=column)
    if not value:
        return None
    chosen_period = (nfkc(hint or "") or nfkc(period or "")).strip()
    return {
        "value": value,
        "period": chosen_period,
        "unit": rec.get("unit") or "",
        "header_hint": hint,
        "row_label": rec.get("row_label") or "",
        "record_source": {"page": page, "table": table},
    }


def _locate_records_hits(records: list[dict], need: str, *, max_hits: int = 20) -> list[dict]:
    hits: list[dict] = []
    seen: set[tuple[int, int, str]] = set()
    for kw in expand_need_keywords(need):
        for h in locate_in_records(records, kw, max_hits=max_hits):
            key = (int(h.get("page") or 0), int(h.get("table") or 0), _norm_label(h.get("row_label") or ""))
            if key in seen:
                continue
            seen.add(key)
            hits.append(h)
            if len(hits) >= max_hits:
                return hits
    return hits


def _find_result_table_file_by_record_table_index(result_dir: Path, manifest: dict, rec_table_idx: int) -> tuple[str, str] | tuple[None, None]:
    """
    通过 result 中任意 tables/*.json 的 provenance.tables 映射回原表文件。
    用于 L2 record_hits -> FieldRecord.source.file。
    """
    catalog = (manifest.get("catalog") or {}).get("tables") or []
    for ent in catalog:
        rid = ent.get("id")
        f = ent.get("file")
        if not rid or not f:
            continue
        obj = read_json(result_dir / f, {}) or {}
        prov_tables = ((obj.get("provenance") or {}).get("tables") or [])
        if any(int(x or 0) == int(rec_table_idx) for x in prov_tables):
            return rid, f
    return None, None


def cmd_resolve(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py resolve",
        description="按需字段 resolve：L1（typed 表 verdict=pass）→ records → 正文 locate；落盘 fields/*.json 可被外界枚举复用。",
    )
    ap.add_argument("sha12")
    ap.add_argument("--need", action="append", dest="needs", required=True, help="查询字段，可重复")
    ap.add_argument("--result", default="", help="指定 result-* 目录名；不传则取最新")
    ap.add_argument("--period", default="", help="期间消歧（如 2025 或 2025-12-31），可选")
    ap.add_argument("--column", default="", help="列消歧（如 期末/期初/本年发生额），可选")
    ap.add_argument("--write-fields", action="store_true", help="写入 result-{ts}/fields 并更新 manifest.catalog.fields")
    ap.add_argument("--max-hits", type=int, default=20)
    args = ap.parse_args(argv)

    d = entry_dir(args.sha12)
    md_path = d / "report.md"
    if not md_path.is_file():
        raise SystemExit(f"缓存 {args.sha12} 缺 report.md，请先 convert")
    records = read_json(d / "records.json", []) or []
    md_lines = md_path.read_text(encoding="utf-8").split("\n")
    page_texts = _page_texts_from_md_lines(md_lines)
    records_index = _build_records_index(records)
    need_period = args.period.strip() or None
    need_column = args.column.strip() or None

    result_dir = _latest_result_dir(args.sha12) if not args.result else (d / args.result)
    manifest_path = result_dir / "manifest.json"
    quality_path = result_dir / "quality.json"
    if not manifest_path.is_file():
        raise SystemExit(f"{result_dir}/manifest.json 不存在，请先 materialize-tables")
    manifest = read_json(manifest_path, {}) or {}

    quality = read_json(quality_path, {}) if quality_path.is_file() else None
    pass_table_ids = None
    if quality is not None:
        pass_table_ids = {
            t.get("id") for t in (quality.get("tables") or []) if (t.get("verdict") or "") == "pass"
        }

    # L1：扫描 verdict=pass 且 table.record_type 非空的 typed tables（用于字段级确定性）
    typed_tables: list[dict] = []
    for ent in (manifest.get("catalog") or {}).get("tables") or []:
        tid = ent.get("id")
        rel_file = ent.get("file")
        if not tid or not rel_file:
            continue
        if pass_table_ids is not None and tid not in pass_table_ids:
            continue
        obj = read_json(result_dir / rel_file, {}) or {}
        if obj.get("record_type") is None:
            continue
        typed_tables.append({"table_id": tid, "file": rel_file, "obj": obj})

    # 需要写盘的 manifest.catalog.fields
    if args.write_fields:
        fields_dir = result_dir / "fields"
        fields_dir.mkdir(parents=True, exist_ok=True)
        catalog = manifest.setdefault("catalog", {})
        catalog.setdefault("fields", [])
        existing_fields = {f.get("id") for f in catalog.get("fields") or [] if isinstance(f, dict)}
    else:
        existing_fields = set()

    out_items = []
    for need in args.needs:
        need_variants = expand_need_keywords(need)
        need_norms = [_norm_label(v) for v in need_variants]

        field_id = _field_id_from_need(need)
        chosen = None

        # ---------- L1 ----------
        # 优先 exact match（确定性），再退化成 substring match
        for nt, norm_need in zip(need_variants, need_norms):
            for tt in typed_tables:
                obj = tt["obj"]
                rows = obj.get("rows") or []
                for row in rows:
                    row_item = row.get("item") or ""
                    row_norm = _norm_label(row_item)
                    if row_norm == norm_need:
                        src = row.get("source") or {}
                        page = int(src.get("page") or 0)
                        table_idx = int(src.get("table") or 0)
                        rec_sel = _best_matching_value_from_records(
                            records_index,
                            need_label_norm=norm_need,
                            page=page,
                            table=table_idx,
                            period=need_period,
                            column=need_column,
                        )
                        if rec_sel:
                            quote_src = (src.get("quote") or "").strip()
                            quote_fallback = f"{row_item} {rec_sel['value']}".strip()
                            quote = quote_src or quote_fallback
                            pt = page_texts.get(page) or ""
                            ok = quote_on_page(quote, pt)
                            if not ok:
                                # 部分 table markdown 会对千分位/中英文逗号做格式化差异；
                                # 为避免“证据存在但字符串不完全一致”误判，允许逗号剔除的二次匹配。
                                q2 = quote.replace(",", "").replace("，", "")
                                pt2 = pt.replace(",", "").replace("，", "")
                                ok = quote_on_page(q2, pt2)
                            # 若 typed 表的 quote 与 report.md slice 不完全一致，则回退到可构造的确定性 quote。
                            if (not ok) and quote_src and quote_fallback:
                                ok2 = quote_on_page(quote_fallback, pt)
                                if (not ok2):
                                    q2 = quote_fallback.replace(",", "").replace("，", "")
                                    pt2 = pt.replace(",", "").replace("，", "")
                                    ok2 = quote_on_page(q2, pt2)
                                if ok2:
                                    quote = quote_fallback
                                    ok = True
                            if not ok:
                                # 最后兜底：允许 markdown 中 cell 拼接符（如 `|`）导致子串匹配失败；
                                # 若 quote 中“数值 token”全部出现在该页文本中，则认为证据可复核。
                                q_toks = set(_numeric_tokens(quote))
                                pt_toks = set(_numeric_tokens(pt))
                                if q_toks and q_toks.issubset(pt_toks):
                                    ok = True
                            status = "found" if ok else "ambiguous"
                            chosen = {
                                "field_id": field_id,
                                "label": need,
                                "value": rec_sel["value"],
                                "unit": rec_sel.get("unit") or "",
                                "period": rec_sel.get("period") or "",
                                "layer": "L1",
                                "method": "record_map",
                                "status": status,
                                "source": {
                                    "cache_id": args.sha12,
                                    "result_dir": result_dir.name,
                                    "page": page,
                                    "table": table_idx,
                                    "quote": quote if ok else None,
                                    "file": tt.get("file"),
                                },
                                "operation_id": f"{SKILL_ID}.resolve",
                            }
                            break
                if chosen:
                    break
            if chosen:
                break

        if not chosen:
            # substring fallback（不引入随机：按 typed_tables 顺序取第一个）
            for norm_need in need_norms:
                for tt in typed_tables:
                    rows = tt["obj"].get("rows") or []
                    for row in rows:
                        row_item = row.get("item") or ""
                        row_norm = _norm_label(row_item)
                        if norm_need and norm_need in row_norm:
                            src = row.get("source") or {}
                            page = int(src.get("page") or 0)
                            table_idx = int(src.get("table") or 0)
                            rec_sel = _best_matching_value_from_records(
                                records_index,
                                need_label_norm=_norm_label(row_item),
                                page=page,
                                table=table_idx,
                                period=need_period,
                                column=need_column,
                            )
                            if rec_sel:
                                quote_src = (src.get("quote") or "").strip()
                                quote_fallback = f"{row_item} {rec_sel['value']}".strip()
                                quote = quote_src or quote_fallback
                                pt = page_texts.get(page) or ""
                                ok = quote_on_page(quote, pt)
                                if not ok:
                                    q2 = quote.replace(",", "").replace("，", "")
                                    pt2 = pt.replace(",", "").replace("，", "")
                                    ok = quote_on_page(q2, pt2)
                                if (not ok) and quote_src and quote_fallback:
                                    ok2 = quote_on_page(quote_fallback, pt)
                                    if (not ok2):
                                        q2 = quote_fallback.replace(",", "").replace("，", "")
                                        pt2 = pt.replace(",", "").replace("，", "")
                                        ok2 = quote_on_page(q2, pt2)
                                    if ok2:
                                        quote = quote_fallback
                                        ok = True
                                if not ok:
                                    q_toks = set(_numeric_tokens(quote))
                                    pt_toks = set(_numeric_tokens(pt))
                                    if q_toks and q_toks.issubset(pt_toks):
                                        ok = True
                                status = "found" if ok else "ambiguous"
                                chosen = {
                                    "field_id": field_id,
                                    "label": need,
                                    "value": rec_sel["value"],
                                    "unit": rec_sel.get("unit") or "",
                                    "period": rec_sel.get("period") or "",
                                    "layer": "L1",
                                    "method": "record_map",
                                    "status": status,
                                    "source": {
                                        "cache_id": args.sha12,
                                        "result_dir": result_dir.name,
                                        "page": page,
                                        "table": table_idx,
                                        "quote": quote if ok else None,
                                        "file": tt.get("file"),
                                    },
                                    "operation_id": f"{SKILL_ID}.resolve",
                                }
                                break
                    if chosen:
                        break
                if chosen:
                    break

        # ---------- L2 ----------
        if not chosen:
            rec_hits = _locate_records_hits(records, need, max_hits=args.max_hits)
            if rec_hits:
                primary = rec_hits[0]
                page = int(primary.get("page") or 0)
                table_idx = int(primary.get("table") or 0)
                values = primary.get("values") or []
                value, hint = _select_value(values, period=need_period, column=need_column)
                if value:
                    unit = primary.get("unit") or ""
                    quote = " ".join(x for x in [primary.get("row_label") or "", value] if x).strip()
                    ok = quote_on_page(quote, page_texts.get(page) or "")
                    status = "found" if ok else "ambiguous"
                    tid, rel_file = _find_result_table_file_by_record_table_index(result_dir, manifest, table_idx)
                    chosen = {
                        "field_id": field_id,
                        "label": need,
                        "value": value,
                        "unit": unit,
                        "period": (nfkc(hint or "").strip() or (need_period or "")) if hint else (need_period or ""),
                        "layer": "L2",
                        "method": "record_map",
                        "status": status,
                        "source": {
                            "cache_id": args.sha12,
                            "result_dir": result_dir.name,
                            "page": page,
                            "table": table_idx,
                            "quote": quote if ok else None,
                            "file": rel_file or (f"tables/{_slug(tid)}.json" if tid else None),
                        },
                        "operation_id": f"{SKILL_ID}.resolve",
                    }

        # ---------- MD fallback ----------
        if not chosen:
            md_hits = []
            for kw in need_variants:
                md_hits.extend(locate_in_md(md_lines, kw, max_hits=1))
            md_hits = md_hits[:1]
            if md_hits:
                h = md_hits[0]
                page = int(h.get("page") or 0)
                quote = (h.get("text") or "").strip()
                ok = quote_on_page(quote, page_texts.get(page) or "")
                chosen = {
                    "field_id": field_id,
                    "label": need,
                    "value": "",
                    "unit": "",
                    "period": "",
                    "layer": "L2",
                    "method": "text_scan",
                    "status": "found" if ok else "not_found",
                    "source": {
                        "cache_id": args.sha12,
                        "result_dir": result_dir.name,
                        "page": page,
                        "table": None,
                        "quote": quote if ok else None,
                        "file": None,
                    },
                    "operation_id": f"{SKILL_ID}.resolve",
                }
            else:
                chosen = {
                    "field_id": field_id,
                    "label": need,
                    "value": "",
                    "unit": "",
                    "period": "",
                    "layer": "L2",
                    "method": "record_map",
                    "status": "not_in_pdf",
                    "source": {
                        "cache_id": args.sha12,
                        "result_dir": result_dir.name,
                        "page": None,
                        "table": None,
                        "quote": None,
                        "file": None,
                    },
                    "operation_id": f"{SKILL_ID}.resolve",
                }

        out_items.append(chosen)

        if args.write_fields:
            field_file = result_dir / "fields" / f"{field_id}.json"
            write_json(field_file, chosen)
            # manifest index
            catalog = manifest.setdefault("catalog", {})
            catalog_fields = catalog.setdefault("fields", [])
            if field_id not in existing_fields:
                catalog_fields.append({"id": field_id, "file": f"fields/{field_id}.json", "layer": chosen.get("layer")})
                existing_fields.add(field_id)

    if args.write_fields:
        write_json(manifest_path, manifest)
        # batch index
        batch = {"cache_id": args.sha12, "result_dir": result_dir.name, "needs": args.needs, "items": out_items, "created_at": now_iso()}
        write_json(result_dir / "fields" / "_batch.json", batch)

    print(json.dumps({
        "cache_id": args.sha12,
        "result_dir": result_dir.name,
        "fields": [it["field_id"] for it in out_items],
        "items": [{"field_id": it["field_id"], "status": it["status"], "value": it.get("value")} for it in out_items],
    }, ensure_ascii=False, indent=1))


def cmd_extract_needs(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py extract-needs",
        description="批量按需字段 resolve：从 request-specific.json 读 fields[]，落盘 fields/*.json。",
    )
    ap.add_argument("sha12")
    ap.add_argument("--file", required=True, help="request json：{fields:[...]} 或 {needs:[...]}（natural language 即可）")
    ap.add_argument("--result", default="", help="指定 result-* 目录名；不传则取最新")
    ap.add_argument("--period", default="", help="期间消歧（可选）")
    ap.add_argument("--column", default="", help="列消歧（可选）")
    ap.add_argument("--max-hits", type=int, default=20)
    args = ap.parse_args(argv)

    req = read_json(Path(args.file).expanduser(), {}) or {}
    needs = req.get("fields") or req.get("needs") or []
    if not isinstance(needs, list) or not needs:
        raise SystemExit("--file 缺 fields[]/needs[]")

    # 直接复用 resolve-cmd 的逻辑
    cmd = [args.sha12]
    for n in needs:
        cmd += ["--need", n]
    if args.result:
        cmd += ["--result", args.result]
    if args.period:
        cmd += ["--period", args.period]
    if args.column:
        cmd += ["--column", args.column]
    cmd += ["--write-fields", "--max-hits", str(args.max_hits)]
    cmd_resolve(cmd)


def cmd_capabilities(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py capabilities",
        description="输出本技能可发现的 operation 清单（供 Agent / pack 做路由）。",
    )
    ap.add_argument("--json", action="store_true", help="始终输出 JSON（默认）")
    args = ap.parse_args(argv)

    operations = [
        {
            "id": "resolve",
            "layer": "L2",
            "summary": "按需字段：L1 pass 表 → records → 正文 locate，确定性 value 填充 + quote 回验；可选 --write-fields 落盘 FieldRecord。",
            "cli": "wm_report.py resolve <cache_id> --need <label> [--result <result-...>] [--period <token>] [--column <token>] [--write-fields]",
        },
        {
            "id": "extract-needs",
            "layer": "L2",
            "summary": "批量 resolve：从 request json 的 fields[]/needs[] 读取需求清单，逐条写入 fields/*.json，并生成 fields/_batch.json。",
            "cli": "wm_report.py extract-needs <cache_id> --file <request-specific.json> [--result <result-...>]",
        },
        {
            "id": "materialize-tables",
            "layer": "L1",
            "summary": "全量分表：records.json + meta.json → result-{ts} typed 表产物与 manifest/catalog 索引。",
            "cli": "wm_report.py materialize-tables <cache_id> [--force] [--out <result-...>]",
        },
        {
            "id": "adapt-plan",
            "layer": "L1.5",
            "summary": "根据 meta/document_profile 生成本次提取剧本，给出 coverage_groups、convert_strategy、narratives 与异常处置建议。",
            "cli": "wm_report.py adapt-plan <cache_id> [--result <result-...>] [--force]",
        },
        {
            "id": "review-extract",
            "layer": "L1.8",
            "summary": "独立审核提取产物：检查 quality/gaps/narratives 与画像一致性，并在 novelty 时生成 evolution_proposal。",
            "cli": "wm_report.py review-extract <cache_id> [--result <result-...>]",
        },
        {
            "id": "render-html",
            "layer": "L1.9",
            "summary": "将 result-* 渲染为单文件 HTML：仅 quality=pass 表 + gaps/review；只读阅览，不改数。",
            "cli": "wm_report.py render-html <cache_id> [--result <result-...>] [--out report.html]",
        },
    ]
    print(json.dumps({"skill_id": SKILL_ID, "operations": operations}, ensure_ascii=False, indent=1))


# --------------------------------------------------------------------------
# ④ materialize-tables：records + meta -> result-{ts}/ 分表产物
# --------------------------------------------------------------------------

def _slug(s: str) -> str:
    out = re.sub(r"[^a-z0-9_]+", "_", (s or "").lower())
    return re.sub(r"_+", "_", out).strip("_") or "table"


def _table_title_hint(table_meta: dict) -> str:
    headers = table_meta.get("headers") or []
    head0 = nfkc(headers[0] if headers else "")
    if "分行业" in head0:
        return "segments_by_industry"
    if "分产品" in head0:
        return "segments_by_product"
    if "分地区" in head0:
        return "segments_by_region"
    return "segments_by_region"


def _build_generic_columns(headers: list[str], periods: dict | None = None) -> list[dict]:
    cols = [{"key": "item", "label": "科目/项目", "type": "string", "description": "报表行名称"}]
    periods = periods or {}
    for ci, h in enumerate(headers[1:], start=1):
        period_hint = periods.get(ci)
        label = nfkc(h).strip() or nfkc(period_hint or "").strip() or f"第{ci+1}列"
        cols.append({
            "key": f"c{ci}",
            "label": label,
            "type": "string",
            "description": f"原表第{ci+1}列",
        })
    return cols


def _pick_value(values: list[dict], pats: list[str]) -> str:
    for v in values:
        hdr = nfkc(v.get("header") or "")
        if any(p in hdr for p in pats):
            return v.get("value") or ""
    return ""


def _build_variance_row(rec: dict) -> dict:
    """按表头语义取本期/上年/变动/原因，禁止把占比列当上年金额。"""
    vals = rec.get("values") or []
    amounts: list[str] = []
    yoy = ""
    reason = ""
    for v in vals:
        hdr = nfkc(v.get("header") or "")
        raw = (v.get("value") or "").strip()
        if not raw:
            continue
        if any(p in hdr for p in ("原因说明", "情况说明", "变动原因")) and not any(
            p in hdr for p in ("变动幅度", "变动比例")
        ):
            reason = raw
            continue
        if any(p in hdr for p in ("变动幅度", "变动比例")) or (hdr.strip() in ("增减", "增减(%)")):
            yoy = raw
            continue
        if any(p in hdr for p in ("占总", "占总资产", "占总负债", "资产比重", "负债比重")):
            continue
        if re.search(r"[\d,.\-]", raw):
            amounts.append(raw)
    if not yoy:
        yoy = _pick_value(vals, ["变动幅度", "变动比例", "增减"])
    if not reason:
        reason = _pick_value(vals, ["原因说明", "情况说明", "变动原因"])
    quote_vals = amounts[:2] + ([yoy] if yoy else [])
    return {
        "item": rec.get("row_label") or "",
        "value_current": amounts[0] if len(amounts) >= 1 else "",
        "value_prior": amounts[1] if len(amounts) >= 2 else "",
        "yoy_pct": yoy,
        "reason": reason,
        "reason_method": "record_map" if reason else "",
        "source": {"page": rec.get("page"), "table": rec.get("table"), "quote": _clip_quote(" ".join(quote_vals))},
    }


def _clip_quote(s: str, limit: int = 120) -> str:
    """quote 截断且不产生数值残片：截断点落在数值中间时（原串该数值仍在继续），
    回退到该数值段之前——半截数值会成回验幻觉残片（上港 '105,005,100'→'105'）。"""
    if len(s) <= limit:
        return s
    head = s[:limit]
    m = re.search(r"\d[\d,，.\s]*$", head)
    if m and limit < len(s) and re.match(r"[\d,，.]", s[limit]):
        head = head[:m.start()].rstrip()
    return head


def _build_generic_row(rec: dict, n_cols: int) -> dict:
    row = {"item": rec.get("row_label") or ""}
    by_col = {int(v.get("col", 0)): v for v in rec.get("values") or []}
    for ci in range(1, n_cols):
        row[f"c{ci}"] = (by_col.get(ci) or {}).get("value") or ""
    row["source"] = {"page": rec.get("page"), "table": rec.get("table"), "quote": _clip_quote(" ".join(
        [str(row.get(f"c{ci}", "")) for ci in range(1, min(n_cols, 4))]
    ).strip())}
    return row


def _page_lines_map(md_lines: list[str]) -> dict[int, tuple[int, int]]:
    page_lines: dict[int, tuple[int, int]] = {}
    marks = [(i, int(m.group(1))) for i, ln in enumerate(md_lines)
             if (m := PAGE_MARKER_RE.match(ln.strip()))]
    for j, (start, page) in enumerate(marks):
        end = (marks[j + 1][0] - 1) if j + 1 < len(marks) else len(md_lines) - 1
        page_lines[page] = (start, end)
    return page_lines


def _page_text(md_lines: list[str], page_lines: dict[int, tuple[int, int]], page: int) -> list[str]:
    span = page_lines.get(page)
    if not span:
        return []
    start, end = span
    return md_lines[start:end + 1]


def _clean_line(s: str) -> str:
    return nfkc(s).strip()


def _fallback_variance_reason(md_lines: list[str], page_lines: dict[int, tuple[int, int]],
                              sections_by_key: dict[str, dict], row: dict) -> tuple[str, dict]:
    item = _clean_line(row.get("item") or "")
    source = row.get("source") or {}
    page = int(source.get("page") or 0)
    page_candidates = []
    if page:
        page_candidates.extend([page, page + 1])
    mda = sections_by_key.get("mda_overview") or {}
    mda_page = int(mda.get("page") or 0)
    if mda_page:
        for p in range(mda_page, mda_page + 6):
            if p not in page_candidates:
                page_candidates.append(p)
    for p in page_candidates:
        for raw in _page_text(md_lines, page_lines, p):
            line = _clean_line(raw)
            if not line or line.startswith("|") or line.startswith("<!--"):
                continue
            if item and item in line and any(tok in line for tok in ("主要", "原因", "由于", "系", "变动")):
                quote = _clip_quote(line)
                return line[:200], {"page": p, "section": "mda_overview", "quote": quote}
    return "", {}


# 单位注记行判定：「人民币元」「（除特别注明外，货币单位均以人民币百万元列示）」等——
# 无数字、简短、含"单位"或全由单位/括号/日期字符构成
UNIT_ANNOTATION_RE = re.compile(r"^[（(）)：:，,\s　0-9年月日除特别注明外金额单位人民币拾佰千百亿万元％%．.、]+$")
# 纯日期/会计期间行（「2025 年 12 月 31 日」「…止年度」）是期间注记，不是标题
DATE_ANNOTATION_RE = re.compile(r"^[\d\s\-—–至~.年月日止度]+$")


def _is_unit_annotation(line: str) -> bool:
    line = (line or "").strip()
    if not line or len(line) > 45:
        return False
    if re.search(r"\d", line):
        return bool(DATE_ANNOTATION_RE.fullmatch(line))  # 有数字时仅纯日期行算注记
    return "单位" in line or bool(UNIT_ANNOTATION_RE.fullmatch(line))


def _guess_table_title(md_lines: list[str], line_start: int) -> str:
    for i in range(line_start - 1, max(-1, line_start - 8), -1):
        line = _clean_line(md_lines[i])
        if not line or line.startswith("|") or line.startswith("<!--"):
            continue
        bare = line.lstrip("# ").strip()
        if _is_unit_annotation(bare):
            continue  # 单位注记行（含被 Docling 误标为标题的「## 人民币元」）跳过，继续向上找
        if line.startswith("#"):
            return bare[:60]
        if len(line) <= 60:
            return line
    return ""  # 无真实标题：返回空串（结构性定型凭空串判定「无标题证据」，不行使否决权）


def _build_narrative_catalog(meta: dict) -> tuple[list[dict], list[dict]]:
    """按 filing_kind / industry 生成 narratives 索引与 gaps 初始项。"""
    filing_kind = meta.get("filing_kind") or infer_filing_kind(meta.get("source") or {},
                                                               (meta.get("doc") or {}).get("pages") or 0)
    industry = (meta.get("industry_hint") or {}).get("industry")
    narratives: list[dict] = []
    gaps: list[dict] = []
    for nid in NARRATIVE_REQUIRED_IDS:
        if _is_q1_q3(filing_kind):
            narratives.append({
                "id": nid, "file": f"narratives/{nid}.json", "group": "D_mda",
                "method": "text_scan", "anchor": nid, "status": "not_applicable",
            })
            gaps.append({
                "id": nid, "group": "D_mda",
                "reason": "一季报/三季报通常无完整 MD&A 章节，不适用",
                "status": "not_applicable",
            })
        else:
            narratives.append({
                "id": nid, "file": f"narratives/{nid}.json", "group": "D_mda",
                "method": "text_scan", "anchor": nid, "status": "pending",
            })
            gaps.append({
                "id": nid, "group": "D_mda",
                "reason": "待 Agent text_scan 补全", "status": "pending",
            })
    ext = INDUSTRY_EXT_GROUPS.get(industry) or {}
    if ext.get("narratives") and not _is_q1_q3(filing_kind):
        for nid in ext["narratives"]:
            narratives.append({
                "id": nid, "file": f"narratives/{nid}.json", "group": ext["group"],
                "method": "text_scan", "anchor": nid, "status": "pending",
            })
            gaps.append({
                "id": nid, "group": ext["group"],
                "reason": "待 Agent text_scan 补全（行业特色叙述）", "status": "pending",
            })
    # checklist 指标无 typed 表时强制进 gaps，避免清单承诺超过机器能力
    for item in ext.get("required_gaps") or []:
        gid = item.get("id")
        if not gid:
            continue
        gaps.append({
            "id": gid,
            "group": ext.get("group") or "X_industry",
            "reason": item.get("reason") or "清单指标无专用表，须补全或标未披露",
            "status": "required",
        })
    # 交运：按 transport_segment 追加子业态 gaps；不适用侧标 not_applicable
    if industry == "transport_infrastructure":
        segment = (meta.get("industry_hint") or {}).get("transport_segment")
        seg_gaps = ext.get("segment_gaps") or {}
        for seg_name, items in seg_gaps.items():
            applicable = segment in (None, "mixed") or segment == seg_name
            for item in items:
                gid = item.get("id")
                if not gid:
                    continue
                if applicable:
                    gaps.append({
                        "id": gid,
                        "group": ext.get("group") or "X_transport_infrastructure",
                        "reason": item.get("reason") or "交运子业态清单指标",
                        "status": "required",
                        "transport_segment": seg_name,
                    })
                else:
                    gaps.append({
                        "id": gid,
                        "group": ext.get("group") or "X_transport_infrastructure",
                        "reason": f"当前 transport_segment={segment}，{seg_name} 子业态不适用",
                        "status": "not_applicable",
                        "transport_segment": seg_name,
                    })
    return narratives, gaps


def _generic_table_id(table_meta: dict) -> str:
    page = table_meta.get("page", 0)
    idx = table_meta.get("index", 0)
    return f"generic_table_p{page:03d}_i{idx:03d}"


def _materialize_generic_table(md_lines: list[str], table_meta: dict, fitz_entry: dict | None = None) -> dict:
    block = md_lines[table_meta["line"]:table_meta["line_end"] + 1]
    schema = parse_table_schema(block)
    headers = schema.get("headers") or []
    row_bboxes = (fitz_entry or {}).get("row_bboxes") or []
    rows = []
    for di, data_row in enumerate(schema.get("rows") or []):
        if not data_row:
            continue
        source = {"page": table_meta.get("page"), "table": table_meta.get("index")}
        # 多级表头粘连常使行首出现相邻重复 cell（如 肿瘤|肿瘤），quote 拼接去重相邻同值，
        # 否则「肿瘤 肿瘤 药名」在页面单次出现，token 级回验必败
        q_cells: list[str] = []
        for x in data_row[:4]:
            c = x.strip()
            if c and (not q_cells or c != q_cells[-1]):
                q_cells.append(c)
        source["quote"] = _clip_quote(" ".join(q_cells))
        # fitz 轨道行级 bbox：md 数据行 di ↔ row_bboxes[di+1]（0 位为表头）
        if di + 1 < len(row_bboxes) and row_bboxes[di + 1]:
            source["bbox"] = row_bboxes[di + 1]
        row = {"item": data_row[0].strip(), "source": source}
        for ci, cell in enumerate(data_row[1:], start=1):
            row[f"c{ci}"] = cell.strip()
        rows.append(row)
    return {
        "table_id": _generic_table_id(table_meta),
        "title": _guess_table_title(md_lines, table_meta.get("line", 0)) or "未定型通用表",
        "description": "未定型通用表，保底物化供上层消费判读",
        "method": "record_map",
        "group": "Z_generic",
        "source_type": "generic_table",
        "record_type": None,
        "type_hint": table_meta.get("type_hint"),
        "nearby_title": table_meta.get("nearby_title") or _guess_table_title(md_lines, table_meta.get("line", 0)) or "未定型通用表",
        "unit_default": schema.get("unit") or table_meta.get("unit") or "",
        "schema": {"columns": _build_generic_columns(headers, schema.get("periods") or {})},
        "rows": rows,
        "row_count": len(rows),
        "provenance": {"pages": [table_meta.get("page")], "tables": [table_meta.get("index")]},
    }


def materialize_tables(sha12: str, *, out_name: str | None, force: bool) -> dict:
    d = entry_dir(sha12)
    meta = read_json(d / "meta.json")
    records = read_json(d / "records.json", [])
    if not meta or not records:
        raise SystemExit(f"缓存 {sha12} 缺 meta.json/records.json，请先 scan + extract-tables")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_name = out_name or f"result-{ts}"
    result_dir = d / result_name
    # 手工闭环层（Agent text_scan 落盘的 narratives + gaps 显式判定）在 --force 重建时保留回放，
    # 否则一次误操作清零 P0 闭环成果；qa::/narrative_kpi:: 为 QA 机器快照不在此列
    overrides_narr: dict[str, dict] = {}
    overrides_gaps: dict[str, dict] = {}
    if result_dir.exists() and force:
        narr_dir = result_dir / "narratives"
        if narr_dir.is_dir():
            for p in sorted(narr_dir.glob("*.json")):
                try:
                    overrides_narr[p.stem] = json.loads(p.read_text(encoding="utf-8"))
                except ValueError:
                    continue
        old_gaps = read_json(result_dir / "gaps.json", [])
        overrides_gaps = {
            g.get("id"): g for g in (old_gaps or [])
            if g.get("id") and not str(g.get("id")).startswith(("qa::", "narrative_kpi::"))
            and g.get("status") in ("found", "not_disclosed", "not_applicable", "not_found")
        }
        shutil.rmtree(result_dir)
    result_dir.mkdir(parents=True, exist_ok=True)
    (result_dir / "tables").mkdir(parents=True, exist_ok=True)
    (result_dir / "narratives").mkdir(parents=True, exist_ok=True)
    (result_dir / "derived").mkdir(parents=True, exist_ok=True)
    md_path = d / "report.md"
    md_lines = md_path.read_text(encoding="utf-8").split("\n") if md_path.is_file() else []
    page_lines = _page_lines_map(md_lines) if md_lines else {}
    sections_by_key = {s.get("key"): s for s in (meta.get("sections") or [])}

    # fitz 轨道 bbox：物理表 index → (page, 页内顺序) → fitz_tables.json 条目
    fitz_pages = (read_json(d / "fitz_tables.json", {}) or {}).get("pages") or {}
    order_by_index: dict[int, tuple[int, int]] = {}
    seq_by_page: dict[int, list[dict]] = {}
    for t in meta.get("tables") or []:
        seq_by_page.setdefault(t.get("page") or 0, []).append(t)
    for p, seq in seq_by_page.items():
        for k, t in enumerate(sorted(seq, key=lambda x: x.get("line") or 0)):
            order_by_index[t.get("index")] = (p, k)

    def _fitz_entry(table_index):
        loc = order_by_index.get(table_index)
        if not loc:
            return None
        for e in (fitz_pages.get(str(loc[0])) or []):
            if int(e.get("order", -1)) == loc[1]:
                return e
        return None

    table_meta_by_index = {t.get("index"): t for t in (meta.get("tables") or [])}
    chain_head_by_index: dict[int, int] = {}
    for t in meta.get("tables") or []:
        chain_head_by_index[t.get("index")] = t.get("chain_head", t.get("index"))
    specs_by_type: dict[str, list[dict]] = {}
    for spec in TABLE_CATALOG:
        specs_by_type.setdefault(spec["record_type"], []).append(spec)

    # 按 (table_id 基名, 合并链头) 分组：同类型多条独立物理链不静默拼接（禁混源纪律）
    grouped: dict[tuple[str, int], list[dict]] = {}
    for rec in records:
        rtype = rec.get("type")
        if not rtype:
            continue
        head = chain_head_by_index.get(rec.get("table"), rec.get("table"))
        if rtype == "segments":
            base = _table_title_hint(table_meta_by_index.get(head, {}))
        else:
            specs = specs_by_type.get(rtype) or []
            base = specs[0]["table_id"] if specs else rtype
        grouped.setdefault((base, head), []).append(rec)

    def _summary_years(head: int) -> int:
        """期数列中的不同年份数——多年摘要表判据（神华 p301 近5年摘要 2021-2025）；
        不能用期数列计数：docling 表头回声会把 期末/期初 碎成多列（盾安 BS 实证）。"""
        tm2 = table_meta_by_index.get(head) or {}
        labels = " ".join(str(v) for v in (tm2.get("periods") or {}).values())
        return len(set(re.findall(r"20\d{2}", labels)))

    def _chain_score(recs: list[dict], head: int) -> float:
        """链结构分：行数 + 标题含报表名 + 合计行数 + 主表偏好（合并优先/摘要惩罚）。"""
        tm = table_meta_by_index.get(head) or {}
        score = float(len(recs))
        title = nfkc(tm.get("nearby_title") or "")
        for tok in (STMT_TITLE_TOKS.get(recs[0].get("type")) or ()):
            if tok in title:
                score += 5
                break
        if md_lines and tm.get("line") is not None:
            block = md_lines[tm.get("line", 0):tm.get("line_end", 0) + 1]
            score += min(3, sum(1 for ln in block if "合计" in ln))
        # 主表偏好：合并报表优先于母公司（陕煤/盾安/宁沪裸 id 曾锚在母公司表实证）
        if "母公司" in title:
            score -= 30
        elif "合并" in title or "合併" in title:
            score += 8
        # 多年摘要惩罚：期数列含 ≥3 个不同年份（近5年摘要表）或标题带摘要词——
        # 同型摘要副本不得抢裸 id（神华 p301「合并利润表」5 年摘要抢走 income_stmt 实证）
        if _summary_years(head) >= 3:
            score -= 25
        if re.search(r"摘要|近.{0,4}年主要|概览|补充资料", title):
            score -= 25
        return score

    # canonical table_id 给结构分最高的链；其余独立链用 {base}_p{page}_i{idx}
    by_base: dict[str, list[tuple[int, list[dict]]]] = {}
    for (base, head), recs in grouped.items():
        by_base.setdefault(base, []).append((head, recs))
    id_for_key: dict[tuple[str, int], str] = {}
    variant_for_key: dict[tuple[str, int], str] = {}
    used_ids: set[str] = set()

    def _table_variant(head: int, rank0: bool) -> str:
        """typed 表物理角色：primary/parent_company/summary/analysis/supplementary/duplicate。"""
        tm = table_meta_by_index.get(head) or {}
        title = nfkc(tm.get("nearby_title") or "")
        if ANALYSIS_TITLE_RE.search(title):
            return "analysis"
        if _summary_years(head) >= 3 or re.search(r"摘要|近.{0,4}年主要|概览", title):
            return "summary"
        if "补充资料" in title:
            return "supplementary"
        if "母公司" in title:
            return "parent_company"
        return "primary" if rank0 else "duplicate"

    for base, chains in by_base.items():
        for rank, (head, recs) in enumerate(
                sorted(chains, key=lambda hr: (-_chain_score(hr[1], hr[0]), hr[0]))):
            if rank == 0:
                tid = base
            else:
                tm = table_meta_by_index.get(head) or {}
                tid = f"{base}_p{int(tm.get('page') or 0):03d}_i{head:03d}"
                n = 2
                while tid in used_ids:
                    tid = f"{base}_p{int(tm.get('page') or 0):03d}_i{head:03d}_{n}"
                    n += 1
            used_ids.add(tid)
            id_for_key[(base, head)] = tid
            variant_for_key[(base, head)] = _table_variant(head, rank == 0)

    catalog_tables = []
    pending_narr, gap_base = _build_narrative_catalog(meta)
    gaps = list(gap_base)
    for key in sorted(grouped, key=lambda k: id_for_key[k]):
        table_id, recs = id_for_key[key], grouped[key]
        # 非 canonical 链（{base}_p…）沿用基名的目录元数据，仅 table_id 区分物理来源
        spec = TABLE_SPEC_BY_ID.get(table_id) or TABLE_SPEC_BY_ID.get(key[0]) or {
            "table_id": table_id, "record_type": recs[0].get("type"), "group": "Z_misc",
            "title": table_id, "description": "自动生成的数据表",
        }
        sample_meta = table_meta_by_index.get(recs[0].get("table"), {})
        headers = sample_meta.get("headers") or recs[0].get("headers") or ["项目"]
        if key[0] == "variance_reasons":
            columns = [
                {"key": "item", "label": "科目/项目", "type": "string", "description": "报表行名称"},
                {"key": "value_current", "label": "本期金额", "type": "string", "description": "本报告期金额"},
                {"key": "value_prior", "label": "上年同期金额", "type": "string", "description": "上年同期金额"},
                {"key": "yoy_pct", "label": "同比变动(%)", "type": "string", "description": "变动幅度/比例"},
                {"key": "reason", "label": "变动原因说明", "type": "text", "description": "管理层原文原因说明"},
            ]
            rows = [_build_variance_row(r) for r in recs]
            for row in rows:
                if row.get("reason"):
                    continue
                reason, src = _fallback_variance_reason(md_lines, page_lines, sections_by_key, row)
                if reason:
                    row["reason"] = reason
                    row["reason_method"] = "text_scan"
                    row["source"].update(src)
                else:
                    gaps.append({
                        "id": f"variance_reason::{row.get('item','')}",
                        "group": "D_mda",
                        "table_id": table_id,
                        "page": row.get("source", {}).get("page"),
                        "reason": "该行未在表格中披露原因，text_scan 也未命中可回补正文",
                        "status": "not_found",
                    })
        else:
            columns = _build_generic_columns(headers, sample_meta.get("periods") or {})
            rows = [_build_generic_row(r, len(headers)) for r in recs]
        file_rel = f"tables/{_slug(table_id)}.json"
        payload = {
            "table_id": table_id,
            "title": spec.get("title"),
            "description": spec.get("description"),
            "method": "record_map",
            "group": spec.get("group"),
            "variant": variant_for_key.get(key, "primary"),
            "source_type": "pdf_table",
            "record_type": spec.get("record_type"),
            "unit_default": sample_meta.get("unit") or recs[0].get("unit") or "",
            "schema": {"columns": columns},
            "rows": rows,
            "row_count": len(rows),
            "provenance": {
                "pages": sorted({r.get("page") for r in recs if r.get("page") is not None}),
                "tables": sorted({r.get("table") for r in recs if r.get("table") is not None}),
            },
        }
        fitz_bboxes = {}
        for r in recs:
            ent = _fitz_entry(r.get("table"))
            if ent and ent.get("bbox") is not None:
                fitz_bboxes[str(r.get("table"))] = ent["bbox"]
        if fitz_bboxes:
            payload["provenance"]["fitz_bboxes"] = fitz_bboxes
        write_json(result_dir / file_rel, payload)
        catalog_tables.append({
            "id": table_id, "file": file_rel, "group": spec.get("group"),
            "method": "record_map", "row_count": len(rows),
            "variant": variant_for_key.get(key, "primary"),
        })

    # P1-A：跨页续片 hint 传染 + 同 hint 相邻片合并。碎表中段表头被数据吞掉导致 hint 丢失
    # （恒瑞新药注册表 p64 带_hint p65/66 丢失），传染条件保守：后片无 hint、页差恰 1、
    # cols 差 ≤3、未定型、≥2 行，链式传递；合并仅在页连续（差 ≤1）且 ≥2 片时产出合并候选
    def _effective_hint(t: dict):
        return t.get("type_hint") or t.get("_inherited_hint")

    metas_sorted = sorted(meta.get("tables") or [], key=lambda t: t.get("index") or 0)
    prev_t = None
    for t in metas_sorted:
        if (prev_t is not None and _effective_hint(prev_t) and not t.get("type_hint")
                and t.get("type") is None
                and (t.get("page") or 0) - (prev_t.get("page") or 0) == 1
                and abs((t.get("cols") or 0) - (prev_t.get("cols") or 0)) <= 3
                and int(t.get("rows") or 0) >= 2):
            t["_inherited_hint"] = _effective_hint(prev_t)
        prev_t = t

    for table_meta in meta.get("tables") or []:
        # 带（含传染）hint 的小表（跨页续表首片常仅 2 行）放行进候选；无 hint 的 2 行表仍是噪声
        eff_hint = _effective_hint(table_meta)
        min_rows = 2 if eff_hint else 3
        if table_meta.get("type") is not None or int(table_meta.get("rows", 0)) < min_rows:
            continue
        payload = _materialize_generic_table(md_lines, table_meta,
                                             fitz_entry=_fitz_entry(table_meta.get("index")))
        if eff_hint and not payload.get("type_hint"):
            payload["type_hint"] = eff_hint
            payload["hint_source"] = "contagion" if table_meta.get("_inherited_hint") else "signature"
        file_rel = f"tables/{_slug(payload['table_id'])}.json"
        write_json(result_dir / file_rel, payload)
        catalog_tables.append({
            "id": payload["table_id"], "file": file_rel, "group": payload["group"],
            "method": payload["method"], "row_count": payload["row_count"],
            "record_type": payload["record_type"], "source_type": payload["source_type"],
            "type_hint": payload.get("type_hint"),
        })

    by_hint: dict[str, list[dict]] = {}
    for t in metas_sorted:
        h = _effective_hint(t)
        if h and t.get("type") is None and int(t.get("rows") or 0) >= 2:
            by_hint.setdefault(h, []).append(t)
    merged_candidates = []
    echo_candidates = []
    for hint, ts in by_hint.items():
        clusters, cur = [], [ts[0]]
        for t in ts[1:]:
            # 簇切分：页断（差>1）或原生 hint 相邻（两张独立表各有原生签名，禁混源；
            # 恒瑞附表3/4/5 同构连排，p34/p35 原生 hint 处必须切断）
            native_clash = bool(t.get("type_hint")) and any(x.get("type_hint") for x in cur)
            if (t.get("page") or 0) - (cur[-1].get("page") or 0) <= 1 and not native_clash:
                cur.append(t)
            else:
                clusters.append(cur)
                cur = [t]
        clusters.append(cur)
        for cl in clusters:
            if len(cl) < 2:
                continue
            objs = []
            for t in cl:
                p = result_dir / "tables" / f"{_generic_table_id(t)}.json"
                if p.is_file():
                    o = read_json(p, {}) or {}
                    if o.get("rows"):
                        objs.append((t, o))
            if len(objs) < 2:
                continue
            base = objs[0][1]
            rows = []
            for t, o in objs:
                frag_rows = list(o.get("rows") or [])
                # 传染片（表头被数据吞掉）首行被 parse_table_schema 当表头丢掉——回收为数据行。
                # 护栏：回收行与簇首片表头高度重叠（≥60% cell 相同）时是真表头回声（如地产年
                # 报担保各片逐页重复同款表头），不回收——只回收真正的数据首行
                if t.get("_inherited_hint"):
                    block = md_lines[t.get("line", 0):t.get("line_end", 0) + 1]
                    hdr_cells = (parse_table_schema(block).get("headers") or [])
                    if any((c or "").strip() for c in hdr_cells):
                        base_hdrs = {(c or "").strip() for c in (objs[0][0].get("headers") or [])
                                     if (c or "").strip()}
                        cellset = {(c or "").strip() for c in hdr_cells if (c or "").strip()}
                        if len(cellset & base_hdrs) / max(1, len(cellset)) < 0.6:
                            src = {"page": t.get("page"), "table": t.get("index"),
                                   "quote": " ".join((c or "").strip() for c in hdr_cells[:4])[:120]}
                            row = {"item": (hdr_cells[0] or "").strip(), "source": src}
                            for ci, cell in enumerate(hdr_cells[1:], start=1):
                                row[f"c{ci}"] = (cell or "").strip()
                            frag_rows.insert(0, row)
                rows.extend(frag_rows)
            pages = sorted({r.get("source", {}).get("page") for _, o in objs
                            for r in (o.get("rows") or []) if r.get("source", {}).get("page")})
            mid = f"generic_merged_{_slug(hint)}_p{cl[0].get('page') or 0:03d}_p{cl[-1].get('page') or 0:03d}"
            payload = dict(base)
            payload.update({
                "table_id": mid, "method": "merge_fragments", "type_hint": hint,
                "rows": rows, "row_count": len(rows),
                "merged_from": [o.get("table_id") for _, o in objs],
                "provenance": {"pages": pages, "tables": [t.get("index") for t in cl], "merged": True},
            })
            mfile = f"tables/{mid}.json"
            write_json(result_dir / mfile, payload)
            catalog_tables.append({
                "id": mid, "file": mfile, "group": "Z_generic",
                "method": "merge_fragments", "row_count": len(rows),
                "record_type": None, "source_type": "generic_table", "type_hint": hint,
            })
            merged_candidates.append({
                "file": mfile, "table_id": mid,
                "title": base.get("title") or base.get("nearby_title") or "",
                "headers": [c.get("label") for c in (base.get("schema") or {}).get("columns", [])],
                "sample_rows": rows[:8], "type_hint": hint, "row_count": len(rows),
            })

    # 置前过滤：行内容为表头回声（item 与 c1 大面积相同，如恒瑞附表3 fitz 错乱片）
    # 的合并簇不置前——auto_promote 同 hint 取首张，错乱簇置前会被选中并 QA demote
    def _echo_ratio(c: dict) -> float:
        ss = c.get("sample_rows") or []
        if not ss:
            return 0.0
        echo = sum(1 for r in ss if isinstance(r, dict) and r.get("item") and r.get("item") == r.get("c1"))
        return echo / len(ss)

    echo_candidates = [c for c in merged_candidates if _echo_ratio(c) > 0.5]
    merged_candidates = [c for c in merged_candidates if _echo_ratio(c) <= 0.5]

    source = meta.get("source") or {}
    candidates = []
    for ent in catalog_tables:
        if not str(ent.get("id") or "").startswith("generic_table_"):
            continue
        obj = read_json(result_dir / ent["file"], {}) or {}
        # 目录/释义页是确定性噪声：点线目录被当表、术语表（词语|指|含义）不进晋升候选；
        # tables/ 保底物化不动，只减 Agent 决策面
        title_blob = f"{obj.get('title') or ''} {obj.get('nearby_title') or ''}"
        col_labels = [c.get("label") or "" for c in (obj.get("schema") or {}).get("columns", [])]
        if "目录" in title_blob or ("指" in col_labels and "释义" in title_blob):
            continue
        candidates.append({
            "file": ent["file"],
            "table_id": ent["id"],
            "title": obj.get("title") or obj.get("nearby_title") or "",
            "headers": [c.get("label") for c in (obj.get("schema") or {}).get("columns", [])],
            "sample_rows": (obj.get("rows") or [])[:8],
            "type_hint": obj.get("type_hint") or ent.get("type_hint"),
            "row_count": obj.get("row_count") or 0,
        })
    # 合并候选置前：auto_promote 同 hint 取首张，跨页合并表（行更全）优先于单页片；
    # 表头回声簇（行质量差）沉底仅作 Agent 参考
    candidates = merged_candidates + candidates + echo_candidates
    filing_kind = meta.get("filing_kind") or infer_filing_kind(source, (meta.get("doc") or {}).get("pages") or 0)
    write_json(result_dir / "promote_candidates.json", {
        "cache_id": sha12,
        "filing_kind": filing_kind,
        "industry": (meta.get("industry_hint") or {}).get("industry"),
        "candidates": candidates,
    })

    manifest = {
        "version": RESULT_LAYOUT_VERSION,
        "layout": RESULT_LAYOUT_NAME,
        "cache_id": sha12,
        "created_at": now_iso(),
        "source": {
            "title": source.get("title") or "",
            "symbol": source.get("symbol") or "",
            "report_date": source.get("report_date") or "",
            "filing_kind": meta.get("filing_kind") or infer_filing_kind(source, (meta.get("doc") or {}).get("pages") or 0),
            "industry_hint": (meta.get("industry_hint") or {}).get("industry"),
        },
        "catalog": {"tables": catalog_tables, "narratives": pending_narr, "fields": [], "derived": []},
        "coverage_groups": [g["group"] for g in PRIORITY_GROUPS_BASE],
        "gaps_file": "gaps.json",
        "promote_candidates_file": "promote_candidates.json",
        "quality_file": "quality.json",
    }
    # 手工闭环层回放：narratives 文件写回；gaps 同 id 条目以手工版整体替换，手工独有 id 追加
    for nid, nobj in overrides_narr.items():
        write_json(result_dir / "narratives" / f"{nid}.json", nobj)
    gaps = [overrides_gaps.pop(g["id"], g) if g.get("id") in overrides_gaps else g for g in gaps]
    gaps.extend(overrides_gaps.values())
    for n in pending_narr:
        ov = overrides_narr.get(n.get("id"))
        if ov and ov.get("status"):
            n["status"] = ov["status"]
            n["replayed_override"] = True
    write_json(result_dir / "manifest.json", manifest)
    write_json(result_dir / "gaps.json", gaps)
    index_upsert(
        sha12,
        latest_result=result_name,
        materialized_at=manifest.get("created_at"),
        quality_status="pending",
        catalog_tables=len(catalog_tables),
        catalog_fields=0,
    )
    return {"cache_id": sha12, "result_dir": str(result_dir), "tables": len(catalog_tables)}


def cmd_materialize_tables(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py materialize-tables",
        description="records.json + meta.json 生成 result-{ts}/ 分表产物（自解释 schema）"
    )
    ap.add_argument("sha12")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out", default="")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    out = materialize_tables(args.sha12, out_name=args.out or None, force=args.force)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def _result_dir(sha12: str, out_name: str | None) -> Path:
    d = entry_dir(sha12)
    if out_name:
        return d / out_name
    dirs = sorted([p for p in d.glob("result-*") if p.is_dir()], key=lambda p: p.name)
    if not dirs:
        raise SystemExit(f"缓存 {sha12} 无 result-* 目录，请先 materialize-tables")
    return dirs[-1]


def _load_manifest(result_dir: Path) -> dict:
    man = read_json(result_dir / "manifest.json")
    if not man:
        raise SystemExit(f"缺少 {result_dir / 'manifest.json'}")
    return man


def _ensure_result_dir(sha12: str, out_name: str | None = None) -> Path:
    d = entry_dir(sha12)
    if out_name:
        candidate = d / out_name
        if (candidate / "manifest.json").is_file():
            return candidate
        out = materialize_tables(sha12, out_name=out_name, force=False)
        return Path(out["result_dir"])
    try:
        return _result_dir(sha12, out_name)
    except SystemExit:
        out = materialize_tables(sha12, out_name=None, force=False)
        return Path(out["result_dir"])


def _adapt_coverage_groups(meta: dict) -> list[str]:
    base = [g["group"] for g in PRIORITY_GROUPS_BASE]
    profile = meta.get("document_profile") or {}
    industry = (meta.get("industry_hint") or {}).get("industry")
    if industry and (profile.get("industry_confidence") or 0) >= 0.15:
        ext = INDUSTRY_EXT_GROUPS.get(industry) or {}
        if ext.get("group"):
            base.append(ext["group"])
    return base


CORE_STATEMENT_TYPES = ("balance_sheet", "income_stmt", "cashflow_stmt")

# 跨行业 hint：仅当 document industry 不等于锁定行业时视为噪声
SECTOR_LOCKED_HINTS: dict[str, frozenset[str]] = {
    "bank": frozenset({"deposit_loan"}),
    "insurance": frozenset({
        "premium_income", "claims_payout", "solvency", "investment_assets", "nbv_ev", "channel_mix",
    }),
    "broker": frozenset({
        "brokerage_income", "ib_underwriting", "am_aum", "risk_indicators", "margin_trading", "prop_trading",
    }),
    "real_estate": frozenset({
        "contracted_sales", "land_bank", "delivery_completion", "contract_liabilities", "three_red_lines",
    }),
}

STMT_ROW_LABEL_RULES: dict[str, dict] = {
    "balance_sheet": {
        "any_of": (
            "货币资金", "资产总计", "资产合计", "資產總值", "流动资产合计", "非流动资产合计",
            "负债合计", "负债和所有者权益总计", "負債總額", "權益總額",
        ),
        "min_hits": 2,
        "min_rows": 5,
    },
    "income_stmt": {
        "any_of": (
            "营业总收入", "营业收入", "净利润", "年內虧損", "年內溢利", "期內虧損", "期內溢利",
            "營業收入", "來自客戶合同的收入", "营业成本", "所得税费用",
        ),
        "min_hits": 2,
        "min_rows": 3,
    },
    "cashflow_stmt": {
        "any_of": (
            "经营活动产生的现金流量净额", "经营活动产生的现金流量", "经营活动产生/(使用)的现金流量",
            "經營活動產生的現金流量", "經營活動所得現金淨額",
            "销售商品、提供劳务收到的现金",
            "投资活动", "筹资活动", "投資活動", "融資活動",
        ),
        "min_hits": 2,
        "min_rows": 5,
    },
}


def _table_base_id(tid: str | None) -> str:
    tid = str(tid or "")
    if "_p" in tid:
        return tid.split("_p", 1)[0]
    return tid


def _typed_base_ids(catalog_tables: list | None) -> set[str]:
    bases: set[str] = set()
    for t in catalog_tables or []:
        tid = str(t.get("id") or "")
        if tid.startswith("generic_"):
            continue
        bases.add(_table_base_id(tid))
    return bases


def _item_looks_like_entity_name(item: str) -> bool:
    s = re.sub(r"\s+", "", nfkc(item or ""))
    if not s or len(s) < 4:
        return False
    if any(k in s for k in ("收入", "利润", "成本", "费用", "亏损", "溢利", "稅", "税", "损益", "現金", "现金")):
        return False
    return any(k in s for k in ("公司", "集团", "集團", "有限", "股份", "企业", "企業"))


def _content_blob_from_meta(meta: dict) -> str:
    parts: list[str] = []
    for sec in meta.get("sections") or []:
        if isinstance(sec, dict):
            parts.append(str(sec.get("title") or sec.get("name") or ""))
        else:
            parts.append(str(sec))
    for ch in meta.get("chapters") or []:
        if isinstance(ch, dict):
            parts.append(str(ch.get("title") or ch.get("name") or ""))
        else:
            parts.append(str(ch))
    for t in meta.get("tables") or []:
        if not isinstance(t, dict):
            continue
        parts.append(str(t.get("title") or t.get("nearby_title") or ""))
        parts.extend(str(x) for x in (t.get("headers") or [])[:12])
        parts.extend(str(x) for x in (t.get("sample_labels") or [])[:12])
        if t.get("type"):
            parts.append(str(t.get("type")))
        if t.get("type_hint"):
            parts.append(str(t.get("type_hint")))
    return nfkc("\n".join(parts))


def _observe_type_in_blob(typ: str, blob: str) -> dict | None:
    title_toks = STMT_TITLE_TOKS.get(typ) or ()
    title_hits = [k for k in title_toks if k in blob]
    struct = next((groups for t, groups in STRUCTURAL_RULES if t == typ), None)
    label_hits: list[str] = []
    groups_hit = 0
    if struct:
        for grp in struct:
            hit = next((k for k in grp if k in blob), None)
            if hit:
                groups_hit += 1
                label_hits.append(hit)
    rules = STMT_ROW_LABEL_RULES.get(typ) or {}
    for lab in rules.get("any_of") or ():
        if lab in blob and lab not in label_hits:
            label_hits.append(lab)
    # key_financials: 主要会计数据类标题 + 常用 KPI 行
    if typ == "key_financials":
        kf_title = any(k in blob for k in ("主要会计数据", "主要财务指标", "主要財務指標"))
        kf_labs = [k for k in ("营业收入", "营业总收入", "净利润", "经营活动产生的现金流量净额") if k in blob]
        if kf_title or len(kf_labs) >= 2:
            return {
                "type": typ,
                "strength": "strong" if kf_title or len(kf_labs) >= 3 else "weak",
                "evidence": (["主要会计数据"] if kf_title else []) + kf_labs[:4],
            }
        return None
    if title_hits and (groups_hit >= 1 or len(label_hits) >= 1):
        return {"type": typ, "strength": "strong", "evidence": list(dict.fromkeys(list(title_hits) + label_hits))[:8]}
    if struct and groups_hit >= len(struct):
        return {"type": typ, "strength": "strong", "evidence": label_hits[:8]}
    if len(label_hits) >= 2 or (title_hits and label_hits):
        return {"type": typ, "strength": "weak", "evidence": list(dict.fromkeys(list(title_hits) + label_hits))[:8]}
    if title_hits:
        return {"type": typ, "strength": "weak", "evidence": list(title_hits)[:4]}
    return None


def observe_document_content_signals(
    meta: dict,
    *,
    sha12: str | None = None,
    result_dir: Path | None = None,
) -> dict:
    """从报告正文/meta 表地图观察应出现的表类型（内容优先于行业先验）。"""
    blob = _content_blob_from_meta(meta)
    cid = sha12 or meta.get("cache_id")
    if cid:
        md_path = entry_dir(str(cid)) / "report.md"
        if md_path.is_file():
            # 控制体积：报表信号集中在全文，截断仍覆盖绝大多数年报
            blob = nfkc(blob + "\n" + md_path.read_text(encoding="utf-8")[:400_000])
    if result_dir is not None:
        cand = read_json(result_dir / "promote_candidates.json", {}) or {}
        for c in cand.get("candidates") or []:
            blob += "\n" + nfkc(
                f"{c.get('title') or ''} {' '.join(str(h) for h in (c.get('headers') or [])[:8])} "
                f"{' '.join(str((r.get('item') if isinstance(r, dict) else r) or '') for r in (c.get('sample_rows') or [])[:6])}"
            )
            if c.get("type_hint"):
                blob += "\n" + str(c.get("type_hint"))
    observed: list[dict] = []
    for typ in (*CORE_STATEMENT_TYPES, "key_financials"):
        hit = _observe_type_in_blob(typ, blob)
        if hit:
            observed.append(hit)
    # 建材等高频行业表：正文标题命中则记入观察
    for typ, titles in (
        ("construction_projects", ("在建工程", "重要在建工程")),
        ("segments", ("分部信息", "主营业务分行业", "分产品")),
    ):
        ev = [t for t in titles if t in blob]
        if ev:
            observed.append({"type": typ, "strength": "weak", "evidence": ev})
    return {"observed_signals": observed, "blob_chars": len(blob)}


def _statement_row_qa_finding(tid: str, base: str, obj: dict, file_rel: str) -> dict | None:
    rules = STMT_ROW_LABEL_RULES.get(base)
    if not rules:
        return None
    rows = obj.get("rows") or []
    items = [str(r.get("item") or "") for r in rows if isinstance(r, dict)]
    # 科目词扫整行文本列：盾安类「节标签前置列」版式科目在 c1 而非 item
    blob = nfkc("\n".join(
        " ".join(v for v in (str(x) for x in r.values()) if v and v != "None")
        for r in rows if isinstance(r, dict)) or "\n".join(items))
    hits = [lab for lab in rules["any_of"] if lab in blob]
    entity_rows = sum(1 for it in items if _item_looks_like_entity_name(it))
    if base == "income_stmt" and items and entity_rows >= max(1, len(items) // 2):
        return {
            "id": tid, "verdict": "demote", "reason": "statement_row_labels_invalid",
            "file": file_rel,
            "detail": "利润表行标签疑似公司名而非科目",
        }
    min_hits = int(rules.get("min_hits") or 0)
    min_rows = int(rules.get("min_rows") or 0)
    # 现金流量表续页常只含投资/筹资一段：标题含报表名时放宽行数/命中
    title_blob = nfkc(
        f"{obj.get('title') or ''} {(obj.get('source') or {}).get('nearby_title') or ''} "
        f"{(obj.get('source') or {}).get('title') or ''}"
    )
    if base == "cashflow_stmt" and any(tok in title_blob for tok in ("现金流量表", "現金流量表")):
        min_hits = min(min_hits, 1)
        min_rows = min(min_rows, 3)
    if len(rows) < min_rows:
        return {
            "id": tid, "verdict": "demote", "reason": "statement_row_labels_invalid",
            "file": file_rel,
            "detail": f"{base} 行数过少 ({len(rows)}<{min_rows})",
        }
    if len(hits) < min_hits:
        return {
            "id": tid, "verdict": "demote", "reason": "statement_row_labels_invalid",
            "file": file_rel,
            "detail": f"{base} 缺少科目词 (hits={hits})",
        }
    return None

def _is_noise_type_hint(hint: str | None, industry: str | None) -> bool:
    if not hint:
        return False
    for locked_ind, types in SECTOR_LOCKED_HINTS.items():
        if hint in types and industry != locked_ind:
            return True
    return False


def build_adapt_plan(meta: dict, result_name: str, *, sha12: str | None = None) -> dict:
    profile = meta.get("document_profile") or {}
    coverage_groups = _adapt_coverage_groups(meta)
    tables: list[str] = []
    for group_name in coverage_groups:
        spec = next((g for g in PRIORITY_GROUPS_BASE if g["group"] == group_name), None)
        if spec:
            tables.extend(spec.get("tables") or [])
            continue
        for ext in INDUSTRY_EXT_GROUPS.values():
            if ext.get("group") == group_name:
                tables.extend(ext.get("tables") or [])
                break
    if profile.get("industry_confidence", 0.0) < 0.15:
        tables = [t for t in tables if t in ("key_financials", "balance_sheet", "income_stmt", "cashflow_stmt",
                                             "segments", "production_sales", "top_holders", "dividend",
                                             "employees", "executives", "rd_investment", "related_txn", "guarantees")]
    cid = sha12 or meta.get("cache_id")
    result_dir = entry_dir(str(cid)) / result_name if cid and result_name else None
    if result_dir is not None and not result_dir.is_dir():
        result_dir = None
    content = observe_document_content_signals(meta, sha12=str(cid) if cid else None, result_dir=result_dir)
    observed = content.get("observed_signals") or []
    observed_types = [o.get("type") for o in observed if o.get("type")]
    # promote 优先级：正文强信号 → 弱信号 → 先验 coverage（去重）
    strong = [o["type"] for o in observed if o.get("strength") == "strong" and o.get("type")]
    weak = [o["type"] for o in observed if o.get("strength") != "strong" and o.get("type")]
    promote_priority = list(dict.fromkeys([*strong, *weak, *tables]))
    typed_bases = _typed_base_ids(
        ((_load_manifest(result_dir).get("catalog") or {}).get("tables") if result_dir else None) or []
    ) if result_dir else set()
    filing_kind = profile.get("filing_kind") or meta.get("filing_kind") or ""
    expected: set[str] = set()
    if filing_kind in ("annual", "semi"):
        expected.update(CORE_STATEMENT_TYPES)
    for o in observed:
        if o.get("strength") == "strong" and o.get("type") in (*CORE_STATEMENT_TYPES, "key_financials"):
            expected.add(o["type"])
    expected_but_missing = sorted(t for t in expected if t not in typed_bases)
    narratives, gaps = _build_narrative_catalog(meta)
    anomaly_strategy = [anomaly_strategy_text(a) for a in (meta.get("anomalies") or [])]
    return {
        "cache_id": meta.get("cache_id"),
        "result_dir": result_name,
        "created_at": now_iso(),
        "document_profile": profile,
        "coverage_groups": coverage_groups,
        "tables": list(dict.fromkeys(tables)),
        "observed_signals": observed,
        "observed_types": observed_types,
        "promote_priority": promote_priority,
        "expected_but_missing": expected_but_missing,
        "narratives": narratives,
        "required_gaps": [g for g in gaps if g.get("status") == "required"],
        "convert_strategy": build_convert_strategy(profile),
        "anomaly_strategy": anomaly_strategy,
        "review_hard_gates": [
            "quality_json_required",
            "narrative_quote_page_required",
            "required_gaps_must_be_terminal",
            "quote_must_verify_on_page",
            "profile_consistency",
            "statement_signature_gap",
        ],
    }


def _upsert_manifest_derived(manifest: dict, item: dict) -> None:
    derived = manifest.setdefault("catalog", {}).setdefault("derived", [])
    item_id = item.get("id")
    if item_id:
        derived = [d for d in derived if d.get("id") != item_id]
    derived.append(item)
    manifest["catalog"]["derived"] = derived


def cmd_adapt_plan(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py adapt-plan",
        description="根据报告正文信号 + document_profile 生成本次提取剧本（adapt_plan.json）",
    )
    ap.add_argument("sha12")
    ap.add_argument("--result", default="")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    result_name = args.result or ""
    result_dir = _ensure_result_dir(args.sha12, result_name or None)
    adapt_path = result_dir / "adapt_plan.json"
    if adapt_path.is_file() and not args.force:
        print(json.dumps({"cache_id": args.sha12, "cached": True, "adapt_plan": str(adapt_path)}, ensure_ascii=False))
        return
    meta = read_json(entry_dir(args.sha12) / "meta.json")
    if not meta:
        raise SystemExit(f"缓存 {args.sha12} 缺 meta.json，请先 scan")
    plan = build_adapt_plan(meta, result_dir.name, sha12=args.sha12)
    write_json(adapt_path, plan)
    manifest = _load_manifest(result_dir)
    manifest["adapt_plan_file"] = "adapt_plan.json"
    manifest["coverage_groups"] = plan.get("coverage_groups") or manifest.get("coverage_groups") or []
    write_json(result_dir / "manifest.json", manifest)
    print(json.dumps({"cache_id": args.sha12, "result_dir": str(result_dir), "adapt_plan": str(adapt_path)}, ensure_ascii=False, indent=1))


def _promoted_table_id(dest_id: str, payload: dict, existing_ids: set[str], dest_exists: bool) -> str:
    """同类型多张物理表用独立 id，禁止静默合并以免混源。"""
    if dest_id not in existing_ids and not dest_exists:
        return dest_id
    pages = (payload.get("provenance") or {}).get("pages") or [0]
    tables = (payload.get("provenance") or {}).get("tables") or [0]
    page = int(pages[0] if pages else 0)
    idx = int(tables[0] if tables else 0)
    candidate = f"{dest_id}_p{page:03d}_i{idx:03d}"
    n = 2
    while candidate in existing_ids:
        candidate = f"{dest_id}_p{page:03d}_i{idx:03d}_{n}"
        n += 1
    return candidate


def apply_promotions(sha12: str, promotions: list[dict], *, result_name: str | None = None) -> dict:
    """执行 Agent type_promote 结果：generic → 稳定 table_id（仅 high）。"""
    result_dir = _result_dir(sha12, result_name)
    manifest = _load_manifest(result_dir)
    catalog = manifest.setdefault("catalog", {}).setdefault("tables", [])
    applied = []
    skipped = []
    for item in promotions or []:
        rel = item.get("table_file") or item.get("file") or ""
        dest_type = item.get("promote_to")
        conf = item.get("confidence") or "low"
        if not rel or not dest_type or conf != "high":
            skipped.append({**item, "skip": "not_high_or_incomplete"})
            continue
        src = result_dir / rel
        if not src.is_file() or dest_type not in TABLE_SPEC_BY_ID:
            skipped.append({**item, "skip": "missing_file_or_unknown_type"})
            continue
        spec = TABLE_SPEC_BY_ID[dest_type]
        payload = read_json(src, {}) or {}
        src_id = payload.get("table_id") or Path(rel).stem
        existing_ids = {e.get("id") for e in catalog}
        canonical_rel = f"tables/{_slug(dest_type)}.json"
        dest_id = _promoted_table_id(
            dest_type, payload, existing_ids, (result_dir / canonical_rel).is_file()
        )
        dest_rel = f"tables/{_slug(dest_id)}.json"
        dest = result_dir / dest_rel
        payload["table_id"] = dest_id
        payload["title"] = spec.get("title")
        payload["description"] = spec.get("description")
        payload["group"] = spec.get("group")
        payload["record_type"] = spec.get("record_type")
        payload["source_type"] = "pdf_table"
        payload["promoted"] = True
        payload["promoted_from"] = src_id
        payload["promoted_to_type"] = dest_type
        write_json(dest, payload)
        src.unlink(missing_ok=True)
        catalog[:] = [e for e in catalog if e.get("file") != rel]
        dest_payload = read_json(dest, {}) or {}
        catalog.append({
            "id": dest_id, "file": dest_rel, "group": spec.get("group"),
            "method": "record_map", "row_count": dest_payload.get("row_count") or 0,
            "promoted": True, "record_type": spec.get("record_type"),
        })
        applied.append({"from": rel, "to": dest_id, "type": dest_type, "reason": item.get("reason")})
    n_applied, n_skipped = len(applied), len(skipped)
    # 补晋升会分多次调用：合并历史而非覆写；applied 按 (from,to) 去重（重复执行时 src 已删、本次为空）
    prev = read_json(result_dir / "promotions_applied.json", {}) or {}
    prev_applied = prev.get("applied") or []
    seen_pairs = {(a.get("from"), a.get("to")) for a in prev_applied}
    applied = prev_applied + [a for a in applied if (a.get("from"), a.get("to")) not in seen_pairs]
    skipped = (prev.get("skipped") or []) + skipped
    write_json(result_dir / "manifest.json", manifest)
    write_json(result_dir / "promotions_applied.json", {"applied": applied, "skipped": skipped})
    return {"result_dir": str(result_dir), "applied": n_applied, "skipped": n_skipped}


def _num_magnitude(s: str) -> int | None:
    raw = re.sub(r"[,\s]", "", nfkc(s or "")).replace("%", "")
    if not re.search(r"\d", raw):
        return None
    try:
        v = abs(float(raw))
    except ValueError:
        return None
    if v == 0:
        return 0
    return int(max(0, round(math.log10(v))))


_DASH_UNIFY = str.maketrans("‐‑‒–—―﹣－−", "-" * 9)


def _seg_norm(s: str) -> str:
    """quote 段与 PDF 页文本的对称归一化（去空白/全半角标点，保留数字）。
    Unicode dash 家族统一为 '-'：NFKC 不折叠 en dash，而 docling 常把页上
    「–」空值占位转成 '-'、fitz 侧保留原字符——不对称会令占位段整条误报。"""
    return re.sub(r"[\s，,％%：:；;（）()]", "", nfkc(s)).translate(_DASH_UNIFY)


def _pdf_page_ground(pdf_path: Path) -> tuple[dict[int, set], dict[int, str]]:
    """PDF 页文本 → (每页数字 token 集, 每页归一化全文)。数值存在性/quote 回验的地面真值。
    token 集为行级 ∪ 全文级：数值在 PDF 文本流中可能跨行断裂（「11,543,178.\n34」），
    仅按行切会丢失整值 token，与 md 侧同构归一后无法对齐。"""
    import fitz

    tokens: dict[int, set] = {}
    normtext: dict[int, str] = {}
    with fitz.open(pdf_path) as doc:
        for pno in range(doc.page_count):
            text = nfkc(doc[pno].get_text() or "")
            toks = set()
            for line in text.splitlines():
                for variant in _numeric_token_variants(line):
                    toks.update(variant)
            for variant in _numeric_token_variants(text):  # 全文级：跨行断裂数值
                toks.update(variant)
            tokens[pno + 1] = toks
            normtext[pno + 1] = _seg_norm(text)
    return tokens, normtext


def _iter_numeric_cells(obj: dict):
    """产出 (row_item, value)：含数字的数据 cell（列名与值拼接）。"""
    for row in obj.get("rows") or []:
        item = row.get("item") or ""
        for k, v in row.items():
            if k in ("item", "source", "reason", "reason_method") or not isinstance(v, str):
                continue
            if re.search(r"\d", v):
                yield item, v


def _unique_prefix_repair(val: str, union: set) -> dict:
    """cell 内 miss 的数值残片在页 token 集中的唯一前缀候选。仅诊断提示（docling cell 内
    换行丢尾位形态），人工复核后决定是否修表——不自动回填防盲猜污染。候选长度须在
    残片 +6 位内：全文级 merged 会把整行数值连成几十位巨型 token，不挡会淹没唯一性。"""
    out: dict[str, str] = {}
    for variant in _numeric_token_variants(val):
        for tok in variant:
            if tok in union:
                continue
            cands = sorted(t for t in union
                           if t.startswith(tok) and t != tok and len(t) <= len(tok) + 6)
            if len(cands) == 1:
                out.setdefault(tok, cands[0])
    return out


def value_existence_findings(obj: dict, tid: str, file_rel: str,
                             page_tokens: dict[int, set]) -> list[dict]:
    """数值存在性：表内每个数字 token 必须真实出现在其溯源页的 PDF 文本（幻觉硬拦截）。"""
    pages = (obj.get("provenance") or {}).get("pages") or []
    union: set = set()
    for p in pages:
        union |= page_tokens.get(int(p), set())
    if not union:
        return []
    suspects, repairs, total = [], {}, 0
    for item, val in _iter_numeric_cells(obj):
        total += 1
        if not _tokens_all_hit(val, union):
            suspects.append(f"{item}:{val[:24]}")
            repairs.update(_unique_prefix_repair(val, union))
    if not suspects:
        return []
    ratio = len(suspects) / max(1, total)
    verdict = "demote" if (ratio > 0.3 or len(suspects) > 20) else "degraded"
    finding = {"id": tid, "verdict": verdict, "reason": "value_not_on_page",
               "file": file_rel, "detail": f"{len(suspects)}/{total} 数值不存在于溯源页文本",
               "samples": suspects[:6]}
    if repairs:
        finding["repair_candidates"] = dict(list(repairs.items())[:6])
    return [finding]


FOOT_TOTAL_RE = re.compile(r"合计|小计|总计")


def _parse_num(s) -> float | None:
    raw = nfkc(str(s or "")).strip()
    neg = bool(re.fullmatch(r"[（(][\d.,\-]+[)）]", raw))
    # 粘连多值单元格（docling 把两行并成 "(164,904,908) (6,155,136)"，美的 CF 1.6e15 实证）：
    # 直接拼接成天文数字会污染勾稽与下游——多于一个长数字 token 即放弃；
    # 短 token（附注序号）容忍并取最长 token 解析
    toks = re.findall(r"\d[\d,，.]*", raw)
    if len(toks) > 1:
        longest = max(toks, key=len)
        if any(len(t) >= 3 and t != longest for t in toks):
            return None
        raw = longest
    raw = re.sub(r"[（）(),，\s]", "", raw).replace("％", "").replace("＋", "+").replace("－", "-")
    if not re.search(r"\d", raw):
        return None
    try:
        v = float(raw.rstrip("%"))
    except ValueError:
        return None
    return -v if neg else v


def _row_cells_numeric(row: dict) -> dict[str, float]:
    out = {}
    for k, v in row.items():
        if k in ("item", "source", "reason", "reason_method") or not isinstance(v, str):
            continue
        n = _parse_num(v)
        if n is not None:
            out[k] = n
    return out


def crossfoot_findings(obj: dict, tid: str, file_rel: str) -> list[dict]:
    """勾稽校验：恒等式（资产=负债+权益）、合计=Σ分项（减:负、其中:跳过）、期初+增减=期末、yoy 重算。

    只记 degraded 异常（quality.json + gaps），不删行——跨页合计/准则口径差异留给 Agent 复核。
    """
    rows = obj.get("rows") or []
    rtype = obj.get("record_type") or obj.get("promoted_to_type") or ""
    findings: list[dict] = []
    notes: dict[str, list] = {}

    def note(kind, sample):
        notes.setdefault(kind, []).append(sample)

    if rtype == "balance_sheet":
        def _nums_by_pred(pred):
            for row in rows:
                sq = re.sub(r"\s+", "", nfkc(row.get("item") or ""))
                if pred(sq):
                    nums = _row_cells_numeric(row)
                    if nums:
                        return nums
            return None

        # 资产侧须整行精确匹配「资产总计」——子串匹配会先命中「非流动资产合计」
        # （续片链缺流动资产半段时，神华 480,792≠668,022 误报实证）
        assets = _nums_by_pred(
            lambda s: s in ("资产总计", "资产合计", "资产总值", "資產總值"))
        liab_eq = _nums_by_pred(lambda s: bool(re.search(
            r"负债[和及](?:所有者|股东|股東)?权益(?:总计|总额|合计)", s)))
        if assets is not None and liab_eq is not None:
            # 期别列对齐：只比较两侧共有的数值列（多年摘要表各年份列各自恒等）；
            # 禁止 max-abs 整行取值——会错拿异期列（摘要表 2022 列对 2024 列实证）
            for col in sorted(set(assets) & set(liab_eq)):
                a_v, l_v = assets[col], liab_eq[col]
                if abs(a_v - l_v) > max(1, 0.005 * abs(a_v)):
                    note("identity_mismatch", f"{col} 资产总计 {a_v:g} ≠ 负债和权益总计 {l_v:g}")

    if rtype in ("balance_sheet", "income_stmt", "cashflow_stmt"):
        # 同一 typed 表文件 = 同一合并链 = 同一逻辑报表：跨物理分片累计勾稽，
        # 仅在 合计/小计 行清零——按 source.table 分段会把节截断（陕煤「非流动资产合计」
        # 分片起点在节中段，局部和≠合计 的误报实证）
        col_max: dict[str, float] = {}
        for row in rows:
            for k, v in _row_cells_numeric(row).items():
                col_max[k] = max(col_max.get(k, 0.0), abs(v))
        amt_cols = {k for k, m in col_max.items() if m >= 100}  # 排除附注号/序号列
        # CF 节结果行（各活动净额/净增加额）：是节结果而非分项，计入累计会污染下一节小计；
        # 但「…定期存款」「…限制用途资金的净额」等是真实分项——只匹配节结果（神华 p163 实证）
        cf_section_result = re.compile(
            r"(?:经营|投资|筹资|經營|投資|籌資)活动产生的现金流量净额|现金及现金等价物净[减增]加额")

        def _reconcilable(vals: list[float], v: float) -> bool:
            """合计不平时：剔除单行或相邻两行后能精确勾稽（0.5%）→ 未标注其中子项
            （长电 应收股利≈其他应收款）或折行残片（神华 p162「股利、利润」），豁免不报。"""
            tol = max(1, 0.005 * abs(v))
            total = sum(vals)
            for i in range(len(vals)):
                if abs(total - vals[i] - v) <= tol:
                    return True
            for i in range(len(vals) - 1):
                if abs(total - vals[i] - vals[i + 1] - v) <= tol:
                    return True
            return False

        bad_total = 0
        for col in sorted(amt_cols):
            run, contributors, bad = 0.0, 0, 0
            contrib_vals: list[float] = []
            for row in rows:
                label = (row.get("item") or "").strip()
                # docling 常在科目名中断空白（「归属于母公司股东权益合 计」长电实证）——
                # 标签判定一律用去空白形式
                label_sq = re.sub(r"\s+", "", label)
                nums = _row_cells_numeric(row)
                v = nums.get(col)
                if FOOT_TOTAL_RE.search(label_sq):
                    # 合计行是节边界：本列无数值也要清零（跨片列错位时防止上游节渗入，
                    # 长电 p081「股东权益合计」Σ≈资产总计 实证）
                    if v is not None and contributors >= 2 \
                            and abs(run - v) > max(1, 0.005 * abs(v)) \
                            and not _reconcilable(contrib_vals, v):
                        bad += 1
                        note("subtotal_mismatch", f"{label_sq} {v:g} ≠ Σ分项 {run:g}")
                    run, contributors, contrib_vals = 0.0, 0, []
                elif v is None:
                    continue
                elif label_sq.startswith("其中"):
                    continue
                elif cf_section_result.search(label_sq):
                    continue
                else:
                    # 「减:」前缀仅在数值为正时取负——括号负数已含符号，双重取反
                    # 会把 减:库存股 (8,151,117) 加成 +8,151,117（美的 BS 实证）
                    contrib = -v if (label_sq.startswith("减") and v > 0) else v
                    run += contrib
                    contributors += 1
                    contrib_vals.append(contrib)
            bad_total += bad
        if bad_total:
            findings.append({"id": tid, "verdict": "degraded", "reason": "subtotal_mismatch",
                             "file": file_rel, "detail": f"{bad_total} 处合计与分项之和不符",
                             "samples": (notes.get("subtotal_mismatch") or [])[:6]})

    labels = {c.get("key"): nfkc(c.get("label") or "")
              for c in (obj.get("schema") or {}).get("columns") or []}
    k_begin = next((k for k, lb in labels.items() if "期初" in lb), None)
    k_end = next((k for k, lb in labels.items() if "期末" in lb or "本年" in lb), None)
    k_chg = next((k for k, lb in labels.items()
                  if ("增减" in lb or "变动" in lb) and "%" not in lb and "％" not in lb), None)
    if k_begin and k_end and k_chg:
        bad = 0
        for row in rows:
            nb, ne, nc = (_parse_num(row.get(k)) for k in (k_begin, k_end, k_chg))
            if nb is None or ne is None or nc is None:
                continue
            if abs(nb + nc - ne) > max(1, 0.005 * abs(ne)):
                bad += 1
                note("roll_mismatch", row.get("item") or "")
        if bad:
            findings.append({"id": tid, "verdict": "degraded", "reason": "roll_mismatch",
                             "file": file_rel, "detail": f"{bad} 行 期初+增减≠期末"})

    if rtype == "variance_reasons":
        bad = 0
        for row in rows:
            cur = _parse_num(row.get("value_current") or "")
            pri = _parse_num(row.get("value_prior") or "")
            yoy = _parse_num(str(row.get("yoy_pct") or ""))
            if cur is None or pri is None or not pri or yoy is None:
                continue
            expect = (cur - pri) / abs(pri) * 100
            if abs(expect - yoy) > max(0.5, 0.01 * abs(yoy)):
                bad += 1
                note("yoy_mismatch", f"{row.get('item')}: 表述 {yoy:g}% vs 重算 {expect:.1f}%")
        if bad:
            findings.append({"id": tid, "verdict": "degraded", "reason": "yoy_mismatch",
                             "file": file_rel, "detail": f"{bad} 行同比与金额重算不符"})

    if notes.get("identity_mismatch"):
        findings.append({"id": tid, "verdict": "degraded", "reason": "identity_mismatch",
                         "file": file_rel, "detail": "; ".join(notes["identity_mismatch"][:2])})
    return findings


def quote_verify_findings(obj: dict, tid: str, file_rel: str,
                          page_tokens: dict[int, set], page_normtext: dict[int, str]) -> list[dict]:
    """quote 回验（逐 token）：quote 的每个数值 token 必须在该页文本中存在；非数字段
    按 cell 分段校验存在性。整串连续匹配不可行——docling 行 cell 序与 PDF 文本流序
    （fitz 按 y 坐标，多行 cell/列序错位）结构性不一致，行级拼接子串必误报。"""
    bad = []
    for row in obj.get("rows") or []:
        src = row.get("source") or {}
        q, page = src.get("quote") or "", src.get("page")
        if not q or not page:
            continue
        toks = page_tokens.get(int(page), set())
        ground = page_normtext.get(int(page), "")
        num_miss = not _tokens_all_hit(q, toks)
        seg_miss = any(
            seg and seg not in ground
            # 与 ground 同归一化（_seg_norm，保留数字）——seg 删数字会与保留数字的
            # ground 不对称（如「减少0.47个百分点」段删数字后必不匹配）
            for seg in (_seg_norm(s) for s in q.split())
        )
        if num_miss or seg_miss:
            bad.append(f"{row.get('item')}:{q[:30]}")
    if bad:
        return [{"id": tid, "verdict": "degraded", "reason": "quote_unverified",
                 "file": file_rel, "detail": f"{len(bad)} 条 quote 未通过溯源页校验",
                 "samples": bad[:5]}]
    return []


def python_qa_findings(result_dir: Path, pdf_path: Path | None = None) -> list[dict]:
    """机械化检查：列错位、缺单位、垃圾表头 + 勾稽/数值存在性/quote 回验（v2 质量门）。"""
    manifest = _load_manifest(result_dir)
    findings = []
    page_tokens = page_normtext = None
    if pdf_path is not None and pdf_path.is_file():
        try:
            page_tokens, page_normtext = _pdf_page_ground(pdf_path)
        except Exception as e:
            print(f"PDF 地面真值不可用（跳过数值/quote 校验）: {e}", file=sys.stderr)
    for ent in manifest.get("catalog", {}).get("tables") or []:
        tid = ent.get("id") or ""
        if tid.startswith(("generic_table_", "generic_merged_")):
            continue
        obj = read_json(result_dir / ent["file"], {}) or {}
        rows = obj.get("rows") or []
        cols = [c.get("label") or "" for c in (obj.get("schema") or {}).get("columns") or []]
        if cols and len(set(nfkc(c) for c in cols[1:] if c)) == 1 and len(cols) > 3:
            findings.append({"id": tid, "verdict": "degraded", "reason": "duplicate_headers",
                             "file": ent["file"]})
        rtype = obj.get("record_type") or obj.get("promoted_to_type") or tid
        if rtype == "key_financials" and not (obj.get("unit_default") or "").strip():
            findings.append({"id": tid, "verdict": "degraded", "reason": "missing_unit",
                             "file": ent["file"]})
        if rtype == "variance_reasons":
            bad = 0
            checked = 0
            for row in rows:
                cur_m = _num_magnitude(str(row.get("value_current") or ""))
                pri_m = _num_magnitude(str(row.get("value_prior") or ""))
                if cur_m is None or pri_m is None:
                    continue
                checked += 1
                if abs(cur_m - pri_m) >= 2:
                    bad += 1
            if checked and bad / checked >= 0.4:
                findings.append({"id": tid, "verdict": "demote", "reason": "column_misaligned",
                                 "file": ent["file"], "detail": f"{bad}/{checked} rows magnitude gap"})
        findings += crossfoot_findings(obj, tid, ent["file"])
        if page_tokens is not None:
            findings += value_existence_findings(obj, tid, ent["file"], page_tokens)
            findings += quote_verify_findings(obj, tid, ent["file"], page_tokens, page_normtext)
        base = _table_base_id(tid)
        if base not in STMT_ROW_LABEL_RULES and rtype in STMT_ROW_LABEL_RULES:
            base = str(rtype)
        if base in STMT_ROW_LABEL_RULES:
            stmt_f = _statement_row_qa_finding(tid, base, obj, ent["file"])
            if stmt_f:
                findings.append(stmt_f)
    return findings


def _demote_table(result_dir: Path, catalog: list, ent: dict, reason: str, *, unlink_src: bool = True) -> dict:
    src = result_dir / ent["file"]
    obj = read_json(src, {}) or {}
    page = (obj.get("provenance") or {}).get("pages") or [0]
    idx = (obj.get("provenance") or {}).get("tables") or [0]
    new_id = _generic_table_id({"page": page[0] if page else 0, "index": idx[0] if idx else 0})
    if any(e.get("id") == new_id for e in catalog) or (result_dir / f"tables/{_slug(new_id)}.json").is_file():
        new_id = f"{new_id}_demoted"
    dest_rel = f"tables/{_slug(new_id)}.json"
    obj["table_id"] = new_id
    obj["group"] = "Z_generic"
    obj["source_type"] = "generic_table"
    obj["record_type"] = None
    obj["demoted_from"] = ent.get("id")
    obj["demote_reason"] = reason
    obj["description"] = "质量门取消定型，退回 generic"
    write_json(result_dir / dest_rel, obj)
    if unlink_src and src.resolve() != (result_dir / dest_rel).resolve() and src.is_file():
        src.unlink(missing_ok=True)
    return {
        "id": new_id, "file": dest_rel, "group": "Z_generic",
        "method": "record_map", "row_count": obj.get("row_count") or 0,
        "record_type": None, "source_type": "generic_table",
        "demoted_from": ent.get("id"),
    }


def validate_narrative_kpi_gate(result_dir: Path) -> list[dict]:
    """叙述 KPI 硬门：status=found 必须有 quote+page；否则记 suspect。

    关键词命中不等于提取成功。已落盘 narratives/*.json 中 found bullet 缺证据 → gaps。
    """
    findings: list[dict] = []
    narr_dir = result_dir / "narratives"
    if not narr_dir.is_dir():
        return findings
    for path in sorted(narr_dir.glob("*.json")):
        obj = read_json(path, {}) or {}
        nid = obj.get("narrative_id") or path.stem
        for i, bullet in enumerate(obj.get("bullets") or []):
            if not isinstance(bullet, dict):
                continue
            st = (bullet.get("status") or "").strip().lower()
            if st != "found":
                continue
            quote = (bullet.get("quote") or "").strip()
            page = bullet.get("page")
            ok_page = isinstance(page, int) and page > 0
            if not quote or not ok_page:
                findings.append({
                    "id": f"narrative_kpi::{nid}::{i}",
                    "narrative_id": nid,
                    "verdict": "degraded",
                    "reason": "narrative_kpi_gate",
                    "detail": "found bullet 缺少 quote 或 page，不得当作下游事实",
                    "label": bullet.get("label"),
                })
        if (obj.get("status") or "").strip().lower() == "found":
            quote = (obj.get("quote") or "").strip()
            page = obj.get("page")
            ok_page = isinstance(page, int) and page > 0
            if not quote or not ok_page:
                findings.append({
                    "id": f"narrative_kpi::{nid}",
                    "narrative_id": nid,
                    "verdict": "degraded",
                    "reason": "narrative_kpi_gate",
                    "detail": "found 叙述块缺少 quote 或 page",
                })
    return findings


def apply_qa(sha12: str, agent_verdicts: list[dict] | None = None, *, result_name: str | None = None) -> dict:
    result_dir = _result_dir(sha12, result_name)
    manifest = _load_manifest(result_dir)
    catalog = list(manifest.setdefault("catalog", {}).setdefault("tables", []))
    pdf_path = entry_dir(sha12) / "report.pdf"
    py_findings = python_qa_findings(result_dir, pdf_path=pdf_path)
    narr_findings = validate_narrative_kpi_gate(result_dir)
    merged: dict[str, dict] = {}
    for f in py_findings:
        if f.get("verdict") in ("demote", "split"):
            merged[f["id"]] = {**f, "source": "python"}
    for v in agent_verdicts or []:
        tid = v.get("id") or v.get("table_id")
        if not tid:
            continue
        prev = merged.get(tid, {})
        if prev.get("verdict") == "demote" and (v.get("verdict") or "") != "demote":
            continue
        merged[tid] = {**v, "id": tid, "source": "agent"}
    table_results = []
    new_catalog = []
    demoted = 0
    by_id = {e.get("id"): e for e in catalog}
    handled = set()
    for tid, finding in merged.items():
        ent = by_id.get(tid)
        if not ent or str(tid).startswith("generic_table_"):
            continue
        verdict = finding.get("verdict") or "pass"
        if verdict == "split" and finding.get("keep_items"):
            obj = read_json(result_dir / ent["file"], {}) or {}
            keep = set(finding.get("keep_items") or [])
            keep_rows = [r for r in obj.get("rows") or [] if (r.get("item") or "") in keep]
            drop_rows = [r for r in obj.get("rows") or [] if (r.get("item") or "") not in keep]
            obj["rows"] = keep_rows
            obj["row_count"] = len(keep_rows)
            write_json(result_dir / ent["file"], obj)
            ent["row_count"] = len(keep_rows)
            if drop_rows:
                generic = _demote_table(
                    result_dir, catalog, dict(ent), finding.get("reason") or "split",
                    unlink_src=False,
                )
                drop_obj = read_json(result_dir / generic["file"], {}) or {}
                drop_obj["rows"] = drop_rows
                drop_obj["row_count"] = len(drop_rows)
                write_json(result_dir / generic["file"], drop_obj)
                generic["row_count"] = len(drop_rows)
                new_catalog.append(generic)
            new_catalog.append(ent)
            handled.add(tid)
            table_results.append({"id": tid, "verdict": "split", "reason": finding.get("reason")})
            continue
        if verdict == "demote":
            generic = _demote_table(result_dir, catalog, ent, finding.get("reason") or "contaminated")
            new_catalog.append(generic)
            handled.add(tid)
            demoted += 1
            table_results.append({
                "id": tid, "verdict": "demote", "reason": finding.get("reason"),
                "became": generic["id"],
            })
            continue
        table_results.append({"id": tid, "verdict": verdict, "reason": finding.get("reason")})
    for ent in catalog:
        if ent.get("id") in handled:
            continue
        new_catalog.append(ent)
        if not str(ent.get("id") or "").startswith("generic_table_"):
            if ent.get("id") not in merged:
                table_results.append({"id": ent.get("id"), "verdict": "pass"})
    manifest["catalog"]["tables"] = new_catalog
    split_or_demote = demoted or any(t.get("verdict") in ("demote", "split") for t in table_results)
    quality = {
        "status": "fail" if split_or_demote else "pass",
        "checked_at": now_iso(),
        "tables": table_results,
        "python_findings": py_findings,
        "narrative_kpi_findings": narr_findings,
    }
    manifest["quality"] = {"status": quality["status"], "file": "quality.json"}
    write_json(result_dir / "quality.json", quality)
    write_json(result_dir / "manifest.json", manifest)
    # suspect 数值/quote 落 gaps.json，供 Agent 复核闭环
    qa_gaps = []
    for f in py_findings:
        if f.get("reason") in ("value_not_on_page", "quote_unverified"):
            qa_gaps.append({
                "id": f"qa::{f.get('id')}", "group": "Z_qa", "table_id": f.get("id"),
                "reason": f"{f.get('reason')}: {f.get('detail')}",
                "status": "suspect", "samples": f.get("samples") or [],
            })
    for f in narr_findings:
        qa_gaps.append({
            "id": f.get("id"),
            "group": "Z_narrative_kpi",
            "narrative_id": f.get("narrative_id"),
            "reason": f"{f.get('reason')}: {f.get('detail')}",
            "status": "suspect",
            "label": f.get("label"),
        })
    # qa::/narrative_kpi:: 前缀是本次 QA 的机器发现快照：重跑全量重建，
    # 修复（换源/改 quote）后旧 suspect 自动消失；Agent 复核结论请用独立 id 落盘
    gaps_path = result_dir / "gaps.json"
    gaps = read_json(gaps_path, [])
    if isinstance(gaps, list):
        gaps = [g for g in gaps if not str(g.get("id") or "").startswith(("qa::", "narrative_kpi::"))]
        gaps.extend(qa_gaps)
        write_json(gaps_path, gaps)
    # 同步缓存索引：用于 `wm_report.py cache info` 的快速定位
    index_upsert(
        sha12,
        latest_result=result_dir.name,
        quality_status=quality["status"],
        quality_checked_at=quality.get("checked_at"),
        catalog_tables=len(manifest.get("catalog", {}).get("tables") or []),
        catalog_fields=len(manifest.get("catalog", {}).get("fields") or []),
    )
    return {"result_dir": str(result_dir), "status": quality["status"], "demoted": demoted}


def _terminal_gap_status(status: str | None) -> bool:
    return (status or "") in ("found", "not_disclosed", "not_applicable", "not_found")


def build_evolution_proposal(meta: dict, adapt_plan: dict, review: dict, result_dir: Path) -> dict:
    profile = meta.get("document_profile") or {}
    industry = (meta.get("industry_hint") or {}).get("industry") or profile.get("industry")
    # 行业置信度分级（E4）：weak 显性化；年报 null/weak 未继承时警示（未适配行业应显式暴露）
    _conf = float(profile.get("industry_confidence")
                  or (meta.get("industry_hint") or {}).get("confidence") or 0.0)
    profile["industry_confidence_bucket"] = (
        "strong" if _conf >= 0.5 else "medium" if _conf >= 0.3
        else "weak" if _conf > 0.0 else "none")
    gaps = read_json(result_dir / "gaps.json", []) or []
    required_open = [
        {"id": g.get("id"), "status": g.get("status"), "reason": g.get("reason")}
        for g in gaps if g.get("status") == "required"
    ]
    generic_candidates = read_json(result_dir / "promote_candidates.json", {}) or {}
    typed_bases = _typed_base_ids(((_load_manifest(result_dir).get("catalog") or {}).get("tables")) or [])
    observed = adapt_plan.get("observed_signals") or []
    observed_by_type = {o.get("type"): o for o in observed if o.get("type")}
    expected_missing = list(adapt_plan.get("expected_but_missing") or [])
    for h in review.get("hard_failures") or []:
        if h.get("id") == "statement_signature_gap":
            for tid in h.get("items") or []:
                if tid not in expected_missing:
                    expected_missing.append(tid)
    missing_type_signatures = []
    evidence_quotes = []
    for typ in expected_missing:
        obs = observed_by_type.get(typ) or {}
        ev = list(obs.get("evidence") or [])
        missing_type_signatures.append({
            "type": typ,
            "evidence_quotes": ev,
            "strength": obs.get("strength") or "prior",
            "suggested_action": "补 type 签名或重跑 extract-tables --force 后再 promote",
        })
        evidence_quotes.extend(ev[:3])
    noise_hints = []
    useful_hints = []
    for c in generic_candidates.get("candidates") or []:
        hint = c.get("type_hint")
        if not hint:
            continue
        entry = {
            "table_id": c.get("table_id"),
            "type_hint": hint,
            "title": c.get("title"),
        }
        if _is_noise_type_hint(hint, industry):
            noise_hints.append({**entry, "reason": f"hint 锁定行业≠当前 industry={industry}"})
        elif hint in expected_missing or hint not in typed_bases:
            if hint in expected_missing:
                useful_hints.append(entry)
    actions = []
    if expected_missing:
        actions.append({
            "cmd": f"wm_report.py extract-tables {meta.get('cache_id')} --force",
            "reason": f"内容/先验期望未定型: {expected_missing}",
        })
        actions.append({
            "cmd": f"wm_report.py adapt-plan {meta.get('cache_id')} --result {result_dir.name} --force",
            "reason": "重抽后刷新 observed_signals / expected_but_missing",
        })
    if noise_hints:
        actions.append({
            "cmd": "review promote_candidates: drop sector-locked noise hints",
            "reason": f"跨行业噪声 hint ×{len(noise_hints)}",
        })
    novelty_reasons = list(profile.get("novelty_reasons") or [])
    for h in review.get("hard_failures") or []:
        rid = h.get("id")
        if rid and rid not in novelty_reasons:
            novelty_reasons.append(str(rid))
    return {
        "id": "evolution_proposal",
        "created_at": now_iso(),
        "source_cache_id": meta.get("cache_id"),
        "document_profile": profile,
        "novelty_reasons": novelty_reasons,
        "review_warnings": review.get("warnings") or [],
        "review_hard_failures": review.get("hard_failures") or [],
        "required_open_gaps": required_open,
        "suggestions": {
            "actions": actions,
            "missing_type_signatures": missing_type_signatures,
            "noise_type_hints": noise_hints[:12],
            "candidate_signatures_to_add": useful_hints[:8],
            "new_industry_keywords": [],
            "new_type_hint_signatures": useful_hints[:8] or [
                {"type": m.get("type"), "evidence_quotes": m.get("evidence_quotes")}
                for m in missing_type_signatures[:8]
            ],
            "filing_kind_examples": [{
                "title": (meta.get("source") or {}).get("title") or "",
                "filing_kind": meta.get("filing_kind"),
                "market": profile.get("market"),
            }],
            "fixture_draft": {
                "cache_id": meta.get("cache_id"),
                "industry": industry,
                "filing_kind": meta.get("filing_kind"),
                "expected_but_missing": expected_missing,
            },
        },
        "gate_requirements": [
            "ci/validate.sh 全绿",
            "新增或更新 required/nightly 样本",
            "人工批准后再并入规则库",
        ],
        "evidence_quotes": list(dict.fromkeys(evidence_quotes))[:12],
    }


def review_extract(sha12: str, *, result_name: str | None = None) -> dict:
    result_dir = _result_dir(sha12, result_name)
    manifest = _load_manifest(result_dir)
    meta = read_json(entry_dir(sha12) / "meta.json", {}) or {}
    adapt_plan = read_json(result_dir / "adapt_plan.json")
    if not adapt_plan:
        adapt_plan = build_adapt_plan(meta, result_dir.name, sha12=sha12)
        write_json(result_dir / "adapt_plan.json", adapt_plan)
        manifest["adapt_plan_file"] = "adapt_plan.json"
    quality = read_json(result_dir / "quality.json")
    gaps = read_json(result_dir / "gaps.json", []) or []
    narratives = manifest.setdefault("catalog", {}).get("narratives") or []
    typed_tables = [t for t in (manifest.get("catalog", {}).get("tables") or [])
                    if not str(t.get("id") or "").startswith("generic_")]
    hard_failures: list[dict] = []
    warnings: list[dict] = []
    narrative_findings = validate_narrative_kpi_gate(result_dir)
    if not quality:
        hard_failures.append({"id": "quality_json_required", "reason": "missing quality.json"})
    else:
        if narrative_findings:
            hard_failures.append({"id": "narrative_quote_page_required", "reason": "narrative KPI 缺 quote/page"})
        if any(q.get("verdict") in ("demote", "split") for q in (quality.get("tables") or [])):
            warnings.append({"id": "demote_or_split_detected", "reason": "quality.json 存在 demote/split"})
    required_ids = {g.get("id") for g in (adapt_plan.get("required_gaps") or []) if g.get("id")}
    gap_by_id = {g.get("id"): g for g in gaps if g.get("id")}
    open_required = [gid for gid in sorted(required_ids) if not _terminal_gap_status((gap_by_id.get(gid) or {}).get("status"))]
    if open_required:
        hard_failures.append({
            "id": "required_gaps_must_be_terminal",
            "reason": "required gaps 尚未终态",
            "items": open_required,
        })
    md_path = entry_dir(sha12) / "report.md"
    page_texts = _page_texts_from_md_lines(md_path.read_text(encoding="utf-8").splitlines()) if md_path.is_file() else {}
    for n in narratives:
        nfile = result_dir / (n.get("file") or "")
        if not nfile.is_file():
            continue
        obj = read_json(nfile, {}) or {}
        if (obj.get("status") or "").strip().lower() != "found":
            continue
        quote = (obj.get("quote") or "").strip()
        page = obj.get("page")
        if quote and isinstance(page, int) and page > 0 and not quote_on_page(quote, page_texts.get(page) or ""):
            hard_failures.append({
                "id": "quote_must_verify_on_page",
                "reason": f"narrative {obj.get('id') or n.get('id')} quote 不在声明页",
            })
            break
    profile = meta.get("document_profile") or {}
    if not (meta.get("industry_hint") or {}).get("industry"):
        invalid = [t.get("id") for t in typed_tables if str(t.get("group") or "").startswith("X_")]
        if invalid:
            hard_failures.append({
                "id": "profile_consistency",
                "reason": "industry=null 时出现行业层 typed 表",
                "items": invalid,
            })
    filing_kind = meta.get("filing_kind") or profile.get("filing_kind")
    if _is_q1_q3(filing_kind):
        invalid = []
        for n in narratives:
            if n.get("group") == "D_mda" and n.get("status") == "found":
                invalid.append(n.get("id"))
        if invalid:
            hard_failures.append({
                "id": "profile_consistency",
                "reason": "q1/q3 不应把完整 MD&A 叙述标为 found",
                "items": invalid,
            })
    typed_bases = _typed_base_ids(typed_tables)
    missing_statements = [tid for tid in CORE_STATEMENT_TYPES if tid not in typed_bases]
    # 正文已观察但未定型 → 并入缺口
    for o in adapt_plan.get("observed_signals") or []:
        typ = o.get("type")
        if typ in CORE_STATEMENT_TYPES and typ not in typed_bases and typ not in missing_statements:
            missing_statements.append(typ)
    for typ in adapt_plan.get("expected_but_missing") or []:
        if typ in CORE_STATEMENT_TYPES and typ not in typed_bases and typ not in missing_statements:
            missing_statements.append(typ)
    if missing_statements:
        gap_item = {
            "id": "statement_signature_gap",
            "reason": "三表未全部定型或正文信号未落地",
            "items": missing_statements,
        }
        # 年报/半年报：硬失败；一季报/三季报：仅 warning（体量常缺完整利润表）
        if filing_kind in ("annual", "semi") or (
            filing_kind not in ("q1", "q3", "quarter", "prospectus") and not _is_q1_q3(filing_kind)
        ):
            hard_failures.append(gap_item)
        else:
            warnings.append(gap_item)
    generic_candidates = read_json(result_dir / "promote_candidates.json", {}) or {}
    latent_hints = [c.get("table_id") for c in (generic_candidates.get("candidates") or [])
                    if c.get("type_hint") and _table_base_id(c.get("table_id")) not in typed_bases
                    and not _is_noise_type_hint(c.get("type_hint"),
                                               (meta.get("industry_hint") or {}).get("industry") or profile.get("industry"))]
    if latent_hints:
        warnings.append({"id": "unpromoted_type_hints", "reason": "存在反复出现但未 promote 的 type_hint", "items": latent_hints[:12]})
    # 裸 id 三表 variant 异常：canonical 不应是摘要/分析/母公司副本（B2 选主回归监控）
    variant_anomaly = []
    for cat in (manifest.get("catalog") or {}).get("tables") or []:
        if cat.get("id") in CORE_STATEMENT_TYPES and cat.get("variant") not in (None, "primary"):
            variant_anomaly.append({"id": cat.get("id"), "variant": cat.get("variant")})
    if variant_anomaly:
        warnings.append({
            "id": "primary_statement_variant_anomaly",
            "reason": "裸 id 三表的 variant 非 primary（选主异常，下游慎用）",
            "items": variant_anomaly,
        })
    if profile.get("industry_confidence_bucket") in ("weak", "none") \
            and (filing_kind == "annual" or filing_kind == "semi") \
            and not (meta.get("industry_hint") or {}).get("inherited_from"):
        warnings.append({
            "id": "annual_industry_weak",
            "reason": f"年报/半年报行业置信度 {profile.get('industry_confidence_bucket')}"
                      f"（conf={_conf:.2f}）——行业目录可能未适配，按 adaptation.md 提案",
        })
    degraded_findings = [{"id": f.get("id"), "reason": f.get("reason"),
                          "adjudicated": f.get("adjudicated")}
                         for f in (quality or {}).get("python_findings") or []
                         if f.get("verdict") == "degraded" and not f.get("adjudicated")]
    if degraded_findings:
        warnings.append({
            "id": "tables_with_degraded_findings",
            "reason": "存在未仲裁的 degraded 勾稽/回验发现（qa_adjudication 任务可闭环）",
            "items": degraded_findings[:12],
        })
    # 刷新 adapt 中的 expected_but_missing（review 时点更准）
    adapt_plan["expected_but_missing"] = sorted(
        set(adapt_plan.get("expected_but_missing") or []) | set(missing_statements)
    )
    write_json(result_dir / "adapt_plan.json", adapt_plan)
    review = {
        "cache_id": sha12,
        "result_dir": result_dir.name,
        "reviewed_at": now_iso(),
        "status": "fail" if hard_failures else "pass",
        "hard_failures": hard_failures,
        "warnings": warnings,
        "document_profile": profile,
        "quality_status": (quality or {}).get("status") or "missing",
        "novelty": bool(profile.get("novelty") or warnings or hard_failures),
    }
    proposal = None
    if review["novelty"] or hard_failures:
        proposal = build_evolution_proposal(meta, adapt_plan, review, result_dir)
        proposal_path = result_dir / "derived" / "evolution_proposal.json"
        write_json(proposal_path, proposal)
        _upsert_manifest_derived(manifest, {
            "id": "evolution_proposal",
            "file": "derived/evolution_proposal.json",
            "group": "Z_evolution",
            "method": "review_extract",
        })
        review["evolution_proposal_file"] = "derived/evolution_proposal.json"
    write_json(result_dir / "review.json", review)
    manifest["review"] = {"status": review["status"], "file": "review.json"}
    write_json(result_dir / "manifest.json", manifest)
    return review


def cmd_apply_promotions(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(prog="wm_report.py apply-promotions",
                                 description="应用 Agent type_promote JSON（仅 confidence=high）")
    ap.add_argument("sha12")
    ap.add_argument("--file", required=True, help="promotions JSON：list 或 {promotions:[]}")
    ap.add_argument("--result", default="")
    args = ap.parse_args(argv)
    raw = read_json(Path(args.file).expanduser(), {}) or {}
    items = raw if isinstance(raw, list) else (raw.get("promotions") or raw.get("items") or [])
    out = apply_promotions(args.sha12, items, result_name=args.result or None)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_qa_tables(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py qa-tables",
        description="提取后质量门：Python 机械化检查 + 可选 Agent verdicts；污染表 demote",
    )
    ap.add_argument("sha12")
    ap.add_argument("--result", default="")
    ap.add_argument("--verdicts", default="", help="Agent QA JSON：list 或 {verdicts:[]}")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    verdicts = []
    if args.verdicts:
        raw = read_json(Path(args.verdicts).expanduser(), {}) or {}
        verdicts = raw if isinstance(raw, list) else (raw.get("verdicts") or raw.get("tables") or [])
    out = apply_qa(args.sha12, verdicts, result_name=args.result or None)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_review_extract(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py review-extract",
        description="独立审核提取产物：检查 quality/gaps/narratives，并在 novelty 时生成 evolution_proposal",
    )
    ap.add_argument("sha12")
    ap.add_argument("--result", default="")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    out = review_extract(args.sha12, result_name=args.result or None)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_render_html(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py render-html",
        description="将 result-* 渲染为单文件 HTML（仅 quality=pass 表；只读阅览）",
    )
    ap.add_argument("sha12")
    ap.add_argument("--result", default="", help="指定 result-*；默认取最新")
    ap.add_argument("--out", default="", help="输出路径；默认 {result_dir}/report.html")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    result_dir = _result_dir(args.sha12, args.result or None)
    if not (result_dir / "manifest.json").is_file():
        raise SystemExit(f"缺少 {result_dir}/manifest.json，请先 materialize-tables")
    from render_html import write_html_report  # noqa: WPS433 — 同目录模块

    out_path = Path(args.out).expanduser() if args.out else None
    dest = write_html_report(result_dir, cache_id=args.sha12, out_path=out_path)
    print(json.dumps({
        "cache_id": args.sha12,
        "result_dir": str(result_dir),
        "html": str(dest),
        "bytes": dest.stat().st_size,
    }, ensure_ascii=False, indent=1))


# --------------------------------------------------------------------------
# ⑤ fetch：wm-filings 查链接 / 直链 / 下载
# --------------------------------------------------------------------------

HUB_SCRIPTS = Path(__file__).resolve().parents[2] / "wm-skillhub" / "scripts"
if not (HUB_SCRIPTS / "_wm_runtime.py").is_file():
    HUB_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "wm-skillhub" / "scripts"


def query_filings(symbol: str, filing_type: str, report_date: str) -> dict:
    """调 wm-filings（经 wm-skillhub 的 _wm_runtime 鉴权）→ 选定条目。"""
    try:
        sys.path.insert(0, str(HUB_SCRIPTS))
        from _wm_runtime import api_base, post_json_authed
    except ImportError:
        raise SystemExit(
            "未找到 wm-skillhub 的 _wm_runtime（需已安装 wm-skillhub pack），或改用 --pdf-url"
        )
    if report_date:
        args_body = {"mode": "list", "filing_type": filing_type, "limit": 50}
    else:
        args_body = {"mode": "latest", "filing_type": filing_type}
    url = f"{api_base()}/v1/skills/wm-filings/run"
    payload = {"args": args_body, "symbol": symbol}
    skill_dir = Path(__file__).resolve().parents[1]
    status, raw = post_json_authed(url, payload, skill_dir=skill_dir)
    if status >= 400:
        raise SystemExit(f"wm-filings 调用失败 HTTP {status}: {raw[:200]}")
    try:
        result = json.loads(raw).get("data", {}).get("result", {})
    except ValueError:
        raise SystemExit(f"wm-filings 返回非 JSON: {raw[:200]}")
    items = result.get("items") or ([result["item"]] if result.get("item") else [])
    if not items:
        raise SystemExit(f"wm-filings 未返回财报条目（symbol={symbol}, filing_type={filing_type}）")
    if report_date:
        matched = [it for it in items if str(it.get("report_date") or "").startswith(report_date)]
        item = matched[0] if matched else items[0]
        if not matched:
            print(f"提示: report_date={report_date} 未精确命中，取最近一条 "
                  f"(report_date={item.get('report_date')})", file=sys.stderr)
    else:
        item = items[0]
    return item


def _open_url(url: str, headers: dict, *, no_proxy: bool, timeout: int = 60):
    """no_proxy=True 时绕过系统代理（macOS 上 urllib 会读系统代理，本地/内网直链会被代理劫持成 502）。"""
    if no_proxy:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        return opener.open(urllib.request.Request(url, headers=headers), timeout=timeout)
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout)


def download_pdf(url: str, dest: Path) -> None:
    attempts = [
        {"headers": {"User-Agent": UA}, "no_proxy": True},      # 直连优先
        {"headers": {"User-Agent": UA, "Referer": "https://www.cninfo.com.cn/"}, "no_proxy": True},
        {"headers": {"User-Agent": UA}, "no_proxy": False},     # 兜底走系统代理（公司网环境）
    ]
    last_err = None
    for a in attempts:
        try:
            with _open_url(url, a["headers"], no_proxy=a["no_proxy"]) as resp, dest.open("wb") as f:
                shutil.copyfileobj(resp, f)
            return
        except Exception as e:
            last_err = e
    raise SystemExit(f"下载失败: {url}\n最后错误: {last_err}")


def validate_downloaded_pdf(pdf_path: Path, *, filing_type: str, title: str, report_date: str) -> dict:
    """下载后校验页数/标题与 filing_type 一致，防并行竞态或错链。"""
    try:
        import fitz
    except ImportError:
        print("提示: 未安装 pymupdf，跳过 PDF 下载校验", file=sys.stderr)
        return {"pages": 0, "skipped": True}
    doc = fitz.open(pdf_path)
    pages = doc.page_count
    meta_title = nfkc(doc.metadata.get("title") or "")
    doc.close()
    combined = nfkc(title) + meta_title
    info = {"pages": pages, "pdf_title": meta_title}
    if filing_type == "quarter":
        if pages > 80:
            raise SystemExit(
                f"下载校验失败：季报预期 ≤80 页，实际 {pages} 页（可能下载到年报或错误文件）"
            )
        if "季度" not in combined and not any(k in combined for k in ("第一季度", "第二季度", "第三季度")):
            print(f"警告: 标题未含季度字样（pages={pages}）", file=sys.stderr)
    elif filing_type == "annual":
        if pages < 50:
            raise SystemExit(
                f"下载校验失败：年报预期 ≥50 页，实际 {pages} 页（可能下载到季报或错误文件）"
            )
    if report_date and report_date[:4] in combined:
        info["report_date_hint"] = report_date[:4]
    return info


def cmd_fetch(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(prog="wm_report.py fetch", description="查财报链接并下载入缓存")
    ap.add_argument("--symbol", default="")
    ap.add_argument("--filing-type", default="annual", choices=["annual", "semi", "quarter", "all"])
    ap.add_argument("--report-date", default="", help="如 2024-12-31；缺省取最新")
    ap.add_argument("--pdf-url", default="", help="直接给 PDF 链接（不经 wm-filings）")
    ap.add_argument("--title", default="", help="--pdf-url 时的标题备注")
    ap.add_argument("--convert", action="store_true", help="下载后立即转换")
    ap.add_argument("--accurate", action="store_true")
    ap.add_argument("--ocr", action="store_true")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--device", default="cpu", choices=["cpu", "mps", "cuda", "auto"])
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)

    if not args.symbol and not args.pdf_url:
        raise SystemExit("需要 --symbol 或 --pdf-url")
    if args.pdf_url:
        item = {"pdf_url": args.pdf_url, "title": args.title or args.pdf_url.split("/")[-1]}
    else:
        item = query_filings(args.symbol, args.filing_type, args.report_date)
    pdf_url = item.get("pdf_url")
    if not pdf_url:
        raise SystemExit(f"条目无 pdf_url: {json.dumps(item, ensure_ascii=False)[:300]}")

    tmp = cache_root() / f".download-{uuid.uuid4().hex}.pdf"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    print(f"下载 {pdf_url} …", file=sys.stderr)
    download_pdf(pdf_url, tmp)
    pdf_info = validate_downloaded_pdf(
        tmp,
        filing_type=args.filing_type,
        title=item.get("title") or args.title or "",
        report_date=str(item.get("report_date") or args.report_date or ""),
    )
    sha = sha12_of_file(tmp)
    d = entry_dir(sha)
    d.mkdir(parents=True, exist_ok=True)
    shutil.move(str(tmp), d / "report.pdf")
    source = {"symbol": args.symbol or None, "title": item.get("title"),
              "report_date": item.get("report_date"), "notice_date": item.get("notice_date"),
              "pdf_url": pdf_url, "fetched_at": now_iso()}
    write_json(d / "fetch_meta.json", {"source": source, "pdf_info": pdf_info})
    index_upsert(sha, symbol=source["symbol"], title=source["title"],
                 report_date=source["report_date"], source=source,
                 converted=(d / "report.md").is_file(), scanned=(d / "meta.json").is_file())
    print(json.dumps({"cache_id": sha, "dir": str(d), "source": source}, ensure_ascii=False))
    if args.convert:
        cmd_convert(_fetch_convert_argv(args, sha))


def _fetch_convert_argv(args, sha: str) -> list[str]:
    # 关掉的开关不能传空串占位——argparse 会把 "" 当未知位置参数报错
    argv = [sha, "--threads", str(args.threads), "--device", args.device]
    for flag in ("accurate", "ocr", "force"):
        if getattr(args, flag, False):
            argv.append(f"--{flag}")
    return argv


# --------------------------------------------------------------------------
# ⑤ cache 管理
# --------------------------------------------------------------------------

def cmd_cache(argv: list[str]) -> None:
    if not argv:
        raise SystemExit("用法: cache list | info <sha12> | clean <--id sha12|--all>")
    sub = argv[0]
    root = cache_root()
    if sub == "list":
        idx = index_load()
        if not idx["entries"]:
            print("（缓存为空）")
            return
        for sha, ent in sorted(idx["entries"].items(), key=lambda kv: str(kv[1].get("added_at") or ""), reverse=True):
            print(f"{sha}  symbol={ent.get('symbol') or '-':8} 报告期={ent.get('report_date') or '-':12} "
                  f"converted={'Y' if ent.get('converted') else 'N'} scanned={'Y' if ent.get('scanned') else 'N'} "
                  f"{ent.get('title') or ''}")
    elif sub == "info":
        if len(argv) < 2:
            raise SystemExit("cache info <sha12>")
        sha = argv[1]
        d = entry_dir(sha)
        if not d.is_dir():
            raise SystemExit(f"无缓存 {sha}")
        idx = index_load()["entries"].get(sha, {})
        conv = read_json(d / "convert_meta.json", {}) or {}
        out = {
            "cache_id": sha, "dir": str(d), "files": sorted(p.name for p in d.iterdir()),
            "index": idx, "convert_seconds": conv.get("seconds"),
            "pages": conv.get("pdf", {}).get("pages"),
        }
        meta = read_json(d / "meta.json")
        if meta:
            out["summary"] = meta_summary_text(meta)
        # materialize/qa 之后：快速列出最新 result 与质量状态（从 index 优先，从文件系统兜底）
        latest_dirs = sorted([p for p in d.glob("result-*") if p.is_dir()], key=lambda p: p.name)
        latest_dir = latest_dirs[-1] if latest_dirs else None
        if idx.get("latest_result"):
            out["latest_result"] = idx.get("latest_result")
        elif latest_dir is not None:
            out["latest_result"] = latest_dir.name
        if idx.get("quality_status"):
            out["quality_status"] = idx.get("quality_status")
        elif latest_dir is not None and (latest_dir / "quality.json").is_file():
            q = read_json(latest_dir / "quality.json", {}) or {}
            if q:
                out["quality_status"] = q.get("status")
        if latest_dir is not None:
            man = read_json(latest_dir / "manifest.json", {}) or {}
            catalog = man.get("catalog") or {}
            tables = catalog.get("tables") or []
            fields = catalog.get("fields") or []
            out["catalog_summary"] = {"tables": len(tables), "fields": len(fields)}
            # typed pass 的表数量：质量门 verdict=pass
            q = read_json(latest_dir / "quality.json", {}) if (latest_dir / "quality.json").is_file() else {}
            if q and isinstance(q.get("tables"), list):
                pass_ids = {t.get("id") for t in q.get("tables") or [] if (t.get("verdict") or "") == "pass"}
                out["typed_pass_tables"] = len([t for t in tables if t.get("id") in pass_ids])
            out["available_operations"] = ["resolve", "extract-needs", "materialize-tables"]
        print(json.dumps(out, ensure_ascii=False, indent=1))
    elif sub == "clean":
        ap = argparse.ArgumentParser(prog="wm_report.py cache clean")
        ap.add_argument("--id", default="")
        ap.add_argument("--all", action="store_true")
        cargs = ap.parse_args(argv[1:])
        if cargs.all:
            n = 0
            for sub_d in root.iterdir():
                if sub_d.is_dir() and not sub_d.name.startswith("."):
                    shutil.rmtree(sub_d)
                    n += 1
            index_save({"entries": {}})
            print(f"已清理 {n} 个缓存条目")
        elif cargs.id:
            d = entry_dir(cargs.id)
            if d.is_dir():
                shutil.rmtree(d)
                idx = index_load()
                idx["entries"].pop(cargs.id, None)
                index_save(idx)
                print(f"已清理 {cargs.id}")
            else:
                print(f"无缓存 {cargs.id}")
        else:
            raise SystemExit("cache clean 需要 --id <sha12> 或 --all")
    else:
        raise SystemExit(f"未知子命令 {sub}")


# --------------------------------------------------------------------------

# --------------------------------------------------------------- auto-heal (close) ----

def auto_promote(sha12: str, *, result_name: str | None = None,
                 preferred: list[str] | None = None, min_cooccurrence: int = 2) -> dict:
    """规则化 auto-promote：行业 allowlist ∪ 跨业态邻接白名单（hint 共现≥N）内，
    每 hint 取首个候选晋升；不设总数上限（原 _live_pipeline 上限 6 会截断跨业态表——
    神华 5 处 power_generation hint 未晋升实证）。"""
    from domain.policy import CROSS_INDUSTRY_TABLE_ALLOWLIST

    result_dir = _result_dir(sha12, result_name)
    cand = read_json(result_dir / "promote_candidates.json", {}) or {}
    meta = read_json(entry_dir(sha12) / "meta.json", {}) or {}
    industry = (meta.get("industry_hint") or {}).get("industry")
    allow = set(preferred or [])
    if industry and industry in INDUSTRY_EXT_GROUPS:
        allow |= set(INDUSTRY_EXT_GROUPS[industry].get("tables") or [])
    if not allow:
        allow = {"production_sales", "segments", "key_financials"}
    freq: dict[str, int] = {}
    for c in cand.get("candidates") or []:
        h = str(c.get("type_hint") or "")
        if h:
            freq[h] = freq.get(h, 0) + 1
    cross_applied: dict[str, int] = {}
    for _adj, hints in (CROSS_INDUSTRY_TABLE_ALLOWLIST.get(industry or "") or {}).items():
        for h in hints:
            if freq.get(h, 0) >= min_cooccurrence:
                allow.add(h)
                cross_applied[h] = freq[h]

    def sort_key(c: dict) -> tuple:
        hint = str(c.get("type_hint") or "")
        try:
            pri = (preferred or []).index(hint)
        except ValueError:
            pri = 999
        return (pri, hint)

    promotions: list[dict] = []
    seen: set[str] = set()
    for c in sorted(cand.get("candidates") or [], key=sort_key):
        hint = c.get("type_hint")
        if not hint or hint in seen or hint not in allow:
            continue
        table_file = c.get("table_file") or c.get("file")
        if not table_file:
            continue
        reason = f"auto-promote type_hint={hint}"
        if hint in cross_applied:
            reason += f"（跨业态邻接，共现 {cross_applied[hint]} 次）"
        promotions.append({
            "table_file": table_file,
            "promote_to": hint,
            "confidence": "high",
            "reason": reason,
        })
        seen.add(hint)
    if not promotions:
        return {"applied": 0, "promotions": [], "cross_industry": cross_applied}
    out = apply_promotions(sha12, promotions, result_name=result_dir.name)
    out["promotions"] = promotions
    out["cross_industry"] = cross_applied
    return out


def _section_ranges(meta: dict, md_lines: list[str], spec: dict) -> list[tuple[int, int, str]]:
    """按 spec 定位章节行区间：先 meta.sections 的 anchor key，退而求其次标题正则。"""
    secs = meta.get("sections") or []
    out: list[tuple[int, int, str]] = []
    for key in spec.get("section_keys") or []:
        for i, s in enumerate(secs):
            if s.get("key") == key:
                start = int(s.get("line") or 0)
                # sections 列表按发现序非行序（神华 mda_outlook 实证）——
                # 取行号大于本节的最近节为边界
                later = [int(s2.get("line")) for s2 in secs
                         if s2.get("line") is not None and int(s2["line"]) > start]
                end = min(later) if later else start + 400
                out.append((start, min(end, start + 900), f"section:{key}"))
                break
    if not out:
        pats = [re.compile(p) for p in spec.get("section_patterns") or []]
        for i, ln in enumerate(md_lines):
            t = ln.strip()
            if not t or t.startswith("|") or len(t) > 80:
                continue
            if any(p.search(t) for p in pats):
                out.append((i, min(i + 400, len(md_lines)), f"pattern:{t[:24]}"))
                break
    return out


def narrative_scan(sha12: str, *, result_name: str | None = None) -> dict:
    """叙述层证据扫描（auto-heal 第 3 步）：
    - 叙述 needle 命中 → 自动 found（quote+page，review 硬门回验）；
    - 未命中 → agent_tasks 证据包（章节区间/页码/excerpt/needles），**不自动 not_disclosed**；
    - required_gaps 一律生成带候选证据的 agent_tasks（口径判断须 Agent 终审）。"""
    from domain.narratives import (INDUSTRY_GAP_NEEDLES, INDUSTRY_NARRATIVE_SPECS,
                                   NARRATIVE_SPECS)

    result_dir = _result_dir(sha12, result_name)
    meta = read_json(entry_dir(sha12) / "meta.json", {}) or {}
    industry = (meta.get("industry_hint") or {}).get("industry")
    md_lines = (entry_dir(sha12) / "report.md").read_text(encoding="utf-8").splitlines()
    manifest = _load_manifest(result_dir)
    gaps = read_json(result_dir / "gaps.json", []) or []
    nar_catalog = (manifest.get("catalog") or {}).get("narratives") or []
    tasks_dir = result_dir / "agent_tasks"
    tasks_dir.mkdir(exist_ok=True)
    (result_dir / "narratives").mkdir(exist_ok=True)

    def _sq(s: str) -> str:
        return re.sub(r"\s+", "", nfkc(s or ""))

    def find_needle_lines(ranges: list[tuple[int, int, str]], needles: list[str]) -> list[tuple[int, str, str]]:
        prose, headings, table_rows = [], [], []
        for lo, hi, _src in ranges:
            for i in range(lo, min(hi, len(md_lines))):
                ln = md_lines[i].rstrip()
                if not ln.strip():
                    continue
                n = _sq(ln)
                for nd in needles:
                    if nd and nd in n:
                        s = ln.lstrip()
                        if s.startswith("|"):
                            table_rows.append((i, ln.strip(), nd))
                        elif s.startswith("#"):
                            headings.append((i, ln.strip(), nd))
                        else:
                            prose.append((i, ln.strip(), nd))
                        break
        # 内容行 > 章节标题行（标题命中只证明章节存在，不证明披露内容） > 表格行
        return prose + headings + table_rows

    specs: dict[str, dict] = {nid: dict(sp) for nid, sp in NARRATIVE_SPECS.items()}
    for nid, sp in (INDUSTRY_NARRATIVE_SPECS.get(industry or "") or {}).items():
        specs[nid] = dict(sp)

    found: list[dict] = []
    pending: list[str] = []
    for entry in nar_catalog:
        nid = entry.get("id")
        if not nid or entry.get("status") in ("found", "not_applicable"):
            continue
        sp = specs.get(nid) or {"needles": [], "section_keys": [nid], "section_patterns": [nid]}
        # 行业叙述优先扫 MD&A 章节（commodity_price 命中董事会报告开头弱证据实证）
        if not sp.get("section_keys") and not sp.get("section_patterns"):
            sp = {**sp, "section_keys": ["mda_overview", "mda_industry"]}
        ranges = _section_ranges(meta, md_lines, sp) or [(0, len(md_lines), "whole_doc")]
        hits = find_needle_lines(ranges, sp.get("needles") or [])
        hit = next((h for h in hits if len(_sq(h[1])) >= 12), None)
        if hit:
            i, ln, nd = hit
            page_n = page_of_line(md_lines, i)
            write_json(result_dir / "narratives" / f"{nid}.json", {
                "narrative_id": nid, "group": entry.get("group"),
                "anchor": entry.get("anchor") or nid,
                "quote": ln, "page": page_n,
                "notes": f"narrative-scan 自动命中 needle「{nd}」",
                "needles": sp.get("needles") or [], "status": "found", "bullets": [],
            })
            entry["status"] = "found"
            for g in gaps:
                if g.get("id") == nid:
                    g.update({"status": "found", "quote": ln, "page": page_n,
                              "evidence": f"narrative-scan needle「{nd}」quote+page"})
            found.append({"id": nid, "page": page_n, "needle": nd})
        else:
            lo, hi, src = ranges[0]
            write_json(tasks_dir / f"narrative-{nid}.json", {
                "task": "narrative_close", "id": nid, "group": entry.get("group"),
                "status": "pending",
                "section": [{"source": src, "start_line": lo, "end_line": hi,
                             "pages": [page_of_line(md_lines, lo), page_of_line(md_lines, hi - 1)]}],
                "needles": sp.get("needles") or [],
                "excerpt": [md_lines[i].strip() for i in range(lo, min(lo + 60, hi))
                            if md_lines[i].strip()][:14],
                "instructions": (
                    "读 section 页区间原文判断披露状态：found→quote+page；not_disclosed→reason"
                    "（引用披露范围证据）；not_found。结果写 agent_tasks_done/narrative-{id}.json，"
                    "由 agent-apply 校验落地（found 的 quote 须逐字在 report.md 且页码一致）。"),
            })
            pending.append(nid)

    gap_needles = INDUSTRY_GAP_NEEDLES.get(industry or "") or {}
    nar_ids = {e.get("id") for e in nar_catalog}
    for g in gaps:
        gid = g.get("id")
        if not gid or gid in ("variance_reason",) or gid in nar_ids \
                or str(gid).startswith(("qa::", "narrative_kpi::")) \
                or g.get("status") in ("found", "not_disclosed", "not_applicable", "not_found"):
            continue
        needles = gap_needles.get(gid) or []
        hits = find_needle_lines([(0, len(md_lines), "whole_doc")], needles) if needles else []
        ev_hits = [{"quote": ln, "page": page_of_line(md_lines, i), "needle": nd}
                   for i, ln, nd in hits[:5]]
        write_json(tasks_dir / f"gap-{gid}.json", {
            "task": "narrative_close", "id": gid, "group": g.get("group"),
            "status": "pending", "reason_required": g.get("reason"),
            "needles": needles, "evidence_hits": ev_hits,
            "instructions": (
                "候选证据仅供参考：口径/数值判断须 Agent 定论（如 权益 vs 并表产量、"
                "洗选率是否披露数值）。found→quote+page；not_disclosed→reason 引范围证据；"
                "not_found。写 agent_tasks_done/gap-{id}.json。"),
        })
        pending.append(gid)

    write_json(result_dir / "gaps.json", gaps)
    write_json(result_dir / "manifest.json", manifest)
    # 清理已终态 id 的陈旧任务包（上一轮 pending、本轮已闭环）
    terminal_ids = {e.get("id") for e in nar_catalog
                    if e.get("status") in ("found", "not_applicable")} | {
        g.get("id") for g in gaps
        if g.get("status") in ("found", "not_disclosed", "not_applicable", "not_found")}
    for fp in tasks_dir.glob("*.json"):
        tid = fp.stem.replace("narrative-", "", 1).replace("gap-", "", 1)
        if tid in terminal_ids:
            fp.unlink()
    return {"found": found, "pending": pending,
            "tasks_dir": str(tasks_dir)}


def agent_apply(sha12: str, *, result_name: str | None = None,
                tasks_dirname: str = "agent_tasks_done") -> dict:
    """校验并落地 Agent 判断（auto-heal 第 4 步）。校验不过即拒——不放宽任何门：
    - found：quote 逐字（NFKC 去空白）在 report.md 且页码一致；
    - not_disclosed：reason ≥8 字符；
    - qa_adjudication：adjudication ∈ rule_limitation|real，标注进 quality.json（不删 finding）。"""
    result_dir = _result_dir(sha12, result_name)
    done_dir = result_dir / tasks_dirname
    md_lines = (entry_dir(sha12) / "report.md").read_text(encoding="utf-8").splitlines()
    manifest = _load_manifest(result_dir)
    gaps = read_json(result_dir / "gaps.json", []) or []
    quality = read_json(result_dir / "quality.json", {}) or {}

    def _sq(s: str) -> str:
        return re.sub(r"\s+", "", nfkc(s or ""))

    md_sq = [_sq(ln) for ln in md_lines]
    applied, rejected = [], []

    def _set_gap(gid: str, status: str, quote: str | None, page: int | None,
                 reason: str, evidence: str) -> None:
        for g in gaps:
            if g.get("id") == gid:
                g["status"] = status
                if quote and page is not None:
                    g["quote"], g["page"] = quote, page
                else:
                    g.pop("quote", None), g.pop("page", None)
                g["reason"] = reason
                g["evidence"] = evidence
                return
        gaps.append({"id": gid, "group": "Z_agent", "status": status, "reason": reason,
                     "evidence": evidence})

    for fp in sorted(done_dir.glob("*.json")):
        t = read_json(fp, {}) or {}
        task, tid = t.get("task"), t.get("id")
        if not tid:
            rejected.append({"file": fp.name, "reject": "no_id"})
            continue
        if task in ("narrative_close", "gap_close"):
            status = t.get("status")
            if status not in ("found", "not_disclosed", "not_found"):
                rejected.append({"id": tid, "reject": "bad_status"})
                continue
            quote = (t.get("quote") or "").strip()
            page = t.get("page")
            if status == "found":
                if not quote or page is None:
                    rejected.append({"id": tid, "reject": "found_requires_quote_page"})
                    continue
                qn = _sq(quote)
                hit_i = next((i for i, ln in enumerate(md_sq) if qn and qn in ln), None)
                if hit_i is None:
                    rejected.append({"id": tid, "reject": "quote_not_in_md"})
                    continue
                if page_of_line(md_lines, hit_i) != int(page):
                    rejected.append({"id": tid, "reject": "page_mismatch"})
                    continue
            elif status == "not_disclosed" and len((t.get("reason") or "").strip()) < 8:
                rejected.append({"id": tid, "reject": "not_disclosed_requires_reason"})
                continue
            nar_ids = {e.get("id") for e in (manifest.get("catalog") or {}).get("narratives") or []}
            if tid in nar_ids and status == "found":
                (result_dir / "narratives").mkdir(exist_ok=True)
                write_json(result_dir / "narratives" / f"{tid}.json", {
                    "narrative_id": tid, "quote": quote, "page": page,
                    "notes": t.get("notes") or "", "bullets": t.get("bullets") or [],
                    "status": "found", "method": "agent_close",
                })
                for e in (manifest.get("catalog") or {}).get("narratives") or []:
                    if e.get("id") == tid:
                        e["status"] = "found"
            elif tid in nar_ids:
                for e in (manifest.get("catalog") or {}).get("narratives") or []:
                    if e.get("id") == tid:
                        e["status"] = status
            _set_gap(tid, status,
                     quote if status == "found" else None,
                     page if status == "found" else None,
                     (t.get("reason") or "").strip() or f"agent_close {status}",
                     f"agent_close {status}")
            applied.append({"id": tid, "status": status})
        elif task == "qa_adjudication":
            adj = t.get("adjudication")
            if adj not in ("rule_limitation", "real"):
                rejected.append({"id": tid, "reject": "bad_adjudication"})
                continue
            n_marked = 0
            for f in quality.get("python_findings") or []:
                if (f.get("id") == (t.get("finding_id") or tid)
                        and (not t.get("reason_kind") or f.get("reason") == t.get("reason_kind"))):
                    f["adjudicated"] = adj
                    f["adjudication_reason"] = (t.get("rationale") or "").strip()
                    n_marked += 1
            if not n_marked:
                rejected.append({"id": tid, "reject": "finding_not_found"})
                continue
            applied.append({"id": tid, "adjudication": adj})
        elif task == "industry_confirm":
            ind = t.get("industry")
            if ind not in INDUSTRY_HINTS:
                rejected.append({"id": tid, "reject": "unknown_industry"})
                continue
            meta = read_json(entry_dir(sha12) / "meta.json", {}) or {}
            ih = meta.setdefault("industry_hint", {})
            ih["industry"] = ind
            ih["confirmed_by"] = "agent"
            ih["confidence"] = max(float(ih.get("confidence") or 0.0), 0.5)
            write_json(entry_dir(sha12) / "meta.json", meta)
            applied.append({"id": tid, "industry": ind})
        else:
            rejected.append({"id": tid, "reject": "unknown_task"})

    write_json(result_dir / "gaps.json", gaps)
    write_json(result_dir / "manifest.json", manifest)
    if quality:
        write_json(result_dir / "quality.json", quality)
    # 已落地任务从待办目录移除（重跑 close 不再列出）
    for a in applied:
        aid = str(a.get("id") or "")
        for prefix in ("narrative-", "gap-"):
            p = result_dir / "agent_tasks" / f"{prefix}{aid}.json"
            if p.is_file():
                p.unlink()
    return {"applied": applied, "rejected": rejected}


def close_extract(sha12: str, *, result_name: str | None = None,
                  apply_tasks: bool = True) -> dict:
    """auto-heal 编排：auto-promote → narrative-scan → agent-apply（若有 done 任务）
    → qa-tables → review-extract；输出最小待办清单。禁止：静默改数字、无 quote 的 found、
    跳过 quality.json。"""
    promo = auto_promote(sha12, result_name=result_name)
    nar = narrative_scan(sha12, result_name=result_name)
    appl: dict = {"applied": [], "rejected": []}
    result_dir = _result_dir(sha12, result_name)
    if apply_tasks and (result_dir / "agent_tasks_done").is_dir() \
            and list((result_dir / "agent_tasks_done").glob("*.json")):
        appl = agent_apply(sha12, result_name=result_dir.name)
    qa = apply_qa(sha12, [], result_name=result_dir.name)
    rev = review_extract(sha12, result_name=result_dir.name)
    todo = [str(p.name) for p in sorted((result_dir / "agent_tasks").glob("*.json"))]
    return {
        "cache_id": sha12, "result_dir": result_dir.name,
        "promoted": [p.get("promote_to") for p in promo.get("promotions") or []],
        "cross_industry": promo.get("cross_industry") or {},
        "narratives_found": [f.get("id") for f in nar.get("found") or []],
        "agent_applied": [a.get("id") for a in appl.get("applied") or []],
        "agent_rejected": appl.get("rejected") or [],
        "quality_status": qa.get("status"),
        "review_status": rev.get("status"),
        "review_hard_failures": rev.get("hard_failures"),
        "todo_tasks": todo,
    }


def cmd_auto_promote(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py auto-promote",
        description="规则化晋升：行业 allowlist + 跨业态邻接（hint 共现≥2）内每 hint 取首候选",
    )
    ap.add_argument("sha12")
    ap.add_argument("--result", default="")
    ap.add_argument("--core-table", action="append", default=[],
                    help="优先晋升的 type_hint（可多次）")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    out = auto_promote(args.sha12, result_name=args.result or None,
                       preferred=args.core_table or None)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_narrative_scan(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py narrative-scan",
        description="叙述层证据扫描：needle 命中自动 found；未命中生成 agent_tasks 证据包",
    )
    ap.add_argument("sha12")
    ap.add_argument("--result", default="")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    out = narrative_scan(args.sha12, result_name=args.result or None)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def cmd_agent_apply(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py agent-apply",
        description="校验并落地 Agent 判断（agent_tasks_done/*.json）；校验不过即拒",
    )
    ap.add_argument("sha12")
    ap.add_argument("--result", default="")
    ap.add_argument("--tasks-dir", default="agent_tasks_done")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    out = agent_apply(args.sha12, result_name=args.result or None,
                      tasks_dirname=args.tasks_dir)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    if out.get("rejected"):
        raise SystemExit(1)


def cmd_close(argv: list[str]) -> None:
    ap = argparse.ArgumentParser(
        prog="wm_report.py close",
        description="auto-heal 编排：auto-promote → narrative-scan → agent-apply → qa → review",
    )
    ap.add_argument("sha12")
    ap.add_argument("--result", default="")
    ap.add_argument("--no-apply", action="store_true", help="跳过 agent_tasks_done 应用")
    args = ap.parse_args(argv)
    warn_stale_cache(args.sha12)
    out = close_extract(args.sha12, result_name=args.result or None,
                        apply_tasks=not args.no_apply)
    print(json.dumps(out, ensure_ascii=False, indent=1))


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(__doc__)
        return
    sub, rest = argv[0], argv[1:]
    if sub == "fetch":
        cmd_fetch(rest)
    elif sub == "convert":
        cmd_convert(rest)
    elif sub == "scan":
        cmd_scan(rest)
    elif sub == "extract-tables":
        cmd_extract_tables(rest)
    elif sub == "locate":
        cmd_locate(rest)
    elif sub == "extract-query":
        cmd_extract_query(rest)
    elif sub == "resolve":
        cmd_resolve(rest)
    elif sub == "extract-needs":
        cmd_extract_needs(rest)
    elif sub == "capabilities":
        cmd_capabilities(rest)
    elif sub == "materialize-tables":
        cmd_materialize_tables(rest)
    elif sub == "adapt-plan":
        cmd_adapt_plan(rest)
    elif sub == "apply-promotions":
        cmd_apply_promotions(rest)
    elif sub == "auto-promote":
        cmd_auto_promote(rest)
    elif sub == "narrative-scan":
        cmd_narrative_scan(rest)
    elif sub == "agent-apply":
        cmd_agent_apply(rest)
    elif sub == "close":
        cmd_close(rest)
    elif sub == "qa-tables":
        cmd_qa_tables(rest)
    elif sub == "review-extract":
        cmd_review_extract(rest)
    elif sub == "render-html":
        cmd_render_html(rest)
    elif sub == "cache":
        cmd_cache(rest)
    else:
        print(__doc__)
        raise SystemExit(f"未知子命令: {sub}")


if __name__ == "__main__":
    main()
