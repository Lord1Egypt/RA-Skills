#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts'
LOAD = ROOT / 'load_game.py'
RUN = ROOT / 'run_daily_evolution_job.py'
REENTRY = ROOT / 'build_reentry_context.py'


def run_json(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f'command failed: {cmd}')
    return json.loads(proc.stdout)


def short_text(value, limit=88):
    text = str(value or '').strip().replace('\n', ' ')
    if len(text) <= limit:
        return text
    return text[: limit - 1] + '…'


def route_target(route):
    if not isinstance(route, dict):
        return ''
    return str(route.get('target') or '').strip()


def route_label(route):
    if not isinstance(route, dict):
        return ''
    return str(route.get('label') or '').strip()


def likely_generic_route_target(target: str) -> bool:
    generic = {
        '当前关键目标', 'current key target', 'the current scene', 'the road ahead', 'the current line', 'location', '当前主线'
    }
    return str(target or '').strip().lower() in {g.lower() for g in generic}


def classify_findings(result: dict, reentry: dict) -> tuple[list[str], list[str]]:
    problems = []
    warnings = []

    if not result.get('summary'):
        problems.append('missing_summary')
    elif len(str(result.get('summary')).strip()) < 8:
        warnings.append('summary_too_thin')

    if not result.get('recap_text'):
        problems.append('missing_recap_text')
    elif len(str(result.get('recap_text')).strip()) < 20:
        warnings.append('recap_too_thin')

    routes = result.get('suggested_routes')
    if not isinstance(routes, list) or not routes:
        problems.append('missing_suggested_routes')
    else:
        top_target = route_target(routes[0])
        if not top_target:
            warnings.append('top_route_missing_target')
        elif likely_generic_route_target(top_target):
            warnings.append('top_route_target_generic')

    default_route = result.get('default_route')
    if not isinstance(default_route, dict) or not default_route:
        problems.append('missing_default_route')
    else:
        default_target = route_target(default_route)
        if not default_target:
            warnings.append('default_route_missing_target')
        elif likely_generic_route_target(default_target):
            warnings.append('default_route_target_generic')

    if result.get('advancement_level') not in {'normal', 'major'}:
        problems.append('bad_advancement_level')

    preferred_language = reentry.get('preferred_language')
    active_route = reentry.get('active_route') or {}
    if reentry.get('reentry_has_active_route') or active_route.get('label'):
        active_target = route_target(active_route)
        if not active_target:
            warnings.append('reentry_active_route_missing_target')
        elif likely_generic_route_target(active_target):
            warnings.append('reentry_active_route_target_generic')
    if preferred_language not in {'zh', 'en'}:
        warnings.append('reentry_language_unclear')

    return problems, warnings


def main():
    parser = argparse.ArgumentParser(description='Batch smoke test YumFu daily evolution outputs')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universes', nargs='*', default=None)
    args = parser.parse_args()

    all_worlds = ['journey-to-west', 'xiaoao', 'lotr', 'game-of-thrones', 'harry-potter', 'warrior-cats', 'sengoku', 'yitian']
    universes = args.universes or all_worlds
    report = []
    summary_lines = []

    for universe in universes:
        entry = {'universe': universe, 'save_exists': False, 'ok': False}
        try:
            save = run_json(['python3', str(LOAD), '--user-id', args.user_id, '--universe', universe, '--quiet'])
            if not save.get('exists') or not save.get('data'):
                entry['error'] = 'save_missing'
                report.append(entry)
                summary_lines.append(f'- {universe}: save missing')
                continue

            entry['save_exists'] = True
            evo = run_json(['python3', str(RUN), '--user-id', args.user_id, '--universe', universe])
            result = evo.get('result') or {}
            reentry = run_json(['python3', str(REENTRY), '--user-id', args.user_id, '--universe', universe])

            top_route = (result.get('suggested_routes') or [{}])[0]
            default_route = result.get('default_route') or {}
            reentry_active = reentry.get('active_route') or {}
            problems, warnings = classify_findings(result, {
                **reentry,
                'reentry_has_active_route': bool(reentry_active.get('label'))
            })

            entry.update({
                'summary': result.get('summary'),
                'recap_text': result.get('recap_text'),
                'suggested_routes': result.get('suggested_routes'),
                'default_route': default_route,
                'advancement_level': result.get('advancement_level'),
                'reentry_language': reentry.get('preferred_language'),
                'reentry_has_active_route': bool(reentry_active.get('label')),
                'diagnostics': {
                    'top_route_label': route_label(top_route),
                    'top_route_target': route_target(top_route),
                    'default_route_target': route_target(default_route),
                    'active_route_target': route_target(reentry_active),
                    'summary_preview': short_text(result.get('summary'), 60),
                    'recap_preview': short_text(result.get('recap_text'), 100),
                }
            })

            entry['problems'] = problems
            entry['warnings'] = warnings
            entry['ok'] = not problems

            marker = 'OK' if not problems else 'FAIL'
            warning_suffix = f" | warnings: {', '.join(warnings)}" if warnings else ''
            summary_lines.append(
                f"- {universe}: {marker} | top={route_target(top_route) or '-'} | default={route_target(default_route) or '-'} | lang={reentry.get('preferred_language') or '-'}{warning_suffix}"
            )
        except Exception as e:
            entry['error'] = str(e)
            summary_lines.append(f'- {universe}: ERROR | {e}')
        report.append(entry)

    ok = all(item.get('ok') or item.get('error') == 'save_missing' for item in report)
    print(json.dumps({'success': ok, 'summary_text': '\n'.join(summary_lines), 'report': report}, ensure_ascii=False, indent=2))
    if not ok:
        sys.exit(1)


if __name__ == '__main__':
    main()
