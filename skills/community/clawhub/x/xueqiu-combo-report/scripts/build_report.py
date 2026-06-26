#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def normalize_combo_list(raw):
    if isinstance(raw, dict) and 'comboHoldings' in raw:
        return list(raw['comboHoldings']), list(raw.get('failures', []))
    if isinstance(raw, list):
        return list(raw), []
    raise ValueError('Input JSON must be either a list of combo objects or an object with comboHoldings/failures')


def apply_patch(combos, patch_items):
    by_symbol = {c['combo_symbol']: c for c in combos}
    for item in patch_items:
        by_symbol[item['combo_symbol']] = item
    return sorted(by_symbol.values(), key=lambda x: x['combo_symbol'])


def build_ranking(combos):
    stock_map = {}
    for combo in combos:
        for h in combo.get('holdings', []):
            weight = float(h.get('weight', 0) or 0)
            if weight <= 0:
                continue
            sym = h['stock_symbol']
            if sym not in stock_map:
                stock_map[sym] = {
                    'stock_symbol': sym,
                    'stock_name': h['stock_name'],
                    'combo_count': 0,
                    'total_weight': 0.0,
                    'combos': []
                }
            stock_map[sym]['combo_count'] += 1
            stock_map[sym]['total_weight'] += weight
            stock_map[sym]['combos'].append({
                'combo_name': combo['combo_name'],
                'combo_symbol': combo['combo_symbol'],
                'weight': weight,
                'best_record_at': combo.get('best_record_at', '')
            })
    return sorted(stock_map.values(), key=lambda x: (-x['combo_count'], -x['total_weight'], x['stock_symbol']))


def render_markdown(output, ranking, title, note):
    lines = [
        f'# {title}', '', note, '',
        f'- 组合总数：{output["comboCount"]}',
        f'- 成功纳入统计：{output["successComboCount"]}',
        f'- 失败组合数：{output["failureCount"]}',
        f'- 去重后股票数：{output["uniqueStockCount"]}', '',
        '## 股票排名总表', '',
        '| 排名 | 股票名称 | 股票代码 | 被持仓组合数量 | 合计持仓比例 | 所在组合及持仓比例 |',
        '| --- | --- | --- | ---: | ---: | --- |',
    ]
    for i, item in enumerate(ranking, 1):
        combos_text = '<br>'.join(
            f'{c["combo_name"]}（{c["combo_symbol"]}，{c["weight"]}%）' for c in sorted(item['combos'], key=lambda x: (-x['weight'], x['combo_symbol']))
        )
        lines.append(f'| {i} | {item["stock_name"]} | {item["stock_symbol"]} | {item["combo_count"]} | {item["total_weight"]:.2f}% | {combos_text} |')
    return '\n'.join(lines)


def render_html(output, ranking, title, note):
    parts = [f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8" /><title>{title}</title>
<style>
body {{ font-family: "Noto Sans CJK SC", "Microsoft YaHei", Arial, sans-serif; margin: 24px; color: #222; }}
table {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin: 12px 0 24px; font-size: 12px; }}
th, td {{ border: 1px solid #999; padding: 6px 8px; vertical-align: top; word-break: break-word; }}
th {{ background: #f3f3f3; }}
@page {{ size: A4 landscape; margin: 12mm; }}
</style></head><body>
<h1>{title}</h1><p>{note}</p>
<ul><li>组合总数：{output['comboCount']}</li><li>成功纳入统计：{output['successComboCount']}</li><li>失败组合数：{output['failureCount']}</li><li>去重后股票数：{output['uniqueStockCount']}</li></ul>
<table><thead><tr><th style="width:50px">排名</th><th style="width:110px">股票名称</th><th style="width:90px">股票代码</th><th style="width:80px">被持仓组合数量</th><th style="width:80px">合计持仓比例</th><th>所在组合及持仓比例</th></tr></thead><tbody>
''']
    for i, item in enumerate(ranking, 1):
        combos_html = '<br>'.join(
            f'{c["combo_name"]}（{c["combo_symbol"]}，{c["weight"]}%）' for c in sorted(item['combos'], key=lambda x: (-x['weight'], x['combo_symbol']))
        )
        parts.append(f'<tr><td>{i}</td><td>{item["stock_name"]}</td><td>{item["stock_symbol"]}</td><td>{item["combo_count"]}</td><td>{item["total_weight"]:.2f}%</td><td>{combos_html}</td></tr>')
    parts.append('</tbody></table></body></html>')
    return '\n'.join(parts)


def maybe_render_pdf(html_path: Path, pdf_path: Path):
    chrome = shutil.which('google-chrome-stable') or shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome:
        return False, 'No Chrome/Chromium binary found'
    subprocess.run([chrome, '--headless', '--disable-gpu', '--no-sandbox', f'--print-to-pdf={pdf_path}', html_path.resolve().as_uri()], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return True, None


def main():
    ap = argparse.ArgumentParser(description='Build ranked stock-holdings reports (JSON/MD/HTML/PDF) from Xueqiu combo holdings data.')
    ap.add_argument('input_json')
    ap.add_argument('--patch-json')
    ap.add_argument('--output-prefix', required=True)
    ap.add_argument('--title', default='雪球组合股票持仓完整汇总')
    ap.add_argument('--note', default='按“被持仓组合数量”从高到低排序，仅统计权重大于0的持仓。')
    args = ap.parse_args()

    combos, failures = normalize_combo_list(load_json(Path(args.input_json)))
    if args.patch_json:
        patch_obj = load_json(Path(args.patch_json))
        patch_items = patch_obj if isinstance(patch_obj, list) else patch_obj.get('comboHoldings', patch_obj.get('patches', []))
        combos = apply_patch(combos, patch_items)
        patched_symbols = {x['combo_symbol'] for x in patch_items}
        failures = [f for f in failures if f.get('combo_symbol') not in patched_symbols]

    ranking = build_ranking(combos)
    output = {
        'note': args.note,
        'comboCount': len(combos),
        'successComboCount': len(combos) - len(failures),
        'failureCount': len(failures),
        'failures': failures,
        'uniqueStockCount': len(ranking),
        'ranking': ranking,
        'comboHoldings': sorted(combos, key=lambda x: x['combo_symbol']),
    }

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = prefix.with_suffix('.json')
    md_path = prefix.with_suffix('.md')
    html_path = prefix.with_suffix('.html')
    pdf_path = prefix.with_suffix('.pdf')

    dump_json(json_path, output)
    md_path.write_text(render_markdown(output, ranking, args.title, args.note), encoding='utf-8')
    html_path.write_text(render_html(output, ranking, args.title, args.note), encoding='utf-8')

    ok, err = maybe_render_pdf(html_path, pdf_path)
    print(json_path)
    print(md_path)
    print(html_path)
    print(pdf_path if ok else f'PDF skipped: {err}')


if __name__ == '__main__':
    main()
