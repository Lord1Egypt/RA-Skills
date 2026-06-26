#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'rpg-character-builder'
PROMPT_TEMPLATE = """Translate a real-life growth direction into a grounded RPG build.
Infer a main class, a secondary class, practical attributes, a build route, and 1 to 3 weekly upgrade actions. Keep the language vivid but realistic."""

ARCHETYPES = {
    'strategist': {
        'label': 'Strategist',
        'summary': 'Wins by reading the map clearly before spending effort.',
        'keywords': ['analysis', 'strategy', 'clarity', 'think', 'read', 'learn', 'research', 'plan', 'logic', 'ai'],
        'stats': ['Insight', 'Discipline'],
    },
    'builder': {
        'label': 'Builder',
        'summary': 'Turns ideas into reliable systems, structures, and repeatable output.',
        'keywords': ['build', 'ship', 'system', 'process', 'execute', 'routine', 'habit', 'organize', 'make'],
        'stats': ['Craft', 'Discipline'],
    },
    'guide': {
        'label': 'Guide',
        'summary': 'Levels up through teaching, support, and steady care for others.',
        'keywords': ['teach', 'help', 'support', 'family', 'parent', 'mentor', 'care', 'communicate', 'coach'],
        'stats': ['Influence', 'Resilience'],
    },
    'explorer': {
        'label': 'Explorer',
        'summary': 'Grows by curiosity, experimentation, and contact with new terrain.',
        'keywords': ['explore', 'curious', 'experiment', 'try', 'discover', 'adventure', 'novelty'],
        'stats': ['Insight', 'Resilience'],
    },
    'creator': {
        'label': 'Creator',
        'summary': 'Turns internal vision into expressive work that others can feel or use.',
        'keywords': ['write', 'design', 'create', 'story', 'art', 'expression', 'craft', 'content'],
        'stats': ['Craft', 'Influence'],
    },
}

STAT_KEYWORDS = {
    'Insight': ['analysis', 'learn', 'study', 'read', 'research', 'reflect', 'strategy', 'clarity', 'curious'],
    'Discipline': ['discipline', 'routine', 'consistency', 'execute', 'system', 'habit', 'finish', 'reliable'],
    'Resilience': ['calm', 'grit', 'recover', 'patient', 'steady', 'stamina', 'courage', 'endure'],
    'Influence': ['teach', 'guide', 'communicate', 'support', 'lead', 'connect', 'parent', 'coach'],
    'Craft': ['build', 'create', 'write', 'design', 'make', 'ship', 'practice', 'tool'],
}

