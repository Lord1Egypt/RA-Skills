"""
PSD 批量导出 v3.0 — Excel + PSD → 批量 PNG
=============================================
v3.0: 智能分析报告 | 容量预警 | 字体智能匹配 | 导出验证 | --analyze 模式
v2.3: 背景预渲染缓存(性能提升) | 跨平台字体 | 文本容量+样式预览 | --dry-run

用法:
  python batch_from_excel.py 名单.xlsx 模板.psd output/
  python batch_from_excel.py 名单.xlsx 模板.psd output/ --dry-run
  python batch_from_excel.py 名单.xlsx 模板.psd output/ --analyze
  python batch_from_excel.py 名单.xlsx 模板.psd output/ --cols 姓名,学校,赛区
"""
import sys, argparse, time
import copy
from pathlib import Path
import random
import json
import pandas as pd
from psd_tools import PSDImage
from PIL import Image, ImageChops
import re
import difflib
import os

from console_utils import configure_stdio

configure_stdio()

try:
    import pytesseract
except Exception:
    pytesseract = None

sys.path.insert(0, str(Path(__file__).parent))
from psd_text_editor import patch_psd_text
from render_psd_batch import (prerender_background, render_with_background,
                               get_text_style, match_psd_font,
                               show_psd_styles, find_fonts, render_psd_to_png)


SYNONYMS = {
    '名字': ['姓名','名称','name','名字'],
    '姓名': ['名字','名称','name'],
    '赛区': ['赛区','division','赛','赛区名称'],
    '学校': ['学校','school','university','大学','学院','院校'],
    '编号': ['编号','号码','number','id','序号','no'],
    'title': ['标题','title','名称','名字','name'],
}

CONF_ICON = {'high':'✓','medium':'~','low':'?','none':'✗'}


def _detect_psd_dpi(psd_path):
    """尝试从 PSD 文件头读取分辨率（16.16 定点），未找到则返回 None。"""
    try:
        b = open(str(psd_path), 'rb').read(64)
        if len(b) < 22:
            return None
        def fixed_to_float(bs):
            if len(bs) < 4:
                return 0.0
            v = int.from_bytes(bs, 'big')
            return float((v >> 16) + (v & 0xFFFF) / 65536.0)
        h = fixed_to_float(b[14:18])
        v = fixed_to_float(b[18:22])
        if h <= 0 and v <= 0:
            return None
        val = h if h > 0 else v
        return int(round(val))
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════
# v3.0: 智能分析报告
# ═══════════════════════════════════════════════════════════════

