#!/usr/bin/env python3
"""Fail-closed translation coverage, searchable-text, font and page-review audit.
Exit 0 means recorded gates pass, not an independent guarantee of linguistic accuracy.
"""
import argparse, hashlib, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path
import fitz


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(t): return re.sub(r'\s+', '', unicodedata.normalize('NFKC', t).replace('\u00ad', ''))
def english(t): return set(re.findall(r'\b[A-Za-z][A-Za-z-]{3,}\b', t))
def numbers(t): return Counter(re.findall(r'\d+(?:\.\d+)?', unicodedata.normalize('NFKC', t)))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('inventory', type=Path)
    ap.add_argument('plan', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('report_dir', type=Path)
    ap.add_argument('--dpi', type=int, default=144)
    a = ap.parse_args()
    a.report_dir.mkdir(parents=True, exist_ok=True)
    inv, plan = (json.loads(p.read_text()) for p in (a.inventory, a.plan))
    issues, warnings = [], []
    def require(ok, message):
        if not ok: issues.append(message)
    require(plan.get('schema') == 1, 'Unsupported plan schema')
    require(plan.get('source_sha256') == inv['source']['sha256'], 'Source checksum mismatch')
    require(plan.get('inventory_sha256') == sha(a.inventory), 'Inventory checksum mismatch')
    rights = plan.get('rights', {})
    require(rights.get('verified') and rights.get('basis') and rights.get('evidence'), 'Source provenance/rights not verified')
    d = fitz.open(a.output)
    output_hash = sha(a.output)
    require(plan.get('output_sha256') == output_hash, 'QA is not bound to current output checksum')
    pages = {i+1: p.get_text() for i, p in enumerate(d)}
    page_norm = {p:norm(t) for p,t in pages.items()}
    font_info = {}
    for page in d:
        for f in page.get_fonts(full=True):
            xref = f[0]
            if xref in font_info: continue
            try: name, ext, kind, data = d.extract_font(xref)
            except Exception: name, ext, kind, data = f[3], '', '', b''
            font_info[xref] = {'name':name, 'type':kind, 'embedded':bool(data)}
    require(any(re.search(r'[\u3400-\u9fff]', t) for t in pages.values()), 'Output has no extractable Chinese text')
    for pn, text in pages.items():
        compatibility = sorted({f'U+{ord(c):04X}' for c in text if (0xF900 <= ord(c) <= 0xFAFF or 0x2F800 <= ord(c) <= 0x2FA1F) and unicodedata.normalize('NFKC',c) != c})
        require(not compatibility, f'Output page {pn}: normalize CJK compatibility ToUnicode mappings for exact search: {compatibility}')
        for character in ('\ufffd', '\x00'):
            count = text.count(character)
            if count:
                exceptions = [e for e in plan.get('glyph_exceptions', []) if e.get('page') == pn and e.get('character') == character and e.get('count') == count and e.get('visual_checked') is True and e.get('reason')]
                require(bool(exceptions), f'Output page {pn}: {count} replacement/null glyphs need exact visual review or text-layer repair')
    # Inspect fonts actually attached to extracted Chinese spans, not only names.
    cjk_font_names = set()
    for page in d:
        for b in page.get_text('dict')['blocks']:
            if b['type'] == 0:
                for l in b['lines']:
                    for s in l['spans']:
                        if re.search(r'[\u3400-\u9fff]', s['text']): cjk_font_names.add(s['font'])
    def simple(name):
        base = re.sub(r'-Identity-[HV]$', '', name.split('+')[-1], flags=re.I)
        return re.sub('[^a-z0-9]', '', base.lower())
    for name in cjk_font_names:
        matching = [f for f in font_info.values() if simple(name) == simple(f['name'])]
        require(bool(matching) and all(f['embedded'] for f in matching), f'Chinese font embedding unverified: {name}')
    expected = {u['id']: u for u in inv['units']}
    actual = plan.get('units', [])
    ids = [u['id'] for u in actual]
    require(len(ids) == len(set(ids)), 'Duplicate source unit entries')
    require(set(ids) == set(expected), 'Source unit coverage differs from inventory')
    allowed = {p:set() for p in pages}
    retained_kinds = {'math', 'identifier', 'citation', 'reference', 'author', 'number'}
    counts = {'translated':0, 'retained':0, 'pending':0}
    numeric_candidates = []
    for u in actual:
        ident = u['id']; status = u.get('status'); source = expected.get(ident)
        if source is None: continue
        if status in counts: counts[status] += 1
        require(status in {'translated','retained'}, f'{ident}: unfinished status')
        require(u.get('fidelity_checked') is True, f'{ident}: semantic/numeric/math/citation review missing')
        out_pages = u.get('output_pages', [])
        require(bool(out_pages) and all(p in pages for p in out_pages), f'{ident}: output page mapping missing/invalid')
        output_text = ''.join(page_norm.get(p,'') for p in out_pages)
        if status == 'translated':
            target = u.get('target','')
            require(bool(target.strip()), f'{ident}: target translation missing')
            require(bool(target.strip()) and norm(target) in output_text, f'{ident}: target not found in searchable PDF text')
            require(bool(re.search(r'[\u3400-\u9fff]', target)), f'{ident}: translated target contains no Chinese')
            if numbers(source['source_text']) != numbers(target):
                numeric_candidates.append({'id':ident, 'source':dict(numbers(source['source_text'])), 'target':dict(numbers(target)), 'review':u.get('numeric_review','')})
                require(bool(u.get('numeric_review')), f'{ident}: numeric-token difference requires explicit review')
        elif status == 'retained':
            require(u.get('kind') in retained_kinds and bool(u.get('reason')), f'{ident}: invalid/unexplained English retention')
            require(norm(source['source_text']) in output_text, f'{ident}: retained source not found in PDF text')
            for p in out_pages:
                if p in allowed: allowed[p].update(english(source['source_text']))
    (a.report_dir/'numeric_candidates.json').write_text(json.dumps(numeric_candidates,ensure_ascii=False,indent=2))
    visual_ids = [u.get('id') for u in plan.get('visual_units', [])]
    require(len(visual_ids) == len(set(visual_ids)), 'Duplicate visual unit IDs')
    for u in plan.get('visual_units', []):
        require(u.get('status') in {'translated','retained'} and u.get('fidelity_checked') is True,
                f'Visual unit {u.get("id")}: unfinished translation/review')
        require(bool(u.get('bbox')) and u.get('page') in range(1,len(inv['pages'])+1), f'Visual unit {u.get("id")}: source location missing')
        if u.get('status') == 'translated':
            text = ''.join(page_norm.get(p,'') for p in u.get('output_pages',[]))
            require(bool(u.get('target')) and norm(u['target']) in text, f'Visual unit {u.get("id")}: target not searchable')
        else:
            require(u.get('kind') in retained_kinds and bool(u.get('reason')), f'Visual unit {u.get("id")}: unjustified retained content')
    source_review_list = plan.get('source_reviews',[])
    source_reviews = {r.get('source_page'):r for r in source_review_list}
    require(len(source_reviews) == len(source_review_list) and set(source_reviews) == set(range(1,len(inv['pages'])+1)), 'Source page review coverage invalid')
    for p in inv['pages']:
        review = source_reviews.get(p['page'], {})
        require(review.get('visual_inventory_checked') is True, f'Source page {p["page"]}: raster/vector labels, footnotes and appendix not inventoried')
        require(set(review.get('visual_unit_ids',[])) == {u['id'] for u in plan.get('visual_units',[]) if u['page']==p['page']}, f'Source page {p["page"]}: visual unit list mismatch')
        if p.get('needs_ocr_review'):
            require(review.get('ocr_checked') is True, f'Source page {p["page"]}: sparse/scanned text needs OCR review')
    for item in plan.get('allowed_english', []):
        if not isinstance(item, dict) or not item.get('reason') or not item.get('text') or item.get('page') not in pages:
            issues.append('Allowed English entries require exact text, output page and reason')
            continue
        allowed[item['page']].update(english(item['text']))
    remaining = [{'page':p, 'words':sorted(english(t)-allowed[p])} for p,t in pages.items() if english(t)-allowed[p]]
    require(not remaining, 'Unreviewed English remains; inspect remaining_english.json')
    (a.report_dir/'remaining_english.json').write_text(json.dumps(remaining, ensure_ascii=False, indent=2))
    review_list = plan.get('page_reviews',[])
    reviews = {r.get('output_page'):r for r in review_list}
    require(len(reviews) == len(review_list) and set(reviews) == set(pages), 'Output page review coverage invalid')
    template = []
    for pn, page in enumerate(d,1):
        path = a.report_dir/f'page-{pn:03d}.png'
        page.get_pixmap(matrix=fitz.Matrix(a.dpi/72,a.dpi/72),alpha=False).save(path)
        image_hash = sha(path)
        r = reviews.get(pn,{})
        require(r.get('render_sha256') == image_hash and r.get('passed') is True and bool(r.get('reviewer')),
                f'Output page {pn}: current rendered-page visual inspection not recorded')
        for key in ('no_clipping','no_overlap','legible','figures_complete','math_data_citations_checked'):
            require(r.get(key) is True, f'Output page {pn}: {key} not verified')
        template.append({'output_page':pn,'render_sha256':image_hash,'render_path':str(path),
                         'passed':False,'reviewer':'','no_clipping':False,'no_overlap':False,
                         'legible':False,'figures_complete':False,'math_data_citations_checked':False,'notes':''})
    (a.report_dir/'qa-template.json').write_text(json.dumps({'output_sha256':output_hash,'page_reviews':template},ensure_ascii=False,indent=2))
    if len(d) != len(inv['pages']): warnings.append('Page count changed; verify source-to-output mapping and appendix coverage')
    result = {'gate_passed':not issues, 'output_sha256':output_hash, 'source_units':len(expected),
              'coverage':counts,'output_pages':len(d),'fonts':list(font_info.values()),
              'issues':issues,'warnings':warnings,
              'meaning':'Automated checks and recorded human/model reviews pass only when gate_passed is true. Semantic accuracy still depends on genuine inspection.'}
    (a.report_dir/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({'gate_passed':not issues,'issues':len(issues),'coverage':counts,
                      'report':str(a.report_dir/'audit.json')},ensure_ascii=False))
    return 0 if not issues else 1

if __name__ == '__main__': sys.exit(main())
