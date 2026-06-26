#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

LOAD_GAME = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'load_game.py'
DETECT_LANGUAGE = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'detect_recent_language.py'
WORLD_DIR = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'worlds'


def load_world(universe: str):
    direct = WORLD_DIR / f'{universe}.json'
    nested = WORLD_DIR / universe / 'world.json'
    path = direct if direct.exists() else nested
    if not path.exists():
        raise FileNotFoundError(f'World config not found for {universe}')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f), str(path)


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


def extract_story_spine(world: dict, save: dict) -> dict:
    quests = save.get('quests', [])
    active_quests = [q for q in quests if q.get('status') == 'active']
    active_names = [str(q.get('name') or q.get('title') or '').strip() for q in active_quests]
    active_names = [name for name in active_names if name]

    mq = world.get('main_questline') or {}
    if isinstance(mq, dict):
        main_objective = str(mq.get('main_objective') or '').strip()
        mainline_lines = [str(x).strip() for x in (mq.get('major_story_threads') or []) if str(x).strip()]
    else:
        mainline_lines = _flatten_lines(mq)
        main_objective = mainline_lines[0] if mainline_lines else ''
    chapter_lines = _flatten_lines((world.get('gameplay_pacing') or {}).get('chapter_milestones'))
    gate_lines = _flatten_lines((world.get('gameplay_pacing') or {}).get('major_plot_gates'))
    blocker_lines = _flatten_lines((world.get('gameplay_pacing') or {}).get('progression_blockers'))

    main_objective = main_objective or (
        str(world.get('description_en') or world.get('description_zh') or '').strip()
    )
    current_drive = active_names[0] if active_names else (chapter_lines[0] if chapter_lines else (mainline_lines[0] if mainline_lines else main_objective))

    return {
        'main_objective': main_objective,
        'active_player_quests': active_names[:3],
        'current_drive': current_drive,
        'mainline_beats': mainline_lines[:6],
        'chapter_milestones': chapter_lines[:8],
        'major_plot_gates': gate_lines[:6],
        'progression_blockers': blocker_lines[:6],
        'key_figures': (world.get('key_figures') or [])[:5],
        'city_hubs': (world.get('city_and_region_hubs') or [])[:4],
        'relationship_webs': (world.get('relationship_webs') or [])[:4],
        'story_pressure_tracks': (world.get('story_pressure_tracks') or [])[:4],
        'quest_hubs': (world.get('quest_hubs') or [])[:4],
        'item_threads': (world.get('item_threads') or [])[:4],
        'instruction': (
            'Keep the player oriented toward the world\'s main story spine. '
            'Every daily evolution update should remind them what larger line they are already inside, '
            'what current major task / pressure matters most, and what concrete route naturally follows next. '
            'Use the world\'s richer structure when useful: key figures, hubs, relationship webs, pressure tracks, and item threads should give the update specific named texture instead of generic filler. '
            'Do not let the world drift into generic atmosphere with no recognizable main objective.'
        )
    }