def generate_intelligent_report(psd_path, excel_path=None, df=None, manual_font=None):
    """
    生成完整的智能分析报告。
    包含: PSD 结构、文本图层详情、容量分析、字体推荐、列匹配预览。
    
    返回: dict 包含报告各部分数据，供后续流程使用。
    """
    psd_path = Path(psd_path)
    report = {'psd_path': str(psd_path), 'warnings': [], 'tips': []}
    
    # ── PSD 基本信息 ──
    psd = PSDImage.open(str(psd_path))
    report['size'] = f"{psd.width}×{psd.height} px"
    dpi_val = _detect_psd_dpi(psd_path)
    report['dpi'] = f"{dpi_val}" if dpi_val else '未嵌入'
    
    # ── 文本图层分析 ──
    text_layers = []
    all_styles = []
    for layer in psd.descendants():
        if layer.kind != 'type':
            continue
        text = layer.text.strip('\x00').strip()
        if not text:
            continue
        style = get_text_style(layer)
        all_styles.append(style)
        
        layer_info = {
            'name': layer.name,
            'text': text,
            'text_len': len(text),
            'bbox': layer.bbox,
            'font_size': style['font_size'] if style else None,
            'font_family': style['font_family'] if style else None,
            'fill_color': style['fill_color'] if style else None,
        }
        text_layers.append(layer_info)
    
    report['text_layers'] = text_layers
    report['layer_count'] = len(text_layers)
    
    if not text_layers:
        report['warnings'].append('未检测到文本图层！请确认 PSD 文件包含可编辑的文字图层。')
        return report
    
    # ── 列匹配（若有 Excel 数据，先匹配列以便后续容量分析使用） ──
    mapping = None
    if df is not None:
        layers_for_match = [(l['name'], l['text']) for l in text_layers]
        mapping = match_columns(layers_for_match, df.columns)
        report['column_mapping'] = [
            {'layer': ln, 'original': lt, 'excel_col': cn, 'confidence': conf}
            for ln, lt, cn, conf in mapping
        ]

    # ── 容量分析（结合 Excel 最大长度判断风险） ──
    capacity_data = _analyze_capacity_data(psd_path, text_layers, df=df, mapping=mapping)
    report['capacity'] = capacity_data

    for cap in capacity_data:
        if cap.get('risk'):
            report['warnings'].append(
                f"图层「{cap['name']}」的 Excel 数据最大长度 {cap.get('data_max_len')} 超过容量 {cap.get('capacity')}，可能被截断。"
            )
        elif cap['capacity'] > 0 and cap['capacity'] < 20:
            report['warnings'].append(
                f"图层「{cap['name']}」容量仅 {cap['capacity']} 字符（原文 {cap['text_len']} 字符），长文本可能被截断。"
            )
    
    # ── 字体推荐 ──
    available_fonts = [manual_font] if manual_font else find_fonts()[:10]
    report['available_fonts'] = [Path(f).name for f in available_fonts if f]
    
    font_recommendations = []
    for layer in text_layers:
        if layer['font_family']:
            matched, conf = match_psd_font(layer['font_family'], available_fonts)
            font_recommendations.append({
                'layer': layer['name'],
                'psd_font': layer['font_family'],
                'matched_font': Path(matched).name if matched else None,
                'confidence': conf or 'not found',
                'fallback': '系统默认中文字体' if not matched else None,
            })
    report['font_recommendations'] = font_recommendations
    
    # 检查是否有未匹配字体
    unmatched = [f for f in font_recommendations if f['confidence'] == 'not found']
    if unmatched:
        names = ', '.join(f"「{u['layer']}」({u['psd_font']})" for u in unmatched)
        report['tips'].append(f"以下字体未在系统中找到: {names}。将使用最接近的匹配字体或系统默认字体。")
    
    # ── 列匹配预览 ──
    if df is not None:
        layers_for_match = [(l['name'], l['text']) for l in text_layers]
        mapping = match_columns(layers_for_match, df.columns)
        report['column_mapping'] = [
            {'layer': ln, 'original': lt, 'excel_col': cn, 'confidence': conf}
            for ln, lt, cn, conf in mapping
        ]
        unmatched_cols = [m for m in report['column_mapping'] if m['confidence'] == 'none']
        if unmatched_cols:
            names = ', '.join(f"「{m['layer']}」" for m in unmatched_cols)
            report['warnings'].append(f"以下图层未匹配到 Excel 列: {names}")
    
    # ── 数据量预估 ──
    if df is not None:
        report['data_rows'] = len(df)
        report['data_cols'] = len(df.columns)
        if len(df) > 100:
            report['tips'].append(f"数据量较大（{len(df)} 行），建议使用背景预渲染优化（自动启用）。")
    
    return report


def print_intelligent_report(report):
    """格式化打印智能分析报告"""
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        📋 PSD 智能分析报告 v3.0                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"  文件: {Path(report['psd_path']).name}")
    print(f"  尺寸: {report['size']}  |  DPI: {report['dpi']}")
    print(f"  文本图层: {report['layer_count']} 个")
    
    # 图层详情
    if report.get('text_layers'):
        print(f"\n  ── 文本图层详情 ──")
        print(f"  {'图层':<16} {'原文':<20} {'字号':>6} {'颜色':>16} {'字体'}")
        print(f"  {'─'*16} {'─'*20} {'─'*6} {'─'*16} {'─'*20}")
        for l in report['text_layers']:
            color_str = f"#{l['fill_color'][0]:02X}{l['fill_color'][1]:02X}{l['fill_color'][2]:02X}" if l['fill_color'] else 'auto'
            font_str = (l['font_family'] or '?')[:20]
            print(f"  {l['name']:<16} {l['text']:<20} {l['font_size'] or '?':>6} {color_str:>16} {font_str}")
    
    # 容量分析
    if report.get('capacity'):
        print(f"\n  ── 容量分析 ──")
        for c in report['capacity']:
            used = c['text_len']; cap = c['capacity']
            data_max = c.get('data_max_len')
            bar_len = 20
            if cap > 0:
                used_for_bar = data_max if (data_max is not None) else used
                filled = min(int(used_for_bar / max(cap, 1) * bar_len), bar_len)
                bar = '█' * filled + '░' * (bar_len - filled)
                risk = ' ⚠ 数据超出容量!' if (data_max is not None and data_max > cap) else ''
                note = f" (模板{used} / 数据最大{data_max} / 容量{cap})"
            else:
                bar = '█' * bar_len
                risk = ''
                note = f" (模板{used})"
            print(f"  {c['name']:<16} [{bar}]{note}{risk}")
    
    # 字体推荐
    if report.get('font_recommendations'):
        print(f"\n  ── 字体匹配 ──")
        for f in report['font_recommendations']:
            icon = {'exact':'✓','family':'~','similar':'?','not found':'✗'}.get(f['confidence'], '?')
            matched = f['matched_font'] or f['fallback'] or '未找到'
            print(f"  [{icon}] {f['layer']:<16} {f['psd_font'][:20]:<22} → {matched}")
    
    # 列匹配
    if report.get('column_mapping'):
        print(f"\n  ── Excel 列匹配 ──")
        for m in report['column_mapping']:
            icon = CONF_ICON.get(m['confidence'], '?')
            target = m['excel_col'] if m['excel_col'] else '(未匹配)'
            print(f"  [{icon}] {m['layer']:<16} ← {target}")
    
    # 数据概览
    if report.get('data_rows'):
        print(f"\n  ── 数据概览 ──")
        print(f"  Excel 行数: {report['data_rows']}  |  列数: {report['data_cols']}")
    
    # 警告
    if report.get('warnings'):
        print(f"\n  ╔══ ⚠ 警告 ({len(report['warnings'])}项) ══╗")
        for w in report['warnings']:
            print(f"  ║  • {w}")
        print(f"  ╚{'═'*40}╝")
    
    # 提示
    if report.get('tips'):
        print(f"\n  💡 建议:")
        for t in report['tips']:
            print(f"     • {t}")
    
    print(f"\n{'═'*62}\n")


