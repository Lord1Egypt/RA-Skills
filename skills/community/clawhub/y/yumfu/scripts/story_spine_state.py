#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

WORLD_DIR = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'worlds'
SAVE_ROOT = Path.home() / 'clawd' / 'memory' / 'yumfu' / 'saves'


def load_world(universe: str) -> dict[str, Any]:
    direct = WORLD_DIR / f'{universe}.json'
    nested = WORLD_DIR / universe / 'world.json'
    path = direct if direct.exists() else nested
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def load_save(user_id: str, universe: str) -> tuple[dict[str, Any], Path]:
    path = SAVE_ROOT / universe / f'user-{user_id}.json'
    if not path.exists():
        return {}, path
    return json.loads(path.read_text(encoding='utf-8')), path


def flatten_lines(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, dict):
        lines: list[str] = []
        for k, v in value.items():
            if isinstance(v, str) and v.strip():
                lines.append(f'{k}: {v.strip()}')
            elif isinstance(v, (dict, list)):
                nested = flatten_lines(v)
                if nested:
                    lines.extend([f'{k}: {item}' for item in nested[:3]])
        return lines
    if isinstance(value, list):
        lines: list[str] = []
        for item in value:
            lines.extend(flatten_lines(item))
        return lines
    return []


def derive_spine(save: dict[str, Any], world: dict[str, Any]) -> dict[str, Any]:
    quests = save.get('quests') or []
    active_quests = [q for q in quests if q.get('status') == 'active']
    active_names = [str(q.get('name') or q.get('title') or '').strip() for q in active_quests if str(q.get('name') or q.get('title') or '').strip()]

    save_spine = save.get('story_spine') or {}
    world_main = world.get('main_questline') or {}
    mainline_beats = flatten_lines(world_main.get('major_story_threads') or world_main)[:6]
    chapter_milestones = flatten_lines((world.get('gameplay_pacing') or {}).get('chapter_milestones'))[:8]
    current_main_task = (
        str(save_spine.get('current_main_task') or '').strip()
        or (active_names[0] if active_names else '')
        or (chapter_milestones[0] if chapter_milestones else '')
        or (mainline_beats[0] if mainline_beats else '')
    )

    return {
        'main_objective': str(save_spine.get('main_objective') or world_main.get('main_objective') or world.get('description_zh') or world.get('description_en') or '').strip(),
        'current_main_task': current_main_task,
        'active_player_quests': active_names[:3],
        'active_pressure': str(save_spine.get('active_pressure') or '').strip(),
        'next_route_hint': str(save_spine.get('next_route_hint') or '').strip(),
        'major_story_threads': mainline_beats,
        'chapter_milestones': chapter_milestones,
        'default_route_logic': str(world_main.get('default_route_logic') or '').strip(),
    }


def merge_spine(existing: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    updated = dict(existing)
    if args.current_main_task:
        updated['current_main_task'] = args.current_main_task.strip()
    if args.active_pressure:
        updated['active_pressure'] = args.active_pressure.strip()
    if args.next_route_hint:
        updated['next_route_hint'] = args.next_route_hint.strip()
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description='Read or update YumFu story spine state for a save')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--set', action='store_true', help='Persist updated story spine into the save')
    parser.add_argument('--current-main-task')
    parser.add_argument('--active-pressure')
    parser.add_argument('--next-route-hint')
    args = parser.parse_args()

    save, save_path = load_save(args.user_id, args.universe)
    if not save:
        raise SystemExit(json.dumps({'success': False, 'error': 'save not found', 'save_path': str(save_path)}, ensure_ascii=False))

    world = load_world(args.universe)
    base = derive_spine(save, world)
    result = merge_spine(base, args)

    if args.set:
        save['story_spine'] = result
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(save, ensure_ascii=False, indent=2), encoding='utf-8')

    print(json.dumps({'success': True, 'story_spine': result, 'save_path': str(save_path)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
