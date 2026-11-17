import re
from typing import Tuple


def count_wechat_units(text: str) -> float:
    total = 0.0
    for ch in text:
        code = ord(ch)
        if (
            0x4E00 <= code <= 0x9FFF or
            0x3400 <= code <= 0x4DBF or
            0x20000 <= code <= 0x2A6DF or
            0x2A700 <= code <= 0x2CEAF or
            0xF900 <= code <= 0xFAFF or
            0xFF00 <= code <= 0xFFEF or
            0x3000 <= code <= 0x303F or
            0x1F300 <= code <= 0x1FAFF
        ):
            total += 1.0
        else:
            total += 0.5
    return total


def truncate_digest(digest: str, max_units: int = 120) -> str:
    if not digest:
        return ""
    
    result = []
    used = 0.0
    for ch in digest:
        code = ord(ch)
        if (
            0x4E00 <= code <= 0x9FFF or
            0x3400 <= code <= 0x4DBF or
            0x20000 <= code <= 0x2A6DF or
            0x2A700 <= code <= 0x2CEAF or
            0xF900 <= code <= 0xFAFF or
            0xFF00 <= code <= 0xFFEF or
            0x3000 <= code <= 0x303F or
            0x1F300 <= code <= 0x1FAFF
        ):
            cost = 1.0
        else:
            cost = 0.5
        if used + cost > max_units + 1e-9:
            break
        result.append(ch)
        used += cost
    
    temp = "".join(result)
    
    for punct in ['\u3002', '\uff0c', '\uff1b', '\uff01', '\uff1f', '. ', ', ']:
        idx = temp.rfind(punct)
        if idx > int(max_units * 0.5):
            temp = temp[:idx + len(punct)]
            break
    
    temp = temp.rstrip('\uff0c\u3001')
    
    return temp


def validate_digest(digest: str, max_units: int = 120) -> Tuple[str, bool]:
    if not digest:
        return "", False
    
    units = count_wechat_units(digest)
    if units <= max_units:
        return digest, False
    
    truncated = truncate_digest(digest, max_units)
    return truncated, True


def extract_digest(html_content: str, max_units: int = 120) -> str:
    content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    # Replace block-level closing tags with newline to preserve text separation
    content = re.sub(r'</(?:p|div|section|h[1-6]|li|tr|blockquote|pre|ul|ol)[^>]*>', '\n', content, flags=re.IGNORECASE)
    content = re.sub(r'<[^>]+>', '', content)
    content = re.sub(r'&[a-zA-Z]+;', ' ', content)
    content = re.sub(r'\s{2,}', '\n', content)
    
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    candidates = []
    for line in lines:
        if len(line) < 15:
            continue
        if re.match(r'^\d+[\.\u3001\s]', line):
            continue
        if re.match(r'^[#*\-+]+', line):
            continue
        candidates.append(line)
    
    if candidates:
        result = candidates[0]
        for line in candidates[1:]:
            if count_wechat_units(result + ' ' + line) <= max_units:
                result += ' ' + line
            else:
                break
    else:
        result = content[:int(max_units)]
    
    return truncate_digest(result, max_units)
