#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'quest-chain-decomposer'
PROMPT_TEMPLATE = """Turn a fuzzy goal into a quest chain.
Focus on the finish line, prerequisite and waiting nodes, explicit Definition of Done, a starter trio that can begin today, and reroute rules when blockers appear."""

CATEGORY_RULES = {
    'learning': ['learn', 'study', 'exam', 'course', 'practice', 'essay', 'homework', '读', '学', '考试', '作业'],
    'admin': ['apply', 'application', 'form', 'document', 'visa', 'register', 'appointment', 'tax', '申请', '材料', '报名'],
    'organize': ['clean', 'organize', 'declutter', 'sort', 'pack', '整理', '收纳', '家务'],
}

CATEGORY_BLUEPRINTS = {
    'learning': [
        {
            'title': 'Quest 1, define the learning win',
            'objective': 'Turn the goal into one visible proof of learning for {goal}.',
            'dod': 'A concrete proof exists, such as one solved set, one outline, one mock answer, or one finished page.',
            'trap': 'Staying in broad research mode instead of choosing the smallest proof.',
        },
        {
            'title': 'Quest 2, gather only the minimum materials',
            'objective': 'Pick the exact sources, examples, or tools needed for the first learning sprint.',
            'dod': 'The minimum study pack is listed and opened, with obvious extras parked for later.',
            'trap': 'Collecting ten resources when two would unlock the next action.',
        },
        {
            'title': 'Quest 3, produce a first practice artifact',
            'objective': 'Create the first draft, problem set, recap note, or rehearsal artifact.',
            'dod': 'A rough but real artifact exists and can be reviewed.',
            'trap': 'Waiting to feel ready before attempting a first pass.',
        },
        {
            'title': 'Quest 4, review gaps and ship the next version',
            'objective': 'Check weak spots, patch the highest-value gap, and submit or store the final version.',
            'dod': 'The deliverable is submitted, stored, or scheduled for the next iteration with one clear follow-up.',
            'trap': 'Polishing forever instead of closing the loop.',
        },
    ],
    'admin': [
        {
            'title': 'Quest 1, define the exact requirement',
            'objective': 'Name what must be submitted, confirmed, or approved for {goal}.',
            'dod': 'A one-line requirement summary exists with deadline and owner.',
            'trap': 'Starting forms before knowing the finish condition.',
        },
        {
            'title': 'Quest 2, gather required documents and facts',
            'objective': 'Collect IDs, receipts, screenshots, contact details, and missing facts.',
            'dod': 'All must-have materials are ready or each missing item has an owner and follow-up date.',
            'trap': 'Opening the submission flow with missing proof.',
        },
        {
            'title': 'Quest 3, complete the submission path',
            'objective': 'Fill the form, send the email, book the slot, or file the request.',
            'dod': 'The request is fully submitted and a confirmation artifact exists.',
            'trap': 'Leaving the process half-finished without proof.',
        },
        {
            'title': 'Quest 4, confirm and archive the result',
            'objective': 'Verify status, record the confirmation, and set the next follow-up if needed.',
            'dod': 'Status is checked and the proof is stored in an easy-to-find place.',
            'trap': 'Assuming it is done before receiving confirmation.',
        },
    ],
    'organize': [
        {
            'title': 'Quest 1, define the done line',
            'objective': 'Choose the exact space, list, or category that counts as complete for {goal}.',
            'dod': 'One bounded scope is selected, such as one shelf, one folder, or one drawer.',
            'trap': 'Trying to reorganize the whole world at once.',
        },
        {
            'title': 'Quest 2, sort by category and friction',
            'objective': 'Group items into keep, move, process, and discard buckets.',
            'dod': 'Every item in the current scope has a temporary category.',
            'trap': 'Rearranging clutter without deciding what it is.',
        },
        {
            'title': 'Quest 3, clear the highest-friction batch',
            'objective': 'Finish the most valuable processing batch first.',
            'dod': 'One real area is visibly clearer and a follow-up batch is queued.',
            'trap': 'Stopping after sorting without completing a batch.',
        },
        {
            'title': 'Quest 4, reset and maintain',
            'objective': 'Label where things go and define a small maintenance rule.',
            'dod': 'The space is reset and one rule exists to stop the clutter from respawning.',
            'trap': 'Creating a one-day clean space with no maintenance rule.',
        },
    ],
    'general': [
        {
            'title': 'Quest 1, define the mission',
            'objective': 'Describe the smallest visible outcome that counts as success for {goal}.',
            'dod': 'The mission has one sentence, one owner, and one visible finish line.',
            'trap': 'Keeping the goal abstract or motivational instead of concrete.',
        },
        {
            'title': 'Quest 2, unlock prerequisites',
            'objective': 'List missing inputs, approvals, tools, and decisions needed before execution.',
            'dod': 'Every obvious blocker is either resolved, delegated, or parked as a waiting node.',
            'trap': 'Mistaking dependency confusion for lack of motivation.',
        },
        {
            'title': 'Quest 3, build the first shippable piece',
            'objective': 'Produce the first usable draft, checklist, or working version.',
            'dod': 'A real artifact exists and can be reviewed by you or someone else.',
            'trap': 'Thinking about the work longer than it takes to create version one.',
        },
        {
            'title': 'Quest 4, review and close the loop',
            'objective': 'Check quality, submit, communicate status, and define the next checkpoint if needed.',
            'dod': 'The artifact is shipped or parked with a precise next step and date.',
            'trap': 'Letting a near-finished task drift in limbo.',
        },
    ],
}

