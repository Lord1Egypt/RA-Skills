#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path


def which(name: str) -> str | None:
    return shutil.which(name)


def run(cmd: list[str], *, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def chunk_text(text: str, target_chars: int, overlap_chars: int) -> list[str]:
    if target_chars <= 0:
        return [text]
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + target_chars)
        chunks.append(text[start:end])
        if end >= n:
            break
        start = max(end - overlap_chars, start + 1)
    return chunks


def detect_uvx() -> str | None:
    candidates = [which('uvx'), os.path.expanduser('~/.local/bin/uvx')]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def derive_filename_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    name = Path(parsed.path).name or 'downloaded.pdf'
    if not name.lower().endswith('.pdf'):
        name += '.pdf'
    return name


def download_pdf(url: str, download_path: Path, timeout: int) -> dict:
    ensure_parent(download_path)
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw resilient-pdf/1.1.0'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get('Content-Type', '')
            payload = response.read()
    except Exception as exc:
        return {'ok': False, 'error': f'download failed: {exc}', 'url': url}

    if not payload.startswith(b'%PDF') and 'pdf' not in content_type.lower():
        return {
            'ok': False,
            'error': 'downloaded content does not look like a PDF',
            'url': url,
            'content_type': content_type,
        }

    download_path.write_bytes(payload)
    return {
        'ok': True,
        'url': url,
        'download_path': str(download_path),
        'download_bytes': len(payload),
        'content_type': content_type,
    }


def extract_with_markitdown(pdf_path: Path, output_path: Path, timeout: int) -> dict:
    uvx = detect_uvx()
    if not uvx:
        return {
            'ok': False,
            'method': 'markitdown',
            'error': 'uvx not found',
            'install_hint': "python3 -m pip install --user --break-system-packages uv",
        }

    ensure_parent(output_path)
    cmd = [uvx, '--from', 'markitdown[pdf]', 'markitdown', str(pdf_path), '-o', str(output_path)]
    try:
        proc = run(cmd, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'ok': False, 'method': 'markitdown', 'error': 'timed out', 'command': cmd}

    if proc.returncode != 0:
        return {
            'ok': False,
            'method': 'markitdown',
            'error': 'conversion failed',
            'command': cmd,
            'stderr': proc.stderr[-4000:],
            'stdout': proc.stdout[-2000:],
        }

    if not output_path.exists() or output_path.stat().st_size == 0:
        return {'ok': False, 'method': 'markitdown', 'error': 'no output produced', 'command': cmd}

    return {
        'ok': True,
        'method': 'markitdown',
        'output_path': str(output_path),
        'bytes': output_path.stat().st_size,
        'command': cmd,
        'stderr_tail': proc.stderr[-2000:],
    }


