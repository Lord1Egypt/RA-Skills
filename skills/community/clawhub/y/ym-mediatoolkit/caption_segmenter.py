import json
import re
from pathlib import Path

from subtitle_extractor import clean_captions, normalize_caption
from utils import prepare_output_path


STRONG_PUNCTUATION = set('。！？!?')
WEAK_PUNCTUATION = set('，、；：,;:')
CONNECTORS = ('然后', '但是', '所以', '因为', '就是', '这个', '那个', '以及', '并且')


def _safe_read_json(path: str):
    p = Path(path)
    if any(part == '..' for part in p.parts):
        raise ValueError(f"禁止路径穿越 (..): {path}")
    resolved = p.resolve()
    try:
        resolved.relative_to(Path('.').resolve())
    except ValueError:
        raise ValueError(f"配置文件路径超出工作目录: {path}")
    if not resolved.exists():
        raise ValueError(f"配置文件不存在: {path}")
    return json.loads(resolved.read_text(encoding='utf-8'))


def _flatten_terms(value) -> list:
    if not value:
        return []
    if isinstance(value, str):
        return [item.strip() for item in re.split(r'[,\n;；，、]+', value) if item.strip()]
    if isinstance(value, dict):
        terms = []
        for item in value.values():
            terms.extend(_flatten_terms(item))
        return terms
    if isinstance(value, (list, tuple, set)):
        terms = []
        for item in value:
            terms.extend(_flatten_terms(item))
        return terms
    return [str(value).strip()]


def load_protected_terms(protected_terms=None, protected_terms_path: str = None) -> list:
    terms = _flatten_terms(protected_terms)
    if protected_terms_path:
        terms.extend(_flatten_terms(_safe_read_json(protected_terms_path)))

    normalized = []
    seen = set()
    for term in terms:
        term = term.strip()
        if not term or term in seen:
            continue
        normalized.append(term)
        seen.add(term)
    return sorted(normalized, key=len, reverse=True)


def _protected_spans(text: str, protected_terms: list, auto_protect_ascii: bool = True) -> list:
    spans = []
    for term in protected_terms or []:
        start = 0
        while True:
            index = text.find(term, start)
            if index < 0:
                break
            spans.append((index, index + len(term)))
            start = index + len(term)

    if auto_protect_ascii:
        for match in re.finditer(r'[A-Za-z0-9][A-Za-z0-9._:/\\+\-]*[A-Za-z0-9]?', text):
            if len(match.group(0)) >= 2:
                spans.append(match.span())

    spans = sorted(spans)
    merged = []
    for start, end in spans:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return [(start, end) for start, end in merged]


def _is_valid_cut(cut: int, spans: list) -> bool:
    return all(not (start < cut < end) for start, end in spans)


def _cut_after_punctuation(text: str, start: int, target: int, spans: list, punctuation: set):
    for index in range(target - 1, start, -1):
        cut = index + 1
        if text[index] in punctuation and _is_valid_cut(cut, spans):
            return cut
    return None


def _cut_before_connector(text: str, start: int, target: int, spans: list):
    window = text[start:target]
    best = None
    for connector in CONNECTORS:
        offset = window.rfind(connector)
        if offset <= 0:
            continue
        cut = start + offset
        if _is_valid_cut(cut, spans):
            best = max(best or cut, cut)
    return best


def _adjust_cut_around_protected_term(start: int, target: int, text_len: int, spans: list) -> int:
    if _is_valid_cut(target, spans):
        return target
    for span_start, span_end in spans:
        if span_start < target < span_end:
            if span_start > start:
                return span_start
            return min(span_end, text_len)
    return target


