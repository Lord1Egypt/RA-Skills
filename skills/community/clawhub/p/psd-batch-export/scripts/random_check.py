#!/usr/bin/env python3
r"""random_check.py

随机抽查 PSD->PNG 导出结果（视觉比对），并生成 JSON/Markdown 报告与差异图像。

用法示例:
  C:\...\.venv\Scripts\python.exe random_check.py \
    --psd-dir output/test_review/psd \
    --png-dir output/test_review/png \
    --samples 3 \
    --report-dir output/test_review/verify_report
"""
import argparse
import json
import random
import time
from pathlib import Path

from PIL import Image, ImageChops

try:
    from render_psd_batch import render_psd_to_png
except Exception as e:
    render_psd_to_png = None
try:
    import pytesseract
except Exception:
    pytesseract = None
from psd_tools import PSDImage
import re
import difflib

from console_utils import configure_stdio

configure_stdio()


def compare_images(p1: Path, p2: Path):
    a = Image.open(p1).convert('RGBA')
    b = Image.open(p2).convert('RGBA')
    if a.size != b.size:
        # 尝试按目标尺寸调整，记录尺寸差异
        b_resized = b
        a = a.resize(b_resized.size)
        diff = ImageChops.difference(a, b_resized)
    else:
        diff = ImageChops.difference(a, b)

    bbox = diff.getbbox()
    diff_pixels = 0
    if bbox:
        gray = diff.convert('L')
        hist = gray.histogram()
        total = gray.size[0] * gray.size[1]
        diff_pixels = total - hist[0]
    return bbox, diff_pixels, diff


