#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

SKILL_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SKILL_ROOT.parents[1]
DEFAULT_KB_ROOT = WORKSPACE / 'knowledge' / 'video-notes'
YTDLP = shutil.which('yt-dlp') or '/home/jason/.local/bin/yt-dlp'
SUMMARIZE = shutil.which('summarize') or '/home/jason/.local/bin/summarize'
WHISPER = str(SKILL_ROOT / 'scripts' / 'whisper-gpu.sh')

MEDIA_EXTS = {
    '.mp4', '.mkv', '.webm', '.mov', '.m4v', '.avi', '.flv', '.wmv', '.mp3', '.m4a', '.aac', '.wav', '.flac', '.ogg', '.opus'
}
TEXT_EXTS = {'.txt', '.md'}
SUB_EXTS = {'.srt', '.vtt'}
IGNORE_DOWNLOAD_EXTS = {'.json', '.description', '.part', '.ytdl', '.srt', '.vtt', '.ass', '.lrc'}


def is_url(value: str) -> bool:
    p = urlparse(value)
    return p.scheme in {'http', 'https'} and bool(p.netloc)


def slugify(text: str, max_len: int = 80) -> str:
    text = re.sub(r'\s+', '-', text.strip().lower())
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff._-]+', '-', text)
    text = re.sub(r'-{2,}', '-', text).strip('-._')
    return text[:max_len] or 'item'


def normalize_source_url(value: str) -> str:
    if not is_url(value):
        return value

    parsed = urlparse(value)
    host = parsed.netloc.lower()
    query_pairs = parse_qsl(parsed.query, keep_blank_values=True)

    # Bilibili is picky: shared links like bilibili.com/video/... with tracking params
    # can 403 in metadata mode, while www.bilibili.com/video/... works.
    if host in {'bilibili.com', 'm.bilibili.com'}:
        cleaned_query = [(k, v) for k, v in query_pairs if not k.startswith('spm_')]
        parsed = parsed._replace(netloc='www.bilibili.com', query=urlencode(cleaned_query))
        return urlunparse(parsed)

    # Keep YouTube timestamps, but strip common tracking params.
    if host in {'youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be'}:
        allowed = {'v', 't', 'list', 'index', 'start'}
        cleaned_query = [(k, v) for k, v in query_pairs if k in allowed]
        parsed = parsed._replace(query=urlencode(cleaned_query))
        return urlunparse(parsed)

    return value


def run(cmd: list[str], *, cwd: Path | None = None, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env['PATH'] = f"/home/jason/.local/bin:/home/jason/.npm-global/bin:{env.get('PATH','')}"
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        capture_output=capture,
    )
    if check and proc.returncode != 0:
        msg = proc.stderr or proc.stdout or f'command failed: {cmd}'
        raise RuntimeError(msg.strip())
    return proc


def json_dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def strip_subtitle_to_text(path: Path) -> str:
    text = read_text(path)
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip().replace('\ufeff', '')
        if not line:
            continue
        if line == 'WEBVTT' or line.startswith('NOTE'):
            continue
        if re.fullmatch(r'\d+', line):
            continue
        if '-->' in line:
            continue
        if re.match(r'^(kind|language|Style|Format):', line, re.I):
            continue
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'\{\\.*?\}', '', line)
        line = re.sub(r'\s+', ' ', line).strip()
        if line:
            lines.append(line)
    return '\n'.join(lines).strip() + '\n'


def choose_best_subtitle(paths: list[Path]) -> Path | None:
    if not paths:
        return None

    def score(p: Path) -> tuple[int, int, int]:
        name = p.name.lower()
        lang_score = 0
        if '.zh' in name or 'chinese' in name:
            lang_score = 4
        elif '.en' in name or 'english' in name:
            lang_score = 3
        elif '.auto' not in name:
            lang_score = 2
        ext_score = 2 if p.suffix.lower() == '.srt' else 1
        size_score = p.stat().st_size if p.exists() else 0
        return (lang_score, ext_score, size_score)

    return sorted(paths, key=score, reverse=True)[0]


def load_yt_metadata(url: str) -> dict[str, Any]:
    proc = run([YTDLP, '--dump-single-json', '--skip-download', url], capture=True)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f'failed to parse yt-dlp metadata: {e}') from e