ACTION_LIBRARY = {
    'Insight': 'Write one short note that names what season of growth you are actually in and what winning this month looks like.',
    'Discipline': 'Protect one repeatable 20-minute practice block on at least 4 days this week.',
    'Resilience': 'Add one recovery anchor to the week, such as a walk, stretch, or early stop rule before mental fatigue spills over.',
    'Influence': 'Explain your current build to one trusted person and ask for one concrete feedback question.',
    'Craft': 'Ship one small artifact this week, such as a note, checklist, outline, demo, or draft, instead of only thinking about it.',
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


def _choose_classes(raw: str, data: Dict[str, Any]) -> Tuple[str, str, str]:
    current_state = _pick(data, ['current_state', 'situation', '现状'])
    ideal_role = _pick(data, ['ideal_role', 'target_role', '理想角色'])
    values = ' '.join(_split_items(_pick(data, ['values', '价值观'])))
    strengths = ' '.join(_split_items(_pick(data, ['strengths', '优势'])))
    desired = ' '.join(_split_items(_pick(data, ['desired_skills', 'skills', '想练的能力'])))
    context = ' '.join([raw, current_state, ideal_role, values, strengths, desired]).lower()

    scores: Dict[str, int] = {name: 0 for name in ARCHETYPES}
    for name, config in ARCHETYPES.items():
        for keyword in config['keywords']:
            if keyword in context:
                scores[name] += 1
        if ideal_role and config['label'].lower() in ideal_role.lower():
            scores[name] += 2
    ranked = sorted(scores.items(), key=lambda item: (item[1], ARCHETYPES[item[0]]['label']), reverse=True)
    primary = ranked[0][0] if ranked[0][1] > 0 else 'strategist'
    secondary = next((name for name, _ in ranked[1:] if name != primary), 'builder')
    return primary, secondary, current_state or 'life context not fully specified'


def _score_stats(raw: str, data: Dict[str, Any], primary: str, secondary: str) -> Dict[str, int]:
    positives = ' '.join([
        raw,
        _pick(data, ['values', '价值观']),
        _pick(data, ['strengths', '优势']),
        _pick(data, ['desired_skills', 'skills', '想练的能力']),
    ]).lower()
    negatives = _pick(data, ['weaknesses', 'gaps', 'blockers', '短板']).lower()
    scores: Dict[str, int] = {}
    for stat, keywords in STAT_KEYWORDS.items():
        value = 2
        hits = sum(1 for keyword in keywords if keyword in positives)
        misses = sum(1 for keyword in keywords if keyword in negatives)
        value += min(hits, 2)
        value -= min(misses, 2)
        if stat in ARCHETYPES[primary]['stats']:
            value += 1
        if stat in ARCHETYPES[secondary]['stats']:
            value += 1
        scores[stat] = max(1, min(value, 5))
    return scores


def _hidden_talent(stats: Dict[str, int], strengths: List[str]) -> str:
    lowered_strengths = ' '.join(strengths).lower()
    for stat, score in sorted(stats.items(), key=lambda item: item[1], reverse=True):
        if score >= 4 and stat.lower() not in lowered_strengths:
            return stat
    return max(stats, key=stats.get)


def _misallocated_points(weaknesses: List[str], stats: Dict[str, int]) -> str:
    if weaknesses:
        return f"Do not ignore the stated weak spot, especially {weaknesses[0]}, while chasing a shiny side class."
    lowest = min(stats, key=stats.get)
    return f'Do not spend all your points on prestige moves while {lowest} is still the obvious bottleneck.'


def _weekly_actions(stats: Dict[str, int], desired_skills: List[str]) -> List[str]:
    ordered_stats = sorted(stats.items(), key=lambda item: item[1])
    actions: List[str] = []
    for stat, _ in ordered_stats[:3]:
        actions.append(ACTION_LIBRARY[stat])
    if desired_skills:
        actions[0] = f"Use your next small action to move `{desired_skills[0]}` from idea status into one visible practice rep."
    deduped: List[str] = []
    for action in actions:
        if action not in deduped:
            deduped.append(action)
    return deduped[:3]


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    primary, secondary, current_state = _choose_classes(raw, data)
    stats = _score_stats(raw, data, primary, secondary)
    strengths = _split_items(_pick(data, ['strengths', '优势']))
    weaknesses = _split_items(_pick(data, ['weaknesses', 'gaps', 'blockers', '短板']))
    desired_skills = _split_items(_pick(data, ['desired_skills', 'skills', '想练的能力']))
    values = _split_items(_pick(data, ['values', '价值观']))
    ideal_role = _pick(data, ['ideal_role', 'target_role', '理想角色'], 'not fully specified')

    main_class = ARCHETYPES[primary]
    sub_class = ARCHETYPES[secondary]
    hidden = _hidden_talent(stats, strengths)

    lines: List[str] = []
    lines.append('# Grounded RPG Build')
    lines.append('')
    lines.append('## Character Card')
    lines.append(f"- Main class: {main_class['label']}")
    lines.append(f"- Secondary class: {sub_class['label']}")
    lines.append(f"- Current world state: {current_state}")
    lines.append(f"- Target identity: {ideal_role}")
    if values:
        lines.append(f"- Value alignment: {', '.join(values)}")
    lines.append(f"- Build fantasy kept realistic: {main_class['summary']} {sub_class['summary']}")
    lines.append(f"- Build frame: {template.splitlines()[0]}")
    lines.append('')
    lines.append('## Attribute Points')
    for stat, score in stats.items():
        lines.append(f'- {stat}: {score}/5')
    if strengths:
        lines.append(f"- Current strengths: {', '.join(strengths)}")
    if weaknesses:
        lines.append(f"- Current bottlenecks: {', '.join(weaknesses)}")
    lines.append(f'- Hidden talent to lean into: {hidden}')
    lines.append('')
    lines.append('## Build Route')
    lines.append(f"- Current build: a {main_class['label']} core with {sub_class['label']} support.")
    if desired_skills:
        lines.append(f"- Next phase focus: train {', '.join(desired_skills[:2])} without abandoning your base class.")
    else:
        lowest = min(stats, key=stats.get)
        lines.append(f'- Next phase focus: stabilize {lowest} so the current strengths stop carrying the whole build alone.')
    lines.append(f"- Avoid misallocation: {_misallocated_points(weaknesses, stats)}")
    lines.append('')
    lines.append("## This Week's Level-Up Actions")
    for index, action in enumerate(_weekly_actions(stats, desired_skills), start=1):
        lines.append(f'{index}. {action}')
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
        'current_state': 'parent learning AI at home',
        'ideal_role': 'a calm strategist who can teach others',
        'values': 'growth, family, clarity',
        'strengths': ['analysis', 'care', 'curiosity'],
        'weaknesses': ['consistency', 'overthinking'],
        'desired_skills': ['shipping small projects', 'clear teaching'],
    }
    print(json.dumps(handle({'skill_name': SKILL_SLUG, 'input': demo}), ensure_ascii=False, indent=2))