def _analyze_capacity_data(psd_path, text_layers, df=None, mapping=None):
    """分析每个文本图层的字符容量，结合 Excel 数据返回结构化数据
    返回项包含: name, text_len, capacity, remaining, data_max_len, risk
    """
    data = open(str(psd_path), 'rb').read()
    marker = b'Txt TEXT'
    results = []

    # mapping: list of tuples (layer_name, original_text, excel_col, confidence)
    layer_to_col = {}
    if mapping:
        try:
            layer_to_col = {ln: cn for ln, _, cn, _ in mapping if cn}
        except Exception:
            layer_to_col = {}

    for layer_info in text_layers:
        text = layer_info['text']
        capacity = 0
        pos = data.find(marker)
        while pos >= 0:
            cnt = int.from_bytes(data[pos+8:pos+12], 'big')
            txt_bytes = data[pos+12:pos+12+cnt*2]
            if text.encode('utf-16-be') in txt_bytes:
                capacity = cnt - 1  # 减1去掉尾部null
                break
            pos = data.find(marker, pos+1)

        # 计算 Excel 列中的最大字符串长度（若提供）
        data_max = None
        col = layer_to_col.get(layer_info['name']) if layer_to_col else None
        if df is not None and col is not None and col in df.columns:
            try:
                series = df[col].dropna().astype(str).map(len)
                data_max = int(series.max()) if not series.empty else 0
            except Exception:
                data_max = None

        risk = False
        if capacity > 0 and data_max is not None and data_max > capacity:
            risk = True

        results.append({
            'name': layer_info['name'],
            'text_len': layer_info['text_len'],
            'capacity': capacity,
            'remaining': max(capacity - layer_info['text_len'], 0) if capacity > 0 else -1,
            'data_max_len': data_max,
            'risk': risk,
        })
    return results


# ═══════════════════════════════════════════════════════════════
# 原有函数 (保留兼容)
# ═══════════════════════════════════════════════════════════════


def match_columns(layers, df_columns, manual_cols=None):
    """三级智能列匹配: 精确→语义→位置"""
    if manual_cols:
        manual = [c.strip() for c in manual_cols.split(',')]
        result = []
        for i, (ln, lt) in enumerate(layers):
            cn = manual[i] if i < len(manual) else None
            result.append((ln, lt, cn, 'high' if cn and cn in df_columns else 'none'))
        return result
    col_strs = [str(c).lower() for c in df_columns]
    results = []
    for layer_name, original_text in layers:
        ln_lower = layer_name.lower(); best = None; conf = 'none'
        # L1: 精确匹配
        for i, cs in enumerate(col_strs):
            if ln_lower == cs or cs == ln_lower: best = df_columns[i]; conf = 'high'; break
        # L2: 包含/语义匹配
        if not best:
            for i, cs in enumerate(col_strs):
                if ln_lower in cs or cs in ln_lower: best = df_columns[i]; conf = 'medium'; break
        if not best and layer_name in SYNONYMS:
            for syn in SYNONYMS[layer_name]:
                for i, cs in enumerate(col_strs):
                    if syn.lower() in cs or cs in syn.lower(): best = df_columns[i]; conf = 'medium'; break
                if best: break
        # L3: 位置匹配
        if not best:
            idx = [n for n,_ in layers].index(layer_name)
            if idx < len(df_columns): best = df_columns[idx]; conf = 'low'
        results.append((layer_name, original_text, best, conf))
    return results