def find_downloaded_media(download_dir: Path) -> Path | None:
    candidates: list[Path] = []
    for p in download_dir.iterdir():
        if not p.is_file():
            continue
        if p.suffix.lower() in IGNORE_DOWNLOAD_EXTS:
            continue
        candidates.append(p)
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.stat().st_size, reverse=True)[0]


def transcribe_media(media_path: Path, item_dir: Path, language: str | None) -> tuple[Path, str]:
    whisper_dir = item_dir / 'whisper'
    whisper_dir.mkdir(parents=True, exist_ok=True)
    base_cmd = [WHISPER, str(media_path), '--output-dir', str(whisper_dir), '--output-format', 'all']
    if language:
        base_cmd += ['--language', language]

    backend = 'whisper-gpu.sh'
    try:
        run(base_cmd, capture=True)
    except Exception:
        backend = 'whisper-cpu'
        run(base_cmd + ['--device', 'cpu'], capture=True)

    txt_candidates = list(whisper_dir.glob('*.txt'))
    if not txt_candidates:
        raise RuntimeError('whisper did not produce a transcript txt file')
    txt_path = sorted(txt_candidates, key=lambda p: p.stat().st_size, reverse=True)[0]
    transcript_path = item_dir / 'transcript.txt'
    shutil.copy2(txt_path, transcript_path)
    return transcript_path, backend


def summarize_transcript(transcript_path: Path, length: str) -> str:
    proc = run([
        SUMMARIZE,
        str(transcript_path),
        '--plain',
        '--cli', 'codex',
        '--force-summary',
        '--length', length,
        '--timeout', '5m',
    ], capture=True)
    return proc.stdout.strip() + '\n'


def make_item_dir(kb_root: Path, title: str, platform: str, identifier: str) -> Path:
    date_part = dt.datetime.now().strftime('%Y-%m-%d')
    folder = f"{slugify(platform, 20)}-{slugify(identifier, 24)}-{slugify(title, 48)}"
    item_dir = kb_root / date_part / folder
    item_dir.mkdir(parents=True, exist_ok=True)
    return item_dir


def ingest_url(url: str, item_dir: Path, language: str | None) -> tuple[Path, str, dict[str, Any]]:
    raw_meta = load_yt_metadata(url)
    json_dump(item_dir / 'source.info.json', raw_meta)

    download_dir = item_dir / 'downloads'
    download_dir.mkdir(parents=True, exist_ok=True)
    template = str(download_dir / 'source.%(ext)s')

    # First try subtitles without downloading media.
    # Be tolerant here: some subtitle variants may 429/fail even when a usable subtitle
    # file has already been written. As long as at least one subtitle file lands, continue.
    subtitle_attempt = run([
        YTDLP,
        '--skip-download',
        '--write-subs',
        '--write-auto-subs',
        '--sub-langs', 'zh.*,en.*,-live_chat',
        '--convert-subs', 'srt',
        '--write-info-json',
        '-o', template,
        url,
    ], cwd=item_dir, capture=True, check=False)

    subtitle_candidates = sorted([p for p in download_dir.glob('source*.srt')] + [p for p in download_dir.glob('source*.vtt')])
    chosen_sub = choose_best_subtitle(subtitle_candidates)
    if chosen_sub and chosen_sub.stat().st_size > 0:
        transcript_text = strip_subtitle_to_text(chosen_sub)
        transcript_path = item_dir / 'transcript.txt'
        transcript_path.write_text(transcript_text, encoding='utf-8')
        return transcript_path, f'subtitles:{chosen_sub.name}', raw_meta

    # If subtitle download failed and nothing usable landed, fall back to media download.
    # We intentionally do not fail early on subtitle errors because partial subtitle success
    # is common on some platforms (e.g. one language variant 429s while another succeeds).
    _ = subtitle_attempt

    # Fallback: download media and transcribe.
    run([
        YTDLP,
        '-f', 'bestaudio/best',
        '--write-info-json',
        '-o', template,
        url,
    ], cwd=item_dir, capture=True)
    media_path = find_downloaded_media(download_dir)
    if not media_path:
        raise RuntimeError('yt-dlp finished but no media file was downloaded')
    transcript_path, backend = transcribe_media(media_path, item_dir, language)
    return transcript_path, backend, raw_meta