STARTER_ACTIONS = {
    'learning': [
        'Write one sentence that defines the exact proof of learning you want today.',
        'Open the minimum source set and close unrelated tabs or materials.',
        'Create the first rough artifact immediately, even if it is incomplete.',
    ],
    'admin': [
        'Write the exact submission or approval you need in one line.',
        'List the must-have documents and mark which one is still missing.',
        'Start the form, draft email, or booking flow until the next real blocker appears.',
    ],
    'organize': [
        'Choose one bounded zone instead of the whole category.',
        'Set out four temporary buckets: keep, move, process, discard.',
        'Clear one visible batch completely before touching the next area.',
    ],
    'general': [
        'Write the finish line in one sentence that someone else could verify.',
        'List the top dependency or uncertainty blocking action.',
        'Create the first real artifact, even if it is only version 0.1.',
    ],
}


def _load_skill_meta(skill_name):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as handle:
        content = handle.read()
    match = re.search(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL | re.MULTILINE)
    meta = {}
    if match:
        for line in match.group(1).splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip()
    meta['skill_name'] = skill_name or meta.get('name', SKILL_SLUG)
    return meta


def _load_prompt_template(skill_name):
    return PROMPT_TEMPLATE


def _clean_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _parse_text_map(raw: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for line in raw.splitlines():
        if re.search(r'[:：]', line):
            key, value = re.split(r'[:：]', line, maxsplit=1)
            normalized = re.sub(r'\s+', '_', key.strip().lower())
            data[normalized] = value.strip()
    return data


def _coerce_input(user_input: Any) -> Tuple[str, Dict[str, Any]]:
    if isinstance(user_input, dict):
        return json.dumps(user_input, ensure_ascii=False), dict(user_input)
    raw = _clean_text(user_input)
    if raw.startswith('{') and raw.endswith('}'):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return raw, parsed
        except json.JSONDecodeError:
            pass
    return raw, _parse_text_map(raw)


def _pick(data: Dict[str, Any], keys: List[str], default: str = '') -> str:
    for key in keys:
        if key in data:
            text = _clean_text(data.get(key))
            if text:
                return text
    return default


def _first_sentence(raw: str) -> str:
    cleaned = raw.strip()
    if not cleaned:
        return ''
    parts = re.split(r'[\n。.!?！？]', cleaned)
    for part in parts:
        part = part.strip(' -•')
        if part:
            return part
    return ''


def _split_values(value: Any) -> List[str]:
    if isinstance(value, list):
        return [_clean_text(item) for item in value if _clean_text(item)]
    text = _clean_text(value)
    if not text:
        return []
    items = [re.sub(r'^[\-•\d.\s]+', '', part).strip() for part in re.split(r'[\n,;，；]+', text)]
    return [item for item in items if item]


def _detect_category(goal: str, raw: str) -> str:
    combined = f'{goal} {raw}'.lower()
    for category, words in CATEGORY_RULES.items():
        if any(word in combined for word in words):
            return category
    return 'general'


def _waiting_node(blockers: List[str]) -> str:
    lowered = ' '.join(blockers).lower()
    if any(word in lowered for word in ['wait', 'waiting', 'approval', 'reply', 'feedback', 'teacher', 'review', '审批', '回复', '配合']):
        return 'Waiting node: track the external dependency, set a follow-up date, and define parallel work that can continue while you wait.'
    if blockers:
        return 'Blocker node: turn each blocker into either a resolved task, a delegated task, or a clearly parked item with the next check date.'
    return ''


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    goal = _pick(data, ['goal', 'objective', 'project', 'task', 'mission'], _first_sentence(raw) or 'Complete the current goal')
    deadline = _pick(data, ['deadline', 'due', 'timebox', 'date'], 'No explicit deadline provided')
    success_definition = _pick(
        data,
        ['success_definition', 'success', 'definition_of_done', 'done', 'deliverable'],
        f'A visible, reviewable deliverable exists for {goal}.',
    )
    resources = _split_values(data.get('resources', data.get('resource', '')))
    blockers = _split_values(data.get('blockers', data.get('blocker', data.get('constraints', ''))))
    category = _detect_category(goal, raw)
    steps = CATEGORY_BLUEPRINTS[category]
    starter_actions = STARTER_ACTIONS[category]
    waiting_note = _waiting_node(blockers)

    lines: List[str] = []
    lines.append('# Quest Chain Map')
    lines.append('')
    lines.append('## Main Quest Objective')
    lines.append(f'- Goal: {goal}')
    lines.append(f'- Success definition: {success_definition}')
    lines.append(f'- Deadline or timebox: {deadline}')
    lines.append(f'- Planning frame: {template.splitlines()[0]}')
    if resources:
        lines.append(f"- Useful resources: {', '.join(resources)}")
    else:
        lines.append('- Useful resources: Start with the minimum tools needed for the next artifact.')
    if blockers:
        lines.append(f"- Visible blockers: {', '.join(blockers)}")
    else:
        lines.append('- Visible blockers: None stated, so treat hidden ambiguity as the first thing to test.')
    lines.append('')
    lines.append('## Quest Chain Map')
    for index, step in enumerate(steps, 1):
        depends = 'None' if index == 1 else f'Quest {index - 1}'
        lines.append(f"{index}. **{step['title']}**")
        lines.append(f'   - Depends on: {depends}')
        lines.append(f"   - Objective: {step['objective'].format(goal=goal)}")
        lines.append(f"   - Failure trap: {step['trap']}")
    lines.append('- Parallel branch: Prepare support material, checklist, or follow-up messages while the main chain is moving.')
    if waiting_note:
        lines.append(f'- {waiting_note}')
    lines.append('')
    lines.append('## Definition of Done by Step')
    for step in steps:
        lines.append(f"- **{step['title']}**: {step['dod']}")
    lines.append('')
    lines.append('## Starter Trio')
    for index, action in enumerate(starter_actions, 1):
        lines.append(f'{index}. {action}')
    lines.append('')
    lines.append('## Reroute Rules')
    lines.append('- If the goal is still fuzzy after Quest 1, pause decomposition and rewrite the mission as one visible deliverable.')
    lines.append('- If an external dependency stalls the chain, move it into a waiting node with a date, owner, and parallel fallback task.')
    lines.append('- If you keep researching instead of producing, force the next action to create a draft, checklist, or proof artifact in under 25 minutes.')
    lines.append('- If energy drops, keep the main quest but shrink the next step instead of inventing a brand-new plan.')
    return '\n'.join(lines)


def handle(args):
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
