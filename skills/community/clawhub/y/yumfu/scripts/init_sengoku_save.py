#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

WORLD_PATH = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'worlds' / 'sengoku.json'
SAVE_GAME = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'save_game.py'


def load_world():
    return json.loads(WORLD_PATH.read_text(encoding='utf-8'))


def pick(items, item_id, key='id'):
    for item in items:
        if item.get(key) == item_id:
            return item
    raise KeyError(item_id)


def main():
    parser = argparse.ArgumentParser(description='Initialize a YumFu Sengoku Chaos save')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--role', required=True)
    parser.add_argument('--faction', required=True)
    parser.add_argument('--scenario', required=True)
    parser.add_argument('--language', default='zh')
    args = parser.parse_args()

    world = load_world()
    role = pick(world['playable_roles'], args.role)
    faction = pick(world['factions'], args.faction)
    scenario = pick(world['starting_scenarios'], args.scenario)

    save = {
        'character': {
            'name': args.name,
            'role': role['name_zh'],
            'role_id': role['id'],
            'house': faction['name_zh'],
            'faction_id': faction['id'],
            'level': 1,
            'hp': 110,
            'hp_max': 110,
            'stamina': 100,
            'stamina_max': 100,
            'gold': 80,
            'trait': '野心未明',
            'skills': {
                '统率': 1,
                '权谋': 1,
                '火器': 1,
                '交涉': 1
            },
            'attributes': world['character_creation']['starting_stats']
        },
        'location': scenario['name_zh'],
        'region': faction.get('starting_location') or world.get('starting_location'),
        'goal': '在战国乱世中建立自己的权力与生存空间',
        'relationships': {
            faction['leader']: 35,
            '地方商人': 20,
            '可疑密探': 10
        },
        'inventory': [
            {
                'name': '家传刀 / 佩刀',
                'type': 'weapon',
                'damage': '1d6+1',
                'special': '在乱世里，刀先代表身份，再代表生死'
            },
            {
                'name': '军粮票据',
                'type': 'resource',
                'quantity': 2,
                'effect': '可换取少量粮秣或人情'
            },
            {
                'name': '私印与书信袋',
                'type': 'gear',
                'special': '可用于密信、调令、伪造文书或联络'
            }
        ],
        'quests': [
            {
                'id': 'first-foothold',
                'name': '乱世立足',
                'status': 'active',
                'description': scenario['hook'],
                'objectives': [
                    '看清当前城与营的权力链',
                    '找到第一批能用的人',
                    '拿到第一份真正可支配的资源',
                    '在不被大势碾死前先立住脚'
                ],
                'current_stage': f"开局：{scenario['name_zh']}",
                'intel': {
                    'scenario_hook': scenario['hook'],
                    'role_focus': role['focus'],
                    'faction_specialty': faction['specialty']
                }
            }
        ],
        'achievements': [],
        'flags': {
            'game_started': True,
            'sengoku_opening': True,
            'first_scene_pending': True,
            'daily_evolution_opt_in_pending_confirmation': False
        },
        'pawned_items': [],
        'language': args.language,
        'user_id': args.user_id,
        'universe': 'sengoku',
        'version': 1
    }

    proc = subprocess.run(
        ['python3', str(SAVE_GAME), '--user-id', args.user_id, '--universe', 'sengoku', '--quiet'],
        input=json.dumps(save, ensure_ascii=False), capture_output=True, text=True
    )
    if proc.returncode != 0:
        print(proc.stderr.strip() or proc.stdout.strip(), file=sys.stderr)
        sys.exit(proc.returncode)

    result = json.loads(proc.stdout)
    print(json.dumps({
        'success': True,
        'world': world['name_zh'],
        'character_name': args.name,
        'role': role['name_zh'],
        'faction': faction['name_zh'],
        'scenario': scenario['name_zh'],
        'hook': scenario['hook'],
        'save': result
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
