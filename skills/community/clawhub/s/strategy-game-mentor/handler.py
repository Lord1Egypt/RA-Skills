#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'strategy-game-mentor'
PROMPT_TEMPLATE = """Reframe the user's situation as a strategy game board.
Identify the best strategic stance, clarify victory and loss conditions, name supply lines and pressure points, then give opening, midgame, endgame, and decision reminders. Keep it practical, not theatrical."""

PROFILES = {
    'stabilize': {
        'label': 'Stabilize the Board',
        'summary': 'Patch leaks and restore reliable supply lines before taking new fights.',
        'opening': 'Stop the biggest leak, cut one optional front, and secure the next controllable move.',
        'midgame': 'Rebuild repeatable routines, buffers, or visibility so surprises hurt less.',
        'endgame': 'Expand only after the base stops wobbling for several turns.',
        'protect': 'core energy, one essential deliverable, and the people or systems keeping the map functioning',
        'contest': 'the recurring leak that keeps draining time or morale',
        'let_go': 'side quests, prestige tasks, and anything that creates motion without stability',
        'misread': 'Mistaking frantic activity for restored control.',
    },
    'positioning': {
        'label': 'Claim Better Positioning',
        'summary': 'Improve leverage, information, and options before forcing outcomes.',
        'opening': 'Clarify the map, rank fronts by leverage, and move toward the position that makes later turns easier.',
        'midgame': 'Build optionality, gather clean information, and avoid low-value skirmishes.',
        'endgame': 'Convert the better position into a focused push when the path is clear.',
        'protect': 'decision quality and the flexibility to respond after new information appears',
        'contest': 'foggy priorities and scattered commitments',
        'let_go': 'premature commitments made only to feel decisive',
        'misread': 'Treating urgency as proof that a commitment should happen now.',
    },
    'timing_push': {
        'label': 'Timing Push',
        'summary': 'Concentrate force into a short window that matters more than perfect balance.',
        'opening': 'Define the exact window, compress prep, and remove every distraction that does not help the push.',
        'midgame': 'Protect execution bandwidth and keep support resources flowing into the main objective.',
        'endgame': 'Close decisively, then stop instead of drifting into sloppy overtime.',
        'protect': 'the narrow window, focus bandwidth, and the quality of the main attempt',
        'contest': 'distraction, fragmentation, and fear-driven last-minute scope growth',
        'let_go': 'nice-to-have improvements that belong after the push, not before it',
        'misread': 'Trying to optimize every flank instead of winning the window that actually matters.',
    },
    'attrition': {
        'label': 'Attrition and Sustainable Value',
        'summary': 'Win by trading patiently, preserving endurance, and compounding small edges.',
        'opening': 'Choose repeatable trades you can sustain and avoid flashy swings that break your own economy.',
        'midgame': 'Keep pressure steady, document progress, and let the opponent or problem spend more energy than you do.',
        'endgame': 'Close when the cumulative edge becomes obvious, not before.',
        'protect': 'endurance, consistency, and evidence of incremental advantage',
        'contest': 'slow leaks and recurring inefficiencies',
        'let_go': 'dramatic but low-probability gambits',
        'misread': 'Getting bored with compounding and abandoning the plan right before it pays off.',
    },
    'expansion': {
        'label': 'Expand from Advantage',
        'summary': 'Use a strong base to open new lanes without losing control of the old ones.',
        'opening': 'Confirm the current base is real, then choose the one expansion lane with the best upside-to-friction ratio.',
        'midgame': 'Add structure so the new front does not cannibalize the core base.',
        'endgame': 'Lock in the gain and make sure the original engine still runs cleanly.',
        'protect': 'the profitable base that funds the new move',
        'contest': 'overextension and hidden maintenance costs',
        'let_go': 'opening multiple new fronts at once just because momentum feels good',
        'misread': 'Confusing a temporary high with actual spare capacity.',
    },
}


