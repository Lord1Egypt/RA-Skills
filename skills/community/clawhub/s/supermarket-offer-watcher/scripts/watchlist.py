#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DEFAULT_PATH = Path('/data/workspace/data/supermarkt-watchlist.json')


def default_data():
    return {
        'home': {
            'location_text': None,
            'radius_km': 15
        },
        'schedule': {
            'mode': 'daily',
            'time': '07:00',
            'weekday': 'monday',
            'tz': 'Europe/Berlin'
        },
        'products': []
    }


def load(path: Path):
    if path.exists():
        data = json.loads(path.read_text(encoding='utf-8'))
        # Backward-compatible defaults
        data.setdefault('home', default_data()['home'])
        data.setdefault('schedule', default_data()['schedule'])
        data.setdefault('products', [])
        return data
    return default_data()


def save(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def cmd_init(args):
    data = load(args.file)
    if args.location:
        data['home']['location_text'] = args.location
    if args.radius_km:
        data['home']['radius_km'] = args.radius_km
    if args.mode:
        data['schedule']['mode'] = args.mode
    if args.time:
        data['schedule']['time'] = args.time
    if args.weekday:
        data['schedule']['weekday'] = args.weekday.lower()
    if args.tz:
        data['schedule']['tz'] = args.tz
    save(args.file, data)
    print(f'Initialized: {args.file}')


def cmd_set_home(args):
    data = load(args.file)
    if args.location:
        data['home']['location_text'] = args.location
    if args.radius_km:
        data['home']['radius_km'] = args.radius_km
    save(args.file, data)
    print('Home updated')


def cmd_set_schedule(args):
    data = load(args.file)
    if args.mode:
        data['schedule']['mode'] = args.mode
    if args.time:
        data['schedule']['time'] = args.time
    if args.weekday:
        data['schedule']['weekday'] = args.weekday.lower()
    if args.tz:
        data['schedule']['tz'] = args.tz
    save(args.file, data)
    print('Schedule updated')


def cmd_add(args):
    data = load(args.file)
    names = {p['name'].lower(): i for i, p in enumerate(data['products'])}
    item = {
        'name': args.name,
        'aliases': [a.strip() for a in (args.aliases or '').split(',') if a.strip()],
        'stores': [s.strip() for s in (args.stores or '').split(',') if s.strip()],
        'notes': args.notes or ''
    }
    key = args.name.lower()
    if key in names:
        data['products'][names[key]] = item
        action = 'Updated'
    else:
        data['products'].append(item)
        action = 'Added'
    save(args.file, data)
    print(f'{action}: {args.name}')


def cmd_remove(args):
    data = load(args.file)
    before = len(data['products'])
    data['products'] = [p for p in data['products'] if p['name'].lower() != args.name.lower()]
    after = len(data['products'])
    save(args.file, data)
    if after < before:
        print(f'Removed: {args.name}')
    else:
        print(f'Not found: {args.name}')


def cmd_list(args):
    data = load(args.file)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser():
    p = argparse.ArgumentParser(description='Manage supermarket offer watchlist')
    p.add_argument('--file', type=Path, default=DEFAULT_PATH)
    sub = p.add_subparsers(dest='cmd', required=True)

    init = sub.add_parser('init')
    init.add_argument('--location', help='Home location text (e.g. "80331 München")')
    init.add_argument('--radius-km', type=int, default=15)
    init.add_argument('--mode', choices=['daily', 'weekly'])
    init.add_argument('--time', help='HH:MM (24h), e.g. 07:00')
    init.add_argument('--weekday', choices=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
    init.add_argument('--tz', help='IANA timezone, e.g. Europe/Berlin')
    init.set_defaults(func=cmd_init)

    set_home = sub.add_parser('set-home')
    set_home.add_argument('--location', help='Home location text')
    set_home.add_argument('--radius-km', type=int)
    set_home.set_defaults(func=cmd_set_home)

    set_schedule = sub.add_parser('set-schedule')
    set_schedule.add_argument('--mode', choices=['daily', 'weekly'])
    set_schedule.add_argument('--time', help='HH:MM (24h), e.g. 07:00')
    set_schedule.add_argument('--weekday', choices=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
    set_schedule.add_argument('--tz', help='IANA timezone, e.g. Europe/Berlin')
    set_schedule.set_defaults(func=cmd_set_schedule)

    add = sub.add_parser('add')
    add.add_argument('name')
    add.add_argument('--aliases', help='Comma separated aliases')
    add.add_argument('--stores', help='Comma separated preferred stores')
    add.add_argument('--notes')
    add.set_defaults(func=cmd_add)

    rm = sub.add_parser('remove')
    rm.add_argument('name')
    rm.set_defaults(func=cmd_remove)

    ls = sub.add_parser('list')
    ls.set_defaults(func=cmd_list)

    return p


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