def ingest_local(path: Path, item_dir: Path, language: str | None) -> tuple[Path, str, dict[str, Any]]:
    meta = {
        'title': path.stem,
        'source_path': str(path),
        'platform': 'local',
        'id': hashlib.sha1(str(path).encode('utf-8')).hexdigest()[:12],
    }
    json_dump(item_dir / 'source.info.json', meta)

    suffix = path.suffix.lower()
    if suffix in SUB_EXTS:
        transcript_path = item_dir / 'transcript.txt'
        transcript_path.write_text(strip_subtitle_to_text(path), encoding='utf-8')
        return transcript_path, f'subtitles:{path.name}', meta
    if suffix in TEXT_EXTS:
        transcript_path = item_dir / 'transcript.txt'
        shutil.copy2(path, transcript_path)
        return transcript_path, f'text:{path.name}', meta
    if suffix in MEDIA_EXTS:
        transcript_path, backend = transcribe_media(path, item_dir, language)
        return transcript_path, backend, meta
    raise RuntimeError(f'unsupported local file type: {path.suffix}')


def append_index(index_path: Path, entry: dict[str, Any]) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def build_summary_markdown(title: str, source: str, platform: str, transcript_source: str, summary_text: str, transcript_rel: str) -> str:
    lines = [
        f'# {title}',
        '',
        f'- source: {source}',
        f'- platform: {platform}',
        f'- transcript_source: {transcript_source}',
        f'- transcript_file: {transcript_rel}',
        f'- generated_at: {dt.datetime.now().isoformat(timespec="seconds")}',
        '',
        '## Summary',
        '',
        summary_text.strip(),
        '',
    ]
    return '\n'.join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Ingest a video URL/local media into local knowledge base: download/subtitle/transcribe/summarize/save.')
    p.add_argument('source', help='Video URL or local file path')
    p.add_argument('--language', default='zh', help='Preferred transcription language (default: zh)')
    p.add_argument('--length', default='long', help='Summarize length preset (default: long)')
    p.add_argument('--kb-root', default=str(DEFAULT_KB_ROOT), help='Where to store local knowledge base entries')
    return p.parse_args()


def main() -> int:
    args = parse_args()
    source = normalize_source_url(args.source.strip())
    kb_root = Path(args.kb_root).expanduser().resolve()

    if is_url(source):
        meta = load_yt_metadata(source)
        platform = meta.get('extractor_key') or urlparse(source).netloc
        identifier = meta.get('id') or hashlib.sha1(source.encode('utf-8')).hexdigest()[:12]
        title = meta.get('title') or identifier
        item_dir = make_item_dir(kb_root, title, str(platform), str(identifier))
        (item_dir / 'source.url').write_text(source + '\n', encoding='utf-8')
        transcript_path, transcript_source, raw_meta = ingest_url(source, item_dir, args.language)
        title = raw_meta.get('title') or title
        platform = raw_meta.get('extractor_key') or platform
    else:
        src_path = Path(source).expanduser().resolve()
        if not src_path.exists():
            print(f'source not found: {src_path}', file=sys.stderr)
            return 2
        title = src_path.stem
        platform = 'local'
        identifier = hashlib.sha1(str(src_path).encode('utf-8')).hexdigest()[:12]
        item_dir = make_item_dir(kb_root, title, platform, identifier)
        (item_dir / 'source.path').write_text(str(src_path) + '\n', encoding='utf-8')
        transcript_path, transcript_source, raw_meta = ingest_local(src_path, item_dir, args.language)

    transcript_text = read_text(transcript_path)
    if not transcript_text.strip():
        raise RuntimeError('transcript is empty')

    summary_text = summarize_transcript(transcript_path, args.length)
    summary_path = item_dir / 'summary.md'
    summary_path.write_text(
        build_summary_markdown(title, source, str(platform), transcript_source, summary_text, 'transcript.txt'),
        encoding='utf-8',
    )

    entry = {
        'created_at': dt.datetime.now().isoformat(timespec='seconds'),
        'title': title,
        'platform': str(platform),
        'source': source,
        'item_dir': str(item_dir),
        'transcript_path': str(transcript_path),
        'transcript_source': transcript_source,
        'summary_path': str(summary_path),
    }
    json_dump(item_dir / 'record.json', entry)
    append_index(kb_root / 'index.jsonl', entry)

    print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
