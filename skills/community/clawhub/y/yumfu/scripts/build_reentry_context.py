#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LOAD_GAME = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'load_game.py'
LOAD_EVOLUTION = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'load_daily_evolution.py'
DETECT_LANGUAGE = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'detect_recent_language.py'
OUTBOUND_YUMFU = Path.home() / '.openclaw' / 'media' / 'outbound' / 'yumfu'
WORLD_DIR = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'worlds'


def _flatten_lines(value):
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if isinstance(v, str) and v.strip():
                lines.append(f'{k}: {v.strip()}')
            elif isinstance(v, (dict, list)):
                nested = _flatten_lines(v)
                if nested:
                    lines.extend([f'{k}: {item}' for item in nested[:3]])
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            lines.extend(_flatten_lines(item))
        return lines
    return []


def load_world(universe: str) -> dict:
    direct = WORLD_DIR / f'{universe}.json'
    nested = WORLD_DIR / universe / 'world.json'
    path = direct if direct.exists() else nested
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def build_story_spine(universe: str, save: dict) -> dict:
    world = load_world(universe)
    quests = save.get('quests') or []
    active_quests = [q for q in quests if q.get('status') == 'active']
    active_names = [str(q.get('name') or q.get('title') or '').strip() for q in active_quests if str(q.get('name') or q.get('title') or '').strip()]
    mq = world.get('main_questline') or {}
    if isinstance(mq, dict):
        main_objective = str(mq.get('main_objective') or '').strip()
        mainline_beats = [str(x).strip() for x in (mq.get('major_story_threads') or []) if str(x).strip()][:6]
    else:
        main_objective = ''
        mainline_beats = _flatten_lines(mq)[:6]
    chapter_milestones = _flatten_lines((world.get('gameplay_pacing') or {}).get('chapter_milestones'))[:8]
    major_plot_gates = _flatten_lines((world.get('gameplay_pacing') or {}).get('major_plot_gates'))[:6]
    current_main_task = active_names[0] if active_names else (chapter_milestones[0] if chapter_milestones else (mainline_beats[0] if mainline_beats else (main_objective or 'current main line')))
    return {
        'main_objective': main_objective or (mainline_beats[0] if mainline_beats else str(world.get('description_en') or world.get('description_zh') or '').strip()),
        'current_main_task': current_main_task,
        'active_player_quests': active_names[:3],
        'mainline_beats': mainline_beats,
        'chapter_milestones': chapter_milestones,
        'major_plot_gates': major_plot_gates,
        'key_figures': (world.get('key_figures') or [])[:5],
        'city_hubs': (world.get('city_and_region_hubs') or [])[:4],
        'relationship_webs': (world.get('relationship_webs') or [])[:4],
        'story_pressure_tracks': (world.get('story_pressure_tracks') or [])[:4],
        'item_threads': (world.get('item_threads') or [])[:4],
        'quest_hubs': (world.get('quest_hubs') or [])[:4],
    }


def looks_zh(text: str | None) -> bool:
    return bool(text and re.search(r'[\u4e00-\u9fff]', text))


def normalize_lang(value: str | None) -> str:
    v = str(value or '').strip().lower()
    if v in {'zh', 'zh-cn', 'zh-hans', 'zh-tw', 'zh-hant', 'cn', 'chinese', '中文'}:
        return 'zh'
    return 'en'


def looks_generic_target(text: str | None) -> bool:
    value = str(text or '').strip().lower()
    generic = {
        '当前关键目标', 'current key target', 'the current scene', 'the road ahead', 'the current line', '当前主线', 'location'
    }
    return value in {g.lower() for g in generic}


def load_world_language(universe: str) -> str | None:
    direct = WORLD_DIR / f'{universe}.json'
    nested = WORLD_DIR / universe / 'world.json'
    path = direct if direct.exists() else nested
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return normalize_lang(data.get('language'))
    except Exception:
        return None