def _load_skill_meta(skill_name: str) -> Dict[str, str]:
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as handle:
        content = handle.read()
    match = re.search(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL | re.MULTILINE)
    meta: Dict[str, str] = {}
    if match:
        for line in match.group(1).splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip()
    meta['skill_name'] = skill_name or meta.get('name', SKILL_SLUG)
    return meta


def _load_prompt_template(skill_name: str) -> str:
    del skill_name
    return PROMPT_TEMPLATE


def _normalize_key(key: Any) -> str:
    return re.sub(r'[^a-z0-9_\u4e00-\u9fff]+', '_', str(key).strip().lower()).strip('_')


def _clean_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _normalize_map(data: Dict[str, Any]) -> Dict[str, Any]:
    return {_normalize_key(key): value for key, value in data.items()}


def _parse_text_map(raw: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    for line in raw.splitlines():
        if re.search(r'[:：]', line):
            key, value = re.split(r'[:：]', line, maxsplit=1)
            data[_normalize_key(key)] = value.strip()
    return data


def _coerce_input(user_input: Any) -> Tuple[str, Dict[str, Any]]:
    if isinstance(user_input, dict):
        return json.dumps(user_input, ensure_ascii=False), _normalize_map(user_input)
    raw = _clean_text(user_input)
    if raw.startswith('{') and raw.endswith('}'):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return raw, _normalize_map(parsed)
        except json.JSONDecodeError:
            pass
    return raw, _parse_text_map(raw)


def _pick(data: Dict[str, Any], keys: List[str], default: str = '') -> str:
    for key in keys:
        normalized = _normalize_key(key)
        if normalized in data:
            text = _clean_text(data[normalized])
            if text:
                return text
    return default


def _split_items(value: Any) -> List[str]:
    if isinstance(value, list):
        return [_clean_text(item) for item in value if _clean_text(item)]
    text = _clean_text(value)
    if not text:
        return []
    parts = [re.sub(r'^[\-•\d.\s]+', '', part).strip() for part in re.split(r'[\n,;，；]+', text)]
    return [part for part in parts if part]


def _contains_any(text: str, keywords: List[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in keywords)


def _score_profiles(raw: str, data: Dict[str, Any]) -> Tuple[str, Dict[str, str], List[str], List[str]]:
    situation = _pick(data, ['situation', 'current_situation', '现状'])
    goal = _pick(data, ['goal', 'victory_condition', '目标'])
    resources = _split_items(_pick(data, ['resources', 'assets', '资源']))
    constraints = _split_items(_pick(data, ['constraints', 'limits', '约束']))
    pressure = _pick(data, ['pressure', 'resistance', 'opponent', '阻力', '对手'])
    time_window = _pick(data, ['time_window', 'deadline', 'window', '时间窗口'])
    context = ' '.join([raw, situation, goal, pressure, time_window, ' '.join(resources), ' '.join(constraints)]).lower()

    scores = {name: 0 for name in PROFILES}
    if _contains_any(context, ['deadline', 'exam', 'launch', 'sprint', 'window', 'one week', 'this week', '冲刺', '考试']):
        scores['timing_push'] += 5
    if time_window and goal:
        scores['timing_push'] += 2
    if _contains_any(context, ['exam day', 'launch day', 'submission', 'test day', '考试日']):
        scores['timing_push'] += 1
    if _contains_any(context, ['overwhelmed', 'chaos', 'too many fires', 'fatigue', 'low energy', 'mess', 'wobbling', '崩', '乱']):
        scores['stabilize'] += 5
    if _contains_any(context, ['priority', 'position', 'leverage', 'option', 'unclear', 'choose', 'path', '优先级', '取舍']):
        scores['positioning'] += 4
    if _contains_any(context, ['long game', 'season', 'sustainable', 'steady', 'recurring', 'compound', '长期', '稳定']):
        scores['attrition'] += 4
    if _contains_any(context, ['opportunity', 'expand', 'growth', 'new lane', 'runway', 'spare capacity', '扩张', '增长']):
        scores['expansion'] += 4
    if constraints and len(constraints) >= 2:
        scores['stabilize'] += 1
        scores['positioning'] += 1
    if resources and len(resources) >= 3:
        scores['expansion'] += 1
        scores['positioning'] += 1
    if all(score == 0 for score in scores.values()):
        scores['positioning'] = 2
        scores['stabilize'] = 1

    profile_id = sorted(scores.items(), key=lambda item: (item[1], PROFILES[item[0]]['label']), reverse=True)[0][0]
    extracted = {
        'situation': situation or 'current board state not fully specified',
        'goal': goal or 'victory condition not fully specified',
        'pressure': pressure or 'resistance is mostly internal friction or diffuse uncertainty',
        'time_window': time_window or 'time window not fully specified',
    }
    return profile_id, extracted, resources, constraints


def _loss_condition(goal: str, constraints: List[str], pressure: str) -> str:
    if constraints:
        return f"Letting {constraints[0]} keep blocking the line of play until the goal stalls."
    if pressure and pressure != 'resistance is mostly internal friction or diffuse uncertainty':
        return f'Allowing {pressure} to dictate the tempo for too many turns.'
    return 'Spreading effort too thin and never converting progress into a clear win state.'


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    profile_id, extracted, resources, constraints = _score_profiles(raw, data)
    profile = PROFILES[profile_id]

    lines: List[str] = []
    lines.append('# Strategy Map')
    lines.append('')
    lines.append('## Board State')
    lines.append(f"- Current map: {extracted['situation']}")
    lines.append(f"- Victory condition: {extracted['goal']}")
    lines.append(f"- Loss condition: {_loss_condition(extracted['goal'], constraints, extracted['pressure'])}")
    if resources:
        lines.append(f"- Supply lines: {', '.join(resources)}")
    else:
        lines.append('- Supply lines: not fully specified, so protect time, clarity, and stamina as default resources.')
    if constraints:
        lines.append(f"- Contested ground: {', '.join(constraints)}")
    else:
        lines.append('- Contested ground: main friction point not fully specified.')
    lines.append(f"- Pressure source: {extracted['pressure']}")
    lines.append(f"- Time window: {extracted['time_window']}")
    lines.append('')
    lines.append('## Recommended Stance')
    lines.append(f"- Stance: {profile['label']}")
    lines.append(f"- Why now: {profile['summary']}")
    lines.append(f"- Framing guardrail: {template.splitlines()[0]}")
    lines.append('')
    lines.append('## Three-Phase Plan')
    lines.append(f"- Opening: {profile['opening']}")
    lines.append(f"- Midgame: {profile['midgame']}")
    lines.append(f"- Endgame: {profile['endgame']}")
    lines.append('')
    lines.append('## Decision Reminders')
    lines.append(f"- Protect: {profile['protect']}")
    lines.append(f"- Contest: {profile['contest']}")
    lines.append(f"- Let go: {profile['let_go']}")
    lines.append(f"- Likely misread: {profile['misread']}")
    return '\n'.join(lines)


def handle(args: Dict[str, Any]) -> Dict[str, str]:
    skill_name = args.get('skill_name', SKILL_SLUG) or SKILL_SLUG
    user_input = args.get('input', '')
    mode = args.get('mode', 'guide')
    meta = _load_skill_meta(skill_name)
    template = _load_prompt_template(skill_name)
    if mode == 'meta':
        return {'result': json.dumps(meta, ensure_ascii=False, indent=2)}
    if mode == 'prompt':
        return {'result': template}
    raw, data = _coerce_input(user_input)
    return {'result': _build_result(raw, data, template)}


if __name__ == '__main__':
    demo = {
        'situation': 'one week before an exam with too many unfinished review tasks',
        'goal': 'secure the highest-yield topics before exam day',
        'resources': '2 focused hours each morning, class notes',
        'constraints': 'low energy at night, family logistics',
        'resistance': 'panic and jumping between topics',
        'deadline': 'exam day next week',
    }
    print(json.dumps(handle({'skill_name': SKILL_SLUG, 'input': demo}), ensure_ascii=False, indent=2))