def run_random_check(psd_dir: Path, png_dir: Path, samples: int, report_dir: Path, seed: int | None = None, ocr: bool = False, ocr_lang: str | None = None, tesseract_cmd: str | None = None):
    psd_dir = Path(psd_dir)
    png_dir = Path(png_dir)
    report_dir = Path(report_dir)
    renders_dir = report_dir / 'renders'
    diffs_dir = report_dir / 'diffs'
    report_dir.mkdir(parents=True, exist_ok=True)
    renders_dir.mkdir(parents=True, exist_ok=True)
    diffs_dir.mkdir(parents=True, exist_ok=True)

    psd_files = sorted([p for p in psd_dir.glob('*.psd')])
    total = len(psd_files)
    if total == 0:
        raise SystemExit(f'No PSD files found in {psd_dir}')

    if seed is not None:
        random.seed(seed)

    sample_list = psd_files if samples >= total else random.sample(psd_files, samples)

    results = []
    start = time.time()
    for p in sample_list:
        name = p.stem
        actual_png = png_dir / f"{name}.png"
        item = {
            'name': name,
            'psd': str(p),
            'actual_png': str(actual_png),
            'rendered_png': None,
            'diff_png': None,
            'identical': False,
            'diff_pixels': None,
            'diff_bbox': None,
            'error': None,
        }

        if not actual_png.exists():
            item['error'] = 'missing_actual_png'
            results.append(item)
            print(f"[WARN] missing actual png for {name}")
            continue

        # 重新渲染 PSD
        rendered = renders_dir / f"{name}.png"
        try:
            if render_psd_to_png is None:
                raise RuntimeError('render_psd_to_png not available (import failed)')
            render_psd_to_png(p, rendered)
            item['rendered_png'] = str(rendered)
        except Exception as e:
            item['error'] = f'render_error: {e}'
            results.append(item)
            print(f"[ERROR] render failed for {name}: {e}")
            continue

        try:
            bbox, diff_pixels, diff_img = compare_images(actual_png, rendered)
            item['diff_pixels'] = int(diff_pixels)
            item['diff_bbox'] = list(bbox) if bbox else None
            item['identical'] = (diff_pixels == 0)

            diff_path = diffs_dir / f"{name}_diff.png"
            diff_img.save(diff_path)
            item['diff_png'] = str(diff_path)

            # OCR 可选比对：从 PSD 读取期望文本并 OCR 实际图像
            if ocr:
                if not pytesseract:
                    item['ocr'] = {'error': 'pytesseract not installed'}
                else:
                    if tesseract_cmd:
                        try:
                            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
                        except Exception:
                            pass
                    try:
                        psd_obj = PSDImage.open(str(p))
                        layer_data = []
                        for layer in psd_obj.descendants():
                            if layer.kind == 'type':
                                t = layer.text.strip('\x00').strip()
                                if t:
                                    layer_data.append((layer.name, t, layer.bbox))
                    except Exception as e:
                        item['ocr'] = {'error': f'read_psd_error: {e}'}
                        results.append(item)
                        print(f"[ERROR] OCR read PSD failed for {name}: {e}")
                        continue

                    try:
                        png_img = Image.open(str(actual_png)).convert('RGB')
                        img_w, img_h = png_img.size

                        # ── 分图层裁剪 OCR ──
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

                        ocr_scores = []
                        for lname, expected, bbox in layer_data:
                            x1, y1, x2, y2 = bbox
                            # 加 10px padding
                            pad = 10
                            x1, y1 = x1 - pad, y1 - pad
                            x2, y2 = x2 + pad, y2 + pad
                            x1 = max(0, min(x1, img_w - 1))
                            y1 = max(0, min(y1, img_h - 1))
                            x2 = max(x1 + 1, min(x2, img_w))
                            y2 = max(y1 + 1, min(y2, img_h))
                            crop = png_img.crop((x1, y1, x2, y2))
                            ocr_text = pytesseract.image_to_string(crop, lang=ocr_lang, config='--psm 7') if ocr_lang else pytesseract.image_to_string(crop, config='--psm 7')
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
                        all_ok = all(s['score'] >= 0.75 for s in ocr_scores)
                        item['ocr'] = {
                            'ok': all_ok,
                            'avg_score': round(avg_score, 3),
                            'fields': ocr_scores,
                        }
                    except Exception as e:
                        item['ocr'] = {'error': f'ocr_error: {e}'}
                        results.append(item)
                        print(f"[ERROR] OCR failed for {name}: {e}")
                        continue

            results.append(item)
            print(f"[OK] {name} - identical={item['identical']} diff_pixels={item['diff_pixels']}")
        except Exception as e:
            item['error'] = f'compare_error: {e}'
            results.append(item)
            print(f"[ERROR] compare failed for {name}: {e}")

    duration = time.time() - start
    report = {
        'timestamp': time.time(),
        'psd_dir': str(psd_dir),
        'png_dir': str(png_dir),
        'report_dir': str(report_dir),
        'total_psd': total,
        'samples_checked': len(sample_list),
        'duration_seconds': duration,
        'results': results,
    }

    # 保存 JSON 报告与 Markdown 摘要
    json_path = report_dir / 'report.json'
    md_path = report_dir / 'report.md'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    good = sum(1 for r in results if r.get('identical'))
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# 随机抽查报告\n\n")
        f.write(f"PSDs: {total}  Samples checked: {len(sample_list)}  Identical: {good}\n\n")
        for r in results:
            f.write(f"- {r['name']}: identical={r.get('identical')} diff_pixels={r.get('diff_pixels')} error={r.get('error')}\n")
            f.write(f"  - actual_png: {r.get('actual_png')}\n")
            f.write(f"  - rendered_png: {r.get('rendered_png')}\n")
            f.write(f"  - diff_png: {r.get('diff_png')}\n")

    print('\nSummary:')
    print(f"  total_psd={total} samples={len(sample_list)} identical={good}")
    print(f"Report saved: {json_path} and {md_path}")
    return report


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--psd-dir', default='output/test_review/psd')
    p.add_argument('--png-dir', default='output/test_review/png')
    p.add_argument('--samples', type=int, default=3)
    p.add_argument('--report-dir', default='output/test_review/verify_report')
    p.add_argument('--seed', type=int, default=None)
    p.add_argument('--ocr', action='store_true', help='启用 OCR 校验（需安装 pytesseract 与 Tesseract）')
    p.add_argument('--ocr-lang', default=None, help='传递给 tesseract 的语言参数，如 chi_sim 或 eng')
    p.add_argument('--tesseract-cmd', default=None, help='若 tesseract 不在 PATH，传入 tesseract 可执行路径')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    r = run_random_check(Path(args.psd_dir), Path(args.png_dir), args.samples, Path(args.report_dir), args.seed, ocr=args.ocr, ocr_lang=args.ocr_lang, tesseract_cmd=args.tesseract_cmd)
