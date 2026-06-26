#!/usr/bin/env python3
"""Roundtable controller.

Security posture by design:
- No outbound network usage.
- No subprocess execution.
- User input is treated as plain text only.
- File I/O is scoped to the skill directory and runtime state file.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
CHARACTER_POOL_PATH = SKILL_ROOT / 'data' / 'character_pool.json'
CHARACTER_REGISTRY_PATH = SKILL_ROOT / 'data' / 'character_registry.json'
STATE_FILE = SKILL_ROOT / 'runtime' / 'roundtable_state.json'

RARITY_STARS = {
    '史诗': '★★★',
    '传说': '★★',
    '精英': '★',
}
CHOICE_ALIASES = {
    'A': {'A', 'a', '认同A', '认同a', '认同第一位', '同意第一位', '赞同第一位'},
    'B': {'B', 'b', '认同B', '认同b', '认同第二位', '同意第二位', '赞同第二位'},
    'C': {'C', 'c', '认同C', '认同c', '认同第三位', '同意第三位', '赞同第三位'},
    'D': {'D', 'd', '沉默', '继续', '继续讨论', '让讨论继续', '继续聊', '接着聊', '继续吧'},
    'E': {'E', 'e', '我有另外的话要说', '我有别的话要说', '我想说别的', '我想插一句', '另外说一句', '补充一句'},
}
HELP_PATTERNS = ('这是干嘛', '怎么用', '如何使用', '怎么玩', '玩法', 'help')
RESET_EXACT_PATTERNS = {'重置', 'reset', '清空', '清空状态', '重新来过'}
STATUS_EXACT_PATTERNS = {'当前状态', 'status', '进度', '查看状态'}
RESHOW_CANDIDATES_PATTERNS = (
    '候选人',
    '候选人物',
    '候选列表',
    '候选池',
    '重发候选',
    '再发候选',
    '给我候选',
    '把名单发我',
)
START_PREFIXES = (
    '启动圆桌派',
    '用圆桌讨论',
    '启动圆桌讨论',
    '开始讨论',
    '启动技能',
    '开始技能',
    '启动',
    '开始',
)


def ensure_path_in_skill_root(path: Path) -> None:
    root = SKILL_ROOT.resolve()
    target = path.resolve()
    if target != root and root not in target.parents:
        raise RuntimeError(f'Unsafe path outside skill root: {target}')


def validate_runtime_paths() -> None:
    # Explicit path guard to make audit expectations executable.
    for p in (CHARACTER_POOL_PATH, CHARACTER_REGISTRY_PATH, STATE_FILE):
        ensure_path_in_skill_root(p)


def now_iso() -> str:
    return datetime.now().isoformat()


def default_state() -> Dict[str, Any]:
    return {
        'status': 'idle',
        'question': None,
        'candidate_pool': [],
        'participants': [],
        'current_round': 0,
        'max_rounds': 0,
        'user_interventions': [],
        'finished': False,
        'discussion_content': [],
        'last_user_action': None,
        'pending_user_input_type': 'question',
        'created_at': None,
        'updated_at': None,
    }


def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    return default_state()


def save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state['updated_at'] = now_iso()
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def reset_state() -> Dict[str, Any]:
    state = default_state()
    save_state(state)
    return state


def load_character_pool() -> List[Dict[str, Any]]:
    data = json.loads(CHARACTER_POOL_PATH.read_text(encoding='utf-8'))
    return data.get('characters', [])


def load_registry() -> Tuple[Dict[str, Dict[str, Any]], Dict[str, str], Dict[str, str]]:
    data = json.loads(CHARACTER_REGISTRY_PATH.read_text(encoding='utf-8'))
    records = data.get('records', [])
    by_id = {r['character_id']: r for r in records}
    alias_index = data.get('alias_index', {})
    directory_index = data.get('directory_index', {})
    return by_id, alias_index, directory_index


def canonicalize_candidate(char: Dict[str, Any], registry_by_id: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    rec = registry_by_id.get(char['character_id'])
    if not rec:
        return None
    return {
        'display_name': rec['display_name'],
        'character_id': rec['character_id'],
        'rarity': rec.get('rarity', char.get('rarity', '精英')),
        'fit_hint': char.get('fit_hint') or rec.get('fit_hint', ''),
    }


def draw_candidates(characters: List[Dict[str, Any]], count: int = 10) -> List[Dict[str, Any]]:
    registry_by_id, _, _ = load_registry()
    pool: List[Dict[str, Any]] = []
    seen_registry_ids = set()
    for char in characters:
        canonical = canonicalize_candidate(char, registry_by_id)
        if not canonical:
            continue
        cid = canonical['character_id']
        if cid in seen_registry_ids:
            continue
        seen_registry_ids.add(cid)
        pool.append(canonical)

    sampled = random.sample(pool, k=min(count, len(pool)))
    candidates: List[Dict[str, Any]] = []
    for idx, chosen in enumerate(sampled, start=1):
        candidates.append({
            'index': idx,
            'display_name': chosen['display_name'],
            'character_id': chosen['character_id'],
            'rarity': chosen['rarity'],
            'fit_hint': chosen.get('fit_hint', ''),
        })
    return candidates


def format_candidate_pool(candidates: List[Dict[str, Any]]) -> str:
    lines = ['选 3 位你最想听的人物，我来组织讨论：', '']
    for c in candidates:
        rarity = c.get('rarity', '精英')
        stars = RARITY_STARS.get(rarity, '★')
        lines.append(
            f"{c['index']}. {c['display_name']}（{rarity}{stars}）：{c['fit_hint']}"
        )
    lines.extend(['', '请直接回复 3 位人物名字或者序号。'])
    return '\n'.join(lines)


def clean_message(text: str) -> str:
    text = text.strip()
    text = re.sub(r'^/roundtable-pai\s*', '', text, flags=re.I)
    for prefix in START_PREFIXES:
        if text.startswith(prefix):
            text = text[len(prefix):].lstrip('：:，,。 ').strip()
            break
    return text


def is_help_message(text: str) -> bool:
    t = text.lower()
    return any(p in t for p in HELP_PATTERNS)


def is_reset_message(text: str) -> bool:
    t = text.strip().lower()
    return t in RESET_EXACT_PATTERNS


def is_status_message(text: str) -> bool:
    t = text.strip().lower()
    return t in STATUS_EXACT_PATTERNS


def is_reshow_candidates_message(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    return any(p in t for p in RESHOW_CANDIDATES_PATTERNS)


def render_help() -> str:
    return '它用来把你的问题交给 3 位人物展开一场有来有回的讨论。\n你先提问题，我给候选人物，你选 3 位，我再开始。'


def render_status(state: Dict[str, Any]) -> str:
    if state['status'] == 'idle':
        return '现在还没有进行中的讨论。你直接发一个问题，我就先给你候选人物。'
    lines = ['当前还在这场讨论里：']
    if state.get('question'):
        lines.append(f"- 问题：{state['question']}")
    if state.get('participants'):
        lines.append(f"- 人物：{'、'.join(state['participants'])}")
    if state.get('current_round'):
        lines.append(f"- 轮次：第 {state['current_round']} 轮 / 共 {state['max_rounds']} 轮")
    pending = state.get('pending_user_input_type', 'question')
    pending_map = {
        'question': '发一个新问题',
        'participant_pick': '从候选池里选 3 位人物',
        'user_choice': '选 A / B / C / D / E，或者直接说你的看法',
        'free_speech': '把你另外想说的话直接说出来',
    }
    lines.append(f"- 下一步：{pending_map.get(pending, pending)}")
    return '\n'.join(lines)


def normalize_pick_input(user_input: str, candidate_pool: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
    registry_by_id, alias_index, directory_index = load_registry()
    token_candidates = re.split(r'[\s,，、/|；;]+', user_input)
    token_candidates = [t for t in token_candidates if t]
    numbers = re.findall(r'\d+', user_input)
    selections: List[str] = []

    # 先解析序号
    if numbers:
        for n in numbers:
            idx = int(n)
            if 1 <= idx <= len(candidate_pool):
                selections.append(candidate_pool[idx - 1]['character_id'])

    # 再解析名字/别名/目录名
    if token_candidates:
        candidate_lookup = {}
        for c in candidate_pool:
            candidate_lookup[c['character_id']] = c
            candidate_lookup[c['display_name']] = c
        for token in token_candidates:
            for c in candidate_pool:
                rec = registry_by_id.get(c['character_id'], {})
                aliases = set(rec.get('aliases', []))
                aliases.add(rec.get('display_name', ''))
                aliases.add(rec.get('canonical_name', ''))
                aliases.add(rec.get('directory_name', ''))
                alias_hit = token in aliases or alias_index.get(token) == c['character_id'] or directory_index.get(token) == c['character_id']
                substring_hit = token == c['display_name'] or c['display_name'] in user_input
                if alias_hit or substring_hit:
                    selections.append(c['character_id'])
                    break

    ordered_unique: List[str] = []
    for cid in selections:
        if cid not in ordered_unique:
            ordered_unique.append(cid)
    if len(ordered_unique) != 3:
        return None

    id_to_candidate = {c['character_id']: c for c in candidate_pool}
    if not all(cid in id_to_candidate for cid in ordered_unique):
        return None
    return [id_to_candidate[cid] for cid in ordered_unique]


def parse_choice(user_input: str) -> Optional[str]:
    stripped = user_input.strip()
    if not stripped:
        return None
    upper = stripped.upper()
    if upper in CHOICE_ALIASES:
        return upper
    # 单字母或常见前缀
    letter = re.match(r'^([A-Ea-e])(?:\b|[：:：\s]|$)', stripped)
    if letter:
        return letter.group(1).upper()
    for key, aliases in CHOICE_ALIASES.items():
        if stripped in aliases or any(alias in stripped for alias in aliases if len(alias) >= 2):
            return key
    return None


def initialize_discussion_from_pick(state: Dict[str, Any], selected_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    state['participants'] = [c['display_name'] for c in selected_candidates]
    state['status'] = 'awaiting_user_choice'
    state['pending_user_input_type'] = 'user_choice'
    state['current_round'] = 1
    state['max_rounds'] = random.randint(4, 7)
    state['finished'] = False
    state['last_user_action'] = 'pick_participants'
    return state


def ordinal_cn(n: int) -> str:
    mapping = {1:'第一轮',2:'第二轮',3:'第三轮',4:'第四轮',5:'第五轮',6:'第六轮',7:'第七轮'}
    return mapping.get(n, f'第{n}轮')


def discussion_round_payload(state: Dict[str, Any], intervention_type: Optional[str] = None, intervention_content: Optional[str] = None, opening_round: bool = False) -> str:
    lines = [
        'STATUS: DISCUSSION_ROUND',
        f"ROUND_TITLE: {ordinal_cn(state['current_round'])}",
        f"CURRENT_ROUND: {state['current_round']}",
        f"MAX_ROUNDS: {state['max_rounds']}",
        f"QUESTION: {state['question']}",
        f"PARTICIPANTS: {'、'.join(state['participants'])}",
    ]
    if intervention_type and intervention_content:
        lines.append(f"USER_INTERVENTION_TYPE: {intervention_type}")
        lines.append(f"USER_INTERVENTION_CONTENT: {intervention_content}")
    else:
        lines.append('USER_INTERVENTION_TYPE: none')
    lines.extend([
        'MODEL_INSTRUCTIONS:',
        '- 第一次进入讨论正文前，先给一句清晰免责声明：以下内容为基于公开资料整理的人物视角模拟，不代表人物本人真实发言。',
        '- 只生成当前这一轮，不得继续写下一轮。',
        '- 第一轮可以在标题前加 1 到 2 句极短开场；非第一轮不要重新开场。',
        '- 每位人物本轮最多发言 1 次，确保能一眼听出是谁在说话。',
        '- 若有 USER_INTERVENTION_CONTENT，必须自然吸收进本轮讨论。',
        '- 本轮正文结束后，必须按本轮三位人物的发言，生成下面这组用户参与块，然后立刻停止。',
        '- A/B/C 分别对应本轮三位人物，必须写出人物名字和一句话概括其本轮核心观点。',
        '- D 固定写成：沉默，让讨论继续。',
        '- E 固定写成：我有另外的话要说。',
        'USER_OPTIONS_BLOCK_TEMPLATE:',
        '---',
        '请选择：',
        'A. 认同[人物A名字]——[一句话概括人物A本轮核心观点]',
        'B. 认同[人物B名字]——[一句话概括人物B本轮核心观点]',
        'C. 认同[人物C名字]——[一句话概括人物C本轮核心观点]',
        'D. 沉默，让讨论继续',
        'E. 我有另外的话要说',
    ])
    return '\n'.join(lines)


def final_conclusion_payload(state: Dict[str, Any], trigger_reason: str) -> str:
    lines = [
        'STATUS: FINAL_CONCLUSION',
        f"QUESTION: {state['question']}",
        f"PARTICIPANTS: {'、'.join(state['participants'])}",
        f"TRIGGER_REASON: {trigger_reason}",
        'MODEL_INSTRUCTIONS:',
        '- 先用 1 到 2 句自然散场，把话收一收。',
        '- 然后只输出以下 6 个字段，不要额外再起标题。',
        '- 不要再补新一轮讨论。',
        'FIELDS:',
        '关键共识',
        '最大分歧',
        '当前最优建议',
        '这个建议成立的前提',
        '最危险的误判点',
        '给你的一条下一步动作',
    ]
    return '\n'.join(lines)


def start_new_discussion(question: str) -> str:
    state = default_state()
    state['status'] = 'awaiting_participant_pick'
    state['question'] = question
    state['pending_user_input_type'] = 'participant_pick'
    state['created_at'] = now_iso()
    state['candidate_pool'] = draw_candidates(load_character_pool(), 10)
    state['last_user_action'] = 'start_question'
    save_state(state)
    return format_candidate_pool(state['candidate_pool'])


def handle_pick(state: Dict[str, Any], user_message: str) -> str:
    selected = normalize_pick_input(user_message, state['candidate_pool'])
    if not selected:
        return '这 3 位里有角色不在当前候选池中。请直接从刚才展示的 10 位人物里重新选 3 位，可以回名字，也可以回序号。'
    initialize_discussion_from_pick(state, selected)
    save_state(state)
    return discussion_round_payload(state, opening_round=True)


def advance_round_or_finish(state: Dict[str, Any], trigger_reason: str, intervention_type: Optional[str] = None, intervention_content: Optional[str] = None) -> str:
    if state['current_round'] >= state['max_rounds']:
        state['finished'] = True
        state['status'] = 'finished'
        state['pending_user_input_type'] = 'question'
        state['last_user_action'] = trigger_reason
        save_state(state)
        return final_conclusion_payload(state, '达到最大轮数，自动收束')

    state['current_round'] += 1
    state['status'] = 'awaiting_user_choice'
    state['pending_user_input_type'] = 'user_choice'
    state['last_user_action'] = trigger_reason
    save_state(state)
    return discussion_round_payload(state, intervention_type, intervention_content)


def handle_user_choice(state: Dict[str, Any], user_message: str) -> str:
    choice = parse_choice(user_message)
    if choice == 'A':
        state['user_interventions'].append({'round': state['current_round'], 'type': 'agree', 'slot': 'A', 'timestamp': now_iso()})
        return advance_round_or_finish(state, 'agree_A', 'agree', 'A')
    if choice == 'B':
        state['user_interventions'].append({'round': state['current_round'], 'type': 'agree', 'slot': 'B', 'timestamp': now_iso()})
        return advance_round_or_finish(state, 'agree_B', 'agree', 'B')
    if choice == 'C':
        state['user_interventions'].append({'round': state['current_round'], 'type': 'agree', 'slot': 'C', 'timestamp': now_iso()})
        return advance_round_or_finish(state, 'agree_C', 'agree', 'C')
    if choice == 'D':
        state['user_interventions'].append({'round': state['current_round'], 'type': 'silent_continue', 'timestamp': now_iso()})
        return advance_round_or_finish(state, 'silent_continue', 'silent', 'D')
    if choice == 'E':
        state['user_interventions'].append({'round': state['current_round'], 'type': 'request_other_words', 'timestamp': now_iso()})
        state['status'] = 'awaiting_free_speech'
        state['pending_user_input_type'] = 'free_speech'
        state['last_user_action'] = 'vote_E'
        save_state(state)
        return '好，你直接把另外想说的话说出来。'

    # 没选 A-E，默认视为“我有另外的话要说”
    state['user_interventions'].append({'round': state['current_round'], 'type': 'free_speech', 'content': user_message, 'timestamp': now_iso()})
    return advance_round_or_finish(state, 'natural_other_words', 'free_speech', user_message)


def handle_followup_input(state: Dict[str, Any], user_message: str) -> str:
    pending = state.get('pending_user_input_type')
    if pending == 'free_speech':
        state['user_interventions'].append({'round': state['current_round'], 'type': 'free_speech', 'content': user_message, 'timestamp': now_iso()})
        return advance_round_or_finish(state, 'free_speech_submitted', 'free_speech', user_message)
    return handle_user_choice(state, user_message)


def route_message(raw_message: str) -> str:
    user_message = clean_message(raw_message)
    state = load_state()

    if not user_message:
        return render_help()
    if is_help_message(user_message):
        return render_help()
    if is_reset_message(user_message):
        reset_state()
        return '已重置。你现在直接发一个新问题，我就重新给你候选人物。'
    if is_status_message(user_message):
        return render_status(state)

    # 兼容旧命令
    lowered = user_message.lower()
    if lowered.startswith('start '):
        return start_new_discussion(user_message[6:].strip())
    if lowered.startswith('pick '):
        state = load_state()
        if state['status'] != 'awaiting_participant_pick':
            return '当前不是选人阶段。你可以直接发一个新问题，或者继续眼前这场讨论。'
        return handle_pick(state, user_message[5:].strip())
    if lowered == 'continue':
        state = load_state()
        if state['status'] == 'awaiting_user_choice':
            return handle_user_choice(state, 'D')
        if state['status'] in {'awaiting_free_speech'}:
            return '你先把想说的话发出来，我再把它送进下一轮讨论。'
        if state['status'] == 'awaiting_participant_pick':
            return '你先从刚才的 10 位候选人物里选 3 位。'
    if lowered.startswith('vote '):
        state = load_state()
        return handle_user_choice(state, user_message[5:].strip())
    if lowered.startswith('say '):
        state = load_state()
        return handle_followup_input(state, user_message[4:].strip())

    if state['status'] in {'idle', 'finished'}:
        return start_new_discussion(user_message)
    if state['status'] == 'awaiting_participant_pick':
        if is_reshow_candidates_message(user_message):
            if state.get('candidate_pool'):
                return format_candidate_pool(state['candidate_pool'])
            return '我这边候选池暂时不可用。你直接发一个新问题，我会重新给你候选人物。'
        return handle_pick(state, user_message)
    if state['status'] == 'awaiting_user_choice':
        return handle_user_choice(state, user_message)
    if state['status'] in {'awaiting_free_speech'}:
        return handle_followup_input(state, user_message)
    return '我这边状态有点乱了。你可以直接说“重置”，或者直接发一个新问题重新开始。'


def read_message(args: argparse.Namespace) -> str:
    if args.stdin:
        return sys.stdin.read().strip()
    if args.message:
        return ' '.join(args.message).strip()
    return ''


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Roundtable Pai natural-language controller')
    parser.add_argument('--stdin', action='store_true', help='Read latest user message from stdin')
    parser.add_argument('message', nargs='*', help='Latest user message')
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    validate_runtime_paths()
    message = read_message(args)
    print(route_message(message))


if __name__ == '__main__':
    main()
