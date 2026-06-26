#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

INIT_SAVE = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'init_sengoku_save.py'
HANDLE_DE = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'handle_daily_evolution_choice.py'
RENDER_OPENING = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'render_sengoku_opening.py'
WORLD_PATH = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'worlds' / 'sengoku.json'


def load_world():
    return json.loads(WORLD_PATH.read_text(encoding='utf-8'))


def pick(items, item_id, key='id'):
    for item in items:
        if item.get(key) == item_id:
            return item
    raise KeyError(item_id)


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout)


def build_opening(world, name, role, faction, scenario):
    opening_text = (
        f"乱世的风先吹到京都，又吹到堺港、甲斐、对马与每一座还没烧干净的城下町。\n\n"
        f"你叫{name}。你不是史书上已经写好的名字，而是刚刚踏进这场大乱的人。"
        f"你现在的身份是【{role['name_zh']}】，站在【{faction['name_zh']}】这一边，却未必永远只替这一边活。\n\n"
        f"今夜的开场是：{scenario['name_zh']}。\n"
        f"{scenario['hook']}\n\n"
        f"你很清楚，在这个时代，最先到手的从来不是天下，而是：一封信、一批粮、一门炮、一个肯替你去死的人。"
        f"而你要做的第一件事，不是空想大业，是先把眼前这一局吃下来。"
    )

    image_prompt = (
        f"Sengoku Chaos opening scene, {scenario['name_zh']}, protagonist {name}, role {role['name_zh']}, faction {faction['name_zh']}, "
        f"{scenario['hook']}, Japanese ukiyo-e woodblock print style, bold ink outlines, textured washi paper, flat layered colors, lacquer armor, muddy streets, banners, hidden intrigue, matchlocks and power struggle"
    )

    choices = [
        "先看清现场里谁真正有权",
        "先盯住最可能坏你事的人",
        "先拿到第一份能立威的资源",
        "先按你的路子自己开口布局"
    ]

    return {
        'opening_text': opening_text,
        'image_prompt': image_prompt,
        'choices': choices
    }


def main():
    parser = argparse.ArgumentParser(description='Initialize and render a playable YumFu Sengoku Chaos opening')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--role', required=True)
    parser.add_argument('--faction', required=True)
    parser.add_argument('--scenario', required=True)
    parser.add_argument('--language', default='zh')
    parser.add_argument('--daily-evolution', choices=['yes', 'no'], default='no')
    parser.add_argument('--target', default=None)
    parser.add_argument('--channel', default='telegram')
    parser.add_argument('--time', default='10:00')
    parser.add_argument('--tz', default='America/Los_Angeles')
    args = parser.parse_args()

    world = load_world()
    role = pick(world['playable_roles'], args.role)
    faction = pick(world['factions'], args.faction)
    scenario = pick(world['starting_scenarios'], args.scenario)

    save_result = run([
        'python3', str(INIT_SAVE),
        '--user-id', args.user_id,
        '--name', args.name,
        '--role', args.role,
        '--faction', args.faction,
        '--scenario', args.scenario,
        '--language', args.language,
    ])

    de_result = None
    if args.target:
        de_result = run([
            'python3', str(HANDLE_DE),
            '--user-id', args.user_id,
            '--universe', 'sengoku',
            '--target', args.target,
            '--choice', args.daily_evolution,
            '--channel', args.channel,
            '--time', args.time,
            '--tz', args.tz,
        ])

    opening = build_opening(world, args.name, role, faction, scenario)
    rendered_opening = run([
        'python3', str(RENDER_OPENING), '--user-id', args.user_id
    ])

    print(json.dumps({
        'success': True,
        'world': world['name_zh'],
        'save_result': save_result,
        'daily_evolution': de_result,
        'opening': opening,
        'rendered_opening': rendered_opening,
        'daily_evolution_pitch_zh': world.get('daily_evolution_pitch_zh')
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
