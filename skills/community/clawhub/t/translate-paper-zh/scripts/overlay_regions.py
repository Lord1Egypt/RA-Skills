#!/usr/bin/env python3
"""Apply explicitly planned Chinese PDF text regions, preserving original nontext art.
This is a layout aid, not a translator or proof of completeness. Refuse unsafe overlaps.
"""
import argparse, hashlib, html, json
from pathlib import Path
import fitz


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source', type=Path)
    ap.add_argument('inventory', type=Path)
    ap.add_argument('plan', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--font', required=True, type=Path, help='Locally available, embeddable CJK font file')
    ap.add_argument('--min-font-size', type=float, default=8.0)
    a = ap.parse_args()
    inv, plan = (json.loads(p.read_text()) for p in (a.inventory, a.plan))
    if sha(a.source) != inv['source']['sha256'] or sha(a.source) != plan['source_sha256']:
        ap.error('Source hash mismatch')
    if sha(a.inventory) != plan['inventory_sha256']:
        ap.error('Inventory changed; reconcile the plan first')
    if a.output.resolve() == a.source.resolve():
        ap.error('Never overwrite the source PDF')
    if not a.font.is_file(): ap.error('CJK font file does not exist')
    if not plan.get('regions'): ap.error('Plan has no explicit layout regions')
    d = fitz.open(a.source)
    units = {u['id']: u for u in inv['units']}
    planned = {u['id']: u for u in plan['units']}
    used, regions_by_page = set(), {}
    for r in plan['regions']:
        pn = int(r['page']); rect = fitz.Rect(r['bbox']); ids = r['source_ids']
        if not 1 <= pn <= len(d) or rect.is_empty or not rect in d[pn-1].rect:
            ap.error(f'Invalid region page/bbox: {r}')
        if not ids or any(i not in units or units[i]['page'] != pn for i in ids):
            ap.error('Each region must reference valid text units on its source page')
        if used.intersection(ids): ap.error('Source unit assigned to more than one region')
        used.update(ids)
        if any(i not in planned or planned[i]['status'] != 'translated' for i in ids):
            ap.error('Region source units must be explicitly marked translated')
        if not r.get('target', '').strip(): ap.error('Empty translated region')
        if any(planned[i].get('target', '').strip() not in r['target'] for i in ids):
            ap.error('Region target must contain every source unit target')
        for other in inv['units']:
            if other['page'] == pn and other['id'] not in ids:
                if any((rect & fitz.Rect(s['bbox'])).get_area() > 1 for s in other['spans']):
                    ap.error(f'Region overlaps untouched text unit {other["id"]}; replan layout')
        for prior in regions_by_page.get(pn, []):
            if (rect & fitz.Rect(prior['bbox'])).get_area() > 1:
                ap.error('Target regions overlap')
        regions_by_page.setdefault(pn, []).append(r)
    results = []
    for pn, regions in regions_by_page.items():
        page = d[pn-1]
        for r in regions:
            for ident in r['source_ids']:
                for s in units[ident]['spans']:
                    rect = fitz.Rect(s['bbox'])
                    # Shrink vertically to avoid deleting an adjacent line at a shared edge.
                    rect.y0 += min(0.5, rect.height/10); rect.y1 -= min(0.5, rect.height/10)
                    page.add_redact_annot(rect, fill=False, cross_out=False)
        page.apply_redactions(images=0, graphics=0, text=0)
        for r in regions:
            size = float(r.get('font_size', 9.5))
            if size < a.min_font_size: ap.error('Requested font size below readability floor')
            css = f'@font-face{{font-family:paperzh;src:url("{a.font.name}");}} body{{font-family:paperzh;font-size:{size}pt;line-height:{r.get("line_height",1.2)};margin:0;color:#000;}}'
            content = '<div>' + html.escape(r['target']).replace('\n','<br>') + '</div>'
            spare, scale = page.insert_htmlbox(fitz.Rect(r['bbox']), content, css=css,
                archive=fitz.Archive(str(a.font.parent)), scale_low=a.min_font_size/size)
            if spare < 0:
                ap.error(f'Text overflow on page {pn}; adjust region or use source-led reflow. No output saved.')
            results.append({'page': pn, 'source_ids': r['source_ids'],
                            'font_size': size*scale, 'scale': scale})
    a.output.parent.mkdir(parents=True, exist_ok=True)
    d.set_metadata({**d.metadata, 'title': plan.get('title', 'Academic paper — Chinese translation'),
                    'subject': 'Unofficial translation; source authorship and citations retained'})
    d.save(a.output, garbage=4, deflate=True)
    report = {'output_sha256': sha(a.output), 'regions': results,
              'note': 'Layout only. Run audit_translation.py and inspect all rendered pages before delivery.'}
    a.output.with_suffix('.layout.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__': main()
