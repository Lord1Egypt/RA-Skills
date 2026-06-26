#!/usr/bin/env python3
"""Home Assistant CLI - Control smart home devices via the Home Assistant REST API."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def get_config(args):
    """Get server URL and token from args or environment variables."""
    server = getattr(args, 'server', None) or os.environ.get('HA_URL')
    token = getattr(args, 'token', None) or os.environ.get('HA_TOKEN')
    if not server:
        print("Error: Server URL required. Use --server or set HA_URL env var.", file=sys.stderr)
        sys.exit(1)
    if not token:
        print("Error: Token required. Use --token or set HA_TOKEN env var.", file=sys.stderr)
        sys.exit(1)
    return server.rstrip('/'), token


def api_request(server, token, path, method='GET', data=None):
    """Make an API request to Home Assistant."""
    url = f"{server}{path}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode()
            if content:
                return json.loads(content)
            return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ''
        print(f"Error: HTTP {e.code} - {e.reason}", file=sys.stderr)
        if error_body:
            try:
                print(json.dumps(json.loads(error_body), indent=2), file=sys.stderr)
            except json.JSONDecodeError:
                print(error_body, file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to {server} - {e.reason}", file=sys.stderr)
        sys.exit(1)


def call_service(server, token, domain, service, data):
    """Call a Home Assistant service."""
    result = api_request(server, token, f"/api/services/{domain}/{service}", method='POST', data=data)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("OK")


def print_json(data):
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2))


# --- Command handlers ---

def cmd_check(args):
    server, token = get_config(args)
    url = f"{server}/api/"
    headers = {'Authorization': f'Bearer {token}'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"OK - HTTP {resp.status}")
            content = resp.read().decode()
            if content:
                print_json(json.loads(content))
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect - {e.reason}", file=sys.stderr)
        sys.exit(1)


def cmd_entities(args):
    server, token = get_config(args)
    states = api_request(server, token, "/api/states")
    for entity in sorted(states, key=lambda e: e['entity_id']):
        eid = entity['entity_id']
        if args.domain and not eid.startswith(f"{args.domain}."):
            continue
        if args.domain == 'sensor':
            unit = entity.get('attributes', {}).get('unit_of_measurement', '')
            print(f"{eid}: {entity['state']} {unit}".strip())
        else:
            print(f"{eid}: {entity['state']}")


def cmd_state(args):
    server, token = get_config(args)
    result = api_request(server, token, f"/api/states/{args.entity_id}")
    print_json(result)


def cmd_areas(args):
    server, token = get_config(args)
    result = api_request(server, token, "/api/template", method='POST',
                         data={"template": "{{ areas() }}"})
    print(result)


def cmd_area_entities(args):
    server, token = get_config(args)
    template = '{{ area_entities("' + args.area + '") }}'
    if args.domain:
        template = '{{ area_entities("' + args.area + '") | select("match", "' + args.domain + '.") | list }}'
    result = api_request(server, token, "/api/template", method='POST',
                         data={"template": template})
    print(result)


def cmd_area_of(args):
    server, token = get_config(args)
    result = api_request(server, token, "/api/template", method='POST',
                         data={"template": '{{ area_name("' + args.entity_id + '") }}'})
    print(result)


def cmd_floors(args):
    server, token = get_config(args)
    template = '{% for floor in floors() %}{{ floor }}: {{ floor_areas(floor) }}\n{% endfor %}'
    result = api_request(server, token, "/api/template", method='POST',
                         data={"template": template})
    print(result)


def cmd_switch(args):
    server, token = get_config(args)
    call_service(server, token, 'switch', args.action, {"entity_id": args.entity_id})


def cmd_light(args):
    server, token = get_config(args)
    data = {"entity_id": args.entity_id}
    if args.action == 'turn_on':
        if args.brightness is not None:
            data["brightness_pct"] = args.brightness
        if args.rgb:
            data["rgb_color"] = [int(x) for x in args.rgb.split(',')]
        if args.color_temp is not None:
            data["color_temp"] = args.color_temp
    call_service(server, token, 'light', args.action, data)


def cmd_scene(args):
    server, token = get_config(args)
    call_service(server, token, 'scene', 'turn_on', {"entity_id": args.entity_id})


def cmd_script(args):
    server, token = get_config(args)
    if args.action == 'list':
        states = api_request(server, token, "/api/states")
        for entity in sorted(states, key=lambda e: e['entity_id']):
            if entity['entity_id'].startswith('script.'):
                print(f"{entity['entity_id']}: {entity['state']}")
    elif args.action == 'run':
        if args.variables:
            script_name = args.entity_id.replace('script.', '')
            data = {"variables": json.loads(args.variables)}
            call_service(server, token, 'script', script_name, data)
        else:
            call_service(server, token, 'script', 'turn_on', {"entity_id": args.entity_id})


def cmd_automation(args):
    server, token = get_config(args)
    if args.action == 'list':
        states = api_request(server, token, "/api/states")
        for entity in sorted(states, key=lambda e: e['entity_id']):
            if entity['entity_id'].startswith('automation.'):
                print(f"{entity['entity_id']}: {entity['state']}")
    elif args.action == 'trigger':
        call_service(server, token, 'automation', 'trigger', {"entity_id": args.entity_id})
    elif args.action == 'enable':
        call_service(server, token, 'automation', 'turn_on', {"entity_id": args.entity_id})
    elif args.action == 'disable':
        call_service(server, token, 'automation', 'turn_off', {"entity_id": args.entity_id})


def cmd_climate(args):
    server, token = get_config(args)
    if args.action == 'state':
        result = api_request(server, token, f"/api/states/{args.entity_id}")
        attrs = result.get('attributes', {})
        print_json({
            "state": result['state'],
            "current_temp": attrs.get('current_temperature'),
            "target_temp": attrs.get('temperature'),
        })
    elif args.action == 'set_temp':
        call_service(server, token, 'climate', 'set_temperature',
                     {"entity_id": args.entity_id, "temperature": args.temperature})
    elif args.action == 'set_mode':
        call_service(server, token, 'climate', 'set_hvac_mode',
                     {"entity_id": args.entity_id, "hvac_mode": args.mode})


def cmd_cover(args):
    server, token = get_config(args)
    if args.action == 'open':
        call_service(server, token, 'cover', 'open_cover', {"entity_id": args.entity_id})
    elif args.action == 'close':
        call_service(server, token, 'cover', 'close_cover', {"entity_id": args.entity_id})
    elif args.action == 'set_position':
        call_service(server, token, 'cover', 'set_cover_position',
                     {"entity_id": args.entity_id, "position": args.position})


def cmd_lock(args):
    server, token = get_config(args)
    call_service(server, token, 'lock', args.action, {"entity_id": args.entity_id})


def cmd_fan(args):
    server, token = get_config(args)
    data = {"entity_id": args.entity_id}
    if args.action == 'turn_on' and args.percentage is not None:
        data["percentage"] = args.percentage
    call_service(server, token, 'fan', args.action, data)


def cmd_media(args):
    server, token = get_config(args)
    if args.action == 'play_pause':
        call_service(server, token, 'media_player', 'media_play_pause',
                     {"entity_id": args.entity_id})
    elif args.action == 'volume':
        call_service(server, token, 'media_player', 'volume_set',
                     {"entity_id": args.entity_id, "volume_level": args.level})


def cmd_vacuum(args):
    server, token = get_config(args)
    if args.action == 'start':
        call_service(server, token, 'vacuum', 'start', {"entity_id": args.entity_id})
    elif args.action == 'dock':
        call_service(server, token, 'vacuum', 'return_to_base', {"entity_id": args.entity_id})


def cmd_alarm(args):
    server, token = get_config(args)
    data = {"entity_id": args.entity_id}
    if args.action == 'arm_home':
        call_service(server, token, 'alarm_control_panel', 'alarm_arm_home', data)
    elif args.action == 'disarm':
        if args.code:
            data["code"] = args.code
        call_service(server, token, 'alarm_control_panel', 'alarm_disarm', data)


def cmd_notify(args):
    server, token = get_config(args)
    if args.action == 'list':
        services = api_request(server, token, "/api/services")
        for svc in services:
            if svc.get('domain') == 'notify':
                for name in sorted(svc.get('services', {}).keys()):
                    print(f"notify.{name}")
    elif args.action == 'send':
        data = {"message": args.message}
        if args.title:
            data["title"] = args.title
        call_service(server, token, 'notify', args.service, data)


def cmd_presence(args):
    server, token = get_config(args)
    states = api_request(server, token, "/api/states")
    if args.trackers:
        for entity in sorted(states, key=lambda e: e['entity_id']):
            if entity['entity_id'].startswith('device_tracker.'):
                print(f"{entity['entity_id']}: {entity['state']}")
    else:
        for entity in sorted(states, key=lambda e: e['entity_id']):
            if entity['entity_id'].startswith('person.'):
                name = entity.get('attributes', {}).get('friendly_name', entity['entity_id'])
                print(f"{name}: {entity['state']}")


def cmd_weather(args):
    server, token = get_config(args)
    entity_id = args.entity_id or 'weather.home'
    if args.forecast:
        result = api_request(server, token, "/api/services/weather/get_forecasts",
                             method='POST',
                             data={"entity_id": entity_id, "type": args.forecast})
        print_json(result)
    else:
        result = api_request(server, token, f"/api/states/{entity_id}")
        attrs = result.get('attributes', {})
        print_json({
            "state": result['state'],
            "temperature": attrs.get('temperature'),
            "humidity": attrs.get('humidity'),
            "wind_speed": attrs.get('wind_speed'),
        })


def cmd_input(args):
    server, token = get_config(args)
    domain_service_map = {
        'boolean': ('input_boolean', 'toggle', None),
        'number': ('input_number', 'set_value', 'value'),
        'select': ('input_select', 'select_option', 'option'),
        'text': ('input_text', 'set_value', 'value'),
        'datetime': ('input_datetime', 'set_datetime', 'time'),
    }
    domain, service, value_key = domain_service_map[args.type]
    data = {"entity_id": args.entity_id}
    if value_key and args.value:
        try:
            data[value_key] = json.loads(args.value)
        except (json.JSONDecodeError, TypeError):
            data[value_key] = args.value
    call_service(server, token, domain, service, data)


def cmd_calendar(args):
    server, token = get_config(args)
    if args.action == 'list':
        result = api_request(server, token, "/api/calendars")
        for cal in result:
            print(cal['entity_id'])
    elif args.action == 'events':
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        days = args.days or 7
        end = now + timedelta(days=days)
        start_str = now.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        end_str = end.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        result = api_request(server, token,
                             f"/api/calendars/{args.entity_id}?start={start_str}&end={end_str}")
        print_json(result)


def cmd_tts(args):
    server, token = get_config(args)
    call_service(server, token, 'tts', 'speak', {
        "entity_id": args.tts_entity,
        "media_player_entity_id": args.media_player,
        "message": args.message,
    })


def cmd_services(args):
    server, token = get_config(args)
    result = api_request(server, token, "/api/services")
    for svc in sorted(result, key=lambda s: s.get('domain', '')):
        domain = svc.get('domain', '')
        if args.domain and domain != args.domain:
            continue
        for name in sorted(svc.get('services', {}).keys()):
            print(f"{domain}.{name}")


def cmd_service(args):
    server, token = get_config(args)
    data = json.loads(args.data) if args.data else {}
    call_service(server, token, args.domain, args.service, data)


def cmd_template(args):
    server, token = get_config(args)
    result = api_request(server, token, "/api/template", method='POST',
                         data={"template": args.template})
    print(result)


def cmd_history(args):
    server, token = get_config(args)
    path = "/api/history/period"
    if args.start:
        path += f"/{args.start}"
    path += f"?filter_entity_id={args.entity_id}"
    if args.end:
        path += f"&end_time={args.end}"
    result = api_request(server, token, path)
    if result and len(result) > 0:
        entries = [{"state": e['state'], "last_changed": e['last_changed']} for e in result[0]]
        print_json(entries)
    else:
        print("No history data found.")


def cmd_logbook(args):
    server, token = get_config(args)
    path = "/api/logbook"
    if args.entity:
        path += f"?entity={args.entity}"
    result = api_request(server, token, path)
    limit = args.limit or 10
    for entry in result[:limit]:
        name = entry.get('name', '')
        message = entry.get('message', '')
        when = entry.get('when', '')
        print(f"{when} - {name}: {message}")


def cmd_dashboard(args):
    server, token = get_config(args)
    states = api_request(server, token, "/api/states")

    sections = {
        'Lights ON': lambda e: e['entity_id'].startswith('light.') and e['state'] == 'on',
        'Open Doors/Windows': lambda e: (
            e['entity_id'].startswith('binary_sensor.')
            and e['state'] == 'on'
            and e.get('attributes', {}).get('device_class') in ('door', 'window')
        ),
        'Temperature Sensors': lambda e: (
            e['entity_id'].startswith('sensor.')
            and e.get('attributes', {}).get('device_class') == 'temperature'
        ),
        'Climate': lambda e: e['entity_id'].startswith('climate.'),
        'Locks': lambda e: e['entity_id'].startswith('lock.'),
        'Presence': lambda e: e['entity_id'].startswith('person.'),
    }

    for title, filter_fn in sections.items():
        matches = [e for e in states if filter_fn(e)]
        if matches:
            print(f"\n--- {title} ---")
            for e in sorted(matches, key=lambda x: x['entity_id']):
                name = e.get('attributes', {}).get('friendly_name', e['entity_id'])
                if title == 'Temperature Sensors':
                    unit = e.get('attributes', {}).get('unit_of_measurement', '')
                    print(f"  {name}: {e['state']}{unit}")
                elif title == 'Climate':
                    attrs = e.get('attributes', {})
                    cur = attrs.get('current_temperature', '?')
                    tgt = attrs.get('temperature', '?')
                    print(f"  {name}: {e['state']}, current: {cur}°, target: {tgt}°")
                else:
                    print(f"  {name}: {e['state']}")


def cmd_tesla(args):
    server, token = get_config(args)
    if args.action == 'battery':
        result = api_request(server, token, "/api/states/sensor.mao_dou_battery")
        print(f"Battery: {result['state']}%")
    elif args.action == 'location':
        result = api_request(server, token,
                             "/api/states/device_tracker.mao_dou_location_tracker")
        attrs = result.get('attributes', {})
        print_json({
            "entity_id": result['entity_id'],
            "state": result['state'],
            "latitude": attrs.get('latitude'),
            "longitude": attrs.get('longitude'),
            "heading": attrs.get('heading'),
            "speed": attrs.get('speed'),
        })
    elif args.action == 'destination':
        result = api_request(server, token,
                             "/api/states/device_tracker.mao_dou_destination_location_tracker")
        attrs = result.get('attributes', {})
        print_json({
            "entity_id": result['entity_id'],
            "state": result['state'],
            "latitude": attrs.get('latitude'),
            "longitude": attrs.get('longitude'),
        })
    elif args.action == 'automations':
        states = api_request(server, token, "/api/states")
        for entity in sorted(states, key=lambda e: e['entity_id']):
            if 'tesla' in entity['entity_id'].lower():
                print(f"{entity['entity_id']}: {entity['state']}")


def build_parser():
    parser = argparse.ArgumentParser(
        description='Home Assistant CLI - Control smart home devices via REST API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--server', help='Home Assistant URL (or set HA_URL env var)')
    parser.add_argument('--token', help='Long-lived access token (or set HA_TOKEN env var)')

    sub = parser.add_subparsers(dest='command', help='Available commands')

    # check
    sub.add_parser('check', help='Check API connectivity')

    # entities
    p = sub.add_parser('entities', help='List entities')
    p.add_argument('--domain', '-d', help='Filter by domain (e.g. light, switch, sensor)')

    # state
    p = sub.add_parser('state', help='Get entity state')
    p.add_argument('entity_id', help='Entity ID (e.g. light.living_room)')

    # areas
    sub.add_parser('areas', help='List all areas')

    # area-entities
    p = sub.add_parser('area-entities', help='List entities in an area')
    p.add_argument('area', help='Area name')
    p.add_argument('--domain', '-d', help='Filter by domain')

    # area-of
    p = sub.add_parser('area-of', help='Find which area an entity belongs to')
    p.add_argument('entity_id', help='Entity ID')

    # floors
    sub.add_parser('floors', help='List all floors and their areas')

    # switch
    p = sub.add_parser('switch', help='Control switches')
    p.add_argument('action', choices=['turn_on', 'turn_off', 'toggle'])
    p.add_argument('entity_id', help='Switch entity ID')

    # light
    p = sub.add_parser('light', help='Control lights')
    p.add_argument('action', choices=['turn_on', 'turn_off'])
    p.add_argument('entity_id', help='Light entity ID')
    p.add_argument('--brightness', '-b', type=int, help='Brightness percentage (0-100)')
    p.add_argument('--rgb', help='RGB color as R,G,B (e.g. 255,150,50)')
    p.add_argument('--color-temp', type=int, help='Color temperature in mireds')

    # scene
    p = sub.add_parser('scene', help='Activate a scene')
    p.add_argument('entity_id', help='Scene entity ID')

    # script
    p = sub.add_parser('script', help='List or run scripts')
    p.add_argument('action', choices=['list', 'run'])
    p.add_argument('entity_id', nargs='?', help='Script entity ID (for run)')
    p.add_argument('--variables', '-v', help='Variables as JSON string')

    # automation
    p = sub.add_parser('automation', help='Manage automations')
    p.add_argument('action', choices=['list', 'trigger', 'enable', 'disable'])
    p.add_argument('entity_id', nargs='?', help='Automation entity ID')

    # climate
    p = sub.add_parser('climate', help='Control climate/thermostat')
    p.add_argument('action', choices=['state', 'set_temp', 'set_mode'])
    p.add_argument('entity_id', help='Climate entity ID')
    p.add_argument('--temperature', '-t', type=float, help='Target temperature')
    p.add_argument('--mode', '-m', help='HVAC mode (heat, cool, auto, off)')

    # cover
    p = sub.add_parser('cover', help='Control covers (blinds, garage doors)')
    p.add_argument('action', choices=['open', 'close', 'set_position'])
    p.add_argument('entity_id', help='Cover entity ID')
    p.add_argument('--position', '-p', type=int, help='Position (0=closed, 100=open)')

    # lock
    p = sub.add_parser('lock', help='Control locks')
    p.add_argument('action', choices=['lock', 'unlock'])
    p.add_argument('entity_id', help='Lock entity ID')

    # fan
    p = sub.add_parser('fan', help='Control fans')
    p.add_argument('action', choices=['turn_on', 'turn_off'])
    p.add_argument('entity_id', help='Fan entity ID')
    p.add_argument('--percentage', '-p', type=int, help='Fan speed percentage')

    # media
    p = sub.add_parser('media', help='Control media players')
    p.add_argument('action', choices=['play_pause', 'volume'])
    p.add_argument('entity_id', help='Media player entity ID')
    p.add_argument('--level', '-l', type=float, help='Volume level (0.0-1.0)')

    # vacuum
    p = sub.add_parser('vacuum', help='Control vacuum')
    p.add_argument('action', choices=['start', 'dock'])
    p.add_argument('entity_id', help='Vacuum entity ID')

    # alarm
    p = sub.add_parser('alarm', help='Control alarm panel')
    p.add_argument('action', choices=['arm_home', 'disarm'])
    p.add_argument('entity_id', help='Alarm panel entity ID')
    p.add_argument('--code', '-c', help='Alarm code (if required)')

    # notify
    p = sub.add_parser('notify', help='List targets or send notifications')
    p.add_argument('action', choices=['list', 'send'], help='list targets or send a message')
    p.add_argument('service', nargs='?', help='Notification service (e.g. mobile_app_phone, notify)')
    p.add_argument('message', nargs='?', help='Notification message')
    p.add_argument('--title', '-t', help='Notification title')

    # presence
    p = sub.add_parser('presence', help='Check who is home')
    p.add_argument('--trackers', action='store_true', help='Show device trackers instead')

    # weather
    p = sub.add_parser('weather', help='Get weather info')
    p.add_argument('--entity-id', '-e', help='Weather entity ID (default: weather.home)')
    p.add_argument('--forecast', '-f', choices=['daily', 'hourly'], help='Get forecast')

    # input
    p = sub.add_parser('input', help='Control input helpers')
    p.add_argument('type', choices=['boolean', 'number', 'select', 'text', 'datetime'])
    p.add_argument('entity_id', help='Input entity ID')
    p.add_argument('value', nargs='?', help='Value to set (not needed for boolean toggle)')

    # calendar
    p = sub.add_parser('calendar', help='Calendar operations')
    p.add_argument('action', choices=['list', 'events'])
    p.add_argument('entity_id', nargs='?', help='Calendar entity ID (for events)')
    p.add_argument('--days', '-d', type=int, help='Number of days ahead (default: 7)')

    # tts
    p = sub.add_parser('tts', help='Text-to-speech')
    p.add_argument('tts_entity', help='TTS entity ID (e.g. tts.google_en)')
    p.add_argument('media_player', help='Media player entity ID')
    p.add_argument('message', help='Message to speak')

    # services (list available services)
    p = sub.add_parser('services', help='List available services')
    p.add_argument('--domain', '-d', help='Filter by domain (e.g. light, notify)')

    # service (call a service)
    p = sub.add_parser('service', help='Call any service')
    p.add_argument('domain', help='Service domain')
    p.add_argument('service', help='Service name')
    p.add_argument('--data', '-d', help='Service data as JSON string')

    # template
    p = sub.add_parser('template', help='Evaluate a Jinja2 template')
    p.add_argument('template', help='Template string')

    # history
    p = sub.add_parser('history', help='Get entity state history')
    p.add_argument('entity_id', help='Entity ID')
    p.add_argument('--start', '-s', help='Start time (ISO 8601)')
    p.add_argument('--end', '-e', help='End time (ISO 8601)')

    # logbook
    p = sub.add_parser('logbook', help='View logbook entries')
    p.add_argument('--entity', '-e', help='Filter by entity ID')
    p.add_argument('--limit', '-l', type=int, help='Number of entries (default: 10)')

    # dashboard
    sub.add_parser('dashboard', help='Quick status overview of all active devices')

    # tesla
    p = sub.add_parser('tesla', help='Tesla vehicle controls')
    p.add_argument('action', choices=['battery', 'location', 'destination', 'automations'])

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        'check': cmd_check,
        'entities': cmd_entities,
        'state': cmd_state,
        'areas': cmd_areas,
        'area-entities': cmd_area_entities,
        'area-of': cmd_area_of,
        'floors': cmd_floors,
        'switch': cmd_switch,
        'light': cmd_light,
        'scene': cmd_scene,
        'script': cmd_script,
        'automation': cmd_automation,
        'climate': cmd_climate,
        'cover': cmd_cover,
        'lock': cmd_lock,
        'fan': cmd_fan,
        'media': cmd_media,
        'vacuum': cmd_vacuum,
        'alarm': cmd_alarm,
        'notify': cmd_notify,
        'presence': cmd_presence,
        'weather': cmd_weather,
        'input': cmd_input,
        'calendar': cmd_calendar,
        'tts': cmd_tts,
        'services': cmd_services,
        'service': cmd_service,
        'template': cmd_template,
        'history': cmd_history,
        'logbook': cmd_logbook,
        'dashboard': cmd_dashboard,
        'tesla': cmd_tesla,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
