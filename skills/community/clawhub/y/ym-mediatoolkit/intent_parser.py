import json
import re
from pathlib import Path


SUPPORTED_FORMATS = ('mp3', 'wav', 'aac', 'm4a')
MEDIA_EXTENSIONS = ('mp4', 'mov', 'mkv', 'avi', 'webm', 'm4v')


def _strip_token(value: str) -> str:
    return value.strip().strip('，。,.；;')


def _extract_quoted_values(message: str) -> list:
    patterns = [
        r'"([^"]+)"',
        r"'([^']+)'",
        r'“([^”]+)”',
        r'‘([^’]+)’',
        r'`([^`]+)`',
        r'《([^》]+)》',
    ]
    values = []
    for pattern in patterns:
        values.extend(_strip_token(match) for match in re.findall(pattern, message))
    return values


def _looks_like_media_source(value: str) -> bool:
    if re.match(r'^https?://', value, re.I):
        return True
    if re.search(r'\.(' + '|'.join(MEDIA_EXTENSIONS) + r')$', value, re.I):
        return True
    return False


def _extract_source(message: str) -> str:
    for value in _extract_quoted_values(message):
        if _looks_like_media_source(value):
            return value

    url_match = re.search(r'https?://[^\s，。；;]+', message, re.I)
    if url_match:
        return _strip_token(url_match.group(0))

    windows_match = re.search(
        r'[A-Za-z]:[\\/][^\s"\'`<>|]+\.(' + '|'.join(MEDIA_EXTENSIONS) + r')',
        message,
        re.I,
    )
    if windows_match:
        return _strip_token(windows_match.group(0))

    local_match = re.search(
        r'(?:\.{0,2}[\\/])?[^\s"\'`<>|，。；;]+\.(' + '|'.join(MEDIA_EXTENSIONS) + r')',
        message,
        re.I,
    )
    if local_match:
        return _strip_token(local_match.group(0))

    return ''


def _extract_output_dir(message: str, source: str) -> str:
    match = re.search(r'(?:输出到|保存到|放到)\s*["“`]?([^"”`\s，。；;]+)', message)
    if not match:
        return ''
    value = _strip_token(match.group(1))
    if value == source:
        return ''
    return value


def _extract_format(message: str) -> str:
    lower = message.lower()
    for audio_format in SUPPORTED_FORMATS:
        if re.search(rf'\b{audio_format}\b', lower):
            return audio_format
    return 'mp3'


def _extract_time_seconds(message: str):
    match = re.search(r'(?:第\s*)?(\d+(?:\.\d+)?)\s*秒', message)
    if match:
        value = float(match.group(1))
        return int(value) if value.is_integer() else value
    hms_match = re.search(r'(\d{1,2}):(\d{1,2})(?::(\d{1,2}(?:\.\d+)?))?', message)
    if hms_match:
        first, second, third = hms_match.groups()
        if third is None:
            return int(first) * 60 + int(second)
        return int(first) * 3600 + int(second) * 60 + float(third)
    return None


def _extract_overwrite(message: str):
    lower = message.lower()
    if any(token in message for token in ('不要覆盖', '不覆盖', '别覆盖')) or 'overwrite=false' in lower:
        return False
    if '覆盖' in message or 'overwrite=true' in lower:
        return True
    return None


def _json_intent(message: str):
    text = message.strip()
    if not (text.startswith('{') and text.endswith('}')):
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict) and data.get('steps'):
        return {
            'intent': 'pipeline',
            'confidence': 1.0,
            'action': 'pipeline',
            'params': data,
            'missing_fields': [],
        }
    action = data.get('action') if isinstance(data, dict) else None
    if action in ('audio', 'thumbnail', 'compress', 'info', 'audio_info', 'asr', 'ocr', 'subtitle'):
        params = {key: value for key, value in data.items() if key != 'action'}
        return {
            'intent': action,
            'confidence': 1.0,
            'action': action,
            'params': params,
            'missing_fields': [],
        }
    return None


def parse_media_intent(message: str) -> dict:
    if not isinstance(message, str) or not message.strip():
        return {
            'intent': 'unknown',
            'confidence': 0,
            'action': None,
            'params': {},
            'missing_fields': ['message'],
        }

    json_result = _json_intent(message)
    if json_result:
        return json_result

    source = _extract_source(message)
    missing_fields = [] if source else ['source']
    lower = message.lower()
    params = {'source': source} if source else {}
    output_dir = _extract_output_dir(message, source)
    overwrite = _extract_overwrite(message)
    if output_dir:
        params['output_dir'] = output_dir
    if overwrite is not None:
        params['overwrite'] = overwrite

    subtitle_tokens = ('识别字幕', '提取字幕', '转字幕', '生成字幕', '字幕识别', '字幕 json', '字幕JSON')
    subtitle_verbs = ('识别', '提取', '生成', '转', '导出')
    if any(token in message for token in subtitle_tokens) or ('字幕' in message and any(verb in message for verb in subtitle_verbs)):
        action = 'subtitle'
        intent = 'subtitle'
        if 'ocr' in lower or '画面' in message or '硬字幕' in message:
            params['mode'] = 'ocr'
        elif 'asr' in lower or '语音' in message or '声音' in message:
            params['mode'] = 'asr'
        else:
            params['mode'] = 'fusion'
    elif '音频信息' in message or '音轨' in message:
        action = 'audio_info'
        intent = 'audio_info'
    elif '音频' in message or '提取声音' in message or '导出声音' in message:
        action = 'audio'
        intent = 'extract_audio'
        params['format'] = _extract_format(message)
    elif any(token in message for token in ('封面', '缩略图', '截图', '帧')):
        action = 'thumbnail'
        intent = 'extract_thumbnail'
        time_seconds = _extract_time_seconds(message)
        params['time_seconds'] = 0 if time_seconds is None else time_seconds
    elif any(token in message for token in ('压缩', '变小', '瘦身')):
        action = 'compress'
        intent = 'compress'
    elif any(token in message for token in ('信息', '详情', '元数据', '查看')):
        action = 'info'
        intent = 'info'
    else:
        return {
            'intent': 'unknown',
            'confidence': 0,
            'action': None,
            'params': params,
            'missing_fields': missing_fields or ['action'],
        }

    if source:
        params['name'] = Path(source).stem or 'media'
    return {
        'intent': intent,
        'confidence': 0.85 if not missing_fields else 0.5,
        'action': action,
        'params': params,
        'missing_fields': missing_fields,
    }