def fallback_image_prompt(save: dict, evo: dict, preferred_language: str) -> str:
    character = ((save.get('character') or {}).get('name') or 'the player').strip()
    location = (save.get('location') or 'the current scene').strip()
    universe = (save.get('universe') or save.get('world_id') or '').strip()
    summary = (evo.get('last_summary') or '').strip()
    world = load_world(universe) if universe else {}
    art_style = world.get('art_style')
    art_direction = world.get('art_direction') or {}
    visual_style = art_direction.get('visual_style')
    style_bits = [str(x).strip() for x in [art_style, visual_style] if isinstance(x, str) and str(x).strip()]
    style_clause = ', '.join(style_bits[:2]) if style_bits else 'world-specific YumFu illustration style'

    if preferred_language == 'zh':
        return (
            f"YumFu 游戏续玩场景图，主角 {character}，地点 {location}，"
            f"延续当前存档剧情，不要像新开局，不要做成独立海报；"
            f"重点表现回到现场时的局势压力与继续推进感。"
            f"{(' 当前风声：' + summary) if summary and looks_zh(summary) else ''}"
            f" 世界观：{universe or '当前世界'}。"
            f" 画风要求：{style_clause}。"
            f" No text, no words, no letters, no captions, no signs, no speech bubbles, no watermark, image-only illustration."
        )

    return (
        f"YumFu continue-time gameplay image for {character} at {location}, visual continuity with the current save, "
        f"not a fresh opening scene, not a disconnected poster, emphasize immediate re-entry into the ongoing situation. "
        f"{('Current pressure: ' + summary + '. ') if summary and not looks_zh(summary) else ''}"
        f"World: {universe or 'current world'}. "
        f"Art direction: {style_clause}. "
        f"No text, no words, no letters, no captions, no signs, no speech bubbles, no watermark, image-only illustration."
    )


