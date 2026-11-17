#!/usr/bin/env python3
"""Inventory source PDF text/visuals and render pages; no translation service required."""
import argparse, hashlib, json
from pathlib import Path
import fitz


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pdf', type=Path)
    ap.add_argument('out', type=Path)
    ap.add_argument('--source-url', default='')
    ap.add_argument('--rights-basis', default='unverified')
    ap.add_argument('--dpi', type=int, default=120)
    ap.add_argument('--no-render', action='store_true')
    a = ap.parse_args()
    if not 36 <= a.dpi <= 600:
        ap.error('--dpi must be 36–600')
    a.out.mkdir(parents=True, exist_ok=True)
    d = fitz.open(a.pdf)
    if d.is_encrypted:
        ap.error('Unlock the authorized PDF before inventorying it')
    inventory = {'schema': 1, 'source': {'path': str(a.pdf.resolve()),
                 'sha256': sha(a.pdf), 'url': a.source_url,
                 'rights_basis': a.rights_basis}, 'pages': [], 'units': []}
    for pn, page in enumerate(d, 1):
        words = page.get_text('words')
        pg = {'page': pn, 'width': page.rect.width, 'height': page.rect.height,
              'image_count': len(page.get_images()), 'drawing_count': len(page.get_drawings()),
              'text_word_count': len(words), 'needs_ocr_review': len(words) < 20,
              'render': None, 'visual_inventory_checked': False}
        for bi, b in enumerate(page.get_text('dict', sort=True)['blocks']):
            if b['type'] != 0:
                continue
            spans = [{'text': s['text'], 'bbox': list(s['bbox']), 'font': s['font'],
                      'size': s['size']} for l in b['lines'] for s in l['spans']]
            text = '\n'.join(''.join(s['text'] for s in l['spans']) for l in b['lines'])
            if not text.strip():
                continue
            inventory['units'].append({'id': f'p{pn:03d}-b{bi:03d}', 'page': pn,
                'bbox': list(b['bbox']), 'source_text': text, 'spans': spans,
                'kind': 'unclassified'})
        if not a.no_render:
            filename = f'source-{pn:03d}.png'
            page.get_pixmap(matrix=fitz.Matrix(a.dpi/72, a.dpi/72), alpha=False).save(a.out/filename)
            pg['render'] = filename
        inventory['pages'].append(pg)
    (a.out/'inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2))
    plan = {'schema': 1, 'source_sha256': inventory['source']['sha256'],
            'inventory_sha256': sha(a.out/'inventory.json'),
            'rights': {'verified': False, 'basis': a.rights_basis, 'evidence': a.source_url},
            'units': [{'id': u['id'], 'status': 'pending', 'target': '', 'output_pages': [],
                       'fidelity_checked': False, 'kind': 'unclassified', 'reason': ''} for u in inventory['units']],
            'visual_units': [], 'regions': [], 'allowed_english': [], 'output_sha256': '',
            'source_reviews': [{'source_page': p['page'], 'visual_inventory_checked': False, 'ocr_checked': False, 'visual_unit_ids': []} for p in inventory['pages']], 'page_reviews': []}
    path = a.out/'translation.json'
    if not path.exists():
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    print(json.dumps({'pages': len(d), 'units': len(inventory['units']),
          'inventory': str(a.out/'inventory.json'), 'plan': str(path),
          'warning': 'Inspect every source page; extracted blocks do not discover all raster/vector labels.'}))

if __name__ == '__main__':
    main()