def summarize_text(text: str, chunk_paths: list[str] | None = None) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    headings = [line for line in lines if line.startswith('#')][:12]
    bullet_candidates = []
    for line in lines[:400]:
        lower = line.lower()
        if len(line) < 40:
            continue
        if any(token in lower for token in ['abstract', 'introduction', 'conclusion', 'summary', 'results', 'discussion', 'evaluation', 'safety', 'alignment', 'cyber']):
            bullet_candidates.append(line)
        if len(bullet_candidates) >= 12:
            break

    preview = lines[:18]
    summary_lines = ['# First-pass summary', '']
    if preview:
        summary_lines.append('## Opening preview')
        for line in preview[:8]:
            summary_lines.append(f'- {line[:220]}')
        summary_lines.append('')

    if headings:
        summary_lines.append('## Detected headings')
        for line in headings:
            summary_lines.append(f'- {line[:220]}')
        summary_lines.append('')

    if bullet_candidates:
        summary_lines.append('## Likely key passages')
        for line in bullet_candidates[:10]:
            summary_lines.append(f'- {line[:260]}')
        summary_lines.append('')

    summary_lines.append('## Stats')
    summary_lines.append(f'- Characters: {len(text)}')
    summary_lines.append(f'- Non-empty lines scanned: {len(lines)}')
    if chunk_paths:
        summary_lines.append(f'- Chunk count: {len(chunk_paths)}')
    summary_lines.append('')
    summary_lines.append('## Note')
    summary_lines.append('- This is a lightweight first-pass summary artifact, not a substitute for a model-written final summary.')

    return {
        'summary_markdown': '\n'.join(summary_lines) + '\n',
        'heading_count': len(headings),
        'key_passage_count': len(bullet_candidates),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Resilient local PDF extraction with URL fetch, chunking, and first-pass summary support.')
    parser.add_argument('pdf', nargs='?', help='Path to local PDF file')
    parser.add_argument('--url', help='Remote PDF URL to download first')
    parser.add_argument('--download-to', help='Where to save the downloaded PDF when using --url')
    parser.add_argument('--out', required=True, help='Output markdown/text file path')
    parser.add_argument('--timeout', type=int, default=600, help='Extraction timeout in seconds')
    parser.add_argument('--chunk-dir', help='Optional output directory for chunk files')
    parser.add_argument('--chunk-chars', type=int, default=120000, help='Characters per chunk')
    parser.add_argument('--chunk-overlap', type=int, default=4000, help='Overlap characters between chunks')
    parser.add_argument('--summary-out', help='Optional path for first-pass summary markdown')
    parser.add_argument('--json', action='store_true', help='Emit JSON result')
    args = parser.parse_args()

    if not args.pdf and not args.url:
        result = {'ok': False, 'error': 'provide either a local pdf path or --url'}
        print(json.dumps(result, indent=2) if args.json else result['error'])
        return 1

    output_path = Path(args.out).expanduser().resolve()

    if args.url:
        download_name = derive_filename_from_url(args.url)
        download_target = Path(args.download_to).expanduser().resolve() if args.download_to else (output_path.parent / download_name)
        dl = download_pdf(args.url, download_target, args.timeout)
        if not dl.get('ok'):
            print(json.dumps(dl, indent=2) if args.json else dl.get('error', 'download failed'))
            return 1
        pdf_path = Path(dl['download_path']).resolve()
        result = {'download': dl}
    else:
        pdf_path = Path(args.pdf).expanduser().resolve()
        result = {}

    if not pdf_path.exists():
        result = {'ok': False, 'error': f'pdf not found: {pdf_path}'}
        print(json.dumps(result, indent=2) if args.json else result['error'])
        return 1

    if pdf_path.suffix.lower() != '.pdf':
        result = {'ok': False, 'error': f'not a pdf: {pdf_path}'}
        print(json.dumps(result, indent=2) if args.json else result['error'])
        return 1

    extract_result = extract_with_markitdown(pdf_path, output_path, args.timeout)
    if not extract_result.get('ok'):
        print(json.dumps(extract_result, indent=2) if args.json else extract_result.get('error', 'extraction failed'))
        return 1

    result.update(extract_result)
    result['pdf_path'] = str(pdf_path)

    text = output_path.read_text(encoding='utf-8', errors='replace')
    result['text_chars'] = len(text)
    chunk_paths = None

    if args.chunk_dir:
        chunk_dir = Path(args.chunk_dir).expanduser().resolve()
        chunk_dir.mkdir(parents=True, exist_ok=True)
        chunks = chunk_text(text, args.chunk_chars, args.chunk_overlap)
        chunk_paths = []
        for i, chunk in enumerate(chunks, start=1):
            chunk_path = chunk_dir / f'chunk-{i:03d}.md'
            chunk_path.write_text(chunk, encoding='utf-8')
            chunk_paths.append(str(chunk_path))
        result['chunk_dir'] = str(chunk_dir)
        result['chunk_count'] = len(chunk_paths)
        result['chunk_paths'] = chunk_paths

    if args.summary_out:
        summary_path = Path(args.summary_out).expanduser().resolve()
        ensure_parent(summary_path)
        summary_result = summarize_text(text, chunk_paths)
        summary_path.write_text(summary_result['summary_markdown'], encoding='utf-8')
        result['summary_path'] = str(summary_path)
        result['summary_heading_count'] = summary_result['heading_count']
        result['summary_key_passage_count'] = summary_result['key_passage_count']

    result['ok'] = True

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"OK: {result['output_path']} ({result['text_chars']} chars)")
        if 'chunk_count' in result:
            print(f"Chunks: {result['chunk_count']} in {result['chunk_dir']}")
        if 'summary_path' in result:
            print(f"Summary: {result['summary_path']}")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
