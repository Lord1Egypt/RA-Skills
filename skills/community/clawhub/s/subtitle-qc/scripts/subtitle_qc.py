#!/usr/bin/env python3
"""Reading-speed QC for SRT and WebVTT subtitles.

Standard library only, Python 3.8+. Three commands:

  check  report reading speed (CPS), line length, duration and gap problems
  fix    timing-only repair: extend cues into the following pause, then merge
         short neighbours; never edits a word and never overwrites the input
  apply  write text edits (condensed cues) from a JSON file, then re-check

Thresholds follow the Netflix Timed Text Style Guides: 17 CPS / 42 chars per
line for Latin scripts (the children's ceiling; adult is 20), 9 CPS / 16 chars
for Chinese, Japanese and Korean, 2 lines, 5/6 s to 7 s on screen, and an
80 ms (about 2 frames) gap between cues.

Method: https://scribetoany.com/blog/subtitle-reading-speed-cps
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

SITE = 'https://scribetoany.com'
METHOD_URL = SITE + '/blog/subtitle-reading-speed-cps'

# ---------------------------------------------------------------------------
# Thresholds


@dataclass
class Thresholds:
    family: str
    cps: float
    max_chars: int
    max_lines: int = 2
    min_dur_ms: int = 833
    max_dur_ms: int = 7000
    min_gap_ms: int = 80

    def describe(self) -> str:
        return (
            f'{self.family} · {fmt_num(self.cps)} CPS · '
            f'{self.max_chars} chars/line · {self.max_lines} lines · '
            f'{self.min_dur_ms / 1000:.2f}–{self.max_dur_ms / 1000:g} s · '
            f'gap ≥ {self.min_gap_ms} ms'
        )


PRESETS: Dict[str, Tuple[str, float, int]] = {
    # name: (family, cps, max chars per line)
    'latin': ('Latin', 17, 42),
    'netflix-adult': ('Latin', 20, 42),
    'cjk': ('CJK', 9, 16),
    'netflix-ja': ('Japanese', 4, 13),
}

# Kana, CJK ideographs (+ Ext A), compatibility ideographs, Hangul syllables.
CJK_RE = re.compile('[぀-ヿ㐀-䶿一-鿿豈-﫿가-힯]')


def is_cjk_text(sample: str) -> bool:
    cjk = len(CJK_RE.findall(sample))
    non_space = len(re.sub(r'\s', '', sample))
    return non_space > 0 and cjk / non_space >= 0.2


# ---------------------------------------------------------------------------
# Cues and text measurement

TAG_RE = re.compile(r'<[^>]*>|\{\\[^}]*\}')
SPEAKER_RE = re.compile(r'^\s*(?:[-–—]\s|>>|\[[^\]]{1,30}\]\s*:?|[A-Z][\w .\'-]{0,24}:\s)')
END_PUNCT_RE = re.compile(r'[.!?…,;:。！？，；：、]["\'”’」』)）]*\s*$')
SENTENCE_END_RE = re.compile(r'[.!?…。！？]["\'”’」』)）]*\s*$')


def visible(text: str) -> str:
    """The text the eye reads: formatting tags removed."""
    return TAG_RE.sub('', text)


def count_chars(lines: List[str]) -> int:
    """Characters that count toward reading speed: everything visible except
    the line breaks between rows (spaces and punctuation included)."""
    return sum(len(visible(line)) for line in lines)


@dataclass
class Cue:
    start: int
    end: int
    lines: List[str]
    settings: str = ''
    ident: str = ''
    sources: List[int] = field(default_factory=list)

    @property
    def dur(self) -> int:
        return self.end - self.start

    @property
    def chars(self) -> int:
        return count_chars(self.lines)

    @property
    def text(self) -> str:
        return '\n'.join(self.lines)

    def cps(self) -> float:
        if self.dur <= 0:
            return 0.0
        return self.chars / (self.dur / 1000)


# ---------------------------------------------------------------------------
# Parsing

TIME = r'(?:(\d+):)?(\d{1,2}):(\d{2})[,.](\d{1,3})'
TIMING_RE = re.compile(r'^\s*' + TIME + r'\s*-{1,2}>\s*' + TIME + r'(.*)$')


def to_ms(h: Optional[str], m: str, s: str, frac: str) -> int:
    ms = int(frac.ljust(3, '0')[:3])
    return ((int(h or 0) * 60 + int(m)) * 60 + int(s)) * 1000 + ms


@dataclass
class SubFile:
    path: str
    fmt: str  # 'srt' | 'vtt'
    cues: List[Cue]
    header: List[str]
    crlf: bool
    bom: bool
    encoding: str
    warnings: List[str]


def read_text(path: str) -> Tuple[str, str, bool]:
    with open(path, 'rb') as f:
        raw = f.read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    try:
        return raw.decode('utf-8-sig'), 'utf-8', bom
    except UnicodeDecodeError:
        return raw.decode('cp1252', errors='replace'), 'cp1252', False


def parse(path: str) -> SubFile:
    text, encoding, bom = read_text(path)
    crlf = '\r\n' in text
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    first = next((ln.strip() for ln in lines if ln.strip()), '')
    is_vtt = first.startswith('WEBVTT') or path.lower().endswith('.vtt')
    warnings: List[str] = []
    if encoding != 'utf-8':
        warnings.append(
            'File is not UTF-8; read it as Windows-1252. Output is written as UTF-8.'
        )

    timing_rows = [i for i, ln in enumerate(lines) if TIMING_RE.match(ln)]
    cues: List[Cue] = []
    header: List[str] = []
    for n, i in enumerate(timing_rows):
        m = TIMING_RE.match(lines[i])
        assert m
        g = m.groups()
        start = to_ms(g[0], g[1], g[2], g[3])
        end = to_ms(g[4], g[5], g[6], g[7])
        settings = g[8].strip()

        # Identifier: the non-blank line directly above the timing line,
        # unless that line belongs to the previous cue's text.
        ident = ''
        if i > 0 and lines[i - 1].strip():
            ident = lines[i - 1].strip()

        stop = timing_rows[n + 1] if n + 1 < len(timing_rows) else len(lines)
        body: List[str] = []
        for ln in lines[i + 1 : stop]:
            if not ln.strip():
                break
            body.append(ln.rstrip())
        # A cue number with no blank line before it lands at the end of the
        # previous body ("text\n2\n00:00..."): drop it from the text.
        if (
            n + 1 < len(timing_rows)
            and body
            and i + 1 + len(body) == timing_rows[n + 1]
            and body[-1].strip().isdigit()
        ):
            body.pop()
        if not is_vtt and ident.isdigit():
            ident = ''
        cues.append(Cue(start, end, body, settings, ident, [n + 1]))

    if is_vtt:
        first_row = timing_rows[0] if timing_rows else len(lines)
        cut = first_row - 1 if cues and cues[0].ident else first_row
        header = [ln for ln in lines[:cut]]
        while header and not header[-1].strip():
            header.pop()
        if not header:
            header = ['WEBVTT']
        if any(ln.startswith('NOTE') for ln in lines[first_row:]):
            warnings.append('NOTE blocks between cues are not kept in output files.')

    if not cues:
        warnings.append('No cues found. Is this an SRT or WebVTT file?')
    return SubFile(path, 'vtt' if is_vtt else 'srt', cues, header, crlf, bom, encoding, warnings)


# ---------------------------------------------------------------------------
# Writing


def fmt_time(ms: int, vtt: bool) -> str:
    ms = max(ms, 0)
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, rem = divmod(rem, 1000)
    sep = '.' if vtt else ','
    return f'{h:02d}:{m:02d}:{s:02d}{sep}{rem:03d}'


def serialize(sub: SubFile, cues: List[Cue]) -> str:
    vtt = sub.fmt == 'vtt'
    out: List[str] = []
    if vtt:
        out.extend(sub.header)
        out.append('')
    for n, c in enumerate(cues, 1):
        if vtt:
            if c.ident:
                out.append(c.ident)
        else:
            out.append(str(n))
        timing = f'{fmt_time(c.start, vtt)} --> {fmt_time(c.end, vtt)}'
        if c.settings:
            timing += ' ' + c.settings
        out.append(timing)
        out.extend(c.lines)
        out.append('')
    body = '\n'.join(out)
    if sub.crlf:
        body = body.replace('\n', '\r\n')
    return body


def write_output(sub: SubFile, cues: List[Cue], out_path: str) -> None:
    if os.path.abspath(out_path) == os.path.abspath(sub.path):
        die('Refusing to overwrite the input file. Pass a different -o path.')
    data = serialize(sub, cues)
    try:
        with open(out_path, 'w', encoding='utf-8-sig' if sub.bom else 'utf-8', newline='') as f:
            f.write(data)
    except OSError as e:
        die(f'cannot write {out_path}: {e.strerror}')


# ---------------------------------------------------------------------------
# Analysis


def gap_before(cues: List[Cue], i: int) -> Optional[int]:
    return None if i == 0 else cues[i].start - cues[i - 1].end


def hard_problems(cues: List[Cue]) -> List[Dict]:
    out = []
    for i, c in enumerate(cues):
        if c.dur <= 0:
            out.append({'cue': i + 1, 'problem': 'end time is not after start time'})
        if i > 0 and c.start < cues[i - 1].start:
            out.append({'cue': i + 1, 'problem': f'starts before cue {i} (out of order)'})
        elif i > 0 and c.start < cues[i - 1].end:
            out.append({
                'cue': i + 1,
                'problem': f'overlaps cue {i} by {cues[i - 1].end - c.start} ms',
            })
    return out


def cue_report(cues: List[Cue], i: int, th: Thresholds) -> Dict:
    c = cues[i]
    cps = c.cps()
    gap = gap_before(cues, i)
    lines = [len(visible(ln)) for ln in c.lines]
    budget = math.floor(th.cps * c.dur / 1000) if c.dur > 0 else 0
    issues = []
    if cps > th.cps:
        issues.append('cps')
    if c.dur < th.min_dur_ms:
        issues.append('short')
    if c.dur > th.max_dur_ms:
        issues.append('long')
    if any(n > th.max_chars for n in lines):
        issues.append('line_length')
    if len(c.lines) > th.max_lines:
        issues.append('too_many_lines')
    if gap is not None and 0 <= gap < th.min_gap_ms:
        issues.append('tight_gap')
    return {
        'cue': i + 1,
        'start': fmt_time(c.start, False),
        'end': fmt_time(c.end, False),
        'duration_s': round(c.dur / 1000, 3),
        'chars': c.chars,
        'cps': round(cps, 1),
        'line_lengths': lines,
        'gap_before_ms': gap,
        'chars_to_cut': max(c.chars - budget, 0) if cps > th.cps else 0,
        'issues': issues,
        'text': c.text,
    }


def summarize(cues: List[Cue], th: Thresholds) -> Dict:
    reports = [cue_report(cues, i, th) for i in range(len(cues))]
    valid = [r for r in reports if r['duration_s'] > 0]
    n = len(cues)

    def count(issue: str) -> int:
        return sum(1 for r in reports if issue in r['issues'])

    total_chars = sum(r['chars'] for r in reports)
    to_cut = sum(r['chars_to_cut'] for r in reports)
    return {
        'cues': n,
        'thresholds': th.__dict__,
        'median_cps': round(statistics.median(r['cps'] for r in valid), 1) if valid else 0,
        'over_cps': count('cps'),
        'near_cps': sum(1 for r in reports if 'cps' not in r['issues'] and r['cps'] >= th.cps * 0.85),
        'short': count('short'),
        'long': count('long'),
        'line_length': count('line_length'),
        'too_many_lines': count('too_many_lines'),
        'tight_gap': count('tight_gap'),
        'total_chars': total_chars,
        'chars_to_cut': to_cut,
        'hard_problems': hard_problems(cues),
        'cue_reports': reports,
    }


def pick_thresholds(cues: List[Cue], args: argparse.Namespace) -> Thresholds:
    if args.preset:
        fam, cps, chars = PRESETS[args.preset]
    else:
        sample = ' '.join(visible(c.text) for c in cues[:400])
        fam, cps, chars = PRESETS['cjk' if is_cjk_text(sample) else 'latin']
    th = Thresholds(fam, cps, chars)
    if args.cps:
        th.cps = args.cps
    if args.max_chars:
        th.max_chars = args.max_chars
    if args.max_lines:
        th.max_lines = args.max_lines
    if args.min_duration:
        th.min_dur_ms = int(args.min_duration * 1000)
    if args.max_duration:
        th.max_dur_ms = int(args.max_duration * 1000)
    if args.min_gap is not None:
        th.min_gap_ms = args.min_gap
    return th


# ---------------------------------------------------------------------------
# Timing repair (never touches words)


def needed_ms(c: Cue, th: Thresholds) -> int:
    return max(math.ceil(c.chars / th.cps * 1000), th.min_dur_ms)


def severity(c: Cue, th: Thresholds) -> float:
    """How far a cue is from passing: 1.0 or below passes on both reading
    speed and minimum duration."""
    if c.dur <= 0:
        return math.inf
    return max(c.cps() / th.cps, th.min_dur_ms / c.dur)


def failing(c: Cue, th: Thresholds) -> bool:
    return c.dur > 0 and (c.cps() > th.cps or c.dur < th.min_dur_ms)


def extend_pass(cues: List[Cue], th: Thresholds, bad: set, log: List[Dict]) -> int:
    """Move a failing cue's end into the silence after it, only as far as it
    needs, keeping the minimum gap and the maximum duration."""
    changed = 0
    for i, c in enumerate(cues):
        if i in bad or not failing(c, th):
            continue
        limit = c.start + th.max_dur_ms
        if i + 1 < len(cues):
            limit = min(limit, cues[i + 1].start - th.min_gap_ms)
        new_end = min(c.start + needed_ms(c, th), limit)
        if new_end > c.end:
            log.append({
                'action': 'extend',
                'cues': c.sources,
                'end': f'{fmt_time(c.end, False)} -> {fmt_time(new_end, False)}',
                'cps': f'{c.cps():.1f} -> {c.chars / ((new_end - c.start) / 1000):.1f}',
            })
            c.end = new_end
            changed += 1
    return changed


def close_gaps_pass(cues: List[Cue], th: Thresholds, bad: set, log: List[Dict]) -> int:
    """Pull back the end of a cue that touches the next one, so the viewer sees
    the change, but only when the cue still passes after the trim."""
    changed = 0
    for i in range(len(cues) - 1):
        c, nxt = cues[i], cues[i + 1]
        if i in bad or (i + 1) in bad:
            continue
        gap = nxt.start - c.end
        if 0 <= gap < th.min_gap_ms:
            new_end = nxt.start - th.min_gap_ms
            trial = Cue(c.start, new_end, c.lines)
            if trial.dur >= th.min_dur_ms and trial.cps() <= th.cps:
                log.append({
                    'action': 'gap',
                    'cues': c.sources,
                    'end': f'{fmt_time(c.end, False)} -> {fmt_time(new_end, False)}',
                })
                c.end = new_end
                changed += 1
    return changed


ARTICLE_WORDS = {
    'a', 'an', 'the', 'of', 'to', 'in', 'on', 'at', 'for', 'with', 'from',
    'by', 'and', 'or', 'but', 'my', 'your', 'our', 'their', 'his', 'her', 'its',
}


def break_lines(text: str, th: Thresholds, cjk: bool) -> List[str]:
    """One line if it fits; otherwise the best two-line break: after
    punctuation, never after an article or preposition, bottom-heavy."""
    if len(visible(text)) <= th.max_chars:
        return [text]
    best: Optional[Tuple[float, List[str]]] = None
    positions = range(1, len(text)) if cjk else [m.start() for m in re.finditer(' ', text)]
    for p in positions:
        a = text[:p].rstrip()
        b = text[p:].lstrip()
        if not a or not b:
            continue
        la, lb = len(visible(a)), len(visible(b))
        score = abs(la - lb)
        if la > th.max_chars or lb > th.max_chars:
            score += 1000
        if re.search(r'[,.;:!?…，。；：！？、]$', a):
            score -= 12
        if not cjk and a.split()[-1].lower() in ARTICLE_WORDS:
            score += 25
        if la > lb:
            score += 3
        if best is None or score < best[0]:
            best = (score, [a, b])
    return best[1] if best else [text]


def try_merge(cues: List[Cue], i: int, j: int, th: Thresholds, cjk: bool) -> Optional[Cue]:
    """Merge cues i and j (j == i + 1) when the result stays within the line
    and duration limits, ends at punctuation, and no speaker change."""
    a, b = cues[i], cues[j]
    if b.start - a.end > 1000:
        return None
    if SPEAKER_RE.match(visible(b.text)) or SPEAKER_RE.match(visible(a.text)):
        return None
    if not END_PUNCT_RE.search(visible(b.text)):
        return None
    if a.settings != b.settings:
        return None
    joiner = '' if cjk else ' '
    joined = joiner.join(ln.strip() for ln in a.lines + b.lines)
    lines = break_lines(joined, th, cjk)
    merged = Cue(a.start, b.end, lines, a.settings, a.ident or b.ident, a.sources + b.sources)
    if len(lines) > th.max_lines or any(len(visible(ln)) > th.max_chars for ln in lines):
        return None
    if merged.dur > th.max_dur_ms:
        return None
    return merged


def merge_pass(cues: List[Cue], th: Thresholds, cjk: bool, log: List[Dict]) -> List[Cue]:
    bad = {p['cue'] - 1 for p in hard_problems(cues)}
    out: List[Cue] = []
    i = 0
    while i < len(cues):
        c = cues[i]
        merged = None
        if i not in bad and failing(c, th):
            # Prefer joining the next cue; fall back to the previous one when
            # this cue closes a sentence the previous one started.
            if i + 1 < len(cues) and (i + 1) not in bad:
                cand = try_merge(cues, i, i + 1, th, cjk)
                if cand and severity(cand, th) < severity(c, th):
                    merged = cand
                    i += 2
            if not merged and out and (i - 1) not in bad:
                cand = try_merge([out[-1], c], 0, 1, th, cjk)
                if cand and severity(cand, th) < severity(c, th):
                    out.pop()
                    merged = cand
                    i += 1
        if merged:
            log.append({
                'action': 'merge',
                'cues': merged.sources,
                'cps': f'{merged.cps():.1f}',
                'text': merged.text,
            })
            out.append(merged)
        else:
            out.append(c)
            i += 1
    return out


def lines_pass(cues: List[Cue], th: Thresholds, cjk: bool, bad: set, log: List[Dict]) -> int:
    """Re-break cues whose lines run over the limit, when the same words fit
    in the allowed number of lines. Cues that cannot fit stay as they are."""
    changed = 0
    for i, c in enumerate(cues):
        if i in bad:
            continue
        lens = [len(visible(ln)) for ln in c.lines]
        if all(n <= th.max_chars for n in lens) and len(c.lines) <= th.max_lines:
            continue
        joined = ('' if cjk else ' ').join(ln.strip() for ln in c.lines)
        lines = break_lines(joined, th, cjk)
        if len(lines) <= th.max_lines and all(len(visible(ln)) <= th.max_chars for ln in lines):
            if lines != c.lines:
                log.append({'action': 'lines', 'cues': c.sources, 'text': '\n'.join(lines)})
                c.lines = lines
                changed += 1
    return changed


def fix(cues: List[Cue], th: Thresholds, steps: List[str]) -> Tuple[List[Cue], List[Dict]]:
    cues = [Cue(c.start, c.end, list(c.lines), c.settings, c.ident, list(c.sources)) for c in cues]
    cjk = th.family in ('CJK', 'Japanese')
    log: List[Dict] = []
    bad = {p['cue'] - 1 for p in hard_problems(cues)}
    if 'extend' in steps:
        extend_pass(cues, th, bad, log)
    if 'merge' in steps:
        cues = merge_pass(cues, th, cjk, log)
        bad = {p['cue'] - 1 for p in hard_problems(cues)}
        if 'extend' in steps:
            extend_pass(cues, th, bad, log)
    if 'gaps' in steps:
        bad = {p['cue'] - 1 for p in hard_problems(cues)}
        close_gaps_pass(cues, th, bad, log)
    if 'lines' in steps:
        bad = {p['cue'] - 1 for p in hard_problems(cues)}
        lines_pass(cues, th, cjk, bad, log)
    return cues, log


# ---------------------------------------------------------------------------
# Output


def fmt_num(x: float) -> str:
    return f'{x:g}'


def pct(n: int, total: int) -> str:
    return f'{round(100 * n / total)}%' if total else '–'


def print_summary(path: str, s: Dict, th: Thresholds, worst: int, warnings: List[str]) -> None:
    n = s['cues']
    print(f'subtitle-qc · {os.path.basename(path)} · {n} cues')
    print(f'Thresholds: {th.describe()}')
    for w in warnings:
        print(f'Note: {w}')
    print()
    rows = [
        (f'Over {fmt_num(th.cps)} CPS', s['over_cps']),
        (f'Near the limit (≥ {th.cps * 0.85:.1f} CPS)', s['near_cps']),
        (f'Shorter than {th.min_dur_ms / 1000:.2f} s', s['short']),
        (f'Longer than {th.max_dur_ms / 1000:g} s', s['long']),
        (f'Lines over {th.max_chars} chars', s['line_length']),
        (f'More than {th.max_lines} lines', s['too_many_lines']),
        (f'Gap under {th.min_gap_ms} ms', s['tight_gap']),
    ]
    print(f'  {"Check":<34}{"Cues":>6}{"Share":>8}')
    for label, v in rows:
        print(f'  {label:<34}{v:>6}{pct(v, n):>8}')
    print(f'  {"Median CPS":<34}{s["median_cps"]:>6}')
    print()
    if s['hard_problems']:
        print('Fix these by hand first (fix leaves them untouched):')
        for p in s['hard_problems']:
            print(f'  cue {p["cue"]}: {p["problem"]}')
        print()
    if s['over_cps']:
        print(
            f'Characters to cut to reach {fmt_num(th.cps)} CPS at the current timing: '
            f'{s["chars_to_cut"]:,} of {s["total_chars"]:,} '
            f'({100 * s["chars_to_cut"] / max(s["total_chars"], 1):.1f}%)'
        )
        print()
    if worst:
        bad = [r for r in s['cue_reports'] if r['issues'] and r['issues'] != ['tight_gap']]
        bad.sort(key=lambda r: (-('cps' in r['issues']), -r['cps']))
        if bad:
            print(f'Worst cues (up to {worst}):')
            for r in bad[:worst]:
                text = r['text'].replace('\n', ' / ')
                if len(text) > 60:
                    text = text[:57] + '...'
                print(
                    f'  #{r["cue"]:<5}{r["start"]}  {r["duration_s"]:>5.2f} s  '
                    f'{r["cps"]:>5.1f} CPS  {",".join(r["issues"]):<22} "{text}"'
                )
            print()
    print(f'Method and sources: {METHOD_URL}')


def die(msg: str) -> None:
    print(f'error: {msg}', file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Commands


def cmd_check(args: argparse.Namespace) -> int:
    sub = parse(args.file)
    th = pick_thresholds(sub.cues, args)
    s = summarize(sub.cues, th)
    if args.json:
        s['file'] = args.file
        s['warnings'] = sub.warnings
        if not args.all_cues:
            s['cue_reports'] = [r for r in s['cue_reports'] if r['issues']]
        print(json.dumps(s, ensure_ascii=False, indent=2))
    else:
        print_summary(args.file, s, th, args.worst, sub.warnings)
    return 1 if (s['over_cps'] or s['hard_problems']) and args.strict else 0


TODO_ISSUES = {'cps', 'short', 'line_length', 'too_many_lines'}


def parse_time(value: str) -> int:
    m = re.match('^' + TIME + '$', value.strip())
    if not m:
        die(f'bad time {value!r}; use HH:MM:SS,mmm')
    g = m.groups()
    return to_ms(g[0], g[1], g[2], g[3])


def cmd_fix(args: argparse.Namespace) -> int:
    sub = parse(args.file)
    th = pick_thresholds(sub.cues, args)
    steps = [x.strip() for x in args.steps.split(',') if x.strip()]
    unknown = set(steps) - {'extend', 'merge', 'gaps', 'lines'}
    if unknown:
        die(f'unknown step(s): {", ".join(sorted(unknown))}')
    before = summarize(sub.cues, th)
    cues, log = fix(sub.cues, th, steps)
    after = summarize(cues, th)
    write_output(sub, cues, args.output)
    if args.log:
        with open(args.log, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

    def row(label: str, key: str) -> None:
        print(f'  {label:<30}{before[key]:>8}{after[key]:>8}')

    print(f'subtitle-qc fix · {os.path.basename(args.file)} -> {args.output}')
    print(f'Thresholds: {th.describe()} · steps: {", ".join(steps)}')
    print('Words were not changed: only start/end times, cue grouping and line breaks.')
    print()
    print(f'  {"":<30}{"Before":>8}{"After":>8}')
    row('Cues', 'cues')
    row('Median CPS', 'median_cps')
    row(f'Over {fmt_num(th.cps)} CPS', 'over_cps')
    row(f'Shorter than {th.min_dur_ms / 1000:.2f} s', 'short')
    row(f'Lines over {th.max_chars} chars', 'line_length')
    row(f'Gap under {th.min_gap_ms} ms', 'tight_gap')
    row('Chars to cut to pass', 'chars_to_cut')
    print()
    counts: Dict[str, int] = {}
    for e in log:
        counts[e['action']] = counts.get(e['action'], 0) + 1
    print(
        f'Changes: {counts.get("extend", 0)} end times extended, '
        f'{counts.get("merge", 0)} merges, {counts.get("gap", 0)} gaps opened, '
        f'{counts.get("lines", 0)} cues re-broken'
        + (f' (details in {args.log})' if args.log else '')
    )
    if after['hard_problems']:
        print(f'{len(after["hard_problems"])} hard problem(s) left untouched; run check to list them.')
    if args.todo:
        todo = [
            {'cue': r['cue'], 'start': r['start'], 'end': r['end'],
             'issues': [x for x in r['issues'] if x in TODO_ISSUES],
             'cps': r['cps'], 'duration_s': r['duration_s'], 'chars': r['chars'],
             'chars_to_cut': r['chars_to_cut'], 'line_lengths': r['line_lengths'],
             'text': r['text']}
            for r in after['cue_reports'] if set(r['issues']) & TODO_ISSUES
        ]
        with open(args.todo, 'w', encoding='utf-8') as f:
            json.dump({'file': args.output, 'target_cps': th.cps, 'cues': todo},
                      f, ensure_ascii=False, indent=2)
        print(f'{len(todo)} cue(s) that need a person or a text edit listed in {args.todo}.')
    print(f'Method and sources: {METHOD_URL}')
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    sub = parse(args.file)
    th = pick_thresholds(sub.cues, args)
    with open(args.edits, encoding='utf-8') as f:
        data = json.load(f)
    edits = data['cues'] if isinstance(data, dict) else data
    cues = [Cue(c.start, c.end, list(c.lines), c.settings, c.ident, list(c.sources)) for c in sub.cues]
    replaced: Dict[int, List[Cue]] = {}
    for e in edits:
        n = int(e['cue'])
        if not 1 <= n <= len(cues):
            die(f'cue {n} does not exist (file has {len(cues)} cues)')
        c = cues[n - 1]
        if 'split' in e:
            # One cue becomes several inside the same span. Every part but the
            # last gives its end time; the next part starts min_gap later.
            parts = e['split']
            if len(parts) < 2:
                die(f'cue {n}: a split needs at least two parts')
            if all('end' in part for part in parts[:-1]):
                ends = [parse_time(part['end']) for part in parts[:-1]]
            else:
                # No times given: share the span by character count.
                sizes = [max(count_chars(str(part['text']).split('\n')), 1) for part in parts]
                usable = c.dur - th.min_gap_ms * (len(parts) - 1)
                ends, t = [], c.start
                for k, size in enumerate(sizes[:-1]):
                    t += round(usable * size / sum(sizes))
                    ends.append(t)
                    t += th.min_gap_ms
            start, out = c.start, []
            for k, part in enumerate(parts):
                last = k == len(parts) - 1
                end = c.end if last else ends[k]
                if not start < end <= c.end:
                    die(f'cue {n} split part {k + 1}: end must be after its start and inside the cue')
                out.append(Cue(start, end, str(part['text']).split('\n'), c.settings,
                               c.ident if k == 0 else '', list(c.sources)))
                start = end + th.min_gap_ms
            replaced[n - 1] = out
        else:
            if 'text' in e:
                c.lines = str(e['text']).split('\n')
            if 'start' in e:
                c.start = parse_time(e['start'])
            if 'end' in e:
                c.end = parse_time(e['end'])
    if replaced:
        cues = [p for i, c in enumerate(cues) for p in replaced.get(i, [c])]
    before = summarize(sub.cues, th)
    after = summarize(cues, th)
    write_output(sub, cues, args.output)
    print(f'subtitle-qc apply · {len(edits)} edit(s) -> {args.output}')
    print(f'  Over {fmt_num(th.cps)} CPS: {before["over_cps"]} -> {after["over_cps"]}')
    print(f'  Lines over {th.max_chars} chars: {before["line_length"]} -> {after["line_length"]}')
    still = [r['cue'] for r in after['cue_reports'] if 'cps' in r['issues']]
    if still:
        print(f'  Still over: cues {", ".join(map(str, still[:30]))}')
    return 0


def add_threshold_args(p: argparse.ArgumentParser) -> None:
    p.add_argument('--preset', choices=sorted(PRESETS), help='threshold set (default: auto by script)')
    p.add_argument('--cps', type=float, help='reading-speed ceiling, characters per second')
    p.add_argument('--max-chars', type=int, help='characters per line')
    p.add_argument('--max-lines', type=int, help='lines per cue')
    p.add_argument('--min-duration', type=float, help='seconds (default 0.833)')
    p.add_argument('--max-duration', type=float, help='seconds (default 7)')
    p.add_argument('--min-gap', type=int, help='milliseconds between cues (default 80)')


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog='subtitle_qc.py', description=__doc__.split('\n\n')[0])
    sp = ap.add_subparsers(dest='cmd', required=True)

    p = sp.add_parser('check', help='report reading-speed and layout problems')
    p.add_argument('file')
    add_threshold_args(p)
    p.add_argument('--json', action='store_true', help='machine-readable output')
    p.add_argument('--all-cues', action='store_true', help='with --json, include passing cues')
    p.add_argument('--worst', type=int, default=10, help='how many problem cues to list')
    p.add_argument('--strict', action='store_true', help='exit 1 when any cue is over the CPS limit')
    p.set_defaults(func=cmd_check)

    p = sp.add_parser('fix', help='timing-only repair into a new file')
    p.add_argument('file')
    p.add_argument('-o', '--output', required=True)
    add_threshold_args(p)
    p.add_argument('--steps', default='extend,merge,gaps,lines', help='comma list of extend,merge,gaps,lines')
    p.add_argument('--log', help='write a JSON list of every change')
    p.add_argument('--todo', help='write cues still over the limit to this JSON file')
    p.set_defaults(func=cmd_fix)

    p = sp.add_parser('apply', help='apply text edits from JSON into a new file')
    p.add_argument('file')
    p.add_argument('edits', help='JSON file of edits; see references/apply-format.md')
    p.add_argument('-o', '--output', required=True)
    add_threshold_args(p)
    p.set_defaults(func=cmd_apply)

    args = ap.parse_args(argv)
    if not os.path.isfile(args.file):
        die(f'file not found: {args.file}')
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
