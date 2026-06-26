#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

PREPARE = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'daily_evolution_prepare.py'
APPLY = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'apply_daily_evolution.py'


def main():
    parser = argparse.ArgumentParser(description='Run YumFu daily evolution and emit a ready-to-use agent payload')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--channel', default='telegram')
    parser.add_argument('--target', default=None)
    parser.add_argument('--apply-from-json', default=None,
                        help='Optional path to a JSON file containing generated evolution output to write to sidecar')
    args = parser.parse_args()

    if args.apply_from_json:
        payload = json.loads(Path(args.apply_from_json).read_text(encoding='utf-8'))
        if isinstance(payload, dict) and 'result' in payload and isinstance(payload.get('result'), dict):
            payload = payload['result']
        summary = payload['summary']
        story_text = payload['story_text']
        severity = payload.get('severity', 'minor')
        image_prompt = payload.get('image_prompt', '')
        hooks = payload.get('pending_hooks') or payload.get('hooks', [])
        meta = payload.get('sidecar_meta') or payload.get('meta', {})
        routes = payload.get('suggested_routes', [])
        default_route = payload.get('default_route', {})
        advancement_level = payload.get('advancement_level', 'normal')
        advancement_at = payload.get('advancement_at', '')
        proc = subprocess.run([
            'python3', str(APPLY),
            '--user-id', args.user_id,
            '--universe', args.universe,
            '--summary', summary,
            '--story-text', story_text,
            '--severity', severity,
            '--image-prompt', image_prompt,
            '--hooks-json', json.dumps(hooks, ensure_ascii=False),
            '--meta-json', json.dumps(meta, ensure_ascii=False),
            '--routes-json', json.dumps(routes, ensure_ascii=False),
            '--default-route-json', json.dumps(default_route, ensure_ascii=False),
            '--advancement-level', advancement_level,
            '--advancement-at', advancement_at,
        ], capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stderr.strip() or proc.stdout.strip(), file=sys.stderr)
            sys.exit(proc.returncode)
        print(proc.stdout)
        return

    prep = subprocess.run([
        'python3', str(PREPARE),
        '--user-id', args.user_id,
        '--universe', args.universe,
    ], capture_output=True, text=True)
    if prep.returncode != 0:
        print(prep.stderr.strip() or prep.stdout.strip(), file=sys.stderr)
        sys.exit(prep.returncode)

    prep_obj = json.loads(prep.stdout)
    context = prep_obj['context']

    instruction = {
        'purpose': 'Use this payload in an agent turn to generate one safe daily YumFu evolution update.',
        'channel': args.channel,
        'target': args.target,
        'agent_task': {
            'generate': {
                'story_text': '100-220 words, concise, scene-forward, easy re-entry hook at the end',
                'summary': 'one-sentence summary',
                'severity': 'minor|medium|major',
                'image_prompt': 'one strong scene prompt matched to the update',
                'pending_hooks': ['1-3 short hooks for next active play'],
                'suggested_routes': [
                    {
                        'label': 'short route label',
                        'why_now': 'why this route matters now',
                        'target': 'person/place/object/faction line',
                        'urgency': 'low|medium|high'
                    }
                ],
                'default_route': {
                    'label': 'the route the story will naturally assume if the player does nothing',
                    'why_now': 'why this is the easiest natural continuation',
                    'target': 'person/place/object/faction line'
                },
                'advancement_level': 'normal|major',
                'advancement_at': 'ISO timestamp for this advancement tick',
                'sidecar_meta': {
                    'rumor_threads': ['soft rumors'],
                    'faction_movements': ['soft world changes'],
                    'npc_watchlist': ['watch targets'],
                    'item_threads': ['letters, relics, cargo, maps, seals, weapons, etc.'],
                    'world_detail_notes': ['concrete details worth resurfacing on continue']
                }
            },
            'must_not_do': [
                'do not modify the main save directly',
                'do not kill the player offline',
                'do not auto-finish the main story',
                'do not send a separate report-generated message'
            ],
            'after_generation': [
                'generate one image from image_prompt',
                'send one in-world message with the image',
                'write the generated result to a temporary JSON file',
                'call run_daily_evolution.py --apply-from-json <file> to persist the sidecar state'
            ]
        },
        'context': context
    }

    print(json.dumps({'success': True, 'payload': instruction}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
