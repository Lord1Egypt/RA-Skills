#!/usr/bin/env python3
import json
import os
import re
import sys
from typing import Any, Dict, List, Sequence


def _load_skill_meta(slug):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    meta = re.search(r'^---$(.*?)^---$', content, re.DOTALL | re.MULTILINE)
    return meta.group(1).strip() if meta else ''


def _normalize_inputs(inputs: Any) -> str:
    if inputs is None:
        return ''
    if isinstance(inputs, str):
        return inputs.strip()
    if isinstance(inputs, dict):
        parts: List[str] = []
        for key, value in inputs.items():
            if value in (None, '', [], {}, ()):  # type: ignore[comparison-overlap]
                continue
            if isinstance(value, (list, tuple, set)):
                rendered = ', '.join(str(item) for item in value)
            else:
                rendered = str(value)
            parts.append(f"{key}: {rendered}")
        return ' | '.join(parts)
    if isinstance(inputs, (list, tuple, set)):
        return ' | '.join(str(item) for item in inputs)
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


def _coerce_dict(inputs: Any) -> Dict[str, Any]:
    return inputs if isinstance(inputs, dict) else {}


def _pick_text(data: Dict[str, Any], keys: Sequence[str], default: str = '') -> str:
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            text = ', '.join(str(item) for item in value if str(item).strip())
        else:
            text = str(value).strip()
        if text:
            return text
    return default


def _listify(value: Any) -> List[str]:
    if value in (None, '', [], {}, ()):  # type: ignore[comparison-overlap]
        return []
    if isinstance(value, str):
        clean = value.replace(';', '\n').replace(',', '\n')
        return [chunk.strip() for chunk in clean.splitlines() if chunk.strip()]
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


