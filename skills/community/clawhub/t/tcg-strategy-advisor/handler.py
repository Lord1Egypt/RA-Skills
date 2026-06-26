#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'tcg-strategy-advisor'
PROMPT_TEMPLATE = """Identify the user's real win condition and map it to a stable TCG structure.
Cover main engine, draw or consistency, interaction, finishers, backup line, match tempo, and common greed traps. Do not pretend to know the live metagame."""

ARCHETYPES = {
    'aggro': {
        'label': 'Aggro / Tempo Pressure',
        'summary': 'Win before the opponent fully stabilizes.',
        'main_engine': 'Cheap threats, curve discipline, and pressure pieces that matter from turn one.',
        'draw': 'Light but efficient refill so the deck does not stall after the first wave.',
        'interaction': 'Low-cost removal, bounce, or combat tricks that preserve the lead.',
        'finish': 'Reach damage, burst turns, or sticky threats that convert a small gap into a win.',
        'backup': 'A small resilient package that keeps the clock running if the opener gets answered.',
        'early': 'Spend mana cleanly, establish the first clock, and force bad blocks or awkward answers.',
        'mid': 'Keep pressure high and trade only when it protects the clock.',
        'late': 'Count exact reach and avoid pretending the deck wants a twenty-turn game.',
        'curve': 'Bias the deck toward early turns. If too many cards cost four or more, the engine is lying about its identity.',
        'mistakes': [
            'Keeping slow hands because every card looks powerful.',
            'Adding too many cute top-end cards and ruining the early curve.',
            'Trading away pressure for value that the deck is not built to exploit long-term.',
        ],
    },
    'control': {
        'label': 'Control / Resource Denial',
        'summary': 'Survive, answer threats efficiently, and win after the opponent runs out of meaningful pressure.',
        'main_engine': 'Reliable answers, card advantage, and repeatable resource stabilization.',
        'draw': 'High-quality filtering, draw, or recursion so the deck keeps seeing the right half.',
        'interaction': 'Removal, counters, sweeps, and defensive tools sized for the expected pace.',
        'finish': 'A few durable closers, not a pile of expensive vanity cards.',
        'backup': 'Secondary value engines that still matter when the primary finisher is buried.',
        'early': 'Preserve life total and card parity without spending premium answers too loosely.',
        'mid': 'Trade at favorable rates and turn the game into a smaller decision tree.',
        'late': 'Lock the game with superior resources and finish with minimal exposure.',
        'curve': 'Respect the early defense slots. A control shell that cannot survive the first pressure wave is not a control deck yet.',
        'mistakes': [
            'Loading up on finishers while cutting early interaction.',
            'Using premium answers on low-value threats because of panic.',
            'Drawing cards without checking whether the deck still has time to cash them in.',
        ],
    },
    'combo': {
        'label': 'Combo / Engine Assembly',
        'summary': 'Assemble a specific interaction and convert it into a decisive swing or one-turn finish.',
        'main_engine': 'The exact pieces, tutors, or setup cards that enable the combo turn.',
        'draw': 'Filtering, tutoring, and redundancy that increase assembly consistency.',
        'interaction': 'Protection, stall tools, or selective removal that buy the needed setup window.',
        'finish': 'The actual combo conversion step, plus a clean explanation of how it ends the game.',
        'backup': 'A secondary fair plan so the deck does not auto-lose when one piece is missing.',
        'early': 'Find pieces, protect life total, and avoid wasting combo resources on low-value exchanges.',
        'mid': 'Sequence setup carefully and identify when to hold versus jam the engine.',
        'late': 'Either execute decisively or pivot into the backup line before dead draws pile up.',
        'curve': 'Redundancy matters more than flashy one-ofs. Every card should either find, protect, or convert the engine.',
        'mistakes': [
            'Adding too many fun side packages and lowering combo density.',
            'Keeping hands that have no setup path because one card looks exciting.',
            'Forgetting to define a backup line when the main combo is disrupted.',
        ],
    },
    'midrange': {
        'label': 'Midrange / Flexible Value',
        'summary': 'Win by playing efficient threats and answers that can switch roles across the game.',
        'main_engine': 'Flexible threats that matter when ahead or behind.',
        'draw': 'Moderate draw or recursion to stop the shell from running out of gas.',
        'interaction': 'Versatile answers that are rarely dead in hand.',
        'finish': 'A few sticky value closers that turn board control into inevitability.',
        'backup': 'Role-switch tools so the deck can become slightly faster or slower by matchup.',
        'early': 'Contest the board without overcommitting to one role too early.',
        'mid': 'Identify whether you are the beatdown or the value deck in this specific game.',
        'late': 'Close with sticky threats instead of hoarding cards forever.',
        'curve': 'The deck should have live plays across the whole curve. Too much top-end or too much cheap fluff will blur the plan.',
        'mistakes': [
            'Trying to include every strong standalone card and losing the deck’s center of gravity.',
            'Refusing to decide whether to race or trade in a given matchup.',
            'Treating flexible cards as a reason to skip real curve discipline.',
        ],
    },
    'ramp': {
        'label': 'Ramp / Top-End Conversion',
        'summary': 'Accelerate resources early, then land threats that invalidate smaller exchanges.',
        'main_engine': 'Mana acceleration, cost reduction, or resource engines that jump the curve.',
        'draw': 'Filtering that finds either acceleration early or payoffs later.',
        'interaction': 'Stall tools that buy the time needed to cash in the acceleration.',
        'finish': 'Top-end payoffs that swing the game hard enough to justify the slower start.',
        'backup': 'Mid-cost stabilizers so the deck is not dead when the dream draw misses.',
        'early': 'Prioritize acceleration only if the deck can survive the tempo loss.',
        'mid': 'Bridge from ramp pieces into stabilizers or immediate-impact threats.',
        'late': 'Make every top-end draw matter instead of playing expensive cards that do not swing the board.',
        'curve': 'The payoff cards must justify the weak early turns. If the finish is only medium, the ramp shell is overpaying for fantasy.',
        'mistakes': [
            'Stuffing the deck with huge cards and forgetting survival tools.',
            'Playing acceleration without enough meaningful payoffs.',
            'Assuming all big cards are finishers when some simply extend the game.',
        ],
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


def _to_int(value: Any, default: int = 0) -> int:
    if isinstance(value, int):
        return value
    text = _clean_text(value)
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else default


def _contains_any(text: str, keywords: List[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in keywords)


def _score_archetypes(raw: str, data: Dict[str, Any]) -> Tuple[Dict[str, int], str, int, str]:
    scores = {name: 0 for name in ARCHETYPES}
    declared = _pick(data, ['archetype', 'style', 'plan', '套路', '风格'])
    win_condition = _pick(data, ['win_condition', 'goal', 'victory_condition', 'how_to_win', '胜利条件'])
    core = _pick(data, ['core_components', 'core_cards', 'engine', 'key_cards', '核心组件'])
    risks = _pick(data, ['risks', 'problems', 'consistency_problem', '担忧'])
    turns = _to_int(_pick(data, ['turns_to_win', 'key_turn', 'speed', '启动回合', '回合']), 0)
    game_name = _pick(data, ['game', 'title', 'tcg', '游戏'])
    context = ' '.join([raw, declared, win_condition, core, risks, game_name]).lower()

    if _contains_any(context, ['aggro', 'tempo', 'rush', 'pressure', 'fast', 'beatdown', '快攻', '抢节奏']):
        scores['aggro'] += 5
    if _contains_any(context, ['control', 'stall', 'deny', 'removal', 'counter', 'grind', '控制', '拖后期']):
        scores['control'] += 5
    if _contains_any(context, ['combo', 'assemble', 'engine', 'synergy', 'loop', 'otk', '连招', '组合技']):
        scores['combo'] += 5
    if _contains_any(context, ['midrange', 'flexible', 'value', 'board-based', 'mid game', '中速', '价值']):
        scores['midrange'] += 4
    if _contains_any(context, ['ramp', 'mana', 'big threat', 'top end', 'accelerate', '资源积累', '跳费']):
        scores['ramp'] += 5

    if turns:
        if turns <= 4:
            scores['aggro'] += 3
        elif turns <= 6:
            scores['midrange'] += 2
            scores['combo'] += 1
        else:
            scores['control'] += 2
            scores['ramp'] += 2
            scores['combo'] += 1

    if _contains_any(context, ['draw', 'filter', 'consistency', 'mulligan', '过牌', '稳定']):
        scores['combo'] += 1
        scores['control'] += 1
        scores['midrange'] += 1
    if _contains_any(context, ['protect', 'backup line', 'fallback', 'secondary plan', '保护', '备用方案']):
        scores['combo'] += 1
        scores['control'] += 1
    if all(score == 0 for score in scores.values()):
        scores['midrange'] = 2
        scores['control'] = 1

    return scores, win_condition or 'not fully specified', turns, game_name or 'generic TCG / CCG context'


def _rank_archetypes(scores: Dict[str, int]) -> List[Tuple[str, int]]:
    return sorted(scores.items(), key=lambda item: (item[1], ARCHETYPES[item[0]]['label']), reverse=True)


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    scores, win_condition, turns, game_name = _score_archetypes(raw, data)
    profile_id = _rank_archetypes(scores)[0][0]
    profile = ARCHETYPES[profile_id]

    lines: List[str] = []
    lines.append('# TCG Structure Review')
    lines.append('')
    lines.append('## Strategy Identity')
    lines.append(f"- Profile: {profile['label']}")
    lines.append(f"- Core plan: {profile['summary']}")
    lines.append(f'- Stated win condition: {win_condition}')
    if turns:
        lines.append(f'- Expected key turn: around turn {turns}')
    else:
        lines.append('- Expected key turn: not specified, so the shell is inferred from the stated role and keywords.')
    lines.append(f'- Context read: {game_name}')
    lines.append(f"- Guardrail: {template.splitlines()[0]}")
    lines.append('')
    lines.append('## Build Structure')
    lines.append(f"- Main engine: {profile['main_engine']}")
    lines.append(f"- Draw / consistency: {profile['draw']}")
    lines.append(f"- Interaction: {profile['interaction']}")
    lines.append(f"- Finishers: {profile['finish']}")
    lines.append(f"- Backup plan: {profile['backup']}")
    lines.append(f"- Curve reminder: {profile['curve']}")
    lines.append('')
    lines.append('## Match Tempo')
    lines.append(f"- Early game: {profile['early']}")
    lines.append(f"- Mid game: {profile['mid']}")
    lines.append(f"- Late game: {profile['late']}")
    lines.append('')
    lines.append('## Common Mistakes')
    for item in profile['mistakes']:
        lines.append(f'- {item}')
    lines.append('')
    lines.append('## Transferable Resource Lesson')
    lines.append('- Build around the win condition first, then fund consistency, then add interaction, then cut greed.')
    lines.append('- If a card does not help the main plan, the backup plan, or the survival window, it is probably a luxury slot.')
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
        'archetype': 'combo',
        'win_condition': 'assemble two engine pieces and protect them',
        'turns_to_win': 6,
        'core_components': 'engine piece A, engine piece B',
    }
    print(json.dumps(handle({'skill_name': SKILL_SLUG, 'input': demo}), ensure_ascii=False, indent=2))
