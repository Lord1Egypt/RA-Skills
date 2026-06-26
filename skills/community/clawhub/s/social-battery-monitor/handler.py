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

BATTERY_RULES = {
'Depleted': ['depleted', 'shutdown', 'burned out', 'burnt out', 'exhausted'],
'Low': ['drained', 'tired', 'overwhelmed', 'brain fog', 'low battery', 'irritable'],
'Moderate': ['okay', 'fine', 'steady', 'medium'],
'Full': ['energized', 'excited', 'full battery', 'ready', 'good social energy'],
}

SIGN_RULES = {
'irritability': ['irritable', 'snappy', 'annoyed'],
'brain fog': ['brain fog', 'foggy', 'fried'],
'numbness': ['numb', 'flat'],
'urge to withdraw': ['hide', 'withdraw', 'avoid'],
'shutdown feeling': ['shutdown', 'silent', 'checked out'],
}

EVENT_RULES = {
'Networking event': ['networking', 'conference', 'mixer', 'industry event'],
'Team meeting or workshop': ['meeting', 'workshop', 'offsite', 'standup'],
'Family gathering': ['family', 'relative', 'parent', 'in-law'],
'Friend catch-up': ['friend', 'coffee', 'hangout', 'dinner with friends'],
'Party or celebration': ['party', 'birthday', 'wedding', 'celebration'],
'School or caregiving event': ['school', 'teacher', 'pickup', 'caregiving', 'parent meeting'],
}


def _battery_level(text: str) -> str:
    return _detect_one(text, BATTERY_RULES, 'Moderate')


def _default_signs(level: str) -> List[str]:
    mapping = {
        'Depleted': ['brain fog', 'urge to withdraw', 'shutdown feeling'],
        'Low': ['irritability', 'brain fog', 'urge to withdraw'],
        'Moderate': ['mild fatigue by the end of the day'],
        'Full': ['clear focus and easier small talk'],
    }
    return mapping.get(level, ['mild fatigue by the end of the day'])


def _event_entries(data: Dict[str, Any], text: str) -> List[str]:
    provided = _listify(data.get('events'))
    if provided:
        return provided[:3]
    return _detect_many(text, EVENT_RULES, ['Upcoming social commitments this week'], limit=3)


def _event_plan(label: str, level: str) -> Dict[str, str]:
    lower = label.lower()
    if 'network' in lower or 'conference' in lower:
        cost = 'High' if level in ['Low', 'Depleted'] else 'Medium to high'
        value = 'Opportunity, visibility, and useful connection'
        recovery = '60 to 90 minutes of quiet time afterward'
    elif 'family' in lower:
        cost = 'Medium to high' if level in ['Low', 'Depleted'] else 'Medium'
        value = 'Relationship maintenance and family presence'
        recovery = 'A lighter evening or early exit buffer'
    elif 'friend' in lower:
        cost = 'Low to medium'
        value = 'Potentially nourishing if the relationship feels safe and easy'
        recovery = 'A short decompression block afterward'
    elif 'party' in lower or 'celebration' in lower:
        cost = 'High'
        value = 'Joy or connection, but only if duration is capped'
        recovery = 'A protected quiet block and no stacked plans after'
    elif 'school' in lower or 'care' in lower:
        cost = 'Medium'
        value = 'Necessary presence and practical support'
        recovery = '15 to 30 minutes alone before the next obligation'
    elif 'meeting' in lower or 'workshop' in lower:
        cost = 'Medium'
        value = 'Work coordination and reduced future friction'
        recovery = 'A short reset walk or no-meeting buffer afterward'
    else:
        cost = 'Medium'
        value = 'Social maintenance with mixed payoff'
        recovery = 'A short quiet reset afterward'
    return {'cost': cost, 'value': value, 'recovery': recovery}


def _exit_line(event_label: str) -> str:
    lower = event_label.lower()
    if 'family' in lower:
        return 'I can come for a shorter window, but I will not stay the whole time tonight.'
    if 'meeting' in lower or 'workshop' in lower:
        return 'I can stay for the key part, then I need to step out for another commitment.'
    if 'friend' in lower:
        return 'I want to see you, and I only have about an hour today, so I need to keep it short.'
    return 'I can be there for the important part, then I need to head out and recharge.'


def _quick_recharge(level: str) -> str:
    if level in ['Low', 'Depleted']:
        return '10 to 20 minutes alone, no notifications, low light, and zero conversation.'
    return 'A short walk, quiet tea, or one low-stimulation break between plans.'


def _deep_recharge(level: str) -> str:
    if level in ['Low', 'Depleted']:
        return 'A protected half-day or evening with no performance demands and no stacked social plans.'
    return 'One longer block of solo time, sleep recovery, and a low-input activity.'


def handle(inputs):
    meta = _load_skill_meta('social-battery-monitor')
    data = _coerce_dict(inputs)
    text = _normalize_inputs(inputs)
    level = _pick_text(data, ['current_level', 'battery', 'energy_level'], _battery_level(text))
    signs = _listify(data.get('signs')) or _detect_many(text, SIGN_RULES, _default_signs(level), limit=4)
    events = _event_entries(data, text)
    first_event = events[0] if events else 'Upcoming social commitments this week'

    before = 'Protect a small buffer before the event, eat something, and decide the maximum duration in advance.'
    if level in ['Low', 'Depleted']:
        before = 'Protect 30 to 60 minutes alone before the event, reduce extra errands, and decide the shortest acceptable version.'
    during = 'Check body cues halfway through, step outside if needed, and avoid performing harder than the situation requires.'
    after = 'Block a recharge window right after the event instead of stacking another draining plan.'
    if level in ['Low', 'Depleted']:
        after = 'Leave a clean recovery block afterward with no calls, no chores, and no surprise social spillover.'

    lines: List[str] = []
    lines.append('# Social Battery Plan')
    lines.append('')
    lines.append('## Current Battery')
    lines.append(f'- Current level: {level}')
    lines.append(f"- Signs I am already low: {', '.join(signs)}")
    lines.append('')
    lines.append('## Upcoming Social Load')
    for event in events:
        plan = _event_plan(event, level)
        lines.append(f'- Event: {event}')
        lines.append(f'  - Expected cost: {plan["cost"]}')
        lines.append(f'  - Expected value: {plan["value"]}')
        lines.append(f'  - Recovery needed: {plan["recovery"]}')
    lines.append('')
    lines.append('## Protection Plan')
    lines.append(f'- Before the event: {before}')
    lines.append(f'- During the event: {during}')
    lines.append(f'- Exit line: {_exit_line(first_event)}')
    lines.append(f'- After the event: {after}')
    lines.append('')
    lines.append('## Recharge Menu')
    lines.append(f'- Quick recharge: {_quick_recharge(level)}')
    lines.append(f'- Deep recharge: {_deep_recharge(level)}')
    return '\n'.join(lines)

if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
