#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, Sequence, Tuple


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
        parts = []
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
            text = ', '.join(str(item).strip() for item in value if str(item).strip())
        else:
            text = str(value).strip()
        if text:
            return text
    return default


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


def _shorten(text: str, limit: int = 120) -> str:
    clean = ' '.join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + '...'


ACTIVITY_RULES = {
    'High': ['workout', 'work out', 'working out', 'exercise', 'run', 'gym', 'training', 'sports', 'hike', 'sweat'],
    'Low': ['desk', 'sedentary', 'indoors', 'sitting', 'low activity'],
}

WEATHER_RULES = {
    'Hot': ['hot', 'heat', 'summer', 'humid', 'warm'],
    'Cool': ['cold', 'winter', 'cool', 'mild'],
}

CAFFEINE_RULES = {
    'Higher caffeine': ['energy drink', 'multiple coffees', 'lots of coffee', '3 coffees', '4 coffees', 'caffeine'],
}

TRACKING_RULES = {
    'Bottle refill system': ['bottle', 'refill', 'thermos'],
    'Cup count': ['cup', 'glass', 'mug'],
    'Tally marks': ['tally', 'check mark', 'checkbox'],
}


def _build_range(activity: str, weather: str, caffeine: str) -> Tuple[str, str]:
    minimum, maximum = 1.8, 2.3
    reasons = ['it starts from a steady baseline instead of a rigid universal rule']

    if activity == 'High':
        minimum += 0.4
        maximum += 0.6
        reasons.append('higher activity usually means more sweat loss')
    elif activity == 'Low':
        minimum -= 0.2
        maximum -= 0.2
        reasons.append('lighter activity keeps the target a bit lower')

    if weather == 'Hot':
        minimum += 0.2
        maximum += 0.3
        reasons.append('hot weather raises hydration demand')
    elif weather == 'Cool':
        reasons.append('cooler weather keeps the need closer to baseline')

    if caffeine == 'Higher caffeine':
        minimum += 0.1
        maximum += 0.1
        reasons.append('more caffeine makes a structured rhythm more useful')

    minimum = max(1.5, minimum)
    maximum = max(minimum + 0.3, maximum)
    return f'{minimum:.1f} to {maximum:.1f} L', '; '.join(reasons)


def _build_anchors(activity: str) -> Dict[str, str]:
    afternoon = 'Use one work-block reminder, drink with lunch, and add another glass mid-afternoon.'
    if activity == 'High':
        afternoon = 'Use one work-block reminder, drink one bottle around workouts or walks, and replace sweat loss before dinner.'
    return {
        'Morning': 'Drink 300 to 500 mL within 30 minutes of waking and pair another glass with breakfast.',
        'Midday': 'Aim to reach about half of the daily range by lunch so the rest of the day stays easy.',
        'Afternoon': afternoon,
        'Evening': 'Drink moderately with dinner, then taper so catch-up does not spill into late-night waking.',
    }


def handle(inputs):
    meta = _load_skill_meta('skill')
    data = _coerce_dict(inputs)
    raw = _normalize_inputs(inputs)

    current_pattern = _pick_text(
        data,
        ['current_pattern', 'pattern', 'intake', 'baseline'],
        _shorten(raw) if raw else 'Hydration happens inconsistently and mostly depends on memory or thirst cues.',
    )
    activity = _pick_text(data, ['activity_level', 'activity'], _detect_one(raw, ACTIVITY_RULES, 'Moderate'))
    weather = _pick_text(data, ['weather'], _detect_one(raw, WEATHER_RULES, 'Temperate'))
    caffeine = _pick_text(data, ['caffeine', 'caffeine_use'], _detect_one(raw, CAFFEINE_RULES, 'Moderate caffeine'))
    tracking_method = _pick_text(data, ['tracking_method', 'tracking', 'log_method'], _detect_one(raw, TRACKING_RULES, 'Bottle refill system'))
    suggested_range = _pick_text(data, ['suggested_range'])
    why_range = _pick_text(data, ['why_range'])
    if not suggested_range:
        suggested_range, why_range = _build_range(activity, weather, caffeine)

    routine = _pick_text(data, ['routine', 'schedule'])
    context_bits = [f'activity={activity}', f'weather={weather}', f'caffeine={caffeine}']
    if routine:
        context_bits.append(f'routine={routine}')

    anchors = _build_anchors(activity)
    return f"""# Hydration Plan
## Baseline
- Current pattern: {current_pattern}
- Context factors: {'; '.join(context_bits)}

## Daily Range
- Suggested range: {suggested_range}
- Why this range: {why_range}

## Drinking Anchors
- Morning: {anchors['Morning']}
- Midday: {anchors['Midday']}
- Afternoon: {anchors['Afternoon']}
- Evening: {anchors['Evening']}

## Tracking Method
- Cup, bottle, or tally system: {tracking_method}
- Catch-up rule: If you are behind by midday, add one glass with lunch and one in the next work block, but stop aggressive catch-up within 2 hours of bed.

## Watch-outs
- Signs I am underhydrated: dry mouth, darker yellow urine, headache, unusual fatigue, or strong thirst.
- When not to force more water: when urine is already very pale, your stomach feels sloshy, night waking is rising, or a clinician has given you a fluid limit.
"""