# 保留旧版兼容
def analyze_capacity(psd_path):
    """旧版容量分析（控制台输出），保留向后兼容"""
    psd = PSDImage.open(str(psd_path))
    print(f'\n  {"Layer":<20} {"Original":<25} {"Max Chars":>10}')
    print(f'  {"-"*20} {"-"*25} {"-"*10}')
    data = open(psd_path, 'rb').read()
    marker = b'Txt TEXT'
    for layer in psd.descendants():
        if layer.kind != 'type': continue
        text = layer.text.strip('\x00').strip()
        capacity = 0
        pos = data.find(marker)
        while pos >= 0:
            cnt = int.from_bytes(data[pos+8:pos+12], 'big')
            txt_bytes = data[pos+12:pos+12+cnt*2]
            if text.encode('utf-16-be') in txt_bytes:
                capacity = cnt - 1; break
            pos = data.find(marker, pos+1)
        print(f'  {layer.name:<20} {text[:25]:<25} {capacity:>10}')


def verify_export(output_dir, expected_count, psd_template=None, sample_count=3, fps=None, color=None, font_size=None, align='center', dpi=300, ocr=False, ocr_lang=None, tesseract_cmd=None, tessdata_dir=None):
    """导出后验证：数量检查、空文件检查、随机抽查比对。

    - 将随机抽样的 PSD 重新渲染并与实际 PNG 做像素差异对比。
    - 结果会写入 `output_dir/verify_report`（包含 JSON/MD 报告和差异图）。
    """
    png_dir = Path(output_dir) / 'png'
    psd_dir = Path(output_dir) / 'psd'
    report_dir = Path(output_dir) / 'verify_report'
    report_dir.mkdir(parents=True, exist_ok=True)

    if not png_dir.exists():
        return {'ok': False, 'error': 'PNG 目录不存在'}

    pngs = sorted(png_dir.glob('*.png'))
    result = {
        'ok': True,
        'total': len(pngs),
        'expected': expected_count,
        'empty_files': [],
        'errors': [],
        'samples': [],
    }
    result['report_dir'] = str(report_dir)
    result['ocr_requested'] = bool(ocr)
    result['ocr_available'] = bool(pytesseract)

    if len(pngs) != expected_count:
        result['ok'] = False
        result['errors'].append(f"数量不匹配: 预期 {expected_count}, 实际 {len(pngs)}")

    for p in pngs:
        if p.stat().st_size == 0:
            result['empty_files'].append(p.name)
            result['ok'] = False

    # 随机抽查（若存在 PSD 输出并且 sample_count>0）
    if sample_count and psd_dir.exists():
        psd_files = sorted(psd_dir.glob('*.psd'))
        if psd_files:
            sample_list = psd_files if sample_count >= len(psd_files) else random.sample(psd_files, sample_count)
            renders_dir = report_dir / 'renders'
            diffs_dir = report_dir / 'diffs'
            renders_dir.mkdir(parents=True, exist_ok=True)
            diffs_dir.mkdir(parents=True, exist_ok=True)

            for psd_path in sample_list:
                name = psd_path.stem
                actual_png = png_dir / f"{name}.png"
                sample_rec = {'name': name, 'psd': str(psd_path), 'actual_png': str(actual_png), 'rendered_png': None, 'diff_png': None, 'identical': False, 'diff_pixels': None, 'error': None}

                if not actual_png.exists():
                    sample_rec['error'] = 'missing_actual_png'
                    result['samples'].append(sample_rec)
                    result['ok'] = False
                    continue

                # 重新渲染 PSD 到临时文件
                rendered = renders_dir / f"{name}.png"
                try:
                    render_psd_to_png(psd_path, rendered, dpi=(dpi, dpi))
                    sample_rec['rendered_png'] = str(rendered)
                except Exception as e:
                    sample_rec['error'] = f'render_error: {e}'
                    result['samples'].append(sample_rec)
                    result['ok'] = False
                    continue

                try:
                    a = Image.open(actual_png).convert('RGBA')
                    b = Image.open(rendered).convert('RGBA')
                    if a.size != b.size:
                        b = b.resize(a.size)
                    diff = ImageChops.difference(a, b)
                    bbox = diff.getbbox()
                    diff_pixels = 0
                    if bbox:
                        gray = diff.convert('L')
                        hist = gray.histogram()
                        total_px = gray.size[0] * gray.size[1]
                        diff_pixels = total_px - hist[0]

                    diff_path = diffs_dir / f"{name}_diff.png"
                    diff.save(diff_path)
                    sample_rec['diff_png'] = str(diff_path)
                    sample_rec['diff_pixels'] = int(diff_pixels)
                    sample_rec['identical'] = (diff_pixels == 0)
                    # OCR 校验（可选）
                    if ocr:
                        if not pytesseract:
                            sample_rec['ocr'] = {'error': 'pytesseract not installed'}
                            result['ok'] = False
                        else:
                            # 可选设置 tesseract 路径
                            if tesseract_cmd:
                                try:
                                    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
                                except Exception:
                                    pass
                            # 可选设置 tessdata 目录
                            if tessdata_dir:
                                try:
                                    os.environ['TESSDATA_PREFIX'] = str(Path(tessdata_dir))
                                except Exception:
                                    pass
                            # 从 PSD 读取预期文本 + bbox（分图层）
                            try:
                                layer_data = []  # [(name, text, bbox), ...]
                                psd_obj = PSDImage.open(str(psd_path))
                                for layer in psd_obj.descendants():
                                    if layer.kind == 'type':
                                        t = layer.text.strip('\x00').strip()
                                        if t:
                                            layer_data.append((layer.name, t, layer.bbox))
                            except Exception as e:
                                sample_rec['ocr'] = {'error': f'read_psd_error: {e}'}
                                result['ok'] = False
                                result['samples'].append(sample_rec)
                                continue

                            try:
                                # 加载实际 PNG 图像
                                png_img = Image.open(str(actual_png)).convert('RGB')
                                img_w, img_h = png_img.size

                                ocr_kwargs = {'lang': ocr_lang or 'eng'}

                                # ── 分图层裁剪 OCR ──
                                ocr_scores = []
                                for lname, expected, bbox in layer_data:
                                    x1, y1, x2, y2 = bbox
                                    # 加 10px padding 避免裁切文字边缘
                                    pad = 10
                                    x1, y1 = x1 - pad, y1 - pad
                                    x2, y2 = x2 + pad, y2 + pad
                                    # 边界保护
                                    x1 = max(0, min(x1, img_w - 1))
                                    y1 = max(0, min(y1, img_h - 1))
                                    x2 = max(x1 + 1, min(x2, img_w))
                                    y2 = max(y1 + 1, min(y2, img_h))

                                    crop = png_img.crop((x1, y1, x2, y2))
                                    # 使用 PSM 7 (单行文本) 以获得最佳识别率
                                    ocr_text = pytesseract.image_to_string(crop, config='--psm 7', **ocr_kwargs)

                                    # 模糊打分
                                    def _normalize(s, level='full'):
                                        s = str(s).strip()
                                        if level == 'full':
                                            s = re.sub(r'[\s\W_]+', '', s).lower()
                                        elif level == 'alnum':
                                            s = re.sub(r'[^\w]', '', s, flags=re.UNICODE).lower()
                                        elif level == 'tokens':
                                            s = ' '.join(re.findall(r'\w+', s)).lower()
                                        return s

                                    def _fuzzy_score(expected, ocr_text, threshold=0.6):
                                        exp_full = _normalize(expected, 'full')
                                        ocr_full = _normalize(ocr_text, 'full')
                                        if exp_full == ocr_full:
                                            return 1.0, 'exact_full', None
                                        if exp_full and exp_full in ocr_full:
                                            return 0.95, 'substring', None
                                        exp_tokens = set(_normalize(expected, 'tokens').split())
                                        ocr_tokens = set(_normalize(ocr_text, 'tokens').split())
                                        if exp_tokens:
                                            token_overlap = len(exp_tokens & ocr_tokens) / len(exp_tokens)
                                            if token_overlap >= 0.8:
                                                return 0.85, f'tokens_{token_overlap:.2f}', {'missing': list(exp_tokens - ocr_tokens)}
                                            elif token_overlap >= 0.5:
                                                return 0.65, f'tokens_{token_overlap:.2f}', {'missing': list(exp_tokens - ocr_tokens)}
                                        ratio = difflib.SequenceMatcher(None, exp_full, ocr_full).ratio()
                                        if ratio >= threshold:
                                            return ratio, f'fuzzy_{ratio:.2f}', None
                                        exp_alnum = _normalize(expected, 'alnum')
                                        ocr_alnum = _normalize(ocr_text, 'alnum')
                                        if exp_alnum and exp_alnum in ocr_alnum:
                                            return 0.75, 'alnum_substring', None
                                        ratio2 = difflib.SequenceMatcher(None, exp_alnum, ocr_alnum).ratio()
                                        if ratio2 >= threshold:
                                            return ratio2, f'alnum_fuzzy_{ratio2:.2f}', None
                                        return 0.0, 'no_match', None

                                    score, method, detail = _fuzzy_score(expected, ocr_text, threshold=0.6)
                                    ocr_scores.append({
                                        'layer': lname,
                                        'expected': expected,
                                        'ocr_text': ocr_text.strip()[:100],
                                        'bbox': [x1, y1, x2, y2],
                                        'score': round(score, 3),
                                        'method': method,
                                        'detail': detail,
                                    })

                                avg_score = sum(s['score'] for s in ocr_scores) / max(len(ocr_scores), 1)
                                all_ok = all(s['score'] >= 0.6 for s in ocr_scores) and avg_score >= 0.7

                                sample_rec['ocr'] = {
                                    'ok': all_ok,
                                    'avg_score': round(avg_score, 3),
                                    'fields': ocr_scores,
                                }
                                if not all_ok:
                                    result['ok'] = False
                            except Exception as e:
                                sample_rec['ocr'] = {'error': f'ocr_error: {e}'}
                                result['ok'] = False

                    result['samples'].append(sample_rec)
                    if diff_pixels != 0:
                        result['ok'] = False
                except Exception as e:
                    sample_rec['error'] = f'compare_error: {e}'
                    result['samples'].append(sample_rec)
                    result['ok'] = False

    # 保存报告
    with open(report_dir / 'report.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 简要 Markdown 摘要
    with open(report_dir / 'report.md', 'w', encoding='utf-8') as f:
        f.write(f"# 导出验证报告\n\n")
        f.write(f"总 PNG: {result['total']}  预期: {result['expected']}\n\n")
        if result['errors']:
            for e in result['errors']:
                f.write(f"- ERROR: {e}\n")
        if result['empty_files']:
            f.write(f"- 空文件: {', '.join(result['empty_files'])}\n")
        if result['samples']:
            f.write('\n## 抽查样本\n')
            for s in result['samples']:
                f.write(f"- {s['name']}: identical={s.get('identical')} diff_pixels={s.get('diff_pixels')} error={s.get('error')}\n")

    return result


def print_verify_report(verify_result, elapsed_sec):
    """打印导出验证报告"""
    print(f"\n{'═'*62}")
    if verify_result['ok']:
        print(f"  ✅ 导出验证通过")
    else:
        print(f"  ⚠ 导出验证发现问题")
    
    print(f"  生成 PNG: {verify_result['total']} 个")
    print(f"  预期数量: {verify_result['expected']}")
    print(f"  耗时: {elapsed_sec:.1f} 秒")
    
    if verify_result['empty_files']:
        print(f"  ❌ 空文件 ({len(verify_result['empty_files'])}个): {', '.join(verify_result['empty_files'][:5])}")
    
    if verify_result['errors']:
        for e in verify_result['errors']:
            print(f"  ⚠ {e}")
    
    # 抽查样本详情
    if verify_result.get('samples'):
        print('\n  ── 随机抽查样本──')
        for s in verify_result['samples']:
            status = 'OK' if s.get('identical') else ('ERR' if s.get('error') else 'DIFF')
            print(f"  - {s['name']}: {status} diff_pixels={s.get('diff_pixels')} error={s.get('error')}")
        print(f"  报告目录: {verify_result.get('report_dir', '(none)')}\n")
    
    print(f"{'═'*62}\n")


def batch_export(excel_path, psd_template, output_dir, font=None, color=None,
                 font_size=None, align='center', dpi=300, cols=None, sheet=0,
                 dry_run=False, analyze_only=False, verify_samples=3, ocr=False, ocr_lang=None, tesseract_cmd=None, tessdata_dir=None):
    excel_path = Path(excel_path)
    psd_template = Path(psd_template)
    output_dir = Path(output_dir)
    effective_color = color
    
    df = pd.read_excel(excel_path, sheet_name=sheet).dropna(how='all')
    print(f'📊 Excel: {len(df)} rows × {len(df.columns)} cols  |  Sheet: {sheet}')
    
    # ── v3.0: 智能分析报告 ──
    report = generate_intelligent_report(psd_template, excel_path, df, manual_font=font)
    print_intelligent_report(report)
    
    # 仅分析模式
    if analyze_only:
        print("🔍 分析模式 — 仅生成报告，不执行导出。\n")
        return 0
    
    # 检查警告
    if report['warnings']:
        print("⚠ 上述警告可能导致导出结果不理想，请确认是否继续。\n")
    
    psd = PSDImage.open(str(psd_template))
    layers = [(l.name, l.text.strip('\x00').strip())
              for l in psd.descendants() if l.kind == 'type']
    if not layers:
        print('❌ 未检测到文本图层！'); return 0
    
    # 列匹配（复用报告中的结果）
    if report.get('column_mapping'):
        mapping = [(m['layer'], m['original'], m['excel_col'], m['confidence'])
                   for m in report['column_mapping']]
    else:
        mapping = match_columns(layers, df.columns, cols)
    
    # 旧版兼容：简要输出列匹配
    has_warn = False
    print(f'── Column Mapping ──')
    for ln, lt, cn, conf in mapping:
        status = f'-> {cn}' if cn else '(NOT FOUND)'
        print(f'  [{CONF_ICON.get(conf,"?")}] {ln:<20} {status}')
        if conf in ('low','none'): has_warn = True
    if has_warn and not cols:
        print(f'\n  💡 TIP: --cols {",".join(str(c) for c in df.columns[:len(layers)])}')
    
    # Dry-run 模式
    if dry_run:
        print(f'\n── 📸 DRY RUN ──')
        # 简要文本预览（控制台）
        for _, row in df.head(3).iterrows():
            parts = []
            for ln, lt, cn, conf in mapping:
                if cn and conf != 'none' and cn in df.columns:
                    parts.append(f'{ln}={row[cn]}')
            print(f'  {" | ".join(parts)}')

        # 生成前三张 PNG 预览
        try:
            print('\n  生成预览图片（前三条）...')
            fps = [font] if font else find_fonts()[:5]
            bg_cache = prerender_background(psd_template)
            psd_obj = PSDImage.open(str(psd_template))
            template_styles = []
            for layer in psd_obj.descendants():
                if layer.kind != 'type':
                    continue
                s = get_text_style(layer)
                if not s: continue
                s['layer_name'] = layer.name
                template_styles.append(s)

            layer_to_col = {ln: cn for ln, _, cn, conf in mapping if cn and conf != 'none'}
            preview_dir = output_dir / 'dryrun_preview'
            preview_dir.mkdir(parents=True, exist_ok=True)

            for i, (_, row) in enumerate(df.head(3).iterrows(), start=1):
                styles = copy.deepcopy(template_styles)
                for s in styles:
                    col = layer_to_col.get(s.get('layer_name'))
                    if col and col in df.columns:
                        val = row[col]
                        if pd.notna(val):
                            s['text'] = str(val).strip()
                img = render_with_background(bg_cache, styles, fps, effective_color, font_size, align)
                outp = preview_dir / f'preview_{i:03d}.png'
                img.save(str(outp), 'PNG', dpi=(dpi, dpi))

            print(f'  预览已保存到: {preview_dir.resolve()}')
        except Exception as e:
            print(f'  预览生成失败: {e}')

        print(f'  ... ({len(df)} rows total)')
        print(f'  输出目录: {output_dir.resolve()}')
        return 0
    
    # 字体准备
    fps = [font] if font else find_fonts()[:5]
    if fps and fps[0]:
        print(f'\n🔤 渲染字体: {Path(fps[0]).name}')
    
    # ── 预渲染背景（一次）──
    print(f'\n🖼 Pre-rendering template background...')
    t0 = time.time()
    bg_cache = prerender_background(psd_template)
    template_styles = [get_text_style(l) for l in PSDImage.open(str(psd_template)).descendants() if l.kind=='type']
    template_styles = [s for s in template_styles if s]
    print(f'   Background cached ({time.time()-t0:.2f}s)')
    
    # ── Step 1: 批量 PSD ──
    psd_dir = output_dir / 'psd'
    png_dir = output_dir / 'png'
    psd_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)
    
    total = len(df)
    print(f'\n=== Step 1/2: Generating {total} PSDs ===')
    psd_count = 0
    t1 = time.time()
    
    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        text_map = {}
        for (_, original), (_, _, cn, conf) in zip(layers, mapping):
            if cn and conf != 'none' and cn in df.columns:
                val = row[cn]
                if pd.notna(val): text_map[original] = str(val).strip()
        if not text_map: continue
        
        patch_psd_text(psd_template, psd_dir/f'{idx:03d}.psd', text_map)
        psd_count += 1
        if idx % max(1, total//20) == 0 or idx == total:
            pct = idx*100//total
            bar = '█'*(pct//5) + '░'*(20-pct//5)
            print(f'  [{bar}] {idx}/{total} ({pct}%)')
    
    psd_elapsed = time.time() - t1
    print(f'  ✅ {psd_count} PSDs → {psd_dir}  ({psd_elapsed:.1f}s)')
    
    # ── Step 2: 批量 PNG（使用缓存背景）──
    psd_files = sorted(psd_dir.glob('*.psd'))
    png_total = len(psd_files)
    print(f'\n=== Step 2/2: Rendering {png_total} PNGs @{dpi}DPI ===')
    t2 = time.time()
    errors = []
    
    for i, psd_path in enumerate(psd_files, 1):
        try:
            psd = PSDImage.open(str(psd_path))
            styles = [get_text_style(l) for l in psd.descendants() if l.kind=='type']
            styles = [s for s in styles if s]
            if styles:
                result = render_with_background(bg_cache, styles, fps, effective_color, font_size, align)
                png_path = png_dir / f'{psd_path.stem}.png'
                result.save(str(png_path), 'PNG', dpi=(dpi, dpi))
        except Exception as e:
            errors.append((psd_path.name, str(e)))
        
        if i % max(1, png_total//20) == 0 or i == png_total:
            pct = i*100//png_total
            bar = '█'*(pct//5) + '░'*(20-pct//5)
            print(f'  [{bar}] {i}/{png_total} ({pct}%)')
    
    png_elapsed = time.time() - t2
    total_elapsed = time.time() - t0
    
    if errors:
        print(f'\n  ⚠ {len(errors)} 个渲染错误:')
        for name, err in errors[:5]:
            print(f'    - {name}: {err}')
    
    print(f'\n  ✅ {png_total} PNGs → {png_dir}  ({png_elapsed:.1f}s)')
    
    # ── v3.0: 导出验证 ──
    verify = verify_export(output_dir, psd_count, psd_template=psd_template, sample_count=verify_samples, fps=fps, color=effective_color, font_size=font_size, align=align, dpi=dpi, ocr=ocr, ocr_lang=ocr_lang, tesseract_cmd=tesseract_cmd, tessdata_dir=tessdata_dir)
    print_verify_report(verify, total_elapsed)
    
    return psd_count


def main():
    p = argparse.ArgumentParser(
        description='PSD 批量导出 v3.0 — 智能分析 + 批量导出',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s 名单.xlsx 模板.psd output/              # 完整导出
  %(prog)s 名单.xlsx 模板.psd output/ --analyze    # 仅智能分析
  %(prog)s 名单.xlsx 模板.psd output/ --dry-run    # 预览模式
  %(prog)s 名单.xlsx 模板.psd output/ --cols 姓名,学校  # 手动列映射
        """
    )
    p.add_argument('excel', help='Excel 数据文件路径')
    p.add_argument('psd', help='PSD 模板文件路径')
    p.add_argument('output', nargs='?', default='output', help='输出目录 (默认: output)')
    p.add_argument('--font', help='指定渲染字体路径')
    p.add_argument('--color', nargs=3, type=int, metavar=('R','G','B'), help='文字颜色 RGB (默认: 保持 PSD 图层颜色)')
    p.add_argument('--size', type=int, help='字号 (默认: PSD原始字号)')
    p.add_argument('--align', choices=['left','center','right'], default='center', help='对齐方式')
    p.add_argument('--dpi', type=int, default=300, help='输出 DPI (默认: 300)')
    p.add_argument('--cols', help='手动列映射，逗号分隔，如: 姓名,学校,赛区')
    p.add_argument('--sheet', default=0, help='Excel Sheet 名称或索引 (默认: 0)')
    p.add_argument('--dry-run', action='store_true', help='预览模式，不实际导出')
    p.add_argument('--analyze', action='store_true', help='仅生成智能分析报告，不导出')
    p.add_argument('--verify-samples', type=int, default=3, help='导出后随机抽查样本数量 (默认: 3)')
    p.add_argument('--ocr', action='store_true', help='在抽查时启用 OCR 文本校验（需安装 Tesseract/pytesseract）')
    p.add_argument('--ocr-lang', default=None, help='传递给 tesseract 的语言参数，如 chi_sim 或 eng')
    p.add_argument('--tesseract-cmd', default=None, help='若 tesseract 不在 PATH，传入 tesseract 可执行路径')
    p.add_argument('--tessdata-dir', default=None, help='tessdata 目录路径（如 ~/tessdata），用于加载额外语言包')
    a = p.parse_args()
    color = tuple(a.color) if a.color else None
    batch_export(a.excel, a.psd, a.output, a.font, color, a.size, a.align, a.dpi, a.cols, a.sheet, a.dry_run, a.analyze, a.verify_samples, ocr=a.ocr, ocr_lang=a.ocr_lang, tesseract_cmd=a.tesseract_cmd, tessdata_dir=a.tessdata_dir)


if __name__ == '__main__':
    main()
