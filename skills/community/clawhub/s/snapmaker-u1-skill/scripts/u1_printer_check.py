#!/usr/bin/env python3
"""Read a local U1 snapshot and optionally compare physical spools; never control it."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import http.client
import ipaddress
import json
import math
import os
from pathlib import Path
import re
from urllib.parse import quote
import zipfile

MAX_BYTES = 1024 * 1024
OBJECTS = ('print_stats', 'virtual_sdcard', 'heater_bed', 'extruder', 'extruder1',
           'extruder2', 'extruder3', 'filament_detect', 'print_task_config',
           *(f'filament_motion_sensor e{i}_filament' for i in range(4)))
ENDPOINTS = {'info': '/printer/info', 'objects': '/printer/objects/list', 'query': '/printer/objects/query'}


class CheckError(ValueError):
    pass


def validate_connection(host, port, timeout):
    try:
        address = ipaddress.ip_address(host)
    except (TypeError, ValueError) as exc:
        raise CheckError('host must be an explicit private or loopback IP address; no discovery or DNS') from exc
    local_networks = ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '169.254.0.0/16', 'fc00::/7', 'fe80::/10')
    if not (address.is_loopback or any(address in ipaddress.ip_network(net) for net in local_networks)):
        raise CheckError('host must be a private or loopback unicast IP address')
    if type(port) is not int or not 1 <= port <= 65535:
        raise CheckError('port must be between 1 and 65535')
    if type(timeout) not in (int, float) or not math.isfinite(timeout) or not 0 < timeout <= 10:
        raise CheckError('timeout must be finite, positive and at most 10 seconds per request')


def get_json(host, port, endpoint, *, objects=(), timeout=5, api_key=None):
    """Only three fixed GET routes, no redirects, proxies, uploads or arbitrary paths."""
    validate_connection(host, port, timeout)
    if endpoint not in ENDPOINTS or any(name not in OBJECTS for name in objects):
        raise CheckError('unsupported read-only query')
    if (endpoint == 'query') != bool(objects):
        raise CheckError('only object queries accept a nonempty object list')
    path = ENDPOINTS[endpoint]
    if objects:
        path += '?' + '&'.join(quote(name, safe='') for name in objects)
    if api_key is not None and (not isinstance(api_key, str) or not api_key.isascii() or any(ord(c) < 33 or ord(c) == 127 for c in api_key)):
        raise CheckError('invalid API key format')
    connection = http.client.HTTPConnection(str(host), port, timeout=timeout)
    try:
        connection.request('GET', path, headers={'Accept': 'application/json', **({'X-Api-Key': api_key} if api_key else {})})
        response = connection.getresponse()
        if response.status != 200:
            raise CheckError(f'printer returned HTTP {response.status}; redirects are not followed')
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise CheckError('printer response exceeds 1 MiB')
        payload = json.loads(body)
        if not isinstance(payload, dict) or 'error' in payload or not isinstance(payload.get('result'), dict):
            raise CheckError('printer returned an API error or invalid result')
        return payload['result']
    except (OSError, http.client.HTTPException, ValueError) as exc:
        if isinstance(exc, CheckError):
            raise
        # Do not echo response bodies, headers, credentials or arbitrary socket errors.
        raise CheckError('printer request failed or returned invalid JSON') from exc
    finally:
        connection.close()


def _text(value):
    return value.strip() if isinstance(value, str) and value.strip().upper() not in {'', 'NONE', 'UNKNOWN', '?'} else None


def _number(value):
    try:
        return value if type(value) in (int, float) and math.isfinite(value) else None
    except OverflowError:
        return None


def _color(value):
    if not isinstance(value, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}(?:FF|ff)?', value):
        raise CheckError('expected physical spool colors must be #RRGGBB (or opaque #RRGGBBFF)')
    return value[:7].upper()


def _item(values, index):
    return values[index] if isinstance(values, list) and index < len(values) else None


def _rgb(value):
    return f'#{value:06X}' if type(value) is int and 0 <= value <= 0xFFFFFF else None


def tag_metadata(entry):
    """Keep decoded tag fields separate from editable printer configuration."""
    if _text(entry.get('VENDOR')) is None:
        return None
    tag = {key: _text(entry.get(key)) for key in ('VENDOR', 'MANUFACTURER', 'MAIN_TYPE', 'SUB_TYPE')}
    for key in ('DIAMETER', 'WEIGHT', 'LENGTH', 'DRYING_TEMP', 'DRYING_TIME', 'HOTEND_MIN_TEMP',
                'HOTEND_MAX_TEMP', 'BED_TEMP', 'FIRST_LAYER_TEMP', 'OTHER_LAYER_TEMP', 'SKU'):
        value = _number(entry.get(key))
        tag[key] = value if value is not None and value > 0 else None
    count = entry.get('COLOR_NUMS')
    count = count if type(count) is int and 1 <= count <= 5 else None
    tag['COLOR_NUMS'] = count
    for i in range(1, 6):
        tag[f'RGB_{i}'] = _rgb(entry.get(f'RGB_{i}')) if i == 1 or (count is not None and i <= count) else None
    alpha = entry.get('ALPHA')
    tag['ALPHA'] = alpha if type(alpha) is int and 0 <= alpha <= 255 else None
    tag['OFFICIAL'] = entry.get('OFFICIAL') if type(entry.get('OFFICIAL')) is bool else None
    uid = entry.get('CARD_UID')
    tag['CARD_UID'] = uid if isinstance(uid, list) and 1 <= len(uid) <= 32 and all(type(v) is int and 0 <= v <= 255 for v in uid) and any(uid) else None
    return tag


def configured_filament(config, index):
    material = _text(_item(config.get('filament_type'), index))
    if material is None:
        return None
    rgba = _item(config.get('filament_color_rgba'), index)
    rgba = re.fullmatch(r'#?([0-9A-Fa-f]{8})', rgba) if isinstance(rgba, str) else None
    rgba = rgba[1].upper() if rgba else None
    official = _item(config.get('filament_official'), index)
    return {'source': 'printer_configuration', 'material': material.upper(),
            'vendor': _text(_item(config.get('filament_vendor'), index)),
            'sub_type': _text(_item(config.get('filament_sub_type'), index)),
            'color': '#' + rgba[:6] if rgba else None, 'alpha': int(rgba[6:], 16) if rgba else None,
            'official': official if type(official) is bool else None}


def load_expected(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise CheckError('expected slots must be a regular JSON file no larger than 1 MiB')
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or not data or set(data) - {'1', '2', '3', '4'}:
        raise CheckError('expected slots must be an object keyed by physical tools 1–4')
    expected = {}
    for tool, entry in data.items():
        if not isinstance(entry, dict) or not _text(entry.get('material')):
            raise CheckError('each expected slot needs material and color')
        expected[int(tool)] = {'material': entry['material'].strip().upper(), 'color': _color(entry.get('color'))}
    return expected


def project_expected(path, slot_map):
    """Read ordinary filament arrays; never infer physical slots from virtual colors."""
    path = Path(path)
    try:
        with zipfile.ZipFile(path) as archive:
            if 'Metadata/u1_target_colors.json' in archive.namelist():
                raise CheckError('target palette is not a physical spool list; use --expected-slots')
            member = archive.getinfo('Metadata/project_settings.config')
            if member.file_size > MAX_BYTES:
                raise CheckError('project settings exceed 1 MiB')
            settings = json.loads(archive.read(member))
    except (OSError, KeyError, zipfile.BadZipFile, ValueError, RuntimeError, NotImplementedError) as exc:
        if isinstance(exc, CheckError):
            raise
        raise CheckError('project must contain readable native Orca project settings') from exc
    if not isinstance(settings, dict):
        raise CheckError('project settings must be a JSON object')
    definitions = settings.get('mixed_filament_definitions', '')
    if not isinstance(definitions, str) or definitions:
        raise CheckError('Full Spectrum project: provide --expected-slots for physical spools; recipes and virtual colors are not inferred')
    arrays = [settings.get(key) for key in ('filament_settings_id', 'filament_type', 'filament_colour')]
    if any(not isinstance(values, list) for values in arrays) or not 1 <= len(arrays[0]) <= 4 or any(len(v) != len(arrays[0]) for v in arrays):
        raise CheckError('project needs 1–4 ordinary filaments with complete matching arrays; otherwise use --expected-slots')
    try:
        pairs = [tuple(map(int, pair.split(':'))) for pair in slot_map.split(',')]
        if any(len(pair) != 2 for pair in pairs):
            raise ValueError
        mapping = dict(pairs)
        if len(mapping) != len(pairs) or set(mapping) != set(range(1, len(arrays[0]) + 1)) or len(set(mapping.values())) != len(mapping) or any(t not in range(1, 5) for t in mapping.values()):
            raise ValueError
    except (AttributeError, ValueError) as exc:
        raise CheckError('supply a complete distinct project-filament:physical-tool --slot-map, e.g. 1:2,2:1') from exc
    expected = {}
    for source, tool in mapping.items():
        if not _text(arrays[0][source - 1]) or not _text(arrays[1][source - 1]):
            raise CheckError('project filament identity/material is missing')
        expected[tool] = {'material': arrays[1][source - 1].strip().upper(), 'color': _color(arrays[2][source - 1])}
    return expected


def collect_snapshot(host, port=80, *, timeout=5, api_key=None):
    info = get_json(host, port, 'info', timeout=timeout, api_key=api_key)
    available = get_json(host, port, 'objects', timeout=timeout, api_key=api_key).get('objects')
    if not isinstance(available, list) or not all(isinstance(name, str) for name in available):
        raise CheckError('printer returned an invalid object list')
    selected = tuple(name for name in OBJECTS if name in available)
    status = get_json(host, port, 'query', objects=selected, timeout=timeout, api_key=api_key).get('status') if selected else {}
    if not isinstance(status, dict) or any(not isinstance(value, dict) for value in status.values()):
        raise CheckError('printer returned invalid object status')
    slots = []
    metadata = status.get('filament_detect', {}).get('info', [])
    config = status.get('print_task_config', {})
    if not isinstance(metadata, list):
        metadata = []
    for index in range(4):
        entry = metadata[index] if index < len(metadata) and isinstance(metadata[index], dict) else {}
        sensor = status.get(f'filament_motion_sensor e{index}_filament', {})
        has_metadata = _text(entry.get('VENDOR')) is not None
        rgb = entry.get('RGB_1') if has_metadata else None
        material = _text(entry.get('MAIN_TYPE')) if has_metadata else None
        configured = configured_filament(config, index)
        identity = {'material': material.upper() if material else None, 'color': _rgb(rgb)}
        conflicts = [key for key, value in identity.items() if configured and value is not None and configured[key] is not None and value != configured[key]]
        slots.append({'tool': index + 1, 'sensor_enabled': sensor.get('enabled') if type(sensor.get('enabled')) is bool else None,
                      'filament_detected': sensor.get('filament_detected') if type(sensor.get('filament_detected')) is bool else None,
                      'metadata_available': has_metadata, **identity,
                      'metadata_source': 'filament_detect' if has_metadata else 'unknown',
                      'manufacturer': _text(entry.get('MANUFACTURER')) if has_metadata else None,
                      'tag_metadata': tag_metadata(entry), 'configured_filament': configured, 'metadata_conflicts': conflicts})
    print_state = _text(status.get('print_stats', {}).get('state'))
    printer_state = _text(info.get('state'))
    progress = _number(status.get('virtual_sdcard', {}).get('progress'))
    duration = _number(status.get('print_stats', {}).get('print_duration'))
    mapping = config.get('extruder_map_table')
    mapping = [v + 1 if type(v) is int and 0 <= v <= 3 else None for v in mapping] if isinstance(mapping, list) and 1 <= len(mapping) <= 32 else None
    return {'captured_at_utc': datetime.now(timezone.utc).isoformat(), 'printer_state': printer_state,
            'print_state': print_state, 'idle': printer_state == 'ready' and print_state in {'standby', 'complete', 'cancelled'},
            'progress_percent': progress * 100 if progress is not None and 0 <= progress <= 1 else None,
            'print_duration_seconds': duration if duration is not None and duration >= 0 else None,
            'temperatures_c': {name: {key: _number(status.get(name, {}).get(key)) for key in ('temperature', 'target')}
                               for name in ('heater_bed', 'extruder', 'extruder1', 'extruder2', 'extruder3')},
            'slots': slots, 'logical_to_physical_tools': mapping,
            'tool_map_scope': 'One-based physical tools for the printer current task, not a mapping for a new project.',
            'unavailable_objects': [name for name in OBJECTS if name not in status]}


def compare_slots(snapshot, expected):
    rows = []
    for tool, wanted in sorted(expected.items()):
        actual = snapshot['slots'][tool - 1]
        presence = actual['filament_detected'] if actual['sensor_enabled'] is True else None
        checks = {'presence': 'unknown' if presence is None else 'match' if presence else 'mismatch'}
        for key in ('material', 'color'):
            checks[key] = 'unknown' if actual[key] is None else 'match' if actual[key] == wanted[key] else 'mismatch'
        if actual.get('metadata_conflicts'):
            checks['metadata_consistency'] = 'mismatch'
        rows.append({'tool': tool, 'expected': wanted, 'reported': actual, 'checks': checks})
    return {'scope': 'Known idle state, explicit physical slots, presence and printer-reported material/RGB metadata only; no calibration, pigmentation or remaining-weight verification.',
            'slots': rows, 'passed': bool(rows) and snapshot['idle'] and all(value == 'match' for row in rows for value in row['checks'].values())}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', required=True, help='Explicit private/loopback IP address; no network discovery')
    parser.add_argument('--port', type=int, default=80)
    parser.add_argument('--timeout', type=float, default=5, help='Per-request seconds, maximum 10; at most three GETs')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--project', type=Path, help='Native Orca 3MF with 1–4 ordinary filaments')
    group.add_argument('--expected-slots', type=Path, help='Physical-spool JSON keyed by tools 1–4, including for Full Spectrum')
    parser.add_argument('--slot-map', help='Required with --project: explicit one-based filament:physical-tool pairs')
    parser.add_argument('--output', type=Path, help='Optional fresh JSON file; never overwrite existing files')
    args = parser.parse_args(argv)
    report = {'schema_version': 1, 'read_only': True, 'ready_to_print': False, 'snapshot_completed': False, 'preflight_passed': None}
    try:
        validate_connection(args.host, args.port, args.timeout)
        report['target'] = {'host': args.host, 'port': args.port}
        if bool(args.project) != bool(args.slot_map):
            raise CheckError('--project and --slot-map must be supplied together')
        if args.output and os.path.lexists(args.output):
            raise CheckError('output must be a fresh file')
        if args.output and not args.output.parent.is_dir():
            raise CheckError('output parent directory must already exist')
        expected = project_expected(args.project, args.slot_map) if args.project else load_expected(args.expected_slots) if args.expected_slots else None
        if args.project or args.expected_slots:
            source = args.project or args.expected_slots
            report['expectations_source'] = {'kind': 'orca_project' if args.project else 'physical_slots', 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
        snapshot = collect_snapshot(args.host, args.port, timeout=args.timeout, api_key=os.environ.get('SNAPMAKER_API_KEY') or None)
        report.update(snapshot_completed=True, snapshot=snapshot, status='snapshot_only')
        if expected:
            report['comparison'] = compare_slots(snapshot, expected)
            report['preflight_passed'] = report['comparison']['passed']
            report['status'] = 'checks_passed_review_required' if report['preflight_passed'] else 'review_required'
        code = 1 if report['preflight_passed'] is False else 0
    except (OSError, ValueError) as exc:
        report.update(status='check_failed', error=str(exc))
        code = 2
    serialized = json.dumps(report, indent=2, allow_nan=False) + '\n'
    if args.output:
        try:
            with args.output.open('x') as stream:
                stream.write(serialized)
        except OSError:
            print(json.dumps({'status': 'check_failed', 'error': 'cannot create fresh output file', 'read_only': True, 'ready_to_print': False}))
            return 2
    print(serialized, end='')
    return code


if __name__ == '__main__':
    raise SystemExit(main())
