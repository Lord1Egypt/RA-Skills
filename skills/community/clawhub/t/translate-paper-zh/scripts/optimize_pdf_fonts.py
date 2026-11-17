#!/usr/bin/env python3
"""Subset embedded fonts only if extracted text and every rendered page stay identical."""
import argparse, hashlib, json
from pathlib import Path
import fitz


def fingerprint(doc, dpi):
    result = []
    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72,dpi/72), alpha=False)
        result.append((page.get_text(), tuple(page.rect), pix.width, pix.height,
                       hashlib.sha256(pix.samples).hexdigest()))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--dpi', type=int, default=144)
    a = ap.parse_args()
    if a.input.resolve() == a.output.resolve(): ap.error('Keep the original PDF; use a different output path')
    if not 72 <= a.dpi <= 300: ap.error('--dpi must be 72–300')
    source = a.input.read_bytes(); d = fitz.open(stream=source, filetype='pdf')
    before = fingerprint(d, a.dpi)
    try:
        # FontTools fallback handles CFF/CJK fonts that may fail the MuPDF subsetter.
        d.subset_fonts(fallback=True)
        candidate = d.tobytes(garbage=4, deflate=True)
        out = fitz.open(stream=candidate, filetype='pdf')
        after = fingerprint(out, a.dpi)
    except Exception as exc:
        ap.error(f'Font optimization failed; keep the original. {exc}')
    if before != after:
        ap.error('Optimization changed text or rendered pixels; no optimized output written')
    if len(candidate) >= len(source):
        ap.error('No file-size reduction; keep the original PDF')
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes(candidate)
    print(json.dumps({'input_bytes':len(source),'output_bytes':len(candidate),
        'pages_checked':len(out),'dpi':a.dpi,'text_identical':True,'pixels_identical':True,
        'output_sha256':hashlib.sha256(candidate).hexdigest(),
        'note':'Run the final coverage/visual audit on this output; its checksum has changed.'}))

if __name__ == '__main__': main()