def split_caption_text(
    text: str,
    max_chars: int = 12,
    protected_terms=None,
    auto_protect_ascii: bool = True,
) -> list:
    text = str(text or '').strip()
    if not text:
        return []
    max_chars = max(1, int(max_chars or 12))
    if len(text) <= max_chars:
        return [text]

    spans = _protected_spans(text, protected_terms or [], auto_protect_ascii=auto_protect_ascii)
    segments = []
    start = 0
    text_len = len(text)

    while start < text_len:
        if text_len - start <= max_chars:
            segments.append(text[start:].strip())
            break

        target = min(text_len, start + max_chars)
        cut = (
            _cut_after_punctuation(text, start, target, spans, STRONG_PUNCTUATION)
            or _cut_after_punctuation(text, start, target, spans, WEAK_PUNCTUATION)
            or _cut_before_connector(text, start, target, spans)
            or _adjust_cut_around_protected_term(start, target, text_len, spans)
        )

        while cut > start and not _is_valid_cut(cut, spans):
            cut -= 1
        if cut <= start:
            cut = _adjust_cut_around_protected_term(start, target, text_len, spans)
            while cut < text_len and not _is_valid_cut(cut, spans):
                cut += 1
        if cut <= start:
            cut = min(text_len, start + max_chars)

        segment = text[start:cut].strip()
        if segment:
            segments.append(segment)
        start = cut
        while start < text_len and text[start].isspace():
            start += 1

    return [segment for segment in segments if segment]


def _allocate_caption_time(caption: dict, segments: list) -> list:
    if not segments:
        return []

    start_us = int(caption['startTimeUs'])
    end_us = int(caption['endTimeUs'])
    duration = max(1, end_us - start_us)
    weights = [max(1, len(segment)) for segment in segments]
    total_weight = sum(weights)

    output = []
    current = start_us
    for index, segment in enumerate(segments):
        if index == len(segments) - 1:
            segment_end = end_us
        else:
            segment_duration = max(1, round(duration * weights[index] / total_weight))
            segment_end = min(end_us, current + segment_duration)
        if segment_end <= current:
            segment_end = current + 1
        output.append({
            'captionTxt': segment,
            'startTimeUs': current,
            'endTimeUs': segment_end,
            'source': caption.get('source') or 'segment',
            'confidence': caption.get('confidence', 0),
        })
        current = segment_end
    return output


def segment_captions(
    captions: list,
    max_chars: int = 12,
    protected_terms=None,
    auto_protect_ascii: bool = True,
) -> list:
    terms = load_protected_terms(protected_terms)
    segmented = []
    for raw in clean_captions(captions):
        caption = normalize_caption(raw)
        parts = split_caption_text(
            caption['captionTxt'],
            max_chars=max_chars,
            protected_terms=terms,
            auto_protect_ascii=auto_protect_ascii,
        )
        segmented.extend(_allocate_caption_time(caption, parts))
    return clean_captions(segmented)


def _default_segmented_name(caption_path: str = None, source: str = None) -> str:
    raw_name = Path(caption_path or source or 'captions').stem
    if raw_name.endswith('.captions'):
        raw_name = raw_name[:-len('.captions')]
    if raw_name.endswith('.segmented'):
        return raw_name
    return f'{raw_name}.segmented'


def load_captions_payload(caption_path: str) -> dict:
    data = _safe_read_json(caption_path)
    if isinstance(data, list):
        return {'captions': data}
    if isinstance(data, dict):
        return data
    raise ValueError('字幕 JSON 必须是对象或 captions 数组')


def write_segmented_captions_json(
    captions: list,
    output_path: str = None,
    caption_path: str = None,
    source: str = None,
    max_chars: int = 12,
    protected_terms=None,
    overwrite: bool = True,
) -> str:
    output_path = prepare_output_path(
        output_path=output_path,
        default_dir='output/subtitles',
        default_name=_default_segmented_name(caption_path=caption_path, source=source),
        extension='.captions.json',
        overwrite=overwrite,
    )
    payload = {
        'source': source,
        'mode': 'segment',
        'maxChars': int(max_chars or 12),
        'protectedTerms': protected_terms or [],
        'captions': clean_captions(captions),
    }
    Path(output_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return output_path