def _detect_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    lower = text.lower()
    found = [label for label, keywords in rules.items() if any(keyword in lower for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _shorten(text: str, limit: int = 140) -> str:
    clean = ' '.join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + '...'

DEVICE_RULES = {
'Phone': ['phone', 'mobile', 'iphone', 'android'],
'Laptop': ['laptop', 'computer', 'desktop', 'work computer'],
'Tablet': ['tablet', 'ipad'],
'TV': ['tv', 'television'],
}

APP_RULES = {
'Short video apps': ['tiktok', 'douyin', 'reels', 'short video'],
'Social feeds': ['instagram', 'xiaohongshu', 'xhs', 'facebook', 'twitter', 'social media'],
'Messaging and checking': ['wechat', 'slack', 'telegram', 'message', 'checking'],
'News or reading drift': ['news', 'reddit', 'headline'],
'Games': ['game', 'gaming'],
'Shopping apps': ['taobao', 'jd', 'amazon', 'shopping'],
}

TIME_RULES = {
'Late night': ['late night', 'late-night', 'before bed', 'midnight', 'night'],
'Morning startup': ['morning', 'after waking', 'wake up'],
'Work transitions': ['between tasks', 'transition', 'between meetings', 'break'],
'Stress moments': ['stress', 'anxious', 'overwhelmed'],
'Study avoidance': ['procrastination', 'avoid', 'deadline'],
}

TRIGGER_RULES = {
'Boredom': ['bored', 'boredom'],
'Fatigue': ['tired', 'fatigue', 'exhausted'],
'Procrastination': ['procrastination', 'avoid', 'put off'],
'Stress relief': ['stress', 'anxious', 'overwhelmed'],
'Social comparison': ['compare', 'comparison', 'jealous'],
}


def _trigger_details(trigger: str) -> Dict[str, str]:
    mapping = {
        'Boredom': {
            'behavior': 'Open the easiest feed or app for stimulation.',
            'gain': 'Quick novelty without needing effort.',
            'substitute': 'Keep one offline micro-option ready, such as a short walk, paper notes, or stretching.',
        },
        'Fatigue': {
            'behavior': 'Scroll passively instead of transitioning into real rest.',
            'gain': 'Numbing relief and low-effort input.',
            'substitute': 'Charge the phone away from the body and switch to a short wind-down ritual.',
        },
        'Procrastination': {
            'behavior': 'Check apps in fragments to avoid the harder task.',
            'gain': 'Temporary escape from resistance.',
            'substitute': 'Use a 10-minute starter task before any check and keep the harder task visible.',
        },
        'Stress relief': {
            'behavior': 'Reach for the screen to downshift emotionally.',
            'gain': 'A fast feeling of comfort or distraction.',
            'substitute': 'Use a lower-stimulation reset first, like breathing, walking, or making tea.',
        },
        'Social comparison': {
            'behavior': 'Keep checking feeds that spark comparison loops.',
            'gain': 'A sense of being plugged in, even when it feels bad later.',
            'substitute': 'Replace one comparison loop with direct contact, journaling, or a saved reading list.',
        },
    }
    return mapping.get(trigger, {
        'behavior': 'Check the nearest screen automatically.',
        'gain': 'A fast shift of attention.',
        'substitute': 'Add one offline reset between urge and action.',
    })


def _friction_changes(apps: List[str], time_bands: List[str]) -> str:
    changes = ['turn off non-critical notifications', 'move high-drift apps off the home screen']
    if 'Late night' in time_bands:
        changes.append('charge the phone outside the bedroom')
    if 'Short video apps' in apps:
        changes.append('log out of short-video apps after each session')
    return ', '.join(changes[:4])


def _phone_free_zone(time_bands: List[str]) -> str:
    if 'Late night' in time_bands:
        return 'Bedroom after the evening cutoff and the last 30 minutes before sleep.'
    if 'Morning startup' in time_bands:
        return 'The first 30 minutes after waking.'
    return 'One meal and one focused work block each day.'


def _weekly_target(time_bands: List[str]) -> str:
    if 'Late night' in time_bands:
        return 'No scrolling in bed for 5 of the next 7 nights.'
    if 'Work transitions' in time_bands:
        return 'Batch checking into 3 planned windows per day for one week.'
    return 'Reduce the main leakage zone with one rule that holds for 5 of the next 7 days.'


def handle(inputs):
    meta = _load_skill_meta('screen-time-auditor')
    data = _coerce_dict(inputs)
    text = _normalize_inputs(inputs)
    devices = _listify(data.get('devices')) or _detect_many(text, DEVICE_RULES, ['Phone', 'Laptop'], limit=3)
    apps = _listify(data.get('apps')) or _detect_many(text, APP_RULES, ['Social feeds', 'Messaging and checking'], limit=4)
    time_bands = _listify(data.get('time_bands')) or _detect_many(text, TIME_RULES, ['Late night', 'Work transitions'], limit=3)
    triggers = _listify(data.get('triggers')) or _detect_many(text, TRIGGER_RULES, ['Boredom', 'Fatigue'], limit=2)
    replacement = _trigger_details(triggers[0])['substitute']

    lines: List[str] = []
    lines.append('# Screen Time Audit')
    lines.append('')
    lines.append('## Current Pattern')
    lines.append(f"- Main devices: {', '.join(devices)}")
    lines.append(f"- Main drain apps or behaviors: {', '.join(apps)}")
    lines.append(f"- Worst time bands: {', '.join(time_bands)}")
    lines.append('')
    lines.append('## Trigger Map')
    for trigger in triggers[:3]:
        detail = _trigger_details(trigger)
        lines.append(f'- Trigger: {trigger}')
        lines.append(f'  - Typical behavior: {detail["behavior"]}')
        lines.append(f'  - What it gives me: {detail["gain"]}')
        lines.append(f'  - Better substitute: {detail["substitute"]}')
    lines.append('')
    lines.append('## Reduction Plan')
    lines.append(f'- Friction to add: {_friction_changes(apps, time_bands)}')
    lines.append(f'- Phone-free zone: {_phone_free_zone(time_bands)}')
    lines.append(f'- Replacement action: {replacement}')
    lines.append(f'- Weekly target: {_weekly_target(time_bands)}')
    return '\n'.join(lines)

if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