def pick_latest_image(user_id: str, universe: str) -> str | None:
    if not OUTBOUND_YUMFU.exists():
        return None
    candidates = sorted(
        OUTBOUND_YUMFU.glob(f'{universe}-user-{user_id}-*.png'),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return str(candidates[0]) if candidates else None


def main():
    parser = argparse.ArgumentParser(description='Build a concise YumFu re-entry context from save + daily evolution sidecar')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--recent-text', action='append', default=[])
    parser.add_argument('--recent-texts-json', default=None)
    args = parser.parse_args()

    save_proc = subprocess.run([
        'python3', str(LOAD_GAME), '--user-id', args.user_id, '--universe', args.universe, '--quiet'
    ], capture_output=True, text=True)
    if save_proc.returncode != 0:
        print(save_proc.stderr.strip() or save_proc.stdout.strip(), file=sys.stderr)
        sys.exit(save_proc.returncode)

    save_payload = json.loads(save_proc.stdout)
    evo_proc = subprocess.run([
        'python3', str(LOAD_EVOLUTION), '--user-id', args.user_id, '--universe', args.universe
    ], capture_output=True, text=True)
    evo_payload = json.loads(evo_proc.stdout) if evo_proc.returncode == 0 and evo_proc.stdout.strip() else {'exists': False, 'data': None}

    save = save_payload.get('data') or {}
    evo = evo_payload.get('data') or {}
    story_spine = build_story_spine(args.universe, save)
    hooks = evo.get('pending_hooks', [])[:3]
    suggested_routes = evo.get('suggested_routes', [])[:3]
    default_route = evo.get('default_route') or {}
    active_route = evo.get('active_route') or default_route or {}

    lang_cmd = [
        'python3', str(DETECT_LANGUAGE), '--user-id', args.user_id, '--universe', args.universe
    ]
    for text in args.recent_text:
        lang_cmd.extend(['--recent-text', text])
    if args.recent_texts_json:
        lang_cmd.extend(['--recent-texts-json', args.recent_texts_json])

    lang_proc = subprocess.run(lang_cmd, capture_output=True, text=True)
    lang_payload = json.loads(lang_proc.stdout) if lang_proc.returncode == 0 and lang_proc.stdout.strip() else {
        'preferred_language': (save.get('language') or 'en'), 'confidence': 0.0
    }

    canonical_language = normalize_lang(save.get('language'))
    world_language = load_world_language(args.universe)
    preferred_language = (
        lang_payload.get('preferred_language')
        or canonical_language
        or world_language
        or (save.get('language') or 'en')
    )
    if canonical_language and not lang_payload.get('suspect_save_language'):
        preferred_language = canonical_language
    elif world_language and lang_payload.get('suspect_save_language'):
        preferred_language = world_language
    raw_summary = evo.get('last_summary')
    if preferred_language == 'zh' and raw_summary and not looks_zh(raw_summary):
        summary_for_reentry = None
    elif preferred_language == 'en' and raw_summary and looks_zh(raw_summary):
        summary_for_reentry = None
    else:
        summary_for_reentry = raw_summary

    def localize_route(route: dict | None, is_active: bool = False) -> dict:
        if not route:
            return {}
        route = dict(route)
        label = str(route.get('label') or '').strip()
        why = str(route.get('why_now') or '').strip()
        target = str(route.get('target') or '').strip()
        if preferred_language == 'zh' and label.startswith('Default to '):
            route['label'] = '当前主线' if is_active else '默认推进'
        elif preferred_language == 'en' and label.startswith('默认沿'):
            route['label'] = 'Current main line' if is_active else 'Default continuation'
        if preferred_language == 'zh' and why.startswith('if the player does nothing'):
            route['why_now'] = '这是当前最自然、最不容易断档的继续方式'
        elif preferred_language == 'en' and why.startswith('就算玩家暂时不选'):
            route['why_now'] = 'this is the easiest natural continuation right now'

        if preferred_language == 'zh':
            if target.startswith('the ') and looks_generic_target(target):
                route['target'] = '当前关键目标'
        elif preferred_language == 'en':
            if any('\u4e00' <= ch <= '\u9fff' for ch in target) and looks_generic_target(target):
                route['target'] = 'current key target'
        return route

    active_route = localize_route(active_route, is_active=True)
    default_route = localize_route(default_route, is_active=False)

    result = {
        'success': True,
        'character_name': (save.get('character') or {}).get('name'),
        'location': save.get('location'),
        'active_quest': ((save.get('quests') or [{}])[0]).get('name'),
        'story_spine': story_spine,
        'last_daily_summary': raw_summary,
        'summary_for_reentry': summary_for_reentry,
        'pending_hooks': hooks,
        'suggested_routes': suggested_routes,
        'default_route': default_route,
        'active_route': active_route,
        'preferred_language': preferred_language,
        'language_confidence': lang_payload.get('confidence'),
        'locked_to_save_language': lang_payload.get('locked_to_save_language', False),
        'latest_image_path': pick_latest_image(args.user_id, args.universe),
        'image_prompt': (evo.get('last_image_prompt') or '').strip() or fallback_image_prompt(save, evo, normalize_lang(preferred_language)),
        'reentry_instruction': (
            'When the player returns, briefly pull them back into the scene using the latest daily evolution summary and the world\'s current main story spine, '
            'then offer one easy natural next move in the player\'s preferred language. '
            'Always restate the current main task / main line in a compact way so the player does not forget what they are actually doing in this world. '
            'Use enriched world context when useful: named figures, hubs, pressure tracks, and item threads should help the re-entry feel specific instead of generic. '
            'Prefer one concrete active route over vague lore recap. '
            'If a stored active/default route exists, surface it as the easiest path back in when the player seems cold or has been away. '
            'If the save has a canonical language, do not drift away from it automatically. '
            'Continue-time delivery is image-first: reuse the latest save-matched image when available; otherwise generate a fresh image and send it with the re-entry hook. '
            'Do not dump lore or system bulletins.'
        ),
        'continue_prompt_template': {
            'zh': '先用一句话把玩家拉回当前场景，再给 1-2 个最自然的继续动作选项；若有最近图片，一起发。',
            'en': 'Pull the player back into the scene in one short paragraph, then offer 1-2 natural continuation moves; include the latest image when available.'
        }
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
