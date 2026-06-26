#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

BUILD = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'build_reentry_context.py'


def main():
    parser = argparse.ArgumentParser(description='Render a concise continue-time re-entry prompt for YumFu')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--recent-text', action='append', default=[])
    parser.add_argument('--recent-texts-json', default=None)
    args = parser.parse_args()

    cmd = ['python3', str(BUILD), '--user-id', args.user_id, '--universe', args.universe]
    for text in args.recent_text:
        cmd.extend(['--recent-text', text])
    if args.recent_texts_json:
        cmd.extend(['--recent-texts-json', args.recent_texts_json])

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip() or proc.stdout.strip(), file=sys.stderr)
        sys.exit(proc.returncode)

    data = json.loads(proc.stdout)
    lang = data.get('preferred_language') or 'en'
    summary = data.get('summary_for_reentry')
    hooks = data.get('pending_hooks') or []
    routes = data.get('suggested_routes') or []
    default_route = data.get('default_route') or {}
    active_route = data.get('active_route') or default_route or {}
    story_spine = data.get('story_spine') or {}
    character = data.get('character_name') or 'the player'
    location = data.get('location') or 'the current scene'
    quest = data.get('active_quest') or story_spine.get('current_main_task') or 'the active quest'
    main_objective = story_spine.get('main_objective') or ''
    pressure_tracks = story_spine.get('story_pressure_tracks') or []
    key_figures = story_spine.get('key_figures') or []
    hubs = story_spine.get('city_hubs') or []
    quest_line = f"你现在仍在推进「{quest}」。" if lang != 'zh' or any('\u4e00' <= ch <= '\u9fff' for ch in quest) else "你现在还在推进当前主线。"

    if lang == 'zh':
        objective_line = f"这条世界主线眼下压在你身上的事，是「{main_objective}」。" if main_objective else ''
        pressure_line = ''
        if pressure_tracks:
            p = pressure_tracks[0]
            pressure_line = f" 眼下最压人的，是「{p.get('name', '局势压力')}」：{p.get('pressure', '')}".rstrip()
        figure_line = ''
        if key_figures:
            f0 = key_figures[0]
            figure_line = f" {f0.get('name', '某个关键人物')}这条线还没从局里退下。"
        hub_line = ''
        if hubs:
            h0 = hubs[0]
            hub_line = f" {h0.get('name', '关键地点')}仍会是你接下来绕不开的地方。"
        text = (
            f"你回来时，{location} 的局势已经轻轻变了。"
            f"{summary or '你离开的这段时间，暗线还在往前推，只是风声比之前更紧。'}\n\n"
            f"{quest_line}{objective_line}{pressure_line}{figure_line}{hub_line}先别做功课，直接接回现场。"
        )
        if active_route:
            label = (active_route.get('label') or '当前主线').strip()
            why = (active_route.get('why_now') or '').strip()
            target = (active_route.get('target') or '').strip()
            active_line = ' / '.join([p for p in [label, target, why] if p])
            if active_line:
                text += "\n\n当前最该接回的线：\n- " + active_line
        elif routes:
            lines = []
            for r in routes[:2]:
                label = (r.get('label') or '').strip()
                why = (r.get('why_now') or '').strip()
                target = (r.get('target') or '').strip()
                parts = [p for p in [label, target, why] if p]
                if parts:
                    lines.append(' - '.join(parts))
            if lines:
                text += "\n\n现在最值得接的路线：\n" + "\n".join(f"- {line}" for line in lines)
        elif hooks:
            text += "\n\n最自然的下一步：\n" + "\n".join(f"- {h}" for h in hooks[:2])
        if default_route and default_route != active_route:
            label = (default_route.get('label') or '默认推进').strip()
            why = (default_route.get('why_now') or '').strip()
            target = (default_route.get('target') or '').strip()
            default_line = ' / '.join([p for p in [label, target, why] if p])
            if default_line:
                text += "\n\n如果你现在不选，我会默认沿这条线把主剧情往前推：\n- " + default_line
    else:
        objective_line = f" The larger main line still hanging over this run is: '{main_objective}'." if main_objective else ''
        pressure_line = ''
        if pressure_tracks:
            p = pressure_tracks[0]
            pressure_line = f" The sharpest pressure right now is '{p.get('name', 'current pressure')}': {p.get('pressure', '')}."
        figure_line = ''
        if key_figures:
            f0 = key_figures[0]
            figure_line = f" {f0.get('name', 'A key figure')} is still part of the line you cannot ignore."
        hub_line = ''
        if hubs:
            h0 = hubs[0]
            hub_line = f" {h0.get('name', 'A key hub')} is still where the story naturally pulls next."
        text = (
            f"When {character} returns to {location}, the scene has shifted slightly: "
            f"{summary or 'something nearby changed while you were away.'}\n\n"
            f"You are still in the middle of '{quest}'.{objective_line}{pressure_line}{figure_line}{hub_line} Do not dump lore; pull the player straight back into the scene."
        )
        if active_route:
            label = (active_route.get('label') or 'Active line').strip()
            why = (active_route.get('why_now') or '').strip()
            target = (active_route.get('target') or '').strip()
            active_line = ' / '.join([p for p in [label, target, why] if p])
            if active_line:
                text += "\n\nCurrent best line to pick back up:\n- " + active_line
        elif routes:
            lines = []
            for r in routes[:2]:
                label = (r.get('label') or '').strip()
                why = (r.get('why_now') or '').strip()
                target = (r.get('target') or '').strip()
                parts = [p for p in [label, target, why] if p]
                if parts:
                    lines.append(' - '.join(parts))
            if lines:
                text += "\n\nBest routes to pick up now:\n" + "\n".join(f"- {line}" for line in lines)
        elif hooks:
            text += "\n\nMost natural next moves:\n" + "\n".join(f"- {h}" for h in hooks[:2])
        if default_route and default_route != active_route:
            label = (default_route.get('label') or 'Default continuation').strip()
            why = (default_route.get('why_now') or '').strip()
            target = (default_route.get('target') or '').strip()
            default_line = ' / '.join([p for p in [label, target, why] if p])
            if default_line:
                text += "\n\nIf you do nothing, this is the route the story will naturally take next:\n- " + default_line

    print(json.dumps({
        'success': True,
        'preferred_language': lang,
        'text': text,
        'latest_image_path': data.get('latest_image_path'),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
