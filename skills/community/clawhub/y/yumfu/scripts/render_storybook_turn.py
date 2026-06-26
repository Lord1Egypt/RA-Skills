#!/usr/bin/env python3
import argparse
import json
import re


def normalize(text: str) -> str:
    return ' '.join((text or '').strip().split())


def player_to_storybook(text: str) -> str:
    raw = normalize(text)
    if not raw:
        return ''
    lower = raw.lower()
    if lower.startswith('/yumfu '):
        raw = raw[7:].strip()
    elif lower == '/yumfu':
        return 'You continued the adventure.'
    if raw in {'A', 'B', 'C', 'D', '1', '2', '3', '4'}:
        return f'You chose option {raw} and committed yourself to that path.'
    if len(raw) <= 12 and re.fullmatch(r'[0-9a-zA-Z一二三四五六七八九十，。.!?？]+', raw):
        return f'You answered simply: {raw}.'
    if raw.endswith(('。', '.', '！', '!', '？', '?')):
        return raw
    return raw[:1].upper() + raw[1:] + '.'


def ai_to_storybook(text: str) -> str:
    raw = (text or '').strip()
    if not raw:
        return ''
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    filtered = []
    for ln in lines:
        if ln.startswith('[') and ln.endswith(']'):
            continue
        if ln.startswith('**') and ln.endswith('**'):
            filtered.append(ln.strip('*'))
            continue
        filtered.append(ln)
    prose = ' '.join(filtered)
    prose = re.sub(r'\s+', ' ', prose).strip()
    return prose


def main():
    parser = argparse.ArgumentParser(description='Render raw YumFu turn text into storybook-ready prose')
    parser.add_argument('--player', required=True)
    parser.add_argument('--ai', required=True)
    args = parser.parse_args()
    print(json.dumps({
        'player_storybook': player_to_storybook(args.player),
        'ai_storybook': ai_to_storybook(args.ai),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