def main():
    parser = argparse.ArgumentParser(description='Prepare dynamic YumFu daily evolution context')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    args = parser.parse_args()

    load = subprocess.run(
        ['python3', str(LOAD_GAME), '--user-id', args.user_id, '--universe', args.universe, '--quiet'],
        capture_output=True, text=True
    )
    if load.returncode != 0:
        print(load.stderr.strip() or load.stdout.strip(), file=sys.stderr)
        sys.exit(load.returncode)

    payload = json.loads(load.stdout)
    if not payload.get('exists') or not payload.get('data'):
        print(json.dumps({'success': False, 'error': 'Save not found'}))
        sys.exit(1)

    save = payload['data']
    world, world_path = load_world(args.universe)

    character = save.get('character', {})
    relationships = save.get('relationships', {})
    quests = save.get('quests', [])
    active_quests = [q for q in quests if q.get('status') == 'active']
    de = save.get('daily_evolution', {})
    story_spine = extract_story_spine(world, save)

    system_goal = (
        'Generate one plausible daily world-evolution update grounded in the player save and world setting. '
        'Do not hardcode canned events. Infer what happened while the player was offline. '
        'The update should create intrigue, pressure, or momentum, but must not auto-finish the main story or kill the player arbitrarily. '
        'Treat the player main save as canonical and read-only for this daily evolution run; write soft outcomes to sidecar state only.'
    )

    mutation_guardrails = [
        'Allowed: rumor flags, faction pressure, npc movement, relationship shifts, leads, patrol changes, route pressure, local losses/gains.',
        'Avoid: killing the player offline, auto-finishing the main story, removing critical items without explanation, giant irreversible choices every day.',
        'Return structured save mutations that are bounded and plausible.'
    ]

    canonical_language = save.get('language') or world.get('language') or 'en'
    preferred_language = canonical_language
    language_confidence = 1.0 if save.get('language') else 0.0
    try:
        lang_proc = subprocess.run(
            ['python3', str(DETECT_LANGUAGE), '--user-id', args.user_id, '--universe', args.universe],
            capture_output=True, text=True
        )
        if lang_proc.returncode == 0 and lang_proc.stdout.strip():
            lang_payload = json.loads(lang_proc.stdout)
            detected_language = lang_payload.get('preferred_language')
            detected_confidence = lang_payload.get('confidence') or 0.0
            if not save.get('language') and detected_language:
                preferred_language = detected_language
                language_confidence = detected_confidence
            elif save.get('language'):
                language_confidence = max(language_confidence, detected_confidence)
    except Exception:
        pass

    prompt = {
        'goal': system_goal,
        'world': {
            'id': world.get('id', args.universe),
            'name_en': world.get('name_en') or world.get('name') or args.universe,
            'name_zh': world.get('name_zh'),
            'genre': world.get('genre'),
            'themes': world.get('themes', []),
            'description_en': world.get('description_en'),
            'description_zh': world.get('description_zh'),
            'world_path': world_path,
            'key_figures': (world.get('key_figures') or [])[:5],
            'city_and_region_hubs': (world.get('city_and_region_hubs') or [])[:4],
            'relationship_webs': (world.get('relationship_webs') or [])[:4],
            'major_items_and_artifacts': (world.get('major_items_and_artifacts') or [])[:5],
            'mainline_stages': (world.get('mainline_stages') or [])[:5],
            'subfaction_networks': (world.get('subfaction_networks') or [])[:4],
            'quest_hubs': (world.get('quest_hubs') or [])[:4],
            'city_subzones': (world.get('city_subzones') or [])[:4],
            'story_pressure_tracks': (world.get('story_pressure_tracks') or [])[:4],
            'item_threads': (world.get('item_threads') or [])[:4],
        },
        'player': {
            'user_id': args.user_id,
            'character_name': character.get('name'),
            'role': character.get('role'),
            'house': character.get('house'),
            'traits': character.get('trait') or character.get('traits'),
            'location': save.get('location'),
            'inventory': save.get('inventory', []),
            'relationships': relationships,
            'active_quests': active_quests,
            'flags': save.get('flags', {}),
            'save_language': save.get('language'),
            'preferred_language_hint': preferred_language,
            'daily_evolution': de,
            'story_spine': story_spine,
        },
        'language_policy': {
            'priority': [
                'save.language (canonical per save)',
                'recent actual player conversation language (advisory unless explicit switch)',
                'world default language',
                'system fallback'
            ],
            'preferred_language_hint': preferred_language,
            'canonical_language': canonical_language,
            'confidence': language_confidence,
            'instruction': 'Write the daily evolution in the save\'s canonical language first. Do not drift languages just because old sidecar text or weak recent evidence points elsewhere. Only switch languages when the player clearly and explicitly changes play language.'
        },
        'sidecar_policy': {
            'main_save_mutation': 'forbidden in MVP',
            'write_target': '~/clawd/memory/yumfu/evolution/{universe}/user-{id}.json',
            'allowed_outputs': ['summary', 'story_text', 'image_prompt', 'severity', 'pending_hooks', 'soft world pressure', 'rumor threads']
        },
        'output_requirements': {
            'story_words': '100-220 words',
            'must_include': [
                'one short front-context recap (1-3 sentences) that reminds the player of the current main line / major task / why this scene matters now',
                'one meaningful world development',
                'one player-relevant consequence or pressure signal',
                'one hook inviting the player back into active play',
                'one practical route suggestion grounded in the main story spine',
                'one default route the story will assume if the player does nothing',
                'one image prompt matched to the update'
            ],
            'response_json_schema': {
                'summary': 'short summary string',
                'recap_text': '1-3 sentence recap that restates current main line and current pressure',
                'story_text': 'daily evolution notification text',
                'image_prompt': 'scene image prompt',
                'severity': 'minor|medium|major',
                'pending_hooks': ['list of non-destructive hooks to surface next time the player actively plays'],
                'suggested_routes': [
                    {
                        'label': 'short route label tied to the current arc',
                        'why_now': 'why the route matters right now',
                        'target': 'person/place/object/faction/mission line',
                        'urgency': 'low|medium|high'
                    }
                ],
                'default_route': {
                    'label': 'default continuation if player does nothing',
                    'why_now': 'why this is the natural route',
                    'target': 'person/place/object/faction/mission line'
                },
                'sidecar_meta': {
                    'rumor_threads': 'list of rumor/pressure threads',
                    'faction_movements': 'list of soft world changes',
                    'npc_watchlist': 'list of names or unknown actors to watch',
                    'world_detail_notes': 'named details that keep the world and main line concrete'
                }
            }
        },
        'guardrails': mutation_guardrails,
        'generated_at': datetime.now().isoformat()
    }

    print(json.dumps({'success': True, 'context': prompt}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
